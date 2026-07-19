---
name: z-quadrature-belt-discontinuity
description: any z-column quadrature of rho_L (vertical-extent aggregation, target-height-intercept and similar) crosses the belt's hard 0/1 membership cutoff inside the integration domain exactly at the false-safe-zone ring — trapezoid error is non-monotonic and >30% at the derivation's recommended n_z, numerically confirmed
metadata:
  type: project
---

`experiment/fragmentation-field/updates/target-height-intercept/derivation.md` §5
proposes replacing the single `z=0` ρ_L sample with a composite-trapezoid
column integral `λ(x,y) = w_perp·∫₀ʰ ρ_L(x,y,z) dz` (eq. 2/5), and justifies
`n_z = 9` (default 12) by arguing `ρ_L(z)` "varies smoothly" over a human
height. This is false exactly where the fix matters: `lethal_density_point`
(`fragmentation.py:485`, `if abs(cos_Theta) > sin(delta_rad): return 0.0`) is a
**hard 0/1 belt-membership cutoff, not smoothed** — inside the belt `ρ_L` is
finite, immediately outside it is exactly 0, a genuine jump discontinuity in
`z` at fixed `(x,y)`. At the AoF=90°/h_b=2m/δ=15° worked example the derivation
itself uses (§6.3), the belt-edge crossing height `z_edge = h_b − r·tanδ` lies
*inside* `[0, 1.7]` for essentially the entire ring `r ∈ [1.1, 7.5] m` that the
whole fix is designed to make non-zero — i.e., the discontinuity sits inside
the integration domain across almost the full region under test, not in some
unrelated corner of parameter space.

**Numerically confirmed** (`lethal_density_point` + `slant_range_grid` +
`build_mmin_table`, same burst geometry, default `ShellParams`): trapezoid
relative error vs. a 400-point reference at `n_z=9`/`n_z=12`: r=1.5m →
7.6%/21.7%; r=2.0m → 34.0%/1.7%; r=3.0m → 5.1%/6.9%; r=4.0m → 3.6%/9.7%. Errors
are **not monotonically decreasing** from `n_z=9` to `n_z=12` (r=1.5m gets
*worse*, 7.6%→21.7%) — the classic signature of a discontinuous integrand,
where trapezoid error depends on where grid points happen to fall relative to
the jump, not smoothly on `1/n_z`. This also undermines the derivation's own
proposed safety net: its "doubling convergence check,
`|λ_{2n_z}−λ_{n_z}|/λ_{n_z} < few%`" would have failed loudly at exactly the
`n_z=9→12` step *if it had actually been run* — the derivation recommends the
check but never executes it, and asserts the resolution passes without doing
so (same pattern as [[min_lethal_mass_saturation_check]] and
[[derivation_qualitative_claims_need_numeric_check]]: an "it's smooth/it
converges" claim stated on paper, contradicted the moment someone computes
the actual numbers).

**How to apply:** whenever a future derivation proposes numerically
integrating/aggregating `ρ_L` (or any Family-B field) along an axis that can
cross the belt-acceptance boundary within the integration interval — vertical
column height, a line-segment cross-section, a widened silhouette footprint,
etc. — do not accept an "n resolves it because the field is smooth" claim on
paper. Require either (a) an actual numeric convergence table (not just the
claim that a doubling check would pass) at the specific geometry used as the
headline worked example, or (b) a quadrature that locates the belt-boundary
crossing analytically per query point and integrates piecewise-exactly across
it (the discontinuity is a single point per `(x,y)` column, cheap to find),
rather than blind uniform trapezoid across a possible jump.

**Follow-on (option (b) has its own numerical-stability trap):** see
[[piecewise_quadrature_boundary_evaluation]] — once a derivation adopts
option (b), check whether its quadrature rule samples the analytic
breakpoints themselves (endpoint-inclusive trapezoid), which reintroduces a
smaller but still real (~6%, `O(1/n_seg)`) bias at the same ring geometry, via
a different mechanism (floating-point boundary-membership mismatch, not the
uniform-grid straddle this entry describes).
