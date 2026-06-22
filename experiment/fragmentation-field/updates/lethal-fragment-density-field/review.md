# Review — Lethal-Fragment Density Field (target-independent, arbitrary 3D point)

## src/ implementation review (2026-06-20, fourth pass)

**Reviewer:** model-reviewer agent
**Scope:** `git diff src/arty/fragmentation.py src/arty/zones.py` — the src/
implementation pass against the PASSed `derivation.md` (below).

### Verdict: **PASS**

The implementation matches the derivation faithfully and every oracle number
in derivation.md §9 reproduces independently (I did not trust the modeler's
reported figures — I re-derived/re-ran each one myself with my own scripts,
not the modeler's):

| Oracle                                       | Modeler reported | Independently reproduced                                                                                                                              |
| -------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| z=0 reduction (belt pts vs direct bisection) | 1.1e-06          | 1.10e-06 (312 sampled pts)                                                                                                                            |
| m_min interp vs bisection (10 sampled s)     | 6.3e-07          | 5.1e-07                                                                                                                                               |
| Far-field decay, s≈800m                      | 4.4e-09          | 4.45e-09 (found the actual belt-ring geometry myself: at h_b=2, AoF=30° the z=0 belt sits at x≈−1.155, not a naive +x downrange scan)                 |
| Single-vs-four-zone consistency, off-x=0     | 0.0 (exact)      | 0.0 (exact) — built my own synthetic 4-equal-zone collapsed cylinder, point (5,20,0)                                                                  |
| Belt/δ/at-burst guards                       | exact 0          | exact 0 (δ=0, δ\<0, out-of-belt, s\<1e-6 all confirmed); zero-mass/zero-V0/non-finite-mu zone skip confirmed with a synthetic empty zone (no NaN/inf) |

**Axis-convention fix verified non-vacuous.** Scanned a 200×200 (x,y) grid at
z=0 with default params comparing belt acceptance under the legacy
`_shell_axis` `(−cosα,0,−sinα)` vs the new `_forward_shell_axis`
`(+cosα,0,−sinα)`: **3.1% of grid points (1244/40000) disagree** on belt
acceptance between the two conventions — concrete proof this is a real fix,
not a no-op relabeling, consistent with the derivation's own §5.4
non-equivalence proof.

**§9's legacy-bug observation independently confirmed, and confirmed
out-of-scope as claimed.** Read `_expected_kills_3d_point`
(`fragmentation.py:491-532`, untouched by this diff): it still divides by
`sin_Theta` (the field point's own polar angle from the shell axis, line
523/531), not `sinθ^z`. The new `lethal_density_point` correctly hardcodes
`sin_theta_z=1.0` (equatorial, θ=90°) rather than computing `sinΘ`. The
four-zone path was **never** affected — `zones.py`'s pre-existing
`_four_zone_field_split` (line 466, predates this diff) already used
`sin_theta_z = np.sin(theta_z)` correctly; only the single-zone legacy
function had the bug, and only the new `ρ_L` paths fix it (for themselves),
leaving the legacy target-coupled field as-is per the stated out-of-scope
decision. This is a correct, narrowly-scoped fix — no scope creep into the
legacy evaluator.

**Layering:** clean. All new physics lives in `src/arty/fragmentation.py` and
`src/arty/zones.py`; no `.qmd`/`app/` call sites exist yet for this code
(grepped `app/` and `experiment/` — zero references), so there is nothing to
flag for physics leakage at this stage. This is implementation-only; the
notebook-presentation pass has not happened yet.

**Boundary/guard behavior:** all guards (δ≤0, out-of-belt, at-burst
singularity, degenerate zones) return exactly 0.0 and never propagate NaN/inf
— checked directly, not inferred. `compute_lethal_density_field_3d` and
`four_zone_lethal_density_field` size their own `s_grid` from the same `z`
they query (`max(z, h_b)` consistently used for both grid-sizing and the
query height), confirmed by direct computation that `s_grid[-1]` always
covers the true box-corner maximum slant range for several z values tested
(0, 40) — no extrapolation risk through the current call graph.

### Issue (Minor) — silent `np.interp` clipping in the public per-point API

`lethal_density_point` and `lethal_density_four_zone_point` accept a
caller-supplied `s_grid`/`mmin_grid` and call bare `np.interp(s, s_grid, mmin_grid)` with no range check. `np.interp` **silently clips** to the
boundary value when `s` falls outside `[s_grid[0], s_grid[-1]]`, rather than
raising or extrapolating. Verified by hand: building a grid for `z_max=h_b`
and querying a point at `z=79` (`s≈135.7m` vs grid max `118.8m`) gives an
interpolated `m_min=0.00644 kg` vs the true bisected `m_min=0.00723 kg` — an
~11% error that grows with distance past the edge, silently, with no warning.

This is **not exercised by any current call site** — both public field
builders (`compute_lethal_density_field_3d`, `four_zone_lethal_density_field`)
build their grid from the same `z` argument they query, so the mismatch
cannot occur through them today. It is a latent foot-gun in the lower-level
per-point functions' API contract, relevant only if a future caller (e.g. a
single-point probe widget, or a slice/contour helper analogous to
`four_zone_line_split`) builds or reuses a grid for one `z`/box extent and
then queries points outside it.

