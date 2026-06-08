## Context

`compute_frag_field_3d` currently computes `ke_by_mass` using the cross-range slant range:

```python
s_cross = np.sqrt(xy**2 + burst.h_b**2)
ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (V0 * np.exp(-lam_j * s_cross)) ** 2
```

`xy` is the grid linspace from -max_radius to max_radius, so `s_cross` folds from large → 0 → large. The app then plots this against a symmetric x-axis, effectively showing KE as a function of cross-range distance — not pure slant range. The notebook's Figure 2 uses a simple `s = linspace(0, max_range, n)` sweep, which is cleaner and direction-independent.

## Goals / Non-Goals

**Goals:**

- Replace the cross-range KE computation with a pure radial sweep from s=0 to s=max_radius
- Update the app chart to match notebook Figure 2 (x-axis: slant range s [m], one-sided)

**Non-Goals:**

- Adding new fragment mass classes or changing the three representative masses (0.5 g, 5 g, 50 g)
- Changing lethality threshold annotations (100 J, 1 kJ lines stay)
- Any physics model changes

## Decisions

**Radial sweep in library, not app**

Store the corrected KE in `FragField3dResult.ke_by_mass` rather than computing it fresh in the app. The library is the right place — any other consumer of the result struct gets the physically correct values too. The x-axis array is `np.linspace(0, max_radius, n_grid)` stored as a new field `r_ke` on the result, so the app doesn't have to reconstruct it.

Alternative considered: compute in the app only, leave library unchanged. Rejected — leaves a misleading value in the result struct that future callers would misuse.

**`r_ke` field on `FragField3dResult`**

Add `r_ke: np.ndarray` (shape n_grid, values 0…max_radius) as the x-axis companion to `ke_by_mass`. This keeps the chart self-contained — no need for the caller to know max_radius or n_grid.

## Risks / Trade-offs

- Any code that currently uses `ke_by_mass` as cross-range-indexed will silently get different values. Current callers: only `app/sensitivity.py`. Tests do not assert specific ke_by_mass values. → Low risk.
- `r_ke` is a new field on `FragField3dResult` — callers that construct the dataclass directly (none in production) would need updating. → Not applicable.
