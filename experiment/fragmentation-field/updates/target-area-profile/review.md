# Review — angle-dependent presented-area profile $A_p(\\gamma)$

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
  M1 105 mm, AoF = 0°, δ = 15°): $R\_{50}$(standing) = 28 m vs
  $R\_{50}$(prone) = 14 m at $h_b$ = 0.5 m, crossing over to
  $R\_{50}$(standing) = 12 m vs $R\_{50}$(prone) = 18 m at $h_b$ = 20 m. This
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
  The $R\_{50}$-recalibration consequence of the $s^{-1}\\to s^{-2}$ geometry
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
  frozen $A\_{ref}=0.85$) are each independently caveated where they are used
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
$A_p$(PRONE), plus a small $R\_{50}$-or-$P_k$-at-fixed-range table comparing
low-$h_b$ vs high-$h_b$ bursts for both postures (the numbers reproduced in
this review — $R\_{50}$ 28m/14m at $h_b$=0.5m crossing to 12m/18m at
$h_b$=20m — are a ready starting point).

### 3. [Note] Three coexisting presented-area treatments, correctly caveated per panel

Not a target-area-profile defect — recorded for completeness. The Family-A
path (headline 2D field + diff map) uses live $A_p(\\gamma,\\text{posture})$;
the target-height-intercept ground field uses frontal-only $w\_\\perp h$
(γ=0 fixed); the point-in-space volume uses a frozen, posture-independent
$A\_{ref}=0.85$. Each is disclosed where used. No action needed.

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
   that motivates $A_p(\\gamma)$ is implemented and unit-tested at its γ=0/π/2
   endpoints but is not demonstrated end-to-end (γ-sweep, R₅₀ ratio) in any
   notebook cell; verified ad hoc during the 2026-07-19 review
   (`experiment/fragmentation-field/updates/target-area-profile/review.md`)."

No other findings. Dimensional analysis, numerical stability, parameter
bounds (posture dimensions disclosed as unsourced ±25% engineering
convention), and layering all pass.
