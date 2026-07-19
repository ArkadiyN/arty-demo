## Purpose

Define the behaviour of the interactive Streamlit sensitivity explorer (`app/sensitivity.py`): parameter controls, model selection (single-zone legacy vs four-zone), 2D fragmentation field heatmaps and comparison diff map, headline metrics, and the zone breakdown charts.

## Requirements

### Requirement: Shell preset dropdown controls base parameters

The app SHALL display a selectbox populated from `SHELLS.keys()`. Selecting a preset SHALL populate all parameter sliders with that shell's values.

#### Scenario: Selecting 105mm M1 HE loads correct defaults

- **WHEN** user selects "105mm M1 HE" from the dropdown
- **THEN** all sliders reset to the notebook-validated defaults for that shell

______________________________________________________________________

### Requirement: Parameter sliders are grouped by model section

The app SHALL display controls in five collapsible groups: **Shell & Explosive**, **Mott Fragmentation**, **Drag**, **Burst Geometry** (new), **Target**. The **Burst Geometry** group SHALL contain sliders for `h_b` (0–20 m, default 2.0), `angle_of_fall` (0–90°, default 30°), `spray_half_angle` (5–30°, default 15°). The **Target** group SHALL replace the raw presented-width slider with a radio button selecting `Standing` or `Prone` posture.

#### Scenario: Slider ranges cover the uncertainty bands from the notebook

- **WHEN** the Mott group is expanded
- **THEN** `gamma` slider spans 53–80 and `sigma_f` spans 600–1200 MPa

#### Scenario: Slider ranges cover operationally relevant burst parameters

- **WHEN** the Burst Geometry group is expanded
- **THEN** h_b slider spans 0–20 m and angle_of_fall spans 0–90°

#### Scenario: Posture radio replaces width slider

- **WHEN** the Target group is expanded
- **THEN** a radio button with options "Standing" and "Prone" is shown; no raw width slider

______________________________________________________________________

### Requirement: All figures update on any parameter change

The app SHALL display three figures: **Mott cumulative distribution**, **Fragment KE vs Distance from Burst**, and **2D fragmentation field heatmap**. The heatmap SHALL span the full page width and be at least 500 px tall. All figures SHALL recompute when any control changes. The P(kill) vs Cross-Range Distance chart is removed.

The **Fragment KE vs Distance from Burst** chart SHALL use `result.r_ke` as its x-axis, representing slant range s [m] from 0 to `max_radius`.

#### Scenario: Layout is two small charts above one full-width heatmap

- **WHEN** the app loads with default parameters
- **THEN** Mott distribution and Fragment KE vs Distance from Burst appear side-by-side in the top row, and the 2D heatmap spans the full width below them

#### Scenario: 2D field shows asymmetric footprint at non-zero AoF

- **WHEN** `angle_of_fall` is set to 45° and `h_b` to 5 m
- **THEN** the heatmap is visibly asymmetric (offset along the downrange axis)

#### Scenario: KE chart x-axis runs from 0 to max_radius

- **WHEN** the Fragment KE vs Distance from Burst chart is rendered
- **THEN** the x-axis spans 0 to `max_radius` and is labelled "Slant range s [m]"

#### Scenario: All mass curves start at ½mV₀² at the left edge

- **WHEN** the Fragment KE vs Distance from Burst chart is rendered with default params
- **THEN** each of the three mass curves starts (at s=0) at its respective ½mV₀² value

______________________________________________________________________

### Requirement: R₅₀ is displayed as a headline metric

The app SHALL show R₅₀ as a large `st.metric` element above the figures, updating live with slider changes.

#### Scenario: Metric updates on parameter change

- **WHEN** any slider value changes
- **THEN** the R₅₀ metric reflects the new computed value before the user scrolls to the figures

______________________________________________________________________

### Requirement: App title and caption reflect 3D model

The app title SHALL be "Fragmentation Field Sensitivity" and the caption SHALL NOT contain "flat trajectory". It SHALL reference burst height and angle of fall.

#### Scenario: Title and caption are correct on load

- **WHEN** the app loads with any parameter values
- **THEN** the page title reads "Fragmentation Field Sensitivity" and the caption does not contain "flat trajectory"

______________________________________________________________________

### Requirement: Expensive recomputation is cached

The 3D field computation SHALL be wrapped in `@st.cache_data` keyed on all parameter values so re-renders from unrelated UI state changes do not recompute it.

#### Scenario: Repeated identical params do not recompute

- **WHEN** the same parameter values are submitted twice
- **THEN** the 2D field result is returned from cache without calling `compute_frag_field_3d` again

______________________________________________________________________

### Requirement: App exposes the Family-B ground P(kill) column-integral field

The app SHALL display the Family-B ground `P(kill)(x,y)` field (`pkill_field_3d` /
`four_zone_pkill_field`, the vertical-column-integral transform from
`pkill-ground-field`) in its own `st.expander`, placed next to the existing "3D Kill
Probability" expander. This view is a new Plotly `go.Heatmap` (matching the existing
2D-heatmap visual style: `YlOrRd` colorscale, `_r50_contour` white P=0.5 overlay, burst-
point marker) — not a reuse of the notebook's matplotlib `fig_pkill_field` helper, and
NOT a diff/comparison against the Family-A heatmaps (the two families answer different
physical questions, not the same quantity at different resolution). Posture is read from
the existing sidebar `posture` state; the view has its own independent view-radius slider
and grid-resolution `select_slider`, and branches between the single-zone and four-zone
compute paths the same way the existing 3D volume expander does.

#### Scenario: Ground P(kill) expander renders for both model modes

- **WHEN** the app loads and the user expands "Ground Kill Probability"
- **THEN** a Plotly heatmap of `P(kill)(x,y)` is shown, computed via `pkill_field_3d` in
  "Single-zone (legacy)" mode and `four_zone_pkill_field` in "Four-zone (new)" mode

#### Scenario: Posture toggle changes the ground field

- **WHEN** the sidebar Posture radio is switched between "Standing" and "Prone" with
  `angle_of_fall=90°`, `h_b=2.0`
- **THEN** the ground P(kill) heatmap's close-in ring (`2 m < r < 7 m`) shows a
  substantially higher kill probability for "Standing" than for "Prone"

#### Scenario: No Family-A comparison is rendered in this section

- **WHEN** the "Ground Kill Probability" expander is inspected
- **THEN** it contains no diff/comparison trace against the Family-A 2D heatmaps
