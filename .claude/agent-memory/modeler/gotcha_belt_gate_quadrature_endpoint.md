---
name: belt-gate-quadrature-endpoint
description: Integrating a belt/zone-gated ρ_L kernel piecewise on its analytic belt edge must use MIDPOINT sampling, never endpoint-inclusive trapezoid — the edge node coin-flips the 0/1 gate to 0.0
metadata:
  type: project
---

When integrating a **hard 0/1 gated** kernel (`lethal_density_point`'s belt
test `|cosΘ|≤sinδ`, `fragmentation.py:485`) piecewise over the belt segment
whose endpoints are the analytic roots of that same gate (eq. 5 quadratic in
the target-height-intercept derivation), you must **sample strictly-interior
nodes — composite midpoint, not endpoint-inclusive trapezoid.**

**Why:** the kernel *independently re-derives* the gate from `(x,y,z)`, so
evaluating `ρ_L` exactly at an analytic root is a floating-point coin flip —
rounding can put the node just outside the belt and return `0.0`, though the
interior limit is finite (`ρ_L` has a genuine jump there). A trapezoid weights
that endpoint, so whenever the lower node coin-flips it loses `ρ_L·Δz/2`: an
`O(1/n_seg)` bias, `≈ -1/(2n_seg) ≈ -5.4%` at `n_seg=9`, only *halving* under
`n_seg` doubling (so a doubling-convergence check does NOT catch it). Midpoint
never touches the edge, keeps the same `O(1/n_seg²)` order, and is `<0.005%`.

**How to apply:** carry this into the src/ implementation of eq. (6)
(`four_zone_pkill_field`, `pkill_field_3d`) — midpoint per belt segment. Also
applies to any future column/line integral over a zone-gated kernel.

**Verification-design lesson (the reason rev-1 shipped the bug):** the bias is
intermittent — `≈0` at most `r`, `-5.4%` only at coin-flip columns. The rev-1
check used 6 hand-picked `r` that were ALL non-coin-flip, so it looked clean.
Verify gated-quadrature accuracy on a **dense sweep**, never a few points.
Full reasoning + tables: `target-height-intercept/derivation.md` §5.2, §5.4, A4.
Related: [[frag-field-structure]], [[posture-vs-intercept-axis]].
