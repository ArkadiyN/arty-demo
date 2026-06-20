import os
import sys
import io
import re
import base64
import argparse
import fitz  # PyMuPDF
import anthropic
from PIL import Image, ImageDraw
from settings import Settings

_DEFAULT_ANTHROPIC_MODEL = "claude-haiku-4-5"
# Anthropic SDK strips the leading "/" from paths and appends to base_url.path,
# so "https://openrouter.ai/api" + "v1/messages" → "/api/v1/messages" (correct).
_OPENROUTER_BASE_URL = "https://openrouter.ai/api"

_MATH_FONTS = frozenset({"symbol", "cmsy", "cmex", "cmmi", "mtex", "mathtime", "euclid"})
# Greek letters + Mathematical Operators + Misc Math + Supplemental Math
_MATH_RANGES = [(0x0391, 0x03C9), (0x2200, 0x22FF), (0x27C0, 0x27EF), (0x2A00, 0x2AFF)]

_FORMULA_PROMPT = (
    "If this image contains a mathematical equation, graph formula, or coordinate matrix, "
    "transcribe it completely into valid LaTeX display math format using $$ encapsulation. "
    "If it is a pure layout schematic or photo with no explicit equations, reply with: [DIAGRAM]"
)

# Used by the Anthropic per-page path.
_PAGE_VISION_PROMPT = """\
Extract the content of this scanned document page as clean Markdown.

Rules:
- Reproduce all text faithfully.
- Render every mathematical expression in LaTeX:
    Display equations (on their own line):  $$...$$  (equation number if present)
    Inline math within sentences:  $...$
- Use # / ## / ### for section headings based on visual prominence.
- If this page contains a graph, plot, diagram, or experimental photograph
  (NOT a decorative seal/emblem/logo, NOT an administrative form or table):
    Insert the exact token [FIGURE] at the location where the illustration appears.
    Append the line [HAS_FIGURE] at the very end of your response.
- If the page is purely text, tables, or administrative content, omit both tokens.

Output Markdown only — no preamble, no commentary."""

# Used by the Google combined-image path.
_DOC_VISION_PROMPT = """\
This image shows {n} scanned document pages stacked vertically.
Each page is preceded by a blue horizontal bar labeled "PAGE N".

For each page output exactly:
=== PAGE N ===
[page content]

Rules:
- Reproduce all text faithfully.
- Render math in LaTeX: display equations as $$...$$ and inline as $...$.
- Use # / ## / ### for headings based on visual prominence.
- If a page contains a graph, plot, diagram, or experimental photograph
  (NOT a decorative seal/emblem/logo, NOT an administrative form or table):
    Insert [FIGURE] at the location where the illustration appears.
    Append [HAS_FIGURE] at the very end of that page's section.
- Output all {n} pages in order, even if a page is blank (output the header then a blank line).

Output only the page sections — no preamble, no commentary."""

# PyMuPDF ext → MIME type (covers the common cases it returns)
_MIME = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
}


# ---------------------------------------------------------------------------
# Heuristic helpers (no API)
# ---------------------------------------------------------------------------

def _is_math_char(c):
    cp = ord(c)
    return any(lo <= cp <= hi for lo, hi in _MATH_RANGES)


def _block_is_formula(block):
    spans = [s for line in block.get("lines", []) for s in line.get("spans", [])]
    if not spans:
        return False
    if any(mf in s["font"].lower() for s in spans for mf in _MATH_FONTS):
        return True
    text = "".join(s["text"] for s in spans)
    return bool(text.strip()) and sum(_is_math_char(c) for c in text) / len(text) > 0.15


def _block_to_markdown(block):
    lines = block.get("lines", [])
    if not lines:
        return ""

    first_spans = lines[0].get("spans", [])
    font_size = first_spans[0]["size"] if first_spans else 0
    is_bold = bool(first_spans and first_spans[0].get("flags", 0) & 16)

    parts = []
    for line in lines:
        line_text = "".join(s["text"] for s in line.get("spans", [])).strip()
        if line_text:
            parts.append(line_text)
    text = " ".join(parts)

    if font_size >= 16:
        return f"# {text}"
    if font_size >= 13:
        return f"## {text}"
    if font_size >= 11 and is_bold:
        return f"### {text}"
    return text


