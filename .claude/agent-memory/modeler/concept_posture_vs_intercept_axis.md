---
name: posture-vs-intercept-axis
description: Why the standing/prone posture toggle does NOT fix the false-safe-zone gap — target size and ground-plane intercept are two separate axes of the frag-field physics
metadata:
  type: project
---

Frag-field target modelling has TWO independent mechanisms; conflating them is
the trap (user has asked "but we implemented target size / have a standing-prone
toggle — so how is there still a false safe zone?").

1. **Ground-plane intercept / acceptance test** — the "false safe zone" /
   inner safe ring. Target was a thin patch AT the ground plane; horizontal
   fragments (cylinder belt at AoF=90°) never reach `z=0` and were dropped.
   **FIXED (v0.5.1) for the Family-B ground P(kill) field** — `pkill_field_3d`
   (`fragmentation.py`) and `four_zone_pkill_field` (`zones.py`) now form
   `λ = w_perp·∫₀ʰ ρ_L dz` over the target column instead of `ρ_L(z=0)·A_ref`,
   so the ring fills and posture re-couples (STANDING ring 100% P_k>0 vs PRONE
   0% at AoF=90°). Derivation: `updates/target-height-intercept/derivation.md`.
   The graded Family-A fields (`four_zone_field`/`_four_zone_field_split`/
   `_expected_kills_3d_point`) still evaluate a single `z` and are NOT covered
   by this fix.
   **Trap (still live):** `fragment_ground_impact` (`zones.py`, gate `v_gz<0`)
   is NOT the culprit — it feeds no field (only the `plots.py` spray-cone dot
   renderer and `_four-zone-3d.qmd`). The bug lived in evaluating the FIELDS at
   `z=0`, not in that gate.
2. **Presented area A_p(γ)** — `presented_area(gamma,posture)` (`fragmentation.py`
   190-192) `= w_perp·(h·cosγ + d·sinγ)`; STANDING(h=1.7,d=0.3) vs PRONE
   (h=0.3,d=1.8). This is the posture toggle. It scales the silhouette a fragment
   sees GIVEN it already arrived at a `z=0` cell. It does NOT relocate the target
   off the ground plane or give it a ray-traced vertical VOLUME.

**Gotcha:** the toggle changes how lethal an *arriving* fragment is, not *which*
fragments arrive. Mechanism 1 runs first and drops horizontal fragments before
A_p is ever evaluated — so posture cannot close the false-safe-zone gap. The
proposed fix (ray vs target volume `[0,h_person]`) is a change to mechanism 1,
orthogonal to the A_p posture weighting.

Extra: after v0.5.1 the split is — the P(kill) **ground field**
(`pkill_field_3d`/`four_zone_pkill_field`) is posture-coupled via the column
integral (mechanism 1). The P(kill) **3-D volume** field still freezes area at
`A_REF_DEFAULT=0.85 m²` (`pkill_volume_3d`), posture-INDEPENDENT by design as
the point-in-space diagnostic ("one person at exactly this z"). So the volume
view ignores the toggle; the ground field does not.
