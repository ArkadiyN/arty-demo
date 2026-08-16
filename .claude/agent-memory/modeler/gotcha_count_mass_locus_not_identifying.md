---
name: gotcha-count-mass-locus-not-identifying
description: Fitting a fragment spectrum to a cumulative-count-vs-cumulative-mass locus is scale-degenerate — it fits perfectly and implies absurd fragment masses
metadata:
  type: project
---

For the generalised Mott family $N(\ge m)=N_\text{tot}e^{-(m/\mu)^\lambda}$ the
(number-fraction, mass-fraction) locus depends on $\lambda$ **alone** — $\mu$
cancels. That makes it tempting when a census publishes bucket counts and
weights but no screen mesh sizes.

**Why it fails:** $\mu$ is then pinned only by mass closure and runs free. On
Tolch 1938 the fit was excellent (residuals 0.92–1.03×, held-out row 0.99×)
while implying screen boundaries of 87 kg / 4.6 kg / 1.46 kg / 0.93 g against
bucket means of 154 g … 0.61 g. Every exponent trivially "earned" near the full
credit ceiling because $R\to1$ as $\mu$ inflates.

**How to apply:** anchor the fit in **absolute mass** — geometric mean of
adjacent bucket means is a serviceable boundary estimator — and validate on
closures you did *not* fit (mean fragment mass, total metal, count above the
threshold). Note this does not impeach a test that holds $(\mu,N_0)$ fixed and
inverts $\varphi$ only to locate a comparison mass; the degeneracy is in
*fitting*, not in *testing*. See
`experiment/fragmentation-field/challenges/count-gap-1938/mott-tail-shape.md` §3.
