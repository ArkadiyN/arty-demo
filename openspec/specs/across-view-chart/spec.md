## Purpose

Define the across cross-section chart in the Streamlit sensitivity app (`app/sensitivity.py`): the y-z plane (looking downrange) analogue of the elevation cross-section, shown in Four-zone mode's Zone Breakdown section.

## Requirements

### Requirement: Across cross-section chart shows the y-z plane spray geometry

The sensitivity app SHALL provide an across cross-section chart (y-z plane,
looking downrange) as the analogue of the elevation (x-z plane) cross-section.
For Single-zone mode it SHALL draw a single mirror-symmetric belt fan at
azimuth φ=±90° with half-width `spray_half_angle_deg`. For Four-zone mode it
SHALL draw one fan pair per zone (ogive, cylinder, boattail, base), colored
with the standard ogive/cylinder/boattail/base palette (C0/C1/C2/C3). The
chart SHALL display ground fill and the burst point at `(0, h_b)`.

#### Scenario: Across cross-section lobes are mirror-symmetric

- **WHEN** the across cross-section is rendered for any `aof_deg` and `theta_z`
- **THEN** the two lobes (azimuth +90° and -90°) are mirror images of each
  other about y=0 (identical height extent, opposite sign of y)

#### Scenario: Equatorial belt is horizontal in the across view

- **WHEN** Single-zone mode is active (belt spray angle = 90° from the shell
  axis)
- **THEN** the across cross-section fan is horizontal (zero vertical extent)

#### Scenario: Off-equatorial zones show vertical extent

- **WHEN** Four-zone mode is active for a shell with a non-zero boattail or
  base zone (spray angle ≠ 90°)
- **THEN** the boattail and base fans in the across cross-section have
  non-zero vertical extent

#### Scenario: Spray-cone rays are clipped by the plot axes, not a fixed cap

- **WHEN** the across cross-section is rendered at any burst height and AoF
- **THEN** every drawn ray reaches the visible plot boundary (axis-determined
  extent) rather than stopping at a fixed internal length cap, regardless of
  ray orientation (horizontal vs near-vertical)

______________________________________________________________________

### Requirement: Across cross-section pairs with the cross-range slice chart

The across cross-section SHALL be displayed in the same column as the
cross-range slice chart (the chart that fixes downrange x), one row below it,
so the two charts present a consistent "looking downrange at this x" view.
The across cross-section's y-axis range SHALL scale with the magnitude of
the cross-range chart's downrange-slider value, consistent with how the
existing elevation cross-section's x-axis range scales with its paired
cross-range-slider value.

#### Scenario: Across cross-section is positioned under the cross-range slice chart

- **WHEN** the Zone Breakdown section is rendered in Four-zone or
  Single-zone mode
- **THEN** the across cross-section appears directly below the cross-range
  slice chart, and the elevation cross-section appears directly below the
  downrange slice chart
