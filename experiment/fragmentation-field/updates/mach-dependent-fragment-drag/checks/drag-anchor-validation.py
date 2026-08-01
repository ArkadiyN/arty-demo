"""Validation numbers for
experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md.

Runs the three checks that derivation.md's Validation section reports, at the
adopted anchor C_D = 1.28, k = 2.60 g/cm3 (=> C_shape = (rho_steel/k)^(2/3)):

  V1  identity check: arty's lambda and DoD-1975's L = 2(k^2 m)^(1/3)/(C_D rho)
      are the same law; unit-mass 1/e distance L1 reproduces the source's
      247 m/kg^(1/3) to within the air-density convention.
  V2  RMS of ln(v_model/v_source) over the 25-point 1944 Ordnance set and over
      its arrival-Mach > 0.7 subset.  Bar: <= 0.10 on the subset.
  V3  155mm M107 m_min / N_leth vs. slant range, old defaults vs. new.

(m, r, v, V0) triples reused verbatim from
challenges/drag-gap-1944/checks/drag-coefficient-calibration.py (and from this
folder's required-retardation-vs-mach.py, which ranked the candidate laws).
"""
import numpy as np

from arty.shells import SHELLS
from arty.fragmentation import DragParams, min_lethal_mass, mott_params, mott_N

FT_TO_M = 0.3048
OZ_TO_KG = 0.028349523125
RHO_AIR = 1.225
A_SOUND = 340.3  # m/s, sea-level standard

K_DOD = 2600.0    # kg/m3, forged steel projectiles & frag bombs (DoD-1975 p.7)
CD_DOD = 1.28     # supersonic-plateau drag coefficient (DoD-1975 p.8, Fig. 3)
RHO_STEEL = 7850.0

C_SHAPE = (RHO_STEEL / K_DOD) ** (2.0 / 3.0)
COMBINED = CD_DOD * C_SHAPE
COMBINED_OLD = 0.65 * 0.90


def lam(m, combined, rho_steel=RHO_STEEL, rho_air=RHO_AIR):
    """Retardation coefficient [1/m] for fragment mass m [kg] (arty form)."""
    return rho_air * combined / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)


def L_dod(m, k=K_DOD, cd=CD_DOD, rho_air=RHO_AIR):
    """DoD-1975 1/e distance L [m] for fragment mass m [kg]."""
    return 2.0 * (k * k * m) ** (1.0 / 3.0) / (cd * rho_air)


# --- V1: identity + L1 ------------------------------------------------------
print("=== V1  identity / L1 ===")
print(f"C_shape = (rho_steel/k)^(2/3) = ({RHO_STEEL:.0f}/{K_DOD:.0f})^(2/3) "
      f"= {C_SHAPE:.4f}   combined = {COMBINED:.4f}")
for m in (1e-4, 1e-3, 1e-2, 1.0):
    print(f"  m={m:8.4g} kg   1/lambda = {1.0 / lam(m, COMBINED):10.3f} m   "
          f"L_DoD = {L_dod(m):10.3f} m   ratio = {L_dod(m) * lam(m, COMBINED):.12f}")
L1_arty = 1.0 / lam(1.0, COMBINED)
print(f"  L1 (arty, rho_air=1.225)  = {L1_arty:.1f} m/kg^(1/3)")
print(f"  L1 (source, quoted)       = 247   m/kg^(1/3)  "
      f"-> ratio {L1_arty / 247.0:.4f}")
rho_match = 2.0 * K_DOD ** (2.0 / 3.0) / (CD_DOD * 247.0)
print(f"  rho_air implied by the source's 247 = {rho_match:.4f} kg/m3")
print(f"  L1 (arty, current 0.585)  = {1.0 / lam(1.0, COMBINED_OLD):.0f} m/kg^(1/3)")
print(f"  k implied by current 0.585 at C_D=1.28: "
      f"{(RHO_STEEL / (COMBINED_OLD / CD_DOD) ** 1.5):.0f} kg/m3")

