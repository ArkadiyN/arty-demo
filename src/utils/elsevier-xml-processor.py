"""
Process an Elsevier full-text XML article: extract figures and generate Markdown.

Usage:
  uv run src/utils/elsevier-xml-processor.py <doi_or_xml_path> [--output-dir <dir>] [--markdown]

Input:
  - A DOI (e.g. 10.1016/j.measurement.2026.120853) — fetches XML from Elsevier API
  - A local .xml file path

Outputs land next to the XML file by default (or ./ for DOI input):
  - images/fig1.jpeg, fig2.jpeg, ...   (article figures, gr* only — not inline math)
  - <stem>.md                          (with --markdown)

Requires ELSEVIER_API_KEY in environment (load from .env before running).
"""

import os
import sys
import re
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Elsevier XML namespaces
# ---------------------------------------------------------------------------
_CE = "http://www.elsevier.com/xml/common/dtd"
_JA = "http://www.elsevier.com/xml/ja/dtd"
_MML = "http://www.w3.org/1998/Math/MathML"
_SVAPI = "http://www.elsevier.com/xml/svapi/article/dtd"
_XLINK = "http://www.w3.org/1999/xlink"
_DC = "http://purl.org/dc/elements/1.1/"
_PRISM = "http://prismstandard.org/namespaces/basic/2.0/"


def _tag(ns, local):
    return f"{{{ns}}}{local}"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------
def _get_api_key():
    key = os.environ.get("ELSEVIER_API_KEY")
    if not key:
        raise SystemExit(
            "Error: ELSEVIER_API_KEY not set.\n"
            "Add it to .env and run: set -a; source .env; set +a"
        )
    return key


def _fetch(url, accept, out_path=None):
    """Fetch a URL with the Elsevier API key; return bytes or write to out_path."""
    import urllib.request

    req = urllib.request.Request(url, headers={
        "X-ELS-APIKey": _get_api_key(),
        "Accept": accept,
    })
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    if out_path:
        out_path.write_bytes(data)
    return data


def fetch_article_xml(doi):
    """Download full-text XML for a DOI; return bytes."""
    url = f"https://api.elsevier.com/content/article/doi/{doi}"
    print(f"Fetching XML for DOI {doi} ...")
    return _fetch(url, "text/xml")


