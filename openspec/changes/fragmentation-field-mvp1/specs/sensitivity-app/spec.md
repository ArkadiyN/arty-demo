## ADDED Requirements

### Requirement: Shell preset dropdown controls base parameters

The app SHALL display a selectbox populated from `SHELLS.keys()`. Selecting a preset SHALL populate all parameter sliders with that shell's values.

#### Scenario: Selecting 105mm M1 HE loads correct defaults

- **WHEN** user selects "105mm M1 HE" from the dropdown
- **THEN** all sliders reset to the notebook-validated defaults for that shell

______________________________________________________________________

### Requirement: Parameter sliders are grouped by model section

The app SHALL display controls in four collapsible groups matching the model structure: **Shell & Explosive** (filler type selectbox from `FILLERS`, `mass_total`, `mass_filler`, `caliber`, `wall_t`), **Mott Fragmentation** (`gamma`, `sigma_f`, `rho_steel`), **Drag** (`C_D`, `rho_air`), **Target** (`w`).

#### Scenario: Slider ranges cover the uncertainty bands from the notebook

- **WHEN** the Mott group is expanded
- **THEN** `gamma` slider spans 53–80 and `sigma_f` spans 600–1200 MPa

______________________________________________________________________

### Requirement: All four Plotly figures update on any parameter change

The app SHALL display four figures — Mott cumulative distribution, KE vs range (three representative masses), p_kill vs range with R₅₀ annotated, 2D fragmentation field — all recomputed when any slider or dropdown changes.

#### Scenario: R₅₀ annotation updates after sigma_f change

- **WHEN** user moves the `sigma_f` slider
- **THEN** the p_kill figure re-renders with a new R₅₀ value annotated on the curve

#### Scenario: 2D field reflects target width change

- **WHEN** user moves the presented width slider
- **THEN** the 2D field figure re-renders with a visibly smaller lethal radius

______________________________________________________________________

### Requirement: R₅₀ is displayed as a headline metric

The app SHALL show R₅₀ as a large `st.metric` element above the figures, updating live with slider changes.

#### Scenario: Metric updates on parameter change

- **WHEN** any slider value changes
- **THEN** the R₅₀ metric reflects the new computed value before the user scrolls to the figures

______________________________________________________________________

### Requirement: Expensive recomputation is cached

The 2D field computation SHALL be wrapped in `@st.cache_data` keyed on all parameter values so re-renders from unrelated UI state changes do not recompute it.

#### Scenario: Repeated identical params do not recompute

- **WHEN** the same parameter values are submitted twice
- **THEN** the 2D field result is returned from cache without calling `compute_frag_field` again
