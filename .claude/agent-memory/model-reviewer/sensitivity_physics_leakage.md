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

**Resolved going-forward:** `src/arty/zones.py` extracted the shared trig into
`fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)`;
`fragment_ground_impact` and `app/sensitivity.py`'s `_spray_cone`/
`_spray_cone_across` all call it now instead of inlining the formula. Treat
this specific pair as closed; re-open only if a *new* spray-cone-like helper
reappears with inlined trig instead of calling `fragment_velocity` — that
recurrence is the actual gotcha this entry exists for, not the one-time fix.
