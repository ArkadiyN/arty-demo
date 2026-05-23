---
title: Damage Criteria — ES310 Naval Weapons Engineering / FAS DoD Reference
authors: U.S. Navy / Federation of American Scientists
year: 1998
source_url: https://man.fas.org/dod-101/navy/docs/es310/dam_crit/dam_crit.htm
topic: wound-ballistics
---

## Summary

This DoD/Navy training document defines probabilistic damage criteria for fragmentation warheads using a Probability of Kill (Pk) framework with three discrete levels (light/moderate/heavy). Personnel lethality thresholds are given as 100 J (light, Pk = 0.1), 1,000 J (moderate, Pk = 0.5), and 4,000 J (heavy, Pk = 0.9), derived from comparisons to known small-arms calibers. The document formalizes how fragment count, mass, velocity, and range combine into an expected-hits model, making the 79–80 J fixed threshold appear conservative relative to the DoD's own 100 J "light damage" floor.

## Key Findings

- The DoD light-damage threshold for personnel is **100 J** (Pk = 0.1), not 79–80 J; the 79 J value falls *below* even the lightest defined damage level
- Moderate personnel kill criterion is **1,000 J** (Pk = 0.5, ".357 jacketed soft-point" equivalent)
- Heavy personnel kill criterion is **4,000 J** (Pk = 0.9, sufficient to "penetrate body armor")
- Lethality is computed probabilistically via expected fragment hits, not a binary energy pass/fail
- Fragment velocity decays sharply with range: a typical fragment at 200 m retains only ~1/3 of initial velocity, reducing KE to ~1/9 of muzzle value
- "Lethal range" is formally defined as the standoff at which Pk = 0.50 against personnel

## Extracted Content

### Pk Framework

> "Pk = a statistical measure of the likelihood that the target will be incapacitated."
>
> Conditional kill probability:
>
> ```
> Pk = Phit × Pk|hit
> ```

### Fragment Hit Model

Expected fragment hits on a target of frontal area A at range R from a warhead with N₀ initial fragments:

```
Nhits = A × (N₀ / 4πR²)
```

Aggregate Pk from multiple hits:

```
If Nhits > 1:  Pk = 1 - (1 - Pk|hit)^Nhits
If Nhits < 1:  Pk ≈ Nhits × Pk|hit
```

### Personnel Damage Criteria Table

| Damage Level | Pk  | Kinetic Energy Threshold | Caliber Reference         |
| ------------ | --- | ------------------------ | ------------------------- |
| Light        | 0.1 | 100 J (0.1 kJ)           | .22 Long Rifle equivalent |
| Moderate     | 0.5 | 1,000 J (1 kJ)           | .357 jacketed soft-point  |
| Heavy        | 0.9 | 4,000 J (4 kJ)           | Armor-penetrating level   |

### Hand-Grenade Worked Example

At 2 m from a grenade with 200 fragments at 3,000 J each:

- Pk ≈ 0.9984 (near-certain kill)

At 5 m:

- Nhits = 0.6 → Pk ≈ 0.50 (lethal range boundary)

### Implications for 79 J Threshold

The 79 J value commonly cited as the "hazardous fragment energy" threshold in military vulnerability analyses sits below the DoD's own 100 J light-damage floor (Pk = 0.1). This means the fixed 79 J criterion is a minimum-incapacitation floor, not a Pk = 0.5 lethality criterion. Using it as a binary kill threshold in HE fragmentation models will overestimate lethality at short range and misrepresent the probabilistic nature of fragment casualties.
