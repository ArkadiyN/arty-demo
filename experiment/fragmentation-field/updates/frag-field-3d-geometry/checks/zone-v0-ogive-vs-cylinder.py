"""Zone C/M and V0 audit feeding experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md section 6."""
from arty.shells import SHELLS
from arty.zones import compute_shell_zones

for key in SHELLS:
    s = SHELLS[key]
    z = compute_shell_zones(s)
    print(f"=== {key}  D={s.caliber*1000:.0f}mm  M_s(case)  filler={s.filler.name if hasattr(s.filler,"name") else ""} Vg={s.filler.gurney_const}")
    tot_M = tot_C = tot_C_true = tot_E = 0.0
    for name in ("ogive", "cylinder", "boattail", "base"):
        p = getattr(z, name)
        MC = p.mass_kg / p.C_kg if p.C_kg > 0 else float("inf")
        print(f"  {name:9s} M={p.mass_kg:7.3f} kg  C={p.C_kg:7.4f} kg  M/C={MC:8.2f}  V0={p.V0_ms:7.1f} m/s  theta={p.spray_deg:5.1f}")
        tot_M += p.mass_kg
        tot_C += p.C_kg
        if name != "base":  # base's C_kg is an equivalent-column proxy already
            tot_C_true += p.C_kg  # counted in the cylinder's explosive above
        tot_E += 0.5 * p.V0_ms**2 * (p.mass_kg + 0.5 * p.C_kg)
    print(f"  sum M={tot_M:.3f} kg  sum C={tot_C:.4f} kg (incl. base proxy)  true C={tot_C_true:.4f} kg")
    MC = tot_M / tot_C_true
    V_single = s.filler.gurney_const / (MC + 0.5) ** 0.5
    E_single = 0.5 * V_single**2 * (tot_M + 0.5 * tot_C)
    print(f"  single-zone M/C={MC:.3f}  V0={V_single:.1f} m/s")
    print(f"  Gurney energy: zone-sum={tot_E/1e6:.3f} MJ  single={E_single/1e6:.3f} MJ  C*E={tot_C*s.filler.gurney_const**2/2/1e6:.3f} MJ")
    KE_z = sum(0.5 * getattr(z, n).mass_kg * getattr(z, n).V0_ms**2 for n in ("ogive","cylinder","boattail","base"))
    print(f"  metal KE: zone-sum={KE_z/1e6:.3f} MJ  single={0.5*tot_M*V_single**2/1e6:.3f} MJ")
