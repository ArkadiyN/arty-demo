## Why

The Zone Breakdown section only let readers slice the lethality field along
cross-range (at a fixed downrange distance) and view the burst geometry in
the elevation (x-z) plane. There was no way to see how P(kill) varies along
the downrange axis, or to view the spray geometry across the line of fire
(y-z plane) — the natural complement to the existing elevation view. At low
burst heights the existing downrange/cross-range slices could also silently
read as all-zero where the true field has a narrow non-zero band, because
they sampled a coarse shared 2D grid rather than evaluating the line itself.

## What Changes

- Add a **P(kill) vs Downrange** line chart (fixes cross-range y, sweeps
  downrange x), shown side-by-side with the existing P(kill) vs Cross-range
  chart.
- Add an **Across cross-section** chart (y-z plane, looking downrange) as the
  analogue of the existing elevation (x-z plane) cross-section, showing
  per-zone spray fans at azimuth φ=±90°. Shown side-by-side with the
  elevation cross-section, each paired with the slice chart that shares its
  fixed axis.
- Remove the **Spray angle** bar from the Zone Properties chart (redundant
  with the per-zone spray geometry already shown in the cross-section
  charts; not informative as a standalone bar).
- Add a fine-resolution 1D-line P(kill) evaluation path
  (`four_zone_line_split` in `src/arty/zones.py`) so both slice charts sample
  their line at a much finer step than the global 2D heatmap grid, without
  paying the cost of tightening that grid everywhere. This fixes slices that
  could read as all-zero at low burst height even though the true field has
  a real, narrow non-zero band there.

## Capabilities

### New Capabilities

- `across-view-chart`: the across (y-z plane) cross-section diagram and its
  pairing with the downrange slice chart in the sensitivity app.

### Modified Capabilities

- `zone-breakdown-charts`: layout changes to a two-column slice-chart row
  (cross-range + downrange) and a two-column cross-section row (across +
  elevation); Zone Properties chart drops the spray-angle bar.
- `fragmentation-physics`: adds a fine-resolution per-zone P(kill) line
  evaluator alongside the existing 2D grid evaluator, reusing the same
  governing equations at arbitrary line resolution.

## Impact

- `app/sensitivity.py`: new `_spray_cone_across` / `_plotly_elevation_across`
  chart functions, new downrange slice chart, two-column layout for slice
  and cross-section charts, removal of the spray-angle bar, new
  `_compute_zone_line` cached wrapper.
- `src/arty/zones.py`: new `four_zone_line_split` function (no change to
  existing `four_zone_field` / `_four_zone_field_split` behavior).
