---
title: Wound Ballistics & Fragment Lethality Reference Library
topic: wound-ballistics
date-created: 2026-05-24
---

# Wound Ballistics References

A collection of scientific and technical references on fragment armor penetration, human vulnerability modeling, and lethality assessment for fragmentation weapons.

## Collected Articles

### 1. Cunniff, Philip M. — "A Method to Describe the Statistical Aspects of Armor Penetration, Human Vulnerability and Lethality due to Fragmenting Munitions"

**Year:** 2014\
**Type:** Technical Report\
**DOI:** (not available)\
**File:** `/doc-reference/wound-ballistics/cunniff-2014/`

**Summary:** Establishes dimensionless areal density (Ad·Ap/mp) as the unifying parameter for armor penetration, tissue penetration, and environmental drag. Demonstrates that fragment presented area per unit mass follows munition-specific probability distributions independent of individual fragment mass—enabling statistical lethality modeling. Includes Sturdivan tissue penetration model, drag coefficient variability analysis, and computational framework for human phantom vulnerability assessment.

**Key Data:**

- Fragment presented area PDFs for 155 mm M107, 76 mm MK165, MK84 (Figure 3)
- Gelatin and wallboard penetration fits via Ad·Ap/mp parameter (Figures 5–6)
- Human phantom computational method with orientation-dependent impact zones (Figure 7)
- Fragment mass distribution laws (Mott, Grady, Weibull, Log-Normal, etc.; Table 1)

**Relevance to Model:** Directly addresses posture-independent target area variability via munition-specific orientation PDFs; provides unified penetration model across armor, tissue, and reference materials; enables Bayesian posterior updating of fragment threat parameters.

______________________________________________________________________

### 2. Federation of American Scientists / U.S. Navy — "Damage Criteria — ES310 Naval Weapons Engineering"

**Year:** 1998\
**Type:** DoD Training / Reference Document\
**Source:** https://man.fas.org/dod-101/navy/docs/es310/dam_crit/dam_crit.htm\
**File:** `/doc-reference/wound-ballistics/fas-es310-damage-criteria/`

**Summary:** Establishes probabilistic damage criteria for fragmentation warheads using Pk (Probability of Kill) framework. Personnel lethality thresholds: 100 J (Pk = 0.1, light damage), 1,000 J (Pk = 0.5, moderate), 4,000 J (Pk = 0.9, heavy). Formalizes fragment count, mass, velocity, and range integration into expected-hits model. Clarifies why fixed-energy thresholds (e.g., 79 J) misrepresent the probabilistic nature of fragment casualty.

**Key Equations:**

- Pk = P_hit × Pk|hit (conditional kill)
- Nhits = A × (N₀ / 4πR²) (expected hits on area A at range R)
- Pk_multi = 1 − (1 − Pk|hit)^Nhits (aggregate kill from multiple hits)

**Relevance to Model:** Defines the Pk|hit framework; provides baseline energy thresholds for validation; clarifies why Bayesian probabilistic approach is superior to binary kill criteria.

______________________________________________________________________

### 3. British Army War Office, Fire Effect Committee — "Weight of Fire: Historical British Artillery Doctrine and Fragment Lethality"

**Year:** 1944 (original reports); webpage archived\
**Type:** Historical Doctrinal Summary (non-peer-reviewed)\
**Source:** https://www.britishartillery.co.uk/wt_of_fire.htm\
**Report Numbers:** Army Operational Research Group Report No. 179 (March 1944), updated Report No. 234\
**File:** `/doc-reference/wound-ballistics/britishartillery-wt-of-fire/`

**Summary:** Consolidates WWII-era operational research on artillery casualty production, fragmentation lethality, and target vulnerability by posture. Establishes empirical casualty risk factors: prone troops sustain 1/3 the casualties of standing troops; trenched troops sustain 1/15–1/50 the casualties. Documents optimal anti-personnel fragment mass (~1 gram) and required fire intensity for different battlefield effects (neutralising, morale, lethal, material). Includes comparative effectiveness data for British, American, and Soviet artillery systems.

**Key Findings:**

- Optimal anti-personnel fragment mass: ~1 gram (under 1/25 oz)
- 50% lethal fragment (at 200 ft, vital organs): 1/8 oz or more
- Casualty reduction factor: prone troops = 1/3; trenched = 1/15–1/50
- Natural ground protection: ~5× better than level terrain
- Fire intensity for lethal effect: 0.1 lb/sq yd/hr
- Optimal HE content for anti-personnel: ~25% by weight
- British 25-pdr: 7% HE; American M1 105-mm: 14.8% HE

**Casualty Risk by Posture Table:**

