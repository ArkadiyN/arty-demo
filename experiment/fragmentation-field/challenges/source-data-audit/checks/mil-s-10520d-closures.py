"""Closure checks for MIL-S-10520D's Tables I, II and X, including the cross-document diff against AMCP table 6-1.

Consumer: doc-reference/ww2-shells/mil-s-10520d-projectile-steel/
{card.md, tables/*.csv} and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 20.

WHY THIS EXISTS RATHER THAN .invariant FILES.  Two reasons, one per table.

Table I is a chemical specification: six grades x five elements, every cell an
independent policy limit with no arithmetic relation to its neighbours.  Its
sibling document (ammunition-series-6-wdss-specs) had the same problem and
solved it by machine-diffing the embedded text layer cell for cell -- strictly
better than a closure, because it compares position as well as value.  That
route is CLOSED here: this scan has no text layer at all (14 pages, 588
characters, all of it an everyspec watermark; see vision_gating_probe).

So Table I's closure is CROSS-DOCUMENT instead.  MIL-S-10520D's Table I and
AMCP 706-249's table 6-1 are two independent transcriptions, from two
independently-acquired scans, of what the cover page establishes is essentially
the same table: D supersedes "MIL-S-10520C(ORD), 17 February 1953", and 6-14
dates table 6-1 "as of 17 February 1953".  Agreement across 30 cells and a
four-element footnote is a mechanical pass/fail check that no single eyeball
can match, and it is sensitive to exactly the failure mode
.claude/rules/source-data-fidelity.md targets: a row or column misassignment
would have to be replicated identically by two readers of two different scans.

Tables II and X DO carry internal closures -- their yield-strength and
composition brackets must tile without gap or overlap, and coupon size must
fall as required yield rises -- but those are relations BETWEEN ROWS, and the
.invariant DSL has only per-row, whole-column-sum, and adjacent-row-monotonic
handlers.  Hence a script.  (The DSL gap is logged as a Phase 8 candidate; the
one closure the DSL can express, the hold-time monotonicity, is in
tables/table-10-hold-times.invariant rather than duplicated here.)

WHAT THIS DOES NOT ESTABLISH.  Two things, both deliberate:

  - Criterion match -- does a model consuming these numbers compute the
    quantity they tabulate?  That is @model-reviewer's gate.
  - That revision D's numbers may stand in for revision C's.  Grade 1 differs
    between the two documents on four of five elements, and C itself is not in
    hand.  The script reports that difference; it does not adjudicate it.  See
    card.md, "Revision gap".

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mil-s-10520d-closures.py
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/ww2-shells/mil-s-10520d-projectile-steel"
AMCP = ROOT / "doc-reference/ww2-shells/ammunition-series-6-wdss-specs"

TABLE_1 = DOC / "tables/table-1-chemical-requirements.csv"
TABLE_2 = DOC / "tables/table-2-product-analysis-variations.csv"
TABLE_10 = DOC / "tables/table-10-coupon-selection.csv"
TABLE_6_1 = AMCP / "tables/table-6-1-chemical-requirements.csv"

ELEMENTS = ["c", "mn", "p", "s", "si"]

# Grade 1 is the one row the two documents are expected to disagree on: a
# high-manganese, high-sulfur free-machining grade in the 1953 revision, a plain
# low-carbon grade in 1975.  Listing it here makes the expectation explicit --
# a NEW disagreement on any other grade is a failure, and grade 1 SUDDENLY
# AGREEING would equally mean one of the two CSVs had been edited.
EXPECTED_DIVERGENT_GRADE = "1"


def rows(path):
    with path.open(newline="") as fh:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


def num(text):
    """float, or None for a blank cell.  Only for the bracket arithmetic."""
    return float(text.replace(",", "")) if text else None


def grade_key(row):
    """'WDSS 3' and '3' both key to '3', so the two documents line up."""
    return row["grade"].replace("WDSS", "").strip()


def check_table_1_cross_document(failures, notes):
    """Diff all 30 cells of Table I against AMCP table 6-1.

    Cells are compared as the STRINGS each document prints.  In a specification
    the trailing zeros are the stated precision -- "0.040 max" is a
    three-decimal limit and "0.04" is not the same claim -- so comparing floats
    would let a real coarsening pass.  The one normalisation applied is a
    leading zero on values the page prints as ".65": that is a typewriter
    artifact of MIL-S-10520D's own printing (it writes "0.60" and ".65" in
    adjacent rows of one column), not a precision claim, and the CSV already
    carries the normalised form.
    """
    d = {grade_key(r): r for r in rows(TABLE_1)}
    c = {grade_key(r): r for r in rows(TABLE_6_1)}

    print("Table I (MIL-S-10520D, 1975)  vs  table 6-1 (AMCP 706-249, C-era 1953)")
    print(f"{'grade':<6}{'element':<9}{'D':>14}{'C-era':>14}   verdict")

    if set(d) != set(c):
        failures.append(f"grade sets differ: D {sorted(d)} vs C-era {sorted(c)}")

    agree = differ = 0
    for g in sorted(set(d) & set(c), key=int):
        for e in ELEMENTS:
            dv = (d[g][f"{e}_lo"], d[g][f"{e}_hi"])
            cv = (c[g][f"{e}_lo"], c[g][f"{e}_hi"])

            def show(v):
                return f"{v[1]} max" if not v[0] else f"{v[0]}-{v[1]}"

            if dv == cv:
                agree += 1
                continue
            differ += 1
            verdict = "expected (rev)" if g == EXPECTED_DIVERGENT_GRADE else "UNEXPECTED"
            print(f"{g:<6}{e:<9}{show(dv):>14}{show(cv):>14}   {verdict}")
            if g != EXPECTED_DIVERGENT_GRADE:
                failures.append(
                    f"grade {g} {e}: D says {show(dv)}, C-era says {show(cv)} -- "
                    "two independent scans disagree on a grade that should be "
                    "unchanged between revisions"
                )

    print(f"\n  {agree} of {agree + differ} cells identical across the two documents")
    if differ and not any(g == EXPECTED_DIVERGENT_GRADE for g in set(d) & set(c)):
        failures.append("expected-divergent grade absent from both tables")
    if differ == 0:
        failures.append(
            f"grade {EXPECTED_DIVERGENT_GRADE} was expected to differ between "
            "revisions and does not -- has one of the CSVs been edited to match?"
        )
    notes.append(
        f"Table I: {agree}/{agree + differ} cells agree with AMCP table 6-1; "
        f"all {differ} disagreements are in grade {EXPECTED_DIVERGENT_GRADE}."
    )


def check_brackets(failures, notes, path, group_col, lo_col, hi_col, label):
    """Within each group, the brackets must tile: row i's upper == row i+1's lower.

    This is the closure a bracketed limit table actually carries.  The source
    states each bracket as "Over X to Y, incl.", so consecutive brackets sharing
    an endpoint is not a convention -- it is what makes the table total over its
    stated domain.  A gap means a value the table does not cover; an overlap
    means two contradictory answers for one value.  Either is what a row
    misassignment looks like here.
    """
    groups = {}
    for r in rows(path):
        groups.setdefault(r[group_col], []).append(r)

    print(f"\n{label}: bracket tiling")
    for name, grp in groups.items():
        spans = [(num(r[lo_col]), num(r[hi_col])) for r in grp]
        shown = ", ".join(
            f"({'--' if lo is None else f'{lo:g}'}, {'--' if hi is None else f'{hi:g}'})"
            for lo, hi in spans
        )
        print(f"  {name:<30} {shown}")
        for i in range(len(spans) - 1):
            hi, next_lo = spans[i][1], spans[i + 1][0]
            if hi is None or next_lo is None:
                continue
            if hi != next_lo:
                failures.append(
                    f"{label} / {name}: bracket {i} ends at {hi:g} but bracket "
                    f"{i + 1} starts at {next_lo:g} -- "
                    f"{'gap' if next_lo > hi else 'overlap'}"
                )
        open_lo = [i for i, (lo, _) in enumerate(spans) if lo is None and i > 0]
        for i in open_lo:
            notes.append(
                f"{label} / {name}: bracket {i} has no printed lower bound; "
                "recorded as printed, tiling unchecked across it"
            )


def check_coupon_monotonic(failures, notes):
    """Coupon diameter must not rise as the required yield strength rises.

    The source's own logic (4.5.1): the coupon stands in for the projectile
    wall, and a higher yield is reached by quenching a thinner section.  So
    within one projectile-size class, diameter falls as the yield bracket
    climbs.  This is the check that catches the diameter column being read one
    row out of step -- the failure that would otherwise be invisible, since
    every individual value is plausible.
    """
    groups = {}
    for r in rows(TABLE_10):
        groups.setdefault(r["projectile_size_class"], []).append(r)

    print("\nTable X: coupon diameter vs yield bracket")
    for name, grp in groups.items():
        diam = [num(r["coupon_diam_in"]) for r in grp]
        print(f"  {name:<30} {' -> '.join(f'{d:g}' for d in diam)} in")
        for i in range(len(diam) - 1):
            if diam[i + 1] > diam[i]:
                failures.append(
                    f"Table X / {name}: coupon diameter rises {diam[i]:g} -> "
                    f"{diam[i + 1]:g} in as the yield bracket climbs"
                )
    notes.append(
        "Table X: coupon diameter is non-increasing with yield in all "
        f"{len(groups)} projectile-size classes."
    )


def check_table_2_symmetry(failures, notes):
    """Where both tolerances are printed, over-maximum equals under-minimum.

    Table II prints the two columns independently, so their agreement on every
    row that has both is a genuine cross-column check: it is what a one-column
    shift would break.  Phosphorus and Sulfur print only the over-maximum
    tolerance -- both are capped elements with no stated floor, so there is no
    minimum to fall under -- and those rows are skipped, not failed.
    """
    print("\nTable II: over-maximum vs under-minimum tolerance")
    checked = skipped = 0
    for r in rows(TABLE_2):
        over, under = num(r["over_max_pct"]), num(r["under_min_pct"])
        if under is None:
            skipped += 1
            continue
        checked += 1
        if over != under:
            failures.append(
                f"Table II / {r['element']} (to {r['limit_hi']}): over-max "
                f"{over:g} != under-min {under:g}"
            )
    print(f"  {checked} rows symmetric, {skipped} one-sided (capped elements)")
    notes.append(f"Table II: {checked} two-sided rows symmetric, {skipped} one-sided.")


def main():
    failures, notes = [], []

    check_table_1_cross_document(failures, notes)
    check_brackets(
        failures, notes, TABLE_2, "element", "limit_lo", "limit_hi", "Table II"
    )
    check_table_2_symmetry(failures, notes)
    check_brackets(
        failures, notes, TABLE_10,
        "projectile_size_class", "yield_lo_psi", "yield_hi_psi", "Table X",
    )
    check_coupon_monotonic(failures, notes)

    print("\n--- notes ---")
    for n in notes:
        print(f"  {n}")
    print("\n--- failures ---")
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"\nRESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
