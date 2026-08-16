"""Re-runs the Tolch (1938) absolute-perforating-count objection to raising the
fragment drag constant, using the *post-shape-closure* Mott parameters.

Feeds experiment/fragmentation-field/updates/mach-dependent-fragment-drag/scoping.md
(section "Does Tolch still veto a higher drag constant?").

Method reproduces challenges/drag-gap-1944/tolch-1938-panel-distance.md Result 2:
E_thr is the single free parameter, fitted so that the model reproduces Tolch's
observed Panel A (15 ft) -> Panel D (120 ft) perforation-density ratio 0.557;
the *absolute* count N(m >= m_thr(15 ft)) is then a prediction, compared with
Tolch's measured ~700-780 perforations per shell (panel count ~700; pit-test
recovery 779, re-baselined from a published 803).

`mott_params(SHELL, V0)` is called with its default `f_breakup` (no override),
so this script's output moves whenever `breakup_velocity_fraction()` does —
it silently picked up the count-gap-1938 C2 break-up-velocity-fraction change
(commit 74abdd7, 2026-08-10) without being re-run, which is why the table
printed here does not match the one quoted in scoping.md/review.md until this
script is re-run and the doc restated (2026-08-16 restatement). The resolved
`f` is now printed below so a future drift is visible without diffing source.
"""
import numpy as np
from scipy.optimize import brentq

from arty.shells import SHELLS
from arty.fragmentation import (
    DragParams,
    _shell_geometry,
    breakup_velocity_fraction,
    min_lethal_mass,
    mott_N,
    mott_params,
)

FT = 0.3048
R_A, R_D = 15 * FT, 120 * FT
RATIO_OBS = 0.557
# Tolch's two independent estimates of the same quantity (perforating fragments
# per shell at 15 ft): "about 700 perforations" from the panel densities
# (Summary item 6), and 779 fragments recovered in the pit test (Summary items
# 1 and 8; "practically all the fragments obtained in pit tests would be
# perforating fragments in panel tests at 15 ft"). The pit count is 779, NOT
# the 803 that circulated in earlier artifacts — see
# challenges/count-gap-1938/rebaseline-verdict.md. Normalise on the midpoint,
# and report the span too.
TOLCH_PERF_LO, TOLCH_PERF_HI = 700.0, 779.0
TOLCH_PERFORATIONS = 0.5 * (TOLCH_PERF_LO + TOLCH_PERF_HI)  # 739.5

SHELL = SHELLS["75mm M48 HE"]
RHO_S = SHELL.steel.rho


def ratio_for(E, c, V0, mu, N0):
    ma = min_lethal_mass(R_A, V0, E, DragParams(C_D=c, C_shape=1.0), RHO_S)
    md = min_lethal_mass(R_D, V0, E, DragParams(C_D=c, C_shape=1.0), RHO_S)
    na = mott_N(np.array([ma]), N0, mu)[0]
    nd = mott_N(np.array([md]), N0, mu)[0]
    return nd / na, ma, na


def main():
    m_body = _shell_geometry(SHELL)[3]
    print(f"75mm M48 HE, shell body {m_body*1e3:.0f} g, rho_steel {RHO_S:.0f}")
    print(f"f_breakup (default, unpinned) = {breakup_velocity_fraction():.4f}")
    print(f"Tolch observed: {TOLCH_PERF_LO:.0f}-{TOLCH_PERF_HI:.0f} perforating "
          f"fragments per shell at 15 ft (normalising on "
          f"{TOLCH_PERFORATIONS:.1f})\n")
    print(f"{'V0':>7} {'2mu(g)':>7} {'N0':>7} {'C_DC_s':>7} {'E_thr(J)':>9} "
          f"{'m_thr15(g)':>11} {'N_perf':>8} {'N/obs':>6} {'N/779':>6} "
          f"{'N/700':>6}")
    for V0 in (807.5, 838.2, 951.0):
        mu, N0 = mott_params(SHELL, V0)[:2]
        for c in (0.585, 1.2, 1.7, 2.20, 2.67):
            try:
                E = brentq(lambda e: ratio_for(e, c, V0, mu, N0)[0] - RATIO_OBS,
                           1e-4, 5e4, xtol=1e-6, rtol=1e-10)
            except ValueError:
                print(f"{V0:7.1f} {2*mu*1e3:7.3f} {N0:7.0f} {c:7.3f}  "
                      f"no bracket")
                continue
            _, ma, na = ratio_for(E, c, V0, mu, N0)
            print(f"{V0:7.1f} {2*mu*1e3:7.3f} {N0:7.0f} {c:7.3f} {E:9.2f} "
                  f"{ma*1e3:11.4f} {na:8.0f} {na/TOLCH_PERFORATIONS:6.1f} "
                  f"{na/TOLCH_PERF_HI:6.1f} {na/TOLCH_PERF_LO:6.1f}")
        print()


if __name__ == "__main__":
    main()
