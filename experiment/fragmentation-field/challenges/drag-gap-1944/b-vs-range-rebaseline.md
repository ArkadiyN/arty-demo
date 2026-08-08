# Re-baseline: b-vs-range Family-B check against the corrected CASUALTIES columns

**Context.** `b-vs-range-75mm.py`, `-105mm.py`, `-155mm.py` and their write-up
(`b-vs-range.md`, `b-vs-range.qmd`) hand-typed a `CARD_B` series per shell that
each script's own docstring labels "Table 43/51/59 CASUALTIES." Comparing those
series against the now re-baselined, closure-checked CSVs in
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/`
shows every one of those hand-typed series is an **exact digit-for-digit match
to that shell's `*-perforation-1-8in.csv`**, not its `*-casualties.csv` — the
scripts compared the model (run with the 58 ft-lb casualty energy threshold)
against the perforation-of-1/8-in-mild-steel column. This is the blocking
finding already on record in `OPEN-FINDINGS.md`.

This document re-runs the same comparison, same model, same `E_leth`, reading
the genuine casualties column from CSV
(`checks/b-vs-range-rebaseline.py`, `uv run python experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-rebaseline.py`,
runtime ~2.7 s) and classifies what the published verdict becomes.

## 75mm M48 HE (Table 43 CASUALTIES, genuine)

| r (ft) |   B_model | B_card (old, = perforation) | B_card (new, = casualties) | ratio (new) |
| -----: | --------: | --------------------------: | -------------------------: | ----------: |
|     20 |     0.323 |                       0.106 |                      0.213 |        1.52 |
|     30 |    0.1263 |                      0.0391 |                     0.0809 |        1.56 |
|     40 |   0.06273 |                      0.0192 |                     0.0375 |        1.67 |
|     60 |   0.02191 |                      0.0066 |                     0.0141 |        1.55 |
|     80 |   0.00977 |                      0.0030 |                     0.0064 |        1.53 |
|    100 |  0.004989 |                      0.0016 |                     0.0036 |        1.39 |
|    150 |  0.001289 |                      0.0006 |                     0.0013 |       0.991 |
|    200 | 0.0004322 |                      0.0003 |                     0.0006 |        0.72 |
|    300 | 7.238e-05 |                      0.0001 |                     0.0002 |       0.362 |
|    400 | 1.627e-05 |                           — |                     0.0001 |       0.163 |

(The old table's r-grid ran 20-225 ft in 10 rows, matching the *perforation*
table's grid, not the casualties table's own grid, which runs 20-400 ft in 10
rows — a second symptom of the same column swap: not just the wrong B values,
but the wrong r-grid.)

Factor-of-2 band: **8/10 ranges pass** (r=20-150 ft comfortably inside, r=300
and r=400 fall below 0.5x — the model now *under*-predicts at long range).
Ratio spans 0.163x-1.67x, vs. the published 2.66x-5.3x (old data, current
v0.9.0 drag) or 7x-34x (old data, pre-drag-fix). Both model and true-casualty
curve remain monotonically non-increasing (shape check unaffected).

**Classification:**

- Headline "FAIL, over-predicts by ~3-5x at v0.9.0 drag": **void**. The
    comparison was against perforation counts, which run lower than casualty
    counts at every shared range (mild-steel perforation is a harder threshold
    than the 58 ft-lb casualty energy in the fragment population this model
    predicts) — using the correct, larger casualty denominator brings all but
    the two longest ranges inside the factor-of-2 band, and flips the residual
    sign at long range (under-, not over-prediction).
- "Ratio grows with range": **void**. Under the genuine casualties column the
    ratio *shrinks* monotonically with range (1.67x at r=40 down to 0.16x at
    r=400) — the opposite trend from what was published.
- Shape check (both curves monotonic non-increasing): **sound**, holds under
    either column.

## 105mm M1 HE (Table 51 CASUALTIES, genuine)

|  r (ft) |   B_model | B_card (old, = perforation) | B_card (new, = casualties) | ratio (new) |
| ------: | --------: | --------------------------: | -------------------------: | ----------: |
|      20 |      0.46 |                       0.194 |                      0.231 |        1.99 |
|      30 |    0.1898 |                      0.0816 |                     0.0986 |        1.92 |
|      40 |   0.09929 |                      0.0424 |                     0.0533 |        1.86 |
|      60 |    0.0383 |                      0.0155 |                      0.022 |        1.74 |
|      80 |   0.01875 |                      0.0071 |                     0.0116 |        1.62 |
|     100 |   0.01047 |                      0.0037 |                      0.007 |         1.5 |
| 120/150 |  0.003324 |                      0.0022 |                     0.0026 |        1.28 |
| 140/200 |  0.001342 |                      0.0014 |                     0.0013 |        1.03 |
| 170/300 | 0.0003093 |                      0.0007 |                     0.0004 |       0.773 |
| 200/400 | 9.083e-05 |                      0.0004 |                     0.0002 |       0.454 |
| 300/500 | 3.051e-05 |                      0.0001 |                     0.0001 |       0.305 |

(Row labels show old-grid/new-grid r because the two columns' r-grids diverge
past 100 ft: old (perforation) grid is 20-300 ft in 11 rows; new (casualties)
grid is 20-500 ft in 11 rows — again the wrong grid, not just wrong values.
The published script's own "r=100 column-swap fix" note is moot: it was
patching a single row of the wrong column.)

Factor-of-2 band: **9/11 ranges pass**. Ratio spans 0.305x-1.99x, vs. the
published 2.3x-3.4x (v0.9.0) / 9x-26x (pre-drag-fix). Same shape as 75mm: the
ratio decreases monotonically with range, crossing 1x between r=150 and 200 ft,
under-predicting (not over-predicting) beyond ~250 ft.

**Classification:** same as 75mm on every claim — headline over-prediction
claim **void**, "ratio grows with range" **void**, shape check **sound**.

## 155mm M107 HE (Table 59 CASUALTIES, genuine)

|  r (ft) |   B_model | B_card (old, = perforation) | B_card (new, = casualties) | ratio (new) |
| ------: | --------: | --------------------------: | -------------------------: | ----------: |
|      20 |    0.4786 |                       0.247 |                      0.291 |        1.64 |
|      30 |    0.2047 |                       0.104 |                      0.124 |        1.65 |
|      40 |    0.1109 |                      0.0547 |                     0.0676 |        1.64 |
|      60 |   0.04577 |                      0.0209 |                     0.0283 |        1.62 |
|      80 |   0.02394 |                      0.0102 |                     0.0148 |        1.62 |
|     100 |   0.01426 |                      0.0057 |                      0.009 |        1.58 |
| 120/150 |  0.005308 |                      0.0036 |                     0.0034 |        1.56 |
| 140/200 |  0.002502 |                      0.0024 |                     0.0018 |        1.39 |
| 170/300 | 0.0007803 |                      0.0014 |                     0.0007 |        1.11 |
| 200/400 | 0.0003071 |                      0.0009 |                     0.0003 |        1.02 |
| 300/600 | 6.611e-05 |                      0.0002 |                     0.0001 |       0.661 |
|   400/— |         — |                      0.0001 |                          — |           — |

(Old grid: 20-400 ft in 12 rows, = the *perforation* table's grid. New/genuine
casualties grid: 20-600 ft in 11 rows — one fewer row, longer max range, per
the closure-checked CSV.)

Factor-of-2 band: **11/11 ranges pass** — every tabulated range now falls
inside [0.5x, 2x]. Ratio spans 0.661x-1.65x, vs. the published 1.9x-3.9x
(v0.9.0) / 14x-34x (pre-drag-fix). Same decreasing-with-range trend as the
other two shells, but the whole curve now sits inside the band.

**Classification:**

- Headline over-prediction claim: **void** — this shell now fully **passes**
    the scoping doc's §4 quantitative criterion.
- "Ratio grows with range": **void**, same reversal as the other two shells.
- Shape check: **sound**.

## Verdict on the thread's headline claim

The published verdict — **"FAIL against the factor-of-2 band, for all three
shells... over-predicts by roughly 7-34x, growing with range... a systematic
Family B calibration issue"** — is **void**. It was computed against the
mild-steel-perforation column mislabeled as the casualty column in all three
scripts (confirmed by exact digit-for-digit match between each script's
hand-typed `CARD_B` and that shell's `*-perforation-1-8in.csv`, including the
wrong r-grid in every case past the first ~5 rows). Comparing the same model,
same 58 ft-lb `E_leth` override, against the genuine, closure-checked
casualties columns instead gives:

| Shell         | Ranges in factor-of-2 band | Ratio span    |
| ------------- | -------------------------- | ------------- |
| 75mm M48 HE   | 8/10                       | 0.16x - 1.67x |
| 105mm M1 HE   | 9/11                       | 0.30x - 1.99x |
| 155mm M107 HE | 11/11                      | 0.66x - 1.65x |

At the current (v0.9.0, TP-12-anchored) drag calibration, Family B **passes
the scoping doc's §4 criterion at nearly every tabulated range for all three
shells** — the opposite of the published FAIL. The residual pattern also
inverts: instead of a uniform over-prediction that *grows* with range, the
corrected comparison shows the model *over*-predicting at short range and
*under*-predicting at long range (crossing 1x between roughly 150-250 ft for
75mm/105mm; 155mm stays >0.66x everywhere). The "systematic Family B
calibration issue... most plausibly the binary energy-cutoff... combined with
inverse-square/exponential-drag spreading" explanation built on the void
premise is void with it — the corrected data shows a much smaller, sign-
changing residual, not a one-directional several-fold miss needing a
calibration fix.

The qualitative shape claim (`B(r)` monotonically decreasing in both curves,
no spurious plateau) is **sound** and unaffected by the column swap — it holds
identically on the genuine casualties columns.

**Not re-examined in this pass (out of scope — separate documents/scripts):**
the drag-calibration chain that produced the current v0.9.0 `DragParams`
(`initial-conditions-*.py`, `drag-coefficient-calibration.py`,
`updates/mach-dependent-fragment-drag/`) compares model **velocity decay**
against the tables' own `v_fps`/`m_oz` columns, not `B(r)`, and a spot check
here shows `initial-conditions-155mm-decay.py`'s hand-typed triples match the
genuine `155mm-m107-casualties.csv` (not the perforation column) — so that
chain's premise looks independent of this defect. `drag-coefficient- calibration.py`'s 75mm and 155mm triples likewise match their casualties CSVs,
but its 105mm triple (`r=20..300`, `m_oz` starting `0.035`, `v_fts` starting
`2700`) is an exact match to `105mm-m1-perforation-1-8in.csv`, not the
casualties CSV — the same column-swap defect recurring in a script this pass
was not asked to re-run. Flagging rather than fixing:

FINDING\[blocking\]: 105mm triple in drag-coefficient-calibration.py reads the perforation-of-1/8-in-mild-steel column mislabeled as "Table 51 CASUALTIES" (affects: experiment/fragmentation-field/challenges/drag-gap-1944/checks/drag-coefficient-calibration.py; since: 2026-08-03)

Since the v0.9.0 `DragParams` anchor itself (`c_shape_from_ballistic_density`)
was derived from TP-12's own ballistic-density constant, not from this
calibration script's numeric output, this finding does not by itself put the
shipped `C_shape` value in question — but the calibration narrative in
`b-vs-range.qmd`'s "Follow-up closed" section that cites this script's 105mm
row should be re-examined once that script is corrected.
