# Source-data audit ledger — ordnance-1944 and Tolch-1938

Provenance and verdict record for every artifact that consumes numbers from
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/` or
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/`.

Repairs are **deferred by design** — this ledger is the map that drives the
redo, not a record of fixes. `src/arty/` is assessed, never changed here.

| Phase                             | State                                             |
| --------------------------------- | ------------------------------------------------- |
| 0 — inventory & provenance        | **done** (this document, sections 1–4)            |
| 1 — re-baseline ordnance-1944     | **done** — six tables transcribed + verified (§5) |
| 2 — re-baseline Tolch-1938        | **2a–2c done** (§6); 2d card rewrite outstanding  |
| 3 — downstream verdict per thread | pending (verdict column below unfilled)           |
| 4 — `src/arty` assessment         | pending                                           |
| 5 — independent verification      | pending                                           |
| 6 — surface reconciliation        | pending                                           |

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

## 5. Phase 1 result — ordnance-1944 re-baselined

Six tables now live under
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/`,
each with a `.invariant` beside it. `uv run src/utils/check-table-invariants.py doc-reference/ --all` exits 0 — **0 / 6
failed**, 33 checks over 65 rows.

| table                          | rows | closure                               |
| ------------------------------ | ---- | ------------------------------------- |
| `75mm-m48-casualties`          | 10   | 58 ft-lb + 4 monotonic                |
| `75mm-m48-perforation-1-8in`   | 10   | 4 monotonic (identity by elimination) |
| `105mm-m1-casualties`          | 11   | 58 ft-lb + 4 monotonic                |
| `105mm-m1-perforation-1-8in`   | 11   | 4 monotonic                           |
| `155mm-m107-casualties`        | 11   | 58 ft-lb + 4 monotonic                |
| `155mm-m107-perforation-1-8in` | 12   | 4 monotonic                           |

Independently verified cell-by-cell against the scan by three separate
verification passes (one per shell page-block, comparison only — no editing, no
deciding): **315 cells checked, zero discrepancies.** The three open questions
carried into Phase 1 all resolved:

- The 105mm and 155mm casualties columns *do* share identical `(m, v)` pairs at
    matching ranges — confirmed against the scan, not a cross-copy. Both shells
    list `V0 = 3,500 f/s` and the criterion is a fixed energy, so `m(v)` is
    shell-independent; only `N`, `B` and the final range step differ.
- 155mm r=80 ft `B` prints as `..0148` (stray leading dot); `0.0148` confirmed.
- **75mm r=40 is NOT transposed.** The pair sits in normal first/second order
    like every other row, and closes at 57.5 ft-lb in first-line position. The
    swap that `b-vs-range-75mm.py` applies is an artefact of its own inverted
    column assignment and must not be carried forward.

The perforation tables have **no closure of their own** — the source states no
numeric perforation threshold, and `½mv²` on those rows runs 272–1146 ft-lb,
rising with range. Their identity rests on elimination against the casualties
table, which is only sound while both halves of each pair stay transcribed
together. Each `.invariant` says so, and says explicitly that the monotonicity
checks are structural sanity only and can never serve as a column-identity test
— that misuse is what inverted three committed scripts.

## 6. Phase 2 result — Tolch-1938

Evidence: [`checks/tolch-spray-table-closure.py`](checks/tolch-spray-table-closure.py)

**2c — the "UNVERIFIED, do not cite" figure is RESOLVED, and no re-acquisition
dispatch was needed.** The card treats the cumulative base-fragment velocity
distribution as an unreadable *measurement* with two irreconcilable extractions.
It is not a measurement: the report states it is *derived* — "The proportion of
base fragments remaining after giving the shell an increment in velocity may be
obtained from the above table" (anchor: `**Total hits per unit solid angle of the base spray.**`). Recomputing it from the Panel A totals column settles it:

| v (f/s) | derived from table | heuristic reading | vision reading |
| ------- | ------------------ | ----------------- | -------------- |
| 700     | 79.8 %             | 80 %              | 20 %           |
| 1085    | 48.0 %             | 48 %              | 15 %           |
| 1450    | 28.7 %             | 29 %              | 25 %           |
| 1685    | 13.9 %             | 14 %              | 18 %           |
| 2130    | 7.2 %              | 7 %               | 7 %            |

The heuristic reading reproduces the table to 0.3 pp; the vision reading is off
by up to 59.8 pp. **The heuristic reading is correct** and the figure is
citable: 80 % > 700, 48 % > 1085, 29 % > 1450, 14 % > 1685, 7 % > 2130 f/s. The
Phase 2c dispatch budget is unspent.

Caveat that must go in the card: these are ***shell*** remaining velocities. The
quantity is the fraction of base fragments whose charge-imparted velocity
exceeds the shell velocity cancelling it — burst geometry, **not** fragment drag.

**2b — RESOLVED against the original scan. The corrupted copy was
`tolch-1938.md`, not the source.** The user supplied the original DTIC PDF
(AD0702233, `sha256:13e110d7…`), now retained in-repo at
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/source.pdf`
(gitignored blob, provenance recorded in the card).