**Suggested correction (do not apply):** add a one-line docstring caveat on
`lethal_density_point`/`lethal_density_four_zone_point` stating that `s_grid`
must cover the full range of slant ranges that will be queried, and that
out-of-range queries silently clip rather than error; or add a cheap
`assert s_grid[0] <= s <= s_grid[-1]` (debug-mode only, to avoid a per-point
cost in the hot loop) if/when a new caller starts supplying its own grid
independent of the field-builder functions.

### Other checks (no issues)

- **Dimensional analysis:** unaffected by the implementation; matches
  derivation §4 (already validated, no new equations introduced beyond what
  the derivation specified).
- **Parameter ranges:** `E_LETH_DEFAULT=1000.0` matches the derivation's §3
  recorded choice exactly; `n_s=400` default matches §6.2's provisional
  choice; real per-zone params from `compute_shell_zones(ShellParams())`
  spot-checked (V0 650–1020 m/s, masses summing sensibly, spray angles
  78–165°) — all within previously-validated literature bounds for this
  model.
- **Physical plausibility:** default z=0 field (n_grid=80) has 15.7% nonzero
  (in-belt) grid fraction, consistent with a 30°-wide belt; `ρ_L` ranges
  ~0.016–74 m⁻² (peak at the `s_min=0.5m` numerical floor near burst),
  median nonzero ~0.05 m⁻² — sensible magnitude, no red flags.
- **Test suite:** full existing suite passes with no regressions (191
  passed, 4 skipped). No new tests were added for the new functions in this
  pass (`tests/test_fragmentation.py`/`test_zones.py` have zero references) —
  flag for the notebook/validation pass to add the oracle assertions
  derivation.md §6.3/§8 call for as checked-in tests, not just this review's
  ad hoc verification.

### Summary

**PASS.** Implementation is a faithful, narrowly-scoped realization of the
approved derivation; every reported oracle number is real and independently
reproducible; the axis-convention fix is proven non-vacuous; the legacy-bug
observation is accurate and correctly left out of scope. One Minor latent API
foot-gun (`np.interp` silent clipping) noted for awareness — does not block
this pass since it is unreachable through any current call site, but should
be addressed (docstring or assert) before any future caller supplies its own
grid. Recommend adding checked-in tests for the new functions in the
upcoming notebook/validation pass.

______________________________________________________________________

## Derivation review (2026-06-20, third pass — re-review of modeler's second revision)

**Reviewer:** model-reviewer agent
**Scope:** `scoping.md` + `derivation.md` in this folder (pre-implementation; no
`src/arty/` code exists yet).

### Verdict: **PASS**

This is a third-pass re-review of the modeler's latest revision to §5.4/§5.5,
following two prior FAILs on the same belt-axis-convention issue (preserved
below for traceability). **This revision resolves it.** The document no longer
claims the two old axis conventions (`(−cosα,…)` single-zone vs. `(+cosα,…)`
four-zone) are equivalent, invariant, or a "safe"/"physics-neutral"
relabeling under any operation. Instead it:

1. **Keeps the worked counter-example** (`α=30°`, point `(20,0,2)` →
   `|cosΘ_single|≈0.812 ≠ |cosΘ_four|≈0.912`) explicitly labelled "the proof of
   non-equivalence" (derivation.md:276-279, 287-288) — the falsifying evidence
   from the second FAIL is preserved, not papered over.
