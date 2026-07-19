# Scoping — target-height fragment intercept (false safe zone fix)

**Aspect:** replace the ground-plane-only (`z = 0`) fragment acceptance in the
P(kill) ground fields with a target-height-aware intercept, so fragments passing
through the vertical extent a standing/prone person occupies are counted. No
gravity; fragments stay straight-line rays.

**Symptom (already diagnosed, `_limitations.qmd` §184–204):** at steep angle of
fall the near-burst ground map shows a false safe ring. At AoF = 90° the
cylinder belt (θ_z = 90°) sprays horizontally through burst height and never
reaches `z = 0` near the burst, so ground cells there read P(kill) ≈ 0 even
though a standing soldier would be struck at chest height.

## 1 · Where the bug actually lives (code audit)

There are **two** field families in `src/arty`; the false safe zone is a
property of *evaluating either at `z = 0` only*, not of any single function.

| Family                                                  | Functions                                                                                                                                    | Evaluated at                                   | Acceptance                           | Feeds                                                       |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------ | ----------------------------------------------------------- |
| **A. graded target-coupled**                            | `_expected_kills_3d_point`/`compute_frag_field_3d` (single); `four_zone_field`, `_four_zone_field_split`, `four_zone_line_split` (four-zone) | ground `z = 0` (ray to `(x,y,−h_b)`)           | spray-belt \`                        | cosΘ−cosθ_z                                                 |
| **B. target-independent ρ_L density → Poisson P(kill)** | `lethal_density_*`, `four_zone_lethal_density_field/volume`, `four_zone_pkill_field/volume`, `pkill_volume_3d`                               | **arbitrary height `z` (already a parameter)** | same belt test, no `z=0` restriction | ρ_L 2D view (`z=0`) + 3D volume (`sensitivity.py` 955–1008) |

Key finding: **`fragment_ground_impact` (the function named in the limitation
note and the brief) is not used by any field.** Its only callers are the
`plots.py` spray-cone dot renderer (line 629) and the `_four-zone-3d.qmd`
notebook. Modifying *it* alone (the limitation note's literal candidate,
Option 3 below) would not touch a single app heatmap. Implementation must not
chase that function.

## 2 · The 3D-volume interaction — resolved

**The 3D P(kill) volume view is not affected by the bug and needs no physics
change.** Family B (`four_zone_pkill_volume` / `pkill_volume_3d`) already
evaluates ρ_L at every height `z`, so at torso height near the burst it already
reports the horizontal-fragment lethality the `z = 0` map is missing. The false
safe zone is *only* a `z = 0`-slice artefact.

But the volume and the fix are **complementary, not redundant**, because they
answer different questions:

- 3D volume: "P(kill) for a *point* target sitting at spatial point `(x,y,z)`."
  A spatial diagnostic of where lethal density is high.
- Fixed 2D ground map (what the fix produces): "P(kill) for a *standing person*
  whose feet are at ground `(x,y)`, occupying the whole column `z ∈ [0,h]`."

A standing person is a **vertical target**; the correct ground-map P(kill)
aggregates the field over their vertical extent, not a single `z = 0` (nor a
single arbitrary `z`) sample. So the fix reuses the volume's own z-resolved
kernel but collapses it over `[0,h]` — it does **not** modify how the volume is
computed. The only volume-side change is presentational (the app caption should
say the volume is a point-in-space field, distinct from the standing-person
ground map).

**Decompose verdict: this is ONE model aspect.** The 3D-volume question is
resolved as "no physics change," so it is not split into a dependent change.
(A second, genuinely separate aspect is flagged in §5 — the graded Family-A
posture fields — but it is *not* scoped here.)

## 3 · Options

### Option 1 — vertical-extent aggregation of the ρ_L field *(recommended)*

Replace the single `z = 0` sample in the P(kill) transform with the field
integrated over the column the person occupies. Physically, for a vertical
target of width `w_perp` spanning `[0,h]`, the expected lethal intercepts are

`N_leth(x,y) = w_perp · ∫₀ʰ ρ_L(x,y,z) dz`, `P_k = 1 − exp(−N_leth)`,

which is exactly the straight-line "does a lethal ray cross the target volume
`[0,h]`" test written as a field integral over the *already-correct* z-resolved
ρ_L kernel (Family B). The current `P_k = 1 − exp(−ρ_L(z=0)·A_ref)` is the
degenerate case where the whole silhouette is assumed to see the `z = 0`
density; the fix samples the density the target actually spans.

- Constraint check: uses only the existing straight-line belt geometry — no
  trajectory curvature, no gravity. PASS.
- Cost: reuses `four_zone_lethal_density_volume`'s per-layer kernel; a few `n_z`
  layers over `[0,h]` and a trapezoid in `z`. Cheap; no new root-finding.
- Bonus: naturally re-couples posture (h, w_perp differ standing vs prone),
  closing the "P(kill) view ignores the posture toggle" gap where the frozen
  `A_ref = 0.85` currently discards it. Design fork for the derivation: keep
  `A_ref` frozen vs. use `w_perp·∫dz` (the physical choice). Recommend the
  latter and re-anchor `A_ref` as a diagnostic default only.

### Option 2 — explicit ray/target-volume intercept in the graded Family-A loop

Rework the belt-test loop of `_expected_kills_3d_point` / `four_zone_field` so a
cell fires when the belt's vertical intersection with the column `[0,h]` at
`(x,y)` is non-empty, retaining `presented_area(γ)·pk_given_hit(E)`.

- Constraint check: straight-line, PASS.
- Heavier surgery inside a target-coupled integrand; keeps the graded weighting
  but is a separate governing equation set (see §5). Not the minimal fix.

### Option 3 — literal `fragment_ground_impact` volume-intercept (limitation-note candidate)

Change `fragment_ground_impact` to test intersection with `[0,h_person]` instead
of `z = 0`.

- **Rejected as the primary fix:** that function feeds no field (see §1), so it
  cannot close the false safe zone in any app heatmap. It only changes the
  discrete spray-cone dot renderer. A ray-vs-segment update there may still be
  worth a small follow-up for renderer honesty, but it is not this aspect.

## 4 · Recommendation

Implement **Option 1** on the Family-B ρ_L → P(kill) fields
(`four_zone_pkill_field` and its single-zone twin `pkill_field_3d`, plus the
line variant used by the app cross-sections): swap the `ρ_L(z=0)·A_ref` transform
for the vertical-extent integral `w_perp·∫₀ʰ ρ_L dz`. This is the minimal,
straight-line-consistent change; it reuses the volume kernel, closes the false
safe zone, and restores posture sensitivity. The derivation pass should:

1. State the vertical-target flux integral and confirm the `z = 0` transform is
   its degenerate constant-density limit.
1. Resolve the `A_ref`-frozen vs `w_perp·∫dz` fork and the posture re-coupling.
1. Give the `[0,h]` quadrature (how many z-layers; reuse of the m_min tables per
   layer) and a unit/limit check: at AoF = 90°, near-burst P(kill) must be
   non-zero for `h` reaching the belt at burst height, and must reduce to the
   old value when the belt already crosses `z = 0`.

## 5 · Deferred dependent aspect (do NOT scope here)

The graded Family-A fields (`compute_frag_field_3d`, `four_zone_field` and the
app's headline `field_pk` / `pk_total` heatmaps) also exhibit the false safe
zone but use a **different governing weighting** — `presented_area(γ)· pk_given_hit(E)` belt integral, a separate parameter group, separately
PASS/FAIL-able. Per the decompose-first rule this is its own aspect. Two paths
for a follow-on change:

- migrate the app's headline 2D heatmaps onto the fixed Family-B P(kill) (then
  Family A needs no fix), or
- apply Option 2 to Family A directly.
  Record this as a dependency of the app-wiring/presentation step; sequence it
  **after** this aspect is derived, reviewed, and in `src/arty/`.
