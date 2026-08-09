# Scoping — Mott fragment mass closure: restoring shape fidelity

**Aspect**: the closure that turns Mott's fracture-spacing length scale `x₀`
into a fragment mass `μ` in `mott_params()` (`src/arty/fragmentation.py:209`).
Independently validatable against Tolch (1938) screened mass data. Does **not**
cover `gurney_velocity`, drag, or lethality.

**Inputs (do not re-derive)**: `challenges/mott-scale-gap/_params_provenance_note.md`,
`challenges/mott-scale-gap/_scale_verdict_ledger.md`,
`challenges/mott-scale-gap/_shape_closure_check.md`.

## 1. Problem

Implemented: `μ = √(2/ρ)·(σ_f/γ)^{3/2}·(r_bu/V₀)³`, `N₀ = M/2μ`, with
`γ = 65` read from Mott (1947) §3's carbon-content table and `σ_f = 800 MPa`.

Two coupled defects, both confirmed in `_shape_closure_check.md`:

1. **Cube closure.** The implemented form is algebraically `μ = ½ρx₀³`, i.e.
   Gold (2017) eq. (4) `μ = ½·α·ρ·x₀³` with the shape factor
   `α = (l₀/x₀)(t₀/x₀)` silently set to **1** — a cube of edge `x₀`. Neither
   cited source supports a cube; both describe a wall-thickness prism.
1. **Wrong γ fed to a shape-absorbed formula.** The coded formula is Gold
   eq. (16), which is eq. (7) — the form where shape has already been *absorbed*
   into a redefined `γ ≡ α^{-2/3}γ′` (eq. 6). The code supplies Mott's raw
   material constant `γ′` in that slot. Independent of (1), and in the same
   direction.

Consequence (ledger §3): `μ` is 4–8× low, `N₀` ~4–12× high — the shell breaks
into far too many, far too light fragments. This inflates hit counts while
shortening per-fragment reach, and is confounded with the drag gap in
`b-vs-range.md`. Fixing it is a precondition for any further drag
calibration.

## 2. Literature audit

Read from source (not cards):

| Fact | Source |
| --- | --- |
| `x₀ = (2σ_F/ργ′)^{1/2}·r/V`, called "the average circumferential length"; `γ′` = material fracture constant | Gold 2017 eq. (2) + preamble (`…conwep/1-s2.0-S221491471730079X-main.md:56-60`) |
| Fragments are prisms idealized as a **parallelepiped** `l₀ × x₀ × t₀`; `μ = ½αρx₀³`, `α = (l₀/x₀)(t₀/x₀)` | Gold eq. (4), lines 70-76 |
| `γ ≡ α^{-2/3}γ′`, then eq. (7) ≡ eq. (16) — the shape-absorbed form the code uses | Gold eqs. (6)-(7), (16) |
| `μ` is **one half the average fragment mass**; `N₀ = M/2μ` | Gold line 54. So the closure is exactly `mean mass = ρ·l₀·x₀·t₀`, and the code's `N₀ = M/2μ` is **correct** (Gold's own eq. (17) `N₀ = m/μ` contradicts his line 54 and is a typo — do not follow it) |
| Gold's `γ` is **calibrated against explosive CJ pressure**, not composition; he runs `γ = 50` for HF-1/Comp-B and 20–50 across regions | lines 190, 212, 218 |
| Mott's own statistic: fragment lengths mostly `x₀…2x₀`, **average ≈ 1.5x₀** | Mott 1947 finding (1), `…gurney-equations-fragmentation/`, p.305, anchor `The fragments have lengths most of which lie` |
| Mott's `x₀` is a *circumferential* spacing from a 1-D ruled-line simulation; he never converts it to a mass | Mott lines 156-187 |
| **Thin-case fragments retain the casing thickness**; Mott's engineering closure `M_A = B_m t^{5/6} d^{1/3}(1+t/d)` with `μ = M_A²`, `N₀ = M/2M_A²` | `…explosion-fragment-model/1-s2.0-S221491472030502X-main.md:34` — this **resolves ledger §4 item 3's caveat**: the form *is* in `doc-reference/`. `B_m` values are not (referred out to Needham, *Blastwaves*) |
| Fragment aspect ratio (width:length) **1:1.6** from three independent datasets (Mott's own distribution, Grady, Hiroe); corroborated by Wilson 1:1.65 (W-alloy) and Grady 1:1.5 (AERMET-100). Cuboid, mean length 1.1 cm | same file, §2.5, §4.1.3, §5 (lines 51, 137, 5-conclusions) |
| Cubic/spherical fragment assumptions "give inaccurate results for drag and armour penetration" | same file, §5 |

**Verdict on literature sufficiency: sufficient — no @librarian pass is
required to proceed.** Every factor needed for the recommended option (`α`
decomposition, `t₀ =` wall thickness, `l₀/x₀ = 1.6`) is sourced in-repo. Two
optional asks are noted in §6.

**Not usable:** Tolch's own fragment-dimension table (his 9 armour-perforating
fragments, `tolch-1938.md:1459`) is OCR-destroyed in the digitized copy — `α`
cannot be read off Tolch directly. Tolch constrains `μ` only, via the screened
mass distribution.

