"""
Tests for src/utils/pdf-processor.py

Coverage map
============

_is_math_char / _block_is_formula / _block_to_markdown
  (unchanged — see docstrings in the test classes below)

_try_get_google_client
  • Returns (client, model) when GOOGLE_API_KEY is set.
  • Returns None when the key is absent.

_get_anthropic_client
  • Prefers ANTHROPIC_API_KEY over OpenRouter.
  • Falls back to OpenRouter when only OPENROUTER_API_KEY is set.
  • Raises SystemExit when neither key is present.

_render_pages_combined
  • Returns non-empty bytes for a single real PDF page.
  • Output decodes as a valid JPEG (starts with FF D8 FF).
  • Combined image is taller than a single page render (separator included).

_parse_page_vision_response
  • Correctly splits N pages on === PAGE N === markers.
  • Extracts [HAS_FIGURE] flag and strips it from the markdown.
  • Strips [FIGURE] token when has_figure is False.
  • Pages with no matching section get ("", False).
  • Handles extra whitespace / CRLF around markers.

_extract_doc_via_vision_google (Google client mocked)
  • Calls client.models.generate_content exactly once (1 API call for N pages).
  • Returns per-page (markdown, has_figure) matching page count.

Vision pipeline — Google path (Google client mocked, real fitz pages)
  • generate_markdown with analyze_formulas=True uses Google when available.
  • A single API call is made for all image-based pages.
  • [HAS_FIGURE] pages result in saved images and embedded Markdown references.
  • Model text from the combined response appears in the output markdown.

Vision pipeline — Anthropic fallback (Google absent, Anthropic mocked)
  • When _try_get_google_client returns None, falls through to Anthropic.
  • Anthropic client is called once per image-based page.

Integration — real API calls (pytest.mark.integration, skipped when no creds)
  • TestGoogleAuth: live ping to Google API, response contains text.
  • TestRealPDF: heuristic-path assertions on ADA462991.pdf.
  • TestRealPDF.test_generate_markdown_with_vision: live Google vision call.
"""

import importlib.util
import os
import re
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
_try_get_google_client = _mod._try_get_google_client
_get_anthropic_client = _mod._get_anthropic_client
_assert_not_scanned = _mod._assert_not_scanned
_page_is_image_based = _mod._page_is_image_based
_analyze_image_for_formula = _mod._analyze_image_for_formula
_render_pages_combined = _mod._render_pages_combined
_parse_page_vision_response = _mod._parse_page_vision_response
_extract_doc_via_vision_google = _mod._extract_doc_via_vision_google
extract_pdf_images = _mod.extract_pdf_images
generate_markdown = _mod.generate_markdown

REAL_PDF = Path(__file__).parent / "pdf-sample" / "ADA462991.pdf"


# ── Block / span construction helpers ─────────────────────────────────────────
def _span(text, font="Helvetica", size=12.0, flags=0):
    return {"text": text, "font": font, "size": size, "flags": flags}


def _block(*texts, font="Helvetica", size=12.0, flags=0):
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


def _has_google_auth():
    return bool(os.environ.get("GOOGLE_API_KEY"))


def _has_anthropic_auth():
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENROUTER_API_KEY"))


# ══════════════════════════════════════════════════════════════════════════════
# _is_math_char
# ══════════════════════════════════════════════════════════════════════════════

class TestIsMathChar:
    def test_greek_lowercase(self):
        assert _is_math_char("α")

    def test_greek_range_start(self):
        assert _is_math_char("Α")

    def test_greek_range_end(self):
        assert _is_math_char("ω")

    def test_math_operator_summation(self):
        assert _is_math_char("∑")

    def test_misc_math_symbol(self):
        assert _is_math_char("⟂")

    def test_supplemental_math_operator(self):
        assert _is_math_char("⨀")

    def test_ascii_letter_excluded(self):
        assert not _is_math_char("a")

    def test_digit_excluded(self):
        assert not _is_math_char("0")

    def test_space_excluded(self):
        assert not _is_math_char(" ")

    def test_char_above_greek_range_excluded(self):
        assert not _is_math_char("ϊ")


# ══════════════════════════════════════════════════════════════════════════════
# _block_is_formula
# ══════════════════════════════════════════════════════════════════════════════

