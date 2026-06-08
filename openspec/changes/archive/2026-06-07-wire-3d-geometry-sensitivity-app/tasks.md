## 1. Add `_four_zone_field_split` helper to `zones.py`

- [x] 1.1 Add `_four_zone_field_split(zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, max_r, n_grid, delta_deg)` to `src/arty/zones.py` — identical loop body to `four_zone_field` but accumulates a `field_N_by_zone` dict keyed by zone name alongside the total `field_N`, and returns `(X, Y, pk_total, pk_by_zone)` where `pk_by_zone[z] = 1 - exp(-field_N_by_zone[z])`
- [x] 1.2 Assert `abs(pk_total - four_zone_field(...)[2]).max() < 1e-9` in a sanity check (can be a comment + manual test, not a production guard)

## 2. Update `ShellParams` construction in `app/sensitivity.py`

- [x] 2.1 Pass all ogive geometry fields from `preset` into the `ShellParams(...)` constructor call: `ogive_outer_R`, `ogive_inner_R`, `ogive_len`, `ogive_tip_dia`, `cylinder_len`, `boattail_len`, `boattail_angle_deg`, `boattail_inner_dia`, `base_thickness`, `has_boattail`, `base_treatment`, `ogive_crh`

## 3. Add Model selector and Tier badge to sidebar

- [x] 3.1 Add `model_mode = st.radio("Model", ["Single-zone (legacy)", "Four-zone (new)"])` to the sidebar (above the shell/explosive expander)
- [x] 3.2 Show `st.caption(tier_label)` immediately below the shell preset selectbox when `model_mode == "Four-zone (new)"`, where `tier_label` is "Tier-1 · arc geometry" if `preset.ogive_outer_R is not None` else "Tier-2 · CRH fallback"

## 4. Add four-zone cached compute function

- [x] 4.1 Add imports: `from arty.zones import compute_shell_zones, _four_zone_field_split` (and `four_zone_field` if used separately)
- [x] 4.2 Add `@st.cache_data` function `_compute_zones(shell_name, mass_total, mass_filler, caliber_mm, wall_t_mm, gamma, sigma_f, rho_steel, C_D, rho_air, h_b, angle_of_fall, spray_half_angle, posture, max_radius)` that builds `ShellParams` from `SHELLS[shell_name]` plus the scalar editables, calls `compute_shell_zones`, then `_four_zone_field_split`, and returns a dict with keys: `X`, `Y`, `pk_total`, `pk_by_zone`, `zones`
- [x] 4.3 Rename the existing `_compute` function to `_compute_legacy` for clarity

## 5. Update headline metrics

- [x] 5.1 Branch on `model_mode`: in Four-zone mode, derive V₀, N₀, μ from `result_zones["zones"].cylinder`; compute R₅₀ from the cross-range slice of `result_zones["pk_total"]`; label V₀/N₀/μ with delta text "(cyl zone)"
- [x] 5.2 In Single-zone mode, keep existing metric derivation from `FragField3dResult` with no delta text

## 6. Update 2D heatmap section

- [x] 6.1 In Single-zone mode: render the existing single full-width heatmap unchanged
- [x] 6.2 In Four-zone mode: render two side-by-side heatmaps — legacy `field_pk` (left) and `result_zones["pk_total"]` (right) — both using `RdYlGn_r` scale, zmin=0, zmax=1, height≥400 px; add titles "Single-zone" and "Four-zone"
- [x] 6.3 In Four-zone mode: render a full-width signed difference heatmap (`pk_4z − pk_1z`) with a diverging colorscale (e.g. `RdBu`), midpoint 0, colorbar labelled "ΔP(kill)", height≥400 px

## 7. Add Zone Breakdown section (Four-zone mode only)

- [x] 7.1 Below the heatmaps, add a `st.divider()` and `st.subheader("Zone Breakdown")` gated on `model_mode == "Four-zone (new)"`
- [x] 7.2 Create the **Zone Properties grouped bar chart**: `go.Figure` with three `go.Bar` traces (V₀, spray angle on primary y-axis; N₀ on secondary y-axis), x = `["ogive","cylinder","boattail","base"]`, values from `result_zones["zones"]`; use `barmode="group"`
- [x] 7.3 Create the **Per-zone P(kill) vs cross-range line chart**: extract the column of `pk_by_zone[z]` nearest x=0 for each zone and the total pk_total cross-range slice; plot one `go.Scatter` line per zone plus a "total" line; x-axis = cross-range [m] from 0 to `max_radius`
- [x] 7.4 Render both charts side-by-side in `st.columns(2)`
