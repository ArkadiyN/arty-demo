# Source-data audit ledger — ordnance-1944 and Tolch-1938

Provenance and verdict record for every artifact that consumes numbers from
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/` or
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/`.

Repairs are **deferred by design** — this ledger is the map that drives the
redo, not a record of fixes. `src/arty/` is assessed, never changed here.

| Phase                             | State                                   |
| --------------------------------- | --------------------------------------- |
| 0 — inventory & provenance        | **done** (this document, sections 1–4)  |
| 1 — re-baseline ordnance-1944     | pending                                 |
| 2 — re-baseline Tolch-1938        | pending                                 |
| 3 — downstream verdict per thread | pending (verdict column below unfilled) |
| 4 — `src/arty` assessment         | pending                                 |
| 5 — independent verification      | pending                                 |
| 6 — surface reconciliation        | pending                                 |

## 1. The discriminator

Evidence: [`checks/column-identity-energy-closure.py`](checks/column-identity-energy-closure.py)

Each 1944 Ordnance shell page prints **two tables interleaved row-by-row** from
a two-column scan — CASUALTIES and PERFORATION OF 1/8-IN. MILD STEEL. Column
identity is not derivable from the layout. The one relation internal to the
table is the source's own definition: every row lists the *lightest effective
fragment* `(m, v)`, so `½mv²` must reproduce the caption's stated 58 ft-lb
casualty criterion, and only on the casualties column.

Run on the merged `ordnance-1944.md` (post-`e62ff71`, which repaired the OCR
row-order swaps):

| shell      | line of pair | range grid | B(20 ft) | ½mv² across all rows | identity       |
| ---------- | ------------ | ---------- | -------- | -------------------- | -------------- |
| 75mm M48   | **first**    | 20–400 ft  | 0.213    | 57.5 – 58.0 ft-lb    | **CASUALTIES** |
| 75mm M48   | second       | 20–225 ft  | 0.106    | 271.9 – 828.6 ft-lb  | perforation    |
| 105mm M1   | **first**    | 20–500 ft  | 0.231    | 57.7 – 58.2 ft-lb    | **CASUALTIES** |
| 105mm M1   | second       | 20–300 ft  | 0.194    | 247.8 – 930.1 ft-lb  | perforation    |
| 155mm M107 | **first**    | 20–600 ft  | 0.291    | 55.9 – 58.2 ft-lb    | **CASUALTIES** |
| 155mm M107 | second       | 20–400 ft  | 0.247    | 247.8 – 1145.8 ft-lb | perforation    |

Uniform across all three shells: **first line of each printed row-pair is
CASUALTIES.** No ambiguity, no shell-specific exception.

Three things that look like discriminators and are not:

- **Max range.** Casualties runs *longer* (400/500/600 ft) than perforation
    (225/300/400 ft) — but nothing in the scan says so. `b-vs-range-75mm.py`
    asserted the reverse and had no way to tell.
- **`B` non-increasing.** True of *both* columns, every row, all three shells.
    Zero discriminating power, yet cited as a corroborating check.
- **Caption order.** The two `TABLE nn` lines print in the opposite order to the
    two caption lines (`TABLE 44 / TABLE 43 / CASUALTIES / PERFORATION…`), so
    even the table-number-to-caption mapping is unresolved by position.

## 2. How the inversion entered and spread

1. **`card.md` summarised each table-pair into loose fields** — one column's
    `B` beside the other column's range (75mm: `B@20 = 0.213` is casualties,
    `20–225 ft` is perforation). Coherent-looking, and wrong as a pair.
