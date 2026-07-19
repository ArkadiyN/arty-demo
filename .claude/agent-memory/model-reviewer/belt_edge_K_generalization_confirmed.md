---
name: belt-edge-K-generalization-confirmed
description: fragmentation.py belt_column_breakpoints' per-zone K=cosθ^z±sinδ quadratic (generalizing target-height-intercept derivation eq. 5, worked only for cosθ^z=0) is a sound algebraic generalization, confirmed both by hand-derivation and against an independent brute-force reference across multiple four-zone columns; also documents a self-caught verification trap (aof=90° masks axis-convention bugs)
metadata:
  type: project
---

`experiment/fragmentation-field/updates/target-height-intercept/derivation.md` §5.2
only works the belt-edge quadratic (eq. 5) for the single equatorial belt
(`cosθ^z = 0`). The src/ implementation (`fragmentation.py:belt_column_breakpoints`,
reused by `zones.py:four_zone_pkill_field`/`four_zone_pkill_line`) generalizes it
per-zone to `K = cosθ^z ± sinδ`, `A = sin²α − K²`, `C = x²cos²α − K²(x²+y²)`.
Re-derived by hand from `cosΘ = K ⟺ (x cosα − ζ sinα)² = K²(x²+y²+ζ²)`: this is
exactly the same substitution as eq. 5 with `K` replacing `sinδ` (the `cosθ^z=0`
case is the `K=±sinδ` special case) — not a new model, a correct parametrization
of the same closed-form intercept for an off-centre belt. Also verified
numerically: at six four-zone columns (`105mm M1 HE`, AoF 90°, exercising
`ogive`/`cylinder`/`boattail`/`base` cos θ^z simultaneously), the piecewise
composite-midpoint quadrature (`n_seg=9`) matched a 20000-point brute-force
reference to `<0.01%` at every point (harness deleted after use, not kept).
Squaring `cosΘ=K` does admit a spurious `cosΘ=−K` root per `K`, but since both
`±K` roots are always collected, no genuine crossing can be missed — only extra
(harmless) breakpoints subdividing an already-smooth interval — so the docstring's
"handled harmlessly" claim holds.

The `_stable_quadratic_roots` cancellation-free form (`q = −½(B+sgn(B)√disc)`,
roots `q/A`, `C/q`) also already degenerates correctly as `A→0` *without*
needing the explicit `|A|<eps` linear-fallback branch to fire: one root (`C/q`)
naturally converges to the linear solution `−C/B`, the other (`q/A`) diverges
and gets filtered by the `(z_lo,z_hi)` domain test. The explicit branch only
guards the literal `A=0`/`B=0` division. Confirmed stable (no NaN/Inf, `P_k`
always in `[0,1]`) across an angle-of-fall sweep 1°–89° in 2° steps on the
four-zone field.

**Self-caught verification trap (useful for future reviews of this file):**
when checking `four_zone_pkill_line`'s docstring claim ("matches
`four_zone_pkill_field` exactly at coincident nodes"), a first pass compared
`fixed_axis="x"` output against `Pk_field[10, :]` and got a false "0.0 diff"
pass — because the test config used AoF=90°, whose vertical-fall belt is
rotationally symmetric, so the (wrong) row slice and the (correct) column
slice `Pk_field[:, 10]` happen to coincide. Re-running at AoF=30° (asymmetric)
exposed the mismatch (`Pk_field[5,:]` differs from the line by 0.66; `Pk_field[:,5]`
matches to `0.0`) — confirming the actual claim is true, but only once verified
at an asymmetric AoF. Same root cause as [[zones_meshgrid_convention]] and
[[belt_axis_convention_pitfall]]: this file's X/Y meshgrid-axis roles are easy
to get backwards, and AoF=90° silently hides the mistake. **How to apply:**
any future numeric equivalence check between a `zones.py` line helper and its
2D field counterpart must use an asymmetric AoF (not 90°) or it can pass for
the wrong reason.
