---
name: gotcha-n0-insensitive-to-case-mass
description: N0 is NOT linear in M_case despite N0 = M_case/2mu — Gurney feedback cancels ~93% of it; sensitivity is (C/M)/(2+C/M) ~ 0.07
metadata:
  type: project
---

`N0 = M_case/(2 mu)` reads linear in case mass, but `mu` depends on `V0` which
depends on `M_case`. With the Mott shape closure, `mu ∝ V0^-2` (not `V0^-3` —
the `alpha^(-2/3)` gamma correction eats one power), so

    N0 ∝ C·M_case/(M_case + C/2),   ∂lnN0/∂lnM_case = (C/M)/(2 + C/M)

≈ 0.055–0.092 across the registry. **Fragment count is set by filler mass, not
case mass** (∂lnN0/∂lnC ≈ 0.93).

**Why:** a scoping pass sized a 16% `M_case` defect as a 16% count error and
mis-ranked the whole aspect; the real shift was +4.8%, and most of *that* came
from the filler moving.

**How to apply:** before sizing any `mass_total`/`mass_filler`/
`mass_deductions` exposure, use the formula above — deduction errors are
usually far inside the fidelity bar, filler errors are not. Derivation + the
analytic-vs-finite-difference check:
`experiment/fragmentation-field/updates/shell-case-mass-basis/derivation.md`
sect. 5 and its `checks/registry-case-mass-consistency.py`.
See also [[gotcha-tolch-empty-shell-includes-fuze]].
