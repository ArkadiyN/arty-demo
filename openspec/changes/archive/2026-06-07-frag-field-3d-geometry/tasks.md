## Implementation Tasks

All implementation is complete. This file records what was delivered and the
verification steps that confirm each spec is satisfied.

______________________________________________________________________

### Task: Extend ShellParams with Tier-1 zone arc fields and metadata

**Status:** Done\
**Spec:** `specs/shell-registry`

- Added `ogive_outer_R`, `ogive_inner_R`, `ogive_len`, `ogive_tip_dia`, `cylinder_len`,
  `boattail_inner_dia`, `base_thickness`, `boattail_len`, `boattail_angle_deg`, `ogive_crh`,
  `has_boattail`, `base_treatment` to `ShellParams` in `src/arty/fragmentation.py`.
- `ogive_outer_R is None` → Tier-2 (fraction-based). Present → Tier-1 (arc integration).

**Verify:** `SHELLS["105mm M1 HE"].ogive_outer_R == 0.6477` and `SHELLS["155mm M107 HE"].boattail_angle_deg == 8.0`

______________________________________________________________________

### Task: Populate M1, M107 registry entries with drawing-derived Tier-1 geometry

**Status:** Done\
**Spec:** `specs/shell-registry`

- Updated `SHELLS["105mm M1 HE"]` and `SHELLS["155mm M107 HE"]` in `src/arty/shells.py`
  with all arc radii, zone lengths, and taper angles from US Army drawings.

**Verify:** All `Scenario: M1 ogive outer arc radius` and `Scenario: Both M1 and M107 are classified as Tier 1` scenarios pass.

______________________________________________________________________

### Task: Add 75mm M48 HE shell as Tier-2 registry entry

**Status:** Done\
**Spec:** `specs/shell-registry`

- Added `"75mm M48 HE"` to `SHELLS` with values from *Handbook of Ballistic and Engineering
  Data for Ammunition Vol. 1* (1930): `ogive_crh=7.43`, `ogive_len=0.08850` m (1.18 cal),
  `cylinder_len=0.15900` m (2.12 cal), `boattail_angle_deg=9.0`, `boattail_len=0.03675` m
  (0.49 cal), `base_treatment="mott"`.
- `ogive_len` activates the secant-ogive spray-angle formula in `compute_shell_zones`
  (spray ≈ 85.4° vs. 79.6° from full-tangent formula).

**Verify:** `SHELLS["75mm M48 HE"].ogive_outer_R is None`, `shell.ogive_crh == 7.43`,
`shell.boattail_angle_deg == 9.0`, `shell.ogive_len == 0.08850`

______________________________________________________________________

### Task: Implement compute_shell_zones with Tier-1 arc integration

**Status:** Done\
**Spec:** `specs/shell-zone-model`

- Implemented in `src/arty/zones.py`: `compute_shell_zones(shell) -> ShellZones`.
- Tier-1 path: 200-slice Riemann integration of annular steel volume between outer and inner
  arc profiles. Inner ogive arc uses two-point circular fit anchored at shoulder bore and
  drawing tip bore (`_arc_centre_two_point` helper).
- Returns `ShellZones(ogive, cylinder, boattail, base)` each with `ZoneParams(mass_kg, wall_t, spray_deg, V0_ms, mu, r_bu, C_kg)`.

**Verify:**

- M1 ogive fraction: `0.25 < result / M_steel < 0.42` ✓ (actual ~31%)
- M1 cylinder fraction: `0.35 < result / M_steel < 0.55` ✓ (actual ~45%)
- M107 ogive fraction: `0.45 < result / M_steel < 0.65` ✓ (actual ~52%)
- M107 cylinder fraction: `0.20 < result / M_steel < 0.35` ✓ (actual ~28%)

______________________________________________________________________

### Task: Implement Tier-2 fraction-based fallback in compute_shell_zones

**Status:** Done\
**Spec:** `specs/shell-zone-model`

- Tier-2 path applies fractions: ogive 42%, cylinder 36%, boattail 17%, base 5%
  (shells with boattail) or ogive 42%, cylinder 53%, boattail 0%, base 5% (no boattail).
  Corrected from initial 53/27 estimate after geometry-recalibration of M1 inner arc.
- Ogive spray angle: if `shell.ogive_len is not None` (secant ogive), uses
  `atan2(sqrt(R_o² − x_m²), x_m)` where `x_m = ogive_len/2`, `R_o = crh × D`.
  Otherwise uses full-tangent formula from `ogive_crh` (or `CRH_DEFAULT_TIER2 = 6.0`).

