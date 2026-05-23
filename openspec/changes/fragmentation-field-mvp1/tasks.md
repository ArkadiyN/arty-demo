## 1. Project Setup

- [x] 1.1 Add `streamlit` and `plotly` to `pyproject.toml` dependencies
- [x] 1.2 Create `src/arty/__init__.py` (empty, marks package)
- [x] 1.3 Verify `src/arty/` is importable from project root (check `pyproject.toml` package config)

## 2. Physics Module

- [x] 2.1 Create `src/arty/fragmentation.py` with `ShellParams`, `MottParams`, `DragParams`, `TargetParams` dataclasses (typed fields, defaults from notebook)
- [x] 2.2 Implement `FragFieldResult` dataclass with all output fields (`r`, `p_kill`, `ke_by_mass`, `field_x`, `field_y`, `field_pk`, `r50`, `N0`, `mu`)
- [x] 2.3 Extract and implement `gurney_velocity(shell)` from notebook
- [x] 2.4 Extract and implement `mott_params(shell, mott, V0)` returning `(mu, N0)` from notebook
- [x] 2.5 Extract and implement `retardation_coeff(m, drag)` from notebook
- [x] 2.6 Extract and implement `pk_given_hit(E)` with ES-310 anchors from notebook
- [x] 2.7 Extract and implement `expected_kills(r, N0, mu, V0, drag, target)` from notebook
- [x] 2.8 Implement `compute_frag_field(shell, mott, drag, target, max_radius, n_r)` composing all sub-functions and returning `FragFieldResult`

## 3. Shell Registry

- [x] 3.1 Create `src/arty/shells.py` with `SHELLS: dict[str, ShellParams]`
- [x] 3.2 Add `"105mm M1 HE"` entry with all geometry, mass, and explosive parameters matching notebook defaults

## 4. Unit Tests

- [x] 4.1 Create `tests/test_fragmentation.py`
- [x] 4.2 Test `ShellParams` default values match notebook constants
- [x] 4.3 Test `gurney_velocity` result is within 900–1400 m/s for M/C = 4–8
- [x] 4.4 Test `mott_params` fragment count N(>0.5g) is within 3000–8000 for default shell
- [x] 4.5 Test `retardation_coeff` is strictly decreasing with mass
- [x] 4.6 Test `pk_given_hit` returns ~[0.10, 0.50, 0.90] at ES-310 anchor energies
- [x] 4.7 Test `compute_frag_field` returns `p_kill` that is monotonically non-increasing
- [x] 4.8 Test `compute_frag_field` returns `r50` between 50 and 200 m for default params
- [x] 4.9 Test `SHELLS["105mm M1 HE"]` exists and has correct `gurney_const`, `mass_shell`, `mass_charge`

## 5. Streamlit Sensitivity App

- [x] 5.1 Create `app/sensitivity.py` with page title and layout skeleton
- [x] 5.2 Add shell preset selectbox populated from `SHELLS.keys()`
- [x] 5.3 Add **Shell & Explosive** collapsible group: sliders for `gurney_const`, `mass_shell`, `mass_charge`, `r_inner`, `wall_t` — ranges covering ±20% of defaults
- [x] 5.4 Add **Mott Fragmentation** collapsible group: sliders for `gamma` (53–80), `sigma_f` (600–1200 MPa), `rho_steel` (7600–8000 kg/m³)
- [x] 5.5 Add **Drag** collapsible group: sliders for `C_D` (0.4–0.9), `rho_air` (0.9–1.4 kg/m³)
- [x] 5.6 Add **Target** collapsible group: radio for standing/prone (sets `w` to 0.5/0.25 m) plus explicit `w` slider
- [x] 5.7 Wire all slider values into param struct construction and call `compute_frag_field`
- [x] 5.8 Display R₅₀ as `st.metric` headline above figures
- [x] 5.9 Implement Plotly Mott cumulative distribution figure (log-x, fragment count vs mass)
- [x] 5.10 Implement Plotly KE vs range figure (three representative masses: 0.5 g, 5 g, 50 g)
- [x] 5.11 Implement Plotly p_kill vs range figure with R₅₀ vertical line annotated
- [x] 5.12 Implement Plotly 2D fragmentation field figure (polar contour or scatter coloured by p_kill)
- [x] 5.13 Wrap `compute_frag_field` call in `@st.cache_data` keyed on all params
- [x] 5.14 Manually verify app launches (`streamlit run app/sensitivity.py`) and all figures update on slider change
