---
name: zones-meshgrid-convention
description: X/Y meshgrid axis convention in arty/zones.py — needed to verify any new per-point function (line split, contour, slice) reproduces the same grid semantics
metadata:
  type: project
---

In `src/arty/zones.py`, `_four_zone_field_split` / `four_zone_field` build the
ground grid with `xy = np.linspace(-max_r, max_r, n_grid); X, Y = np.meshgrid(xy, xy)` (default `indexing='xy'`). This means:

- `X[i, j] = xy[j]` — varies along **columns** (axis=1) — this is the
  **downrange** axis.
- `Y[i, j] = xy[i]` — varies along **rows** (axis=0) — this is the
  **cross-range** axis.

`app/sensitivity.py`'s legacy R50 computation reads `pk_total[:, x_idx]`
(fixed column = fixed X = fixed downrange, sweep rows = sweep Y =
cross-range) and labels it "cross-range slice at x=0" — confirms the
convention above is the one actually exercised by the app, not just an
assumption from reading the source.

**Why this matters for review:** any new function that evaluates the same
physics off the square mesh (e.g. `four_zone_line_split`, added 2026-06,
which evaluates a fixed-x or fixed-y 1D line at finer resolution than the
mesh for the two slice charts in `app/sensitivity.py` ~lines 845-905) must
map `fixed_axis="x"` → hold X (downrange) fixed, sweep Y (cross-range), and
`fixed_axis="y"` → hold Y (cross-range) fixed, sweep X (downrange) — matching
`xg_arr`/`yg_arr` to the same X/Y roles, not transposed. Validated by hand
trace on 2026-06-20 (PASS) — `four_zone_line_split`'s `fixed_axis="x"`
correctly assigns `xg_arr = fixed_coord` (column/downrange role),
`yg_arr = line_coords` (row/cross-range role), matching `_four_zone_field_split`'s
`X[i,j]`/`Y[i,j]` roles exactly. The per-point physics body (spray-belt
acceptance test, presented_area, drag attenuation, Mott pdf, the
`2π·s²·2·sinθ_z·delta` solid-angle normalization) was a verbatim copy in that
diff — check this textually (diff the loop bodies) rather than re-deriving,
it's the fastest way to rule out formula drift when a function is
"generalized from mesh to line/contour".

**How to apply:** when reviewing any new grid-derived sampling function
(line slice, contour overlay, single-point probe) in this file, diff the new
loop body against the existing `_four_zone_field_split` loop body line-by-line
first; only re-derive from physics if there's an actual textual difference.
Also check `app/sensitivity.py`'s slider/grid construction
(`np.linspace(-max_radius, max_radius, _N_GRID)`) uses the *same* `max_radius`
and `_N_GRID` as the mesh function's `xy`, so `fixed_coord` passed by sliders
lands exactly on grid nodes — this is what makes "matches the grid exactly"
docstring claims true in practice, not just in theory.

See \[[sensitivity_physics_leakage]\] for a related, separate finding in the
same file.
