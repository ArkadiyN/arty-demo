"""Flag markdown extractions whose *glyphs* are damaged — and nothing more.

This is a **glyph-level** gate, and a green result is not admissibility. It
cannot see the defect class `.claude/rules/source-data-fidelity.md` exists to
prevent: every digit extracted perfectly and assigned to the wrong row, column,
or table. A clean table of wrong numbers passes here. Admissibility comes from
a closure invariant (`check-table-invariants.py`), never from this script.

Broken glyphs counted: Private Use Area codepoints (U+E000-F8FF), C0 control
characters other than tab/newline/CR/form-feed, and U+FFFD. A font that maps
its unmapped glyphs into the C0 range instead of the PUA used to score zero here
— Gold 2017 carries 61 such characters in its text layer, including the minus
sign that decides an exponent's sign (2026-08-03 finding, fixed 2026-09-26).

**A vision-reconstructed `.md` has already been laundered.** The vision pass
emits well-formed characters whether or not it read them correctly, so scanning
the `.md` alone reports on the reconstruction, not the source. `--text-layer`
closes that gap: for each scanned `.md` it finds the sibling `card.md`, resolves
the blob-store PDF(s) the card cites, and runs the same glyph count on the PDF's
own text layer (`pdftotext`). It reports a PDF with no text layer (a pure scan)
as such, because then the `.md` is a reconstruction and a clean `.md` scan
certifies strictly less. Opt-in, because some blobs are hundreds of MB.

Usage:
    uv run src/utils/scan-extraction-quality.py <file.md>
    uv run src/utils/scan-extraction-quality.py doc-reference/   # default path
    uv run src/utils/scan-extraction-quality.py doc-reference/fragmentation/ --text-layer
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

PUA_START = 0xE000
PUA_END = 0xF8FF
# C0 controls a font can map unmapped glyphs into. Tab, LF, CR are text; FF is
# the page break pdftotext emits between pages.
_BENIGN_CONTROLS = {"\t", "\n", "\r", "\f"}
_REPLACEMENT_CHAR = "�"
_BLOB_RE = re.compile(r"(/mnt/f/Projects/TMP/Docs/[^`\s]+?\.pdf)")
# A text layer with fewer word characters than this per page is treated as absent.
TEXT_LAYER_MIN_CHARS_PER_PAGE = 200
_SYMBOL_RUN_RE = re.compile(r"[-*_=~^]{4,}")
_THEMATIC_BREAK_RE = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
_SHORT_TOKEN_RE = re.compile(r"\b\w{1,2}\b")
_WORD_RE = re.compile(r"\b\w+\b")

# Calibrated against doc-reference/: flags files with PUA (Private Use Area)
# glyphs from broken cmap fonts, runs of suspicious symbol characters outside
# thematic breaks/table separators, or an abnormally high ratio of 1-2 char
# tokens (a symptom of garbled/fragmented word extraction).
SHORT_TOKEN_RATIO_THRESHOLD = 0.42
SHORT_TOKEN_MIN_WORDS = 200
SUSPECT_LINE_THRESHOLD = 3


def _is_broken_glyph(ch):
    o = ord(ch)
    return (
        PUA_START <= o <= PUA_END
        or (o < 0x20 and ch not in _BENIGN_CONTROLS)
        or ch == _REPLACEMENT_CHAR
    )


def glyph_flags(text):
    """Return flags for broken glyphs (PUA, stray C0 controls, U+FFFD) in text."""
    pua = [i for i, ch in enumerate(text) if PUA_START <= ord(ch) <= PUA_END]
    ctrl = [
        i for i, ch in enumerate(text) if _is_broken_glyph(ch) and not PUA_START <= ord(ch) <= PUA_END
    ]
    flags = []
    for label, positions in (("PUA glyphs", pua), ("control/U+FFFD glyphs", ctrl)):
        if positions:
            line = text.count("\n", 0, positions[0]) + 1
            flags.append(f"{label}={len(positions)} first_at_line={line}")
    return flags


def scan_text(text):
    """Return (flags, suspect_lines) for a single document's markdown text."""

    suspect_lines = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not _SYMBOL_RUN_RE.search(line):
            continue
        if _THEMATIC_BREAK_RE.match(line) or _TABLE_SEP_RE.match(line):
            continue
        suspect_lines.append((lineno, line.strip()))

    words = _WORD_RE.findall(text)
    short_tokens = _SHORT_TOKEN_RE.findall(text)
    short_ratio = len(short_tokens) / max(1, len(words))

    flags = glyph_flags(text)
    if len(suspect_lines) > SUSPECT_LINE_THRESHOLD:
        flags.append(f"suspect_symbol_lines={len(suspect_lines)}")
    if short_ratio > SHORT_TOKEN_RATIO_THRESHOLD and len(words) > SHORT_TOKEN_MIN_WORDS:
        flags.append(f"short_token_ratio={short_ratio:.2f}")

    return flags, suspect_lines