1. **Correctly identifies the one operation that *would* be neutral** —
   negating the entire axis vector (`ê → −ê`, all three components, giving
   `cosΘ → −cosΘ` so `|cosΘ|` is exactly invariant) — and explicitly
   distinguishes it from the x-only flip actually being adopted, which it
   states plainly is "not the same... does not leave `|cosΘ|` invariant off
   the `x=0` plane" (derivation.md:285-294). This is precisely the distinction
   the second-pass revision blurred.
1. **Reframes the resolution as a deliberate standardisation choice**, not a
   proof: "We therefore make **no** claim that the flip is physics-neutral...
   pick **one** convention and write it into both paths" (derivation.md:294-296).
   The post-standardisation pointwise agreement is stated correctly as holding
   *by construction* — i.e., trivially, because both paths literally evaluate
   the same formula — never because the old formulas were shown equivalent
   (derivation.md:298-301, 312-319, 340-346, 354).
1. **Defers all quantitative pointwise-agreement evidence to §8's numerical
   spot-check**, repeated four times for emphasis (§5.4 "What this is, and is
   not, evidence of," §5.5 closing paragraph, §7 checklist row, §8 bullet) —
   each instance correctly states the by-construction belt-test argument is
   *not* sufficient on its own and the spot-check is the "sole evidence."
1. **Keeps §5.5's Mott-`μ` collapse tolerance argument appropriately scoped**:
   it reuses the prior `frag-field-3d-geometry/derivation.md:309` aggregate
   magnitude-after-merging statement (verified to exist at that line, vendored
   accurately) only for the parameter/mass-collapse part of the consistency
   claim — not for the belt-test pointwise claim, which is correctly kept
   separate and deferred to §8.

I independently re-derived the counter-example algebra (§5.4) symbolically
from `cosΘ = r̂·ê_axis` for both conventions and confirmed
`cosΘ_single = -rx·cosα - rz·sinα`, `cosΘ_four = rx·cosα - rz·sinα` are equal
in magnitude only on `rx=0` or `rz=0` or `α=0` — matching the document's own
statement of when they coincide, with no overreach beyond that. I also
confirmed both axis formulas and accept-test forms against current source
(`fragmentation.py` belt guard ~line 414, `_shell_axis`; `zones.py:429,453`)
— the document's quoted code locations and formulas match the actual
implementation exactly (see Bash excerpts below in this review's working
notes; not reproduced here since they match verbatim).

**No remaining issue.** The §6.1/§6.2 Moderate issue (near-burst `m_min(s)`
"flat plateau" claim) was already resolved in the prior pass and remains
correctly resolved — unchanged in this revision.

______________________________________________________________________

## Resolution history — Major issue (now resolved) — axis-convention "equivalence" claims, three attempts

**Claim (derivation.md:281-297):** "At `θ = 90°` ... the sign of `ê_axis`'s
x-component is *physically arbitrary* ... flipping the x-sign cannot change
which side is 'forward' — it merely relabels a symmetric belt. Hence replacing
the single-zone path's historical `(−cosα,…)` with `(+cosα,…)` is a **safe
normalisation, not a physics change**, for the equatorial case."

**This is incorrect.** The operation that *would* be a harmless relabeling of
a fore/aft-symmetric equatorial belt is negating the **entire** axis vector,
`ê → −ê` (all three components) — under that transformation `cosΘ → −cosΘ`,
so `|cosΘ|` (which is all the equatorial test ever uses) is exactly invariant,
for any ray. That is not the transformation being proposed. The proposal flips
**only the x-component**, leaving the z-component (`−sinα`) untouched:

```
ê_old = (−cosα, 0, −sinα)        ê_new = (+cosα, 0, −sinα)
```

This is a different vector, not `−ê_old` (unless `sinα = 0`, i.e. `α = 0`).
For a general ray `r̂ = (rx, ry, rz)`:

```
cosΘ_old = −rx·cosα − rz·sinα
cosΘ_new = +rx·cosα − rz·sinα
```

`|cosΘ_old| = |cosΘ_new|` only when `rx·cosα` and `rz·sinα` happen to combine
symmetrically — i.e. only on `rx = 0`, `rz = 0`, or `α = 0` — exactly the same
degeneracy condition flagged in the *original* Major issue. **This is the same
algebra, unchanged**; the revision did not fix the underlying claim, it
re-derived the identical false conclusion from a differently-worded premise.

**Hand re-check using the document's own worked example** (`α = 30°`, point
`(20, 0, 2)` rel. burst, `s ≈ 20.0998`). Using the opposite sign convention for
the z-component of `r̂` than the document used (`rz = +0.0995` instead of
`−0.0995` — an internal sign-convention detail that does not matter for
`|·|`), by hand:

