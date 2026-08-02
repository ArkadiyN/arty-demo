import os
import sys
import io
import re
import time
import base64
import argparse
import fitz  # PyMuPDF
import anthropic
from PIL import Image, ImageDraw
from settings import ENV_PATHS, Settings

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

# Appended to both vision prompts. The observed failure mode was not garbled
# glyphs but *invented* values in cells the source leaves empty — a table that
# reads as complete and plausible while carrying numbers that are not on the
# page. Requiring an explicit marker for both "blank in the source" and
# "present but unreadable" makes that distinction visible in the output instead
# of leaving the model to fill the gap silently.
_TABLE_FIDELITY_RULES = """
Table fidelity (applies to every table):
- Transcribe only what is printed. Never infer, interpolate, or complete a value.
- A cell that is blank in the source must be transcribed as a single dash: -
- A cell that has content you cannot read with confidence must be transcribed
  as a single question mark: ?
- Never substitute a plausible number for a ? or a - .
"""

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
""" + _TABLE_FIDELITY_RULES + """
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
""" + _TABLE_FIDELITY_RULES + """
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
# Vision client factory — one explicitly selected provider, no fallback
# ---------------------------------------------------------------------------

#: `kind` is the request shape, not the vendor: "anthropic" covers OpenRouter
#: too, because OpenRouter is reached through the Anthropic SDK.
_VISION_PROVIDERS = ("google", "anthropic", "openrouter")

_ENV_VAR_FOR = {
    "google": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}


def _no_credentials(provider):
    searched = "\n".join(
        f"  {p}  {'(found)' if p.exists() else '(absent)'}" for p in ENV_PATHS
    )
    return SystemExit(
        f"Error: vision provider '{provider}' selected but {_ENV_VAR_FOR[provider]} "
        f"is not set.\nSet it, or select another provider with --provider "
        f"({'|'.join(_VISION_PROVIDERS)}) or VISION_PROVIDER.\n"
        f".env files searched, in precedence order:\n{searched}"
    )


def _assert_google_model_usable(client, model):
    """Fail at startup on a retired/unusable model id, not mid-document.

    `gemini-2.5-flash` 404s for this project's key ("no longer available to new
    users") — but only on `generate_content`. `models.get` returns its metadata
    happily, so a listing probe reports the model as fine and the run dies
    pages later, after the document has been opened and rendered. The probe has
    to be the same call the extraction makes; a one-token prompt is the
    cheapest form of it.
    """
    from google.genai import errors
    try:
        client.models.generate_content(model=model, contents="ping")
    except errors.ClientError as e:
        raise SystemExit(
            f"Error: Google model '{model}' is not usable with this API key:\n  {e}\n"
            "Set GOOGLE_MODEL to a current id (default: gemma-4-31b-it)."
        ) from e


def _get_vision_client(provider):
    """Return (kind, client, model) for the explicitly selected provider.

    There is deliberately **no fallback**. The previous `Google → except →
    Anthropic` chain turned any Google failure — a transient 503, a retired
    model id, a missing key — into a silent switch to a paid per-page path,
    with a one-line print as the only signal. A configured provider that fails
    must fail loudly.

    OAuth tokens (sk-ant-oat01-*) are rejected by api.anthropic.com and are
    never attempted here.
    """
    s = Settings()
    if provider not in _VISION_PROVIDERS:
        raise SystemExit(
            f"Error: unknown vision provider '{provider}'. "
            f"Choose one of: {', '.join(_VISION_PROVIDERS)}."
        )

    if provider == "google":
        from google import genai  # deferred so the package is optional at import time
        from google.genai import types
        if not s.google_api_key:
            raise _no_credentials("google")
        client = genai.Client(
            api_key=s.google_api_key,
            # A request timeout is required: without one, an SDK call that
            # stalls server-side blocks forever instead of raising, since the
            # underlying httpx client has no default deadline.
            http_options=types.HttpOptions(timeout=s.google_timeout_ms),
        )
        _assert_google_model_usable(client, s.google_model)
        return "google", client, s.google_model

    if provider == "anthropic":
        if not s.anthropic_api_key:
            raise _no_credentials("anthropic")
        return ("anthropic",
                anthropic.Anthropic(api_key=s.anthropic_api_key),
                _DEFAULT_ANTHROPIC_MODEL)

    if not s.openrouter_api_key:
        raise _no_credentials("openrouter")
    return ("anthropic",
            anthropic.Anthropic(api_key=s.openrouter_api_key,
                                base_url=_OPENROUTER_BASE_URL),
            s.openrouter_model)


