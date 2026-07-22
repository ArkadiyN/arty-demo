# Scoping — Legacy single-zone field shell-axis fix (down-range mirror error)

**Aspect:** correct the **shell-axis sign convention** in the single-zone
("legacy") 3-D fragmentation-field kernel
(`fragmentation.py:_expected_kills_3d_point` / `_expected_kills_3d_vec`, feeding
`compute_frag_field_3d` → the app's "2D Fragmentation Field" P(kill) heatmap, its
cross-range R₅₀, and the "Four-zone − Single-zone" difference map). The kernel
builds its equatorial belt on the **backward** axis
`ê = (−cosα, 0, −sinα)`, an **x-mirror** of the forward axis
`ê = (+cosα, 0, −sinα)` used by every other path. Straight-line rays only.

**This overrides a prior framing — read first.** `_limitations.qmd` #12 and the
modeler memory `shell-axis-sign-convention` both describe this mismatch as a
*deliberate standardisation by construction, benign off the x=0 plane*. That
framing is **wrong and is retired by this aspect.** A numerically-verified
correctness pass (reproduced below) shows the backward axis is not a benign
convention choice: it is a physical **sign error** that places the entire
single-zone down-range hazard lobe on the wrong side of the burst.

## 0 · Established finding (do not re-derive)

At `h_b=8 m, AoF=40°, δ=30°`, the trusted forward convention
(`fragment_velocity`/`fragment_ground_impact`, four-zone, `lethal_density_point`)
puts equatorial-belt ground impacts only on the **backward** ground side,
`x ∈ [−22, −1.4] m` (belt centre `x = −h_b tanα = −6.7 m`). The legacy kernel's
field is nonzero only at **positive** x, `x ∈ [+1.4, +22] m`, zero at negative x —
an exact mirror (confirmed in this pass; matches the correctness report).

**Why it is a genuine error, not a convention choice.** The equatorial belt gate
`|cosΘ| ≤ sinδ` *is* invariant under a full axis reversal `ê → −ê`. But the
backward `_shell_axis` is **not** the reversal of the forward axis — reversing
`(+cosα,0,−sinα)` gives `(−cosα,0,+sinα)`; the backward axis is
`(−cosα,0,−sinα)`, i.e. only the **x-component** is flipped. That is a mirror
reflection across the `x=0` plane, physically a shell travelling *backward*
(−x) and down — the opposite of its actual forward-down trajectory. The two
conventions agree only on `x=0` (where the flip is a no-op) and at `AoF=90°`
(where `cosα=0`), which is exactly why the mismatch survived: every on-axis and
every 90° test passes with the wrong sign.

## 1 · Where the bug lives (code audit, read fresh)

The single-zone legacy kernel is the **sole** backward-axis user in `src/arty/`.
Three coupled spots encode it (all in `fragmentation.py`):

| Spot | Line | Backward-axis encoding |
| ---- | ---- | ---------------------- |
| `_expected_kills_3d_vec` belt-geometry call | 1024 | `x_axis=-x_g` into `_belt_column_zrep_vec` |
| `_expected_kills_3d_vec` inline `cosΘ` | 1036 | `(-x_g*cA - dz*sA)/s_safe  # backward axis` |
| `_expected_kills_3d_point` belt-geometry call | 940 | `x_axis=np.array([-x_g])` |
| `_expected_kills_3d_point` feet-lit `cosΘ` | 959 | `e_axis = _shell_axis(alpha_rad)` |

The `-x` feed is **not itself a bug** — `belt_column_breakpoints` /
`_belt_column_zrep_vec` are written forward-native (`B=-2x cosα sinα`), so
`x_axis=-x` faithfully reproduces the *backward*-axis membership. It is a correct
implementation of a wrong axis. The compensating x-flip is a **symptom** of the
underlying `_shell_axis` being backward, not an independent defect.

