"""Closure checks on the two Tolch-1938 *count* numbers the drag update consumes.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          phase4b-tolch-mach-drag-assessment.md  (F2, F4, F5)

Complements checks/tolch-side-spray-closure.py, which closed the side-spray
DENSITY ratio (RATIO_OBS = 0.557).  This script closes the other two Tolch
numbers the update rests on:

  * the pit-test recovered-fragment count -- committed artifacts say 803,
    the report's own screen table and body text say 779;
  * the panel-derived perforating count ~700 (part of the 5000 total).

and adds a cross-surface closure for the side-spray component table against
the report's separately typeset "Total number of hits ..." table, which the
earlier script could not do for Panel A (illegible in the component table).

Greppable source anchors (all resolve in source.pdf and in any re-extraction;
NO bare line numbers):
  screen table : "Fragments caught by following screens:"
  screen counts: "Four rounds were fragmented in sand pit tests"
  narrative    : "In the pit fragmentation tests, an average of"
  item 6       : "total number of fragments issuing from the shell"
  totals table : "Total number of hits per unit solid angle in side spray."
  components   : "Number of perforations, penetrations, and dents per unit solid angle of the sidespray."
  stated loss  : "the losses in density of"
  hole areas   : "of all the perforating fragments issuing"

Both series are read from tables/*.csv, transcribed once off the page images
and each carrying its own closure invariant (see the .invariant files).  This
script previously held them as hand-typed literals off the garbled pdftotext
layer; that is what put the v=1085 side-spray totals at 4.26 / 3.56 / 1.90
(the page prints 4.06 / 3.42 / 1.96) and the screen-4 count at "illegible"
(the page prints 142).
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
TABLES = (
    ROOT
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)

LB_G = 453.59237
fails = 0


def check(label, got, want, tol):
    global fails
    ok = abs(got - want) <= tol
    fails += not ok
    print(f"  {label:<52} {got:9.3f} vs {want:9.3f}  {'PASS' if ok else 'FAIL'}")
    return ok


# --- P1. pit-test screen table: which total closes, 779 or 803? -------------
# Read once from tables/pit-screen-recovery.csv (anchor "Fragments caught by
# following screens:", report page -6-, the four-round average).
SCREENS = []
with (TABLES / "pit-screen-recovery.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        SCREENS.append((r["screen"], int(r["n_frag"]), float(r["pct_no"]),
                        float(r["wt_lb"])))

PRINTED_TOTAL = 779       # the table's own total row
PRINTED_WT_LB = 12.708    # = 95.6 % of empty shell + fuze

print("== P1. pit-test count: percent-of-total column discriminates 779 vs 803 ==")
for cand in (779, 803):
    print(f"  candidate total = {cand}")
    for name, n, pct, _ in SCREENS:
        check(f"    screen {name}: {n}/{cand} vs printed %",
              100.0 * n / cand, pct, 0.06)
# the 803 rows above are EXPECTED to fail; undo their contribution and assert it.
# Screens 1 and 4 have small enough shares that the 779-vs-803 gap stays inside
# the rounding band; screens 2, 3 and "thru 4" do not.
expected_803_failures = sum(
    abs(100.0 * n / 803 - pct) > 0.06 for _, n, pct, _ in SCREENS
)
fails -= expected_803_failures
print(f"  (the {expected_803_failures} failures under 803 are the finding, not a defect)")

print("\n== P2. screen counts sum to the printed total ==")
# Cross-checked by summary item 1, anchor "Four rounds were fragmented in sand
# pit tests", which lists the same five counts in prose.
check("  sum of the five screen counts",
      sum(n for _, n, _, _ in SCREENS), PRINTED_TOTAL, 0.5)
check("  sum of the five printed percentages",
      sum(p for _, _, p, _ in SCREENS), 100.0, 0.15)
check("  sum of the five screen weights, lb",
      sum(w for _, _, _, w in SCREENS), PRINTED_WT_LB, 0.005)

print("\n== P3. mean recovered fragment mass under each total ==")
m_recovered_g = PRINTED_WT_LB * LB_G
print(f"  recovered metal {PRINTED_WT_LB} lb = {m_recovered_g:.0f} g (95.6 % of empty shell+fuze)")
for cand in (779, 803):
    print(f"  mean fragment at N={cand}: {m_recovered_g / cand:.2f} g")
print("  (committed artifacts quote 6.85 g = 5755 g body x 0.956 / 803)")
check("  6.85 g re-derived at N=779 from the same 5755 g body",
      5755.0 * 0.956 / 779, 7.06, 0.02)

# --- P4. panel-derived count: item 6 self-closes ---------------------------
print("\n== P4. item 6 'about 5000 = 700 perf + 900 penet + 3400 dents' ==")
check("  700+900+3400", 700 + 900 + 3400, 5000, 0.5)

# --- P5. side-spray components vs the separately typeset totals table ------
# Read once from tables/side-spray-density.csv (extracted off the page images;
# see side-spray-density.invariant). This script previously held the series as
# a hand-typed literal off the garbled text layer, whose v=1085 totals of
# 4.26 / 3.56 / 1.90 failed this check; the page prints 4.06 / 3.42 / 1.96.
SIDE = {}
with (TABLES / "side-spray-density.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        SIDE[(int(r["v_fps"]), r["panel"])] = {
            k: float(r[k]) for k in ("perf", "penet", "dents", "total")
        }

print("\n== P5. side-spray components sum to the separately typeset totals ==")
for (v, panel), row in sorted(SIDE.items()):
    check(f"  v={v:<5} panel {panel}: sum vs printed total",
          row["perf"] + row["penet"] + row["dents"], row["total"], 0.015)

# --- P6. the perf row the update consumes is confirmed independently -------
print("\n== P6. perf row confirmed by the source's own stated A->D losses ==")
for v, stated in ((0, 44.0), (700, 19.0), (1085, 33.0)):
    a, d = SIDE[(v, "A")]["perf"], SIDE[(v, "D")]["perf"]
    check(f"  v={v:<5} 1 - D/A", 100.0 * (1 - d / a), stated, 0.5)
check("  RATIO_OBS consumed by the update (static D/A)",
      SIDE[(0, "D")]["perf"] / SIDE[(0, "A")]["perf"], 0.557, 0.001)

# --- P7. hole-area floor used in scoping 3d --------------------------------
# anchor "of all the perforating fragments issuing": 2 % of perforating
# fragments have sectional area < .02 sq.in.; 10 % < .04 sq.in.
print("\n== P7. 0.02 sq.in perforation floor -> compact-fragment mass ==")
A_mm2 = 0.02 * 645.16
check("  0.02 sq.in in mm^2", A_mm2, 12.90, 0.01)
check("  rho*A^(3/2) at 7850 kg/m^3 [g]", 7.85e-3 * A_mm2 ** 1.5, 0.36, 0.01)

# --- P8. impact of 803 -> 779 on the update's N/observed band --------------
print("\n== P8. update's N/obs band under the corrected observed count ==")
N_lo, N_hi = 3.9 * 750.0, 5.6 * 750.0     # scoping 3d row for combined 2.67
for lo, hi, tag in ((700, 803, "as published (700-803, quoted 3.9-5.6x)"),
                    (700, 779, "corrected  (700-779)")):
    print(f"  {tag:<42} N/obs = {N_lo / hi:.2f} - {N_hi / lo:.2f}")

print(f"\nRESULT: {fails} failure(s)")
