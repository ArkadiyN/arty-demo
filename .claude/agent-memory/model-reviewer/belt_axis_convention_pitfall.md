---
name: belt-axis-convention-pitfall
description: Single-zone vs four-zone shell-axis signs agree only on x=0 — re-derive any "equivalence" claim algebraically, grep for sibling phrasing
metadata:
  type: project
---

`fragmentation.py:_shell_axis = (−cosα,0,−sinα)`; `zones.py` four-zone paths
use `(+cosα,0,−sinα)` — an x-component-only flip, which is NOT negating the
whole vector, so `|cosΘ|` is not invariant: the belt tests provably agree
only on x=0 (or α=0). Only the aggregate field magnitude was ever validated;
pointwise cosΘ agreement does not hold (off-axis hand-checked counterexample).

**How to apply:** any claim that the two belt tests are "equivalent" /
"identical in magnitude" — including reworded forms ("safe normalisation",
"no physics change", "exact attribution/isolation" of a diff like
`app/sensitivity.py`'s `diff_pk`, whose two sides sit on unreconciled axis
conventions) — hand-check a concrete off-axis point (x≠0, α≠0) and re-derive
the algebra symbolically before accepting. The only framing that survives
review is "deliberate standardisation by construction, verified numerically"
(see `lethal-fragment-density-field/review.md`).

**Recurrence trap:** fixing one flagged phrasing instance doesn't sweep the
file — grep the whole file for "isolat", "exact", "diff" before sign-off (a
second instance survived in `_four-zone-3d.qmd` §6.8, attached to a plot
that performs no diff at all).

See [[zones_meshgrid_convention]] (grid-indexing pitfall, same file) and
[[lethal_density_field_implementation]] (the legacy path's sinΘ bug).
