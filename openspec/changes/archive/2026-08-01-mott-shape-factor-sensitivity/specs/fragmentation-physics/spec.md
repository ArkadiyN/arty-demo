## MODIFIED Requirements

### Requirement: gurney_velocity and mott_params are zone-aware via zones.py

`arty.zones` SHALL provide helpers `_zone_gurney` and `_zone_mott_mu` that compute per-zone Gurney velocity and Mott half-mass from zone-local mass and wall thickness. The top-level `gurney_velocity(shell)` and `mott_params(shell, V0)` in `fragmentation.py` SHALL retain their existing signatures and remain backward-compatible within 0.1%. `mott_params` SHALL read the Mott fragment-shape closure's aspect ratio and breadth factor from `shell.aspect_ratio` and `shell.breadth_factor` (`ShellParams` fields defaulting to `1.6` and `1.5` respectively) rather than fixed module constants, so default-input numerical output is unchanged while both values become overridable per call without altering the function's positional signature.

#### Scenario: gurney_velocity backward compatibility

- **WHEN** `gurney_velocity(SHELLS["105mm M1 HE"])` is called
- **THEN** result equals the value from before this change within 0.1% (≈ 1647 m/s for M1 with TNT Gurney 2440 m/s)

#### Scenario: mott_params default shape factors preserve existing output

- **WHEN** `mott_params(shell, V0)` is called with a `ShellParams` instance that does not override `aspect_ratio` or `breadth_factor`
- **THEN** the returned `(mu, N0)` matches the mott-fragment-shape-closure derivation's reviewed baseline values (defaults `aspect_ratio=1.6`, `breadth_factor=1.5`) within floating-point tolerance

#### Scenario: mott_params responds to an overridden aspect ratio

- **WHEN** `mott_params(shell, V0)` is called with `shell.aspect_ratio` set higher than the `1.6` default (all else held fixed)
- **THEN** the returned `mu` increases relative to the default-`aspect_ratio` call, consistent with `μ` scaling as `α^(-2/3)` and `α` scaling with the aspect ratio (derivation.md eq. 4b-4c)
