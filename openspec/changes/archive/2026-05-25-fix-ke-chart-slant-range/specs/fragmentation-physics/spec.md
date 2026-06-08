## MODIFIED Requirements

### Requirement: compute_frag_field_3d returns asymmetric 2D footprint

The module SHALL expose `compute_frag_field_3d(shell, mott, drag, burst, posture, max_radius, n_grid) -> FragField3dResult`. The result SHALL include `field_x`, `field_y`, `field_pk` (2D arrays), `r_cross` / `pk_cross` (cross-range slice at x=0), `r50_cross`, `r_ke` (1D radial distance array from 0 to max_radius), `ke_by_mass` (KE indexed by `r_ke`, not by cross-range position), and the diagnostics `N0`, `mu`, `V0`, `burst`, `posture`.

#### Scenario: ke_by_mass is indexed by radial slant range

- **WHEN** `compute_frag_field_3d` is called with default params
- **THEN** `result.r_ke[0] == 0.0` and `result.r_ke[-1] == max_radius` and `len(result.r_ke) == n_grid`

#### Scenario: KE at s=0 equals ½mV₀²

- **WHEN** `result.ke_by_mass[m_g][0]` is evaluated for any representative mass
- **THEN** it equals `0.5 * m_g * 1e-3 * result.V0 ** 2` within 0.1%
