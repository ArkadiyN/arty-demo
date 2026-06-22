## Context

`src/arty/fragmentation.py:compute_lethal_density_field_3d` and `src/arty/zones.py:four_zone_lethal_density_field` each evaluate ρ_L on an (x, y) grid at a single fixed height `z`. They are already implemented, reviewed (PASS), and presented as 2D ground-plane contour plots in the notebook (`experiment/fragmentation-field/_lethal-density.qmd`). A true 3D view needs ρ_L over a 3D `(x, y, z)` grid, which means evaluating the existing per-z function at multiple heights and stacking the results — no new formula, the same reviewed math at more sample points.

**Update (2026-06-21):** the rendered field changed from raw ρ_L to the point kill probability `P_k = 1 − exp(−ρ_L·A_ref)` (model aspect `pkill-poisson-field`, derivation reviewed PASS — see `experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md`). This was a separate, full new-math cycle (the `P_k` transform itself is a new derived quantity); the grid-stacking plumbing described below (D1) is unchanged by it — `pkill_volume_3d` / `four_zone_pkill_volume` apply the same z-loop-and-stack pattern as the ρ_L builders they wrap, just followed by the elementwise `P_k` transform. Everywhere below that says "ρ_L," the grid-construction/caching/resolution reasoning (D1, D3, D4) still applies verbatim to `P_k`; only D2's colour-scale tuning changed (see its update note) because `P_k` is bounded [0,1] while ρ_L spans orders of magnitude.

## Goals / Non-Goals

**Goals:**

- Render ρ_L as an interactive 3D Plotly `go.Volume` in `app/sensitivity.py`, for both the single-zone and four-zone paths, reusing the app's existing model-selection toggle.
- Keep the 3D grid construction cheap enough for interactive use (cached, modest default resolution), consistent with the user's stated preference for vectorization over reduced fidelity when performance is a concern.
- Keep the data pipeline (3D grid → scalar array) independent of the rendering style, so a fallback to `go.Isosurface` or `go.Scatter3d` is a one-function swap if volume rendering proves too visually busy.

**Non-Goals:**

- No notebook changes (confirmed with user: app only).
- No new physics, formulas, or parameters — this is purely evaluating the existing ρ_L functions at more points and visualizing the result.
- No change to the existing 2D heatmap views or their specs.

## Decisions

**D1 — Where the z-stacking loop lives: a thin grid-builder added to `src/arty/fragmentation.py` / `src/arty/zones.py`, written directly (no modeler derivation pass).**
The new-math gate triggers on a *physical or derived quantity* not already returned by `src/arty` — stacking the already-reviewed per-z evaluator over a z-array introduces no new formula or quantity, only more sample points of the same ρ_L. Per the project's own convention ("computation reused across figures belongs in `src/arty`, not inlined in app/notebook code"), the loop-and-stack helper (e.g. `compute_lethal_density_volume_3d`, `four_zone_lethal_density_volume`) is added to `src/arty`, but as plumbing — not a derivation — so it does not need a scoping/derivation/review cycle. `app/sensitivity.py` only imports and calls it.

**D2 — Rendering style: `go.Volume`, tuned, after two rounds of visual iteration.**
User confirmed: try volume rendering first; if too visually busy, fall back to isosurface or 3D scatter. The grid-builder returns plain `(X, Y, Z, rho_L)` 3D meshgrids — the same shape `go.Isosurface` and `go.Scatter3d` (flattened) both consume — so swapping the Plotly call does not require touching the data layer (this property held throughout both rounds below).

**Round 1 (rejected):** the default 25×25×20 grid spanning the app's full analysis radius (up to 80–200 m) produced sharp, jagged triangulated faceting with visible gaps in the low-density isosurface shells ("origami crane" artifact) — a marching-cubes coarse-grid effect, not a data issue; the dense core near burst rendered cleanly. Root cause diagnosed as **anisotropic, over-extended sampling**: the grid spacing in x/y (≈6 m at 25 points over 160 m) was far coarser than the field's actual length scale near the burst, and z (0.5 m at 20 points over 10 m) was disproportionately fine by comparison — most of the box was sampled far too sparsely relative to the 1/r² falloff. Switched to `go.Scatter3d` as the first fallback attempt (eliminates faceting structurally since it draws points, not fitted surfaces) — this worked but lost the smooth volumetric look the user wanted.

