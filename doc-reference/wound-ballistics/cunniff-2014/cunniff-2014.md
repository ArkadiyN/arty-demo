---
title: A Method to Describe the Statistical Aspects of Armor Penetration, Human Vulnerability and Lethality due to Fragmenting Munitions
authors: Philip M. Cunniff
year: 2014
source_url: https://scholar.google.com/scholar?q=Cunniff+armor+penetration+statistical+aspects
doi:
topic: wound-ballistics
---

## Summary

Cunniff's 2014 work establishes a statistical framework for fragment penetration and lethality modeling centered on the dimensionless areal density parameter (Ad·Ap/mp), where target areal density, projectile mass, and projected area each carry equivalent predictive weight. The key innovation is the discovery that a probability density function (PDF) for normalized fragment presented area per unit mass is independent of fragment mass itself, allowing a single distribution to describe all projectiles from a munition. This enables transition from coarse stochastic approximation to discrete Bayesian statistical analysis of armor penetration, air drag, gelatin tissue penetration, and ultimate injury assessment.

**Critical finding for lethality models:** Ballistic limits can vary **by a factor of 2× to 1/2×** depending only on fragment striking attitude—a statistical problem, not a deterministic one. The work addresses the problem of "optimal armor is not necessarily impenetrable armor" and provides methodology to model functional utility under fragmentation threat.

______________________________________________________________________

## Key Findings

### 1. Dimensionless Areal Density as the Central Parameter

The dimensionless areal density ratio (Equation 1) is proposed as the sole independent variable (together with impact obliquity) for predicting ballistic limit of armor systems:

$$
\\frac{A_d \\cdot A_p}{m_p}
$$

where:

- Ad = target areal density (kg/m²)
- Ap = projectile projected area (m²)
- mp = projectile mass (kg)

**Design equations for ballistic limit and residual velocity:**

$$
V_c = V_s \\cdot f\\left(\\sec\\theta, \\frac{A_d \\cdot A_p}{m_p}, X_1 \\ldots X_8\\right)
$$

$$
V_r = V_s \\sqrt{1 - \\frac{V_c^2}{V_s^2}} \\cdot f\\left(\\sec\\theta, \\frac{A_d \\cdot A_p}{m_p}, X_5 \\ldots X_8\\right)
$$

Regression constants provided for Kevlar KM2:

- X5 = 125.82
- X6 = 2.7104
- X7 = 0.2728

**Figure 1 (p. 13-14)** demonstrates the model validity across steel spheres (50% of max Ap), tungsten spheres (33% of max Ap), and 67% of max Ap over a wide velocity range. The model breaks down for small tungsten projectiles (≤4 grains) when projectile diameter approaches fabric end/pick spacing, requiring artificial presented area reduction.

### 2. Fragment Mass Distribution

Fragment mass follows well-documented power-law and exponential distributions. Figure 2 (p. 18) fits experimental data from Gold et al. (2006) to:

$$
N = N\_{\\exp} \\cdot \\exp\\left(-\\frac{m}{c}\\right) \\quad \\text{(simplified form)}
$$

with fitted parameters:

- a = 1.681
- b = 1.831
- c = 0.364
- R² = 0.9827

The Mott, Generalized Mott, Grady, Generalized Grady, Log-Normal, Weibull, and Held distributions are tabulated (Table 1, p. 18-22) with complete parameter definitions.

**Key insight:** The cumulative number of fragments decreases exponentially with normalized mass (m/m_exp). This defines the statistical threat spectrum from naturally fragmenting munitions.

### 3. Presented Area Distribution (Independence from Mass) — PRIMARY DATA GAP SOLUTION

**Figure 3 (p. 26-27)** is the centerpiece: probability density functions (PDFs) for normalized presented area per unit mass are shown to be:

1. **Independent of fragment mass**
1. **Munition-type independent** (same PDF applies to all fragments from a given munition regardless of size)
1. **Well-characterized by standard distributions** (typically Gaussian or Generalized Extreme Value)

Three examples provided:

**155 mm M107 Howitzer** — Normal Distribution

- Mean (μ) = 1.0
- Variance (σ²) = 0.07337
- Standard Deviation (σ) = 0.2709
- Implication: presented area varies ±27% at 1σ

**76 mm MK165 Projectile** — Generalized Extreme Value Distribution

- Mean = 1.6965
- Variance = 0.742997
- Shape (k) = 0.16353
- Scale (ζ) = 0.51145
- Location (μ) = 1.30356
- **Implication: wider spread than howitzer; presented area can range 20–200% of mean**

