---
name: pkill-poisson-es310-mismatch
description: P_k = 1-exp(-rho_L*A_ref) derivation must disclose it is the Pk|hit=1 limit of ES-310's own 1-(1-Pk|hit)^Nhits aggregate (Pk|hit=0.5 at the 1000J anchor) as a second, separate simplification beyond the rho_L kernel's binary cut — re-check this disclosure if eq(1) or E_leth changes
metadata:
  type: project
---

`experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md`
derives `P_k = 1 - exp(-ρ_L·A_ref)`. The source it cites for the casualty-
model shape, `doc-reference/wound-ballistics/fas-es310-damage-criteria`,
defines a **different** aggregate, `Pk = 1-(1-Pk|hit)^Nhits`, anchoring
`Pk|hit = 0.5` at exactly 1000 J — the same `E_leth` the prerequisite `ρ_L`
kernel uses (`fragmentation.py:141` `_PK_E/_PK_VAL`,
`pk_given_hit(1000.0) == 0.5`). `1-exp(-λ)` only equals ES-310's form when
`Pk|hit=1`, so eq.(1) is the `Pk|hit→1` limit, not the literal ES-310 result —
it is systematically more pessimistic at the same `ρ_L` (e.g. λ=2: ES-310
form 0.75 vs eq.(1)'s 0.865).

**The disclosure requirement, stated precisely:** this `Pk|hit:0.5→1`
promotion is a **second, separate** simplification from the prerequisite
`lethal-fragment-density-field` kernel's own binary `E_leth` cut (which
already frames counted fragments as "≥50% lethal on a hit," not certainly
lethal — derivation §3 there). A derivation that collapses these two into one
("binary cut ⇒ certain kill, by definition") understates its own pessimism
relative to the cited source and FAILs review; one that states them as two
stacked, separately-quantified steps PASSes (confirmed
2026-06-21 re-review — the fix added an explicit "not a logical consequence
of the binary cut" framing plus the quantitative λ=2/λ=5 comparison, all
independently re-verified numerically).

**Why this is easy to re-miss:** the dimensional/limit/monotonicity checks
pass cleanly regardless — the defect is purely in whether the *cited source*
supports the *specific aggregation formula chosen*, not in the algebra. You
have to open the cited `doc-reference/` file and compare its formula
directly, not trust that "ES-310 expected-hits shape" was paraphrased
correctly.

**If this resurfaces** (eq. (1) changed, `E_leth` changed, or a new pass
re-derives the Poisson step): re-check whether the per-hit lethality implicit
in whatever count is being exponentiated is disclosed as 1 (and as a step
separate from the kernel's own binary cut), or whether the derivation
re-conflates the two simplifications into one claim.
