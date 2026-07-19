---
name: zones-meshgrid-convention
description: X/Y meshgrid axis convention in arty/zones.py — X varies along columns (downrange), Y along rows (cross-range)
metadata:
  type: project
---

`_four_zone_field_split` / `four_zone_field` build the grid with
`X, Y = np.meshgrid(xy, xy)` (indexing='xy'): `X[i,j] = xy[j]` varies along
**columns** = downrange; `Y[i,j] = xy[i]` varies along **rows** =
cross-range. Confirmed as the convention the app actually exercises
(`app/sensitivity.py` R50 reads `pk_total[:, x_idx]` as the cross-range
slice).

Any new off-mesh sampler (`four_zone_line_split`, contours, probes) must map
`fixed_axis="x"` → hold X/downrange, sweep Y/cross-range — not transposed.

**Review method:** diff the new loop body textually against
`_four_zone_field_split` first; only re-derive physics on an actual textual
difference. Also check `app/sensitivity.py` slider grids use the same
`max_radius`/`_N_GRID` so fixed coords land exactly on grid nodes — that is
what makes "matches the grid exactly" docstring claims true.

See [[sensitivity_physics_leakage]] for a related finding in the same file.
