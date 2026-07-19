---
name: pkill-volume-bimodal-no-penumbra
description: Volume P_k is bimodal (no near-burst penumbra) ONLY on the single-zone path; four-zone has a real graded fringe — don't conflate
metadata:
  type: project
---

`pkill_volume_3d` (single-zone): bimodal — a voxel is exactly 0 or ≳0.05,
zero voxels in (0, 0.05) across the AoF × h_b × radius sweep, so lowering
isomin reveals nothing near the burst (only the outer envelope edge).

`four_zone_pkill_volume`: NOT bimodal — superposed zone cones give a real,
grid-stable graded near-burst fringe (~21% of voxels in (0, 0.05) at
AoF=30°/h_b=2/r=30 m). There isomin=0.01 genuinely reveals structure.

A docstring FAIL came from generalizing a single-zone spot check to the
four-zone grid — when verifying a whole-grid claim, sweep the whole grid on
BOTH paths.

Near-burst zero geometry is a pinched bicone (belt lights z = h_b ± r·tanδ),
not a column; head-lit annulus bounds: r from (h_b−1.7)/tanδ to h_b/tanδ.
Related: [[hard-step-fraction-grid-aliasing]], [[posture-vs-intercept-axis]].
