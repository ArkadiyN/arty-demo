# AISI 1335 Alloy Steel (UNS G13350) — Card

## Identification

|            |                                                        |
| :--------- | :----------------------------------------------------- |
| Title      | AISI 1335 Alloy Steel (UNS G13350)                     |
| Publisher  | AZoM (materials data sheet, secondary compilation)     |
| URL        | `https://www.azom.com/article.aspx?ArticleID=6667`     |
| Local copy | `aisi-1335.md` (no PDF; the source is a live web page) |
| Re-fetched | 2026-08-02, cell-for-cell against the live page        |

## Tables

Transcribed once into `tables/`, per `.claude/rules/source-data-fidelity.md`.
Consumers read the CSV; nothing re-types this series.

| Table                | CSV                        | Closure                                                                 |
| :------------------- | :------------------------- | :---------------------------------------------------------------------- |
| Chemical Composition | `chemical-composition.csv` | iron-balance mass closure, both legs — `chemical-composition.invariant` |

The closure is the source's own construction rule, not a plausibility check:
AZoM computes iron as the balance, so each Fe bound is the complement of the
opposite-extreme sum of every other element. Both legs pass — 100.005 and
100.000 against a target of 100. Because it crosses both columns and all six
elements at once, a value landed on the wrong element or the wrong bound
breaks it.

**Anchor:** the printed heading `Chemical Composition` and the column labels
`Min (%)` / `Max (%)`. No bare line numbers — and note the row-order warning
below, which rules out positional anchors into `aisi-1335.md` as well.

## Composition (from `tables/chemical-composition.csv`)

| Element        | Min (%) | Max (%) |
| :------------- | ------: | ------: |
| Iron, Fe       |    97.3 |   97.92 |
| Manganese, Mn  |    1.60 |    1.90 |
| Carbon, C      |   0.330 |   0.380 |
| Silicon, Si    |    0.15 |    0.35 |
| Sulfur, S      |       — |   0.040 |
| Phosphorous, P |       — |   0.035 |

Row order above is **as printed on the page**. Carbon is 0.33–0.38 %, i.e. not
the ~0.45 % of SAE 1045.

## Mechanical and physical properties

- **Hardness, Brinell (average):** 179–235
- **Hardness, Rockwell C:** 15
- **Elastic modulus:** 190–210 GPa
- **Bulk modulus:** 140 GPa
- **Shear modulus:** 80 GPa
- **Machinability:** 55 (AISI 1212 = 100)
- **Density:** 7.87 g/cm³
- **Thermal expansion:** 11.5 μm/(m·K)
- **Thermal conductivity:** 51.9 W/(m·K)

**Yield strength and tensile strength do not appear anywhere on this page**,
confirmed on re-fetch. Any downstream "min YS 65 ksi, 15 % elong" attached to
this grade came from somewhere else and must cite that source, not this card.

**Specific heat capacity is not on the page either** — `aisi-1335.md` records
it as "(not specified)", which is correct.

## What this document does *not* establish

**No War Department nomenclature appears here.** The steel is identified solely
as AISI 1335 / UNS G13350. The page carries no WD-series linkage of any kind.

So the downstream identification **WD-X1335 ≈ AISI 1335** — which is what puts
0.33–0.38 %C into `experiment/fragmentation-field/_parameters.qmd` for
`WW2 US HE Shell` — is an inference from grade-name similarity, and this
document is not evidence for it. That gap is already recorded downstream as
limitation 13 (`_limitations.qmd`) and as finding F5 in
`experiment/fragmentation-field/updates/wdss1-steel-grade/review.md`; nothing
here closes it.

The distinction that matters for the audit: **the transcription is admissible,
the attribution is not.** A closure invariant certifies that these numbers are
AISI 1335's; it says nothing about whether AISI 1335 is the right steel.

## Provenance of this card

1. **Original extraction** into `aisi-1335.md`.
1. **Independent re-fetch of the live page, 2026-08-02**, reproducing every
    cell of the composition table and every property value.
1. **Iron-balance closure** on `tables/chemical-composition.csv`, passing both
    legs.

### Divergence found on re-fetch, recorded not repaired

**`aisi-1335.md` reorders the composition rows.** The page prints Fe, Mn, C,
Si, S, P; the extraction rewrote them as C, Fe, Mn, Si, P, S. Every
element↔value pairing survived the reordering, so no number is wrong — but a
reader who anchors on "the third row" lands on a different element in the two
files. This is why the anchor above is the column labels and not a position.

**`aisi-1335.md` prints carbon as 0.33/0.38 where the page prints
0.330/0.380.** Trailing zeros dropped; the CSV carries the as-printed
three-decimal form.

### Method note — a fetch summary is not a transcription

The first re-fetch of this page returned a complete-looking property list that
silently omitted `Hardness, Rockwell C: 15`, which had been read as a
disagreement with `aisi-1335.md`. A second, narrowly-targeted fetch confirmed
the value *is* on the page. **An omission in a summarising fetch is not
evidence of absence**; only a question aimed at the specific cell settles it.
Phase 2.5c leans on re-fetches, so this bounds what one of them proves.
