# Derivation — Point kill-probability field $P_k(x,y,z)$ from lethal-fragment density

**Author:** modeler agent
**Date:** 2026-06-21
**Status:** derivation pass — no `src/arty/` implementation (derivation.md only)
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Scoping:** `updates/pkill-poisson-field/scoping.md` (approved; `A_ref = 0.85 m²`
and binary-cut-vs-Poisson settled there §2, §3, §6 — **not** re-litigated here).
**Depends on:** `updates/lethal-fragment-density-field/derivation.md` (the `ρ_L`
kernel; approved + implemented). This aspect adds a **pure elementwise transform**
of that field — no new field integral, no change to the `ρ_L` kernel.
**Wraps (src/ pass):** `compute_lethal_density_field_3d` (`fragmentation.py:600`,
returns `(X, Y, ρ_L)` [m, m, m⁻²]) and `compute_lethal_density_volume_3d`
(`:646`, returns `(X, Y, Z, ρ_L)` [m, m, m, m⁻²]), plus the four-zone
counterparts in `zones.py`.

______________________________________________________________________

## 1 · Quantity and governing equation

`ρ_L(x,y,z)` [m⁻²] is the target-independent areal density of **lethal**
fragments crossing a unit patch at the field point (`lethal-fragment-density-field`
derivation eq. 3 — fragments past the binary `E_leth = 1000 J` mass cut). We map
it to a **point kill probability**

$$
\\boxed{;P_k(x,y,z) ;=; 1 - \\exp!\\bigl(-,\\rho_L(x,y,z),\\cdot,A\_\\text{ref}\\bigr);}
\\qquad (1)
$$

with `A_ref` [m²] a **fixed** nominal personnel presented area. `P_k` answers:
"if one representative person stood at this point, what is the probability that
**at least one** lethal fragment strikes them?"

`A_ref` is a single overridable scalar, **not** a live `presented_area(γ, posture)`
call (that varies with arrival angle/posture — exactly what `P_k` abstracts away,
scoping §2). Recommended value (scoping §2, option R1):

$$
A\_\\text{ref} ;=; A_f ;=; w\_\\perp, h ;=; 0.5 \\times 1.7 ;=; 0.85\\ \\text{m}^2
\\qquad (2)
$$

the standing frontal silhouette already defined in `fragmentation.py:96`
(`STANDING = PostureParams(w_perp=0.5, h=1.7, …)`), i.e. `presented_area(γ=0, standing)` frozen as a constant. **Caveat (carry into docstring + caption):**
`0.85 m²` is an engineering convention and a *lower bound* — real silhouettes
with helmet/armour/kit run 10–25% larger (scoping §2; `target-area-profile`
derivation §5.1).

### Symbols

| Symbol          | Meaning                                                | Unit       |
| --------------- | ------------------------------------------------------ | ---------- |
| `ρ_L(x,y,z)`    | lethal-fragment areal density (existing kernel)        | m⁻²        |
| `A_ref`         | fixed nominal personnel presented area                 | m²         |
| `λ ≡ ρ_L·A_ref` | mean number of lethal fragments hitting the silhouette | –          |
| `P_k(x,y,z)`    | point kill probability, eq. (1)                        | – (∈[0,1]) |

______________________________________________________________________

## 2 · Derivation of eq. (1) — Poisson "≥1 lethal hit"

The Poisson form is a member of the Cookson / ES-310 expected-hits casualty
family (scoping §3; ES-310 expected-hits `N_hits = N₀·A/(4πδs²)`,
`doc-reference/wound-ballistics/fas-es310-damage-criteria`). **It is not,
however, the literal ES-310 aggregate formula** — ES-310 (same document,
L42–46) writes the multi-hit aggregate as

$$
P_k ;=; 1 - (1 - P\_{k|\\text{hit}})^{N\_\\text{hits}}
\\qquad (\\text{ES-310 aggregate})
$$

