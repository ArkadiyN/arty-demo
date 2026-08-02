"""Decompose Tolch's ~4-6x absolute perforating-count over-prediction.

Produces the numbers cited in
experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md
(Sections 3 and 5): where in the count chain the 75mm M48 residual sits, and
how much of it is the fitted-threshold artefact vs. a genuine N0/spectrum error.

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-decomposition.py
"""

import numpy as np

from arty.fragmentation import (
    DragParams,
    gurney_velocity,
    min_lethal_mass,
    mott_N,
    mott_params,
    _shell_geometry,
)
from arty.shells import SHELLS

shell = SHELLS["75mm M48 HE"]
rho = shell.steel.rho
r_o, r_i, r_bu, M_case = _shell_geometry(shell)
V0_model = gurney_velocity(shell)

print(f"case mass         = {M_case*1e3:8.1f} g   (Tolch shell body 6030 g)")
print(f"r_bu              = {r_bu*1e3:8.2f} mm")
print(f"V0 (Gurney)       = {V0_model:8.1f} m/s")

V0_tolch = 838.2  # Tolch Summary item 10, measured perforating-fragment velocity
drag = DragParams()
print(f"C_D*C_shape       = {drag.C_D*drag.C_shape:8.3f}")

for V0 in (V0_model, V0_tolch):
    mu, N0 = mott_params(shell, V0)
    print(f"\n--- V0 = {V0:.1f} m/s ---")
    print(f"mu = {mu*1e3:.3f} g   N0 = {N0:.0f}   mean frag mass 2mu = {2*mu*1e3:.2f} g")

    # (a) the fitted-threshold operating point (scoping.md 3d, DoD anchor row)
    for E_thr, label in (
        (1.9, "fitted E_thr lo (falloff-ratio fit @2.67)"),
        (3.6, "fitted E_thr hi (falloff-ratio fit @2.67)"),
        (78.6, "1944 Ordnance Dept. card's own casualty threshold, 58 ft-lb"),
        (126.0, "Tolch hole-size bound, m>=0.36 g @838 m/s"),
        (294.5, "pre-anchor fitted E_thr (0.585 drag)"),
    ):
        m_thr = min_lethal_mass(4.572, V0, E_thr, drag, rho)  # 15 ft = 4.572 m
        N = mott_N(np.array([m_thr]), N0, mu)[0]
        print(
            f"  E_thr={E_thr:7.1f} J -> m_thr(15ft)={m_thr*1e3:7.3f} g  "
            f"N={N:7.0f}  N/N0={N/N0:5.2f}  N/700={N/700:5.2f}  N/803={N/803:5.2f}"
        )

# (b) sensitivity of N0 to the velocity that sets the fracture spacing x0.
# mott_params uses the terminal Gurney V0 for x0; break-up happens earlier.
print("\n--- N0 sensitivity to break-up velocity fraction f = v_bu/V0 ---")
mu_ref, N0_ref = mott_params(shell, V0_model)
for f in (1.0, 0.9, 0.8, 0.7, 0.6):
    mu_f, N0_f = mott_params(shell, f * V0_model)
    print(
        f"  f={f:4.2f}  mu={mu_f*1e3:6.3f} g  N0={N0_f:7.0f}  "
        f"N0/N0_ref={N0_f/N0_ref:5.2f}  mu/mu_ref={mu_f/mu_ref:5.2f}"
    )

# (b2) combined: the two non-fitted thresholds (78.6 J, 126 J) evaluated at
# each break-up velocity fraction f, so C2's leverage is measured against a
# sourced threshold rather than a fitted one (count-chain.md C2, corrects the
# "cannot be measured against anything" claim for these two rows only).
print("\n--- Combined: non-fitted E_thr x break-up velocity fraction f ---")
for f in (1.0, 0.9, 0.8, 0.7, 0.6):
    mu_f, N0_f = mott_params(shell, f * V0_model)
    for E_thr, label in (
        (78.6, "1944 Ordnance Dept. card"),
        (126.0, "Tolch hole-size bound"),
    ):
        m_thr = min_lethal_mass(4.572, f * V0_model, E_thr, drag, rho)
        N = mott_N(np.array([m_thr]), N0_f, mu_f)[0]
        print(
            f"  f={f:4.2f}  E_thr={E_thr:6.1f} J ({label:24s})  "
            f"m_thr={m_thr*1e3:7.3f} g  N={N:7.0f}  N/700={N/700:5.2f}  N/803={N/803:5.2f}"
        )

# (c) how much of N0 sits below Tolch's finest screen cut (0.63 g)
mu, N0 = mott_params(shell, V0_model)
for cut_g in (0.63, 0.36, 0.13, 0.05):
    N_above = mott_N(np.array([cut_g * 1e-3]), N0, mu)[0]
    print(
        f"  cut {cut_g:5.2f} g: N(>=cut)={N_above:7.0f} "
        f"({100*N_above/N0:4.1f}% of N0)   [Tolch pit: 803 recovered, mean 6.85 g]"
    )
