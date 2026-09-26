## 1. src/arty grid-builders (no new physics — stacking existing per-z evaluators)

- [x] 1.1 Add `compute_lethal_density_volume_3d(shell, drag, burst, z_max, n_grid, n_z, E_leth, n_s)` to `src/arty/fragmentation.py`: loop `compute_lethal_density_field_3d` over a z-array from 0 to `z_max`, stack into 3D `(X, Y, Z, rho_L)` arrays.
- [x] 1.2 Add `four_zone_lethal_density_volume(zones, aof_deg, h_b, drag, rho_steel, z_max, n_grid, n_z, delta_deg, E_leth, n_s)` to `src/arty/zones.py`: same stacking pattern over `four_zone_lethal_density_field`.
- [x] 1.3 Add a pytest in `tests/` asserting the new volume builders' `z=0` slice is numerically identical (within float tolerance) to the existing single-z `compute_lethal_density_field_3d` / `four_zone_lethal_density_field` direct output for matching parameters — covers the "Volume grid matches the existing 2D field at z=0" scenario.

## 2. Plotly rendering helper

- [x] 2.1 Add `fig_lethal_density_volume(X, Y, Z, rho_L, title)` to `src/arty/plots.py`, distinct from the existing matplotlib `fig_lethal_density_field` used by the notebook.
- [x] 2.2 Shape the function so swapping the trace type later only touches this one function, not the data layer (per design.md D2). Exercised in practice across two rounds: `go.Volume` → `go.Scatter3d` (round 1, after faceting) → tuned `go.Volume` (round 2, after fixing extent/resolution); data layer never touched.

## 3. App wiring (app/sensitivity.py)

- [x] 3.1 Add a new expander/section for the 3D ρ_L view, placed near the existing 2D field views.
- [x] 3.2 Wire the section to call `compute_lethal_density_volume_3d` or `four_zone_lethal_density_volume` depending on the app's existing single-zone/four-zone model selection.
- [x] 3.3 Wrap the call in `@st.cache_data` keyed on shell, drag, burst, grid resolution, z-extent, and model selection — covers the "Repeated identical params do not recompute" scenario.
- [x] 3.4 Add a z-extent control (e.g. slider, capped at a few multiples of `h_b`) and a **separate view-radius control independent of the main `max_radius` slider** (default ≈30 m), with default grid resolution bumped to `n_grid≈40`, `n_z≈30` per design.md D3 (round 2) — covers the "Default grid resolution is bounded" scenario.
- [x] 3.5 Render the figure via `st.plotly_chart`.

## 4. Verification

- [x] 4.1 Run the full pytest suite and confirm no regressions.
- [x] 4.2 Manually exercise the app: toggle single-zone/four-zone, change burst geometry sliders, confirm the 3D view re-renders without error for both paths. (No browser tool available in this environment — verified headlessly via `streamlit.testing.v1.AppTest` driving both model modes, zero exceptions, figure trace confirmed present.)
- [x] 4.3 Visually assess whether `go.Volume` is legible or too busy. Round 1: rendered both model paths to PNG (kaleido + Chrome) — dense core near burst was clean, but the low-density isosurface shell showed jagged triangulated faceting with gaps at default grid resolution/extent — too busy; switched to `go.Scatter3d` (flagged to user, not silent). Round 2: user supplied a reference image of a smooth `go.Volume` render and asked to retry; diagnosed the real cause (extent too large for the grid resolution, not an inherent `go.Volume` limitation), decoupled the view radius from `max_radius`, raised resolution, tuned `isomin`/`opacity`/`surface_count`/`caps`, re-rendered to PNG and confirmed the artifact is gone — reverted to tuned `go.Volume`.
- [x] 4.4 Fix two small-view-radius defects surfaced by exercising the view radius down to its slider minimum (10 m). (1) Single-zone: `slant_range_grid` (`src/arty/fragmentation.py`) used a fixed 0.5 m floor for the m_min lookup table instead of the box's true geometric minimum slant range, tripping `AssertionError` when a z-layer landed near the burst height at small radius — fixed to derive the lower bound from `max(0, h_b − z_max, z_min − h_b)`. (2) Four-zone: `four_zone_lethal_density_field` (`src/arty/zones.py`) built its table's z-extent via `max(z, h_b)`, which collapsed the vertical offset to zero for layers below burst height and under-sized the table's *upper* bound, tripping the same assertion from the other end — fixed to pass the true layer height as both `z_max` and `z_min`, reusing the now-shared `slant_range_grid`. Both are grid-construction/lookup-table corrections (no new physics); verified by sweeping radius 10–30 m on both paths directly and through the app (AppTest), plus full pytest suite (195 passed, 4 skipped) — also separately confirmed the "tiny-looking volume" symptom at small radius is a genuine physical feature (tilted spray-belt asymmetry + steep 1/s² falloff cropped by `isomin`), not a defect.

## 5. ρ_L → P_k rewiring (supersedes the raw-ρ_L volume view above)

Per `experiment/fragmentation-field/updates/pkill-poisson-field/scoping.md` §4: the rendered field changed from raw ρ_L to the point kill probability `P_k = 1 − exp(−ρ_L·A_ref)`, derived and reviewed (PASS) as a separate model aspect.

- [x] 5.1 `src/arty/fragmentation.py` / `src/arty/zones.py` (modeler, src/ pass): add `pkill_field_3d` / `pkill_volume_3d` and `four_zone_pkill_field` / `four_zone_pkill_volume`, wrapping the existing ρ_L grid builders with the `P_k` transform and `A_REF_DEFAULT = 0.85` m². Reviewed PASS (oracle-script cross-check, bit-identical to manual ρ_L→P_k transform; full suite 202 passed, 4 skipped).
- [x] 5.2 `tests/test_pkill_field.py`: new tests for `ρ_L=0⇒P_k=0`, monotonicity, `P_k∈[0,1]` bounds (incl. saturation), per-wrapper bounds on real fields, z=0 slice identity for both single- and four-zone paths.
- [x] 5.3 `src/arty/plots.py`: renamed `fig_lethal_density_volume` → `fig_pkill_volume`; switched `isomin`/`isomax` from relative-to-field-max (ρ_L is unbounded, multi-decade) to fixed `0.05`/`1.0` (P_k is bounded [0,1]); colourbar/annotation text updated to `P(kill) [-]`.
- [x] 5.4 `app/sensitivity.py`: swapped the 3D-view imports/calls from `compute_lethal_density_volume_3d` / `four_zone_lethal_density_volume` / `fig_lethal_density_volume` to `pkill_volume_3d` / `four_zone_pkill_volume` / `fig_pkill_volume`; rewrote the expander header/caption to describe `P_k` (definition, `A_ref` convention, independence/sharp-threshold caveats) instead of raw ρ_L; renamed the local `rho_vol` variable to `pk_vol`.
- [x] 5.5 Verified: full pytest suite (202 passed, 4 skipped); headless `AppTest` run of both single-zone and four-zone modes with no exception and `plotly_chart` widgets present; direct render of both paths to PNG via `pkill_volume_3d`/`four_zone_pkill_volume` + `fig_pkill_volume` confirmed a graded [~0.1, ~0.9+] colourbar with a near-saturated core fading at the fringes (matches derivation.md §4.7's predicted near-saturation behavior), not an all-saturated or empty render.
- [x] 5.6 OpenSpec: capability renamed `lethal-density-3d-view` → `pkill-3d-view`; `proposal.md`, `design.md`, `specs/pkill-3d-view/spec.md` updated to specify `P_k` instead of ρ_L, per scoping.md §4.
