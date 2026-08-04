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

### 7a. Phase 7 item 6 — the fixed pipeline reproduces the known-good CSV

Evidence:
[`checks/vision-pipeline-regression-p41.py`](checks/vision-pipeline-regression-p41.py),
input retained at `checks/fixtures/tolch-p41-post-fix-extraction.md`.

This is the plan's stated regression test, and it passes. Page 41 re-extracted
through the fixed path (`--pages 41`, chunk size 1) and scored against
`tables/base-spray-density.csv`:

| pass                                | result                                 |
| ----------------------------------- | -------------------------------------- |
| shipped 8-page stack (§7, historic) | **5 / 18** cells on the `Perf.` block  |
| fixed path, full 51-cell table      | **49 correct, 1 wrong, 1 flagged `?`** |

Three things worth separating, because only the first is the regression:

1. **The transcription is right.** 49 of 51 cells match the CSV that was
    transcribed off the page images and closes on the independently-printed
    totals table.
1. **The one unread cell is marked, not invented.** The extraction emitted `?`
    for (1685 f/s, Panel A, Dents) rather than a plausible number. That is
    Phase 7 item 5 working as designed, and it is the *specific* historic
    failure — §7 above records the old path filling a dashed row with the next
    row's values, confidently and unmarked. A `?` is a cell a human can go
    check; a fabricated `.12` is not.
1. **The closure adjudicated the single disagreement, against the extraction.**
    On (Static, Panel A, Perf.) the extraction gives 1.62 and the CSV 1.82. The
    page's own printed total for that row is 9.71; the CSV's three components
    sum to 9.71 and the extraction's to 9.51. The CSV closes, so the extraction
    is wrong there — decided by arithmetic internal to the source, not by
    preferring the older artifact. Note *which* value the fixed path still gets
    wrong: `1.62` is the exact wrong number the 8-page stack produced and that
    reached `tolch-1938.md`. Single-page extraction is much better, not
    infallible, and the closure is what remains load-bearing.

`uv run src/utils/check-table-invariants.py doc-reference/ --all` → **0 / 24
tables failed**, up from 21 tables as §21–22 added three.

### 7b. Serial extraction was costing hours of pure idle — chunks now run concurrently

Evidence:
[`checks/vision-concurrency-ordering.py`](checks/vision-concurrency-ordering.py)

The instrumentation added for §7's diagnosis answered a question that had been
guessed at for several passes: a single page costs **~145 s**, essentially all
of it blocked on the API. Chunk size is pinned at 1 for correctness, so a
document is one request per page — which made a 7-page block ~17 min and would
make the 56-page Sandia report over two hours, with the CPU idle throughout.

The requests are independent, so they now run 8 in flight, paced to the 30
req/min free-tier quota. Measured on the same 7-page Tolch block:
**3 min 11 s against ~17 min serial, 5.4×**, and the per-page transcription is
*identical* — re-scoring page 41 out of the concurrent run reproduces 49/51
with the same single wrong cell and the same flagged `?`.

**The risk this introduces is exactly this audit's defect class, so it is
tested directly.** Chunks no longer complete in the order they were sent: the
live run completed p44, p42, p45, p43, p41, p40, p39 — near-exactly reversed.
Reassembling on completion order would transpose a document's pages, producing
perfectly-extracted numbers under the wrong page — "every digit correct, wrong
row" (§1), reintroduced by a performance fix rather than by an extractor.

Two independent checks that it does not:

- `checks/vision-concurrency-ordering.py` stubs the API and makes the earliest
    chunk sleep longest, so completion order is the deliberate reverse of input
    order; output must still be in input order. It also asserts the pacer
    admits 30 starts and holds the 31st. Retries and halved sub-chunks pass
    through the same pacer, since the quota counts requests, not chunks.
- The live 7-page output carries the report's own printed page numbers, which
    come out **17, 18, 19, 20, 21, 23** — strictly increasing, from a run whose
    completions were reversed.

Rendering stays serialized under a lock: PyMuPDF is not thread-safe across one
document, and at ~0.1 s/page against a ~145 s call it costs nothing to give up.

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

| Document                                           | Numbers reach                                            | Source form       | Since resolved         |
| -------------------------------------------------- | -------------------------------------------------------- | ----------------- | ---------------------- |
| `fragmentation/dod-1975-fragment-debris-hazards`   | **`src/arty/fragmentation.py`** + 7 artifacts            | scanned DoD TP-12 | §13 — scan re-acquired |
| `ww2-shells/ammunition-series-6-wdss-specs`        | `updates/wdss1-steel-grade/` incl. `checks/recompute.py` | printed manual    | §19 — scan re-acquired |
| `ww2-shells/ammunition-series-6-steel-composition` | `updates/wdss1-steel-grade/` scoping + review            | printed manual    | **open**               |
| `azom-steel-grades/aisi-1335`                      | `updates/wdss1-steel-grade/` incl. `checks/recompute.py` | web article       | §21 — no scan needed   |

`wound-ballistics/aep-55-vol3` is cited only in one `scoping.md` and carries no
`card.md`; narrative-only, so not exposed. `aisi-1020` and `aisi-1045` are
uncited.

**None of the four retains its source.** `tolch-1938.../source.pdf` is the only
PDF in `doc-reference/`.

> **Three of the four have since closed, and one of them shows this section's
> reasoning was too narrow.** Two closed the expected way — the user supplied
> the scan (§13, §19). `aisi-1335` closed with **no scan at all** (§21): its
> source is a live web page, so it is re-fetchable rather than lost, and its
> composition table carries an arithmetic closure (Fe is stated as "balance",
> so each Fe bound is the complement of the opposite-extreme sum of the other
> five elements) that is checkable without seeing a page. Neither route was
> considered below. The inference "no retained scan → cannot be re-baselined"
> is therefore **not sound in general**; it holds only for a document that is
> both unobtainable *and* carries no internal closure. Test both before
> recording a document unverifiable. So these tables *cannot* be re-baselined the way the
> Tolch tables just were — the only surviving copy is the extracted markdown,
> which is the artifact whose fidelity is in question. Transcribing a CSV out of
> it would launder an unverified extraction into an apparently-checked one, which
> is worse than leaving it visibly unchecked. **Re-acquisition comes first**;
> that is the finding, and it is why nothing was extracted here.

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

FINDING\[deferrable\]: one doc-reference document feeds numbers into committed artifacts with no tables/\*.csv and no retained source PDF, so it cannot be re-baselined without re-acquisition (dod-1975 closed in §13 by re-acquisition, ammunition-series-6-wdss-specs in §19, aisi-1335 in §21 — the last of these needed no scan at all, its source is a live page and its table carries an arithmetic closure) (affects: doc-reference/ww2-shells/ammunition-series-6-steel-composition/; since: 2026-08-02)

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

Its seven anchors are also all bare line numbers (`ordnance-1944.md#L261`,
`#L340-L369`, …) — the form `.claude/rules/source-data-fidelity.md` forbids, and
the form that rotted onto the wrong shell's data in the original incident.

FINDING\[blocking\]: ordnance-1944 card.md labels all three shell sections with the table number of a neighbouring shell (43→81mm M43A1, 51→105mm M38A1, 59→8in M103; correct are 38/39, 48/49, 56/57) and prints each casualties B value beside the perforation table's range — the exact lossy-summary mechanism that caused the column inversion; quoted numbers are correct, labels are not, and experiment/fragmentation-field/\_validation.qmd Check 7 repeats the wrong set "Tables 43/51/59" on a rendered reader-facing surface (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md, experiment/fragmentation-field/\_validation.qmd; since: 2026-08-02)

FINDING\[deferrable\]: ordnance-1944 card.md cites all seven of its anchors as bare line numbers into ordnance-1944.md, the anchor form source-data-fidelity.md forbids; replace with greppable strings when the card is split (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md; since: 2026-08-02)

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

## 17 · Tier-2 re-baseline — `gurney-equations-fragmentation` (Mott 1947)

Scan supplied by the user 2026-08-02 and retained as `source.pdf` (9 pp.,
gitignored). Pages 304–308 were read at 200–420 dpi. The PDF carries an
embedded OCR layer of its own, and that layer is poor — so page-fidelity here
is a *visual* read, not a text-layer string match as it was for the 105 mm BOM.

### 17a · The shipped constant is correct, and closes on the paper's own example

`_MOTT_BREADTH_FACTOR = 1.5` comes from finding (1) on p.305: *"The fragments
have lengths most of which lie between x₀ and 2x₀, and that the average length
is about 1·5x₀."* Verbatim on the page.

Better than a page match, it **closes arithmetically**. p.306 states
x₀ = 1·6/√γ in. for its 3 in. bomb and concludes *"if γ ~ 100, the average
fragment length is about 0·24 in."* — and 1.5 × 1.6/√100 = 0.24 exactly. So the
1.5 in finding (1) is demonstrably the same 1.5 Mott used to reach his own
printed answer, rather than a plausible number read off a neighbouring
sentence. That is the shape of check this audit was set up to produce:
`checks/mott-1947-gamma-and-length-closure.py`, C1.

### 17b · The γ column does not close — blocking

p.308 states γ ~ 160 P₂/P_F(1 + s_F) two lines above the table it then
tabulates, and introduces that table as values *"of P₂, P_F, s_F … deduced
below"*. Feeding the tabulated columns back through the formula:

| material     | printed γ | s_F = reduction in area | s_F = ln(1/(1−RA)) |
| ------------ | --------- | ----------------------- | ------------------ |
| iron         | 20        | 55.0                    | 36.3               |
| steel 0.1 C  | 42        | 56.5                    | 43.6               |
| steel 0.25 C | 53        | 55.2                    | 45.1               |
| steel 0.45 C | 67        | 47.2                    | 40.2               |

Both readings are essentially **flat** — ×1.20 across the four rows — where the
printed column rises **×3.35**. The implied proportionality constant would have
to run 58 → 227.

**Every digit was confirmed against the page at 420 dpi.** This is therefore
not a transcription defect: it is either a fuller derivation Mott did not print
(he writes "~", and says N "can only be guessed"), or an inconsistency in the
1947 paper.

It matters because the *rising trend* is precisely what this repo consumes.
`src/arty/fragmentation.py` carries γ = 47 for WDSS-1, interpolated inside the
0.1 C → 0.25 C segment, and γ = 65 anchored just under the 0.45 C row. Both
read that column and nothing else in the table. Whether a series that does not
reproduce from its own stated formula is still usable as a calibration ladder
is a **modelling** question, not a librarian one — registered `blocking`
against `src/arty/fragmentation.py`, for Phase 4.

A second non-closure, consumed by nothing and recorded only for completeness:
p.308's "average length 0·6 in." for mild steel implies γ = 16, below even the
iron row.

### 17c · A prior flag was stale in the safe direction

The extraction's own header said `wdss1-steel-grade/derivation.md` still
interpolated γ on the pre-2026-07-25 bracketing points (0.1 %C → 32, 0.2 %C →
53). It does not — that derivation was redone and now brackets 0.1 %C → 42 and
0.25 %C → 53, which is what the page says. The header has been corrected.

Worth naming as a pattern: **a "flagged, not yet fixed" note is a claim with a
shelf life, and nothing re-checks it.** This one had already been discharged;
the reverse — a note saying "fixed" when it was not — would have read exactly
as trustworthy.

### 17d · The extraction is unsafe for equations, and one is materially wrong

The §3 table is faithful. Several equations are not, and one is serious: the
line after eq. (5) should read **x₀ = (2P_F/ργ)^{1/2}·r/v**; the extraction
renders it `(2P_y/ρv)^{1/2} r/v`. That drops the **γ** dependence entirely —
the dependence the whole of §3 exists to quantify, and the one that makes
p.306's x₀ = 1·6/√γ true.

Nothing derived from the corrupt line: `mott-fragment-shape-closure/ derivation.md` (G2) carries the correct form, having taken it via Gold 2017
eq. (2), which agrees with the page symbol-for-symbol. **The redundancy caught
it, not the extraction gate** — the same lesson as §15's BOM cross-table
corroboration. Four further defects (a `^4` for `^{1/2}`, `x_g` for `x₀`, a
figure numbered 3 that is 4, a garbled abstract sentence) are listed in the
new `card.md`; none is consumed.

### 17e · The document had no card

Like `explosion-fragment-model` (§16b), a source feeding **two** shipped
constants had no `card.md` at all — only a raw extraction. That is now two of
the two documents in this class. The 2.5c triage should be "cited by shipped
code with no card", not merely "no `tables/*.csv`"; on this evidence it would
have found both.

The folder is also misnamed: `gurney-equations-fragmentation` contains no
Gurney equation. Kept, because eight artifacts cite the path; recorded in the
card so the next reader is not misled.

### 17f · Anchors repaired

Bare line numbers into `rspa.1947.0042.md` replaced with greppable page
anchors in `mott-fragment-shape-closure/derivation.md` and `scoping.md`,
`mott-scale-gap/_scale_verdict_ledger.md`, and
`wdss1-steel-grade/checks/recompute.py`. `recompute.py` still hand-copies the
γ series into a literal array — values verified correct, so this is fragility
not wrongness; marked `deferrable` for the pass that next re-runs it and can
diff the output.

### 17g · State

`gurney-equations-fragmentation` is **re-baselined**. The remaining Tier-2
sources — `ammunition-series-6-wdss-specs`, `sandia-sand92-0243`, `aisi-1335` —
were supplied by the user in the same batch and are next; 2.5b is not yet
closed. The `fragmentation.py` blocking marker for `kappa_x` is **cleared**,
replaced by the narrower and more consequential γ-column finding in 17b.

## 18 · Primary acquired — Mott & Linfoot 1943 (A.C. 3348)

The user supplied a scan of the second Mott paper
(`/mnt/f/Projects/TMP/Docs/mott_ADB968781.pdf`, DTIC `ADB968781`), flagged as
poor quality. It was not on the audit's source list, because no repo artifact
cites it directly. It is on the list now, retained at
`doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/`, for
one reason: it is the **primary behind Gold 2017's `Mott (1943)`
attributions**, and Gold is what the shipped fragment-shape closure is derived
from.

### 18a · The scan defeats text matching, so the closures carry the fidelity

The embedded OCR layer does not reconstruct into sentences — a page of it is
unusable. This is the same wall §17 hit on the 1947 scan, one notch worse: there
the text layer was poor but greppable, here it is not. Every digit and quotation
on the card was read off a 200–400 dpi render of the page.

That makes the closure invariant the *only* thing standing between a visual
read and a wrong number, which is exactly the case
`.claude/rules/source-data-fidelity.md` was written for. Three hold, in
`checks/mott-linfoot-1943-closures.py`:

- **The calculated column of the p.3 count table is a one-parameter fit.** It
    is eq. (4) `N(m)dm = C exp(-M/M₀)dM`, `M = m^(1/3)`, at the printed
    M₀ = 0.33 oz^(1/3); dividing each printed count by its bin's probability
    mass must give the same `K = C·M₀` on every row. It does, to **±2%**, and
    the column regenerates from that single K as 455/128/181/13/5 against the
    printed 454/129/181/13/5.
- **Both obs/calc column pairs sum identically** — 782 = 782 and 1478 = 1478,
    with no free parameter, because C is fitted to the observed total.
- **The p.2 worked example reproduces to 4%** — `a = (24r²W/ρV²)^(1/3)` at
    W = 70 ft-lb/in², r = 2.2 in., V = 2500 ft/s gives 0.529 in. against the
    printed 0.55.

The first of these settled a bin boundary I could not read confidently: the
`½ – 4 oz` bin really is that wide, because reading it as `½ – 1` predicts 92
where the page prints 181. **A closure resolved a glyph ambiguity that no
amount of re-rendering would have** — worth recording as a use of the rule
beyond catching outright errors.

A fourth closure surfaced while transcribing the quotes and is now on the card:
**eq. (3) closes against eq. (2) algebraically.** The page propagates
`a = (24r²W/ρV²)^(1/3)` into a mean fragment weight `∝ ρa²t` and prints
`ρ^(1/3) r^(4/3) W^(2/3) V^(-4/3) t`, which is exactly what squaring eq. (2)
gives. A misread exponent in (2) would not reproduce (3) — and eq. (2)'s
exponents are precisely what the §18b `(r/V)^(2/3)` verdict turns on, so the
finding no longer rests on reading a handwritten `⅓` off a bad scan.

#### The gap the closures do *not* close: greppability

Prompted by the user asking whether this document needs vision re-extraction.
**It does not, and vision extraction is the wrong tool for what is actually
missing.** What the document supplies here is *prose* — the whole §18b finding
rests on three sentences — and prose has **no closure invariant**. A table can
be closed arithmetically; a paragraph cannot. The observed failure mode of the
unfixed pipeline is invented values in cells the source leaves empty
(`checks/vision-provider-probe.py`, 5/18 cells); its prose analogue is a fluent
sentence the page does not contain, and on a scan this degraded there is no
detector for it. A 400 dpi visual read is *stronger* evidence than an OCR pass,
because it reads the actual page. Running the pipeline now would also mean
running the known-broken configuration, ahead of Phase 7.

But the anchors were only greppable in principle: `.claude/rules/source-data-fidelity.md`
requires a stable string `grep` will find, and here there was no text to grep.
Measured — **1 of the 9 anchors this repo cites is present in the embedded OCR
layer** (`checks/mott-linfoot-1943-anchor-greppability.py`).

Closed by transcribing the cited passages verbatim into
`doc-reference/.../mott-linfoot-1943-theory-of-fragmentation/quotes.md`,
deliberately a **quotation set, not an extraction**: only what is cited, in the
report's own words, from the 300 dpi render (`checks/mott-linfoot-1943-page-render.py`).
Both scripts are retained; the greppability one is a live regression guard, and
it earned that status immediately — see below.

Two things this turned up that belong in Phase 8:

