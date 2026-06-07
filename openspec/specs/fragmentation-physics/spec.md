## Purpose

Define the fragmentation physics layer: backward-compatible `gurney_velocity` and `mott_params` functions in `fragmentation.py`, the four-zone P(kill) ground-field computation (`four_zone_field` in `arty.zones`), and the routing of `compute_frag_field_3d` through the zone model while preserving its existing public signature.

## Requirements

### Requirement: gurney_velocity and mott_params are zone-aware via zones.py

`arty.zones` SHALL provide helpers `_zone_gurney` and `_zone_mott_mu` that compute per-zone Gurney velocity and Mott half-mass from zone-local mass and wall thickness. The top-level `gurney_velocity(shell)` and `mott_params(shell, V0)` in `fragmentation.py` SHALL retain their existing signatures and remain backward-compatible within 0.1%.

#### Scenario: gurney_velocity backward compatibility

- **WHEN** `gurney_velocity(SHELLS["105mm M1 HE"])` is called
- **THEN** result equals the value from before this change within 0.1% (≈ 1647 m/s for M1 with TNT Gurney 2440 m/s)

______________________________________________________________________

### Requirement: four_zone_field accumulates per-zone P(kill) fields

`arty.zones.four_zone_field` SHALL compute and return `(X, Y, P_kill)` meshgrids where `P_kill[i,j]` is the expected number of kills at ground position `(X[i,j], Y[i,j])` from the burst, summed over all four zones. Zones with zero mass, zero V₀, or non-finite μ SHALL be silently skipped.

The per-zone geometry factor is:
$$
g^z = \\frac{A_p(\\gamma, \\text{posture})}{2\\pi s^2 \\cdot 2\\sin\\theta^z \\cdot \\delta}
$$
where $\\delta$ is the spray-belt half-width (default 15°), $s$ is slant range,
and $A_p(\\gamma, \\text{posture})$ uses the arrival elevation angle $\\gamma = \\arcsin(h_b/s)$.

A ground point at `(x_g, y_g)` receives a contribution from zone $z$ only when the
polar angle $\\Theta\_\\text{burst}$ from the shell axis to that ground point lies within
$\\delta$ of $\\theta^z$ (spray-belt acceptance test).

#### Scenario: Forward sector dominated by ogive

- **WHEN** `four_zone_field(zones_m1, aof_deg=30.0, h_b=2.0, posture=STANDING, ...)` is called
- **THEN** `P_kill` at the forward ground point (positive x along the line of fire) is non-zero
  and reflects the ogive zone's spray angle (< 90°)

#### Scenario: Symmetry at AoF = 90° (vertical shell)

- **WHEN** `four_zone_field(zones_m1, aof_deg=90.0, h_b=5.0, posture=STANDING, ...)` is called
- **THEN** `P_kill` is azimuthally symmetric: `P_kill[i,j] ≈ P_kill[j,i]` within 1% for all grid points

#### Scenario: Dead base treatment contributes zero

- **WHEN** `zones` is a `ShellZones` where `base.mass_kg > 0` but the calling shell has
  `base_treatment == "dead"` and `four_zone_field` is called with those zones
- **THEN** the base zone is excluded from `field_N` (base has `mass_kg == 0.0` in the
  `ShellZones` produced by `compute_shell_zones` when `base_treatment == "dead"`,
  per the shell-zone-model spec)

**Note:** `base_treatment == "dead"` is the current default for all shells in the registry.
The base zone always receives `mass_kg > 0` from geometry, but its contribution is zeroed by
setting the `ZoneParams.mass_kg` to effectively exclude it in the `four_zone_field` loop
(`z.mass_kg <= 1e-6` guard). The `"mott"` treatment (M1, M107) propagates the base mass
through to the field.

______________________________________________________________________

### Requirement: compute_frag_field_3d signature is stable; implementation routes to four_zone_field

`compute_frag_field_3d(shell, burst, posture, drag, ...)` in `fragmentation.py` SHALL retain
its existing signature. When the shell is Tier-1 or Tier-2 (i.e., always), it SHALL internally
call `compute_shell_zones(shell)` and `four_zone_field(...)` from `arty.zones`, replacing the
former single-zone belt implementation. The returned `(X, Y, P_kill)` arrays have the same
shape semantics as before this change.

#### Scenario: compute_frag_field_3d produces asymmetric field at AoF = 30°

- **WHEN** `compute_frag_field_3d(SHELLS["105mm M1 HE"], BurstParams(angle_of_fall=30.0, h_b=2.0), STANDING, drag)` is called
- **THEN** `P_kill` is not azimuthally symmetric: the forward half (`x > 0`) has a different
  mean value than the rear half (`x < 0`)

#### Scenario: compute_frag_field_3d produces symmetric field at AoF = 90°

- **WHEN** `compute_frag_field_3d(SHELLS["105mm M1 HE"], BurstParams(angle_of_fall=90.0, h_b=5.0), STANDING, drag)` is called
- **THEN** `P_kill` field is azimuthally symmetric within 2%

______________________________________________________________________

### Requirement: compute_frag_field (1D) is backward-compatible

`compute_frag_field(shell, drag, ...)` SHALL remain unmodified. Its output (radial
`P_kill` array) SHALL match the pre-change result within 0.1% for M1 HE at default parameters.

#### Scenario: 1D field backward compatibility

- **WHEN** `compute_frag_field(SHELLS["105mm M1 HE"], drag)` is called
- **THEN** `P_kill` at r = 20 m matches the pre-change value within 0.1%
  (the single-zone symmetric model is unchanged)
