"""Re-extract Ammunition Series 6 table 6-1 from the scan and diff it against the CSV.

Consumer: doc-reference/ww2-shells/ammunition-series-6-wdss-specs/
{card.md, tables/table-6-1-chemical-requirements.csv} and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 19.

WHY THIS EXISTS RATHER THAN A CLOSURE INVARIANT.  Table 6-1 is a chemical
specification -- six steel grades x five elements, each cell a range or a
maximum.  There is no arithmetic relation among its cells, so
.claude/rules/source-data-fidelity.md's closure invariant has nothing to close
on; the only internal regularity is that the phosphorus column is constant down
all six rows, which the .invariant file checks and which is far too weak on its
own.  Under that rule the table would be "flagged for human review".

It does not need to be, because this scan is the rare case where the stronger
check is available: the PDF carries a clean embedded text layer that renders the
table cell-for-cell, so fidelity can be settled by EXACT MACHINE COMPARISON
against the page rather than inferred from arithmetic.  That is strictly better
than a closure for the failure mode the rule targets -- every digit right,
assigned to the wrong row or column -- because it compares position as well as
value.

What this script does NOT establish is criterion match (does the model consume
the quantity this table tabulates?).  That is @model-reviewer's gate.

The CSV it checks was itself written by this script's --emit mode, through the
same parser, so no digit in it was ever hand-typed
(.claude/rules/source-data-fidelity.md, "Numbers are extracted once").

Requires the retained scan, which is gitignored (.gitignore:58); re-acquire as
DTIC AD830266 (AMCP 706-249, July 1964).  Absent it, the script reports skipped
rather than passing.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/ammunition-series-6-table-6-1-fidelity.py
    uv run python .../ammunition-series-6-table-6-1-fidelity.py --emit   # regenerate the CSV
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/ww2-shells/ammunition-series-6-wdss-specs"
PDF = DOC / "source.pdf"
TABLE = DOC / "tables/table-6-1-chemical-requirements.csv"

# Table 6-1 sits alone on pdf page 11 (0-indexed); sect. 6-14, which introduces
# it, is on pdf page 10.  Anchors: "Table 6-1" and "Prevailing Shell Steel
# Specifications" -- both greppable in the text layer and in the .md.
TABLE_PAGE = 11
INTRO_PAGE = 10
INTRO_ANCHOR = "Prevailing Shell Steel Specifications"

# The five element columns, in the order the page prints them left to right.
ELEMENTS = ["c", "mn", "p", "s", "si"]

# One cell as the page prints it: "0.14-0.20" (a range) or "0.040 max." (a
# ceiling with no stated floor).  Hyphen class covers the scan's en-dashes.
_CELL = re.compile(r"(\d+\.\d+)\s*(?:[-‐-―]\s*(\d+\.\d+)|(max\.?))", re.I)
_GRADE = re.compile(r"^WDSS\s+(\d+)\s*$")


def parse_page(text):
    """Return {grade: [(lo, hi), ...]} read off the page's own text layer.

    The layer emits the table row-major: a "WDSS n" line, then that row's five
    cells.  A max-only cell yields ("", ceiling).

    Cells are kept as the STRINGS the page prints, not floats.  In a
    specification table the trailing zeros are the stated precision -- "0.040
    max." is a three-decimal limit and "0.04" is not the same claim -- so
    round-tripping through float() would quietly coarsen the source.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out = {}
    grade = None
    for line in lines:
        g = _GRADE.match(line)
        if g:
            grade = f"WDSS {g[1]}"
            out[grade] = []
            continue
        if grade is None or len(out[grade]) >= len(ELEMENTS):
            continue
        m = _CELL.match(line)
        if m:
            lo, hi, ismax = m[1], m[2], m[3]
            out[grade].append(("", lo) if ismax else (lo, hi))
    return out


def load_csv():
    """Return {grade: [(lo, hi), ...]} in the same shape as parse_page."""
    with TABLE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    return {
        r["grade"]: [
            ((r.get(f"{e}_lo") or "").strip(), (r.get(f"{e}_hi") or "").strip())
            for e in ELEMENTS
        ]
        for r in rows
    }


def emit(page):
    """Write the parsed table to the CSV, so no digit in it is hand-typed."""
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    fields = ["grade"] + [f"{e}_{b}" for e in ELEMENTS for b in ("lo", "hi")]
    with TABLE.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for grade in sorted(page, key=lambda g: int(g.split()[1])):
            row = [grade]
            for lo, hi in page[grade]:
                row += [lo, hi]
            w.writerow(row)
    print(f"wrote {TABLE.relative_to(ROOT)} ({len(page)} rows)")


def main():
    if not PDF.exists():
        print(f"skipped: {PDF.relative_to(ROOT)} absent (gitignored; DTIC AD0830266)")
        print("RESULT: skipped -- cannot verify without the scan")
        return 0

    import fitz  # noqa: PLC0415 -- only needed when the scan is present

    with fitz.open(PDF) as doc:
        page_text = doc[TABLE_PAGE].get_text()
        intro_text = doc[INTRO_PAGE].get_text()

    failures = []

    if INTRO_ANCHOR not in intro_text:
        failures.append(
            f"anchor {INTRO_ANCHOR!r} not found on pdf page {INTRO_PAGE} -- "
            f"the scan has been re-paginated or re-extracted"
        )

    page = parse_page(page_text)
    if "--emit" in sys.argv:
        emit(page)

    have = load_csv()

    print(f"page  {len(page)} grades read off the text layer of pdf page {TABLE_PAGE}")
    print(f"csv   {len(have)} grades in {TABLE.relative_to(ROOT)}")
    print()

    if set(page) != set(have):
        failures.append(
            f"grade set differs -- page {sorted(page)} vs csv {sorted(have)}"
        )

    header = "  ".join(f"{e:>13s}" for e in ELEMENTS)
    print(f"{'grade':<8s}  {header}")
    for grade in sorted(set(page) & set(have)):
        cells = []
        for element, (pv, cv) in zip(ELEMENTS, zip(page[grade], have[grade]), strict=True):
            lo, hi = pv
            shown = f"{hi} max" if not lo else f"{lo}-{hi}"
            cells.append(f"{shown:>13s}" if pv == cv else f"{shown + ' !':>13s}")
            if pv != cv:
                failures.append(
                    f"{grade} {element}: page {pv}, csv {cv} -- the CSV does not "
                    f"match the page"
                )
        print(f"{grade:<8s}  {'  '.join(cells)}")

    for grade in sorted(set(page) & set(have)):
        n = len(page[grade])
        if n != len(ELEMENTS):
            failures.append(f"{grade}: read {n} cells off the page, expected {len(ELEMENTS)}")

    print()
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
