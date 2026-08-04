---
name: fixed-geometry-sweep-drag-degenerate
description: An observable swept at fixed range under constant-C_D exponential decay is exactly drag-degenerate — the decay factor folds into any fitted threshold, so it can never calibrate drag
metadata:
  type: project
---

Under $v(R) = V\exp(-R/L(m))$, the decay factor depends on $R$ and $m$ but
**not on $V$**. So any dataset swept along an axis *other than* $R$ — a
detonation/impact velocity, a charge, a firing condition — at **fixed
geometry** carries a drag factor that is identical at every point of the
sweep. It folds entirely into whatever marking/lethality threshold is being
fitted, and the predicted curve's shape is invariant under rescaling
$C_D C_{\text{shape}}$. Not "weakly sensitive" — exactly degenerate.

Concrete instance: Tolch 1938's base-spray density collapse vs the shell's
remaining velocity at burst, all at Panel A (15 ft). Detail in
`experiment/fragmentation-field/challenges/source-data-audit/review-provenance.md` §3c.
Even the axis that *does* vary $R$ there proved degenerate over a 5× $C_D$
span once the threshold was refitted.

**How to apply:** before accepting any source axis as a drag/decay
calibration anchor, ask two questions — (1) does the sweep vary $R$? (2) is
there a free fitted threshold? If the answer is no-then-yes, the anchor has
zero discriminating power regardless of data quality, and a card or
derivation recommending it is wrong on structure, not on precision. The
discriminating quantity in such a dataset is usually the **absolute count**,
not the ratio, because fitting the threshold to the ratio then makes the
count a prediction.
