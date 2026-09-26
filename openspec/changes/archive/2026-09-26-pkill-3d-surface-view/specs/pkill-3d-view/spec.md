## ADDED Requirements

### Requirement: App shows an interactive 3D volume view of P_k

The app SHALL display a 3D Plotly figure rendering the point kill probability `P_k(x,y,z) = 1 − exp(−ρ_L(x,y,z)·A_ref)` over an `(x, y, z)` grid spanning a configurable radius and height around the burst point, using `go.Volume` (see design.md D2 for the two rounds of visual iteration that settled the trace type and tuning, and D2's 2026-06-21 update for the fixed [0,1] colour-scale range). `A_ref` is the fixed nominal personnel presented area defined in `experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md` (`A_REF_DEFAULT = 0.85 m²`), not the live `presented_area(γ, posture)`. The view SHALL be available for both the single-zone and four-zone model selections, using whichever model the user has currently selected elsewhere in the app.

#### Scenario: 3D view renders for single-zone model

- **WHEN** the user has the single-zone model selected and expands the 3D `P_k` view
- **THEN** a Plotly 3D figure is rendered using `pkill_volume_3d`'s output, with no error

#### Scenario: 3D view renders for four-zone model

- **WHEN** the user has the four-zone model selected and expands the 3D `P_k` view
- **THEN** a Plotly 3D figure is rendered using `four_zone_pkill_volume`'s output, with no error

#### Scenario: View updates when burst geometry or shell parameters change

- **WHEN** any slider affecting burst geometry, shell, or drag parameters changes
- **THEN** the 3D `P_k` view recomputes and re-renders to reflect the new parameters

______________________________________________________________________

### Requirement: 3D grid construction is the P_k transform of the existing ρ_L grid, with no new physics beyond the reviewed pkill-poisson-field transform

The 3D volume grid SHALL be built by evaluating the already-implemented, already-reviewed `pkill_volume_3d` (single-zone) or `four_zone_pkill_volume` (four-zone), each of which stacks the existing per-z ρ_L evaluators (`compute_lethal_density_field_3d` / `four_zone_lethal_density_field`) over multiple `z` heights and applies the `P_k = 1 − exp(−ρ_L·A_ref)` transform (`experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md`). No physical quantity, formula, or parameter beyond that reviewed transform SHALL be introduced to produce this grid.

#### Scenario: Volume grid matches the existing 2D P_k field at z=0

- **WHEN** the 3D grid's `z=0` slice is compared against the `P_k` transform of `compute_lethal_density_field_3d`'s direct single-z output for the same parameters
- **THEN** the two are numerically identical (within floating-point tolerance)

______________________________________________________________________

### Requirement: 3D field evaluation is cached

The 3D grid evaluation SHALL be wrapped in `@st.cache_data` keyed on all parameters that affect it (shell, drag, burst, grid resolution, z-extent, model selection), consistent with the app's existing 2D field caching.

#### Scenario: Repeated identical params do not recompute

- **WHEN** the same parameter values (including z-extent and resolution) are submitted twice
- **THEN** the 3D grid is returned from cache without recomputing

______________________________________________________________________

### Requirement: 3D view defaults keep interactive use responsive and well-resolved

The 3D grid SHALL default to a radius independent of (and smaller than) the app's main analysis-radius slider, sized so the default grid resolution actually resolves the underlying ρ_L field's length scale near the burst (the `P_k` transform does not change the grid's spatial requirements), and a bounded number of z-layers, so that the default view renders both smoothly and within an interactive time budget.

#### Scenario: Default grid resolution is bounded

- **WHEN** the 3D view is rendered with default parameters and no user override of resolution or radius
- **THEN** the grid resolution in each of x, y, and z is no larger than the documented default caps, and the 3D view's radius control is independent of the app's main `max_radius` slider
