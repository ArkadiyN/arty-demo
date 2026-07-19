---
name: hard-step-fraction-grid-aliasing
description: Threshold-crossing counts over a hard physical step alias on a coarse grid — use a dense near-field grid or the onset radius
metadata:
  type: project
---

Any "fraction of cells with P_k>0"-style statistic over a hard physical step
is unstable when the lit feature is thinner than the node spacing. Shipped
trap: the PRONE/AoF=90° false-safe-ring demo read 0% off the 60-node plot
grid (~2 m spacing vs a ~0.65 m lit band) while 40/80/…/300 nodes all read
18–25% — the exact 0% was grid aliasing presented as evidence for a fix.

**Rule:** never read a threshold-crossing statistic near a hard step off the
coarse plot grid. Either evaluate on a dense near-field grid sized to the
feature, or report the physically exact illumination-onset radius (a
descriptive read of the returned field — stays in the notebook). Verify
grid-stability on a resolution sweep before presenting an exact percent.

Spatial-aggregation cousin of [[belt-gate-quadrature-endpoint]] (different
mechanism: grid coarser than the feature, not an endpoint node on the gate).
