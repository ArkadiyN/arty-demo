## Purpose

Define the ground `P(kill)(x,y)` field computation for both the single-zone (`arty.fragmentation.pkill_field_3d`) and four-zone (`arty.zones.four_zone_pkill_field`) paths: the target-height column-integral transform that replaces the ground-plane-only (`z=0`) sample, its posture coupling (`STANDING` vs `PRONE`), and its relationship to the unchanged `P(kill)(x,y,z)` point-diagnostic volume view.

## Requirements

### Requirement: Ground P(kill) fields integrate lethal density over the target's vertical column

`arty.fragmentation.pkill_field_3d` and `arty.zones.four_zone_pkill_field` SHALL compute
the ground P(kill) transform as
$$
P_k(x,y) = 1 - \\exp!\\big(-w\_\\text{perp} \\cdot \\textstyle\\int_0^h \\rho_L(x,y,z),dz\\big)
$$
using the posture's height `h` and presented width `w_perp` (`STANDING` or `PRONE` from
`arty.fragmentation`), instead of the single-plane sample
`P_k = 1 - \exp(-\rho_L(z=0)\cdot A_\text{ref})`. Both functions SHALL accept a
`posture` parameter (default `STANDING`). The column integral SHALL be evaluated with
composite-midpoint quadrature over the belt's analytic breakpoints (`n_seg` segments,
default 9), not a uniform grid, so no quadrature node coincides with the belt-membership
discontinuity.

#### Scenario: Ground field values stay in [0, 1]

- **WHEN** `pkill_field_3d(shell, drag, burst, max_radius=50.0, n_grid=12, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** every value of the returned `P_k` grid satisfies `0 <= P_k <= 1`

#### Scenario: Four-zone ground field values stay in [0, 1]

- **WHEN** `four_zone_pkill_field(zones, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel, max_r=50.0, n_grid=12, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** every value of the returned `P_k` grid satisfies `0 <= P_k <= 1`

______________________________________________________________________

### Requirement: Ground P(kill) is posture-coupled: standing never scores below prone

Because the vertical-column integral's height `h` extends monotonically from `PRONE` to
`STANDING`, and `\rho_L \geq 0`, the standing-posture field SHALL never be less lethal
than the prone-posture field at the same ground point, for both the single-zone and
four-zone paths.

#### Scenario: Single-zone standing dominates prone

- **WHEN** `pkill_field_3d` is called twice with `posture=STANDING` and `posture=PRONE`,
  all other parameters equal, at `angle_of_fall=90.0`, `h_b=2.0`
- **THEN** `P_k_stand.max() >= P_k_prone.max()`

#### Scenario: Four-zone standing dominates prone

- **WHEN** `four_zone_pkill_field` is called twice with `posture=STANDING` and
  `posture=PRONE`, all other parameters equal, at `aof_deg=90.0`, `h_b=2.0`
- **THEN** `P_k_stand.max() >= P_k_prone.max()`

______________________________________________________________________

### Requirement: The false-safe ring is filled at steep angle of fall

At `angle_of_fall = 90°` (a horizontal spray belt at burst height), the ground ring
`2.0 m < r < 7.0 m` — which the previous `z = 0`-only transform scored as `P_k = 0`
because the belt never reaches the ground plane that close to the burst — SHALL now
read a substantial standing-posture kill probability, for both the single-zone and
four-zone paths.

#### Scenario: Single-zone close-in ring is lethal for a standing target

- **WHEN** `pkill_field_3d(shell, drag, BurstParams(angle_of_fall=90.0, spray_half_angle=15.0, h_b=2.0), posture=STANDING, max_radius=20.0, n_grid=41, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** the maximum `P_k` over ground points with `2.0 < r < 7.0` exceeds `0.5`

#### Scenario: Four-zone close-in ring is lethal for a standing target

- **WHEN** `four_zone_pkill_field(zones, aof_deg=90.0, h_b=2.0, drag=drag, rho_steel=rho_steel, posture=STANDING, max_r=30.0, n_grid=31, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** the maximum `P_k` over ground points with `2.0 < r < 7.0` exceeds `0.5`

______________________________________________________________________

### Requirement: The 3D P(kill) volume view is unchanged and remains a point-in-space diagnostic

`arty.fragmentation.pkill_volume_3d` and `arty.zones.four_zone_pkill_volume` SHALL
retain the frozen-`A_ref` point transform `P_k(x,y,z) = 1 - \exp(-\rho_L(x,y,z)\cdot A_\text{ref})`
at every height layer, unmodified by this change. In particular, the volume's ground
(`z = 0`) layer SHALL continue to reproduce the point transform of the ground-plane
lethal density exactly, and SHALL NOT match the new column-integral ground field.

#### Scenario: Single-zone volume ground layer matches the point transform bit-for-bit

- **WHEN** `pkill_volume_3d(shell, drag, burst, z_max=8.0, max_radius=50.0, n_grid=12, n_z=5, E_leth=E_LETH_DEFAULT)`
  is called, and separately `compute_lethal_density_field_3d(shell, drag, burst, z=0.0, max_radius=50.0, n_grid=12, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** the volume's `z=0` layer equals `1 - exp(-rho_L0 * A_REF_DEFAULT)` within
  `rtol=0.0, atol=0.0`

#### Scenario: Four-zone volume ground layer matches the point transform bit-for-bit

- **WHEN** `four_zone_pkill_volume(zones, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel, z_max=8.0, max_r=50.0, n_grid=12, n_z=5, E_leth=E_LETH_DEFAULT)`
  is called, and separately `four_zone_lethal_density_field(zones, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel, z=0.0, max_r=50.0, n_grid=12, E_leth=E_LETH_DEFAULT)`
  is called
- **THEN** the volume's `z=0` layer equals `1 - exp(-rho_L0 * A_REF_DEFAULT)` within
  `rtol=0.0, atol=0.0`

______________________________________________________________________

### Requirement: Fragment trajectories remain straight-line rays

This change SHALL NOT introduce gravity or ballistic curvature into any fragment
trajectory calculation. All belt-membership, drag-attenuation, and quadrature logic
SHALL operate on the existing straight-line spray-belt geometry.

#### Scenario: No new trajectory parameters

- **WHEN** the diffs for `pkill_field_3d`, `four_zone_pkill_field`, and their shared
  quadrature helpers are inspected
- **THEN** no gravitational acceleration constant or curved-trajectory parameter is
  introduced; the only new parameters are `posture`, `n_seg`, and the internal
  belt-breakpoint/quadrature helpers
