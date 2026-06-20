## RENAMED Requirements

- FROM: `### Requirement: Zone Properties bar chart shows per-zone V₀, N₀, and spray angle`
- TO: `### Requirement: Zone Properties bar chart shows per-zone V₀ and N₀`

## MODIFIED Requirements

### Requirement: Zone breakdown section is shown in Four-zone mode

The app SHALL display a **Zone Breakdown** section below the heatmaps when the Four-zone model is active. The section SHALL contain, top to bottom: a full-width **Zone Properties bar chart**; a two-column row of per-zone P(kill) slice charts (cross-range on the left, downrange on the right); and a two-column row of cross-section charts (across cross-section on the left, paired with the cross-range slice chart above it; elevation cross-section on the right, paired with the downrange slice chart above it). The section SHALL be hidden when Single-zone mode is active.

#### Scenario: Zone breakdown is visible only in Four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the Zone Breakdown section with the Zone Properties chart, both slice charts, and both cross-section charts is visible below the heatmaps

#### Scenario: Zone breakdown is hidden in Single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** no Zone Breakdown section is shown

______________________________________________________________________

### Requirement: Zone Properties bar chart shows per-zone V₀ and N₀

The Zone Properties chart SHALL display a grouped bar chart with zone names (ogive, cylinder, boattail, base) on the x-axis and two grouped bar series: **V₀ [m/s]** (primary y-axis) and **N₀ (fragment count)** (secondary y-axis). The chart SHALL NOT display a spray-angle series. Zones with zero mass or invalid V₀ SHALL be shown with zero-height bars. The chart SHALL update when shell preset or editable parameters change.

#### Scenario: N₀ bars sum approximately to total headline N₀

- **WHEN** the zone bar chart is rendered
- **THEN** the four N₀ bars sum to within 1% of the total N₀ from the cylinder-zone headline metric denominator

______________________________________________________________________

### Requirement: Per-zone P(kill) vs cross-range line chart shows zone contributions

The Per-zone P(kill) vs Cross-range chart SHALL display P(kill) vs cross-range distance [m] for each active zone as a separate line, plus a **total** line, evaluated at a finer step than the shared 2D heatmap grid via the fine-resolution line evaluator. The total line SHALL be computed from the four-zone model (not a sum of per-zone values). Zone names SHALL appear in the legend. The x-axis shall span 0 to `max_radius`. The chart SHALL update when any parameter changes.

#### Scenario: Total line matches the cross-range slice of the heatmap

- **WHEN** the per-zone cross-range chart is rendered
- **THEN** the total line values match (within floating-point tolerance) the cross-range slice at x=0 of the four-zone 2D heatmap, at the grid coordinates the two share

#### Scenario: Cylinder zone dominates at intermediate ranges

- **WHEN** the user selects "105mm M1 HE" with default burst parameters
- **THEN** the cylinder zone line is at or above the ogive line at ranges between 20 m and 50 m from the burst point

#### Scenario: Narrow low-burst footprint is visible

- **WHEN** the burst height is low enough that the true P(kill) footprint along the cross-range line is narrower than the shared 2D heatmap grid step
- **THEN** the per-zone cross-range chart's total line shows the non-zero footprint rather than reading as all-zero

______________________________________________________________________

### Requirement: Zone Breakdown section includes the elevation cross-section chart

The elevation cross-section chart SHALL be displayed in the right column of the cross-section row, directly below the downrange slice chart. In Single-zone mode the elevation chart SHALL appear as a standalone chart outside the Zone Breakdown block (which is hidden in that mode).

#### Scenario: Elevation chart is visible in four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the elevation cross-section chart is shown in the right column of the Zone Breakdown section's cross-section row, below the downrange slice chart

#### Scenario: Elevation chart is visible in single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** the elevation cross-section chart is shown outside the Zone Breakdown block (which remains hidden), using the single-zone horizontal-ray variant

## ADDED Requirements

### Requirement: Per-zone P(kill) vs downrange line chart shows zone contributions

The Per-zone P(kill) vs Downrange chart SHALL display P(kill) vs downrange distance [m] for each active zone as a separate line, plus a **total** line, fixing the cross-range coordinate and sweeping downrange, evaluated via the fine-resolution line evaluator. The total line SHALL be computed from the four-zone model (not a sum of per-zone values). Zone names SHALL appear in the legend. The chart SHALL be displayed in the right column of the slice-chart row, beside the cross-range chart. The chart SHALL update when any parameter changes.

#### Scenario: Total line matches the downrange slice of the heatmap

- **WHEN** the per-zone downrange chart is rendered
- **THEN** the total line values match (within floating-point tolerance) the downrange slice of the four-zone 2D heatmap at the grid coordinates the two share

#### Scenario: Narrow low-burst footprint is visible

- **WHEN** the burst height is low enough that the true P(kill) footprint along the downrange line is narrower than the shared 2D heatmap grid step
- **THEN** the per-zone downrange chart's total line shows the non-zero footprint rather than reading as all-zero
