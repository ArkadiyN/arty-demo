"""Verify tables/bill-of-material.csv against page 16 of the 105mm M1
manufacture document, cell by cell, and render the page for a human to look at.

Consumer: doc-reference/ww2-shells/ordnance-105mm-m1-1940/card.md and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 15.

This is the transcription-fidelity gate that the closure invariant beside the
CSV cannot provide. The invariant proves the two amount columns are internally
consistent; it says nothing about whether "Gilding Metal" was transcribed as
"Gliding Metal" or spec 3-67 as 3-87 -- both of which the prior card.md did.
This page happens to carry a real text layer, so every cell can be checked
against it verbatim rather than by eye.

SKIPs cleanly when source.pdf is absent: doc-reference/**/*.pdf is gitignored
(.gitignore:58), so the scan sits beside its extraction but is never committed.
Re-acquire from https://www.bulletpicker.com/pdf/Shell-HE-105mm-M1.pdf .

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/ordnance-105mm-bom-page-fidelity.py [--render]
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/ww2-shells/ordnance-105mm-m1-1940"
PDF = DOC / "source.pdf"
CSV = DOC / "tables/bill-of-material.csv"
PAGE = 16  # 1-based pdf page; document page 7, anchor "BILL OF MATERIAL"

# Cells whose exact spelling matters and which are not worth reconstructing
# from the CSV: the page header words that define what the amount columns mean,
# and the anchors the citations use.
REQUIRED_ON_PAGE = [
    "BILL OF MATERIAL",
    "MACHINING SHELL, H.E., 105 MM.",
    "AVERAGE \nAMOUNT \nOF MATERIAL \nPER SHELL",
    "AMOUNT OF \nMATERIAL PER \n100,000 SHELL",
]


def norm(text):
    """Collapse whitespace so the page's line breaks do not defeat a match."""
    return re.sub(r"\s+", " ", text).strip()


def main():
    if not PDF.exists():
        print(f"SKIP: {PDF} absent (retained scan, not committed).")
        return 0

    import fitz

    doc = fitz.open(PDF)
    page = doc[PAGE - 1]
    raw = page.get_text()
    flat = norm(raw)

    if "--render" in sys.argv:
        out = pathlib.Path.cwd() / "105mm-bom-page16.png"
        page.get_pixmap(dpi=300).save(out)
        print(f"rendered {out}")

    failures = []

    for phrase in REQUIRED_ON_PAGE:
        if norm(phrase) not in flat:
            failures.append(f"page 16 is missing the anchor {norm(phrase)!r}")

    with CSV.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Every transcribed cell must appear verbatim on the page. Numeric cells are
    # matched in the page's own printed form (thousands separators, leading '.'
    # on .0852) rather than the CSV's normalised form.
    printed = {"5390000": "5,390,000", "65300": "65,300", "8520": "8,520",
               "0.0852": ".0852"}
    skip_cols = {"commercial_form"}  # wraps across several lines; checked below

    for i, row in enumerate(rows):
        for col, val in row.items():
            if not val or col in skip_cols:
                continue
            needle = printed.get(val, val)
            if norm(needle) not in flat:
                failures.append(f"row {i} ({row['part']}) column {col!r}: "
                                f"{needle!r} does not appear on page 16")

    # commercial_form is reassembled from wrapped lines, so check its tokens.
    for i, row in enumerate(rows):
        for token in row["commercial_form"].split():
            if token and norm(token) not in flat:
                failures.append(f"row {i} ({row['part']}) commercial_form "
                                f"token {token!r} does not appear on page 16")

    # The one cell that reaches shipped code, called out so a future reader sees
    # what this whole file is protecting.
    body = rows[0]
    if (body["material"], body["spec"]) != ("Steel WD-X1335", "57-107"):
        failures.append("the Body, Shell material/spec pair cited at "
                        "src/arty/fragmentation.py has changed in the CSV")

    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s) over {len(rows)} rows")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
