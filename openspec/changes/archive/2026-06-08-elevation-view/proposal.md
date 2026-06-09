## Why

Both the single-zone and four-zone models resolve fragment geometry in 3D against angle of fall (AoF) and burst height, but neither model has a diagram showing what this looks like in the vertical plane. For the old model the limitation is invisible: a user cannot see that all fragments fly horizontally regardless of AoF, which is the primary reason the single-zone model breaks down at steep angles. For the new four-zone model, users encounter artefacts like the "safe zone" near the burst at steep AoF (limitation §12 in `_limitations.qmd`) without a visual that explains the cause — horizontal cylinder fragments have vgz=0 and are excluded from the ground-impact test.

## What Changes

- Add `fig_single_zone_elevation(aof_deg, h_b, r_person)` to `src/arty/plots.py`: vertical cross-section for the single-zone model showing the burst at (0, h_b), the shell arrival arrow at AoF, the horizontal spray belt (fragment ray always at θ=0° regardless of AoF), and a person silhouette. Replaces the role of `fig_cross_section` for parameterised geometry; `fig_cross_section` is retained for the v0.1/v0.2 limitations narrative.
- Add `fig_zone_elevation(zones, aof_deg, h_b, r_person)` to `src/arty/plots.py`: same layout for the four-zone model, drawing per-zone spray rays at phi=±90° (the two azimuths with vgy=0), color-coded by zone.
- Update the fragmentation-field notebook: add `fig_single_zone_elevation` in the single-zone model section and `fig_zone_elevation` in the four-zone section (`_four-zone-3d.qmd` partial).
- Add a Plotly elevation panel to `app/sensitivity.py` that shows the appropriate cross-section for the active model mode (single-zone or four-zone), updated by the existing AoF, h_b, and downrange sliders.

## Capabilities

### New Capabilities

- `elevation-view-chart`: Vertical cross-section (x-z plane) diagram for both model modes — burst point, shell arrival direction, fragment spray rays, ground fill, and person silhouette. Two variants: single-zone (one horizontal ray, illustrates the AoF-blind limitation) and four-zone (per-zone colored rays, illustrates the vgz=0 exclusion artefact). Rendered as matplotlib in `src/arty/plots.py` (for the notebook) and as a Plotly figure in `app/sensitivity.py`.

### Modified Capabilities

- `zone-breakdown-charts`: The Zone Breakdown section (four-zone mode) gains the elevation cross-section chart. The single-zone section gains its own elevation chart outside the Zone Breakdown block.

## Impact

- `src/arty/plots.py` — two new functions: `fig_single_zone_elevation`, `fig_zone_elevation`
- `experiment/fragmentation-field/_four-zone-3d.qmd` — new subsection calling `fig_zone_elevation`
- `experiment/fragmentation-field/fragmentation-field.qmd` (or single-zone partial) — new cell calling `fig_single_zone_elevation`
- `app/sensitivity.py` — elevation panel shown in both model modes
- No changes to physics (`src/arty/zones.py`, `src/arty/fragmentation.py`), no new parameters, no breaking API changes
