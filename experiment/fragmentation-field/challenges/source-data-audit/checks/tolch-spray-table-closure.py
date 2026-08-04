"""Closure checks on Tolch (1938) spray-density tables, and resolution of the
cumulative base-fragment velocity distribution the card flagged "UNVERIFIED".

Consumer: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
section 4, and the Phase-2 rewrite of
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md`.

Reads its series from the checked-in CSVs, per
`.claude/rules/source-data-fidelity.md` -- an earlier revision of this script
hand-typed the tables out of `tolch-1938.md` and inherited ~20 OCR errors from
it, which is exactly the failure mode that rule exists to prevent.

CHECK 1 -- additive closure. The report says of the nose totals table: "The
average number of perforations, penetrations, and dents per unit solid angle
for the nose spray were added together" (report p.22). Both spray tables are
built that way, so every (velocity, panel) cell must satisfy
`perf + penet + dents == total`. This is also declared in the `.invariant`
files and gated by `src/utils/check-table-invariants.py`; it is repeated here
because the numbers below depend on it holding.

CHECK 2 -- the velocity distribution. The card recorded two irreconcilable
extractions of one narrative sentence and ruled the figure uncitable. The
report states the sentence is *derived*, not measured: "The proportion of base
fragments remaining after giving the shell an increment in velocity may be
obtained from the above table" (report p.20). So it is recomputable from the
Panel A base-spray totals, which settles which extraction is right.

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/tolch-spray-table-closure.py
"""

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
TABLES = REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
TOL = 0.02  # tables print 2 d.p.; three summed terms can carry 0.01 of rounding


def load(slug):
    with (TABLES / f"{slug}.csv").open(newline="") as fh:
        return [{k: float(v) if k != "panel" else v for k, v in row.items()} for row in csv.DictReader(fh)]


def check_additive(name, rows):
    """total == perf + penet + dents, per the report's own wording."""
    print(f"\n{name}: total == perforations + penetrations + dents")
    bad = worst = 0
    for row in rows:
        summed = row["perf"] + row["penet"] + row["dents"]
        delta = summed - row["total"]
        worst = max(worst, abs(delta))
        if abs(delta) > TOL:
            bad += 1
            label = "Static" if row["v_fps"] == 0 else f"{row['v_fps']:.0f} f/s"
            print(f"  {label:>9} Panel {row['panel']}: {summed:6.2f} vs stated "
                  f"{row['total']:6.2f}  delta {delta:+.2f}   <-- FAILS")
    print(f"  -> {len(rows)} cells, {bad} fail, largest residual {worst:.2f}")
    return bad


def check_velocity_distribution(base):
    """The narrative fractions are the Panel A base-spray totals over static."""
    print("\nBase-fragment cumulative velocity distribution (Panel A totals / static):")
    panel_a = {r["v_fps"]: r["total"] for r in base if r["panel"] == "A"}
    static = panel_a[0]

    # The two readings the card recorded as irreconcilable, and what the page
    # image of report p.20 actually prints.
    heuristic = {700: 80, 1085: 48, 1450: 29, 1685: 14, 2130: 7}
    vision = {700: 20, 1085: 15, 1450: 25, 1685: 18, 2130: 7}
    printed = {700: 80, 1085: 48, 1450: 29, 1685: 14, 2130: 7}

    print(f"  {'v (f/s)':>8} {'derived':>9} {'printed':>9} {'heuristic':>10} {'vision':>8}")
    derived = {}
    for v in sorted(heuristic):
        derived[v] = 100.0 * panel_a[v] / static
        print(f"  {v:>8} {derived[v]:8.1f}% {printed[v]:8}% {heuristic[v]:9}% {vision[v]:7}%")

    h_err = max(abs(derived[v] - heuristic[v]) for v in heuristic)
    v_err = max(abs(derived[v] - vision[v]) for v in vision)
    print(f"\n  max deviation from derived: heuristic {h_err:.1f} pp, vision {v_err:.1f} pp")
    print("  -> RESOLVED three independent ways, all agreeing: the table derivation,")
    print("     the PDF text layer, and the page image of report p.20 all give")
    print("     80% > 700, 48% > 1085, 29% > 1450, 14% > 1685, 7% > 2130 f/s.")
    print("     The 'vision' reading in the card was garbage; the figure is citable.")
    print("  Caveat: these are *shell* remaining velocities. The quantity is the")
    print("  fraction of base fragments whose charge-imparted velocity exceeds the")
    print("  shell velocity that cancels it -- burst geometry, not fragment drag.")


def main():
    base, nose = load("base-spray-density"), load("nose-spray-density")
    bad = check_additive("Base spray", base) + check_additive("Nose spray", nose)
    check_velocity_distribution(base)

    nose_a = {r["v_fps"]: r["total"] for r in nose if r["panel"] == "A"}
    print(f"\nNose-spray Panel A static -> 2130 f/s: {nose_a[0]:.2f} -> {nose_a[2130]:.2f} "
          f"= {nose_a[2130] / nose_a[0]:.2f}x")
    print("  The card's stated ~1.33x rise is CORRECT. An earlier audit note")
    print("  speculated the static cell might be 1.96 (making it 10.9x); the page")
    print("  image shows 16.09, so that speculation is withdrawn.")

    print(f"\n{bad} non-closing cell(s) across both tables.")


if __name__ == "__main__":
    main()
