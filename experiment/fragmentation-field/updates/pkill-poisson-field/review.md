# Review — Point kill-probability field $P_k(x,y,z)$ (pkill-poisson-field)

**Reviewer:** model-reviewer agent
**Date:** 2026-06-21 (re-review)
**Scope:** `experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md`
(revised), re-checked against the prior **FAIL (moderate)** finding and the
rest of the derivation. `scoping.md` was not updated by this pass — see note
at the end.

## Verdict: **PASS**

The prior FAIL finding is resolved. The revision correctly disentangles two
previously-conflated simplifications, correctly characterizes the cited
ES-310 source, and quantifies the consequence accurately. The rest of the
derivation (dimensional analysis, limit cases, monotonicity, linearization,
z=0 inheritance) remains sound on re-check.

______________________________________________________________________

## Resolution of prior Issue 1 (ES-310 mismatch) — CONFIRMED FIXED

**§2 (intro + step 3, lines 64–87, 114–142) and (A2)(ii) (lines 151–164).**
The derivation now:

1. Quotes the literal ES-310 aggregate `Pk = 1 - (1-Pk|hit)^Nhits` and states
   plainly that eq. (1) "is **not**... the literal ES-310 aggregate formula" —
   re-verified against `doc-reference/wound-ballistics/fas-es310-damage-criteria/fas-es310-damage-criteria.md`
   (lines 42–55): the quoted formula and the `Pk|hit=0.5` anchor at 1000 J are
   reproduced accurately.
1. Correctly identifies eq. (1) as the `P_k|hit → 1` special case of that
   aggregate, not a consequence of it.
1. Separates the **two** simplifications cleanly: (i) the binary `E_leth`
   threshold inherited from the prerequisite `ρ_L` derivation (≥50%-lethal-
   on-hit membership — re-verified the prerequisite's own §3 wording,
   `lethal-fragment-density-field/derivation.md:152-160`, matches exactly what
   the new derivation attributes to it), and (ii) the new `P_k|hit:0.5→1`
   promotion made at the Poisson aggregation step. No remaining language
   states or implies that (ii) is forced by (i) ("by definition" language is
   gone; checked the full file).
