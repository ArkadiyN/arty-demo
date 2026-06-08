## Why

The "Fragment KE vs Cross-Range Distance" chart in the sensitivity dashboard uses cross-range position (y) as its x-axis. KE decay is a function of slant range only — it is direction-agnostic. Framing it on the cross-range axis is arbitrary and misleading: it implies the chart is specific to the cross-range direction when it is not. The notebook's Figure 2 ("Fragment KE vs Distance from Burst") uses slant range s [m] as the x-axis, which is the physically correct framing.

## What Changes

- **`FragField3dResult.ke_by_mass`** — values changed from KE sampled along the cross-range slice (`s = sqrt(y² + h_b²)`) to KE sampled along a pure radial sweep (`s = linspace(0, max_radius, n_grid)`)
- **`app/sensitivity.py`** — KE chart x-axis changed from cross-range y [m] to slant range s [m]; title and axis label updated to match notebook Figure 2

## Capabilities

### New Capabilities

- none

### Modified Capabilities

- `fragmentation-physics`: `FragField3dResult.ke_by_mass` now stores KE vs radial slant range, not KE vs cross-range position
- `sensitivity-app`: KE chart x-axis is slant range s [m] from 0 to max_radius; matches notebook Figure 2

## Impact

- `src/arty/fragmentation.py` — `compute_frag_field_3d` ke_by_mass computation
- `app/sensitivity.py` — Figure 2 x-axis and labels
- No new public symbols; `FragField3dResult` field names unchanged, values corrected
