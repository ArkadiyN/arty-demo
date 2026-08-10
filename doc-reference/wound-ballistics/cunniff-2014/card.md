---
title: A Method to Describe the Statistical Aspects of Armor Penetration, Human Vulnerability and Lethality due to Fragmenting Munitions
authors: Philip M. Cunniff
year: 2014
venue: 28th International Symposium on Ballistics, Atlanta, GA, 2014-09-22/26
doi: ''
source: DEStech Publications, Two-volume proceedings, ISBN 978-1-60595-149-2
---

## Source

- **URL:** Paywalled proceedings (USD ~220/set from DEStech; accessible via International Ballistics Society membership)
- **Pages:** 21 pages
- **PDF SHA256:** `3ce25f1cddfb79e323b4d1c06115fe31002b0a01e808af6a1f47a35f328bae02`
- **Extracted:** 2026-08-10

## Central Equation and Dimensionless Parameter

**Cunniff's core claim:** Ballistic limit and residual velocity depend on a single dimensionless parameter:

$$\frac{A_d \cdot A_p}{m_p}$$

where:

- $A_d$ = target areal density (kg/m²)
- $A_p$ = projectile presented area (m²)
- $m_p$ = projectile mass (kg)

**Design equations (p. 15):**

$$V_c = V_s \cdot f\left(\sec\theta, \frac{A_d A_p}{m_p}, X_1 \ldots X_8\right)$$

$$V_r = V_s \sqrt{1 - \frac{V_c^2}{V_s^2}} \cdot f\left(\sec\theta, \frac{A_d A_p}{m_p}, X_5 \ldots X_8\right)$$

Regression constants for Kevlar KM2: $X_5 = 125.82$, $X_6 = 2.7104$, $X_7 = 0.2728$ (Figure 1, p. 4-6).

Impact obliquity $\theta$ is the second independent variable.

## Fragment Mass Distribution

**Figure 2 (pp. 6-7):** Empirical fit to Gold et al. (2006) data:

$$N = N_{\exp} \cdot \exp\left(-\frac{m}{c}\right)$$

with $a = 1.681$, $b = 1.831$, $c = 0.364$, $R^2 = 0.9827$.

Seven distribution forms tabulated (Mott, Generalized Mott, Grady, Generalized Grady, Log-Normal, Weibull, Held); Cunniff's exponential fit is slightly superior to Generalized Mott/Grady for this dataset.

## Presented Area Distribution — **Independent of Fragment Mass**

**Figure 3 (pp. 12-13):** Probability density functions (PDFs) for normalized presented area per unit mass:

| Munition             | Distribution              | Mean   | Variance σ² | 1σ Range    |
| -------------------- | ------------------------- | ------ | ----------- | ----------- |
| 155 mm M107 Howitzer | Normal                    | 1.0    | 0.07337     | 0.729–1.271 |
| 76 mm MK165          | Generalized Extreme Value | 1.6965 | 0.743       | 1.186–2.207 |
| MK84 Low Drag Bomb   | Normal                    | 1.0    | 0.082       | 0.714–1.286 |

**Key finding:** A single PDF describes all fragments from a given munition, independent of individual mass. Presented area varies ±20–40% at 1σ; over ±2σ, 40–200% of mean is possible. Ballistic limits consequently vary by factor of 2–3 depending on fragment striking attitude alone.

## Air Drag and Velocity Reduction

**Driels formula (p. 20):**

$$V_0 = V_p \cdot \exp\left(\frac{ar \cdot m^{1/3}}{1 - ar \cdot m^{1/3}}\right)$$

where $ar = 12 K_d K^{2/3}$, $K = (m \cdot A_p) / (\rho \cdot A_p^{3/2})$, $K_d \approx 0.66$ (drag coefficient), $\rho$ = air density.

**Figure 4 (p. 22):** Drake data (1945, 2200–3700 ft/s, 0.40–80 g) show no clear correlation between velocity ratio and $A_p/m_p$. McCleskey wind-tunnel drag coefficients vary 0.5–1.5 with munition type. **Conclusion:** Variance in velocity reduction is "considerable"; mean presented area alone is insufficient—statistical approach mandatory.

## Tissue Penetration (Gelatin Simulant)

**Sturdivan force-balance model (pp. 26-28):**

$$F = m_p \frac{dV}{dt} = -C_V \rho A_p V^b - C_I A_p V^2$$

**Penetration depth solution:**

$$x = \frac{m_p}{C_I A_p} \ln\left(1 + \frac{C_I V_0}{C_V + C_I b}\right)$$

with inferred initial velocity (steel):

$$V_0 = V_s \left(1 + 0.0378 e^{-V_s/82000}\right) \quad [\text{m/s}]$$