- `ê_old = (−0.8660, 0, −0.5)`: `cosΘ_old = 0.99503(−0.8660) + 0.0995(−0.5) = −0.8617 − 0.0498 = −0.9114`
- `ê_new = (+0.8660, 0, −0.5)`: `cosΘ_new = 0.99503(0.8660) + 0.0995(−0.5) = 0.8617 − 0.0498 = 0.8119`

`|cosΘ_old| ≈ 0.911 ≠ |cosΘ_new| ≈ 0.812` — a ~0.10 gap, the same order as the
document's own §5.4 example (`0.812` vs `0.912`, those exact two numbers,
just swapped which convention lands on which value because of the z-sign
flip). **The revision's own arithmetic, run with the point on the other side
of the sign convention, reproduces the discrepancy it claims to have resolved
away.** With `δ = 15°` (`sinδ ≈ 0.259`), both numbers here still exceed
`sinδ` so both conventions reject this particular point — but as before, the
two `|cosΘ| = sinδ` boundary surfaces are different surfaces in space whenever
`α ≠ 0`, `rx ≠ 0`, `rz ≠ 0`; there exist points (near either boundary) accepted
by one convention and rejected by the other. Swapping which convention is
"new" vs "old" does not change this.

**Why this still matters:** §5.5 ("Single-zone ↔ four-zone consistency") now
explicitly leans on §5.4's normalisation as "exactly what lifts \[the
consistency statement\] to a pointwise statement" (derivation.md:321-323,
333). Since the normalisation step is not actually a no-op at θ=90° (it
changes the accepted point set, as shown above), §5.5's claim that the
collapsed four-zone test becomes "the same equatorial test ... with the same
`ê_axis` ... so the accepted point set is now identical pointwise, everywhere,
not only on `x=0`" inherits the same flaw. The four-zone path's `ê_axis = (+cosα,0,−sinα)` does not change in this proposal (it's already that), so the
real content of the "fix" is only: *replace the single-zone path's
`(−cosα,…)` with `(+cosα,…)` too.* That is a legitimate, even sensible,
implementation choice on its own engineering merits (one canonical convention
is good practice) — but it is **not** "physics-neutral" as claimed, and after
making it, single- and four-zone equatorial belts are pointwise identical
**by construction** (both literally use the same `ê_axis` formula), which is
a trivially true and different statement than what §5.4/§5.5 currently argue
("the sign flip doesn't matter, so doing it is safe"). The document should
make the trivial argument, not the false one.

**Suggested correction (do not apply):** Rewrite §5.4's resolution to state
plainly: *the single-zone path's existing `(−cosα,…)` convention and the
four-zone path's `(+cosα,…)` convention are genuinely different (not
equivalent, not a relabeling) for any `α≠0`; we choose to standardise on the
four-zone convention for the unified evaluator going forward, which makes the
two paths trivially identical by construction (same formula) rather than
provably equivalent under the old single-zone formula.* Drop "physically
arbitrary," "safe normalisation, not a physics change," and "merely relabels a
symmetric belt" — these phrases assert an invariance that the document's own
numbers contradict. Then §5.5 should say the post-normalisation pointwise
agreement holds *because both paths now share one formula*, not because the
change was shown to be neutral. This changes no recommended code (still:
adopt `(+cosα,…)` everywhere) and needs no new derivation — it is purely a
correction to the written justification, but it must be fixed because the
document currently asserts something false as the *reason* the implementation
choice is safe, and a future reader (or the src/ implementation pass) may
rely on the false invariance claim elsewhere (e.g. to skip the numerical
spot-check §5.5/§8 already — to its credit — flags as required). Keep the
already-planned numerical spot-check in the src/ pass regardless — it is now
the *only* thing actually establishing pointwise agreement, not a
confirmation of an independently-argued equivalence.

