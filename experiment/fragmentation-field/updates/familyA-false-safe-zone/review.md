# Review — Family-A false safe zone (graded ground P(kill) heatmaps)

**Verdict: FAIL**

## Scope

`scoping.md` (Option 2 selected: relocate the Family-A belt gate + ray
geometry to the illuminated column, keep `A_p(γ)·pk_given_hit(E)` intact) and
`derivation.md` (eq. 2/3, fork resolutions §3, reduction identity §4,
geometry checks §5). No `src/arty/` code exists yet — this gates whether the
derivation is sound enough to implement. Verified against the **current**
`src/arty/fragmentation.py` (`_expected_kills_3d_point/_vec`, `_shell_axis`,
`_forward_shell_axis`, `belt_column_breakpoints`, `_stable_quadratic_roots`)
and `src/arty/zones.py` (`_four_zone_familyA_eval`), and cross-checked against
the already-reviewed `updates/target-height-intercept/derivation.md` §6.3.

## Verification performed

`numpy`/`arty` **are** available in this repo's `uv` environment (confirmed:
`uv run python -c "import numpy"` → 2.4.6) — contrary to derivation §7 (A5)'s
"numpy is unavailable in the derivation environment." Since the belt-edge
machinery this aspect reuses (`belt_column_breakpoints`, `presented_area`,
`pk_given_hit`, `_shell_axis`/`_forward_shell_axis`) already exists and is
callable today, I reimplemented eq. (3) literally as specified — gate on
`belt_column_breakpoints(...)` non-empty, take `z_rep = z_lo` (lower edge of
the lowest active sub-interval, membership tested at the sub-interval
midpoint per §3.1), then evaluate the **existing** per-point kernel
(`_expected_kills_3d_point`'s body) at `z_rep` in place of `z=0` — and ran it
against the derivation's own §5.1 worked table (AoF=90°, `h_b=2.0`, `δ=15°`,
standing `h=1.7`, TNT/WW2-shell defaults). Script and raw output are in this
session's scratchpad; the essential result is reproduced under Findings.

Also independently confirmed:

- **Exact-reduction identity (§4).** For feet-lit cells (`r ≥ h_b/tanδ ≈
  7.46 m`), `N_new == N_old` to the bit (`equal=True` at `r=7.5,8,10,15,20`).
  Matches the derivation's claim.
- **Standing ≥ prone monotonicity and non-decreasing-in-`h`** (spot-checked
  `h ∈ {0.3,…,2.5}` at several `r`): holds in every sampled case.
- **The `belt_column_breakpoints`/Family-B §6.3 citation is not stale** — the
  cited segment table (`r=1.2→1.678`, `1.5→1.598`, …) still exists verbatim
  in `target-height-intercept/derivation.md` §6.3 and matches this
  derivation's §5.1 table exactly (cross-checked function output vs. both
  documents' printed numbers, not just algebra).
- **A3's axis-sign concern is real, not academic.** At AoF `=60°`,
  `x∈{-6,…,-1}`, calling `belt_column_breakpoints` with `+x` (the natural,
  un-flipped call) instead of the derivation-mandated `-x` returns a
  **materially different, spurious interior root** at every tested point
  (e.g. `x=-3,y=1.0`: `-x` call → `[0.0, 1.7]` (no crossing); `+x` call →
  `[0.0, 1.24, 1.7]` (fabricated crossing)) — confirms this is a real,
  easy-to-get-wrong implementation trap, not a hypothetical.

## Findings

**Blocking — the boxed fix (eq. 3, `z_rep = z_lo`) silently fails to close
the defect on roughly half of its own worked example, due to a
floating-point coin-flip evaluating the kernel exactly at the belt-edge
root.** `derivation.md` §3.1 claims: *"The kernel is then evaluated at
`z_lo`; because we have already established membership, no gate is
re-applied there, so evaluating on the belt edge is safe."* This is false as
specified. `z_lo` is, by construction, an exact root of the same inequality
(`|cosΘ − cosθ^z| ≤ sinδ`) that eq. (1)'s kernel re-tests internally
(`_expected_kills_3d_point`/`_vec` and `_four_zone_familyA_eval` all embed
their own per-point gate check — nothing in eq. (3) or §8's implementation
notes says to bypass it). Re-evaluating `cosΘ` from scratch at `z = z_lo`
therefore reproduces the boundary value to ~1e-16, and whether that lands
inside or outside the strict `≤` gate is pure rounding-direction luck:

```
x=1.20  cosΘ(z_lo) − sinδ = +1.11e-16   gate FAILS → kernel returns 0
x=1.50  cosΘ(z_lo) − sinδ = +5.55e-17   gate FAILS → kernel returns 0
x=2.00  cosΘ(z_lo) − sinδ = +1.11e-16   gate FAILS → kernel returns 0
x=3.00  cosΘ(z_lo) − sinδ = +5.55e-17   gate FAILS → kernel returns 0
x=5.00  cosΘ(z_lo) − sinδ = −5.55e-17   gate passes → nonzero
x=7.00  cosΘ(z_lo) − sinδ =  0.00e+00   gate passes → nonzero
```