with a **per-hit** kill probability `P_{k|hit}`, and anchors `P_{k|hit} = 0.5`
at the very 1000 J energy that defines `ρ_L`'s lethal-mass cut (L16, L51–55;
the same `_PK_VAL` table in `fragmentation.py:141`, where `pk_given_hit(1000 J) = 0.5` exactly). Eq. (1) `1 − e^{−λ}` is the **special case of this aggregate
with `P_{k|hit} = 1`** (the Poisson `≥1` limit of `1 − (1 − P_{k|hit})^{N}` as
`P_{k|hit} → 1`, `N` Poisson). Adopting eq. (1) therefore makes a **second,
explicit simplification** — promoting each ρ_L-counted fragment from ES-310's
`0.5` lethal-on-hit to *certainly* lethal once counted — stacked on top of the
binary-cut simplification the ρ_L kernel already made. This is a defensible
modelling choice (it keeps `P_k` a pure "≥1 lethal-threshold hit" reading,
consistent with `ρ_L` being a target-independent count kernel), but it is **not
a logical consequence of the binary cut and does not inherit ES-310's
numbers** — see step 3 and the (A2) caveat for the quantitative consequence.
Construction:

1. **Mean lethal-hit count.** A silhouette of area `A_ref` placed in a lethal
   areal-fragment density `ρ_L` intercepts, on average,

   $$
   \\lambda(x,y,z) ;=; \\rho_L(x,y,z),\\cdot,A\_\\text{ref}
   \\qquad (3)
   $$

   lethal fragments. `ρ_L` already counts **only** fragments past the lethal-mass
   threshold (binary cut, `lethal-fragment-density-field` derivation §1–3), so `λ`
   is a pure **expected count of lethal hits** — every per-hit lethality is
   already baked into membership in `ρ_L`. **Do not** fold the graded
   `pk_given_hit(E)` in again: that would exponentiate an already-probabilistic
   weight and double-count (scoping §3 — category error). `λ` here is a count, not
   a probability sum.

1. **Poisson hit count.** Model the number `K` of lethal fragments striking the
   silhouette as Poisson with mean `λ`:

   $$
   P(K = k) ;=; \\frac{\\lambda^{k},e^{-\\lambda}}{k!},\\qquad k = 0,1,2,\\dots
   \\qquad (4)
   $$

1. **At least one hit ⇒ kill (`P_{k|hit} = 1` simplification, beyond the binary
   cut).** We treat each ρ_L-counted fragment as *certainly* lethal once it
   hits, so the target is killed iff `K ≥ 1`:

   $$
   P_k ;=; P(K \\ge 1) ;=; 1 - P(K = 0) ;=; 1 - e^{-\\lambda}
   ;=; 1 - \\exp(-\\rho_L,A\_\\text{ref}),
   $$

   which is eq. (1). ∎

   **This is a second, explicit simplification, not a consequence of the binary
   cut.** The ρ_L kernel's binary `1000 J` cut counts fragments that ES-310 and
   the model's own `pk_given_hit(1000 J) = 0.5` rate as **≥50%-lethal-on-hit**
   (the cut sits exactly at the 50% crossing; see the prerequisite
   `lethal-fragment-density-field` derivation §3, which frames `ρ_L` as the
   areal density of fragments "each **≥50% lethal on a hit**"). Setting
   `P_{k|hit} = 1` for those counted fragments is a further approximation on top
   of the cut, *not* something the cut forces. The ES-310-consistent alternative
   keeps `P_{k|hit} = 0.5`, giving `P_k = 1 − (1 − 0.5)^λ = 1 − 0.5^{\,λ}` (for
   `λ ≥ 1`) and `P_k ≈ 0.5\,λ` (for `λ < 1`). **Consequence:** eq. (1) is
   **systematically more pessimistic (higher `P_k`)** than this ES-310 form for
   the same `ρ_L`. At small `λ` it is ~2× higher (`P_k ≈ λ` vs `≈ 0.5λ`); at
   large `λ` it saturates faster (e.g. `λ=2`: `0.865` vs `0.75`; `λ=5`: `0.993`
   vs `1 − 0.5^5 = 0.969`). A reader comparing eq. (1)'s `P_k` against an ES-310
   worked example for the same hit count will find eq. (1) higher by this
   amount — by construction, not error. Adopting the literal ES-310 aggregate
   with `P_{k|hit} = 0.5` is the natural follow-on refinement but is out of
   scope here (it is orthogonal to the frozen `A_ref = 0.85 m²` choice).

