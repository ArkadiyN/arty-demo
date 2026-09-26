"""Box-extent and grid-spacing convergence of the §6.6.1 whole-field lethal-area ratio.

Consumer: experiment/fragmentation-field/_four-zone-3d.qmd §6.6.1
(tbl-posture-lethal-area-aof grid choice) and the status paragraph of
experiment/fragmentation-field/updates/target-area-profile/derivation.md.
Compares prone/standing FragField3dResult.lethal_area for candidate grids
(half-extent R [m], n_grid) against a wide fine reference (R = 300 m, 1 m spacing),
M1 105 mm, delta = 15 deg, and times each grid.
"""
import time
from arty.fragmentation import (STANDING, PRONE, compute_frag_field_3d,
                                BurstParams, ShellParams, DragParams)
from arty.shells import SHELLS

reg = SHELLS["105mm M1 HE"]
shell = ShellParams(caliber=reg.caliber, wall_t=0.011, mass_total=reg.mass_total,
                    mass_filler=reg.mass_filler, mass_deductions=reg.mass_deductions,
                    filler=reg.filler, steel=reg.steel, aspect_ratio=reg.aspect_ratio)

GRIDS = ((150.0, 151), (200.0, 201), (200.0, 401), (300.0, 601))  # last = reference
AOFS = (0.0, 30.0, 75.0)
HBS = (0.5, 20.0)

res, cost = {}, {}
for R, n in GRIDS:
    t0 = time.time()
    for aof in AOFS:
        for hb in HBS:
            la = {}
            for post, nm in ((STANDING, "s"), (PRONE, "p")):
                la[nm] = compute_frag_field_3d(
                    shell=shell, drag=DragParams(),
                    burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
                    posture=post, max_radius=R, n_grid=n).lethal_area
            res[(R, n, aof, hb)] = (la["s"], la["p"], la["p"] / la["s"])
    cost[(R, n)] = (time.time() - t0) / (len(AOFS) * len(HBS) * 2)
    print(f"grid R={R:.0f} n={n}: {cost[(R, n)]:.2f} s per field run", flush=True)

ref = GRIDS[-1]
print("\n AoF   h_b  grid(R,n)    LA_stand  LA_prone  ratio  d_ratio_vs_ref  d_LAstand_vs_ref")
for aof in AOFS:
    for hb in HBS:
        rs, rp, rr = res[(ref[0], ref[1], aof, hb)]
        for R, n in GRIDS:
            s, p, q = res[(R, n, aof, hb)]
            print(f"{aof:4.0f} {hb:5.1f}  ({R:3.0f},{n:3d})  {s:9.1f} {p:9.1f} {q:6.3f}"
                  f"  {100 * (q / rr - 1):+7.2f} %  {100 * (s / rs - 1):+7.2f} %")
