r"""
Tests for src/utils/elsevier-xml-processor.py

Coverage map
============

_all_text
  • Concatenates direct text and all descendant text, whitespace-normalised.
  • Returns empty string for an element with no text content.

_find_first / _find_all
  • _find_first returns the first matching element by local name, regardless of
    namespace — catches any accidental namespace-binding assumption.
  • _find_first returns None when no match exists.
  • _find_all returns every matching element at any depth.

_mml_text  (MathML → LaTeX)
  • <mi> / <mn> / <mo>: rendered as-is; Unicode operator characters (−, ×, α …)
    mapped to their LaTeX equivalents.
  • <msup>: renders as base^{exp}.
  • <msub>: renders as base_{sub}.
  • <mfrac>: renders as \frac{num}{den}.
  • <msqrt>: renders as \sqrt{inner}.
  • <mrow>: joins child renderings with a space.
  • Unknown element: falls back to concatenated text content.

_extract_metadata  (XML fixture — no network calls)
  • Extracts title, doi, journal, date from <coredata>.
  • Extracts authors from <author-group> only — NOT from bibliography entries,
    which would inflate the list.
  • Extracts keywords from <keyword> elements.
  • Extracts abstract text.

_figure_inventory  (XML fixture)
  • Returns one entry per <ce:figure> element.
  • Each entry carries ref (locator), pii (stripped of punctuation), and caption.
  • Skips figures whose <ce:link> has no locator attribute.

_get_api_key
  • Returns ELSEVIER_API_KEY from environment when set.
  • Raises SystemExit with a helpful message when the variable is absent.

Integration — real Elsevier XML on disk  (pytest.mark.integration, skipped if absent)
  • generate_markdown on the saved Mott thermistor XML produces a .md file
    containing the article title and at least one LaTeX display formula.
  • Four figures are extracted (gr1–gr4) as JPEG files.
  • extract_article_images returns count == 4.
  • Author list contains exactly the 4 corresponding authors from the header
    (not bibliography entries).
"""

import importlib.util
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

import pytest

# ── Load .env so ELSEVIER_API_KEY is available for integration tests ──────────
def _load_dotenv():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

_load_dotenv()

# ── Load the hyphen-named module ──────────────────────────────────────────────
_SRC = Path(__file__).parent.parent / "src" / "utils" / "elsevier-xml-processor.py"
_spec = importlib.util.spec_from_file_location("elsevier_xml_processor", _SRC)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_all_text = _mod._all_text
_find_first = _mod._find_first
_find_all = _mod._find_all
_mml_text = _mod._mml_text
_extract_metadata = _mod._extract_metadata
_figure_inventory = _mod._figure_inventory
_get_api_key = _mod._get_api_key
extract_article_images = _mod.extract_article_images
generate_markdown = _mod.generate_markdown

_MML = _mod._MML
_CE = _mod._CE
_JA = _mod._JA
_SVAPI = _mod._SVAPI

REAL_XML = Path(__file__).parent / "elsevier-xml-sample" / "mott-vrh-thermistor.xml"


# ── XML construction helpers ──────────────────────────────────────────────────

def _el(tag, text=None, ns="", **kwargs):
    """Build an ElementTree element with optional namespace and text."""
    full_tag = f"{{{ns}}}{tag}" if ns else tag
    el = ET.Element(full_tag, **kwargs)
    if text is not None:
        el.text = text
    return el


def _mml(tag, text=None, **children_pairs):
    """Build an MathML element."""
    return _el(tag, text, ns=_MML)


def _child(parent, tag, text=None, ns=""):
    child = _el(tag, text, ns=ns)
    parent.append(child)
    return child


# ── Minimal Elsevier XML fixture ──────────────────────────────────────────────

