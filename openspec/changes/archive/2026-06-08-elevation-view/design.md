## Context

Both fragmentation models compute fragment geometry in the vertical plane but have no diagram showing it. The single-zone model fires all fragments horizontally (theta=0°) regardless of AoF — an obvious limitation that becomes invisible without a diagram. The four-zone model assigns each zone a distinct spray elevation angle resolved against AoF; the two limiting azimuths in the x-z plane are phi=+90° and phi=-90° (vgy=0), bounding the fragment envelope in cross-section.

Current state:

- `src/arty/zones.py`: `fragment_ground_impact(zone, aof_deg, h_b, phi_deg)` computes x-z velocity components for any zone, AoF, and azimuth.
- `src/arty/plots.py`: `fig_cross_section` is an older diagram (static h_b=0, no AoF parameter, no zone data). It stays in the notebook's limitations narrative; the new functions are additive.
- `app/sensitivity.py`: Zone Breakdown section shows Zone Properties and Per-zone P(kill) charts (four-zone mode only). Single-zone mode has no zone breakdown section.
- `experiment/fragmentation-field/fragmentation-field.qmd`: Uses `fig_cross_section` for the single-zone limitations discussion. `_four-zone-3d.qmd` has no cross-section.

## Goals / Non-Goals

**Goals:**

- Add `fig_single_zone_elevation(aof_deg, h_b, r_person)` to `src/arty/plots.py`: horizontal spray ray (theta=0° always), AoF arrow, burst point, ground, person silhouette — makes the AoF-blind limitation visible for the old model.
- Add `fig_zone_elevation(zones, aof_deg, h_b, r_person)` to `src/arty/plots.py`: per-zone phi=+-90° rays (color-coded), AoF arrow, burst, ground, person silhouette.
- Show the appropriate elevation chart in `app/sensitivity.py` for both model modes: single-zone chart in the single-zone section, four-zone chart in the Zone Breakdown section.
- Add both figures to the fragmentation-field notebook in their respective sections.

**Non-Goals:**

- No physics changes to `zones.py` or `fragmentation.py`.
- Not replacing `fig_cross_section` — it stays in the limitations narrative.
- Not adding within-zone spread cones (+-delta_deg) — that is limitation §12 item 4.
- Not animating AoF changes in the app (static snapshot at current slider values).

## Decisions

### D1 — Two rays per zone, not a spread cone

Only phi=+90° and phi=-90° are drawn per zone (vgy=0 exactly). This keeps the diagram clean and unambiguous. The spray-half-angle belt (+-delta_deg) is noted in a legend caption but not rendered as a filled cone; adding a cone is straightforward later but adds visual noise for four zones at once.

Alternative: draw phi=0,+-90°,180° (four rays). Rejected — phi=0 and phi=180° give vgy=sin(theta_z)\*cos(0 or pi)=+-sin(theta_z), leaving the x-z plane, and their x-projections collapse to vgx = cos(aof)\*cos(theta_z) — not the widest spread.

### D2 — Single-zone elevation uses the same layout as four-zone

`fig_single_zone_elevation` draws a single "cylinder" ray at theta=0° (phi=+90°, phi=-90°), identical in structure to the four-zone variant but without zone data. This means the two diagrams are visually comparable side-by-side in the notebook, making the difference between models clear at a glance. The AoF arrow is drawn in both, showing that the old model ignores it for fragment direction.

### D3 — matplotlib for `plots.py`, Plotly inline for `app/sensitivity.py`

`plots.py` stays matplotlib to match every other figure in the module and in the notebook renderer. The Streamlit app already uses Plotly for all charts, so a helper `_plotly_elevation(zones_or_none, aof_deg, h_b, x_person)` is created inline in `sensitivity.py`. `zones_or_none=None` triggers the single-zone variant; a `ShellZones` object triggers the four-zone variant.

### D4 — Upward rays drawn as dashed arrows of fixed length

When vgz >= 0 for a ray (fragment goes upward, cannot hit the ground), the ray is drawn as a dashed line of length 30 m along its unit-vector direction, annotated "upward (excluded)". This makes the ground-impact exclusion visually explicit.

### D5 — Person silhouette position

In `plots.py` the person position is an `r_person` parameter (default 30 m). In the app the downrange slider (`x_slice`) drives the position. Guard: if abs(x_person) < 2 m, the silhouette is suppressed and a "(burst proximity)" note shown instead.

### D6 — Notebook placement

`fig_single_zone_elevation` goes into the single-zone section of `fragmentation-field.qmd` (near the existing `fig_cross_section` call, as a follow-on parameterised version). `fig_zone_elevation` goes into `_four-zone-3d.qmd` as a new subsection after the zone footprint plot and before the AoF sweep.

## Risks / Trade-offs

- [Four zones x two rays = eight lines; diagram may be crowded] -> Zones use the established C0/C1/C2/C3 palette; phi=+90° solid, phi=-90° dashed (same color). Legend compact.
- [At AoF=0° with h_b=0 all rays start at (0,0)] -> y-axis lower bound clamped to min(-2, -0.1\*h_b) so the diagram is still readable.
- [Single-zone elevation may look trivial] -> That is the point: the diagram makes the triviality explicit and sets up the four-zone comparison.

## Open Questions

- None blocking implementation. Post-implementation: consider whether within-zone spread cones (+-delta_deg) add clarity or clutter.
