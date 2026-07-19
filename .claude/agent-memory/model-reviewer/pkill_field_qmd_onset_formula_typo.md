---
name: pkill-field-qmd-onset-formula-typo
description: Inline prose formulas in a .qmd can silently drop a term — evaluate them numerically against the cell's own printed results
metadata:
  type: project
---

A hand-written boundary formula in `_pkill-field.qmd` prose stated the inner
dead zone as `h_b/tanδ` (7.46 m) instead of `(h_b−h)/tanδ` (≈1.12 m) —
contradicting the 100% ring-fill number printed two paragraphs earlier in
the SAME cell, plus the derivation's own table and `_limitations.qmd`.
Likely cause: compressing a per-height table into one formula and dropping
the −h term.

**How to apply:** treat every inline closed-form formula in notebook prose
(anything not a `print()` of a computed value) as the "new math in a .qmd"
the layering gate exists to catch: evaluate it numerically and cross-check
against (a) the derivation's worked table and (b) nearby printed statistics
in the same cell.
Related: [[derivation_qualitative_claims_need_numeric_check]].
