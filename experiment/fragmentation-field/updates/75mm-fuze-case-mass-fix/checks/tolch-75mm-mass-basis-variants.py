"""Case-mass / Gurney / Mott sensitivity to the 75mm M48 mass_deductions basis.

Produces the numbers cited in
experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/scoping.md and
.../derivation.md (variant table: M_case, V0, mu, N0 under each candidate mass
basis, plus the Mott mass-closure and cross-basis M_case agreement checks).

Run: uv run python experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/tolch-75mm-mass-basis-variants.py
"""

import dataclasses

import numpy as np

from arty.fragmentation import gurney_velocity, mott_N, mott_params
from arty.shells import SHELLS

LB = 0.45359237  # kg per lb

base = SHELLS["75mm M48 HE"]

# Tolch (1938) weight row, tolch-1938.md anchor "Wt. empty shell & fuze":
#   loaded unfuzed 12.50 lb; fuze M39 P.D. 2.35 lb; TNT 1.56 lb;
#   empty shell & fuze 13.29 lb.  Closure: 12.50 - 1.56 + 2.35 = 13.29.
TOLCH_LOADED_UNFUZED, TOLCH_TNT, TOLCH_FUZE, TOLCH_EMPTY_FUZE = 12.50, 1.56, 2.35, 13.29
assert abs((TOLCH_LOADED_UNFUZED - TOLCH_TNT + TOLCH_FUZE) - TOLCH_EMPTY_FUZE) < 5e-3
TOLCH_CASE = TOLCH_LOADED_UNFUZED - TOLCH_TNT           # 10.94 lb, case metal alone
TOLCH_COMPLETE = TOLCH_LOADED_UNFUZED + TOLCH_FUZE      # 14.85 lb, complete round

# Production basis (variant E, adopted in derivation.md).  All three fields
# from in-repo processed sources:
#   mass_total   14.6 lb  "Mean weight of loaded and fuzed projectile"
#                TM-9-1904 source.pdf p.414, grep "Fuzes M48, M48A1 and M54"
#   mass_filler  1.47 lb  official M48 gun filler (shipped value, unchanged)
#   mass_deduct  M48 fuze 1.41 lb (TM-9-1901 sec.319.b, grep "weight, 1.41
#                pounds") + M20/M20A1 booster stood in by the closure-checked
#                M21A2 increment 0.74 lb (TM-9-1901 card "Closure Invariant":
#                2.15-1.41 = 2.16-1.42 = 0.74 lb) = 2.15 lb.
PROD_TOTAL, PROD_TNT = 14.6, 1.47
M48_FUZE, BOOSTER_INC = 1.41, 0.74
assert abs((2.15 - 1.41) - BOOSTER_INC) < 5e-3   # M51A3 - M48A2 pair
assert abs((2.16 - 1.42) - BOOSTER_INC) < 5e-3   # M55A2 - M54   pair
PROD_DED = M48_FUZE + BOOSTER_INC                # 2.15 lb fuze + booster
PROD_CASE = PROD_TOTAL - PROD_TNT - PROD_DED     # 10.98 lb, case metal alone

variants = {
    "A shipped (placeholder ded=0.200)": dict(),
    "B TM-9-1901 M48 fuze only (1.41 lb)": dict(mass_deductions=M48_FUZE * LB),
    "C full Tolch rebaseline": dict(
        mass_total=TOLCH_COMPLETE * LB,
        mass_filler=TOLCH_TNT * LB,
        mass_deductions=TOLCH_FUZE * LB,
    ),
    "D residual ded, TM total/filler kept": dict(
        mass_deductions=base.mass_total - base.mass_filler - TOLCH_CASE * LB,
    ),
    "E production basis (ADOPTED)": dict(
        mass_total=PROD_TOTAL * LB,
        mass_filler=PROD_TNT * LB,
        mass_deductions=PROD_DED * LB,
    ),
}

