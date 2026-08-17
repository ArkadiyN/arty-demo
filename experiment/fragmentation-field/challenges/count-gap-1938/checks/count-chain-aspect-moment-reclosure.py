"""Re-close the count-gap-1938 count chain against the shipped per-shell aspect-ratio moment c.

Consumer: experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md
(banner, sec.1-4) and rebaseline-verdict.md (sec.4 re-baseline table, sec.5),
and the count-gap-1938 rows of experiment/fragmentation-field/challenges/README.md.

Commit 5d742b4 shipped ShellParams.aspect_ratio = mott_aspect_ratio(<shell>)
= 1.6 * MOTT_ASPECT_MOMENT_C[<shell>] in arty.shells.SHELLS; for 75mm M48 HE
c = 0.9854, so A_eff 1.600 -> 1.577.  mu ~ alpha^(-2/3 * -3/2) = alpha ~ A_eff,
so mu scales by exactly c and N0 = M/2mu by 1/c.  Every count in the thread was
last closed against the bare A_eff = 1.600 default, i.e. against the LEGACY
column below; the SHIPPED column is what src/arty produces today.

This script prints both columns for every figure the thread cites, so the
re-closure is auditable line by line rather than scaled by hand.  (N does NOT
scale as 1/c: N = N0 exp(-sqrt(m_thr/mu)) and the falling mu partly eats the
rising N0 -- see the realised-leverage rows.)

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-aspect-moment-reclosure.py
"""

import csv
import dataclasses
from functools import partial
from pathlib import Path

import numpy as np

from arty.fragmentation import (
    _MOTT_ASPECT_RATIO,
    MOTT_ASPECT_MOMENT_C,
    DragParams,
    _shell_geometry,
    breakup_velocity_fraction,
    gurney_velocity,
    min_lethal_mass,
    mott_N,
    mott_params,
)
from arty.perforation import (
    ETA_RIGID,
    TAU_SPFS,
    TAU_SPFS_COV,
    TAU_SYP,
    WoodPanelTarget,
    perforation_threshold_energy,
)
from arty.shells import SHELLS

REPO = next(
    p for p in Path(__file__).resolve().parents if (p / "doc-reference").is_dir()
)
TABLES = (
    REPO
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)
S_PANEL = 4.572  # Tolch's 15 ft panel standoff [m]
N_PANEL = 700.0  # Tolch's panel perforation count (Summary item 6)

with open(TABLES / "pit-screen-recovery.csv", newline="") as fh:
    N_REC = sum(float(r["n_frag"]) for r in csv.DictReader(fh))  # 779

shipped = SHELLS["75mm M48 HE"]
legacy = dataclasses.replace(shipped, aspect_ratio=_MOTT_ASPECT_RATIO)
V0 = gurney_velocity(shipped)  # aspect ratio does not enter Gurney
drag = DragParams()
_ro, _ri, _rbu, M_case = _shell_geometry(shipped)

CASES = (("legacy A=1.600", legacy), ("shipped A=1.577", shipped))
c75 = MOTT_ASPECT_MOMENT_C["75mm M48 HE"]

print("=== (A) the shipped change, 75mm M48 HE ===")
print(f"  c = {c75:.4f}   A_eff = 1.6*c = {1.6*c75:.4f}   f_breakup = "
      f"{breakup_velocity_fraction():.3f}   V0 = {V0:.1f} m/s   M_case = {M_case*1e3:.0f} g")
for lbl, sh in CASES:
    mu, N0 = mott_params(sh, V0)
    print(f"  {lbl:16s}  mu = {mu*1e3:.3f} g   2mu = {2*mu*1e3:.3f} g   N0 = {N0:.0f}")


def N_at_mass(sh, m_g):
    mu, N0 = mott_params(sh, V0)
    return float(mott_N(np.array([m_g * 1e-3]), N0, mu)[0])


def N_at_Ethr(sh, E_thr):
    mu, N0 = mott_params(sh, V0)
    m_thr = min_lethal_mass(S_PANEL, V0, E_thr, drag, sh.steel.rho)
    return float(m_thr) * 1e3, float(mott_N(np.array([m_thr]), N0, mu)[0]), N0


print("\n=== (B) sec.1 scalar-E_thr table (m_thr unchanged: it never sees mu) ===")
print(f"{'E_thr[J]':>9} {'m_thr[g]':>9} | {'N legacy':>9} {'%N0':>5} {'/700':>6} {'/779':>6}"
      f" | {'N shipped':>10} {'%N0':>5} {'/700':>6} {'/779':>6}")
for E in (1.9, 3.6, 78.6, 126.0, 294.5):
    cells = []
    for _lbl, sh in CASES:
        m_thr, N, N0 = N_at_Ethr(sh, E)
        cells.append((m_thr, N, N / N0, N / N_PANEL, N / N_REC))
    (m_thr, Nl, fl, p7l, p8l), (_m, Ns, fs, p7s, p8s) = cells
    print(f"{E:9.1f} {m_thr:9.3f} | {Nl:9.0f} {100*fl:4.0f}% {p7l:6.2f} {p8l:6.2f}"
          f" | {Ns:10.0f} {100*fs:4.0f}% {p7s:6.2f} {p8s:6.2f}")

