## MODIFIED Requirements

### Requirement: All figures update on any parameter change

The app SHALL display three figures: **Mott cumulative distribution**, **Fragment KE vs Distance from Burst**, and **2D fragmentation field heatmap**. The KE chart SHALL use `result.r_ke` as its x-axis (slant range s [m] from 0 to max_radius), show three representative masses (0.5 g, 5 g, 50 g), and annotate lethality thresholds at 100 J and 1 kJ. The heatmap SHALL span the full page width and be at least 500 px tall. All figures SHALL recompute when any control changes.

#### Scenario: KE chart x-axis is slant range from 0 to max_radius

- **WHEN** the app renders with default parameters
- **THEN** the KE chart x-axis runs from 0 to max_radius labelled "Slant range s [m]", not cross-range y

#### Scenario: KE at origin equals ½mV₀²

- **WHEN** the KE chart is rendered
- **THEN** all three mass curves start at the left edge at their respective ½mV₀² values
