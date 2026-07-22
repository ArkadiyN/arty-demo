# Review — Legacy single-zone field forward shell-axis fix (derivation pass)

**Scope:** `scoping.md` + `derivation.md` only. No `src/arty/` change has been made
yet (derivation-only gate) — `fragmentation.py` still ships the backward axis at
all four flagged spots (lines 940, 959, 1024, 1036; `_shell_axis` still defined
at 381), confirmed by direct read.

## Verdict: **PASS-with-limitations**

No Blocking findings. The physics claim (backward axis is a genuine x-mirror
bug, forward axis is correct, fix is axis-only) is sound and I independently
reverified every quantitative claim in derivation.md §2/§3 with dense sweeps
(not just re-reading the modeler's numbers — see below). Two **Deferrable**
completeness gaps in the "test & documentation impact" audit (derivation §4,
scoping §3) must be folded into the implementation pass's task list; neither
is a physics defect and neither changes any rendered demo output.

---

## Independent verification performed

All checks below were run against the **live, unmodified** `src/arty/fragmentation.py`
(for the shipped-backward comparison) plus a from-scratch reimplementation of
the derivation's literal A1–A4 forward-axis prescription (for the fixed side),
built and run via `uv run python` in `experiment/_scratch/` (deleted after use,
per harness convention). This goes beyond the derivation's own worked table
(one config, six spot rows) per the project's standing "dense sweep, not a
lucky point" bar for belt-gated kernels.

1. **Mirror identity, reference config (h_b=8, AoF=40°, δ=30°), 4000 random
   (x,y) points, max_radius=40 m:**
   `max|N_fwd(x,y) − N_bwd(−x,y)| = 0.0` exactly (both directions). Confirms
   derivation §3's "Exact mirror" row is not a rounding coincidence at a
   handful of points but holds over a dense random sample.
2. **x=0 cross-range slice (boundary case), 500 points:**
   `max|N_fwd − N_bwd| = 8.9e-16` (machine epsilon). `r50_cross` (read
   exclusively at x=0 by `compute_frag_field_3d`) is therefore unaffected —
   confirms derivation §2's reduction claim and scoping §1's "bounded blast
   radius" argument.
3. **AoF=90° (grazing/degenerate boundary), 4000 points:**
   `max|N_fwd − N_bwd| = 1.3e-15`. Confirms the axis is genuinely sign-blind
   there (cosα=0 zeroes the only differing term), exactly as claimed.
4. **vec ≡ point, off-axis (AoF=40°, δ=30°, x≠0), 500 points:** hand-built both
   the A1–A2 (vec) and A3–A4 (point) fixes per the derivation's literal
   formulas (not copy-pasted from one path) and compared:
   `max|N_vec − N_point| = 8.9e-16`. The claimed vec≡point equivalence holds
   under the corrected convention, off the x=0/AoF=90° planes where it would
   be easy to fake.
5. **Existing off-axis test probe points
   (`test_offaxis_single_zone_axis_sign`, AoF=60°, δ=15°, the 5 pinned
   points):** confirmed all 5 remain **lit** under the forward fix, with
   magnitudes matching a from-scratch forward brute-force reference to
   `~1e-16` relative — i.e., derivation §4's claim "the same points work,
   only the reference cosT sign flips" is exactly right, not approximately.
   Also directly confirmed the **currently shipped** (backward) kernel
   returns `N=0` at all 5 of these points — a live, reproducible instance of
   the bug scoping §0 describes, not just an algebraic argument.
6. **Broad numerical-stability sweep:** `h_b ∈ {0, 0.5, 2, 8, 20}` ×
   `AoF ∈ {0°, 1°, 30°, 45°, 60°, 89°, 90°}` × `δ ∈ {0.5°, 15°, 30°, 44°}`
   (140 configs), 4000 random (x,y) points each, forward-fixed kernel: no
   NaN, no negative `N` anywhere, including the grazing-angle case
   `AoF=0.5°` and the near-vertical `δ=44°` (app's slider max is 30°, so this
   is margin beyond the in-scope range). No new instability introduced by the
   axis flip.
7. **Two pre-existing, unrelated regression tests** in `test_fragmentation.py`
   (`test_3d_burst_origin_zero_hb_guard`, `test_3d_shell_axis_alignment_guard`)
   were independently re-evaluated under the forward-fixed kernel and both
   still assert correctly (both guard conditions — `s≈0` and `sinΘ=0` at
   exact axis alignment — are symmetric in `cosΘ → −cosΘ`, i.e. axis-sign
   blind, since `sinΘ` only depends on `cosΘ²`). Not claimed by the
   derivation, but good incremental confidence nothing outside the flagged
   spots regresses.

Dimensional check: eq. (1) `cosΘ = (x cosα − ζ sinα)/s` is a ratio of
[m]/[m] → dimensionless, consistent with its use as a direction cosine
throughout. No units issue.

---

## Findings

### Finding 1 (Deferrable) — `_shell_axis` deletion audit missed a second call site

`scoping.md` §1 states `_shell_axis` "has exactly **one** call site — L959
above. After this fix it has **zero** callers," and Option A instructs
"Delete the now-dead `_shell_axis` constructor (L381) to prevent future
misuse." This audit only grepped `fragmentation.py`. A second, real call site
exists in the test suite:

```
tests/test_familyA_false_safe_zone.py:34:    _shell_axis,          # import
tests/test_familyA_false_safe_zone.py:91:    e_axis = _shell_axis(alpha_rad)   # usage, in _ref_z0_single()
```

`_ref_z0_single` is the reference helper for `test_feet_lit_reduction`
(the bit-exact reduction-identity test). **Impact if unaddressed:** if the
implementation pass follows scoping's literal instruction and deletes
`_shell_axis` without also patching this import, the whole
`test_familyA_false_safe_zone.py` module fails to **collect**
(`ImportError`) — not just the one test scoping/derivation §3/§4 flagged for
rewrite, but all ~10 tests in that file (dense-ring sweep, four-zone checks,
prone/standing monotonicity, the reduction identity itself), none of which
exercise the axis fix. This is a loud, CI-visible collection failure, not a
silent physics error, so it does not rise to Blocking — but it is a concrete
gap in the derivation's own completeness claim.

**Numerically risk-free to fix:** `test_feet_lit_reduction`'s only config is
`alpha = np.radians(90.0)` (line 176; `_ref_z0_single` is called from no
other test). At AoF=90°, `_shell_axis(90°) = (0,0,−1) = _forward_shell_axis(90°)`
exactly (`cos 90° = 0` zeroes the only differing component), so swapping the
import/usage there is a pure rename with zero numeric change at that test's
config — verified by inspection of both function bodies, not just asserted.

**Suggested correction (do not apply):** add one line to derivation §4 (or
scoping §3): "Also swap the `_shell_axis` import (L34) and `_ref_z0_single`'s
use (L91) in `tests/test_familyA_false_safe_zone.py` to
`_forward_shell_axis` before/while deleting the dead constructor — inert at
that test's AoF=90° config." More generally, brief the implementation pass to
`grep -rn "_shell_axis(" .` across the **whole repo** before deleting, not
just the file being edited (the belt-axis-convention-pitfall memory's
"re-grep for sibling phrasing" habit, generalized past a single file).

### Finding 2 (Deferrable) — `_expected_kills_3d_point` has no regression coverage, so the derivation's vec≡point claim is unenforced

Repo-wide grep confirms `_expected_kills_3d_point` (the function A3/A4 patch)
is called **nowhere** — not by any test, and not by
`compute_frag_field_3d` (the sole production/app entry point), which calls
only `_expected_kills_3d_vec`. `test_fragmentation.py`'s own comment ("§
`_expected_kills_3d_point` guard branches (via compute_frag_field_3d)",
line 500) is itself misleading — those two tests exercise the **vec** path
only. This is not new to this aspect, but it directly affects this
derivation's central §2 claim ("vec ≡ point... carries over unchanged").

