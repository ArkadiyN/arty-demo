---
name: piecewise-quadrature-boundary-evaluation
description: Sampling ρ_L exactly AT an analytic belt-edge root is fp-fragile — require midpoint/interior nodes and a fine sweep between spot-check points
metadata:
  type: project
---

Companion to [[z_quadrature_belt_discontinuity]], found in the FIXED version
of the same derivation: solving the belt crossing analytically and then
using endpoint-inclusive trapezoid still fails, because the kernel
re-derives cosΘ independently — evaluating exactly at the analytic root is
a roundoff coin flip that can return 0.0 where the interior limit is finite.
One spuriously-zeroed endpoint → O(1/n_seg) bias (~6% at n_seg=9, only
halving per doubling — far from the claimed <0.01%), clustered near thin
segments (ring tangency loci). The modeler's 6-point worked table happened
to land on lucky r values throughout.

**How to apply:** for any piecewise-on-belt quadrature, check whether the
rule samples the breakpoints themselves. Require segment midpoints (or an
inward epsilon nudge) — midpoint gave ~0% error at the same n. And don't
accept a spot-check table as convergence proof: sweep a fine grid of r
between the table's points ([[derivation_qualitative_claims_need_numeric_check]]).
Detail: `target-height-intercept/derivation.md` §5.2/eq. 6 re-review.
