---
name: familya-false-safe-zone-derivation-fail
description: Family-A false-safe-zone fix — FAILED derivation review on the first pass (fp coin-flip zeroed ~half the ring), PASSED on re-review after the modeler bypassed the internal gate + used analytic-K; independently reverified with a dense sweep
metadata:
  type: project
---

`experiment/fragmentation-field/updates/familyA-false-safe-zone/` (Option 2:
relocate the belt gate + ray geometry to the illuminated column, keep
`A_p(γ)·pk_given_hit(E)` graded kernel intact).

**Pass 1 (2026-07-20) — FAIL.** No `src/arty/` code written yet
(derivation-only gate). Scoping/decomposition (Family-A vs Family-B,
double-count avoidance, Option 2 over 1/3) was sound. The blocking defect
was the representative-height choice: see
[[piecewise_quadrature_boundary_evaluation]] for the mechanism (fp
coin-flip evaluating a belt-gated kernel exactly at its own gate's root).
Also flagged, non-blocking: A3's axis-sign fix (`-x` into
`belt_column_breakpoints` for the single-zone legacy backward axis, see
[[belt_axis_convention_pitfall]]) was correctly derived but untested off
the one AoF=90° config where the bug is invisible (`B=0`); the
"conservative flux" justification in §3.1 item 2 silently assumed
`h_b > h_target`, not guaranteed by the app's `h_b∈[0,20]` slider.

**Pass 2 (2026-07-20, same day, revised `derivation.md`) — PASS.** The
modeler's fix: bypass the kernel's own internal belt gate at `z_rep`
(membership already decided by `belt_column_breakpoints`) and, for the
single-zone `1/sinΘ` magnitude, substitute the **analytically known**
boundary value `sinΘ(z_rep)=√(1-(cosθ^z±sinδ)²)` instead of recomputing
`cosΘ` from `(x,y,z_rep)` — exact by construction since that boundary value
depends only on `cosθ^z,δ`, not `(x,y)`. Four-zone path needs no `cosΘ` at
all once the gate is bypassed (magnitude uses fixed `1/sinθ^z`), so it's
coin-flip-free by construction. Independently reimplemented eq. (3) from
scratch against live `src/arty` (not the modeler's script) and reproduced
every §5 number exactly: dense 316-cell sweep `r∈[1.13,7.45)` — naive rule
zeros `54/316`, fixed rule zeros `0/316`, `min N=12.14 ⇒ min P_k=0.999995`;
bit-exact reduction identity at feet-lit cells; four-zone relocated
`N=182.7/79.5` at `r=2,3`; off-axis (AoF=60°, `x<0`) axis-sign trap
reproduced exactly. Both deferrables addressed (§5.5 executed off-axis
check + required src/ test named in §7 A5/§8; `h_b>h` qualifier added and
algebraically checked to hold). One Note fixed (inequality wording); one
Note left unswept (`z_lo`/`z_rep` symbol overload persists in §5.1/§7 A2
outside the revised §3.1 text) — cosmetic, not blocking.

**Pass 3 (2026-07-20, `src/arty/` implementation) — PASS.** `fragmentation.py`
(`_belt_column_zrep_vec`, `_expected_kills_3d_point`/`_vec`) and `zones.py`
(`_four_zone_familyA_eval`) implement revision-1 verbatim. Independently
reran the full derivation §5 sweep against the new src/ code (not the
diff's own numbers): dense-ring `P_k>0` sweeps (single- and four-zone),
bit-exact feet-lit reduction (single-zone, and independently for four-zone —
`max|Δ|=0.0`, reimplemented from scratch, not just re-run), off-axis
axis-sign pin, standing/prone monotonicity — all reproduced; full test suite
251 passed/4 skipped, no regressions; broad `AoF×h_b` sweep (incl. `h_b=0`)
shows no NaN/inf/out-of-[0,1] `P_k`. Two non-blocking findings: (1)
[[four_zone_test_parity_gap]] recurred exactly as the memory predicts — the
new test file has a single-zone `test_feet_lit_reduction` but no four-zone
counterpart, despite the derivation claiming the reduction identity for
both; (2) `_four_zone_familyA_eval`'s near-burst guard silently loosened
`valid=s>=1e-3`→`ok=s_z>=1e-6` (matching the single-zone convention) with no
comment/derivation mention — harmless in practice (app only ever reads
`Pk=1-exp(-N)`, which saturates; confirmed no NaN even at `h_b=0,x→1e-5`
where `N~9e12`), but an undocumented deviation worth a one-line comment or
revert. No `.qmd`/`app/` touched — layering held.

**Takeaway for future re-reviews of this failure class:** the fix pattern
that closes an "evaluate at an exact gate root" coin-flip is (a) bypass the
kernel's internal re-test of that gate, plus (b) substitute the
analytically-known boundary value rather than recomputing it — a nudge-ε is
an acceptable alternative but the analytic substitution is preferred
(exact, no tunable). Acceptance bar is a **dense sweep** across the
affected region reproduced independently (not trusting the modeler's
printed numbers) — a single lucky spot-check or `max()`-over-ring assertion
is exactly the hole the original defect fell through twice in this
project's history (see [[piecewise_quadrature_boundary_evaluation]]).
