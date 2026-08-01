from arty.shells import SHELLS
from arty.fragmentation import gurney_velocity
from arty.zones import compute_shell_zones

FT_TO_M = 0.3048
MS_TO_FPS = 1/FT_TO_M

for name in ["75mm M48 HE", "105mm M1 HE", "155mm M107 HE"]:
    shell = SHELLS[name]
    V0 = gurney_velocity(shell)
    print(name, "single-cylinder Gurney V0 =", V0, "m/s =", V0*MS_TO_FPS, "fps")
    zones = compute_shell_zones(shell)
    print("  zone M/C, V0 per zone:")
    for z in ["ogive","cyl","bt","base"]:
        Mz = getattr(zones, f"M_{z}", None)
        Cz = getattr(zones, f"C_{z}", None)
        print("   zone attrs:", [a for a in dir(zones) if not a.startswith("_")])
        break
