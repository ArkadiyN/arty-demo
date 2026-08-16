# Sanborn et al. (2019): Ballistic Performance of Cross-Laminated Timber (CLT)

## Source

- **DOI:** 10.1016/j.ijimpeng.2018.11.007
- **Citation:** Sanborn, K., Gentry, T.R., Koch, Z., Valkenburg, A., Conley, C., Stewart, L.K. (2019). "Ballistic performance of Cross-laminated Timber (CLT)." *International Journal of Impact Engineering*, 128:11–23.
- **Pages:** 13
- **SHA256:** 42164160c28b02352712d42917574b0e87fdb3b8787b1924bd628c63d1af51b3
- **Scope:** Experimental ballistic penetration and residual-velocity data for 0.5 in. (12.7 mm) hardened S-2 tool-steel sphere projectiles (180–1200 m/s) fired into Spruce Pine Fir-South (SPF-S) and Southern Yellow Pine (SYP) CLT targets, with penetration models calibrated to this data.

## Projectile Specifications

**Material & geometry** (`hardened impact-resistant S-2 tool steel`): 0.5 in. (12.7 mm) diameter steel sphere.

**Velocity range** (`striking velocities of 500 to just over 3500 ft/s`): 180–1200 m/s.

**Test count** (`Table 3 Breakdown of number of ballistic tests`): 122 total sphere shots across both species—63 embedded (partial penetration) + 59 perforation (complete penetration).

## Test Specimens

**Material:** Two softwood species, cross-laminated timber (CLT) with orthogonally oriented plies:

- **SPF-S (Spruce Pine Fir-South):** V4 grade, manufactured by SmartLam per APA standard
- **SYP (Southern Yellow Pine):** Experimentally manufactured at Georgia Tech per ANSI/APA PRG 320-2012, expected to meet V3 grade specifications

**Size** (`12 in. by 12 in. (30.5 cm by 30.5 cm) in height and width`): Square specimens, 12 in. × 12 in. nominal plan.

**Plies:** Specimens varied in thickness (number of plies); testing included 3-ply and 5-ply configurations. Adjacently stacked orthogonal layers secured with polyurethane adhesive (~29.3 g/ft² per `2.3. Ballistic targets`).

**Clamping:** 100 psi (0.7 MPa) pressure for 2 h during press (source.md line 58).

## Material Properties

**Table 2** (`SPF-S and SYP physical and mechanical properties`):

| Property                             | Method                | SPF-S Mean              | SPF-S COV | SYP Mean                | SYP COV |
| ------------------------------------ | --------------------- | ----------------------- | --------- | ----------------------- | ------- |
| Density                              | average of entire set | 28.4 lb/ft³ (455 kg/m³) | –         | 34.2 lb/ft³ (548 kg/m³) | –       |
| Moisture Content (%)                 | pin meter             | 10.5%                   | –         | 9.0%                    | –       |
| Shear Strength ∥ grain (psi / MPa)   | ASTM D143 Section 14  | 1,300 (8.96)            | 27%       | 1,600 (11.0)            | 13%     |
| Hardness ⊥ grain (lb / N)            | ASTM D1037            | 605 (2,690)             | 29%       | 656 (2,920)             | 30%     |
| Bond Line Shear Strength (psi / MPa) | ASTM D905             | 399 (2.75)              | 32%       | 880 (6.07)              | 19%     |

**Note:** SYP exhibits higher density, shear strength, and hardness than SPF-S, resulting in superior penetration resistance (source.md line 85–86).

## UFC 4-023-07 Perforation-Thickness Equation (Original)

**Equation 2** (`UFC provides an equation for the thickness of wood necessary to resist perforation (see Eq. (2))`):

$$T_w = \frac{9,837 \, v^{0.4113} w^{1.4897}}{({\pi D^2}/{4})^{1.3596} \rho H^{0.5414}}$$

**Variables:**

- $T_w$ = thickness of wood required to prevent perforation (in)
- $v$ = projectile impact velocity (ft/s)
- $w$ = projectile weight (lb)
- $D$ = projectile diameter (in)
- $\rho$ = wood density (lb/ft³)
- $H$ = wood hardness (lb, Janka)

**Status on CLT data:** The original UFC coefficients (C₁=9,837; a=0.411; b=1.490; c=1.360; d=0.541) were calibrated on THOR 1950s data using relatively thin solid wood blocks. When applied to CLT embedment depth (`The stark difference between the UFC equation and the CLT data is a perfect example of this`, source.md line 105), the equation overpredicts required thickness significantly—not acceptable for CLT design. Re-calibration was required.

