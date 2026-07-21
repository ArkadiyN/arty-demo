# Scoping — Family-A false safe zone (graded ground P(kill) heatmaps)

**Aspect:** close the false-safe-zone artefact in the **graded Family-A** ground
P(kill) fields — the app's headline single-zone and four-zone 2D heatmaps, their
difference map, and the cross-section slices. These use the
`presented_area(γ)·pk_given_hit(E)` belt-integral kernel, a *different governing
weighting* from the Family-B ρ_L→Poisson fields fixed in
`updates/target-height-intercept/`. Straight-line rays only; no gravity.

**Sibling / prior work (reference, not re-derived):**
- `updates/target-height-intercept/scoping.md` §5 explicitly defers this aspect
  and sketches two follow-on paths (ranked below). Its §3 Option 2 is one of them.
- `updates/target-height-intercept/derivation.md` + `review.md` — the accepted,
  implemented, reviewed Family-B fix (column integral `λ = w_perp∫₀ʰ ρ_L dz`,
  eq. 5 belt-breakpoint quadratic, composite-midpoint quadrature).
- `openspec/changes/archive/2026-07-19-target-height-intercept/proposal.md` —
  records Family-A as out of scope and that the app's headline heatmaps still
  call the Family-A path (a separate Family-B expander was *added*, not swapped in).

## 1 · Where the bug lives in Family-A (code audit, read fresh)

The headline app charts call, all evaluated on the ground plane `z = 0`:

| App chart | `app/sensitivity.py` | Family-A entry point |
| --------- | -------------------- | -------------------- |
| single-zone P(kill) heatmap | `compute_frag_field_3d` (L170) → `field_pk` | `_expected_kills_3d_vec`/`_point` (`fragmentation.py`) |
| four-zone P(kill) heatmap | `_four_zone_field_split` (L218) → `pk_total` | `_four_zone_familyA_eval` (`zones.py:453`) |
| four-zone − single-zone diff map | L812 (`pk_total − field_pk`) | both of the above |
| cross-section slices | `four_zone_line_split` (L308) | `_four_zone_familyA_eval` |

The Family-A per-cell kernel (`_four_zone_familyA_eval`, and the single-zone twin
`_expected_kills_3d_point`) is
`N = Σ_zone [ ∫ pdf·pk_given_hit(E(s))·A_p(γ) / (2π s²·2 sinθ^z·δ) dm ]`, gated by
the belt test `|cosΘ − cosθ^z| ≤ sinδ`, with **every geometric quantity taken on
the single ray to `(x,y,−h_b)`**: `s=√(x²+y²+h_b²)`, `γ = arcsin(h_b/s)`,
`cosΘ = (x cosα + h_b sinα)/s`. `P_k = 1 − exp(−N)`.

**Crucial distinction from Family-B — the presented area already carries the
target height.** `presented_area(γ,posture) = w_perp·(h·cosγ + d·sinγ)`
(`fragmentation.py:190`): the `h·cosγ` frontal term *is* the vertical silhouette
and the `d·sinγ` term is the top-down footprint. So Family-A does **not** ignore
the target's vertical extent in the *silhouette* — it already integrates it into
a lumped scalar `A_p`. The defect is narrower: the **belt gate and arrival
geometry (`s,γ,cosΘ`) are sampled only along the ray to the feet (`z=0`).** At
steep AoF near the burst the belt fails the `z=0` gate and the whole cell zeros,
even though the belt crosses the ray to the chest/head. This is the same
false-safe symptom as Family-B but a different lever: Family-B was missing the
*height in the silhouette*; Family-A is missing the *height in the field
geometry*.

This immediately disqualifies a naive "integrate the Family-A kernel over `[0,h]`"
fix: `A_p` already contains `w_perp·h`, so `∫₀ʰ A_p(γ)…dz` **double-counts the
height**. The correct Family-A fix relocates *where the field is evaluated*, not
the silhouette size.

## 2 · Options

### Option 1 — migrate the headline heatmaps onto the fixed Family-B field
Repoint the four app charts from the Family-A functions to
`four_zone_pkill_field`/`pkill_field_3d`/`four_zone_pkill_line`; delete no
Family-A code (still used by the notebook / diff). Family-A needs no fix.