class TestBlockIsFormula:
    def test_empty_block_is_false(self):
        assert not _block_is_formula({"lines": []})

    def test_whitespace_only_text_is_false(self):
        assert not _block_is_formula(_block("   "))

    def test_math_font_substring_detected(self):
        assert _block_is_formula(_block("f(x)", font="CMSY10"))

    def test_symbol_font_detected(self):
        assert _block_is_formula(_block("•", font="Symbol"))

    def test_euclid_font_detected(self):
        assert _block_is_formula(_block("x", font="Euclid Math One"))

    def test_high_unicode_density_detected(self):
        assert _block_is_formula(_block("αβγ"))

    def test_low_unicode_density_not_formula(self):
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
        assert _block_to_markdown(_block("Subsection", size=11.0, flags=16)) == "### Subsection"

    def test_small_non_bold_is_plain(self):
        assert _block_to_markdown(_block("body text", size=11.0, flags=0)) == "body text"

    def test_below_all_thresholds_is_plain(self):
        assert _block_to_markdown(_block("caption", size=9.0, flags=16)) == "caption"

    def test_multiline_block_joined_with_space(self):
        b = _block("First line", "Second line", size=12.0)
        assert _block_to_markdown(b) == "First line Second line"

    def test_blank_line_inside_block_is_skipped(self):
        b = {
            "lines": [
                {"spans": [_span("text")]},
                {"spans": [_span("")]},
                {"spans": [_span("more")]},
            ]
        }
        assert _block_to_markdown(b) == "text more"


# ══════════════════════════════════════════════════════════════════════════════
# _try_get_google_client
# ══════════════════════════════════════════════════════════════════════════════