**Figure 5 (p. 28):** Quadratic fit to gelatin and goat tissue data (Breeze et al. 2013, Sturdivan 1978) with no systematic mass dependence. Model validity: intermediate velocities only; breaks down near gelatin sound speed (~1500 m/s) where compressional effects dominate, and at low velocity where gelatin elasticity (not modeled) becomes important.

## Reference Material Penetration (Wallboard)

**Figure 6 (p. 29):** Jordan (2009) data for Celotex® wallboard ($\rho = 0.285$ g/cc):

$$V_s [\text{m/s}] = 59.46 \left(\frac{A_d A_p}{m_p}\right)^2 + 116.5 \left(\frac{A_d A_p}{m_p}\right) + 191.1$$

Valid range: $0 < A_d A_p/m_p < 4$. Error bars added for MK84 Low Drag Bomb PDF (±1σ, 2σ, 3σ) show ±30–40% uncertainty in $V_{50}$ from attitude variance alone.

## Human Phantom Geometry and Orientation

**Section: "ORIENTATION OF TARGET RELATIVE TO MUNITION BURST POINT" (pp. 30-31, Figure 7, PDF pages 16-17):**

Target area defined by a human phantom centered at origin. Munition burst locations discretized as equally spaced viewpoints distributed on concentric spheres. Each viewpoint is re-oriented as a "viewpoint" onto the phantom; impact points evaluated if outward normal dot product with viewpoint vector > 0 (entry wounds only, not exits). **Each viewpoint assigned equal probability.**

**Figure 7(a) caption (p. 31):** "a munition is shown to burst above ground and behind a prone rifleman."

**Figure 7(b):** Below-ground equivalent representation.

**Critical gap:** The paper describes the **computational approach** (human phantom with normal vectors and viewpoint enumeration) but **does not provide tabulated projected areas** for standing, crouching, or prone postures as a function of fragment arrival angle. The phantom framework is flexible and notation-only; no resultin area values or posture-dependent silhouette tables are given.

## Munition Characterization and Spray Zones

Naturally fragmenting munitions assumed symmetric within solid angle from nose; mass/velocity characteristics differ by solid angle (spray zones). Typically ~25 spray zones per howitzer. For munition mix (10 types × 25 zones = 250 threats), each assigned fractional probability. Initial velocity/mass/shape PDFs best approximated from finite-element simulations of bursting; munition-specific priors can be refined iteratively.

## Statistical Lethality Framework

The paper reformats armor assessment from "coarse stochastic approximation to discrete Bayesian statistical analysis." A complete threat model is a **joint probability density function:**

$$f(V, m, \text{shape}, n \mid \text{spray zone, munition type})$$

Transformations: detonation → environmental drag → armor engagement → tissue penetration → wound tract → incapacitation probability. First evidence that Pk(incapacitation | hit) can be placed in statistical confidence intervals, with prior knowledge continuously refined per engagement data.

## Applicability and Gaps

**Direct use for fragmentation lethality:**

- Figure 3 PDFs (munition-specific $A_p/m$ distributions) can be directly sampled in Monte Carlo lethality models
- $A_d A_p/m_p$ unifies armor, tissue, and reference-material penetration into one dimensionless space
- Sturdivan force-balance model + Figure 5 gelatin data provide depth-of-penetration and wound severity

**Limitations:**

- **No posture-dependent silhouette values:** Figure 7 describes computational framework but gives no tabulated projected areas for standing/crouching/prone vs. fragment arrival angle (note in source.pdf p.30–31)
- **No $P_k|\text{hit}$ mapping:** Penetration probability is derived; wound-depth-to-incapacitation mapping not provided (deferred to p. 27 summary)
- **Limited munition spectrum:** Only three munitions shown (155 mm M107, 76 mm MK165, MK84); extrapolation to mortars, grenades not discussed
- **Drag model empirical:** Cd = 0.66–1.5 is fit-based, not first-principles; transition to Bayesian prior acknowledges this uncertainty

## References Cited (Key Ballistics)

- [37] Driels, M. R. (2004). *Weaponeering*, 2nd ed. — fragment velocity calculation
- [57-58] Breeze et al. (2013), Sturdivan (1978) — gelatin/tissue penetration data
- [59] Jordan, J. B. (2010). "Calculating fragment impact velocity from penetration data", *Int. J. Impact Eng.* 37(5):530–536

## Provenance and Verification

**Claim verified against primary:** The existing extraction's statement "no tabulated posture silhouette" is **confirmed accurate**. Figure 7 (source.pdf pp. 16–17, printed page ~31 in proceedings) depicts a prone rifleman in a computational framework with human phantom and viewpoint enumeration, but provides no table of projected areas by posture or fragment arrival angle.

**Extraction quality note:** The source PDF was created in FrameMaker 10.0 and contains FrameMaker-embedded fonts with PUA character encoding issues; heuristic extraction flags 266 PUA glyphs across symbol runs. Content remains readable; equations and posture-silhouette claims verified against the raw page text.
