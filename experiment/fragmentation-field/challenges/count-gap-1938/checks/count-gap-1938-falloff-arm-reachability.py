"""Predicted Tolch A->D (15 ft -> 120 ft) perforation falloff ratio at the sourced plug-shear threshold.

Consumer: experiment/fragmentation-field/challenges/count-gap-1938/review.md
(2026-09-23 Pass 1 adversarial critique). Shows the falloff arm is reachable
from the count chain's own arty calls (min_lethal_mass + mott_N) and that it
depends on mu, i.e. on the aspect_ratio moved by 630dac8/18cd069.
Per-unit-solid-angle ratio: N0 and 1/r^2 cancel; only drag, E_thr(m), mu enter.
"""
import dataclasses
from functools import partial

import numpy as np

from arty.fragmentation import (
    _MOTT_ASPECT_RATIO,
    DragParams,
    gurney_velocity,
    min_lethal_mass,
    mott_N,
    mott_params,
)
from arty.perforation import WoodPanelTarget, perforation_threshold_energy
from arty.shells import SHELLS

FT = 0.3048
R_A, R_D = 15 * FT, 120 * FT
TOLCH_AD = 0.557

shipped = SHELLS["75mm M48 HE"]
cases = {
    "pre-c legacy A=1.600": dataclasses.replace(shipped, aspect_ratio=_MOTT_ASPECT_RATIO),
    "2026-08-16 A=1.577": dataclasses.replace(shipped, aspect_ratio=1.577),
    f"live A={shipped.aspect_ratio:.3f}": shipped,
}
V0 = gurney_velocity(shipped)
drag = DragParams()
E_of_m = partial(perforation_threshold_energy, target=WoodPanelTarget())

for lbl, sh in cases.items():
    mu, N0 = mott_params(sh, V0)
    m = [float(min_lethal_mass(r, V0, float("nan"), drag, sh.steel.rho, E_thr=E_of_m))
         for r in (R_A, R_D)]
    NA, ND = (float(mott_N(np.array([x]), N0, mu)[0]) for x in m)
    ratio = ND / NA
    print(f"{lbl:22s} mu={mu*1e3:.3f} g  m_thr A/D = {m[0]*1e3:.3f}/{m[1]*1e3:.3f} g  "
          f"N_A={NA:.0f}  pred D/A = {ratio:.3f}  |pred-0.557| = {abs(ratio-TOLCH_AD):.3f}"
          f"  {'within 0.10' if abs(ratio-TOLCH_AD) <= 0.10 else 'OUTSIDE 0.10'}")
