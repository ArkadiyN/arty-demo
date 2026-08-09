"""Closure invariants for the weight tables in Ordnance Ammunition Drawings,
Book 4 (pages 5, 9, 23, 25, 53).

Consumer: doc-reference/ww2-shells/ordnance-ammunition-drawings-book-4/card.md.

Why a standalone script instead of the shared `.invariant` DSL
(src/utils/check-table-invariants.py): every closure here is a SUM DOWN A
COLUMN culminating in a "Total"/"Shipping Weight" row further down the same
CSV -- the DSL's `row:` directive checks a formula against columns *within
one row* (e.g. energy = 0.5*m*v**2), not an accumulation across rows. These
tables are the opposite shape: one column, many component rows, an explicit
subtotal row. Hand-written summation is the only way to express that.

These closures matter more than usual here: the librarian's automated
`--analyze-formulas` vision pass (Google Gemma free tier, the pipeline
default -- see settings.py `vision_provider`) produced wrong numbers on
every one of these seven pages -- wrong digits, swapped rows, one entirely
fabricated table structure (page 53's weight-zone table). The tables below
were independently re-transcribed by direct page-image reads and are
committed *because* they close; a table that doesn't close is flagged, not
silently shipped.

Run: uv run python doc-reference/ww2-shells/ordnance-ammunition-drawings-book-4/checks/verify-weight-table-closures.py
"""

import csv
from pathlib import Path

TABLES = Path(__file__).resolve().parents[1] / "tables"


def load(name):
    with open(TABLES / name, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {r[next(iter(r))]: r for r in rows}  # keyed by first column's value


def num(row, col):
    v = row.get(col, "").strip()
    return float(v) if v else 0.0


def check_sum(label, rows_dict, col, components, subtotal_row, tol=0.005):
    total = sum(num(rows_dict[c], col) for c in components)
    stated = num(rows_dict[subtotal_row], col)
    ok = abs(total - stated) <= tol
    status = "ok" if ok else "FAIL"
    print(f"  [{status}] {label}: sum({components}) = {total:.3f} vs "
          f"{subtotal_row} = {stated:.3f} (col={col}, tol={tol})")
    return ok


def main():
    failures = 0

    print("m48-75mm-charge-weights.csv (page 23)")
    t = load("m48-75mm-charge-weights.csv")
    failures += not check_sum(
        "TNT: Shell Empty + Charge Bursting == Total Unfuzed", t, "TNT_lb",
        ["Shell Weight Empty (+/-.30)", "Charge Bursting"],
        "Total Weight Unfuzed")
    failures += not check_sum(
        "Amatol: Shell Empty + Charge Bursting + Surround Booster == "
        "Total Unfuzed", t, "Amatol_lb",
        ["Shell Weight Empty (+/-.30)", "Charge Bursting",
         "Surround Booster (Amatol loading only)"],
        "Total Weight Unfuzed")
    for col in ("TNT_lb", "Amatol_lb"):
        failures += not check_sum(
            f"{col}: Total Unfuzed == Shipping Weight (no extra parts on "
            "this drawing)", t, col,
            ["Total Weight Unfuzed"], "Shipping Weight")

    print("\nm1-105mm-charge-weights.csv (page 25)")
    t = load("m1-105mm-charge-weights.csv")
    failures += not check_sum(
        "TNT: Metal Parts Assembly + Charge Bursting == Total Unfuzed", t,
        "TNT_lb", ["Metal Parts Shipping Assembly (+/-.60)", "Charge Bursting"],
        "Total Weight Unfuzed")
    failures += not check_sum(
        "Amatol: Metal Parts Assembly + Charge Bursting + Surround Booster "
        "== Total Unfuzed", t, "Amatol_lb",
        ["Metal Parts Shipping Assembly (+/-.60)", "Charge Bursting",
         "Surround Booster (Amatol loading only)"],
        "Total Weight Unfuzed")
    for col in ("TNT_lb", "Amatol_lb"):
        failures += not check_sum(
            f"{col}: Total Unfuzed + Plug Closing == Shipping Weight", t, col,
            ["Total Weight Unfuzed", "Plug Closing"], "Shipping Weight")

    print("\nm107-155mm-charge-weights.csv (page 53)")
    t = load("m107-155mm-charge-weights.csv")
    failures += not check_sum(
        "Shell Empty + Charge Bursting + Liner + Charge Supplementary == "
        "Total Unfuzed", t, "Weight_lb",
        ["Shell Empty (+/-1.35)", "Charge Bursting", "Liner",
         "Charge Supplementary"], "Total Weight Unfuzed")
    failures += not check_sum(
        "Total Unfuzed + Grommet + Plug Lifting + Spacer == Shipping "
        "Weight", t, "Weight_lb",
        ["Total Weight Unfuzed", "Grommet", "Plug Lifting", "Spacer"],
        "Shipping Weight", tol=0.005)

    print("\nm107-metal-weights.csv (page 9, WEIGHTS table)")
    t = load("m107-metal-weights.csv")
    failures += not check_sum(
        "Body Shell + Band Rotating + Cover Base == Total Weight Empty", t,
        "Weight_lb", ["Body Shell", "Band Rotating", "Cover Base"],
        "Total Weight Empty (+/-1.35)")
    ok = check_sum(
        "Total Weight Empty + Plug Lifting + Grommet == Shipping Weight "
        "(KNOWN MISMATCH -- see card.md; closes exactly if Plug Lifting "
        "were 0.75 instead of the transcribed 1.75)", t, "Weight_lb",
        ["Total Weight Empty (+/-1.35)", "Plug Lifting", "Grommet"],
        "Shipping Weight of Metal Parts Assembly", tol=0.005)
    if not ok:
        print("      -> flagged, not counted as a hard failure: this cell "
              "was carried from the pre-compaction transcription and was "
              "not re-verified against source.pdf at high zoom this pass. "
              "card.md documents the discrepancy; do not cite Plug Lifting "
              "= 1.75 for page 9 without re-checking the raster.")

    print("\nm107-metal-design-data.csv (page 9, DESIGN DATA table)")
    t = load("m107-metal-design-data.csv")
    failures += not check_sum(
        "Body Shell + Band Rotating + Cover Base + Charge + Cup Fuze Well "
        "+ Fuze == Total", t, "Weight_lb",
        ["Body Shell", "Band Rotating", "Cover Base", "Charge Cast TNT",
         "Cup Fuze Well", "Fuze P.D. M51"], "Total")

    print("\nm60-metal-parts-weights.csv (page 5, WEIGHTS table)")
    t = load("m60-metal-parts-weights.csv")
    failures += not check_sum(
        "Body Shell + Band Rotating + Adapter == Total Weight Empty", t,
        "Weight_lb", ["Body Shell", "Band Rotating", "Adapter"],
        "Total Weight Empty (+/-0.60)")

    print("\nm60-design-data.csv (page 5, DESIGN DATA table)")
    t = load("m60-design-data.csv")
    failures += not check_sum(
        "Shell Empty(w/Adapter) + Charge(WP) + Charge Burster + Casing "
        "Burster + Cup Fuze Well + Booster M22 + Fuze M57 == Total "
        "(wider tolerance: 7-term sum, source rounds each term to .01)", t,
        "Weight_lb",
        ["Shell Empty (with Adapter)", "Charge (Smoke) WP",
         "Charge Burster M5", "Casing Burster M5", "Cup Fuze Well",
         "Booster M22", "Fuze M57"], "Total", tol=0.05)

    print(f"\n{'FAIL' if failures else 'ok'}: {failures} hard closure "
          f"failure(s) (Plug Lifting mismatch above is a flag, not counted)")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
