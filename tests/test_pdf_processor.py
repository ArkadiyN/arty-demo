"""
Tests for src/utils/pdf-processor.py

Coverage map
============

_is_math_char
  • Each of the four Unicode ranges has at least one representative character
    tested as True, and characters just outside are tested as False.  Catches
    any accidental narrowing or widening of the ranges.

_block_is_formula
  • Font-name path: checks that any font whose lowercase name contains a known
    math-font substring (e.g. "cmsy", "symbol") is flagged as a formula.
  • Unicode-density path: verifies the 15 % threshold — blocks above it are
    formulas, blocks below are not.
  • Edge cases: empty block and whitespace-only text must return False (avoids
    ZeroDivisionError and false positives on blank lines).

_block_to_markdown
  • All four output branches: H1 (≥16 pt), H2 (≥13 pt), H3 (≥11 pt + bold
    flag), and plain text.
  • Multi-line blocks are joined with a single space.
  • Empty-text lines inside a block are silently dropped.
  • An all-empty-lines block returns an empty string (not "# ").

_get_anthropic_client
  • Happy path: reads the OAuth access token from ~/.claude/.credentials.json
    and passes it as auth_token= to Anthropic().
  • API-key fallback: when the credentials file is absent the function reads
    ANTHROPIC_API_KEY from the environment.
  • Corrupt JSON fallback: a malformed credentials file triggers the except
    clause and falls back to the env var rather than crashing.
  • No-auth exit: when neither credentials file nor env var is present the
    function raises SystemExit with a helpful message.

_analyze_image_for_formula  (Anthropic client mocked — no network calls)
  • Sentinel detection: a "[DIAGRAM]" reply from the model returns None so the
    caller knows not to save a .tex file.
  • LaTeX passthrough: any other reply is returned verbatim, preserving the
    full transcription the model produced.
  • MIME mapping: known extensions (jpg, png, …) are mapped to their correct
    MIME type; unknown extensions fall back to "image/<ext>".

_assert_not_scanned  (fitz.Document mocked)
  • All-text document passes without error.
  • Exactly 30 % scanned pages passes (the threshold is strictly > 0.3).
  • More than 30 % scanned pages raises SystemExit mentioning "scanned".
  • Pages whose image covers ≤ 50 % of the page area are not counted as scanned
    even when no text is present — avoids false positives from small insets.

_page_is_image_based  (real fitz pages)
  • Returns True when a page carries a full-page embedded JPEG (>50 % coverage).
  • Returns False for pages with only vector text and no large images.

Vision pipeline  (Anthropic client mocked, real fitz pages)
  • generate_markdown(analyze_formulas=True) calls client.messages.create
    exactly once per image-based page — verifies the SDK is wired into the loop.
  • A page whose response contains [HAS_FIGURE] causes the page image to be
    saved to images/ and the [FIGURE] token to be replaced with a Markdown
    image reference in the output.
  • Text returned by the mocked model is present verbatim in the output
    markdown — verifies the response is not discarded.

Integration — real PDF on disk  (pytest.mark.integration, skipped if absent)
  • extract_pdf_images (heuristic path) returns 0 for ADA462991.pdf: every
    embedded image in that PDF is a full-page background scan that the
    skip_page_backgrounds filter correctly drops.
  • generate_markdown (heuristic path) does NOT emit image references for
    ADA462991.pdf — page-background scans are not surfaced in the output.
  • generate_markdown produces at least one heading line (# …).
  • generate_markdown(analyze_formulas=True) calls the live Anthropic API and
    produces a non-empty markdown file containing recognised text — skipped
    when no Anthropic credentials are available.
  • _assert_not_scanned does NOT reject ADA462991.pdf: despite every page
    being stored as a full-page JPEG, the OCR text layer means the function
    correctly passes it through.
  • _page_is_image_based returns True for every page of ADA462991.pdf (all
    pages are full-page JPEG scans).
"""

import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import fitz
import pytest

