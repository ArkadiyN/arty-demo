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

### 4. U.S. Ordnance Department — "Terminal Ballistic Data: Shell Fragment Damage"

**Year:** 1944 (declassified)\
**Type:** Technical Military Reference / Experimental Ballistics Data\
**Source:** US Ordnance Department, Volume II, Part 3 (pages 126–186 of original)\
**File:** `/doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/`

**Summary:** Quantitative experimental data on fragment damage patterns and effective-hits-per-square-foot (B) tables for field artillery shells, derived from Ordnance Department ballistic trials. Covers three key systems in this project's fragmentation model: 75-mm H.E. M48 (Table 43), 105-mm H.E. M1 (Table 51), and 155-mm H.E. M107 (Table 59). Provides independent validation dataset for fragment velocity decay, damage-pattern distribution, casualty threshold initialization, and range-dependent effectiveness. Damage patterns are presented as 60+ detailed figures showing spatial distribution of effective hits at various ranges, burst heights, and impact types.

**Key Data:**

- **Initial fragment velocities:** 75-mm M48 (3,120 f/s); 105-mm M1 (3,500 f/s); 155-mm M107 (3,500 f/s)
- **Effective-hits-per-sq-ft (B) @ 20 ft range:** 75-mm M48 (0.213); 105-mm M1 (0.231); 155-mm M107 (0.291)
- **Casualty threshold:** ≥58 ft-lb kinetic energy (incapacitation definition)
- **Distance ranges:** 75-mm (20–225 ft), 105-mm (20–300 ft), 155-mm (20–400 ft) from burst center
- **Damage-pattern figures:** 75-mm (Figs. 67–73); 105-mm (Figs. 93–100); 155-mm (Figs. 117–125) showing hit-density contours by range and burst height
- **Lightest effective fragment (@ 20 ft):** 75-mm (0.014 oz, 2,060 f/s); 105-mm (0.010 oz, 2,440 f/s); 155-mm (0.010 oz, 2,440 f/s)

**Relevance to Model:** Provides quantitative validation targets for the fragmentation model: (1) calibrate initial fragment velocity distribution per shell type; (2) constrain velocity decay constants against measured B-value tables; (3) validate casualty threshold initialization (58 ft-lb minimum energy); (4) cross-check predicted damage-pattern geometry (hit-density contours) against experimental figures; (5) independent verification dataset alongside British WoF 1944 empirical casualty data to ensure model predictions are grounded in independent WWII-era measurement.

______________________________________________________________________

### 5. U.S. Army/ARL (Misc.) — "Army Equipment Publication 55-Vol. 3: Casualty Criteria"

**Year:** ~1995–2010 (multiple editions)\
**Type:** Military Casualty Assessment Standard\
**File:** `/doc-reference/wound-ballistics/aep-55-vol3/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 6. PMC7295711 — Bone Fragments in Blast Injury

**Year:** (Pending metadata)\
**Type:** Journal Article / Systematic Review\
**File:** `/doc-reference/wound-ballistics/pmc7295711-bone-fragments/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 7. Lethality Threshold Critique

