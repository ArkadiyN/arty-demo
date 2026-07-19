## Context

The Family-B ρ_L → P(kill) ground fields (`four_zone_pkill_field`, `pkill_field_3d`,
and the app's line-slice variant) evaluated lethal fragment density at `z = 0` only,
producing a false safe zone at steep angle of fall: near the burst, the spray belt
sprays near-horizontally through burst height and never crosses the ground plane,
so those cells read `P(kill) ≈ 0` even though a standing or prone person occupying
that column would be struck.

Root-cause and options analysis were done in a modeler scoping pass
(`experiment/fragmentation-field/updates/target-height-intercept/scoping.md`).
Physics derivation, `src/arty/` implementation, and notebook presentation have
since been completed and independently reviewed to PASS
(`experiment/fragmentation-field/updates/target-height-intercept/derivation.md`).
This design document records the decisions made during that work, per
`.claude/rules/agents-routing.md`'s ordering: the notebook derivation and review
happen first, and the OpenSpec artifacts document the already-confirmed approach
rather than prescribing it in advance.

## Goals / Non-Goals

**Goals:**

- Replace the single-plane `z = 0` sample in the Family-B ground P(kill) transform
  with a vertical-extent integral over the target's height column `[0, h]`, reusing
  the already z-resolved ρ_L kernel.
- Re-couple posture sensitivity (standing vs. prone `h`, `w_perp`) to the ground
  P(kill) fields, which the previous frozen `A_ref = 0.85 m²` constant discarded.
- Preserve straight-line fragment trajectories — no gravity or ballistic curvature.
- Keep the 3D `P(kill)(x,y,z)` volume view (`pkill_volume_3d` /
  `four_zone_pkill_volume`) computationally unchanged; it already answers a
  different question (point-in-space lethality) and needs no fix.

**Non-Goals:**

- Fixing the analogous false-safe-zone symptom in the graded Family-A fields
  (`four_zone_field`, `compute_frag_field_3d`, the app's headline 2D heatmaps).
  These use a different governing weighting (`presented_area(γ)·pk_given_hit(E)`)
  and are a separate, independently PASS/FAIL-able model aspect — deferred to a
  future change per the scoping pass's decompose-first rule.
- Changing `fragment_ground_impact` (the spray-cone dot renderer) — it feeds no
  field and is out of scope for closing the false safe zone in any app heatmap.

## Decisions

**D1 — Vertical-extent flux integral over the frozen-`A_ref` alternative.**
`P_k = 1 − exp(−w_perp·∫₀ʰ ρ_L(x,y,z) dz)` replaces
`P_k = 1 − exp(−ρ_L(z=0)·A_ref)`. The old transform is the degenerate
constant-density limit of the new one. Chosen over keeping `A_ref` frozen because
the frozen constant discards posture entirely (standing and prone produced
identical ground fields), while the integral naturally re-couples `h` and
`w_perp` per posture. Cost is cheap: reuses the volume kernel's per-layer
belt/Mott/drag evaluation already used by `four_zone_pkill_volume`.

**D2 — Composite-midpoint quadrature over uniform trapezoid and endpoint-inclusive
piecewise trapezoid.** The belt-membership test (`lethal_density_point`'s
`|cosΘ| ≤ sinδ` gate) is a hard 0/1 discontinuity in `z`, not smooth. Three
quadrature designs were tried, in order:

1. *Uniform trapezoid* — rejected: non-monotone error up to 34% as `n_z`
   increases, because naive trapezoid nodes don't align with the belt edge.
1. *Analytic belt-edge crossing + endpoint-inclusive piecewise trapezoid* —
   rejected: evaluating exactly at the analytic breakpoints hit floating-point
   coin-flips against the independently re-derived belt gate, an `O(1/n_seg)`
   bias (−5.45% at `n_seg=9`, only halving at `n_seg=18` — invisible to a
   doubling-convergence check).
1. *Composite-midpoint on the analytic breakpoints* (accepted) — all quadrature
   nodes are strictly interior to each smooth sub-interval, so no node ever
   lands exactly on the discontinuity. Verified to \<0.005% error across a dense
   59-point r-sweep. `n_seg=9` is the default.

Belt-edge crossings are found via a closed-form quadratic (per-zone generalized
as `A=sin²α−K²`, `K=cosθ^z±sinδ`), using the numerically-stable root form
(Numerical Recipes §5.6) rather than the naive `(−B±√disc)/(2A)` form, which
suffers catastrophic cancellation as `A→0` (angle-of-fall approaching the spray
half-angle).

**D3 — `slant_range_grid`'s `s_max` widened to `max(|z_min−h_b|, |z_max−h_b|)`.**
Needed so the drag-attenuated velocity/Mott tables cover the full slant-range
span exercised by the column integral, not just the old single-plane range.

**D4 — 3D volume view left computationally untouched.** Confirmed in scoping
(§2): the volume already evaluates ρ_L at arbitrary height, so it already shows
near-burst horizontal-fragment lethality at torso height. The fix only changes
the ground-map transform; the volume's app caption may be reworded for clarity
(presentational only, not part of this change's `src/arty/` scope).

**D5 — App exposure: new standalone Plotly heatmap, not a Family-A diff.**
Reopened after the change was initially marked complete: the app had no
consumer of the fixed transform at all (its 2D heatmaps and cross-section
slices are Family-A). Decided, after discussion:

- A new `go.Heatmap`-based Plotly view (matching the app's existing 2D-heatmap
  visual style — `YlOrRd`, `_r50_contour` overlay, burst-point marker), not a
  reuse of the notebook's matplotlib `fig_pkill_field` helper, which is
  presentation-only for the Quarto notebook and stylistically inconsistent
  with the app's interactive Plotly views.
- Its own new `st.expander`, structurally mirroring the existing "3D Kill
  Probability" expander (independent view-radius slider, grid-resolution
  `select_slider`, cached compute function, single-zone/four-zone branching),
  placed next to it — not folded into the existing Family-A heatmap section.
- **No diff/comparison against the Family-A heatmaps.** Rejected: an early
  proposed option was a side-by-side diff map, by analogy with the app's
  existing single-zone-vs-four-zone diff. That existing diff is valid because
  both sides are the *same* governing equations (Family A) at different
  zone-geometry granularity. Family A and Family B are different physical/
  probabilistic models (graded per-hit energy-based lethality vs. binary-
  threshold Poisson "≥1 hit") answering different questions, not two estimates
  of the same quantity — a diff map would misleadingly imply otherwise.

## Risks / Trade-offs

- [Risk] Quadrature accuracy still has a residual near-burst caveat for
  pathological configurations not exercised by the worked examples (derivation
  §7, assumption A4) → Mitigation: composite-midpoint's \<0.005% error was
  confirmed across a dense r-sweep; the stable quadratic root form removes the
  specific `A→0` cancellation failure mode identified in review.
- [Risk] `four_zone_pkill_line` (new Family-B line helper) risked shipping
  unused/untested → Mitigation: exercised and tested in the notebook
  presentation pass; four-zone posture/false-safe-ring regression test added
  (`test_four_zone_pkill_field_posture_and_false_safe_ring`) to close the parity
  gap with the existing single-zone test.
- [Risk] Notebook presentation of the fix can silently rely on grid-resolution
  coincidences when reporting threshold-crossing statistics near a hard belt
  edge → Mitigation: caught in review (PRONE ring-fill read a spurious 0% at one
  specific `n_grid`); fixed by reporting on a resolution-confirmed dense
  near-field grid and a grid-stable onset radius instead of a single coarse-grid
  percentage.
- [Trade-off] The fix is scoped to Family B only; Family A ships with the same
  symptom until its own change lands. Accepted per the decompose-first rule —
  bundling both would mix two independently reviewable governing-equation sets
  into one change.
- [Risk] The original proposal's Impact section claimed the app would "pick up
  the new transform with no call-signature changes" — false: the app's 2D
  heatmaps and cross-section slices call the unaffected Family-A path, so the
  fix shipped in `src/arty/` with zero app-visible effect. Caught when the user
  asked to verify the app change before testing it live → Mitigation: change
  reopened (D5) to add a dedicated app section; verify app-impact claims
  against actual call sites in future proposals, not just capability names.

## Migration Plan

No data migration. This changes the transform used by `four_zone_pkill_field`,
`pkill_field_3d`, and the app's line-slice consumers; call signatures are
unchanged aside from adding the `posture` parameter (already the existing
`PostureParams` type used elsewhere in `arty`). Rollback is a plain revert of
the `src/arty/fragmentation.py` / `src/arty/zones.py` commit — no schema or
stored-state changes to unwind.

## Open Questions

- None outstanding for this change. The deferred Family-A aspect (§ Non-Goals)
  is tracked as a candidate future change, not an open question here.
