# Source-data audit ledger — ordnance-1944 and Tolch-1938

Provenance and verdict record for every artifact that consumes numbers from
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/` or
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/`.

Repairs are **deferred by design** — this ledger is the map that drives the
redo, not a record of fixes. `src/arty/` is assessed, never changed here.

| Phase                             | State                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| 0 — inventory & provenance        | **done** (this document, sections 1–4)                                                      |
| 1 — re-baseline ordnance-1944     | **done** — six tables transcribed + verified (§5)                                           |
| 2 — re-baseline Tolch-1938        | **2a–2c done** (§6, incl. 2b's missed third table); 2d card rewrite blocked on Ph. 8 item 2 |
| 2.5 — source admissibility gate   | **2.5a closed** (§15, §16); 2.5b–d open, still block 3 and 5                                |
| 3 — downstream verdict per thread | **blocked on 2.5** (verdict column below unfilled)                                          |
| 4 — `src/arty` assessment         | **1944 drag law done** (§8); **unblocked** — 2.5a closed (§16e)                             |
| 5 — independent verification      | **blocked on 2.5 and 3**                                                                    |
| 6 — surface reconciliation        | pending                                                                                     |

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

**2b, second sitting — the SIDE-spray table was missed the first time, and is
now re-baselined too.** Phase 2b called for one dispatch per spray class; only
base and nose reached `tables/`. The side spray — the table the
`mach-dependent-fragment-drag` update actually consumes, via the Panel A→D
perforation ratio — survived as a hand-typed literal inside two check scripts,
typed off the garbled `pdftotext` layer. Extracted through the fixed
single-page vision path (§7) from source.pdf pp.39–40 (report pages -17-, -18-)
to
[`tables/side-spray-density.csv`](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/side-spray-density.csv):

| Table      | Cells | Fail | Largest residual |
| ---------- | ----- | ---- | ---------------- |
| Side spray | 20    | 0    | 0.00             |

**All 20 cells close exactly**, so the blocking finding that the series fails
its closure at v = 1085 f/s is **resolved as a transcription error, not a
source defect.** The literal put that row's totals at 4.26 / 3.56 / 1.90; the
page prints 4.06 / 3.42 / 1.96 — exactly the component sums. It also recorded
Panel D @ 700 f/s penetrations as illegible; the page prints 0.49. Same shape
as the incident this audit exists for, one table over: a series re-typed
instead of read once.

Three independent cross-checks on the perf column beyond the row sums, all
passing: the source's own stated A→D perforating losses (44 / 19 / 33 %,
"averaging 32 %") reproduce at 44.3 / 19.2 / 33.3 %, mean 32.3; its stated
total-hit loss "about 57 %" reproduces at 56.4 %; and `RATIO_OBS = 0.557`
reproduces at 0.5570. Both check scripts now read the CSV — no hand-typed
array remains in either.

**The pit screen table is recorded too, and it sharpens the 803-vs-779
finding.** Same situation: cited by the update, never extracted, held as a
literal with the screen-4 count marked illegible. Now at
[`tables/pit-screen-recovery.csv`](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/pit-screen-recovery.csv)
off source.pdf p.10 (report page -6-), with the screen-4 count legible at 142.
Its invariant is four-fold — the counts sum to the printed 779, both
percentage columns reproduce from the counts and weights against bases the
source states, and all four column totals close.

That makes the count question decisive rather than suggestive. The earlier
literal could only test two screen rows against 803; the full table tests
five, and **four of them fail their printed percentage under 803** (by 1.03,
0.94, 0.52 and 0.45 pp) while **all five close under 779** (worst residual
0.05 pp). The finding stands, with stronger evidence.

Shell identity was checked before recording, since the pit table's own heading
reads "75 mm T3 Shell": the report is titled "FRAGMENTATION EFFECTS OF THE
75MM H.E. SHELL T3 (M48)" and T3 is the M48's developmental designation, not a
different projectile. The 105 mm M1 results are "reserved for a separate
report". No criterion mismatch.

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

## 8. Phase 4 result — the two shipped drag conclusions

Full assessment: [`phase4-drag-law-assessment.md`](phase4-drag-law-assessment.md).
Evidence: [`checks/drag-law-recheck-corrected-column.py`](checks/drag-law-recheck-corrected-column.py).

That script reproduces the shipped derivation's V2 numbers digit-for-digit when
run on the old mixed row set, so every difference it reports is the column
correction and not method drift.

| claim                                                                                                          | verdict        | note                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `C_D = 1.28` / `C_shape = 2.0890`, `src/arty/fragmentation.py`                                                 | **SOUND**      | bar still passes (RMS M>0.7 0.092 → 0.096); parameter is source-anchored to TP-12's *k* = 2600, never fitted to the 1944 set |
| rejection of Mach-dependent $C_D$ (`updates/mach-dependent-fragment-drag` §5)                                  | **SHIFTED**    | conclusion stands on §5's structural-cost argument; its *accuracy* evidence does not survive                                 |
| §3c parameter-dependent scripts (`r50-drag-anchor-shift`, `drag-update-demo-impact`, `check5b-drag-spotcheck`) | **not voided** | they consume `C_D·C_shape`, which is unchanged                                                                               |