def scan_paths(paths):
    """Scan a list of markdown file paths. Returns a report list, sorted worst-first."""
    report = []
    for f in paths:
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text:
            continue
        flags, suspect_lines = scan_text(text)
        if flags:
            report.append((str(f), len(text), flags, suspect_lines[:4]))
    report.sort(key=lambda r: -len(r[2]))
    return report


def blob_pdfs_for(md_path):
    """Blob-store PDFs cited by the card.md next to md_path (existing files only)."""
    card = md_path.parent / "card.md"
    if not card.is_file():
        return []
    found = dict.fromkeys(_BLOB_RE.findall(card.read_text(encoding="utf-8", errors="replace")))
    return [Path(p) for p in found if Path(p).is_file()]


def scan_text_layer(pdf):
    """Return (flags, note) for a PDF's own text layer, via pdftotext."""
    try:
        out = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
            capture_output=True,
            check=True,
            timeout=300,
        ).stdout.decode("utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError) as e:
        return [], f"text layer: unreadable ({e.__class__.__name__})"
    pages = out.count("\f") or 1
    if len(_WORD_RE.findall(out)) * 5 < TEXT_LAYER_MIN_CHARS_PER_PAGE * pages:
        return [], (
            "text layer: none -- the .md is a vision/OCR reconstruction; "
            "a clean .md scan certifies strictly less"
        )
    return glyph_flags(out), None


def scan_text_layers(md_paths):
    """Scan the text layer of each blob PDF cited beside md_paths, once per PDF."""
    report = []
    seen = set()
    for md in md_paths:
        if md.name == "card.md":
            continue
        for pdf in blob_pdfs_for(md):
            if pdf in seen:
                continue
            seen.add(pdf)
            flags, note = scan_text_layer(pdf)
            if flags or note:
                report.append((str(md), str(pdf), flags, note))
    return report


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Scan extracted markdown for signs of broken PDF/XML extraction: "
            "Private Use Area, stray control and U+FFFD glyphs (broken font "
            "cmaps), suspicious symbol-run "
            "lines, and abnormal short-token ratios (fragmented word extraction). "
            "GLYPH-LEVEL ONLY: a clean pass says nothing about whether a number "
            "landed in the right row or column, and is not admissibility -- see "
            "the module docstring and .claude/rules/source-data-fidelity.md."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="doc-reference",
        help="A single .md file or a directory to scan recursively (default: doc-reference/)",
    )
    parser.add_argument(
        "--fail-on-flag",
        action="store_true",
        help="Exit with status 1 if any file is flagged (for use as a pipeline gate).",
    )
    parser.add_argument(
        "--text-layer",
        action="store_true",
        help=(
            "Also glyph-scan the text layer of each blob-store PDF cited by the "
            "sibling card.md (needs pdftotext), and report PDFs with no text layer."
        ),
    )
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file():
        paths = [target]
    else:
        paths = sorted(target.rglob("*.md"))

    report = scan_paths(paths)

    for path, n, flags, samples in report:
        print(f"{path}  ({n} chars)")
        for fl in flags:
            print(f"    {fl}")
        for lineno, line in samples:
            print(f"      L{lineno}: {line[:100]!r}")

    print(f"\n{len(report)} / {len(paths)} file(s) flagged")

    layer_flagged = []
    if args.text_layer:
        layer_report = scan_text_layers(paths)
        print()
        for md, pdf, flags, note in layer_report:
            print(f"{pdf}  (text layer, for {md})")
            for fl in flags:
                print(f"    {fl}")
            if note:
                print(f"    {note}")
        layer_flagged = [r for r in layer_report if r[2]]
        print(
            f"\n{len(layer_flagged)} PDF text layer(s) flagged, "
            f"{len(layer_report) - len(layer_flagged)} without a text layer"
        )

    if args.fail_on_flag and (report or layer_flagged):
        sys.exit(1)


if __name__ == "__main__":
    main()
