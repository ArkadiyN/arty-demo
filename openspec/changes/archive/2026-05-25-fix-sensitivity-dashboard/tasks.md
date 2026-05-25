## 1. Library — cross-range slice bug fix

- [x] 1.1 In `compute_frag_field_3d`, replace the `j0`-column extraction with a dedicated 1D sweep: call `_expected_kills_3d_point(0.0, float(y_g), ...)` for each `y_g` in `xy` and derive `pk_cross` from that array

## 2. App — layout restructure

- [x] 2.1 Remove Figure 3 (P(kill) vs Cross-Range Distance) and its `left2`/`right2` column block
- [x] 2.2 Promote Figure 4 (2D heatmap) to full-width (`st.plotly_chart` outside any column), increase height to 500 px, add `st.divider()` above it

## 3. Tests

- [x] 3.1 Add `test_cross_range_no_gap` — verify `pk_cross` at y≈0 is > 0.5 for `h_b=0, AoF=0°, n_grid=80` (even grid)

## 4. Smoke test

- [x] 4.1 Run `uv run pytest tests/test_fragmentation.py -q` — all tests pass
- [ ] 4.2 Run `uv run streamlit run app/sensitivity.py` — three charts render, heatmap is full-width, no gap visible at AoF=0°/h_b=0
