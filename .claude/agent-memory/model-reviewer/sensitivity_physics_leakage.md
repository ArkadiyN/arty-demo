---
name: sensitivity-physics-leakage
description: app/sensitivity.py repeatedly duplicates fragment ground-impact ray geometry inline instead of calling arty.zones.fragment_ground_impact — flag every time a new spray-cone/cross-section helper is added
metadata:
  type: project
---

`app/sensitivity.py` has a recurring layering violation: `_spray_cone`
(elevation x-z plane, introduced commit 5335b43) and `_spray_cone_across`
(across y-z plane, added in the 2026-06 across-slice-view change) both
re-derive the fragment ray unit-vector projection inline:

```
vgx = cA*cT + sA*sT*phi_sign
vgz = -sA*cT + cA*sT*phi_sign
```

This is the *same* formula as `src/arty/zones.fragment_ground_impact`
(`vgx = cA*cT + sA*sT*sP`, `vgz = -sA*cT + cA*sT*sP`, with `sP = phi_sign`),
just inlined for the chart's ray-drawing loop instead of imported. Per
project layering rule (`.qmd`/`app/` must import all physics from
`src/arty/`), this is a defect in spirit even though the formula matches
the reference exactly (no drift found on 2026-06-20 review) — there's no
single source of truth, so a future `fragment_ground_impact` fix would not
propagate to the chart rays.

**Why:** the new-math gate in `agents-routing.md` is about *new* physics;
this is *duplicated existing* physics, which the gate doesn't explicitly
name but the "Layering" review checklist item does ("no physics, computation,
or parameter values leaked into the .qmd/app").

**How to apply:** this is a pre-existing pattern (the first instance,
`_spray_cone`, predates the diff under review and was presumably accepted
already) — do not block a new PASS on it alone, but call it out as a
secondary/low-severity finding every time a new helper perpetuates it
(e.g. `_spray_cone_across`), recommending consolidation into a shared
`arty` ray-geometry helper (or reuse of `fragment_ground_impact` directly)
rather than re-fixing it ad hoc per review.

**RESOLVED 2026-06-20:** `src/arty/zones.py` extracted the shared trig into
`fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)` (a pure
unit-vector helper, no h_b/guard logic); `fragment_ground_impact` now calls
it, and `app/sensitivity.py`'s `_spray_cone`/`_spray_cone_across` both call
it too (reconstructing `phi_rad` from `phi_sign`/`y_sign` — `phi_sign*π/2` or
`0`/`π` — which correctly collapses to the old inline `sP=phi_sign`
substitution since `sin(±π/2)=±1`). Verified bit-identical formula, all 34
`tests/test_zones.py` cases (incl. the 4 burst-geometry spec scenarios) still
pass. Treat this leakage pattern as closed for `_spray_cone`/`_spray_cone_across`
specifically; re-open only if a *new* spray-cone-like helper reappears with
inlined trig instead of calling `fragment_velocity`.

**New secondary finding from the same diff (app-layer wiring, not physics):**
the new `_plotly_elevation_across` call site in `app/sensitivity.py` passes
`x_slice` (downrange) into the function's `y_person` (cross-range-sizing)
positional parameter — an argument-order/wiring bug, not a `arty` defect.
Per `agents-routing.md`'s correctness-question gate this routes to an
app-layer fix, not @modeler. Check call-site argument order whenever
reviewing diffs that add a sibling "across/elevation" pair of plot functions
sharing similar positional signatures — this is an easy copy-paste mistake
between the two.

**2026-06-20, `pkill-3d-surface-view` change — PASS, clean.** New
`_fig_pkill_surface(x, y, z, title, colorscale="YlOrRd")` helper adds a
`go.Surface` trace + a `field_view` radio toggle at all three call sites
(single-zone, four-zone legacy panel, four-zone new panel). Verified: every
call site passes the *exact same* `x, y, z` arrays already used by the
adjacent (now-conditional) `go.Heatmap` branch right next to it
(`result.field_x[0], result.field_y[:, 0], result.field_pk` and
`xy_grid, yy_grid, result_zones["pk_total"]`) — no new grid construction, no
recomputation, no new `src/arty/` call. `cmin=0, cmax=1` / `zaxis range=[0,1]`
is a display-clamp matching the heatmap's pre-existing `zmin=0, zmax=1`, not
a new constant (P(kill) bounded in [0,1] by construction per
`fragmentation.py`'s `1 - exp(-N_eff)`, as design.md states). The 2D-only
difference map (`diff_pk = pk_total - field_pk`) was correctly left
untouched, matching design.md's stated non-goal of no 3D diff surface in this
change. No formula drift, no leaked physics, no boundary issues (function has
no math to misbehave at limits). This is the template for how a pure
presentation-toggle change should look — use it as the comparison baseline
for future "view toggle" or "alternate chart of the same grid" diffs in this
file.