1. **Line breaks are load-bearing in an anchor surface.** Two of the nine
    anchors failed their first grep because the quoted paragraph wrapped
    mid-phrase. An anchor that straddles a newline is not greppable, and
    nothing about the file *looks* wrong. The fidelity rule says anchors must
    be greppable strings; it does not say the surface they are greppable
    *against* must keep them unbroken, and any markdown re-flow can silently
    break one. Candidate rule text, plus the check shape that catches it.
1. **The repo has no prose ground truth for the extractor.** Tolch's
    `tables/*.csv` covers tables only. Once Phase 7 lands, running the fixed
    pipeline over this `source.pdf` and diffing against `quotes.md` scores
    prose fidelity on the exact failure mode the fix targets. `quotes.md` says
    so in its closing section; folded into Phase 7 item 6 as a second
    regression case.

### 18b · Gold's `Mott (1943)` citation is wrong on two of three counts

Gold 2017 (anchor `A series of engineering assumptions`) attributes three
things to Mott (1943). Against the page:

| Gold's attribution                               | Verdict against the primary         |
| ------------------------------------------------ | ----------------------------------- |
| breadth:length ratio "is approximately constant" | **contradicted**                    |
| average cross-sectional area ∝ `(r/V)²`          | **wrong paper** — that is Mott 1947 |
| fragments idealized as a parallelepiped          | **supported** (sect. 3)             |

The report disclaims a length theory twice, in terms that leave no room:
*"We have not been able to find a theory to account for the average **length**
of the splinters in this type of shell"* (p.2) and *"our theory is incomplete,
as it does not account for the length of splinters from shells, but only for
their **breadth**"* (p.4). Where sect. 3 does treat length, it makes it
*independent* of breadth — two separate exponential parameters `x₀` and `y₀`,
which is the opposite of a fixed ratio.

The `(r/V)²` area scaling is 1947's: eq. (2) here gives breadth ∝ `(r/V)^(2/3)`
from an energy-of-fracture argument, whereas `x₀ ∝ r/v` — hence area ∝ `(r/V)²`
— comes from the 1947 Mott-wave argument. Gold's own eq. (2) is the 1947 form.
The two theories are **alternatives, not a chain**, and the citation merges
them.

**Impact: no wrong number, one unsupported premise.** `_MOTT_ASPECT_RATIO = 1.6`
takes its value from Felix 2022 Table 4 (§16), not from Mott 1943, so nothing
shipped is wrong. What is unsupported is the *structural* premise that one
constant `A = l̄/x̄` applies across shells, which Gold presents as
primary-backed and `mott-fragment-shape-closure/derivation.md` inherits.
Registered `deferrable` against that derivation for the Phase-3 pass.

### 18c · The defect class this adds to the audit

§15 and §17 both found **wrong digits or corrupt equations in an extraction**.
This is different and new: the *extraction of the citing paper is fine*, the
*digits are fine*, and the defect is that a secondary source attributes a claim
to a primary that denies it. No glyph-level scan, no closure invariant, and no
`tables/*.csv` can catch it — the only detector is reading the primary.

That is worth stating plainly, because the audit's machinery is now good at
digits and has nothing at all pointed at provenance. It is also the cheapest
class to check *if* the primary is in hand, and the most expensive if it is
not: this one cost a scan the user happened to have.

The `.claude/rules/source-data-fidelity.md` "criterion match" gate
(@model-reviewer's) is the nearest existing hook — *does the cited data measure
the same quantity the model computes?* — but it is aimed at data, not at
citation chains. Phase 8 should consider widening it to: **a claim attributed
to a primary is checked against that primary, or marked secondhand.** Filed
under Phase 8 rather than fixed here.

### 18d · What this document does not settle

- **No γ and no composition table** — the 1943 theory has no `γ` at all; its
    material input is the rupture energy `W`. It therefore cannot adjudicate
    the §17b γ-column non-closure, which stands.
- **No breadth:length ratio value**, per 18b — so it neither confirms nor
    moves the shipped 1.6.
- Figures 3–7 (pdf pp. 10–12) are plates with no text layer; not digitized,
    not cited.

### 18e · State

Retained, carded, one table transcribed and closed, cited prose transcribed
verbatim to `quotes.md` and all nine anchors verified greppable. Three retained
scripts: `mott-linfoot-1943-closures.py` (0 failures),
`mott-linfoot-1943-anchor-greppability.py` (0 failures; reports 1/9 against the
OCR layer), `mott-linfoot-1943-page-render.py`. Tier assignment: **Tier 3**
(no repo artifact cites it) promoted to *read* status because it adjudicates a
Tier-1 premise. Two `deferrable` findings registered against
`mott-fragment-shape-closure/` — the Gold attribution, and that derivation's
remaining bare-line-number citations into Gold, which are the same anchor-rot
defect already registered for `ordnance-1944` and `dod-1975`.

Phase 2.5b is still open: `ammunition-series-6-wdss-specs`,
`sandia-sand92-0243` and `aisi-1335` remain.

______________________________________________________________________

## 19 · Tier-2 re-baseline — `ammunition-series-6-wdss-specs` (Phase 2.5b)

**Verdict: transcription clean, card materially wrong.** Every digit of the
composition table survives; the defects are all narrative, and one of them is
the exact failure mode this audit was opened to catch.

### 19a · The plan mis-tiered it — this is a Tier-1 dependency

The plan lists `ammunition-series-6-wdss-specs` under **2.5b, "sources feeding
committed check scripts"**. It does more than that: it reaches **shipped
code**. `src/arty/fragmentation.py:67-68` cites "Ammunition Series 6, Table
6-1, 17 Feb 1953" for the `0.14-0.20 %C, 1.00-1.30 %Mn` band of the
`"US WW2 WDSS1"` steel entry, and that band's 0.17 % midpoint is what produces
the shipped `gamma = 47.0`. By 2.5a's own criterion — "sources reaching shipped
`src/arty/`" — it belongs in Tier 1, and the gate should have blocked on it.

It was missed because the tiering was built from a grep for source *slugs*, and
`fragmentation.py` cites this one by **title and table number**, not by
directory name. That is a general hole in the triage, not a one-off: see 19f.

No shipped number moves as a result — the band is correct — but the gate
ordering was wrong, and Phase 4 must treat this as a Tier-1 source.

### 19b · The scan, and why it needed no closure invariant

The user-supplied `source.pdf` is DTIC **AD830266** — and the document is not
what the repo called it. It is *Engineering Design Handbook, Ammunition Series,
Section 6*, **AMCP 706-249**, HQ U.S. Army Materiel Command, **July 1964**,
prepared by McGraw-Hill's Technical Writing Service from Picatinny Arsenal
data. The 17 Feb 1953 date belongs to the *specification*, not the handbook.

The scan carries a clean machine-readable text layer (~2 077 chars/page), which
changes what admissibility costs here. Table 6-1 is a chemical specification:
six grades x five elements, every cell an independent policy limit. **It has no
arithmetic closure invariant** — nothing sums, nothing is monotonic down a
column, no stated criterion closes on the rows. Under
`.claude/rules/source-data-fidelity.md` that means "flagged for human review".

It does not need to be, and the reason is worth recording as a general point:

> A closure invariant is a **proxy** for the question "was the right row and
> column read?" — it is what you use when the only access to the table is a
> human eye on a raster. When a clean text layer exists, that question can be
> answered **directly and positionally, cell by cell**, which is strictly
> stronger than the proxy. A closure catches a misread digit somewhere in a
> summed column; a positional diff names the cell.

So the table was extracted **by script** from the text layer and diffed against
the CSV per cell:
`checks/ammunition-series-6-table-6-1-fidelity.py` (0 failures). The CSV is
written by that same script's `--emit` mode, so no digit in it was ever typed
by hand — the rule's "extracted once, not re-typed" clause is satisfied
mechanically rather than by discipline. The `.invariant` carries the one real
internal check that exists (the phosphorus ceiling is constant on all six
rows), plus an explicit statement of why there is nothing else and what
substitutes.

One transcription subtlety: printed precision is load-bearing in a spec table.
`0.040 max.` is a three-decimal limit and `0.04` is not the same claim, so the
CSV stores the page's own strings. The first emit ran the values through `%g`
and silently coarsened five columns; caught on read-back.

### 19c · The table is correct — including the value flagged twice as suspect

All six rows reproduce cell-for-cell. That **closes a doubt open since the card
was written**: `ammunition-series-6-wdss-specs.md` flagged WDSS 1's sulfur
`0.08-0.13 %` as "unusually high; verify against original image" in its
confidence table, and repeated it as an open action. It is faithful. The
incidental-elements footnote (Ni 0.25, Cr 0.20, Cu 0.50, Mo 0.06) is also
faithful — and is *not* the same list as §6-13's post-WWII residuals (Ni 0.35,
Cr 0.30, Cu 0.25, sum ≤ 0.50), which is an easy conflation the card now warns
about.

### 19d · The finding: a card that told readers the source lacked what it has

§6-14, one sentence above the table:

> "The other grades cover all calibers from 37-mm to over 155-mm, in which the
> yield strengths vary from 60,000 psi to 80,000 psi."

The old `card.md` listed **yield strength** and **applicable shell calibers for
WDSS 3, 5, 6, 7** under a heading reading *"Data Gaps: Mechanical Properties
Not Specified — the following are NOT stated"*, and marked those four grades
"(Not specified in source)" in its table. Both claims are false against the
page. The companion `.md` repeated them in its confidence table ("Not stated;
pure inference"; "Source is silent") and carried "Clarify WDSS 3, 5, 6, 7
Applications" as an open research action — for a fact printed in the paragraph
that introduces the table.

**This is the 2.5d class in its purest form.** Nothing was mis-transcribed. A
reference card asserted an absence, and the assertion is self-sealing: a
reader who trusts it has no reason to open the page, so the error cannot be
found by anyone downstream of the card. It survived at least one prior pass
that was *specifically looking* for missing mechanical-property data.

It propagated. `_limitations.qmd` §13 (A6) states "Table 6-1 is chemistry-only:
no yield strength, no heat treatment" — true of the *table*, false of the
*source* — and on that basis the shipped `sigma_f = 800 MPa` (116 000 psi) has
never been compared against the 60 000–80 000 psi (414–552 MPa) the source
gives for artillery-caliber shell steel. Whether it should be is a
criterion-match question (static yield vs. dynamic fracture stress are
different quantities) and therefore @model-reviewer's, not this pass's.
Registered `deferrable` on `card.md`, routed to `_limitations.qmd`,
`fragmentation.py` and `wdss1-steel-grade/derivation.md`.

A second, smaller one registered as `note`: the shipped identifier
`"US WW2 WDSS1"` **misdates its own grade**. The handbook titles §6-11 *Steel
Used Early in World War II* (X-1340) and §6-13 *Steels Used After World War
II*; WDSS is the 1953 prevailing spec, downstream of both. Applicability is
already recorded correctly in `_parameters.qmd` (60/81 mm mortar, 57 mm
recoilless), so no number is misapplied — the name is simply wrong.

### 19e · Source-internal inconsistencies, neither of them ours

Both confirmed against the text layer; neither may be "fixed" in the CSV.

1. **Silicon.** §6-14 says all shell steel is made "silicon 0.15 to 0.30
    percent". Table 6-1 prints that on five rows and `0.10 max.` on WDSS 1. The
    prose and the table disagree about WDSS 1.
1. **X-1340 phosphorus.** §6-11 prints "phosphorus, 0.45 percent maximum",
    an order of magnitude above table 6-1's 0.040 and almost certainly a typo
    or scan defect for 0.045. Nothing cites it; flagged so nothing starts.

### 19f · What this adds to Phase 8

**A source can be cited by title instead of by slug, and the triage grep does
not see it.** 19a's mis-tiering was not a judgment error — the inventory was
built by grepping directory slugs, and `fragmentation.py` names this source in
prose. Any future "which sources reach shipped code" sweep must grep **document
titles and table numbers** as well as slugs, or it will keep under-tiering
exactly the citations that were written most carefully. Candidate rule text for
Phase 8, alongside the §18c citation-chain widening.

**`doc-reference/<slug>/<slug>.md` is not reliably an extraction.** This one is
a model-authored essay — metallurgical theory, σ_y estimates, design rationale
— with a header calling it a "transcribed excerpt". Its filename and location
both imply it is the processed source. It now carries a header saying plainly
that it is not, and pointing at `card.md` and the CSV. The general fix belongs
with Phase 8 item 2 (split `card.md`): the naming convention needs to
distinguish *extraction* from *commentary*, because right now nothing does.

### 19g · State

Re-baselined. `tables/table-6-1-chemical-requirements.csv` +
`.invariant` (1 check, passing; no closure exists and the file says so),
`card.md` rewritten against the scan with greppable anchors, `<slug>.md`
annotated with four refutations and three closed actions. Two findings
registered (one `deferrable`, one `note`).
`check-table-invariants.py doc-reference/ --all`: **0 / 19 failed**.

Two retained scripts, split along the table/prose line because the two need
different kinds of check:

- `checks/ammunition-series-6-table-6-1-fidelity.py` — emits **and** verifies
    the CSV against the text layer, positionally, per cell. 0 failures.
- `checks/ammunition-series-6-source-locator.py` — resolves the seven anchors
    the card cites and confirms its six quoted passages appear verbatim. 0
    failures. This is the greppability guard, not a fidelity proof: prose has no
    closure invariant, and the defect here was in prose. It replaces three
    throwaway `_scratch/` probes and reproduces their cited output (page
    indices, the ~2 077 chars/page density, the accession).

Writing the second one surfaced a small transcription trap worth recording: the
scan preserves the printed page's **soft hyphens** (`forg- ings`, `per- cent`,
`open- hearth`), which are indistinguishable from the hard hyphens in `37-mm`
and `open-hearth`. A quotation check that de-hyphenates only at line ends fixes
one and breaks the other, so both sides are reduced to a bare character run
instead. The same trap would silently corrupt any future prose extraction from
this scan.

One near-miss caught on read-back: the card first quoted the governing spec as
`MIL-S-10520C (ORD)` when the page prints `(ORO)`. `(ORD)` is certainly what was
meant, but silently repairing a source is the habit this audit exists to break —
it is now quoted as printed, with the artifact named.

Tier corrected to **Tier 1**. Phase 4 must treat it as such.

Phase 2.5b remains open: `sandia-sand92-0243` (scan retained, no `card.md` at
all) and `aisi-1335` (no local copy; azom URL only).

## 20 · `mil-s-10520d-projectile-steel` — the governing spec, one revision late

**Verdict: admissible, and it confirms the shipped WDSS1 band belongs to the
revision that is actually cited.** The lead it was acquired to chase — per-grade
yield strength from the governing specification — is a **dead end for a reason
worth recording**, and the acquisition incidentally exposed the worst
extraction-pipeline defect found so far (20d).

The user supplied `MIL-S-10520D.pdf` after §19 closed on `(ORO)`/`(ORD)`. It is
revision **D**, not the **C** that AMCP 706-249 §6-14 cites.

### 20a · What the cover page settles

`MIL-S-10520D(MU)`, 27 August 1975, **"SUPERSEDING MIL-S-10520C(ORD), 17
February 1953"** — and §6-14 dates table 6-1 "as of 17 February 1953". Same
day, same table. Three §19 loose ends close on that one line:

- Table 6-1 **is** MIL-S-10520C's Table I, not a handbook paraphrase of it.
- `(ORO)` is **confirmed** a scan artifact for `(ORD)`, no longer inferred.
- WDSS grades 1–7 are MIL-S-10520 grades 1–7; the missing grade 4 is real in
    both documents.

### 20b · The revision gap, and what the cross-document diff actually shows

D is direct evidence about **D** and only presumptive about **C**. Treating a
later revision as the cited one is the same species of error as reading the
wrong column, so the gap is carried rather than assumed away.

`checks/mil-s-10520d-closures.py` diffs all 30 cells of D's Table I against
§19's C-era `table-6-1-chemical-requirements.csv`:

- **26 of 30 cells identical**, plus the four-element incidental-elements
    footnote word for word. Grades 2, 3, 5, 6, 7 are unchanged between revisions.
- **All 4 disagreements are in grade 1.** C-era: C 0.14–0.20, Mn 1.00–1.30,
    S 0.08–0.13, Si 0.10 max. D: C 0.20 max, Mn 0.90 max, S 0.050 max, Si 0.20
    max. A high-Mn, high-S free-machining grade replaced by a plain low-carbon
    one — a **grade redefinition**, not a digit slip.

**Consequence for `src/arty/fragmentation.py`: none, and that is the finding.**
The shipped `"US WW2 WDSS1"` band (0.14–0.20 %C → 0.17 % midpoint → `gamma = 47.0`) is the **1953** grade 1, which is the revision AMCP cites. Correct as
shipped; it must **not** be "updated" toward D. Phase 4 inherits this as
settled.

This is also the first use in this audit of **cross-document agreement as a
closure**. Two independent transcriptions, from two independently-acquired
scans, of the same table: a row or column misassignment would have to be
replicated identically by two readers of two different rasters. For a table
with no arithmetic closure and no text layer, this is the strongest check
available — stronger than either reading alone.

### 20c · The lead does not deliver, and the reason generalises

**MIL-S-10520 states no mechanical properties of its own.** §3.7.1 requires the
steel to be demonstrated capable of meeting "the physical properties specified
on the **drawing of the projectile** for which the steel is intended"; §4.5.3
defines yield strength against a **specified** value supplied elsewhere. The
spec governs *chemistry and process*; the *numbers* live on the drawing.

So AMCP §6-14's 60,000–80,000 psi is the **handbook's own summary**, not a spec
value it quotes. Any future pass tempted to "go to the governing specification"
for a mechanical property of a US WW2 shell should read this section first.

Two indirect corroborations of §6-14 do fall out, and both are independent of
it:

- **The mortar/artillery grade split is real.** §3.7.2(b) exempts grades 1 and
    2 from the heat-treat demonstration; §4.5.1 selects coupons "from each heat of
    grades **3, 5, 6, and 7**."