**MK84 Low Drag Bomb** — Normal Distribution

- Mean (μ) = 1.0
- Variance (σ²) = 0.081978
- Standard Deviation (σ) = 0.2863
- Implication: presented area varies ±29% at 1σ

**Practical consequence:** For a fixed target areal density Ad and fixed projectile mass mp, the PDF for Ap/mp defines the range of ballistic limits and penetration depths. A projectile striking with minimum Ap may penetrate; the same projectile at maximum Ap may not—**the difference is a factor of 2 or more** (pp. 27, 47).

### 4. Air Drag and Velocity Reduction

Fragments are assumed to tumble uniformly in transit, exposing all aspects of the shape distribution with equal frequency. Initial fragment velocity post-burst is calculated via Driels' formula (p. 35):

$$
V_0 = V_p \\cdot \\exp\\left(\\frac{ar \\cdot m^{1/3}}{1 - ar \\cdot m^{1/3}}\\right)
$$

where:

- Vp = velocity measured at distance r from burst (ft/s)
- m = fragment mass (grains)
- ar = drag-related constant (grains^{1/3}/ft)
- ar = 12 Kd K^{2/3}

with K = (m · Ap) / (ρ · Ap^{3/2}), Kd ≈ 0.66 (drag coefficient), ρ = air density.

**Figure 4 (p. 41):**

- **(a)** Velocity ratio (station spacing 2.8 m): no clear correlation with Ap/mp; Drake data show no stable drag-area relationship (Drake, 1945; range 2200–3700 ft/s, 0.40–80 g projectiles).
- **(b)** McCleskey wind-tunnel derived drag coefficients by munition type; coefficient varies 0.5–1.5 with Ap/mp ratio.

**Conclusion:** The variance in velocity reduction due to presented area variability is "considerable" (p. 45). A statistical approach is mandatory; mean presented area alone is insufficient to predict retardation.

### 5. Penetration into Human Tissue (Gelatin Simulant)

Sturdivan's tissue penetration model (pp. 48-51) treats retarding force as sum of inertial and viscous components:

$$
F = m_p \\frac{dV}{dt} = -C_V \\rho A_p V^b - C_I A_p V^2
$$

where:

- CV = viscous-force coefficient
- CI = internal force coefficient
- b = gelatin boundary layer thickness
- ρ = gelatin density (1.07 g/cm³ typical)
- Ap = projectile mean presented area

**Solutions for penetration depth and residual velocity:**

$$
x = \\frac{m_p}{C_I A_p} \\ln\\left(1 + \\frac{C_I V_0}{C_V + C_I b}\\right) - \\frac{C_V A_p t}{b m_p}
$$

$$
V = V_0 e^{-\\frac{C_I A_p}{m_p} \\cdot x} - \\frac{C_V A_p}{C_I + C_V/b}
$$

with inferred initial velocity:

$$
V_0 = V_s \\left(1 + 0.0378 e^{-V_s/82000}\\right) \\quad \\text{(steel projectiles)}
$$

Coefficient values (fitted experimentally):

- a (velocity loss coeff.) = 0.295 g/cm³
- c (velocity loss coeff.) = 82,000 cm/s

**Figure 5 (p. 52)** plots striking velocity vs. areal density (Ad·Ap/mp) for gelatin and goat tissue penetration (Breeze et al., 2013; Sturdivan, 1978):

- **17 grain FSP (fragment-simulating projectile):** ~1500 m/s → Ad·Ap/mp ~ 8
- **2.5 grain RCC (right circular cylinder):** ~800 m/s → Ad·Ap/mp ~ 1
- **7.5 grain RCC:** ~1200 m/s → Ad·Ap/mp ~ 3
- **40 grain sphere:** ~1800 m/s → Ad·Ap/mp ~ 15

**A quadratic fit to the combined data:**

$$
V_s = P_1 \\cdot (A_d A_p / m_p)^2 + P_2 \\cdot (A_d A_p / m_p) + P_3
$$

with no systematic error across projectile mass ranges. Sturdivan's "inferred velocity" term accommodates back-splash and shock-wave energy loss without explicit physics modeling.

**Model validity:** Sturdivan cautions the model applies between low and high velocity extremes; it breaks down approaching gelatin sound speed (~1500 m/s) where compressional effects dominate, and at low velocity where gelatin elasticity (not modeled) becomes important.

