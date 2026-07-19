# Review — field-builder performance refactor

**Verdict: PASS-with-limitations**

Scope: pure vectorisation of the field/volume/line/pkill builders in
`src/arty/zones.py` and `src/arty/fragmentation.py`. Contract claimed by
`derivation.md`: no physics/API change, numerical equivalence to the
pre-refactor per-cell code (worst-case max abs diff 1.44e-15).

## Verification performed

- Reran `experiment/_scratch/bench.py compare` against the pre-refactor
  `ref.npz` — reproduced the derivation's reported diffs exactly (worst
  `1.443e-15` on `four_zone_pkill_field`, all others ≤ 4.4e-16). Confirms the
  regression table in `derivation.md` §6 is not cherry-picked/stale.
- `uv run pytest -q`: 220 passed, 4 skipped. `ruff check`: clean.
- Independent edge-case sweep (not covered by `bench.py`, which only exercises
  one parameter set: 155mm M107 HE, AoF 30°, h_b=2m, δ=15°, STANDING) —
  compared the scalar reference path (`belt_column_breakpoints` +
  `integrate_column_density` + `lethal_density_four_zone_point`, all still
  present/unchanged) against the new `_pkill_columns_vec` across:
  grazing AoF (1°), steep AoF (89°), AoF exactly at (and 0.01° past) an active
  zone's spray half-angle (the `A→0` quadratic-degeneracy regime called out in
  memory as a known risk for this kind of code), a very narrow belt (δ=0.5°),
  h_b→0 (0.05 m), and PRONE/STANDING posture changes. Max diff across all
  cases: **2.33e-15** — same machine-epsilon regime as the reported benchmark,
  confirming the equivalence claim generalizes past the single tested
  configuration, including the near-coincident-breakpoint deviation
  `derivation.md` §3 discloses as the one non-bit-exact approximation.
- `build_mmin_table` (vectorised bisection) vs scalar `min_lethal_mass`:
  swept `V0 ∈ {50, 300, 500, 900, 1500, 1800, 2500, 4000}` m/s and `s` ranges
  including `s→0` and large `s`. `np.array_equal` true (0.0 diff) in every
  case — confirms the "freeze-on-early-stop" bit-identical bisection claim.
- Chunking is a pure performance knob: shrunk `_FAMILY_A_CHUNK` from
  2,000,000 to 137 on a 300×300 `four_zone_field` call (forces dozens of
  chunk boundaries) — 0.0 diff vs the default chunk size. Split/stitched a
  `_pkill_columns_vec` call across its own P-chunking boundary — 0.0 diff.
  No off-by-one or boundary-loss in either chunked loop.
- No `.qmd` file is touched by this diff at all (`git diff --name-only`:
  only `src/arty/zones.py`, `src/arty/fragmentation.py`, and the modeler's
  own memory file). Layering check is trivially satisfied for this pass —
  nothing to leak.

## Findings

**Deferrable — dropped defensive assert in the vectorised four-zone
density/pkill paths.** The scalar `lethal_density_four_zone_point`
(unchanged by this diff) asserts `s_grid[0] <= s <= s_grid[-1]` before its
`np.interp` call, specifically to turn np.interp's silent-clip behaviour into
a loud failure (this is a previously-logged footgun — see reviewer memory
`lethal_density_field_implementation.md`). The new vectorised
`_four_zone_density_layer_vec` (`zones.py`, new) and the per-zone loop inside
`_pkill_columns_vec` (`fragmentation.py`, new) call
`np.interp(s_safe, spec["s_grid"], spec["mmin"])` directly with no equivalent
bounds check.

- **Impact today: none.** `slant_range_grid` is sized to cover the full query
  range by construction for every current caller (verified: same `s_grid`
  construction feeds both the scalar and vectorised paths), so the guard is
  currently unreachable in both the old and new code. Confirmed via the edge
  sweep above — no clipping observed anywhere.
- **Why it's not Blocking:** no observable output changes; the removed check
  only protects against a *future* caller/refactor that violates grid
  coverage, which is exactly the scenario the assert was added to catch
  loudly instead of silently.
- **Suggested limitation entry / fix:** either re-add a vectorised bounds
  check (e.g. `assert s_safe.min() >= s_grid[0] and s_safe.max() <= s_grid[-1]`,
  gated so it's cheap) to the two new functions for parity with the scalar
  path, or log in `derivation.md`/`_limitations.qmd`: "the vectorised
  four-zone density/pkill paths rely on caller-guaranteed `s_grid` coverage
  (via `slant_range_grid`) with no runtime check; the scalar reference
  functions still assert this and remain the place to catch a coverage
  regression via the regression harness."

**Note — stale comments describing a rejected design.** In `zones.py`, the
module comment above `_ZONE_NAMES` (~line 413) and the docstring of
`_four_zone_familyA_eval` (~line 468) both say the Family-A mass integral is
"tabulated once per zone on a dense 1-D s-grid and interpolated per cell."
That's the interpolation approach `derivation.md` §1 explicitly says was
tried and **reverted** (residual ~1e-3 error at 4000 nodes); the shipped
`_familyA_zone_massintegral` evaluates the integral *exactly* on each cell's
real slant range (chunked only for memory), not via interpolation. The
comment contradicts both `derivation.md`'s own account and the function it
describes. No output impact — code is correct, comment is wrong — but it
could mislead a future maintainer into assuming an interpolation-error budget
exists where there is none. Suggested fix: reword to match `derivation.md`
§1 ("exact vectorised in-belt evaluation, chunked for memory").

**Note — stale docstring references / dead code.** `four_zone_pkill_field`'s
docstring (`zones.py` ~1005-1008) and `pkill_field_3d`'s docstring
(`fragmentation.py` ~1129-1130) still cite `belt_column_breakpoints` /
`integrate_column_density` as the mechanism; both now route through
`_pkill_columns_vec` / `_belt_breakpoints_vec`. `belt_column_breakpoints`,
`integrate_column_density`, and `_active_zone_cos_theta` (zones.py) are left
in the tree, correct, but have no remaining production caller (confirmed via
repo-wide grep — they're only used by this review's own scratch scripts).
No output impact; suggest updating the docstrings to name the vectorised
functions, or noting explicitly that the scalar functions are intentionally
kept as the reference implementation for `bench.py`.

**Note — duplicated constant.** `_FAMILY_A_CHUNK = 2_000_000` is defined
separately in both `zones.py` and `fragmentation.py` with a comment
acknowledging the duplication ("see zones.\_FAMILY_A_CHUNK") rather than a
shared import. Cosmetic only.

## Limitations to log

- Vectorised four-zone `ρ_L`/`P_k` paths (`_four_zone_density_layer_vec`,
  `_pkill_columns_vec`) depend on caller-supplied `s_grid`/`mmin` tables
  covering every queried slant range; unlike the scalar reference functions,
  they do not assert this at runtime (removed for vectorisation) and would
  silently clip via `np.interp` if it were ever violated. Currently
  unreachable given how `slant_range_grid` sizes every grid, but any future
  change to grid construction should re-verify coverage or reinstate a
  vectorised bounds check.
- The belt-breakpoint vectoriser (`_belt_breakpoints_vec`) does not
  deduplicate near-coincident roots the way the scalar
  `belt_column_breakpoints` does (merges within 1e-12); this leaves an
  O(1e-12)-wide extra integration segment on affected columns. Measured
  effect (benchmark case + this review's edge sweep) stays at
  1e-16–1e-15 on `P_k`, i.e. float-reassociation noise, not a real deviation.