**No `src/arty/` value changes.** Both required corrections are text: derivation
§4 V2's cited RMS pair (0.349 / 0.092 over 25 mixed points → 0.405 / 0.096 over
32 casualty points), and the false "does not beat this constant" claim carried
in both §5 and the `DragParams` comment. Phase 6 surface edits, not Workflow B.

### 8a. Separate finding — §5's comparison is not reproducible, and never was

Logged apart from the verdict above **because the column error did not cause
it.** Derivation §5 compares a zero-free-parameter Fig-3 run against a
one-free-parameter best constant and concludes the Mach law "does not beat"
the constant. Given equal freedom the Fig-3 law scores 0.201 / 0.034 against
the constant's 0.250 / 0.047 — it *did* beat it, on the very data §5 cites.

This is a pre-existing methodological defect that this audit surfaced
incidentally. A reader tracing *what the column inversion broke* must not be
handed it as one of the casualties; a reviewer re-running §5 must not miss it
either. On the corrected data the two laws are indistinguishable — every
margin sits inside the ±10% fidelity bar and inside the digitized Fig-3's own
±0.02 read uncertainty.

## 9. Remaining work

- **Phase 2b is complete as of the second sitting** (§6). All four Tolch
    tables any consumer cites now sit in `tables/` with a passing invariant:
    base spray, nose spray, side spray, pit screen recovery. The first sitting
    covered only two of the three spray classes, and the omission is what let a
    hand-typed literal stand in for the side-spray series.
- **Phase 2d** — rewrite the Tolch `card.md`: drop the wrong "Drag Model
    Relevance" recommendation, move every anchor off bare line numbers, record
    the source PDF's provenance (DTIC AD0702233 + sha256), and link the four
    CSVs. **Blocked on Phase 8 item 2** (splitting the interpretive half out of
    `card.md`) — rewriting the card before that split just re-authors the
    interpretive section in the place the split is meant to empty.
- **`tolch-1938.md` is a known-corrupted extraction** and is now the *second*
    citable surface after `tables/`. Either re-extract it from `source.pdf` or
    mark it non-citable; any consumer reading numbers out of it is unsafe.
- **Phase 3** — downstream verdicts (§3, §4 verdict columns).
- **Phase 4b** — the two shipped Tolch-1938 updates (§4); the 1944 drag law is
    settled in §8. Source-side groundwork is closed and two defects are
    registered in §10; the verdict layer is outstanding and **escalated** after
    three dispatches — see `phase4b-tolch-mach-drag-assessment.md`
    "Dispatch history" before spending a fourth.
- **Phase 5** — independent verification of this ledger.
- **Phase 6** — surface reconciliation (§3d).

## 10. Registered findings

Repairs are deferred by design in this audit, which is exactly the condition
`.claude/rules/deferred-findings.md` exists for. The markers below put each
deferred item into `OPEN-FINDINGS.md`, so the pass that eventually touches one
of the named paths is briefed with it instead of rediscovering it.

They are recorded *here*, not in the affected files, because this audit's scope
forbids editing `src/arty/` and the downstream artifacts — `affects:` does the
routing, so a marker never has to sit in a file the pass may not touch.

FINDING\[blocking\]: Fig-3 Mach drag is claimed not to beat the constant C_D on the 1944 data; false on both old and corrected columns, and the comparison gave the constant a free parameter the Fig-3 run did not have (affects: src/arty/fragmentation.py, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md; since: 2026-08-02)

FINDING\[blocking\]: derivation §4 V2 cites velocity-decay RMS 0.349 / 0.092 from a 25-point set that mixed casualties and perforation rows; the all-casualties figures are 0.405 / 0.096 over 32 points (affects: experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md; since: 2026-08-02)

FINDING\[blocking\]: B-vs-range check scripts read the perforation-of-1/8-in-mild-steel column while applying the 58 ft-lb casualty criterion, and hand-type the series instead of reading tables/\*.csv (affects: experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-75mm.py, experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-105mm.py, experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-155mm.py, experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-familyA.py, experiment/fragmentation-field/challenges/drag-gap-1944/checks/drag-coefficient-calibration.py; since: 2026-08-02)

FINDING\[blocking\]: card.md's "Drag Model Relevance" section recommends the velocity-sweep density collapse as the drag calibration anchor, but that axis is the shell's velocity at burst — a burst-geometry observable, near-insensitive to fragment drag (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md; since: 2026-08-02)

FINDING\[blocking\]: tolch-1938.md is a known-corrupted vision extraction (page-stacking defect, §7) yet remains a citable surface alongside tables/; it must be re-extracted or marked non-citable (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md; since: 2026-08-02)

FINDING\[deferrable\]: the cumulative fragment-velocity distribution is unresolved — two extractions disagree and one is provably non-monotonic; no better scan surfaced within the one-dispatch cap (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md; since: 2026-08-02)

FINDING\[blocking\]: the pit-test recovered-fragment count is 803 in committed artifacts but the report's own screen table (now at tables/pit-screen-recovery.csv, where 4 of 5 screen rows fail their printed percentage under 803 and all 5 close under 779) and body text both say 779, which shifts the derived mean fragment mass 6.85 g -> 7.06 g and the update's N/observed band 3.9-5.6x -> 3.75-6.00x (affects: experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/scoping.md, experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md; since: 2026-08-02)