- Constraint: straight-line, inherited from Family-B. PASS.
- Cost: near-zero physics; small app rewiring.
- **What it does to the graded weighting: destroys it.** Family-B replaces
  `pk_given_hit(E)` (graded ES-310 energy roll-off) and the `A_p(γ)` obliquity
  with a **binary** lethal-mass cut (`E_leth=1000 J`, `P_{k|hit}=1` once counted)
  + Poisson. The headline map would stop being the graded field that is the whole
  reason Family-A exists.
- **Feature loss:** `four_zone_pkill_field` returns only `(X,Y,P_k)` — no
  per-zone breakdown, and the single-vs-four-zone **difference map** (L812) and
  zone-lobe attribution collapse (both operands become the same Family-B
  quantity). The archived proposal already ruled the two families "not the same
  quantity at different resolution" and therefore added Family-B as a *separate*
  expander rather than a replacement — this option contradicts that decision.
- **Rejected:** cheapest, but abandons the distinct Family-A physics and two
  headline features to do it.

### Option 2 — relocate the Family-A belt gate + geometry to the illuminated column *(recommended)*
This is `target-height-intercept` scoping §5's second path (its §3 Option 2).
Keep the graded kernel `A_p(γ)·pk_given_hit(E)` **intact**; change only the gate
and the height at which the ray geometry is read: a cell fires when the belt
illuminates **any** part of the target column `[0,h]`, and `s,γ,cosΘ` (hence
`A_p`, `E`, the mass integral) are evaluated at the **illuminated height**, not
at `z=0`.

- The belt∩column membership is already solved, derived and reviewed: reuse
  `belt_column_breakpoints` (`fragmentation.py:577`) — it takes `cos_theta_z` as a
  list and already generalises to the single-zone `[0]` and four-zone belts, via
  the closed-form quadratic eq. (5). No new geometry, no new literature.
- Constraint: straight-line — the intercept is the same algebraic belt-edge solve,
  no trajectory integration. PASS.
- **Graded weighting preserved exactly.** The kernel, `pk_given_hit`, `A_p(γ)`,
  the per-zone `1/sinθ^z`, the diff map and per-zone attribution all survive; only
  the evaluation height moves.
- Cost: moderate, bounded. Edit `_four_zone_familyA_eval` and
  `_expected_kills_3d_vec/_point`; the per-cell mass integral `J(s)` is still
  evaluated **once per cell** (at the representative `s`), so the hot vectorised
  path stays O(cells), unlike Option 3.
- Reduction-to-current: when the belt already floods the column (low AoF, open
  footprint) the illuminated segment includes `z=0`, so choosing the
  representative height to recover the `z=0` evaluation there reproduces the
  shipped value. Satisfies the acceptance criterion.
