---
name: posture-vs-intercept-axis
description: The standing/prone A_p toggle and the target-column intercept are independent mechanisms — posture cannot fix a false safe zone
metadata:
  type: project
---

Two independent target mechanisms; conflating them is the recurring trap
("we have a standing/prone toggle — how is there still a false safe zone?"):

1. **Intercept/acceptance** — which fragments reach the target at all. The
   false-safe-zone bug lived in evaluating the FIELDS at z=0; fixed for the
   ground P(kill) field (`pkill_field_3d`, `four_zone_pkill_field`) by the
   column integral λ = w_perp·∫₀ʰ ρ_L dz. The graded Family-A fields still
   evaluate a single z. `fragment_ground_impact`'s v_gz<0 gate feeds no
   field (plots only) — not the culprit.
2. **Presented area A_p(γ, posture)** — how lethal an *arriving* fragment
   is. It never relocates the target off the evaluation height, so the
   toggle cannot close an intercept gap; mechanism 1 drops fragments before
   A_p is ever evaluated.

Post-fix split: the ground field is posture-coupled via the column integral;
`pkill_volume_3d` stays a point diagnostic at fixed `A_REF_DEFAULT`,
posture-independent by design. Derivation:
`updates/target-height-intercept/derivation.md`.
