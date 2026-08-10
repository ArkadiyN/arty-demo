"""Headline numbers for the 0.12.0 Change Log row in experiment/fragmentation-field/_change-log.qmd."""
import numpy as np
from arty.shells import SHELLS
from arty.fragmentation import (breakup_velocity_fraction, gurney_velocity,
                                mott_N, mott_params)

f = breakup_velocity_fraction()
print(f"f = {f:.4f}")
for key in ("WW2 US 105mm M1 HE", *SHELLS.keys()):
    if key not in SHELLS:
        continue
    s = SHELLS[key]
    V0 = gurney_velocity(s)
    mu1, N1 = mott_params(s, V0, f_breakup=1.0)
    mu, N = mott_params(s, V0)
    n1 = mott_N(np.array([0.5e-3]), N1, mu1)[0]
    n = mott_N(np.array([0.5e-3]), N, mu)[0]
    print(f"{key:26s} V0={V0:6.1f} mu {mu1*1e3:.3f}->{mu*1e3:.3f} g  "
          f"N0 {N1:.0f}->{N:.0f} ({N/N1-1:+.1%})  N(>0.5g) {n1:.0f}->{n:.0f} ({n/n1-1:+.1%})")
