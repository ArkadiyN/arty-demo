---
name: pkill-columns-padded-segment-bounds
description: _pkill_columns_vec pads collapsed belt segments to z=h_b, so a bounds check over all samples false-fires on zero-weight artifacts
metadata:
  type: project
---

`_pkill_columns_vec` (fragmentation.py) pads collapsed belt segments (width 0,
weight 0) by forcing `z=h_b` → `dz=0` → spurious `s=`horizontal-radius, which
can fall *below* the m_min `s_grid` floor. Those samples carry zero integration
weight and are never evaluated by the scalar reference path.

**Why:** a naive `np.interp` bounds guard over *all* `s_safe` samples false-fires
on these artifacts (observed: assert tripped on the standard benchmark case).
Restrict any such guard to weighted samples (`wt > 0`).

**How to apply:** when adding/moving a slant-range bounds check in the vectorised
column integral, mask by weight first. Full reasoning: field-builder-performance
derivation.md §7 (Deferrable closure) and §3.
