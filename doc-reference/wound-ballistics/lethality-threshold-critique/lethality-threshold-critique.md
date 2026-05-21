---
title: What's Wrong with the Wound Ballistics Literature, and Why
authors: Fackler, M.L.
year: 1987
source_url: https://www.rkba.org/research/fackler/wrong.html
topic: wound-ballistics
---

## Summary

Fackler's 1987 Army Institute of Research technical report argues that kinetic energy transfer is fundamentally the wrong framework for predicting wound severity. Using identical KE, a large slow fragment crushes more tissue (larger permanent cavity) while a small fast one stretches more tissue (large temporary cavity with potentially minimal lasting damage) — the wound morphologies are entirely different. Fackler recommends replacing fixed-energy thresholds with wound profiles that separately quantify the permanent crush cavity and temporary stretch cavity as functions of penetration depth.

## Key Findings

- **KE ≠ damage**: Two projectiles with identical KE but different mass/velocity combinations produce qualitatively different wound morphologies and tissue destruction patterns
- Elastic tissues (muscle, lung, bowel) recover from stretch (temporary cavity) with minimal lasting damage; rigid structures (liver, bone, fluid-filled organs) do not — tissue type dominates over KE
- The standard 15 cm gelatin block test is insufficient: actual human torso penetration paths can be **up to 4× longer**, and the block does not account for projectile fragmentation
- Broadhead arrow with only ~68 J (50 ft-lb) can be immediately lethal via hemorrhage; a 79 J fragment may not incapacitate at all if it traverses only elastic soft tissue
- Temporary cavity pressure cited in ballistics literature (~100 atm) is a "100× overestimate"; actual measured values are ~4 atm
- Temporary cavity diameter cited as "30× projectile diameter" is incorrect; actual data shows ~11 sphere-diameters
- Recommended replacement: **wound profiles** — tissue crush cross-section vs. penetration depth curves that explicitly separate permanent cavity from temporary cavity

## Extracted Content

### Core Argument Against KE Thresholds

> "A large slow projectile...will crush a large amount of tissue, whereas a small fast missile with the same kinetic energy...will stretch more tissue but crush little."

KE deposit is consumed by multiple non-destructive pathways:

1. Sonic pressure wave propagation (no tissue disruption at realistic fragment velocities)
1. Tissue heating
1. Projectile deformation
1. Tissue kinetic motion (recovers elastically in compliant tissues)

None of these pathways necessarily disrupts tissue, yet all consume KE that a threshold model counts as "lethal energy."

### Tissue-Dependency of Damage

| Tissue Type                  | Response to Temporary Cavity Stretch                           |
| ---------------------------- | -------------------------------------------------------------- |
| Skeletal muscle              | Elastic recovery, minimal lasting damage                       |
| Lung                         | Elastic recovery, typically not lethal unless large vessel hit |
| Bowel (air-filled)           | Elastic recovery                                               |
| Liver, spleen (solid organs) | Fractures, significant damage                                  |
| Bone                         | Shatters above threshold velocity                              |
| Fluid-filled structures      | Hydraulic rupture, severe damage                               |

A 79 J fragment through skeletal muscle may cause a survivable wound; the same fragment perforating liver may be fatal. A single energy threshold cannot capture this.

### What Fackler Recommends Instead

1. **Wound profiles**: Plot of crush (permanent) cavity diameter and stretch (temporary) cavity diameter vs. penetration depth for each specific projectile
1. **Objective clinical assessment**: Physical examination and radiographic findings, not pre-calculated energy budgets
1. **Projectile-specific characterization**: Whether the fragment deforms, tumbles, or fragments in tissue determines the permanent cavity independent of initial KE
1. **Penetration depth accounting**: A 15 cm test block dramatically underestimates tissue path length; the exit velocity (remaining energy) must be measured

### Specific Numerical Corrections

| Parameter                 | Literature Value (erroneous) | Fackler's Measured Value |
| ------------------------- | ---------------------------- | ------------------------ |
| Temporary cavity pressure | ~100 atm                     | ~4 atm                   |
| Temp. cavity diameter     | 30× projectile diameter      | ~11 sphere diameters     |
| Torso tissue path length  | 15 cm (gelatin block)        | Up to 60 cm              |

### Historical Infection Rate Data (Validates Conservative Management)

| Conflict     | Clostridium myositis rate |
| ------------ | ------------------------- |
| World War I  | 5%                        |
| World War II | 0.7%                      |
| Korean War   | 0.08%                     |

Decline attributed to improved surgical technique, not to better lethality threshold models.

### Citation Information

**Document**: Institute Report No. 239\
**Institution**: Letterman Army Institute of Research, Presidio of San Francisco\
**Date**: July 1987\
**Author**: M.L. Fackler, M.D.\
**Web source**: HTML conversion of scanned report, hosted at rkba.org

### Implications for 79 J Fixed Threshold

Fackler's analysis directly undermines a binary 79 J kill threshold. The 79 J value was derived from empirical infantry-fire datasets without controlling for tissue type, fragment shape, or velocity/mass ratio. A single threshold predicts neither Pk nor wound severity reliably — it only identifies the approximate floor at which penetration of soft tissue becomes probable. For an HE fragmentation model, replacing the 79 J binary with a Pk curve parameterized by fragment mass, velocity, and standoff range (as in the DoD ES310 framework) would be substantially more defensible.