**Impact if unaddressed:** zero effect on any rendered demo output today
(point path is unreachable from the app). But since nothing calls it, a
mistake in A3 or A4 alone (e.g. fixing the `x_axis` sign at line 940 but
missing the `_shell_axis` → `_forward_shell_axis` swap at line 959, or vice
versa) would leave `_expected_kills_3d_point` silently inconsistent with
`_expected_kills_3d_vec` — exactly falsifying derivation §2's acceptance
claim — with no test to catch it, now or on any future edit to this file.
I independently reimplemented both halves (A1–A2 and A3–A4) from the
derivation's literal formulas and confirmed they agree to ~9e-16 off-axis
(see verification item 4 above), so the derivation's claim is correct as
specified today — the gap is that nothing keeps it correct going forward.

**Suggested correction (do not apply):** implementation pass should add one
direct unit test calling both `_expected_kills_3d_point` and
`_expected_kills_3d_vec` at a handful of matched off-axis points
(AoF≠90°, x≠0 — the derivation's own §4 probe points work) and asserting
agreement to float tolerance. Cheap, and closes the only currently-unverified
claim in this derivation.

---

## Checklist coverage

- **Dimensional analysis:** eq. (1) is dimensionless; consistent. No new
  constants introduced (pure sign/axis correction) — parameter-bounds check
  N/A.
- **Boundary cases:** x=0 (machine-zero diff, item 2), AoF=90° (machine-zero
  diff, item 3), grazing AoF=0.5° (no NaN/negative, item 6), zero-range /
  s→0 guard (untouched, confirmed via item 7) all checked and pass.
- **Numerical stability:** 140-config broad sweep, no NaN/negative (item 6);
  stable-quadratic-root machinery (`_stable_quadratic_roots`,
  `_belt_column_zrep_vec`'s coin-flip-free `sinΘ` substitution from the prior
  Family-A pass) is untouched by this fix — only the `x_axis` argument value
  and the two `cosΘ` sign literals change, confirmed by direct code read.
- **Physical plausibility:** not re-litigated here per scoping §0 ("do not
  re-derive") — the forward-axis conclusion was already established by the
  correctness-classification pass this aspect implements.
- **Source attribution:** internal consistency fix against already-cited
  in-repo derivations (`lethal-fragment-density-field/derivation.md` §5.4,
  `target-height-intercept/derivation.md`); no new external literature
  needed, correctly identified as no-`@librarian` in scoping §4.
- **Layering:** no `.qmd`/`app/` file touched in this pass; confirmed
  `app/sensitivity.py`'s "Four-zone − Single-zone" diff (`diff_pk`, line 826)
  is a plain subtraction of two `arty` outputs — no physics computed in the
  app, so the diff map will pick up the fix automatically with no app change
  needed, as scoping claims.
- **Limitations:** `_limitations.qmd` still carries the stale
  "backward shell-axis convention... deliberately not reconciled" bullet
  (lines 193–206) — expected, since the doc-update is explicitly deferred to
  the implementation pass (scoping §3/§5, derivation §5). Confirmed the
  unrelated `sinΘ`-parity bullet (lines 174–187) correctly stays untouched —
  it is genuinely independent of the axis.
- **Data-driven analysis:** derivation §3's worked-check table is
  reproduced and *extended* by the dense sweeps above; all rows confirmed,
  not merely re-read.

## What the implementation-pass review (next pass) should re-check

- Both Deferrable items above are resolved (test-file `_shell_axis` swap;
  optionally the new point-vs-vec unit test).
- The four A1–A4 spots are flipped **together** (a partial flip is worse than
  no flip — derivation §1 already flags this; confirm on the actual diff).
- `_limitations.qmd` #12 and the modeler memory entry are updated per
  scoping §3.
- Full test suite green, plus a fresh look at whether `test_feet_lit_reduction`
  and the other AoF=90° tests in `test_familyA_false_safe_zone.py` still pass
  bit-for-bit (they should, per item 3/7 above, but confirm against the real
  diff, not my standalone reimplementation).