### Assumptions (state explicitly — model caveats, not defects)

- **(A1) Poisson independence / no shielding.** Fragment arrivals on the
  `A_ref` patch are independent Poisson events with mean `λ = ρ_L·A_ref`. Spatial
  correlation of the spray, fragment–fragment overlap, body armour, and partial
  cover are ignored. This is the conventional first-order casualty model (scoping
  §3, caveat 1).
- **(A2) Sharp lethality threshold *and* `P_{k|hit} = 1` once counted — two
  stacked simplifications.** (i) "Lethal" is the binary `E_leth = 1000 J`
  membership already inside `ρ_L`; the soft transition the graded
  `pk_given_hit(E)` captures is discarded (scoping §3, caveat 2). (ii) Eq. (1)
  then treats every ρ_L-counted fragment as `P_{k|hit} = 1`, whereas ES-310 —
  and the model's own `pk_given_hit(1000 J)` — assign `P_{k|hit} = 0.5` at that
  exact threshold. Simplification (ii) is **separate from and additional to**
  (i): the binary cut alone yields a ≥50%-lethal-on-hit count, and promoting it
  to certainly-lethal is a further choice (step 3). Net effect: `P_k` reads as
  "P(≥1 fragment above the lethal-energy threshold strikes a 0.85 m² silhouette,
  *each such fragment assumed certainly lethal*)," and is **more pessimistic
  than the ES-310 `1 − (1 − 0.5)^λ` aggregate** for the same `ρ_L` (step 3) —
  **not** a tissue-level wound model and not numerically equal to ES-310's
  worked examples.
- **(A3) Frozen presented area.** `A_ref` is posture/angle-independent by
  construction (eq. 2); `P_k` deliberately ignores target orientation and size.

The binary `ρ_L` and the Poisson `1 − e^{−λ}` reading are a **matched pair up to
the `P_{k|hit} = 1` approximation in (A2)(ii)** — they share the binary
lethal-membership cut, but eq. (1) additionally promotes each counted fragment
to certainly-lethal rather than ES-310's `0.5`. (Note this is the *opposite*
direction of error from folding the graded `pk_given_hit` back in: re-weighting
each Poisson event by a graded `pk_given_hit` would double-count the per-hit
probability against the count, scoping §3; eq. (1) instead drops the per-hit
probability entirely by setting it to 1. Neither is the literal ES-310 aggregate
`1 − (1 − P_{k|hit})^λ`; eq. (1) is its `P_{k|hit} = 1` limit and is the chosen
model here.)

______________________________________________________________________

## 3 · Unit / dimensional check

| Quantity                | Expression                              | Units                                             | OK? |
| ----------------------- | --------------------------------------- | ------------------------------------------------- | --- |
| `λ` (exponent argument) | `ρ_L · A_ref`                           | m⁻² × m² = **dimensionless**                      | ✓   |
| `exp(−λ)`               | well-defined only for dimensionless `λ` | –                                                 | ✓   |
| `P_k`                   | `1 − exp(−λ)`                           | dimensionless − dimensionless = **dimensionless** | ✓   |

`A_ref` [m²] cancels the [m⁻²] of `ρ_L` so the exponent is a pure number; the
transcendental `exp` is therefore dimensionally legal, and `P_k` is a pure number.
✓

______________________________________________________________________

## 4 · Validation / limit cases (scoping §6)

`λ = ρ_L·A_ref ≥ 0` always (`ρ_L ≥ 0` as a count density; `A_ref > 0`). With
`f(λ) = 1 − e^{−λ}` on `λ ∈ [0, ∞)`:

### 4.1 `ρ_L → 0 ⇒ P_k → 0`

`λ → 0 ⇒ P_k = 1 − e^{0} = 1 − 1 = 0`. ✓ No lethal fragments in the field ⇒ zero
kill probability. (Out-of-belt points and the `δ→0` guard already return
`ρ_L = 0` in both kernels, so eq. (1) maps them to `P_k = 0` automatically —
consistent with the `ρ_L` derivation §5.4 guard.)

### 4.2 `ρ_L → ∞ ⇒ P_k → 1`

`λ → ∞ ⇒ e^{−λ} → 0 ⇒ P_k → 1`. ✓ Saturating: a dense lethal field gives
near-certain kill, and `P_k` **bounds** at 1 (cannot exceed certainty), unlike the
unbounded raw `ρ_L`. This bounded saturation is the legibility advantage motivating
the transform (scoping §1, §4).

### 4.3 `P_k ∈ [0, 1]` everywhere

For `λ ∈ [0, ∞)`: `e^{−λ} ∈ (0, 1]`, so `1 − e^{−λ} ∈ [0, 1)`, attaining `0` at
`λ=0` and approaching (never exceeding) `1` as `λ→∞`. Therefore
`P_k ∈ [0, 1]` for **every** field point. ✓ A genuine probability everywhere; the
floating-point image lands in `[0, 1)` and clamps cleanly to `[0,1]`.

### 4.4 Monotone increasing in `ρ_L`

$$
\\frac{\\partial P_k}{\\partial \\rho_L}
= A\_\\text{ref},e^{-\\rho_L A\_\\text{ref}} ;>; 0
\\qquad\\text{for all } \\rho_L \\ge 0\\ (A\_\\text{ref}>0).
$$

Strictly positive everywhere ⇒ `P_k` is **strictly monotone increasing** in `ρ_L`.
✓ The transform preserves the rank ordering of the `ρ_L` field (more lethal
fragments ⇒ higher kill probability), so the `P_k` map is just a monotone,
bounded re-scaling of the `ρ_L` map — same spatial structure, legible axis.
The slope `A_ref·e^{−λ}` also decreases in `ρ_L`, i.e. **diminishing returns**:
the curve is concave, steep near the burst-shadow edge and flattening into the
lethal core — the correct qualitative shape for a saturating kill map.

### 4.5 Small-`ρ_L` linearisation matches expected lethal-hit count

Taylor expand eq. (1) about `λ = 0`:

$$
P_k = 1 - e^{-\\lambda}
= \\lambda - \\tfrac{\\lambda^2}{2} + O(\\lambda^3)
;\\approx; \\lambda ;=; \\rho_L,A\_\\text{ref}
\\qquad (\\lambda \\ll 1).
$$

So at the **lethal fringe** (`ρ_L·A_ref ≪ 1`), `P_k ≈ ρ_L·A_ref` — the kill
probability equals the **expected number of lethal hits** on the silhouette, the
expected behaviour of a Poisson "≥1 event" model when events are rare (one
expected hit ⇒ one kill, no double-counting). ✓ The leading correction
`−λ²/2 < 0` means eq. (1) sits **below** the bare expected count, correctly
accounting for the "two hits still one kill" overlap that the linear count
ignores. Numerically: at `λ = 0.05`, `P_k = 0.04877` vs `λ = 0.05` (2.4% below);
at `λ = 0.01`, `P_k = 0.009950` (0.5% below) — linearisation tightens as `λ→0`. ✓

### 4.6 `z = 0` slice consistency with the 2D `ρ_L` field

Eq. (1) is a **pure elementwise** function of `ρ_L` with no explicit `z`
dependence. The `ρ_L` kernel's `z=0` layer is already numerically identical to the
2D ground field (`compute_lethal_density_volume_3d` docstring: "the z=0 layer is
numerically identical to `compute_lethal_density_field_3d(z=0.0)`";
`lethal-fragment-density-field` derivation §5.1). Therefore