## Classical Penetration Models (Euler–Robins, Poncelet, Resal)

**Table 5** (`Classic penetration equations and associated penetration depth expressions`):

| Model            | Deceleration       | Penetration Depth $d$                             | Calibrated Constants to CLT Data |
| ---------------- | ------------------ | ------------------------------------------------- | -------------------------------- |
| **Euler–Robins** | $a = C$ (constant) | $d = \frac{v_s^2}{2C}$                            | $C_1 = 3.776$                    |
| **Poncelet**     | $a = C + Bv^2$     | $d = \frac{1}{B} \ln(1 + Bv_s^2) + \frac{C_1}{B}$ | $C_1 = 1.887$, $B = 0.0672$      |
| **Resal**        | $a = Av + Bv^2$    | $d = \frac{1}{B} \ln(1 + Bv_s^2) + \frac{A}{B}$   | $A = 0.0497$, $B = 363.9$        |

**Derivation basis:** Constants determined via Levenberg–Marquardt fitting to 63 embedded CLT sphere data points. Reference (not measured) hardness and density values used per source.md line 137: "the reference values [3] for hardness and density were used in this calibration because it is expected that a typical user would not necessarily conduct material testing."

**Velocity validity range:** Applies to striking velocities in the range measured (embedded shots through first perforation threshold).

**Performance** (`MSE` in Table 9): Euler–Robins MSE=3.11, Poncelet MSE=1.34, Resal MSE=1.71 (lower is better fit).

## Force Law Model (Physics-Based Penetration)

**Conceptual basis** (`5.3. Force law model`): A resisting force exerted by the target reduces the projectile's velocity. General quadratic form in velocity.

**Residual velocity form** (Eq. 6):
$$v_r = v_s - ax^2 - bx - c$$

where:

- $v_r$ = residual velocity
- $v_s$ = striking velocity
- $x$ = distance traveled in target
- $a, b, c$ = model constants

**Ballistic limit / zero-residual-velocity depth** (Eq. 7, solving $v_r = 0$ for penetration depth at ballistic limit):

$$x = d = \frac{-b + \sqrt{b^2 + 4a(v_s^2 - c)}}{2a}$$

**Recalibrated constants to CLT embedment data** (Table 6):

- $a = 3.550$
- $b = 190.5$
- $c = 574.7$

**Performance** (Table 9): MSE = 1.32 on combined SPF-S + SYP data—best fit among classical/physics-based models.

**Interpretation:** The constants encode a target material's resistance function (quadratic in penetration distance); they lack explicit material properties and rely solely on striking velocity for predictions.

## THOR-Based Penetration Model (Empirical, Material-Dependent)

**Original THOR equation** (Eq. 8, from 1960s Ballistic Analysis Lab): Predicts residual velocity with projectile and target parameters:

$$v_r = v_s - \left( \frac{c \, t \, A \, w}{10^{\sec(\theta)}} \right)^{\alpha, \beta, \gamma} v_s^{\lambda}$$

where secondary variables (fragment weight loss, obliquity angle θ) apply to fragment data but are simplified here.

**CLT THOR model** (Eq. 11, calibrated to sphere data):

$$d = C_1 v_s^f \frac{\left( \frac{\rho}{H} \right)^{g}}{10^a H^b}$$

**Calibrated constants** (Table 7, combined SPF-S + SYP):

- $C_1 = 164.3$
- $f = 1.493$
- $g = 4.022$
- $a = 1.373$
- $b = 0.102$

**Key advantage:** Explicitly incorporates target material properties (density ρ, hardness H); projectile weight $w$ excluded because all tests used identical sphere mass.

**Performance** (Table 9): MSE = 0.303—best overall fit among all penetration-depth models tested.

**Velocity validity range** (`Section 6.6`): Recommended for striking velocities 400–3,000 ft/s (120–910 m/s), CLT thickness > 4 in. (10.1 cm), and projectiles with size/mass similar to 0.50 in. sphere. Extrapolation to hypervelocity not recommended without re-calibration.

## Recalibrated UFC Model for CLT (Penetration Depth)

**Generic UFC form** (Eq. 12, unsolved):

$$d = \frac{C_1 v^a w^b}{D^c \rho^d H}$$

**Recalibrated constants to CLT embedment data** (Table 8):

- $C_1 = 6.91$
- $a = 1.495$
- $b = 1.434$
- $c = 0.201$
- $d = 0.237$

(Original UFC coefficients: C₁=9,837; a=0.411; b=1.490; c=1.360; d=0.541 — note substantial changes in exponents, especially on diameter and density.)

