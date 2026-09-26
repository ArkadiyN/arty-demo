"""R50 before (argmin |P_k-0.5|) vs after (arty r50_cross_slice / r50_outer).

Consumer: experiment/fragmentation-field/updates/r50-not-reached/derivation.md, "Before / after".
The "before" column re-applies the deleted argmin rule to the same P_k slice.
"""
import numpy as np
from arty.fragmentation import (STANDING, PRONE, compute_frag_field_3d, compute_frag_field,
                                BurstParams, ShellParams, DragParams)
from arty.shells import SHELLS

reg = SHELLS["105mm M1 HE"]
shell_105 = ShellParams(caliber=reg.caliber, wall_t=0.011, mass_total=reg.mass_total,
                        mass_filler=reg.mass_filler, mass_deductions=reg.mass_deductions,
                        filler=reg.filler, steel=reg.steel, aspect_ratio=reg.aspect_ratio)


def before_3d(res, max_radius, n_grid):
    """Return the old argmin R50 [m] on the result's cross-range slice."""
    xy = np.linspace(-max_radius, max_radius, n_grid)
    return float(abs(xy[np.argmin(np.abs(res.pk_cross - 0.5))]))


cases = [
    # label, shell, h_b, AoF, posture, max_radius, n_grid
    ("105 M1 hb=20 AoF=0 standing", shell_105, 20.0, 0.0, STANDING, 60.0, 121),
    ("105 M1 hb=20 AoF=0 prone", shell_105, 20.0, 0.0, PRONE, 60.0, 121),
    ("105 M1 hb=0.5 AoF=0 standing", shell_105, 0.5, 0.0, STANDING, 60.0, 121),
    ("105 M1 hb=0.5 AoF=0 prone", shell_105, 0.5, 0.0, PRONE, 60.0, 121),
    ("default hb=0.5 AoF=30 standing", ShellParams(), 0.5, 30.0, STANDING, 80.0, 80),
    ("default hb=10 AoF=30 standing", ShellParams(), 10.0, 30.0, STANDING, 80.0, 80),
    ("default hb=10 AoF=30 prone", ShellParams(), 10.0, 30.0, PRONE, 80.0, 80),
]
for lab, sh, hb, aof, post, R, n in cases:
    res = compute_frag_field_3d(shell=sh, drag=DragParams(),
                                burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
                                posture=post, max_radius=R, n_grid=n)
    print(f"{lab:34s} maxPk={res.pk_cross.max():.3f}  before={before_3d(res, R, n):6.2f} m"
          f"  after={res.r50_cross:6.2f} m  grid step={2 * R / (n - 1):.2f} m")

res1 = compute_frag_field()
old1 = float(res1.r[np.argmin(np.abs(res1.p_kill - 0.5))])
print(f"{'1D compute_frag_field default':34s} maxPk={res1.p_kill.max():.3f}  before={old1:6.2f} m"
      f"  after={res1.r50:6.2f} m  grid step={res1.r[1] - res1.r[0]:.2f} m")
