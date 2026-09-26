---
name: field-integral-box-truncation
description: Field-integrated ratios (sum P_kill dA) over a fixed ±60 m box truncate airburst far fields and bias posture ratios; sweep box size before trusting them
metadata:
  type: feedback
---

A lethal-area style aggregate over `compute_frag_field_3d`'s ±max_radius box is only
whole-field if P_kill at the box edge is ~0. At the notebook's ±60 m, the 105 mm 20 m
airburst still has P_kill ~0.016 at the edge. The truncation is **asymmetric by
posture**: the far field is low-γ, where standing presents more area, so the
prone/standing ratio is biased upward, toward a spurious flip.

**Why:** I accepted a ±60 m table in one pass and it produced a false ">1 at
near-horizontal AoF" row. The converged ratio (±200 m) was <1 everywhere. Detail is in
experiment/fragmentation-field/updates/target-area-profile/review.md ("fix cycle 1", R1).

**How to apply:** for any ΣP·dA or area-integrated comparison, print the edge-max
P_kill and rerun at 2–4× the box with the same spacing before trusting a threshold
crossing. Related: [[ground-grid-threshold-fraction-aliasing]].
