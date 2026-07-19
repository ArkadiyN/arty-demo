---
name: pkill-field-qmd-onset-formula-typo
description: a hand-written inline boundary-radius formula in notebook prose (not computed by code) can drop a term and go undetected even though the same cell prints a numeric result that contradicts it — check inline formulas against the src-computed number, not just against the derivation doc
metadata:
  type: project
---

`experiment/fragmentation-field/_pkill-field.qmd` ("The false safe zone it
removes" section, STANDING/AoF=90° example) states the inner true-dead-zone
boundary as "$r\lesssim h_b/\tan\delta$" — evaluates to 7.46 m (h_b=2,
δ=15°). The correct boundary (where the belt's lowest ray reaches head
height h) is $(h_b-h)/\tan\delta$ ≈ 1.12 m — confirmed against
`derivation.md` §6.3's own per-height table (`(h_b-z)/tanβ` at z=1.7 → 1.1
m), against `_limitations.qmd`'s parallel statement ("r≲1.1 m"), and by
direct root-find on `pkill_field_3d` (min lit r ≈ 1.1197 m). The wrong
7.46 m value directly contradicts the "100%" ring-fill figure the *same*
notebook cell prints two paragraphs earlier for the [1.5, 7.0] m ring — if
the dead zone really extended to 7.46 m, that ring could not be 100% lit.
Likely cause: compressing the derivation's `(h_b-z)/tanβ` per-height table
into a single inline formula for the reader and dropping the `-h`/`-z` term.

**How to apply:** any inline closed-form formula written directly into
notebook prose (not a `print()` of a computed value) is exactly the kind of
"new math in a .qmd" the layering gate exists to catch — even when it's just
restating an already-derived result rather than deriving something new, it
can silently diverge from both the source derivation and the notebook's own
computed numbers. When reviewing, evaluate every such inline formula
numerically and cross-check it against (a) the derivation doc's worked table
and (b) any nearby printed statistic in the same cell — don't accept it on
sight because the derivation.md it's summarizing is correct. Related to but
distinct from [[derivation_qualitative_claims_need_numeric_check]] (that one
is about untested qualitative fraction claims; this one is a plain algebraic
slip in a restated closed-form formula).
