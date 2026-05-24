## Why

The sensitivity dashboard (`app/sensitivity.py`) still runs the original flat-trajectory, radially-symmetric 1D model (`compute_frag_field`), while the notebook has moved to a full 3D geometry with burst height, angle of fall, belt spray, and posture-dependent target area (`A_p(γ)`). The app caption still reads "flat trajectory" — it no longer reflects what the model actually computes.

## What Changes

- **Port 3D geometry to `src/arty/fragmentation.py`**: add `BurstParams`, `PostureParams` (STANDING/PRONE), `expected_kills_3d`, and `compute_frag_field_3d` — promoting the notebook's §6 implementation to the importable library
- **Update `app/sensitivity.py`** to use the 3D API: replace `compute_frag_field` with `compute_frag_field_3d`, add burst-height / AoF / spray-angle / posture controls, update the 2D field heatmap to show the asymmetric footprint, and remove the stale "flat trajectory" caption
- **Update app title and captions** to reflect 3D airburst model
- **No changes** to Mott distribution, ES-310 Pk|hit, drag model, or shell/filler registries — those are frozen

## Capabilities

### New Capabilities

- `burst-geometry`: 3D burst parameters exposed in the library and app — burst height, angle of fall, spray half-angle

### Modified Capabilities

- `sensitivity-app`: adds posture selector, burst-geometry controls, asymmetric 2D footprint; removes flat-trajectory assumption
- `fragmentation-physics`: adds `BurstParams`, `PostureParams`, `compute_frag_field_3d` to the public API

## Impact

- `src/arty/fragmentation.py` — new dataclasses and functions added; existing API unchanged (backward compatible)
- `app/sensitivity.py` — UI controls and plots updated; imports change
- `tests/test_fragmentation.py` — new tests for 3D API and backward-compat check