# ── Load the hyphen-named module ───────────────────────────────────────────────
_PROCESSOR = Path(__file__).parent.parent / "src" / "utils" / "pdf-processor.py"
_spec = importlib.util.spec_from_file_location("pdf_processor", _PROCESSOR)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_is_math_char = _mod._is_math_char
_block_is_formula = _mod._block_is_formula
_block_to_markdown = _mod._block_to_markdown
_get_anthropic_client = _mod._get_anthropic_client
_assert_not_scanned = _mod._assert_not_scanned
_page_is_image_based = _mod._page_is_image_based
_analyze_image_for_formula = _mod._analyze_image_for_formula
extract_pdf_images = _mod.extract_pdf_images
generate_markdown = _mod.generate_markdown

REAL_PDF = Path(__file__).parent / "pdf-sample" / "ADA462991.pdf"


# ── Block / span construction helpers ─────────────────────────────────────────
def _span(text, font="Helvetica", size=12.0, flags=0):
    return {"text": text, "font": font, "size": size, "flags": flags}


def _block(*texts, font="Helvetica", size=12.0, flags=0):
    """Build a minimal text block dict: one span per line."""
    return {
        "lines": [
            {"spans": [_span(t, font=font, size=size, flags=flags)]}
            for t in texts
        ]
    }


# ── Fitz document / page mock helpers ─────────────────────────────────────────
def _text_page():
    page = MagicMock()
    page.get_text.return_value = "some text"
    page.get_images.return_value = []
    return page


def _image_page(coverage=0.8):
    """A text-free page with a single image covering `coverage` of the area."""
    page = MagicMock()
    page.get_text.return_value = ""
    page.rect.width = page.rect.height = 100.0
    rect = MagicMock()
    side = 100.0 * (coverage ** 0.5)
    rect.width = rect.height = side
    page.get_images.return_value = [(99,)]
    page.get_image_rects.return_value = [rect]
    return page


def _doc(*pages):
    doc = MagicMock()
    doc.__len__.return_value = len(pages)
    doc.__getitem__.side_effect = lambda i: pages[i]
    return doc


# ══════════════════════════════════════════════════════════════════════════════
# _is_math_char
# ══════════════════════════════════════════════════════════════════════════════

class TestIsMathChar:
    def test_greek_lowercase(self):
        assert _is_math_char("α")   # 0x03B1 — Greek small letter alpha

    def test_greek_range_start(self):
        assert _is_math_char("Α")   # 0x0391 — inclusive lower bound

    def test_greek_range_end(self):
        assert _is_math_char("ω")   # 0x03C9 — inclusive upper bound

    def test_math_operator_summation(self):
        assert _is_math_char("∑")   # 0x2211 — Mathematical Operators block

    def test_misc_math_symbol(self):
        assert _is_math_char("⟂")  # 0x27C2 — Misc Mathematical Symbols-A

    def test_supplemental_math_operator(self):
        assert _is_math_char("⨀")  # 0x2A00 — boundary of Supplemental block

    def test_ascii_letter_excluded(self):
        assert not _is_math_char("a")

    def test_digit_excluded(self):
        assert not _is_math_char("0")

    def test_space_excluded(self):
        assert not _is_math_char(" ")

    def test_char_above_greek_range_excluded(self):
        assert not _is_math_char("ϊ")  # 0x03CA — one above Greek range end


# ══════════════════════════════════════════════════════════════════════════════
# _block_is_formula
# ══════════════════════════════════════════════════════════════════════════════

class TestBlockIsFormula:
    def test_empty_block_is_false(self):
        assert not _block_is_formula({"lines": []})

    def test_whitespace_only_text_is_false(self):
        assert not _block_is_formula(_block("   "))

    def test_math_font_substring_detected(self):
        # "cmsy" appears in the font name → formula regardless of content
        assert _block_is_formula(_block("f(x)", font="CMSY10"))

    def test_symbol_font_detected(self):
        assert _block_is_formula(_block("•", font="Symbol"))

    def test_euclid_font_detected(self):
        assert _block_is_formula(_block("x", font="Euclid Math One"))

    def test_high_unicode_density_detected(self):
        # "αβγ": 3 math chars / 3 total = 100 % → formula
        assert _block_is_formula(_block("αβγ"))

    def test_low_unicode_density_not_formula(self):
        # 1 math char in 20 normal chars ≈ 5 % < 15 %
        assert not _block_is_formula(_block("plain sentence with oneαchar"))

    def test_plain_ascii_not_formula(self):
        assert not _block_is_formula(_block("Introduction to the topic"))