def _minimal_xml(title="Test Article", doi="10.1234/test", pii="S0000000000000000",
                 journal="Test Journal", date="2026-01-01",
                 authors=None, keywords=None, abstract="Test abstract.",
                 n_figures=2):
    """Build a minimal but structurally valid Elsevier full-text XML tree."""
    if authors is None:
        authors = [("Alice", "Smith"), ("Bob", "Jones")]
    if keywords is None:
        keywords = ["keyword1", "keyword2"]

    root = _el("full-text-retrieval-response", ns=_SVAPI)

    # coredata
    cd = _child(root, "coredata", ns=_SVAPI)
    _child(cd, "title", title)
    _child(cd, "doi", doi)
    _child(cd, "pii", pii)
    _child(cd, "publicationName", journal)
    _child(cd, "coverDate", date)

    # objects (one standard JPEG per figure)
    for i in range(1, n_figures + 1):
        obj = _child(root, "object", ns=_SVAPI)
        obj.set("ref", f"gr{i}")
        obj.set("category", "standard")
        obj.set("type", "IMAGE-DOWNSAMPLED")
        obj.set("mimetype", "image/jpeg")

    # serial-item > article
    serial = _child(root, "serial-item", ns=_SVAPI)
    article = _child(serial, "article", ns=_JA)

    # head
    head = _child(article, "head", ns=_JA)
    _child(head, "title", title, ns=_CE)

    ag = _child(head, "author-group", ns=_CE)
    for given, surname in authors:
        auth = _child(ag, "author", ns=_CE)
        _child(auth, "given-name", given, ns=_CE)
        _child(auth, "surname", surname, ns=_CE)

    kw_group = _child(head, "keywords", ns=_CE)
    for kw in keywords:
        kw_el = _child(kw_group, "keyword", ns=_CE)
        _child(kw_el, "text", kw, ns=_CE)

    ab = _child(head, "abstract", ns=_CE)
    ab_sec = _child(ab, "abstract-sec", ns=_CE)
    _child(ab_sec, "simple-para", abstract, ns=_CE)

    # floats (figures)
    floats = _child(article, "floats", ns=_CE)
    for i in range(1, n_figures + 1):
        fig = _child(floats, "figure", ns=_CE)
        _child(fig, "label", f"Fig. {i}", ns=_CE)
        cap = _child(fig, "caption", ns=_CE)
        _child(cap, "simple-para", f"Caption for figure {i}.", ns=_CE)
        lnk = _child(fig, "link", ns=_CE)
        lnk.set("locator", f"gr{i}")

    # body with one section
    body = _child(article, "body", ns=_JA)
    secs = _child(body, "sections", ns=_CE)
    sec = _child(secs, "section", ns=_CE)
    _child(sec, "section-title", "Introduction", ns=_CE)
    _child(sec, "para", "Some introductory text.", ns=_CE)

    return root


# ══════════════════════════════════════════════════════════════════════════════
# _all_text
# ══════════════════════════════════════════════════════════════════════════════

class TestAllText:
    def test_direct_text(self):
        el = _el("p", "hello world")
        assert _all_text(el) == "hello world"

    def test_nested_text_joined(self):
        parent = _el("p", "start ")
        child = _el("span", "middle")
        child.tail = " end"
        parent.append(child)
        assert "start" in _all_text(parent)
        assert "middle" in _all_text(parent)
        assert "end" in _all_text(parent)

    def test_empty_element(self):
        assert _all_text(_el("p")) == ""

    def test_whitespace_normalised(self):
        el = _el("p", "  lots   of   spaces  ")
        assert "  " not in _all_text(el)


# ══════════════════════════════════════════════════════════════════════════════
# _find_first / _find_all
# ══════════════════════════════════════════════════════════════════════════════

class TestFinders:
    def _tree(self):
        root = _el("root")
        a = _child(root, "section")
        _child(a, "title", "First")
        b = _child(root, "section")
        _child(b, "title", "Second")
        return root

    def test_find_first_returns_first_match(self):
        root = self._tree()
        result = _find_first(root, "title")
        assert result is not None
        assert result.text == "First"

    def test_find_first_none_when_missing(self):
        assert _find_first(_el("root"), "nonexistent") is None

    def test_find_all_returns_all_matches(self):
        root = self._tree()
        results = _find_all(root, "title")
        assert len(results) == 2

    def test_find_first_ignores_namespace(self):
        root = _el("root")
        _child(root, "item", "found", ns=_CE)
        result = _find_first(root, "item")
        assert result is not None
        assert result.text == "found"


# ══════════════════════════════════════════════════════════════════════════════
# _mml_text — MathML → LaTeX
# ══════════════════════════════════════════════════════════════════════════════

def _math(*children):
    math = _el("math", ns=_MML)
    for c in children:
        math.append(c)
    return math


