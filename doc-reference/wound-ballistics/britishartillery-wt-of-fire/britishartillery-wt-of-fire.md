---
title: Weight of Fire — Historical British Army Artillery Doctrine and Fragment Lethality
authors: British Army War Office, Fire Effect Committee; 1 Operations Research Section (Italy), 2 ORS (Northwest Europe)
year: 1944
source_url: https://www.britishartillery.co.uk/wt_of_fire.htm
source_type: Historical Doctrinal Summary (non-peer-reviewed)
report_number: Army Operational Research Group Report No. 179 (March 1944), updated Report No. 234
topic: wound-ballistics
---

## Summary

This historical British Army doctrinal summary consolidates WWII operational research on artillery weight of fire, fragment lethality, and casualty production. Establishes empirically-derived casualty risk factors by target posture (standing, prone, trenched), optimal anti-personnel fragment mass (~1 gram), required fire intensity for different battlefield effects, and the probability distribution of fragments by mass from 25-pounder shells. Key finding: natural ground offers ~5× the protection to prone soldiers compared to level surfaces. Includes comparative effectiveness data for Allied and Soviet artillery systems and the theoretical framework for calculating expected casualties from multi-round bombardments.

## Key Findings

### Fragment Lethality & Optimal Anti-Personnel Design

- **Optimal anti-personnel fragment mass:** Under 1/25 oz (~0.04 oz or ~1.1 grams; exact conversion uncertain in historical sources)
- **50% Lethality Criterion:** A fragment of 1/8 oz (~28 grams) or more had 50% probability of lethality at 200 feet when striking vital organs
- **Energy threshold for incapacitation:** Approximately 5 ft-lbs of kinetic energy (British research), **versus** earlier criterion of 58 ft-lbs
  - 5 ft-lbs ≈ 6.78 J
  - 58 ft-lbs ≈ 78.6 J (note: close to the widely-cited 79 J threshold in modern literature)

### Fragment Distribution from 25-pdr Shells

At 15% HE content by weight:

- **< 19 fragments over 2 oz** (56.7 grams)
- **> 1,122 fragments under 1/25 oz** (~1.1 grams)
- Optimal anti-personnel performance required minimum **~25% HE content** by weight
- British 25-pdr design: 19-ton steel casing + 7% HE fill
- American equivalent (M1): 23-ton steel casing + 15% HE fill

### Target Vulnerability by Posture (Casualty Risk Factors)

Ground-burst artillery effects on average terrain:

| Posture                   | Relative Risk Factor            |
| ------------------------- | ------------------------------- |
| **Standing (exposed)**    | **1.0** (baseline)              |
| **Lying prone**           | **1/3** (~0.33)                 |
| **Open fire trenches**    | **1/15 to 1/50** (0.067–0.020)  |
| **Crouching in trenches** | **1/25 to 1/100** (0.040–0.010) |

**Protective effect of natural ground:** Approximately 5× better than level surfaces for prone soldiers.

## Battlefield Effects Framework

British researchers defined artillery effects in order of difficulty to achieve:

1. **Neutralising** – Prevent movement, observation, and effective weapon use *during* bombardment (immediate suppression)
1. **Morale** – Induce loss of will to resist, lasting *beyond* bombardment (sustained psychological effect)
1. **Lethal** – Kill or wound personnel (physical casualty production)
1. **Material** – Destroy or damage equipment

This hierarchy reflects the observation that suppression and morale effects precede and often prevent lethal effects.

## Required Fire Intensity (Expressed in 25-pdr Equivalence)

Minimum fire intensity to achieve each effect on typical targets:

| Effect                            | Fire Intensity Requirement                                              |
| --------------------------------- | ----------------------------------------------------------------------- |
| **Neutralising** (open positions) | 0.02–0.08 lb/sq yd/hr                                                   |
| **Morale**                        | **0.1 lb/sq yd/hr for 4 hours** OR **0.25 lb/sq yd/min for 15 minutes** |
| **Lethal**                        | 0.1 lb/sq yd/hr (2% casualties in weapon pits; 20% in open positions)   |
| **Material**                      | 0.1 lb/sq yd/hr (1.5% weapon damage in pits; 20% soft vehicle damage)   |

**Note:** lb/sq yd/hr = pound per square yard per hour. 1 pound = 453.6 grams; 1 square yard ≈ 0.836 square meters.

### Practical Density Examples

To achieve **40% casualties among troops in weapon pits**:

- **25-pdr shells:** 40 rounds per 100×100 yard area
- **5.5-inch shells:** 16 rounds per 100×100 yard area (2.5× more effective due to larger HE charge)

## Comparative Shell Effectiveness Data

### HE Content by Shell Type (WWII era)

| Shell System           | HE Content (%) |
| ---------------------- | -------------- |
| 25-pdr (UK)            | 7.0            |
| 4.5-inch Gun (UK)      | 6.9            |
| 105-mm M1 (US)         | 14.8           |
| 122-mm OF-471 (Soviet) | 15.2           |
| 155-mm M107 (US)       | 15.8           |

