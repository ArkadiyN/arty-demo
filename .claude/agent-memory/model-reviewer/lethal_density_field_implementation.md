---
name: lethal-density-field-implementation
description: src/ implementation review of rho_L(x,y,z) lethal-fragment areal density (fragmentation.py + zones.py, 2026-06-20) — verified oracle numbers, found one latent np.interp silent-clip foot-gun in the public per-point API
metadata:
  type: project
---

`experiment/fragmentation-field/updates/lethal-fragment-density-field/` —
src/ implementation review of `fragmentation.py`/`zones.py`'s
ρ_L(x,y,z) lethal-fragment areal density. Full numeric re-verification lives
in that folder's `review.md`; this entry keeps only what generalizes.

**Legacy bug, confirmed real and intentionally out of scope:**
`_expected_kills_3d_point` (fragmentation.py, untouched by this change) still
divides by `sin_Theta` (the field point's own polar angle) instead of
`sinθ^z` (the zone's). The new `lethal_density_point` and the four-zone path
both correctly use `sinθ^z`. If anything ever proposes reconciling or
deleting `_expected_kills_3d_point`, this is the known defect it carries —
don't assume it's already fixed just because the new functions are correct.

**Latent footgun: bare `np.interp` silently clips out-of-range queries.**
`lethal_density_point`/`lethal_density_four_zone_point` take a caller-supplied
`s_grid`/`mmin_grid` and call `np.interp(s, s_grid, mmin_grid)` with no bounds
check — for `s > s_grid[-1]` this clips to the boundary value instead of
erroring, silently understating `m_min` (and thus the density) the further
past the grid edge a query lands. **Not currently exercised** — both public
3D-field entrypoints build their own grid from the same `z` they query, so
`s_grid[-1]` always covers the query range. Flag this the moment any future
change calls these point functions from outside their own field-builder
(e.g. a per-point probe widget) with an externally supplied table — that's
exactly when the clip becomes a silent correctness bug instead of a
no-op.