$$
P_k(x,y,0)
= 1 - \\exp!\\bigl(-\\rho_L(x,y,0),A\_\\text{ref}\\bigr)
= 1 - \\exp!\\bigl(-\\rho_L^{,2\\mathrm D}(x,y),A\_\\text{ref}\\bigr),
$$

i.e. applying eq. (1) to the volume's `z=0` slice gives **exactly** the same
`P_k` as applying eq. (1) to the standalone 2D `ρ_L` field — to machine precision,
since the two `ρ_L` inputs are bit-identical and `f(λ)=1−e^{−λ}` is deterministic.
✓ No new `z=0` numerical-identity argument is needed beyond the `ρ_L` kernel's;
eq. (1) inherits it. (The src/ pass should still assert this slice identity on the
`P_k` field, mirroring the existing `ρ_L` slice oracle.)

______________________________________________________________________

### 4.7 Fringe-dominated field: saturation confined to a small near-burst core (notebook-verified)

Because eq. (1) is the more-pessimistic `P_{k|hit} = 1` choice (step 3, A2),
`P_k` saturates quickly **where `ρ_L` is large**: `λ = ρ_L·A_ref` with
`A_ref = 0.85 m²` reaches `P_k = 0.817` already at `ρ_L = 2 m⁻²` and `P_k → 1`
by `ρ_L ≈ 10 m⁻²`. The spatial question — *how much of the field* saturates —
turns on where `ρ_L` actually sits, and the field is **fringe-dominated**, not
uniformly appreciable: although `ρ_L` peaks at ~74 m⁻² near the `s_min` floor,
that saturating core is spatially small, and `ρ_L` falls off steeply (∝ `s⁻²`
under the eq. 22′ inverse-square geometry) so that **most lethal cells sit at
`λ ≲ 1`**, in the graded regime where `P_k` varies smoothly with `ρ_L`.

The notebook pass measured this directly at the representative burst geometry
(AoF = 30°, `h_b = 2 m`, `z = 0`): only **~3 % (single-zone) / ~1 % (four-zone)
of lethal-field cells clear `P_k > 0.95`** — the map is fringe-dominated, with
full saturation (`λ ≫ 1`) confined to a small near-burst core. The frozen-`A_ref`
point transform this figure describes (`P_k = 1 − exp(−ρ_L·A_ref)`) is
implemented in `pkill_volume_3d`/`four_zone_pkill_volume`'s `z = 0` slice and
is what the app's interactive 3-D `P_k` volume view (`fig_pkill_volume`)
renders; `_pkill-field.qmd` was subsequently rewritten by the
`target-height-intercept` aspect (v0.5.1) for a different ground-column
computation and no longer carries this figure. The `~3 %/~1 %` numbers were
independently reconfirmed at this geometry, grid-stable over `n_grid = 30–200`,
as **3.18 % (single-zone) / 1.05 % (four-zone)** in
`updates/pkill-poisson-field/review.md`'s 2026-07-19 delta review — that
review is the citable artifact for this figure.

**Correction to an earlier paper estimate.** An initial estimate here
anticipated a *mostly-saturated* map — `P_k ≈ 1` over "most of the spatial
extent" where `ρ_L` is appreciable. That over-stated the saturated fraction: it
treated "densities of order 1–10 m⁻² over much of the belt" as typical, whereas
the `s⁻²` falloff confines the appreciable-`ρ_L` region to a thin near-burst
annulus rather than "most of the extent." The saturated fraction does grow
toward the burst and with lower `h_b` / steeper AoF (which pack more `ρ_L` into
the near field), but at representative geometry it is a **few percent, not a
majority**. The legibility goal from scoping §1 (compress `ρ_L`'s multi-decade
dynamic range into `[0,1]`) is met, and — because the graded fringe *is* the
bulk of the map — the mid-range renders legibly with a plain linear `[0,1]`
scale; no special near-saturation colour handling is needed.