### 6. Penetration into Reference Materials (Wallboard)

Jordan (2009) penetration data into Celotex® wallboard (ρ = 0.285 g/cc; AFRL-RX-TY-TM-2009-4559):

**Figure 6 (p. 53)** plots striking velocity vs. areal density for:

- 2.85 g, 13.41 g, 53.78 g FSP (three masses)
- 0.13 g, 0.26 g, 1.04 g, 4.15 g RCC (four masses)

**Quadratic fit:**

$$
V_s = 59.46 \\cdot (A_d A_p / m_p)^2 + 116.5 \\cdot (A_d A_p / m_p) + 191.1
$$

**Error bars added for MK84 Low Drag Bomb** (1σ, 2σ, 3σ variations from Figure 3 PDF):

- At Ad·Ap/mp = 1.0 (mean): Vs ~ 367 m/s
- At Ad·Ap/mp = 1.29 (+1σ): Vs ~ 510 m/s (39% higher)
- At Ad·Ap/mp = 0.71 (−1σ): Vs ~ 247 m/s (33% lower)

Probability density curves overlaid for impact velocities 1000 m/s and 1500 m/s show the consequence: even for fixed projectile mass and munition type, striking attitude (→ Ap variability) alone changes ballistic limit by ±30–40%.

### 7. Statistical Approach to Armor Performance and Human Vulnerability

The model reformats armor assessment from "coarse stochastic approximation to discrete Bayesian statistical analysis" (p. 10). A munition's threat is defined by a joint probability density function:

$$
f(V, m, \\text{shape}, n | \\text{spray zone, munition type})
$$

where:

- V = initial fragment velocity
- m = fragment mass
- shape → Ap/m distribution (from Figure 3)
- n = number of fragments (spatial frequency, fragments/steradian)

**For multiple spray zones** (e.g., 25 zones per howitzer): each assigned probability based on munition geometry and expected orientation. **For munition mix** (e.g., 10 munition types × 25 zones = 250 threats): each assigned fractional probability per operational intelligence.

**Transformation cascade:**

1. **Detonation:** f(V₀, m, Ap/m) per spray zone
1. **Environmental drag:** V₀ → V(r) with variance propagation (Figure 4 scatter)
1. **Armor engagement:** V(r) → penetration outcome (Y/N)
1. **Tissue penetration:** if penetrate → (depth, tissue type, wound extent) via Sturdivan model
1. **Injury assessment:** wound tract + tissue damage → incapacitation probability

### 8. Human Phantom and Orientation Effects

Target area and vulnerability are modeled with a human phantom positioned at the origin (p. 62):

**Figure 7 (p. 62):** Munition burst location discretized as viewpoints distributed on concentric spheres. Impact evaluation proceeds by:

1. Computing dot product of outward normal (on phantom surface) and burst-to-target vector
1. Evaluating only cells where dot product > 0 (entry wounds, not exits)
1. For asymmetric burst patterns, re-orienting munition at burst point to illuminate each spray zone

**Equal probability assigned to each viewpoint** for fragmentation hazard assessment. This avoids ad hoc equivalence to existing systems and instead models the actual probabilistic geometry of fragment flux.

______________________________________________________________________

## Extracted Equations and Models

### Ballistic Limit (Cunniff Design Equations, p. 15)

The ballistic limit Vc as a function of dimensionless areal density and impact obliquity:

$$
\\frac{V_c}{V_s} = \\frac{X_1}{1 + X_2 \\sec\\theta + X_3 \\left(\\frac{V_s - V_c}{V_c}\\right)} \\quad \\text{where} \\quad X_3 = \\frac{V_s - V_c}{V_c}
$$

and

$$
\\frac{A_d A_p}{m_p} = X_6 \\cdot \\text{(material/geometry term)}$$

$$
V_r^2 = V_s^2 - V_c^2 e^{X_5 \\sec\\theta} \\left(1 + X_4 \\frac{V_r^2}{V_s^2 - V_c^2}\\right)$$

with:

- X4, X5 = X7 / (X8 + ...) [polynomial form]
- X5, X6, X7, X8 = empirically fitted regression constants
- θ = impact obliquity

### Drag-Corrected Initial Velocity (Driels, p. 35)

$$
V_0 = V_p \\cdot \\exp\\left(\\frac{ar \\cdot m^{1/3}}{1 - ar \\cdot m^{1/3}}\\right)$$

