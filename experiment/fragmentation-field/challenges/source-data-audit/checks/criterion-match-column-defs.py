"""Column-definition closures for the criterion-match review
(experiment/fragmentation-field/challenges/source-data-audit/review-criterion-match.md).

Checks, on all six 1944 Ordnance CSVs:
  (a) B == N / (4 pi r^2)   -> B is a WHOLE-SPHERE AVERAGE areal density
  (b) 0.5 m v^2 in ft-lb    -> which column carries the fixed 58 ft-lb criterion
  (c) implied exp-decay lambda from the stated INITIAL FRAGMENT VELOCITY
"""
import csv
import math
import pathlib

ROOT = pathlib.Path("/home/arkadiy/arty_demo/.claude/worktrees/fix+source-data-fidelity-gate")
T = ROOT / "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"
V0 = {"75mm-m48": 3120.0, "105mm-m1": 3500.0, "155mm-m107": 3500.0}

for stem in V0:
    for col in ("casualties", "perforation-1-8in"):
        rows = list(csv.DictReader((T / f"{stem}-{col}.csv").open()))
        print(f"\n== {stem}-{col}")
        print(f"  {'r_ft':>5} {'N':>5} {'B_tab':>8} {'N/4pir^2':>9} {'B ratio':>8} "
              f"{'E ftlb':>7} {'lam 1/ft':>9}")
        for row in rows:
            r = float(row["r_ft"])
            N = float(row["N"])
            B = float(row["B"])
            m = float(row["m_oz"])
            v = float(row["v_fps"])
            Bs = N / (4.0 * math.pi * r * r)
            E = 0.5 * (m / 16.0 / 32.174) * v * v
            lam = math.log(V0[stem] / v) / r
            print(f"  {r:5.0f} {N:5.0f} {B:8.4f} {Bs:9.4f} {B/Bs:8.3f} "
                  f"{E:7.1f} {lam:9.5f}")

# ---- lambda * m^(1/3) drift: is the source's decay a constant-C_D exponential?
print("\n\n== lambda * m^(1/3) [oz^(1/3)/ft], per column (constant => const-C_D exp)")
for stem in V0:
    for col in ("casualties", "perforation-1-8in"):
        rows = list(csv.DictReader((T / f"{stem}-{col}.csv").open()))
        vals = []
        for row in rows:
            r = float(row["r_ft"])
            m = float(row["m_oz"])
            v = float(row["v_fps"])
            vals.append(math.log(V0[stem] / v) / r * m ** (1.0 / 3.0))
        print(f"  {stem}-{col}: first={vals[0]:.5f} last={vals[-1]:.5f} "
              f"drift={vals[0]/vals[-1]:.2f}x  min={min(vals):.5f} max={max(vals):.5f}")

# ---- Is B_model a whole-sphere average?  Cross-check against the INDEPENDENT
# count-gap-1938 chain, which prints N(>= m_thr) for the SAME shell, SAME
# E_thr = 78.6 J = 58 ft-lb, SAME DragParams, at r = 15 ft.
# If B_model is whole-sphere:  N_implied = B_model * 4 pi r^2  should land near
# that N.  If B_model were belt/zone-local, N_implied would be 4-10x too small.
print("\n\n== B_model -> implied whole-sphere N at r = 20 ft "
      "(B_model from b-vs-range-rebaseline.md)")
B_MODEL_20FT = {"75mm M48 HE": 0.323, "105mm M1 HE": 0.46, "155mm M107 HE": 0.4786}
CARD_N_20FT = {"75mm M48 HE": 1070, "105mm M1 HE": 1160, "155mm M107 HE": 1460}
for shell, b in B_MODEL_20FT.items():
    n_imp = b * 4.0 * math.pi * 20.0 ** 2
    print(f"  {shell:16s} B_model={b:.4f} -> N_implied(20 ft) = {n_imp:6.0f}   "
          f"card N = {CARD_N_20FT[shell]:5d}  ratio {n_imp/CARD_N_20FT[shell]:.2f}")
print("  75mm independent anchor: count-chain-rebaseline.py section (D) prints")
print("    N(>= m_thr) = 1779 at E_thr = 78.6 J, r = 15 ft, same shell/drag.")
print(f"    whole-sphere hypothesis: 1623 at 20 ft vs 1779 at 15 ft "
      f"-> {1623/1779:.3f} (8.8% decay over 5 ft) - CONSISTENT")
print("    belt-local hypothesis (30 deg belt, solid-angle fraction ~0.26):")
print(f"    implied total N = {1623*0.26:.0f}, i.e. {1779/(1623*0.26):.1f}x below"
      " the independent count - REJECTED")
