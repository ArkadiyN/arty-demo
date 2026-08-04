"""Consistent-mass-basis recomputation of the count-gap-1938 threshold-free test.

Produces the numbers cited in
experiment/fragmentation-field/challenges/source-data-audit/review-void-rulings.md
section 2 (adversarial review of the "1.2-2.7x" band).

Tolch's own weight table (tolch-1938.md, anchor "Wt. empty shell & fuze")
separates fuze (2.35 lb) from the empty shell body (10.94 lb). The committed
check script normalises recovered CASE mass by a fuze-INCLUSIVE denominator,
which is what produces its 1.19x floor. This script redoes the same
matched-cumulative-mass-fraction test on a fuze-consistent basis.

Run: uv run python experiment/_scratch/tolch-case-mass-basis.py
"""

import csv
from pathlib import Path

import numpy as np

REPO = next(p for p in Path(__file__).resolve().parents if (p / "doc-reference").is_dir())
TABLES = REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
LB_G = 453.59237

rows = list(csv.DictReader(open(TABLES / "pit-screen-recovery.csv", newline="")))
n = np.array([float(r["n_frag"]) for r in rows])
w = np.array([float(r["wt_lb"]) for r in rows]) * LB_G
screens = [r["screen"] for r in rows]

# Tolch weight table closure: loaded unfuzed 12.50 - TNT 1.56 + fuze 2.35 = 13.29
LOADED_UNFUZED, TNT, FUZE, EMPTY_PLUS_FUZE = 12.50, 1.56, 2.35, 13.29
print("Tolch weight-table closure (lb):")
print(f"  12.50 - 1.56 + 2.35 = {LOADED_UNFUZED - TNT + FUZE:.2f}  (printed {EMPTY_PLUS_FUZE})")
CASE_LB = LOADED_UNFUZED - TNT
CASE_G = CASE_LB * LB_G
print(f"  empty shell body (case metal, no fuze, no TNT) = {CASE_LB:.2f} lb = {CASE_G:.1f} g")

M_CASE_MODEL = 5755.2  # printed by count-chain-rebaseline.py block (C)
MU_G, N0_MODEL = 0.793, 3627.0
print(f"  model M_case = {M_CASE_MODEL:.1f} g = {M_CASE_MODEL/LB_G:.2f} lb "
      f"-> model / Tolch case = {M_CASE_MODEL/CASE_G:.3f}")

# recovery closure on a case-only basis: screen 1 is "mostly pieces of fuze"
rec_all, rec_case = w.sum(), w[1:].sum()
print(f"  recovered all = {rec_all:.1f} g = {100*rec_all/(EMPTY_PLUS_FUZE*LB_G):.1f} % of shell+fuze")
print(f"  screen-1 mass = {w[0]:.1f} g vs fuze weight {FUZE*LB_G:.1f} g")
print(f"  recovered case (screens 2..thru4) = {rec_case:.1f} g = {100*rec_case/CASE_G:.1f} % of case")

x = np.linspace(0.0, 30.0, 300_001)
phi = (x**2 + 2 * x + 2) * np.exp(-x) / 2.0
def inv(p):
    return np.interp(p, phi[::-1], x[::-1])


cum_n, cum_w = np.cumsum(n[1:]), np.cumsum(w[1:])
print("\nthreshold-free test, fuze-consistent (case metal both sides):")
print("  screen | cum n | cum w [g] |  phi   |  m*[g] | N(model M) | ratio | N(Tolch M) | ratio")
for s, cn, cw in zip(screens[1:], cum_n, cum_w):
    p = cw / CASE_G
    u = inv(p)
    n_model = N0_MODEL * np.exp(-u)
    n_tolchmass = (CASE_G / (2 * MU_G)) * np.exp(-u)
    print(f"  {s:>6s} | {cn:5.0f} | {cw:9.1f} | {p:6.4f} | {MU_G*u**2:6.2f} | "
          f"{n_model:10.0f} | {n_model/cn:5.2f}x | {n_tolchmass:10.0f} | {n_tolchmass/cn:5.2f}x")
