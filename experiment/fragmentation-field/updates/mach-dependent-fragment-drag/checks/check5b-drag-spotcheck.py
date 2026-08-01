"""Produces the Check 5b numbers cited in
experiment/fragmentation-field/_validation.qmd (3.5 g fragment at 61 m,
old vs new drag constants) and the mass/range thresholds for the Pk table."""
import numpy as np
from dataclasses import replace
from scipy.optimize import brentq
from arty.fragmentation import (ShellParams, DragParams, retardation_coeff,
                                pk_given_hit, gurney_velocity, _PK_E, _PK_VAL)

shell = ShellParams(caliber=0.105, wall_t=0.011,
                    mass_total=14.97, mass_filler=2.18, mass_deductions=0.75)
V0 = gurney_velocity(shell)
rho_steel = shell.steel.rho
drag_new = DragParams()
drag_old = replace(drag_new, C_D=1.0, C_shape=0.585)

m, s = 3.5e-3, 61.0
print(f"V0 = {V0:.1f} m/s, rho_steel = {rho_steel}")
print(f"Pk table anchors: E={_PK_E} J -> Pk={_PK_VAL} (left=0 below 100 J)")
for name, d in [("old 0.585", drag_old), ("new 2.674", drag_new)]:
    lam = retardation_coeff(np.array([m]), d, rho_steel)[0]
    V = V0*np.exp(-lam*s)
    KE = 0.5*m*V**2
    print(f"{name}: lam={lam:.5f} 1/m  1/lam={1/lam:.1f} m  V(61m)={V:.1f} m/s "
          f"KE={KE:.1f} J  Pk={pk_given_hit(KE):.3f}")

lam_c = drag_new.rho_air*drag_new.C_D*drag_new.C_shape/(2*rho_steel**(2/3))
lam = lam_c*m**(-1/3)
for KE_t, lbl in [(100.0, "Pk onset (0.10)"), (1000.0, "Pk=0.50")]:
    V_t = np.sqrt(2*KE_t/m)
    r = -np.log(V_t/V0)/lam
    mm = brentq(lambda x: 0.5*x*(V0*np.exp(-lam_c*x**(-1/3)*s))**2 - KE_t, 1e-5, 20.0)
    print(f"{lbl}: 3.5 g reaches KE={KE_t:.0f} J at r={r:.1f} m; at 61 m needs m={mm*1e3:.1f} g")

# Sensitivity of the 61 m Pk to combined drag constant
print("\ncombined  lam[1/m]  V(61)  KE(61)   Pk")
for comb in [0.585, 1.0, 1.28, 2.0, 2.674]:
    d = replace(drag_new, C_D=1.0, C_shape=comb)
    lm = retardation_coeff(np.array([m]), d, rho_steel)[0]
    V = V0*np.exp(-lm*s)
    KE = 0.5*m*V**2
    print(f"{comb:7.3f}  {lm:8.5f}  {V:6.1f}  {KE:7.1f}  {pk_given_hit(KE):.3f}")

# --- Cross-check of arty's lambda against the standard engineering decay law ---
# TP-12 (DoD 1975, lines 345-357): L = L1 m^(1/3), L1 = 247 m/kg^(1/3) for
# k = 2.6 g/cm3, C_D = 1.28.  UFC 3-340-02 / TM 5-1300 write the same law as
# V = V0 exp(-0.004 R / W^(1/3)) with R [ft], W [oz]; converting that constant
# to SI shows it *is* TP-12's L1, not an independent datum.
L1_arty = 1.0/retardation_coeff(np.array([1.0]), drag_new, rho_steel)[0]
L1_ufc = 1.0/(0.004/0.0283495**(1/3)*3.280840)      # ft,oz -> m,kg
print(f"\nL1 (m/kg^1/3): arty {L1_arty:.1f} | TP-12 quoted 247 | "
      f"UFC/TM5-1300 0.004-constant {L1_ufc:.1f}")
L1_old = 1.0/retardation_coeff(np.array([1.0]), drag_old, rho_steel)[0]
print(f"L1 with the old 0.585 constant: {L1_old:.0f} m/kg^1/3 "
      f"({L1_old/L1_ufc:.1f}x the standard law)")

# --- Re-banding Check 5b on the WW2-era lethality criterion (58 ft-lb = 78.6 J) ---
# What combined C_D*C_shape does a factor-2 band around 78.6 J admit at 3.5 g / 61 m?
def comb_for_KE(KE_t):
    def f(c):
        return 0.5*m*(V0*np.exp(-drag_new.rho_air*c/(2*rho_steel**(2/3))
                                 * m**(-1/3)*s))**2 - KE_t
    return brentq(f, 1e-3, 20.0)
print(f"\nWW2 criterion 58 ft-lb = 78.6 J -> combined = {comb_for_KE(78.6):.3f}")
print(f"factor-2 band 39.3-157.2 J -> combined in "
      f"[{comb_for_KE(157.2):.2f}, {comb_for_KE(39.3):.2f}] "
      f"(new 2.674 inside; old 0.585 outside)")