## 11. Sweep of the rest of `doc-reference/` (Phase 8 item 3)

The audit was scoped to two sources on the assumption the other 21 processed
documents are unaffected. That assumption is now tested, not assumed.

Criterion: a document is exposed if some committed artifact reads *numbers*
out of it (not merely points at it) and it has no `tables/*.csv` with a passing
invariant. Four qualify:

| Document                                           | Numbers reach                                            | Source form       |
| -------------------------------------------------- | -------------------------------------------------------- | ----------------- |
| `fragmentation/dod-1975-fragment-debris-hazards`   | **`src/arty/fragmentation.py`** + 7 artifacts            | scanned DoD TP-12 |
| `ww2-shells/ammunition-series-6-wdss-specs`        | `updates/wdss1-steel-grade/` incl. `checks/recompute.py` | printed manual    |
| `ww2-shells/ammunition-series-6-steel-composition` | `updates/wdss1-steel-grade/` scoping + review            | printed manual    |
| `azom-steel-grades/aisi-1335`                      | `updates/wdss1-steel-grade/` incl. `checks/recompute.py` | web article       |

`wound-ballistics/aep-55-vol3` is cited only in one `scoping.md` and carries no
`card.md`; narrative-only, so not exposed. `aisi-1020` and `aisi-1045` are
uncited.

**None of the four retains its source.** `tolch-1938.../source.pdf` is the only
PDF in `doc-reference/`. So these tables *cannot* be re-baselined the way the
Tolch tables just were — the only surviving copy is the extracted markdown,
which is the artifact whose fidelity is in question. Transcribing a CSV out of
it would launder an unverified extraction into an apparently-checked one, which
is worse than leaving it visibly unchecked. **Re-acquisition comes first**;
that is the finding, and it is why nothing was extracted here.

What the sweep *could* check cheaply, and did: whether the two constants
DoD-1975 puts into shipped code still read as claimed. `_K_BALLISTIC = 2600.0`
and `C_D = 1.28` are cited at `10-F-0806_Fragment_and_Debris_Hazards.md` lines
316 / 321 / 338-339. All three lines currently resolve and say what
`fragmentation.py` says they say ("the average value of 660 grains/in.3 (2.60
g/cm3) has been recommended"; "take the drag coefficient as constant at its
supersonic value of 1.28"). **The numbers are right today.** But they are bare
line numbers in shipped code — the anchor form
`.claude/rules/source-data-fidelity.md` forbids, because it fails silently: a
re-extraction moves them and the reader lands on different text that looks
right. This is the same rot that moved the Tolch card's anchors ~250 lines
(§6). Both are scalars quoted from prose, not table cells, so the
extract-once rule does not apply to them — only the anchor rule does.

FINDING\[deferrable\]: shipped code cites DoD-1975 by bare line number (lines 316, 321, 338-339) for \_K_BALLISTIC and C_D; the lines resolve correctly today but rot silently on any re-extraction — replace with greppable strings (affects: src/arty/fragmentation.py, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md; since: 2026-08-02)

FINDING\[deferrable\]: three doc-reference documents feed numbers into committed artifacts with no tables/\*.csv and no retained source PDF, so they cannot be re-baselined without re-acquisition (dod-1975 was the fourth and is now closed — scan retained, tables written, see §13) (affects: doc-reference/ww2-shells/ammunition-series-6-wdss-specs/, doc-reference/ww2-shells/ammunition-series-6-steel-composition/, doc-reference/azom-steel-grades/aisi-1335/; since: 2026-08-02)

## 12. The 1944 source scan, recovered — column identity checked at the page

