## 1. Library

- [x] 1.1 Add `r_ke: np.ndarray` field to `FragField3dResult` dataclass
- [x] 1.2 In `compute_frag_field_3d`, replace the cross-range ke_by_mass computation with a radial sweep: `r_ke = np.linspace(0, max_radius, n_grid)` and `ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (V0 * np.exp(-lam_j * r_ke)) ** 2`
- [x] 1.3 Pass `r_ke` into the returned `FragField3dResult`

## 2. App

- [x] 2.1 Update Figure 2 x-axis to use `result.r_ke` instead of the cross-range `x_vals`
- [x] 2.2 Update Figure 2 title to "Fragment KE vs Distance from Burst" and x-axis label to "Slant range s [m]"
- [x] 2.3 Update threshold annotation x-anchors to use `result.r_ke[-1]`

## 3. Tests

- [x] 3.1 Add `test_ke_by_mass_radial` — verify `result.r_ke[0] == 0`, `result.r_ke[-1] == max_radius`, and `ke_by_mass[0.5][0] ≈ 0.5 * 0.5e-3 * V0²`

## 4. Smoke test

- [x] 4.1 Run `uv run pytest tests/test_fragmentation.py -q` — all tests pass
- [ ] 4.2 Run `uv run streamlit run app/sensitivity.py` — KE chart shows s from 0 to max_radius, curves start at ½mV₀² at left edge
