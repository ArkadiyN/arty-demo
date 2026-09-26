# R50 when P_kill never reaches 0.5

## Defect

`compute_frag_field_3d` (and the four-zone copy in `app/sensitivity.py`,
`_compute_zones`) set `r50_cross = |xy[argmin |P_k - 0.5|]|`. The argmin always
returns *some* grid point, so a slice whose maximum P_k is below 0.5 still gets
a "range": the sample where P_k is closest to 0.5, i.e. the peak of the slice.
The app then shows that number as R50. `compute_frag_field` (1D legacy) had the
same pattern, harmless there only because its P_k(1 m) is above 0.5.

## Decision

**Definition.** R50 is the *outermost* range at which the P_k profile falls
through 0.5: the largest r such that P_k ≥ 0.5 there, with P_k < 0.5 at the next
sample outward. It is found by linear interpolation between that pair of samples.
This is the lethal-radius meaning the notebook and app attach to R50: beyond it,
a target's P_k is below one half.

Why outermost, and not the nearest-to-0.5 sample:

- An airburst profile is not monotone. Its P_k is lower under the burst and
    peaks on a ring. The argmin could land on the *inner* rising flank, which
    understates the lethal footprint. The outer falling edge is the one that
    bounds it.
- Interpolation removes the half-grid-step quantisation of the argmin
    (Δ = 2·max_radius/(n_grid−1), which is 2.0 m at the defaults 80 m / 80 pts).
    The new value can therefore differ from the old one by up to Δ/2. That is
    the "documented better value" allowed by the brief.

**Representation.**

- Not reached (max P_k < 0.5 on the slice): `float('nan')`. The field stays
    `float`, so no caller breaks on the type. NaN also makes any downstream
    arithmetic visibly undefined instead of silently wrong.
- P_k ≥ 0.5 at the outermost sample: `float('inf')`. R50 lies beyond the
    computed domain. Returning the domain edge would be a distance the field
    does not support.

The one implementation is `arty.fragmentation.r50_outer(r, pk)`. The 3D paths
apply it to each half of the cross-range slice (y ≥ 0 and y ≤ 0) and take the
larger result, so an asymmetric slice is also bounded correctly. The app's
four-zone path calls the same helper; its private copy is deleted.

**App display.** `_fmt_r50` in `app/sensitivity.py` is presentation only. It
returns `"not reached"` for NaN and `"> {max_radius} m"` for inf, and is used in
both headline metrics and all three figure titles. When R50 is not reached, the
metric carries the slice's max P_k as its delta caption (`max P(kill) 0.16`), so
the user sees why. The elevation panel used R50 only to size its x-axis. A
non-finite R50 now passes 0 there, which falls back to the 50 m floor.

## Consumers found

| Consumer | Use | Action |
|---|---|---|
| `src/arty/fragmentation.py` `compute_frag_field_3d` | `r50_cross` | argmin replaced by `r50_cross_slice` |
| `src/arty/fragmentation.py` `compute_frag_field` (1D) | `r50` | argmin replaced by `r50_outer` |
| `app/sensitivity.py` `_compute_zones` (four-zone) | private copy of argmin | replaced by `r50_cross_slice` |
| `app/sensitivity.py` metrics, 3 figure titles, `_plotly_elevation` | display / axis extent | `_fmt_r50`, finite guard |
| `tests/test_fragmentation.py::test_3d_ground_burst_limit` | asserted `r50_cross > 0` at h_b = 10 m | see below |
| `tests/…::test_r50_in_expected_range`, `test_backward_compat` | 1D `r50` in 30–80 m | unchanged, pass (44.44 m) |
| `experiment/…/mach-dependent-fragment-drag/checks/r50-drag-anchor-shift.py` | 1D `r50` | now interpolated (≤ Δr/2 shift) |
| `experiment/…/wdss1-steel-grade/checks/recompute.py` | 1D `r50` | now interpolated (≤ Δr/2 shift) |
| `experiment/…/target-area-profile/checks/posture-crossover-ground-vs-air.py` | prints `r50_cross` | now prints `nan` at h_b = 20 m; its docstring's "argmin artefact" wording is stale (another pass's file, not edited) |
| `experiment/fragmentation-field/_field-plots.qmd:31` | own inline argmin on the 1D ground-burst P | not touched (finding below) |
| `experiment/fragmentation-field/_change-log.qmd:51,61` | own inline argmin in γ/σ_F sweeps | not touched (finding below) |

`test_3d_ground_burst_limit` had been passing on the artefact. Its h_b = 10 m,
AoF = 30° standing slice peaks at P_k ≈ 0.50 at `n_grid = 30`, and at 0.425 at
`n_grid = 80`. The test now asserts only the defined-iff-reached invariant.
The former comment's claim that "higher h_b raises r50_cross" was never
supported by the field.

**Rendered surfaces that showed a wrong R50.** Only the app. It displayed a
peak-location range as R₅₀ whenever the cross-range slice stayed below 0.5
(e.g. airbursts, prone at height). No notebook partial renders
`r50_cross`. The two `.qmd` argmin copies act on ground-burst 1D profiles that
start above 0.5 and fall monotonically, so their printed R₅₀ is correct to
within one grid step. They are still inline physics.

FINDING[deferrable]: _field-plots.qmd and _change-log.qmd compute R50 inline with the old argmin rule instead of calling arty.fragmentation.r50_outer; values are correct to one grid step on their monotone ground-burst profiles but the pattern is inline physics and would mis-report a not-reached profile (affects: experiment/fragmentation-field/_field-plots.qmd, experiment/fragmentation-field/_change-log.qmd; since: 2026-09-26)

## Before / after

Produced by `checks/r50-before-after.py` (runs in < 1 s). Before = old argmin on
the same slice; after = shipped helper. 105 mm M1 cases use wall_t 0.011 m,
max_radius 60 m, n_grid 121 (Δ = 1.0 m), the same as
`target-area-profile/checks/posture-crossover-ground-vs-air.py`. Default-shell
cases use max_radius 80 m, n_grid 80 (Δ = 2.03 m).

| Case | max P_k | before [m] | after [m] |
|---|---|---|---|
| 105 M1, h_b 20, AoF 0, standing | 0.152 | 11.00 | not reached (NaN) |
| 105 M1, h_b 20, AoF 0, prone | 0.314 | 1.00 | not reached (NaN) |
| 105 M1, h_b 0.5, AoF 0, standing | 1.000 | 15.00 | 15.04 |
| 105 M1, h_b 0.5, AoF 0, prone | 1.000 | 8.00 | 7.92 |
| default, h_b 0.5, AoF 30, standing | 1.000 | 17.22 | 16.36 |
| default, h_b 10, AoF 30, standing | 0.425 | 15.19 | not reached (NaN) |
| default, h_b 10, AoF 30, prone | 0.261 | 17.22 | not reached (NaN) |
| 1D `compute_frag_field` default | 1.000 | 44.57 | 44.44 (Δ 1.50) |

Every crossing case moves by less than Δ/2 (the largest move is 0.86 m on a
2.03 m grid). That is the quantisation removed by interpolation.
