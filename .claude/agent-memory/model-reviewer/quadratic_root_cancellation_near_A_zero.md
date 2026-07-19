---
name: quadratic-root-cancellation-near-A-zero
description: eq(5)'s belt-edge quadratic in zeta (A zeta^2 + B zeta + C) uses coefficient A = sin^2(alpha) - sin^2(delta); naive +/- quadratic formula suffers catastrophic cancellation as A->0 (angle-of-fall approaching the belt half-angle) and literal div-by-zero at A=0 exactly — not exercised by the standard AoF=90/delta=15 worked example (A=0.933) but must be handled in the src/ implementation
metadata:
  type: project
---

Third installment in the target-height-intercept quadrature chain (after
[[z_quadrature_belt_discontinuity]] and
[[piecewise_quadrature_boundary_evaluation]]), surfaced on the *second*
re-review (2026-07-18) of
`experiment/fragmentation-field/updates/target-height-intercept/derivation.md`
§5.2, after the midpoint-rule fix had already resolved the two prior defects
(numerically re-confirmed independently — see the derivation's own §5.4 table,
which matched a from-scratch reimplementation to ~4 significant figures).

§5.2 solves the belt-membership boundary as a quadratic in `ζ = z − h_b`:
`A ζ² + Bζ + C ≤ 0`, `A = sin²α − sin²δ`. The text names "A≈0 linear" as one
of four cases the breakpoint-finding must handle, but the actual root formula
given, `ζ_± = (−B ± √(B²−4AC))/(2A)`, is the textbook-unstable form: as
`A → 0` (i.e. angle-of-fall `α` approaching the belt half-angle `δ` — a real,
reachable parameter combination, not a contrived corner), `√(B²−4AC) → |B|`,
so `−B + |B|` (when `B>0`) is a subtraction of two nearly-equal numbers —
catastrophic cancellation — immediately followed by division by a near-zero
`2A`. At `A = 0` exactly it is a literal division by zero. Algebraically the
formula *does* degenerate correctly in the limit (one root → the true linear
root `−C/B`, the other → ±∞ and gets filtered by the `(0,h)` domain test), so
the defect is purely a floating-point stability issue in a naive
implementation, not a wrong model — but it will silently produce garbage
breakpoints for `α` near `δ` if implemented literally as written.

**How to apply:** when @modeler's src/ implementation pass (derivation §8)
lands, or when re-reviewing it, check that the belt-edge root solve uses the
numerically stable quadratic form (`q = −½[B + sign(B)·√disc]`, roots `q/A`
and `C/q`) with an explicit `abs(A) < eps` branch to the linear root
`ζ = −C/B`, rather than the naive `±` formula divided by `2A`. Not exercised
by any worked example in the derivation (default AoF=90°/δ=15° gives
`A ≈ 0.933`), so it won't show up in a spot-check at the standard config —
specifically probe `angle_of_fall` near `spray_half_angle` (or any config
where they're close) if verifying this pass.
