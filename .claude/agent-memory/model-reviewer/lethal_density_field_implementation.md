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

**Latent footgun:** `lethal_density_point`/`lethal_density_four_zone_point`
call `np.interp(s, s_grid, mmin_grid)` with no bounds check — queries past
`s_grid[-1]` silently clip, understating m_min. Currently unexercised (the
field builders construct covering grids), but flag the moment any change
calls these point functions with an externally supplied table.
