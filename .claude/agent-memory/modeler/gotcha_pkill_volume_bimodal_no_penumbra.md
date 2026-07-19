---
name: pkill-volume-bimodal-no-penumbra
description: The 3D P_k volume field is bimodal (0 or ≥~0.05, no near-burst penumbra) ONLY on the single-zone path (pkill_volume_3d). The four-zone path (four_zone_pkill_volume) is NOT bimodal — it has a real, grid-stable graded near-burst low-P_k fringe. Do not generalize the single-zone bimodal claim to four-zone.
metadata:
  type: project
---

`fig_pkill_volume` renders `pkill_volume_3d` (single-zone) OR
`four_zone_pkill_volume` (four-zone), both P_k = 1−exp(−ρ_L·A_ref) point-in-space
transforms. **The two paths behave differently near the burst — do not conflate
them** (this conflation drew a FAIL: a docstring spot-checked only the narrow
AoF=90°/h_b∈{2,5}/r≤20 m slice, which reads zero, and wrongly generalized
"bimodal / no penumbra" to the whole four-zone grid).

**Single-zone (`pkill_volume_3d`) — bimodal, no near-burst penumbra.** One
equatorial spray belt: a voxel is either exactly 0 (belt misses that height) or
already ≳0.05 (P_k saturates fast once intercepted). Recomputing across
AoF∈{30,60,90}°, h_b∈{2,5,10} m, Rview 10–30 m (app default n_grid=40,n_z=30):
**zero** voxels in (0,0.05) everywhere. Lowering `isomin` 0.05→0.01 reveals
nothing near the burst; the only low-P_k fringe is the OUTER envelope edge
(r≈55–85 m), visible only at max view radius.

**Four-zone (`four_zone_pkill_volume`) — NOT bimodal.** Superposes four zone
cones (ogive/cylinder/boattail/base) with distinct angular half-widths and
launch velocities; a height reached by only one narrow/slow zone carries small
nonzero ρ_L, producing a real **graded near-burst low-P_k fringe**. Same grid:
a substantial, grid-stable fraction of voxels fall in (0,0.05) at most
combinations (AoF=30°/h_b=2/r=30 m: 21.5%, stable n_grid 40→60→80:
21.5→21.4→21.4%, so not aliasing). Only AoF=90°/h_b∈{2,5}/r≤20 m reads exactly
zero (near-vertical fall collapses the cones onto one tight band). So on the
four-zone path isomin=0.01 genuinely reveals near-burst structure the 0.05
cutoff hid — not just the far outer taper.

**Near-burst zero geometry is a bicone, not a column** (single-belt picture).
Exactly-P_k=0 core is full-height only on the exact axis (r≈0). Off-axis it is
the lower nappe of a bicone: the belt (half-angle δ) lights a band centred on
z=h_b, z = h_b ± r·tanδ. Annulus where **ground (z=0) reads 0 while head (z=1.7
m, STANDING) is lethal**: lower bound (head-lit) = (h_b−1.7)/tanδ, upper bound
(ground-lit) = h_b/tanδ. For δ=15°: h_b=5 m → r≈12.3–18.7 m; h_b=2 m →
r≈1.1–7.5 m (the h_b=2 lower bound is ~1.1 m, NOT 1.5 m — an earlier docstring
had 1.5, ~30% high and inconsistent with its own h_b=5 numbers).

**How to apply:** when reasoning about the *volume* (point) P_k view, first ask
which path. Single-zone: no near-burst taper, reserve penumbra talk for the 2D
ground heatmap / `pkill_field` column integral. Four-zone: a genuine near-burst
fringe exists — do not claim it away. When "verifying" a whole-grid claim, sweep
the whole grid, not one slice. Related:
[[hard-step-fraction-grid-aliasing]], [[concept-posture-vs-intercept-axis]].
