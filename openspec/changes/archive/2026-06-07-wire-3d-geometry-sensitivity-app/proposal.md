## Why

The sensitivity app currently drives `compute_frag_field_3d`, which treats the shell as a single-belt cylinder and uses one spray half-angle for all fragments. The `zones.py` physics (merged in `feature/frag-field-3d-geometry`) decomposes each shell into four zones — ogive, cylinder, boattail, base — each with its own Gurney velocity, Mott half-mass, and spray elevation angle; this is the model the experiment notebook now validates. Adding the four-zone model to the app lets users see how much difference the per-zone geometry makes and which zones drive lethality.

## What Changes

- The sidebar gains a **Model** radio: `Single-zone (legacy)` and `Four-zone (new)`.
  - Legacy path: `compute_frag_field_3d` exactly as before.
  - New path: `compute_shell_zones` + `four_zone_field` from `arty.zones`.
- The **2D heatmap section** switches to a **side-by-side comparison**: legacy field on the left, four-zone field on the right, and a signed difference map (Pk_new − Pk_old) spanning the full width below — but only when **Model = Four-zone**. When Model = Single-zone, only the single heatmap is shown (preserving the original layout).
- A new **Zone Breakdown** section appears below the heatmaps when Model = Four-zone:
  - A **grouped bar chart**: x-axis = zone (ogive, cylinder, boattail, base); bars for V₀ [m/s], N₀ (fragment count), and spray angle [°] for each zone (triple-grouped or faceted).
  - A **per-zone P(kill) vs cross-range** line chart: one line per zone plus a "total" line, showing which zone dominates lethality at each distance.
- `ShellParams` construction passes the ogive geometry fields from the preset (not user-sliders); users who want to explore ogive sensitivity use the notebook.
- Headline metrics show R₅₀, V₀, N₀, μ from the active model:
  - Legacy: same as before.
  - Four-zone: cylinder zone; labelled "(cyl zone)".
- A read-only **Tier badge** in the sidebar ("Tier-1 · arc geometry" / "Tier-2 · CRH fallback") appears next to the preset selectbox when Model = Four-zone.

## Capabilities

### New Capabilities

- `zone-breakdown-charts`: per-zone fragment properties (V₀, N₀, spray angle) grouped bar chart, and per-zone P(kill) vs cross-range contribution chart.

### Modified Capabilities

- `sensitivity-app`: model selector added; 2D heatmap section expands to side-by-side + diff when four-zone is active; headline metrics update to show cylinder-zone values with subtitle; cache now covers both compute paths.

## Impact

- `app/sensitivity.py` — primary edit target
- `src/arty/zones.py` — new imports (`compute_shell_zones`, `four_zone_field`)
- No changes to `src/arty/fragmentation.py`, `src/arty/shells.py`, or `src/arty/zones.py` physics
