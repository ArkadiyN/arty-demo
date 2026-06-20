## ADDED Requirements

### Requirement: four_zone_line_split evaluates per-zone P(kill) along an arbitrary line

`arty.zones.four_zone_line_split` SHALL compute per-zone and total P(kill) along a
caller-specified 1D line (fixed downrange x with varying cross-range y, or fixed
cross-range y with varying downrange x), using the same per-point governing
equations (spray-belt acceptance test, presented area, drag-attenuated velocity,
Mott mass integration, solid-angle normalization) as `_four_zone_field_split`.
Its cost SHALL scale with the number of requested line points, not with the
area of the shared 2D grid, so callers can request a resolution finer than the
2D heatmap grid without the O(n_grid²) cost of tightening that grid globally.

#### Scenario: Line evaluator matches the grid evaluator at shared nodes

- **WHEN** `four_zone_line_split` is called with `line_coords` aligned to the
  shared 2D grid's node positions, for the same `zones`, `aof_deg`, `h_b`,
  `posture`, `drag_lam_grid`, `m_grid`, and `delta_deg` as a
  `_four_zone_field_split` call
- **THEN** the per-zone and total P(kill) values returned match the
  corresponding `_four_zone_field_split` grid values within floating-point
  tolerance

#### Scenario: Resolution is independent of the shared grid step

- **WHEN** `four_zone_line_split` is called with a `line_coords` array spaced
  finer than the shared 2D grid step
- **THEN** it returns one P(kill) value (per zone, plus total) for each
  requested line coordinate, evaluated directly rather than interpolated from
  the coarser grid

#### Scenario: Narrow low-burst-height footprint is resolved

- **WHEN** `four_zone_line_split` is evaluated along a line at a burst height
  where the true P(kill) footprint width is narrower than the shared 2D grid
  step
- **THEN** it returns non-zero P(kill) values within that footprint, rather
  than the all-zero result a coarser grid read would give
