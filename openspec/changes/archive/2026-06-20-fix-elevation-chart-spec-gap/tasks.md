## 1. Dedupe ray-projection formula (src/arty/zones.py)

- [x] 1.1 Extract `fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)` from `fragment_ground_impact`'s inline trig
- [x] 1.2 Re-wire `fragment_ground_impact` to call `fragment_velocity` and apply its ground-impact guards on top, with no change to its public signature or behavior
- [x] 1.3 Add `tests/test_zones.py` coverage (or confirm existing `fragment_ground_impact` scenario tests still pass unmodified) verifying `fragment_velocity`'s output matches the pre-extraction inline formula — burst-geometry spec scenario "fragment_velocity matches fragment_ground_impact's pre-extraction formula"

## 2. Wire the app's spray-cone renderers to the shared source (app/sensitivity.py)

- [x] 2.1 Change `_spray_cone`/`_spray_cone_across` signatures to take `aof_deg` (dropping the precomputed `cA`/`sA`) and call `arty.zones.fragment_velocity` instead of recomputing `vgx`/`vgy`/`vgz` inline
- [x] 2.2 Update the four call sites in `_plotly_elevation`/`_plotly_elevation_across` for the new signatures
- [x] 2.3 Fix `_spray_cone_across`'s docstring (claimed phi=±90°; actual azimuths are φ∈{0, π})
- [x] 2.4 Numerically spot-check old-inline vs new `fragment_velocity`-based ray output across representative `(h_b, aof_deg, spray_deg, delta_deg)` cases and both ray-direction signs — confirms no rendering change (elevation-view-chart spec scenario "Spray-cone ray geometry is sourced from arty.zones, not re-derived")

## 3. Correct the elevation-view-chart spec

- [x] 3.1 Update the sensitivity-app elevation-chart requirement in `openspec/specs/elevation-view-chart/spec.md` to name `_plotly_elevation`/`_spray_cone` in `app/sensitivity.py`, not the notebook-only `fig_single_zone_elevation`/`fig_zone_elevation`
- [x] 3.2 Add the "sourced from arty.zones, not re-derived" scenario

## 4. Review

- [x] 4.1 @model-reviewer reviews the `fragment_velocity` extraction and its wiring in `app/sensitivity.py` — PASS
