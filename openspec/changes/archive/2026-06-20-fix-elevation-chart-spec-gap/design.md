## Context

`_spray_cone`/`_spray_cone_across` in `app/sensitivity.py` re-derived the
fragment ray-projection trig (`vgx`/`vgy`/`vgz`) inline instead of going
through `arty.zones`, where `fragment_ground_impact` already implements and
documents that exact formula (see `burst-geometry` spec). The
`elevation-view-chart` spec also misattributed the app's elevation charts to
the notebook-only matplotlib functions in `src/arty/plots.py`.

## Goals / Non-Goals

**Goals:**

- Single source of the AoF-rotation ray-direction formula, reused by both
  `fragment_ground_impact` and the app's spray-cone renderers.
- Correct the `elevation-view-chart` spec to name the actual app-local Plotly
  functions and their file.

**Non-Goals:**

- No new physics or behavior change to the rendered charts.
- Does not address the pre-existing `x_slice`/`y_slice` staleness in the
  silhouette-suppression language already in the spec (separate, flagged to
  the user as a follow-up, out of scope here).

## Decisions

- **Extracted `fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)` in `src/arty/zones.py`**, factored out of `fragment_ground_impact`'s
  body. `fragment_ground_impact` now calls it and applies its own
  ground-impact guards (`vgz >= -1e-6` early-return, `arcsin` domain clamp) on
  top — those guards stay local to `fragment_ground_impact`, not duplicated
  into the new primitive, since they're specific to the ground-impact use
  case (the app's capped-ray rendering needs the raw direction without them).
  Alternative considered: exposing the existing `(vgx, vgy, vgz)` tuple via a
  new keyword on `fragment_ground_impact` itself — rejected because the app
  needs the direction for rays that never hit the ground (capped at
  `max_len`), where `fragment_ground_impact` itself would return `None`.
- **Changed `_spray_cone`/`_spray_cone_across` signatures to take `aof_deg`
  directly**, replacing the precomputed `cA`/`sA` (and `sA` alone) they
  previously took. The original proposal's "no signature changes" framing
  didn't survive contact with `fragment_velocity`'s actual parameter list; both
  call sites already have `aof_deg` in scope, so passing it straight through
  is simpler than reconstructing it from `cA`/`sA` via `arctan2`/`arcsin`.
  `_plotly_elevation`'s own local `cA`/`sA` (used separately for the shell
  arrival arrow) were left untouched.
- **Fixed `_spray_cone_across`'s docstring**, which claimed the two lobes are
  at "phi=±90°" — the actual azimuths are φ∈{0, π} (`y_sign=+1` → φ=0,
  `y_sign=-1` → φ=π). Caught independently by both the implementing pass and
  review.
- **Spec correction is additive, not a rewrite**: the existing requirement
  text for the sensitivity-app elevation chart is kept, with the function
  names/file corrected and a new scenario added asserting the ray geometry is
  sourced from `arty.zones.fragment_velocity`.

## Risks / Trade-offs

- [Risk] Behavior could shift subtly when reading the inline trig as a
  black-box. → Mitigation: numerical spot-check comparing old-inline vs new
  `fragment_velocity`-based output across multiple `(h_b, aof_deg, spray_deg, delta_deg)` cases and both ray-direction signs showed max abs error
  ~4e-14 (floating-point noise only); full test suite (191 passed/4 skipped)
  and the 34 `tests/test_zones.py` cases pass unmodified.