# ---------------------------------------------------------------------------
# Client factories — Google first, Anthropic/OpenRouter as fallback
# ---------------------------------------------------------------------------

def _try_get_google_client():
    """Return (client, model) if GOOGLE_API_KEY is configured, else None.

    A request timeout is required here: without one, an SDK call that stalls
    server-side (e.g. a slow multimodal response) blocks forever instead of
    raising, since the underlying httpx client has no default deadline.
    """
    from google import genai  # deferred so the package is optional at import time
    from google.genai import types
    s = Settings()
    if not s.google_api_key:
        return None
    client = genai.Client(
        api_key=s.google_api_key,
        http_options=types.HttpOptions(timeout=s.google_timeout_ms),
    )
    return client, s.google_model


def _get_anthropic_client():
    """Return (client, model). Priority: ANTHROPIC_API_KEY → OPENROUTER_API_KEY.

    OAuth tokens (sk-ant-oat01-*) are rejected by api.anthropic.com and are
    never attempted here.
    """
    s = Settings()
    if s.anthropic_api_key:
        return anthropic.Anthropic(api_key=s.anthropic_api_key), _DEFAULT_ANTHROPIC_MODEL

    if s.openrouter_api_key:
        return (
            anthropic.Anthropic(
                api_key=s.openrouter_api_key,
                base_url=_OPENROUTER_BASE_URL,
            ),
            s.openrouter_model,
        )

    raise SystemExit(
        "Error: No AI credentials found. Set GOOGLE_API_KEY, ANTHROPIC_API_KEY, "
        "or OPENROUTER_API_KEY in .env"
    )


# ---------------------------------------------------------------------------
# Page / image utilities
# ---------------------------------------------------------------------------

def _assert_not_scanned(doc):
    """Raise if the PDF has no text layer (scanned image-only document)."""
    scanned = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        if bool(page.get_text().strip()):
            continue
        page_area = page.rect.width * page.rect.height
        for img_info in page.get_images(full=True):
            for rect in page.get_image_rects(img_info[0]):
                if (rect.width * rect.height) / page_area > 0.5:
                    scanned += 1
                    break
    if scanned / len(doc) > 0.3:
        raise SystemExit(
            f"Error: PDF appears to be scanned ({scanned}/{len(doc)} pages have no text "
            "layer). Run OCR before processing."
        )


def _page_is_image_based(page):
    """True when the page stores its content as a full-page embedded image."""
    page_area = page.rect.width * page.rect.height
    for img_info in page.get_images(full=True):
        for rect in page.get_image_rects(img_info[0]):
            if (rect.width * rect.height) / page_area > 0.5:
                return True
    return False


def _render_page_jpeg(page, dpi=150):
    """Render a page to JPEG bytes at the given DPI."""
    return page.get_pixmap(dpi=dpi).tobytes("jpeg")


def _get_fullpage_image(page):
    """Return (bytes, ext) for the embedded full-page image, or render as fallback."""
    page_area = page.rect.width * page.rect.height
    doc = page.parent
    for img_info in page.get_images(full=True):
        xref = img_info[0]
        for rect in page.get_image_rects(xref):
            if (rect.width * rect.height) / page_area > 0.5:
                base = doc.extract_image(xref)
                return base["image"], base["ext"]
    return _render_page_jpeg(page), "jpeg"


# ---------------------------------------------------------------------------
# Google combined-image vision
# ---------------------------------------------------------------------------

