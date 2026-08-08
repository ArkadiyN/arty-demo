---
name: gotcha-n0-insensitive-to-case-mass
description: N0 barely moves when M_case is corrected, because mu ~ V0^-3 cancels it; the real shift is in V0 and mu
metadata:
  type: project
---

Correcting a shell's `M_case` (e.g. a wrong `mass_deductions`) moves `N0`
almost not at all: `N0 = M_case/2mu`, but a smaller case raises Gurney `V0`,
and `mu ∝ V0⁻³`, so the two effects nearly cancel. A 16 % `M_case` error on
75 mm M48 shifted `N0` by under 5 % (3627 → 3801).

**Why:** it makes a real mass-bookkeeping defect invisible on any
fragment-count comparison — the surface people naturally check.

**How to apply:** never validate a case-mass fix on `N0` or count ratios.
The materially-shifted quantities are `V0` (+10 %) and `mu` (−18 %), i.e.
per-fragment energy and the mass spectrum. Full variant table:
`experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/scoping.md`.
See also [[gotcha-r50-insensitive-to-steel]].