- **The yield envelope.** Table X brackets span **60,000–85,000 psi** over
    37 mm to over-155 mm. §6-14 says 60,000–80,000 psi over the same caliber
    span — lower bound exact, upper plausibly extended 1953 → 1975. This
    corroborates the very number §19 recorded the source as not stating.

### 20d · The extraction pipeline failed silently on this document — Phase 7 item 7

Routing this scan through `pdf-processor.py` — instead of hand-reading rasters,
which is what I had started doing — was what caught it. The first run produced
**14 copies of an everyspec watermark, 66 lines, exit 0, "Done."**

Two gates failed at once, in the same direction:

- `_page_is_image_based` required **one** image rect covering >50 % of the page.
    This scan stores each page as **43–58 horizontal strips**, largest 3.4 %. So
    1 of 14 pages routed to vision.
- `_assert_not_scanned` tested `bool(text.strip())`. The 41-character watermark
    is truthy on every page, so a document with **no text layer at all** (588
    chars across 14 pages) presented as fully text-based.

`--analyze-formulas` was passed and did not help: it forces the *vision path*,
not vision *on a given page*, and the per-page heuristic still routed 13 pages
to their watermark. **The memory note `project_pdf_processor.md` ("scanned PDFs
need `--analyze-formulas`") is therefore insufficient as written.**

Fix: sum coverage over all rects, and count characters instead of testing
truthiness; plus a routing line printed every run, and a warning naming any page
that was *not* routed to vision yet carries under 100 characters. Routing on
this document went **1/14 → 14/14**. Probe: `checks/vision-gating-probe.py`
(takes any PDF — it doubles as the Phase 2.5c triage tool).

**Severity relative to Phase 7 items 1–5.** Those produced *wrong numbers*, and
a wrong number is at least visible to a closure check. This produced **no
content while reporting success** — nothing to check, and a `source.md` that
looks like a short document rather than a failed one.

A second defect surfaced on the re-run: a single `httpx.ReadTimeout` killed the
whole 14-page document after most of it had transcribed, because the retry
handler caught `errors.ServerError` and empty responses but not client-side
timeouts. A local timeout is the same deadline as a server 504 seen from the
other end, so it now retries-then-halves identically (item 8).

**And a third, in my own tooling rather than the pipeline:** the first run was
piped through `tail -30`, so the task notification reported **exit code 0** on a
run that died in a traceback. Pipelines mask exit status; a background
extraction must not be piped.

### 20e · Tables, closures, and one irregularity left as printed

Four CSVs under `doc-reference/ww2-shells/mil-s-10520d-projectile-steel/tables/`.
Tables III–IX and XI are dimensional tolerances, carry no physics, and are not
transcribed.

| Table                            | Closure                                                                          | Result                      |
| :------------------------------- | :------------------------------------------------------------------------------- | :-------------------------- |
| I — Chemical Requirements        | cross-document diff vs table 6-1 (20b); P/S column-identity sums in `.invariant` | 26/30 identical, 4 expected |
| II — Product-Analysis Variations | bracket tiling; over-max == under-min where both printed                         | 6 symmetric, 2 one-sided    |
| X — coupon selection             | bracket tiling; coupon diameter non-increasing as yield rises                    | pass, 3 classes             |
| X — hold times                   | `.invariant`: diameter increasing, both times non-decreasing                     | pass                        |

`check-table-invariants.py` on the new `tables/`: **0 / 2 failed**; the closures
script: **0 failures**.

**Irregularity, recorded not repaired:** Table X's "Over 105mm to 155mm, incl."
class opens with a bare **`65,000`** where the other two classes print a range.
By analogy with the over-155 mm row it should read "60,000 to 65,000, incl.";
as printed, that caliber has no bracket below 65,000. **Both independent
readings show the bare value**, which is what makes it the source's own
irregularity rather than a misread — and is exactly the kind of thing a reader
"tidying up" a table would silently normalise away.

### 20f · Why this document's admissibility rests on three legs

`.claude/rules/source-data-fidelity.md` assumes a closure invariant is
available. §19 showed a clean text layer beats one (a positional diff names the
cell). This document has **neither**: no text layer, and a composition table
with no arithmetic. So admissibility is three independent legs that agree:

1. **Direct read** of 300-dpi renders (`checks/mil-s-10520d-page-render.py`).
1. **Vision extraction** through the *fixed* pipeline, producing `source.md`.
1. **Cross-document agreement** with AMCP table 6-1 (20b).

Legs 1 and 2 agree **cell-for-cell** on Tables I, II and X — including the
inconsistently-dropped leading zeros (`.65` beside `0.60`) and the bare
`65,000`. That the two readers reproduce the same *anomalies*, not just the same
values, is what makes the agreement evidence rather than two readers smoothing
the same page the same way.

### 20g · Method note for Phase 8 — the invariant DSL has no cross-row handler

Tables II and X carry genuine closures that `check-table-invariants.py` cannot
express: bracket **tiling** (row *i*'s upper bound == row *i+1*'s lower bound,
within a group) and monotonicity **within a group** rather than down the whole
column. The DSL has exactly three handlers — per-row expression, whole-column
sum, adjacent-row monotonic — so both had to go into a check script.

This is not a one-off: any table of bracketed limits (calibre classes, velocity
bands, thickness ranges) has the same shape, and tiling is precisely the check
that catches a row read out of step. Phase 8 candidate: a `tiling:` directive
and a `group:` qualifier on `monotonic:`.

### 20h · Status

Re-baselined. `card.md`, four CSVs, one `.invariant`, three retained scripts
(`mil-s-10520d-closures.py`, `mil-s-10520d-page-render.py`,
`vision-gating-probe.py`); `experiment/_scratch/` back to empty. The pipeline
fix is committed with them, since this document is its regression case.

Phase 2.5b still open on `sandia-sand92-0243` and `aisi-1335`.

______________________________________________________________________

## 21 · Tier-2 re-baseline — `aisi-1335` (Phase 2.5b)

### 21a · What it feeds, and the two questions that are not the same one

One number: **0.33–0.38 %C**, reaching `_parameters.qmd` as the composition of
`WW2 US HE Shell` via the identification **WD-X1335 ≈ AISI 1335**.

Those are two separable claims, and conflating them is what left this document
looking unverifiable for longer than it was:

- *Is the transcription faithful to the page?* — **yes**, settled below.
- *Is AISI 1335 the right steel for WD-X1335?* — **not settled by this
    document, and it never can be.** The page carries no War Department
    nomenclature of any kind.

The gap is already recorded downstream as limitation 13 and as finding F5 in
`updates/wdss1-steel-grade/review.md`. Nothing here closes it, and nothing here
was expected to.

### 21b · The closure — iron as the balance element

This document was on the "cannot be re-baselined without re-acquisition" list
(§11 finding) on the reasoning that it has no retained PDF. That reasoning was
wrong twice over: the source is a **live web page**, so it can simply be
re-fetched; and the composition table carries a genuine arithmetic closure that
needs no page at all.

AZoM computes iron as the balance, which is the source's own construction rule.
So each Fe bound is the complement of the **opposite-extreme** sum of every
other element — Fe sits at its minimum when the alloying additions are all at
their maxima, and vice versa. Both legs pass:

| Leg                                          |     Sum | Target |
| :------------------------------------------- | ------: | -----: |
| `fe_lo + c_hi + mn_hi + si_hi + s_hi + p_hi` | 100.005 |    100 |
| `fe_hi + c_lo + mn_lo + si_lo + s_lo + p_lo` | 100.000 |    100 |

It crosses both columns and all six elements at once, so a value landing on the
wrong element, or on the wrong bound of the right element, breaks it. That is
the shape the column-inversion incident would have needed.

`tables/chemical-composition.csv` + `.invariant`; passes.

### 21c · Independent re-fetch, and two divergences recorded not repaired

The live page was re-fetched 2026-08-02 and reproduces every cell of the
composition table and every property value. Two divergences from
`aisi-1335.md`, neither of them a wrong number:

- **Row order was silently changed.** The page prints Fe, Mn, C, Si, S, P; the
    extraction rewrote them C, Fe, Mn, Si, P, S. Every element↔value pairing
    survived, but no anchor into that file may depend on row position — which
    is why the card anchors on the column labels instead.
- **Trailing zeros dropped.** The page prints carbon 0.330/0.380; the
    extraction has 0.33/0.38. The CSV carries the as-printed form.

Confirmed absent from the page, so any downstream use must cite elsewhere:
**yield strength and tensile strength appear nowhere on it.**

### 21d · Method note — a fetch summary is not a transcription

The first re-fetch returned a complete-looking property list that silently
omitted `Hardness, Rockwell C: 15`, and that omission was briefly read as a
disagreement with `aisi-1335.md`. A second, narrowly-targeted fetch confirmed
the value *is* on the page.

**An omission in a summarising fetch is not evidence of absence.** Phase 2.5c
leans on re-fetches to triage the remaining documents, so this bounds what one
of them proves: a fetch can confirm a value present, and cannot establish one
absent unless asked about that value by name.

### 21e · Status

Re-baselined. `card.md` rewritten, one CSV, one `.invariant`, no script needed
(the closure is expressible in the DSL). The §11 finding must drop `aisi-1335`
from its list.

______________________________________________________________________

## 22 · Tier-2 re-baseline — `sandia-sand92-0243` (Phase 2.5b)

### 22a · A clean text layer, so the check is the page itself

56/56 pages carry real text, 0 fall under the thin-page threshold
(`checks/vision-gating-probe.py`). No vision extraction is involved and none of
the §7 pipeline failure modes apply. As established in §19, a clean text layer
**beats** a closure: it answers "was the right line read?" directly.

Three arithmetic closures are declared anyway, and all pass
(`tables/site-and-material-constants.invariant`):

1. **The density span closes on the materials.** §9 item (c) gives
    2.77–16.6 g/cc; the appendix `Conditions:` blocks give aluminium 2.77, steel
    7.86, tantalum 16.6. The span is exactly the min and max — two
    independently-printed places in the document.
1. **Air density closes on the stated atmosphere.** The appendices' 0.000957
    g/cc is within **0.15 %** of the dry-air ideal-gas value for the 12.06 psia
    and 30 °C those same appendices state.
1. **The velocity bounds close across units.** The Introduction prints them in
    both ft/sec and mm/µs; the two printings agree to the printed precision.
    Swapping the two ends moves the residual from 0.04 to 7.4.

**The drag-coefficient row has no closure available anywhere in the document** —
flagged for human review per the rule, since absence of a check is a finding.
22b and 22c are why none exists.

### 22b · The page states two ranges, and the repo cites the weaker one

Page 18 (§9, *Discussion and Conclusions*) carries both, twenty lines apart:

| Where                     | Statement                                               |
| :------------------------ | :------------------------------------------------------ |
| parameter-range list, (e) | "Drag coefficient: **1.0 to 1.71**"                     |
| prose, three ¶ later      | "The drag coefficient can vary between **1.2 and 1.7**" |

Item (e) is the range **spanned by this report's own computed trajectory
data**. The prose is a general statement about tumbling plate/disk fragments.

Every citation in this repo uses 1.2–1.7 — a faithful quotation of the prose
sentence. But `checks/drag-coefficient-calibration.py` labels 1.2 as
"SAND92-0243 low", and the report's own data floor is **1.0**.

This is the audit's own defect class in a new form. Not a mis-transcribed digit
and not a wrong column: a number taken from the **wrong sentence on the right
page**, where a different sentence on the same page gives a different range for
the same symbol. A closure invariant would not have caught it, and neither
would a glyph-level scan. What caught it was reading the page around the
citation instead of the cited line alone — the same move that caught §12.

**Direction, for Phase 3/4 to settle:** the thread argues the model's $C_D$ sits
far below the literature. A floor of 1.0 rather than 1.2 narrows that gap
without closing it — 0.585 is still well under 1.0. Expect *shifted*, not
*void*.

### 22c · The report has the range but not the dependence

Every citation in this repo says "1.2–1.7, **velocity-dependent**". The report
states the velocity dependence exists and never gives its form. Its own
analyses take `Drag coefficient = variable (Ref. 1)` in the `Conditions:`
blocks of Appendices A, B and C, and Ref. 1 is:

> Vigil, *"Explosively Driven Missile Trajectory Parameters for Various
> Fragment Materials and Velocities,"* Sandia National Laboratories,
> **SAND91-0277**, June 1991.

**SAND91-0277 is not held.** So the functional form is cited but not sourced —
structurally the same as MIL-S-10520D delegating its mechanical properties to
the projectile drawing (§20c). Both were found the same way: by asking what the
cited document *itself* says, rather than treating a card's summary as the
source.

The asterisk in "a function of initial fragment velocity\*" has **no footnote
text**. Checked against raw block order rather than reading-order extraction —
a footnote lost to reading order would still appear as a block; the only block
below the marker is the page number.

### 22d · Criterion match — open, and not this ledger's to close

Recorded for @model-reviewer, whose mandate it is. Sandia's $C_d$ is defined
for "tumbling (assumed), plate or disk like irregular fragments" and enters the
range calculation only as a product with the shape factor $R_e$ and the
effective thickness factor $S_f$:

```
K = 0.262(Rhop)Sf/[Cd(Rhoa)(Re + 1)]        (9)
```

Whether a bare $C_D$ in `src/arty` is the same quantity is exactly the
criterion-match check. The report also warns its data "may not give accurate
results for more regular shapes like spheres or cubes."

### 22e · Two source irregularities, recorded not repaired

- **Appendix D cites the wrong equation for $C_d$.** A–C say
    `variable (Ref. 1)`; D says `variable (Equation 12)`. Equation 12 as printed
    is `R = Vb2/(K)(g)`, the range parameter, not a drag coefficient.
- **`K` carries two meanings.** The List of Symbols has "K Fluid flow
    parameter, plate or disk, 0.93"; equations (8)–(9) have
    `K = 0.262(Rhop)Sf/[Cd(Rhoa)(Re + 1)]`, a dimensional ballistic
    coefficient. Anyone reimplementing must not carry 0.93 into equation (9).

### 22f · Status

Re-baselined. `card.md` written (there was none), two CSVs, two `.invariant`
files, one retained script (`checks/sandia-cd-provenance.py`, which prints all
of 22b–22e off the page). Findings registered below.

**Phase 2.5b is closed** — `gurney-equations-fragmentation` (§17),
`ammunition-series-6-wdss-specs` (§19), `aisi-1335` (§21) and
`sandia-sand92-0243` (§22) are all re-baselined.

FINDING\[blocking\]: SAND92-0243 is cited as "C_D 1.2-1.7" and 1.2 is used as its low end, but that is the report's general prose sentence; its parameter-range list on the same page gives the span of its own computed data as 1.0 to 1.71, so the cited floor is 0.2 high (affects: experiment/fragmentation-field/challenges/drag-gap-1944/checks/drag-coefficient-calibration.py, experiment/fragmentation-field/challenges/drag-gap-1944/drag-coefficient-calibration.md, experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.qmd, experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md, experiment/fragmentation-field/\_limitations.qmd; since: 2026-08-02)

FINDING\[deferrable\]: SAND92-0243 is cited for a velocity-DEPENDENT C_D but states no functional form; its own analyses take "Drag coefficient = variable (Ref. 1)" and Ref. 1 is SAND91-0277, which is not held, so the dependence is cited but unsourced (affects: experiment/fragmentation-field/challenges/drag-gap-1944/drag-coefficient-calibration.md, experiment/fragmentation-field/updates/frag-field-3d-geometry/scoping.md, doc-reference/ww2-shells/sandia-sand92-0243/card.md; since: 2026-08-02)

FINDING\[note\]: SAND92-0243's C_D is defined for tumbling plate/disk fragments and enters its range formula only as a product with the shape factor Re and thickness factor Sf, never alone; whether a bare C_D in src/arty measures the same quantity is an open criterion-match question for @model-reviewer (affects: src/arty/fragmentation.py, doc-reference/ww2-shells/sandia-sand92-0243/card.md; since: 2026-08-02)

______________________________________________________________________

## 23 · Phase 2.5c — the `doc-reference/` admissibility sweep

Phase 2.5c asks a mechanical question of all 25 collected documents: which
carry numbers read by eye or by the vision extractor and never checked against
the page, and — the part the plan added after DoD-1975 — *who reads them*. An
uncited document with unchecked numbers is a latent problem; one whose numbers
reach `src/arty/` is a live one.

Tool: `checks/doc-reference-admissibility-sweep.py`. Triage is the plan's — an
`images/` directory or a markdown table of numbers, with no `tables/*.csv`
beside it. Exposure is a grep across `experiment/`, `src/` and `app/`,
deliberately over-broad, with this audit's own bookkeeping excluded (it names
every document it sweeps, so counting it would mark all 25 "cited" and destroy
the signal).

### 23a · The sweep's first answer was wrong, in exactly the way §19f predicted

The first revision grepped directory slugs and processed-source filenames. It
reported `wound-ballistics/fas-es310-damage-criteria` as reaching **zero**
shipped files.

That was false. `src/arty/fragmentation.py` cites the source as
`ES-310 (FAS/Navy 1998)` — the report designator, never the slug. §19f recorded
this failure mode as a *hypothesis* about `ammunition-series-6-wdss-specs`; here
it recurred inside the tool written after it, which is the useful part: the
lesson had been written down and still did not survive contact.

The fix is mechanical and now lives in the script — a `DESIGNATOR` regex
(letters-then-digits as printed on a cover: `ES310`, `SAND92-0243`,
`MIL-S-10520D`, `AD-A462991`) harvested from the directory name and front
matter, searched with and without its hyphen because the two surfaces disagree
("ES310" in the title, "ES-310" in the code).

| ES-310 exposure  | slug grep | + designator grep |
| :--------------- | --------: | ----------------: |
| citing artifacts |         8 |                30 |
| shipped files    |         0 |                 4 |

**A slug-only sweep under-tiers precisely the most carefully written
citations** — the ones that name the report rather than the file path.

### 23b · The sweep's finding: the widest-footprint unverified source in the repo

