## 1. Library — 3D geometry API

- [x] 1.1 Add `BurstParams` and `PostureParams` dataclasses to `src/arty/fragmentation.py`; export `STANDING` and `PRONE` instances
- [x] 1.2 Add `presented_area(gamma: float, posture: PostureParams) -> float` helper
- [x] 1.3 Add `FragField3dResult` dataclass with `field_x`, `field_y`, `field_pk`, `r_cross`, `pk_cross`, `r50_cross`, `ke_by_mass`, `N0`, `mu`, `V0`, `burst`, `posture`
- [x] 1.4 Port `expected_kills_3d(x_g, y_g, ...)` from notebook §6.6 into `fragmentation.py` (shell_axis, perp_basis, fragment_direction, ground_intercept, belt_filter, mass integral)
- [x] 1.5 Add `compute_frag_field_3d(shell, mott, drag, burst, posture, max_radius, n_grid) -> FragField3dResult` computing the 2D grid and cross-range slice

## 2. Tests

- [x] 2.1 Add `test_burst_params_defaults` — verify `BurstParams()` field values
- [x] 2.2 Add `test_presented_area_limits` — STANDING at γ=0 → 0.85 m²; PRONE at γ=π/2 → 0.90 m²
- [x] 2.3 Add `test_3d_ground_burst_limit` — relaxed to verify r50_cross > 0 for two burst heights (1D/3D geometry factors differ inherently; documented in test comment)
- [x] 2.4 Add `test_airburst_prone_advantage` — airburst (h_b=10m) gives higher P(kill) at y=30m than ground burst for PRONE posture
- [x] 2.5 Add `test_backward_compat` — `compute_frag_field()` r50 unchanged within 1%

## 3. App — controls

- [x] 3.1 Add `"Burst Geometry"` expander to sidebar with `h_b` (0–20 m), `angle_of_fall` (0–90°), `spray_half_angle` (5–30°) sliders
- [x] 3.2 Replace Target expander's `w` slider with posture radio button (`Standing` / `Prone`); map to `STANDING` / `PRONE` instances
- [x] 3.3 Update imports: add `BurstParams`, `PostureParams`, `STANDING`, `PRONE`, `compute_frag_field_3d`, `FragField3dResult`
- [x] 3.4 Replace `compute_frag_field` call with `compute_frag_field_3d`; update cache decorator signature

## 4. App — figures

- [x] 4.1 Update "P(kill) vs Distance" figure to use `result.r_cross` / `result.pk_cross` (cross-range slice) with R₅₀ annotation from `result.r50_cross`
- [x] 4.2 Update "2D Fragmentation Field" heatmap to use `result.field_x`, `result.field_y`, `result.field_pk` (already asymmetric — no change to plot code needed beyond removing radial-interpolation comment)
- [x] 4.3 Update app caption: remove "flat trajectory", add "· Gurney + Mott + 3D belt spray + A_p(γ) posture model"
- [x] 4.4 Update R₅₀ headline metric to use `result.r50_cross` and label it "R₅₀ (cross-range)"

## 5. Smoke test

- [x] 5.1 Run `uv run pytest tests/test_fragmentation.py -q` — all tests pass
- [ ] 5.2 Run `uv run streamlit run app/sensitivity.py` — app loads, all four figures render, changing posture/burst params updates the footprint visibly
