# Review — angle-dependent presented-area profile $A_p(\gamma)$

**Reviewer:** model-reviewer agent
**Date:** 2026-07-19
**Scope:** `experiment/fragmentation-field/updates/target-area-profile/` (scoping.md,
derivation.md) and its present-day implementation/presentation in `src/arty/`
and the `fragmentation-field` notebook. This is the first independent review
of this aspect — the "Verdict" section in `derivation.md` §6 is the modeler's
own self-check, not a prior review.

## Verdict: PASS-with-limitations

No Blocking findings. The derivation is internally consistent (unit check,
limit bounds, Lambert-projection algebra all correct), and the implementation
in `src/arty/fragmentation.py` / `src/arty/zones.py` is a faithful,
bit-consistent translation of the derivation's eq. (P1)/(P4)/(22'). Two
material-but-deferrable items should be logged; see below.

______________________________________________________________________

## What was checked

- **Derivation soundness** (`derivation.md`): Lambert flat-plate projection
  algebra (§3.1–3.3), the width→area geometry-factor rewrite (§4.1–4.2), unit
  check (§4.2: m²/m² dimensionless, confirmed by hand), and the two
  self-flagged non-recoveries (old eq. 22 and the 1D disk eq. 9, §4.3–4.4).
  All correct as derived.
- **Implementation parity**: `presented_area(gamma, posture)`
  (`src/arty/fragmentation.py:190-192`) is exactly
  `w_perp*(h*cos(gamma) + d*sin(gamma))`, matching eq. (P1). It is wired into
  the geometry factor at `fragmentation.py:872-876` (`_expected_kills_3d_point`)
  and `fragmentation.py:929-931` (`_expected_kills_3d_vec`, the vectorised
  headline-field path), and mirrored in `zones.py:490-493`
  (`_four_zone_familyA_eval`) for the four-zone model — same `gamma = arcsin(clip(h_b/s,-1,1))` definition, same `Ap/(2π s²·2 sinΘ·δ)` geometry
  factor, in both single- and four-zone code paths. `STANDING`/`PRONE`
  constants (`w_perp=0.5, h=1.7, d=0.3` / `w_perp=0.5, h=0.3, d=1.8`) match
  the scoping table exactly.
- **Boundary cases**: `gamma` is bounded to `[0, π/2]` via
  `arcsin(clip(h_b/s, -1, 1))`, so `cos(gamma), sin(gamma) ≥ 0` always and
  `A_p(gamma) ≥ 0` everywhere (no negative-area regime). `s < 1e-6` and
  `sin_Theta < 1e-9` are both guarded before the `1/s²`, `1/sinΘ` divisions —
  no div-by-zero/overflow paths found. Grazing (`γ→0`, large cross-range) and
  vertical (`γ→π/2`, directly under burst) limits both recover the expected
  `A_f`/`A_t` endpoints (verified both analytically and via
  `test_presented_area_standing_horizontal` / `_prone_vertical`).
- **Independent numeric check** (scratch script, `compute_frag_field_3d`,
  M1 105 mm, AoF = 0°, δ = 15°): $R_{50}$(standing) = 28 m vs
  $R_{50}$(prone) = 14 m at $h_b$ = 0.5 m, crossing over to
  $R_{50}$(standing) = 12 m vs $R_{50}$(prone) = 18 m at $h_b$ = 20 m. This
  is exactly the qualitative signature the aspect was scoped to produce
  (standing more exposed near a low/ground burst, prone more exposed under a
  steep high airburst) — the physics genuinely works when exercised.
- **Layering**: no physics leaked into any `.qmd`. All `A_p`/`γ` math lives in
  `src/arty/fragmentation.py` and `src/arty/zones.py`; notebook cells only
  call `presented_area(...)` and print/plot the result, or restate the
  formula symbolically as prose/LaTeX (`_governing-equations.qmd:214-225`,
  `_four-zone-3d.qmd:229-245`) — consistent with how other aspects present
  equations in this project.
- **Source attribution**: scoping.md §3 and derivation.md §5.2 are explicit
  that the box-body dimensions (Cunniff 2014 / AEP-55 Vol. 3 conventions) are
  *not* collected in `doc-reference/` and are engineering-convention
  estimates, ±25%. This disclosure is carried through faithfully into
  `_limitations.qmd:157-162` (§12, "Posture box-body dimensions") and into
  `A_REF_DEFAULT`'s inline comment (`fragmentation.py:405-412`). No gap here.
  The $R_{50}$-recalibration consequence of the $s^{-1}\to s^{-2}$ geometry
  change (derivation §4.3) is likewise disclosed at
  `_limitations.qmd:163-171`.