Running the derivation's own §5.1 checklist config (standing, AoF=90°,
`h_b=2`) through the literal eq. (3) recipe: **`r = 1.2, 1.5, 2.0, 3.0 m` —
4 of the 6 tabulated points inside the claimed-fixed ring `[1.12, 7.46) m` —
return `N = 0`, i.e. `P_k = 0`, exactly reproducing the false-safe defect
this aspect exists to remove.** Only `r = 1.12` (huge `N≈587`, a genuine
near-burst near-certain-kill value, not a bug) and `r = 5.0, 7.0` (nonzero by
luck of the rounding direction) read correctly. This directly falsifies
derivation §5.1's own "✓" conclusion and the acceptance criterion in
`scoping.md` §4.3 — under a literal implementation of what's specified, the
fix does not reliably close the ring.

This is the same failure family the sibling aspect already solved and
recorded: `integrate_column_density`'s docstring (and
`target-height-intercept/derivation.md` §5.2/§5.4) explicitly requires
**strictly-interior** sample points for exactly this reason ("evaluating
ρ_L exactly at a breakpoint is a floating-point coin flip... an
endpoint-weighted rule loses ρ_L·Δz/2 intermittently"). This derivation
correctly applies that lesson to the **sub-interval membership test**
(§3.1: "tested at its midpoint, never an endpoint") but then reintroduces
the identical anti-pattern one line later by picking the **representative
evaluation point itself** to be the endpoint/root, not an interior point.

- **Confirmed not a one-off artifact of my reimplementation:** the
  sign/magnitude of `cosΘ(z_lo) − sinδ` alternates with no discernible
  pattern across `x` (see table above) — consistent with pure rounding
  noise, not a systematic offset that could be patched by adjusting the gate
  direction (`<` vs `≤`).
- **A concrete fix exists and is cheap** (not applying it — flagging for the
  next derivation/implementation pass): nudging `z_rep` a small interior
  epsilon off the root before evaluating `s, γ, cosΘ` resolves all 6 test
  points (verified: `z_rep = z_lo + 1e-9·(z_hi_segment − z_lo)` → gate passes
  at every one of `x = 1.2, 1.5, 2.0, 3.0, 5.0, 7.0`). An equally valid
  alternative is to use the **analytically known** boundary value
  (`cosΘ = cosθ^z ± sinδ`, whichever root was solved) directly instead of
  recomputing `cosΘ` numerically from `(x,y,z_rep)` — since that value is
  already exact by construction, no rounding is introduced. Either requires
  the fix to **not** call the "unchanged" per-point kernels verbatim with a
  substituted height; the gate/`cosΘ` handling at `z_rep` needs bespoke
  treatment, contradicting the "kernel is unchanged" framing in §2 unless
  that framing is qualified in the derivation.
- **Why this wasn't caught pre-review:** the derivation states magnitudes
  were "not executed this pass" because numpy was reported unavailable
  (§7 A5). That premise is incorrect for this repo (`uv run python` has
  numpy 2.4.6, and every function this fix reuses — `belt_column_breakpoints`,
  `presented_area`, `pk_given_hit`, `_shell_axis` — already exists and is
  directly callable). A ten-line scratch script exercising eq. (3) against
  the existing machinery, mirroring the sibling aspect's own §5.4 executed
  convergence sweep, would have surfaced this immediately.
- **Required before this can PASS:** (1) correct §3.1's "evaluating on the
  belt edge is safe" claim and specify the concrete numerically-safe
  evaluation rule (nudge or analytic-K substitution); (2) replace the
  planned src/ test (§7 A5's single ring-max assertion,
  `P_k[ring].max()>0.5`) with a **dense sweep across the whole target ring**
  (e.g. every `r` on a fine grid in `[1.13, 7.4]` at AoF=90°, standing) that
  would have failed on the current wording — a single max-over-ring
  assertion can pass even when half the ring is silently still zero, since
  `max()` only needs one lucky point (`r=1.12` or `r=7.0` would already
  satisfy it, as shown above).
- **Impact estimate:** high. This is not a rare corner case — it is the
  generic behavior of the primary mechanism (representative height chosen
  to *be* a belt-edge root) for the majority of newly-lit cells in the
  target ring, at the exact config the derivation itself uses as its
  headline defect-removal demonstration.

**Deferrable — A3's axis-sign correction is correctly identified but not
covered by a required test, and the one worked example (AoF=90°) structurally
cannot exercise it.** §7 (A3) correctly derives that the single-zone legacy
kernel's backward axis `(−cosα,0,−sinα)` requires calling
`belt_column_breakpoints` with `-x` (equivalent to the forward-axis formula
evaluated at `-x`), and correctly notes `B=0` at AoF=90° so the bug is
invisible there — but §5's checks and §7 (A5)'s required test list are both
confined to AoF=90°, the one config where getting the sign wrong is
consequence-free. This project has hit this exact class of bug before
(single-/four-zone axis convention mismatch off the `x=0` plane, previously
found via an off-axis hand-check, and later fixed for the ρ_L/Family-B path
via the shared `_forward_shell_axis` — the single-zone Family-A kernel is the
one remaining holdout still on the backward axis). Independently confirmed
in this review (see Verification) that calling with the wrong sign at
AoF=60°, `x<0` fabricates spurious breakpoints, not just a sign flip on an
existing one — i.e. a wrong-sign implementation would not merely mis-locate
`z_rep`, it could gate cells on/off incorrectly.
**Impact estimate:** medium — silent for every AoF=90° test but wrong for
essentially all other angles, i.e. most of the app's `angle_of_fall` slider
range. **Suggested correction:** add an explicit required test at
`α≠90°, x≠0` (e.g. AoF=60°, comparing the relocated single-zone kernel
against an independent, non-`belt_column_breakpoints`-based per-point
reference) to §7/§8's implementation checklist.

**Deferrable — §3.1 item 2's "conservative flux" justification silently
assumes `h_b > h` (burst above the target's head), which is not guaranteed
by the app's parameter range.** The app's `h_b` slider spans `[0, 20]` m
(`app/sensitivity.py:104`), so `h_b ≤ h_target` (burst at or below head
height) is reachable. In that regime `s(z) = √(r²+(h_b−z)²)` is *not*
maximized at the lowest lit height (it is minimized near `z=h_b`, which can
sit inside the column), so `z_lo` need not be the "least-aggressive"
representative point, weakening the "partially offsetting the
lumped-silhouette over-count" argument used to support §7 (A1)'s
"conservative-high, safe direction" framing. This does not threaten
correctness of the core fix (the gate/reduction logic in §2/§4 is
unconditional on the `h_b` vs. `h` ordering), only the completeness of the
error-direction narrative for A1. **Impact estimate:** low — affects
limitation wording accuracy, not output values. **Suggested correction:**
qualify item 2 explicitly as "for `h_b` above the column" and note that A1's
bias direction is unverified (not necessarily unsafe, just unproven) for low
airburst / near-ground-level configurations.

**Note — §3.1's "`sinΘ(z_lo)=cosδ>0`" states an equality where only an
inequality is guaranteed.** `sinΘ(z_rep) ≥ cosδ` follows directly from the
gate `|cosΘ|≤sinδ` holding anywhere inside the segment (including at `z_rep`
when `z_rep` is the column bound `z=0` and *not* a genuine belt-edge root —
the feet-lit reduction case). Equality (`=cosδ`) only holds when `z_rep` is
itself exactly a belt-edge crossing. The numerical-stability conclusion
(division by `sinΘ` is safe) is correct either way; only the stated formula
is imprecise. **Suggested correction:** reword to `sinΘ(z_rep) ≥ cosδ > 0`.

**Note — the symbol `z_lo` is overloaded.** `belt_column_breakpoints`'s
signature uses `z_lo` for the column's fixed lower bound (`0`); §3.1 reuses
the same symbol for fork-1's chosen representative height ("the lower edge
of the lowest belt-active sub-interval"), which is a different quantity that
only coincides with the column bound in the feet-lit reduction case.
**Suggested correction:** rename the fork-1 quantity (it is already called
`z_rep` in the boxed eq. 3 — use that consistently in §3.1 too) to avoid
confusion when the src/ pass reads this against the function signature.

## Limitations to log (once the Blocking finding is resolved)

- A1 (lumped-silhouette over-count, conservative-high) — log as scoped, with
  the h_b>h qualifier from the Deferrable finding above.
- A2 (representative-height far/mid-field approximation) — log as scoped.
- A4 (obliquity/Poisson caveats inherited unchanged) — log as scoped.

## Checklist coverage

- Dimensional analysis: PASS — eq. (3) is eq. (1) evaluated at a different
  height; units unchanged (`A_p[m²]·J[count]/(s²[m²]·δ[-]·g[-]) = [count]`).
- Boundary cases: zero range / inner-edge honesty (§5.2) verified correct
  (no interior root ⇒ `N=0`, confirmed numerically); grazing angle inherited
  unchanged from already-reviewed `_stable_quadratic_roots`; **maximum range
  / general far-field not independently re-checked this pass (low risk, no
  new geometry there)**. See Blocking finding for the boundary case that
  *is* broken (evaluation exactly at the belt-edge root).
- Parameter ranges: no new constants introduced; posture/δ/`h_b`/AoF ranges
  are pre-existing and previously accepted.
- Numerical stability: **FAIL** — see Blocking finding (fp coin-flip at
  `z_rep = z_lo`). The `1/sinΘ` guard itself (single-zone) is fine once a
  numerically-safe `z_rep` is used.
- Physical plausibility: near-burst magnitudes (`N≈587` at `s≈1.16 m`) are
  sensible (near-certain kill close to burst); standing/prone ordering and
  height-monotonicity hold; the ring geometry (`r=1.12, 3.73, 7.46 m` for
  onset/chest/feet) is dimensionally and physically consistent WW2-HE-shell
  fragmentation behavior at `h_b=2 m, δ=15°`.
- Source attribution: no new literature required or cited; unchanged from
  prior reviews (ES-310 `pk_given_hit`, NATO `presented_area` convention,
  both already flagged/accepted).
- Layering: N/A this pass — `scoping.md`/`derivation.md` contain no code;
  correctly deferred to the future src/ and notebook passes.
- Data-driven analysis: **weak** — the derivation's §5 checks are hand
  arithmetic on a single parametric family, not executed against the
  already-available `arty` code, despite that code being callable in this
  environment; this is exactly what let the Blocking finding through. The
  sibling aspect's derivation (§5.4) set a stronger precedent (executed
  convergence sweep) that this pass should match.

## Suggested next steps (not applied)

1. Fix §3.1's evaluation rule for `z_rep` (nudge-inward or analytic-K
   substitution) and rerun the §5.1 worked table through the corrected rule
   to confirm all six points, and a dense sweep, now read `N>0`.
