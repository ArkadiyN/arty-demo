## Why

The `elevation-view-chart` spec says the sensitivity app's elevation cross-section
uses `fig_single_zone_elevation`/`fig_zone_elevation` from `src/arty/plots.py`.
In reality those two functions render matplotlib figures for the Quarto
notebook only; the Streamlit app has its own local Plotly functions
(`_plotly_elevation`, `_plotly_elevation_across`, `_spray_cone`,
`_spray_cone_across`) in `app/sensitivity.py`. Worse, `_spray_cone` and
`_spray_cone_across` re-derive the fragment ray-projection formula
(`vgx`/`vgy`/`vgz`) inline instead of going through
`arty.zones.fragment_ground_impact`, which already implements and documents
that exact formula (see `burst-geometry` spec) — a physics formula duplicated
in the app layer, which this project's architecture rules forbid. This was
already flagged once by `@model-reviewer` as a follow-up during the
`across-slice-view` change and deferred as out of scope; fixing it now closes
both the spec-accuracy gap and the underlying duplication.

## What Changes

- Eliminate the duplicated ray-projection trig in `_spray_cone` /
  `_spray_cone_across` (`app/sensitivity.py`) by sourcing the ray-direction
  geometry from `arty.zones` instead of recomputing it locally. The exact
  shape of that shared source (e.g. exposing the direction vector from
  `fragment_ground_impact`, or a new small helper) is a `src/arty/` design
  decision, not prescribed here.
- Correct the `elevation-view-chart` spec so it documents the sensitivity
  app's actual local Plotly functions (names, file, behavior) instead of
  implying they live in `src/arty/plots.py`. The notebook-facing
  `fig_single_zone_elevation`/`fig_zone_elevation` requirements are unaffected
  (those remain correct for the Quarto notebook).

## Capabilities

### Modified Capabilities

- `burst-geometry`: `fragment_ground_impact` (or a small companion helper)
  becomes the single source of the ray-direction formula used both for
  ground-impact computation and for the app's spray-cone ray rendering
  (including rays that don't reach the ground and are drawn capped instead).
- `elevation-view-chart`: the "Elevation chart appears in the sensitivity app"
  requirement is corrected to name the actual app-local Plotly functions and
  their file, and gains a requirement that their ray geometry is sourced from
  `arty.zones`, not re-derived.

## Impact

- `src/arty/zones.py`: `fragment_ground_impact` and/or a new companion helper
  exposing the ray-direction components for rendering use.
- `app/sensitivity.py`: `_spray_cone` / `_spray_cone_across` refactored to call
  the shared source instead of recomputing `vgx`/`vgy`/`vgz` inline. No visual
  change to the rendered charts.
- `openspec/specs/elevation-view-chart/spec.md`: corrected function names/
  locations for the sensitivity-app requirement.
