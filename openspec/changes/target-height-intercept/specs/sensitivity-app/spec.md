## ADDED Requirements

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