def _render_pages_combined(pages, dpi=60):
    """Render a list of fitz pages into one tall JPEG with blue PAGE N separator bars.

    Returns JPEG bytes. The separator bars are 30 px tall and labeled "PAGE N"
    so the vision model can identify page boundaries.
    """
    SEP_H = 30
    SEP_COLOR = (30, 80, 200)
    TEXT_COLOR = (255, 255, 255)

    rendered = []
    for page in pages:
        pm = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
        rendered.append(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))

    if not rendered:
        return b""

    width = max(img.width for img in rendered)
    total_h = sum(img.height for img in rendered) + SEP_H * len(rendered)

    combined = Image.new("RGB", (width, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(combined)

    y = 0
    for i, img in enumerate(rendered):
        draw.rectangle([0, y, width - 1, y + SEP_H - 1], fill=SEP_COLOR)
        draw.text((10, y + 8), f"PAGE {i + 1}", fill=TEXT_COLOR)
        y += SEP_H
        combined.paste(img, (0, y))
        y += img.height

    buf = io.BytesIO()
    combined.save(buf, "JPEG", quality=70)
    return buf.getvalue()


def _parse_page_vision_response(text, n_pages):
    """Split a combined-page vision response into per-page (markdown, has_figure) tuples.

    Expects sections delimited by '=== PAGE N ===' (1-indexed).
    Returns a list of length n_pages; pages with no matching section get ("", False).
    """
    results = [("", False)] * n_pages
    pattern = re.compile(r"=== PAGE (\d+) ===\s*(.*?)(?==== PAGE \d+ ===|\Z)", re.DOTALL)
    for m in pattern.finditer(text):
        idx = int(m.group(1)) - 1  # 0-based
        if 0 <= idx < n_pages:
            content = m.group(2).strip()
            has_fig = "[HAS_FIGURE]" in content
            md = content.replace("[HAS_FIGURE]", "").strip()
            if not has_fig:
                md = md.replace("[FIGURE]", "")
            results[idx] = (md, has_fig)
    return results


def _extract_doc_via_vision_google(pages, client, model):
    """Send all pages as one combined image to Google; return per-page (md, has_figure).

    pages: ordered list of fitz.Page objects (the image-based pages only).
    The combined image is labeled PAGE 1..N so the response maps back positionally.
    """
    from google.genai import types

    n = len(pages)
    combined_bytes = _render_pages_combined(pages)
    prompt = _DOC_VISION_PROMPT.format(n=n)

    print(f"  Sending {n} pages as combined image to Google ({model})...")
    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=combined_bytes, mime_type="image/jpeg"),
            prompt,
        ],
    )
    return _parse_page_vision_response(response.text, n)


# ---------------------------------------------------------------------------
# Anthropic per-page vision (fallback)
# ---------------------------------------------------------------------------

def _extract_page_via_vision(page, client, model):
    """Ask Claude to extract text+LaTeX from a single page image.

    Returns (markdown_text, has_figure).
    """
    image_b64 = base64.standard_b64encode(_render_page_jpeg(page)).decode()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_b64,
                    },
                },
                {"type": "text", "text": _PAGE_VISION_PROMPT},
            ],
        }],
    )
    content = next((b.text for b in response.content if hasattr(b, "text")), None)
    if content is None:
        import httpx
        raise anthropic.APIError(
            "Vision model returned no text block (model may not support image input)",
            request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
            body=None,
        )
    has_figure = "[HAS_FIGURE]" in content
    markdown = content.replace("[HAS_FIGURE]", "").strip()
    if not has_figure:
        markdown = markdown.replace("[FIGURE]", "")
    return markdown, has_figure


def _analyze_image_for_formula(image_bytes, image_ext, client, model=_DEFAULT_ANTHROPIC_MODEL):
    """Return LaTeX string if image contains a formula, None if it's a diagram/photo."""
    media_type = _MIME.get(image_ext.lower(), f"image/{image_ext.lower()}")
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": _FORMULA_PROMPT},
            ],
        }],
    )
    transcription = next((b.text for b in response.content if hasattr(b, "text")), "")
    return None if "[DIAGRAM]" in transcription else transcription


# ---------------------------------------------------------------------------
# Image extraction helpers (heuristic path)
# ---------------------------------------------------------------------------

