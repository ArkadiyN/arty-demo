## 1. Fine-resolution line evaluator (src/arty/zones.py)

- [x] 1.1 Add `four_zone_line_split(zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, *, fixed_axis, fixed_coord, line_coords, delta_deg=15.0)`, reusing the per-point physics loop body from `_four_zone_field_split` (spray-belt acceptance test, presented area, drag-attenuated velocity, Mott mass integration, solid-angle normalization).
- [x] 1.2 Verify (modeler/model-reviewer pass) that `four_zone_line_split` matches `_four_zone_field_split` at shared grid nodes within floating-point tolerance, per the `fragmentation-physics` spec's "Line evaluator matches the grid evaluator at shared nodes" scenario.
- [x] 1.3 Add a `tests/test_zones.py` regression test asserting `four_zone_line_split` matches `_four_zone_field_split` at shared grid nodes (no automated test exists yet — verification so far was manual/notebook-level).

## 2. App wiring (app/sensitivity.py)

- [x] 2.1 Add `_compute_zone_line` cached wrapper calling `four_zone_line_split` at a 0.25 m line step for both slice charts.
- [x] 2.2 Add the **P(kill) vs Downrange** chart (fixes cross-range y, sweeps downrange x), mirroring the existing **P(kill) vs Cross-range** chart, both reading from `_compute_zone_line` instead of indexing the coarse 2D grid.
- [x] 2.3 Arrange the two slice charts side-by-side (cross-range left, downrange right).

## 3. Across cross-section chart (app/sensitivity.py)

- [x] 3.1 Add `_spray_cone_across` (per-zone fan geometry at azimuth φ=±90°, mirror-symmetric vy/vz) and `_plotly_elevation_across` (y-z plane rendering: ground fill, burst point, per-zone fans).
- [x] 3.2 Derive the ray-length cap from the axis range (`max_len = y_max + z_max`) rather than a fixed constant, so every ray is clipped by the visible plot boundary.
- [x] 3.3 Place the across cross-section in the left column (paired with, and below, the cross-range slice chart) and the elevation cross-section in the right column (paired with, and below, the downrange slice chart).

## 4. Zone Properties chart cleanup (app/sensitivity.py)

- [x] 4.1 Remove the spray-angle bar series from the Zone Properties grouped bar chart, leaving V₀ and N₀.

## 5. Spec backfill

- [x] 5.1 Write `proposal.md`, `design.md`, and the delta specs (`across-view-chart` new capability; `zone-breakdown-charts`, `fragmentation-physics` modified capabilities) documenting the already-implemented and reviewed change.
- [x] 5.2 Add the regression test from 1.3, then close out this change.
