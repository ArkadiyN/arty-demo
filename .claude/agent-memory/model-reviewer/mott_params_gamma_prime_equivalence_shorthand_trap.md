---
name: mott-params-gamma-prime-equivalence-shorthand-trap
description: mu ~ sigma_f/(gamma' V^2) power-counting gives the wrong gamma'_eq exponent for mott_params; must numerically root-find against the real code
metadata:
  type: project
---

`mott_params` (`src/arty/fragmentation.py`) folds a shape-closure factor
`alpha = A*kappa_x^2*t_bu/x0` into an effective `gamma = alpha^(-2/3)*gamma'`,
and `alpha` itself depends on `gamma'` through `x0`. This self-consistent
coupling means the simplified shorthand `mu ~ sigma_f/(gamma' V^2)` (used as
a quick mental model in `updates/breakup-velocity-fraction/derivation.md`
§6) gives the **wrong power** if you hand-derive a "what gamma' would
reproduce this mu" claim from it — naive counting predicts
`gamma'_eq = gamma' * f^(4/3)`, but the actual code gives
`gamma'_eq = gamma' * f^2` (confirmed by `brentq` root-find against
`mott_params` directly).

**Why:** the shorthand drops the self-consistent `alpha(gamma')` dependence
that only shows up when you trace `x0` and `alpha` through the real formula.

**How to apply:** any future review of a `gamma'`-equivalence or
degeneracy claim in this module — numerically root-find against the actual
`mott_params` call, never trust a hand power-counted shorthand from the
prose, even when the prose's shorthand looks dimensionally reasonable. See
`experiment/fragmentation-field/updates/breakup-velocity-fraction/review.md`
for the full check.