### Relative Effectiveness to 25-pdr (Effect Multiplier)

| Shell System           | Casualty Effect Multiplier |
| ---------------------- | -------------------------- |
| 76.2-mm Soviet         | 0.9×                       |
| 3.7-inch Howitzer (UK) | 1.0×                       |
| 122-mm Soviet HE-FRAG  | 2.2×                       |
| 7.2-inch Howitzer (UK) | 4.0×                       |

Higher HE content, larger bursting radius, and more efficient fragmentation design compound to produce multiplicative casualty effects.

## Fragment Ballistics

### Initial and Terminal Velocity

- **Initial fragment velocity:** 3,000+ ft/sec from detonation
- **Terminal velocity at impact:** 600–1,000 ft/sec (varies by fragment mass and atmospheric density)
- **Velocity decay:** Rapid initial deceleration due to drag; heavier fragments retain velocity better

### Fragment Spatial Distribution

- **Ground burst pattern:** "Wing-shaped" distribution with forward bias (~25° ahead of static omnidirectional direction)
  - More fragments directed toward friendly forces or advancing assaulting troops
  - Fewer fragments propagate backward toward artillery
- **Air-burst optimal heights:**
  - 5–10 feet: Maximum effectiveness against troops in open
  - 30 feet: Optimal against dug-in troops in trenches (increased coverage area, reduced earth-burst deflection)

### Example Fragmentation Pattern (25-pdr)

From 25-pdr shell at 15% HE content:

```
Fragment size range: <1/25 oz to >2 oz
Total fragment count: ~1,140 fragments
Distribution (approximately):
  - >2 oz:           <19 fragments (large, low-velocity lethal range)
  - 1/4–2 oz:        ~300 fragments (medium, 200–400 ft range)
  - 1/25–1/4 oz:     ~600 fragments (small, 100–200 ft range)
  - <1/25 oz:        >1,122 fragments (dust, minimal range)
```

Optimal anti-personnel design requires maximization of the 1/25–1/4 oz band while minimizing dust and very large fragments.

## Fire Effect Calculation Variables

Weight of fire models must account for numerous sources of uncertainty and error:

### Targeting & Accuracy

- Target location error (intelligence/survey uncertainty)
- Predicted vs. actual fire accuracy (deviation from firing solutions)
- Range probable error (PE_range)
- Line probable error (PE_line)

### Terrain & Geometry

- Ground slope effects on fragment distribution
- Angle of descent influencing fragment pattern orientation
- Terrain roughness and its protective effect (factor of ~5 for prone)

### Munition Performance

- "Blinds" (shells failing to detonate; typically 1–5% of rounds)
- Fuze reliability (ranging from ~95–99% in WWII)
- Fragment mass distribution variability

### Target Characteristics

- Protective qualities of available cover (trenches, fortifications, vehicles)
- Target posture distribution (mix of standing, prone, dug-in troops)
- Unit dispersion (close-packed vs. dispersed formations)

### Model Output

- **Expected casualties** given as percentage with confidence bounds (e.g., "9% ± 3–4 percentage points")
  - Stated range in original: "as low as 5% or as high as 15%"
  - But not: "as low as 2–3% or as high as 30–40%"

## Post-WWII Development & Modernization

### 1960s Improvements

1. **Higher-strength steels** enabling greater HE content:

   - 105-mm Field Howitzer: ~16% HE
   - 155-mm FH70: 26% HE
   - Contrast to WWII 25-pdr at 7%

1. **Explosive charge evolution:**

   - Replacement of TNT with RDX-based explosives (higher detonation velocity, better fragmentation)

1. **Fuze technology:**

   - Modern proximity fuzes with variable height-of-burst options
   - Enables optimization for different target types (open → low burst; trenched → high burst)

### Impact on Casualty Density

Modern systems with ~25% HE content (vs. WWII 7–15%) achieve 3–4× better casualty production per round, partially explaining why post-war artillery doctrine shifted toward rapid fire in brief concentrations rather than prolonged bombardment.

## Model Limitations & Uncertainty

The original researchers explicitly acknowledged the inherent difficulty of predicting artillery casualties:

> "Expected casualties as 9% might range as low as 5% or as high as 15%, but not as low as 2–3% or as high as 30–40%."

This ±4–6 percentage point uncertainty stems from:

1. Variability in terrain protection factors
1. Uncertainty in actual target posture distribution
1. Fuze reliability variation
1. Unpredictable fragment velocity decay in different atmospheric/weather conditions
1. Incomplete knowledge of target armor/fortification quality

**Conclusion:** "There is not, even today [1944–1960s], a good model capable of handling all the variables."

This caveat remains relevant in modern casualty estimation; purely deterministic models that ignore posture, cover, and fragmentation variability will systematically mispredict observed casualties.

## Historical Context & Source

**Conducting Organizations:**

- 1 Operations Research Section (Italy) — Mediterranean theater analysis
- 2 ORS (Northwest Europe) — European theater validation

**Parent Authority:** British War Office, Fire Effect Committee (established 1943)

**Primary Reports:**