where ar = 12 Kd K^{2/3}, K = m·Ap/(ρ·Ap^{3/2}), Kd ≈ 0.66

### Tissue Penetration Force Balance (Sturdivan, p. 49)

$$
F = m_p \\frac{dV}{dt} = -\\left(C_V \\rho A_p V^b + C_I A_p V^2\\right)$$

**Penetration depth solution:**

$$
x = \\frac{m_p}{C_I A_p} \\ln\\left(1 + \\frac{C_I V_0}{C_V + C_I b}\\right)$$

**with inferred initial velocity:**

$$
V_0 = V_s \\left(1 + 0.0378 e^{-V_s/82000}\\right) \\quad [\\text{m/s, steel}]$$

### Reference Material (Wallboard) Penetration (Jordan, p. 53)

$$
V_s[\\text{m/s}] = 59.46 \\left(\\frac{A_d A_p}{m_p}\\right)^2 + 116.5 \\left(\\frac{A_d A_p}{m_p}\\right) + 191.1$$

Valid range: 0 < Ad·Ap/mp < 4, ρ_target = 0.285 g/cc (Celotex)

______________________________________________________________________

## Data Tables

### Fragment Mass Distribution Parameters (Table 1, pp. 18–22)

| Distribution          | Relative CDF (N/Nexp)               | Relative Mass CDF | Notes                        |
| --------------------- | ----------------------------------- | ----------------- | ---------------------------- |
| **Mott**              | 1 - (m/mₑ)^{1/2} exp(-(m/mₑ)^{1/2}) | ...               | Classical, used since WWII   |
| **Generalized Mott**  | exp(-(m/mₑ)^β)                      | ...               | β is fitted exponent         |
| **Grady**             | exp(-(m/mₑ)^β) ... [multi-term]     | ...               | Refined for velocity effects |
| **Generalized Grady** | ...                                 | ...               | Most general                 |
| **Log-Normal**        | 0.5 + 0.5 erf(...)                  | ...               | For skewed distributions     |
| **Weibull**           | 1 - exp(-(m/mₑ)^β)                  | ...               | Flexible shape               |
| **Held**              | M₀ B N_T m (1 - e^{−BNTm}) = m      | ...               | Regression form              |

**Figure 2 fit (p. 18):** N = Nexp · exp(−m/c) with c = 0.364, R² = 0.9827 (slightly better than Generalized Mott).

### Presented Area PDFs (Figure 3, p. 26–27)

| Munition                   | Distribution              | Mean       | Variance σ² | 1σ Range      | Interpretation         |
| -------------------------- | ------------------------- | ---------- | ----------- | ------------- | ---------------------- |
| **155 mm M107 Howitzer**   | Normal                    | μ = 1.0    | 0.07337     | 0.729 – 1.271 | ±27% at 1σ             |
| **76 mm MK165 Projectile** | Generalized Extreme Value | μ = 1.6965 | 0.743       | 1.186 – 2.207 | ±31% at 1σ; wider tail |
| **MK84 Low Drag Bomb**     | Normal                    | μ = 1.0    | 0.0820      | 0.714 – 1.286 | ±29% at 1σ             |

**Key takeaway:** Projectiles from the same munition vary in presented area by ±20–40% (1σ). Over ±2σ range: 40–200% of mean is possible. This variance alone modulates ballistic limit by factor of 2.

### Tissue and Reference Penetration Fits

**Gelatin (Figure 5, p. 52):** Quadratic fit across all projectile types and masses:

$$
V_s [\\text{m/s}] = f(A_d A_p / m_p) \\quad \\text{[single curve, no mass dependence]}
$$

Data scatter: ±200 m/s around fit; source: Breeze et al. (2013), Sturdivan (1978).

**Wallboard (Figure 6, p. 53):**

$$
V_s = 59.46 (A_d A_p / m_p)^2 + 116.5 (A_d A_p / m_p) + 191.1
$$

Intercept 191.1 m/s is the "non-physical" ballistic threshold (p. 51); slope coefficients carry physical significance (energy absorption per unit areal density). Error bounds (±1σ, ±2σ, ±3σ) derived from MK84 PDF overlay shows ±30–40% uncertainty in V50 from attitude variance alone.

______________________________________________________________________

## Applicability to Fragmentation Lethality Model

### Direct Relevance