class TestTryGetGoogleClient:
    def test_returns_client_and_model_when_key_set(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "fake-google-key")  # pragma: allowlist secret
        monkeypatch.setenv("GOOGLE_MODEL", "gemma-4-31b-it")
        mock_genai = MagicMock()
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        with patch.dict("sys.modules", {"google": MagicMock(genai=mock_genai), "google.genai": mock_genai}):
            result = _try_get_google_client()
        assert result is not None
        client, model = result
        assert model == "gemma-4-31b-it"

    def test_returns_none_when_key_absent(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        result = _try_get_google_client()
        assert result is None


# ══════════════════════════════════════════════════════════════════════════════
# _get_anthropic_client
# ══════════════════════════════════════════════════════════════════════════════

class TestGetAnthropicClient:
    def test_uses_anthropic_api_key(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-api-test")  # pragma: allowlist secret
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(api_key="sk-ant-api-test")  # pragma: allowlist secret

    def test_falls_back_to_openrouter_when_no_anthropic_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")  # pragma: allowlist secret
        monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")
        with patch.object(_mod.anthropic, "Anthropic") as mock_cls:
            _get_anthropic_client()
        mock_cls.assert_called_once_with(
            api_key="sk-or-test", base_url="https://openrouter.ai/api"  # pragma: allowlist secret
        )

    def test_raises_system_exit_when_no_auth_available(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
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
        assert _page_is_image_based(_image_page(coverage=0.8))

    def test_text_only_page_not_image_based(self):
        assert not _page_is_image_based(_text_page())

    def test_small_image_not_image_based(self):
        assert not _page_is_image_based(_image_page(coverage=0.3))

    def test_exactly_50_percent_boundary(self):
        assert not _page_is_image_based(_image_page(coverage=0.5))

    def test_just_above_50_percent(self):
        assert _page_is_image_based(_image_page(coverage=0.51))


# ══════════════════════════════════════════════════════════════════════════════
# _assert_not_scanned
# ══════════════════════════════════════════════════════════════════════════════

class TestAssertNotScanned:
    def test_all_text_pages_pass(self):
        doc = _doc(*[_text_page() for _ in range(10)])
        _assert_not_scanned(doc)

    def test_exactly_30_percent_scanned_passes(self):
        pages = [_image_page()] * 3 + [_text_page()] * 7
        _assert_not_scanned(_doc(*pages))

    def test_above_30_percent_raises(self):
        pages = [_image_page()] * 4 + [_text_page()] * 6
        with pytest.raises(SystemExit, match="scanned"):
            _assert_not_scanned(_doc(*pages))

    def test_small_image_not_counted_as_scanned(self):
        pages = [_image_page(coverage=0.3)] * 5 + [_text_page()] * 5
        _assert_not_scanned(_doc(*pages))

    def test_single_page_scanned_document_rejected(self):
        with pytest.raises(SystemExit, match="scanned"):
            _assert_not_scanned(_doc(_image_page()))


# ══════════════════════════════════════════════════════════════════════════════
# _render_pages_combined  (real fitz pages)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestRenderPagesCombined:
    def _first_page(self):
        return fitz.open(str(REAL_PDF))[0]

    def test_returns_nonempty_bytes(self):
        data = _render_pages_combined([self._first_page()])
        assert len(data) > 0

    def test_output_is_valid_jpeg(self):
        data = _render_pages_combined([self._first_page()])
        assert data[:3] == b"\xff\xd8\xff"

    def test_combined_taller_than_single_page(self):
        from PIL import Image
        import io

        page = self._first_page()
        single = _render_pages_combined([page])
        two = _render_pages_combined([page, page])

        h_single = Image.open(io.BytesIO(single)).height
        h_two = Image.open(io.BytesIO(two)).height
        assert h_two > h_single

    def test_separator_bar_is_blue(self):
        """The first row of the combined image should be the blue separator."""
        from PIL import Image
        import io

        data = _render_pages_combined([self._first_page()])
        img = Image.open(io.BytesIO(data)).convert("RGB")
        pixel = img.getpixel((img.width // 2, 0))
        assert isinstance(pixel, tuple)
        r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
        assert b > r and b > g  # blue channel dominates


# ══════════════════════════════════════════════════════════════════════════════
# _parse_page_vision_response
# ══════════════════════════════════════════════════════════════════════════════

class TestParsePageVisionResponse:
    def test_single_page_extracted(self):
        text = "=== PAGE 1 ===\nHello world"
        results = _parse_page_vision_response(text, 1)
        assert results[0] == ("Hello world", False)

    def test_two_pages_split_correctly(self):
        text = "=== PAGE 1 ===\nPage one text\n=== PAGE 2 ===\nPage two text"
        results = _parse_page_vision_response(text, 2)
        assert results[0] == ("Page one text", False)
        assert results[1] == ("Page two text", False)

    def test_has_figure_flag_extracted(self):
        text = "=== PAGE 1 ===\nText [FIGURE] more\n[HAS_FIGURE]"
        results = _parse_page_vision_response(text, 1)
        md, has_fig = results[0]
        assert has_fig is True
        assert "[HAS_FIGURE]" not in md
        assert "[FIGURE]" in md  # kept when has_figure is True

    def test_figure_token_stripped_when_no_has_figure(self):
        text = "=== PAGE 1 ===\nText [FIGURE] more"
        results = _parse_page_vision_response(text, 1)
        md, has_fig = results[0]
        assert has_fig is False
        assert "[FIGURE]" not in md

    def test_missing_page_gets_empty_tuple(self):
        text = "=== PAGE 1 ===\nOnly page one"
        results = _parse_page_vision_response(text, 3)
        assert results[1] == ("", False)
        assert results[2] == ("", False)

    def test_out_of_range_page_number_ignored(self):
        text = "=== PAGE 5 ===\nOut of range"
        results = _parse_page_vision_response(text, 2)
        assert results[0] == ("", False)
        assert results[1] == ("", False)

    def test_extra_whitespace_around_marker_handled(self):
        text = "\n=== PAGE 1 ===\n\n  Content here  \n\n=== PAGE 2 ===\nMore"
        results = _parse_page_vision_response(text, 2)
        assert results[0][0] == "Content here"
        assert results[1][0] == "More"


# ══════════════════════════════════════════════════════════════════════════════
# _extract_doc_via_vision_google  (Google client mocked)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestExtractDocViaVisionGoogle:
    def _mock_google_client(self, response_text):
        client = MagicMock()
        client.models.generate_content.return_value.text = response_text
        return client

    def test_single_api_call_for_multiple_pages(self):
        doc = fitz.open(str(REAL_PDF))
        pages = [doc[i] for i in range(3)]
        reply = "=== PAGE 1 ===\nP1\n=== PAGE 2 ===\nP2\n=== PAGE 3 ===\nP3"
        client = self._mock_google_client(reply)
        _extract_doc_via_vision_google(pages, client, "gemma-4-31b-it")
        assert client.models.generate_content.call_count == 1

    def test_returns_per_page_results(self):
        doc = fitz.open(str(REAL_PDF))
        pages = [doc[i] for i in range(2)]
        reply = "=== PAGE 1 ===\nFirst page content\n=== PAGE 2 ===\nSecond page content"
        client = self._mock_google_client(reply)
        results = _extract_doc_via_vision_google(pages, client, "gemma-4-31b-it")
        assert len(results) == 2
        assert results[0][0] == "First page content"
        assert results[1][0] == "Second page content"

    def test_has_figure_propagated(self):
        doc = fitz.open(str(REAL_PDF))
        pages = [doc[0]]
        reply = "=== PAGE 1 ===\nText [FIGURE] end\n[HAS_FIGURE]"
        client = self._mock_google_client(reply)
        results = _extract_doc_via_vision_google(pages, client, "gemma-4-31b-it")
        _, has_fig = results[0]
        assert has_fig is True


# ══════════════════════════════════════════════════════════════════════════════
# Vision pipeline — Google path (mocked, real fitz pages)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestVisionPipelineGoogle:
    """generate_markdown with Google client mocked — verifies the Google dispatch path."""

    def _mock_google_client(self, n_pages, has_figure_on_page=None):
        lines = []
        for i in range(1, n_pages + 1):
            lines.append(f"=== PAGE {i} ===")
            if has_figure_on_page == i:
                lines.append(f"Content of page {i} [FIGURE] more text\n[HAS_FIGURE]")
            else:
                lines.append(f"UNIQUE_GOOGLE_TEXT page {i}")
        response_text = "\n".join(lines)
        client = MagicMock()
        client.models.generate_content.return_value.text = response_text
        return client

    def test_google_client_used_when_available(self, tmp_path):
        doc = fitz.open(str(REAL_PDF))
        n_image = sum(1 for i in range(len(doc)) if _page_is_image_based(doc[i]))
        g_client = self._mock_google_client(n_image)

        with patch.object(_mod, "_try_get_google_client", return_value=(g_client, "gemma-4-31b-it")):
            generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)

        assert g_client.models.generate_content.call_count == 1

    def test_google_text_appears_in_output(self, tmp_path):
        doc = fitz.open(str(REAL_PDF))
        n_image = sum(1 for i in range(len(doc)) if _page_is_image_based(doc[i]))
        g_client = self._mock_google_client(n_image)

        with patch.object(_mod, "_try_get_google_client", return_value=(g_client, "gemma-4-31b-it")):
            md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)

        assert "UNIQUE_GOOGLE_TEXT" in Path(md_path).read_text()

    def test_has_figure_saves_image_and_embeds_reference(self, tmp_path):
        doc = fitz.open(str(REAL_PDF))
        n_image = sum(1 for i in range(len(doc)) if _page_is_image_based(doc[i]))
        g_client = self._mock_google_client(n_image, has_figure_on_page=1)

        with patch.object(_mod, "_try_get_google_client", return_value=(g_client, "gemma-4-31b-it")):
            md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)

        assert (tmp_path / "images" / "fig1.jpeg").exists()
        assert "![fig1" in Path(md_path).read_text()


# ══════════════════════════════════════════════════════════════════════════════
# Vision pipeline — Anthropic fallback (Google absent, Anthropic mocked)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestVisionPipelineAnthropicFallback:
    """When _try_get_google_client returns None, Anthropic is used per-page."""

    def _mock_anthropic_client(self, reply="Extracted page text."):
        c = MagicMock()
        c.messages.create.return_value.content = [MagicMock(text=reply)]
        return c

    def test_anthropic_called_per_page_when_google_absent(self, tmp_path):
        client = self._mock_anthropic_client()
        with (
            patch.object(_mod, "_try_get_google_client", return_value=None),
            patch.object(_mod, "_get_anthropic_client", return_value=(client, "claude-haiku-4-5")),
        ):
            generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)

        doc = fitz.open(str(REAL_PDF))
        expected = sum(1 for i in range(len(doc)) if _page_is_image_based(doc[i]))
        assert client.messages.create.call_count == expected

    def test_anthropic_text_appears_in_output(self, tmp_path):
        marker = "UNIQUE_ANTHROPIC_MARKER_77"
        client = self._mock_anthropic_client(f"Page content containing {marker}.")
        with (
            patch.object(_mod, "_try_get_google_client", return_value=None),
            patch.object(_mod, "_get_anthropic_client", return_value=(client, "claude-haiku-4-5")),
        ):
            md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)
        assert marker in Path(md_path).read_text()