**Verify:** `compute_shell_zones(SHELLS["75mm M48 HE"])` zone masses sum to total steel
within 1%; `result.ogive.spray_deg` is between 83.0 and 88.0.

______________________________________________________________________

### Task: Implement fragment_ground_impact with AoF rotation

**Status:** Done\
**Spec:** `specs/burst-geometry`

- Implemented in `src/arty/zones.py`: `fragment_ground_impact(theta_z_deg, phi_rad, aof_deg, h_b)`.
- Returns `(x_hit, y_hit, gamma_rad)` or `None` when `v_gz >= 0`.
- AoF rotation verified: vertical shell (AoF=90°) ogive zone produces azimuthally symmetric
  ring with `r = h_b * tan(theta_o)` within 1e-6 m.

**Verify:** Ring symmetry assertion in `_four-zone-3d.qmd` §6.5 passes (rendered clean).

______________________________________________________________________

### Task: Implement PostureParams and presented_area(γ, posture)

**Status:** Done\
**Spec:** `specs/burst-geometry`

- Implemented in `src/arty/fragmentation.py`:
  `presented_area(gamma, posture) = posture.w_perp * (posture.h * cos(gamma) + posture.d * sin(gamma))`.
- `STANDING = PostureParams(0.5, 1.7, 0.3)`, `PRONE = PostureParams(0.5, 0.3, 1.8)`.

**Verify:** All four limit checks in `_four-zone-3d.qmd` §6.6 pass (STANDING γ=0: 0.85 m², γ=π/2: 0.15 m²; PRONE γ=0: 0.15 m², γ=π/2: 0.90 m²).

______________________________________________________________________

### Task: Implement four_zone_field accumulating per-zone P(kill)

**Status:** Done\
**Spec:** `specs/fragmentation-physics`

- Implemented in `src/arty/zones.py`: `four_zone_field(zones, aof_deg, h_b, posture, ...)`.
- Per-zone geometry factor $g^z = A_p(\\gamma) / (2\\pi s^2 \\cdot 2\\sin\\theta^z \\cdot \\delta)$.
- Spray-belt acceptance test: polar angle from shell axis within δ=15° of θ^z.
- Zones with `mass_kg ≤ 1e-6`, `V0_ms ≤ 0`, or non-finite μ are skipped.

**Verify:** Four-zone field heatmap renders in `fragmentation-field.qmd` §6.7 without error.

______________________________________________________________________

### Task: Add §6 Burst Geometry to governing equations notebook partial

**Status:** Done\
**Spec:** `specs/burst-geometry`

- Added §6 · Burst Geometry and Height of Burst to
  `experiment/fragmentation-field/_governing-equations.qmd`.
- Covers: slant range and arrival elevation (eq. 15–16), ground footprint scaling,
  ground burst vs. airburst trade-off, angle-of-fall asymmetry (eq. 17).
- Prose only — no code cells added to the partial.

**Verify:** `uv run quarto render experiment/fragmentation-field/fragmentation-field.qmd` completes clean.

______________________________________________________________________

### Limitations and Deferred Work

The following items were identified during derivation review and are deferred to future changes:

- **R₅₀ recalibration** — the geometry factor changed from $s^{-1}$ to $s^{-2}$; absolute P_kill
  values and the calibrated 50%-lethality radius need re-anchoring against TM 9-1901.
- **Boattail angle convention** — `boattail_angle_deg` is the full included taper angle
  (half-angle used for spray offset); this asymmetry between field names and usage should be
  documented in a future `ShellParams` docstring update.
- **γ notation collision** — `gamma` in `SteelParams` is the Mott material constant;
  `gamma` in the 3D geometry is arrival elevation angle. The notebook disambiguates with
  `γ_M`; code uses `gamma_M` in the `SteelParams` field name (pending rename).
- **M107 secant-ogive spot-check** — the secant ogive geometry for M107 was accepted on
  mass-fraction plausibility; a direct comparison against tabulated WW2 M107 fragmentation
  data (BRL MR 1009 or equivalent) is deferred.
- **Elevation spread within zones** — Gold 2007 Fig. 9 velocity-vs-angle variation within
  each zone is not modelled; single midpoint spray angle per zone is the current approximation.
- **Hard-cutoff spray belt gaps** — the ±15° (`delta_deg`) rect-function acceptance test
  creates hard-edged dead zones between zone belts (nose shadow ~0°–65°; boattail-to-base
  gap ~110°–150°). Fix: replace with a smooth angular weight (e.g. Gaussian in polar angle).