The user supplied the original scan (`p4013coll8_2373.pdf`, 105 pp.,
sha256 `bd97d4ee…`), retained at
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/source.pdf`
(gitignored blob, per `.gitignore doc-reference/**/*.pdf`, same convention as
Tolch). The three shells sit on pdf pages 84 / 89 / 93 = report pages 70 / 75 /
79\.

This closes the largest open gap in the audit. Phase 1 (§5) re-baselined the six
tables off the **merged markdown** `ordnance-1944.md` — an artifact in which the
two side-by-side tables have already been flattened into a linear reading order,
i.e. one that no longer carries the geometry distinguishing them. Column
identity there rested on the 58 ft-lb energy closure plus elimination for its
partner. Sound, but indirect, and it could not confirm the one thing the
incident turned on: *which half of the page a value is actually printed on.*

### 12a. Result — the Phase 1 re-baseline is confirmed, cell for cell

All three pages render cleanly at 200 dpi and were read directly. **All 322
cells across the six CSVs reproduce the page images exactly.** No correction of
any kind was needed. Column identity is unambiguous and no longer inferred: each
page prints `TABLE nn / CASUALTIES` above the left table and
`TABLE nn+1 / PERFORATION OF 1/8 IN. MILD STEEL` above the right one.

[`checks/ordnance-1944-page-geometry.py`](checks/ordnance-1944-page-geometry.py)
makes this re-checkable **without vision** and without trusting reading order:
it splits each page by the x-coordinate of every word and asserts that every
discriminating value in a CSV is physically printed on the half whose caption
names its criterion. Zero cells appear on the wrong half; 97–100% of
discriminating cells are found on their own half, the shortfall being OCR
damage in the text layer, not disagreement. Runtime 0.17 s.

The six `.invariant` files now carry `source: ../source.pdf p.NN` and greppable
`TABLE nn` / caption anchors in place of the pointer to the derived markdown.

### 12b. A closure the page images made available

The 105 mm M1 and 155 mm M107 share `INITIAL FRAGMENT VELOCITY 3,500 F/S`, and
`(m, v)` — the lightest fragment still meeting the criterion at range `r` — is a
single-fragment ballistics result independent of shell size. So the two shells'
tables, typeset four pages apart, should print the same `(m, v)` at the same
range. **They do**, on all 11 shared perforation ranges and 8 of 10 shared
casualties ranges. The 75 mm (3,120 f/s) correctly differs from both.

The two exceptions are the source's own, not ours. At r = 300 ft the 105 mm
prints `0.166 oz / 598 f/s` against the 155 mm's `0.161 / 598`; at r = 400 ft,
`0.232 / 507` against `0.233 / 505`. Both were re-read at **500 dpi** and both
transcriptions are faithful. The 155 mm r=300 row is the weakest energy closure
in the whole six-table set — 55.9 ft-lb, −3.6% from the stated 58, against −0.6%
for the 105 mm reading of the same range. Both pass the 5% band. A consumer
weighting rows by closure quality should prefer the 105 mm value there. The
divergence is pinned in the check rather than smoothed over, so a future
re-extraction that "fixes" one to match the other fails instead of passing.

### 12c. Blocking — `card.md` still carries the defect that caused the incident

Verifying against the scan exposed that **`card.md` was never rewritten** (the
Phase 1 card step, §5, did the CSVs but not the card). It still carries both
halves of the original failure mechanism, now confirmed against the original
pages rather than inferred:

**Every table number in it names a different shell.** Each page of this report
holds one shell's `(casualties, perforation-1/8)` pair, and consecutive pages
are consecutive shells — so a wrong table number lands on an identically
formatted table for another projectile, which is exactly why it survived:

| `card.md` heading                   | That table actually is                | The card's numbers are really from |
| ----------------------------------- | ------------------------------------- | ---------------------------------- |
| `Table 43: 75-mm H.E. Shell, M48`   | 81 mm M43A1, V₀ 3,930 f/s (p.86)      | Tables 38/39 (p.84)                |
| `Table 51: 105-mm H.E. Shell, M1`   | 105 mm **M38A1**, V₀ 3,320 f/s (p.90) | Tables 48/49 (p.89)                |
| `Table 59: 155-mm H.E. Shell, M107` | 8 in. M103, V₀ 2,500 f/s (p.94)       | Tables 56/57 (p.93)                |

The 105 mm case is the nastiest: Table 51 is a *different 105 mm shell*, so the
label is wrong in a way that reads as right.

**And its `Distance Range` field is the other table's range.** For each shell
the card prints a casualties `B` value beside a range taken from the
*perforation* table — 75 mm "20–225 ft" (casualties runs to 400), 105 mm
"20–300 ft" (casualties runs to 500), 155 mm "20–400 ft" (casualties runs to
600). This is verbatim the mechanism the audit was opened on: one column's value
beside another column's range, in a lossy summary that a check script then used
as the column-identity discriminator.

The card's *quoted numbers* are all correct for the shells it means (B = 0.213 /
0.231 / 0.291 at 20 ft; V₀ 3,120 / 3,500 / 3,500). The labels around them are
not. Consistent with this audit's deferred-repairs scope the card is **not
rewritten here**, but per `.claude/rules/deferred-findings.md` a published
artifact known to carry wrong labels cannot be closed by deferral — it is marked
**blocking** and surfaced. The corrections above are exact and verified, so the
rewrite (which Phase 8 item 2 will do anyway, when it splits the card into
mechanical-inventory and interpretive halves) is mechanical.

Its nine anchors are also all bare line numbers (`ordnance-1944.md#L261`,
`#L340-L369`, …) — the form `.claude/rules/source-data-fidelity.md` forbids, and
the form that rotted onto the wrong shell's data in the original incident.

FINDING\[blocking\]: ordnance-1944 card.md labels all three shell sections with the table number of a neighbouring shell (43→81mm M43A1, 51→105mm M38A1, 59→8in M103; correct are 38/39, 48/49, 56/57) and prints each casualties B value beside the perforation table's range — the exact lossy-summary mechanism that caused the column inversion; quoted numbers are correct, labels are not (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md; since: 2026-08-02)

FINDING\[deferrable\]: ordnance-1944 card.md cites all nine of its anchors as bare line numbers into ordnance-1944.md, the anchor form source-data-fidelity.md forbids; replace with greppable strings when the card is split (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md; since: 2026-08-02)

## 13. The DoD-1975 scan, recovered — the digitized Figure 3 does not match it

The user supplied the original (`10-F-0806_Fragment_and_Debris_Hazards.pdf`,
42 pp., sha256 `9ff9e66f…`), retained at
`doc-reference/fragmentation/dod-1975-fragment-debris-hazards/source.pdf`.
This is the source §11 flagged as the priority re-acquisition, because it is the
only one of the four un-baselined documents whose numbers reach shipped
`src/arty/` code.

### 13a. Both shipped constants are confirmed, and now close against a third

