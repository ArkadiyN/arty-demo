---
name: piecewise-quadrature-boundary-evaluation
description: sampling rho_L exactly AT an analytically-solved belt-edge root (not just inside a segment) is numerically fragile — floating-point disagreement between the closed-form root and lethal_density_point's own re-derived cosTheta test can flip membership, biasing endpoint-inclusive trapezoid by ~6% at multiple r within the fixed ring, an O(1/n_seg) bias a "doubling check" resolves only slowly
metadata:
  type: project
---

Companion finding to [[z_quadrature_belt_discontinuity]], surfaced in the
*fixed* version of the same derivation
(`experiment/fragmentation-field/updates/target-height-intercept/derivation.md`
§5.2/eq. 6, 2026-07-18 re-review). The fix correctly stopped integrating
uniformly across the belt's hard `0/1` cutoff by solving the crossing height
analytically (eq. 5, a quadratic in `ζ = z − h_b`) and integrating piecewise
on the resulting sub-intervals `[a_m, b_m]`. But an **endpoint-inclusive**
trapezoid (`np.linspace(a_m, b_m, n_seg)`, sampling `a_m`/`b_m` themselves) is
still fragile: `lethal_density_point` re-derives `cosΘ` from `(x, y, z)`
independently of the closed-form root, so evaluating it *exactly at* the
analytic breakpoint is a coin flip on floating-point roundoff — it can land
just outside the belt (return `0.0`) when the true value approaching from
inside the segment is the finite interior density (occasionally hundreds of
m⁻²). A midpoint rule (never sampling exactly at `a_m`/`b_m`) gives 0.000%
error at `n=9` for the same segments; the endpoint-inclusive trapezoid the
derivation actually specifies gives **~6.2% systematic error**, reproduced at
`r = 1.12, 1.15, 1.22 m` (AoF=90°, `h_b=2.0`, `δ=15°`, STANDING) — all inside
the false-safe-zone ring this fix targets, interleaved with neighboring `r`
(`1.14, 1.16, ..., 1.30`) that show ~0.000% error, i.e. the modeler's own
6-point worked table (`r=1.2, 1.5, 2.0, 3.0, 5.0, 7.0`) happened to land on
the "lucky" side at every chosen point and does not represent the general
behavior between those points.

**Why the doubling check doesn't reliably save it:** the bias comes from one
spuriously-zeroed endpoint sample whose trapezoid weight is `~(b−a)/(2n)` —
an `O(1/n_seg)` error, not the `O(1/n_seg²)` a smooth composite trapezoid
should have. Doubling `n_seg=9→18` only roughly halves it (measured
`−6.2%→−2.9%` at `r=1.12`), so the derivation's own "a doubling check is
cheap insurance" framing (§5.2/§5.3) is true in spirit but does not converge
fast enough to reach the claimed `<0.01%` at a reasonable `n_seg` for these
tangency-adjacent columns — a materially slower rate than the segments the
worked table happened to sample.

**How to apply:** when reviewing (or re-reviewing after a fix lands) any
piecewise-on-belt quadrature that locates the crossing analytically, check
whether the quadrature rule samples the endpoints themselves or only interior
points. Endpoint-inclusive trapezoid at an analytically-derived, not
independently-verified-by-the-kernel breakpoint is unsafe near where the
segment is thin (geometrically, near the ring's inner/outer tangency loci —
not just "near the burst" per this derivation's own A4, which only discloses
the `r→0`/`1/s²`-peak mechanism, not this endpoint-evaluation one). Don't
accept a 6-point spot-check table as proof of "converges cleanly" — sweep a
fine grid of nearby `r` (or query points) between the table's chosen values
before accepting the accuracy claim, per
[[derivation_qualitative_claims_need_numeric_check]]. The durable fix is
simple once flagged: sample at segment midpoints (or nudge `a_m`/`b_m` inward
by a small epsilon before evaluating `ρ_L`) rather than including the
analytic breakpoint itself as a quadrature node.