**Performance** (Table 9): MSE = 0.330—second-best fit, superior to original UFC but behind CLT THOR model.

## Residual Velocity: Force Law + THOR

**Perforation velocity (zero-residual-velocity condition)** (Eq. 15–16, derived from CLT THOR penetration model):

$$v_{\text{per}} = t^{1/f} \left(\frac{10^a H^{b+g}}{C_1 \rho^g}\right)^{1/f}$$

where $t$ = CLT specimen thickness, $C_1, f, g, a, b$ are the CLT THOR constants from Table 7.

**Residual velocity** (Eq. 18, reduced THOR form with calibrated reduction factor R):

$$v_r = v_s - R \left( v_{\text{per}} - t C_1 \left( \frac{H}{10^b} \right)^{a/f} \rho^{1/g} \right)$$

**Calibrated reduction factor** (5-ply SPF-S data, source.md line 248): $R = 0.67$ (accounts for reduced resistance at CLT back face during perforation).

**Model intent:** Captures the physics that back-face resistance in CLT is lower than mid-layer resistance; accounts for scabbing and exit-hole enlargement observed in dissections (Fig. 5(b)).

## Summary of All Penetration-Depth Models

**Table 9** (`Summary of models considered for predicting depth of penetration of CLT`): Full model comparison matrix with equations, constants, factors included, and MSE on combined species data:

| Model        | Constant(s)                                     | Parameters           | MSE       |
| ------------ | ----------------------------------------------- | -------------------- | --------- |
| Euler–Robins | $C_1=3.776$                                     | $v_s$                | 3.11      |
| Poncelet     | $C_1=1.887, B=0.0672$                           | $v_s$                | 1.34      |
| Resal        | $A=0.0497, B=363.9$                             | $v_s$                | 1.71      |
| Force Law    | $a=3.550, b=190.5, c=574.7$                     | $v_s$                | 1.32      |
| General THOR | $f=1.305, g=12.58, h=3.967$                     | $v_s, A, w$          | 1.532     |
| **CLT THOR** | $C_1=164.3, f=1.493, g=4.022, a=1.373, b=0.102$ | $v_s, \rho, H$       | **0.303** |
| CLT UFC      | $C_1=6.91, a=1.495, b=1.434, c=0.201, d=0.237$  | $v_s, w, D, \rho, H$ | 0.330     |

**Design recommendation** (source.md line 191): "it is recommended that the THOR CLT model be used for predicting penetration depth for striking velocity ranging between 400 and 3,000 ft/s (120 to 910 m/s), for CLT of a thickness of greater than 4 in. (10.1 cm), and for projectiles with weights and areas similar to the 0.50 in. (12.7 mm) sphere projectile."

## Experimental Data Plots

**Figure 6** (`Fig. 6. Impact velocity versus penetration depth data from CLT ballistic experiments for Spruce Pine Fir-South CLT and Southern Yellow Pine CLT targets`):

- **Data:** 63 embedded-projectile shots (partial penetration)
- **Axes:** Striking velocity $v_s$ (m/s, x) vs. penetration depth $d$ (in, y)
- **Curves:** Separate traces for SPF-S and SYP species
- **Trend:** Penetration depth increases with striking velocity; SYP exhibits lower penetration depth at matched velocity (higher resistance)
- **Data source:** Individual experiment values per Sanborn (2018) dissertation [20]

**Figure 7** (`Fig. 7. Striking velocity versus residual velocity data from CLT ballistic experiments for 5-ply Spruce Pine Fir-South and Southern Yellow Pine CLT`):

- **Data:** 5-ply specimen perforation events (complete penetration)
- **Axes:** Striking velocity $v_s$ (m/s, x) vs. residual velocity $v_r$ (m/s, y)
- **Curves:** Separate traces for SPF-S and SYP species
- **Trend:** Residual velocity increases monotonically with striking velocity; SYP provides higher velocity attenuation (lower residual velocity at matched striking velocity)
- **Test protocol:** "The majority of these tests fell within a smaller band of striking velocities (target velocity was 2,500 ft/s (762 m/s))" per source.md line 77

**Figure 8** (`Fig. 8. Striking velocity versus residual velocity data from CLT ballistic experiments for 3-ply and 5-ply Southern Yellow Pine CLT`):

- **Data:** SYP specimens, both 3-ply and 5-ply configurations
- **Observation:** "residual velocity increased from 3-ply to 5-ply because there was less material to resist the projectile" (source.md line 75)

## Numeric Data Availability

**Penetration-depth data (Figure 6):** Individual experiment values for 63 embedded shots are available in Sanborn (2018) dissertation [20]; **not tabulated directly in this paper**. Figure 6 presents scatter plot only.

