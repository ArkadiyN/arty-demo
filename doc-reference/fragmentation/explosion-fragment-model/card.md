# Felix, Colwill & Harris (2022) — A model for the fragments of an explosion

**Document:** "Explosion fragment model" — *Defence Technology* **18** (2022) 159–169\
**Authors:** D. Felix, I. Colwill, P. Harris (University of Brighton)\
**DOI:** https://doi.org/10.1016/j.dt.2020.12.006 (open access)\
**Extraction:** `1-s2.0-S221491472030502X-main.md`, figures in `images/`\
**Retained scan:** `source.pdf` beside this card, 11 pages — **not committed**
(`.gitignore:58`); re-acquire from the DOI above.

## Tables — read these, not the prose

| File                                           | What it holds                                                             | Closure                                                                |
| ---------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `tables/table-4-average-aspect-ratios.csv`     | the three per-dataset average aspect ratios whose mean is the shipped 1.6 | sum = 4.72, so mean 1.573 → 1.6                                        |
| `tables/table-4-aspect-ratio-distribution.csv` | Table 4 — bin counts and percentages for Grady, Hiroe and Mott            | each percentage column sums to 100 and reproduces its own count column |
| `tables/table-3-grady-aspect-ratio-counts.csv` | Table 3 — Grady's Fig. 10 counted by size Group and bin                   | Group rows sum to their totals and reproduce the published Total row   |

```
uv run src/utils/check-table-invariants.py doc-reference/fragmentation/explosion-fragment-model/tables --all
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/explosion-fragment-model-aspect-ratio.py
```

## The fact this document supplies to the model

Anchors: `Approximate average ratio` (Table 4, `source.pdf` p.9 = journal
p.167) and `aspect ratio of a fragment is defined` (§2.5, p.3 = p.161).

**Fragment width : length = 1 : 1.6.** `src/arty/fragmentation.py` ships it as
`_MOTT_ASPECT_RATIO = 1.6`.

**The direction of the ratio is the thing to get right.** §2.5 states it
outright — *"The aspect ratio of a fragment is defined as a fragment's width
divided by its length"* — and Table 4's column head repeats it as
`(width: length)`. So **length = 1.6 × width**: fragments are long and thin.
Inverted, the model would produce short fat fragments and there is no numeric
tell, because 1.6 is a plausible number either way round.

Where 1.6 comes from, per Table 4's bottom row:

| Dataset | Figure  | Casing      | Average width:length |
| ------- | ------- | ----------- | -------------------- |
| Grady   | Fig. 10 | ogive       | 1 : 1.58             |
| Hiroe   | Fig. 11 | cylindrical | 1 : 1.66             |
| Mott    | Table 2 | cylindrical | 1 : 1.48             |

Mean 1.573, rounded to **1.6**. Corroborated in §2.5 on other materials:
Wilson **1 : 1.65** (tungsten-alloy cylindrical casing), Grady **1 : 1.5**
(AERMET-100 steel casing) — note these are a *different* Grady figure from the
1.58 in Table 4.

### Caveat carried with the number

The bottom row of Table 4 is labelled "Approximate average ratio" and the three
values do **not** reproduce as count-weighted means of their own columns: Mott's
59/30/10/1 gives 1.53 rather than the printed 1.48, and Grady's 1.58 requires
the open "1:4 and more" bin to be weighted near 6. The paper states no
weighting rule for the open bin. The spread of the three (1.48–1.66) is wider
than that discrepancy, and 1.6 is exactly what the paper concludes, so this is
a transparency note rather than a correction — but a pass that wanted to
re-derive the average from the distributions should expect not to land on 1.6.

## Other content cited elsewhere in this repo

- **Mott's engineering closure** `M_A = B_m t^{5/6} d^{1/3} (1 + t/d)` with
    `μ = M_A²`, `N₀ = M / 2M_A²` — §3, anchor `Mott's equation is shown in`.
    `B_m` values are *not* in this paper; it refers them out to Needham,
    *Blastwaves*.
- **The three stated weaknesses of Mott's number model** — anchor
    `The main weakness of Mott's work`: no fragment shape, no origin position on
    the casing, and the small-fragment count.
- **§5 warning on cubic-fragment assumptions**, cited by
    `updates/mott-fragment-shape-closure/`.
- **Simulation setup** (§4.2): cuboid fragments, Poisson-distributed length
    with mean 1.1 cm (Mott's estimate, §2.4) and width `1/1.6`. Those two means
    imply a ratio of 1.76, not 1.6 — the paper does not reconcile it. Nothing
    in this repo consumes the simulation setup.

## Applicability

Casings are ogive (Grady) and cylindrical (Hiroe, Mott); the corroborating
values are for tungsten alloy and AERMET-100. The repo applies 1.6 to WW2 US
forged-steel HE shell bodies. Whether that transfer is sound is a
criterion-match question for @model-reviewer, not a transcription question —
see `.claude/rules/source-data-fidelity.md`.

## Provenance of this card

Written 2026-08-02 during the Phase-2.5 source admissibility gate; this
document previously had **no card at all** despite being cited by shipped code.
Detail: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
§16.