`wound-ballistics/fas-es310-damage-criteria` — 30 citing artifacts, four of
them shipped (`src/arty/fragmentation.py`, `src/arty/plots.py`,
`src/arty/zones.py`, `app/sensitivity.py`), plus eight `.qmd` partials
including `_limitations.qmd` and the top-level source table in
`fragmentation-field.qmd`.

It had **no card, no `tables/`, no closure invariant and no retained scan.**
Its three anchors are hardcoded at `fragmentation.py:271-272`, and its 1 kJ
anchor is the default binary lethal-KE threshold at `fragmentation.py:544`.

No prior pass had looked at it. The plan's Tier-1 list (§2.5a) named two
documents; this was a third, and it was found only because the sweep counted
exposure rather than trusting the tiering.

### 23c · Re-baselined — and the closure had to come from outside the table

Source is a live FAS page, so like `aisi-1335` (§21) it needs no scan.
Re-fetched 2026-08-03 in three targeted passes.

**Table 3 as printed** (`tables/table-3-fragmentation-damage-criteria.csv`) is
a 3×3 matrix, fragment energy in kJ:

| Target          | Light (Pk = 0.1) | Moderate (Pk = 0.5) | Heavy (Pk = 0.9) |
| :-------------- | ---------------: | ------------------: | ---------------: |
| Personnel       |              0.1 |                   1 |                4 |
| Aircraft        |                4 |                  10 |               20 |
| Armored vehicle |               10 |                 500 |             1000 |

**Table 3 has no internal closure.** Nine independent criteria, no arithmetic
linking them — a plausible wrong cell reads exactly like a right one. Per the
rule that is recorded as a finding, not waved through, and the ordering
relations that *do* exist are labelled ordering checks in the `.invariant`
rather than dressed up as closures.

**The closure is elsewhere on the page.** The page works a hand-grenade example
numerically, and to do so must read a Pk|hit off Table 3 at 3000 J. Only one
row can supply the 0.8 it takes:

```
target            linear in E  linear in logE   verdict
personnel               0.767           0.817   MATCHES the page
aircraft                0.000           0.000   cannot produce 0.8
armored vehicle         0.000           0.000   cannot produce 0.8
```

3000 J sits *below* the aircraft row's own light-damage floor of 4 kJ, so
neither other row comes near. **The example identifies the personnel row
uniquely** — the row-inversion defence, available only because the page states
a criterion in one place and exercises it in another.

The example also closes on its own terms
(`tables/worked-example-hand-grenade.invariant`): the page's stated hit model
`Nhits = A(N₀/4πR²)` reproduces both printed Nhits values (residuals 0.021 and
0.037 against printed roundings of "4" and "0.6"; transposing the two ranges
gives residuals of 3.4 and 3.3), and its two-branch aggregation rule reproduces
both printed Pk values.

Script: `checks/es310-worked-example-closure.py`. It reads both CSVs and checks
`_PK_E` / `_PK_VAL` against the CSV rather than a retyped array.

### 23d · Verdict on the shipped constants — admissible, with one limit

**`fragmentation.py:271-272` is faithful.** 100 J / 1 kJ / 4 kJ at
Pk|hit 0.1 / 0.5 / 0.9 are this page's personnel row, verified against the CSV
by script. So is the 1 kJ default at line 544, and so is the multi-hit formula
cited in `_limitations.qmd`.

**What is *not* certified is the interpolation between anchors.** The page
states no functional form. `pk_given_hit` interpolates in log₁₀E; the page's
prose reasons linearly in E. At the one point the page works, log₁₀E gives
0.817 and linear-in-E gives 0.767 against a stated 0.8 — the shipped scheme
sits closer, on a single point, which is agreement and not derivation. Any
claim turning on the *shape* of Pk|hit between anchors rests on a choice this
document does not make. Registered as a note.

### 23e · What the extraction added that the page does not say

Every *number* this repo consumes is faithful. The divergences are structural
and narrative — none visible to a glyph-level scan.

1. **The "Personnel Damage Criteria Table" is not a table on the page.** It is
    Table 3's personnel row transposed into three rows, the aircraft and
    armored-vehicle rows silently dropped, and a "Caliber Reference" column
    welded on from prose elsewhere. Values right; the *object* is a
    construction, and a reader citing it would never find the aircraft row
    beside it.
1. **The caliber references drift.** Page: ".22 long bullet" → extraction:
    ".22 Long Rifle equivalent", a cartridge designation the page never uses.
    Page: "sufficient to penetrate body armor", "7.62 full metal jacket or
    .30-06 armor piercing bullet" → extraction: "Armor-penetrating level".
1. **The velocity-decay figure is re-derived, not quoted.** Page: kinetic
    energy "down to 10% of its original value". Extraction: "~1/9 of muzzle
    value" — the square of the stated 1/3 velocity ratio, i.e. 11.1%. The
    extractor's arithmetic presented as the source's number.
1. **The worked example is transcribed lossily** — both answers kept,
    `A = 1 m²` and `Pk|hit = 0.8` dropped. Those are the two numbers that make
    it closable at all. This is the ordnance-1944 failure in miniature: a
    summary that keeps the conclusion and discards the fields identifying what
    it was computed from. Had they been kept, §23c would have been available to
    any earlier pass.
1. **The page never mentions 79 J or 80 J** — confirmed by targeted re-fetch.
    See next.

### 23f · A whole argument attributed to a source that does not make it

`fas-es310-damage-criteria.md` carries a section "Implications for 79 J
Threshold", a Key Findings bullet leading "not 79–80 J", and a Summary clause
about "making the 79–80 J fixed threshold appear conservative". **None of it is
on the page.** It is a comparison between this source and a threshold used
elsewhere in the repo, written into the reference document as though the DoD
had made it.

The comparison may be correct — this ledger does not adjudicate it. What is
wrong is its *location*. A @modeler or @model-reviewer reading this card
inherits it as a premise instead of reviewing it as an argument. That is the
Tolch "Drag Model Relevance" defect exactly (Phase 2.5d), and it confirms 2.5d
is chasing a real class rather than a suspected one: **two of two sources
examined for interpretive contamination had it.**

Note it is load-bearing downstream — `_limitations.qmd` §374-396 turns on the
same ES-310-vs-78.6 J criterion mismatch — so relocating it must not mean
losing it.

### 23g · The remaining seven, adjudicated

After ES-310 closed, the sweep reads: **25 documents, 11 carrying unchecked
numbers, 7 cited, and — the number that matters — 0 reaching `src/` or `app/`.**
ES-310 was the last unchecked source with a path into shipped code.

| Document                                                            | Cited by                                                                      | Numbers taken?                                                                        | Outcome                                                                                                                            |
| :------------------------------------------------------------------ | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- |
| `fragmentation/fragment-size-distribution-conwep` (= **Gold 2017**) | `mott-fragment-shape-closure` ×3, `mott-scale-gap`, `fragmentation-field.qmd` | **yes — equations (2)/(4)/(6)/(7)≡(16)**, which `fragmentation.py:309-318` implements | **BLOCKS Phase 3.** Needs a card with greppable anchors. Every citation is a bare line number (`:58-60`, `lines 70-76`, `line 78`) |
| `wound-ballistics/aep-55-vol3`                                      | `_limitations.qmd`, 4 update docs                                             | **no** — cited only for what it does *not* contain                                    | Non-citable-for-numbers; no re-baseline needed. But see the stale-claim finding below                                              |
| `wound-ballistics/cunniff-2014`                                     | `pkill-poisson-field/scoping.md`                                              | **no** — same shape as AEP-55                                                         | Non-citable-for-numbers                                                                                                            |
| `fragmentation/ada462991-fragment-velocity` (Gold 2007)             | `fragmentation-field.qmd`, `target-area-profile/scoping.md`                   | source-table entry + narrative; 4 images, no CSV                                      | Deferrable — no Phase-3 thread reads it                                                                                            |
| `ww2-shells/ammunition-series-6-steel-composition`                  | `wdss1-steel-grade` ×2                                                        | yes (3 rows)                                                                          | Still open from §11 — the one §11 document that has not closed                                                                     |
| `wound-ballistics/britishartillery-wt-of-fire`                      | `_validation.qmd`                                                             | yes (4 rows) — reaches a **published surface**                                        | Deferrable; live web page, so re-fetchable like §21                                                                                |
| `wound-ballistics/lethality-threshold-critique` (Fackler 1987)      | `target-area-profile/scoping.md`                                              | yes (3 rows)                                                                          | Deferrable; live web page                                                                                                          |

**Latent, uncited, no artifact rests on them today** — recorded, not
re-baselined: `azom-steel-grades/aisi-1020`, `azom-steel-grades/aisi-1045`,
`fragmentation/ml-warhead-fragmentation` (54 images), `ww2-shells/nwc-tp-7124`.
If any is ever cited, it enters the gate first.

### 23h · A contradiction between surfaces, found in passing

`_limitations.qmd:239-240` states that Cunniff (2014) and AEP-55 Vol. 3 "are
**not** present in `doc-reference/`". Both directories exist and have for some
time. `pkill-poisson-field/scoping.md:75-81` has the correct account — both
*are* collected, and neither carries a quotable man-silhouette scalar, which is
a different and weaker claim than absence.

The `0.85 m²` convention is unaffected either way; what is affected is a reader
of the published limitations page being told to go find two documents that are
already in the repo. Registered, and it belongs to Phase 6.

### 23i · Status

**Phase 2.5c is closed for the shipped-code question and open for two
documents.** ES-310 re-baselined: `card.md` written (there was none), two CSVs,
two `.invariant` files, one retained script. `check-table-invariants.py doc-reference/ --all` → **0 / 26 tables failed**.

**Superseded by §24.** Gold 2017 (`fragment-size-distribution-conwep`) was the
one remaining Phase-3 blocker with real numeric exposure — closed in §24a once
the user supplied the scan. `ammunition-series-6-steel-composition` remains open
from §11; it is uncited, so it gates nothing.

FINDING\[blocking\]: ES-310's "Implications for 79 J Threshold" section, Key Findings bullet 1 and Summary "79–80 J" clause are not on the source page — it never mentions 79 J or 80 J — so a repo argument is published as a DoD/Navy claim (affects: doc-reference/wound-ballistics/fas-es310-damage-criteria/fas-es310-damage-criteria.md, experiment/fragmentation-field/\_limitations.qmd; since: 2026-08-03)

*(The Gold 2017 blocking finding registered here — no card, no closure, no
retained scan, bare-line-number citations — is closed by §24a; its marker is
deleted per `.claude/rules/deferred-findings.md`. The bare-line-number half
survives as a live deferrable finding on
`updates/mott-fragment-shape-closure/derivation.md:21`.)*

FINDING\[deferrable\]: \_limitations.qmd tells readers Cunniff (2014) and AEP-55 Vol. 3 are not present in doc-reference/, but both are collected; the correct claim is that neither carries a quotable man-silhouette scalar (affects: experiment/fragmentation-field/\_limitations.qmd, experiment/fragmentation-field/updates/target-area-profile/derivation.md, experiment/fragmentation-field/updates/familyA-false-safe-zone/scoping.md; since: 2026-08-03)

FINDING\[note\]: pk_given_hit interpolates ES-310's three anchors in log10(E), a scheme the source never states; at the one point the page works it gives 0.817 against a stated 0.8, where linear-in-E gives 0.767 — agreement on a single point, not a derivation (affects: src/arty/fragmentation.py, doc-reference/wound-ballistics/fas-es310-damage-criteria/card.md; since: 2026-08-03)

______________________________________________________________________

## 24 · The two blockers close — Gold 2017 and AEP-55 Vol. 3

Both scans were supplied by the user on 2026-08-03, in response to §23i naming
them as the outstanding gaps. Both turned out to have clean text layers on
every page, which changes the instrument: as with `sandia-sand92-0243` (§22),
the question "was the right line read?" is answered by *printing the line*, not
by inventing a closure around it. Only one of the two needed more than that,
and it needed it for a reason worth recording.

### 24a · Gold 2017 — the closure had to be algebra, because no surface carries the sign

`fragment-size-distribution-conwep` (the slug is misleading; this is Gold 2017,
*Defence Technology* 13(4) 300–309) supplies no data series. What it supplies is
the PAFRAG-Mott equation chain implemented in `fragmentation.py:mott_params`
and `zones.py:_zone_mott_mu`. So the fidelity question is not *was the right
cell read* but **was the right formula read**.

Everything turns on one character. Eq. (6) is `γ = α^{-2/3} γ′`, and **the
entire content of that equation is the sign**. Take it wrong and μ is off by a
factor of **α²** — 14× to 32× across the break-up velocities this model runs at
— in the direction that makes fragments smaller and more numerous. Two surfaces
could in principle settle it, and neither does:

- **The committed `.md`'s equations are reconstructed, not transcribed.** They
    are LaTeX; the raw text layer contains no LaTeX at all. So the minus in
    `\alpha^{-2/3}` is a **vision model's reading** — the same pipeline Phase 7
    of this audit caught inventing values in table cells. It is the reading
    under test, so it cannot also be the evidence.
- **The raw text layer cannot arbitrate.** It has a clean text layer on all 10
    pages, but it encodes the minus as the unmapped control character `\x04`,
    which it *also* uses for hyphens: `a\x042=3g0` is eq. (6), and
    `the Q\x04angle` is prose "Θ-angle". The same byte, two meanings. Being
    non-printable it is dropped by any printable-character filter, silently
    yielding `α^{2/3}` — the wrong-sign reading, with no glyph-level trace.

**And the extraction-quality gate cannot see any of it, twice over.**
`scan-extraction-quality.py` flags Private Use Area glyphs (U+E000–F8FF). This
font maps its unmapped glyphs into the **C0 control range** instead — 61 in the
text layer, 0 PUA — so the detector's range misses every one. It also runs on
the `.md`, which the vision pass has already laundered to zero control
characters. It reports `0 / 2 file(s) flagged` here.

That is a second structural blind spot in that gate, and it is *not* the same
as the column-inversion one. There the gate saw clean glyphs that happened to
be the wrong cell. Here the reconstruction step **removes the evidence** before
the gate runs: the ambiguity exists only in a surface the gate never inspects.
A green scan on a vision-reconstructed document therefore certifies less than a
green scan on a transcribed one, and nothing currently records that difference
(Phase 8 item 6).

An earlier revision of this section, the card, and the check script all
asserted the simpler and wrong story — "the text layer drops minus signs, so
`α^{-2/3}` and `α^{+2/3}` extract identically". They do not extract identically
(the plus maps to `þ`); the minus is present but unreadable. The verdict is
unchanged because it never rested on that claim, but the correction is recorded
rather than quietly applied: the sharper reading is what exposes the
`scan-extraction-quality.py` consequence, which the wrong one hid.

**The source closes it itself.** Eq. (5) is *stated* to be eq. (2) substituted
into eq. (4), and only one exponent makes that substitution true. Solved
numerically at five values of α, the exponent comes back **−2/3 exactly**,
every time. That is a closure invariant in the sense
`.claude/rules/source-data-fidelity.md` means — arithmetic internal to the
source, from the source's own stated relations, with a pass/fail answer. It
just closes a formula rather than a table, which is a shape the rule's four
listed forms do not cover and probably should (Phase 8).

Verified, all in `checks/gold-2017-equation-provenance.py` (~0.3 s):

| Check                                                                 | Result                                                                                  |
| :-------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| 9 greppable anchors, unique in the extraction and located on the scan | pass, pp. 301–306                                                                       |
| exponent on α required by (2)→(4)→(5)                                 | −2/3, at 5 values of α                                                                  |
| the `.md` reconstruction carries `\alpha^{-2/3}` in both (5) and (6)  | pass — the vision reading agrees with the algebra, which is what promotes it to checked |
| eq. (7) ≡ eq. (16)                                                    | identical to 4 × 10⁻¹⁶ over 7 parameter sets                                            |
| shipped `mott_params` composition vs eq. (4) in one step              | equal to 2 × 10⁻¹⁶ at three V₀                                                          |

**Verdict on the shipped code: admissible.** The three-step composition
(eq. 2 → eq. 6 → eq. 16) reproduces eq. (4) evaluated directly, which it can do
only if `alpha ** (-2.0/3.0)` carries the sign the algebra demands. `zones.py`
uses the identical form.

### 24b · Gold 2017 contradicts itself on N₀, and `src/arty` takes the right side

Eq. (1): `N₀ = M/2μ`. Eq. (17): `N₀ⱼ = mⱼ/μⱼ`. These differ by exactly 2.

Eq. (1) is the self-consistent one — μ is defined two sentences earlier as
**half** the average fragment mass, so total mass over μ counts half-fragments.
`mott_params` uses `M/(2μ)`. At M1 geometry and V₀ = 1000 m/s the two readings
give 3 959 vs 7 918 fragments.

There is nothing to repair. It is recorded because the failure mode here is
*forward*: a future pass that reads eq. (17) off the page and "corrects" the
code to match would double every fragment count, and would be able to cite the
paper for it.

### 24c · Gold 2017 — what is not certified

- **γ = 50 is the shape-absorbed γ of eq. (6), not γ′.** Gold never states α for
    Charge A, so his 50 cannot be back-converted to a γ′. `_validation.qmd:48`
    already reads it correctly — as an un-shape-corrected value, i.e. the cube
    limit α = 1 where γ = γ′ — and declines to score the model against the
    resulting band. **That reading is sound**; the risk is a future pass
    treating 50 as a `SteelParams.gamma`.
- **Figures 1–11 are curves and none is digitized anywhere in this repo.** That
    is the finding for this document's `images/` directory: not that the figures
    were checked, but that nothing rests on them. Any future digitization is a
    fresh job with its own closure — §13b (DoD-1975 Figure 3) is what happens
    when that is done by eye.
- **Nothing about the multi-region model** (eqs. 18–26). The repo uses the
    one-region chain only.