# ---------------------------------------------------------------------------
# Page / image utilities
# ---------------------------------------------------------------------------

def _parse_page_spec(spec, n_pages):
    """Parse a 1-indexed page spec like "40-44" or "40,42,50-52" into a sorted
    list of 0-indexed page numbers, bounds-checked against n_pages."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
        else:
            start = end = int(part)
        if start < 1 or end > n_pages or start > end:
            raise SystemExit(
                f"Error: page range '{part}' out of bounds for a {n_pages}-page document"
            )
        pages.update(range(start - 1, end))
    return sorted(pages)


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

#: DPI used for the stacked combined image. Raising it does not improve
#: transcription accuracy (dpi=200 scored no better than dpi=60 on the Tolch
#: base-spray table); page *count* per call is the variable that matters.
_COMBINED_DPI = 60

#: Longest edge the vision API accepts before downscaling server-side. A stack
#: taller than this is silently resized, so the pages the model actually sees
#: are lower-resolution than the ones that were rendered.
_MAX_COMBINED_PX = 3072

#: Height of the blue "PAGE N" separator bar drawn above each stacked page.
_SEPARATOR_H = 30


def _render_pages_combined(pages, dpi=_COMBINED_DPI):
    """Render a list of fitz pages into one tall JPEG with blue PAGE N separator bars.

    Returns JPEG bytes. The separator bars are 30 px tall and labeled "PAGE N"
    so the vision model can identify page boundaries.
    """
    SEP_H = _SEPARATOR_H
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


def _warn_if_table_has_no_fidelity_markers(page_idx, page_md):
    """Flag a transcribed table that emitted neither a `?` nor a `-` cell.

    Both vision prompts require `?` for an unreadable cell and `-` for one the
    source leaves blank. A table page that came back with every cell populated
    and neither marker anywhere is the signature of the observed failure —
    values invented for cells that are empty on the page. It is not proof of a
    defect (a genuinely complete table looks the same), so this warns rather
    than raising; the closure invariant in `.claude/rules/source-data-fidelity.md`
    is what actually decides admissibility.
    """
    rows = [ln for ln in page_md.splitlines() if ln.count("|") >= 2]
    if len(rows) < 3:
        return
    cells = [c.strip() for row in rows for c in row.split("|")]
    if any(c in ("?", "-", "--", "—", "–") for c in cells):
        return
    print(f"  Page {page_idx + 1}: CAUTION — transcribed a {len(rows)}-row table with no "
          "'?' (unreadable) or '-' (blank) cells. Verify against the source page "
          "before citing; every cell being filled is what an invented value looks like.")


class _EmptyVisionResponse(Exception):
    """Raised when Google returns no text part (retryable, like a ServerError)."""


# Pages per Google vision request.
#
# One. Page stacking is the established cause of the transcription failures
# this default exists to prevent: on the Tolch base-spray table, a single-page
# call at dpi=60 scored 18/18 ground-truth cells, the shipped 8-page stack
# scored 5/18 and returned the exact wrong value that reached the repo, and
# even a 3-page stack already cost 2 of 18 cells. Neither the model tier nor
# the raster resolution moved those numbers (`checks/vision-provider-probe.py`).
#
# Stacking remains available via --vision-chunk-size for prose-only documents,
# where it demonstrably works and is much cheaper. It must never be the default
# for a document with tables, and a document's tables are not known in advance.
_DEFAULT_VISION_CHUNK_SIZE = 1


def _bounded_chunk_size(pages, requested):
    """Clamp `requested` so the stacked image never exceeds _MAX_COMBINED_PX.

    Above that height the API downscales the stack server-side, so the model
    reads pages at a lower resolution than was rendered — a quality loss with
    no visible symptom. Derived from the actual rendered page height rather
    than assumed, since page geometry varies by document.
    """
    if requested <= 1 or not pages:
        return max(1, requested)
    pm = pages[0].get_pixmap(dpi=_COMBINED_DPI)
    per_page_px = pm.height + _SEPARATOR_H
    allowed = max(1, _MAX_COMBINED_PX // per_page_px)
    if allowed < requested:
        print(f"  Capping vision chunk size {requested} -> {allowed} "
              f"({per_page_px} px/page at dpi={_COMBINED_DPI}; "
              f"max combined edge {_MAX_COMBINED_PX} px)")
    return min(requested, allowed)


def _extract_doc_via_vision_google_chunk(pages, client, model):
    """Send one batch of pages as a combined image to Google; return per-page (md, has_figure).

    pages: ordered list of fitz.Page objects (the image-based pages only).
    The combined image is labeled PAGE 1..N so the response maps back positionally.

    A DEADLINE_EXCEEDED (504) means this batch's transcription genuinely takes
    longer than GOOGLE_TIMEOUT_MS — identical retries hit the same fixed
    deadline again, not a transient fluke, so they're not a reliable fix on
    their own. Once retries are exhausted on a multi-page batch, split it in
    half and retry each half fresh (smaller combined image, less to
    transcribe, comfortably faster) instead of giving up or resending the
    same oversized request a 4th time.
    """
    from google.genai import types, errors

    n = len(pages)
    combined_bytes = _render_pages_combined(pages)
    prompt = _DOC_VISION_PROMPT.format(n=n)

    print(f"  Sending {n} pages as combined image to Google ({model})...")
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_bytes(data=combined_bytes, mime_type="image/jpeg"),
                    prompt,
                ],
            )
            if response.text is None:
                # The model can burn its whole output budget on internal
                # "thinking" and never emit the actual transcription part;
                # response.text then comes back None with no exception raised.
                # Retrying is usually enough to get a real answer.
                raise _EmptyVisionResponse("no text part returned")
            return _parse_page_vision_response(response.text, n)
        except (errors.ServerError, _EmptyVisionResponse) as e:
            if attempt == max_attempts:
                if n > 1:
                    mid = n // 2
                    print(f"  Still failing after {max_attempts} attempts at {n} pages "
                          f"({e}); splitting into {mid}+{n - mid} pages and retrying smaller "
                          "instead of repeating the same request")
                    return (_extract_doc_via_vision_google_chunk(pages[:mid], client, model)
                            + _extract_doc_via_vision_google_chunk(pages[mid:], client, model))
                raise
            wait_s = 2 ** attempt
            print(f"  Google vision call failed ({e}); retrying in {wait_s}s "
                  f"(attempt {attempt}/{max_attempts})...")
            time.sleep(wait_s)


def _extract_doc_via_vision_google(pages, client, model, chunk_size=_DEFAULT_VISION_CHUNK_SIZE):
    """Send all pages to Google in batches of chunk_size; return per-page (md, has_figure).

    pages: ordered list of fitz.Page objects (the image-based pages only).
    Chunking keeps each request well within the API timeout and the 30
    req/min quota (an 8-page chunk needs no artificial pacing), and confines
    the output-budget failure mode to one chunk instead of the whole
    document. Results are concatenated in input order, so callers see the
    same shape as a single combined call.

    A chunk that still fails after its internal retries does NOT abort the
    whole document: its pages come back as `None` (instead of an (md, has_figure)
    tuple) so the caller's already-succeeded chunks are still returned, and
    `generate_markdown`'s existing per-page Anthropic fallback (for pages
    "missing" from the Google vision_map) picks up the `None` pages the same
    way it already picks up pages Google never attempted.
    """
    chunk_size = _bounded_chunk_size(pages, chunk_size)
    results = []
    for start in range(0, len(pages), chunk_size):
        chunk = pages[start:start + chunk_size]
        # A chunk that survives neither its retries nor the halving above is a
        # hard failure. It used to be swallowed into `None` pages for the
        # cross-provider fallback to pick up; with no fallback, swallowing it
        # would mean silently emitting heuristic text for those pages, which is
        # the class of quiet degradation this pipeline is being hardened
        # against. Abort and name the pages instead.
        results.extend(_extract_doc_via_vision_google_chunk(chunk, client, model))
    return results


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

def extract_pdf_images(pdf_path, output_dir="output", analyze_formulas=False,
                        vision_chunk_size=_DEFAULT_VISION_CHUNK_SIZE,
                        screenshot_pages=False, provider=None):
    provider = provider or Settings().vision_provider
    doc = fitz.open(pdf_path)
    images_dir = os.path.join(output_dir, "images")
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")
    _assert_not_scanned(doc)

    if screenshot_pages:
        os.makedirs(images_dir, exist_ok=True)
        count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            if _page_is_image_based(page):
                count += 1
                img_bytes, img_ext = _get_fullpage_image(page)
                name = f"page{page_num + 1}.{img_ext}"
                with open(os.path.join(images_dir, name), "wb") as f:
                    f.write(img_bytes)
                print(f"  Page {page_num + 1}: saved as images/{name}")
    elif analyze_formulas:
        os.makedirs(images_dir, exist_ok=True)
        fig_counter = 0

        kind, client, model = _get_vision_client(provider)
        print(f"Vision provider: {provider} ({model})")
        image_pages = [(i, doc[i]) for i in range(len(doc)) if _page_is_image_based(doc[i])]

        if kind == "google":
            results = _extract_doc_via_vision_google(
                [p for _, p in image_pages], client, model,
                chunk_size=vision_chunk_size,
            ) if image_pages else []
            figure_flags = [(idx, page, results[j][1])
                            for j, (idx, page) in enumerate(image_pages)]
        else:
            figure_flags = []
            for page_idx, page in image_pages:
                print(f"  Page {page_idx + 1}/{len(doc)}: checking for figure...")
                _, has_figure = _extract_page_via_vision(page, client, model)
                figure_flags.append((page_idx, page, has_figure))

        for page_idx, page, has_figure in figure_flags:
            if has_figure:
                fig_counter += 1
                img_bytes, img_ext = _get_fullpage_image(page)
                name = f"fig{fig_counter}.{img_ext}"
                with open(os.path.join(images_dir, name), "wb") as f:
                    f.write(img_bytes)
                print(f"  Page {page_idx + 1}: figure saved as images/{name}")
        count = fig_counter
    else:
        _, count = _extract_all_images(doc, images_dir)

    print(f"\nDone. Extracted {count} figures to {images_dir}")
    return count


def generate_markdown(pdf_path, output_dir="output", analyze_formulas=False,
                       vision_chunk_size=_DEFAULT_VISION_CHUNK_SIZE, pages=None,
                       provider=None):
    """pages: optional 1-indexed page spec (e.g. "40-44") to process only a
    subset — for re-extracting specific pages (garbled tables, broken cmap)
    at vision quality without re-running the whole document. Output lands in
    a separate `<stem>-pNN-NN.md` file so it never clobbers a prior full
    extraction; merge the improved section in by hand."""
    provider = provider or Settings().vision_provider
    doc = fitz.open(pdf_path)
    images_dir = os.path.join(output_dir, "images")
    print(f"Opened PDF: {pdf_path} ({len(doc)} pages)")
    _assert_not_scanned(doc)

    page_range = _parse_page_spec(pages, len(doc)) if pages else list(range(len(doc)))

    if not analyze_formulas:
        xref_to_name, _ = _extract_all_images(doc, images_dir)
    else:
        xref_to_name = {}
        os.makedirs(images_dir, exist_ok=True)

    pdf_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    if pages:
        suffix = pages.replace(",", "_").replace("-", "to")
        md_path = os.path.join(output_dir, f"{pdf_stem}-p{suffix}.md")
    else:
        md_path = os.path.join(output_dir, f"{pdf_stem}.md")
    parts = []
    fig_counter = 0

    # Build a vision_map: doc_page_index → (markdown, has_figure)
    vision_map = {}
    if analyze_formulas:
        image_page_indices = [i for i in page_range if _page_is_image_based(doc[i])]

        if image_page_indices:
            kind, client, model = _get_vision_client(provider)
            print(f"Vision provider: {provider} ({model})")
            if kind == "google":
                results = _extract_doc_via_vision_google(
                    [doc[i] for i in image_page_indices], client, model,
                    chunk_size=vision_chunk_size,
                )
                vision_map = dict(zip(image_page_indices, results))
            else:
                for page_idx in image_page_indices:
                    print(f"  Page {page_idx + 1}/{len(doc)}: vision extraction ({provider})...")
                    vision_map[page_idx] = _extract_page_via_vision(doc[page_idx], client, model)

        for page_idx, (page_md, _) in sorted(vision_map.items()):
            _warn_if_table_has_no_fidelity_markers(page_idx, page_md)

    for page_num in page_range:
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
            "real figures only. Uses the provider named by --provider, with no "
            "fallback to another provider. Requires that provider's credentials."
        )
    )
    parser.add_argument(
        "--provider", choices=_VISION_PROVIDERS, default=None,
        help=(
            "Vision provider for --analyze-formulas (default: VISION_PROVIDER, "
            "or 'google'). Selection is explicit and there is no fallback: if the "
            "chosen provider lacks credentials or fails, the run stops rather than "
            "silently switching to another (possibly paid) provider."
        )
    )
    parser.add_argument(
        "--vision-chunk-size", type=int, default=_DEFAULT_VISION_CHUNK_SIZE,
        help=(
            "Pages stacked into one Google vision request when --analyze-formulas "
            f"is set (default: {_DEFAULT_VISION_CHUNK_SIZE}). Stacking is measurably "
            "lossy on tables — 1 page scored 18/18 ground-truth cells where an "
            "8-page stack scored 5/18 — so raise it only for prose-only documents. "
            "The value is capped so the stacked image never exceeds the API's "
            f"{_MAX_COMBINED_PX} px limit and gets downscaled server-side."
        )
    )
    parser.add_argument(
        "--pages",
        help=(
            "Restrict --markdown to a 1-indexed page subset, e.g. '40-44' or "
            "'40,42,50-52'. Use with --analyze-formulas to re-extract just the "
            "pages with garbled tables/formulas at vision quality without "
            "re-running the whole document. Writes to a separate "
            "'<stem>-pNN-NN.md' file rather than overwriting the full transcript."
        )
    )
    parser.add_argument(
        "--screenshot-pages", action="store_true",
        help=(
            "Save every image-based page as a full-page screenshot, with no vision "
            "AI call and no figure-detection gating. Pure local rasterization "
            "(no network/API dependency). Ignores --analyze-formulas."
        )
    )
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: '{args.pdf}' not found.", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or os.path.dirname(os.path.abspath(args.pdf))

    if args.markdown:
        generate_markdown(args.pdf, output_dir, analyze_formulas=args.analyze_formulas,
                           vision_chunk_size=args.vision_chunk_size, pages=args.pages,
                           provider=args.provider)
    else:
        extract_pdf_images(args.pdf, output_dir, analyze_formulas=args.analyze_formulas,
                            vision_chunk_size=args.vision_chunk_size,
                            screenshot_pages=args.screenshot_pages,
                            provider=args.provider)


if __name__ == "__main__":
    main()
