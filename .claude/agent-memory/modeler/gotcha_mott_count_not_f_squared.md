---
name: gotcha-mott-count-not-f-squared
description: A velocity correction f entering Mott's x0 does NOT move the thresholded count N by f^2 — the rising mu partly cancels it; always compute N, never scale
metadata:
  type: project
---

Any correction $f$ applied to the velocity in `mott_params`' $x_0$ moves the
**thresholded** count $N = N_0\exp(-\sqrt{m_{thr}/\mu})$ by *less* than $f^2$.
$N_0\propto f^2$ but $\mu\propto f^{-2}$, and the larger $\mu$ raises the
survival exponential — at $f=0.943$ the realised leverage is 1.096×, not 1.125×,
so ~22 % of the intended correction is eaten back.

**Why:** scoping for the break-up-velocity fraction predicted the count arm
would land at 2.0–2.2× by scaling 2.47× by $f^2$; the actual computed range is
2.09–2.29×. The error is small here but always in the optimistic direction, so
it can turn a predicted PASS into a real FAIL.

**How to apply:** never quote a count movement by scaling $N_0$'s exponent —
call `mott_N` at both $f$ values. Full table:
`experiment/fragmentation-field/updates/breakup-velocity-fraction/derivation.md` §8.
Related: [[gotcha-n0-insensitive-to-case-mass]], [[gotcha-steel-sigma-gamma-ratio-only]].