# ══════════════════════════════════════════════════════════════════════════════
# Integration — real API calls
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestGoogleAuth:
    """Verifies that _try_get_google_client() produces a working client via a live ping."""

    def test_google_key_can_reach_api(self):
        if not _has_google_auth():
            pytest.skip("No GOOGLE_API_KEY available")
        from google.genai.errors import ClientError
        result = _try_get_google_client()
        assert result is not None, "Expected (client, model) but got None"
        client, model = result
        try:
            response = client.models.generate_content(
                model=model,
                contents=["Reply with the single word: OK"],
            )
            assert response.text.strip() != ""
        except ClientError as e:
            if e.code != 429:
                raise
            # 429 rate limit proves the connection and auth work — pass.


@pytest.mark.integration
class TestAnthropicAuth:
    """Verifies that _get_anthropic_client() produces a working client via a live ping."""

    def test_anthropic_key_can_reach_api(self):
        if not _has_anthropic_auth():
            pytest.skip("No Anthropic credentials available")
        import anthropic as _anthropic
        client, model = _get_anthropic_client()
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=256,
                messages=[{"role": "user", "content": "reply ok"}],
            )
            text = next((b.text for b in msg.content if hasattr(b, "text")), None)
            assert text is not None and text.strip() != ""
        except _anthropic.RateLimitError:
            # 429 proves the connection and auth work — pass.
            pass