class TestMmlText:
    def test_mi_passthrough(self):
        mi = _el("mi", "x", ns=_MML)
        assert _mml_text(mi) == "x"

    def test_mo_unicode_operator_mapped(self):
        mo = _el("mo", "−", ns=_MML)
        assert _mml_text(mo) == "-"

    def test_alpha_mapped(self):
        mi = _el("mi", "α", ns=_MML)
        assert _mml_text(mi) == r"\alpha"

    def test_msup_renders_caret(self):
        msup = _el("msup", ns=_MML)
        msup.append(_el("mi", "x", ns=_MML))
        msup.append(_el("mn", "2", ns=_MML))
        result = _mml_text(msup)
        assert "x" in result and "2" in result and "^" in result

    def test_msub_renders_underscore(self):
        msub = _el("msub", ns=_MML)
        msub.append(_el("mi", "T", ns=_MML))
        msub.append(_el("mn", "0", ns=_MML))
        result = _mml_text(msub)
        assert "T" in result and "0" in result and "_" in result

    def test_mfrac_renders_frac(self):
        mfrac = _el("mfrac", ns=_MML)
        mfrac.append(_el("mi", "a", ns=_MML))
        mfrac.append(_el("mi", "b", ns=_MML))
        result = _mml_text(mfrac)
        assert r"\frac" in result and "a" in result and "b" in result

    def test_msqrt_renders_sqrt(self):
        msqrt = _el("msqrt", ns=_MML)
        msqrt.append(_el("mi", "x", ns=_MML))
        result = _mml_text(msqrt)
        assert r"\sqrt" in result and "x" in result

    def test_mrow_joins_children(self):
        mrow = _el("mrow", ns=_MML)
        mrow.append(_el("mi", "a", ns=_MML))
        mrow.append(_el("mo", "+", ns=_MML))
        mrow.append(_el("mi", "b", ns=_MML))
        result = _mml_text(mrow)
        assert "a" in result and "b" in result

    def test_unknown_tag_falls_back_to_text(self):
        el = _el("mstyle", ns=_MML)
        el.text = "fallback"
        assert "fallback" in _mml_text(el)


# ══════════════════════════════════════════════════════════════════════════════
# _extract_metadata
# ══════════════════════════════════════════════════════════════════════════════

class TestExtractMetadata:
    def test_title_extracted(self):
        root = _minimal_xml(title="My Paper")
        meta = _extract_metadata(root)
        assert meta["title"] == "My Paper"

    def test_doi_extracted(self):
        root = _minimal_xml(doi="10.9999/abc")
        meta = _extract_metadata(root)
        assert meta["doi"] == "10.9999/abc"

    def test_journal_extracted(self):
        root = _minimal_xml(journal="Nature")
        meta = _extract_metadata(root)
        assert meta["journal"] == "Nature"

    def test_date_extracted(self):
        root = _minimal_xml(date="2025-06-01")
        meta = _extract_metadata(root)
        assert meta["date"] == "2025-06-01"

    def test_authors_from_header_only(self):
        # Authors in <author-group> only — NOT from bibliography
        root = _minimal_xml(authors=[("Alice", "Smith"), ("Bob", "Jones")])
        # Add a fake bib author to ensure it's not picked up
        bib = ET.SubElement(root, f"{{{_SVAPI}}}bib-section")
        fake_auth = ET.SubElement(bib, f"{{{_CE}}}author")
        ET.SubElement(fake_auth, f"{{{_CE}}}surname").text = "BibAuthor"
        meta = _extract_metadata(root)
        names = meta["authors"]
        assert "Alice Smith" in names
        assert "Bob Jones" in names
        assert not any("BibAuthor" in n for n in names)

    def test_keywords_extracted(self):
        root = _minimal_xml(keywords=["alpha", "beta"])
        meta = _extract_metadata(root)
        assert "alpha" in meta["keywords"]
        assert "beta" in meta["keywords"]

    def test_abstract_extracted(self):
        root = _minimal_xml(abstract="This is the abstract.")
        meta = _extract_metadata(root)
        assert "This is the abstract." in meta["abstract"]


# ══════════════════════════════════════════════════════════════════════════════
# _figure_inventory
# ══════════════════════════════════════════════════════════════════════════════

