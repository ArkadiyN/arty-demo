---
title: British Artillery Weight of Fire — WWII Casualty & Fragment Lethality
source_type: Secondary historical summary (primary: AORG Report No. 179, 1944)
---

## Source

**Secondary source:** https://www.britishartillery.co.uk/wt_of_fire.htm (Nigel F Evans, © 2001–2014)

**Primary source cited:** Army Operational Research Group Report No. 179, "Lethal and Material Effects of Gunfire and Bombing on Land Targets" (20 March 1944); updated Report No. 234

**Original not re-acquirable at this pass** — archival AORG Report 179 and 234 do not surface in web search or public repositories. Card built from the secondary summary alone.

## Known Defect

**Line 20 (section "Fragment Lethality & Optimal Anti-Personnel Design")** states:

> "A fragment of 1/8 oz (~28 grams) or more had 50% probability of lethality"

**Error:** 1/8 oz ≈ 3.54 grams, not 28 grams. (1 oz ≈ 28.35 g; 1/8 × 28.35 ≈ 3.54.)
The conversion shown is internally inconsistent — 28 g is approximately 1 oz, not 1/8 oz.

## Governing Definitions & Constants

**Casualty Vulnerability by Posture** — "Target Vulnerability by Posture (Casualty Risk Factors)" (line 35):

| Posture               | Risk Multiplier          | Notes                                                |
| --------------------- | ------------------------ | ---------------------------------------------------- |
| Standing (baseline)   | 1.0                      | Reference                                            |
| Lying prone           | 1/3 ≈ 0.33               | ~5× protection from natural ground vs. level surface |
| Open trenches         | 1/15–1/50 (0.067–0.020)  | Range given; boundaries not specified                |
| Crouching in trenches | 1/25–1/100 (0.040–0.010) | Range given; boundaries not specified                |

**Fire Intensity for Effects** — "Required Fire Intensity" table (line 59), units lb/sq yd/hr:

| Effect       | Intensity                                 | Target Type                           | Casualty Yield                           |
| ------------ | ----------------------------------------- | ------------------------------------- | ---------------------------------------- |
| Neutralising | 0.02–0.08                                 | Open positions                        | Suppression only                         |
| Morale       | 0.1 (sustained 4 hr) or 0.25/min (15 min) | —                                     | Psychological lasting beyond bombardment |
| Lethal       | 0.1                                       | Weapon pits: 2%; open: 20%            | Physical casualties                      |
| Material     | 0.1                                       | Pits: 1.5% damage; soft vehicles: 20% | Equipment damage                         |

Conversion given: 1 lb = 453.6 g; 1 sq yd ≈ 0.836 m².

**Fragment Distribution from 25-pdr @ 15% HE** (line 119):

Total ~1,140 fragments:

- ">2 oz": \<19 fragments
- "1/4–2 oz": ~300 fragments
- "1/25–1/4 oz": ~600 fragments (optimal anti-personnel band)
- "\<1/25 oz": >1,122 fragments (dust, minimal range)

**Optimal HE Content:** ~25% by weight for anti-personnel effect (line 31).

## Validity & Scope

**Data source:** Combat artillery effects from North Africa, Italy, Normandy, NW Europe, Burma, 1943–1946.

**Acknowledged uncertainty (line 197):** "Expected casualties as 9% might range as low as 5% or as high as 15%, but not as low as 2–3% or as high as 30–40%." ±4–6 percentage point range; stems from terrain variability, posture distribution unknown, fuze reliability, atmospheric decay, fortification quality.

**Explicit caveat:** "There is not, even today [1944–1960s], a good model capable of handling all the variables" (line 207).

## Numeric Series for Transcription

No CSV-worthy table suitable for closure invariant — casualty risk factors and fire intensity thresholds are empirical aggregates lacking supporting row structure or stated totals.