1. States the quantitative consequence ("systematically more pessimistic...
   by construction, not error") with specific numbers, all independently
   recomputed and confirmed exact:
   - λ=2: eq.(1)=0.8647 vs ES-310 `1-(1-0.5)^2`=0.75 ✓
   - λ=5: eq.(1)=0.9933 vs `1-0.5^5`=0.9688 ✓
   - small-λ ratio ≈2 (λ=0.01: 0.0100 vs 0.0050; λ=0.05: 0.0488 vs 0.0250) ✓

This is no longer an uncited, silently-strengthened claim — it is an
explicit, disclosed, quantified modelling choice, which is exactly what the
prior review asked for. The (A2) caveat and the "matched pair up to..."
paragraph (lines 168–177) are now mutually consistent with step 3.

**New §4.7** (near-saturation consequence) is a reasonable and accurate
follow-on: re-verified ρ_L=2 m⁻² → λ=1.7 → P_k=0.8173 (matches text "0.817"),
and ρ_L=10 m⁻² → P_k=0.9998 (matches "→1 by ρ_L≈10"). Correctly framed as an
expected, non-defect consequence to be handled in the notebook/colour-scale
pass, not silently absorbed.

______________________________________________________________________

## Re-checked and still PASS (unchanged math)

- **Dimensional analysis (§3).** `ρ_L[m⁻²]·A_ref[m²]` → dimensionless
  exponent; `P_k` dimensionless. Correct.
- **Limit cases (§4.1–4.4).** λ→0 ⇒ P_k→0; λ→∞ ⇒ P_k→1; P_k∈[0,1] always;
  `∂P_k/∂ρ_L = A_ref·e^{-λ} > 0` strictly — re-verified numerically.
- **§4.5 linearization.** `P_k ≈ λ - λ²/2`; spot-check λ=0.05 → 0.04877
  matches text.
- **§4.6 z=0 slice.** Pure elementwise map of an already-verified-identical
  ρ_L slice; correctly inherits the prerequisite's slice-identity argument,
  no new work needed.
- **A_ref = 0.85 m².** Unchanged, correctly traced to
  `fragmentation.py` `STANDING.w_perp=0.5, h=1.7`.
- **Source attribution.** Now accurate throughout — the ES-310 citation
  supports the *aggregation shape* and the *0.5 anchor it contradicts*, both
  correctly distinguished from the model's own chosen simplification.
- **No leaked physics.** Still prose/math only; no `src/arty/` or `.qmd`
  changes exist yet for this pass (unchanged from prior review — re-check
  again once those passes land).

______________________________________________________________________

## Non-blocking note — `scoping.md` not updated

`scoping.md` §3 (lines 126, 170–171: "the binary cut and the Poisson reading
are the *matched* pair... No physics defect here") still carries the
original, now-superseded framing. This is **acceptable to leave as-is**:
`derivation.md` is the operative document that downstream consumers (src/
docstrings, app captions, the OpenSpec spec text) will be briefed from, and
it now carries the corrected, quantified caveat language throughout.
Recommended (optional, non-blocking): add a one-line pointer in scoping.md §3
to derivation.md §2 step 3 / (A2) so a future reader landing on scoping.md
alone isn't misled by its still-overstated "no physics defect" line.

______________________________________________________________________

## Not reviewed (out of scope for this pass)

- `src/arty/` implementation does not exist yet — re-review when
  `pkill_field_3d`/`pkill_volume_3d` land (derivation §6 plan).
- `.qmd`/app wiring does not exist yet — re-check "no physics in notebook"
  once that pass lands; also re-check the §4.7 near-saturation consequence is
  handled deliberately in the colour-scale choice, not just inherited
  silently.
- OpenSpec `pkill-3d-surface-view` spec text — main agent's follow-up.

______________________________________________________________________

## Implementation review (2026-06-21)

**Scope:** `src/arty/fragmentation.py` (`A_REF_DEFAULT`, `pkill_field_3d`,
`pkill_volume_3d`) and `src/arty/zones.py` (`four_zone_pkill_field`,
`four_zone_pkill_volume`), plus `tests/test_pkill_field.py`. Diffed with
`git diff src/arty/fragmentation.py src/arty/zones.py tests/test_pkill_field.py`.

### Verdict: **PASS**

### Formula fidelity — independently re-verified, not trusted from the diff

Built an independent oracle script (computed `ρ_L` via the already-reviewed
`compute_lethal_density_field_3d` / `compute_lethal_density_volume_3d` /
`four_zone_lethal_density_field` / `four_zone_lethal_density_volume`, then
applied `1 − exp(−ρ_L·A_ref)` myself) and compared against each of the four
new wrapper functions on real (non-trivial) shell/burst parameters:

- `pkill_field_3d` vs `1 − exp(−ρ_L·A_REF_DEFAULT)`: max abs err **0.0** (bit-identical).
- `pkill_volume_3d` with a non-default `A_ref=1.23` override: max abs err **0.0**.
- `four_zone_pkill_field` vs the four-zone `ρ_L` oracle: max abs err **0.0**.
- `four_zone_pkill_volume[0]` vs transform of `four_zone_lethal_density_volume[0]`: max abs err **0.0**.

All four wrappers are exactly the elementwise transform claimed in the
derivation — no hidden re-weighting, no accidental use of a different `ρ_L`
path, no off-by-one in argument forwarding (`X`, `Y` meshgrids from
`pkill_field_3d` are array-identical to the independently-called `ρ_L`
builder's `X`, `Y`, confirming no grid mismatch).

### A_ref constant

`A_REF_DEFAULT = 0.85` matches `STANDING = PostureParams(w_perp=0.5, h=1.7, …)`
→ `0.5 × 1.7 = 0.85` exactly, per derivation eq. (2). It is a plain
module-level float, not a `presented_area(...)` call — matches the derivation
§6 implementation note (frozen, posture/angle-independent scalar). All four
function signatures expose `A_ref: float = A_REF_DEFAULT` as an overridable
argument, confirmed with a non-default value above.

### Boundary / numerical-stability cases

- Out-of-belt points (`ρ_L = 0`, 338/400 grid points on the default-shell
  z=0 field): `P_k` is **exactly** `0.0`, not just close — `1 − exp(0) = 1 − 1`
  is exact in floating point, no epsilon leakage.
- Near-peak `ρ_L` (≈5.48 m⁻² at the grid resolution tested, consistent with
  the reviewed `ρ_L` magnitude range): `P_k ≈ 0.990`, correctly `< 1`, no
  saturation-to-exactly-1.0 artifact at finite `ρ_L`.
- `exp(−ρ_L·A_ref)` — the exponent is always `≤ 0` since `ρ_L ≥ 0` and
  `A_ref > 0` by construction, so this is `exp` of a non-positive argument:
  **no overflow path exists** (only `exp(+x)` for large `x` overflows; here
  the worst case underflows cleanly to `0.0`, giving `P_k → 1.0`). Checked
  `ρ_L ∈ {0, 1e-9, 1e-3, 1, 10, 100, 1e6}` — all map into `[0,1]`, including
  the `1e6` extreme.
- Each of the four wrappers carries `assert np.all((P_k >= 0.0) & (P_k <= 1.0))`
  before returning — a real runtime guard, not just a derivation claim;
  confirmed present in the diff for all four functions and never tripped
  across all test/oracle runs.
- `z=0` slice identity (`pkill_volume_3d`, `four_zone_pkill_volume`): re-ran
  independently — `0.0` max abs err against the field function, confirming
  the deterministic-transform inheritance argument (derivation §4.6) holds
  in code, not just on paper.

### Dimensional / physical plausibility

No new dimensional content beyond the derivation's own check (§3) — confirmed
the code performs exactly `ρ_L[m⁻²] · A_ref[m²] → [-]` then `1 − exp(·)`,
nothing else folded in. `P_k` magnitudes observed (saturating to ~0.99 well
before the field's peak `ρ_L`) are consistent with the derivation's §4.7
near-saturation prediction — not a red flag, the expected and disclosed
behaviour of the `P_{k|hit}=1` choice.

### Tests (`tests/test_pkill_field.py`)

Coverage matches the derivation's validation checklist (§5): zero-density →
zero, monotonicity, `[0,1]` bounds (including the geometry-independent
transform-only tests, which correctly avoid re-testing the `ρ_L` kernel
itself per the file's own docstring rationale), and `z=0` slice identity for
both single- and four-zone wrappers. `pytest tests/test_pkill_field.py tests/test_lethal_density_volume.py -q` → 11 passed; full suite `pytest -q`
→ 202 passed, 4 skipped, no regressions.

### Layering — no physics leaked

`grep`-confirmed zero references to `pkill_field_3d` / `pkill_volume_3d` /
`four_zone_pkill_*` in `app/` or any `.qmd`/`openspec/changes/*/specs` —
the wiring pass has not landed yet, so there is nothing to flag here. The
`openspec/changes/pkill-3d-surface-view/` folder exists (proposal/design/
tasks/specs) but does not yet reference the new functions; re-check this
item once the notebook/app/spec pass lands.

### Source attribution

Unchanged from the derivation review — the implementation carries the A1/A2
caveats and the ES-310-mismatch disclosure verbatim into the four functions'
docstrings (Poisson independence/no shielding; binary threshold +
`P_{k|hit}=1` promotion; "more pessimistic than the ES-310 aggregate; not a
tissue-level wound model"). No claim in the code is unsupported by the
already-reviewed derivation.

### Not reviewed (out of scope for this pass)

- The prerequisite `ρ_L` kernel itself (`lethal_density_point`,
  `compute_lethal_density_field_3d`/`_volume_3d`,
  `four_zone_lethal_density_field`/`_volume`, `slant_range_grid`,
  `build_mmin_table`/`build_zone_mmin_tables`) — these appear in the same
  working-tree diff (uncommitted alongside the `pkill_*` wrappers) but belong
  to the separate, already-reviewed `updates/lethal-fragment-density-field/`
  change (see `[[lethal_density_field_implementation]]` memory entry). Noted
  in passing: `slant_range_grid`'s geometric-lower-bound logic and the
  `four_zone_lethal_density_field` `z_min` fix visible in this diff are *not*
  part of this change's scope and were not re-reviewed here.
- `.qmd`/app wiring and the OpenSpec `pkill-3d-surface-view` spec text — not
  yet written; re-check layering and the §4.7 colour-scale handling once they
  land.

______________________________________________________________________

## Delta review — 2026-07-19 (commit `a98aa5b`, presentation-layer pass)

**Scope:** commit `a98aa5b` ("docs(fragmentation-field): separate Family A/B
presentation, add pkill-field notebook section") diffed against its parent,
plus the current state of `derivation.md` and every notebook partial the
commit touched: `_four-zone-3d.qmd`, `_governing-equations.qmd`,
`_limitations.qmd`, `_pkill-field.qmd` (new file), `_change-log.qmd`,
`fragmentation-field.qmd`. This pass post-dates a *further*, separately
reviewed rewrite of `_pkill-field.qmd` by the `target-height-intercept`
aspect (v0.5.1, `updates/target-height-intercept/review.md`,
PASS-with-limitations) — where that later rewrite fully superseded content
`a98aa5b` added, this review says so explicitly rather than re-reviewing
already-reviewed material.

### Verdict: **PASS-with-limitations**

No Blocking findings. One Deferrable finding (stale citation, numerically
reconfirmed correct in this pass — see below).

### Findings

**Note — belt-axis-convention disclosure (`_four-zone-3d.qmd` intro table +
§6.8, `_limitations.qmd` §12 bullet).** This commit adds exactly the framing
memory (`belt_axis_convention_pitfall`) says survives review: the
single-zone/four-zone `P(kill)` diff in the app is described as a
"directional indicator," explicitly **not** a "clean physical isolation," and
the root cause is named (legacy backward axis `(−cosα,0,−sinα)` vs. the
four-zone forward axis `(+cosα,0,−sinα)`). Independently re-verified against
`src/arty/fragmentation.py`: `_expected_kills_3d_point`/`_expected_kills_3d_vec`
(feeding `result.field_pk`, the single-zone side of `app/sensitivity.py`'s
`diff_pk`) call `_shell_axis` (backward); `zones.py`'s `four_zone_field`
(feeding `result_zones["pk_total"]`) calls `_forward_shell_axis` at both its
call sites (`:709`, `:791`) — the claimed divergence is real and correctly
attributed to the Family-A graded pathway, not the eq. (1)/(23) Poisson path
this aspect owns. `app/sensitivity.py:812` confirms both sides of `diff_pk`
share one grid (`X[0]`/`Y[:,0]` from the same `linspace`), so the "grid-exact
diff, non-exact attribution" framing is accurate. This also closes the
specific second-instance recurrence the memory entry flagged at
`_four-zone-3d.qmd` §6.8 ("attached to a plot that performs no diff at
all") — re-read `plots.fig_zone_footprint` and confirmed it plots each zone's
own rays from a single call with no subtraction, matching the new prose
exactly. No output impact either way (documentation-only); recorded because
it resolves a previously-open memory item, not because it changes a number.

**Deferrable — `derivation.md` §4.7 cites a notebook computation that no
longer exists in the file it names; the underlying number is independently
reconfirmed correct here.** §4.7 (as revised by this commit) states the
`P_k` field is fringe-dominated, quoting "~3% (single-zone) / ~1% (four-zone)
of lethal-field cells clear `P_k > 0.95`" and cites `_pkill-field.qmd` plus
"@model-reviewer's independent re-check of the same geometry" as the
evidence. Two problems with the citation trail, neither changing the
underlying claim:

- `_pkill-field.qmd` was completely rewritten by the later
  `target-height-intercept` pass (v0.5.1): it no longer samples the `z=0`
  plane at AoF=30°/h_b=2m with the frozen-`A_ref` transform, and prints no
  `P_k>0.95` fraction anywhere. A reader following the derivation's
  citation into the current notebook will not find the number it names.
- No committed `review.md` entry (before this one) documents a
  model-reviewer re-check of this specific figure — the claim in
  `derivation.md` predates any artifact backing it, the same
  inline-review-without-artifact pattern already seen and accepted in
  `updates/target-height-intercept/review.md`.
- **Independent reconfirmation performed in this pass:** the frozen-`A_ref`
  point transform derivation eq. (1) describes is still live, unchanged, in
  `pkill_volume_3d`/`four_zone_pkill_volume`'s `z=0` slice (confirmed by
  reading `fragmentation.py:1228-1234`: `P_k = 1 - exp(-rho_L * A_ref)`,
  bit-for-bit eq. (1)). Recomputed the fraction at the stated geometry
  (AoF=30°, `h_b=2` m, `z=0`, 105 mm M1 HE, same `shell`/`drag` params as
  the notebook's `_parameters.qmd`/`_lethal-density.qmd` cells) at the
  notebook's own grid resolutions (`n_grid=60` single-zone, `n_grid=50`
  four-zone): **3.18% single-zone, 1.05% four-zone** — matches the "~3%/~1%"
  claim closely. Swept `n_grid` from 30–200 for both paths to rule out the
  grid-threshold-fraction-aliasing failure mode this reviewer has
  previously caught elsewhere (`ground_grid_threshold_fraction_aliasing`
  memory): single-zone stays in 2.4–3.2%, four-zone in 1.0–1.2% across the
  whole sweep — grid-stable, not an aliasing artifact.
- **Impact: none on any rendered output.** `pkill_volume_3d` is still wired
  into the interactive app's 3-D `P_k` volume view
  (`app/sensitivity.py:261,1034`, `fig_pkill_volume`), so the fringe-dominated
  behaviour this figure describes is exactly what that live view renders.
  This is a documentation cross-reference gap, not a wrong number.
- **Suggested correction (doc-fix, not a code change):** repoint
  `derivation.md` §4.7's citation from `_pkill-field.qmd` to
  `pkill_volume_3d`'s `z=0` slice / the app's 3-D volume view (or, if a
  notebook demonstration is wanted again, add the fraction print-out back
  into wherever the point-transform is next shown); cite this review's
  independent recheck (3.18%/1.05%, grid-stable 30–200) as the artifact
  that was previously missing.

**Note — `_change-log.qmd` 0.5.0/0.5.1 entries remain mutually consistent.**
The 0.5.0 entry this commit adds ("feeds the interactive 3-D `P_k` volume
view") stays true after the later 0.5.1 rewrite, since `pkill_volume_3d`
specifically retained that role while `pkill_field_3d` was repurposed for the
ground column integral — verified by reading both changelog rows together
against current `fragmentation.py` docstrings. No correction needed.

**Layering — PASS.** Every `.qmd` edit in this commit is prose only, except
the one code cell the (now-superseded) `_pkill-field.qmd` version added,
which computed `np.mean(lethal > 0.95)` — a display-layer threshold-fraction
diagnostic over already-computed `arty` output arrays, the same accepted
pattern used elsewhere in this notebook (e.g. the still-live `ring_fill`
helper in the current `_pkill-field.qmd`, already reviewed and passed in
`updates/target-height-intercept/review.md`). No physical constant, formula,
or quantity is computed inline anywhere in the diff; every formula/axis
convention named in the new prose (`A_ref=0.85`, eq. (23)/(1), `(±cosα,…)`)
was cross-checked directly against the corresponding `src/arty/` source and
matches.

**Note — Family A/B terminology.** The commit message's "Family A/B" labels
do not appear verbatim in any `.qmd`; the notebook instead uses "graded
per-hit pathway" / "Poisson binary-cut pathway" (`_pkill-field.qmd`'s
comparison table). Checked against `src/arty/zones.py`'s own internal
`_familyA_zone_massintegral`/`_four_zone_familyA_eval` naming: "Family A" in
code denotes exactly the graded ES-310 `P_k|hit` + `A_p` mass-integral
pathway the notebook calls "graded per-hit pathway" — consistent, just a
different label in reader-facing prose vs. internal code. No discrepancy; not
actionable.

### Checklist coverage (this delta only)

- Dimensional analysis / boundary cases / numerical stability: unchanged by
  this commit (prose + one diagnostic statistic only); re-verified nothing
  new was computed that needed these checks.
- Physical plausibility: fringe-dominated saturation claim independently
  reconfirmed with real numbers (3.18%/1.05%, grid-stable) — see Deferrable
  finding.
- Source attribution: one stale internal citation (Deferrable finding above);
  no external-source claims changed.
- Layering: PASS, no physics/computation/parameters leaked into any `.qmd`.
- Limitations: the axis-convention divergence is now correctly logged in both
  `_four-zone-3d.qmd` and `_limitations.qmd` §12 — no further limitation
  needed for that item. Log the §4.7 citation fix (see Suggested correction
  above) the next time `derivation.md` is touched; not urgent enough to
  warrant its own pass.
- Data-driven analysis: this review's own grid sweep (n_grid 30–200, both
  paths) supports the reconfirmed fraction; no other new quantitative claim
  in the diff required data support beyond what was already checked.
