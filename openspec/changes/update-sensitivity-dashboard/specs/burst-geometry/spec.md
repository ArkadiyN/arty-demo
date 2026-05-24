## Requirements

### Requirement: BurstParams dataclass encodes 3D burst configuration

The module SHALL expose `BurstParams` with fields `h_b: float = 2.0` (burst height, m), `angle_of_fall: float = 30.0` (degrees, 0=horizontal, 90=vertical), `spray_half_angle: float = 15.0` (belt half-width δ, degrees). All fields SHALL have defaults.

#### Scenario: Default construction gives non-zero burst height

- **WHEN** `BurstParams()` is constructed
- **THEN** `h_b == 2.0`, `angle_of_fall == 30.0`, `spray_half_angle == 15.0`

______________________________________________________________________

### Requirement: PostureParams encodes angle-dependent target silhouette

The module SHALL expose `PostureParams` with fields `w_perp: float`, `h: float`, `d: float` representing body width, vertical extent, and top-down depth (all in metres). Two named instances SHALL be exported: `STANDING = PostureParams(0.5, 1.7, 0.3)` and `PRONE = PostureParams(0.5, 0.3, 1.8)`.

#### Scenario: STANDING presented area at γ=0 is 0.85 m²

- **WHEN** `presented_area(gamma=0.0, posture=STANDING)` is called
- **THEN** result equals `0.5 * 1.7 = 0.85` m²

#### Scenario: PRONE presented area at γ=90° is 0.90 m²

- **WHEN** `presented_area(gamma=π/2, posture=PRONE)` is called
- **THEN** result equals `0.5 * 1.8 = 0.90` m²

______________________________________________________________________

### Requirement: compute_frag_field_3d returns asymmetric 2D footprint

The module SHALL expose `compute_frag_field_3d(shell, mott, drag, burst, posture, max_radius, n_grid) -> FragField3dResult`. The result SHALL include `field_x`, `field_y`, `field_pk` (2D arrays), `r_cross` / `pk_cross` (cross-range slice at x=0), `r50_cross` (R50 along cross-range), and the diagnostics `N0`, `mu`, `V0`, `ke_by_mass`.

#### Scenario: Ground-burst limit matches 1D model within 10%

- **WHEN** called with `BurstParams(h_b=0.001, angle_of_fall=0.0)` and `STANDING`
- **THEN** `r50_cross` is within 10% of `compute_frag_field().r50` with equivalent target width `w = STANDING.w_perp * STANDING.h`

#### Scenario: Airburst against PRONE gives higher P(kill) than ground burst at y=30m

- **WHEN** called with `BurstParams(h_b=10.0)` vs `BurstParams(h_b=0.001)`, `PRONE` posture
- **THEN** `field_pk` at the cross-range point nearest y=30m is higher for h_b=10
