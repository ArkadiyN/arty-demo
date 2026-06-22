---
name: lethal-density-field-implementation
description: src/ implementation review of rho_L(x,y,z) lethal-fragment areal density (fragmentation.py + zones.py, 2026-06-20) — verified oracle numbers, found one latent np.interp silent-clip foot-gun in the public per-point API
metadata:
  type: project
---

`experiment/fragmentation-field/updates/lethal-fragment-density-field/` —
derivation.md PASSed (3rd pass, see [[belt_axis_convention_pitfall]] and
[[min_lethal_mass_saturation_check]]); this entry covers the **src/
implementation** pass review (`fragmentation.py`/`zones.py` diff,
+173/+150 lines respectively).

**New public API:** `fragmentation.py`: `_forward_shell_axis`,
`E_LETH_DEFAULT=1000.0`, `build_mmin_table`, `lethal_density_point`,
`slant_range_grid`, `compute_lethal_density_field_3d`. `zones.py`:
`lethal_density_four_zone_point`, `build_zone_mmin_tables`,
`four_zone_lethal_density_field`. Legacy `_shell_axis` and
`_expected_kills_3d_point` (with its pre-existing `sinΘ` bug, see below) are
**untouched** — confirmed by diff, no edits in that line range.

**Independently re-verified (did not trust the modeler's reported numbers),
all reproduced within float noise of the §9 table:**
- z=0 reduction (312 sampled belt pts vs direct bisection): got 1.10e-6 max
  rel err vs reported 1.1e-06.
- m_min interp vs bisect (10 sampled s): got 5.1e-7 vs reported 6.3e-07.
- Far-field decay along the actual belt line (not a naive +x scan — at
  h_b=2m, AoF=30°, the z=0 belt ring sits at x≈-1.155, not far downrange;
  had to solve for the ring geometrically) at s=800m: got 4.45e-9 vs reported
  4.4e-09 — exact match.
- Single-vs-four-zone consistency: built a synthetic 4-equal-zone collapsed
  cylinder (θ=90° all zones, summing to the single-zone N0/μ) myself rather
  than reusing modeler code; got exact 0.0 rel error at an off-x=0 point
  (5,20,0) — matches reported "0.0 (exact)."
- δ≤0, out-of-belt, at-burst (s<1e-6) guards all return exactly 0.0 in both
  paths; zero-mass/zero-V0/non-finite-mu zones are skipped (no NaN/inf
  propagation) — checked with a synthetic empty boattail zone.

**Confirmed §9's legacy-bug observation is real and correctly left
unfixed-in-scope:** `_expected_kills_3d_point` (fragmentation.py:491-532,
untouched) still divides by `sin_Theta` (field point's own polar angle,
line 523/531) instead of `sinθ^z`; the new `lethal_density_point` and the
pre-existing (already-correct) `_four_zone_field_split`/
`lethal_density_four_zone_point` both correctly use `sinθ^z`
(`sin_theta_z=1.0` hardcoded for the equatorial single-zone case; `np.sin(theta_z)`
per-zone in the four-zone path, e.g. `zones.py:466` — that line predates this
diff, confirming the four-zone path was never the buggy one).

**One real (latent, low-severity) finding not previously flagged:**
`lethal_density_point`/`lethal_density_four_zone_point` take a caller-supplied
`s_grid`/`mmin_grid` and call bare `np.interp(s, s_grid, mmin_grid)` with no
bounds check. `np.interp` silently **clips** to the boundary value for
`s > s_grid[-1]` rather than erroring or extrapolating — verified by hand:
mismatching a grid built for `z_max=h_b` against a query at `z=79` (s=135.7m
vs grid max 118.8m) gives `m_min=0.00644` interpolated vs `0.00723` true
bisection (~11% error, growing with distance past the edge). **Not currently
exercised** — both public 3D-field entrypoints
(`compute_lethal_density_field_3d`, `four_zone_lethal_density_field`) build
their own grid from the same `z` they query, verified by direct computation
that `s_grid[-1] >= max box corner distance` holds for every z tested
(including z=40, above h_b=2). So this is an API-misuse footgun for any
*future* direct caller of the lower-level point functions with an externally
supplied table, not a bug in the current call graph. Worth a one-line
docstring caveat or an assert if a future change starts calling these point
functions from outside their own field-builder (e.g. a per-point probe widget).

**No app/.qmd wiring exists yet** — confirmed via grep, zero call sites in
`app/` or `experiment/`. No new tests added either (`tests/test_fragmentation.py`,
`tests/test_zones.py` have zero references to the new functions) — full
existing suite (191 passed, 4 skipped) has no regressions, but the new code
itself is currently only covered by this review's ad hoc verification, not a
checked-in test. Flag for the notebook/test-adding pass.

**Physical plausibility spot-check:** default-shell z=0 field, n_grid=80,
nonzero (in-belt) fraction 15.7% of grid (consistent with a 30°-wide belt out
of the angular range), ρ_L ranges from ~0.016 to ~74 m⁻² (peak right at the
s_min=0.5m numerical floor), median nonzero ~0.05 m⁻² — sensible order of
magnitude for a lethal-fragment areal density field, no red flags.