# ══════════════════════════════════════════════════════════════════════════════
# _block_to_markdown
# ══════════════════════════════════════════════════════════════════════════════

class TestBlockToMarkdown:
    def test_no_lines_returns_empty(self):
        assert _block_to_markdown({"lines": []}) == ""

    def test_large_font_becomes_h1(self):
        assert _block_to_markdown(_block("Big Title", size=16.0)) == "# Big Title"

    def test_medium_font_becomes_h2(self):
        assert _block_to_markdown(_block("Section", size=13.0)) == "## Section"

    def test_small_bold_becomes_h3(self):
        # Flag bit 4 (value 16) = bold
        assert _block_to_markdown(_block("Subsection", size=11.0, flags=16)) == "### Subsection"

    def test_small_non_bold_is_plain(self):
        assert _block_to_markdown(_block("body text", size=11.0, flags=0)) == "body text"

    def test_below_all_thresholds_is_plain(self):
        # Bold flag present but size too small for H3
        assert _block_to_markdown(_block("caption", size=9.0, flags=16)) == "caption"

    def test_multiline_block_joined_with_space(self):
        b = _block("First line", "Second line", size=12.0)
        assert _block_to_markdown(b) == "First line Second line"

    def test_blank_line_inside_block_is_skipped(self):
        b = {
            "lines": [
                {"spans": [_span("text")]},
                {"spans": [_span("")]},   # blank — should be dropped
                {"spans": [_span("more")]},
            ]
        }
        assert _block_to_markdown(b) == "text more"


# ══════════════════════════════════════════════════════════════════════════════
# _get_anthropic_client
# ══════════════════════════════════════════════════════════════════════════════

class TestGetAnthropicClient:
    def test_uses_oauth_token_from_credentials_file(self, tmp_path, monkeypatch):
        creds = tmp_path / "creds.json"
        creds.write_text(json.dumps({"claudeAiOauth": {"accessToken": "tok-xyz"}}))
        monkeypatch.setattr(_mod.os.path, "expanduser", lambda _: str(creds))
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(auth_token="tok-xyz")

    def test_falls_back_to_api_key_when_no_credentials_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_mod.os.path, "expanduser", lambda _: str(tmp_path / "absent.json"))
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api-test")
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(api_key="sk-ant-api-test") # pragma: allowlist secret

    def test_falls_back_to_api_key_on_malformed_json(self, tmp_path, monkeypatch):
        creds = tmp_path / "creds.json"
        creds.write_text("{{not valid json")
        monkeypatch.setattr(_mod.os.path, "expanduser", lambda _: str(creds))
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fallback") # pragma: allowlist secret
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(api_key="sk-ant-fallback") # pragma: allowlist secret

    def test_falls_back_to_api_key_when_token_key_missing(self, tmp_path, monkeypatch):
        # Valid JSON but no accessToken field
        creds = tmp_path / "creds.json"
        creds.write_text(json.dumps({"claudeAiOauth": {}}))
        monkeypatch.setattr(_mod.os.path, "expanduser", lambda _: str(creds))
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-via-env")
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(api_key="sk-ant-via-env") # pragma: allowlist secret

    def test_raises_system_exit_when_no_auth_available(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_mod.os.path, "expanduser", lambda _: str(tmp_path / "absent.json"))
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(SystemExit):
            _get_anthropic_client()


# ══════════════════════════════════════════════════════════════════════════════
# _analyze_image_for_formula
# ══════════════════════════════════════════════════════════════════════════════