**Year:** (Pending metadata)\
**Type:** (Pending classification)\
**File:** `/doc-reference/wound-ballistics/lethality-threshold-critique/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 8. Tolch, N.A. — "Fragmentation Effects of the 75mm H.E. Shell T3 (M48)"

**Year:** 1944 (declassified)\
**Type:** Technical Military Report / Experimental Ballistics Data\
**Source:** Ballistic Research Laboratory Report, US Army Proving Ground\
**File:** `/doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/`

**Summary:** Direct measurement of fragment density (hits per unit solid angle) as a function of remaining shell velocity, distance, and angular sector for 75mm M48 shell via semi-circular wood panel firings. Independent second source on the same shell already covered in Ordnance Dept (1944) entry #4, but provides raw fragment-density data parameterized by velocity (700–2,130 f/s) rather than casualty-weighted effective-hits tables. Demonstrates sharp velocity-dependence: base-spray density collapses ~93% from static to 2,130 f/s (opposing velocity suppression), while nose-spray density rises substantially with velocity (additive velocity effect). Uniquely captures fragment spatial and velocity distribution for velocity-decay model calibration.

**Key Data:**

- **Fragment classification:** perforations (complete penetration), penetrations (partial depth), dents (surface mark only)
- **Measurement basis:** semi-circular wood panels at 15, 36, 75, 120 ft; impacts classified and counted per unit solid angle
- **Velocity conditions tested:** static (0 f/s), 700, 1,085, 1,450, 1,685, 2,130 f/s remaining velocity
- **Base spray density (Panel A, 15 ft):** 9.71 hits/u.s.a. static → 0.70 hits/u.s.a. at 2,130 f/s (93% reduction)
- **Nose spray density:** Panel B rises 2.42 → 26.31 hits/u.s.a. (static → 2,130 f/s, ~11×); Panel A rises more modestly, 16.09 → 21.45 (~+33%)
- **Side spray angle shift:** ~95° (static) to ~55° off shell axis (2,130 f/s)
- **Base fragment velocity distribution: unverified** — the source sentence sits on a ~100 DPI scan too degraded to transcribe reliably; two independent extractions disagree and neither is internally consistent (see `card.md` for both readings and why neither is trustworthy). Do not cite specific percentages from this report until checked against a better copy.
- **Battle typical remaining velocity:** 800–900 f/s (range 700–1,100 f/s)
- **Fragment charge velocities:** perforating 2,750 f/s; penetrating 3,030 f/s

**Relevance to Model:** Provides quantitative velocity-dependent fragment-density data for model validation and drag-coefficient calibration. Unlike Ordnance Dept (1944) B-value tables (casualty-weighted, integrated over all angles), this report preserves directional structure and pure ballistic marking ability vs. velocity. Second independent 1944 source on same shell enables cross-check of fragment velocity decay: the sharp base-spray collapse at modest remaining velocities (1,085–1,450 f/s, still in typical battle range) is directly usable to constrain whether the model under-decelerates fragments relative to historical data.

______________________________________________________________________

## Cross-Reference Index

### By Topic

**Fragment Armor Penetration:**

- Cunniff (2014) — Figure 1, ballistic limit model; Figure 3, presented area PDFs

**Fragment Damage Patterns & Effective Hits:**

- US Ordnance Dept (1944) — Tables 43, 51, 59; B-value tables 20–400 ft; damage pattern figures for three project-matched shells
- Tolch (1938) — Fragment density (hits/u.s.a.) vs. remaining velocity for 75mm M48; velocity-dependent spatial distribution; base/side/nose spray decomposition
- British Artillery WoF (1944) — Fire intensity; casualty-production scaling

**Fragment Lethality & Casualty Production:**

- British Artillery WoF (1944) — Casualty risk factors by posture; fire intensity thresholds; optimal fragment mass
- FAS ES-310 (1998) — Damage criteria table, Pk thresholds
- US Ordnance Dept (1944) — 58 ft-lb casualty threshold; range-dependent effectiveness data
- Tolch (1938) — Velocity-dependent fragment marking ability; base-spray density collapse (93% at 2,130 f/s); nose-spray expansion (Panel B ~11× at 2,130 f/s)

**Human Vulnerability & Pk|hit:**

- FAS ES-310 (1998) — Damage criteria table, Pk thresholds
- Cunniff (2014) — Sturdivan tissue penetration model, Figures 5–6
- British Artillery WoF (1944) — Empirical casualty multipliers by posture

**Statistical Methods & Uncertainty:**

- Cunniff (2014) — Bayesian posterior framework, munition threat PDFs, Monte Carlo approach
- British Artillery WoF (1944) — Uncertainty bounds in casualty prediction (±4–6 percentage points); model limitations
- US Ordnance Dept (1944) — Averaging methodology for B-values; applicability constraints

**Casualty Assessment:**

- British Artillery WoF (1944) — Fire intensity requirements; casualty percentages by effect type
- US Ordnance Dept (1944) — Casualty vs. perforation thresholds; target protection state dependency
- AEP-55 Vol. 3 (TBD)
- PMC7295711 (TBD)

### By Historical Period

**WWII / 1940s:**

- British Artillery WoF (1944) — Empirical data from North Africa, Italy, Northwest Europe, Burma
- US Ordnance Dept (1944) — Experimental ballistics data from Army and Navy proving grounds
- Tolch (1938) — Velocity-dependent fragmentation data for 75mm M48 shell from ballistic research trials

**1990s–2000s:**

- FAS ES-310 (1998) — DoD training standard
- AEP-55 Vol. 3 (1995–2010) — Army casualty criteria

**2010s–Present:**

- Cunniff (2014) — Modern statistical fragmentation model

______________________________________________________________________

## Usage Notes

### For Fragmentation Lethality Model Development

1. **Start with Ordnance Dept (1944) for empirical shell-specific data:**

    - Extract initial fragment velocities per shell type (75-mm: 3,120 f/s; 105-mm: 3,500 f/s; 155-mm: 3,500 f/s)
    - Use B-value tables (Tables 43, 51, 59) to calibrate velocity decay and range-dependent lethality
    - Cross-check damage pattern predictions against provided figures (Figs. 67–125)
    - Initialize casualty threshold at 58 ft-lb minimum kinetic energy

1. **Validate Against British Artillery WoF (1944) for empirical baseline:**

    - Extract posture-dependent casualty multipliers (prone = 1/3, trenched = 1/15–1/50)
    - Note fire intensity requirement: 0.1 lb/sq yd/hr for lethal effect
    - Ensure model-predicted casualty rates match historical WWII field data

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
- [ ] Initial fragment velocity matches Ordnance Dept values within 3% (75-mm: 3,120 f/s; 105-mm: 3,500 f/s; 155-mm: 3,500 f/s)
- [ ] Velocity decay predicts Ordnance Dept B-values (±5%) across 20–400 ft range

______________________________________________________________________

## Numerical Reference Tables

### Fragment Lethality Thresholds (Compiled)

| Source               | Framework                   | Light/Threshold | Moderate/50%  | Heavy/90%  |
| -------------------- | --------------------------- | --------------- | ------------- | ---------- |
| British WoF (1944)   | Energy (ft-lbs)             | 5               | —             | —          |
| British WoF (1944)   | Fragment mass @ 200 ft      | —               | 1/8 oz (28 g) | —          |
| FAS ES-310 (1998)    | Pk / Energy (J)             | 0.1 / 100 J     | 0.5 / 1 kJ    | 0.9 / 4 kJ |
| Ordnance Dept (1944) | Casualty threshold (energy) | 58 ft-lb        | —             | —          |

### Effective Hits per Square Foot (B-value) at 20 ft — Ordnance Dept 1944

| Shell       | Initial Velocity | B @ 20 ft (Casualty) | B @ 20 ft (1/8-in. Steel) | Max Range |
| ----------- | ---------------- | -------------------- | ------------------------- | --------- |
| 75-mm M48   | 3,120 f/s        | 0.213                | —                         | 225 ft    |
| 105-mm M1   | 3,500 f/s        | 0.231                | —                         | 300 ft    |
| 155-mm M107 | 3,500 f/s        | 0.291                | —                         | 400 ft    |

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
| 75-mm M48 (US)          | —    | —          | —                                    |
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

### US Ordnance Dept (1944) Limitations

1. **B-value applicability:** Requires multiple random-burst trials; not valid for single-shot prediction
1. **Azimuthal averaging:** B-values average over all firing directions; burst-specific asymmetry unmeasured
1. **Unshielded targets only:** Data assume exposed personnel; insufficient data for deeply dug-in targets
1. **Burst-height discretization:** Tested at discrete heights (grazing, 30 ft, 60 ft, etc.); continuous curves interpolated only
1. **Soil/terrain variability:** Penetration depth depends on soil type, moisture, and fuze setting; limited to "typical" soil only
1. **No fragment-mass distribution:** Tables report aggregate B-values; individual mass/velocity characteristics not separated
1. **WWII projectile design:** Fragment mass and velocity distributions reflect 1940s metallurgy and bursting charge; modern shells differ significantly

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

**Last updated:** 2026-07-26\
**Maintained by:** @librarian\
**Source repository:** https://github.com/[project]/doc-reference/\\