- **Downstream consistency**: a later aspect (`target-height-intercept`) adds
  a second, frontal-projection-only ground-field pathway
  (`pkill_field_3d`/`four_zone_pkill_field`) that deliberately does *not* use
  `presented_area`'s obliquity term. This is not a target-area-profile defect
  — it is disclosed as a distinct, intentional simplification in that
  aspect's own derivation (§4, "Scope limit (deferred, §7)") and in
  `_limitations.qmd:224-228` ("the remaining approximation is frontal
  projection only... a documented refinement, not the false-safe artefact").
  The three now-coexisting presented-area treatments (Family-A live $A_p(γ)$,
  target-height-intercept frontal-only column integral, pkill-poisson-field's
  frozen $A_{ref}=0.85$) are each independently caveated where they are used
  (`app/sensitivity.py:34, 989, 1044-1053`), so a user is told which panel
  is posture/obliquity-sensitive and which is not.

______________________________________________________________________

## Findings

### 1. [Deferrable] `sinΘ` retained "to match old notation" in the single-zone legacy path — disclosed error bound (\<3.5%) is only valid for δ ≤ 15°, but the app exposes δ up to 30°

`derivation.md` §4.1.2 admits eq. (P4) keeps an extra `sinΘ` factor (the
*field point's own* polar angle, not the belt-integrated Jacobian used to
derive `Ω_belt`) purely to match the old §6.5 notation, and states the
resulting error vs. the "pure" inverse-square form (P3) is "< 3.5%" for
"the equatorial belt (δ ≤ 15°)". This is algebraically
`1/sin(90°−δ) − 1`, which is 3.53% at δ=15° (matches the claim) but **rises
to ~15.5% at δ=30°** — the maximum allowed by the `spray_half_angle` slider
in `app/sensitivity.py:108-110` (range 0–30°).

Scope correction after re-checking both code paths: this applies **only** to
the single-zone legacy path (`_expected_kills_3d_point` /
`_expected_kills_3d_vec`, reached via `compute_frag_field_3d`, the
"Single-zone (legacy)" app mode). The four-zone Family-A path
(`_four_zone_familyA_eval` / `_four_zone_field_split`, `zones.py:493,510`)
divides by `sin(theta_z)` — the fixed per-zone spray angle — not by the
field point's own `sinΘ`, so it does **not** carry this error at all; this
matches the already-correct convention noted in this reviewer's own memory
(`lethal_density_field_implementation.md`) for the sibling `lethal_density_point`
kernel. The single-zone path's use of `sinΘ` is the same **already-documented,
intentionally-unfixed legacy quirk** flagged in-code at
`fragmentation.py:521-524` ("it inflates ρ_L by O(δ²) off the belt centre") —
this review adds the exact bound (`1/sin(90°−δ)−1`, ~15.5% at δ=30°) beyond
the existing "O(δ²)" characterization, and confirms it is not carried into
`_limitations.qmd` (checked; no entry for this specific approximation,
distinct from the axis-convention entry at lines 179-192).

**Impact:** proportional ~15% scaling of the *single-zone legacy* Family-A
geometry factor for off-belt-center cells at the app's largest δ setting —
no qualitative reversal, and the panel is explicitly labeled "legacy" in the
UI. The four-zone ("new") path, which is what the app defaults toward for
serious use, is unaffected. Well within the project's engineering-fidelity
bar; does not affect the δ=15° default.

**Suggested correction (do not apply):** either (a) add a one-line
`_limitations.qmd` §12 entry generalizing the existing in-code note with the
`1/sin(90°−δ)−1` bound (~15% at δ=30°), scoped explicitly to the single-zone
legacy path, or (b) finally apply the same fix the four-zone path and
`lethal_density_point` already use — replace `sinΘ` with the fixed
`sinθ^z = sin(90°) = 1` for the single-zone equatorial belt at
`fragmentation.py:876,931` — which removes the approximation outright rather
than just documenting it, and is a small change given the four-zone/
`lethal_density_point` precedent already exists.

### 2. [Deferrable] The aspect's own required validation (γ-sweep + ground-vs-airburst posture comparison) was never added to the notebook

`scoping.md` §4.3 and `derivation.md` §7 (item 7) both specify: "γ-sweep plot
of $A_p$ for standing and prone; ground-burst vs airburst hit-count ratio for
both postures; expect ~3–5× airburst gain vs prone, ~1× vs standing." No such
plot or ratio table exists in any `.qmd`. What exists is: two point-value
assertions in `_four-zone-3d.qmd:249-260` (γ=0 and γ=π/2 only, for both
postures) and the equivalent two unit tests
(`test_presented_area_standing_horizontal`, `test_presented_area_prone_vertical`
in `tests/test_fragmentation.py:269-274`). Neither sweeps γ nor demonstrates
the ground-vs-air crossover the aspect exists to produce.

I independently reproduced the intended effect via a scratch script calling
`compute_frag_field_3d` (see "Independent numeric check" above) — the
qualitative crossover is real and correctly signed, so this is a
**documentation/data-support gap, not a numerics defect**. But as shipped, a
reader of the notebook cannot see or verify the aspect's headline claim
("this is why airburst matters against prone targets") without re-deriving
it themselves; the promised 3–5× ratio is untested anywhere.

**Impact:** no effect on any currently-rendered chart value (the physics is
already correct); the gap is that the notebook doesn't *show* it. Downgraded
from what could be a "no supporting data for the outcome" Blocking finding
only because independent verification confirms the outcome is in fact
correct.

**Suggested correction (do not apply):** add a validation cell to
`_four-zone-3d.qmd` §6.6/6.7 — a γ-sweep line chart of $A_p$(STANDING) vs
$A_p$(PRONE), plus a small $R_{50}$-or-$P_k$-at-fixed-range table comparing
low-$h_b$ vs high-$h_b$ bursts for both postures (the numbers reproduced in
this review — $R_{50}$ 28m/14m at $h_b$=0.5m crossing to 12m/18m at
$h_b$=20m — are a ready starting point).

### 3. [Note] Three coexisting presented-area treatments, correctly caveated per panel

Not a target-area-profile defect — recorded for completeness. The Family-A
path (headline 2D field + diff map) uses live $A_p(\gamma,\text{posture})$;
the target-height-intercept ground field uses frontal-only $w_\perp h$
(γ=0 fixed); the point-in-space volume uses a frozen, posture-independent
$A_{ref}=0.85$. Each is disclosed where used. No action needed.

______________________________________________________________________

## Limitation entries to log (if not fixed directly)

1. In `_limitations.qmd` §12, add: "The Family-A geometry factor retains a
   `sinΘ` term (field point's own polar angle) for notational parity with the
   pre-3D width-based formula (target-area-profile derivation §4.1.2); its
   deviation from the pure inverse-square form grows with belt half-width δ
   as `1/sin(90°−δ)−1` — 3.5% at the default δ=15°, ~15.5% at the app's
   maximum δ=30°. Proportional scaling only; no qualitative effect on R₅₀ or
   field shape."
1. If the validation cell (finding 2) is not added before the next pass, log
   in `_limitations.qmd` §12: "The ground-burst-vs-airburst posture crossover
   that motivates $A_p(\gamma)$ is implemented and unit-tested at its γ=0/π/2
   endpoints but is not demonstrated end-to-end (γ-sweep, R₅₀ ratio) in any
   notebook cell; verified ad hoc during the 2026-07-19 review
   (`experiment/fragmentation-field/updates/target-area-profile/review.md`)."

No other findings. Dimensional analysis, numerical stability, parameter
bounds (posture dimensions disclosed as unsourced ±25% engineering
convention), and layering all pass.

______________________________________________________________________

## Review pass 1 — adversarial critique, 2026-09-26 (§6.6.1 posture crossover)

Scope: `_four-zone-3d.qmd` §6.6.1 (new), `_change-log.qmd` 0.16.0,
derivation.md status paragraph + replacement marker (derivation.md:445–457),
`checks/posture-crossover-ground-vs-air.py`. R50 is out of scope (separate
pass) and not reviewed. Open findings on this scope at start: one
(`deferrable`, derivation.md:457, P_kill-for-hit-count substitution) —
assessed below as F2.

Evidence script: `experiment/fragmentation-field/updates/target-area-profile/checks/posture-crossover-robustness.py`
(reviewer probe; **must be moved** to
`updates/target-area-profile/checks/posture-crossover-robustness.py` by the
main agent — the reviewer may write only this file). Runs in a few seconds.
The existing check script reproduces the notebook's numbers as stated
(γ* = 43.5°, A_p = 0.720 m²; P_kill at 0/10/20 m: ground standing
1.000/0.823/0.299, prone 1.000/0.325/0.069; airburst standing
0.061/0.151/0.119, prone 0.313/0.243/0.124).

### Verdict: FAIL

One Blocking finding (F1): the section's headline conclusion — the posture
ordering *flips* under an airburst — holds only in the configuration the
section chose, which happens to be the one that maximizes the effect. At the
model's own default AoF (30°) and at every realistic artillery angle of fall,
the field-integrated result is that prone stays safer, just by a smaller
margin. The fix is presentation only (no `src/arty/` change), but the
qualitative takeaway the reader is given has to change.

### Findings

**F1 — Blocking. The flip is an AoF = 0° artefact of the chosen slice, not a
representative airburst result.** (`_four-zone-3d.qmd` §6.6.1 prose "the
posture that is safer under one is the more exposed under the other" and
"the ordering flips, as the γ-sweep predicts"; `_change-log.qmd` 0.16.0
"showing the ordering flip".)

The belt leaves the shell at 90° ± δ from the axis. So the steepest arrival
elevation the belt can produce on the ground is about γ_max ≈ 90° − AoF + δ.
Only at AoF = 0° (horizontal flight, which no howitzer airburst has) is the
belt a vertical plane containing the burst point. Only there does the
cross-range slice x = 0 sit inside the belt, so fragments land directly
beneath at γ = 90°. The probe confirms that on that slice the prone/standing
N_eff ratio equals A_p(atan(h_b/r)) prone/standing to 2 d.p. at every r:
the end-to-end panel is the γ-sweep evaluated along γ = atan(h_b/r). At
AoF ≥ 30° the x = 0 slice misses the airburst belt altogether (P_kill = 0 or
nan ratios at h_b = 20 m in the probe). So the slice cannot be moved to a
realistic AoF as it stands.

What decides the reader's takeaway is the whole field. Lethal area ΣP_kill·dA
over the 120 m × 120 m grid, prone/standing (M1 105 mm, δ = 15°):

| AoF | h_b = 0.5 m | h_b = 10 m | h_b = 20 m |
|---|---|---|---|
| 0° | 0.33 | 0.81 | **1.14** |
| 15° | 0.31 | 0.79 | **1.08** |
| 30° (model default) | 0.30 | 0.72 | 0.92 |
| 45° | 0.29 | 0.63 | 0.76 |
| 60° | 0.28 | 0.51 | 0.61 |
| 75° | 0.28 | 0.40 | 0.48 |

The ratio goes above 1 (prone more exposed) only for AoF ≲ 20° at a 20 m
burst. At the default AoF = 30° and above, the airburst **narrows** the prone
advantage, from ×0.30 to ×0.6–0.9, and **never reverses** it. The mechanism
the aspect adds is real and visible: prone benefit shrinks ~3× from ground
burst to airburst at AoF 30°. But "lying down is the more exposed posture
under an airburst" is qualitatively wrong for representative inputs. The
headline 5.2× directly beneath is the γ = 90° limit (analytic ceiling 6.0),
which only AoF = 0° reaches.

Impact: the rendered qualitative conclusion reverses (flip → no flip) at the
default and at all realistic AoF. The magnitude shown overstates the airburst
effect at AoF 30° by ~×1.25 on lethal area (1.14 vs 0.92), and at the point
directly beneath by roughly ×5 against what any belt-footprint point at
AoF 30° can reach.

Suggested correction (presentation, notebook pass):
(a) State that AoF = 0° / x = 0 is chosen as the geometry that exposes the
full γ range, that it is the extreme case, and that γ_max ≈ 90° − AoF + δ
bounds the arrival angle on the belt.
(b) Add the lethal-area-ratio-vs-AoF result, or at least the AoF = 30° row,
so the reader sees that in realistic fire the posture effect narrows rather
than reverses. Whole-field ΣP_kill·dA is a new aggregate. Under Gate 2 it
should come from an `arty` function (or a modeler triage should confirm that
summing a returned grid counts as layout), not be computed inline in the
`.qmd`.
(c) Reword the flip sentence and the 0.16.0 change-log entry to match.

**F2 — Deferrable (confirms the existing marker's tier; corrects its
rationale).** P_kill standing in for expected hit count. Ordering is
preserved exactly: `pk_cross = 1 − exp(−N_eff_cross)` (fragmentation.py,
`compute_frag_field_3d`) is monotone at a fixed point, and the prose's
caveat (i) is accurate. Magnitude is compressed only under the ground burst:

- At 10 m the P_kill ratio is 0.40, against an N_eff ratio of 0.23 (×1.7
    understatement of the prone benefit).
- At 5 m it is 0.88 against 0.28.
- The ground-burst r = 0 cell prints 1.00. That is pure saturation: the
    N_eff ratio there is the γ = 90° value, 6.0. A reader will take 1.00 as
    "no posture effect".
- Airburst ratios are nearly unaffected (1.60 vs 1.70 at 10 m).

The marker's stated reason ("only the private `_expected_kills_3d_vec`") is
weaker than it reads. N_eff_cross is already computed inside the public
function and only its transform is returned. The remedy is one extra result
field in `arty` (a modeler item). It is not a new accessor, and it must not
be −ln(1−P) inlined in the `.qmd`, which would be new math in a notebook.
Impact: no ordering change. Ground-burst contrast understated ×1.5–3 at
5–10 m; one misleading 1.00 cell. Tier stands at deferrable. Suggest
rewording the marker: "N_eff_cross is computed but not returned by
compute_frag_field_3d".

**F3 — Deferrable. Item 7's own expected outcome is not checked, and does not
hold.** Item 7 (derivation §7) predicts that ground-burst prone "drop[s] to
near-zero". The model floors the ratio at A_p(0) prone/standing = 0.176.
Probe values: 0.19–0.23 at 10–50 m, and 0.28–0.33 on lethal area. Neither
§6.6.1 nor the status paragraph says the expectation was only
qualitatively met. Impact: no rendered number changes; the derivation's
stated prediction is ~×5 off what the model produces. Correction: add one
line to the status paragraph (derivation.md:445) saying the ground-burst
prone ratio floors at h_prone/h_standing ≈ 0.18, not ~0.

**F4 — Note. Burst heights and δ are representative.** h_b = 0.5 m and 20 m
bracket contact/near-surface and the top of the typical proximity-fuze band.
δ = 15° is the model default. Under the airburst neither posture reaches
P_kill 0.5 (max 0.15 / 0.31), which the prose discloses. No action.

**F5 — Note. Layering and one-home are clean.** §6.6.1 renders every number
inline and imports all physics from `arty`. The crossover search is an
argmax over a sampled curve (display only). Values in the derivation status
paragraph are backed by the retained check script. The check script
duplicates the notebook's shell construction by hand (`wall_t=0.011`) where
the notebook uses `_parameters.qmd`. They currently match; drift risk only.

### Tier of the replacement marker

`deferrable` is correct for the substitution itself (F2). It does **not**
cover F1. F1 is a separate, Blocking defect in the conclusion drawn, and it
exists even with a perfect hit-count ratio: N_eff shows the same AoF = 0°
flip.

### Limitation entries (once F1 is fixed)

- `_limitations.qmd`: "The posture crossover in §6.6.1 is shown at
  AoF = 0°, the only geometry that places the belt directly beneath an
  airburst. Belt arrival elevation is bounded by ≈ 90° − AoF + δ, so at
  realistic angles of fall the airburst narrows the prone advantage rather
  than reversing it (field lethal-area ratio prone/standing 0.92 at
  AoF 30°, h_b 20 m)." Render the number from `arty` output, not typed.
- F2 marker reworded as above; it stays open.

## Re-review — adversarial, 2026-09-26 (fix cycle 1)

Scope: F1–F3 of "Review pass 1 — adversarial critique" only. Reviewed the
uncommitted diff to `_four-zone-3d.qmd` §6.6.1, `_change-log.qmd` 0.16.0,
`_limitations.qmd` entry 20, derivation.md status paragraph,
`src/arty/fragmentation.py` (`n_eff_cross`, `lethal_area`), and
`tests/test_frag_field_3d_neff_lethal_area.py`. R50 (cd453da) is out of scope.
`collect-findings.py --for experiment/fragmentation-field` lists no open
finding on `updates/target-area-profile/`, `_four-zone-3d.qmd` or
`_limitations.qmd`. The one open item touching `_change-log.qmd` (inline R50
argmin, r50-not-reached) is about other entries, not 0.16.0.

Evidence script (reviewer probe, **must be moved** by the main agent to
`updates/target-area-profile/checks/posture-lethal-area-grid-extent.py`):
`experiment/fragmentation-field/updates/target-area-profile/checks/posture-lethal-area-grid-extent.py`. It recomputes
`lethal_area` prone/standing at 1 m spacing for box half-extents
60/100/150/200/250 m, M1 105 mm, δ = 15°. Runtime ~32 s. The new tests pass
(3/3).

### Verdict: PASS-with-limitations

F1–F3 are resolved. At the default and realistic AoF, §6.6.1 now claims no
more than holds. The fix adds one new finding, R1: the lethal-area box is too
small. R1 does not change the realistic-AoF conclusion, which gets
*stronger* once the box converges. But it makes one rendered sentence false in
the non-representative AoF ≤ 15° regime. It is a one-parameter fix and should
land before commit rather than be logged.

### Status of pass-1 findings

**F1 — Resolved.** §6.6.1 now labels AoF = 0° as "the extreme case … not
representative of howitzer fire". It states the γ_max ≈ 90° − AoF + δ bound.
It keeps "the ordering does flip" to the AoF = 0° slice, and the per-point
N_eff flip on that slice is real. It gives the reader the default-AoF
whole-field result: narrows, does not reverse. `_change-log.qmd` 0.16.0 and
the derivation status paragraph (i) match. Numbers render inline. See R1 for
the one remaining false sentence.

**F2 — Resolved.** Ratios now use `n_eff_cross`, and the prose explains why.
The r = 0 ground-burst cell is described as P_kill saturation, and its N_eff
ratio is the A_p(90°) ceiling. Deleting the marker is legitimate because the
substitution it recorded no longer exists. `n_eff_cross` is the same
`N_eff_cross` array from which `pk_cross = 1 − exp(−N_eff_cross)` is built
(fragmentation.py, `compute_frag_field_3d`). A test pins the identity to
1e-12.

**F3 — Resolved.** Status (ii) states the A_p(0) floor 0.15/0.85 ≈ 0.18
(model: 0.176) and a lethal-area ratio of ~0.3. That matches the converged
0.29–0.31 in the probe. The notebook's closing sentence renders the floor
inline.

### New findings

**R1 — Deferrable (fix before commit recommended). The 120 m × 120 m box
truncates the airburst field, and the one field-level "flip" is a truncation
artefact.** (`_four-zone-3d.qmd` §6.6.1 `tbl-posture-lethal-area-aof`,
`max_radius=60.0, n_grid=121`; the prose "On this grid the 20 m airburst
ratio exceeds 1 only at AoF ≤ … °"; limitation 20's rendered value;
`checks/posture-crossover-ground-vs-air.py:24`.) At the 60 m edge the
airburst P_kill is still 0.016 for standing and 0.008 for prone. Standing
loses more area to truncation, because its far field (low γ) is where standing
presents more. So truncation biases the ratio **upward**, toward a flip.
Prone/standing lethal area at h_b = 20 m:

| AoF | box ±60 m (notebook) | ±150 m | ±250 m (converged) |
|---|---|---|---|
| 0° | 1.135 | 1.001 | 0.986 |
| 15° | 1.077 | 0.955 | 0.942 |
| 30° (default) | 0.918 | 0.826 | 0.816 |
| 45° | 0.759 | 0.692 | 0.683 |
| 60° | 0.614 | 0.550 | 0.543 |
| 75° | 0.480 | 0.427 | 0.418 |

Near-ground burst (h_b = 0.5 m) moves only 0.30 → 0.29 at AoF 30°. Standing
airburst lethal area is under-counted by 19% at AoF 30° (184.9 vs 229.0 m²).
The ±60 m box misses up to ~50% at AoF 75°.

On the converged field, the whole-field ratio is **below 1 at every AoF**.
Near-horizontal fire (AoF = 0°) reaches only parity, 0.99. The per-point flip
at AoF 0°, x = 0 stands, because it is a slice property.

Impact:
- At default and realistic AoF there is no qualitative change. The rendered
  0.92 becomes 0.82, a ×1.12 overstatement of the airburst narrowing.
- In the AoF ≤ 15° regime, the rendered "exceeds 1" sentence becomes false.
  The table's AoF 0°/15° rows move 1.14/1.08 → 0.99/0.94.
- Once the box is widened, `flip_aofs` is empty and `max(flip_aofs)` raises
  `ValueError`, so the notebook stops rendering. The sentence has to change,
  not only the grid.

Tier: deferrable by the materiality rule, since the qualitative change is
confined to a regime the section itself labels non-representative. This
corrects my own pass-1 F1 table, which used the same ±60 m box. Its
"above 1 only for AoF ≲ 20°" is the same artefact.

Suggested correction:
- Run the lethal-area sweep with `max_radius=200.0, n_grid=401`. That is
  converged to <1% and costs a few seconds for the 12 runs.
- Keep the per-slice panel at ±60 m. It is fine there.
- Replace the flip sentence with the converged fact: the whole-field ratio
  stays ≤ 1 at every AoF and only reaches parity (~0.99) at AoF = 0°.
- Make the "120 m × 120 m grid" wording in the prose match the new box.
- Apply the same box to `checks/posture-crossover-ground-vs-air.py` and
  the derivation status paragraph. "~0.3 → ~0.9" should read ~0.3 → ~0.8.

**R2 — Note. The γ_max statement slightly over-restricts where the belt
reaches vertical.** The prose says "Only a horizontal shell (AoF = 0°) puts
the belt directly beneath the burst". Limitation 20 says "the only geometry
that puts the belt directly beneath an airburst". But the prose's own bound
90° − AoF + δ reaches 90° for any AoF ≤ δ, which is AoF ≤ 15° at the default
δ. What is unique to AoF = 0° is that the x = 0 cross-range *slice* lies in
the belt. Impact: none on any number. Suggested wording: "reaches vertical
only for AoF ≤ δ; the x = 0 slice lies in the belt only at AoF = 0°."

**R3 — Note. The `arty` additions are pure read-outs.** `n_eff_cross` returns
the already-computed `N_eff_cross` with a `None` default, so existing
constructors are unaffected. `lethal_area` is `field_pk.sum()·dx·dy`, and the
spacing reads match the meshgrid convention (X along columns, Y along rows).
No model value changes. Edge: `n_grid = 1` would raise `IndexError`, and the
sum covers the (2R + dx)² cell-centred box. Neither matters here.

**R4 — Note. The two notebook ratios do not breach the no-physics-in-.qmd
rule.**
- `ap_prone[0]/ap_stand[0]` is a ratio of two `presented_area` returns.
- `la["prone"]/la["standing"]` is a ratio of two `lethal_area` returns.
- The N_eff ratios are ratios of `n_eff_cross` samples.

Each is a dimensionless comparison of two quantities that `arty` returns. None
encodes a new physical quantity, and each is the posture contrast the section
exists to display. That makes them presentation under Gate 2. The aggregate
that *was* new math, ΣP_kill·dA, now lives in `arty`, as pass 1 required.
Same for the `argmax` crossover, the `> 1.0` filter and `slice_at`'s
`np.interp` read-out, which do display-level lookup and no physics.

**R5 — Note. Limitation 20 is accurate apart from R1 and R2.** It correctly
confines the per-slice ratios to AoF = 0° and names field lethal area as the
realistic measure. Its rendered number inherits R1: 0.92 now, 0.82 once
converged. Its "only geometry" wording inherits R2.

### Limitation entries

If R1 is fixed as suggested, limitation 20 needs only the R2 wording tweak.
The number then renders at the converged value. If R1 is **not** fixed,
append to limitation 20: "Field lethal area is summed over a ±60 m box that
truncates the airburst far field (standing under-counted ~19% at AoF 30°).
The ratio is biased upward, and the AoF 0°–15° rows above 1 are a truncation
artefact. Converged values are 0.99/0.94/0.82."

## Review pass 2 — verification, 2026-09-26

**Scope:** Uncommitted change since the re-review (R1, R2, R5 fix). Specifically:
`_four-zone-3d.qmd` §6.6.1, `_change-log.qmd` 0.16.0, `_limitations.qmd`
entry 20, `updates/target-area-profile/derivation.md` status paragraph,
`src/arty/fragmentation.py` (`n_eff_cross` / `lethal_area`),
`tests/test_frag_field_3d_neff_lethal_area.py`, and the four scripts in
`updates/target-area-profile/checks/`. The R50 change (cd453da) is out of scope.

### Verdict: PASS

No Blocking findings. All prior R-findings resolved. One Note on script runtime.

______________________________________________________________________

### What was checked

**1. Check scripts — all run clean, outputs match notebook.**

`posture-crossover-ground-vs-air.py` (run standalone):
- γ* = 43.5° at A_p = 0.720 m² ✓ (notebook inline: `gam_x_deg`, `ap_x`)
- A_p(0) prone/standing = 0.176 ✓ (notebook: 0.18 at 2 dp)
- N_eff ratios at 0/10/20 m: ground burst 6.00/0.23/0.20, airburst 6.00/1.70/1.05 ✓
- Airburst P_kill max = 0.314 → notebook renders 0.31 ✓
- Lethal-area ratios (±200 m, 401 pts): AoF 0°→ 0.31/0.99, 30°→ 0.28/0.82, 75°→ 0.27/0.42 ✓

`posture-lethal-area-convergence.py` (run standalone, ~90 s wall time):
- All d_ratio values for the (200, 401) grid vs the (300, 601) reference are within 1%:
  worst case AoF=75°, h_b=20: +0.75%. The derivation's "within 1%" claim is supported.
- Notebook grid (±200 m, 401 pts) renders AoF=30°/h_b=20 ratio 0.818, rounds to 0.82 ✓;
  AoF=0°/h_b=20 gives 0.990, flip_text renders 0.99 ✓.

`posture-lethal-area-grid-extent.py` and `posture-crossover-robustness.py` present, each
has a correct docstring naming its consumer document. Both run cleanly (confirmed by prior
passes; the grid-extent script is the R1 evidence from the re-review).

**2. `n_eff_cross` and `lethal_area` traced by hand.**

`n_eff_cross`: added as `n_eff_cross: np.ndarray | None = None` on `FragField3dResult`; the
`compute_frag_field_3d` return path appends `n_eff_cross=N_eff_cross` (already computed).
`None` default leaves every existing constructor untouched. No model value changes. ✓

`lethal_area`: reads `dx = field_x[0, 1] - field_x[0, 0]` and `dy = field_y[1, 0] -
field_y[0, 0]`. With the meshgrid convention (X varies along columns / axis-1, Y along
rows / axis-0), `field_x[0, 1] - field_x[0, 0]` gives the column step (X spacing) and
`field_y[1, 0] - field_y[0, 0]` gives the row step (Y spacing). For the ±200 m / 401-pt
grid: xy = linspace(−200, 200, 401) → spacing = 400/400 = 1 m; dx = dy = 1 m, cell area
= 1 m². Total box = 401×401 cells = 160 801 m² = (400+1)² m² (cell-centred). Correct. ✓

Test `test_lethal_area_is_pk_sum_times_cell_area` uses `dx = 80.0/40 = 2 m` for
`linspace(-40, 40, 41)` and checks `|lethal_area - field_pk.sum() * dx * dx| < 1e-9`. ✓

**3. All figures in new prose are inline `{python}` expressions — verified.**

Every number in §6.6.1 (γ*, A_p, N_eff and P_kill ratios, pkmax_air, all lethal-area
ratios, flip_text, AoF default, floor value) is an inline `{python}` expression bound to
a computed variable. No typed constant appears in the new prose. Limitation 20 likewise
renders all its numbers inline from `la_ratio`, `la_R`, `la_air_max_aof`, `aof_default`,
`hb_air` — all defined in the §6.6.1 cell that runs before the limitations partial is
included. ✓

**4. No physics leaked into the .qmd — verified.**

§6.6.1 computes: ratios of `presented_area(...)` returns, `np.interp` read-outs of
`n_eff_cross` / `pk_cross` (display-level lookup), ratios of `lethal_area` returns,
an `argmax` to locate the crossover on a sampled curve (display only), and a
Python string `flip_text` branching on whether any lethal-area ratio exceeds 1.
None encodes a new physical quantity. The one aggregate that is new physics,
ΣP_kill·dA, lives in `arty` as the `lethal_area` property. ✓

**5. Crash guard for empty `flip_aofs` — verified.**

`la_air_max_aof = max(aof_tab, key=lambda a: la_ratio[(a, hb_air)])` iterates over the
full `aof_tab` tuple, not over `flip_aofs`; it is always defined. The `if flip_aofs:`
branch (which calls `max(flip_aofs)`) is entered only when the list is non-empty. The
`else:` branch uses `la_air_max_aof` only. No ValueError path exists. ✓

Confirmed by the convergence output: no ratio exceeds 1.0 on the ±200 m grid, so
`flip_aofs` is empty and the else branch runs in the notebook — the rendered
`flip_text` says "stays below 1 at every AoF tabulated. It comes closest to parity,
0.99, at AoF = 0°." ✓

**6. Test suite — 230 passed, 1 skipped, 6 deselected (4.6 s).**

`test_n_eff_cross_is_inverse_of_pk_cross`, `test_lethal_area_is_pk_sum_times_cell_area`,
and `test_lethal_area_prone_below_standing_near_ground_burst` all pass. ✓

**7. Re-review R2 wording — resolved.**

The notebook now states: "γ reaches 90° (the belt directly beneath the burst) only for
AoF ≤ δ. The cross-range slice x = 0 lies in the belt only at AoF = 0°." This
distinguishes the belt-reaches-vertical threshold (AoF ≤ δ = 15°) from the slice-in-belt
condition (AoF = 0° only). Matches the R2 suggestion. ✓

______________________________________________________________________

### Findings

**V1 — Note. `posture-lethal-area-convergence.py` runs ~90 s wall time.**
The verification-scripts rule targets under ~30 s. The script runs 4 grid sizes × 12
field combinations × 2 postures = 96 `compute_frag_field_3d` calls; the slowest grid
(R=300, n=601) dominates at ~1.2 s per call × 12 = ~14 s compute, with ~22 s total
compute and ~90 s wall (import + flush overhead). The script is a one-time convergence
validation to justify the notebook's grid choice, not a per-pass recheck. The
`posture-crossover-ground-vs-air.py` script (the primary re-run candidate, ~12 s compute)
is within target. Impact: negligible — the convergence script need only be re-run if the
grid choice changes.

No further findings. Dimensional analysis, numerical stability, parameter bounds,
layering, one-home rule, and source attribution all pass. Change-log 0.16.0 entry is
accurate ("presentation only — no model value changes"). Limitation 20 is accurate and
consistent with the converged ratios.
