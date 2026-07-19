---
name: pkill-volume-penumbra-is-outer-not-near-burst
description: Single-zone volume P_k is near-binary near the burst; the four-zone field genuinely is NOT — recompute claims separately per path
metadata:
  type: project
---

`pkill_volume_3d` (single-zone): zero voxels with 0 < P_k < 0.05 across the
whole AoF × h_b × radius sweep, stable under 2–3× grid refinement — the
belt test is a hard cutoff with no within-belt angle dependence, so the
field jumps 0 → ~0.09+. The only low-P_k fringe is the outer envelope edge.

`four_zone_pkill_volume`: NOT shared — most parameter combinations show a
substantial, grid-stable low-value voxel fraction (~21% at
AoF=30°/h_b=2/r=30 m); a genuine graded fringe from superposed zone cones.
A docstring claim generalizing single-zone bimodality to both paths was
falsified on the first independent recheck.

The near-burst P_k=0 void is a pinched bicone (collapsing at z=h_b), not a
uniform column — a standing target near the burst can be lethal at torso
height where z=0 reads 0.

**How to apply:** any isomin/opacity tuning or near-burst value-distribution
claim on `fig_pkill_volume` must recompute the (0, isomin) voxel count
separately for BOTH builders at app-default grids
([[derivation_qualitative_claims_need_numeric_check]]).
