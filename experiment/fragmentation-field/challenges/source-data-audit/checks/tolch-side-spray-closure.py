"""Closure check on Tolch-1938's SIDE-spray density table (panels A-D, 15/36/75/120 ft).

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          phase4b-tolch-mach-drag-assessment.md  (F2, F3)

Why this table and not tables/*.csv: the two re-baselined CSVs under
doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/
cover the BASE spray (162.5-180 deg) and NOSE spray. The drag observable the
mach-dependent-fragment-drag update consumes -- the Panel A (15 ft) -> Panel D
(120 ft) perforation-density ratio 0.557 -- comes from a THIRD table, the SIDE
spray averaged over 35 deg of arc, which has NOT been extracted into tables/.
Until it is, the series below is provisional and is held here as a literal on
purpose: the point of the script is to decide whether the table is admissible
at all, which cannot be done by reading a CSV that does not yet exist.

Source anchors (greppable strings in source.pdf / any re-extraction):
  table   : "the hits per unit solid angle were averaged over certain"
            ... "included between 76 and 111 deg. with the shell axis"
  totals  : "Total number of hits per unit solid angle in side spray."
  stated  : "the losses in density of"  ... "perforating"
            "fragments between Panels A and D for remaining"
  counts  : "about 700 perforating"     /  "an average of 779"
  areas   : "of all the perforating fragments issuing"

Series transcribed from the retained source.pdf text layer (pdftotext -layout);
digits confirmed against the report's own summary paragraphs.
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
TABLES = (
    ROOT
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)

# --- SIDE spray, hits per unit solid angle, panels A/B/C/D = 15/36/75/120 ft ---
# rows: (shell remaining velocity f/s, arc deg, perf, penet, dents, printed total)
SIDE_STATIC = dict(
    perf=[1.49, 1.47, 1.18, 0.83],
    penet=[0.97, 1.29, 0.47, 0.65],
    dents=[2.39, 1.13, 0.18, 0.04],
)
# Kept out of SIDE_STATIC so the component lists stay float-only: Panel A's
# printed total is an unreadable glyph, and a None in the same dict makes every
# component lookup Optional to the type checker.
SIDE_STATIC_TOTAL = [None, 3.89, 1.83, 1.52]
SIDE_PERF_BY_V = {0: [1.49, 1.47, 1.18, 0.83], 700: [1.25, 1.29, 0.94, 1.01],
                  1085: [1.53, 1.41, 1.15, 1.02]}
# Source's own stated A->D perforating-density losses, in per cent:
STATED_LOSS = {0: 44.0, 700: 19.0, 1085: 33.0}
STATED_MEAN_LOSS = 32.0

fails = 0

print("== C1. component-sum closure, side spray, static (same invariant as tables/) ==")
for i, panel in enumerate("ABCD"):
    s = SIDE_STATIC["perf"][i] + SIDE_STATIC["penet"][i] + SIDE_STATIC["dents"][i]
    t = SIDE_STATIC_TOTAL[i]
    if t is None:
        print(f"  panel {panel}: components sum to {s:.2f}; printed total illegible"
              f" -> reconstructed as {s:.2f}")
        continue
    ok = abs(s - t) <= 0.02
    fails += not ok
    print(f"  panel {panel}: {s:.2f} vs printed {t:.2f}  resid {s - t:+.2f}"
          f"  {'PASS' if ok else 'FAIL'}")

print("\n== C2. source's own stated A->D perforating-density loss reproduces ==")
losses = []
for v, row in SIDE_PERF_BY_V.items():
    loss = 100.0 * (1.0 - row[3] / row[0])
    losses.append(loss)
    ok = abs(loss - STATED_LOSS[v]) <= 0.5
    fails += not ok
    print(f"  v_shell={v:>4} f/s: 1 - {row[3]}/{row[0]} = {loss:5.1f}%"
          f"  vs stated {STATED_LOSS[v]:.0f}%   {'PASS' if ok else 'FAIL'}")
mean = sum(losses) / len(losses)
ok = abs(mean - STATED_MEAN_LOSS) <= 0.5
fails += not ok
print(f"  mean {mean:.1f}% vs stated 'averaging {STATED_MEAN_LOSS:.0f}%'"
      f"   {'PASS' if ok else 'FAIL'}")

print("\n== C3. the ratio the update consumes ==")
ratio = SIDE_PERF_BY_V[0][3] / SIDE_PERF_BY_V[0][0]
ok = abs(ratio - 0.557) <= 0.001
fails += not ok
print(f"  static Panel D / Panel A perforations = {ratio:.4f}"
      f"  vs update's RATIO_OBS 0.557   {'PASS' if ok else 'FAIL'}")

print("\n== C4. text layer agrees with the re-baselined CSVs (cross-surface check) ==")
# base-spray static row read off the SAME pdftotext layer used for C1-C3
TEXT_LAYER_BASE_STATIC = {"perf": [1.82, 1.93, 1.48],
                          "penet": [1.59, 2.76, 1.49],
                          "dents": [6.30, 2.76, 0.96]}
rows = list(csv.DictReader((TABLES / "base-spray-density.csv").open()))
for kind, vals in TEXT_LAYER_BASE_STATIC.items():
    csv_vals = [float(r[kind]) for r in rows
                if r["v_fps"] == "0" and r["panel"] in "ABC"]
    ok = all(abs(a - b) <= 0.005 for a, b in zip(vals, csv_vals))
    fails += not ok
    print(f"  base static {kind:<6}: text {vals}  csv {csv_vals}"
          f"   {'PASS' if ok else 'FAIL'}")

print(f"\nRESULT: {fails} failure(s)")