**Sibling audit — everything else is already forward, so there is no sibling to
break.** `grep` confirms: `zones.py` four-zone Family-A (`_four_zone_familyA_eval`
belt call L500 `x_axis=xg`; `cos_Theta` L723/L807) and `_forward_shell_axis`
(L721/L803), and `fragmentation.py:lethal_density_point` (L509), all use the
forward axis. `_shell_axis` (the backward constructor, L381) has exactly **one**
call site — L959 above. After this fix it has **zero** callers.

**Blast radius is bounded to the down-range shape.** `compute_frag_field_3d`'s
`r50_cross` (app L227–232) is read from the **cross-range slice at `x=0`**, where
the two conventions are identical — so R₅₀ metrics and the
`50 ≤ r50 ≤ 200` range tests are **unaffected**. Only the 2-D heatmap's
down-range (`x≠0`) lobe and the diff map change. The mirror does not alter the
*radial magnitude* of the field, only which side of the burst it sits on and
whether the diff map is meaningful.

## 2 · Options

The physics answer is settled — the forward axis is correct (it agrees with
`fragment_velocity`, the elevation chart, four-zone, and ρ_L). The decision is
*how* to realise it.

### Option A — repoint the single-zone kernel to the shared forward axis *(recommended)*
Drop the backward convention in all four spots: pass `x_axis=+x_g` (or default)
to `_belt_column_zrep_vec` (L940, L1024); flip the inline `cosΘ` to
`(+x_g*cA - dz*sA)/s_safe` (L1036); use `_forward_shell_axis` in the feet-lit
branch (L959). Delete the now-dead `_shell_axis` constructor (L381) to prevent
future misuse. Update the tests that pin the backward sign (§3).

- **Correctness:** the single-zone field lands on the same (backward-ground)
  side as the four-zone and the elevation chart; the two conventions now agree
  pointwise off `x=0`, not merely on it. PASS.