print(f"Tolch case metal  = {TOLCH_CASE:.2f} lb = {TOLCH_CASE * LB * 1e3:.1f} g")
print(f"Tolch complete rd = {TOLCH_COMPLETE:.2f} lb = {TOLCH_COMPLETE * LB * 1e3:.1f} g")
print()
hdr = f"{'variant':38s} {'ded[g]':>8s} {'M_case[g]':>10s} {'vs Tolch':>9s} " \
      f"{'V0[m/s]':>8s} {'mu[g]':>7s} {'N0':>7s}"
print(hdr)
shells = {}
for name, over in variants.items():
    s = dataclasses.replace(base, **over) if over else base
    shells[name] = s
    m_case = s.mass_total - s.mass_filler - s.mass_deductions
    v0 = gurney_velocity(s)
    mu, n0 = mott_params(s, v0)
    print(
        f"{name:38s} {s.mass_deductions*1e3:8.1f} {m_case*1e3:10.1f} "
        f"{m_case / (TOLCH_CASE * LB):8.3f}x {v0:8.1f} {mu*1e3:7.3f} {n0:7.0f}"
    )

# --- derivation.md checks -------------------------------------------------
E = shells["E production basis (ADOPTED)"]
m_case_E = E.mass_total - E.mass_filler - E.mass_deductions
v0_E = gurney_velocity(E)
mu_E, n0_E = mott_params(E, v0_E)

print()
print("Check 1  weight-row closure 12.50 - 1.56 + 2.35 = 13.29 lb .......... PASS (assert)")
print("Check 1b booster increment closes on two pairs at 0.74 lb ........... PASS (assert)")

# Check 2: cross-basis agreement on the ONLY quantity the physics consumes.
d = m_case_E / (TOLCH_CASE * LB) - 1.0
print(f"Check 2  M_case production {m_case_E*1e3:.1f} g vs Tolch case metal "
      f"{TOLCH_CASE*LB*1e3:.1f} g -> {d*100:+.2f} %  (bar +/-3 %)  "
      f"{'PASS' if abs(d) < 0.03 else 'FAIL'}")

# Check 3: Mott mass closure -- integral of m*(-dN/dm) over [0,inf) = 2*N0*mu = M_case.
# Numerically, on a dense grid out to many mu, against the shell's own M_case.
# Truncating at x0 = sqrt(m_max/mu) leaves a tail 2*N0*mu*(x0+1)*exp(-x0);
# x0 = 20 (m_max = 400*mu) puts that at 4e-8 of the total, so any residual is
# quadrature error, not truncation.
m_grid = np.linspace(0.0, 400.0 * mu_E, 400_001)
N_of_m = mott_N(m_grid, n0_E, mu_E)                       # number heavier than m
mass_int = np.trapezoid(N_of_m, m_grid)                   # = int_0^inf m*(-dN/dm) dm
print(f"Check 3  Mott mass closure int N(m) dm = {mass_int*1e3:9.2f} g vs "
      f"M_case {m_case_E*1e3:9.2f} g -> {(mass_int/m_case_E-1)*100:+.3f} %  "
      f"{'PASS' if abs(mass_int/m_case_E - 1) < 2e-3 else 'FAIL'}")
print(f"         (analytic 2*N0*mu = {2*n0_E*mu_E*1e3:.2f} g)")

# Check 4: V0 against Tolch's own inferred fragment velocities.
TOLCH_V_PEN, TOLCH_V_PERF = 923.5, 838.0   # 3030 f/s, ~2750 f/s (third digit unreadable)
print(f"Check 4  V0 = {v0_E:.1f} m/s; Tolch inferred band "
      f"{TOLCH_V_PERF:.0f}-{TOLCH_V_PEN:.1f} m/s -> "
      f"{'inside' if TOLCH_V_PERF <= v0_E <= TOLCH_V_PEN else 'OUTSIDE'}")

# Check 5: rotating-band exposure. Neither basis deducts the gilding-metal
# band, so both M_case figures include it; a nominal 75-mm band of ~0.2 lb is
# the size of the residual disagreement to keep in view.
band = 0.20 * LB
print(f"Check 5  nominal band 0.20 lb = {band*1e3:.0f} g = "
      f"{band/m_case_E*100:.1f} % of M_case (carried inside M_case on BOTH bases)")
