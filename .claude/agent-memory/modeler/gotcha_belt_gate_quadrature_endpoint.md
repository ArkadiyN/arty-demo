---
name: belt-gate-quadrature-endpoint
description: Integrate a belt-gated kernel piecewise with MIDPOINT nodes, never endpoint trapezoid — the edge node coin-flips the 0/1 gate
metadata:
  type: project
---

When integrating a hard 0/1 gated kernel (`lethal_density_point`'s belt test)
piecewise between the analytic roots of that same gate, sample
strictly-interior nodes — composite midpoint, never endpoint-inclusive
trapezoid. The kernel re-derives the gate from (x,y,z), so evaluating at an
analytic root is a floating-point coin flip that can return 0.0; a trapezoid
weights that endpoint → O(1/n_seg) bias (~−5% at n_seg=9) that a doubling
check only halves. Midpoint never touches the edge and stays O(1/n_seg²).

Applies to `four_zone_pkill_field`, `pkill_field_3d`, and any future
column/line integral over a zone-gated kernel.

**Verification lesson:** the bias is intermittent (only coin-flip columns) —
verify gated-quadrature accuracy on a dense sweep, never a few hand-picked
points. Tables: `target-height-intercept/derivation.md` §5.2, §5.4, A4.
Related: [[frag-field-structure]], [[posture-vs-intercept-axis]].
