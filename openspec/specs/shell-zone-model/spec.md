## Purpose

Define the four-zone shell decomposition model in `arty.zones`: the `ShellZones` / `ZoneParams` data structures, the `compute_shell_zones` function (Tier-1 arc integration and Tier-2 fraction fallback), ogive spray-angle derivation (including secant-ogive correction), and the configurable base-plate treatment.

## Requirements

### Requirement: ShellZones dataclass carries per-zone mass, wall thickness, and spray angle

The module SHALL expose `ShellZones` with fields `ogive`, `cylinder`, `boattail`, `base` — each a `ZoneParams(mass_kg: float, wall_t: float, spray_angle_deg: float)`. `spray_angle_deg` is the mean fragment spray angle from the forward shell axis (cylinder = 90°, ogive < 90°, boattail > 90°, base ≈ 160–170°). Shells without a boattail (e.g., older Russian designs such as the F-354) SHALL have `boattail.mass_kg == 0.0`; the boattail zone is then excluded from hazard computation.

#### Scenario: Cylinder zone spray angle is exactly 90 degrees

- **WHEN** `compute_shell_zones(shell)` is called for any shell
- **THEN** `result.cylinder.spray_angle_deg == 90.0`

#### Scenario: Ogive spray angle is less than 90 degrees

- **WHEN** `compute_shell_zones(shell)` is called for any shell
- **THEN** `result.ogive.spray_angle_deg < 90.0`

#### Scenario: Boattail spray angle is greater than 90 degrees when present

- **WHEN** `compute_shell_zones(shell)` is called for a shell with `boattail_len > 0`
- **THEN** `result.boattail.spray_angle_deg > 90.0`

#### Scenario: Shell without boattail has zero boattail mass

- **WHEN** `compute_shell_zones(shell)` is called for a shell with no boattail (`boattail_len == 0` or boattail fields absent)
- **THEN** `result.boattail.mass_kg == 0.0`

#### Scenario: Zone masses sum to total shell steel mass

- **WHEN** `compute_shell_zones(shell)` is called
- **THEN** `ogive.mass_kg + cylinder.mass_kg + boattail.mass_kg + base.mass_kg` equals `shell.mass_total - shell.mass_filler - shell.mass_deductions` within 1%

______________________________________________________________________

### Requirement: Tier-1 shells compute zone masses from arc geometry by numerical integration

For shells where `ShellParams` carries zone arc fields (`ogive_outer_R`, `ogive_inner_R`, `ogive_len`, `cylinder_len`, `boattail_len`, `boattail_angle_deg`, `base_thickness`, `boattail_inner_dia`, `ogive_tip_dia`), `compute_shell_zones` SHALL integrate the annular steel volume between the outer and inner arc profiles in 200 equal axial slices. The cylinder zone uses the uniform-wall analytic formula. `boattail_len == 0` is valid and produces zero boattail mass.

#### Scenario: M1 ogive mass fraction reflects short-ogive geometry

- **WHEN** `compute_shell_zones(SHELLS["105mm M1 HE"])` is called
- **THEN** `result.ogive.mass_kg / total_steel` is between 0.25 and 0.42
- **Note:** M1 has a short ogive (5.78") nearly equal in length to its cylinder (6.195"); the inner arc uses a two-point fit anchored at the shoulder bore and drawing tip bore. Geometry gives ~31%; original derivation estimate of 54% was incorrect.

#### Scenario: M1 cylinder mass fraction reflects long-cylinder geometry

- **WHEN** `compute_shell_zones(SHELLS["105mm M1 HE"])` is called
- **THEN** `result.cylinder.mass_kg / total_steel` is between 0.35 and 0.55

#### Scenario: M107 ogive mass fraction reflects long-ogive geometry

- **WHEN** `compute_shell_zones(SHELLS["155mm M107 HE"])` is called
- **THEN** `result.ogive.mass_kg / total_steel` is between 0.45 and 0.65

#### Scenario: M107 cylinder mass fraction is between 20% and 35% of total steel

- **WHEN** `compute_shell_zones(SHELLS["155mm M107 HE"])` is called
- **THEN** `result.cylinder.mass_kg / total_steel` is between 0.20 and 0.35

______________________________________________________________________

### Requirement: Tier-2 shells receive fraction-based zone mass estimates

For shells where zone arc fields are absent, `compute_shell_zones` SHALL apply default mass fractions to total shell steel. Two sub-cases apply: shells with a boattail use ogive 42%, cylinder 36%, boattail 17%, base 5%; shells without a boattail (`has_boattail=False`) use ogive 42%, cylinder 53%, boattail 0%, base 5%, with the boattail share redistributed to the cylinder. Fractions are midpoints of the geometry-corrected M1 (ogive 31%, cyl 45%, bt 19%, base 6%) and M107 (ogive 52%, cyl 28%, bt 15%, base 5%) values. Zone wall thicknesses SHALL be estimated by scaling from `shell.wall_t` using fixed ratios (cylinder 1.0×, ogive 0.75×, boattail 2.0×, base 2.5×).

