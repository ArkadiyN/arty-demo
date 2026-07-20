---
name: cross-aspect-notebook-citation-staleness
description: A derivation's citation to "the notebook" can go stale when a LATER, unrelated aspect rewrites that .qmd section — check the citation resolves, not just whether the claim is true
metadata:
  type: project
---

`pkill-poisson-field/derivation.md` §4.7 cited `_pkill-field.qmd` for a
computed "~1-3% saturated" fraction. A later, separate aspect
(`target-height-intercept`, v0.5.1) fully rewrote that same `.qmd` file for
its own demo (different transform, different geometry) and the cited
computation no longer exists there — no contradiction, just a dangling
pointer. Recomputing the number independently via the still-live function
(`pkill_volume_3d`'s z=0 slice) confirmed it was still numerically correct
(3.18%/1.05%, grid-stable) — so the claim was fine, only the citation was
stale.

**How to apply:** when a derivation cites "the notebook" or a specific
`.qmd` section as evidence, don't stop at recomputing the *number* — open
the cited file and confirm the citing computation still exists there. A
later, unrelated aspect touching the same shared `.qmd` file is enough to
strand the pointer even when nothing about the cited claim changed.
Related: [[derivation_qualitative_claims_need_numeric_check]] (same failure
family, contradiction case rather than dangling-pointer case).
