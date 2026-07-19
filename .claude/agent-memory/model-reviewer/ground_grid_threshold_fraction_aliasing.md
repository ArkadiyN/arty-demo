---
name: ground-grid-threshold-fraction-aliasing
description: a notebook diagnostic like "fraction of ring cells with P_k>0" on a coarse (x,y) Cartesian grid can land exactly on a hard physical threshold radius and report a coincidental 0%/100% that isn't robust to n_grid
metadata:
  type: project
---

Found in the target-height-intercept notebook-presentation pass
(`experiment/fragmentation-field/_pkill-field.qmd`, `ring_fill()` helper).
For the PRONE/AoF=90° example, the column-integral threshold radius where the
belt starts intersecting `[0, h=0.3]` is analytically ~6.35 m (matches
`(h_b-h)/tan(delta)`). The notebook's `pkill_field_3d(..., n_grid=60)` call
happens to place no grid point with `P_k>0` inside the reported ring
`[1.5, 7.0] m`, so the printed statistic reads a clean "0%". Sweeping
`n_grid` (40/60/80/100/150/200/300) gives 25%/**0%**/25%/22%/21%/20%/18% —
i.e. the "0%" is a coincidental aliasing artifact of that one grid choice
against a real hard step in the underlying (correct, analytically-verified)
physics, not a converged or robust number. The single-zone STANDING and
four-zone STANDING companion claims in the same section (both threshold well
inside the ring, at r≈1.1m) are *not* fragile this way — confirmed robust at
n_grid 30/50/70/100.

**Resolved** in the subsequent notebook-presentation pass: the PRONE ring
statistic now runs on a dedicated dense near-field grid
(`max_radius=10, n_grid=201`) instead of the shared 60 m plot grid, and the
notebook additionally reports a grid-stable "illumination-onset radius"
instead of leaning on the fraction alone. Re-swept `n_grid` 101–401 and
`max_radius` 8–15 m at fixed spacing on this dense grid: fraction converges to
~18.6–19% (vs the old aliased "0%") and onset to 6.345–6.353 m — both stable
to within noise. The general pattern below remains useful for the next
notebook stat of this shape.

**How to apply:** when a notebook prints a binary/fractional statistic
("fraction of cells where X>0", "cells lit vs dark") derived from a field with
a known hard cutoff (belt edges, presented-area cutoffs, etc.), don't trust a
single n_grid rendering — sweep n_grid or sample off-grid near the analytic
threshold before treating the printed percentage as a stable, reader-safe
claim. This is a *presentation-layer* aliasing issue, not a src/ physics bug —
the underlying field (`pkill_field_3d`/`four_zone_pkill_field`) itself is
smooth and matches its analytic threshold to <1% when sampled finely; only the
coarse-grid diagnostic statistic is fragile. Related to but distinct from
[[z_quadrature_belt_discontinuity]] (that one is about the *z*-column
quadrature; this one is about the outer *(x,y)* ground grid used for
notebook-level statistics) and from
[[pkill_field_qmd_onset_formula_typo]] (a hand-written formula summarizing
the same onset radius, checked separately from the printed statistic).
