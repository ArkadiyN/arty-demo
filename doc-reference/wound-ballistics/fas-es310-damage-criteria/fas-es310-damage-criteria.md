---
title: Damage Criteria — ES310 Naval Weapons Engineering / FAS DoD Reference
authors: U.S. Navy / Federation of American Scientists
year: 1998
source_url: https://man.fas.org/dod-101/navy/docs/es310/dam_crit/dam_crit.htm
topic: wound-ballistics
---

## Summary

This DoD/Navy training document defines probabilistic damage criteria for fragmentation warheads using a Probability of Kill (Pk) framework with three discrete levels (light/moderate/heavy). Personnel lethality thresholds are given as 100 J (light, Pk = 0.1), 1,000 J (moderate, Pk = 0.5), and 4,000 J (heavy, Pk = 0.9), derived from comparisons to known small-arms calibers. The document formalizes how fragment count, mass, velocity, and range combine into an expected-hits model.

## Key Findings

- The DoD light-damage threshold for personnel is **100 J** (Pk = 0.1)
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

### Personnel Damage Criteria (reconstructed, not a table on the page)

**This is not a table on the source page.** It is Table 3's personnel row
transposed into its own table, with the aircraft and armored-vehicle rows
dropped and a "Caliber Reference" column welded on from prose elsewhere on
the page. Cite `tables/table-3-fragmentation-damage-criteria.csv` (the
personnel row) instead of this reconstruction.

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

## Findings from the 2026-08-03 re-fetch

Do not renumber or reflow the sections above: `updates/pkill-poisson-field/derivation.md` cites this file by bare line number (L16, L42–46, L51–55), which is why finding 3 exists. See `card.md` for the full divergence list and the closure that admits the personnel row.

The "Implications for 79 J Threshold" section, a Key Findings bullet, and a
Summary clause about "79–80 J" previously published here have been removed:
the source page never mentions 79 J or 80 J (confirmed by targeted re-fetch),
so that comparison was a repo argument published as a DoD/Navy claim. The
comparison itself is not lost — it belongs, and already lives, as a modelling
claim in `experiment/fragmentation-field/_limitations.qmd` (limitation 14),
where it is reviewed as an argument rather than inherited as a source premise.
See `card.md`, "The 'Implications for 79 J Threshold' section is not from
this source", for the full account.

**Closed 2026-08-10.** The "Personnel Damage Criteria Table" section above is
now labeled as a reconstruction with a pointer to the CSV, so a reader hitting
it directly (not through `pkill-poisson-field/derivation.md`'s line anchors)
also gets the caveat.

**Closed 2026-08-09.** `pkill-poisson-field/derivation.md` now anchors this
source on the multi-hit aggregation line (line 42 below) and on the
0.5-at-1,000-J per-hit criterion line (line 16 above), both grep-verified
against this file — quoted in full above rather than restated here, so this
note itself does not collide with either anchor. Its third citation, which
pointed at the "Personnel Damage Criteria Table" rows, was moved onto the
`personnel` row of `tables/table-3-fragmentation-damage-criteria.csv` instead —
so it no longer rests on the reconstructed table flagged directly above, without pre-empting
that finding.