- **Two design forks for the derivation pass** (do not pre-decide here):
  1. *Representative height.* Where in belt∩column to read `s,γ,cosΘ` — e.g. the
     belt-centre crossing height (`cosΘ = cosθ^z`) clamped to `[0,h]`, or the
     segment midpoint. Must reduce to `z=0` when the segment reaches the ground.
  2. *Illuminated-fraction weighting.* A single representative height makes the
     cell value **jump** from full-`A_p` to 0 at the inner ring edge
     (`r ≈ (h_b−h)/tanδ`, belt lifting off the head), and **over-counts** when the
     belt grazes only a sliver of the column (full standing silhouette scored for a
     head-only strike). Scaling `A_p` by the illuminated column fraction
     `(z_hi−z_lo)/h` restores a smooth taper (matching Family-B's behaviour there)
     and removes the over-count, at the cost of not reducing to current on
     partially-lit-but-`z=0`-crossing cells — acceptable, since the Family-B fix
     read "reduce to current" as the *fully-flooded* limit (its derivation §6.2),
     not every `z=0`-crossing cell. The derivation should adopt fraction-weighting
     unless it breaks the flooded-limit check.

### Option 3 — full graded flux integral (unbundle `A_p`, "graded Family-B")
Re-derive Family-A as a height-resolved flux density: replace `A_p(γ)` with a
per-height frontal strip `w_perp·cosγ(z) dz` carrying the graded `pk_given_hit`,
integrated over the illuminated segment, plus a separate top-down `w_perp·d·sinγ`
patch — i.e. Family-B's column integral with the graded kill weighting restored.

- Constraint: straight-line. PASS. Physically the most faithful (both height *and*
  graded weighting resolved).
- **Cost: high, and it erodes the family split.** The mass integral `J` now
  depends on `s(z)`, so it must be evaluated at every `z`-node → `n_seg×` the mass
  integrals per cell in the hot vectorised path. It is a **new governing-equation
  set** needing its own derivation, double-count-avoidance care (the `A_p`
  unbundling), a top-down patch to reduce to current, and its own review. The
  result is a third field that is neither cleanly Family-A nor Family-B, muddying
  the two-family comparison and the diff map that justify keeping both.
- **Rejected as the primary fix:** disproportionate for a false-safe-zone closure
  when Family-A's own lumped-silhouette philosophy is internally consistent with
  Option 2. Worth recording as a *future refinement* if a vertically-graded field
  is ever wanted, not this change.

## 3 · Literature audit

No new external literature is required. The belt-edge intercept is closed-form
geometry (derived + reviewed in `target-height-intercept`). `presented_area(γ)`
is NATO casualty-modelling convention (Cunniff 2014 / AEP-55 Vol. 3), already
flagged as **not present in `doc-reference/`** in `_limitations.qmd` #12 —
unchanged by this aspect (absolute posture-resolved counts stay ±25 % engineering
estimates). `pk_given_hit` is the ES-310 curve, already cited. No `@librarian`
pass needed.

## 4 · Recommendation

Adopt **Option 2** — relocate the Family-A belt gate and ray geometry to the
illuminated column segment, keeping the graded `A_p(γ)·pk_given_hit(E)` kernel
intact. It is the only option that (i) closes the false safe zone on the headline
charts, (ii) **preserves** the graded weighting and the diff/zone-attribution
features that make Family-A distinct, (iii) reuses the already-derived-and-reviewed
`belt_column_breakpoints` machinery so it is straight-line-compliant by
construction and cheap (one mass integral per cell), and (iv) reduces to the
shipped values in the flooded regime. Option 1 destroys the graded physics;
Option 3 is a disproportionate new kernel.

The derivation pass should:
1. State the relocated evaluation: gate on belt∩`[0,h]` non-empty via
   `belt_column_breakpoints`; evaluate `s,γ,cosΘ,A_p,E,J` at the representative
   illuminated height. Confirm it reduces to the shipped `z=0` kernel when the
   segment reaches the ground (acceptance criterion 2).
2. Resolve the two forks — representative-height rule and illuminated-fraction
   weighting (§2 Option 2) — with a flooded-limit self-consistency check and the
   inner-edge honesty check (`r < (h_b−h)/tanδ`: belt overhead, `P_k≈0`, correct).
3. Give the unit/limit checks mirroring the Family-B fix: at AoF=90°, `h_b=2`,
   standing/prone, near-burst ring `P_k > 0` (was 0 for `r<7.5 m`); prone column
   capped at `h=0.3` correctly less exposed than standing near a low high-angle
   burst; `P_k∈[0,1]`, monotone non-decreasing in `h`.
4. Log the retained lumped-silhouette approximation (Family-A resolves the graded
   energy/obliquity weighting but not vertical flux structure — the dual of
   Family-B's tradeoff) as a limitation, distinct from the Family-B entry.

## 5 · Scope boundary

This aspect touches **only** the Family-A ground-field evaluation
(`_four_zone_familyA_eval`, `_expected_kills_3d_vec/_point`, and the line/field
wrappers that call them). It does **not** modify the Family-B ρ_L/Poisson fields
or their volume builders (separate, already-fixed aspect), the ρ_L kernel, or
`fragment_ground_impact` (feeds no field — `target-height-intercept` scoping §1).
