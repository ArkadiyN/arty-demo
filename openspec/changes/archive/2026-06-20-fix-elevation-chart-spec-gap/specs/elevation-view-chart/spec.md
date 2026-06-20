## MODIFIED Requirements

### Requirement: Elevation chart appears in the sensitivity app for both model modes

The sensitivity app SHALL display an elevation cross-section chart for the active model mode, implemented as local Plotly helpers in `app/sensitivity.py` — `_plotly_elevation` builds the figure and calls `_spray_cone` to draw each zone's filled spray-cone ray polygon — not the matplotlib `fig_single_zone_elevation`/`fig_zone_elevation` in `src/arty/plots.py`, which serve the notebook only. In Single-zone mode the chart SHALL show the equatorial belt (spray_deg=90°, half-width δ = spray_half_angle_deg, rotating with AoF). In Four-zone mode the chart SHALL show per-zone colored ray cones. Both variants SHALL be Plotly figures. The person silhouette position SHALL be driven by the downrange slider (`x_slice`). If `abs(x_slice) < 2 m`, the silhouette SHALL be suppressed and a note shown instead.

#### Scenario: Spray-cone ray geometry is sourced from arty.zones, not re-derived

- **WHEN** `_spray_cone` or `_spray_cone_across` computes a ray's direction
- **THEN** it calls `arty.zones.fragment_velocity` for the ground-frame velocity components rather than recomputing the AoF-rotation trig inline

#### Scenario: Elevation chart updates when AoF slider changes

- **WHEN** the user moves the angle_of_fall slider
- **THEN** the shell arrival arrow in the elevation chart reorients immediately

#### Scenario: Elevation chart updates when downrange slider changes

- **WHEN** the user moves the downrange slider
- **THEN** the person silhouette moves to the new x position

#### Scenario: Silhouette suppressed near burst

- **WHEN** x_slice is set to 0 m
- **THEN** no person silhouette is drawn and a "(burst proximity)" note is shown
