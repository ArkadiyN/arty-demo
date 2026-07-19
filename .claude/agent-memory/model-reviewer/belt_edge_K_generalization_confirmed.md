---
name: belt-edge-K-generalization-confirmed
description: belt_column_breakpoints' per-zone K=cosθ^z±sinδ generalization is sound — don't re-derive; retest equivalences at an asymmetric AoF
metadata:
  type: project
---

`fragmentation.py:belt_column_breakpoints`' per-zone `K = cosθ^z ± sinδ`
quadratic is the same substitution as derivation eq. 5 with K replacing
sinδ — verified by hand-derivation and against a brute-force reference
across all four zones (<0.01%). Spurious `cosΘ=−K` roots from squaring are
harmless (both ±K collected; extra breakpoints only subdivide smooth
intervals), and `_stable_quadratic_roots` degenerates correctly as A→0
without the explicit fallback branch firing. Don't re-litigate any of this.

**Durable verification trap (self-caught):** AoF=90° is rotationally
symmetric, so a transposed row/column slice comparison can pass for the
wrong reason — a first check of `four_zone_pkill_line` vs the field did
exactly that. Any numeric equivalence check between a zones.py line helper
and its 2D field counterpart MUST use an asymmetric AoF. Same root cause as
[[zones_meshgrid_convention]] / [[belt_axis_convention_pitfall]].
