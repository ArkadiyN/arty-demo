# Drag-coefficient calibration check — does a higher combined C_D·C_shape close the velocity-decay gap?

Assessment only (no `src/arty/` changes). Follows up the three
`initial-conditions-{75,105,155}mm.md` findings, which
all show `retardation_coeff`'s velocity decay several-fold too slow vs. the
source's own tabulated `(m(r), v(r))` pairs, and flag `DragParams`'s
`C_D=0.65`/`C_shape=0.90` (combined ≈0.585) as the leading suspect.

Two literature sources give a higher combined drag value for tumbling
fragments of this kind:

- `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md` — combined ≈1.28
- `doc-reference/ww2-shells/sandia-sand92-0243/index.md` — 1.2–1.7, velocity-dependent

This check calls `arty.fragmentation.retardation_coeff` unmodified, substituting
`DragParams(C_D=<combined>, C_shape=1.0)` (the function only ever uses the
product `C_D · C_shape`), against the three calibers' already-tabulated
`(m(r), v(r), V0)` triples, reused verbatim from the three check files.
Script: `experiment/fragmentation-field/challenges/drag-gap-1944/checks/drag-coefficient-calibration.py`.

Candidates tested: current (0.585), 1.2 (SAND92-0243 low end), 1.7
(SAND92-0243 high end).

## Results

`v_model/v_source` ratio at each source-tabulated range point (1.00 = exact
match; >1 = model decays too slowly, i.e. predicts a higher velocity than the
source measured at that range).

### 75mm M48 HE (V0 = 3120 ft/s)

| r (ft) | current (0.585) |  1.2 |  1.7 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.40 | 1.30 | 1.22 |
|    100 |            2.56 | 2.01 | 1.66 |
|    400 |            3.53 | 1.92 | 1.17 |

### 105mm M1 HE (V0 = 3500 ft/s)

| r (ft) | current (0.585) |  1.2 |  1.7 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.23 | 1.16 | 1.10 |
|     30 |            1.34 | 1.23 | 1.16 |
|     40 |            1.44 | 1.31 | 1.21 |
|     60 |            1.62 | 1.43 | 1.29 |
|     80 |            1.74 | 1.50 | 1.33 |
|    100 |            1.93 | 1.64 | 1.43 |
|    120 |            2.08 | 1.73 | 1.50 |
|    140 |            2.20 | 1.82 | 1.55 |
|    170 |            2.38 | 1.93 | 1.62 |
|    200 |            2.51 | 2.00 | 1.66 |
|    300 |            2.80 | 2.12 | 1.68 |

### 155mm M107 HE (V0 = 3500 ft/s)

| r (ft) | current (0.585) |  1.2 |  1.7 |
| -----: | --------------: | ---: | ---: |
|     20 |            1.32 | 1.21 | 1.12 |
|     30 |            1.52 | 1.35 | 1.22 |
|     40 |            1.73 | 1.50 | 1.33 |
|     60 |            2.08 | 1.73 | 1.49 |
|     80 |            2.41 | 1.94 | 1.63 |
|    100 |            2.65 | 2.06 | 1.68 |
|    150 |            3.03 | 2.18 | 1.67 |
|    200 |            3.24 | 2.18 | 1.57 |
|    300 |            3.55 | 2.10 | 1.37 |
|    400 |            3.84 | 2.07 | 1.25 |
|    600 |            4.37 | 2.01 | 1.07 |

## Verdict

**75mm.** Raising the combined drag value shrinks the ratio at every range
point tested, but does not close it uniformly: at 1.7 the ratio is 1.22 at
r=20 ft, *rises* to a peak of 1.66 at r=100 ft, then falls back through the
gap to 1.17 at r=400 ft. The model's decay curve has the wrong shape, not
just the wrong scale — a constant bigger drag only happens to cross back near
unity at the longest range tested.

**105mm.** No candidate closes the gap anywhere in the 20-300 ft range
tested. Even at 1.7 the ratio never drops below ~1.10 (r=20 ft) and climbs
monotonically to 1.68 by r=300 ft — still diverging at the far end of the
table, with no turnover the way 75mm and 155mm show. This caliber's residual
is the worst-behaved of the three.

**155mm.** Same qualitative pattern as 75mm: ratio rises from ~1.1-1.3 at
short range to a peak of ~1.63-1.68 around r=100-150 ft, then falls back
toward unity by r=600 ft (1.07 at 1.7 — the closest any caliber/value
combination gets to a true close). Again the curve shape, not just its
scale, is wrong.

**Overall.** Raising the combined `C_D·C_shape` from 0.585 to 1.2-1.7 is a
step in the right direction — it substantially shrinks the ratio everywhere
— but no single constant value in this range closes the velocity-decay gap
uniformly, either across calibers or across range within one caliber. 75mm
and 155mm both show a rise-then-fall ratio shape (overshoot at mid-range,
approach to unity only at the far range tested); 105mm shows no turnover at
all within its shorter tested range and keeps diverging. A caliber/range-
dependent residual remains: because `retardation_coeff`'s exponential decay
has one fixed rate, it cannot reproduce a `v(r)` curve whose deviation from
that decay changes sign with range. This is consistent with the Sandia
source's own framing of 1.2-1.7 as a *velocity-dependent* combined drag, not
a single constant — closing the gap fully would need a velocity- or
range-dependent drag term, not merely a larger constant one.
