"""Zone-level effect of the 75 mm M48 mass_deductions change.

Consumer: experiment/fragmentation-field/_four-zone-3d.qmd Sec 6.4 prose note
and _change-log.qmd v0.9.1 entry. Compares the shipped (old 0.200 kg
placeholder) and revised (0.97522 kg fuze+booster) mass_deductions bases
through arty.zones.compute_shell_zones.
"""

from dataclasses import replace

from arty.shells import SHELLS
from arty.zones import compute_shell_zones

new = SHELLS["75mm M48 HE"]
old = replace(new, mass_deductions=0.200)

for label, sh in (("old ded=0.200", old), ("new ded=0.97522", new)):
    z = compute_shell_zones(sh)
    m_case = sh.mass_total - sh.mass_filler - sh.mass_deductions
    print(f"{label}:  M_case = {m_case*1e3:.1f} g")
    for name in ("ogive", "cylinder", "boattail", "base"):
        zz = getattr(z, name)
        print(f"   {name:<9} M={zz.mass_kg:6.3f} kg  frac={zz.mass_kg/m_case:6.3f}"
              f"  V0={zz.V0_ms:7.1f} m/s  spray={zz.spray_deg:5.1f} deg")

zo, zn = compute_shell_zones(old), compute_shell_zones(new)
print("\nV0 ratio new/old by zone:")
for name in ("ogive", "cylinder", "boattail", "base"):
    print(f"   {name:<9} {getattr(zn, name).V0_ms / getattr(zo, name).V0_ms:.4f}")
