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
g^z = \\frac{A_p(\\gamma(z_{rep}), \\text{posture})}{2\\pi s(z_{rep})^2 \\cdot 2\\sin\\theta^z \\cdot \\delta}
$$
where $\\delta$ is the spray-belt half-width (default 15°), $s(z_{rep})$ is the slant
range from the burst to height $z_{rep}$ on the target column at ground point
$(x_g, y_g)$, and $A_p(\\gamma(z_{rep}), \\text{posture})$ uses the arrival elevation
angle $\\gamma(z_{rep}) = \\arcsin\\big((h_b - z_{rep})/s(z_{rep})\\big)$.

$z_{rep}$ is a **representative illuminated height on the target column**
`[0, h]` (`h` = posture height) at $(x_g, y_g)$ — the lower edge of the lowest
belt-active sub-interval of `[0, h]`, found via `belt_column_breakpoints`
(`arty.fragmentation`) — **not** the fixed ground ray `z = 0`. A ground point
receives a contribution from zone $z$ only when the spray belt intersects the
column, `belt ∩ [0, h] ≠ ∅` (spray-belt acceptance test evaluated against the
whole column, not a single ray at the feet). When the belt already reaches the
feet (`z = 0` is itself belt-active — e.g. far enough downrange, or a high
burst), `z_{rep} = 0` and the formula reduces exactly (to floating-point
round-off) to evaluating on the feet ray, preserving the pre-fix result there.

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

______________________________________________________________________

### Requirement: four_zone_line_split evaluates per-zone P(kill) along an arbitrary line

`arty.zones.four_zone_line_split` SHALL compute per-zone and total P(kill) along a
caller-specified 1D line (fixed downrange x with varying cross-range y, or fixed
cross-range y with varying downrange x), using the same per-point governing
equations (spray-belt acceptance test, presented area, drag-attenuated velocity,
Mott mass integration, solid-angle normalization) as `_four_zone_field_split`.
Its cost SHALL scale with the number of requested line points, not with the
area of the shared 2D grid, so callers can request a resolution finer than the
2D heatmap grid without the O(n_grid²) cost of tightening that grid globally.

#### Scenario: Line evaluator matches the grid evaluator at shared nodes

- **WHEN** `four_zone_line_split` is called with `line_coords` aligned to the
  shared 2D grid's node positions, for the same `zones`, `aof_deg`, `h_b`,
  `posture`, `drag_lam_grid`, `m_grid`, and `delta_deg` as a
  `_four_zone_field_split` call
- **THEN** the per-zone and total P(kill) values returned match the
  corresponding `_four_zone_field_split` grid values within floating-point
  tolerance

#### Scenario: Resolution is independent of the shared grid step

- **WHEN** `four_zone_line_split` is called with a `line_coords` array spaced
  finer than the shared 2D grid step
- **THEN** it returns one P(kill) value (per zone, plus total) for each
  requested line coordinate, evaluated directly rather than interpolated from
  the coarser grid

#### Scenario: Narrow low-burst-height footprint is resolved

- **WHEN** `four_zone_line_split` is evaluated along a line at a burst height
  where the true P(kill) footprint width is narrower than the shared 2D grid
  step
- **THEN** it returns non-zero P(kill) values within that footprint, rather
  than the all-zero result a coarser grid read would give
