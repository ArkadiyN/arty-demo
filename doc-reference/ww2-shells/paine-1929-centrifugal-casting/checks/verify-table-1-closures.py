"""Closure invariants for Table I (Paine 1929, "Properties of Steels
Suitable for Shell Manufacture", Army Ordnance Vol. 10 No. 56, p.121).

Consumer: doc-reference/ww2-shells/paine-1929-centrifugal-casting/card.md.

Why a standalone script instead of a `.invariant` DSL file (see
src/utils/check-table-invariants.py): that DSL requires (a) CSV headers that
are valid Python identifiers, and (b) every row to evaluate its `row:` check
-- there is no conditional "skip this row, its value is a range" primitive.
Table I fails both: its headers carry units in parens ("Ultimate Strength
(lbs/in²)"), and roughly half its rows carry ranges ("70000-80000"),
asterisked footnote values ("21*"), or blanks by design (the source itself
leaves cells empty -- see card.md). A shared per-row equality-with-tolerance
check has no way to skip those without misreporting them as failures, so the
closures below are hand-written instead, per source-data-fidelity.md's "a
closure the DSL cannot express goes in a check script" escape valve.

Three closures, each derived from the source's own table structure/captions,
run against every one of the 28 data rows:

1. ROW SHAPE -- every data row must carry exactly as many comma-delimited
   fields as the header (14). This is the closure that actually matters here:
   an earlier extraction pass silently dropped one field on 14 of 28 rows
   (the physically-blank "Yield Point" cell was skipped instead of preserved
   as blank, left-shifting Elongation and Reduction of Area by one column and
   dropping Reduction of Area off the end entirely). A field-count mismatch
   is exactly what a column-shifted row looks like.
2. ORDERING -- where Ultimate Strength and Elastic Limit are BOTH given as a
   single concrete number (not a range, not blank), Ultimate Strength must be
   >= Elastic Limit (rupture stress cannot be below the onset-of-deformation
   stress). Verified true for every qualifying row in the source page image.
3. PERCENT BOUND -- Elongation and Reduction of Area are defined by the
   source as percentages (card.md "Strength term definitions"); where given
   as a single concrete number, each must be < 100. This is the second half
   of the same column-shift defect: a stress value (tens of thousands) stray
   into a percent column would fail this instantly, just as it would have
   failed to catch closure #1's absence before the fix.

Run: uv run python doc-reference/ww2-shells/paine-1929-centrifugal-casting/checks/verify-table-1-closures.py
"""

import csv
import re
from pathlib import Path

TABLE = (
    Path(__file__).resolve().parents[1]
    / "tables"
    / "table-1-shell-steel-properties.csv"
)

_NUMBER_RE = re.compile(r"^\d+(\.\d+)?$")


def as_single_number(cell):
    """Return float(cell) if `cell` is a single concrete number (no range,
    no asterisk, not blank); otherwise None (excluded from that closure)."""
    if not cell or "-" in cell or "*" in cell:
        return None
    if not _NUMBER_RE.match(cell):
        return None
    return float(cell)


def main():
    text = TABLE.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    header = next(csv.reader([lines[0]]))
    n_cols = len(header)
    idx = {name: i for i, name in enumerate(header)}

    rows = list(csv.reader(lines[1:]))

    failures = []

    # 1. Row shape
    for i, row in enumerate(rows, start=2):  # 1-indexed CSV line number
        if len(row) != n_cols:
            failures.append(
                f"line {i}: {len(row)} fields, expected {n_cols} "
                f"({row[0]!r})"
            )

    # 2. Ordering: Ultimate Strength >= Elastic Limit, where both concrete
    ult_i = idx["Ultimate Strength (lbs/in²)"]
    ela_i = idx["Elastic Limit (lbs/in²)"]
    elg_i = idx["Elongation (%)"]
    rda_i = idx["Reduction of Area (%)"]
    for i, row in enumerate(rows, start=2):
        if len(row) != n_cols:
            continue  # already flagged by the shape check; don't cascade
        ult = as_single_number(row[ult_i])
        ela = as_single_number(row[ela_i])
        if ult is not None and ela is not None and ult < ela:
            failures.append(
                f"line {i}: Ultimate Strength {ult:g} < Elastic Limit "
                f"{ela:g} ({row[0]!r})"
            )

    # 3. Percent bound: Elongation, Reduction of Area < 100 where concrete
    for i, row in enumerate(rows, start=2):
        if len(row) != n_cols:
            continue
        for label, col_i in (("Elongation", elg_i), ("Reduction of Area", rda_i)):
            val = as_single_number(row[col_i])
            if val is not None and val >= 100:
                failures.append(
                    f"line {i}: {label} = {val:g} >= 100, not a plausible "
                    f"percent ({row[0]!r})"
                )

    print(f"{len(rows)} data rows checked against {TABLE.name}")
    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        raise SystemExit(1)
    print("ok: row shape, Ultimate>=Elastic ordering, and Elongation/"
          "Reduction percent bounds all hold")


if __name__ == "__main__":
    main()
