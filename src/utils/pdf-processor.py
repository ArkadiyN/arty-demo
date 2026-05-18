import os
import sys
import json
import base64
import argparse
import fitz  # PyMuPDF
import anthropic

_MATH_FONTS = frozenset({"symbol", "cmsy", "cmex", "cmmi", "mtex", "mathtime", "euclid"})
# Greek letters + Mathematical Operators + Misc Math + Supplemental Math
_MATH_RANGES = [(0x0391, 0x03C9), (0x2200, 0x22FF), (0x27C0, 0x27EF), (0x2A00, 0x2AFF)]

_FORMULA_PROMPT = (
    "If this image contains a mathematical equation, graph formula, or coordinate matrix, "
    "transcribe it completely into valid LaTeX display math format using $$ encapsulation. "
    "If it is a pure layout schematic or photo with no explicit equations, reply with: [DIAGRAM]"
)

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

# PyMuPDF ext → MIME type (covers the common cases it returns)
_MIME = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
}


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


def _get_anthropic_client():
    """Return an authenticated Anthropic client.

    Prefers Claude Code's stored OAuth token (~/.claude/.credentials.json).
    Falls back to ANTHROPIC_API_KEY if the credentials file is absent or expired.
    """
    credentials_path = os.path.expanduser("~/.claude/.credentials.json")
    if os.path.exists(credentials_path):
        try:
            with open(credentials_path) as f:
                creds = json.load(f)
            token = creds.get("claudeAiOauth", {}).get("accessToken")
            if token:
                return anthropic.Anthropic(auth_token=token)
        except (json.JSONDecodeError, KeyError, OSError):
            pass

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return anthropic.Anthropic(api_key=api_key)

    raise SystemExit(
        "Error: No Anthropic credentials found. Either:\n"
        "  1. Log in via Claude Code (claude auth login), or\n"
        "  2. Set the ANTHROPIC_API_KEY environment variable"
    )


def _assert_not_scanned(doc):
    """Raise if the PDF has no text layer (scanned image-only document)."""
    scanned = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        has_text = bool(page.get_text().strip())
        if has_text:
            continue
        # No text — check whether any image covers >50% of the page area
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
    """True when the page stores its content as a full-page embedded image (scanned+OCR)."""
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


def _extract_page_via_vision(page, client):
    """Ask Claude to extract text+LaTeX from a page image.

    Returns (markdown_text, has_figure).
    """
    image_b64 = base64.standard_b64encode(_render_page_jpeg(page)).decode()
    response = client.messages.create(
        model="claude-haiku-4-5",
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
    content = response.content[0].text
    has_figure = "[HAS_FIGURE]" in content
    markdown = content.replace("[HAS_FIGURE]", "").strip()
    if not has_figure:
        markdown = markdown.replace("[FIGURE]", "")
    return markdown, has_figure


def _analyze_image_for_formula(image_bytes, image_ext, client):
    """Return LaTeX string if image contains a formula, None if it's a diagram/photo."""
    media_type = _MIME.get(image_ext.lower(), f"image/{image_ext.lower()}")
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model="claude-haiku-4-5",
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

    transcription = response.content[0].text.strip()
    return None if "[DIAGRAM]" in transcription else transcription


def _extract_all_images(doc, images_dir, equations_dir=None, client=None,
                        skip_page_backgrounds=True):
    """Extract unique non-background images; return xref→filename map and count.

    When skip_page_backgrounds=True (default), images covering >50% of their
    page are assumed to be scanned-page backgrounds and are not saved.
    """
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


def extract_pdf_images(pdf_path, output_dir="output", analyze_formulas=False):
    doc = fitz.open(pdf_path)
    images_dir = os.path.join(output_dir, "images")
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")
    _assert_not_scanned(doc)

    if analyze_formulas:
        client = _get_anthropic_client()
        os.makedirs(images_dir, exist_ok=True)
        fig_counter = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            if _page_is_image_based(page):
                print(f"  Page {page_num + 1}/{len(doc)}: checking for figure...")
                try:
                    _, has_figure = _extract_page_via_vision(page, client)
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

    client = _get_anthropic_client() if analyze_formulas else None

    # For the heuristic path, pre-extract all non-background images upfront.
    if not analyze_formulas:
        xref_to_name, _ = _extract_all_images(doc, images_dir)
    else:
        xref_to_name = {}
        os.makedirs(images_dir, exist_ok=True)

    pdf_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, f"{pdf_stem}.md")

    parts = []
    fig_counter = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        if analyze_formulas and _page_is_image_based(page):
            # Vision path: Claude extracts text+LaTeX and identifies figures.
            print(f"  Page {page_num + 1}/{len(doc)}: vision extraction...")
            try:
                page_md, has_figure = _extract_page_via_vision(page, client)
                if has_figure:
                    fig_counter += 1
                    img_bytes, img_ext = _get_fullpage_image(page)
                    name = f"fig{fig_counter}.{img_ext}"
                    with open(os.path.join(images_dir, name), "wb") as f:
                        f.write(img_bytes)
                    page_md = page_md.replace("[FIGURE]", f"![{name}](images/{name})")
                    print(f"    -> Figure saved: images/{name}")
                parts.append(page_md)
            except anthropic.APIError as e:
                print(f"  Page {page_num + 1}: vision failed ({e}), falling back to heuristic")
                bbox_to_name = _build_bbox_to_name(page, xref_to_name)
                parts.append(_page_to_markdown_heuristic(page, bbox_to_name))
        else:
            # Heuristic path: font/Unicode detection, no API calls.
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
            "Use Claude vision for high-quality extraction: clean LaTeX formulas, "
            "real figures only (skips page-background scans). Requires authentication."
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