______________________________________________________________________

## Resolved — §6.1/§6.2 near-burst `m_min(s)` claim (prior Moderate issue)

**Now correctly fixed.** §2 explicitly states "there is no flat near-burst
plateau to lean on in §6" and gives the same numeric check as the prior
review (`mass_shell = 12.04 kg`, `V0 ≈ 995 m/s`, `KE(m_lo) ≈ 0.49 J ≪ E_leth = 1000 J`), independently re-verified here against current
`fragmentation.py:46-53` defaults (`mass_total=14.97`, `mass_filler=2.18`,
`mass_deductions=0.75` unchanged) and `gurney_velocity`/TNT constant
(`fragmentation.py:19,164-166`) — the arithmetic holds. §6.1 now correctly
frames `s_min = 0.5 m` purely as a numerical guard against the `1/s²`
singularity, not a region of flatness. §6.2 has been rewritten to drop the
flat-plateau justification, explicitly label its own resolution argument as
"not backed by an actual `max|m_min''(s)|` estimate ... a qualitative
expectation," and correctly designates the §6.3 interpolation oracle as the
real acceptance gate with `n_s=400` as a provisional, oracle-confirmed
starting point. This matches suggested correction (b) from the prior review
exactly. No remaining issue here.

______________________________________________________________________

## Original Major issue text (superseded by the re-check above; kept for traceability)

**Claim (prior derivation.md:254-262):** "For the equatorial belt (θ=90° ⇒
cosθᶻ=0) the four-zone test reduces to `|cosΘ| ≤ sinδ`, **identical in
magnitude** to the single-zone test. The x-sign flip in `ê_axis` flips the
sign of `cosΘ` but the single-zone guard takes `|cosΘ|`, so the **accepted
set is the same** for the equatorial belt."

**This is incorrect in general.** The two axis conventions are
`e_single = (-cosα, 0, -sinα)` (`fragmentation.py:382`) and
`e_four = (cosα, 0, -sinα)` (`zones.py:429,453`). These differ by a sign flip
on the **x-component only**, not the whole vector — so `cosΘ_single` and
`cosΘ_four` are not simply each other's negation. For a general ray
`r̂ = (rx, ry, rz)`:

```
cosΘ_single = -rx·cosα - rz·sinα
cosΘ_four   =  rx·cosα - rz·sinα
```

`cosΘ_single = -cosΘ_four` only holds when `rz = 0`; the two are unrelated in
general. Worked counter-example: `α = 30°` (AoF), field point `(x,y,z) = (20, 0, 2)` relative to burst → `s ≈ 20.1`, `r̂ ≈ (0.995, 0, -0.0995)`.

- `cosΘ_single = -0.995·cos30° - (-0.0995)·sin30° ≈ -0.812`
- `cosΘ_four   =  0.995·cos30° - (-0.0995)·sin30° ≈ +0.912`

`|cosΘ_single| = 0.812 ≠ |cosΘ_four| = 0.912`. With `δ = 15°` (`sinδ ≈ 0.259`), `single` would be tested as `0.812 > 0.259` → **rejected**, while
`four` would be tested as `0.912 > 0.259` → also rejected here, but the
*magnitudes* differ enough that there exist points accepted by one
convention and rejected by the other (the boundary `|cosΘ|=sinδ` is crossed
at different physical points for the two conventions whenever `α≠0` and
`rx≠0`, i.e. whenever AoF is nonzero and the point is off the `y-z` plane —
which is the entire interesting region of a downrange field plot). The claim
only happens to hold on the `x=0` plane (`rx=0`) or in the degenerate
`α=0` (perfectly horizontal AoF) case.

**Why this matters:** §5.5 ("Single-zone ↔ four-zone consistency") leans on
§5.4 to argue the four per-zone belt tests "collapse to the one equatorial
test" when zones are merged. That collapse is only true exactly on the
`x=0` line, not generally — so the §5.5 consistency check, as currently
justified, does not establish what it claims for an arbitrary 3D point (the
stated aspiration of this whole derivation, per B1). The prior
`frag-field-3d-geometry/derivation.md` (§5, line ~309) only ever validated
field *magnitude* equivalence after full integration/merging into one
equivalent cylinder (an aggregate statement) — it never asserted pointwise
`|cosΘ|` equivalence between the two axis conventions, so this derivation
has overextended that prior, weaker result into a stronger (and false)
pointwise claim.

