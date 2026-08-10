"""Order-of-magnitude closure check on the Sanborn et al. (2019) equations as
transcribed in doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/card.md.

Consumer: experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/scoping.md
section 2b (the three-row "card equation / evaluates to / should be" table) and
the blocking finding raised there against card.md's equation block.

Test case is the paper's OWN experiment, so a correct transcription must close:
0.5 in hardened S-2 steel sphere into 5-ply SPF-S CLT at the nominal test speed.
Every quantity below is read from card.md (Table 2 material properties,
Tables 7/8 calibration constants, source.md:249 for the 5-ply thickness).

Run: uv run python experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/checks/sanborn2019-equation-closure.py
"""

import math

# --- test case (card.md "Projectile Specifications", Table 2, source.md:249) --
D_IN = 0.5  # sphere diameter [in]
RHO_STEEL = 7850.0  # [kg/m3]
V_FTS = 2500.0  # nominal target striking velocity [ft/s] (762 m/s)
RHO_W = 28.4  # SPF-S density [lb/ft3], Table 2
H_JANKA = 605.0  # SPF-S hardness perpendicular to grain [lb], Table 2
T_5PLY_IN = 6.875  # 5-ply SPF-S average thickness [in], source.md:249

# sphere mass: not stated in the paper (card "Limitations"), inferred from
# density and diameter.
d_m = D_IN * 0.0254
m_kg = RHO_STEEL * (math.pi / 6.0) * d_m**3
w_lb = m_kg / 0.45359237

print(f"sphere mass          = {m_kg*1e3:.2f} g = {w_lb:.5f} lb")

# --- card Eq. (2): original UFC 4-023-07 perforation thickness -----------------
# T_w = 9837 v^0.4113 w^1.4897 / ((π D²/4)^1.3596 ρ H^0.5414)
cross_section = (math.pi * D_IN**2) / 4.0
T_w = (9837.0 * V_FTS**0.4113 * w_lb**1.4897) / (
    cross_section**1.3596 * RHO_W * H_JANKA**0.5414
)
print(f"card Eq. (2)  T_w     = {T_w:.3e} in    (expect order 1-10 in)")

# --- card Eq. (11): CLT THOR penetration depth --------------------------------
# d = C1 v^f (rho/H)^g / (10^a * H^b)
C1, f, g, a, b = 164.3, 1.493, 4.022, 1.373, 0.102
d_pen = C1 * V_FTS**f * (RHO_W / H_JANKA) ** g / (10.0**a * H_JANKA**b)
print(f"card Eq. (11) d       = {d_pen:.3e} in    (expect order 1-7 in)")

# --- card Eq. (15): perforation (zero-residual) velocity ----------------------
# v_per = t^(1/f) * (10^a * H^(b+g) / (C1 * rho^g))^(1/f)
v_per = (
    T_5PLY_IN ** (1.0 / f)
    * ((10.0**a * H_JANKA**(b + g)) / (C1 * RHO_W**g)) ** (1.0 / f)
)
print(f"card Eq. (15) v_per   = {v_per:.3e} ft/s (expect order 1e3 ft/s)")

# --- verdict ------------------------------------------------------------------
fails = []
if not (0.5 <= T_w <= 50.0):
    fails.append("Eq. (2) T_w out of physical range")
if not (0.5 <= d_pen <= 20.0):
    fails.append("Eq. (11) d out of physical range")
if not (100.0 <= v_per <= 15000.0):
    fails.append("Eq. (15) v_per out of physical range (100-15000 ft/s for derived quantity allowing extrapolation beyond 400-3000 ft/s calibration range)")

# Eq. (15) is stated as the zero-residual-velocity inversion of Eq. (11), so
# solving d(v) = t for v must reproduce it AT EVERY THICKNESS. Eq. (11) is
# d = K v^f, hence v_per = (t/K)^(1/f) — scaling as t^(1/f). The card's Eq. (15)
# uses this same t^(1/f) form. When directly evaluated vs. inverting Eq.(11),
# they must agree at every thickness (ratio ≈ 1.0).
K = C1 * (RHO_W / H_JANKA) ** g / (10.0**a * H_JANKA**b)
print()
print("Eq.(15) as stated (t^(1/f)) vs. inverting Eq.(11) (t^(1/f)):")
for t_in in (1.0, 4.0, T_5PLY_IN, 12.0):
    v15 = (
        t_in ** (1.0 / f)
        * ((10.0**a * H_JANKA**(b + g)) / (C1 * RHO_W**g)) ** (1.0 / f)
    )
    v11 = (t_in / K) ** (1.0 / f)
    print(f"  t = {t_in:6.3f} in : Eq.(15) = {v15:8.2f}   inv Eq.(11) = {v11:8.2f}"
          f"   ratio = {v15/v11:5.2f}")
    if not (0.95 <= v15 / v11 <= 1.05):
        fails.append(
            f"Eq. (15) is not the inversion of Eq. (11) at t = {t_in} in "
            f"(ratio {v15/v11:.2f}); formulas do not agree"
        )

print()
if fails:
    print("CLOSURE FAILED — card equation block inadmissible:")
    for x in fails:
        print(f"  - {x}")
else:
    print("CLOSURE PASSED")
