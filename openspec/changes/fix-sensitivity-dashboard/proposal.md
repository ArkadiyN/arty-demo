## Why

Two issues were found in the sensitivity dashboard after the 3D model integration: (1) the cross-range P(kill) slice had a grid-alignment bug that produced a spurious zero-P(kill) gap at y=0, and (2) the P(kill) vs Cross-Range chart was identified as redundant — the cross-range axis is geometrically insensitive to angle of fall, making the chart less informative than the 2D heatmap it sits alongside.

## What Changes

- **Bug fix**: cross-range slice in `compute_frag_field_3d` is now evaluated at exactly x=0 via a dedicated 1D sweep, rather than reading column `j0` from the 2D grid (which was offset by ~1 m when n_grid is even)
- **Removed**: P(kill) vs Cross-Range Distance chart (Figure 3 of the previous 2×2 layout)
- **Resized**: 2D Fragmentation Field heatmap promoted to full-width, height increased from 340 px to 500 px

## Capabilities

### New Capabilities

- none

### Modified Capabilities

- `sensitivity-app`: layout changes from 2×2 to 2+1 (two small charts top row, one full-width heatmap); cross-range chart removed
- `fragmentation-physics`: `compute_frag_field_3d` cross-range slice now evaluated at x=0 exactly, independent of grid resolution

## Impact

- `src/arty/fragmentation.py` — `compute_frag_field_3d` cross-range sweep change
- `app/sensitivity.py` — layout restructure, Figure 3 removed
- No API changes; `FragField3dResult` fields unchanged