**Suggested correction (do not apply):** Drop the "identical in magnitude"
claim. State instead that eq. (3) should be written with **one** convention
applied consistently to both paths (the four-zone forward-axis convention
`(+cosα, 0, -sinα)` is fine to standardize on, as the derivation already
recommends for the implementation), and that the single-zone path's existing
`(-cosα, 0, -sinα)` + `|cosΘ|`-guard is a **historical, not provably
equivalent**, convention that the field-evaluator implementation should
either (a) replace with the four-zone convention for the single-zone case too
(since at `θ=90°` the sign of `e_axis`'s x-component is physically arbitrary
for an isolated cylinder — there is no "forward" zone to break the symmetry —
so this is a safe normalization), or (b) keep separate and document that the
two paths are *not* expected to agree pointwise off the `x=0` plane, only in
the aggregate/merged sense already validated upstream. Re-run §5.5's
consistency check under whichever resolution is chosen, since the current
text's justification chain is broken.

______________________________________________________________________

## Moderate issue — §6.1/§6.2 near-burst "flat" `m_min(s)` claim does not hold for default shell parameters

**Claim (derivation.md §6.1, §6.2):** floor the slant-range grid at `s_min = 0.5 m`, "below which `m_min = m_lo` and `N → N0`, flat," and the resolution
argument in §6.2 assumes the only steep region in `m_min(s)` is "the
immediate neighbourhood of the lethal edge" (far field), implying a flat
near-burst region.

**Checked against actual defaults** (`ShellParams()`, TNT filler,
`gurney_velocity`): `mass_shell = 14.97 - 2.18 - 0.75 = 12.04 kg`,
`V0 = 2440 / sqrt(12.04/2.18 + 0.5) ≈ 995 m/s`. The `min_lethal_mass`
saturation-to-`m_lo` branch only triggers when `_ke(m_lo) ≥ E_leth`, i.e.
`0.5 · 1e-6 · (995·e^{-λs})² ≥ 1000 J`. Even at `s → 0` (no drag at all),
`0.5·1e-6·995² ≈ 0.49 J`, four orders of magnitude below `E_leth = 1000 J`.
**The `m_lo` saturation branch is essentially unreachable for this shell's
parameters at the chosen `E_leth`** — `m_min(s)` is solved by bisection (a
genuinely varying, not flat, value) arbitrarily close to the burst, not
clipped to `m_lo`.

