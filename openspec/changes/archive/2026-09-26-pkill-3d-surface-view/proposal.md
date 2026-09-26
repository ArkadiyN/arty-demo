## Why

The sensitivity app currently only shows ρ_L (and the legacy P(kill) field) as 2D ground-plane (z=0) heatmaps. There is no way to see how the lethal-fragment density actually behaves above the ground — e.g. near the burst point or at a target's standing height — even though `compute_lethal_density_field_3d` and `four_zone_lethal_density_field` already evaluate the field at arbitrary `(x, y, z)`. A prior attempt at a 3D view mapped target-coupled P(kill) magnitude onto a height axis, which was rejected as physically incoherent (P(kill) already lives on the 2D ground plane). The newly reviewed, target-independent ρ_L(x,y,z) field has no such problem — it is a genuine 3D scalar field — so it is the right quantity to finally add a true 3D view for.

While building the view, raw ρ_L [m⁻²] turned out to be hard to read directly: it is a flux density, not a probability, and its dynamic range spans orders of magnitude near vs. far from the burst, so a colour scale tuned for one region saturates or washes out another. The `pkill-poisson-field` model aspect (`experiment/fragmentation-field/updates/pkill-poisson-field/`, derivation reviewed PASS) converts ρ_L into a bounded, reader-legible point kill probability `P_k(x,y,z) = 1 − exp(−ρ_L·A_ref) ∈ [0,1]` — "if a representative person stood here, what's the chance at least one lethal fragment hits them" — using a fixed nominal personnel area `A_ref = 0.85 m²`. This change therefore renders `P_k`, not raw `ρ_L`.

## What Changes

- Add a new interactive 3D view to `app/sensitivity.py` rendering `P_k(x,y,z)` as a Plotly `go.Volume` over a 3D grid spanning ground level up to a configurable height, for both the single-zone and four-zone paths (mirroring the app's existing single-/four-zone toggle).
- The 3D field evaluation (calling `pkill_volume_3d` / `four_zone_pkill_volume`, which wrap the existing per-z ρ_L evaluators and apply the Poisson `P_k` transform, over a z-range) is wrapped in `@st.cache_data`, consistent with the existing 2D field caching.
- The `ρ_L → P_k` transform is new math (a new derived quantity) and went through the full derivation → review → `src/arty/` cycle as the separate `pkill-poisson-field` model aspect; this change only wires the resulting, already-reviewed `pkill_volume_3d` / `four_zone_pkill_volume` functions into the app. No physics is authored here.
- Volume rendering is the rendering style, tuned for `P_k`'s bounded [0,1] range (fixed `isomin`/`isomax`, rather than relative to the field's own max as was needed for unbounded ρ_L); if it proves too visually busy in practice, the design allows falling back to an isosurface or 3D-scatter style without changing the underlying data pipeline (see design.md).

## Capabilities

### New Capabilities

- `pkill-3d-view`: the interactive 3D (x, y, z) volume-rendered `P_k` view in the Streamlit app — grid construction, caching, Plotly `go.Volume` rendering, and single-/four-zone toggle behavior.

### Modified Capabilities

(none — `sensitivity-app`'s existing requirements are unchanged; this adds a new self-contained view alongside them)

## Impact

- `app/sensitivity.py`: new UI section/expander, new cached field-evaluation call, new Plotly figure.
- `src/arty/plots.py`: a new `fig_pkill_volume(...)` Plotly plotting helper (app-only — distinct from the existing matplotlib `fig_lethal_density_field` used by the notebook).
- `src/arty/fragmentation.py` / `src/arty/zones.py`: the `pkill-poisson-field` aspect added `pkill_volume_3d` / `four_zone_pkill_volume` (and their 2D counterparts), wrapping the already-implemented, already-reviewed ρ_L grid builders with the `P_k = 1 − exp(−ρ_L·A_ref)` transform — see `experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md`.
- No changes to the Quarto notebook (scope confirmed with user: app only).
