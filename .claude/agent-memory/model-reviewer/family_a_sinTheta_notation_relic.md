---
name: family-a-sintheta-notation-relic
description: Quantified bound for the already-known legacy sinΘ quirk (see lethal_density_field_implementation.md) — 1/sin(90°−δ)−1, ~15.5% at the app's δ=30° max; confined to the single-zone path only
metadata:
  type: project
---

Extends [[lethal-density-field-implementation]]'s "legacy `_expected_kills_3d_point`
sinΘ bug" entry with the exact bound, derived from
`target-area-profile/derivation.md` §4.1.2's own `Ω_belt = 4π sinδ` algebra:
error vs. the Jacobian-free form is `1/sin(90°−δ)−1` — matches the
derivation's claimed "<3.5%" at δ=15°, but reaches **~15.5% at δ=30°**, the
app's `spray_half_angle` slider max. Confirmed still confined to the
single-zone legacy path (`_expected_kills_3d_point`/`_vec`) — the four-zone
Family-A path (`_four_zone_familyA_eval`, `zones.py:493,510`) already divides
by the fixed `sin(theta_z)`, not the point's own `sinΘ`, so it does not
carry this error.

Full writeup: `experiment/fragmentation-field/updates/target-area-profile/review.md`
(2026-07-19).
