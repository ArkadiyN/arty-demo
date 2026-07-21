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

**Concrete trap when reusing the forward-axis belt machinery for the
single-zone path.** `belt_column_breakpoints` / `_belt_column_zrep_vec` are
written in the FORWARD-axis convention (`B=−2x cosα sinα`). To use them for the
backward-axis single-zone kernel you must pass `-x` (flips B's sign → the
backward-axis roots); the four-zone Family-A path uses `+x` directly.
**Why it bites:** at AoF=90° `cosα=0` so `B=0` and both signs coincide — every
AoF=90° test passes with the wrong sign. Off-axis (`AoF≠90°, x≠0`) the wrong
sign FABRICATES spurious interior breakpoints (not just a mirror), gating cells
on/off wrongly. Any change here needs an explicit off-axis regression test.
Instance: `familyA-false-safe-zone/derivation.md` §7 A3/§5.5,
`tests/test_familyA_false_safe_zone.py::test_offaxis_single_zone_axis_sign`.