def _extract_all_images(doc, images_dir, equations_dir=None, client=None,
                        skip_page_backgrounds=True):
    """Extract unique non-background images; return xref→filename map and count."""
    os.makedirs(images_dir, exist_ok=True)
    if client and equations_dir:
        os.makedirs(equations_dir, exist_ok=True)

    xref_to_name = {}
    counter = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_area = page.rect.width * page.rect.height

        for img_info in page.get_images(full=True):
            xref = img_info[0]
            if xref in xref_to_name:
                continue

            if skip_page_backgrounds:
                is_background = any(
                    (rect.width * rect.height) / page_area > 0.5
                    for rect in page.get_image_rects(xref)
                )
                if is_background:
                    continue

            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            counter += 1
            name = f"fig{counter}.{image_ext}"
            with open(os.path.join(images_dir, name), "wb") as f:
                f.write(image_bytes)
            xref_to_name[xref] = name
            print(f"  Saved: images/{name}")

            if client and equations_dir:
                print(f"  Analyzing fig{counter} for mathematical formulas...")
                try:
                    latex = _analyze_image_for_formula(image_bytes, image_ext, client)
                    if latex:
                        eq_name = f"equation_fig{counter}.tex"
                        with open(os.path.join(equations_dir, eq_name), "w", encoding="utf-8") as f:
                            f.write(latex)
                        print(f"  -> LaTeX formula saved to: equations/{eq_name}")
                except anthropic.APIError as e:
                    print(f"  -> Vision analysis skipped for fig{counter}: {e}")

    return xref_to_name, counter


def _build_bbox_to_name(page, xref_to_name):
    """Map image bounding boxes on this page to their saved filenames."""
    bbox_to_name = {}
    for img_info in page.get_images(full=True):
        xref = img_info[0]
        name = xref_to_name.get(xref)
        if name:
            for rect in page.get_image_rects(xref):
                bbox_to_name[tuple(rect)] = name
    return bbox_to_name


def _page_to_markdown_heuristic(page, bbox_to_name):
    """Extract page content using font/Unicode heuristics (no API calls)."""
    page_dict = page.get_text("dict", sort=True)
    parts = []
    for block in page_dict["blocks"]:
        if block["type"] == 1:  # image block
            name = bbox_to_name.get(tuple(block["bbox"]))
            if name:
                parts.append(f"![{name}](images/{name})")
        elif block["type"] == 0:  # text block
            text = _block_to_markdown(block)
            if not text:
                continue
            if _block_is_formula(block):
                parts.append(f"$$\n{text}\n$$")
            else:
                parts.append(text)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_pdf_images(pdf_path, output_dir="output", analyze_formulas=False):
    doc = fitz.open(pdf_path)
    images_dir = os.path.join(output_dir, "images")
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")
    _assert_not_scanned(doc)

    if analyze_formulas:
        os.makedirs(images_dir, exist_ok=True)
        fig_counter = 0

        google = _try_get_google_client()
        if google:
            g_client, g_model = google
            image_pages = [(i, doc[i]) for i in range(len(doc)) if _page_is_image_based(doc[i])]
            if image_pages:
                try:
                    results = _extract_doc_via_vision_google(
                        [p for _, p in image_pages], g_client, g_model
                    )
                    for j, (page_idx, page) in enumerate(image_pages):
                        _, has_figure = results[j]
                        if has_figure:
                            fig_counter += 1
                            img_bytes, img_ext = _get_fullpage_image(page)
                            name = f"fig{fig_counter}.{img_ext}"
                            with open(os.path.join(images_dir, name), "wb") as f:
                                f.write(img_bytes)
                            print(f"  Page {page_idx + 1}: figure saved as images/{name}")
                except Exception as e:
                    print(f"  Google vision failed ({e}), falling back to Anthropic")
                    google = None

        if not google:
            a_client, a_model = _get_anthropic_client()
            for page_num in range(len(doc)):
                page = doc[page_num]
                if _page_is_image_based(page):
                    print(f"  Page {page_num + 1}/{len(doc)}: checking for figure...")
                    try:
                        _, has_figure = _extract_page_via_vision(page, a_client, a_model)
                        if has_figure:
                            fig_counter += 1
                            img_bytes, img_ext = _get_fullpage_image(page)
                            name = f"fig{fig_counter}.{img_ext}"
                            with open(os.path.join(images_dir, name), "wb") as f:
                                f.write(img_bytes)
                            print(f"    -> Saved: images/{name}")
                    except anthropic.APIError as e:
                        print(f"  Page {page_num + 1}: vision failed: {e}")
        count = fig_counter
    else:
        _, count = _extract_all_images(doc, images_dir)

    print(f"\nDone. Extracted {count} figures to {images_dir}")
    return count


