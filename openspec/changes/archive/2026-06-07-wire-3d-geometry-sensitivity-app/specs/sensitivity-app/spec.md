## ADDED Requirements

### Requirement: Model selector radio controls active compute path

The app SHALL display a `Model` radio button in the sidebar with two options: **Single-zone (legacy)** and **Four-zone (new)**. Selecting Single-zone SHALL use `compute_frag_field_3d` exactly as before. Selecting Four-zone SHALL use `compute_shell_zones` + `four_zone_field`.

#### Scenario: Single-zone mode preserves original layout

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** the app displays the same three-figure layout as before (Mott CDF, KE chart, single 2D heatmap)

#### Scenario: Four-zone mode activates comparison layout

- **WHEN** the user selects "Four-zone (new)"
- **THEN** the heatmap section shows two side-by-side heatmaps (legacy left, four-zone right) and a full-width difference map below

### Requirement: Shell tier badge is shown when Four-zone is active

When the Four-zone model is selected, the app SHALL display a read-only tier badge as `st.caption` immediately below the shell preset selectbox. The badge SHALL read "Tier-1 · arc geometry" when the selected preset carries full ogive arc fields (`ogive_outer_R` is not None), and "Tier-2 · CRH fallback" otherwise.

#### Scenario: Tier-1 shell shows arc geometry badge

- **WHEN** the user selects "105mm M1 HE" or "155mm M107 HE" with Four-zone model active
- **THEN** the sidebar shows "Tier-1 · arc geometry" below the preset selectbox

#### Scenario: Tier-2 shell shows CRH fallback badge

- **WHEN** the user selects "75mm M48 HE" with Four-zone model active
- **THEN** the sidebar shows "Tier-2 · CRH fallback" below the preset selectbox

#### Scenario: Tier badge is absent in Single-zone mode

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** no tier badge is shown

## MODIFIED Requirements

### Requirement: All figures update on any parameter change

The app SHALL display at minimum three figures: **Mott cumulative distribution**, **Fragment KE vs Distance from Burst**, and a 2D fragmentation field. All figures SHALL recompute when any control changes. The P(kill) vs Cross-Range Distance chart is removed.

In **Single-zone mode** the 2D field section shows a single heatmap spanning the full page width (≥500 px tall), identical to the original layout.

In **Four-zone mode** the 2D field section shows:

1. Two side-by-side heatmaps (legacy single-zone left, four-zone right), each ≥400 px tall.
1. A full-width signed difference heatmap (P_k_four_zone − P_k_single_zone) with a diverging colorscale centred at zero, ≥400 px tall.

Ogive geometry fields from the selected shell preset SHALL be forwarded to `ShellParams`; users cannot override them via sliders.

The **Fragment KE vs Distance from Burst** chart uses the cylinder-zone V₀ in Four-zone mode, and the Gurney V₀ in Single-zone mode.

#### Scenario: Layout is two small charts above heatmap(s)

- **WHEN** the app loads with any model selected
- **THEN** Mott distribution and Fragment KE vs Distance from Burst appear side-by-side in the top row, and the heatmap section appears below them

#### Scenario: Four-zone diff map is centred at zero

- **WHEN** the user selects "Four-zone (new)" with default parameters
- **THEN** the difference heatmap uses a diverging colorscale with midpoint 0 and the colorbar label reads "ΔP(kill)"

#### Scenario: 2D field shows asymmetric footprint at non-zero AoF

- **WHEN** `angle_of_fall` is set to 45° and `h_b` to 5 m
- **THEN** both heatmaps (in Four-zone mode) are visibly asymmetric

### Requirement: R₅₀ is displayed as a headline metric

The app SHALL show four `st.metric` elements above the figures: **R₅₀ (cross-range)**, **V₀**, **N₀ (total frags)**, and **μ (half-mass)**. In Four-zone mode V₀, N₀, and μ SHALL be derived from the **cylinder zone** of `ShellZones` and SHALL include a "(cyl zone)" subtitle. In Single-zone mode the values come from `FragField3dResult` as before with no subtitle. All metrics SHALL update live with slider changes.

#### Scenario: Four-zone mode shows cylinder-zone subtitle

- **WHEN** the user selects "Four-zone (new)"
- **THEN** V₀, N₀, and μ metrics each display "(cyl zone)" as their delta/subtitle text

#### Scenario: Single-zone mode shows no zone subtitle

- **WHEN** the user selects "Single-zone (legacy)"
- **THEN** V₀, N₀, and μ metrics show no subtitle

### Requirement: Expensive recomputation is cached

Each compute path SHALL be wrapped in its own `@st.cache_data` function. The legacy cache is keyed on the scalar `ShellParams` inputs and `BurstParams`. The four-zone cache is keyed on the shell preset **name** (string) and the user-editable scalar parameters; ogive geometry fields are taken from `SHELLS[shell_name]` inside the cached function. Re-renders that do not change parameter values SHALL NOT call the physics functions.

#### Scenario: Switching model mode does not recompute the same model

- **WHEN** the user switches from Four-zone to Single-zone and back without changing sliders
- **THEN** neither `compute_frag_field_3d` nor `compute_shell_zones` is called again
