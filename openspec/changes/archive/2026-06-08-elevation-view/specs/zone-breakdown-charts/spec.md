## ADDED Requirements

### Requirement: Zone Breakdown section includes the elevation cross-section chart

The Zone Breakdown section (four-zone mode) SHALL include the elevation cross-section chart as a third row below the Zone Properties and Per-zone P(kill) charts. The chart SHALL be full-width. In Single-zone mode the elevation chart SHALL appear as a standalone chart outside the Zone Breakdown block (which is hidden in that mode).

#### Scenario: Elevation chart is visible in four-zone mode

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the elevation cross-section chart is shown in the Zone Breakdown section below the existing two charts

#### Scenario: Elevation chart is visible in single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** the elevation cross-section chart is shown outside the Zone Breakdown block (which remains hidden), using the single-zone horizontal-ray variant
