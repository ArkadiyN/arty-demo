---
name: quadratic-root-cancellation-near-A-zero
description: Belt-edge quadratic ζ_± formula is fp-unstable as A→0 (angle-of-fall → spray half-angle) — require the stable form and probe that regime
metadata:
  type: project
---

The belt-membership boundary quadratic `Aζ² + Bζ + C ≤ 0` has
`A = sin²α − sin²δ`: the textbook `ζ_± = (−B ± √disc)/(2A)` suffers
catastrophic cancellation as α → δ (a reachable configuration) and literal
division by zero at A=0. The model is fine — the limit degenerates
correctly to the linear root — the defect is purely numerical in a literal
implementation.

**How to apply:** check the src/ root solve uses the stable form
(`q = −½[B + sign(B)√disc]`, roots `q/A`, `C/q`) with an `|A| < eps` linear
branch. Not exercised by the standard AoF=90°/δ=15° worked example
(A≈0.933) — specifically probe `angle_of_fall` near `spray_half_angle`.
See [[belt_edge_K_generalization_confirmed]] for confirmation that the
implemented form handles this.