2. Expand the required src/ test list (§7 A5, §8) to a dense ring sweep
   (not a single max-over-ring point) and an off-axis (`α≠90°, x≠0`)
   single-zone regression test for A3.
3. Qualify §3.1 item 2 / §7 A1's "conservative-high" claim to the `h_b>h`
   regime, or explicitly extend the analysis to `h_b≤h`.
4. Minor: fix the `sinΘ(z_lo)=cosδ` equality→inequality wording and the
   `z_lo` symbol overload.

______________________________________________________________________

## Re-review (2026-07-20, revised `derivation.md`)

**Verdict: PASS**

### Scope of this pass

`derivation.md` revised in place (§3.1 "revision 1", §5 re-executed, §7/§8
updated); `scoping.md` unchanged (confirmed by re-read — no re-litigation
needed, Option 2 selection and scope boundary still hold). No `src/arty/`
code exists yet (still a derivation-only gate — confirmed via `git status`:
only `experiment/fragmentation-field/updates/familyA-false-safe-zone/` and
agent-memory files are touched in this worktree).

### Independent re-verification performed

Per the prior review's own precedent (and this repo's
`familyA_false_safe_zone_derivation_fail` / `piecewise_quadrature_boundary_evaluation`
memory guidance not to trust the modeler's account), I did **not** re-read
the derivation's numbers as given — I reimplemented eq. (3)'s revision-1
rule from scratch against the live `src/arty/fragmentation.py` /
`src/arty/zones.py` code (`belt_column_breakpoints`, `_shell_axis`,
`_forward_shell_axis`, `presented_area`, `pk_given_hit`,
`_expected_kills_3d_point`, `_familyA_zone_massintegral`,
`_four_zone_familyA_eval`, `compute_shell_zones`) via `uv run python`
(numpy 2.4.6), and reran every quantitative claim in derivation §5
independently. Script: this session's scratchpad
(`verify_familyA_fix.py`). Results, compared against the derivation's
printed numbers:

| Check | Derivation claims | Independent result | Match |
| --- | --- | --- | --- |
| §5.0 worked table, naive rule (recompute `cosΘ`, re-gate at `z_rep`) | `N=0` at `r=1.2,1.5,2.0,3.0`; nonzero at `r=5.0,7.0` (luck) | identical: `N=0.0000` at `r=1.2,1.5,2.0,3.0`; `N=27.81,13.82` at `r=5.0,7.0` | exact |
| §5.0 worked table, fixed rule (gate bypass + analytic-`K` `sinΘ`) | `510.7, 324.1, 181.4, 79.3, 27.8, 13.8` | `510.66, 324.14, 181.35, 79.33, 27.81, 13.82` | exact (to printed precision) |
| §5.0 dense sweep `r∈[1.13,7.45)` step 0.02 (316 cells) | naive zeros `54/316`; fixed zeros `0/316`; `min N=12.1 ⇒ min P_k=0.999995` | naive zeros `54/316`; fixed zeros `0/316`; `min N=12.1412 ⇒ min P_k=0.999995` | exact |
| §5.4 reduction identity, feet-lit `r=7.5,8,12,20` | `N_new==N_old` bit-exact | `equal=True` at all four `r` (`N_old`/`N_new` identical to 10 decimal places) | exact |
| §5.4 four-zone relocated, `r=2,3` (old `z=0` reads 0) | `N=182.7, 79.5` | `N=182.666, 79.451` | matches (printed precision) |
| §5.5 off-axis axis-sign trap, AoF=60°, `x∈{-3,-5}` | `-x`→`[0,1.7]` (no crossing) vs `+x`→ fabricated interior root at `1.24`/`0.667` | identical breakpoints reproduced exactly | exact |
| §5.3 standing/prone, `r=2,4,6,6.4` | `Pk(stand)=1.000/1.000/1.000`, `Pk(prone)=0.000/0.000/0.000`, `Pk(prone@6.4)=0.999` | `1.0/1.0/1.0`, `0.0/0.0/0.0`, `0.999331` | exact |
| §5.1 onset/chest/feet radii (`1.12, 3.73, 7.46` m) | derived from `(h_b-h)/tanδ` etc. | recomputed algebraically: `1.1196, 3.732, 7.464` | exact |

Every number in derivation §5 that I attempted to reproduce, reproduced —
including the specific counter-example the prior review used to fail this
derivation (4/6 worked points, 54/316 sweep cells zeroed by the naive
recipe). This is not a re-statement of the modeler's account; it is an
independent reimplementation exercising the same live functions, built
without reading the modeler's script.

### Blocking finding — resolved, verified independently

The original Blocking finding (representative height `z_rep` is an exact
root of the kernel's own belt gate ⇒ fp coin-flip ⇒ ~half the ring silently
reads `N=0`) is fixed by revision 1's rule: **bypass the kernel's internal
belt gate at `z_rep`** (membership is already decided by
`belt_column_breakpoints`), and for the single-zone `1/sinΘ` magnitude,
**substitute the analytically-known boundary value**
`sinΘ(z_rep)=√(1-(cosθ^z±sinδ)²)` (`=cosδ` for the equatorial belt) instead
of recomputing `cosΘ` from `(x,y,z_rep)`. This is algebraically sound (the
boundary `cosΘ` value depends only on `cosθ^z` and `δ`, not on `(x,y)`, so
the substitution is exact by construction, not an approximation) and I
confirmed it numerically eliminates every zero on the dense 316-cell sweep
(`0/316`, vs. `54/316` under the naive recipe) — satisfying the acceptance
bar this project's own memory sets for this failure class (a dense sweep,
not a lucky spot-check or a single `max()`-over-ring assertion). The
four-zone path is coin-flip-free by construction once the gate is bypassed
(its magnitude uses fixed `1/sinθ^z`, never `cosΘ`) — verified: relocated
four-zone reads `N=182.7, 79.5` at `r=2,3` where the old `z=0` path read `0`.

