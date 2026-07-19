---
name: ground-grid-threshold-fraction-aliasing
description: A printed "fraction of cells with P_k>0" near a hard cutoff can alias to a coincidental 0%/100% at one n_grid — sweep before trusting it
metadata:
  type: project
---

A notebook statistic over a field with a hard cutoff (belt edge at an
analytic threshold radius) can read a clean but coincidental value at the
plot grid's resolution — observed: 0% at n_grid=60 vs 18–25% at every other
tested n_grid. Presentation-layer aliasing; the underlying field matches
its analytic threshold when sampled finely.

**How to apply:** for any binary/fractional notebook statistic near a known
hard cutoff, sweep n_grid (or sample off-grid near the analytic threshold)
before treating the printed number as reader-safe; prefer a dense dedicated
grid plus a grid-stable onset radius over a fraction on the plot grid.
Related: [[z_quadrature_belt_discontinuity]] (z-column quadrature),
[[pkill_field_qmd_onset_formula_typo]] (hand-written onset formula).
