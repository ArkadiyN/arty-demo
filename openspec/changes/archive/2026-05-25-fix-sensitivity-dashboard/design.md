## Context

After integrating the 3D burst geometry model, two issues were identified in the sensitivity dashboard:

1. **Grid-alignment bug**: `compute_frag_field_3d` extracted the cross-range slice by reading grid column `j0 = argmin(|xy|)`. With even `n_grid`, zero never falls on a grid point — `j0` lands at x ≈ ±1 m. At AoF=0° this offset puts near-center cross-range points outside the belt window, producing a spurious P(kill)=0 gap at y=0.

1. **Redundant chart**: P(kill) vs Cross-Range is insensitive to angle of fall because the cross-range axis (y) is always perpendicular to the shell axis (which lies in the xz-plane). The 2D heatmap shows the same information plus the downrange asymmetry.

## Goals / Non-Goals

**Goals:**

- Eliminate the grid-alignment artifact from the cross-range slice
- Remove the redundant P(kill) vs Cross-Range chart
- Give the 2D heatmap more visual space

**Non-Goals:**

- Changing any physics or adding new model capabilities
- Modifying `FragField3dResult` fields or any public API

## Decisions

**Cross-range slice at x=0 via dedicated sweep (not grid column)**

Instead of reading `field_pk[:, j0]`, compute `pk_cross` by calling `_expected_kills_3d_point(0.0, y_g, ...)` for each `y_g` in `xy`. This adds one grid row of evaluations (~80 × 300 mass-bin integrals) but is exact and invariant to `n_grid` parity.

Alternative considered: force `n_grid` to be odd so zero always lands on a grid point. Rejected — fragile; breaks silently if a caller passes even `n_grid`.

**Layout: 2+1 (two small top, one full-width bottom)**

Remove Figure 3 (P(kill) cross-range), promote heatmap to full width at 500 px height. The two remaining small charts (Mott distribution, KE vs range) stay in the top row.

## Risks / Trade-offs

- Slight compute increase: ~1 extra grid row of `_expected_kills_3d_point` calls per render. At n_grid=80, n_mass=300 this is negligible (\<5% overhead). → No mitigation needed.
- `r50_cross` and `ke_by_mass` in `FragField3dResult` remain derived from the cross-range sweep, so their values change slightly (now exact at x=0 vs previously at x≈±1 m). This is a correction, not a regression. → Existing tests already pass with the corrected values.