### Deferrable findings — both addressed

- **A3 off-axis coverage.** §5.5 now executes an AoF=60°, `x<0` off-axis
  check (independently reproduced above) demonstrating the wrong-sign call
  fabricates a spurious interior breakpoint, not a hypothetical concern.
  §7 A5 and §8 now explicitly require an off-axis (`AoF≠90°, x≠0`)
  single-zone regression test "against an independent per-point reference"
  in the src/ pass — matching the suggested correction. Not yet an
  implemented test (expected — still derivation-only), but now a named,
  required item rather than absent.
- **`h_b>h` qualifier on the "conservative flux" claim.** §3.1 item 2 now
  explicitly states the ordering "does not hold for `h_b≤h`... reachable on
  the app's `h_b∈[0,20]` slider" and flags the A1 bias-direction narrative
  as unproven (not unsafe, just unproven) in that regime — matching the
  suggested correction. Algebraically checked: for `h_b>h`, `s(z)=√(r²+(h_b-z)²)`
  is monotone decreasing in `z` over `[0,h]` (since `z<h_b` throughout), so
  the lowest lit height does carry the largest `s` among lit heights in that
  column — the claim holds as now scoped. For `h_b≤h` the column can
  straddle `z=h_b`, where `s` is non-monotone, correctly disqualifying the
  claim there.

### Notes — one fixed, one residual (both non-blocking)

- **Fixed:** `sinΘ(z_rep)≥cosδ>0` now stated as an inequality (equality
  only at a genuine belt-edge root), matching the suggested correction.