- Table 1 (Charge B recovery, 2 rows) is transcribed to
    `tables/table-1-charge-b-recovery.csv` with the source's own `N/N*`
    normalisation as its closure. **It is cited nowhere**; it exists so the
    document stops reading as "carries numbers, no CSV" and so a future
    consumer reads a file instead of re-typing prose.

### 24d · AEP-55 Vol. 3 — the citation was misdirected, not merely uncollected

The scan settles §23h decisively, and turns it from a bookkeeping error into a
substantive one. AEP-55 (C) Vol. 3 (Part I) is
*Procedures for Evaluating the Protection Level of Armoured Vehicles — IED
Threat*: a **vehicle test standard**. Occupant survivability is assessed by
firing at instrumented **ATDs** (anthropomorphic test devices) and reading
injury-assessment reference values off transducers. A man-silhouette presented
area is not a quantity such a document would ever state, because nothing in its
method uses one.

Searched over all 106 pages for

```
presented area|projected area|silhouette|man-target|standing man|
prone man|frontal area|exposed area|body area
```

— **0 hits** (`checks/aep-55-vol3-scope-check.py`, ~0.2 s).

So the two disagreeing surfaces resolve as:

- **`pkill-poisson-field/scoping.md:75-81` is correct** — both documents are
    collected, neither carries a quotable scalar, 0.85 m² remains an engineering
    convention.
- **`_limitations.qmd:238-242` is stale twice.** It says the references are "not
    present in `doc-reference/`" (both are), and it tells readers to treat
    posture-resolved hit counts as ±25 % estimates "until the references are
    collected" — an instruction that can never be discharged, because collecting
    AEP-55 Vol. 3 cannot supply posture box-body dimensions. §23h registered
    this as a bookkeeping slip; it is worse than that, and it belongs to Phase 6.

**The trap in this document.** It contains exactly two square-metre figures: a
`2 × 2 m²` test bed, and `A = 0.082 m²` on p.85 — the effective area of the
Annex E lumped-parameter **thorax model** (Figure E7), sitting beside a mass, a
spring constant and a lung gas volume. It is a blast-lung chest-wall area, not a
presented area. It is in the right units, within a factor of ~10 of the 0.85 m²
the repo wants, and in the one document the repo names as canonical for that
number. Named on the card so it is not picked up.

### 24e · §19f a third time — the sweep still could not see Gold 2017

Re-running the sweep after writing the card, it reported
`fragment-size-distribution-conwep` as reaching **0 shipped files** — while
`fragmentation.py` and `zones.py` cite it four times between them. The
designator fix of §23a does not help: journal articles are cited **author-year**
("Gold 2017"), and only reports are cited by designator ("ES-310",
"SAND92-0243"). Same lesson, third distinct spelling, and again found only
because the document had been read closely enough to know the answer in advance.

Fixed by deriving `Surname YYYY` / `Surname (YYYY)` keys from the extraction's
front matter (`author_years()`). The effect is not confined to Gold:

| document                            | cited before → after | shipped before → after |
| :---------------------------------- | -------------------: | ---------------------: |
| `fragment-size-distribution-conwep` |               8 → 23 |                  0 → 2 |
| `mil-s-10520d-projectile-steel`     |              64 → 67 |                  8 → 9 |
| `mott-linfoot-1943-…`               |                3 → 4 |                  0 → 0 |

**The standing conclusion from this is about the instrument, not the
documents.** Three times now, an exposure sweep has under-reported precisely
the most carefully written citations — the ones that name a source the way a
human would rather than by directory slug. Any future "is this source cited?"
answer produced by grepping one key form should be treated as a lower bound.

### 24f · Status — Phase 2.5c is closed

`checks/doc-reference-admissibility-sweep.py` after this pass: 25 documents,
10 carrying unchecked numbers, 7 of those cited, and **0 reaching `src/` or
`app/`**. Both Phase-3 blockers named in §23i are discharged.
`ammunition-series-6-steel-composition` remains open from §11 — it is uncited,
so it gates nothing.

`aep-55-vol3` still reads as "unchecked" in the sweep, correctly and
permanently: its extraction carries markdown tables and no CSV, because none of
those tables is cited and none is transcribed. That is the "explicit
non-citable mark" outcome the sweep offers, and the card carries it.

Phase 3 is unblocked for `mott-fragment-shape-closure` and `mott-scale-gap`,
with one carried caveat: their citations into Gold 2017 are still bare line
numbers (registered on `mott-fragment-shape-closure/derivation.md:21`), and the
anchors that replace them are now tabulated on the card.

FINDING\[note\]: Gold 2017 eq. (17) (N_0j = m_j/mu_j) contradicts its own eq. (1) (N_0 = M/2mu) by exactly a factor of 2; src/arty follows eq. (1), which is the self-consistent reading since mu is defined as HALF the average fragment mass, and a future pass that "corrects" the code toward eq. (17) would double every fragment count with a citation to back it (affects: src/arty/fragmentation.py, src/arty/zones.py, doc-reference/fragmentation/fragment-size-distribution-conwep/card.md; since: 2026-08-03)

FINDING\[note\]: the closure that admits Gold 2017 is algebraic, not tabular — the committed .md's equations are vision-reconstructed LaTeX and the raw text layer encodes the minus as a non-printable char it also uses for hyphens, so neither surface settles eq. (6)'s alpha^(-2/3) and only substituting eq. (2) into eq. (4) fixes the sign; .claude/rules/source-data-fidelity.md lists four forms of closure invariant and none of them covers "an equation the source states is a substitution of two others", which is worth adding in Phase 8 (affects: .claude/rules/source-data-fidelity.md, experiment/fragmentation-field/challenges/source-data-audit/ledger.md; since: 2026-08-03)

FINDING\[deferrable\]: scan-extraction-quality.py flags only Private Use Area glyphs (U+E000-F8FF), but Gold 2017's font maps its unmapped glyphs into the C0 control range (61 in the text layer, 0 PUA) and the scanner runs on the .md, which the vision pass has already laundered to zero control chars — so it reports 0/2 flagged on a document whose sign information is unreadable; a green scan on a vision-reconstructed document certifies strictly less than on a transcribed one and nothing records that (affects: src/utils/scan-extraction-quality.py, .claude/rules/source-data-fidelity.md, doc-reference/fragmentation/fragment-size-distribution-conwep/card.md; since: 2026-08-03)

FINDING\[deferrable\]: \_limitations.qmd tells readers to treat posture-resolved hit counts as provisional "until the references are collected", naming AEP-55 Vol. 3 — but the retained scan shows Vol. 3 is an armoured-vehicle IED test standard assessing occupants with ATDs, so it can never supply a man-silhouette presented area and the caveat as written can never be discharged; the correct disclosure is scoping.md's, that 0.85 m² is an engineering convention (affects: experiment/fragmentation-field/\_limitations.qmd, doc-reference/wound-ballistics/aep-55-vol3/card.md; since: 2026-08-03)

## 25 · Phase 2.5d — narrative admissibility: what a card tells you to *do*

The plan's premise: a `card.md` section that tells a reader what to use a
source **for** is a modelling claim wearing a reference doc's clothes, and a
@modeler dispatched to read that card inherits it as a premise. Tolch's "Drag
Model Relevance" is the proven case (§6) — it recommended a drag anchor that is
near-insensitive to drag, and the correction lived only in agent memory.

Every `card.md` in `doc-reference/` was swept. Script:
`checks/card-anchor-claim-verification.py` (0.3 s).

### 25a · The split is structural, and it is not about the documents

Eleven of eighteen cards carry a "Provenance of this card" / "Why this document
is here" section. All eleven were written or rewritten by **this audit**. The
seven that do not are the pre-audit cards: `aisi-1020`, `aisi-1045`,
`dod-1975`, `m49a2`, `ammunition-series-6-steel-composition`, `ordnance-1944`,
`tolch-1938`.

**Every interpretive defect found in this sweep sits in those seven.** That is
worth stating plainly because it says the fix is a *format*, not vigilance: a
card that has to answer "why does this section exist and who checked it" does
not accumulate unsourced recommendations, and a card with no such slot does.
This is the empirical case for Phase 8 item 2, which until now rested on one
example.

The good pattern already exists and should be copied rather than invented.
`explosion-fragment-model`'s **Applicability** section states the transfer
question, names it as a criterion-match question, and routes it to
@model-reviewer — an interpretive section that ends in a *referral* instead of
a recommendation. `mott-linfoot` and `gurney` do the same in "Why this document
is here" / "The facts this document supplies", both anchored and both explicit
about what the source does **not** contain.

### 25b · Four sections assert something the source does not say

| card                                    | section                   | what it asserts                                                                                                                                                                              | exposure                                                             |
| :-------------------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- |
| `aisi-1045`                             | Applications & Notes      | "**This is likely the source of the '45000 psi' baseline figure in the catalog.**" — a provenance *guess*, bolded, with no hedge in the asserted sentence                                    | uncited outside this ledger                                          |
| `ammunition-series-6-steel-composition` | Material Property Targets | three targets, of which two are not the source's: "Elongation: ~10–20% typical for normalized 1035–1045 equivalent" and "Hardness: ~400–500 HB (normalized state; **not stated in source**)" | uncited                                                              |
| `dod-1975`                              | Applicability & Caveats   | a "**Use:**" recommendation, plus "figure **presumably** covers ~0–Mach 7"                                                                                                                   | cited; numeric content already closed                                |
| `m49a2`                                 | Design Intent and Context | "Likely ductile-steel", "most probable" — self-flagged as not confirmed                                                                                                                      | a catalog entry in `src/arty/shells.py`; no model result rests on it |

Two of these self-flag their own weakness ("not stated in source",
"presumably"), which is the correct instinct landing in the wrong file: the
hedge is visible to someone reading the card and invisible to anyone reading
the artifact that cites it.

`dod-1975` is the mildest case and shows where the line falls. Its *numbers* —
$C_D = 1.28$, $L_1 = 247$ — are already closed by
`tables/ballistic-constants.invariant`, which reproduces the decay recipe from
the source's own definitions and is set just tight enough to reject the
adjacent demolition-bomb $k$. What is unverified is only the surrounding advice.
Closure covers the arithmetic; it does not cover the sentence recommending what
to do with it.

### 25c · `m49a2` — unfinished, and low-exposure

`m49a2` is the only one of the four whose speculation touches shipped code, so
its downstream use was traced. The trace is favourable as far as it goes:
`updates/wdss1-steel-grade/derivation.md` (A6) sources the WDSS-1 grade and
composition to *Ammunition Series 6* **Table 6-1** (17 Feb 1953) — "a direct
transcription of the chemistry of record, and the authority for this entry" —
and explicitly downgrades the drawing to corroboration only, on the stated
ground that its material callout "is not legible in the held OCR". The card's
guess was available and was declined.

**That is not a verdict on the card, and this pass does not issue one.** The
m49a2 document work was never finished (user, 2026-08-03), so its card is an
incomplete artifact: the "Design Intent and Context" speculation and the
"Critical Data Gap" section are mid-work state, not a closed position, and
nothing here should be read as signing them off.

What bounds the exposure is *what the shell is*: a recently added catalog
entry, one `ShellParams` row among several, with **no model physics derived
from it** (user, 2026-08-03). It appears downstream only as one row in
`mott-fragment-shape-closure`'s cross-shell sweep — a consumer of the catalog,
not a claim resting on this document. So the unfinished card is **deferrable**,
not blocking: nothing published would have to be retracted if its speculation
turned out wrong, and the one number it might have supplied is already sourced
elsewhere.

One residue to carry into the finish — the derivation attributes "WDSS 1/2 are
the 60 mm mortar-body grades" to the drawing, which the card says is not
confirmed by visible drawing text.

### 25d · The anchors were never right — 20 of 20, in both cards, at birth

`.claude/rules/source-data-fidelity.md` forbids bare line numbers and gives one
reason: they **rot** when a document is re-extracted. Both remaining cards use
them exclusively — ordnance 7, Tolch 13 — so the sweep tested the claim.

The rule's mechanism is not what happened. Re-running each card's anchors
against the revision that *introduced* it (following renames — Tolch was moved
from `tolch-1944-…`, and a rename-blind check silently compares a file to
itself):

| card            | anchors | failing today | failing at birth | source length then → now |
| :-------------- | ------: | ------------: | ---------------: | -----------------------: |
| `ordnance-1944` |       7 |             7 |                7 |              1466 → 1466 |
| `tolch-1938`    |      13 |            13 |               13 |              1715 → 1715 |

Neither source changed length between its birth commit and today, and every
anchor missed in both. The clearest single case: the Tolch card cites
**"9.71 (static) … [table, lines 617–627]"**, and `9.71` has been on **line
900** since the file entered the repo.

**These were not decayed. They were fabricated** — twenty plausibly-formatted
line ranges written alongside the files they point into, none ever checked. No
re-extraction discipline would have caught this, because there was nothing to
decay from, and the greppable-anchor remedy addresses only the failure that did
not occur here. What catches fabrication is *verifying an anchor when it is
written*, which costs 0.3 s for all twenty.

### 25e · Why the labels are wrong too: the `.md`'s `TABLE n` lines are page furniture

§12 records as **blocking** that the ordnance card labels its three shell
sections with a neighbouring shell's table number (43/51/59; correct 38/39,
48/49, 56/57). That finding is confirmed at the page — scan pp. 84 / 89 / 93
show **75 mm HE SHELL, M48 → TABLE 38/39**, **105 mm M1 → TABLE 48/49**,
**155 mm M107 → TABLE 56/57**, with the casualties first rows matching the
committed CSVs cell for cell. This pass adds the *cause*.

The 1944 report prints two tables side by side under one shell title.
Extraction flattens that page into one column and does not keep a heading with
its own table: both page headings emit together, above data belonging to only
one of them. Locating each shell's CSV first row in the `.md` and asking which
`TABLE n` heading last preceded it:

| shell (as printed)    | data at | `.md` implies | page says |
| :-------------------- | ------: | ------------: | --------: |
| 75 mm HE SHELL, M48   |    L392 |      TABLE 43 |  TABLE 38 |
| 105 mm HE SHELL, M1   |    L738 |      TABLE 51 |  TABLE 48 |
| 155 mm HE SHELL, M107 |    L885 |      TABLE 59 |  TABLE 56 |

The middle column is **exactly** what the card asserts, for all three shells.
The card was not guessing — it was reading the nearest preceding heading in the
flattened file, which is a reasonable thing to do and is wrong here.

This disqualifies the obvious remedy. The natural reading of §12's companion
finding — "replace the bare line numbers with greppable strings" — invites
`TABLE 43` as the replacement anchor, which would encode the same artifact in a
form that greps successfully and therefore looks verified. **`ordnance-1944.md`
cannot support table-level citation at all.** The usable anchor is the shell
title (`# 75-MM H.E. SHELL, M48`, L381) — and it must be *checked* rather than
assumed, because OCR damaged one of the three: the 155 mm title reads
`# 155-MM N.E. SHELL, M107`.

### 25f · A correction to this pass's own first reading

This section's first conclusion was that the card's table labels were **right**
and §12's blocking finding was misdiagnosed. That was wrong, and it was wrong
by the same mechanism the section documents: the check trusted "nearest
preceding `TABLE n`" in the flattened `.md`, which is precisely the inference
that produced the bad labels in the first place. The scan settled it against
that reading.

Recorded rather than quietly fixed, because the near-miss is the point. A
plausible mechanical check, run against the convenient artifact instead of the
source, reproduced the original defect and returned a confident verdict that
would have *retracted a correct blocking finding*. The check is only sound
because §12 had recovered the scan; had it not, this pass would have closed a
real defect as a false alarm. That is a sharper argument for retaining source
scans than "go back to the page" as a slogan.

### 25g · Status

Phase 2.5d is **closed**. All four flagged interpretive sections are registered
and none gates a published claim: three are uncited, and `m49a2`'s sits on a
new catalog entry whose one number of interest is sourced elsewhere (§25c). The
`m49a2` document work itself remains unfinished and is carried as deferrable —
it is a shell to finish, not a defect to retract.

The two anchor findings below supersede nothing — §12's blocking label finding
stands as written and is now confirmed at the page with its cause identified.

FINDING\[deferrable\]: all 20 bare line-number anchors in the ordnance-1944 and tolch-1938 cards fail to resolve to the content they claim, and failed identically at each card's birth commit against sources of unchanged length (1466 and 1715 lines) — e.g. the Tolch card cites 9.71 at "lines 617-627" and 9.71 has always been at line 900; these were fabricated at authoring, not rotted, so the greppable-anchor remedy in source-data-fidelity.md addresses a failure mode that did not occur here and the rule should also require an anchor to be verified when written (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md, doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md, .claude/rules/source-data-fidelity.md, .claude/agents/librarian.md; since: 2026-08-03)

FINDING\[deferrable\]: ordnance-1944.md is a flattened two-up scan whose "TABLE n" heading lines do not belong to the data printed beneath them — the nearest preceding heading implies TABLE 43/51/59 for the three shells where the page says 38/39, 48/49, 56/57 — so the file cannot support table-level citation and any repair of the card's anchors must use the shell title line, not a TABLE number, checking it greps because OCR damaged the 155 mm title to "N.E. SHELL" (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/card.md, doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md; since: 2026-08-03)

FINDING\[note\]: three pre-audit cards carry interpretive sections asserting what the source does not state — aisi-1045 bolds a provenance guess that it is "likely the source of the 45000 psi baseline figure", ammunition-series-6-steel-composition lists elongation and hardness targets it marks "not stated in source", and dod-1975 adds a "Use:" recommendation and a "presumably ~0-Mach 7" range beyond what its closed ballistic constants cover; all three are uncited today so they gate nothing, and all three sit in the seven cards lacking a provenance section, which is the case for splitting card.md in Phase 8 item 2 (affects: doc-reference/azom-steel-grades/aisi-1045/card.md, doc-reference/ww2-shells/ammunition-series-6-steel-composition/card.md, doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md; since: 2026-08-03)

