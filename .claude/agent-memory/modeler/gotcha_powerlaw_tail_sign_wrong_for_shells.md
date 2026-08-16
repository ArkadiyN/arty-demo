---
name: gotcha-powerlaw-tail-sign-wrong-for-shells
description: The "small fragments are power-law not Mott" literature adds fragments to the sub-gram window — wrong sign if your model already over-counts
metadata:
  type: project
---

`doc-reference/mott-distribution-small-fragments/index.md` headlines that the
sub-gram tail is power-law ($\tau\approx1.9$–2.2), not Mott-exponential, and
therefore "Mott is unsound below 0.6 g". **Do not carry that forward as a fix
for an over-counting model.**

**Why:** a power law rises *faster* toward small $m$ than $\exp(-\sqrt{m/\mu})$,
so splicing it in *adds* fragments. Against Tolch 1938 it drove the 75 mm M48
residual from 2.25× to 3.1–3.6×. The three collected sources are brittle-sphere
impact, glass rods and mercury droplets — comminution, not HE-driven
thick-walled steel; Elek & Jaramaz (2009) say the power law "cannot
successfully describe the HE projectile fragmentation". Mott's own 3D exponent
$\lambda=1/3$ is wrong in the same direction. The HE-shell census wants
$\lambda\approx0.76$ (*larger* than 1/2, toward Grady's $\lambda=1$).

**How to apply:** when a spectrum-shape candidate is proposed, compute the
extrapolation multiplier before citing the source — the sign is not what the
card summary implies. Full reasoning:
`experiment/fragmentation-field/challenges/count-gap-1938/mott-tail-shape.md` §4.