**Residual-velocity data (Figures 7–8):** Similar to Figure 6; individual perforation velocities are figure-only and cross-referenced to [20]. **Not transcribed here.**

**Weathering effects** (Table 4): Moisture-content study on 4 specimens (2 species × 2 moisture conditions) at ~762 m/s showed "no statically significant difference between the moisture content and the ballistic performance within the range of values and parameters explored" (source.md line 98). Exterior/interior moisture contents ranged 9–38% depending on treatment (fog room 3 days, water submersion 13 days).

## Extraction Quality & Limitations

**Extraction method:** PDF text extraction via heuristic (no scanned OCR). Quality check passed with 0 flags (glyph-level gate clean; no PUA characters, symbol-run contamination, or short-token anomalies detected).

**Limitations not stated in source:**

- Projectile weight not explicitly given in the text (sphere mass inferred from density and 0.5 in. diameter); exact mass value would require calculation or supplementary data.
- Exact thickness (in inches) of 3-ply and 5-ply specimens not given in main text (only ply count); thickness must be inferred from lamina thickness (~1.375 in. per lamina per manufacturing section) if needed for model application.
- Figure 6–8 data are numeric scatter plots only (coordinates extractable only by digitization, not transcribed directly).

**Recommended next step for model implementation:** Contact authors or consult Sanborn (2018) dissertation [20] for tabulated experimental data (penetration depth $d$ vs. $v_s$ for all 122 shots, sorted by ply/species).

## Criterion-Match Notes

**For project's fragmentation perforation model:** This source reports **penetration depth and residual velocity** for a **compact (0.5 in. sphere) hardened steel projectile** into **softwood CLT** at **intermediate velocities** (180–1200 m/s). The ballistic-limit / zero-residual-velocity relation (Eq. 15–16, perforation thickness $T_w$) is a **direct analog to the thin-wall perforation criterion** in the project's fragmentation framework, provided the following **criterion-match questions** are resolved by @model-reviewer:

1. **Projectile similarity:** Does a 12.7 mm hardened steel sphere represent a valid proxy for the project's compact steel fragment class (e.g., casing shards, fuze debris)? If not, the constants require re-calibration or scaling.
1. **Wood analog:** Do SPF-S and SYP CLT specimens serve as valid proxies for the project's softwood target (birch, pine, etc.)? Density and hardness ranges overlap, but species-specific penetration constants may differ.
1. **Validity range:** Does the project's impact velocity range (180–1200 m/s, 400–3000 ft/s recommended) match the scenario? Extrapolation beyond 3000 ft/s not supported.

No interpretive recommendation belongs here; @model-reviewer owns the criterion-match verdict.

______________________________________________________________________

**Card written:** 2026-08-09\
**Extraction quality:** Clean (0 flags)\
**Full text markdown:** `source.md` (13 pages)\
**Figures:** 18 images extracted (images/ directory)\
**Data tables:** No CSV export (Figure 6–7 are scatter plots, not tabulated); calibration constants tabulated in card above (Tables 5, 7, 8, 9).

## Provenance of this card

- **Document:** K. Sanborn et al., "Ballistic performance of Cross-laminated Timber (CLT)," *International Journal of Impact Engineering*, Vol. 128, pp. 11–23, 2019 (verified anchor "Ballistic performance of Cross-laminated Timber (CLT)" — `source.md:1`, title line; verified anchor "K. Sanborn et al." — `source.md:3`, author line).
- **DOI:** 10.1016/j.ijimpeng.2018.11.007 (stated in card Source section, confirmed from card.md line 5).
- **`source.pdf`:** **RETAINED** — PDF blob preserved at `doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/source.pdf` (gitignored per project convention).
    - **Origin:** `/mnt/f/Projects/TMP/Docs/pubs_clt1.pdf` (user-supplied WSL mount)
    - **Pages:** 13
    - **SHA256:** 42164160c28b02352712d42917574b0e87fdb3b8787b1924bd628c63d1af51b3 (verified 2026-08-16)
    - **Anchor verification:** "The stark difference between the UFC equation and the CLT data" confirmed at source.pdf page 3 (printed), source.md line 105. Card cites source.md line 102 (3-line offset, minor extraction variance).
- **Extraction method:** PDF text layer heuristic extraction (no vision-assisted OCR); extracted markdown (`source.md`) and 18 figures retained. No secondhand claims — all data reported as first-hand experimental results by Sanborn et al., not attributed to prior sources except where explicitly cited (e.g., Levenberg–Marquardt fitting method, reference [20] for raw data).
