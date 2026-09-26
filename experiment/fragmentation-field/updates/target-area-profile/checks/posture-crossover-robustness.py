"""Adversarial robustness probe for _four-zone-3d.qmd §6.6.1 posture crossover.

Consumer: experiment/fragmentation-field/updates/target-area-profile/review.md,
"Review pass 1 — adversarial critique, 2026-09-26 (§6.6.1 posture crossover)", and the
status paragraph of updates/target-area-profile/derivation.md §7 item 7.
Prints prone/standing ratios of P_kill and of N_eff = -ln(1-P_kill) (exact inverse of
pk_cross = 1-exp(-N_eff_cross) in compute_frag_field_3d) across cross-range, h_b and AoF,
plus the A_p ratio at the geometric arrival elevation atan(h_b/r).
"""
import numpy as np
from arty.fragmentation import (STANDING, PRONE, presented_area, compute_frag_field_3d,
                                BurstParams, ShellParams, DragParams)
from arty.shells import SHELLS

reg = SHELLS["105mm M1 HE"]
shell = ShellParams(caliber=reg.caliber, wall_t=0.011, mass_total=reg.mass_total,
                    mass_filler=reg.mass_filler, mass_deductions=reg.mass_deductions,
                    filler=reg.filler, steel=reg.steel, aspect_ratio=reg.aspect_ratio)
print("A_p(0) prone/standing =", presented_area(0.0, PRONE) / presented_area(0.0, STANDING))
rs = (0, 5, 10, 15, 20, 25, 30, 40, 50)
for aof in (0.0, 30.0, 45.0, 60.0):
    for hb in (0.5, 5.0, 10.0, 20.0):
        res = {}
        for post, nm in ((STANDING, "s"), (PRONE, "p")):
            r = compute_frag_field_3d(shell=shell, drag=DragParams(),
                                      burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
                                      posture=post, max_radius=60.0, n_grid=121)
            half = r.r_cross.size // 2
            res[nm] = np.array([np.interp(x, r.r_cross[half:], r.pk_cross[half:]) for x in rs])
        with np.errstate(divide="ignore", invalid="ignore"):
            pr = res["p"] / res["s"]
            nr = np.log1p(-np.minimum(res["p"], 1 - 1e-15)) / np.log1p(-np.minimum(res["s"], 1 - 1e-15))
        apr = [presented_area(np.arctan2(hb, max(x, 1e-9)), PRONE) / presented_area(np.arctan2(hb, max(x, 1e-9)), STANDING) for x in rs]
        print(f"AoF={aof:>4} hb={hb:>4}  maxPk s/p={res['s'].max():.3f}/{res['p'].max():.3f}")
        print("   r      " + " ".join(f"{x:>6}" for x in rs))
        print("   Pk rat " + " ".join(f"{v:6.2f}" for v in pr))
        print("   N  rat " + " ".join(f"{v:6.2f}" for v in nr))
        print("   Ap rat " + " ".join(f"{v:6.2f}" for v in apr))

# Field-integrated lethal area sum(P_kill) dA, prone/standing, over the full 2D grid
print("\nLethal area [m^2] standing / prone and ratio (full 2D field, 120 m x 120 m, n_grid=121)")
for aof in (0.0, 15.0, 30.0, 45.0, 60.0, 75.0):
    for hb in (0.5, 10.0, 20.0):
        la = {}
        for post, nm in ((STANDING, "s"), (PRONE, "p")):
            r = compute_frag_field_3d(shell=shell, drag=DragParams(),
                                      burst=BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0),
                                      posture=post, max_radius=60.0, n_grid=121)
            dA = (120.0 / 120) ** 2
            la[nm] = float(r.field_pk.sum() * dA)
        print(f"  AoF={aof:>4} hb={hb:>4}  LA_s={la['s']:8.1f}  LA_p={la['p']:8.1f}  p/s={la['p']/max(la['s'],1e-12):5.2f}")