## 3. Options

Notation: `x₀` = Mott breadth scale, `t_bu` = wall thickness **at break-up**
(the case thins as it expands; `_shell_geometry` already computes the expanded
inner/outer radii from the `V/V₀ ~ 3` rule), `t` = as-manufactured wall.

Scoping-grade numbers for 75 mm M48 (`x₀ = 3.91 mm`, `t = 6.00 mm`,
`t_bu = 3.67 mm`, `r_bu = 56.4 mm`, `V₀ = 807.5 m/s`) — to be re-verified in
derivation, not authoritative here. Tolch anchors: `μ = 0.95 g`
(mass-constrained) to `3.46 g` (large-fragment-weighted).

**As of 2026-08-09:** these 75 mm M48 inputs, and the `μ` column below, are
the pre-fix values this scoping was written against; the shipped shell is now
`M_case = 4980.0 g`, `V₀ = 864.4 m/s`, `μ = 0.826 g`, `N₀ = 3016` (M48
fuze/case-mass correction). Left as recorded — the option *comparison* here is
what mattered and its ranking is unaffected. See the as-of banner in
`derivation.md`.

| Option | `μ` (75 mm) | vs Tolch |
| --- | --- | --- |
| **current** (cube, `α=1`) | 0.235 g | 4–15× low |
| **A** plate, `x̄ = x₀`, `t₀ = t_bu` | 0.35 g | still 2.7× low |
| **A** plate, `x̄ = 1.5x₀` (Mott's mean), `t₀ = t_bu` | 0.79 g | at bracket floor |
| **A** plate, `x̄ = 1.5x₀`, `t₀ = t` | 1.30 g | inside bracket |
| **C** Mott `M_A` engineering form, `B ≈ 0.0554` | 1.15 g | inside bracket |

**Option A — explicit `α`, plate closure.** Restore Gold eq. (4)/(5): keep `γ′`
as the material constant it is (Mott's carbon table), and close the mass as
`mean mass = ρ·l₀·x̄·t₀` with `t₀` = wall thickness and `l₀/x̄ = 1.6` from the
aspect-ratio literature. Structurally `μ ∝ (σ_F/γ′)·(r/V)²·t` — mass becomes
**linear in wall thickness**, which is the dominant real driver of fragment
size (and exactly what Mott's `M_A ∝ t^{5/6}` encodes).
*Pros:* every factor sourced, no free knob; preserves `γ′` as a per-grade
material parameter, so the `wdss1-steel-grade` update's carbon interpolation
keeps its meaning. *Cons:* changes the exponent structure, so steel-grade
sensitivity weakens from `μ ∝ γ′^{-3/2}` to `μ ∝ γ′^{-1}`; promotes `wall_t`
(currently an unconfirmed caliber-scaled estimate, `shells.py:57`) from a
second-order to a first-order parameter.

**Option B — recalibrate `γ` as Gold's lumped parameter.** Keep eq. (16) as
coded, but stop sourcing `γ` from the carbon table; take it from Gold's CJ-
pressure axis or fit it to Tolch (a 4× `μ` correction needs `γ ≈ 26`, low but
on-scale for Gold's 20–50).
*Pros:* one-line change, matches the cited equation as published, is what Gold
himself does. *Cons:* `γ` then lumps shape + explosive + material, so it cannot
be read from a composition table and the shell registry's per-grade `γ` becomes
uninterpretable — it would silently invalidate the `wdss1-steel-grade` work. One
fitted knob per shell, no predictive transfer.

**Note — A and B are not actually a dichotomy.** By Gold eq. (6) the algebra is
identical: choosing `α` explicitly *is* choosing `γ = α^{-2/3}γ′`. The real
choice is only whether shape is carried by a *sourced, shell-dependent* `α`
(A) or an *opaque, fitted* `γ` (B). Recommended implementation keeps eq. (16)'s
shape in code and computes `γ = α^{-2/3}γ′` from a shell-level `α`, so the
module stays visibly Gold-eq-16-compatible.

**Option C — Mott engineering closure `√μ = B_m t^{5/6} d^{1/3}(1+t/d)`.** Now
sourced in-repo. *Pros:* the standard ConWep-lineage form, `t`/`d`
parameterized, lands inside Tolch's bracket. *Cons:* **loses velocity
dependence entirely** — `μ` would no longer depend on `V₀`, decoupling the
Gurney→Mott chain, and explosive type would stop affecting fragment size (a
sensitivity the shell/filler registry exists to express). `B_m` values are not
in `doc-reference/`. **Use as a cross-check, not the primary model.**

**Option D — fit `α` (or `μ`) directly to Tolch.** Rejected as primary: single
shell, no transfer to 105/155 mm, and it would absorb the break-up-velocity
error (§5) into a shape parameter, making both un-attributable. Tolch is the
validation target, not the source of the closure.

## 4. Recommendation

**Option A, expressed through Gold eq. (6).** Implement
`α = (l₀/x̄)·(t₀/x̄)` with `l₀/x̄ = 1.6` (sourced) and `t₀` = wall thickness at
break-up, feed `γ = α^{-2/3}γ′` into the existing eq. (16) form, and leave
`σ_f`, `γ′`, `N₀ = M/2μ` untouched. Carry Option C as a validation cross-check
only.

The derivation pass must settle two factor-level questions the table above
shows are worth **3.7× between them** — this is the real work of that pass:

- **(Q1) Is Gold's `x₀` Mott's scale parameter or the mean breadth?** Gold's
    preamble calls eq. (2) "the average circumferential length"; Mott says the
    *average* is `1.5x₀` where `x₀` is that same expression. Gold has therefore
    dropped Mott's 1.5. Worth 1.5× on `μ` under the plate closure (3.4× under
    the cube). Recommended reading: follow Mott (`x̄ = 1.5x₀`) and say so, since
    Mott is the primary and Gold is restating him.
- **(Q2) Thinned or as-manufactured thickness?** Recovered fragments carry the
    post-expansion thickness, so `t_bu` is the physically right choice, but
    `t_bu` is derived from the `V/V₀ ~ 3` expansion rule already baked into
    `_shell_geometry`, whose incompressibility bookkeeping should be checked
    before it is promoted to a first-order factor. Worth 1.63×.

Also verify in derivation: `α` and the drag `C_shape = 0.90`
(`fragmentation.py:113`) must describe the *same* fragment. Asserting a 1.6:1
prism here while the drag term still assumes a near-cube presented area is a new
internal inconsistency; at minimum log it, since `explosion-fragment-model` §5
explicitly warns cubic assumptions corrupt drag.

## 5. Open question — break-up velocity (recommend: separate follow-up)

Ledger §4 item 2 notes the formula is fed `V₀`, the *terminal* Gurney velocity,
where Mott/Gold specify the case velocity **at break-up**; `μ ∝ V^{-3}`, so
break-up at 0.7–0.8 `V₀` is worth 2–3×. The code is already half-committed to
break-up conditions — it uses a break-up *radius* `r_bu` with a terminal
*velocity*, which is internally inconsistent.

**Out of scope for this change.** It is a different governing quantity (the
Gurney/kinematic aspect), it touches every downstream velocity consumer (drag,
KE, lethality) rather than just `mott_params`, and bundling it makes the Tolch
fit un-attributable — you could not tell which correction did the work. Note
that under Option A with Q1/Q2 resolved conservatively the residual gap is
~1.5–2×, which is exactly the size this item predicts; that residual must be
**left standing**, not absorbed by tuning `α`.

## 6. Optional @librarian asks (neither blocks this pass)

1. `B_m` values for steel/TNT (Needham, *Blastwaves*) — only if the Option C
   cross-check is wanted with a sourced constant rather than the ledger's
   uncited `B ≈ 0.0554`.
1. 75 mm M48 wall thickness (`shells.py:57` is a caliber-scaled estimate) —
   Option A makes `μ` linear in it, so it becomes a first-order parameter.

## 7. Validation checks for the derivation/src passes

1. **Units/limits.** `μ` must reduce to the current expression when
   `l₀ = t₀ = x̄`; `[μ] = kg`; `μ > 0`, monotone increasing in `t₀`, `σ_F`,
   `r_bu`, decreasing in `γ′`, `V₀`.
1. **Mass closure.** `∫m·(-dN/dm)dm = 2N₀μ = M` exactly (this is why
   `N₀ = M/2μ`, not Gold's eq. 17) — assert to machine precision.
1. **Tolch spectrum.** Recompute the ledger §2 four-point `N(>m)` table; the
   `N(>6 g) = 278` under-count (currently 3.6× low) must improve, and the
   crossover at the fine end must not worsen beyond the current 3.5×.
1. **Transfer.** Re-run 105 mm and 155 mm; `μ` must stay inside the PAFRAG/arena
   `N(>0.5 g)` = 3000–8000 band (`_validation.qmd` Check 3) — noting that band
   is a model-to-model consistency check, not data.
1. **Option C cross-check.** `M_A` closure vs Option A on all three shells;
   agreement within ~2× is a pass.
1. **Regression.** `tests/test_fragmentation.py`, and the R50 / P(kill) field
   outputs — expect R50 to move little (per memory: R50 is insensitive to
   per-fragment count/reach trade-offs) but hit counts / B(r) to drop ~3–4×.

## 8. Fidelity target

This aspect drives `μ` and `N₀`, hence the fragment mass spectrum → hit counts,
per-fragment reach, and therefore the P(kill) field, R50, and the B(r)
comparison against Ordnance 1944. Tolch's own bracket on `μ` is itself a factor
3.7 wide (0.95–3.5 g), so **a factor of 2 on `μ` is tolerable**: the target is
`μ` inside 0.95–3.5 g and `N(>6 g)` within 2× of Tolch's 278 for the 75 mm M48,
with no re-tuning of `σ_f` or `γ′`.