1. **`b-vs-range-75mm.py` used the card's range field as the column-identity
    discriminator** (docstring: *"the column carrying Table 43 is identified by
    its max range (225 ft), which matches the challenge doc's statement"*). A
    lossy summary became ground truth for the one fact it did not guarantee.
    The corroborating test it cites (`B` monotone) cannot discriminate.
1. **The 75mm r=40 "row-swap correction" is an artefact of that inversion.**
    The script invented a transposition at r=40 to restore monotonicity *within
    its inverted assignment*. In the current file, `r=40` closes at 57.5 ft-lb
    in first-line position like every other row — the pair is in normal order.
1. **`b-vs-range-105mm.py` and `-155mm.py` copied the method**, both landing on
    the perforation column.
1. **The error was then found — twice — and never actioned.**
    `initial-conditions-105mm.md` §(b)/(c) and `initial-conditions-155mm.md`
    both run the energy closure correctly, both conclude the b-vs-range scripts
    used the wrong column, and both defer the fix ("*out of scope — flagged for
    a follow-up fix*"). The follow-up never happened.
1. **A factor-of-4 arithmetic slip inside `initial-conditions-105mm.md`
    admitted the wrong column first.** Line 44 reports `0.035 oz @ 2700 f/s ≈  62.0 ft-lb — within ~7% of 58`. The correct value is **247.8 ft-lb**. That
    bogus "verified" line sits above a reconstructed table labelled *"Table 51
    CASUALTIES"* carrying perforation values — and it is that pre-correction
    table, not the corrected one 40 lines below it, that
    `drag-coefficient-calibration.py` copied and labelled *"corrected
    identification"*.
1. **Propagation by import.** `b-vs-range-familyA.py` loads the three Family B
    modules and reuses their `CARD_R_FT`/`CARD_B` directly — the newest analysis
    inherits the inversion without re-typing a digit. Two further scripts
    inherit from those.

## 3. Ordnance-1944 consumers

Verdict column: **sound** (unaffected) / **shifted** (same conclusion, different
numbers) / **void** (conclusion does not survive). Filled in Phase 3.

### 3a. Direct literal arrays

| artifact                                                                       | numbers consumed                                                                      | provenance                                                 | verdict |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------- |
| `drag-gap-1944/checks/b-vs-range-75mm.py:47`                                   | `CARD_R_FT` 20–225, `CARD_B` [.106 … .0001]                                           | **PERFORATION** ✗                                          | Ph. 3   |
| `drag-gap-1944/checks/b-vs-range-105mm.py`                                     | `CARD_R_FT` 20–300, `CARD_B` [.194 … .0001]                                           | **PERFORATION** ✗                                          | Ph. 3   |
| `drag-gap-1944/checks/b-vs-range-155mm.py:44`                                  | `CARD_R_FT` 20–400, `CARD_B` [.247 … .0001]                                           | **PERFORATION** ✗                                          | Ph. 3   |
| `drag-gap-1944/checks/initial-conditions-105mm.py:19`                          | 105mm `(r, m, v)` to 500 ft                                                           | casualties ✓                                               | Ph. 3   |
| `drag-gap-1944/checks/initial-conditions-155mm-decay.py:21`                    | 155mm `(r, m, v)` to 600 ft                                                           | casualties ✓                                               | Ph. 3   |
| `drag-gap-1944/checks/initial-conditions-105mm-ke.py`                          | 105mm perforation `(m, v)`                                                            | diagnostic — intent ✓                                      | Ph. 3   |
| `drag-gap-1944/checks/initial-conditions-105mm-ke2.py`                         | both 105mm sequences                                                                  | diagnostic ✓ — **this is the script that found the error** | Ph. 3   |
| `drag-gap-1944/checks/initial-conditions-probe3.py:15`                         | perforation *r*-grid + casualties `m/v`                                               | **MIXED** ✗                                                | Ph. 3   |
| `drag-gap-1944/checks/drag-coefficient-calibration.py:71`                      | 75✓ / **105 ✗** / 155✓ in one `DATA` block; comment claims "corrected identification" | **MIXED** ✗                                                | Ph. 3   |
| `drag-gap-1944/checks/shape-closure-orthogonality.py`                          | 75✓ / **105 ✗** / 155✓                                                                | **MIXED** ✗                                                | Ph. 3   |
| `updates/mach-dependent-fragment-drag/checks/drag-anchor-validation.py:82`     | 75✓ / **105 ✗** / 155✓                                                                | **MIXED** ✗                                                | Ph. 3   |
| `updates/mach-dependent-fragment-drag/checks/long-range-residual-diagnosis.py` | 75✓ / **105 ✗** / 155✓                                                                | **MIXED** ✗                                                | Ph. 3   |
| `updates/mach-dependent-fragment-drag/checks/required-retardation-vs-mach.py`  | 75✓ / **105 ✗** / 155✓                                                                | **MIXED** ✗                                                | Ph. 3   |

The 75✓/105✗/155✓ pattern repeats verbatim across five scripts: the 105mm
series was copied from the pre-correction table in `initial-conditions-105mm.md`
while the 75mm and 155mm series came from correctly-identified sources. A single
`DATA` block therefore mixes two different criteria across its three entries —
the shape of the velocity-decay curve it fits is not one physical relation.

`initial-conditions-probe1.py` / `-probe2.py` read only `src/arty` state and
carry no source data — **not affected**.

### 3b. Inherited by import (no digit re-typed)

| artifact                                              | inherits from                        | verdict |
| ----------------------------------------------------- | ------------------------------------ | ------- |
| `drag-gap-1944/checks/b-vs-range-familyA.py:154`      | all three `b-vs-range-*mm` modules ✗ | Ph. 3   |
| `drag-gap-1944/checks/b-vs-range-familyA-aof-ap.py`   | `b-vs-range-familyA.py` ✗            | Ph. 3   |
| `drag-gap-1944/checks/b-vs-range-drag-attribution.py` | all three `b-vs-range-*mm` modules ✗ | Ph. 3   |

### 3c. Parameter-dependent, not table-dependent

These consume `DragParams` defaults whose *justification* is the tainted
velocity-decay comparison. They are only void if Phase 4 voids the parameter.

| artifact                                                                 | dependency                                       | verdict |
| ------------------------------------------------------------------------ | ------------------------------------------------ | ------- |
| `src/arty/fragmentation.py:184` — `C_D = 1.28`                           | justified on "1944 Ordnance velocity-decay data" | Ph. 4   |
| `updates/mach-dependent-fragment-drag/checks/r50-drag-anchor-shift.py`   | `C_D·C_shape` 0.585 → 2.674                      | Ph. 4   |
| `updates/mach-dependent-fragment-drag/checks/drag-update-demo-impact.py` | same                                             | Ph. 4   |
| `updates/mach-dependent-fragment-drag/checks/check5b-drag-spotcheck.py`  | same                                             | Ph. 4   |

`updates/wdss1-steel-grade/checks/recompute.py` touches neither source — **not
affected**.

### 3d. Narrative consumers (quote numbers, hold no arrays)

`drag-gap-1944/README.md` (the 7–34× and 1.9–5.3× ratio tables),
`b-vs-range.md`, `b-vs-range.qmd`, `b-vs-range-familyA.md`, `review.md`,
`initial-conditions-{75,105,155}mm.md`, `_validation.qmd` (Check 7),
`_limitations.qmd` (L3, #14 and its Family-A addendum), `challenges/README.md`
(drag-gap-1944 marked **Closed**), `_change-log.qmd`, `_governing-equations.qmd`,
`updates/mach-dependent-fragment-drag/{scoping,derivation}.md`. Listed for
Phase 6; none can be repaired before Phase 3 assigns verdicts.

## 4. Tolch-1938 consumers

Independent of the column question. The Tolch defect is different in kind: the
card's **"Drag Model Relevance"** section recommends the velocity-sweep density
collapse as the drag calibration anchor, and modeler memory
(`gotcha_tolch_remaining_velocity_is_shell_not_fragment`) records that the axis
is the *shell's* velocity at burst — a burst-geometry observable near-insensitive
to drag, i.e. the least drag-sensitive number in the report. The correction
lives only in agent memory; the card still says it. Every anchor in that card is
a bare line number, into a file that has already been partially re-extracted.

| artifact                                                                        | numbers consumed                                                                              | verdict |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------- |
| `drag-gap-1944/tolch-1938-panel-distance.md`                                    | Panel A (15 ft) → D (120 ft) density ratio 0.557; ~700–800 perforations/shell                 | Ph. 3   |
| `updates/mach-dependent-fragment-drag/checks/tolch-count-post-shape-closure.py` | same ratio + absolute counts, post-shape-closure Mott params                                  | Ph. 3   |
| `count-gap-1938/checks/count-chain-decomposition.py:49,53`                      | 15 ft = 4.572 m; counts normalised to 700 and 803                                             | Ph. 3   |
| `count-gap-1938/count-chain.md`                                                 | the 4–6× absolute over-prediction decomposition                                               | Ph. 3   |
| `mott-scale-gap/_scale_verdict_ledger.md`                                       | pit-test `N(>m)` at screen cuts; panel total ~5 000; mean recovered fragment 7 g ≈ 12×12×6 mm | Ph. 3   |
| `mott-scale-gap/_shape_closure_check.md`                                        | l₀ ≈ 10 mm vs Tolch ~12 mm; μ ≈ 0.95 g                                                        | Ph. 3   |
| `updates/mott-fragment-shape-closure/{scoping,derivation,review}.md`            | μ fits 3.46 g / 0.95 g bracket                                                                | Ph. 4   |
| `updates/frag-field-3d-geometry/scoping.md`                                     | narrative reference only                                                                      | Ph. 6   |
| `_limitations.qmd`                                                              | narrative reference only                                                                      | Ph. 6   |

Open for Phase 2: the cumulative velocity distribution the card flags
"UNVERIFIED, do not cite" — two extractions disagree, one is provably
non-monotonic, no source PDF retained in-repo. Capped at one re-acquisition
dispatch.

## 5. Open questions carried into Phase 1

- **The 105mm and 155mm casualties columns share identical `(m, v)` pairs** at
    matching ranges (`.010/2440`, `.014/2060`, `.019/1770`, …), differing only in
    `N` and `B` and in the last range step (500 vs 600 ft). Physically consistent
    — both shells list `V0 = 3,500 f/s` and the criterion is a fixed energy, so
    `m(v)` is shell-independent — but it should be confirmed against the scan
    rather than assumed, since a cross-copied column would look exactly like
    this. Their perforation columns coincide the same way.
- **155mm r=80 ft, casualties `B`** prints as `..0148` (stray leading dot) in the
    scan. Transcribed as `0.0148`; confirm.
- **75mm r=40** needs an explicit note in the re-transcription that the pair is
    in *normal* order, so the invented swap does not get re-applied.