# ---------------------------------------------------------------------------
# XML parsing helpers
# ---------------------------------------------------------------------------
def _local(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def _all_text(el):
    """All text content recursively, whitespace-normalised."""
    return " ".join("".join(el.itertext()).split())


def _find_first(root, *local_names):
    """Return first element whose local name is in local_names (depth-first)."""
    for el in root.iter():
        if _local(el.tag) in local_names:
            return el
    return None


def _find_all(root, local_name):
    return [el for el in root.iter() if _local(el.tag) == local_name]


# ---------------------------------------------------------------------------
# MathML → LaTeX (best-effort)
# ---------------------------------------------------------------------------
_MML_OP_MAP = {
    "−": "-", "×": r"\times", "÷": r"\div",
    "≤": r"\leq", "≥": r"\geq", "≠": r"\neq",
    "∞": r"\infty", "α": r"\alpha", "β": r"\beta",
    "γ": r"\gamma", "δ": r"\delta", "ε": r"\varepsilon",
    "η": r"\eta", "θ": r"\theta", "λ": r"\lambda",
    "μ": r"\mu", "ν": r"\nu", "σ": r"\sigma",
    "τ": r"\tau", "φ": r"\phi", "ω": r"\omega",
    "Ω": r"\Omega", "Σ": r"\Sigma", "∂": r"\partial",
    "√": r"\sqrt", "∇": r"\nabla", "∫": r"\int",
    "∑": r"\sum", "∏": r"\prod",
}


def _mml_text(el):
    """Recursively render MathML element to a LaTeX-like string."""
    tag = _local(el.tag)
    children = list(el)
    text = (el.text or "").strip()

    def sub(c):
        return _mml_text(c)

    if tag in ("mi", "mn", "mo", "mtext"):
        t = text
        for uni, latex in _MML_OP_MAP.items():
            t = t.replace(uni, latex)
        return t
    if tag == "msup":
        base, exp = (sub(children[0]), sub(children[1])) if len(children) >= 2 else (text, "?")
        return f"{base}^{{{exp}}}"
    if tag == "msub":
        base, sub_ = (sub(children[0]), sub(children[1])) if len(children) >= 2 else (text, "?")
        return f"{base}_{{{sub_}}}"
    if tag == "msubsup":
        if len(children) >= 3:
            return f"{sub(children[0])}_{{{sub(children[1])}}}^{{{sub(children[2])}}}"
    if tag == "mfrac":
        if len(children) >= 2:
            return r"\frac{" + sub(children[0]) + "}{" + sub(children[1]) + "}"
    if tag == "msqrt":
        inner = " ".join(sub(c) for c in children)
        return r"\sqrt{" + inner + "}"
    if tag == "mrow":
        return " ".join(sub(c) for c in children)
    if tag == "math":
        return " ".join(sub(c) for c in children)
    # fallback: concatenate all text
    return _all_text(el)


def _formula_to_latex(formula_el):
    """Convert a <ce:formula> or <mml:math> element to a LaTeX string."""
    math_el = None
    for child in formula_el.iter():
        if _local(child.tag) == "math":
            math_el = child
            break
    if math_el is None:
        return _all_text(formula_el).strip()
    return _mml_text(math_el).strip()


# ---------------------------------------------------------------------------
# Article metadata extraction
# ---------------------------------------------------------------------------
def _extract_metadata(root):
    """Return dict with title, doi, pii, journal, date, authors, keywords, abstract."""
    meta = {}

    # coredata (SVAPI namespace)
    for cd in root.iter(_tag(_SVAPI, "coredata")):
        for child in cd:
            loc = _local(child.tag)
            if loc == "title":
                meta["title"] = (child.text or "").strip()
            elif loc == "doi":
                meta["doi"] = (child.text or "").strip()
            elif loc == "pii":
                meta["pii"] = (child.text or "").strip().replace("-", "").replace("(", "").replace(")", "")
            elif loc == "publicationName":
                meta["journal"] = (child.text or "").strip()
            elif loc == "coverDate":
                meta["date"] = (child.text or "").strip()

    # authors: scope to ja:head/ce:author-group only (avoid bibliography authors)
    authors = []
    head = _find_first(root, "head")
    author_group = _find_first(head, "author-group") if head is not None else None
    if author_group is not None:
        for author in _find_all(author_group, "author"):
            given = _find_first(author, "given-name")
            surname = _find_first(author, "surname")
            if surname is not None:
                name = ((given.text or "").strip() + " ") if given is not None else ""
                name += (surname.text or "").strip()
                if name.strip():
                    authors.append(name.strip())
    meta["authors"] = authors

    # keywords
    kws = []
    for kw in _find_all(root, "keyword"):
        txt = _all_text(kw).strip()
        if txt:
            kws.append(txt)
    meta["keywords"] = kws

    # abstract
    for ab in _find_all(root, "abstract"):
        txt = _all_text(ab).strip()
        if txt:
            meta["abstract"] = txt
            break

    return meta


# ---------------------------------------------------------------------------
# Figure inventory
# ---------------------------------------------------------------------------
def _figure_inventory(root):
    """Return list of dicts: {label, ref, ext, caption} for each ce:figure."""
    # object metadata: ref → category → attrs
    obj_meta = {}
    for obj in root.iter(_tag(_SVAPI, "object")):
        ref = obj.get("ref", "")
        cat = obj.get("category", "")
        if ref not in obj_meta:
            obj_meta[ref] = {}
        obj_meta[ref][cat] = obj.attrib

    # PII for building image URLs
    pii_raw = ""
    for cd in root.iter(_tag(_SVAPI, "coredata")):
        for child in cd:
            if _local(child.tag) == "pii":
                pii_raw = (child.text or "").strip().replace("-", "").replace("(", "").replace(")", "")
                break

    figures = []
    for fig in _find_all(root, "figure"):
        label_el = _find_first(fig, "label")
        label = _all_text(label_el).strip() if label_el is not None else ""
        caption_el = _find_first(fig, "caption")
        caption = _all_text(caption_el).strip() if caption_el is not None else ""

        # link element carries the locator (gr1, gr2 …)
        link_el = _find_first(fig, "link")
        if link_el is None:
            continue
        ref = link_el.get("locator", "")
        if not ref:
            # try xlink:href: "pii:PII/grN"
            href = link_el.get(_tag(_XLINK, "href"), "")
            ref = href.split("/")[-1] if "/" in href else ""
        if not ref:
            continue

        # pick standard (downsampled) JPEG if available
        ext = "jpeg"
        if ref in obj_meta:
            for cat_pref in ("standard", "high", "thumbnail"):
                if cat_pref in obj_meta[ref]:
                    mime = obj_meta[ref][cat_pref].get("mimetype", "")
                    ext = mime.split("/")[-1] if "/" in mime else ext
                    if ext == "gif":
                        ext = "jpeg"  # prefer jpeg; fall back below if needed
                    break

        figures.append({
            "label": label,
            "fig_id": fig.get("id", ""),   # e.g. "fig1" — used by float-anchor refid
            "ref": ref,                     # e.g. "gr1"  — used for image URL
            "ext": ext,
            "pii": pii_raw,
            "caption": caption,
        })

    return figures


# ---------------------------------------------------------------------------
# Image download
# ---------------------------------------------------------------------------
def _download_figures(figures, images_dir):
    """Fetch figure images; return (ref→filename, fig_id→filename) maps."""
    images_dir.mkdir(parents=True, exist_ok=True)
    ref_to_name = {}
    figid_to_name = {}
    counter = 0
    for fig in figures:
        ref = fig["ref"]
        pii = fig["pii"]
        if ref in ref_to_name:
            continue
        counter += 1
        out_name = f"fig{counter}.jpeg"
        out_path = images_dir / out_name
        url = f"https://api.elsevier.com/content/object/eid/1-s2.0-{pii}-{ref}.jpg"
        try:
            _fetch(url, "image/jpeg", out_path)
            ref_to_name[ref] = out_name
            if fig.get("fig_id"):
                figid_to_name[fig["fig_id"]] = out_name
            print(f"  Saved: images/{out_name}  ({fig['label']})")
        except Exception as exc:
            print(f"  Skipped {ref}: {exc}")
    return ref_to_name, figid_to_name


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------
def _section_to_md(section_el, depth=2, figid_to_name=None):
    """Recursively render a <ce:section> to markdown lines."""
    if figid_to_name is None:
        figid_to_name = {}
    lines = []
    prefix = "#" * depth

    for child in section_el:
        loc = _local(child.tag)

        if loc == "section-title":
            label_el = section_el.find(_tag(_CE, "label"))
            label = (_all_text(label_el) + " ") if label_el is not None else ""
            heading = _all_text(child).strip()
            if heading:
                lines.append(f"{prefix} {label}{heading}")

        elif loc == "label":
            pass  # consumed above

        elif loc == "para":
            para = _para_to_md(child, figid_to_name)
            if para:
                lines.append(para)

        elif loc == "section":
            lines.extend(_section_to_md(child, depth + 1, figid_to_name))

        elif loc == "display":
            for formula in _find_all(child, "formula"):
                lbl_el = _find_first(formula, "label")
                lbl = f"  \\quad ({_all_text(lbl_el)})" if lbl_el is not None else ""
                latex = _formula_to_latex(formula)
                if latex:
                    lines.append(f"$$\n{latex}{lbl}\n$$")

        elif loc == "float-anchor":
            fig_id = child.get("refid", "")
            if fig_id in figid_to_name:
                lines.append(f"![{fig_id}](images/{figid_to_name[fig_id]})")

        elif loc in ("list",):
            for item in _find_all(child, "list-item"):
                para = _find_first(item, "para")
                txt = _para_to_md(para, figid_to_name) if para is not None else _all_text(item)
                lines.append(f"- {txt}")

    lines.append("")
    return lines


def _para_to_md(para_el, figid_to_name):
    """Render a <ce:para> to a markdown string (inline math preserved)."""
    parts = []

    def visit(el):
        loc = _local(el.tag)
        if loc == "math":
            latex = _mml_text(el).strip()
            parts.append(f"${latex}$" if latex else "")
            return
        if loc == "display":
            for formula in _find_all(el, "formula"):
                latex = _formula_to_latex(formula)
                if latex:
                    parts.append(f"\n$$\n{latex}\n$$\n")
            return
        if loc == "float-anchor":
            fig_id = el.get("refid", "")
            if fig_id in figid_to_name:
                parts.append(f"\n![{fig_id}](images/{figid_to_name[fig_id]})\n")
            return
        if el.text:
            parts.append(el.text)
        for child in el:
            visit(child)
            if child.tail:
                parts.append(child.tail)

    if para_el.text:
        parts.append(para_el.text)
    for child in para_el:
        visit(child)
        if child.tail:
            parts.append(child.tail)

    return " ".join(" ".join(parts).split()).strip()


def _references_to_md(root):
    """Render bibliography as a numbered list."""
    lines = ["## References", ""]
    for bib in _find_all(root, "bib-reference"):
        label_el = _find_first(bib, "label")
        label = _all_text(label_el).strip() if label_el is not None else ""
        src_el = _find_first(bib, "source-text")
        text = _all_text(src_el).strip() if src_el is not None else _all_text(bib).strip()
        if text:
            lines.append(f"{label}. {text}" if label else f"- {text}")
    lines.append("")
    return lines


def _build_markdown(root, meta, figid_to_name):
    """Assemble full article markdown."""
    lines = []

    # --- Front matter ---
    lines.append(f"# {meta.get('title', 'Untitled')}")
    lines.append("")
    if meta.get("authors"):
        lines.append("**Authors:** " + "; ".join(meta["authors"]))
    if meta.get("journal"):
        lines.append(f"**Journal:** {meta['journal']}")
    if meta.get("date"):
        lines.append(f"**Date:** {meta['date']}")
    if meta.get("doi"):
        lines.append(f"**DOI:** [{meta['doi']}](https://doi.org/{meta['doi']})")
    lines.append("")

    # --- Abstract ---
    if meta.get("abstract"):
        lines.append("## Abstract")
        lines.append("")
        lines.append(meta["abstract"])
        lines.append("")

    # --- Keywords ---
    if meta.get("keywords"):
        lines.append(f"**Keywords:** {', '.join(meta['keywords'])}")
        lines.append("")

    # --- Body sections ---
    body = _find_first(root, "body")
    if body is not None:
        for sec in _find_all(body, "section"):
            lines.extend(_section_to_md(sec, depth=2, figid_to_name=figid_to_name))

    # --- References ---
    lines.extend(_references_to_md(root))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API (mirrors pdf-processor)
# ---------------------------------------------------------------------------
def extract_article_images(xml_path, output_dir):
    """Extract figure images from an Elsevier XML file."""
    root = ET.parse(xml_path).getroot()
    print(f"Opened XML: {xml_path}")
    figures = _figure_inventory(root)
    print(f"  Found {len(figures)} figures: {[f['ref'] for f in figures]}")
    images_dir = Path(output_dir) / "images"
    ref_to_name, _ = _download_figures(figures, images_dir)
    count = len(ref_to_name)
    print(f"\nDone. Extracted {count} figures to {images_dir}")
    return count


def generate_markdown(xml_path, output_dir):
    """Extract figures and generate markdown from an Elsevier XML file."""
    root = ET.parse(xml_path).getroot()
    stem = Path(xml_path).stem
    print(f"Opened XML: {xml_path}")

    meta = _extract_metadata(root)
    print(f"  Title: {meta.get('title', '?')}")
    print(f"  Authors: {', '.join(meta.get('authors', []))}")

    figures = _figure_inventory(root)
    print(f"  Found {len(figures)} figures: {[f['ref'] for f in figures]}")

    images_dir = Path(output_dir) / "images"
    ref_to_name, figid_to_name = _download_figures(figures, images_dir)

    md_path = Path(output_dir) / f"{stem}.md"
    md = _build_markdown(root, meta, figid_to_name)
    md_path.write_text(md, encoding="utf-8")

    print(f"\nDone. {len(ref_to_name)} figures extracted, markdown written to {md_path}")
    return str(md_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Process an Elsevier XML article: extract figures and generate Markdown."
    )
    parser.add_argument(
        "source",
        help="DOI (e.g. 10.1016/j.foo.2026.123) or path to a local .xml file",
    )
    parser.add_argument(
        "--output-dir", "-o", default=None,
        help="Output directory (default: same directory as the XML file, or ./ for DOI input)",
    )
    parser.add_argument(
        "--markdown", "-m", action="store_true",
        help="Generate a .md file with LaTeX formulas and image references",
    )
    args = parser.parse_args()

    src = args.source

    # Determine whether input is a DOI or a local file
    if os.path.exists(src):
        xml_path = src
        output_dir = args.output_dir or os.path.dirname(os.path.abspath(src))
    else:
        # Treat as DOI — fetch and cache next to cwd
        doi = src.removeprefix("doi:").strip()
        safe = re.sub(r"[^\w\-.]", "_", doi)
        xml_path = f"{safe}.xml"
        raw = fetch_article_xml(doi)
        Path(xml_path).write_bytes(raw)
        print(f"  Saved XML to {xml_path}")
        output_dir = args.output_dir or os.getcwd()

    if not os.path.exists(xml_path):
        print(f"Error: '{xml_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.markdown:
        generate_markdown(xml_path, output_dir)
    else:
        extract_article_images(xml_path, output_dir)


if __name__ == "__main__":
    main()