## 5 · Validation checklist status (scoping §6)

| Check                                                                                                                                                                                            | Where         | Status                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ----------------------------------------------------------------------- |
| Unit: `ρ_L`[m⁻²]·`A_ref`[m²] ⇒ dimensionless exponent; `P_k` dimensionless                                                                                                                       | §3            | ✓ by construction                                                       |
| `ρ_L → 0 ⇒ P_k → 0`                                                                                                                                                                              | §4.1          | ✓                                                                       |
| `ρ_L → ∞ ⇒ P_k → 1` (bounded saturation)                                                                                                                                                         | §4.2          | ✓                                                                       |
| `P_k ∈ [0,1]` everywhere                                                                                                                                                                         | §4.3          | ✓ for all `λ∈[0,∞)`                                                     |
| Monotone increasing in `ρ_L` (`∂P_k/∂ρ_L > 0`)                                                                                                                                                   | §4.4          | ✓ strict; concave/diminishing-returns                                   |
| Small-`ρ_L` linearisation `P_k ≈ ρ_L·A_ref` = expected lethal-hit count                                                                                                                          | §4.5          | ✓ leading term, `−λ²/2` correction                                      |
| `z=0` slice consistent with 2D `ρ_L` field through eq. (1)                                                                                                                                       | §4.6          | ✓ inherited from `ρ_L` kernel; assert in src/                           |
| Poisson-independence (A1) + sharp-threshold/`P_{k\|hit}=1` (A2) assumptions stated; eq. (1) is the `P_{k\|hit}=1` limit of ES-310's `1−(1−P_{k\|hit})^λ`, more pessimistic than its `0.5` anchor | §2 step 3, A2 | ✓ recorded as explicit second simplification + quantitative consequence |
| `P_k` field is fringe-dominated; saturation confined to a small near-burst core (~1–3 % of lethal cells at `P_k>0.95`)                                                                           | §4.7          | ✓ notebook-verified; corrects an earlier mostly-saturated estimate      |
| `A_ref = 0.85 m²` fixed scalar, not `presented_area(…)`                                                                                                                                          | §1 eq. (2)    | ✓ + lower-bound caveat                                                  |

All limit/validation cases pass **dimensionally and logically** on paper.

______________________________________________________________________

## 6 · Implementation notes for the src/ pass (not code)

- New `src/arty/` function(s) wrap the existing grid builders and apply eq. (1)
  **elementwise** to the returned `ρ_L` array — no change to the `ρ_L` kernel,
  no new field integral. E.g. a `pkill_field_3d` / `pkill_volume_3d` calling
  `compute_lethal_density_field_3d` / `compute_lethal_density_volume_3d`
  (and four-zone equivalents) and returning `(X, Y[, Z], P_k)` with
  `P_k = 1 - np.exp(-rho_L * A_ref)`.
- Expose `A_ref` as a **named module constant** `A_REF_DEFAULT = 0.85` [m²] and as
  a function argument defaulting to it — overridable, never a `presented_area(…)`
  call (scoping §2 implementation note).
- Docstring (units in one line): "Return point kill probability `P_k` [-] ∈ [0,1]
  = 1 − exp(−ρ_L·A_ref), with `ρ_L` [m⁻²] the lethal-fragment areal density and
  `A_ref` [m²] the fixed nominal personnel presented area (0.85 m², standing
  frontal — lower bound; +10–25% with kit)."
- Carry the A1/A2 caveats (Poisson independence/no shielding; sharp threshold)
  into the docstring and the app caption.
- Assert the §4.6 `z=0` slice identity on the `P_k` field (mirrors the existing
  `ρ_L` slice oracle); `P_k` clamps to `[0,1]` by construction — a cheap
  `0 ≤ P_k ≤ 1` assertion guards against any negative-`ρ_L` regression upstream.
- OpenSpec change `pkill-3d-surface-view` spec shift (ρ_L → `P_k`, scoping §4) is
  the **main agent's** follow-up after src/ + review — not this pass.
