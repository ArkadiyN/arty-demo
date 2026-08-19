"""l/x0 = 2*pi*r_bu/x0 for every shipped shell.

Consumer: experiment/fragmentation-field/updates/kappa-x-shell-regime/scoping.md
(the "is the ruled-line regime caliber-dependent?" question).

Reproduces the x0 of arty.fragmentation.mott_params line-for-line, then forms
the ruled-line length in units of x0 -- the single control parameter of Mott
1947's Monte Carlo.
"""

import numpy as np

from arty.fragmentation import breakup_velocity_fraction, _shell_geometry, gurney_velocity
from arty.shells import SHELLS



f = breakup_velocity_fraction()
print(f"break-up velocity fraction f = {f:.4f}\n")
print(f"{'shell':<16} {'r_bu[mm]':>9} {'V0[m/s]':>8} {'v_bu[m/s]':>9} "
      f"{'a=sqrt(2sf/rg)':>15} {'x0[mm]':>8} {'l/x0':>8} {'kx*x0[mm]':>10}")

for name, sh in SHELLS.items():
    r_o, r_i, r_bu, m_shell = _shell_geometry(sh)
    V0 = gurney_velocity(sh)
    v_bu = f * V0
    a = np.sqrt(2.0 * sh.steel.sigma_f / (sh.steel.rho * sh.steel.gamma))
    x0 = a * r_bu / v_bu
    ell = 2.0 * np.pi * r_bu / x0
    print(f"{name:<16} {r_bu*1e3:9.2f} {V0:8.1f} {v_bu:9.1f} {a:15.2f} "
          f"{x0*1e3:8.3f} {ell:8.1f} {1.5*x0*1e3:10.3f}")

print("\nl/x0 = 2*pi*v_bu/a  -- r_bu cancels identically, so the regime is set")
print("by break-up velocity and steel constants only, NOT by caliber.")
for name, sh in SHELLS.items():
    V0 = gurney_velocity(sh)
    a = np.sqrt(2.0 * sh.steel.sigma_f / (sh.steel.rho * sh.steel.gamma))
    print(f"  {name:<16} 2*pi*v_bu/a = {2*np.pi*f*V0/a:8.2f}")