FINDING\[deferrable\]: the m49a2-60mm-mortar-shell document work was never finished, so its card.md is mid-work state and must not be treated as adjudicated — its "Design Intent and Context" section speculates on the body-shell material ("Likely ductile-steel", "most probable"); exposure is low and bounded — the shell is a recently added catalog entry with no model physics derived from it (user, 2026-08-03), it appears downstream only as one row in mott-fragment-shape-closure's cross-shell sweep, and updates/wdss1-steel-grade/derivation.md A6 sources the composition to Ammunition Series 6 Table 6-1 instead, explicitly declining the drawing; Phase 2.5d issued no verdict on the card and none should be inferred (affects: doc-reference/ww2-shells/m49a2-60mm-mortar-shell/card.md, experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md; since: 2026-08-03)

______________________________________________________________________

## 26 · Phase 8 — the workflow fixes

Phase 8 was written as six items. Three of them (1, 3, 5) were already done —
each was fixed mid-audit, at the moment it bit, which is worth noting because
it is the pattern that makes the remaining three what they are: **nothing
forced them.** Items 2, 4 and 6 cost nothing to skip in any single pass, so
every single pass skipped them.

### 26a · What the audit added to the phase

Six additions, each from a defect this audit measured rather than anticipated:

| from | addition                                                                           | landed in                          |
| :--- | :--------------------------------------------------------------------------------- | :--------------------------------- |
| §18a | an anchor that straddles a line break is not greppable                             | fidelity rule, `librarian.md`      |
| §18c | provenance gate — a claim attributed to a primary is checked, or marked secondhand | fidelity rule, `model-reviewer.md` |
| §19f | consumer sweeps must grep titles and table numbers, not only slugs                 | fidelity rule                      |
| §19f | `<slug>.md` is not reliably an extraction                                          | fidelity rule                      |
| §20g | invariant DSL had no cross-row handler                                             | `check-table-invariants.py`        |
| §24a | algebraic substitution is a fifth closure form                                     | fidelity rule                      |
| §25d | an anchor is verified when it is **written**                                       | fidelity rule, `librarian.md`      |

### 26b · The DSL gains `tiling:` and `by <group>`

§20g recorded that Tables II and X of MIL-S-10520D carry genuine closures the
DSL could not express — bracket tiling, and monotonicity within a group rather
than down a column — so both had to live in a check script. Both are now
directives:

```
tiling:     projectile_size_class yield_lo_psi yield_hi_psi
monotonic:  coupon_diam_in decreasing by projectile_size_class
```

`table-10-coupon-selection.invariant` declares them, which takes the sweep from
27 tables to 28. Negative-tested by swapping two rows inside one size class:
tiling reports the resulting overlap *and* the gap it opens two rows later, and
the grouped monotonic reports the diameter reversal. Before this, that
perturbation was invisible to `--all` and caught only by a bespoke script.

Grouping is by **consecutive run**, not by key — a group whose rows are not
contiguous is itself the misassignment being looked for, so it must fail rather
than be silently gathered. A blank bracket bound is reported as *unchecked*
rather than passed, per the rule's "absence of a check is a finding".

### 26c · Item 2 — the convention lands, the migration does not

The `card.md` split is written as a **rule**, in the fidelity rule and in
`librarian.md`: a card states what the source says, and a section telling a
reader what to *use* it for belongs in `derivation.md` where @model-reviewer
sees it. @model-reviewer gains the matching check.

**The 18 existing cards are not migrated.** That is a repair, and this audit
defers repairs; it is registered below rather than done. What changes today is
that the next card written cannot legitimately reintroduce the defect, and a
reviewer now has standing to reject one that does.

The safe shape is worth stating because one card already has it:
`explosion-fragment-model`'s Applicability section states its transfer
question, names it as a criterion-match question, and **refers** it — an
interpretive section ending in a referral rather than a recommendation.

### 26d · The rule grew, then was cut back

`source-data-fidelity.md` went 97 → 220 lines before being compressed to 189.
It is imported into every session, and it was becoming the largest rule by 40%
while `.claude/incidents.md` — the file that exists precisely to hold this
material and is *not* loaded — stayed at 130 lines.

The evidence moved there as four sections (`fabricated-anchors`,
`card-as-modelling-claim`, `secondhand-attribution`, `laundered-glyphs`),
leaving one-line consequences and links in the rule. This is CLAUDE.md's own
stated convention and the pass had been quietly violating it: writing the
evidence inline reads as thorough and costs every future session context for
material almost none of them need.

`fabricated-anchors` also records §25f — the near-miss where a mechanical check
run against the convenient artifact instead of the source nearly retracted a
correct blocking finding. That belongs in the incident file, not only in this
ledger, because it is the argument for the rule and not merely a note about
this pass.

### 26e · Item 6 — the scanner now says what it cannot see

`scan-extraction-quality.py` had **no module docstring at all**, and its
`--help` described what it flags without saying what a pass does not mean. Both
now carry it, so the disclaimer reaches someone reading the tool rather than
only someone reading the rule. Two limits are named concretely: the flagged
range is PUA-only and misses C0-mapped glyphs, and a vision-reconstructed `.md`
has been laundered before the scanner sees it.

### 26f · Status

Items 1, 3, 5 were already closed. Items 2 (convention), 4 and 6 are closed
here, with 2's migration registered as deferred. All six audit additions are
landed. `check-table-invariants.py doc-reference/ --all`: **0 / 28 failed**.

FINDING\[deferrable\]: the card.md split is now a rule but the 18 existing cards are not migrated — four carry interpretive sections asserting what their source does not say, and none of the seven pre-audit cards has a provenance section; the convention binds new cards only until this migration runs (affects: doc-reference/, .claude/rules/source-data-fidelity.md; since: 2026-08-03)

## 27 · Findings backfill — is any modelling pass sitting on a blocked item?

The register (`OPEN-FINDINGS.md`) is generated from in-file markers, and
markers only exist where someone wrote one. Every finding in it so far was
raised **by this audit**. The reviews that predate the register — twelve
`review.md` files, going back to 2026-06-20 — tagged their findings
Blocking / Deferrable / Note in prose and never emitted a marker, so none of
them routes to a future dispatch. This pass reads all twelve and asks the
narrow question the user posed: **is a modeller working on top of something
that is actually blocked?**

### 27a · Method, and the Gate-3 line

Closure was judged on **whether a record of closure exists** — a later review
pass, a change-log entry, a logged limitation, a test that now exists, a code
comment naming the fix — never on whether the physics is right. Reading
`src/arty/` to adjudicate a correctness question is `agents-routing.md` Gate 3
and belongs to @modeler; confirming that a named guard, test, or wording is
*present* is navigation and is not. Where no record exists, the item is
registered open and routes to a dispatch rather than being adjudicated here.

### 27b · Result — no pass is blocked

**One FAIL verdict exists in the whole history**
(`familyA-false-safe-zone/review.md:3`, the `z_rep = z_lo` boxed fix), and it
is closed: the re-review at line 303 reads "Blocking finding — resolved,
verified independently", having reimplemented the correction rather than
reading the modeller's. Every other verdict across the twelve files is PASS or
PASS-with-limitations — which `model-reviewer.md` defines as terminal, closed
by logging the limitation, not by a re-review.

So the answer to the question is **no**: nothing in the modelling backlog rests
on an unresolved Blocking review finding. The twelve blocking entries now in
the register are all *source-data* findings raised by this audit, and those are
exactly what Phase 2.5 gates.

### 27c · Per-finding disposition

| review                                                                                                              | line     | tag           | disposition                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------- | -------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `familyA-false-safe-zone`                                                                                           | 55       | Blocking      | closed — re-review line 303, independently verified                                                                                                                                      |
|                                                                                                                     | 142, 166 | Deferrable    | closed — "both addressed" (line 323)                                                                                                                                                     |
|                                                                                                                     | 446      | Deferrable    | closed — `tests/test_familyA_false_safe_zone.py:241` now exists                                                                                                                          |
|                                                                                                                     | 471      | Note          | closed — `zones.py:547` carries the harmonisation comment                                                                                                                                |
| `pkill-poisson-field`                                                                                               | 266      | Deferrable    | closed — `derivation.md` §4.7 names the review as the citable artifact                                                                                                                   |
| `field-builder-performance`                                                                                         | 46       | Deferrable    | closed in code — vectorised bounds guard at `zones.py:850`, `fragmentation.py:994`                                                                                                       |
| `target-height-intercept`                                                                                           | 84       | Deferrable    | closed — `derivation.md:251/261/420` carry the corrected "λ diverges as ~1/r" wording                                                                                                    |
| `drag-gap-1944`                                                                                                     | 70       | Deferrable    | closed — `b-vs-range.qmd:55` and `b-vs-range.md:66` now state `E_LETH_DEFAULT` = 1000 J and the 58 ft-lb value as an explicit override                                                   |
|                                                                                                                     | 267      | Deferrable    | closed — `_limitations.qmd:397` carries the cancellation-not-validation reading                                                                                                          |
| `legacy-field-shell-axis-fix`                                                                                       | 82       | Deferrable    | closed by supersession — `_shell_axis` was renamed `_forward_shell_axis`; the tests import the new name                                                                                  |
|                                                                                                                     | 123      | Deferrable    | closed — `test_familyA_false_safe_zone.py:381` is the point-vs-vec equivalence test the finding asked for                                                                                |
| `frag-field-3d-geometry`                                                                                            | 151      | deferred list | CRH-6.0 and $R_{50}$-recalibration entries are in `_limitations.qmd:226/243`; the $\mu^z$ unit check and the $\gamma$ notation collision are derivation-internal with no rendered output |
| `target-area-profile`                                                                                               | 86       | Deferrable    | **open — marker written**                                                                                                                                                                |
|                                                                                                                     | 131      | Deferrable    | **open — marker written**                                                                                                                                                                |
| `wdss1-steel-grade`, `mach-dependent-fragment-drag`, `mott-fragment-shape-closure`, `lethal-fragment-density-field` | —        | —             | all verdicts PASS / PASS-with-limitations; their live defects are already registered by this audit (γ-column, Gold-2017 secondhand attribution, bare-line anchors)                       |

### 27d · The two that were open

Both sit in `target-area-profile`, and both are documentation-scope, not wrong
numbers:

- **The disclosed error bound does not cover the exposed range.** §4.1.2's note
    keeps a $\sin\Theta$ factor "to match the §6.5 belt-Jacobian notation" and
    bounds the resulting deviation at "< 3.5 %" — correctly, *for the
    $\delta \le 15°$ it states*. The deviation is $1/\sin(90° - \delta) - 1$,
    which reaches ~15.5 % at $\delta = 30°$, and 30° is what the app's
    belt half-angle slider exposes (`app/sensitivity.py:131`). A bound stated
    for a narrower range than the surface it governs reads as a bound.
- **The aspect's own required validation was never built.** `scoping.md` §4.3
    and `derivation.md` §7 item 7 both specify a $\gamma$-sweep of $A_p$ plus a
    ground-vs-airburst hit-count ratio; only the $\gamma = 0$ and
    $\gamma = \pi/2$ endpoints exist. The derivation already carries a
    **Status (open, logged 2026-07-19)** paragraph saying so — which is the
    better half of the fix, since a reader of the derivation sees it — but with
    no marker it never reaches the register and never routes to a pass. That
    gap between "documented in the affected file" and "routed to a dispatch" is
    precisely what `.claude/rules/deferred-findings.md` exists to close.

### 27e · What the backfill says about the register

The twelve pre-register reviews produced **two** live findings between them,
and both are presentational. That is a good result for the modelling work and a
poor one for the inference anyone would draw from an empty register: the
reviews were not silent, their findings simply had no route out of the
document. The marker convention is what changes that going forward; this pass
is the one-time catch-up for everything written before it.

## 28 · Phase 6 — the two unswept reader-facing surfaces

Phase 6 lists stale claims on published surfaces; it does not repair them. Of
the four surfaces it names, `_limitations.qmd` and `_parameters.qmd` had already
been swept incidentally — the audit kept landing on them, and eight register
entries name them between them. `_validation.qmd` (183 lines) and
`challenges/README.md` (34) had **zero** entries and had never been read against
the audit's findings. This section is that reading. The rendered
`fragmentation-field.html` is absent from the worktree, so that bullet of the
plan is moot until someone re-renders.

The distinction from §27 matters: §27 asked whether a *reviewer* flagged
something that never routed. This asks whether a *published claim* still asserts
something the audit has since falsified. Nobody flagged these — they went stale
underneath, which is exactly why no marker existed to find.

### 28a · `_validation.qmd` — four stale or unsupported claims

| where              | claim                                                                  | status                                                                                                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Check 7 (L175)     | "1944 US Ordnance Dept. casualty tables (**Tables 43/51/59**)"         | **stale** — 43/51/59 are a neighbouring shell's numbers throughout (correct: 38/39, 48/49, 56/57). The existing blocking marker was extended to name this surface rather than opening a second one.                                                           |
| Check 7 (L176–181) | "**Verdict: FAIL** … Family B over-predicts $B(r)$ by roughly 7–34×"   | **verdict-pending** — the comparison read the perforation column while applying the 58 ft-lb casualty criterion. Both the multiplier and the FAIL rest on it. Phase 3 rules.                                                                                  |
| Check 6 (L97–100)  | `E_ref = 79.0` J, "a convenient reference point"                       | **note** — ES-310's "79 J threshold" section is not on the source page (registered blocking). The check disclaims it in-line as "not the model threshold", so nothing numeric rests on it; the surface merely echoes a number whose provenance is fabricated. |
| Check 3 (L48–56)   | Gold (2017) "γ = 50, cube closure" band, and the shape-closure numbers | **verdict-pending** — touches the registered Gold 2017 findings (eq. 17 vs eq. 1 factor-2, the secondhand Mott attribution). Belongs to the `mott-fragment-shape-closure` Phase 3 pass, not to this sweep.                                                    |

### 28b · `_validation.qmd` — two asserted checks with no admissible source

Both are new. Neither was reachable from the source inventory, because the
inventory was built by grepping the two audited sources and these cite neither.

- **Check 1 asserts against a source that is not in `doc-reference/` at all.**
    The 900–1 400 m/s Gurney bracket is attributed to *Carlucci & Jacobson,
    Ballistics: Theory and Design*, Table 5-1. `grep -rli carlucci doc-reference/`
    returns nothing. The check ends in `assert in_bracket`, so a rendered PASS on
    a reader-facing surface rests on a bracket that cannot be checked against any
    page this repo holds.
- **Check 5b asserts against a document with no card, no CSV and a known
    extraction defect.** `doc-reference/wound-ballistics/britishartillery-wt-of-fire/`
    contains exactly one file — the bare `.md`. No `card.md`, so it was never in
    the 18-card sweep; no `tables/`, so its 58 ft-lb datum is read off prose; no
    closure invariant. The surface *itself* documents the extraction defect —
    "the same source's extraction renders '1/8 oz' as '~28 grams'" — and then
    asserts against that source anyway.

The pattern worth naming: both slipped through because an audit scoped by
*source* cannot see a claim whose source was never collected. The absence is the
defect, and only a sweep of the surface finds it.

### 28c · `challenges/README.md` — the index publishes a settled verdict on inverted evidence

One row, and it is the first thing a reader meets:

> `drag-gap-1944/` — **Closed** → `updates/mach-dependent-fragment-drag/`;
> residual sits at the geometric ceiling, not chased further

That closure is commit `b6a1730`, which rests on the b-vs-range checks that read
the perforation column. An index asserting **Closed** and "not chased further" on
that evidence is a published claim of settledness, so it is marked `blocking`
rather than deferrable — a reader is being told the question is answered. The
`mott-scale-gap` row's **Resolved** is verdict-pending on the same Phase 3 pass
that covers Gold 2017.

The file's closing paragraph — the two lost `mott-scale-gap` scripts — is
accurate, already recorded, and left alone.

### 28d · What Phase 6 cannot close yet

Everything above is either registered or verdict-pending. The verdict-pending
rows need Phase 3, which is now running: a claim like "Closed at the geometric
ceiling" goes stale only once the re-run rules on it, and writing that half now
would mean guessing the verdict the pass exists to produce.

## 29 · `britishartillery-wt-of-fire` — the source under Check 5b's assert

Phase 6 §28b flagged this document as asserted-against but never collected. The
@librarian pass that followed carded it. The result is worse than the flag
assumed, and it is the audit's first source to terminate in the **unverifiable**
state that `.claude/rules/source-data-fidelity.md` provides for.

### 29a · Verdict: unverifiable, and internally broken twice

The primary — **AORG Report No. 179**, "Lethal and Material Effects of Gunfire
and Bombing on Land Targets" (20 March 1944), updated by No. 234 — did not
surface in web search or public archives, and no `source.pdf` is retained. The
only available surface is a secondary web summary
(britishartillery.co.uk, Nigel F Evans). So there is no page to go back to, and
the two defects below cannot be adjudicated — only recorded.

**Defect 1 — the mass conversion.** The source reads "a fragment of 1/8 oz
(~28 grams)". 1/8 oz is 3.54 g; 28 g is a full ounce. `_validation.qmd` already
caught this one and takes the oz figure as authoritative, which is the right
call but an *unchecked* one — nothing available says which figure is the typo.

**Defect 2 — a stated total that does not sum, and the librarian missed it.**
Under the anchor `### Example Fragmentation Pattern (25-pdr)`, four disjoint
mass bands spanning `<1/25 oz to >2 oz` are given against a stated total:

| Band             | Count      |
| ---------------- | ---------- |
| >2 oz            | \<19       |
| 1/4–2 oz         | ~300       |
| 1/25–1/4 oz      | ~600       |
| \<1/25 oz        | >1,122     |
| **Sum**          | **>2,041** |
| **Stated total** | **~1,140** |

Off by ~1.8×; the dust band alone nearly equals the whole. This is the "a
stated total equals the sum of its parts" invariant, and the table fails it.

