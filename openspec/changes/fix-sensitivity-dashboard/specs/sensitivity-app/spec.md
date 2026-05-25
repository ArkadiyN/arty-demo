## MODIFIED Requirements

### Requirement: All figures update on any parameter change

The app SHALL display three figures: **Mott cumulative distribution**, **KE vs cross-range distance**, and **2D fragmentation field heatmap**. The heatmap SHALL span the full page width and be at least 500 px tall. All figures SHALL recompute when any control changes. The P(kill) vs Cross-Range Distance chart is removed.

#### Scenario: Layout is two small charts above one full-width heatmap

- **WHEN** the app loads with default parameters
- **THEN** Mott distribution and KE vs range appear side-by-side in the top row, and the 2D heatmap spans the full width below them

#### Scenario: 2D field shows asymmetric footprint at non-zero AoF

- **WHEN** `angle_of_fall` is set to 45° and `h_b` to 5 m
- **THEN** the heatmap is visibly asymmetric (offset along the downrange axis)