**Why this matters:** the §6.2 resolution justification ("`Δs ≈ s_max/400`
gives error well under 0.1%... everywhere except the immediate neighbourhood
of the lethal edge") implicitly assumes a flat (cheap-to-interpolate) region
near the burst balances the one steep region far away. If `m_min(s)` is
instead varying smoothly-but-non-trivially across the *entire* range
(no flat plateau at either end except possibly the far `m_hi` clip), the
qualitative "order of magnitude below tolerance" argument is weaker than
claimed, though not necessarily wrong — it was never backed by an actual
`max|m_min''(s)|` estimate, only by the (incorrect) assumption of a flat
near-burst region. This doesn't invalidate the recommended C1/C2 strategy,
but the written justification overstates its own basis.

**Suggested correction (do not apply):** Either (a) verify numerically with
the real default parameters where/whether `m_min(s)` actually flattens
near `s_min` (it may not, given the above), and rewrite §6.1/§6.2 to reflect
the true shape, or (b) drop the "flat near burst" framing entirely and rely
solely on the §6.3 interpolation oracle (already planned) as the actual
acceptance gate, treating the `n_s=400` choice as a starting point to be
confirmed empirically rather than analytically justified. Given §6.3's oracle
check already exists and is the right tool for this, (b) is the lower-risk
fix — the analytical resolution argument can be softened to "expected to be
adequate; confirmed empirically by the §6.3 oracle" rather than asserted as
self-evidently correct.

______________________________________________________________________

## Checked and confirmed correct (no issues)

- **Dimensional analysis (§4):** every row checks out against source
  (`fragmentation.py`/`zones.py`), including the `δ`-as-radians and
  `2 sinθ·δ` solid-angle-fraction framing, which matches the prior validated
  `frag-field-3d-geometry/derivation.md` §3.8 exactly (spreading factor alone
  is m⁻²; `A_p · spreading` is dimensionless — consistent both there and
  here).
- **`z=0` reduction (§5.1):** algebraically correct — setting `z=0` in eq.
  (1)-(2) exactly reproduces `fragmentation.py:407,412` /
  `zones.py:448,451`'s hardcoded ground-plane `s` and ray. The
  `A_p ← 1, pk_given_hit ← 𝟙[m≥m_min]` reduction and the boxed reconstruction
  identity are both correct: `∫ n(m)𝟙[m≥m_min] dm = N0 exp(-√(m_min/μ)) = mott_N(m_min, N0, mu)` matches `fragmentation.py:207,214` exactly.
- **Far-field decay (§5.3):** correct and confirmed plausible — at large `s`,
  drag forces `m_min → m_hi`, `N → N0·exp(-√(m_hi/μ)) → 0`; this is the
  correct distinguishing behavior vs. the rejected A2 option.
- **`δ→0` guard (§5.4):** correctly mirrors the existing
  `_expected_kills_3d_point` guard at `fragmentation.py:404-405`.
- **`E_leth = 1000 J` choice (§3):** verified directly against
  `doc-reference/wound-ballistics/fas-es310-damage-criteria/fas-es310-damage-criteria.md`
  — the 100/1000/4000 J → 0.1/0.5/0.9 anchors are accurately quoted, and the
  79 J rejection rationale matches both that document and the existing
  `_validation.qmd:94` comment ("not the model threshold") verbatim. The
  anchor choice (`_PK_E`/`_PK_VAL` at `fragmentation.py:140-141`) is real code,
  not invented. Good source attribution throughout §3.
- **Section citations:** `frag-field-3d-geometry/derivation.md §3.7-3.8` is
  correctly the AoF projection / presented-area-replacement (solid-angle)
  sections — verified against that file's actual heading numbers.
- **Layering:** both documents are pure markdown/math with **no
  implementation code** — appropriate for a pre-implementation derivation
  pass. Nothing to flag for the "no physics in `.qmd`" rule since no `.qmd`
  or `src/arty/` edit exists yet in this change.
- **Boundary/parameter ranges:** `m_lo=1e-6 kg`, `m_hi=2.0 kg` bounds, Mott
  `μ`/`N0` formulas, and Gurney `V0` are all reused unchanged from validated
  existing code — no new constants introduced by this derivation beyond
  `E_leth=1000J` (justified, see above) and the `n_s=400`/grid-extent choices
  (engineering heuristics, now correctly scoped to the §6.3 oracle, see
  "Resolved" above).
- **§2 / §6.1 / §6.2 rewrite:** independently re-verified against current
  `fragmentation.py` defaults (`mass_total=14.97`, `mass_filler=2.18`,
  `mass_deductions=0.75`, `gurney_const=2440.0` for TNT) — arithmetic in the
  derivation is correct and the framing change (drop flat-plateau claim, defer
  to oracle) is the right fix.

## Fallout from the still-open Major issue

- **§7 checklist** rows "Belt geometry guard returns 0 outside belt" and
  "Single- vs four-zone consistency" are both marked ✓ on the strength of the
  §5.4 normalisation argument; both should stay **unresolved** until §5.4 is
  rewritten per the suggested correction above. The underlying recommended
  *implementation* (adopt `(+cosα,0,−sinα)` for both paths) does not need to
  change — only the written justification for why it's safe.
- **§8 implementation note** ("Add a test asserting four-zone ... matches
  single-zone `ρ_L` at off-`x=0` 3D points") is good practice and should be
  kept regardless of how §5.4's prose is fixed — it is in fact the thing that
  will actually establish the pointwise agreement, not the (currently false)
  paper argument preceding it.

## Note for the src/ implementation pass

The recommended convention choice itself — standardise both paths on
`ê_axis = (+cosα,0,−sinα)` — is sound and can proceed once §5.4's prose is
corrected to justify it as "deliberate standardisation, not a provably-neutral
relabeling." The §5.5/§8 numerical spot-check at off-`x=0` 3D points remains
required and is now the *sole* evidence for pointwise agreement (no paper
argument substitutes for it) — do not skip it on the assumption that §5.4
already proved equivalence analytically.