The pass returned "No CSV-worthy table suitable for closure invariant —
empirical aggregates lacking … stated totals," on a table that states its total
on the line above the bands. That is the miss the rule anticipates: a claim that
**no closure invariant exists is a finding flagged for human review, not a
pass**. The mechanical half is safe for a cheap model; *concluding there is
nothing to check* is not mechanical, and this is the evidence.

### 29b · What it does to Check 5b

Check 5b consumes two numbers — 3.5 g and 58 ft-lb (78.6 J) — and hard-`assert`s
that retained KE at 61 m lands within a factor of 2 of the second. Neither
number is shown to be wrong: 3.5 g is the correct conversion of the oz figure,
and the 58 ft-lb criterion sits in a different section from either defect.

**So this is not a void verdict — it is a provisional one.** What fails is the
surface's framing. `_validation.qmd` calls the datum "*independent*" and renders
a PASS from an `assert`, which publishes a degree of checkedness the source
cannot support. Registered blocking, at `_validation.qmd` Check 5b: downgrade
the assert to a reported comparison, or obtain AORG 179.

The distinction matters for the redo. Phase 3's b-vs-range result voids a
verdict because the *data* was wrong. This one leaves the numbers standing and
removes their warrant — a different repair, and a cheaper one.

### 29c · What was fixed in place

`card.md` was rewritten from the librarian's draft: both defects recorded under
`## Known Defects` (Defect 2 newly found here), all seven bare line-number
anchors replaced with greppable strings and each one `grep`-verified against the
stored `.md` at authoring, the fragment-count table marked not-citable rather
than transcribed, and an `## Admissibility` section stating the unverifiable
verdict and its one live consumer. No `tables/*.csv` was written — the only
table with a closure structure fails it, and transcribing it would propagate a
broken series.

## 30 · Phase 3 — `mott-fragment-shape-closure`, and a finding that partly reverses

The second Phase-3 thread to rule. Unlike b-vs-range, this one **overturns the
audit's own blocking finding**, and it is worth recording why the finding was
wrong, because the error is instructive.

Verdict: `experiment/fragmentation-field/updates/mott-fragment-shape-closure/rebaseline-verdict.md`.
Evidence: `.../checks/mott-1947-gamma-column-strain-reading.py` (0.06 s, reads
the CSV).

### 30a · The column closes — on three rows of four

The blocking finding said Mott 1947 p.308's γ column "does not reproduce from
the paper's own stated closure … the formula is flat (spans ×1.20) where the
printed column rises ×3.35". That was true of the two readings of `s_F` that had
been tried, and the finding generalised it to the closure itself.

The page tabulates **reduction in area**, not `s_F`, so how RA maps to the strain
factor is a free choice the page never fixes — and the choice decides the
answer. Reading `s_F` as the engineering fracture strain at constant volume,
`RA/(1−RA)`:

| row     | computed | printed |    residual |
| ------- | -------: | ------: | ----------: |
| iron    |     20.6 |      20 |      +3.2 % |
| 0.1 %C  |     41.1 |      42 |      −2.0 % |
| 0.25 %C |     52.9 |      53 |      −0.3 % |
| 0.45 %C |     55.9 |      67 | **−16.5 %** |

Three consecutive rows to ≤3.2 % on a formula with no free parameter is not
coincidence. The column **is** computed from the tabulated `P_2`, `P_F` and RA.
Verified here independently of the pass that produced it: the four residuals
were hand-computed off `section3-gamma-vs-composition.csv` before the script was
run, and match to the digit.

The 0.45 %C row is then indicted twice more, on evidence that does not depend on
that fit at all: its tabulated `P_2` = 38 breaks the column's own monotone rise
(34, 42, 45, **38**), and `P_2` = 45.5 — a monotone continuation — reproduces the
printed 67 exactly; and the paper's own stated length law *rises* at 0.45 %C
where the printed column requires it to fall.

### 30b · The generalisable lesson

**A closure failure localises where a table may be trusted; it does not condemn
the table.** The correct response to one failing row of four is a per-row
verdict — use the rows that close, refuse the row that does not — which is how
`.claude/rules/source-data-fidelity.md` already reads its monotonicity and
tiling forms (per *group*, not per table). The finding as written skipped that
step and went straight to "the series is unsupported".

Second lesson, narrower: **"no closure exists" and "no closure I tried worked"
are different claims**, and only the first is a finding. Two readings had been
swept; a third closed. §29a records the mirror-image error on the same day — a
pass concluding "no closure invariant exists" on a table that states its total
one line above its parts. Both are the same mistake in opposite directions, and
both are why the rule flags an absent closure for human review rather than
letting it pass.

### 30c · Verdicts

| claim                                     | verdict     | why                                                                                                                                                                                                                                                   |
| ----------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `γ′` = 47, "US WW2 WDSS1" (shipped)       | **sound**   | interpolated *inside* the 0.1→0.25 %C segment, both endpoints closing; recomputing and re-interpolating gives 46.6 vs shipped 47.1, a 1 % shift, inside its own declared 45–49 band                                                                   |
| `γ′` = 65, "WW2 US HE Shell" (shipped)    | **shifted** | anchored "just under" the one row that fails, with no bracketing row above it; at the recomputed anchor the 0.355 %C interpolation drops 60.4 → 54.5 and the shipped 65 sits *above the entire recomputed series*, inverting its stated justification |
| the shape closure itself (§§1–5, 7.1–7.5) | **sound**   | γ′-independent by construction — nothing in §§1–5 reads the γ column; it enters only through registry values used to *evaluate* the validation tables                                                                                                 |
| anything                                  | **void**    | nothing                                                                                                                                                                                                                                               |

On the shape closure's own validation tables, every *fidelity* check either
holds or improves at a rebaselined `γ′` (the 75 mm `μ` miss against Tolch closes
from 1.20× under the floor to 1.03×; §7.5 Option C ratios move toward 1). The
one claim that weakens is a soft cross-check, registered deferrable in
`derivation.md` §7.4.

### 30d · What changed in place, and what did not

`src/arty/` is **assessed, not changed** — the audit's standing constraint. The
γ′ = 65 re-anchor is a `wdss1-steel-grade` registry question, and only `σ_F/γ′`
is identifiable, so it must be argued as a `σ_F/γ′` move. Registered blocking
against `fragmentation.py`; not fixed here.

Two committed artifacts *were* corrected, because both asserted the now-falsified
generalisation and both are read as premises by a later pass:

- `section3-gamma-vs-composition.invariant` — its "what does NOT hold" section
    stated the closure fails under any reading. Rewritten to the three-row
    closure, the localised 0.45 %C defect, and the consumer rule (bracketed rows
    are sourced; on-or-above the failing row is a working value).
- `checks/mott-1947-gamma-and-length-closure.py` — its C2 residuals are correct
    for the two readings it tests and are kept; the docstring's generalisation to
    "either reading of `s_F`" is marked superseded in part.

The γ = 47 marker in `fragmentation.py` was replaced by a note recording that it
was re-checked and is sound — a closed finding leaves the register by deleting
its marker, and the sound half of this one is now closed.

### 30e · Secondary — the Gold 2017 "Mott (1943)" attribution

Recorded, not applied (the marker stays open until `derivation.md` is edited).
Of the three elements Gold routes through "Mott (1943)": the parallelepiped
idealisation **survives**; the mean cross-sectional area `∝ (r/V)²` is **Mott
1947, not 1943**; and `A ≡ l̄/x̄` constant across shells is **not primary-backed**
— Mott & Linfoot disclaim a theory of fragment length twice.

The *value* `A` = 1.6 is unaffected: it was never Gold's, it is Felix 2022
Table 4 (§16), already cited correctly. What changes is the **status** of
assumption A9.2 — from a caliber-independence assumption on a theoretically
motivated constant, to a purely empirical cross-dataset regularity, licensed by
the framework's *silence* on length rather than by a theory. That strengthens the
±5 % sensitivity note rather than weakening it, since a measured spread becomes
the whole of the evidence instead of a perturbation on a theory.

## 31 · Phase 3 — `mott-scale-gap`, and the re-scope the executed phases force

### 31a · `mott-scale-gap` — the localisation survives its own justification being replaced

Verdict: `challenges/mott-scale-gap/rebaseline-verdict.md`. Three claims ruled.

| Claim (thread artifact)                                                                            | Verdict                        |
| -------------------------------------------------------------------------------------------------- | ------------------------------ |
| `_scale_verdict_ledger.md` §1 — gap real, γ/σ_f **not** the cause, localised to the mass closure   | **sound**, magnitudes re-sized |
| `_shape_closure_check.md` — verdict **NO**, the cube closure is the author's, not the literature's | **sound**, strengthened        |
| `challenges/README.md` — thread published as "Resolved"                                            | **wrong word**, restated       |

The interesting one is the first, and it is a **pattern worth naming**: the
ledger justified γ = 65 by reading Mott's 0.45 %C row — precisely the row §30
indicts — yet the conclusion stands, because the exclusion argument never used
the row. It used the *width* of the admissible γ box (≈1.5–2× on μ). The
rebaseline's move, γ′ 65 → 47, is 1.63× on μ, inside the bound the ledger had
already priced. An argument built on a bracket rather than on a point value
survives the point value being wrong.

Magnitudes do move, and the ledger's §3 table is superseded: μ 0.235 → 0.382 g,
N₀ 12 256 → ≈7 540, residual gap 4–15× → ≈2.5–9×, required shape factor α ≈ 4 →
≈2.5. The strongest evidence is untouched by any of it — the *screening-immune*
heavy-fragment deficit (N(>6 g) = 78 model vs 278 observed, 100× short above
34 g) is a **crossover**, and a γ move is a pure rescale of μ, which cannot
remove a crossover.

### 31b · The status word, and what the pass could not rule

The pass correctly declined to rule whether the α correction had shipped —
its brief forbade reading `src/arty/` — and made the status word conditional
instead. Resolved here: `src/arty/fragmentation.py:320-323` computes
`alpha = shell.aspect_ratio * shell.breadth_factor**2 * t_bu / x0` and applies
`gamma = alpha**(-2/3) * shell.steel.gamma`, i.e. Gold 2017 eq. (6) with α
carried, not set to 1. So the index now reads **"Fix landed — revalidation
open"**, not "Resolved" and not "correction open". Still open either way:
`_shape_closure_check.md` §5's predicted x₀ ≈ 3.9 mm sitting ~3× below Tolch's
recovered breadth (which α cannot absorb), and `_scale_verdict_ledger.md` §4's
unquantified break-up velocity.

**A conditional verdict is the right output from a scope-limited pass.** The
pass was told not to read `src/arty/`; it did not read it, and it did not guess
either — it enumerated both branches and named the fact that selects between
them. That cost one grep to close.

### 31c · Re-scope — what the executed phases do to the phases still pending

The plan's ordering exists so that executed steps can re-aim the ones behind
them. Two executed results re-aim Phase 3's drag thread and Phase 4, in
**opposite directions**, and the distinction between them is the whole point.

**What the b-vs-range re-baseline did NOT invalidate.** The published FAIL is
void and Family B passes (`b-vs-range-rebaseline.md`), so the *gap* that
`updates/mach-dependent-fragment-drag` was spawned to close does not exist. But
that update never calibrated against `B(r)`. It calibrated against **velocity
decay**, using the tables' own `v_fps`/`m_oz` columns — and the re-baseline pass
spot-checked those and found `initial-conditions-155mm-decay.py`'s triples
match the genuine casualties CSV. **That chain's premise is independent of the
column swap and survives it.** Phase 4's originally-planned question — "does
`C_D = 1.28` survive once the velocity-decay comparison uses the casualties
column?" — is therefore largely already answered: it was never on the wrong
column, with one exception below.

**What remains live, and is not affected by the reversal at all.** Two
independent defects still bear on the drag rejection:

1. **DoD-1975 `figure-3-digitized.md`** under-states $C_D$ by up to 0.082
    across Mach 1.0–2.2 (§13b) — eyeballed off a scan, never compared to the
    page, and it is the array that **rejected** the Mach-dependent law
    `src/arty` still ships against. It errs in the direction that *weakened the
    rejected candidate*, so it is a defect that could only have produced a false
    rejection, never a false acceptance.
1. **`drag-coefficient-calibration.py`'s 105mm triple** is an exact match to
    `105mm-m1-perforation-1-8in.csv` — the same column swap, recurring in a
    script the re-baseline pass was not asked to re-run. Registered blocking at
    `b-vs-range-rebaseline.md`. The 75mm and 155mm triples in that same script
    read the correct column, so this is one row of three, not a whole-script
    inversion.

**The re-aimed questions.** Phase 3's `mach-dependent-fragment-drag` thread no
longer asks "does the drag-gap conclusion survive the column correction?" — the
gap is gone and the conclusion was never built on the swapped column. It asks
instead: *the motivation for this update is void, and its rejection of a
Mach-dependent law was decided against an under-stated $C_D$ curve — what
survives?* Phase 4 correspondingly drops the casualties-column question and
keeps the DoD-1975 one, plus the 105mm row.

**Direction of travel is opposite in the two cases, which is why they must not
be merged into one pass.** The b-vs-range reversal *removes* a reason to change
the drag model; the DoD-1975 defect *adds* one. A single pass asked to weigh
both at once will net them against each other; two passes will not.

## 32 · Phase 3 — `count-gap-1938`: the verdict stands, one inference does not

Verdict: `challenges/count-gap-1938/rebaseline-verdict.md`. Of 20 published
claims: **12 sound, 7 shifted, 1 void.** Retained script:
`challenges/count-gap-1938/checks/count-chain-rebaseline.py` (~2 s, reads every
Tolch series from the CSVs, nothing hand-typed).

### 32a · Three transcription corrections, all in the same direction

| Quantity                  | Published | Re-baselined | Effect                               |
| ------------------------- | --------: | -----------: | ------------------------------------ |
| Pit-recovered count       |       803 |      **779** | every `N/803` figure ×1.031 (+3.1 %) |
| Mean recovered mass       |    6.85 g |   **7.40 g** | gap vs 2μ widens 4.3× → 4.66×        |
| Tolch's two-totals spread |      15 % |     **11 %** | the two totals agree *better*        |

All three move the model's over-count **up**, and none moves a row across the
factor-of-2 band. 6.85 g is not reproducible from the table on *either* count
basis, so it was never a 803-vs-779 artefact — it was simply wrong.

A fourth observation the pass made in passing is sharper than any of them:
**recovered metal (5764.3 g) exceeds the model's whole case mass (5755.2 g)**.
On a model-mass basis the pit accounts for 100.2 % of the case, so any
matched-mass comparison is degenerate at the tail — the Tolch-metal basis
(13.29 lb = 6028 g) is the only admissible denominator.

### 32b · The void one, and why it was already broken

§2 Fact 2 inferred that the residual sits in the perforating *fraction*, **not
the population**. The pass built a **threshold-free** test — match cumulative
*mass fraction* between model and pit instead of imposing a mass cut — and the
model still over-counts **2.15–2.70×** on the Tolch-metal basis. A residual
that survives deleting the threshold entirely is by definition not "not the
population".

Note this was **not** a re-baseline casualty. §2's own closing paragraph three
lines below already asserted a "genuine count-chain excess" — a population
term. The inference contradicted its own section before any number moved. The
re-baseline is what made someone build the test that settles it.

**Independently verified by the main agent** before commit, because a void
verdict deserves its own arithmetic: at the finest screen φ = 5764.3/6028 =
0.9562 inverts through φ(u) = ½(u²+2u+2)e^(−u) to u ≈ 0.775, giving
m\* = μu² = 0.793 × 0.60 = 0.48 g and N = 3627·e^(−0.775) = 1671, against the
script's printed 0.48 g / 1672 / 2.15×. The corollary f = 1/√ratio reproduces
all four printed velocity fractions (0.609 / 0.682 / 0.760 / 0.917). It closes.

### 32c · What the pass added that the thread did not have

The threshold-free route turns out to **measure μ directly**. At matched mass
fraction φ, u is fixed, so the model/Tolch count ratio is exactly ∝ 1/μ ∝ V₀² —
no threshold, no drag, no spray geometry in it. That hands sub-candidate C2 its
own parameter: f = 1/√ratio = **0.61–0.92**, which brackets the thread's assumed
f ≈ 0.85–0.9 *from below*.

And the spread of that bracket is set almost entirely by C4 (fuze/base mass
bookkeeping) — the coarsest screen is 6 pieces carrying **15.4 %** of recovered
metal against the model's 3.3 % deduction, and dropping it moves the
threshold-free residual 2.15× → 1.19×. C4 was published as "bounded at 5–10 %,
dismissed as a driver, note only". The dismissal *as a driver* survives; the
bound and the priority do not. **C4 now gates C2** — a reordering the thread
does not state.

### 32d · A pattern across §31 and §32 worth naming

Both threads survived, and in both the conclusion outlived the specific
justification published for it — `mott-scale-gap` because its argument used a
bracket rather than a point value, `count-gap-1938` because its headline never
depended on the pit count that moved. **The re-baseline's yield here is not
overturned verdicts; it is the tests that were built to check them.** Neither
the threshold-free spectrum route nor the μ-measurement corollary existed before
someone had to re-justify a claim they already believed.

______________________________________________________________________

## 33 · Phase 3 — `frag-field-3d-geometry`: a citation that was load-bearing

Verdict file: `updates/frag-field-3d-geometry/rebaseline-verdict.md`.
**3 claim-groups sound, 0 shifted, 1 void.** The sound majority is the expected
outcome and was *shown* rather than asserted — zone mass partitioning, the Q2
base-plate evidence, and the Q3/Q4/presented-area/Mott-Gurney bundle each
consume no re-baselined series. Notably the Q2 base-plate argument already
quoted **15.4 %** of recovered metal on Screen 1, which is what the corrected
`pit-screen-recovery.csv` says, so it needed no adjustment at all.

### 33a · The void one is a provenance defect, not a transcription defect