class TestAnalyzeImageForFormula:
    def _client(self, reply):
        c = MagicMock()
        c.messages.create.return_value.content = [MagicMock(text=reply)]
        return c

    def test_diagram_sentinel_returns_none(self):
        assert _analyze_image_for_formula(b"bytes", "png", self._client("[DIAGRAM]")) is None

    def test_diagram_sentinel_in_longer_reply_returns_none(self):
        assert _analyze_image_for_formula(b"bytes", "png", self._client("This is [DIAGRAM] only")) is None

    def test_latex_reply_returned_verbatim(self):
        latex = "$$E = mc^2$$"
        assert _analyze_image_for_formula(b"bytes", "png", self._client(latex)) == latex

    def test_jpg_maps_to_image_jpeg(self):
        client = self._client("latex")
        _analyze_image_for_formula(b"bytes", "jpg", client)
        content = client.messages.create.call_args.kwargs["messages"][0]["content"]
        img = next(c for c in content if c["type"] == "image")
        assert img["source"]["media_type"] == "image/jpeg"

    def test_png_maps_to_image_png(self):
        client = self._client("latex")
        _analyze_image_for_formula(b"bytes", "png", client)
        content = client.messages.create.call_args.kwargs["messages"][0]["content"]
        img = next(c for c in content if c["type"] == "image")
        assert img["source"]["media_type"] == "image/png"

    def test_unknown_extension_falls_back_to_generic_mime(self):
        client = self._client("latex")
        _analyze_image_for_formula(b"bytes", "tiff", client)
        content = client.messages.create.call_args.kwargs["messages"][0]["content"]
        img = next(c for c in content if c["type"] == "image")
        assert img["source"]["media_type"] == "image/tiff"


# ══════════════════════════════════════════════════════════════════════════════
# _page_is_image_based
# ══════════════════════════════════════════════════════════════════════════════

class TestPageIsImageBased:
    def test_fullpage_image_detected(self):
        # Image covering 80 % of the page → image-based
        assert _page_is_image_based(_image_page(coverage=0.8))

    def test_text_only_page_not_image_based(self):
        assert not _page_is_image_based(_text_page())

    def test_small_image_not_image_based(self):
        # Image covering only 30 % → NOT a full-page background
        assert not _page_is_image_based(_image_page(coverage=0.3))

    def test_exactly_50_percent_boundary(self):
        # Exactly 50 % coverage does not exceed the 50 % threshold → False
        assert not _page_is_image_based(_image_page(coverage=0.5))

    def test_just_above_50_percent(self):
        assert _page_is_image_based(_image_page(coverage=0.51))


# ══════════════════════════════════════════════════════════════════════════════
# _assert_not_scanned
# ══════════════════════════════════════════════════════════════════════════════

class TestAssertNotScanned:
    def test_all_text_pages_pass(self):
        doc = _doc(*[_text_page() for _ in range(10)])
        _assert_not_scanned(doc)  # must not raise

    def test_exactly_30_percent_scanned_passes(self):
        # 3/10 = 0.30 — the check is strictly > 0.3, so this must pass
        pages = [_image_page()] * 3 + [_text_page()] * 7
        _assert_not_scanned(_doc(*pages))  # must not raise

    def test_above_30_percent_raises(self):
        # 4/10 = 0.40 > 0.3 → rejected
        pages = [_image_page()] * 4 + [_text_page()] * 6
        with pytest.raises(SystemExit, match="scanned"):
            _assert_not_scanned(_doc(*pages))

    def test_small_image_not_counted_as_scanned(self):
        # Image covers only 30 % of page area — the threshold is 50 %, so this
        # page should NOT increment the scanned counter even though it has no text.
        pages = [_image_page(coverage=0.3)] * 5 + [_text_page()] * 5
        _assert_not_scanned(_doc(*pages))  # must not raise

    def test_single_page_scanned_document_rejected(self):
        # 1/1 = 100 % > 30 %
        with pytest.raises(SystemExit, match="scanned"):
            _assert_not_scanned(_doc(_image_page()))


