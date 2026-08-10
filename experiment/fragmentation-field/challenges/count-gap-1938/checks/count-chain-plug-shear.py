"""Check 4: re-run the count-gap-1938 N/779 chain under the A" plug-shear threshold.

Produces the numbers cited as "Check 4" in
experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/derivation.md
§7.4, and in the Check-4 rows of
experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md,
experiment/fragmentation-field/_limitations.qmd and
experiment/fragmentation-field/challenges/README.md.

This is the sibling of count-chain-rebaseline.py block (D): identical chain,
identical recovered-count denominator (N_rec = 779 from the re-baselined
pit-screen CSV), with the mass-independent scalar E_thr replaced by the
mass-dependent plug-shear callable
arty.perforation.perforation_threshold_energy (derivation.md §7.3 eq. 9).

Per derivation.md A8, eta is NOT free to be tuned to match a count; the eta = 1
row below is the rigid *upper bound* of the pre-registered band, printed for
range, not selected for agreement.

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-plug-shear.py
"""

import csv
from functools import partial
from pathlib import Path

import numpy as np

from arty.fragmentation import (
    DragParams,
    _shell_geometry,
    gurney_velocity,
    ke_at_range,
    min_lethal_mass,
    mott_N,
    mott_params,
    retardation_coeff,
)
from arty.perforation import (
    ETA_RIGID,
    TAU_SPFS,
    TAU_SPFS_COV,
    TAU_SYP,
    WoodPanelTarget,
    ballistic_limit_velocity,
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
LB_G = 453.59237
S_PANEL = 4.572  # Tolch's 15 ft panel standoff [m], as used in block (D)


def load(name):
    with open(TABLES / f"{name}.csv", newline="") as fh:
        return list(csv.DictReader(fh))


# ------------------------------------------------ denominator: re-baselined 779
pit = load("pit-screen-recovery")
n_frag = np.array([float(r["n_frag"]) for r in pit])
N_rec = n_frag.sum()

# ------------------------------------------------------------------- the model
shell = SHELLS["75mm M48 HE"]
rho = shell.steel.rho
_r_o, _r_i, _r_bu, M_case = _shell_geometry(shell)
V0 = gurney_velocity(shell)
drag = DragParams()
mu, N0 = mott_params(shell, V0)

print("=== model, 75mm M48 HE (same basis as count-chain-rebaseline.py block C) ===")
print(f"M_case = {M_case*1e3:.1f} g   V0 = {V0:.1f} m/s   mu = {mu*1e3:.3f} g   N0 = {N0:.0f}")
print(f"denominator N_rec = {N_rec:.0f} recovered fragments; panel count = 700")

# ----------------------------------------- (G1) scalar reference rows, verbatim
print("\n=== (G1) scalar-threshold reference rows (block D, unchanged) ===")
print("  these are plausibility probes / fits, NOT sourced perforation thresholds")
for E_scalar, label in [
    (78.6, "1944 Ordnance casualty criterion, 58 ft-lb - NOT a perforation thr"),
    (126.0, "Tolch hole-size bound"),
]:
    m_thr = min_lethal_mass(S_PANEL, V0, E_scalar, drag, rho)
    N = mott_N(np.array([m_thr]), N0, mu)[0]
    print(
        f"  E_thr={E_scalar:6.1f} J const  m_thr={m_thr*1e3:6.3f} g  N={N:6.0f}  "
        f"N/700={N/700:5.2f}  N/779={N/N_rec:5.2f}   [{label}]"
    )

# ------------------------------------------ (G2) Check 4: plug-shear, A" band
print("\n=== (G2) CHECK 4 - plug-shear threshold E_thr(m) = eta tau pi D(m) t^2 ===")
print("  variant                          m_thr[g]  E_thr(m_thr)[J]  v50[m/s]      N   N/700  N/779")
variants = [
    ("SPF-S, eta=1/2  (CENTRAL)", WoodPanelTarget()),
    ("SPF-S -1sigma, eta=1/2", WoodPanelTarget(tau=TAU_SPFS * (1 - TAU_SPFS_COV))),
    ("SPF-S +1sigma, eta=1/2", WoodPanelTarget(tau=TAU_SPFS * (1 + TAU_SPFS_COV))),
    ("SYP, eta=1/2", WoodPanelTarget(tau=TAU_SYP)),
    ("SPF-S, eta=1 (rigid bound)", WoodPanelTarget(eta=ETA_RIGID)),
    ("SYP, eta=1 (band max)", WoodPanelTarget(tau=TAU_SYP, eta=ETA_RIGID)),
]
rows = []
for label, tgt in variants:
    thr = partial(perforation_threshold_energy, target=tgt)
    m_thr = min_lethal_mass(S_PANEL, V0, float("nan"), drag, rho, E_thr=thr)
    E_at = float(perforation_threshold_energy(m_thr, tgt))
    v50 = float(ballistic_limit_velocity(m_thr, tgt))
    N = mott_N(np.array([m_thr]), N0, mu)[0]
    rows.append((label, m_thr, E_at, v50, N))
    print(
        f"  {label:32s} {m_thr*1e3:7.3f}  {E_at:14.1f}  {v50:8.1f}  {N:6.0f}  "
        f"{N/700:5.2f}  {N/N_rec:5.2f}"
    )

# ------------------------------------- (G3) the pre-registered direction check
print("\n=== (G3) pre-registered direction (derivation.md §7.4) ===")
m_central = rows[0][1]
m_786 = min_lethal_mass(S_PANEL, V0, 78.6, drag, rho)
lam = retardation_coeff(np.array([m_central]), drag, rho)
v_arr = float(
    np.sqrt(
        2
        * ke_at_range(np.array([m_central]), V0, lam, np.array([S_PANEL]))[0]
        / m_central
    )
)
print(f"  m_thr(plug-shear central) = {m_central*1e3:.3f} g")
print(f"  m_thr(78.6 J constant)    = {m_786*1e3:.3f} g")
print(f"  arrival velocity of the plug-shear m_thr at s = {S_PANEL} m: {v_arr:.0f} m/s")
print(
    "  prediction was: A\" admits LIGHTER fragments (m_thr down, N up) if the "
    "arrival\n  velocity exceeds the 243 m/s crossover; otherwise the reverse."
)
print(
    f"  observed: m_thr {'DOWN' if m_central < m_786 else 'UP'} vs the 78.6 J probe, "
    f"N ratio {rows[0][4]/mott_N(np.array([m_786]), N0, mu)[0]:.2f}x"
)

# crossover check, reported from the model rather than restated
m_grid = np.logspace(-6, -2, 20001)
v_cross = np.sqrt(2 * perforation_threshold_energy(m_grid) / m_grid)
ke_eq = 78.6
v_78 = np.sqrt(2 * ke_eq / m_grid)
i = int(np.argmin(np.abs(v_cross - v_78)))
print(
    f"  E_thr crossover: plug-shear == 78.6 J at m = {m_grid[i]*1e3:.3f} g, "
    f"v = {v_cross[i]:.0f} m/s"
)
