## Context

The Zone Breakdown section of `app/sensitivity.py` (four-zone mode) already
had a cross-range slice chart (`fig_pk`, fixed downrange x) and an elevation
(x-z plane) cross-section. Both read off a shared `n_grid x n_grid` square
mesh produced by `_four_zone_field_split` / `four_zone_field` in
`src/arty/zones.py` (default step `max_radius/_N_STEPS` ≈ 2.5 m, set by an
O(n_grid²) double loop — tightening it globally for an interactive app is
prohibitively expensive).

This change adds the downrange-axis counterpart of both charts, removes a
chart element that turned out not to carry independent information, and
fixes a sampling artifact uncovered while building the downrange slice: at
low burst height the true non-zero P(kill) footprint along a slice line can
be narrower than the 2.5 m grid step, so a row/column read off the grid can
read as all-zero even though the field is genuinely non-zero nearby.

## Goals / Non-Goals

**Goals:**

- Mirror the existing cross-range slice chart with a downrange slice chart.
- Mirror the existing elevation (x-z) cross-section with an across (y-z)
  cross-section, pairing each slice chart with the cross-section that shares
  its fixed axis.
- Fix the grid-resolution sampling artifact for both slice charts without
  paying O(n_grid²) cost for a globally finer grid.

**Non-Goals:**

- No change to the underlying physics (spray-belt acceptance test, presented
  area, drag attenuation, Mott integration) — this is a presentation and
  sampling-resolution change, not a new derived quantity.
- No change to `four_zone_field` / `_four_zone_field_split`'s existing public
  behavior; the 2D heatmaps are untouched.
- Does not address the pre-existing pattern (predating this change) of
  `_spray_cone`/`_spray_cone_across` re-deriving the fragment ray-projection
  formula inline in `app/sensitivity.py` instead of calling
  `arty.zones.fragment_ground_impact` — flagged by `@model-reviewer` as a
  candidate follow-up, out of scope here.

## Decisions

**Across-view azimuth math (φ=±90° lobes, mirror-symmetric).** The elevation
view's two lobes correspond to azimuth φ=0°/180° and are asymmetric (AoF
tilts the x-z plane). The across view's two lobes correspond to φ=±90°; AoF
only tilts the x-z plane, so the two across lobes are exact mirror images of
each other (`vy = ±sinθ`, `vz = -sA·cosθ` — identical vz for both signs).
This makes the equatorial belt (θ=90°) horizontal (vz=0) in the across view —
visually degenerate for single-zone mode, but meaningful for four-zone mode's
off-equatorial zones (ogive, boattail, base).

**Ray-length cap derived from axis range, not a fixed constant.** Passing a
fixed `max_len` to the spray-cone polygon made horizontal rays (equatorial
belt) visibly hit a hard stop mid-plot, while near-vertical rays appeared
unbounded (clipped by the axis instead). Computing `max_len = y_max + z_max`
(always longer than any ray could need to cross the visible plot area) makes
the axis range the only visible clipping boundary, consistent across ray
orientations.

**Chart pairing: left↔across, right↔elevation.** The downrange slice chart
(fixes y, sweeps x) pairs with the elevation cross-section (x-z plane,
"looking from the side" at that y) conceptually; the cross-range slice chart
(fixes x, sweeps y) pairs with the across cross-section (y-z plane, "looking
downrange" at that x). Cross-sections are placed under their paired slice
chart so the two columns read top-to-bottom as one consistent view.

**Fine-resolution line evaluation over global grid tightening.** Two options
were considered for the sampling artifact: (a) shrink the global grid step
for the whole heatmap, or (b) add a line-only evaluator. (a) is O(n_grid²)
and would cost ~25x more compute for a 2.5m→0.5m step in an interactive app;
it also doesn't fully eliminate the risk (any fixed global step still has a
breakpoint). (b) reuses the exact governing equations from
`_four_zone_field_split` but evaluates only the points needed for one line,
so cost scales with line length, not grid area — chosen as `four_zone_line_split`
in `src/arty/zones.py`, called at a 0.25 m step (10x finer than the heatmap)
from a new `_compute_zone_line` cached wrapper in the app.

**No new derivation.** `four_zone_line_split` returns the same P(kill)
quantity already returned by `_four_zone_field_split`, just sampled off the
square-mesh constraint — classified as a numerical/sampling change, not new
physics, so it skipped the scoping/derivation pass that a new governing
equation would require.

## Risks / Trade-offs

- \[Two independent evaluators (`_four_zone_field_split` and
  `four_zone_line_split`) duplicate the per-point physics loop body\] →
  Mitigated by `@model-reviewer` confirming the loop bodies are formula-
  identical; any future physics change must be applied to both. A shared
  per-point helper would remove this duplication as a follow-up.
- [Fine line step (0.25 m) is still a fixed step, not adaptive] → Acceptable
  for this app's interactive use; the reported low-burst-height symptom
  (footprint width ≈1.46 m) is well above this step.
