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
   inner safe ring; posture-INDEPENDENT. Target is a thin patch AT the ground
   plane; horizontal fragments (cylinder belt at AoF=90°) never reach `z=0` and
   are dropped. `_limitations.qmd` lines 184-204 is about this.
   **Trap:** the note (and the brief) name `fragment_ground_impact`
   (`zones.py`, gate `v_gz<0`) as the culprit/fix target, but that function
   feeds NO field — its only callers are the `plots.py` spray-cone dot renderer
   and `_four-zone-3d.qmd`. The bug actually lives in evaluating the FIELDS at
   `z=0`: the belt test `|cosΘ−cosθ_z|≤sinδ` + zone gate `sin(aof+θ_z)≤0` in
   `four_zone_field`/`_four_zone_field_split`/`_expected_kills_3d_point` (graded,
   Family A) and the `z=0` slice of the ρ_L fields (Family B). Fixing
   `fragment_ground_impact` alone changes nothing on the heatmaps. The Family-B
   ρ_L/P(kill) fields already take a `z` arg and evaluate any height (so the 3D
   volume view is already unaffected). Full audit + recommended fix (vertical
   `w_perp·∫₀ʰ ρ_L dz` intercept): `updates/target-height-intercept/scoping.md`.
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

Extra: the P(kill) Poisson volume field freezes area at `A_REF_DEFAULT=0.85 m²`
(`fragmentation.py` 403-412), posture-INDEPENDENT by design — so the P(kill)
view ignores the toggle entirely (app self-documents this, `app/sensitivity.py`
~962). `_limitations.qmd` describes mechanism 1 but does not explicitly say the
posture toggle is a different axis — a clarity gap in that artifact.
