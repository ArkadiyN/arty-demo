---
name: moment-correction-is-spectrum-weighted
description: A ratio-of-moments correction derived from a source sample carries that sample's weighting; check the sample mean against the model's own mean before it is applied across calibers
metadata:
  type: feedback
---

A correction of the form `c = ⟨f⟩/(⟨g⟩⟨h⟩)` derived from a source table is a
functional of the **joint** distribution, so it silently inherits the source
sample's *marginal* — it is not a material constant and does not transfer.

**Why:** the derivation justifies the weighting as "the same one the shipped
mean uses" (internal consistency) — true, and not the question. The closure's
`⟨·⟩` runs over the model's own population.

**How to apply:** re-weight the identical source table by each shell's own
model spectrum. If `c` depends on `μ` and `μ = c·μ₀`, that fixed point is
contractive — iterate it ([[unequal_comparison_asymmetric_evaluation]]).

**Second form:** `⟨fg⟩/⟨f⟩⟨g⟩ = c·k` is exact only over ONE population.
Re-deriving one factor from a better source while leaving the other on its
old weighting is a mixed pair that need not lie between the two
self-consistent answers. Ask which population each `⟨·⟩` runs over — and,
when rival populations are scored side by side, whether each row closed its
own `μ` fixed point or was left at `μ₀`; only one side usually did.

Worked instances: `.../updates/mass-dependent-fragment-shape/review.md`
(A1, `checks/spectrum-weighted-c-per-shell.py`) and
`.../updates/breadth-variance-factor-k/review.md`.
