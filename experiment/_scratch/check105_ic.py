import numpy as np
from arty.shells import SHELLS
from arty.fragmentation import gurney_velocity, retardation_coeff
from arty.zones import DragParams

shell = SHELLS["105mm M1 HE"]
V0_model = gurney_velocity(shell)
print("mass_total, mass_filler, mass_deductions:", shell.mass_total, shell.mass_filler, shell.mass_deductions)
mass_shell = shell.mass_total - shell.mass_filler - shell.mass_deductions
print("mass_shell:", mass_shell, "C/M:", shell.mass_filler/mass_shell)
print("gurney_const:", shell.filler.gurney_const)
print("V0_model (m/s):", V0_model, " (f/s):", V0_model/0.3048)

V0_source_fps = 3500.0
V0_source = V0_source_fps * 0.3048
print("V0_source (m/s):", V0_source)
print("ratio model/source:", V0_model/V0_source, " pct diff:", (V0_model-V0_source)/V0_source*100)

# Table 51 CASUALTIES, energy-validated identification (see report), oz->kg, fps->m/s
OZ_TO_KG = 0.0283495
FPS_TO_MPS = 0.3048
FT_TO_M = 0.3048

rows = [
    (20,.010,2440),(30,.014,2060),(40,.019,1770),(60,.030,1410),(80,.043,1180),
    (100,.055,1040),(150,.083,846),(200,.109,738),(300,.166,598),(400,.232,507),(500,.312,438)
]

drag = DragParams()
rho_steel = shell.steel.rho

FT_LB_TO_J = 1.3558179483314004
E_leth = 58.0*FT_LB_TO_J

print(f"\n{'r(ft)':>6} {'m(oz)':>7} {'v_src(fps)':>10} {'KE(ftlb)':>9} {'lam_model':>10} {'v_model(fps)':>12} {'ratio_v':>8} {'lam_src':>10} {'lam_ratio':>10}")
for r_ft, m_oz, v_fps in rows:
    m_kg = m_oz*OZ_TO_KG
    v_mps = v_fps*FPS_TO_MPS
    r_m = r_ft*FT_TO_M
    lam_model = retardation_coeff(np.array([m_kg]), drag, rho_steel)[0]
    v_model = V0_source * np.exp(-lam_model*r_m)  # use SOURCE V0 for apples-to-apples per sibling method
    ke = 0.5*(m_oz/16/32.174)*v_fps**2
    # source-implied lambda: v_src = V0_source * exp(-lam_src * r)  => lam_src = -ln(v/V0)/r
    lam_src = -np.log(v_mps/V0_source)/r_m if r_m>0 else float('nan')
    ratio_v = (v_model/FPS_TO_MPS)/v_fps
    lam_ratio = lam_src/lam_model
    print(f"{r_ft:6.0f} {m_oz:7.3f} {v_fps:10.0f} {ke:9.1f} {lam_model:10.5f} {v_model/FPS_TO_MPS:12.1f} {ratio_v:8.3f} {lam_src:10.5f} {lam_ratio:10.2f}")
