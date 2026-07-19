---
name: hard-step-fraction-grid-aliasing
description: A "fraction of cells with P_k>0" (or any threshold-crossing count) over a hard physical step aliases on a coarse Cartesian field — can coin-flip to exactly 0% at specific n_grid; report on a dense near-field grid or via the onset radius
metadata:
  type: project
---

Any **threshold-crossing count** presented over a hard physical step — e.g.
`ring_fill`'s "fraction of annulus cells with `P_k > 0`" in
`experiment/fragmentation-field/_pkill-field.qmd` — is unstable on a coarse
Cartesian field when the lit feature is thinner than the node spacing.

**Concrete trap that shipped as a FAIL:** the PRONE / AoF=90° false-safe-ring
demo read the fraction off the *plot* grid (`pkill_field_3d`,
`max_radius=60, n_grid=60` → ~2 m node spacing). The prone belt illuminates the
0.3 m column only past an onset radius `r ≈ 6.35 m` — a ~0.65 m-wide lit band
inside the 1.5–7 m ring. Whether any 2 m-spaced node lands in that band is a
coincidence: `n_grid=60` catches none → spurious **0%**, while 40/80/100/…/300
all read 18–25%. The exact "0%" is a Cartesian-grid aliasing artifact of a hard
step, **not** a physical finding — misleading when it's the evidence for a fix.

**Fix / rule:** never read a threshold-crossing statistic near a hard spatial
step off the coarse field used for plotting. Either (a) evaluate the statistic
on a **dense near-field grid** sized to the feature (`max_radius=10, n_grid=201`
→ 0.1 m spacing gives frac ≈18.7%, onset ≈6.35 m, stable to <0.2% across
resolutions), or (b) report the physically exact **illumination-onset radius**
directly (the belt-crossing radius). Keep the coarse 60 m field for the picture
only. Onset radius = `min` illuminated radius on the dense grid is a robust
descriptive read of the returned field — not new physics, so it stays in the
notebook.

**How to apply:** any future "% of region above/below a threshold" chart where
the threshold sits on a sharp step (belt edges, dead-zone boundaries) — verify
grid-stability on a resolution sweep before presenting an exact percent. This is
the spatial-aggregation cousin of the belt-edge quadrature trap; different
mechanism (grid coarser than the step feature, not endpoint node on the gate).
Related: [[belt-gate-quadrature-endpoint]], [[frag-field-structure]].
