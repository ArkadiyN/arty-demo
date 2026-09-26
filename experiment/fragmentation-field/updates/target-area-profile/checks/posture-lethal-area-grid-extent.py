"""Grid-extent (truncation) probe for the §6.6.1 whole-field lethal-area ratio.

Consumer: experiment/fragmentation-field/updates/target-area-profile/review.md,
"Re-review — adversarial, 2026-09-26 (fix cycle 1)". Recomputes
FragField3dResult.lethal_area prone/standing at fixed 1 m spacing for box
half-extents 60 / 100 / 150 / 200 / 250 m, and reports the max P_kill on the box edge of
the 60 m run, to test whether the notebook's 120 m x 120 m box truncates the field.
"""
import time
from arty.fragmentation import (STANDING, PRONE, compute_frag_field_3d,
                                BurstParams, ShellParams, DragParams)
from arty.shells import SHELLS

reg = SHELLS["105mm M1 HE"]
shell = ShellParams(caliber=reg.caliber, wall_t=0.011, mass_total=reg.mass_total,
                    mass_filler=reg.mass_filler, mass_deductions=reg.mass_deductions,
                    filler=reg.filler, steel=reg.steel, aspect_ratio=reg.aspect_ratio)

t0 = time.time()
print("AoF   h_b  R_box  LA_stand  LA_prone  ratio  edgePk_s  edgePk_p")
for aof in (0.0, 15.0, 30.0, 45.0, 60.0, 75.0):
    for hb in (0.5, 20.0):
        for R in (60.0, 100.0, 150.0, 200.0, 250.0):
            n = int(2 * R) + 1  # 1 m spacing
            la, edge = {}, {}
            for post, nm in ((STANDING, "s"), (PRONE, "p")):
                r = compute_frag_field_3d(shell=shell, drag=DragParams(),
                                          burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
                                          posture=post, max_radius=R, n_grid=n)
                la[nm] = r.lethal_area
                pk = r.field_pk
                edge[nm] = float(max(pk[0].max(), pk[-1].max(), pk[:, 0].max(), pk[:, -1].max()))
            print(f"{aof:4.0f} {hb:5.1f} {R:6.0f} {la['s']:9.1f} {la['p']:9.1f} {la['p']/la['s']:6.3f}"
                  f"  {edge['s']:8.4f}  {edge['p']:8.4f}", flush=True)
print(f"elapsed {time.time()-t0:.1f} s")
