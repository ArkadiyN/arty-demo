# DoD Explosives Safety Board, Technical Paper 12 (1975) — Fragment Drag Coefficient

**Extract Card: Page 23, Figure 3 & Section "Ballistic Properties" (pp. 7–10)**

## Tables — read these, not the prose

| File | What it holds | Closure |
| ---- | ------------- | ------- |
| `tables/figure-3-drag-coefficient.csv` | $C_D$(Mach), 140 rows at 0.05 Mach, traced off the scan at 300 dpi | plateau reproduces the source's stated 1.28 |
| `tables/ballistic-constants.csv` | $k$, $C_D$, $\rho$, $L_1$ — the trio the report ties together on p.9 | $L_1 = 2k^{2/3}/(C_D\rho)$ reproduces the stated 247 |

`figure-3-digitized.md` is **superseded** — it was read by eye and is wrong
through the transonic rise. See its banner and
`experiment/fragmentation-field/challenges/source-data-audit/ledger.md` §13.

## Data Content

Figure 3 plots drag coefficient $C_D$ (dimensionless) vs. Mach number, 0–7
(image: `images/figure-3-drag-coefficient-vs-mach.png`; caption anchor
"Figure 3  Drag Coefficient of Fragments", `source.pdf` p.33). Read off the
traced curve:

- **Subsonic (M ≤ 0.6):** flat at $C_D = 1.079$.
- **Transonic (M ≈ 0.7–1.15):** steep rise, 1.09 → 1.32. At M = 1.0 the curve
    is at **1.23**, already two-thirds of the way up.
- **Peak (M = 1.46):** $C_D = 1.400$ — the local peak near sound speed
    mentioned in the text is a real ~9% bump above the supersonic plateau, not
    a minor wiggle.
- **Supersonic plateau (M ≳ 2.9):** settles to $C_D = 1.280$, flat out to
    M = 7 — this is the constant value the report recommends as a
    simplification (p. 8, "supersonic value of 1.28").

## Source & Test Conditions

**Experimental method:** fragments recovered from static detonation tests were fired from a smooth-bore launcher; velocity decay vs. distance observed to extract drag coefficient as function of Mach number (pp. 7–8, Section "Ballistic Properties," anchor L320–L327).

**Fragment type:** recovered from explosive fragmentation of steel cylinders (arena tests); treated as geometrically similar bodies with relation $m = k A^{3/2}$ where $k = 2.6~\text{g/cm}^3$ (forged steel projectile/bomb average); mean presented area measured by icosahedron gage or surface-area geometry (pp. 7–8, L293–L315).

**Original data source:** reference 10 = D. J. Dunn, Jr. and W. R. Porter, *Air Drag Measurements of Fragments*, BRL MR 915, August 1955 (L550).

## Trajectory Model Integration

Per p. 8, velocity decay formula with constant $C_D$:\
$$v = V_0 \exp(-R/L)$$
where $L = 2(k^{2/3} m^{1/3})/(C_D \rho) = L_1 m^{1/3}$ (distance for 1/e decay).
For $k = 2.6~\text{g/cm}^3$, $C_D = 1.28$: $L_1 = 247~\text{m/kg}^{1/3}$ (p. 9, L346).

## Applicability & Caveats

**Geometry assumption:** fragments from naturally fragmenting HE cylinders (steel case + explosive fill), recovered and tested. Shape-factor $k = 2.6$ is **average over diverse recovered pieces** (not strictly tumbling irregular fragments, but includes them).\
**Velocity range:** covers subsonic through supersonic regimes; figure presumably covers ~0–Mach 7.\
**Use:** this 1.28 value and curve are standard reference for 1970s–era U.S. military ordnance hazard assessment; applicability to naturally-fragmenting artillery shells depends on fragment geometry assumption validation.