`src/arty/fragmentation.py` takes two scalars from this report's "Ballistic
Properties" section. Read off the retained scan, both are verbatim right:

- **pdf p.17** — "for forged steel projectiles and fragmentation bombs the
    average value of 660 grains/in.3 (**2.60 g/cm3**) has been recommended,
    while for demolition bombs the value 590 grains/in.3 (2.33 g/cm3) has been
    applied". `_K_BALLISTIC` = 2600 kg/m³ is the first of those.
- **pdf p.18** — "A useful approximation for many applications is to take the
    drag coefficient as constant at its **supersonic value of 1.28**."

Each had been quoted from a *different sentence*, with nothing tying them
together. The scan supplies the tie: **pdf p.19** prints the formula
`L = 2(k²m)^(1/3)/(C_D ρ)` *and* the number it yields — "For k = 2.6 g/cm3 and
CD = 1.28, we find that L1 = 247 m/kg^(1/3) in air at standard conditions". With
`L = L₁ m^(1/3)` that reduces to `L₁ = 2 k^(2/3)/(C_D ρ)`, a closure the two
shipped constants must satisfy jointly. They do: 241.2 against the stated 247,
−2.4%, the residual being the report's unprinted ρ (247 implies ≈1.196; ICAO
standard is 1.225).

The discriminating power is the point. Substituting the *demolition-bomb* value
printed in the same sentence — k = 2.33 g/cm³, exactly the adjacent-value
confusion this audit exists to catch — gives 224.2, **−9.2%**, four times
outside the band. Recorded as
`tables/ballistic-constants.csv` + `.invariant`; the extraction at
`10-F-0806_Fragment_and_Debris_Hazards.md` was checked against the page for all
three passages and is faithful.

### 13b. `figure-3-digitized.md` is wrong through the transonic rise — blocking

