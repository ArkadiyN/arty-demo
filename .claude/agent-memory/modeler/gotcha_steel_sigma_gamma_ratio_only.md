---
name: steel-sigma-gamma-ratio-only
description: SteelParams sigma_f and gamma are not independently identifiable — only the ratio sigma_f/gamma affects anything
metadata:
  type: project
---

`SteelParams.sigma_f` and `.gamma` enter the entire codebase only via
`fragmentation.py:mott_params`, and only as `(sigma_f/gamma)**1.5`. (`rho` is
separate — it also drives `retardation_coeff`.)

**Gotcha:** a "calibrate/estimate the steel parameter pair" task looks like two
numbers but is **one** identifiable DOF plus a split convention. No
fragment-count, field or P(kill) observable can separate them, so any argument
that fixes sigma_f and gamma independently is arguing about something the model
cannot see. Fix one by convention, move the other, and say so.

Scaling: `mu ∝ R^1.5`, `N0 ∝ R^-1.5` with `R = sigma_f/gamma`.

Composition→gamma data (dimensionless, so unit-safe) is Mott 1947 §3 table,
`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`
lines 282–288; that scan's stress column has ambiguous units and its equations
are OCR-garbled — cite Gold 2017 PAFRAG eq. 16 for mu, not this file.
Full reasoning: `experiment/fragmentation-field/updates/wdss1-steel-grade/scoping.md` §2–3.
