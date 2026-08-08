---
title: British Artillery Weight of Fire — WWII Casualty & Fragment Lethality
source_type: 'Secondary historical summary (primary: AORG Report No. 179, 1944)'
---

## Source

**Secondary source:** https://www.britishartillery.co.uk/wt_of_fire.htm (Nigel F Evans, © 2001–2014)

**Primary source cited:** Army Operational Research Group Report No. 179, "Lethal and Material Effects of Gunfire and Bombing on Land Targets" (20 March 1944); updated Report No. 234

**Original not re-acquirable at this pass** — archival AORG Report 179 and 234 do not surface in web search or public repositories. Card built from the secondary summary alone.

## Known Defects

Two independent arithmetic failures internal to this secondary source. Neither
can be adjudicated here: the primary (AORG 179) was not obtainable, so there is
no page to go back to.

**1 — the mass conversion.** Anchor: `50% Lethality Criterion`, under
`### Fragment Lethality & Optimal Anti-Personnel Design`.

> "A fragment of 1/8 oz (~28 grams) or more had 50% probability of lethality at 200 feet"

1/8 oz ≈ 3.54 g, not 28 g (1 oz ≈ 28.35 g). 28 g is a full ounce. Which of the
two figures is the transcription error is not determinable from this document.

**2 — the fragment-count table does not sum to its own stated total.** Anchor:
`Total fragment count: ~1,140 fragments`, under
`### Example Fragmentation Pattern (25-pdr)`. The four bands are stated as
disjoint mass ranges spanning `<1/25 oz to >2 oz`, so they must sum to the
stated total:

| Band             | Count      |
| ---------------- | ---------- |
| >2 oz            | \<19       |
| 1/4–2 oz         | ~300       |
| 1/25–1/4 oz      | ~600       |
| \<1/25 oz        | >1,122     |
| **Sum**          | **>2,041** |
| **Stated total** | **~1,140** |

Off by ~1.8×. The `<1/25 oz` band alone nearly equals the stated total. This is
a closure failure on the source's own stated definitions, not a rounding
artifact — the table is inadmissible as a fragment-count series until the
primary resolves it.

## Governing Definitions & Constants

Anchors below are greppable strings, verified against the stored `.md` at
authoring; line numbers are given only as a convenience and are not the anchor.

**Casualty Vulnerability by Posture** — anchor: `### Target Vulnerability by Posture (Casualty Risk Factors)` (~line 35):

| Posture               | Risk Multiplier          | Notes                                                |
| --------------------- | ------------------------ | ---------------------------------------------------- |
| Standing (baseline)   | 1.0                      | Reference                                            |
| Lying prone           | 1/3 ≈ 0.33               | ~5× protection from natural ground vs. level surface |
| Open trenches         | 1/15–1/50 (0.067–0.020)  | Range given; boundaries not specified                |
| Crouching in trenches | 1/25–1/100 (0.040–0.010) | Range given; boundaries not specified                |

**Fire Intensity for Effects** — anchor: `## Required Fire Intensity (Expressed in 25-pdr Equivalence)` (~line 59), units lb/sq yd/hr:

| Effect       | Intensity                                 | Target Type                           | Casualty Yield                           |
| ------------ | ----------------------------------------- | ------------------------------------- | ---------------------------------------- |
| Neutralising | 0.02–0.08                                 | Open positions                        | Suppression only                         |
| Morale       | 0.1 (sustained 4 hr) or 0.25/min (15 min) | —                                     | Psychological lasting beyond bombardment |
| Lethal       | 0.1                                       | Weapon pits: 2%; open: 20%            | Physical casualties                      |
| Material     | 0.1                                       | Pits: 1.5% damage; soft vehicles: 20% | Equipment damage                         |

Conversion given: 1 lb = 453.6 g; 1 sq yd ≈ 0.836 m².

**Fragment Distribution from 25-pdr @ 15% HE** — anchor:
`### Example Fragmentation Pattern (25-pdr)` (~line 119). **Reproduced under
Known Defect 2 above; it fails its own stated total and is not citable.**

**Optimal HE Content:** ~25% by weight for anti-personnel effect — anchor:
`~25% HE content` (~line 31).

## Validity & Scope

**Data source:** Combat artillery effects from North Africa, Italy, Normandy, NW Europe, Burma, 1943–1946.

**Acknowledged uncertainty** — anchor: `Expected casualties as 9% might range as low as 5%` (~line 197), under `## Model Limitations & Uncertainty`. ±4–6 percentage point range; stems from terrain variability, posture distribution unknown, fuze reliability, atmospheric decay, fortification quality.

**Explicit caveat** — anchor: `There is not, even today` (~line 207): "There is not, even today [1944–1960s], a good model capable of handling all the variables."

## Numeric Series for Transcription

**None extracted.** The one table in this document with a closure structure —
the 25-pdr fragment-count bands against their stated total — **fails that
closure** (Known Defect 2), so transcribing it would propagate a broken series.
The remaining figures (posture risk factors, fire-intensity thresholds) are
empirical aggregates with no internal relation to check.

## Admissibility

**State: unverifiable.** The primary — AORG Report No. 179 (and its update
No. 234) — did not surface in web search or public archives at this pass, and
no `source.pdf` is retained. The only surface available is this secondary
web summary, which carries two internal arithmetic failures.

Per `.claude/rules/source-data-fidelity.md` this is a legitimate terminal
state, not a failure — but it is binding on consumers: **every claim resting on
this document is provisional**, and no number from it may be presented as
checked. Its one live consumer is the Check 5b assert in
`experiment/fragmentation-field/_validation.qmd`.