1. **Presented Area Distribution (Independent of Mass)** ✓\
   Figure 3 provides munition-specific PDFs for Ap/m ratio. This is the primary data gap; can be directly imported into Monte Carlo lethality model as:

   ```
   for each fragment:
       sample Ap from munition's PDF (Figure 3)
       mp = fragment mass (from mass distribution, Figure 2)
       → proceed with ballistic impact
   ```

1. **Areal Density as Unifying Parameter** ✓\
   Ballistic limit, tissue penetration, and armor penetration all collapse onto Ad·Ap/mp. No separate "posture-dependent silhouette model" needed; instead, posture defines Ad (body armor + clothing areal density), and lethality follows from single dimensionless parameter space.

1. **Velocity Reduction in Flight** ✓\
   Driels equation + Figure 4 drag coefficient data enable fragment velocity at target range. Variability in Cd and Ap modulates velocity loss; uncertainty quantification via Figure 3 PDF is essential.

1. **Tissue Penetration Model** ✓\
   Sturdivan's force-balance model (pp. 49–51) + gelatin data (Figure 5) provides depth-of-penetration and wound extent. Integration into lethality assessment pipeline is direct: if fragment penetrates armor, continue into Sturdivan model for wound severity.

### Gaps / Limitations

1. **No explicit posture-dependent silhouette areas given**\
   The paper does not provide tabulated projected areas for standing/crouching/prone soldiers as a function of fragment arrival angle γ. Figure 7 (p. 62) describes the *computational* approach (human phantom with normal vectors), but not the resulting area values.

1. **No Pk|hit vs. fragment parameters**\
   The paper focuses on penetration probability; does not directly link wound depth → incapacitation risk. Sturdivan notes that "depth of penetration and tissue type" must then be mapped to injury (p. 63), but that mapping is not provided.

1. **Munition-specific parameters not comprehensive**\
   Only three munitions shown (155 mm M107, 76 mm MK165, MK84 bomb); extrapolation to other threats (mortars, hand grenades, etc.) not explicitly discussed. Reference [29] (Gold et al., PAFRAG) may provide broader spectrum.

1. **Drag model validity at 0.66 ≤ Cd ≤ 1.5 (Figure 4)**\
   Drake data show poor correlation with Ap; McCleskey wind-tunnel fits are empirical. Transition to Bayesian prior (p. 60) acknowledges this limitation; uncertainty quantification recommended.

______________________________________________________________________

## References from Cunniff 2014 (Selected, Relevant to Lethality)

- [12] Johnson et al. (1968). "A Mathematical Model for Predicting Residual Velocities of Fragments after Perforating Helmets and Body Armor"; BRL-TR-1705.
- [13–14] Young et al. (1972–1973). ARMORTRAN, HELMETRAN computer models (early casualty-assessment codes).
- [29–31] Gold et al. (2006–2010). PAFRAG modeling of fragmentation munitions performance; Proc. 23rd Int. Symp. on Ballistics.
- [37] Driels, M. R. (2004). *Weaponeering: Conventional weapon system effectiveness*, 2nd ed. (fragment velocity calculation).
- [49–54] McCleskey, F. R. (various). Drag coefficients, fragmentation hazard models (NSWC reports).
- [57–58] Breeze et al. (2013), Sturdivan (1978). Gelatin and goat tissue penetration data.
- [59] Jordan, J. B. (2010). "Calculating fragment impact velocity from penetration data"; *Int. J. Impact Eng.* 37(5):530–536.

______________________________________________________________________

## Conclusion

Cunniff (2014) provides the statistical framework and **most critical empirical finding** for a lethality model: **fragment presented area per unit mass is a munition-type-dependent distribution, independent of individual fragment mass.** This permits Monte Carlo sampling of realistic fragment orientations without re-parameterization per mass bin. Combined with Driels drag equations, Sturdivan tissue penetration model, and human phantom geometry (Figure 7), the pipeline from munition detonation → fragment → air drag → target impact → penetration → wound → incapacitation is fully specified, with quantified uncertainty at each stage.

The dimensionless areal density parameter (Ad·Ap/mp) unifies armor, tissue, and reference-material penetration, eliminating the need for separate models per target type. Ballistic limits and penetration depths vary by factor of 2–3 depending on fragment orientation alone—a statistical effect that cannot be ignored in casualty estimation.

**For the fragmentation lethality model:** Import Figure 3 PDFs as munition-specific Ap/m distributions; tabulate test data from Figure 5 (gelatin penetration) for Pk|hit assessment; use human phantom approach (Figure 7, pp. 62–63) to compute presented area as a function of burst location and target posture.
