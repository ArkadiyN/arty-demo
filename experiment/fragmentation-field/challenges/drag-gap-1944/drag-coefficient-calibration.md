# Drag-coefficient calibration check — does a higher combined C_D·C_shape close the velocity-decay gap?

Assessment only (no `src/arty/` changes). Follows up the three
`initial-conditions-{75,105,155}mm.md` findings, which
all show `retardation_coeff`'s velocity decay several-fold too slow vs. the
source's own tabulated `(m(r), v(r))` pairs, and flag `DragParams`'s
`C_D=0.65`/`C_shape=0.90` (combined ≈0.585) as the leading suspect.

Two literature sources give a higher combined drag value for tumbling
fragments of this kind:

- `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md` — combined ≈1.28
- `doc-reference/ww2-shells/sandia-sand92-0243/card.md` — 1.0–1.71, velocity-dependent
    (the report's own parameter-range-list data floor/ceiling, not the "1.2 and
    1.7" prose sentence two paragraphs later on the same page — the audit found
    those disagree and the data-floor number is the one this repo should cite)

This check calls `arty.fragmentation.retardation_coeff` unmodified, substituting
`DragParams(C_D=<combined>, C_shape=1.0)` (the function only ever uses the
product `C_D · C_shape`), against the three calibers' already-tabulated
`(m(r), v(r), V0)` triples, reused verbatim from the three check files.
Script: `experiment/fragmentation-field/challenges/drag-gap-1944/checks/drag-coefficient-calibration.py`.

Candidates tested: current (0.585), 1.0 (SAND92-0243 low end), 1.71
(SAND92-0243 high end).

## Results

`v_model/v_source` ratio at each source-tabulated range point (1.00 = exact
match; >1 = model decays too slowly, i.e. predicts a higher velocity than the
source measured at that range).

### 75mm M48 HE (V0 = 3120 ft/s)

| r (ft) | current (0.585) |  1.0 | 1.71 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.40 | 1.33 | 1.22 |
|    100 |            2.56 | 2.17 | 1.65 |
|    400 |            3.53 | 2.34 | 1.16 |

### 105mm M1 HE (V0 = 3500 ft/s)

Table 51 CASUALTIES triple corrected 2026-08-08 — an earlier version of this
row hand-typed the perforation-of-1/8-in.-mild-steel column mislabeled as
casualties (OPEN-FINDINGS.md blocking finding); see
`initial-conditions-105mm.md`'s "Table-identification correction" and the
casualties CSV. The r-grid changes from 20-300 ft to 20-500 ft.

| r (ft) | current (0.585) |  1.0 | 1.71 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.32 | 1.24 | 1.12 |
|     30 |            1.52 | 1.40 | 1.22 |
|     40 |            1.73 | 1.57 | 1.33 |
|     60 |            2.08 | 1.84 | 1.49 |
|     80 |            2.41 | 2.08 | 1.62 |
|    100 |            2.65 | 2.24 | 1.68 |
|    150 |            3.03 | 2.43 | 1.66 |
|    200 |            3.24 | 2.48 | 1.56 |
|    300 |            3.57 | 2.51 | 1.38 |
|    400 |            3.83 | 2.52 | 1.23 |
|    500 |            4.10 | 2.55 | 1.13 |

### 155mm M107 HE (V0 = 3500 ft/s)

| r (ft) | current (0.585) |  1.0 | 1.71 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.32 | 1.24 | 1.12 |
|     30 |            1.52 | 1.40 | 1.22 |
|     40 |            1.73 | 1.57 | 1.33 |
|     60 |            2.08 | 1.84 | 1.49 |
|     80 |            2.41 | 2.08 | 1.62 |
|    100 |            2.65 | 2.24 | 1.68 |
|    150 |            3.03 | 2.43 | 1.66 |
|    200 |            3.24 | 2.48 | 1.56 |
|    300 |            3.55 | 2.49 | 1.36 |
|    400 |            3.84 | 2.53 | 1.24 |
|    600 |            4.37 | 2.59 | 1.06 |

## Verdict

**75mm.** Raising the combined drag value shrinks the ratio at every range
point tested, but does not close it uniformly: at 1.71 the ratio is 1.22 at
r=20 ft, *rises* to a peak of 1.65 at r=100 ft, then falls back through the
gap to 1.16 at r=400 ft. The model's decay curve has the wrong shape, not
just the wrong scale — a constant bigger drag only happens to cross back near
unity at the longest range tested.

**105mm.** No candidate closes the gap anywhere in the 20-500 ft range now
tested (corrected grid, see above). Even at 1.71 the ratio never drops below
~1.12 (r=20 ft), climbs to a peak of 1.68 at r=100 ft, then falls back to
1.13 by r=500 ft — the same rise-then-fall shape 75mm and 155mm show, not the
monotonic divergence the stale (perforation-table) triple implied.

**155mm.** Same qualitative pattern as 75mm: ratio rises from ~1.1-1.2 at
short range to a peak of ~1.62-1.68 around r=80-150 ft, then falls back
toward unity by r=600 ft (1.06 at 1.71 — the closest any caliber/value
combination gets to a true close). Again the curve shape, not just its
scale, is wrong.

**Overall.** Raising the combined `C_D·C_shape` from 0.585 to 1.0-1.71 is a
step in the right direction — it substantially shrinks the ratio everywhere
— but no single constant value in this range closes the velocity-decay gap
uniformly, either across calibers or across range within one caliber. All
three calibers now show the same rise-then-fall ratio shape (overshoot at
mid-range, approach to unity only at the far range tested) — the 105mm
"no turnover, worst-behaved" reading in an earlier version of this document
was an artifact of the mislabeled perforation triple, not a genuine
caliber-specific difference. A range-dependent residual remains: because
`retardation_coeff`'s exponential decay has one fixed rate, it cannot
reproduce a `v(r)` curve whose deviation from that decay changes sign with
range. This is consistent with the Sandia source's own framing of a
velocity-dependent combined drag (1.0-1.71 by its own data), not a single
constant — closing the gap fully would need a velocity- or range-dependent
drag term, not merely a larger constant one.