- **Residual, cosmetic:** the `z_lo`/`z_rep` symbol overload is fixed inside
  §3.1's revision-1 text (consistently `z_rep` there) but **not** swept
  elsewhere — `z_{lo}` still denotes the fork-1 representative height (not
  the column bound) in §5.1 ("`z_{lo}∈(0,1.7)`"), §5.1's cross-reference
  table, and §7 A2 ("Reading `s,γ` at `z_{lo}`"). Harmless for
  implementation (§8's prose is unambiguous and uses `z_{rep}` throughout),
  but worth a global rename pass before this becomes the basis for
  docstrings/tests, since `belt_column_breakpoints`'s own signature uses
  `z_lo` for the column bound `0` — a reader cross-referencing the two could
  still be confused. **Not required for PASS.**

### Checklist coverage (delta from first pass)

- Numerical stability: **PASS** (was FAIL) — the fp coin-flip is closed by
  construction (gate bypass + analytic-`K`), verified with a dense sweep,
  not a spot-check.
- Data-driven analysis: **PASS** (was weak) — §5 is now executed against
  live `arty` code with a 316-cell dense sweep, matching the sibling
  aspect's precedent; independently reproduced in this review without
  relying on the modeler's script or printed numbers.
- All other checklist items unchanged from the first pass's assessment
  (dimensional analysis, layering, source attribution, parameter ranges) —
  still PASS, nothing in the revision touched those axes.

### Outstanding for the next (implementation) pass — not blocking this gate

- Sweep the residual `z_lo`/`z_rep` symbol overload noted above.
- When `src/arty/` code lands: the dense ring sweep, feet-lit bit-equality,
  prone-below-standing, and off-axis A3 regression tests specified in §7
  A5/§8 are the acceptance bar — a single `max()`-over-ring assertion must
  not be accepted (this is exactly the hole the naive rule fell through).

______________________________________________________________________

## Re-review (2026-07-20, `src/arty/` implementation pass)

**Verdict: PASS**

### Scope of this pass

`src/arty/fragmentation.py` (new `_belt_column_zrep_vec`; `_expected_kills_3d_point`
and `_expected_kills_3d_vec` rewritten to evaluate at `z_rep`),
`src/arty/zones.py` (`_four_zone_familyA_eval` rewritten the same way, calling
the new helper), and the new `tests/test_familyA_false_safe_zone.py`. Confirmed
via `git diff --stat` and `git status` that no `.qmd` or `app/` file is touched
by this pass — the layering rule holds; all physics/constants remain inside
`src/arty/`. `derivation.md`/`scoping.md` unchanged (this pass implements the
already-PASSed revision-1 rule verbatim, per the derivation's own §8).

### Independent verification performed

Reimplemented/re-derived rather than trusting the diff at face value:

- **Ran the new test file and the full suite:** `uv run pytest
  tests/test_familyA_false_safe_zone.py` → 6/6 pass; `uv run pytest tests/` →
  251 passed, 4 skipped, 6 deselected, no regressions elsewhere.
- **Traced the axis algebra by hand** for both `_belt_column_zrep_vec`
  (forward-axis `cosΘ=(x cosα − ζ sinα)/s`, matching `_forward_shell_axis` and
  `belt_column_breakpoints`'s own documented convention) and the single-zone
  backward-axis path (`_shell_axis=(−cosα,0,−sinα)`): confirmed
  `_expected_kills_3d_point`'s interior-branch `cosΘ` (via `_shell_axis`) and
  `_expected_kills_3d_vec`'s inlined `(-x·cosα − dz·sinα)/s` are the *same*
  formula, and confirmed both correctly feed `x_axis=-x_g` into
  `_belt_column_zrep_vec` — i.e. the gate/selection and the interior-case
  magnitude use one consistent backward-axis convention throughout, not two
  that could silently disagree ([[belt_axis_convention_pitfall]] risk,
  checked and clear).
- **Independently reimplemented the four-zone feet-lit reduction identity**
  (derivation §5.4, "four-zone relocated... reduces bit-for-bit at feet-lit
  cells") from scratch — a fresh script computing the old `z=0` four-zone
  kernel via the shipped `presented_area`/`_familyA_zone_massintegral`, not
  reusing any of the modeler's code — and compared it against the current
  `_four_zone_familyA_eval` at `x∈{8,9,10,11,12,15,20}`, off-axis `y≠0`
  included: `max|Δ|=0.0` (bit-exact). This is the counterpart of
  `test_feet_lit_reduction`, which only exercises the single-zone path — see
  Finding 1 below.
- **Swept `field_pk`/`Pk` for NaN/overflow/out-of-[0,1] across a broad grid**
  (`AoF∈{15,45,60,75,90}°×h_b∈{0,1,2,5,20} m`, `max_radius=40 m`, both
  single-zone `compute_frag_field_3d` and four-zone `four_zone_field`,
  `n_grid=61`): all finite, all in `[0,1]`. Includes `h_b=0` (ground burst),
  the regime flagged in Finding 2.
- **Probed the near-burst singularity guard directly** (`h_b=0`,
  `x∈{0,1e-4,1e-5}`, `y=0`) on the four-zone path: `N` ranges up to `~8.9e12`
  at `x=1e-5` — see Finding 2.
- **Confirmed `_expected_kills_3d_point` remains unused dead code**, same as
  before this pass (`git show HEAD:src/arty/fragmentation.py` shows it was
  already uncalled outside its own definition/docstrings pre-diff) — not a
  regression, just noting the parity edit to it doesn't change any live
  code path.
- **Confirmed no `slant_range_grid`/`build_mmin_table` interaction:** the
  Family-A path (single- or four-zone) computes `E`/`pk_given_hit` directly
  from `s`, never through the `m_min` interpolation table used by the
  ρ_L/Family-B path, so relocating `z_rep` cannot trigger the
  `np.interp`-silently-clips grid-coverage failure mode flagged for that
  other path ([[lethal_density_field_implementation]]).

### Findings

**Deferrable — the four-zone feet-lit reduction identity (derivation §5.4) has
no regression test, only the single-zone path does.** `tests/
test_familyA_false_safe_zone.py::test_feet_lit_reduction` locks the
single-zone bit-round-off reduction against an independent `_ref_z0_single`
reference, but there is no analogous test for `_four_zone_familyA_eval`
against an independent old-`z=0` four-zone reference, even though the
derivation explicitly claims the identity for *both* paths (§5.4: "four-zone
relocated: ... N=182.7, 79.5 at r=2,3" plus the general reduction argument of
§4, which is stated per-zone and therefore applies identically to the
four-zone kernel). I independently confirmed the identity holds bit-exact
(see Verification above), so this is not a live correctness defect — but per
this project's own recorded pattern
([[four_zone_test_parity_gap]]: "a zones.py mirror of a fragmentation.py fix
needs the same defect-removal test, not a weaker invariant"), the four-zone
path is exactly the one with no permanent regression coverage for a claim the
derivation itself makes about it. A future refactor of `_four_zone_familyA_eval`
(e.g. touching the zone-iteration order, the `s_z`/`gamma` recompute, or the
`ok` mask) could silently reintroduce a feet-lit discrepancy with nothing to
catch it. **Suggested correction:** add a
`test_four_zone_feet_lit_reduction` mirroring `test_feet_lit_reduction` — an
independent old-`z=0` four-zone reference (straightforward: reuse
`presented_area`/`_familyA_zone_massintegral`/`compute_shell_zones` directly,
as I did for this review) compared against `_four_zone_familyA_eval` at
several feet-lit `(x,y)` including off-axis `y≠0`.

**Note — `_four_zone_familyA_eval`'s near-burst singularity guard silently
tightened from `s ≥ 1e-3` to `s ≥ 1e-6`, undocumented.** The pre-diff code
gated on `valid = s >= 1e-3`; the new code's `ok = s_z >= 1e-6` (harmonizing
with the single-zone path's pre-existing `1e-6` threshold) is three orders of
magnitude looser and is not mentioned in the derivation or in a code comment
as an intentional change. Practically this is **not harmful**: I confirmed
(a) the app only ever consumes `pk_by_zone`/`pk_total`
(`1-exp(-N)`, saturating to 1.0) from `_four_zone_field_split`/
`four_zone_line_split`/`four_zone_field` — `app/sensitivity.py` never reads
raw `field_N`/`by_zone` — so the resulting enormous `N` values (verified up to
`~8.9e12` at `h_b=0`, `x=1e-5` m) never surface to a user; and (b) no
NaN/inf/overflow results from the sweep above. This is a genuine, if
low-impact, unexplained deviation from the prior convention rather than a
correctness bug. **Suggested correction:** either restore `1e-3` for
consistency with the un-touched pre-existing convention, or add a one-line
comment stating the harmonization with the single-zone `1e-6` threshold is
intentional (and, if kept, a boundary test at `h_b≈0`, `x,y→0` asserting
`Pk` still saturates to `≈1` rather than crashing/NaN-ing, matching the
"zero range" checklist item that is otherwise unexercised for this path).

### Checklist coverage

- **Dimensional analysis:** PASS — verified the relocated formulas are eq. (1)
  evaluated at a different `z`; no new terms, units unchanged (`A_p[m²]·J[count]
  /(s²[m²]·δ[-]·g[-]) = [count]`), matching the derivation's own §6 claim.
- **Boundary cases:** zero range (`s<1e-6`) still guarded on both paths;
  maximum range swept (`max_radius=40`, no NaN/overflow); grazing angle —
  the dense-ring sweeps deliberately stay strictly inside `(onset, feet-lit)`
  by a margin (`±0.01`–`0.05` m), appropriately avoiding the exact tangency
  root rather than asserting a specific value there (a genuinely ill-defined
  fp tie, not a defect); PASS. See Note above for the one loosened boundary
  guard (`1e-3→1e-6`), not blocking.
- **Parameter ranges:** no new constants introduced; the fixed epsilons
  (`1e-6`, `1e-9`, `1e-12`) reused from already-accepted convention elsewhere
  in the file except the one noted deviation.
- **Numerical stability:** PASS — the fp coin-flip this whole aspect exists to
  fix is closed exactly as derived (gate bypass + analytic-`K`
  `sinΘ=cosδ`), reverified with the dense sweep (own tests) and a broad
  finite/[0,1]-range sweep (this review) with no NaN/overflow, including at
  `h_b=0`.
- **Physical plausibility:** confirmed — standing struck before prone
  (matches taller silhouette exposed to a low grazing belt sooner),
  `h`-monotonicity holds, magnitudes at the defect config match the already
  twice-verified derivation numbers exactly, four-zone/single-zone reduction
  values agree with the ring geometry cross-check from the sibling aspect.
- **Source attribution:** N/A new — no new literature introduced; unchanged
  from the derivation's already-accepted attribution.
- **Layering:** PASS — confirmed via `git status`/`git diff --stat` that this
  pass touches only `src/arty/{fragmentation,zones}.py` and
  `tests/test_familyA_false_safe_zone.py`; no `.qmd` or `app/` file is part of
  the diff, so no physics/constants leaked outside `src/arty/`.
- **Constraints/limitations:** the derivation's A1 (lumped-silhouette
  over-count, conservative-high, `h_b>h` qualified), A2 (representative-height
  far/mid-field approximation), A4 (inherited obliquity/Poisson caveats) are
  unchanged by this implementation pass and require no code-level disclosure
  beyond what already exists in the derivation; nothing in the src/ diff
  contradicts or silently narrows any of them.
- **Data-driven analysis:** PASS — the new test file executes a dense
  (`~317`-cell / `~127`-cell) sweep across the whole previously-false ring for
  both paths (not a `max()`-over-ring spot check, matching this project's own
  acceptance bar from the derivation review cycle), plus a bit-exact
  reduction test, monotonicity test, and an independent off-axis reference —
  all independently re-executed and reproduced in this review rather than
  taken on the diff's word.

### Suggested next steps (not applied)

1. Add `test_four_zone_feet_lit_reduction` (Deferrable finding above) —
   closes the one asymmetric coverage gap between the single- and four-zone
   paths for a claim the derivation makes about both.
2. Either revert `_four_zone_familyA_eval`'s near-burst guard to `1e-3` or
   add a one-line comment + boundary test documenting the `1e-6`
   harmonization as intentional (Note above) — low priority, no observed
   harm.

______________________________________________________________________

## Re-review (2026-07-20, notebook-presentation pass)

**Verdict: PASS**

Final review gate before commit. Documentation-only diff relative to the
already-PASSed src/ implementation. Effort scaled to the low risk.

### Scope of this pass

Three `.qmd` files (via `git diff`, read fresh):

- `_change-log.qmd` — new `0.6.0` row referencing
  `updates/familyA-false-safe-zone/derivation.md`.
- `_four-zone-3d.qmd` — one prose paragraph in §6.7 (above the
  `fig_zone_elevation` cell) rewritten to separate the ray/dot renderer's
  horizontal-ray exclusion from the (now-fixed) $P_\text{kill}$ field.
- `_limitations.qmd` — the single "False safe zone … fixed in v 0.5.1" note
  expanded into a two-family (B v0.5.1 / A v0.6.0) note.

No `.qmd` code cells changed — the diff is prose and table rows only; the
`{python}` blocks are unchanged context. Confirmed via `git status` that the
notebook pass added no new `src/`, `app/`, or test files: the only
non-`experiment/fragmentation-field/` working-tree changes are the earlier,
already-PASSed `src/arty/{fragmentation,zones}.py` and
`tests/test_familyA_false_safe_zone.py` plus agent-memory writes — none of
which this pass touched.

### Gate 2 (no authored physics in `.qmd`) — PASS

Every equation/number quoted in the diff traces to `derivation.md` (or the
already-shipped Family-B text), not newly computed by the notebook agent:

- $A_p(\gamma)=w_\perp(h\cos\gamma+d\sin\gamma)$ — verbatim from derivation §1
  (line 44) and Symbols (line 110).
- "belt-edge quadratic, eq. 5" and the relocated $(s,\gamma,\cos\Theta)$
  geometry — derivation §2 (lines 62–73), §3 (eq. 3).
- $\lambda = w_\perp\!\int_0^h\!\rho_L\,dz$ (eq. 23) — pre-existing Family-B
  prose, unchanged claim.
- Innermost dead-zone bound $r\lesssim(h_b-h)/\tan\delta$ — this replaces the
  old config-specific "$r\lesssim1.1$ m" with the general onset formula that
  already appears verbatim in derivation §3.2 (line 193), §5.1 (line 252),
  §5.2. Evaluates to 1.12 m at the documented config
  ($h_b{=}2,h{=}1.7,\delta{=}15°$), consistent with the number it replaces.
  Not newly authored — a restatement of an existing derived quantity. The
  accompanying phrase "even the top of the head sits below the belt's lowest
  ray" is a near-verbatim lift of derivation §5.2 (line 271).
- Family-A "conservative-high over-count … thin inner ring (derivation §7
  A1)" — matches derivation §7 A1 (lines 326–334) and §3.2 (lines 198–200).

### Accuracy vs derivation.md — PASS

- The Family-A paragraph correctly states the *narrower* defect (only the
  belt gate + arrival geometry sampled on the feet ray; $A_p$ already carried
  the vertical extent) — matches derivation §1 (lines 43–51), and correctly
  contrasts it with Family-B's silhouette defect.
- The retained limitation (§7 A1) is described honestly and with the correct
  sign: full lumped $A_p$ scored whenever any part of the column is lit ⇒
  head-only grazing strike over-counted at the full standing silhouette ⇒
  bounded, **conservative-high**, safe-direction, confined to the thin inner
  ring. This is the fork-2 rejection rationale (derivation §3.2) plus §7 A1,
  stated as the *dual* of Family-B's conservative-low — matching derivation
  §7 A1 (lines 331–333).
- Family-B's own retained approximation kept as "conservative-low
  (derivation §4, §7 A1)" — this is the pre-existing citation into
  `target-height-intercept/derivation.md`, which I re-checked: its §4 scope
  limit and §7 A1 (frontal projection, no obliquity) do say
  conservative-low-for-prone. Citation still resolves. (Note: within the
  single limitations note, "(derivation §…)" now points at two different
  files depending on paragraph; each paragraph names its own `derivation.md`
  path explicitly, so it is resolvable — see Note below.)

### Consistency — ray/dot renderer vs $P_\text{kill}$ field (item 3) — PASS

The `_four-zone-3d.qmd` edit correctly distinguishes the two things the old
prose conflated:

- **Rendering choice (unaffected):** the ray/dot ground-impact view requires
  $v_{gz}<0$, so at AoF=90° the $\phi=\pm90°$ horizontal rays ($v_{gz}=0$)
  are excluded — consistent with the "$v_{gz}\ge0$ … ↑ excl." text two lines
  above (lines 315–316).
- **Defect closure (the actual fix):** the graded four-zone $P_\text{kill}$
  field (§6.7 — verified that header is "Four-zone field and ground-impact
  diagnostic", the section that hosts both artifacts) no longer shows a
  near-burst safe zone, because as of v0.6.0 the belt gate is evaluated at
  the illuminated column height, not the $z=0$ feet ray. This matches
  derivation §5.4 (old four-zone reads $N=0$ at $r=2,3$ m; relocated reads
  $N=182.7,79.5$, $P_k=1.0$) and the PASSed src/ pass. The old text
  ("…which is why a near-burst safe zone appears in the four-zone field…")
  would now be factually wrong post-fix; the rewrite correctly retires it.

### Render correctness (item 4)

Not re-rendered. The user confirmed a clean 30-cell render with HTML output,
and the diff is prose/table-only with no code-cell changes — no reason to
doubt the render. Cross-references checked statically: §6.7 exists and is the
correct target; eq. 5 / eq. 23 / §7 A1 all resolve.

### Notes (non-blocking, not required for PASS)

- The expanded limitations note reuses the bare token "(derivation §4, §7
  A1)" for Family-B and "(derivation §7 A1)" for Family-A within the same
  bullet, referring to two different `derivation.md` files. Each paragraph
  names its file path, so it is disambiguable, but a future reader skimming
  could tie the wrong §7 A1 to the wrong family. Optional: qualify as
  "(target-height-intercept derivation §7 A1)" / "(this fix's derivation §7
  A1)". Cosmetic.

### Checklist coverage (documentation delta)

- Source attribution: PASS — every equation/number traces to `derivation.md`
  or pre-existing Family-B text; none newly asserted by the notebook agent.
- Layering: PASS — no physics/constants/computation in the `.qmd`; prose and
  cross-refs only, no code cells changed, no `src/`/`app/` touched this pass.
- Constraints/Limitation check: PASS — retained Family-A conservative-high
  over-count (§7 A1) captured accurately and with the correct (safe) sign;
  Family-B conservative-low retained.
- Physical plausibility / consistency: PASS — ray-renderer vs field
  distinction correct; dead-zone bound and onset formula consistent across
  both families and with derivation.

### Suggested next steps (not applied)

1. (Optional, cosmetic) Disambiguate the two "(derivation §7 A1)" citations
   in the limitations note by naming the file each refers to.
