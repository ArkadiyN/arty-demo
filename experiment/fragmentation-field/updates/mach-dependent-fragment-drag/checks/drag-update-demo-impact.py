"""Demo-visible impact of raising combined C_D*C_shape from 0.585 to the
DoD-1975 value 2.67: minimum lethal fragment mass and lethal reach.
Feeds updates/mach-dependent-fragment-drag/scoping.md ("what visibly changes").
"""
import numpy as np
from arty.shells import SHELLS
from arty.fragmentation import DragParams, min_lethal_mass, mott_params, mott_N

sh = SHELLS["155mm M107 HE"]
V0 = 1000.0
E = 79.0  # J, ~58 ft-lb casualty threshold
mu, N0 = mott_params(sh, V0)[:2]
print(f"155mm: mu={mu*1e3:.2f} g  N0={N0:.0f}  V0={V0} m/s  E_leth={E} J")
print(f"{'s(m)':>5} {'m_min old(g)':>13} {'N_leth old':>11} {'m_min new(g)':>13} {'N_leth new':>11}")
for s in (5, 10, 20, 30, 50, 80, 120):
    a = min_lethal_mass(s, V0, E, DragParams(), sh.steel.rho)
    b = min_lethal_mass(s, V0, E, DragParams(C_D=2.67, C_shape=1.0), sh.steel.rho)
    print(f"{s:5.0f} {a*1e3:13.3f} {mott_N(np.array([a]),N0,mu)[0]:11.0f}"
          f" {b*1e3:13.3f} {mott_N(np.array([b]),N0,mu)[0]:11.0f}")
