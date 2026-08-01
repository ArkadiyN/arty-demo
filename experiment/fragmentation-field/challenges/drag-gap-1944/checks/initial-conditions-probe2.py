from arty.shells import SHELLS
from arty.zones import compute_shell_zones

FT_TO_M = 0.3048
MS_TO_FPS = 1/FT_TO_M

SOURCE_V0_FPS = {"75mm M48 HE": 3120, "105mm M1 HE": 3500, "155mm M107 HE": 3500}

for name in ["75mm M48 HE", "105mm M1 HE", "155mm M107 HE"]:
    shell = SHELLS[name]
    zones = compute_shell_zones(shell)
    print(f"\n{name} (source V0 = {SOURCE_V0_FPS[name]} fps):")
    for zname in ["ogive", "cylinder", "boattail", "base"]:
        z = getattr(zones, zname)
        print(f"  {zname:10s}: mass={z.mass_kg:.4f}kg C={z.C_kg:.4f}kg V0={z.V0_ms:.1f} m/s = {z.V0_ms*MS_TO_FPS:.0f} fps  mu={z.mu:.6g}kg spray={z.spray_deg:.1f}deg")