#### Scenario: Tier-2 shell with boattail zone masses sum correctly

- **WHEN** `compute_shell_zones` is called for a Tier-2 shell with `has_boattail=True`
- **THEN** zone masses sum to total steel within 1%

#### Scenario: Tier-2 shell without boattail has zero boattail mass

- **WHEN** `compute_shell_zones` is called for a Tier-2 shell with `has_boattail=False`
- **THEN** `result.boattail.mass_kg == 0.0` and `result.cylinder.mass_kg / total_steel` is approximately 0.53

______________________________________________________________________

### Requirement: Ogive spray angle is derived from outer arc midpoint surface normal

`compute_shell_zones` SHALL compute the ogive spray angle as the outward surface normal angle at the axial midpoint of the ogive outer arc (degrees from the forward shell axis). For Tier-2 shells without `ogive_len`, a default CRH of 6.0 calibers SHALL be assumed and the full-tangent ogive formula applied.

#### Scenario: M1 ogive spray angle is between 75 and 88 degrees from forward axis

- **WHEN** `compute_shell_zones(SHELLS["105mm M1 HE"])` is called
- **THEN** `result.ogive.spray_angle_deg` is between 75.0 and 88.0

#### Scenario: M107 ogive spray angle is between 75 and 88 degrees from forward axis

- **WHEN** `compute_shell_zones(SHELLS["155mm M107 HE"])` is called
- **THEN** `result.ogive.spray_angle_deg` is between 75.0 and 88.0

______________________________________________________________________

### Requirement: Tier-2 secant ogive spray angle uses ogive_len when provided

`compute_shell_zones` SHALL use the secant-arc surface normal formula when a Tier-2 shell carries `ogive_len` (the actual arc section used, shorter than the full tangent ogive of the same CRH), rather than the full-tangent approximation:

$$
\\theta\_\\text{spray} = \\arctan!\\left(\\frac{\\sqrt{R_o^2 - x_m^2}}{x_m}\\right),
\\qquad x_m = \\frac{L_n}{2},\\quad R_o = \\text{CRH} \\times D
$$

This corrects the over-estimate that the full-tangent formula produces for shells where
only a short section of a large-radius arc is used (e.g. M48: CRH 7.43 but only 1.18 cal
long, giving a near-flat section whose midpoint normal is closer to 90° than the
full-tangent midpoint).

The `ogive_len` field activates this branch; `ogive_outer_R is None` still classifies
the shell as Tier-2 (no arc integration). The result SHALL be clipped to [60°, 89.5°].

#### Scenario: M48 secant spray angle is greater than full-tangent prediction

- **WHEN** `compute_shell_zones(SHELLS["75mm M48 HE"])` is called
- **THEN** `result.ogive.spray_angle_deg` is between 83.0 and 88.0
- **Note:** Full-tangent CRH 7.43 gives ≈ 79.6°; secant midpoint at 0.59 cal gives ≈ 85.4°. The secant value is higher (more equatorial) because the short arc is nearly flat.

#### Scenario: Tier-2 shell without ogive_len uses full-tangent formula

- **WHEN** `compute_shell_zones` is called for a Tier-2 shell with `ogive_len is None` and `ogive_crh = 6.0`
- **THEN** `result.ogive.spray_angle_deg` equals `90 - degrees(arcsin(sqrt(6.0 - 0.25) / (2 * 6.0)))` within 0.1°

______________________________________________________________________

### Requirement: Base plate treatment is configurable per shell

`ShellParams` SHALL carry `base_treatment: str` with values `"mott"`, `"plate"`, or `"dead"` (default `"dead"`). When `"dead"`, the base zone contributes zero to hazard computation. When `"plate"`, the base is modelled as a single fragment of mass `base.mass_kg` with V₀ from the Gurney plate formula. When `"mott"`, the base is treated as a separate Mott zone with its own μ.

#### Scenario: Dead base treatment contributes zero to field_pk

- **WHEN** `base_treatment == "dead"` and `compute_frag_field_3d` is called
- **THEN** the base zone contributes zero to `field_pk` at all ground positions

#### Scenario: Plate base treatment adds single-fragment contribution

- **WHEN** `base_treatment == "plate"` and `compute_frag_field_3d` is called
- **THEN** the base zone contributes a non-zero value to `field_pk` at the ground position corresponding to the base spray direction