| Posture               | Risk Factor |
| --------------------- | ----------- |
| Standing              | 1.0         |
| Prone                 | 1/3         |
| Open trenches         | 1/15–1/50   |
| Crouching in trenches | 1/25–1/100  |

**Comparative Shell Effectiveness:**

- 25-pdr (1.0×): baseline reference
- 122-mm Soviet HE-FRAG (2.2×): 2.2× more effective than 25-pdr
- 7.2-inch British How (4.0×): 4× more effective than 25-pdr

**Relevance to Model:** Provides empirical validation of posture-dependent casualty multipliers; establishes historical benchmark for fragment mass optimization; demonstrates that fire intensity (energy density per unit area) scales casualty production; acts as validation target for modern Bayesian casualty models.

______________________________________________________________________

### 4. U.S. Army/ARL (Misc.) — "Army Equipment Publication 55-Vol. 3: Casualty Criteria"

**Year:** ~1995–2010 (multiple editions)\
**Type:** Military Casualty Assessment Standard\
**File:** `/doc-reference/wound-ballistics/aep-55-vol3/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 5. PMC7295711 — Bone Fragments in Blast Injury

**Year:** (Pending metadata)\
**Type:** Journal Article / Systematic Review\
**File:** `/doc-reference/wound-ballistics/pmc7295711-bone-fragments/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 6. Lethality Threshold Critique

