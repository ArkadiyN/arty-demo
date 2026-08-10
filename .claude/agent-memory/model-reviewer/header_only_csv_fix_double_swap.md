---
name: header-only-csv-fix-double-swap
description: a CSV column-swap fix that only renames headers (not reordering data) leaves any reader script with a manual compensating reversal double-swapped
metadata:
  type: feedback
---

When a source-data-fidelity column-transposition fix is committed as a
**header-rename only** (row values unchanged, e.g. `hardness_pounds,density_..`
→ `density_...,hardness_pounds` with the same numbers per row), any check
script that was reading the old headers and **manually reversing** them to
compensate becomes silently wrong post-fix — it now applies a second,
redundant swap to an already-corrected file.

**Why:** exactly this happened in
`experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/`:
commit `10303e0` fixed the CSV header order; a sibling check script's
`wood_props()` kept its pre-fix reversal, producing rho/H swapped by ~1.6x and
table values off by up to 3x from what the document it's supposed to verify
actually cites. Full finding: `.../review.md` Finding 1.

**How to apply:** when reviewing any pass that includes a column-transposition
fix, grep for *other* consumers of the same file (`grep -rl <csv-path>`) and
check each one's read logic against the *post-fix* header meaning — not just
the script the fix commit itself touched.