Read off the page images of report pages 19–22 (PDF pages 41–44), both spray
tables close **exactly**:

| Table      | Cells | Fail | Largest residual |
| ---------- | ----- | ---- | ---------------- |
| Base spray | 17    | 0    | 0.00             |
| Nose spray | 17    | 0    | 0.01             |

Not one cell of genuine disagreement: 33 of 34 sum to the printed 2 d.p. with
zero residual, the 34th (nose Panel C @ 700 f/s) by 0.01 of rounding. **All 21
earlier "failures" were OCR defects in `tolch-1938.md`** — roughly 20 of its 54
component cells are wrong. The worst are not subtle:

| Cell                        | `tolch-1938.md` | Actual page |
| --------------------------- | --------------- | ----------- |
| Nose static Panel A, penet. | 0.37            | **3.47**    |
| Nose static Panel A, dents  | 1.22            | **12.25**   |
| Base 2130 Panel B, total    | 3.12            | **1.12**    |
| Nose 700 Panel B, dents     | 2.77            | **7.97**    |
| Base static Panel A, perf.  | 1.62            | **1.82**    |

Transcribed once to
[`tables/base-spray-density.csv`](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/base-spray-density.csv)
and
[`tables/nose-spray-density.csv`](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/nose-spray-density.csv),
each with its `.invariant`; `check-table-invariants.py` reports 0/2 failed.

**The earlier speculation is withdrawn.** This ledger previously reasoned that
nose Panel A static might truly be 1.96, making the static→2130 rise 10.9×
rather than the card's 1.33×, and noted the ±0.20 quantisation as evidence. The
page shows **16.09**. The card's 1.33× is correct, and the ±0.20 pattern was
coincidence in corrupted data — a reminder that a pattern found *inside* a
failing table is not evidence about the source. Declining to decide it without
the scan was the right call.

