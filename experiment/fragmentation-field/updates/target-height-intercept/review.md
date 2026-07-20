# Review — target-height fragment intercept (false safe-zone fix)

**Verdict: PASS-with-limitations**

**Note on process:** this review was written after the fact (backfill). The
review cycle for this aspect evidently happened inline during derivation —
`derivation.md` itself cites reviewer-measured numbers (§5.1 "Reviewer
independently measured 7.6%→21.7% at n9→12, r=1.5") and a revision-2 fix
(§5.2/§5.4, "revision 1"/"revision 2" endpoint-vs-midpoint quadrature) that
match exactly the defects recorded in this reviewer's own persistent memory
(`z_quadrature_belt_discontinuity`, `piecewise_quadrature_boundary_evaluation`,
`quadratic_root_cancellation_near_A_zero`) — but no `review.md` artifact was
ever committed. This pass re-verifies those closures against the code as it
exists today (post `field-builder-performance` vectorisation, reviewed
separately in `updates/field-builder-performance/review.md`) and adds one new
finding not previously logged.

## Scope

`scoping.md` (Option 1 selected: vertical-extent aggregation of the ρ_L field)
and `derivation.md` (eq. 2/3/6: `λ(x,y) = w_perp·∫₀ʰ ρ_L dz`, `P_k=1−e^{−λ}`,
composite-midpoint quadrature over analytic belt breakpoints), as implemented
in `src/arty/fragmentation.py` (`pkill_field_3d`, `belt_column_breakpoints`,
`integrate_column_density`, `_stable_quadratic_roots`, and their vectorised
counterparts) and `src/arty/zones.py` (`four_zone_pkill_field`,
`four_zone_pkill_line`, `_active_zone_specs`). Numerical equivalence of the
vectorised paths to the scalar reference is **not** re-verified here — that is
`field-builder-performance/review.md`'s scope; this pass treats the retained
scalar `belt_column_breakpoints`/`integrate_column_density` as the physics
reference and checks it (and what it feeds) against the derivation and the
checklist.

## Verification performed

- Read `scoping.md` and `derivation.md` in full; cross-checked every symbol,
  unit, and boundary claim in `derivation.md` §6 (dimensions, degenerate-limit,
  §6.3 worked table, monotonicity, straight-line constraint) against the
  current `pkill_field_3d`/`four_zone_pkill_field` source and docstrings —
  all match; no drift between the derivation and the shipped code.
- Confirmed the four previously-identified quadrature defects are closed in
  the current tree: `integrate_column_density` uses composite **midpoint**
  (never an endpoint) sampling; `_stable_quadratic_roots` uses the
  cancellation-free Numerical-Recipes form with an `|A|<eps` linear fallback;
  `belt_column_breakpoints`'s `K = cosθ^z ± sinδ` generalises correctly to
  four zones; `n_seg=9` is the shipped default in both `pkill_field_3d` and
  `four_zone_pkill_field`.
- Ran `tests/test_pkill_field.py` and `tests/test_vectorized_equivalence.py`:
  34/34 pass. Confirmed both the single-zone and four-zone paths carry the
  **same** headline defect-removal assertion
  (`P_k_stand[ring].max() > 0.5` on the AoF=90° close-in ring), not a weaker
  invariant on one path — closes the parity gap this reviewer has previously
  flagged in sibling aspects.
- Confirmed the `_pkill-field.qmd` inline onset formula
  `r ≈ (h_b−h)/tanδ ≈ 1.1 m` is the corrected form (not the `h_b/tanδ` typo
  previously found and logged); numerically checked it against the printed
  ring statistics (2.0−1.7)/tan15° ≈ 1.12 m, consistent.
- Confirmed the "fine near-field grid for the ring statistic" pattern in the
  PRONE cell of `_pkill-field.qmd` (dense `n_grid=201`, `max_radius=10.0`
  aside from the coarse 60 m plot grid) — addresses the grid-threshold
  aliasing this reviewer previously flagged elsewhere; the qmd explicitly
  documents *why* (a coarse grid can alias the hard belt-crossing step to a
  spurious 0%).
- Checked layering: `app/sensitivity.py` and `src/arty/plots.py` diffs are
  pure wiring/rendering (new `fig_pkill_field`, a new Streamlit expander
  calling `pkill_field_3d`/`four_zone_pkill_field`, and `fig_pkill_volume`
  docstring/isomin retuning explicitly marked "No physics here"). No physical
  quantity is computed inline in the `.qmd` or `app/` beyond descriptive prose
  of an already-implemented formula.
- Independent numerical check (own scratch script, not in the tree) of the
  one derivation claim not covered by an existing test or the worked table: the
  "residual accuracy risk near the burst" case in derivation §5.3/§7 (A4),
  `r→0` with `h_b∈(0,h)` — see Findings below.
- Spot-checked boundary/edge cases: `r=0` exactly under a horizontal
  (AoF=90°) belt with `h_b` inside the standing column reads `P_k=0` at that
  single on-axis point (correct: a horizontal spray plane never sends a
  fragment straight down); every neighbouring cell saturates smoothly to
  `P_k=1` with no NaN or out-of-`[0,1]` values (`assert` in both builders is
  never tripped). Maximum-range falloff (`P_k→0` as `r→∞`) and grazing-angle
  (`AoF→δ`, the `A→0` quadratic degeneracy) are exercised by
  `test_pkill_columns_vec_at_zone_spray_angle`.

## Findings

**Deferrable — derivation §5.3/§7(A4) "λ→0 continuously" claim is backwards
for the case it is stated for; no output impact.** `derivation.md` §5.3
argues the one place `n_seg=9` could under-resolve is `r→0` with
`h_b∈[0,h]` (burst height inside the target's own column), and states "the
segment also narrows as `r→0`, so `λ→0` continuously (no spurious spike)."
Numerically this is inverted: in that exact sub-case (burst height strictly
inside the standing column, e.g. `h_b=0.5`, `h=1.7`, AoF=90°) the belt
segment width narrows as `r·tanδ`, but the density on it scales as
`~1/r²` (since `s≈r` throughout the thin segment), so `λ ~ (2 tanδ)/r`
**diverges** as `r→0` — confirmed by direct computation:
`λ(r=0.05)≈4880`, `λ(r=0.10)≈2438`, `λ(r=1.0)≈240`, an almost-exact `1/r`
scaling, not a decay to zero. The `λ→0` behaviour the derivation describes
is real, but belongs to the *other* case worked in §6.3 (`h_b∉[0,h]`, the
shipped default `h_b=2.0 > h=1.7`), where the column never reaches the belt
near `r=0` — the two cases were conflated in the write-up.

- **Impact on the rendered field: none.** `P_k=1−e^{−λ}` saturates to
  `1.0` for any `λ` beyond a few units, so whether the true `λ` is 240 or
  4880 is invisible in the output — the ground heatmap shows the same
  solid-red near-burst region either way (verified: `pkill_field_3d` at
  `h_b=0.5`, `AoF=90°`, radius 10 m, `n_grid=101` — every cell with
  `r∈[0.2,10)` reads `P_k=1.000000` to 6 decimals, no NaN, no
  out-of-`[0,1]` value; only the single exact-axis `r=0` cell reads `0`,
  correctly).
- **Impact on quadrature accuracy: also none** — the concern that
  `n_seg=9` "could under-resolve" this regime does not materialize either:
  measured relative error of the shipped `n_seg=9` midpoint rule vs.
  `n_seg=999` at `r=0.05,…,2.0` m in this exact configuration stays flat
  at `~0.026%–0.027%` across the whole sweep (no growth toward `r=0`), an
  order of magnitude inside the `<0.005%` (§5.4, default config) to
  single-digit-percent range already accepted elsewhere in the derivation.
  The physical reason: within the thin belt segment `s≈r` varies only
  mildly (by a factor `1/cosδ≈1.035`), so the integrand is nearly flat
  there regardless of how large its absolute value is — midpoint handles
  it fine at `n_seg=9`.
- **Suggested correction (limitation-log only, not a code fix):** reword
  `derivation.md` §5.3 and §7 (A4) to state the correct direction — `λ`
  diverges (not `→0`) as `r→0` when `h_b` lies inside the target's column,
  but `P_k` saturates to 1 well before the quadrature error could matter,
  so the "residual risk" is moot in practice (verified, not merely
  asserted). No `n_seg`-doubling runtime check is needed. Optionally note
  in `_limitations.qmd` that the single exact on-axis point under a
  horizontal belt reads a true `P_k=0` (a physical, not numerical,
  artifact — a horizontal spray plane never sends a fragment straight
  down) while every neighbouring cell is at or near certain-kill — a
  reader glancing at a single-pixel dark spot at the burst cross could
  otherwise misread it as a bug.

**Note — `_limitations.qmd`'s target-height-intercept entry does not restate
assumption A3 (vertical target, flat ground, no terrain/tilt).** A2 (Poisson
independence, binary `E_leth` cut) and A1 (frontal-projection-only, no
obliquity) are both carried into `_limitations.qmd` (§"False safe zone... —
fixed in v0.5.1"); A3 is only in `derivation.md` §7. Since A3 is inherited
from the rest of the ground-field model (already implicit elsewhere in the
notebook) and changes no output, this is presentational completeness only —
no action required.

## Limitations to log

- `derivation.md` §5.3/§7 (A4): the "λ→0 continuously as r→0" claim for the
  `h_b∈(0,h)` near-burst case is directionally wrong (λ actually diverges
  ~1/r there); correct wording per the Deferrable finding above. No output
  or accuracy impact — `P_k` saturates and `n_seg=9` stays \<0.03% accurate
  throughout, both confirmed numerically in this review.

## Checklist coverage

- Dimensional analysis: PASS (derivation §6.1 table verified against code;
  `λ` is a dimensionless count in both eq. 2 and eq. 6).
- Boundary cases: zero range (on-axis dead point, correct), maximum range
  (falls to 0), grazing angle (`α→δ`, tested and stable) — all checked, see
  above.
- Parameter ranges: `STANDING`/`PRONE` `(w_perp, h)` values are ordinary
  human-silhouette dimensions (0.5×1.7 m, 0.5×0.3 m), unchanged by this
  aspect and already accepted in prior reviews.
- Numerical stability: `_stable_quadratic_roots` A→0 fallback verified by
  `test_pkill_columns_vec_at_zone_spray_angle`; `s<1e-6` singularity guard
  and `s_floor` in `slant_range_grid` prevent division-by-zero; no NaN/inf
  observed in any configuration probed.
- Physical plausibility: standing never scores below prone (tested both
  paths); false-safe ring is filled exactly where the geometric honesty
  check predicts (derivation §6.3); ρ_L kernel itself is unchanged and was
  reviewed previously.
- Source attribution: no new physical constants or empirical anchors
  introduced by this aspect (pure reformulation of an existing, already-cited
  kernel and Poisson wrapper); N/A beyond what prior reviews cover.
- Layering: PASS — `.qmd` and `app/` changes are wiring/rendering/prose only,
  explicitly marked "No physics here" where applicable; no computed physical
  quantity leaked into a notebook cell.
- Limitations: PASS-with-limitations — see the one item above to log.
- Data-driven analysis: derivation §5.4's dense 59-column r-sweep plus this
  review's independent near-burst convergence sweep both support the
  accuracy claims with executed numbers, not spot-checks alone.