# ---------------------------------------------------- sec.2 plug-shear verdict
panel = WoodPanelTarget()
tau_lo = TAU_SPFS * (1.0 - TAU_SPFS_COV)
tau_hi = TAU_SPFS * (1.0 + TAU_SPFS_COV)
VARIANTS = (
    ("SPF-S eta=1/2 (VERDICT)", WoodPanelTarget()),
    ("SPF-S -1sigma eta=1/2", WoodPanelTarget(tau=tau_lo)),
    ("SPF-S +1sigma eta=1/2", WoodPanelTarget(tau=tau_hi)),
    ("SYP eta=1/2", WoodPanelTarget(tau=TAU_SYP)),
    ("SPF-S eta=1 rigid", WoodPanelTarget(eta=ETA_RIGID)),
    ("SYP eta=1 rigid", WoodPanelTarget(tau=TAU_SYP, eta=ETA_RIGID)),
)

print("\n=== (C) sec.2 verdict table, plug-shear E_thr(m) ===")
print(f"{'variant':>24} {'m_thr[g]':>9} | {'N legacy':>9} {'/700':>6} {'/779':>6}"
      f" | {'N shipped':>10} {'/700':>6} {'/779':>6}")
verdict = {}
for lbl, tgt in VARIANTS:
    row = []
    for case, sh in CASES:
        E_of_m = partial(perforation_threshold_energy, target=tgt)
        mu, N0 = mott_params(sh, V0)
        m_thr = float(min_lethal_mass(S_PANEL, V0, float("nan"), drag,
                                      sh.steel.rho, E_thr=E_of_m))
        N = float(mott_N(np.array([m_thr]), N0, mu)[0])
        row.append((m_thr * 1e3, N))
        if lbl.endswith("(VERDICT)"):
            verdict[case] = (m_thr * 1e3, N)
    (m_thr, Nl), (_m, Ns) = row
    print(f"{lbl:>24} {m_thr:9.3f} | {Nl:9.0f} {Nl/N_PANEL:6.2f} {Nl/N_REC:6.2f}"
          f" | {Ns:10.0f} {Ns/N_PANEL:6.2f} {Ns/N_REC:6.2f}")

# f = 1 (C1 alone) parenthesised column of the same table
print("\n  same verdict row at f_breakup = 1.0 (C1 alone, the parenthesised column):")
for case, sh in CASES:
    E_of_m = partial(perforation_threshold_energy, target=panel)
    mu, N0 = mott_params(sh, V0, f_breakup=1.0)
    m_thr = float(min_lethal_mass(S_PANEL, V0, float("nan"), drag,
                                  sh.steel.rho, E_thr=E_of_m))
    N = float(mott_N(np.array([m_thr]), N0, mu)[0])
    print(f"    {case:16s} N = {N:.0f}   /700 = {N/N_PANEL:.2f}x   /779 = {N/N_REC:.2f}x")

print("\n=== (D) C2 f-band sweep on the verdict row (breakup-velocity-fraction sec.8) ===")
for f in (0.953, 0.943, 0.899):
    cells = []
    for case, sh in CASES:
        E_of_m = partial(perforation_threshold_energy, target=panel)
        mu, N0 = mott_params(sh, V0, f_breakup=f)
        m_thr = float(min_lethal_mass(S_PANEL, V0, float("nan"), drag,
                                      sh.steel.rho, E_thr=E_of_m))
        cells.append(float(mott_N(np.array([m_thr]), N0, mu)[0]))
    print(f"  f = {f:.3f}   legacy /779 = {cells[0]/N_REC:.2f}x   "
          f"shipped /779 = {cells[1]/N_REC:.2f}x")

print("\n=== (E) fixed-mass cuts (C3/C5 windows) ===")
print(f"{'cut [g]':>8} | {'N legacy':>9} {'/700':>6} {'/779':>6} | {'N shipped':>10} {'/700':>6} {'/779':>6}")
for cut in (0.630, 0.360, 0.166, 0.130, 0.050):
    Nl, Ns = (N_at_mass(sh, cut) for _c, sh in CASES)
    print(f"{cut:8.3f} | {Nl:9.0f} {Nl/N_PANEL:6.2f} {Nl/N_REC:6.2f}"
          f" | {Ns:10.0f} {Ns/N_PANEL:6.2f} {Ns/N_REC:6.2f}")

print("\n=== (F) C5 detection-floor bound, criterion-matched /700 denominator ===")
for case, sh in CASES:
    N_v = verdict[case][1]
    N_det = N_at_mass(sh, 0.36)
    print(f"  {case:16s} verdict N = {N_v:.0f} ({N_v/N_PANEL:.2f}x/700)   "
          f"floor 0.36 g N = {N_det:.0f} ({N_det/N_PANEL:.2f}x/700)   "
          f"realised C5 leverage = {N_v/N_det:.3f}x")

print("\n=== (G) C3 unvalidated-window census (0.166-0.63 g) ===")
for case, sh in CASES:
    N_v = verdict[case][1]
    N_63 = N_at_mass(sh, 0.63)
    print(f"  {case:16s} verdict N = {N_v:.0f}   N(>=0.63 g) = {N_63:.0f}   "
          f"window = {N_v-N_63:.0f} ({100*(N_v-N_63)/N_v:.0f}% of the count)   "
          f"floor if window emptied = {N_63/N_REC:.2f}x/779")
