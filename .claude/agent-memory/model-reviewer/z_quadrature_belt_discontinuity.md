---
name: z-quadrature-belt-discontinuity
description: Column quadratures of ρ_L cross the hard 0/1 belt cutoff exactly where the fix matters — require a real convergence table or analytic piecewise
metadata:
  type: project
---

`lethal_density_point`'s belt test is a hard 0/1 cutoff, so ρ_L(z) at fixed
(x,y) has a genuine jump — and in the target-height-intercept geometry the
crossing height sits inside [0,h] across essentially the whole false-safe
ring. Blind uniform trapezoid there is non-monotonically wrong (up to ~34%
at the derivation's recommended n_z, and error can WORSEN as n_z grows —
the signature of a discontinuous integrand). The derivation's own
recommended doubling check would have caught it but was stated, not run
(same pattern: [[min_lethal_mass_saturation_check]],
[[derivation_qualitative_claims_need_numeric_check]]).

**How to apply:** for any quadrature/aggregation of ρ_L (or any Family-B
field) along an axis that can cross the belt boundary, reject "n resolves
it because the field is smooth" on paper. Require (a) an executed numeric
convergence table at the headline worked-example geometry, or (b) analytic
per-column location of the crossing with piecewise integration — and for
(b) see [[piecewise_quadrature_boundary_evaluation]] for the follow-on
endpoint-sampling trap. Detail: `target-height-intercept/derivation.md` §5.
