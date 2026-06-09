## 1. src/arty/plots.py — single-zone elevation function

- [x] 1.1 Fix `fig_single_zone_elevation(aof_deg, h_b, r_person=30, spray_half_angle_deg=15)` in `src/arty/plots.py`: replace horizontal rays with the two belt-edge rays at angles (90°+AoF)±δ from +x, add belt centre-line (equatorial direction), label δ; belt and shell arrow both rotate with aof_deg
- [x] 1.2 Verify spec scenario "Belt rotates with AoF": call with aof_deg=0, 45, 90 and assert belt bounding-ray endpoints differ across calls
- [x] 1.3 Verify spec scenario "Shell arrival arrow and belt are consistent": assert belt centre-line is perpendicular to shell axis direction for aof_deg=0, 30, 90

## 2. src/arty/plots.py — four-zone elevation function

- [x] 2.1 Add `fig_zone_elevation(zones, aof_deg, h_b, r_person=30)` to `src/arty/plots.py`: for each zone draw phi=+90° (solid) and phi=-90° (dashed) rays using `fragment_ground_impact` velocity components; clip to ground if vgz < 0, else draw 30 m dashed "upward (excluded)" arrow; color-code by ogive/cylinder/boattail/base (C0/C1/C2/C3)
- [x] 2.2 Verify spec scenario "Cylinder zone ray is horizontal at AoF=0°": for M1 shell at aof_deg=0, assert cylinder zone rays lie on the horizontal line z=h_b
- [x] 2.3 Verify spec scenario "Upward rays are drawn dashed with annotation": at AoF=90° assert base zone phi=+90° ray is drawn as dashed upward arrow (vgz>=0 guard triggered)
- [x] 2.4 Verify spec scenario "Zone colors match the Zone Breakdown palette": inspect line colors in the returned figure

## 3. Fragmentation-field notebook — single-zone section

- [x] 3.1 Update cell in `experiment/fragmentation-field/_field-plots.qmd` (Figure 4b) to pass `spray_half_angle_deg` matching the notebook's burst params; add prose note explaining the belt geometry
- [x] 3.2 Render the notebook and confirm the new cell renders without error (spec scenario "Single-zone elevation renders at default AoF=0° and h_b=2 m")

## 4. Fragmentation-field notebook — four-zone section

- [x] 4.1 Add a new subsection "Burst geometry cross-section" in `experiment/fragmentation-field/_four-zone-3d.qmd` after the zone footprint cell, calling `plots.fig_zone_elevation(m1_zones, aof_deg=30, h_b=2.0, r_person=30)`
- [x] 4.2 Render the notebook and confirm the new cell renders without error (spec scenario "Four-zone elevation renders at AoF=30° and h_b=2 m")

## 5. app/sensitivity.py — Plotly elevation panel

- [x] 5.1 Fix `_plotly_elevation` single-zone branch: replace horizontal rays with belt-edge rays at (90°+AoF)±δ from +x; add `spray_half_angle_deg` param; pass spray_half_angle from sidebar at call site
- [x] 5.2 In Single-zone mode, render corrected `_plotly_elevation(None, angle_of_fall, h_b, r50, spray_half_angle)` as a full-width chart below the existing single-zone heatmap
- [x] 5.3 In Four-zone mode, render `_plotly_elevation(zones, angle_of_fall, h_b, x_slice)` as a full-width chart at the bottom of the Zone Breakdown section
- [x] 5.4 Verify spec scenario "Elevation chart updates when AoF slider changes": confirm the chart re-renders when angle_of_fall changes (automatic via Streamlit reactivity — verify no caching breaks the update)
- [x] 5.5 Verify spec scenario "Silhouette suppressed near burst": confirm that x_slice=0 shows "(burst proximity)" note and no silhouette rectangle
