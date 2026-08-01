---
name: gotcha-density-falloff-shape-is-threshold-degenerate
description: Fitting a hits-vs-range falloff curve cannot discriminate drag — one free threshold absorbs any decay rate; use absolute counts instead
metadata:
  type: feedback
---

A hits-per-solid-angle-vs-range falloff (geometric 1/R² already divided out)
looks like a drag measurement but is **shape-degenerate**: with the marking/
lethality threshold free, combined `C_D*C_shape` from 0.585 to 2.93 fits the
same curve to within a flat residual. Refitting the threshold absorbs the
decay rate.

**Why:** validating drag against curve *shape* over a short baseline silently
returns "consistent with everything". The discriminating observable is the
**absolute count** above threshold, because fitting the ratio fixes m_thr and
then the count becomes a prediction — that test separated the drag candidates
by 11–14×.

**How to apply:** whenever a source offers both a normalised falloff and any
absolute fragment count, use the count as the discriminator and treat the
shape as a consistency check only. Worked example:
`experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1944-panel-distance.md`
(Results 1–2). See also [[gotcha-tolch-remaining-velocity-is-shell-not-fragment]].
