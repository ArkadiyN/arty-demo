"""Posture crossover: A_p(gamma) sweep, N_eff standing vs prone (AoF = 0 slice), lethal area vs AoF.

Consumer: experiment/fragmentation-field/_four-zone-3d.qmd §6.6.1 (values rendered inline
there; this script mirrors those cells standalone) and the status paragraph of
experiment/fragmentation-field/updates/target-area-profile/derivation.md.
Also prints r50_cross, which is NaN (not reached) under the 20 m airburst since
P_kill never reaches 0.5 there.
"""
import numpy as np
from arty.fragmentation import (STANDING, PRONE, presented_area, compute_frag_field_3d,
                                BurstParams, ShellParams, DragParams)
from arty.shells import SHELLS

reg = SHELLS["105mm M1 HE"]
shell = ShellParams(caliber=reg.caliber, wall_t=0.011, mass_total=reg.mass_total,
                    mass_filler=reg.mass_filler, mass_deductions=reg.mass_deductions,
                    filler=reg.filler, steel=reg.steel, aspect_ratio=reg.aspect_ratio)


def run(hb, aof, post, R=60.0, n=121):
    """Field at burst height hb [m], AoF [deg]; box half-extent R [m], n_grid points."""
    return compute_frag_field_3d(
        shell=shell, drag=DragParams(),
        burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
        posture=post, max_radius=R, n_grid=n)


g = np.linspace(0, np.pi / 2, 181)
a_s = np.array([presented_area(x, STANDING) for x in g])
a_p = np.array([presented_area(x, PRONE) for x in g])
i = int(np.argmax(a_p >= a_s))
print(f"crossover gamma (0.5 deg grid): {np.degrees(g[i]):.1f} deg, A_p = {a_s[i]:.3f} m^2")
print(f"A_p ratio prone/standing at gamma=0: {a_p[0]/a_s[0]:.3f}, at 90 deg: {a_p[-1]/a_s[-1]:.3f}")

print("\nAoF = 0 cross-range slice (x = 0)")
for hb in (0.5, 20.0):
    out = {}
    for post, nm in ((STANDING, "standing"), (PRONE, "prone")):
        r = run(hb, 0.0, post)
        half = r.r_cross.size // 2
        pk = np.array([np.interp(x, r.r_cross[half:], r.pk_cross[half:]) for x in (0, 10, 20)])
        ne = np.array([np.interp(x, r.r_cross[half:], r.n_eff_cross[half:]) for x in (0, 10, 20)])
        out[nm] = ne
        print(f"h_b={hb:>4} {nm:>9}  Pk(0,10,20 m)={np.round(pk, 3)}  N_eff={np.round(ne, 3)}  "
              f"max Pk={r.pk_cross.max():.3f}  r50_cross={r.r50_cross}")
    print(f"   N_eff ratio prone/standing (0,10,20 m) = {np.round(out['prone'] / out['standing'], 2)}")

print("\nLethal area ratio prone/standing, +/-200 m box, 1 m spacing (converged, see posture-lethal-area-convergence.py)")
for aof in (0.0, 15.0, 30.0, 45.0, 60.0, 75.0):
    row = []
    for hb in (0.5, 20.0):
        row.append(run(hb, aof, PRONE, 200.0, 401).lethal_area / run(hb, aof, STANDING, 200.0, 401).lethal_area)
    print(f"  AoF={aof:>4}  h_b=0.5: {row[0]:.2f}   h_b=20: {row[1]:.2f}")
