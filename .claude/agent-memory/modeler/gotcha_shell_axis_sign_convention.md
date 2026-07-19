---
name: shell-axis-sign-convention
description: Single-zone vs four-zone e_axis sign conventions differ and were never proven equivalent — standardised by construction only
metadata:
  type: project
---

Legacy single-zone `_shell_axis = (−cosα,0,−sinα)` (backward); four-zone and
the new single-zone `lethal_density_point` (via `_forward_shell_axis`) use
`(+cosα,0,−sinα)` (forward). A partial x-only sign flip is NOT negating the
whole vector: the two belt tests are provably equal only on the x=0 plane,
and a hand-checked off-axis point falsifies pointwise equivalence.

Do not re-derive or re-assert an analytic equivalence claim. The resolved
framing is "deliberate standardisation by construction, verified
empirically." The legacy `_shell_axis` / `_expected_kills_3d_point` pair is
intentionally not reconciled. Counterexample and full reasoning:
`lethal-fragment-density-field/derivation.md` §5.4 and `review.md`.