- **Diff map recovered:** "Four-zone − Single-zone" (app L812) currently
  subtracts a forward four-zone field from an x-mirrored single-zone field →
  off-axis garbage (flagged in `_limitations.qmd` #12). With both forward it
  becomes a clean per-zone attribution — the feature works as intended.
- **Cost:** small, local, physics-preserving. The graded Family-A kernel
  (`A_p(γ)·pk_given_hit(E)`, belt-column relocation, mass integral) is untouched;
  only the axis it is evaluated on moves. Vec/point stay bit-identical to each
  other (both flip together).
- **Cross-range invariance:** R₅₀ and its range tests unchanged (§1). Reduces to
  current on `x=0` and at `AoF=90°`.

### Option B — keep the backward kernel, mirror x at the app/presentation layer
Leave `_shell_axis` backward; flip the heatmap's x-axis (or negate `field_x`) in
`app/sensitivity.py` so the *display* looks right.

- **Rejected — symptom mask.** It re-introduces exactly the compensating-x-flip
  antipattern that caused the confusion. It leaves `_expected_kills_3d_vec/_point`
  returning a physically-wrong field, so any *direct* caller (the diff map, which
  is computed in physics space against the forward four-zone field; tests;
  cross-sections) still gets the mirror. It cannot fix the diff map at all, and
  it splits "the number" from "its rendering" — the precise thing Gate 3 warns
  against.

### Option C — replace the single-zone graded kernel with a wrapper over the ρ_L / four-zone forward machinery
Re-express the single-zone path by calling `lethal_density_point` or the
four-zone Family-A evaluator with a single equatorial zone.

- **Rejected — over-scoped, changes physics.** The single-zone legacy path is a
  *graded* `A_p·pk_given_hit` kernel with its own `sinΘ` off-belt normalisation
  (`_limitations.qmd` #12, the `1/sin(90°−δ)` note); ρ_L is a *binary* lethal-mass
  kernel. Swapping kernels would silently change the graded field's magnitude and
  the whole reason the single-zone Family-A path is retained as the graded
  absolute-magnitude baseline. The axis is wrong; the kernel is not. Fixing more
  than the axis is scope creep and would need its own derivation + review.

## 3 · Test & documentation impact (must accompany the fix)

- **`tests/test_familyA_false_safe_zone.py::test_offaxis_single_zone_axis_sign`
  and its helper `_ref_relocated_single_offaxis`** currently pin the **backward**
  axis (`cosΘ = -(x cosα + dz sinα)/s`, test-file L314/L319) and probe `x<0`
  points. This test enforces the very bug being fixed — it MUST be flipped to the
  forward convention (`cosΘ = (x cosα - dz sinα)/s`) and its probe points chosen
  in the now-lit region. **Keep its intent:** it must still catch a wrong
  (mirror) sign off-axis, since `AoF=90°` is sign-blind (`B=0`). The derivation
  pass owns rewriting it as a forward-axis brute reference.
- **`tests/test_fragmentation.py`** (`test_r50_in_expected_range`,
  `test_backward_compat`, the `r50_cross > 0` / monotone-in-`h_b` checks) read
  cross-range / `x=0` quantities → expected to stay green (§1). The impl pass
  should confirm, not assume.
- **`tests/test_vectorized_equivalence.py`** — vec vs point equivalence holds as
  long as both are flipped together; confirm no reference pins the `+x` lobe.
- **`_limitations.qmd` #12** — remove/rewrite the "backward shell-axis convention,
  deliberately not reconciled" bullet and the diff-map caveat: after the fix the
  diff map *is* a clean attribution. The `sinΘ`-parity note (the separate
  `1/sin(90°−δ)` off-belt normalisation) is unrelated to the axis and stays.
- **Modeler memory `shell-axis-sign-convention`** — the "deliberate
  standardisation, do not re-assert equivalence" framing is superseded; update it
  to record that the backward axis was a mirror error, now corrected to forward.

## 4 · Literature audit

No new external literature. This is an internal sign/convention correction
against the project's own already-cited forward geometry (`fragment_velocity`,
zones derivation §, `lethal-fragment-density-field/derivation.md` §5.4). No
`@librarian` pass needed.

## 5 · Recommendation

Adopt **Option A** — repoint the single-zone legacy kernel to the shared
`_forward_shell_axis` convention and delete the dead `_shell_axis` constructor.
It is the only option that (i) puts the single-zone field on the physically
correct (backward-ground) side, matching `fragment_velocity`, the elevation
chart, four-zone, and ρ_L; (ii) turns the diff map into the clean per-zone
attribution it is meant to be; (iii) preserves the graded Family-A kernel exactly
(axis only); (iv) removes the *last* backward-axis holdout so no sibling is left
inconsistent; and (v) is cross-range/R₅₀-invariant, so existing range tests hold.

The derivation pass should:
1. State the forward-axis kernel: belt geometry on `x_axis=+x_g`, inline
   `cosΘ = (x_g cosα - dz sinα)/s`, `_forward_shell_axis` in the feet-lit branch.
   Confirm vec≡point and reduction to current on `x=0` and `AoF=90°`.
2. Rewrite `test_offaxis_single_zone_axis_sign` + `_ref_relocated_single_offaxis`
   to the forward convention with off-axis (`AoF≠90°, x` in the lit region) probe
   points, preserving the wrong-sign-catching intent.
3. Unit/limit checks: at `h_b=8, AoF=40°, δ=30°`, single-zone field nonzero on
   `x<0` and zero on `x>0` (the mirror of today); single-zone belt centre now
   coincident with the equatorial cylinder lobe of the four-zone field (same
   side); `r50_cross` unchanged vs the shipped value; diff map ≈0 on the shared
   equatorial belt.
4. Update `_limitations.qmd` #12 and the modeler memory entry (§3).

**Fidelity target:** this aspect drives the "2D Fragmentation Field" P(kill)
heatmap and the "Four-zone − Single-zone" diff map. The tolerance is a hard
*directional* bar, not a magnitude one — the single-zone down-range lobe must sit
on the **same side of the burst** as the four-zone equatorial lobe (currently
mirror-opposite); the R₅₀ magnitude (cross-range) must be unchanged. A residual
few-percent off-belt `sinΘ`-normalisation difference vs ρ_L (`_limitations.qmd`
#12) is out of scope and acceptable.
