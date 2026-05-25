## MODIFIED Requirements

### Requirement: compute_frag_field_3d returns asymmetric 2D footprint

The module SHALL expose `compute_frag_field_3d(shell, mott, drag, burst, posture, max_radius, n_grid) -> FragField3dResult`. The result SHALL include `field_x`, `field_y`, `field_pk` (2D arrays), `r_cross` / `pk_cross` (cross-range slice evaluated at exactly x=0, independent of grid resolution), `r50_cross` (R50 along cross-range), and the diagnostics `N0`, `mu`, `V0`, `ke_by_mass`.

#### Scenario: Cross-range slice has no spurious gap at y=0

- **WHEN** called with `BurstParams(h_b=0.0, angle_of_fall=0.0)` and any even `n_grid`
- **THEN** `pk_cross` at the index nearest y=0 is greater than 0.5

#### Scenario: Airburst against PRONE gives higher P(kill) than ground burst at y=30m

- **WHEN** called with `BurstParams(h_b=10.0)` vs `BurstParams(h_b=0.001)`, `PRONE` posture
- **THEN** `pk_cross` at the index nearest y=30m is higher for h_b=10
