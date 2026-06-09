## Purpose

Define the Zone Breakdown section of the Streamlit sensitivity app (`app/sensitivity.py`): the per-zone properties bar chart and the per-zone P(kill) vs cross-range line chart, both shown only when the four-zone model is active.

## Requirements

### Requirement: Zone breakdown section is shown in Four-zone mode

The app SHALL display a **Zone Breakdown** section below the heatmaps when the Four-zone model is active. The section SHALL contain two charts side-by-side: a **Zone Properties bar chart** and a **Per-zone P(kill) vs Cross-range** line chart. The section SHALL be hidden when Single-zone mode is active.

#### Scenario: Zone breakdown is visible only in Four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the Zone Breakdown section with two charts is visible below the heatmaps

#### Scenario: Zone breakdown is hidden in Single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** no Zone Breakdown section is shown

______________________________________________________________________

### Requirement: Zone Properties bar chart shows per-zone V₀, N₀, and spray angle

The Zone Properties chart SHALL display a grouped bar chart with zone names (ogive, cylinder, boattail, base) on the x-axis and three grouped bar series: **V₀ [m/s]** (primary y-axis), **spray angle [°]** (primary y-axis), and **N₀ (fragment count)** (secondary y-axis). Zones with zero mass or invalid V₀ SHALL be shown with zero-height bars. The chart SHALL update when shell preset or editable parameters change.

#### Scenario: Cylinder zone has spray angle 90°

- **WHEN** any shell preset is selected with Four-zone model
- **THEN** the cylinder zone bar shows spray angle = 90°

#### Scenario: Ogive spray angle differs from cylinder

- **WHEN** the user selects "105mm M1 HE" with Four-zone model
- **THEN** the ogive zone bar shows a spray angle less than 90° (angled forward relative to cylinder)

#### Scenario: N₀ bars sum approximately to total headline N₀

- **WHEN** the zone bar chart is rendered
- **THEN** the four N₀ bars sum to within 1% of the total N₀ from the cylinder-zone headline metric denominator

______________________________________________________________________

### Requirement: Per-zone P(kill) vs cross-range line chart shows zone contributions

The Per-zone P(kill) chart SHALL display P(kill) vs cross-range distance [m] for each active zone as a separate line, plus a **total** line. The total line SHALL be computed from the four-zone model (not a sum of per-zone values). Zone names SHALL appear in the legend. The x-axis shall span 0 to `max_radius`. The chart SHALL update when any parameter changes.

#### Scenario: Total line matches the cross-range slice of the heatmap

- **WHEN** the per-zone chart is rendered
- **THEN** the total line values match (within floating-point tolerance) the cross-range slice at x=0 of the four-zone 2D heatmap

#### Scenario: Cylinder zone dominates at intermediate ranges

- **WHEN** the user selects "105mm M1 HE" with default burst parameters
- **THEN** the cylinder zone line is at or above the ogive line at ranges between 20 m and 50 m from the burst point

______________________________________________________________________

### Requirement: Zone Breakdown section includes the elevation cross-section chart

The Zone Breakdown section (four-zone mode) SHALL include the elevation cross-section chart as a third row below the Zone Properties and Per-zone P(kill) charts. The chart SHALL be full-width. In Single-zone mode the elevation chart SHALL appear as a standalone chart outside the Zone Breakdown block (which is hidden in that mode).

#### Scenario: Elevation chart is visible in four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the elevation cross-section chart is shown in the Zone Breakdown section below the existing two charts

#### Scenario: Elevation chart is visible in single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** the elevation cross-section chart is shown outside the Zone Breakdown block (which remains hidden), using the single-zone horizontal-ray variant