def generate_markdown(pdf_path, output_dir="output", analyze_formulas=False):
    doc = fitz.open(pdf_path)
    images_dir = os.path.join(output_dir, "images")
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")
    _assert_not_scanned(doc)

    if not analyze_formulas:
        xref_to_name, _ = _extract_all_images(doc, images_dir)
    else:
        xref_to_name = {}
        os.makedirs(images_dir, exist_ok=True)

    pdf_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, f"{pdf_stem}.md")
    parts = []
    fig_counter = 0

    # Build a vision_map: doc_page_index → (markdown, has_figure)
    vision_map = {}
    if analyze_formulas:
        image_page_indices = [i for i in range(len(doc)) if _page_is_image_based(doc[i])]

        google = _try_get_google_client()
        if google and image_page_indices:
            g_client, g_model = google
            image_pages = [doc[i] for i in image_page_indices]
            try:
                results = _extract_doc_via_vision_google(image_pages, g_client, g_model)
                vision_map = {image_page_indices[j]: results[j]
                              for j in range(len(image_page_indices))}
            except Exception as e:
                print(f"  Google vision failed ({e}), falling back to Anthropic")
                google = None

        # Anthropic fallback for any pages not covered by Google
        missing = [i for i in image_page_indices if i not in vision_map]
        if missing:
            a_client, a_model = _get_anthropic_client()
            for page_idx in missing:
                page = doc[page_idx]
                print(f"  Page {page_idx + 1}/{len(doc)}: vision extraction (Anthropic)...")
                try:
                    vision_map[page_idx] = _extract_page_via_vision(page, a_client, a_model)
                except anthropic.APIError as e:
                    print(f"  Page {page_idx + 1}: vision failed ({e}), falling back to heuristic")
                    vision_map[page_idx] = ("", False)

    for page_num in range(len(doc)):
        page = doc[page_num]

        if page_num in vision_map:
            page_md, has_figure = vision_map[page_num]
            if has_figure:
                fig_counter += 1
                img_bytes, img_ext = _get_fullpage_image(page)
                name = f"fig{fig_counter}.{img_ext}"
                with open(os.path.join(images_dir, name), "wb") as f:
                    f.write(img_bytes)
                page_md = page_md.replace("[FIGURE]", f"![{name}](images/{name})")
                print(f"  Page {page_num + 1}: figure saved as images/{name}")
            # Fall back to heuristic if vision returned nothing
            if not page_md.strip():
                bbox_to_name = _build_bbox_to_name(page, xref_to_name)
                page_md = _page_to_markdown_heuristic(page, bbox_to_name)
            parts.append(page_md)
        else:
            bbox_to_name = _build_bbox_to_name(page, xref_to_name)
            parts.append(_page_to_markdown_heuristic(page, bbox_to_name))

        parts.append("")  # blank line between pages

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"\nDone. {fig_counter} figures extracted, markdown written to {md_path}")
    return md_path


def main():
    parser = argparse.ArgumentParser(
        description="Process a PDF: extract images, and optionally generate markdown."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--output-dir", "-o", default=None,
        help="Output directory (default: same directory as the PDF)"
    )
    parser.add_argument(
        "--markdown", "-m", action="store_true",
        help="Generate markdown with LaTeX formulas and image references"
    )
    parser.add_argument(
        "--analyze-formulas", "-f", action="store_true",
        help=(
            "Use vision AI for high-quality extraction: clean LaTeX formulas, "
            "real figures only. Tries Google first, then Anthropic. Requires credentials."
        )
    )
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: '{args.pdf}' not found.", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or os.path.dirname(os.path.abspath(args.pdf))

    if args.markdown:
        generate_markdown(args.pdf, output_dir, analyze_formulas=args.analyze_formulas)
    else:
        extract_pdf_images(args.pdf, output_dir, analyze_formulas=args.analyze_formulas)


if __name__ == "__main__":
    main()
