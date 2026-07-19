---
name: lethal-density-field-implementation
description: Legacy _expected_kills_3d_point sinΘ bug (intentionally unfixed) and np.interp silent-clip footgun in the per-point ρ_L API
metadata:
  type: project
---

Full numeric re-verification of the ρ_L(x,y,z) implementation lives in
`lethal-fragment-density-field/review.md`; this keeps only what generalizes.

**Legacy bug, confirmed real, intentionally unfixed:**
`_expected_kills_3d_point` divides by `sin_Theta` (the field point's own
polar angle) instead of `sinθ^z` (the zone's). The new
`lethal_density_point` and four-zone paths are correct. Any proposal to
reconcile or delete the legacy function carries this known defect — don't
assume it's already fixed.

**Latent footgun:** `np.interp(s, s_grid, mmin_grid)` silently clips past
`s_grid[-1]`, understating m_min. `lethal_density_point` has no bounds check;
`lethal_density_four_zone_point` gained an `assert sg[0]<=s<=sg[-1]` guard —
check each point/vectorised function individually, don't assume parity.
Vectorised replacements (`_four_zone_density_layer_vec`, `_pkill_columns_vec`)
dropped the assert again (unreachable today, per
`updates/field-builder-performance/review.md`). Lesson: vectorisation passes
tend to drop scalar-function asserts — check for parity on every such pass.
