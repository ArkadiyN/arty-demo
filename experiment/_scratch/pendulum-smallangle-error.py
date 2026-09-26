"""Produces the small-angle error figures cited in
experiment/_smoketest-pendulum/updates/pendulum-period/review.md
(section "Adversarial critique -- pendulum-period").

T_exact / T_small = (2/pi) * K(sin^2(theta0/2)), K = complete elliptic
integral of the first kind (parameter-m convention, as scipy uses).
"""

import numpy as np
from scipy.special import ellipk

for deg in [5, 10, 15, 20, 30, 45, 60, 90, 120, 179]:
    m = np.sin(np.radians(deg) / 2.0) ** 2
    ratio = (2.0 / np.pi) * ellipk(m)
    print(f"theta0={deg:5.0f} deg  T_exact/T_small={ratio:.6f}  error={100 * (ratio - 1):8.3f} %")
