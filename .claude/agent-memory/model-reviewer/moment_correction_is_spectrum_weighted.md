---
name: moment-correction-is-spectrum-weighted
description: A ratio-of-moments correction derived from a source sample carries that sample's weighting; check the sample mean against the model's own mean before it is applied across calibers
metadata:
  type: feedback
---

A correction of the form `c = ⟨f⟩/(⟨g⟩⟨h⟩)` derived from a source table is a
functional of the **joint** distribution, so it silently inherits the source
sample's *marginal* — it is not a material constant and does not transfer.

**Why:** the derivation's assumption list will justify the weighting as
"the same weighting the shipped mean uses" (internal consistency), which is
true and is not the question. The closure's `⟨·⟩` runs over the model's own
population.

**How to apply:** before accepting a global multiplier, compute the model's
own mean of the weighting variable per shell and compare with the source
sample's. If they diverge, re-weight the identical source table by each
shell's model spectrum and see whether `c` even keeps its sign. If `c`
depends on `μ` and `μ = c·μ₀`, that fixed point is contractive — iterate it,
don't treat self-reference as a reason to reject the formulation
([[unequal_comparison_asymmetric_evaluation]]).

Worked instance, with the per-caliber numbers and the reversed count-chain
arm: `experiment/fragmentation-field/updates/mass-dependent-fragment-shape/review.md`
(finding A1) and its `checks/spectrum-weighted-c-per-shell.py`.
