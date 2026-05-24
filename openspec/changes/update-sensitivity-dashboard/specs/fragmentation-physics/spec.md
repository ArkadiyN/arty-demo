## ADDED Requirements

### Requirement: 3D burst geometry API is exported from the module

The module SHALL export `BurstParams`, `PostureParams`, `STANDING`, `PRONE`, `presented_area`, `compute_frag_field_3d`, and `FragField3dResult` as public symbols importable from `arty.fragmentation`.

#### Scenario: All new symbols importable

- **WHEN** `from arty.fragmentation import BurstParams, PostureParams, STANDING, PRONE, compute_frag_field_3d` is executed
- **THEN** no `ImportError` is raised

______________________________________________________________________

### Requirement: Backward compatibility: existing API unchanged

The module SHALL continue to export `compute_frag_field`, `FragFieldResult`, `TargetParams`, and all existing symbols with identical signatures. No existing test SHALL break.

#### Scenario: compute_frag_field returns same result as before

- **WHEN** `compute_frag_field()` is called with default params
- **THEN** `r50` matches the value from before this change within 1%