**2d — the card's "Drag Model Relevance" section is confirmed wrong.** The
source is explicit that "remaining velocity when burst" is the *shell's*
velocity, tabulated as a firing condition ("the following table shows the
conditions under which the rounds were fired… Average remaining velocity when
burst"). The base-spray density collapse against it is vector addition of shell
velocity and charge-imparted ejection velocity — burst geometry, near-insensitive
to fragment drag. The card recommends it as *the* drag calibration anchor. This
matches the modeler-memory gotcha
(`gotcha_tolch_remaining_velocity_is_shell_not_fragment`), whose correction never
reached the card.

**Anchor rot confirmed and worse than recorded.** The card cites the spray
tables at `tolch-1938.md` lines 553–684. Those lines now hold panel-layout OCR
garbage; the real tables sit at **813–965**, roughly 250 lines away. Every anchor
in that card is a bare line number.

## 7. Why the extraction was wrong — pipeline diagnosis

Evidence: [`checks/vision-provider-probe.py`](checks/vision-provider-probe.py)

The Tolch table errors are **not** a model-reasoning failure, **not** a
resolution failure, and **not** a consequence of using a free/small model. The
single cause is `pdf-processor.py:_render_pages_combined` **stacking multiple
pages into one tall image**, which the API downscales server-side.

Probed against the live API on the page whose ground truth is now committed —
the base-spray `Perf.` block, 18 cells:

| configuration                      | cells correct |
| ---------------------------------- | ------------- |
| single page, dpi 60 (Gemma)        | **18 / 18**   |
| single page, dpi 200 (Gemma)       | **18 / 18**   |
| single page, dpi 60 (Gemini Flash) | **18 / 18**   |
| 3-page stack, dpi 60               | 16 / 18       |
| **8-page stack, dpi 60 (shipped)** | **5 / 18**    |

**The 8-page stack reproduces the historical error exactly.** It returns `1.62`
for Static Panel A — the precise wrong value in the committed `tolch-1938.md` —
and misreads the row label `1685` as `1665`. A reproduction, not an inference.

Two hypotheses are therefore **refuted**:

- *"dpi=60 is too low."* It is not. 60 dpi single-page is perfect. Raising dpi
    fixes nothing, and combined with stacking makes it **worse** — a taller
    image is downscaled harder. An earlier revision of
    [`checks/vision-raster-resolution.py`](checks/vision-raster-resolution.py)
    argued the opposite; it is retained, corrected, as the measurement it is.
- *"the free Gemma model is too weak."* It is not. `gemma-4-31b-it` matches
    `gemini-3.5-flash` cell-for-cell at 18/18. The cost-saving design is sound;
    only the batching parameter is wrong.

**The failure mode is fabrication, not garbling.** The 8-page stack returned a
smooth, plausible, monotonically-decaying column (`.56, .42, .33`) where the
source prints `.24, .34, 0`. Likewise `tolch-1938.md` fills the Panel C row at
1450 f/s — printed as **dashes**, no data — with `.12 / .04`, the 1685 row's
values pulled up a line. Under-resolution does not make the model refuse; it
makes it interpolate, confidently, with no marker.

**The extraction-quality gate cannot see any of this, by construction.**
`scan-extraction-quality.py` is glyph-level — PUA characters, symbol runs,
short-token ratio. A vision model under-resolved does not emit garbled glyphs;
it emits a *clean, correctly-aligned markdown table* containing wrong numbers.
Running the gate on `tolch-1938.md` flags it — but only for symbol-run noise on
lines 349/1187/1296/1449, elsewhere in the document. The corrupted table itself
is glyph-perfect and passes every heuristic the tool has.

This is the structural reason the closure invariant is the only real gate:
**glyph-level checks catch bad OCR, and the vision path does not fail as bad
OCR — it fails as plausible fiction.**

**Two credential findings, both silent.**

- `.env` exists **only in the primary checkout**. `settings.py` loads it from
    the repo root, so every worktree resolves *zero* credentials — and
    `git-flow.md` mandates that all work happen in a worktree. A librarian
    dispatched the normal way has no keys at all.
- There is **no `ANTHROPIC_API_KEY`** configured. So the
    `except → "falling back to Anthropic"` path in `pdf-processor.py:604` does
    not degrade to an expensive fallback, as this ledger previously suggested —
    it degrades to a hard `"No AI credentials found"` error. Correct outcome,
    reached by accident, and it would silently become a real cost the day a key
    is added. Provider choice must be an explicit setting, not an exception
    handler.

The reported intermittent `403` was **not reproduced**; the configured key
lists 42 usable models and `gemma-4-31b-it` answers normally. A stale model ID
does surface as `404` (`gemini-2.5-flash` is retired for new keys), so at least
some historical failures were model-availability, not authorisation.

## 8. Remaining work

- **Phase 2d** — rewrite the Tolch `card.md`: drop the wrong "Drag Model
    Relevance" recommendation, move every anchor off bare line numbers, record
    the source PDF's provenance (DTIC AD0702233 + sha256), and link the CSVs.
- **`tolch-1938.md` is a known-corrupted extraction** and is now the *second*
    citable surface after `tables/`. Either re-extract it from `source.pdf` or
    mark it non-citable; any consumer reading numbers out of it is unsafe.
- **Phase 3** — downstream verdicts (§3, §4 verdict columns).
- **Phase 4** — `src/arty` assessment (§3c).
- **Phase 5** — independent verification of this ledger.
- **Phase 6** — surface reconciliation (§3d).
