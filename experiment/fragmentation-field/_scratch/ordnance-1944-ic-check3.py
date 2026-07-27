import numpy as np
from arty.shells import SHELLS
from arty.zones import compute_shell_zones
from arty.fragmentation import DragParams, build_mmin_table, gurney_velocity

FT_TO_M = 0.3048
KG_TO_OZ = 35.27396
MS_TO_FPS = 1/FT_TO_M
E_LETH = 58.0 * 1.3558179483314004  # J

drag = DragParams()

SOURCE = {
    "75mm M48 HE": {
        "r_ft": [20,30,40,60,80,100,130,160,190,225],
        "m_oz": [0.014,0.018,0.082,0.037,0.051,0.063,0.090,0.116,0.173,0.244],
        "v_fps": [2060,1820,2010,1270,1080,972,813,716,587,494],
    },
    "105mm M1 HE": {
        "r_ft": [20,30,40,60,80,100,120,140,170,200,300],
        "m_oz": [0.010,0.014,0.019,0.030,0.043,0.055,0.083,None,None,None,None],
        "v_fps": [2440,2060,1770,1410,1180,1040,846,None,None,None,None],
    },
    "155mm M107 HE": {
        "r_ft": [20,30,40,60,80,100,120,140,170,200,300,400],
        "m_oz": [0.010,0.014,0.019,0.030,0.043,0.055,0.083,None,None,None,None,None],
        "v_fps": [2440,2060,1770,1410,1180,1040,846,None,None,None,None,None],
    },
}

for name, dat in SOURCE.items():
    shell = SHELLS[name]
    zones = compute_shell_zones(shell)
    rho_steel = shell.steel.rho
    V0_cyl = zones.cylinder.V0_ms
    V0_single = gurney_velocity(shell)
    r_ft = np.array(dat["r_ft"], dtype=float)
    s_m = r_ft * FT_TO_M
    s_grid = np.linspace(0.01, s_m.max()*1.1, 2000)

    print(f"\n=== {name} ===  V0_cyl={V0_cyl:.1f} m/s ({V0_cyl*MS_TO_FPS:.0f} fps), V0_single={V0_single:.1f} m/s ({V0_single*MS_TO_FPS:.0f} fps)")
    for V0_label, V0 in [("cyl", V0_cyl), ("single", V0_single)]:
        mmin_grid = build_mmin_table(s_grid, V0, E_LETH, drag, rho_steel)
        m_model = np.interp(s_m, s_grid, mmin_grid)
        v_model = np.sqrt(2*E_LETH/m_model)
        print(f"  -- using V0={V0_label} --")
        print(f"  {'r_ft':>6} {'m_src(oz)':>10} {'m_model(oz)':>12} {'m_ratio':>8} {'v_src(fps)':>10} {'v_model(fps)':>12} {'v_ratio':>8}")
        for i in range(len(r_ft)):
            m_src = dat["m_oz"][i]
            v_src = dat["v_fps"][i]
            m_mod_oz = m_model[i]*KG_TO_OZ
            v_mod_fps = v_model[i]*MS_TO_FPS
            if m_src is None:
                print(f"  {r_ft[i]:6.0f} {'--':>10} {m_mod_oz:12.4f} {'--':>8} {'--':>10} {v_mod_fps:12.1f} {'--':>8}")
            else:
                print(f"  {r_ft[i]:6.0f} {m_src:10.4f} {m_mod_oz:12.4f} {m_mod_oz/m_src:8.2f} {v_src:10.0f} {v_mod_fps:12.1f} {v_mod_fps/v_src:8.3f}")