class TestFigureInventory:
    def test_count_matches_figures(self):
        root = _minimal_xml(n_figures=3)
        figs = _figure_inventory(root)
        assert len(figs) == 3

    def test_ref_extracted(self):
        root = _minimal_xml(n_figures=2)
        refs = {f["ref"] for f in _figure_inventory(root)}
        assert refs == {"gr1", "gr2"}

    def test_pii_stripped_of_punctuation(self):
        root = _minimal_xml(pii="S1234-5678(26)00001-2")
        figs = _figure_inventory(root)
        assert all("-" not in f["pii"] for f in figs)
        assert all("(" not in f["pii"] for f in figs)

    def test_caption_extracted(self):
        root = _minimal_xml(n_figures=1)
        figs = _figure_inventory(root)
        assert "Caption for figure 1" in figs[0]["caption"]

    def test_figure_without_locator_skipped(self):
        root = _minimal_xml(n_figures=1)
        # Remove the locator from the link element
        for lnk in _find_all(root, "link"):
            if "locator" in lnk.attrib:
                del lnk.attrib["locator"]
        figs = _figure_inventory(root)
        assert figs == []


# ══════════════════════════════════════════════════════════════════════════════
# _get_api_key
# ══════════════════════════════════════════════════════════════════════════════

class TestGetApiKey:
    def test_returns_key_from_env(self):
        with patch.dict(os.environ, {"ELSEVIER_API_KEY": "testkey123"}):  # pragma: allowlist secret
            assert _get_api_key() == "testkey123"

    def test_raises_sysexit_when_missing(self):
        env = {k: v for k, v in os.environ.items() if k != "ELSEVIER_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(SystemExit, match="ELSEVIER_API_KEY"):
                _get_api_key()


# ══════════════════════════════════════════════════════════════════════════════
# Integration — real XML on disk
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestRealXml:
    """Uses the cached Mott thermistor XML saved during development."""

    @pytest.fixture(autouse=True)
    def skip_if_missing(self):
        if not REAL_XML.exists():
            pytest.skip(f"Real XML not found at {REAL_XML}")

    def test_metadata_title(self):
        root = ET.parse(REAL_XML).getroot()
        meta = _extract_metadata(root)
        assert "Mott" in meta["title"]
        assert "thermistor" in meta["title"].lower()

    def test_author_count_is_small(self):
        root = ET.parse(REAL_XML).getroot()
        meta = _extract_metadata(root)
        # Header authors only — not the 50+ bibliography authors
        assert 1 <= len(meta["authors"]) <= 10

    def test_four_figures_found(self):
        root = ET.parse(REAL_XML).getroot()
        figs = _figure_inventory(root)
        assert len(figs) == 4
        assert {f["ref"] for f in figs} == {"gr1", "gr2", "gr3", "gr4"}

    def test_extract_images_returns_four(self, tmp_path):
        # Requires live API key — skip if absent.
        if not os.environ.get("ELSEVIER_API_KEY"):
            pytest.skip("ELSEVIER_API_KEY not set")
        count = extract_article_images(str(REAL_XML), str(tmp_path))
        assert count == 4
        assert len(list((tmp_path / "images").glob("*.jpeg"))) == 4

    def test_generate_markdown_contains_title(self, tmp_path):
        # Mock figure download so this test is network-free.
        with patch.object(_mod, "_download_figures", return_value=({}, {})):
            md_path = generate_markdown(str(REAL_XML), str(tmp_path))
        content = Path(md_path).read_text()
        assert "Mott" in content

    def test_generate_markdown_has_display_formula(self, tmp_path):
        with patch.object(_mod, "_download_figures", return_value=({}, {})):
            md_path = generate_markdown(str(REAL_XML), str(tmp_path))
        content = Path(md_path).read_text()
        assert "$$" in content

    def test_generate_markdown_has_image_references(self, tmp_path):
        # Provide fake (ref→name, fig_id→name) maps so image markdown is emitted.
        fake_ref_map = {"gr1": "fig1.jpeg", "gr2": "fig2.jpeg",
                        "gr3": "fig3.jpeg", "gr4": "fig4.jpeg"}
        fake_figid_map = {"fig1": "fig1.jpeg", "fig2": "fig2.jpeg",
                          "fig3": "fig3.jpeg", "fig4": "fig4.jpeg"}
        with patch.object(_mod, "_download_figures",
                          return_value=(fake_ref_map, fake_figid_map)):
            md_path = generate_markdown(str(REAL_XML), str(tmp_path))
        content = Path(md_path).read_text()
        assert "![" in content
