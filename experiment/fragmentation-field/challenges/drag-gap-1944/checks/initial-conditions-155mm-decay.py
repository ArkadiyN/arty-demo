"""155mm M107 HE: velocity-decay comparison (model vs source Table 59 CASUALTIES).

Mirrors the 75mm/105mm initial-condition checks. Feeds the model's own
retardation_coeff(m) the source's per-range lightest-effective-fragment mass
m(r) and the source's own V0 (3,500 f/s), computes v_model = V0*exp(-lam*s),
and compares against the source's tabulated v(r).
"""
import numpy as np

from arty.shells import SHELLS
from arty.fragmentation import gurney_velocity, retardation_coeff, DragParams

FT_TO_M = 0.3048
FTS_TO_MS = 0.3048
OZ_TO_KG = 0.028349523125

V0_SRC_FTS = 3500.0
V0_SRC_MS = V0_SRC_FTS * FTS_TO_MS

# Corrected Table 59 CASUALTIES (see 155mm write-up section 1)
r_ft = np.array([20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600], dtype=float)
m_oz = np.array([0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109, 0.161, 0.233, 0.402])
v_fts = np.array([2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505, 383], dtype=float)

shell = SHELLS["155mm M107 HE"]
drag = DragParams()
rho_steel = shell.steel.rho

# (a) Gurney V0
v0_gurney = gurney_velocity(shell)
print(f"(a) Gurney V0 = {v0_gurney:.1f} m/s = {v0_gurney/FTS_TO_MS:.1f} f/s")
print(f"    Source V0 = {V0_SRC_MS:.1f} m/s = {V0_SRC_FTS:.0f} f/s")
print(f"    model/source = {v0_gurney/V0_SRC_MS:.3f}  ({(v0_gurney/V0_SRC_MS-1)*100:+.1f}%)")
print(f"    C/M ratio uses mass_filler={shell.mass_filler}, gurney_const={shell.filler.gurney_const}")
print()

# (c) velocity-decay comparison
s_m = r_ft * FT_TO_M
m_kg = m_oz * OZ_TO_KG
v_src_ms = v_fts * FTS_TO_MS

lam_model = retardation_coeff(m_kg, drag, rho_steel)
v_model_ms = V0_SRC_MS * np.exp(-lam_model * s_m)
ratio_v = v_model_ms / v_src_ms

# source-implied lambda from its own (v(r), V0, s)
lam_src = -np.log(v_src_ms / V0_SRC_MS) / s_m
ratio_lam = lam_src / lam_model

print(f"{'r(ft)':>6} {'m(oz)':>6} {'v_src':>7} {'v_mdl':>7} {'v_m/v_s':>8} "
      f"{'lam_mdl':>8} {'lam_src':>8} {'ls/lm':>6}")
for i in range(len(r_ft)):
    print(f"{r_ft[i]:6.0f} {m_oz[i]:6.3f} {v_fts[i]:7.0f} "
          f"{v_model_ms[i]/FTS_TO_MS:7.0f} {ratio_v[i]:8.2f} "
          f"{lam_model[i]:8.4f} {lam_src[i]:8.4f} {ratio_lam[i]:6.2f}")
