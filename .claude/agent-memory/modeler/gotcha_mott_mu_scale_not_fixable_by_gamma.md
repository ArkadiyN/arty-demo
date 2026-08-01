---
name: mott-mu-scale-not-fixable-by-gamma
description: A fragment-count/size discrepancy in mott_params cannot be closed by re-picking gamma or sigma_f — the scale error lives in the cube closure
metadata:
  type: project
---

`mott_params` under-predicts fragment mass (mu ~4-15x too small vs Tolch 1944
pit screens). The reflex is to re-pick `gamma`/`sigma_f`. **Don't** — it is
arithmetically impossible: `mu ∝ (sigma_f/gamma)^1.5`, so 10x on mu needs 4.6x
on the ratio (sigma_f ~3.7 GPa or gamma ~14), far outside Mott's gamma = 42-67
table. The whole admissible box spans only ~1.5-2x on mu. See also
[[steel-sigma-gamma-ratio-only]].

sigma_f = 800 MPa is *Mott's own* number (rspa.1947.0042.md:201, "50 tons/sq.in.
work-hardened"), not a loose bracket pick — don't treat it as the soft spot.

The scale sits in the mass closure, and it is a **symbol mix-up, not a tuning
problem**: Gold 2017 eq. 4 closes Mott's circumferential breadth into a mass
with a *parallelepiped* shape factor `alpha = (l0/x0)*(t0/x0)`, then eq. 6
defines `gamma = alpha^(-2/3) * gamma'`. The shipped code uses Gold's
shape-absorbed eq. 16 but feeds it `gamma'` off Mott's carbon-content table —
which silently asserts alpha = 1, a **cube**. Gold's own gamma is calibrated
against explosive CJ pressure (he runs 50 for HF-1/Comp-B), not composition.
alpha ~ 4 covers most of the gap; V0 (terminal Gurney, not break-up) covers the
rest.

Evidence, fits and numbers:
`experiment/fragmentation-field/challenges/mott-scale-gap/_scale_verdict_ledger.md` and
`_shape_closure_check.md` (same dir).
