---
name: gotcha-mmin-table-perlayer
description: Sharing one m_min table across z-layers breaks the exact z0-matches-field tests; vectorize the bisection per-layer instead
metadata:
  type: feedback
---

The lethal-density/pkill **volume** builders must keep building the `m_min(s)`
table **per z-layer** (each with the layer's own `slant_range_grid`), not one
shared table over the whole box.

**Why:** four tests assert the volume's z=0 layer equals the standalone
`field(z=0)` at `rtol=0, atol=0`. A shared table changes s-grid node placement,
so the z=0 layer stops bit-matching the field (~1e-7 diff) → tests fail. The
speed win is not from sharing but from **vectorizing the bisection itself**
(`build_mmin_table`), which is bit-identical to the scalar `min_lethal_mass` if
each node is frozen once its bracket < tol.

**How to apply:** on any future field-builder perf pass, don't "cache the m_min
table across layers"; the per-layer table build is already cheap once the
bisection is vectorized. Full reasoning: updates/field-builder-performance/
derivation.md §2, §4.
