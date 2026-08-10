---
name: gotcha-ufc-wood-eq-not-invertible
description: UFC 4-023-07 Eq. 5-1 is a barrier-sizing design curve, not a ballistic-limit law — inverting it for v50 on a thin panel amplifies error by the 2.43 power
metadata:
  type: project
---

UFC 4-023-07 Eq. 5-1 ($T_w \propto v^{0.4113} w^{1.4897} / [\rho A^{1.3596} H^{0.5414}]$)
cannot be inverted to a ballistic limit outside its small-arms/thick-barrier
calibration domain. Solving $T_w = t$ raises everything to $1/0.4113 = 2.431$,
so a 5x thickness bias is a 50x velocity bias and a 2500x energy bias.
At $t$ = 1 in it returns $v_{50}$ ≈ 5 m/s for a 0.63 g fragment.

**Why:** the weak velocity exponent is what makes it a safe *design* curve
(thickness barely depends on v) and what makes it useless inverted.
Full arithmetic and the rejected-option verdict:
`experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/derivation.md` §4.3.

**How to apply:** any THOR-family thickness fit reached for as a perforation
threshold — check the velocity exponent first. If it is well below 1, the
inversion is not usable and an areal (plug-shear) criterion
$E_{thr} = e_a A(m) \propto m^{2/3}$ is the cheap defensible substitute.
Also: over-predicted $T_w$ ⇒ **under**-estimated $v_{50}$ (the curve reaches
$t$ sooner), i.e. anti-conservative on fragment count — the sign is easy to
get backwards. Related: [[gotcha-density-falloff-shape-is-threshold-degenerate]].
