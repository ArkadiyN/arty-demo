"""Closure check on Tolch-1938's SIDE-spray density table (panels A-D, 15/36/75/120 ft).

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          phase4b-tolch-mach-drag-assessment.md  (F2, F3)
          experiment/fragmentation-field/challenges/source-data-audit/ledger.md (section 6)

Why this table and not the other two: the two spray tables re-baselined in
audit Phase 2b cover the BASE spray (162.5-180 deg) and the NOSE spray. The
drag observable the mach-dependent-fragment-drag update consumes -- the Panel A
(15 ft) -> Panel D (120 ft) perforation-density ratio 0.557 -- comes from a
THIRD table, the side spray averaged over ~35 deg of arc, which Phase 2b
missed.

It is now extracted, once, to
doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/
side-spray-density.csv, and this script reads it from there. It previously held
the series as a hand-typed literal off the garbled pdftotext layer; that
literal put the v=1085 totals at 4.26 / 3.56 / 1.90 and failed the row-sum
closure below. The page prints 4.06 / 3.42 / 1.96, which closes on all 20
cells. See side-spray-density.invariant for the full transcription history.

Source anchors (greppable strings in source.pdf / any re-extraction):
  table   : "Number of perforations, penetrations, and dents per unit solid angle of the sidespray."
  totals  : "Total number of hits per unit solid angle in side spray."
  stated  : "the losses in density of perforating fragments between Panels A and D"
  counts  : "about 700 perforating"     /  "an average of 779"
  areas   : "of all the perforating fragments issuing"
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
TABLES = (
    ROOT
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)


def load(slug):
    """(v_fps, panel) -> {perf, penet, dents, total} from tables/<slug>.csv."""
    out = {}
    with (TABLES / f"{slug}.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(int(r["v_fps"]), r["panel"])] = {
                k: float(r[k]) for k in ("perf", "penet", "dents", "total")
            }
    return out


SIDE = load("side-spray-density")
BASE = load("base-spray-density")

# Source's own stated A->D perforating-density losses, in per cent, anchor
# "the losses in density of perforating fragments between Panels A and D".
STATED_LOSS = {0: 44.0, 700: 19.0, 1085: 33.0}
STATED_MEAN_LOSS = 32.0

fails = 0

print("== C1. component-sum closure, side spray, all velocities ==")
print("   (same invariant as tables/side-spray-density.invariant, re-run here")
print("    so this script's own conclusions do not rest on an unchecked read)")
for (v, panel), row in sorted(SIDE.items()):
    s = row["perf"] + row["penet"] + row["dents"]
    ok = abs(s - row["total"]) <= 0.02
    fails += not ok
    print(f"  v={v:<5} panel {panel}: {s:.2f} vs printed {row['total']:.2f}"
          f"  resid {s - row['total']:+.2f}  {'PASS' if ok else 'FAIL'}")

print("\n== C2. source's own stated A->D perforating-density loss reproduces ==")
losses = []
for v, stated in STATED_LOSS.items():
    a, d = SIDE[(v, "A")]["perf"], SIDE[(v, "D")]["perf"]
    loss = 100.0 * (1.0 - d / a)
    losses.append(loss)
    ok = abs(loss - stated) <= 0.5
    fails += not ok
    print(f"  v_shell={v:>4} f/s: 1 - {d}/{a} = {loss:5.1f}%"
          f"  vs stated {stated:.0f}%   {'PASS' if ok else 'FAIL'}")
mean = sum(losses) / len(losses)
ok = abs(mean - STATED_MEAN_LOSS) <= 0.5
fails += not ok
print(f"  mean {mean:.1f}% vs stated 'averaging {STATED_MEAN_LOSS:.0f}%'"
      f"   {'PASS' if ok else 'FAIL'}")

print("\n== C3. the ratio the update consumes ==")
ratio = SIDE[(0, "D")]["perf"] / SIDE[(0, "A")]["perf"]
ok = abs(ratio - 0.557) <= 0.001
fails += not ok
print(f"  static Panel D / Panel A perforations = {ratio:.4f}"
      f"  vs update's RATIO_OBS 0.557   {'PASS' if ok else 'FAIL'}")

print("\n== C4. total-hit loss A->D, the source's own second stated figure ==")
# anchor "the loss of fragment density between Panels A and D averages about"
tot_losses = [100.0 * (1.0 - SIDE[(v, "D")]["total"] / SIDE[(v, "A")]["total"])
              for v in STATED_LOSS]
mean_tot = sum(tot_losses) / len(tot_losses)
ok = abs(mean_tot - 57.0) <= 5.0
fails += not ok
print(f"  mean total-hit loss A->D = {mean_tot:.1f}% vs stated 'about 57%'"
      f"   {'PASS' if ok else 'FAIL'}")

print("\n== C5. base-spray table closes too (cross-table sanity on the reader) ==")
bad = [(v, p) for (v, p), r in BASE.items()
       if abs(r["perf"] + r["penet"] + r["dents"] - r["total"]) > 0.02]
ok = not bad
fails += not ok
print(f"  {len(BASE)} base-spray cells, {len(bad)} failing"
      f"   {'PASS' if ok else 'FAIL'}")

print(f"\nRESULT: {fails} failure(s)")