That file is an eyeballed reading ("curve traced by eye at grid
intersections"). Its 14-point (Mach, C_D) table was **hand-copied** into
`updates/mach-dependent-fragment-drag/checks/required-retardation-vs-mach.py:29`
— a transcribe-once violation — and that check is what **rejected** a
Mach-dependent drag law in favour of the constant `C_D = 1.28` now shipped.
So an eyeball reading of a 1975 scan is load-bearing for a shipped modelling
decision, and until now nothing had compared it back to the page.

It also contradicts `card.md` **in its own folder**: the card says the
transonic rise runs "from 1.08 to ~1.27" over Mach 0.7–1.0 and peaks near
Mach 1.5; the table says C_D = 1.14 at Mach 1.0 and peaks at Mach 1.4. Two
artifacts from one figure, disagreeing by ~0.13.

`checks/dod-1975-figure-3-trace.py` settles it by tracing the curve's black
stroke off a 300-dpi render, independent of both. Its axis calibration is
validated on three features read back out of the trace: supersonic plateau
**1.2801** (the source states 1.28), subsonic plateau **1.0788** (card: ~1.08),
peak **1.4003 at Mach 1.46** (card: ~1.40 near Mach 1.5). A calibration that
reproduces all three to 0.001 is not plausibly wrong in the band between them —
and the card, not the table, is what it confirms.

| Mach | `figure-3-digitized.md` | traced stroke | error      |
| ---- | ----------------------- | ------------- | ---------- |
| 1.0  | 1.14                    | 1.222–1.243   | **−0.082** |
| 1.2  | 1.38                    | 1.347–1.355   | +0.025     |
| 1.6  | 1.35                    | 1.388–1.394   | −0.038     |
| 1.8  | 1.33                    | 1.364–1.368   | −0.034     |
| 2.2  | 1.30                    | 1.320–1.324   | −0.020     |

The nine other points are inside the stroke. The defect is one-directional
where it matters: the published table **under-states** C_D across Mach 1.0–2.2,
by 7% at Mach 1.0. It misplaces the whole transonic rise, putting it between
Mach 1.0 and 1.2 where the page puts it between 0.75 and 1.15, and it peaks
0.06–0.1 Mach early.

**Why this is blocking, not deferrable.** Mach 0.8–2.2 is precisely the band
the 1944 arrival velocities populate (2440 f/s → Mach 2.2 at r = 20 ft, down
through Mach 1 near r ≈ 150 ft). The rejected candidate is a *Mach-dependent*
law, so the rejection test was fed a curve that is too flat exactly where the
data lives, and too flat in the direction that weakens the candidate. Whether
the rejection survives the corrected curve is a modelling question for the
Phase 3/4 @modeler passes — this ledger records only that the input was wrong
and in which direction. It compounds, rather than duplicates, the finding at
§11 that the same comparison mixed casualties and perforation rows.

The corrected curve is recorded at `tables/figure-3-drag-coefficient.csv`
(140 rows at 0.05 Mach, midpoint plus both stroke edges), emitted by the trace
script itself rather than typed, with `figure-3-drag-coefficient.invariant`
pinning the source-stated plateau. `figure-3-digitized.md` is **not** rewritten
here, per the deferred-repairs scope — it is marked blocking and the trace
script pins the exact discrepancy, so a partial re-digitization fails rather
than passing quietly.

The blocking marker for this one lives in `figure-3-digitized.md` itself rather
than here — a reader who opens that table must see it, which is the whole point
of `.claude/rules/deferred-findings.md`.

FINDING\[deferrable\]: dod-1975 card.md cites its passages as bare line ranges (L293-L315, L320-L327, L346, L550), the anchor form source-data-fidelity.md forbids; the page numbers are now known (pdf pp.17-19, figure p.33) so the replacement is mechanical (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md; since: 2026-08-02)

## 14. Phase 2.5 — the source admissibility gate

Added after §13, because §13 refuted the assumption the audit was scoped on.

This audit was opened on two sources on the premise that the rest of
`doc-reference/` was unaffected. DoD-1975 was the first other document anyone
looked at, and it carried a wrong number into shipped code by exactly the
mechanism of the original incident: a lossy derived artifact
(`figure-3-digitized.md`, read by eye) treated as ground truth, hand-copied
into a check script, and never compared back to the page. Three sources, three
independent defects, three for three. **Twenty documents remain unexamined.**

**The gate.** No @modeler or @model-reviewer pass begins while a source it will
read is inadmissible. Dispatching the modeler to adjudicate physics on top of
unverified data reproduces the original failure one level up — it manufactures
a verdict that *looks* independent and is not. This is the same principle that
put Phase 7/8 (workflow fixes) ahead of re-running corrupted work, applied to
the data rather than the tooling.

### 14a. Tiering — what gets a full re-baseline and what gets a sweep

Ranked by how far a wrong number travels. Counts are files citing the document
by folder name.

| Tier  | Documents                                                                                                                                                                                | Reaches                                      | Treatment                                             |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------------- |
| **1** | `ordnance-105mm-m1-1940` (`fragmentation.py:36`), `explosion-fragment-model` (`fragmentation.py:101`)                                                                                    | **shipped `src/arty/`**                      | full re-baseline; **blocks Phases 3, 4, 5**           |
| **2** | `gurney-equations-fragmentation` (1 script, 8 md), `aisi-1335`, `ammunition-series-6-wdss-specs`, `sandia-sand92-0243`                                                                   | committed check scripts → published verdicts | full re-baseline; blocks only the threads citing them |
| **3** | `fas-es310-damage-criteria`, `fragment-size-distribution-conwep`, `ada462991-fragment-velocity`, `britishartillery-wt-of-fire`                                                           | a rendered `.qmd`, no script                 | 14c/14d sweeps only                                   |
| **4** | `aep-55-vol3`, `ammunition-series-6-steel-composition`, `aisi-1020`, `aisi-1045`, `cunniff-2014`, `lethality-threshold-critique`, `pmc7295711-bone-fragments`, `m49a2-60mm-mortar-shell` | one narrative mention each                   | 14c/14d sweeps only                                   |
| —     | `ml-warhead-fragmentation`, `nwc-tp-7124`                                                                                                                                                | uncited                                      | nothing depends on them                               |

**None of Tiers 1–4 had a `tables/*.csv` or a retained scan when this section
was written** — the three re-baselined documents (ordnance-1944, Tolch-1938,
DoD-1975) were the only ones that did. `ordnance-105mm-m1-1940` has since
joined them (§15).

That correction matters more than the one document: this section asserted Tier
1 was blocked on the human, and it held only until the human was asked. For the
105 mm document the deleted extraction was *also* recoverable from git at
`69d3362^`, which nobody had checked. **"No original available" is a conclusion
to reach after looking, not a starting assumption** — and the two cheap places
to look are the user and this repo's own history.

One defect here needed no source to register, and is now marked at
`src/arty/fragmentation.py`: **two bare line numbers inside shipped code** —
`1-s2.0-S221491472030502X-main.md:137` for the 1.6 aspect ratio and
`rspa.1947.0042.md:190` for `kappa_x` — the same class as the DoD anchor
finding at §11, and pointing into two documents (Tier 1 and Tier 2) that are
themselves unverified. A line number rots on re-extraction without failing
loudly; Tolch's own line numbers have already shifted once.

### 14b. Ordering against Phase 7

Where a source needs *re-extraction*, Phase 7 (the pdf-processor fixes) lands
first — pipeline before data. Verifying a table by hand against a retained
scan, as §12 and §13 did, carries no such dependency and can proceed now.

### 14c. The eyeball/vision sweep

Promoted here from Phase 8 item 3. It was written as a cheap precaution
against a hypothetical; §13 makes it a search for a confirmed defect class.
Triage is mechanical: an `images/` directory, or a markdown table of numbers,
with no `tables/*.csv` beside it. Each hit is re-baselined or marked
non-citable — there is no third outcome, and "probably fine" is not one of
them.

### 14d. Narrative admissibility

Wrong *prose* has cost more here than wrong digits. Tolch's "Drag Model
Relevance" section recommended a drag anchor that is near-insensitive to drag
(§6); the correction lived only in agent memory and the card said the wrong
thing for years. A @modeler dispatched to read that card inherits it as a
premise before it computes anything.

So: every `card.md` section that tells a reader **what to use the source for**
is a modelling claim wearing a reference doc's clothes. Each is verified, or
struck and moved to `derivation.md` where @model-reviewer sees it. That is
Phase 8 item 2, which this makes urgent rather than tidy.

### 14e. Exit criterion, and why the gate cannot deadlock

Every source cited by a pending Phase-3 thread ends in exactly one of two
states:

1. **Re-baselined** — `tables/*.csv` plus a passing closure invariant, or an
    explicit "no closure invariant exists" note flagged for human review, per
    `.claude/rules/source-data-fidelity.md` ("absence of a check is a finding,
    not a pass").
1. **Unverifiable** — no original obtainable. Recorded as such here, **and
    every claim resting on it marked provisional.**

State 2 is a legitimate outcome. Some of these documents are web pages and
vendor datasheets that may simply not be re-acquirable, and the audit must not
stall on one. What the gate forbids is state 2 going *unrecorded*: a modeler
brief may not cite an unverifiable source as evidence, and a Phase-3 verdict
resting on one is labelled **provisional**, never **sound**.

## 15. Tier-1 re-baseline: ordnance-105mm-m1-1940 (Phase 2.5a, first of two)

Scan supplied by the user and retained at `source.pdf` (183 pages, gitignored).
Page 16 carries a real text layer, so no vision extraction was involved.

Artifacts: [`tables/bill-of-material.csv`](../../../../doc-reference/ww2-shells/ordnance-105mm-m1-1940/tables/bill-of-material.csv)
\+ `.invariant`, and
[`checks/ordnance-105mm-bom-page-fidelity.py`](checks/ordnance-105mm-bom-page-fidelity.py)
(0 failures over 8 rows).

### 15a. The document supplies exactly one cell to the model, and it is correct

`src/arty/fragmentation.py` quotes `Steel WD-X1335 / 57-107` off the
**Body, Shell** row of the BILL OF MATERIAL. Checked against the page: correct,
and corroborated independently on the LIST OF PARTS table at `source.pdf` p.9.
The 53.9 lb body weight also on that row is quoted in the card but consumed by
nothing (`grep` finds no `53.9` or `24.4` in any `.py` or `.qmd`).

**So the shipped constant's provenance is sound — and that was never where the
risk was.** The composition behind the grade name is an unconfirmed reading of
WD-X1335 as AISI 1335, and `sigma_f` / `gamma` come from elsewhere entirely.
This re-baseline does not touch that; it only establishes that the one sourced
fact is the fact the source states.

### 15b. Why a closure invariant on a column no model reads

The cited cell is a **string**, and a string has no arithmetic — there is no
direct way to show it was read off the row it belongs to. The BOM's two amount
columns supply that indirectly: if the numeric cells sit on their part's row,
the material cell does too. The page's own header words define the relation
(`AVERAGE AMOUNT OF MATERIAL PER SHELL` × 100,000 =
`AMOUNT OF MATERIAL PER 100,000 SHELL`), and it holds on all three rows that
carry both figures.

That is not a hypothetical guard here. The OCR transcription of this page that
was committed until `69d3362` prints the Band, Rotating amounts on the line
**above** the `Band, Rotating` part name — values offset one row from their
labels, the same flattening defect that inverted the 1944 Ordnance tables
(§1). Anything reading that transcription rather than the page could pick the
wrong row off it.

### 15c. Card defects found, none of them consumed

The prior `card.md` was written without the page. Against `source.pdf` p.16:

| card.md said                                                 | page 16 says                                         |
| ------------------------------------------------------------ | ---------------------------------------------------- |
| "Total Material Allotment **5,290,000** pounds per contract" | **5,390,000**, and the column is *per 100,000 shell* |
| **Gliding** Metal                                            | **Gilding** Metal                                    |
| band O.D. **4.58"**                                          | **4.56"**                                            |
| exterior coating **3-87**, stencilling **35-2**              | **3-67**, **36-2**                                   |

None of these reaches a model. Their value is as a **measurement of how much
weight the rest of that card could carry** — four independent errors in one
short table, from a card that also asserted things the document does not
contain.

### 15d. Two claims removed from the card as not belonging to this source

1. **Mechanical properties.** The card carried "Inferred typical range for WW2
    19-ton/20-ton shell steel: 250–350 MPa yield, ~400–500 HB hardness
    (estimated; not confirmed for WD-X1335)". This document supplies **no**
    mechanical data — it defers all of it to spec 57-107, which is not
    reproduced in it. The numbers are also mutually inconsistent (400–500 HB
    implies roughly 1350–1700 MPa tensile, several times the quoted yield), so
    they cannot both be a range for one material. Removed. Nothing consumed
    them; the risk was a future pass quoting a reference card for a property its
    source never stated.
1. **"Compare to SAE 1040"**, from the card's Recommendations section. That is
    a modelling judgment — and specifically the *alternative reading* of
    WD-X1335 that `updates/wdss1-steel-grade/derivation.md` already records in
    three places and that `src/arty/fragmentation.py` names in its own comment.
    Removed from `doc-reference/`, where a @modeler would inherit it as a
    premise; it survives where a reviewer sees it. This is Phase 2.5d applied to
    one card.

### 15e. Recorded, not extracted: the dimensioned drawings

`source.pdf` pp.7–8 carry the full finished-shell dimension set, a stated mean
cavity volume to overflowing of 91 cu. in., and the concentricity tolerances
(anchors `MEAN VOLUME OF CAVITY`, `TOLERANCE ON CAPACITY`). No current model
needs shell geometry from this source, and the text layer on those blueprint
pages is badly corrupted, so extraction is a vision job with real cost and a
known failure mode. Left out deliberately and noted in the card, so a future
geometry pass finds it instead of re-searching for it.

### 15f. Effect on the gate

`ordnance-105mm-m1-1940` moves to **re-baselined** (§14e state 1). Phase 2.5a
is half closed; `explosion-fragment-model` remains. The premise in §14 that
Tier 1 was blocked on the human held only until the human was asked — and for
this document the extraction was additionally recoverable from git at
`69d3362^`, which nobody had checked.

## 16. Tier-1 re-baseline: explosion-fragment-model (Phase 2.5a, second of two)

Felix, Colwill & Harris (2022), *Defence Technology* **18** 159–169. Scan
supplied by the user, retained at `source.pdf` (11 pages, gitignored); the pdf
carries a clean text layer, so no vision extraction was involved.

Artifacts: three CSVs + invariants under
[`tables/`](../../../../doc-reference/fragmentation/explosion-fragment-model/tables),
a new [`card.md`](../../../../doc-reference/fragmentation/explosion-fragment-model/card.md),
and [`checks/explosion-fragment-model-aspect-ratio.py`](checks/explosion-fragment-model-aspect-ratio.py)
(0 failures).

### 16a. The shipped 1.6 is confirmed, in the right direction

`src/arty/fragmentation.py` ships `_MOTT_ASPECT_RATIO = 1.6`. Against the page:

- **Magnitude.** Table 4's bottom row gives per-dataset averages Grady 1.58
    (ogive), Hiroe 1.66 (cylindrical), Mott 1.48 (cylindrical). Mean 1.5733 →
    **1.6**. The paper's own sentence for this is garbled in print — *"the
    average of the three results in Tables 4 and 1:1.6 rounded is taken as the
    starting point"* — so the arithmetic, not the sentence, is what the check
    pins.
- **Direction, which is the part that could have been silently wrong.** §2.5:
    *"The aspect ratio of a fragment is defined as a fragment's width divided by
    its length."* Table 4's column head repeats it: `(width: length)`. So
    length = 1.6 × width — fragments long and thin, which is the sense
    `A = l̄/x̄` uses. **There is no numeric tell for this error class**: 1.6 is
    plausible either way round, and an inverted reading would have produced
    short fat fragments with every arithmetic check still passing. The check
    asserts both defining sentences are still on the page.
- **Corroboration.** §2.5's Wilson 1:1.65 (tungsten alloy) and Grady 1:1.5
    (AERMET-100) both confirmed verbatim. Note the two Gradys are *different
    figures* — 1.58 in Table 4, 1.5 in §2.5 — an easy conflation the card now
    calls out.

### 16b. The document had no card at all

There was no `card.md` in this folder, only a raw extraction, `images/`, and a
citation from shipped code pointing at **line 137 of the extraction**. So the
one summary a future reader would consult did not exist, and the only pointer
to the number was the anchor form this audit exists to eliminate. Written now.

This is a gap the tiering in §14a did not predict: the eyeball/vision sweep
(2.5c) triages on "a numeric table with no `tables/*.csv` beside it", which
would have caught this — but "cited by shipped code with **no card**" is a
sharper and cheaper triage, and worth adding to the 2.5c sweep.

### 16c. A discrepancy recorded, not repaired

Table 4's bottom row is labelled "Approximate average ratio" and its three
values do not reproduce as count-weighted means of their own columns: Mott's
59/30/10/1 gives 1.53, not the printed 1.48; Grady's 1.58 needs the open
"1:4 and more" bin weighted near 6. The paper states no weighting rule for the
open bin, so this cannot be resolved from the page — it is the authors'
arithmetic, not a transcription error.

It does not move the shipped value: 1.6 is exactly what the paper concludes,
and the spread of the three datasets (1.48–1.66) is wider than the
discrepancy. Recorded in the card and in the `.invariant` so a future pass that
tries to re-derive the average from the distributions knows in advance it will
not land on 1.6.

### 16d. Anchors repaired in the citing artifacts

Both bare-line-number citations of this document were replaced with greppable
anchors plus a CSV path: `src/arty/fragmentation.py` (was
`1-s2.0-S221491472030502X-main.md:137`) and
`updates/mott-fragment-shape-closure/derivation.md` (A16, same anchor plus
"§2.5 line 51"). This is a comment/citation edit only — no physics, no value
changed. `scoping.md` and `review.md` in that update folder still carry line
references; they are historical records of passes and were left alone.

**The blocking marker in `fragmentation.py` is narrowed, not cleared.** Its
other half — `rspa.1947.0042.md:190`, backing `kappa_x` — points into
`gurney-equations-fragmentation`, which is Tier 2 and still has no `tables/`
and no re-baseline.

### 16e. Effect on the gate

**Phase 2.5a is closed.** Both Tier-1 sources are re-baselined (§15, §16), and
in both cases the constant `src/arty` ships was confirmed correct. What the
gate bought was not a corrected number — it was knowing that, plus two
anchors that no longer rot, two documents that now have tables a future pass
reads instead of retyping, and a card that did not exist.

Phase 4 (`src/arty` assessment) is **unblocked on its Tier-1 dependency**.
Phase 3 remains blocked for any thread citing a Tier-2 source (§14a), and
`mott-fragment-shape-closure` is such a thread: it rests on `kappa_x` from
`gurney-equations-fragmentation`.
