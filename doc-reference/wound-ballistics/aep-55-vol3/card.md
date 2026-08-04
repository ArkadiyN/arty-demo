# AEP-55 (C) Vol. 3 (Part I) — NATO armoured-vehicle IED protection standard — Card

## Identification

|            |                                                                                                             |
| :--------- | :---------------------------------------------------------------------------------------------------------- |
| Title      | *Procedures for Evaluating the Protection Level of Armoured Vehicles — IED Threat*                          |
| Publisher  | NATO Standardization Agency, Allied Engineering Publication                                                 |
| Edition    | Edition C, Volume 3 (Part I), Version 1, **Ratification Draft 1**                                           |
| Marking    | NATO UNCLASSIFIED, releasable to PFP and Australia                                                          |
| Extraction | `ae-55-c-vol3_compress.md` (full text, 1 623 lines) and `aep-55-vol3.md` (410-line digest)                  |
| Scan       | `source.pdf`, retained on disk, gitignored per `doc-reference/**/*.pdf` — 106 pp., text layer on every page |
| Verified   | 2026-08-03, scope checked against the retained scan                                                         |

## This document supplies no number to this repo, and cannot

**Nothing in `src/arty/`, any `.qmd`, or any check script reads a value out of
it.** That is the whole of its status, and this card exists to make the absence
durable rather than leave it to be re-discovered.

The repo cites AEP-55 Vol. 3 in one role only — as a *canonical reference for
personnel posture geometry* (the box-body dimensions $w_\perp, h, d$ and the
0.85 m² nominal presented area). **It is not one.** Vol. 3 is a vehicle test
standard: an IED threat definition, a phased acceptance process, and blast /
fragmentation / EFP test procedures. Occupant survivability is assessed by
firing at instrumented **ATDs** (anthropomorphic test devices — crash dummies)
and reading injury-assessment reference values off their transducers. A
man-silhouette presented area is not a quantity such a document would ever
state, because nothing in its method uses one.

Verified by search over all 106 pages:

```
terms: presented area|projected area|silhouette|man-target|standing man|
       prone man|frontal area|exposed area|body area
hits:  0
```

Script:
`experiment/fragmentation-field/challenges/source-data-audit/checks/aep-55-vol3-scope-check.py`
(~0.2 s; skips cleanly when the gitignored scan is absent). An absence claim is
the easiest kind to assert and the easiest to get wrong, so it is made here by
re-runnable search rather than by reading.

### The one area figure, and why it is a trap

The document contains exactly two square-metre quantities:

| Page | Figure         | What it is                                                                  |
| ---: | :------------- | :-------------------------------------------------------------------------- |
|   44 | `2 × 2 m²`     | minimum dimensions of the test bed                                          |
|   85 | `A = 0.082 m²` | **effective area of the Annex E lumped-parameter thorax model** (Figure E7) |

`A = 0.082 m²` sits beside a mass, a spring constant, a damping factor and a
lung gas volume: it is the chest-wall area of an Axelsson-type blast-lung
injury model, **not a presented area**. It is within a factor of ~10 of the
0.85 m² the repo wants, is expressed in the same units, and appears in the one
document the repo names as the canonical source for that number — which is
precisely the shape of mistake this audit exists to prevent. It must not be
picked up as a silhouette area.

## Two repo surfaces disagree about this document; one is stale

- **`updates/pkill-poisson-field/scoping.md:75-81` is correct.** It records that
    both Cunniff (2014) and AEP-55 Vol. 3 *are* collected, that neither carries a
    quotable nominal personnel presented-area scalar, and that 0.85 m²
    consequently remains an engineering convention rather than a
    primary-literature citation. The scan confirms this exactly.
- **`_limitations.qmd:238-242` is stale, twice.** It tells readers the canonical
    references "are **not** present in `doc-reference/`" — both are — and it
    advises treating posture-resolved hit counts as ±25 % estimates "until the
    references are collected", which describes an action that can never
    discharge the caveat. Collecting AEP-55 Vol. 3 does not supply posture
    box-body dimensions; the document does not contain them and would not.

The disclosure the model *should* carry is `scoping.md`'s, which is weaker and
true: the value is an engineering convention, and the uncertainty on it is not
retired by any acquisition. Recorded as a finding, **not repaired here**, per
the audit's deferred-repairs scope.

## Anchors

Greppable strings, per `.claude/rules/source-data-fidelity.md`. No bare line
numbers — and note the extraction exists in two forms, so positional anchors
into either are doubly unsafe.

| For                               | Anchor                                                             |
| :-------------------------------- | :----------------------------------------------------------------- |
| the document's identity           | `PROTECTION LEVEL OF ARMOURED VEHICLES - IED THREAT`               |
| the occupant-assessment method    | `Occupant Survivability (Safety) Evaluation`                       |
| the ATD basis (why no silhouette) | `ATD PREPARATION AND CERTIFICATION`, `Anthropomorphic Test Device` |
| the thorax-model area trap        | `Figure E7: Thorax model.`                                         |
| the vulnerable-area section       | `Vehicle Acceptance & Vulnerable Area Assessment`                  |

Note that "Vulnerable Area" here is a **vehicle** VA, not a personnel VA — the
same two words carry the opposite referent from the vulnerability literature
this repo otherwise draws on.

## Tables

**None transcribed.** The document's tables are test-condition matrices and
injury-assessment reference values for ATD instrumentation; none is cited
anywhere in this repo, and none feeds a physical quantity in the model. If a
future pass ever needs an ATD injury threshold, it is a fresh transcription
with its own closure — nothing here is pre-validated for that use.

`images/fig1.png` is a single extracted figure, not digitized anywhere.

## Why this card exists

Written during the Phase 2.5c admissibility sweep of the source-data audit.
The document was flagged as carrying an image and no CSV, and separately as the
subject of a contradiction between two committed surfaces. The scan was
supplied by the user on 2026-08-03 and settled both: the document is
admissible in the only sense that applies to it — **it is cited for nothing,
correctly, and the one surface that implies otherwise is wrong.**
