## MODIFIED Requirements

### Requirement: fragment_ground_impact implements AoF rotation correctly

`arty.zones.fragment_ground_impact(theta_z_deg, phi_rad, aof_deg, h_b)` SHALL compute
the ground impact point of a fragment leaving zone $z$ with spray angle $\\theta^z$ from
the forward shell axis and azimuth $\\phi$ around that axis.

The ground-frame velocity components are computed by
`arty.zones.fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)`,
which SHALL be the single source of this formula — `fragment_ground_impact` and
any other caller needing the ray direction (e.g. the sensitivity app's
spray-cone renderers) SHALL call `fragment_velocity` rather than recomputing
it:

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

#### Scenario: AoF = 30°, forward-biased spray angle hits forward of burst

- **WHEN** `fragment_ground_impact(70.0, phi=0.0, aof_deg=30.0, h_b=2.0)` is called
- **THEN** result is not `None` and `x_hit > 0` (forward hemisphere of shell axis)
- **Note:** The cylinder zone (theta=90°) cannot produce forward ground hits at AoF=30°: `vgz = cos(AoF)·sin(phi)` is positive for phi=π/2, so those fragments travel upward and return None. A spray angle of 70° (forward-biased, phi=0) gives vgz = −sin(30°)·cos(70°) ≈ −0.17 < 0 and vgx = cos(30°)·cos(70°) ≈ 0.30 > 0.

#### Scenario: fragment_velocity matches fragment_ground_impact's pre-extraction formula

- **WHEN** `fragment_velocity(theta_z_deg, phi_rad, aof_deg)` is called for any inputs
- **THEN** the returned `(vgx, vgy, vgz)` are numerically identical (within floating-point precision) to the components `fragment_ground_impact` used to compute inline before the extraction
