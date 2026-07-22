---
name: belt-axis-convention-pitfall
description: An x-component-only axis flip is not a full vector negation and mirrors the whole down-range lobe — re-derive any axis "equivalence" claim off-axis before trusting it
metadata:
  type: project
---

A shell-axis convention like `(−cosα,0,−sinα)` vs `(+cosα,0,−sinα)` differs
only in the x-component — that is a mirror reflection across x=0, not a
vector negation, so `|cosΘ|`/belt membership is NOT invariant between them
off the x=0 / AoF=90° planes. A claim that two such conventions are
"equivalent by construction" or "benign off-axis" is exactly the shape of
claim that turned out to hide a real mirror bug in this project once
(`legacy-field-shell-axis-fix`, `fragmentation.py:_shell_axis`).

**How to apply:** any claim that two belt-axis conventions are "equivalent"
— hand-check a concrete off-axis point (x≠0, α≠0) and re-derive the algebra
before accepting.

**Recurrence trap:** grep the whole **repo**, not just the file being
edited, for call sites before deleting a function an audit calls "dead" —
this project's own axis-fix scoping missed a caller in a test file that an
in-file-only grep wouldn't catch.

See [[zones_meshgrid_convention]], [[lethal_density_field_implementation]].