- Army Operational Research Group Report No. 179 (March 1944) — Initial findings
- Army Operational Research Group Report No. 234 — Updated findings and confirmation

**Time Period:** Data gathered and analyzed 1943–1946, reflecting actual combat artillery effects in North Africa, Italy, Normandy, Northwest Europe, and Burma.

## Comparison to Modern Standards

### vs. FAS ES-310 (1998)

- ES-310 uses probabilistic Pk framework with fixed energy thresholds (100 J light, 1 kJ moderate, 4 kJ heavy)
- British WWII research derived similar energy bounds empirically (~5–60 ft-lbs ≈ 6.8–80 J) but emphasized **posture-dependent multipliers** rather than absolute energy criteria
- British approach is more sophisticated: accounts for target vulnerability distribution rather than single-point kill probability

### vs. Modern NATO Casualty Models

- NATO models (e.g., CASTFOREM, ESAMS) use similar relative risk factors by posture but with different numerical scaling
- British factors (1/3 prone, 1/25 trenched) are conservative relative to some modern estimates
- Emphasis on 25% HE content for optimal anti-personnel effect is consistent with modern 155-mm howitzer design (FH70: 26% HE)

## Extracted Numerical Summary

| Parameter                              | Value(s)                | Units              |
| -------------------------------------- | ----------------------- | ------------------ |
| Optimal anti-personnel fragment mass   | ~1 gram (under 1/25 oz) | grams / oz         |
| 50% lethal fragment mass @ 200 ft      | 1/8 oz or more          | oz                 |
| Lethal incapacitation energy (British) | 5 ft-lbs                | ft-lbs             |
| Earlier criterion (for comparison)     | 58 ft-lbs               | ft-lbs             |
| Casualty risk: prone / standing        | 1/3                     | ratio              |
| Casualty risk: trenched / standing     | 1/15–1/50               | ratio              |
| Ground protection factor               | ~5×                     | relative           |
| 25-pdr HE content                      | 7%                      | % by weight        |
| Optimal anti-personnel HE content      | ~25%                    | % by weight        |
| 25-pdr fragment count @ 15% HE         | ~1,140                  | total fragments    |
| Fragment velocity at impact            | 600–1,000               | ft/sec             |
| Air-burst height (open)                | 5–10                    | feet               |
| Air-burst height (trenches)            | 30                      | feet               |
| Neutralising fire intensity            | 0.02–0.08               | lb/sq yd/hr        |
| Lethal fire intensity                  | 0.1                     | lb/sq yd/hr        |
| Rounds for 40% casualties (25-pdr)     | 40                      | per 100×100 yd     |
| Rounds for 40% casualties (5.5-inch)   | 16                      | per 100×100 yd     |
| 25-pdr effect multiplier               | 1.0×                    | reference          |
| 122-mm Soviet HE-FRAG multiplier       | 2.2×                    | relative to 25-pdr |
| 7.2-inch British multiplier            | 4.0×                    | relative to 25-pdr |

## Relevance to Fragmentation Casualty Modeling

### Direct Application

1. **Posture-dependent casualty factors:** The 1/3 (prone), 1/15–1/50 (trenched) multipliers provide empirical validation of target vulnerability variation. Modern models often treat posture as discrete states; this historical data supports the relative magnitudes.

1. **Fragment mass optimization:** The emphasis on ~1 gram optimal fragment mass aligns with modern fragmentation theory (Mott, Grady) and validates that very small fragments (dust) and very large fragments (low velocity) are inefficient for casualty production.

1. **HE content vs. effects:** The finding that 25% HE content is needed for optimal anti-personnel effect explains the design ratio in modern howitzers (FH70: 26%, M109A7: ~24%).

1. **Fire intensity scaling:** The 0.1 lb/sq yd requirement for lethal effect provides a historical baseline for calibrating modern models against empirical WWII/postwar casualty data.

### Limitations for Modern Modeling

1. **Limited granularity:** Posture categories (standing, prone, trenched) are binary; actual target distributions are continuous mixtures.

1. **No fragmentation size distribution:** The historical data does not provide the detailed Weibull/Log-Normal distributions needed for Monte Carlo casualty simulation (see Cunniff 2014 for modern distributions).

1. **Terrain roughness uncalibrated:** The "5× protection factor" for natural ground is descriptive but lacks functional form (e.g., slope angle, vegetation density).

1. **No probabilistic kill per fragment:** British data aggregates casualties at the salvo level; modern work (Pk|hit framework) separates fragment lethality from target coverage.

### Bridge to Modern Work

This document serves as a **historical validation benchmark** for modern casualty models. If modern Bayesian fragment-by-fragment models predict casualty rates within 5–15% of historical WWII field data (accounting for improved fuze reliability and higher HE content), confidence in the model increases substantially.

______________________________________________________________________

**Document Source:** https://www.britishartillery.co.uk/wt_of_fire.htm\
**Extraction Date:** 2026-05-24\
**Classification:** Historical non-peer-reviewed doctrinal summary\
**Maintained by:** @librarian