`scoping.md:65-66` (restated at `:290`, `derivation.md:358`, `:379`) credits
BRL Report 126 — Tolch 1938 — with nose-spray perforating fragments
"averaging 2740 ft/s". That figure is nowhere in Tolch. It traces to
`doc-reference/ww2-shells/nwc-tp-7124/index.md:260`, a **1990** Naval Weapons
Center report, where **1070–2740 f/s** is a *measured range* of fragment
velocity. Three things are wrong at once: the number, its framing (an
"average" where the source states a range), and its attributed source — which
is a 52-year error in provenance.

This is the class of defect the fidelity rule says nothing else catches:
*"the citing paper's extraction is clean, its digits are right, its own
closures pass, and the error is entirely in what it says another paper says."*
No closure invariant on any Tolch table would ever have found it, because the
number was never in a Tolch table. Only checking the claim against the named
primary does — and here the check is a single `grep` that returns nothing.

**It is also the first defect in this audit found by mining a dead pass.** The
first `frag-field-3d-geometry` dispatch exhausted at 15 tool uses with zero
artifact bytes — textbook over-read, and under the harness rule its window is a
liability to be discarded. Discarding the *window* is not the same as
discarding what it *found*: reading its transcript before dropping it surfaced
this lead, and handing the lead to the fresh dispatch is most of why the
re-run landed a 7.9 KB verdict in 9 tool uses. Worth generalising — an
over-read window is a bad thing to resume and a cheap thing to read.

### 33b · What the citation was doing there

The important part is not that a citation was wrong; it is what it was
holding up. `derivation.md` §6's M1 numerical example computes
$V_0^\text{cylinder} = 1578$ m/s against $V_0^\text{ogive} = 578$ m/s — the
*opposite* of what the scoping's own Q1 rationale predicted ("ogive $C/M$
higher → higher ogive $V_0$"). The BRL-126 attribution was the "range-panel
artefact" paragraph that reconciled the two. Strike the citation and the
reconciliation goes with it, so the contradiction is left **unexplained rather
than merely uncited**.

The Q1 recommendation itself (Option A, cylinder Gurney per zone) survives: it
rests independently on the CRH radial-impulse geometry argument at
`scoping.md:87-90`, which cites no re-baselined source. What must be struck or
re-attributed are the corroboration bullets and the whole §6/§7 velocity
narrative.

### 33c · Why the compounding note was escalated to `blocking`

The pass tagged the contradiction `deferrable` — correct on the evidence it was
allowed, since its brief forbade `src/arty/` and from inside the update folder
this reads as two working documents disagreeing. It is not confined to them.
`src/arty/zones.py:14` names this `derivation.md` as its source and
`zones.py:384-385` computes `V0_ogive` and `V0_cyl` via `_zone_gurney`, shipped
as v0.3.0 in `_change-log.qmd` and rendered by `_four-zone-3d.qmd`. So either
the Q1 rationale is wrong or a velocity in shipped code is, and **which is not
known**. `.claude/rules/deferred-findings.md` reserves that call to the human.

Two general lessons, both about scope rather than about drag or geometry:

1. **A scope restriction that makes a pass cheap also caps the severity it can
    assign.** Forbidding `src/arty/` is what kept this dispatch to 9 turns, and
    it is precisely what made a blocking finding look deferrable. The
    restriction was still right — the fix is for the dispatcher to re-tier
    findings on return, which costs one `grep`, not to widen the brief.
1. **The audit keeps finding that its own instrument is the yield.** §32
    recorded that the re-baseline's value was the tests built to re-check
    believed claims; here it is that a routine "does this update consume a
    corrected series?" question, answered honestly per claim, turned up a
    misattribution nobody was looking for.

______________________________________________________________________

## 34 · Phase 3 — `mach-dependent-fragment-drag`: the rejection was not a fair fight

Verdict file: `updates/mach-dependent-fragment-drag/rebaseline-verdict.md`;
evidence `updates/mach-dependent-fragment-drag/checks/mach-law-rebaseline.py`
(4.5 s, reads both columns from the closure-checked CSVs and parses the
superseded eyeballed curve from its own markdown rather than retyping it).
**15 claims: 8 sound, 4 shifted, 3 void.**

### 34a · The comparison that decided it had one free parameter on one side

This is the finding, and it is not about drag. The Mach-dependent law was
evaluated at the *derived* $k$ = 2600 — **zero fitted parameters** — against a
constant **fitted to the very data being scored**. Scored that way the constant
wins, and "Mach dependence buys nothing" followed. Give both laws the same one
scale parameter and the Mach law wins on **both** columns and in **both** bands:

| Comparison                | Mach law | best-fit constant |
| ------------------------- | -------- | ----------------- |
| casualties, all points    | 0.199    | 0.247             |
| casualties, arrival M>0.7 | 0.052    | 0.069             |
| perforation, all points   | 0.036    | 0.045             |

A consistent ~20–25 % reduction in RMS log-residual. Sharper still: on the
casualties column in the lethal band the Mach law with **no** fitted parameter
(0.068) already ties the best *fitted* constant (0.069). C11 — the stated
reason for the rejection — is **void**.

**Shock B is the smaller half.** The corrected Fig-3 curve accounts for only
~10 % of the reversal; the unequal-parameter framing accounts for the rest.
Worth stating plainly, because the DoD-1975 digitization defect is the one that
was already registered as a finding, and it turns out to be the lesser cause.
A wrong number got a finding; a wrong *comparison protocol* got none, and was
the dominant term.

### 34b · The dataset was mixed, and mixed in the worst possible direction

Not "the wrong column" — **both**. 105mm digit-for-digit from
`105mm-m1-perforation-1-8in.csv`, 75mm only 3 of the 10 available casualties
rows, 155mm casualties: 3 + 11 + 11 = the published n = 25, about **44 %**
wrong-column. The compounding fact is the selection: all 33 perforation rows
have arrival M > 0.7, against 21 of 32 casualties rows, so the "lethal-relevant"
subset the verdict leaned on was *preferentially* the wrong column. That is a
criterion-match failure in the `source-data-fidelity.md` sense — the cited data
does not measure the quantity the model computes — not a transcription slip,
and no glyph-level or closure check could have seen it.

### 34c · The decision survives; the reason is replaced

C12 — *do not implement* — is **shifted, not void**. Both laws sit inside the
±10 % fidelity bar (7.1 % vs 5.3 %), so the honest closure is *immaterial at the
stated fidelity target*, with the architectural cost carrying the decision
alone. The pass ruled this conditional on a shipped-code fact it was forbidden
to check; the main agent closed it, and it came back **stronger** than assumed:
`retardation_coeff` (`fragmentation.py:333`) feeds seven call sites that all
evaluate `V0 * np.exp(-lam * s)`, `np.log` appears nowhere in the module, and
the field kernel at `:1210` evaluates `lam[None, :] * s_c[:, None]` — one
broadcast outer product over the entire mass × standoff grid. A velocity-
dependent $C_D$ turns that single exponential into a per-fragment, per-standoff
ODE march. Leg (b) is the dominant cost, not a makeweight.

### 34d · Shock A is void but does not resurrect the old constant

Rescaling the published 7–34 × by the casualties/perforation ratio (1.2–2.25 ×)
still leaves 3–28 ×, so the motive's collapse does not restore $C_D$ = 0.585.
With C1 gone the update's load-bearing leg is **C4**, the geometric
admissibility bound — 0.585 implies $k$ ≈ 25 400 kg/m³, denser than any
plausible fragment — which consumes **no dataset at all** and is therefore
immune to every shock in this audit. C10 (adopt combined 2.674) stands on it.

That is the same shape as §31's `mott-scale-gap` result and §32's
`count-gap-1938` result, now three times over: **the conclusions that survived a
source re-baseline are the ones that never rested on a tabulated number.**
`mott-scale-gap` used the *width* of a bracket, `count-gap-1938` used a
threshold-free mass-fraction identity, and here a density bound. The audit is
steadily converting "this agrees with the data" arguments into "this is
impossible regardless of the data" arguments, and only the latter are holding.

### 34e · Phase 4 is answered by this pass

The re-scoped Phase 4 asked two questions. Both are now ruled and neither needs
a separate `src/arty/` dispatch: the shipped constant survives (C10, on C4's
dataset-free ground), and the rejection of Mach-dependent drag survives **as a
decision** while its **stated reason is void** (C11 void, C12 shifted). What
Phase 4 must still carry forward is the justification now sitting in shipped
code. On `DragParams.C_D` (`src/arty/fragmentation.py:201-203`, greppable
anchor `does not` / `beat this constant`) the comment reads:

> "take the drag coefficient as constant at its supersonic value of 1.28". The
> Mach dependence of its Fig. 3 does not beat this constant on the 1944
> Ordnance velocity-decay data (derivation §5).

The **value is sound** (C10) and must not change. The **second sentence is
false**: on a like-for-like comparison the Mach dependence does beat it, on both
columns and in both bands. It must be replaced by the immateriality argument
(both inside the ±10 % bar; the closed-form λ at `:1210` is what carries the
decision), not deleted — a bare constant with no recorded reason is how this
whole thread started. Note the audit plan cited this comment as
`fragmentation.py:184`; it has since moved to `:201-203`, which is the bare
line-number anchor rot `source-data-fidelity.md` exists to prevent, occurring
inside the audit's own planning document.

FINDING\[blocking\]: src/arty/fragmentation.py:201-203 justifies the shipped C_D=1.28 with "The Mach dependence of its Fig. 3 does not beat this constant on the 1944 Ordnance velocity-decay data", which ledger 34a rules void — given equal scale freedom the Mach law beats it on both columns and both bands; the constant itself is sound (C10) so only the stated reason must be replaced, with the immateriality argument (affects: src/arty/fragmentation.py, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md; since: 2026-08-03)

______________________________________________________________________

## 35 · Phase 5 — independent verification, and what it overturned

Four @model-reviewer passes, split by claim class rather than by thread
(criterion-match; adversarial refutation of the void rulings; provenance;
the Tolch card). Artifacts: `review-criterion-match.md`,
`review-void-rulings.md`, `review-provenance.md` (§1–3).

The headline is that **the verification pass earned its cost by overturning
the audit's own work, twice** — once a ruling this ledger published, once a
finding the main agent had escalated by hand. A verification phase that only
ratifies is indistinguishable from no verification phase.

### 35a · The BRL-126 "2740 ft/s" ruling was right for the wrong reason

§33a ruled the figure **void** on the grounds that it *is not in Tolch at
all* and traces to NWC TP 7124, a 1990 document. That premise is false. The
figure is in Tolch three times — `tolch-1938.md:146`, `:1658`, `:1698` —
as *"the perforating fragments … averaged **27^0 f/s** while that of the
penetrating fragments was **3030 f/s**"*. It is a four-digit number whose
third glyph OCR destroyed, so **a repo-wide `grep` for the literal `2740`
could not see it, and returning nothing was read as proof of absence**.

The void ruling survives, on different and narrower grounds: the figure is
Tolch's **side** spray (the source says three times it was *computed from the
change in the sidespray angle*), not the nose spray, and its companion is
**3030 f/s penetrating** — *faster*, which Tolch attributes to smaller
ballistic coefficients. The scoping inverted that. So the defect is a
criterion mismatch plus an inverted companion, not a fabrication.

**The consequential part is the repair.** §33 prescribed re-attributing the
figure to NWC TP 7124. Carrying that out would have moved a genuine Tolch
side-spray value onto a 1990 document that merely prints overlapping digits —
**the audit would have introduced a second misattribution while closing the
first**, and the new one would have looked freshly verified.

**Lesson (a new one, and it generalises past this audit).** *A negative
provenance claim cannot be established by literal `grep` against an OCR'd
source.* Absence of the string is evidence about the extraction, not about the
document. Where the claim is "the primary does not say this", the check must
run against the retained `source.pdf`, or against a glyph-tolerant search, or
be downgraded to "not found in the processed text". This is the same class as
`#laundered-glyphs`: the extraction looked clean because the damage was one
character wide.

### 35b · `TABLE nn` renumbers between the scan and the extraction

The criterion-match pass flagged that consuming documents cite "Table 43/51/59"
for the casualties series while the six `.invariant` files anchor "TABLE
38/48/56". **The natural repair — align the invariants to the extraction — is
wrong**, and the main agent had begun it before checking.

`checks/ordnance-1944-page-geometry.py` establishes by *page geometry* (word
x-coordinates on the retained scan, never reading order) that `source.pdf`
prints TABLE 38/39, 48/49, 56/57 — and it passes on every anchor. The
flattened extraction `ordnance-1944.md` prints TABLE 43/44, 51/52, 59/60 above
the very same rows. `checks/ordnance-1944-table-number-anchors.py` confirms the
data is identical (65 of 66 CSV rows appear verbatim in the extraction; the
one gap is the already-known 155 mm r=300 divergence) and that each anchored
`TABLE nn` lands, in the extraction, under a **different shell**.

So the anchors are correct and the surfaces disagree. What is missing is a
warning that `TABLE nn` must never be grepped against `ordnance-1944.md`. This
is the rule's own case — *"a `TABLE n` line is only an anchor if the extraction
kept it attached to its own rows"* — with the twist that here the **PDF** is
right and the derived copy is the liar.

### 35c · A shipped case mass resting on a placeholder

Independent of any re-baseline, the refutation pass found that
`count-gap-1938` compares the model's **case metal** against Tolch's **shell
plus fuze**. Tolch's own weight row closes exactly and settles the basis
(`tolch-1938.md:232`):

```
12.50 (loaded unfuzed) - 1.56 (TNT) + 2.35 (M39 P.D. fuze) = 13.29 lb   ✓
```

so case metal is 10.94 lb = **4962 g**. Shipped `src/arty/shells.py` implies
6.622 − 0.6668 − 0.200 = **5755 g**, because `mass_deductions = 0.200` kg is a
self-declared *placeholder* against a stated fuze weight of 2.35 lb (1066 g).
The model is **~16% high**, not the 4.5% low the thread recorded — the sign
flips with the basis. `N0 = M_case / 2μ` carries this into every fragment
count. Note also the fuze is Tolch's **M39** P.D.; the code comment names an
"M48 PD fuze", which is the *shell's* designation.

### 35d · The Tolch drag anchor is exactly degenerate, not merely weak

The card's "Drag Model Relevance" section recommends the velocity-sweep density
collapse as the drag-calibration anchor. The standing correction (in agent
memory for years, then in `tolch-1938-panel-distance.md`) called that axis
"near-insensitive" to drag. The provenance pass sharpened it to **exact**: at
fixed panel radius, `exp(-R/L(m))` is independent of the shell's remaining
velocity, so it folds entirely into the fitted marking threshold and the
collapse curve is *invariant* under any rescaling of `C_D·C_shape`. The source
itself attributes the collapse to vector addition (`:853-857`) and attributes
the **distance** axis to air resistance (`:804`) — the card recommends the
first and never mentions the second.

The card also anchors this table at `tolch-1938.md#L617-L627`, which is a bare
line-number anchor landing on solid-angle prose and OCR noise — verified, not
inferred — and that markdown surface misprints two cells of the very table the
card calls "high-confidence" (Panel B at 2130 f/s: **3.12** vs the CSV's
**1.12**; Panel C at 1085 f/s: **0.65** vs **0.85**).

### 35e · What the four passes did to the audit's own confidence

| Pass             | Ratified                                                            | Overturned                                                          |
| ---------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| criterion-match  | all three consuming artifacts PASS                                  | — (both its conditionals closed by arithmetic)                      |
| refute-the-voids | C11 upheld on *stronger* grounds; count-gap Fact 2 upheld, narrower | the BRL-126 premise **and** its prescribed repair                   |
| provenance §1–2  | Gold eq. (6) substitution closes                                    | DoD-1975 CSV row at Mach 1.00; two card-as-modelling-claim sections |
| provenance §3    | —                                                                   | the Tolch drag anchor, upgraded to *exactly* degenerate             |

The converging pattern noted at §30/§31/§34 now has a counterpart on the
verification side: **every ruling that survived Phase 5 unchanged was one that
rested on an identity or a closure, and every ruling Phase 5 moved was one that
rested on a search returning nothing.** Absence-of-evidence is the audit's
weakest instrument, and it is the one it reached for most cheaply.

FINDING\[blocking\]: src/arty/shells.py:58-60 gives 75mm M48 mass_deductions=0.200 kg as a self-declared placeholder, but Tolch 1938's own weight row (tolch-1938.md:232, closing exactly as 12.50-1.56+2.35=13.29 lb) states the M39 P.D. fuze at 2.35 lb = 1066 g; shipped case metal is therefore 5755 g against the source's 4962 g, ~16% high, and N0 = M_case/2mu carries it into every fragment count (affects: src/arty/shells.py, experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md, experiment/fragmentation-field/challenges/source-data-audit/checks/tolch-case-mass-basis.py; since: 2026-08-03)

FINDING\[deferrable\]: the six ordnance-1944 .invariant files anchor TABLE 38/39,48/49,56/57 which are correct against the retained source.pdf (geometry-verified by checks/ordnance-1944-page-geometry.py) but resolve to a DIFFERENT shell in the flattened extraction ordnance-1944.md, which renumbers the same tables 43/44,51/52,59/60; no data is wrong, but nothing warns a reader not to grep TABLE nn against the extraction (affects: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables, experiment/fragmentation-field/challenges/source-data-audit/checks/ordnance-1944-table-number-anchors.py; since: 2026-08-03)

FINDING\[note\]: two retained scripts disagree on the traced page value of DoD-1975 Figure 3 at Mach 1.00 - checks/dod-1975-figure-3-mach1-gridline-probe.py gives ~1.257 (the value review-provenance.md quotes) and checks/dod-1975-figure-3-independent-trace.py gives 1.274; both agree the CSV's 1.233 is wrong and that this is the largest residual on the curve, but the size of the correction is not settled (affects: experiment/fragmentation-field/challenges/source-data-audit/checks/dod-1975-figure-3-independent-trace.py, experiment/fragmentation-field/challenges/source-data-audit/review-provenance.md; since: 2026-08-03)
