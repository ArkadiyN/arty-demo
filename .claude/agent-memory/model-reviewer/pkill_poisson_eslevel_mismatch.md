---
name: pkill-poisson-es310-mismatch
description: P_k = 1−exp(−ρ_L·A_ref) is the Pk|hit→1 limit of ES-310's aggregate — must be disclosed as a second, separate simplification
metadata:
  type: project
---

`pkill-poisson-field/derivation.md` derives `P_k = 1−exp(−ρ_L·A_ref)`, but
the cited source (`doc-reference/wound-ballistics/fas-es310-damage-criteria`)
defines `Pk = 1−(1−Pk|hit)^Nhits` with `Pk|hit=0.5` at the same 1000 J
anchor. Eq. (1) equals that only as `Pk|hit→1`, so it is systematically more
pessimistic (λ=2: 0.865 vs 0.75).

**Disclosure requirement:** the `Pk|hit: 0.5→1` promotion is a SECOND
simplification, separate from the ρ_L kernel's binary E_leth cut. Collapsing
them into one ("binary cut ⇒ certain kill") FAILs; two stacked, quantified
steps PASS (the current derivation does this).

**Easy to re-miss:** dimensional/limit/monotonicity checks pass regardless —
you must open the cited doc-reference file and compare the formula itself.
Re-check the disclosure whenever eq. (1) or E_leth changes.
