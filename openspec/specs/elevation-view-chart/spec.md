## Purpose

Define the elevation cross-section chart: a vertical (x-z plane) diagram showing burst geometry, fragment spray rays, and a person silhouette. Two variants — single-zone and four-zone — are rendered in both the fragmentation-field notebook (matplotlib) and the sensitivity app (Plotly).

## Requirements

### Requirement: Single-zone elevation chart shows the belt spray geometry

The `fig_single_zone_elevation(aof_deg, h_b, r_person, spray_half_angle_deg)` function in `src/arty/plots.py` SHALL render a vertical cross-section that faithfully represents `_expected_kills_3d_point`. The single-zone model sprays fragments in a belt of angular half-width δ = `spray_half_angle_deg` (default 15°) centred on the plane **perpendicular to the shell axis**. In the x–z plane the two bounding rays of this belt are at angles `(90° + AoF) ± δ` from the +x axis. Both shell arrival arrow and fragment belt SHALL rotate with `aof_deg`. The diagram SHALL display: ground fill, burst point at (0, h_b), shell arrival arrow at `aof_deg`, the two belt-edge rays from the burst, the belt centre-line (equatorial direction), the half-angle δ label, and a person silhouette at `r_person`.

#### Scenario: Belt rotates with AoF

- **WHEN** `fig_single_zone_elevation` is called with aof_deg=0, aof_deg=45, and aof_deg=90
- **THEN** the belt centre-line and bounding rays rotate with AoF (they are NOT identical across calls)

#### Scenario: Shell arrival arrow and belt are consistent

- **WHEN** `fig_single_zone_elevation` is called with any aof_deg
- **THEN** the belt centre-line is visually perpendicular to the shell arrival arrow

#### Scenario: Belt half-angle is labelled

- **WHEN** the figure is rendered
- **THEN** the half-angle δ = spray_half_angle_deg is shown as a label on the diagram

______________________________________________________________________

### Requirement: Four-zone elevation chart shows per-zone spray directions

The `fig_zone_elevation(zones, aof_deg, h_b, r_person)` function in `src/arty/plots.py` SHALL render a vertical cross-section showing: ground fill, burst point at (0, h_b), shell arrival arrow at `aof_deg`, and for each zone two fragment rays at phi=+90° and phi=-90° (the azimuths with vgy=0), color-coded by zone using the standard ogive/cylinder/boattail/base palette (C0/C1/C2/C3). phi=+90° SHALL be drawn as a solid line; phi=-90° as a dashed line of the same color. A standing person silhouette SHALL appear at `r_person`.

#### Scenario: Cylinder zone ray is horizontal at AoF=0°

- **WHEN** `fig_zone_elevation` is called with aof_deg=0
- **THEN** the cylinder zone rays (theta_z=90°) are horizontal lines (vgz=0) at height h_b from x=0

#### Scenario: Upward rays are drawn dashed with annotation

- **WHEN** a zone ray has vgz >= 0 (fragment goes upward or horizontal)
- **THEN** the ray is drawn as a dashed line of fixed length (~30 m along the ray direction) with an "upward (excluded)" annotation, rather than being omitted

#### Scenario: Zone colors match the Zone Breakdown palette

- **WHEN** `fig_zone_elevation` is called for any shell
- **THEN** ogive rays are drawn in C0 (blue), cylinder in C1 (orange), boattail in C2 (green), base in C3 (red)

______________________________________________________________________

### Requirement: Elevation charts appear in the fragmentation-field notebook

The fragmentation-field notebook SHALL call `fig_single_zone_elevation` in the single-zone model section and `fig_zone_elevation` in the four-zone section (`_four-zone-3d.qmd`). Both calls SHALL import from `arty.plots`. No physics SHALL be computed inline in the notebook cells.

#### Scenario: Single-zone elevation renders at default AoF=0° and h_b=2 m

- **WHEN** the single-zone notebook section is rendered
- **THEN** `fig_single_zone_elevation(aof_deg=0, h_b=2.0, r_person=30)` renders without error and is displayed

#### Scenario: Four-zone elevation renders at AoF=30° and h_b=2 m

- **WHEN** the four-zone section of the notebook is rendered
- **THEN** `fig_zone_elevation(m1_zones, aof_deg=30, h_b=2.0, r_person=30)` renders without error and is displayed

______________________________________________________________________

### Requirement: Elevation chart appears in the sensitivity app for both model modes

The sensitivity app SHALL display an elevation cross-section chart for the active model mode. In Single-zone mode the chart SHALL use `fig_single_zone_elevation` geometry (belt perpendicular to shell axis, half-width δ = spray_half_angle_deg, rotating with AoF). In Four-zone mode the chart SHALL show per-zone colored rays. Both variants SHALL be Plotly figures. The person silhouette position SHALL be driven by the downrange slider (`x_slice`). If `abs(x_slice) < 2 m`, the silhouette SHALL be suppressed and a note shown instead.

#### Scenario: Elevation chart updates when AoF slider changes

- **WHEN** the user moves the angle_of_fall slider
- **THEN** the shell arrival arrow in the elevation chart reorients immediately

#### Scenario: Elevation chart updates when downrange slider changes

- **WHEN** the user moves the downrange slider
- **THEN** the person silhouette moves to the new x position

#### Scenario: Silhouette suppressed near burst

- **WHEN** x_slice is set to 0 m
- **THEN** no person silhouette is drawn and a "(burst proximity)" note is shown

______________________________________________________________________

### Requirement: Zone Breakdown section includes the elevation cross-section chart

The Zone Breakdown section (four-zone mode) SHALL include the elevation cross-section chart as a third row below the Zone Properties and Per-zone P(kill) charts. The chart SHALL be full-width. In Single-zone mode the elevation chart SHALL appear as a standalone chart outside the Zone Breakdown block (which is hidden in that mode).

#### Scenario: Elevation chart is visible in four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the elevation cross-section chart is shown in the Zone Breakdown section below the existing two charts

#### Scenario: Elevation chart is visible in single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** the elevation cross-section chart is shown outside the Zone Breakdown block (which remains hidden), using the single-zone horizontal-ray variant
