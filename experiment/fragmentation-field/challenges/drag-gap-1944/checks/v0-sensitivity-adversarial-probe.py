"""Posture-ratio (prone/standing lethal area) response to a common Gurney V0 scale.

Consumer: experiment/fragmentation-field/challenges/drag-gap-1944/review.md
("V0 sensitivity -- adversarial critique" section) -- tests the argued-not-computed
claim in v0-sensitivity.md section 5 that a common V0 scale cannot move the
posture comparison (target-area-profile review: 0.92 at AoF 30, h_b 20 m, 105 mm).
"""
import csv
import dataclasses
import pathlib
import time

import numpy as np

import arty.fragmentation as F
from arty.shells import SHELLS

sh0 = SHELLS["105mm M1 HE"]
PRONE = getattr(F, "PRONE")
STANDING = getattr(F, "STANDING")
t0 = time.time()
for (aof, hb), (R, n) in [(c, g) for g in ((60.0, 121), (200.0, 401))
                          for c in ((30.0, 20.0), (15.0, 20.0), (30.0, 10.0))]:
    row = []
    for s in (0.86, 0.9, 1.0, 1.1):
        sh = dataclasses.replace(sh0, filler=dataclasses.replace(
            sh0.filler, gurney_const=sh0.filler.gurney_const * s))
        b = F.BurstParams(h_b=hb, angle_of_fall=aof, spray_half_angle=15.0)
        la = {}
        for name, post in (("prone", PRONE), ("standing", STANDING)):
            r = F.compute_frag_field_3d(sh, burst=b, posture=post, max_radius=R, n_grid=n)
            la[name] = r.lethal_area
        row.append(f"s={s:.2f}: P/S={la['prone']/la['standing']:.3f}")
    print(f"box=+-{R:.0f} m n={n} AoF={aof:4.0f} h_b={hb:4.0f}  " + "  ".join(row))
print(f"({time.time()-t0:.1f} s)")

# ---- Pooled V2 RMS(M>0.7) with the model's own per-caliber Gurney V0 (argued, not computed, in v0-sensitivity.md s3)
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "doc-reference").is_dir())
TAB = ROOT / "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"
FT, OZ, A_SOUND = 0.3048, 0.028349523125, 340.3
STEM = {"75mm M48 HE": "75mm-m48", "105mm M1 HE": "105mm-m1", "155mm M107 HE": "155mm-m107"}
drag = F.DragParams()
C = drag.C_D * drag.C_shape
for col in ("casualties", "perforation-1-8in"):
    res = []
    for shell, stem in STEM.items():
        sh = SHELLS[shell]
        g = F.gurney_velocity(sh)
        with (TAB / f"{stem}-{col}.csv").open() as fh:
            for row in csv.DictReader(fh):
                r, m, v = float(row["r_ft"]) * FT, float(row["m_oz"]) * OZ, float(row["v_fps"]) * FT
                if v / A_SOUND <= 0.7:
                    continue
                x = drag.rho_air / (2.0 * sh.steel.rho ** (2 / 3)) * m ** (-1 / 3) * r
                res.append(np.log(g / v) - C * x)
    res = np.array(res)
    print(f"V2 with Gurney V0 {col:18s} n={res.size} RMS={np.sqrt(np.mean(res**2)):.3f} bias={res.mean():+.3f}")