@pytest.mark.integration
@pytest.mark.skipif(not REAL_PDF.exists(), reason="test PDF not found on disk")
class TestRealPDF:
    def test_extract_images_zero_without_vision(self, tmp_path):
        count = extract_pdf_images(str(REAL_PDF), str(tmp_path))
        assert count == 0

    def test_images_dir_empty_without_vision(self, tmp_path):
        extract_pdf_images(str(REAL_PDF), str(tmp_path))
        images_dir = tmp_path / "images"
        assert images_dir.exists()
        assert list(images_dir.iterdir()) == []

    def test_generate_markdown_creates_file(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        assert Path(md_path).exists()
        assert Path(md_path).stat().st_size > 0

    def test_markdown_has_no_spurious_page_images(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        assert "![fig" not in Path(md_path).read_text()

    def test_markdown_contains_ocr_text(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        assert "FRAGMENTATION" in Path(md_path).read_text().upper()

    def test_markdown_contains_heading(self, tmp_path):
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path))
        lines = Path(md_path).read_text().splitlines()
        assert any(line.startswith("#") for line in lines)

    def test_generate_markdown_with_vision(self, tmp_path):
        """Live Google vision call — sends all pages combined in one request.

        ADA462991.pdf is a fragmentation report with equations. The heuristic
        path reads the OCR text layer but cannot produce LaTeX — it has no math
        fonts or Unicode math density to trigger _block_is_formula. Presence of
        $$ or $ in the output therefore proves vision ran and extracted math.
        """
        if not _has_google_auth():
            pytest.skip("No GOOGLE_API_KEY available")
        md_path = generate_markdown(str(REAL_PDF), str(tmp_path), analyze_formulas=True)
        content = Path(md_path).read_text()
        has_display_math = "$$" in content
        has_inline_math = bool(re.search(r'\$[^$]+\$', content))
        assert has_display_math or has_inline_math, (
            "Vision extraction should produce LaTeX math from this equations-heavy PDF; "
            "got none — vision may have fallen back to heuristic for all pages"
        )

    def test_ocrd_pdf_passes_scanned_check(self):
        doc = fitz.open(str(REAL_PDF))
        _assert_not_scanned(doc)

    def test_all_pages_are_image_based(self):
        doc = fitz.open(str(REAL_PDF))
        assert all(_page_is_image_based(doc[i]) for i in range(len(doc)))
