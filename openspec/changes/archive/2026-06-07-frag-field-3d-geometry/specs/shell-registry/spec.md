## MODIFIED Requirements

### Requirement: Shell registry exposes named presets

`src/arty/shells.py` SHALL export `SHELLS: dict[str, ShellParams]` mapping display names to fully-populated `ShellParams` instances. The registry SHALL include at minimum: `"105mm M1 HE"` and `"155mm M107 HE"`.

#### Scenario: Registry contains the 105mm M1 HE preset

- **WHEN** `from arty.shells import SHELLS` is imported
- **THEN** `"105mm M1 HE"` is a key in `SHELLS`

#### Scenario: Registry contains the 155mm M107 HE preset

- **WHEN** `from arty.shells import SHELLS` is imported
- **THEN** `"155mm M107 HE"` is a key in `SHELLS`

______________________________________________________________________

### Requirement: Preset values match notebook defaults

`SHELLS["105mm M1 HE"]` SHALL carry the validated M1 HE mass and filler parameters, with `wall_t` derived from the M1 drawing (cylinder wall 0.3625″ = 0.009208 m).

#### Scenario: M1 preset values match drawing data

- **WHEN** `SHELLS["105mm M1 HE"]` is accessed
- **THEN** `filler.name == "TNT"`, `filler.gurney_const == 2440.0`, `mass_total == 14.97`, `mass_filler == 2.18`, `wall_t == 0.009208`

#### Scenario: M107 preset values match drawing data

- **WHEN** `SHELLS["155mm M107 HE"]` is accessed
- **THEN** `filler.name == "TNT"`, `mass_total == 43.09`, `mass_filler == 6.863`, `wall_t == 0.014288`

______________________________________________________________________

## ADDED Requirements

### Requirement: ShellParams carries optional Tier-1 zone arc geometry fields

`ShellParams` SHALL accept the following optional zone geometry fields (all in SI units — metres and degrees), each defaulting to `None` unless noted:
`ogive_outer_R`, `ogive_inner_R`, `ogive_len`, `ogive_tip_dia`, `cylinder_len`, `boattail_inner_dia`, `base_thickness` (all `float | None = None`);
`boattail_len: float = 0.0`, `boattail_angle_deg: float = 0.0`.
When `ogive_outer_R is None`, the shell is classified as Tier 2 and `compute_shell_zones` applies fraction-based mass estimates.

#### Scenario: Tier-2 shell omits zone arc fields

- **WHEN** `ShellParams(caliber=0.122, wall_t=0.008, mass_total=21.76, mass_filler=3.8, filler=FILLERS["TNT"], steel=STEELS["WW2 US HE Shell"])` is constructed without zone arc fields
- **THEN** `shell.ogive_outer_R is None` and `shell.cylinder_len is None`

#### Scenario: Tier-1 shell accepts zone arc fields

- **WHEN** `ShellParams(caliber=0.105, ogive_outer_R=0.6477, ogive_inner_R=0.4572, ogive_len=0.14681, ogive_tip_dia=0.07315, cylinder_len=0.15735, boattail_len=0.05156, boattail_angle_deg=9.267, boattail_inner_dia=0.0635, base_thickness=0.017653, wall_t=0.009208, mass_total=14.97, mass_filler=2.18, filler=FILLERS["TNT"], steel=STEELS["WW2 US HE Shell"])` is constructed
- **THEN** `shell.ogive_outer_R == 0.6477`

______________________________________________________________________

### Requirement: ShellParams carries has_boattail and base_treatment metadata

`ShellParams` SHALL accept `has_boattail: bool = True` and `base_treatment: str = "dead"`. `base_treatment` SHALL be one of `"dead"`, `"plate"`, or `"mott"`. These fields apply to both Tier-1 and Tier-2 shells.

#### Scenario: Default has_boattail is True

- **WHEN** `ShellParams` is constructed without specifying `has_boattail`
- **THEN** `shell.has_boattail == True`

#### Scenario: Default base_treatment is dead

- **WHEN** `ShellParams` is constructed without specifying `base_treatment`
- **THEN** `shell.base_treatment == "dead"`

#### Scenario: Shell without boattail sets has_boattail False

- **WHEN** `ShellParams(has_boattail=False, ...)` is constructed
- **THEN** `shell.has_boattail == False`

______________________________________________________________________

### Requirement: M1 and M107 SHELLS entries carry Tier-1 zone geometry

The `"105mm M1 HE"` and `"155mm M107 HE"` entries in `SHELLS` SHALL be populated with drawing-derived Tier-1 zone geometry fields.

`"105mm M1 HE"` values (from US Army drawing):

- `ogive_outer_R = 0.6477` m (25.5″), `ogive_inner_R = 0.4572` m (18″)
- `ogive_len = 0.14681` m (5.78″), `ogive_tip_dia = 0.07315` m (2.88″)
- `cylinder_len = 0.15735` m (6.195″)
- `boattail_len = 0.05156` m (2.03″), `boattail_angle_deg = 9.267`, `boattail_inner_dia = 0.06350` m (2.5″ approx.)
- `base_thickness = 0.017653` m (0.695″)