**Round 2 (adopted):** user supplied a reference image showing a smooth, well-resolved `go.Volume` blob and asked to retry rather than settle for scatter. Reverted to `go.Volume`, fixed the actual root cause instead of just changing trace type: the 3D view's spatial extent is **decoupled from the app's main `max_radius` slider** and defaults to a much smaller, burst-centered radius (≈30 m) so the existing grid resolution actually covers the field's interesting region densely, plus a higher default grid (`n_grid≈40`, `n_z≈30`, ~2 s compute, cached) and tuned trace parameters: `isomin = rho_max * 0.1` (crops the badly-resolved far tail rather than rendering it), `opacity=0.2`, `surface_count=25`, `caps` disabled on all axes, `colorscale="Hot"`. This combination reproduced the user's reference look with no visible faceting.

**D3 — Grid resolution, radius, and z-extent: modest defaults sized to the field's length scale, cached.**
Volume rendering needs `n_x × n_y × n_z` points, which grows faster than the existing 2D heatmap's `n_grid²`. Per the D2 round-1 finding, what matters for a smooth `go.Volume` render is not just point count but matching the grid's *spatial extent* to the field's actual length scale near the burst — so the 3D view gets its **own radius control, independent of the app's main `max_radius` slider**, defaulting to ≈30 m (vs. the main slider's 40–200 m range) plus a z-extent slider capped at a few multiples of `h_b`. Default grid resolution (`n_grid≈40`, `n_z≈30`) is higher than originally planned but still ~2 s to compute, cached exactly like the existing 2D field — consistent with the user's earlier direction to prefer vectorization/caching over cutting fidelity.

**D4 — Reuse the existing single-zone/four-zone toggle.**
The 3D view calls whichever of `compute_lethal_density_volume_3d` / `four_zone_lethal_density_volume` matches the app's current model-selection state, rather than introducing a separate selector.

## Risks / Trade-offs

- [Risk] `go.Volume` can be slow or visually noisy at higher resolutions in a browser. → Mitigation: conservative default grid (D3); design explicitly allows falling back to isosurface/scatter (D2) without a data-layer rewrite.
- [Risk] Adding `compute_lethal_density_volume_3d`/`four_zone_lethal_density_volume` to `src/arty` without a modeler pass could be seen as bypassing the project's physics-ownership convention. → Mitigation: scoped narrowly to looping + stacking an already-PASSed function with no new formula (D1); flagged explicitly in this design doc rather than done silently.
- [Risk] Two near-duplicate plotting helpers (matplotlib `fig_lethal_density_field` for the notebook vs. a new Plotly volume helper for the app) could drift. → Mitigation: both call the same `src/arty` data functions; only the rendering call differs, consistent with the existing app/notebook split for other charts (e.g. 2D heatmaps already use separate matplotlib/Plotly renderers).

**D2 update (2026-06-21) — fixed isomin/isomax for the bounded `P_k` field.**
The round-2 tuning above (`isomin = rho_max * 0.1`) was sized relative to ρ_L's own max because that field is unbounded and spans multiple decades. `P_k ∈ [0,1]` by construction (eq. (1) of `pkill-poisson-field/derivation.md`), so the natural range is already known and fixed rather than data-dependent: `isomin=0.05, isomax=1.0`, with the colourbar labelled `"P(kill) [-]"`. The rest of the round-2 tuning (`opacity`, `surface_count`, disabled `caps`, `colorscale="Hot"`) is unchanged. Per derivation.md §4.7, `P_k` saturates near 1 quickly with distance into the field (e.g. `P_k≈0.82` already at `ρ_L=2 m⁻²`), so most of the rendered volume is expected to show near-saturated colour with the graded variation concentrated in a thin fringe — this is a property of the quantity being plotted, not a rendering defect.

## Open Questions

(none — rendering style resolved in D2 above)