def _has_anthropic_auth():
    """True when Anthropic credentials are available (OAuth token or API key)."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return True
    creds = Path(os.path.expanduser("~/.claude/.credentials.json"))
    if creds.exists():
        try:
            data = json.loads(creds.read_text())
            return bool(data.get("claudeAiOauth", {}).get("accessToken"))
        except Exception:
            pass
    return False


# ══════════════════════════════════════════════════════════════════════════════
# Vision pipeline — mocked Anthropic client, real fitz pages
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestVisionPipeline:
    """Exercises the --analyze-formulas path end-to-end.

    Real fitz pages are used (page rendering is not mocked), but the Anthropic
    client is a MagicMock so no network calls are made.
    """

    def _mock_client(self, reply="Extracted page text."):
        c = MagicMock()
        c.messages.create.return_value.content = [MagicMock(text=reply)]
        return c

    def test_sdk_called_for_every_image_based_page(self, tmp_path):
        client = self._mock_client()
        with patch.object(_mod, "_get_anthropic_client", return_value=client):
            generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)
        doc = fitz.open(str(REAL_PDF))
        expected = sum(1 for i in range(len(doc)) if _page_is_image_based(doc[i]))
        assert client.messages.create.call_count == expected

    def test_has_figure_response_saves_image_and_embeds_reference(self, tmp_path):
        # First call signals a figure; all subsequent calls return plain text.
        calls = [0]

        def _side_effect(*args, **kwargs):
            calls[0] += 1
            reply = "Content with [FIGURE] marker.\n[HAS_FIGURE]" if calls[0] == 1 else "Plain text."
            r = MagicMock()
            r.content = [MagicMock(text=reply)]
            return r

        client = MagicMock()
        client.messages.create.side_effect = _side_effect
        with patch.object(_mod, "_get_anthropic_client", return_value=client):
            md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)

        assert (tmp_path / "images" / "fig1.jpeg").exists()
        assert "![fig1" in Path(md_path).read_text()

    def test_model_text_appears_in_output(self, tmp_path):
        marker = "UNIQUE_VISION_MARKER_99"
        client = self._mock_client(f"Page content containing {marker}.")
        with patch.object(_mod, "_get_anthropic_client", return_value=client):
            md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)
        assert marker in Path(md_path).read_text()


# ══════════════════════════════════════════════════════════════════════════════
# Integration tests — real PDF on disk
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestRealPDF:
    def test_extract_images_zero_without_vision(self, tmp_path):
        # ADA462991.pdf stores every page as a full-page JPEG xref.
        # The skip_page_backgrounds filter should drop all 21 of them, yielding 0.
        count = extract_pdf_images(str(REAL_PDF), str(tmp_path))
        assert count == 0

    def test_images_dir_empty_without_vision(self, tmp_path):
        extract_pdf_images(str(REAL_PDF), str(tmp_path))
        images_dir = tmp_path / "images"
        # Directory is created but contains no files
        assert images_dir.exists()
        assert list(images_dir.iterdir()) == []

    def test_generate_markdown_creates_file(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        assert Path(md_path).exists()
        assert Path(md_path).stat().st_size > 0

    def test_markdown_has_no_spurious_page_images(self, tmp_path):
        # Without --analyze-formulas, page-background scans must NOT appear as
        # Markdown image references in the output.
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        content = Path(md_path).read_text()
        assert "![fig" not in content

    def test_markdown_contains_ocr_text(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        content = Path(md_path).read_text()
        # The OCR text layer should be present regardless of vision mode
        assert "FRAGMENTATION" in content.upper()

    def test_markdown_contains_heading(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        lines = Path(md_path).read_text().splitlines()
        assert any(line.startswith("#") for line in lines)

    def test_generate_markdown_with_vision(self, tmp_path):
        if not _has_anthropic_auth():
            pytest.skip("No Anthropic credentials available")
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)
        content = Path(md_path).read_text()
        assert len(content) > 500
        assert "FRAGMENTATION" in content.upper() or any(line.startswith("#") for line in content.splitlines())

    def test_ocrd_pdf_passes_scanned_check(self):
        # Every page is a full-page JPEG, but all pages carry an OCR text layer,
        # so none should be counted as scanned.
        doc = fitz.open(str(REAL_PDF))
        _assert_not_scanned(doc)  # must not raise

    def test_all_pages_are_image_based(self):
        # ADA462991.pdf is a scanned document — every page should be identified
        # as image-based so the vision pipeline can be applied per-page.
        doc = fitz.open(str(REAL_PDF))
        assert all(_page_is_image_based(doc[i]) for i in range(len(doc)))
