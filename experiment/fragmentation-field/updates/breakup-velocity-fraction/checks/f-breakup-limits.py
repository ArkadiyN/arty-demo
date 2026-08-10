"""Break-up velocity fraction f(eta; gamma_g): limit checks, geometry bookkeeping,
count-arm movement and the double-count (mean-mass) check.

Produces every number cited in
experiment/fragmentation-field/updates/breakup-velocity-fraction/derivation.md
(sections 4, 5, 6, 8).

Run: uv run python experiment/fragmentation-field/updates/breakup-velocity-fraction/checks/f-breakup-limits.py
"""

import csv
from functools import partial
from pathlib import Path

import numpy as np

from arty.fragmentation import (
    DragParams,
    breakup_velocity_fraction,
    _shell_geometry,
    gurney_velocity,
    min_lethal_mass,
    mott_N,
    mott_params,
)
from arty.perforation import WoodPanelTarget, perforation_threshold_energy
from arty.shells import SHELLS

REPO = next(p for p in Path(__file__).resolve().parents if (p / "doc-reference").is_dir())
TABLES = REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
S_PANEL = 4.572  # Tolch 15 ft panel standoff [m]


def f_asym(eta, g):
    """Released-energy fraction form, normalised at eta -> inf. [-]"""
    v = np.sqrt(1.0 - np.asarray(eta, float) ** (-(g - 1.0)))
    # Cross-check the shipped implementation against this closed form.
    assert np.isclose(float(v.ravel()[0] if v.shape else v),
                      breakup_velocity_fraction(float(np.asarray(eta).ravel()[0]), g))
    return v


def f_norm(eta, g, eta_f):
    """Same, renormalised so f(eta_f) = 1 exactly (Kennedy completion ratio). [-]"""
    num = 1.0 - np.asarray(eta, float) ** (-(g - 1.0))
    den = 1.0 - eta_f ** (-(g - 1.0))
    return np.sqrt(np.minimum(num / den, 1.0))


print("=== (1) limit checks on f(eta) = sqrt(1 - eta^-(gamma_g-1)) ===")
print("  eta ->1+ and eta ->inf, gamma_g = 3 and 2.5")
for g in (3.0, 2.5):
    print(
        f"  gamma_g={g}: f(1.0001)={f_asym(1.0001, g):.4f}  f(1.01)={f_asym(1.01, g):.4f}  "
        f"f(100)={f_asym(100.0, g):.4f}  f(1e4)={f_asym(1e4, g):.6f}"
    )

print("\n=== (2) Kennedy bracket check: f near 1 at eta=7, clearly <1 at eta=2 ===")
print("  gamma_g   f(2)     f(2.7)   f(3)     f(5)     f(7)    1-f(7)")
for g in (3.0, 2.8, 2.5):
    row = [f_asym(e, g) for e in (2.0, 2.7, 3.0, 5.0, 7.0)]
    print(
        f"   {g:4.1f}   " + "  ".join(f"{v:.4f}" for v in row) + f"   {1-row[-1]:.4f}"
    )

print("\n=== (3) upper-bound variant: renormalised at Kennedy's eta_f = 7 (grazing) ===")
print("  gamma_g   f(2)     f(3)     f(7)")
for g in (3.0, 2.5):
    print(
        f"   {g:4.1f}   " + "  ".join(f"{f_norm(e, g, 7.0):.4f}" for e in (2.0, 3.0, 7.0))
    )
print("  (normal-incidence limit eta_f = 2 -> f(eta>=2) = 1, i.e. no correction)")

print("\n=== (4) which radius: eta bookkeeping across the shipped registry ===")
print("  shell                      r_i[mm] r_o[mm] r_bu[mm]  r_bu/r_i  eta_gas  eta_wall  f_gas  f_wall")
for name, sh in SHELLS.items():
    r_o, r_i, r_bu, _M = _shell_geometry(sh)
    r_mean = 0.5 * (r_o + r_i)
    eta_gas = (r_i * np.sqrt(3.0) / r_i) ** 2  # = 3 exactly, by construction
    eta_wall = (r_bu / r_mean) ** 2
    print(
        f"  {name:26s} {r_i*1e3:6.2f} {r_o*1e3:6.2f} {r_bu*1e3:7.2f}  "
        f"{r_bu/r_i:7.3f}  {eta_gas:6.3f}  {eta_wall:7.3f}  "
        f"{f_asym(eta_gas,3.0):.4f}  {f_asym(eta_wall,3.0):.4f}"
    )

# --------------------------------------------------------------- the count arm
shell = SHELLS["75mm M48 HE"]
rho = shell.steel.rho
_r_o, _r_i, _r_bu, M_case = _shell_geometry(shell)
V0 = gurney_velocity(shell)
drag = DragParams()

pit = list(csv.DictReader(open(TABLES / "pit-screen-recovery.csv", newline="")))
N_rec = sum(float(r["n_frag"]) for r in pit)
LB_G = 453.59237
m_rec_mean = sum(float(r["wt_lb"]) for r in pit) * LB_G / N_rec

target = WoodPanelTarget()
thr = partial(perforation_threshold_energy, target=target)


print(f"\n=== (5) count arm, 75mm M48 HE, SPF-S eta=1/2 central row (N_rec={N_rec:.0f}) ===")
print(f"  terminal V0 = {V0:.1f} m/s (unchanged in min_lethal_mass)")
print("     f     mu[g]   2mu[g]    N0    m_thr[g]      N   N/779   ratio_to_f1  f^2")
base = None
for f in (1.0, f_asym(3.0, 3.0), f_asym(3.0, 2.5), f_norm(3.0, 3.0, 7.0), 0.9, 0.8):
    mu, N0 = mott_params(shell, V0, f_breakup=f)
    m_thr = min_lethal_mass(S_PANEL, V0, float("nan"), drag, rho, E_thr=thr)
    N = mott_N(np.array([m_thr]), N0, mu)[0]
    if base is None:
        base = N
    print(
        f"  {f:.4f}  {mu*1e3:6.3f}  {2*mu*1e3:6.3f}  {N0:6.0f}  {m_thr*1e3:7.4f}  "
        f"{N:6.0f}  {N/N_rec:5.2f}   {N/base:9.3f}   {f*f:.3f}"
    )

print("\n=== (6) double-count check: mean fragment mass vs Tolch recovered spectrum ===")
print(f"  Tolch pit-recovered: N = {N_rec:.0f}, mean mass = {m_rec_mean:.2f} g")
for f in (1.0, f_asym(3.0, 3.0), f_asym(3.0, 2.5)):
    mu, N0 = mott_params(shell, V0, f_breakup=f)
    print(
        f"  f={f:.4f}: model 2mu = {2*mu*1e3:.3f} g  -> ratio recovered/model = "
        f"{m_rec_mean/(2*mu*1e3):5.2f}x   N0 = {N0:.0f}"
    )
print("  direction test: f<1 must move 2mu TOWARD the recovered mean while N falls.")
