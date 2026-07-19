---
name: pkill-volume-penumbra-is-outer-not-near-burst
description: single-zone fig_pkill_volume's P_k field is near-binary near the burst, but the four-zone field genuinely is NOT — it has a real, grid-stable, continuous near-burst low-value fringe; don't generalize a single-zone spot-check to the four-zone path
metadata:
  type: project
---

`pkill_volume_3d` (single-zone/legacy) has no continuous low-value fringe near
the burst at the app's actual slider ranges (`View radius` 10-30 m default; up
to 60 m max, `app/sensitivity.py` `_compute_volume_*`). Confirmed: at
AoF∈{30,60,90}°, h_b∈{2,5,10} m, radius∈{10,20,30} m, the count of voxels with
`0 < P_k < 0.05` is exactly zero in every combination, and this holds under
2-3x grid refinement (n_grid 40→120, n_z 30→90) — min nonzero P_k stays
~0.09-0.25, far above any isomin in [0.01,0.05]. The field jumps straight from
0 to that value because `lethal_density_point`'s belt-membership test is a
hard 0/1 angular cutoff with no angle-dependence *within* the belt (only
range-dependence) — see [[z_quadrature_belt_discontinuity]].

**`four_zone_pkill_volume` does NOT share this property** — checked
independently, this is a real, physically-distinct result, not a
generalization from the single-zone case. At the *same* AoF×h_b×radius grid
and app-default resolution (n_grid=40, n_z=30), most combinations have a
substantial count of voxels with `0 < P_k < 0.05` — e.g. AoF=30°/h_b=2m/r=30m:
10,340/48,000 voxels (21.5%), min nonzero 0.0016; AoF=90°/h_b=10m: nonzero at
*every* tested radius (10/20/30 m). Confirmed grid-stable (n_grid 40→80, n_z
30→50: fraction 21.54%→21.36%, 0.83%→0.73%, 0.20%→0.15% across three spot
combos) — a genuine feature of the four-zone field (multiple zones with
distinct angular half-widths/velocity distributions sum to a graded fringe),
not a sampling artifact. Only a narrow slice of parameter space (roughly
AoF=90°, h_b∈{2,5} m, r≤20 m) happens to read exactly zero low-value voxels.

**Why this matters:** a `plots.py::fig_pkill_volume` docstring round claimed
(citing a recompute across "the single-zone and four-zone fields") that *both*
paths are bimodal with zero voxels in (0,0.05) over the full AoF×h_b×radius
grid — true for single-zone, false for four-zone. The four-zone claim was
falsified on the very first independent recheck at app-default grid
resolution. Same lesson as
[[derivation_qualitative_claims_need_numeric_check]]: don't extend a
spot-checked single-zone (or single-combo) numeric claim to the four-zone path
without rerunning it there — the two models are not analogous here.

Also still true from the earlier round: the near-burst "void" in the raw
point field is a **pinched bicone** centered on the burst point (wide at z=0,
collapsing to zero radius at z=h_b), not a uniform "column" void, and a
standing target's torso/head near the burst sits in the lethal part of that
bicone even where z=0 reads P_k=0.

**How to apply:** if a future pass touches `fig_pkill_volume` /
`pkill_volume_3d` / `four_zone_pkill_volume` isomin/opacity tuning, or makes
any claim about the near-burst value distribution, recompute the (0, isomin)
voxel count **separately for both the single-zone and four-zone builders** at
the app's actual default view-radius/grid resolution — a result confirmed for
one is not evidence for the other.
