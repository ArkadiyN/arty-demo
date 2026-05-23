## ADDED Requirements

### Requirement: Parameter structs define all model inputs

The module SHALL expose four dataclasses — `ShellParams`, `MottParams`, `DragParams`, `TargetParams` — with typed fields and default values matching the validated 105mm M1 HE parameters from the Quarto notebook. All fields SHALL have defaults so callers can override only what they need. Explosive type SHALL be encoded via `FillerParams` (name, gurney_const) with a `FILLERS` registry; `ShellParams.filler` references a `FillerParams` instance.

#### Scenario: Default construction matches notebook values

- **WHEN** `ShellParams()` is constructed with no arguments
- **THEN** `filler.name == "TNT"`, `filler.gurney_const == 2440.0`, `mass_total == 14.97`, `mass_filler == 2.18`

#### Scenario: Field override leaves others unchanged

- **WHEN** `MottParams(gamma=53.0)` is constructed
- **THEN** `sigma_f` retains its default value of `800e6`

______________________________________________________________________

### Requirement: Gurney velocity is computed from shell and filler mass

The module SHALL expose `gurney_velocity(shell: ShellParams) -> float` returning initial fragment velocity in m/s using the Gurney cylinder formula.

#### Scenario: Result is within published bracket for M/C = 4–8

- **WHEN** `gurney_velocity` is called with default `ShellParams`
- **THEN** the result is between 900 and 1400 m/s

______________________________________________________________________

### Requirement: Mott parameters are computed from shell geometry and material

The module SHALL expose `mott_params(shell: ShellParams, mott: MottParams, V0: float) -> tuple[float, float]` returning `(mu, N0)` — the half-mass parameter and total fragment count.

#### Scenario: Fragment count for default shell is within PAFRAG expected range

- **WHEN** called with default params
- **THEN** fragments heavier than 0.5 g number between 3000 and 8000

#### Scenario: Increasing gamma decreases mu

- **WHEN** `MottParams(gamma=67)` is used versus `MottParams(gamma=53)`
- **THEN** the returned `mu` is smaller for `gamma=67` (mu ∝ (sigma_f/gamma)^1.5)

______________________________________________________________________

### Requirement: Retardation coefficient scales as m⁻¹/³

The module SHALL expose `retardation_coeff(m: np.ndarray, drag: DragParams) -> np.ndarray` returning the drag decay constant λ per metre for an array of fragment masses.

#### Scenario: Heavier fragments have lower retardation

- **WHEN** called with masses `[0.001, 0.01, 0.1]` kg
- **THEN** returned λ values are strictly decreasing

______________________________________________________________________

### Requirement: ES-310 graded Pk|hit is returned for a KE array

The module SHALL expose `pk_given_hit(E: np.ndarray) -> np.ndarray` returning per-fragment kill probability using log-linear interpolation between anchors (100 J → 0.10, 1 kJ → 0.50, 4 kJ → 0.90), clipped to [0, 0.9].

#### Scenario: Anchors match ES-310 values

- **WHEN** called with `E = [100.0, 1000.0, 4000.0]`
- **THEN** result is approximately `[0.10, 0.50, 0.90]`

#### Scenario: Zero energy returns zero probability

- **WHEN** called with `E = [0.0]`
- **THEN** result is `[0.0]`

______________________________________________________________________

### Requirement: compute_frag_field returns a complete result struct

The module SHALL expose `compute_frag_field(shell, mott, drag, target, max_radius, n_r) -> FragFieldResult` integrating all sub-models and returning a `FragFieldResult` dataclass with fields: `r` (radial distance from burst array), `p_kill` (per-distance kill probability), `ke_by_mass` (dict of representative masses → KE arrays), `field_x`, `field_y`, `field_pk` (2D field arrays), `r50` (scalar), `N0` (total fragment count), `mu` (Mott half-mass).

#### Scenario: p_kill is strictly decreasing with distance from burst

- **WHEN** called with default params and `max_radius=300`
- **THEN** `result.p_kill` is monotonically non-increasing

#### Scenario: R₅₀ is within expected range for 105mm M1 HE

- **WHEN** called with default 105mm M1 HE params
- **THEN** `result.r50` is between 50 and 200 m

#### Scenario: 2D field arrays have consistent shape

- **WHEN** called with any valid params
- **THEN** `field_x`, `field_y`, `field_pk` all have the same length