**Year:** (Pending metadata)\
**Type:** (Pending classification)\
**File:** `/doc-reference/wound-ballistics/lethality-threshold-critique/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

## Cross-Reference Index

### By Topic

**Fragment Armor Penetration:**

- Cunniff (2014) — Figure 1, ballistic limit model; Figure 3, presented area PDFs

**Fragment Lethality & Casualty Production:**

- British Artillery WoF (1944) — Casualty risk factors by posture; fire intensity thresholds; optimal fragment mass
- FAS ES-310 (1998) — Damage criteria table, Pk thresholds

**Human Vulnerability & Pk|hit:**

- FAS ES-310 (1998) — Damage criteria table, Pk thresholds
- Cunniff (2014) — Sturdivan tissue penetration model, Figures 5–6
- British Artillery WoF (1944) — Empirical casualty multipliers by posture

**Statistical Methods & Uncertainty:**

- Cunniff (2014) — Bayesian posterior framework, munition threat PDFs, Monte Carlo approach
- British Artillery WoF (1944) — Uncertainty bounds in casualty prediction (±4–6 percentage points); model limitations

**Casualty Assessment:**

- British Artillery WoF (1944) — Fire intensity requirements; casualty percentages by effect type
- AEP-55 Vol. 3 (TBD)
- PMC7295711 (TBD)

### By Historical Period

**WWII / 1940s:**

- British Artillery WoF (1944) — Empirical data from North Africa, Italy, Northwest Europe, Burma

**1990s–2000s:**

- FAS ES-310 (1998) — DoD training standard
- AEP-55 Vol. 3 (1995–2010) — Army casualty criteria

**2010s–Present:**

- Cunniff (2014) — Modern statistical fragmentation model

______________________________________________________________________

## Usage Notes

### For Fragmentation Lethality Model Development

1. **Start with British Artillery WoF (1944) for empirical baseline:**

   - Extract posture-dependent casualty multipliers (prone = 1/3, trenched = 1/15–1/50)
   - Note fire intensity requirement: 0.1 lb/sq yd/hr for lethal effect
   - Validate modern model predictions against historical WWII casualty data

1. **Apply Cunniff (2014) for fragment-level physics:**

   - Import Figure 3 munition-specific presented area distributions
   - Use Driels equation (p. 35) for velocity-reduction-in-flight calculations
   - Apply Sturdivan model (pp. 49–51) for tissue penetration depth
   - Compute individual fragment lethality (Pk|hit) as function of fragment energy + target area

1. **Validate Against FAS ES-310:**

   - Compare computed Pk vs. tabulated energy thresholds (100 J light, 1 kJ moderate, 4 kJ heavy)
   - Verify Pk|hit assignment per fragment kinetic energy
   - Ensure probabilistic framework (not binary kill threshold) matches ES-310 guidance

1. **Extend to Posture & Presented Area:**

   - Cunniff's human phantom method (Figure 7) computes area as f(burst location, posture)
   - Cross-check against British WoF posture multipliers to ensure model predicts correct casualty scaling
   - Consider NATO "man-as-box" silhouette model for standing/crouching/prone dimensions

### Model Validation Checklist

- [ ] Fragment mass distribution matches munition design (e.g., 155-mm M107: ~1–50 gram mode)
- [ ] Presented area PDF reproduces Cunniff Figure 3 or similar empirical data
- [ ] Pk|hit per fragment agrees with FAS ES-310 thresholds (±10%)
- [ ] Aggregate casualty rate (multi-hit) matches historical WWII field data (±15%)
- [ ] Posture multipliers reproduce British WoF casualty factors (within 20% of 1/3 and 1/15–1/50)
- [ ] Fire intensity scaling matches British WoF (0.1 lb/sq yd ≈ 0.12 kg/m²)

______________________________________________________________________

## Numerical Reference Tables

### Fragment Lethality Thresholds (Compiled)

| Source             | Framework              | Light/Threshold | Moderate/50%  | Heavy/90%  |
| ------------------ | ---------------------- | --------------- | ------------- | ---------- |
| British WoF (1944) | Energy (ft-lbs)        | 5               | —             | —          |
| British WoF (1944) | Fragment mass @ 200 ft | —               | 1/8 oz (28 g) | —          |
| FAS ES-310 (1998)  | Pk / Energy (J)        | 0.1 / 100 J     | 0.5 / 1 kJ    | 0.9 / 4 kJ |

### Fire Intensity Requirements (British WoF 1944)

| Effect       | Intensity             | Duration / Conditions                        |
| ------------ | --------------------- | -------------------------------------------- |
| Neutralising | 0.02–0.08 lb/sq yd/hr | Continuous, open positions                   |
| Morale       | 0.1 lb/sq yd/hr       | 4 hours continuous OR                        |
| Morale       | 0.25 lb/sq yd/min     | 15 minutes rapid fire                        |
| Lethal       | 0.1 lb/sq yd/hr       | 2% casualties in pits; 20% in open           |
| Material     | 0.1 lb/sq yd/hr       | 1.5% weapon damage in pits; 20% soft vehicle |

### Casualty Risk by Posture (British WoF 1944)

| Target Posture        | Risk Factor | Notes                                             |
| --------------------- | ----------- | ------------------------------------------------- |
| Standing (exposed)    | 1.0         | Baseline reference                                |
| Lying prone           | 0.33        | Ground protection ~5× better than level terrain   |
| Open fire trenches    | 0.067–0.020 | Deep protective trenches reduce risk dramatically |
| Crouching in trenches | 0.040–0.010 | Maximum protection from dug-in posture            |

### Shell Comparison: HE Content & Effectiveness

| Shell System            | Year | HE Content | Effectiveness Multiplier (vs 25-pdr) |
| ----------------------- | ---- | ---------- | ------------------------------------ |
| 25-pdr (UK)             | 1940 | 7.0%       | 1.0×                                 |
| 4.5-inch Gun (UK)       | 1940 | 6.9%       | —                                    |
| 105-mm M1 (US)          | 1943 | 14.8%      | —                                    |
| 122-mm OF-471 (Soviet)  | 1940 | 15.2%      | —                                    |
| 155-mm M107 (US)        | 1950 | 15.8%      | —                                    |
| 76.2-mm Soviet          | —    | —          | 0.9×                                 |
| 3.7-inch How (UK)       | 1940 | —          | 1.0×                                 |
| 122-mm Soviet HE-FRAG   | 1950 | ~15%       | 2.2×                                 |
| 7.2-inch Howitzer (UK)  | 1940 | —          | 4.0×                                 |
| 155-mm FH70 (post-1970) | 1970 | 26%        | ~3.5–4.0× (est.)                     |

______________________________________________________________________

## Limitations & Caveats

### British WoF (1944) Historical Limitations

1. **Posture discretization:** Only four posture states; modern models use continuous distributions
1. **No probabilistic fragment model:** Aggregate casualty data; lacks individual-fragment Pk|hit
1. **Terrain roughness unmeasured:** "~5×" protection factor is qualitative
1. **Fuze reliability:** WWII blinds (~1–5%) differ from modern proximity fuzes (~0.5%)
1. **Confidence bounds:** Stated as ±4–6 percentage points; actual variance may be larger

### FAS ES-310 (1998) Limitations

1. **Fixed energy thresholds:** Does not account for fragment shape, impact angle, or tissue stiffness
1. **No tissue heterogeneity:** Treats all human targets as equivalent (vs. actual variation in bone density, organ location)
1. **Validation data:** Thresholds derived from limited ballistic gelatin tests and small-arms comparison

### Cunniff (2014) Limitations

1. **Monte Carlo intensity:** Computationally expensive for real-time casualty prediction
1. **Presented area distributions:** Munition-specific; extrapolation to other systems uncertain
1. **Velocity decay model:** Driels equation valid for subsonic fragments; hypersonic behavior differs

______________________________________________________________________

**Last updated:** 2026-05-24\
**Maintained by:** @librarian\
**Source repository:** https://github.com/[project]/doc-reference/\\
