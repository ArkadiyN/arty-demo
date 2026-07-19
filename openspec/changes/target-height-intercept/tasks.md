## 1. Derivation

- [x] 1.1 Derive the vertical-column flux integral `P_k = 1 - exp(-w_perp·∫₀ʰ ρ_L dz)` and
  confirm it reduces to the existing `ρ_L(z=0)·A_ref` transform in the constant-density
  limit (`experiment/fragmentation-field/updates/target-height-intercept/derivation.md` §4)
- [x] 1.2 Derive the analytic belt-edge crossing (per-zone `K = cosθ^z ± sinδ` quadratic) and
  settle on composite-midpoint quadrature after ruling out uniform trapezoid (non-monotone
  error) and endpoint-inclusive piecewise trapezoid (floating-point boundary bias)
  (derivation §5, §5.1-§5.4)
- [x] 1.3 Work dimensional/limit/posture/straight-line-consistency checks, including the
  AoF=90° false-safe-ring unit check (derivation §6.1-§6.5)
- [x] 1.4 Record assumptions A1-A4 and the numerically-stable quadratic root note
  (derivation §7)

## 2. src/arty implementation

- [x] 2.1 Add `_stable_quadratic_roots`, `belt_column_breakpoints`, and
  `integrate_column_density` to `src/arty/fragmentation.py` (composite-midpoint
  quadrature over analytic breakpoints, `n_seg=9` default) — implements spec
  "Ground P(kill) fields integrate lethal density over the target's vertical column"
- [x] 2.2 Widen `slant_range_grid`'s `s_max` to `max(|z_min-h_b|, |z_max-h_b|)` so
  drag/Mott tables cover the full column-integral span
- [x] 2.3 Rewrite `pkill_field_3d` to the column-integral transform with a `posture`
  parameter (`STANDING` default), dropping the old `z`/`A_ref` sample-point parameters
- [x] 2.4 Rewrite `four_zone_pkill_field` (`src/arty/zones.py`) to the same column-integral
  transform, generalizing the belt breakpoint to the per-zone `K` form; add
  `_active_zone_cos_theta` helper
- [x] 2.5 Add `four_zone_pkill_line` (Family-B line evaluator, distinct from the Family-A
  `four_zone_line_split`) for app cross-section consumers
- [x] 2.6 Leave `pkill_volume_3d` / `four_zone_pkill_volume` computationally unchanged;
  correct their docstrings to describe the point-in-space diagnostic role — implements
  spec "The 3D P(kill) volume view is unchanged and remains a point-in-space diagnostic"

## 3. Tests

- [x] 3.1 Rework the two volume `z=0 == field` invariant tests (intentionally broken by this
  change) into bit-exact `z=0`-layer-equals-frozen-A_ref-point-transform assertions
  (`tests/test_pkill_field.py::test_single_zone_pkill_volume_z0_is_point_transform`,
  `::test_four_zone_pkill_volume_z0_is_point_transform`) — verifies the volume-unchanged
  spec scenarios
- [x] 3.2 Add `test_single_zone_pkill_field_posture_and_false_safe_ring` and
  `test_four_zone_pkill_field_posture_and_false_safe_ring`, each asserting
  `P_k_stand.max() >= P_k_prone.max()` and `P_k_stand[ring].max() > 0.5` for
  `2.0 < r < 7.0` at AoF=90° — verifies the posture-coupling and false-safe-ring spec
  scenarios for both the single-zone and four-zone paths (closes the test-parity gap
  the four-zone path initially lacked)
- [x] 3.3 Fix bounds-test call signatures for the new `posture`/column-integral parameters
  (`test_single_zone_pkill_field_bounds`, `test_four_zone_pkill_field_bounds`)
- [x] 3.4 Confirm full suite passes (`uv run pytest tests/test_pkill_field.py` and the full
  `tests/` suite)

## 4. Notebook presentation

- [x] 4.1 Rewrite `experiment/fragmentation-field/_pkill-field.qmd` to call the new
  posture-based `pkill_field_3d`/`four_zone_pkill_field` signatures, headlining the
  false-safe-zone fix at AoF=90°/h_b=2m with a STANDING-vs-PRONE contrast
- [x] 4.2 Add `fig_pkill_field` presentation-only plotting helper to `src/arty/plots.py`
- [x] 4.3 Update `experiment/fragmentation-field/_limitations.qmd` item 12 from an open
  limitation to fixed, pointing at the derivation
- [x] 4.4 Add the 0.5.1 row to `experiment/fragmentation-field/_change-log.qmd`
- [x] 4.5 Fix the PRONE ring-fill grid-resolution aliasing artifact (report on a
  resolution-confirmed dense near-field grid and a grid-stable onset radius instead of
  a single coarse-grid percentage) and the resulting overbroad "entire inner ring"
  wording in `_limitations.qmd`
- [x] 4.6 Fix the self-contradicting inline dead-zone-radius formula in `_pkill-field.qmd`
  (`(h_b-h)/tanδ`, not `h_b/tanδ`)
- [x] 4.7 Confirm `quarto render` completes cleanly with no tracebacks

## 5. App wiring (reopened)

- [x] 5.1 Add `pkill_field_3d` / `four_zone_pkill_field` imports and
  `@st.cache_data`-wrapped compute functions (`_compute_pkill_field_legacy`,
  `_compute_pkill_field_zones`) to `app/sensitivity.py`, mirroring the existing
  `_compute_volume_legacy`/`_compute_volume_zones` pattern
- [x] 5.2 Add a new "Ground Kill Probability" `st.expander` next to the existing "3D Kill
  Probability" expander: independent view-radius slider, grid-resolution `select_slider`,
  single-zone/four-zone branching, posture read from the existing sidebar toggle — implements
  `sensitivity-app`'s new requirement
- [x] 5.3 Render as a new Plotly `go.Heatmap` (matching the existing 2D-heatmap style: `YlOrRd`,
  `_r50_contour` overlay, burst-point marker) — no diff/comparison against the Family-A
  heatmaps
- [x] 5.4 Start the Streamlit dev server and exercise the new section live in a browser: confirm
  it renders for both model modes, and confirm toggling Posture at AoF=90°/h_b=2m visibly
  fills the close-in ring for Standing vs Prone (confirmed: Standing shows full close-in
  lethality with no false-safe hole; Prone retains a small residual dead-zone ring right at
  the burst, correctly, since its very low profile still misses the overhead belt at extreme
  close range — matches the notebook's prone dead-zone radius)
