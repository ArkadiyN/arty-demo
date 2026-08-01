## MODIFIED Requirements

### Requirement: Parameter sliders are grouped by model section

The app SHALL display controls in five collapsible groups: **Shell & Explosive**, **Mott Fragmentation**, **Drag**, **Burst Geometry** (new), **Target**. The **Mott Fragmentation** group SHALL contain, in addition to the existing `gamma` and `sigma_f` sliders, a fragment aspect-ratio slider `A` (1.50–1.71, default 1.60) and a mean-breadth-factor slider `κ_x` (1.00–2.00, default 1.50), driving the `ShellParams.aspect_ratio` and `ShellParams.breadth_factor` fields used by `mott_params`. The **Drag** group SHALL contain sliders for `C_D` (0.40–0.90, default 0.65) and `C_shape` (0.50–3.00, default 0.90) — both are `DragParams` assumptions and enter the retardation coefficient only as the product `C_D·C_shape`. The **Burst Geometry** group SHALL contain sliders for `h_b` (0–20 m, default 2.0), `angle_of_fall` (0–90°, default 30°), `spray_half_angle` (5–30°, default 15°). The **Target** group SHALL replace the raw presented-width slider with a radio button selecting `Standing` or `Prone` posture.

#### Scenario: Drag group exposes both drag assumptions

- **WHEN** the Drag group is expanded
- **THEN** both `C_D` and `C_shape` sliders are shown, letting the user probe
    how much of the retardation gap a higher effective drag could close

#### Scenario: Slider ranges cover the uncertainty bands from the notebook

- **WHEN** the Mott group is expanded
- **THEN** `gamma` slider spans 53–80 and `sigma_f` spans 600–1200 MPa

#### Scenario: Mott group exposes both fragment-shape factors

- **WHEN** the Mott group is expanded
- **THEN** an `A` slider (1.50–1.71, default 1.60) and a `κ_x` slider (1.00–2.00, default 1.50) are shown, in addition to the existing `gamma` and `sigma_f` sliders

#### Scenario: Fragment-shape sliders change fragment mass output live

- **WHEN** the `A` slider is moved above its default of 1.60 with all other sliders unchanged
- **THEN** the Mott cumulative distribution and headline `R₅₀` metric recompute to reflect the resulting increase in mean fragment mass `μ`

#### Scenario: Slider ranges cover operationally relevant burst parameters

- **WHEN** the Burst Geometry group is expanded
- **THEN** h_b slider spans 0–20 m and angle_of_fall spans 0–90°

#### Scenario: Posture radio replaces width slider

- **WHEN** the Target group is expanded
- **THEN** a radio button with options "Standing" and "Prone" is shown; no raw width slider
