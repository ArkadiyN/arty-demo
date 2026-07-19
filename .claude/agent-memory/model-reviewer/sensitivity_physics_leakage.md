---
name: sensitivity-physics-leakage
description: app/sensitivity.py repeatedly duplicates fragment ground-impact ray geometry inline instead of calling arty.zones.fragment_ground_impact — flag every time a new spray-cone/cross-section helper is added
metadata:
  type: project
---

`app/sensitivity.py` has a recurring layering violation: `_spray_cone`
(elevation x-z plane, introduced commit 5335b43) and `_spray_cone_across`
(across y-z plane, added in the 2026-06 across-slice-view change) both
re-derive the fragment ray unit-vector projection inline:

```
vgx = cA*cT + sA*sT*phi_sign
vgz = -sA*cT + cA*sT*phi_sign
```

This is the *same* formula as `src/arty/zones.fragment_ground_impact`
(`vgx = cA*cT + sA*sT*sP`, `vgz = -sA*cT + cA*sT*sP`, with `sP = phi_sign`),
just inlined for the chart's ray-drawing loop instead of imported. Per
project layering rule (`.qmd`/`app/` must import all physics from
`src/arty/`), this is a defect in spirit even though the formula matches
the reference exactly (no drift found on 2026-06-20 review) — there's no
single source of truth, so a future `fragment_ground_impact` fix would not
propagate to the chart rays.

**Why:** the new-math gate in `agents-routing.md` is about *new* physics;
this is *duplicated existing* physics, which the gate doesn't explicitly
name but the "Layering" review checklist item does ("no physics, computation,
or parameter values leaked into the .qmd/app").

**How to apply:** this is a pre-existing pattern (the first instance,
`_spray_cone`, predates the diff under review and was presumably accepted
already) — do not block a new PASS on it alone, but call it out as a
secondary/low-severity finding every time a new helper perpetuates it
(e.g. `_spray_cone_across`), recommending consolidation into a shared
`arty` ray-geometry helper (or reuse of `fragment_ground_impact` directly)
rather than re-fixing it ad hoc per review.

**Resolved going-forward (app/sensitivity.py only):** `src/arty/zones.py`
extracted the shared trig into
`fragment_velocity(theta_z_deg, phi_rad, aof_deg) -> (vgx, vgy, vgz)`;
`fragment_ground_impact` and `app/sensitivity.py`'s `_spray_cone`/
`_spray_cone_across` all call it now instead of inlining the formula. Treat
this specific pair as closed; re-open only if a *new* spray-cone-like helper
reappears with inlined trig instead of calling `fragment_velocity` — that
recurrence is the actual gotcha this entry exists for, not the one-time fix.

**plots.py recurrence: fixed.** `src/arty/plots.py:fig_zone_elevation` (had
inlined the same formula as `app/sensitivity.py` once did) now calls
`fragment_velocity(z.spray_deg, phi_sign * np.pi/2, aof_deg)` instead of
inlining the trig — verified bit-exact against the old inline formula
(20k-sample randomized check, max abs diff 0.0; `np.sin(±pi/2)` is exact
±1.0 in float64, and `vgx`/`vgz` depend only on `sin(phi)`, not `cos(phi)`,
so the substitution is an exact identity, not an approximation). Also
verified by reverting `plots.py` to the pre-fix formula in a worktree and
re-running `tests/test_plots.py`: all 15 tests still pass unchanged.

**Durable gotcha — numeric-equivalence tests can't catch a bit-identical
duplication.** That last check is the actual lesson here: because the
duplicated formula and the canonical `fragment_velocity` formula were
*bit-identical* (not just "close"), `tests/test_plots.py`'s regression guard
(`test_zone_elevation_impacts_match_fragment_velocity`, which compares
rendered ray endpoints numerically to a fresh `fragment_velocity` call) would
**not** have failed against the old inlined code — I confirmed this by
actually running it there. A numeric-equivalence test only catches a *future*
re-inlining that also gets the formula *wrong*; it cannot detect "duplicated
but correct," which is the actual layering violation this fix addressed. The
test file's docstring claim that the old code "silently diverged" is
therefore inaccurate for this specific bug (there was no divergence, only
duplication) — don't take a docstring's framing of "what a regression test
protects against" at face value; re-derive it by reverting the fix and
running the test, as done here. If a reviewer wants a test that actually
enforces "calls fragment_velocity" (not just "produces the same numbers"),
it needs to assert the call itself (e.g. monkeypatch/spy), not just compare
outputs.

**Resolved — delegation guard added.** `tests/test_plots.py`'s
`test_zone_elevation_delegates_to_fragment_velocity` now monkeypatches
`arty.plots.fragment_velocity` with a sentinel and asserts (1) it's called
once per (zone, φ=±90°) ray, (2) with the right args, (3) the sentinel's
output actually reaches the rendered rays. Verified this genuinely closes the
gap the numeric-equivalence test left open: re-inlining the exact bit-identical
formula in `fig_zone_elevation` (keeping the now-unused `fragment_velocity`
import) makes this test fail with `assert calls` — the failure mode the old
test structurally could not produce. Treat this as the reference pattern for
"prove layering, not just numeric correctness" when reviewing future
delegation-guard tests in this repo.

**Reviewer gotcha for self:** `git checkout -- <file>` discards the *entire*
uncommitted working-tree diff, not just a reviewer-added scratch edit layered
on top of it — if the file being empirically tested (e.g. by reverting to the
pre-fix formula) already carried its own uncommitted approved changes, `git
stash push -- <file>` / `git stash pop` bracketing the experiment is safe,
`git checkout -- <file>` is not (it silently reverts past the approved diff
to HEAD). Always re-diff against the previously-recorded approved diff after
any revert-based verification to confirm nothing beyond the intentional probe
was undone.

`fig_single_zone_elevation`'s belt-edge-ray trig (`beta_c`/`beta` rotation)
remains a related but distinct construction with no equivalent `arty` helper
to point at — still flag it as "physics computed in plots.py" if touched,
but it's not the same duplicate and wasn't part of this fix.
