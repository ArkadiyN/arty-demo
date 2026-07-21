---
name: piecewise-quadrature-boundary-evaluation
description: Evaluating a belt-gated kernel exactly AT an analytic belt-edge root is fp-fragile — true for quadrature nodes AND for single representative-point selection; require interior nodes and a fine sweep between spot-check points
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

**Recurrence (2026-07-20, `familyA-false-safe-zone/derivation.md`):** same
bug, different shape — not a quadrature node this time but the single
**representative evaluation point** `z_rep` a fix chose for a non-integrated
per-point kernel. The derivation explicitly picked `z_rep = z_lo`, the
belt-edge root itself (by design, for an exact-reduction identity), then
claimed re-evaluating the kernel's own embedded gate there is "safe because
membership was already established" — false: `cosΘ(z_rep)` recomputed from
`(x,y,z_rep)` lands within `~1e-16` of `sinδ`, and the rounding **direction**
determines pass/fail. Independently reran the derivation's own 6-point
worked table (AoF=90°, `h_b=2`, standing) through the literal eq. (3) recipe
using the already-existing, already-callable `belt_column_breakpoints` —
**4 of 6 points silently returned `N=0`**, reproducing the exact
false-safe-zone defect the aspect exists to fix. Root cause is identical to
the quadrature case (fp coin-flip at an exact root) but the trigger is
different: not "which quadrature rule samples the breakpoint" but "which
single height does a point-kernel get evaluated at." A nudge-inward epsilon
(verified: `z_rep + 1e-9·segment_width`) or substituting the *known* analytic
`cosΘ = cosθ^z ± sinδ` (rather than recomputing it) both fix it.

**How to apply:** for ANY belt-gated kernel evaluation — quadrature node or
a single chosen representative point — check whether the height/point used
was *derived as* a root of the same gate inequality the kernel re-tests.
If so, demand either (a) an explicit interior nudge, or (b) reuse of the
already-known analytic boundary value instead of recomputing it from
scratch, and require a **dense sweep across the affected region** (not a
handful of spot-check table rows, and not a single `max()`-over-ring
assertion — a lucky point anywhere in the region can mask total failure
elsewhere) as the acceptance test
([[derivation_qualitative_claims_need_numeric_check]]).
Detail: `target-height-intercept/derivation.md` §5.2/eq. 6 re-review;
`familyA-false-safe-zone/review.md` (2026-07-20) for the recurrence.