# --- V1b: geometric limit check --------------------------------------------
# For any closed convex body the mean presented area is 1/4 the surface area
# (DoD-1975 p.7).  Cube of side a: A = 1.5 a^2 = 1.5 V^(2/3)  -> C_shape = 1.5.
# Sphere of radius R:  A = pi R^2 = pi/(4pi/3)^(2/3) V^(2/3).
# Inverting identity (2), k = rho_steel / C_shape^(3/2), so DoD's own tabulated
# k for cubes and spheres must invert back to the density of steel.
GR_PER_IN3_TO_KG_M3 = 64.79891e-6 / 16.387064e-6  # grain/in^3 -> kg/m^3
print("\n=== V1b  geometric limits: invert DoD's k back to rho_steel ===")
CS_CUBE = 1.5
CS_SPHERE = np.pi / (4.0 * np.pi / 3.0) ** (2.0 / 3.0)
for label, cs, k_gr in [("cube", CS_CUBE, 1080.0), ("sphere", CS_SPHERE, 1490.0)]:
    k_si = k_gr * GR_PER_IN3_TO_KG_M3
    print(f"  {label:7s} C_shape(geom) = {cs:.4f}   k(DoD) = {k_gr:.0f} gr/in3 "
          f"= {k_si:.0f} kg/m3   -> rho_steel = {k_si * cs ** 1.5:.0f} kg/m3")
print(f"  forged-steel anchor k = {K_DOD:.0f} kg/m3 -> C_shape = {C_SHAPE:.4f} "
      f"(vs cube {CS_CUBE:.3f}, sphere {CS_SPHERE:.3f})")

# --- V2: 1944 Ordnance velocity decay --------------------------------------
DATA = [
    ("75mm M48 HE", 3120.0, [20, 100, 400],
     [0.014, 0.063, 0.244], [2060, 972, 494]),
    ("105mm M1 HE", 3500.0,
     [20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300],
     [0.035, 0.047, 0.061, 0.095, 0.137, 0.192, 0.255, 0.326, 0.448, 0.580, 1.05],
     [2700, 2430, 2220, 1920, 1750, 1550, 1420, 1320, 1200, 1120, 955]),
    ("155mm M107 HE", 3500.0,
     [20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600],
     [0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109, 0.161, 0.233, 0.402],
     [2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505, 383]),
]
rows = []
for name, v0f, rf, mo, vf in DATA:
    rho_s = SHELLS[name].steel.rho
    for r_, m_, v_ in zip(rf, mo, vf):
        rows.append((rho_s, v0f * FT_TO_M, r_ * FT_TO_M,
                     m_ * OZ_TO_KG, v_ * FT_TO_M))


def rms(combined, subset=None):
    idx = range(len(rows)) if subset is None else subset
    e = [np.log(rows[i][1] * np.exp(-lam(rows[i][3], combined, rows[i][0]) * rows[i][2])
                / rows[i][4]) for i in idx]
    return float(np.sqrt(np.mean(np.square(e))))


sel = [i for i, r in enumerate(rows) if r[4] / A_SOUND > 0.7]
print("\n=== V2  RMS ln(v_model/v_source), 1944 Ordnance ===")
print(f"  n(all) = {len(rows)}   n(arrival M>0.7) = {len(sel)}")
for label, c in [("current 0.585", COMBINED_OLD), (f"adopted {COMBINED:.3f}", COMBINED)]:
    print(f"  {label:22s}  all = {rms(c):.3f}   M>0.7 = {rms(c, sel):.3f}")
print(f"  bar: RMS(M>0.7) <= 0.10  -> "
      f"{'PASS' if rms(COMBINED, sel) <= 0.10 else 'FAIL'}")

# --- V3: demo-visible 155mm lethal-count impact ----------------------------
sh = SHELLS["155mm M107 HE"]
V0, E = 1000.0, 79.0
mu, N0 = mott_params(sh, V0)[:2]
print(f"\n=== V3  155mm M107, V0={V0:.0f} m/s, E_leth={E:.0f} J, "
      f"mu={mu * 1e3:.2f} g, N0={N0:.0f} ===")
print(f"{'s(m)':>5} {'m_min old(g)':>13} {'N old':>7} {'m_min new(g)':>13} "
      f"{'N new':>7} {'dN':>7}")
for s in (5, 10, 20, 30, 50, 80, 120):
    a = min_lethal_mass(s, V0, E, DragParams(), sh.steel.rho)
    b = min_lethal_mass(s, V0, E, DragParams(C_D=CD_DOD, C_shape=C_SHAPE), sh.steel.rho)
    na = mott_N(np.array([a]), N0, mu)[0]
    nb = mott_N(np.array([b]), N0, mu)[0]
    print(f"{s:5.0f} {a * 1e3:13.3f} {na:7.0f} {b * 1e3:13.3f} {nb:7.0f} "
          f"{(nb / na - 1.0) * 100:6.0f}%")
