## Purpose

Define the burst geometry model: angle-of-fall and burst-height parameters in `BurstParams`, the angle-dependent presented-area model (`PostureParams`, `presented_area`), and the ground-impact projection function (`fragment_ground_impact`) that maps per-zone spray angles and azimuths to ground coordinates given AoF.

## Requirements

### Requirement: BurstParams carries angle_of_fall and h_b

`BurstParams` SHALL carry `h_b: float = 2.0` (burst height above ground, metres) and
`angle_of_fall: float = 30.0` (shell arrival angle from horizontal, degrees;
0° = horizontal flight, 90° = vertical plunge). Both fields are already present;
this change activates their use in the four-zone projection path.

#### Scenario: Default BurstParams angle of fall is 30 degrees

- **WHEN** `BurstParams()` is constructed without arguments
- **THEN** `burst.angle_of_fall == 30.0` and `burst.h_b == 2.0`

______________________________________________________________________

### Requirement: PostureParams and presented_area(γ, posture) replace fixed w_target

`fragmentation.py` SHALL expose `PostureParams(w_perp: float, h: float, d: float)` and
`presented_area(gamma: float, posture: PostureParams) -> float` implementing
$A_p(\\gamma, \\text{posture}) = w\_\\perp (h \\cos\\gamma + d \\sin\\gamma)$ where $\\gamma$ is
the fragment arrival elevation angle from horizontal (radians).

Pre-built constants `STANDING` and `PRONE` SHALL be exported:

| Constant   | `w_perp` | `h`   | `d`   |
| ---------- | -------- | ----- | ----- |
| `STANDING` | 0.5 m    | 1.7 m | 0.3 m |
| `PRONE`    | 0.5 m    | 0.3 m | 1.8 m |

#### Scenario: STANDING horizontal fragment presented area

- **WHEN** `presented_area(0.0, STANDING)` is called (γ = 0, fragment arrives horizontally)
- **THEN** result is `0.5 * 1.7 = 0.85` m² within 0.01 m²

#### Scenario: STANDING vertical fragment presented area

- **WHEN** `presented_area(π/2, STANDING)` is called (γ = π/2, fragment arrives from overhead)
- **THEN** result is `0.5 * 0.3 = 0.15` m² within 0.01 m²

#### Scenario: PRONE vertical fragment presented area

- **WHEN** `presented_area(π/2, PRONE)` is called
- **THEN** result is `0.5 * 1.8 = 0.90` m² within 0.01 m²

#### Scenario: PRONE horizontal fragment presented area

- **WHEN** `presented_area(0.0, PRONE)` is called
- **THEN** result is `0.5 * 0.3 = 0.15` m² within 0.01 m²

______________________________________________________________________

### Requirement: fragment_ground_impact implements AoF rotation correctly

`arty.zones.fragment_ground_impact(theta_z_deg, phi_rad, aof_deg, h_b)` SHALL compute
the ground impact point of a fragment leaving zone $z$ with spray angle $\\theta^z$ from
the forward shell axis and azimuth $\\phi$ around that axis.

The ground-frame velocity components are:

$$
v\_{g,x} = \\cos(\\text{AoF})\\cos\\theta^z + \\sin(\\text{AoF})\\sin\\theta^z\\sin\\phi
$$
$$
v\_{g,y} = \\sin\\theta^z\\cos\\phi
$$
$$
v\_{g,z} = -\\sin(\\text{AoF})\\cos\\theta^z + \\cos(\\text{AoF})\\sin\\theta^z\\sin\\phi
$$

Ground impact (with burst at height $h_b$):
$$
x\_\\text{hit} = -\\frac{v\_{g,x}}{v\_{g,z}} h_b, \\qquad
y\_\\text{hit} = -\\frac{v\_{g,y}}{v\_{g,z}} h_b, \\qquad
\\sin\\gamma = |v\_{g,z}|
$$

The function SHALL return `None` when $v\_{g,z} \\ge 0$ (fragment travels upward or horizontally
and does not reach the ground in the straight-line model).

#### Scenario: Vertical shell, ogive zone forms symmetric ring

- **WHEN** `fragment_ground_impact(theta_o, phi, aof_deg=90.0, h_b=5.0)` is called for 8 uniformly-spaced azimuths φ ∈ \[0, 2π)
- **THEN** all return non-None, and the ring radius `hypot(x_hit, y_hit)` equals `h_b * tan(radians(theta_o))` within 1 mm for all azimuths

#### Scenario: Horizontal shell, equatorial fragment travels upward

- **WHEN** `fragment_ground_impact(90.0, phi=0.0, aof_deg=0.0, h_b=2.0)` is called
  (cylinder spray direction, shell horizontal, fragment pointed straight up from AoF=0)
- **THEN** the result is `None` (v_gz = cos(0)·sin(90°)·sin(0) = 0, does not reach ground)

#### Scenario: AoF = 30°, cylinder zone, forward azimuth hits forward of burst

- **WHEN** `fragment_ground_impact(90.0, phi=π/2, aof_deg=30.0, h_b=2.0)` is called
- **THEN** result is not `None` and `x_hit > 0` (forward hemisphere of shell axis)

______________________________________________________________________

### Requirement: Footprint scales linearly with h_b

Ground impact coordinates SHALL scale linearly with `h_b`: for any zone spray angle θ, AoF, and azimuth φ where `fragment_ground_impact` returns non-None, doubling `h_b` SHALL double both `x_hit` and `y_hit` within floating-point precision.

#### Scenario: h_b doubling doubles hit coordinates

- **WHEN** `fragment_ground_impact(theta, phi, aof_deg, h_b=2.0)` returns `(x1, y1, g1)` and
  `fragment_ground_impact(theta, phi, aof_deg, h_b=4.0)` returns `(x2, y2, g2)`
- **THEN** `abs(x2 - 2*x1) < 1e-9` and `abs(y2 - 2*y1) < 1e-9`
