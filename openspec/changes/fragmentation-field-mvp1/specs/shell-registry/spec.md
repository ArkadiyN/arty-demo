## ADDED Requirements

### Requirement: Shell registry exposes named presets

`src/arty/shells.py` SHALL export `SHELLS: dict[str, ShellParams]` mapping display names to fully-populated `ShellParams` instances. MVP1 SHALL include exactly one entry: `"105mm M1 HE"`.

#### Scenario: Registry contains the 105mm M1 HE preset

- **WHEN** `from arty.shells import SHELLS` is imported
- **THEN** `"105mm M1 HE"` is a key in `SHELLS`

#### Scenario: Preset values match notebook defaults

- **WHEN** `SHELLS["105mm M1 HE"]` is accessed
- **THEN** `gurney_const == 2700.0`, `mass_shell == 14.97`, `mass_charge == 2.18`, `r_inner == 0.0519`, `wall_t == 0.011`

______________________________________________________________________

### Requirement: New shells can be added without changing existing code

The registry SHALL be structured so that adding a new shell requires only appending an entry to `SHELLS` — no changes to `fragmentation.py` or `sensitivity.py`.

#### Scenario: Adding a second shell does not break existing preset

- **WHEN** a second entry is added to `SHELLS`
- **THEN** `SHELLS["105mm M1 HE"]` still returns the correct values
