## Why

The Family-B ρ_L → P(kill) ground fields (`four_zone_pkill_field`, `pkill_field_3d`, and the
app's line-slice variant) evaluate lethal fragment density at `z = 0` only. At steep angle of
fall the belt sprays near-horizontally through burst height, never crossing the ground plane
near the burst — so those cells read `P(kill) ≈ 0` even though a standing or prone person
occupying that column would be struck. This is the "false safe zone" documented in
`experiment/fragmentation-field/_limitations.qmd` (§184-204) and confirmed by a modeler scoping
pass (`experiment/fragmentation-field/updates/target-height-intercept/scoping.md`): the fields
already carry a z-resolved ρ_L kernel (used by the 3D volume view), so the fix is to aggregate
that existing kernel over the target's height column instead of sampling a single plane.

## What Changes

- Replace the `P_k = 1 − exp(−ρ_L(z=0)·A_ref)` transform on the Family-B ground fields with the
  vertical-extent integral `P_k = 1 − exp(−w_perp·∫₀ʰ ρ_L(x,y,z) dz)`, where `h` and `w_perp` come
  from the existing posture parameters (standing/prone).
- This re-couples posture sensitivity to the ground P(kill) fields, which the current frozen
  `A_ref = 0.85 m²` constant discards.
- No change to fragment trajectory physics: fragments remain straight-line rays: no gravity or
  ballistic curvature is introduced.
- The 3D `P(kill)(x,y,z)` volume view (`pkill_volume_3d` / `four_zone_pkill_volume`) is
  **unaffected** — it already evaluates ρ_L at arbitrary height and answers a different question
  (point-in-space lethality vs. a standing/prone person's whole vertical extent). Its app caption
  may be reworded for clarity but no computation changes.
- **Out of scope (deferred, separate aspect):** the graded Family-A fields (`four_zone_field`,
  `compute_frag_field_3d`, and the app's headline 2D heatmaps) exhibit the same false-safe-zone
  symptom via a different governing weighting (`presented_area(γ)·pk_given_hit(E)`) and are not
  touched by this change.
- **Reopened after initial completion:** the app (`app/sensitivity.py`) had no consumer of the
  fixed transform at all — the headline 2D heatmaps and cross-section slices call the Family-A
  `four_zone_field`/`compute_frag_field_3d`/`four_zone_line_split` path, not
  `pkill_field_3d`/`four_zone_pkill_field`. Since this is a major fix to the model, the app now
  gets its own new section exposing it: a standalone Plotly heatmap of the Family-B ground
  `P(kill)(x,y)` field, in its own expander next to the existing "3D Kill Probability" expander —
  not a diff against the Family-A heatmaps, since the two families answer different physical
  questions and are not the same quantity at different resolution.

## Capabilities

### New Capabilities

- `pkill-ground-field`: the Family-B ρ_L→P(kill) ground-map transform, defined as an integral of
  lethal fragment density over the target's vertical extent `[0, h]` rather than a single-plane
  (`z = 0`) sample; covers `four_zone_pkill_field`, `pkill_field_3d`, and the app's cross-section
  line evaluator.

### Modified Capabilities

- `sensitivity-app`: adds a requirement that the app expose the Family-B ground P(kill)
  column-integral field in its own expander (reopened scope — see below). `fragmentation-physics`
  and the Family-A app heatmaps it covers are unmodified; the existing 3D volume capability,
  `pkill-3d-view`, has no requirement change since its transform and grid are untouched.

## Impact

- `src/arty/zones.py`: `four_zone_pkill_field`, `_four_zone_field_split`'s Family-B counterpart,
  `four_zone_line_split`'s Family-B path — swap the z=0 sample for the `[0,h]` vertical integral.
- `src/arty/fragmentation.py`: `pkill_field_3d` (single-zone twin) — same transform swap.
- `app/sensitivity.py`: the existing 2D heatmaps and cross-section slices (lines ~715-953) call
  the unaffected Family-A path and do not change. The 3D volume expander (lines ~955-1008) is
  unchanged except possibly its caption text. A **new** "Ground Kill Probability" expander is
  added (next to the 3D volume one) that calls `pkill_field_3d`/`four_zone_pkill_field` directly —
  this is the app's only consumer of this change's fixed transform.
- `experiment/fragmentation-field/`: notebook section presenting the ground P(kill) field updates
  its change log; `_limitations.qmd`'s false-safe-zone note is updated to point at the fix.
- No changes to `shells.py`, the shell registry, or drag/Mott/Gurney physics.