`"155mm M107 HE"` values (from US Army drawing):

- `ogive_outer_R = 1.66294` m (65.47″, secant ogive), `ogive_inner_R = 1.09220` m (43″)
- `ogive_len = 0.30937` m (12.18″), `ogive_tip_dia = 0.060452` m (2.38″)
- `cylinder_len = 0.18720` m (7.37″)
- `boattail_len = 0.06934` m (2.73″), `boattail_angle_deg = 8.0`, `boattail_inner_dia = 0.081026` m (3.19″)
- `base_thickness = 0.036576` m (1.44″)

#### Scenario: M1 ogive outer arc radius matches drawing

- **WHEN** `SHELLS["105mm M1 HE"]` is accessed
- **THEN** `abs(shell.ogive_outer_R - 0.6477) / 0.6477 < 0.01`

#### Scenario: M107 boattail angle matches drawing

- **WHEN** `SHELLS["155mm M107 HE"]` is accessed
- **THEN** `shell.boattail_angle_deg == 8.0`

#### Scenario: Both M1 and M107 are classified as Tier 1

- **WHEN** `SHELLS["105mm M1 HE"]` and `SHELLS["155mm M107 HE"]` are accessed
- **THEN** `shell.ogive_outer_R is not None` for both entries

______________________________________________________________________

### Requirement: ShellParams carries optional ogive_crh for Tier-2 CRH override

`ShellParams` SHALL accept `ogive_crh: float | None = None`. When not `None` and the shell is Tier-2 (i.e., `ogive_outer_R is None`), `compute_shell_zones` SHALL use this value instead of `CRH_DEFAULT_TIER2` to compute the ogive spray angle. This allows shells with known CRH but no full arc geometry to use a calibrated spray angle.

#### Scenario: Tier-2 shell with ogive_crh overrides default

- **WHEN** `ShellParams(ogive_crh=7.43, ogive_outer_R=None, ...)` is constructed
- **THEN** `shell.ogive_crh == 7.43` and `shell.ogive_outer_R is None`

______________________________________________________________________

### Requirement: 75mm M48 HE shell entry in SHELLS registry

The `"75mm M48 HE"` entry SHALL be added to `SHELLS` as a Tier-2 shell. Known values
from the *Handbook of Ballistic and Engineering Data for Ammunition Vol. 1* (1930):

- `caliber = 0.075` m (75 mm)
- `mass_total = 6.622` kg (14.6 lb complete round with M48 fuze)
- `mass_filler = 0.6668` kg (1.47 lb cast TNT)
- `mass_deductions = 0.200` kg (M48 PD fuze placeholder; source TM 43-0001-28)
- `wall_t = 0.006` m (estimate; caliber-scaled from M1, requires confirmation)
- `filler = FILLERS["TNT"]`, `steel = STEELS["WW2 US HE Shell"]`
- `has_boattail = True`, `base_treatment = "mott"`
- `ogive_crh = 7.43` (7.43 cal radius, handbook)
- `ogive_len = 0.08850` m (1.18 cal, handbook; secant section — only 1.18 cal of a 7.43-cal arc used; drives secant spray angle in `compute_shell_zones`)
- `cylinder_len = 0.15900` m (2.12 cal, handbook)
- `boattail_angle_deg = 9.0` (9° full taper, handbook)
- `boattail_len = 0.03675` m (0.49 cal, handbook)

The M48 remains Tier-2 (`ogive_outer_R is None`) because the inner arc radius is
not available; mass fractions are fraction-based estimates. The `ogive_len` field
activates the secant-ogive spray-angle formula in `compute_shell_zones` without
triggering Tier-1 arc integration.

#### Scenario: Registry contains the 75mm M48 HE preset

- **WHEN** `from arty.shells import SHELLS` is imported
- **THEN** `"75mm M48 HE"` is a key in `SHELLS`

#### Scenario: M48 is classified as Tier-2

- **WHEN** `SHELLS["75mm M48 HE"]` is accessed
- **THEN** `shell.ogive_outer_R is None` and `shell.ogive_crh == 7.43`

#### Scenario: M48 boattail angle matches handbook

- **WHEN** `SHELLS["75mm M48 HE"]` is accessed
- **THEN** `shell.boattail_angle_deg == 9.0`

#### Scenario: M48 ogive_len matches handbook (secant ogive section)

- **WHEN** `SHELLS["75mm M48 HE"]` is accessed
- **THEN** `abs(shell.ogive_len - 0.08850) < 1e-5`

#### Scenario: M48 cylinder_len matches handbook

- **WHEN** `SHELLS["75mm M48 HE"]` is accessed
- **THEN** `abs(shell.cylinder_len - 0.15900) < 1e-5`
