# Derivation — target-height fragment intercept (false safe-zone fix)

**Author:** modeler agent
**Date:** 2026-07-18
**Status:** derivation pass — no `src/arty/` implementation (derivation.md only)
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Scoping:** `updates/target-height-intercept/scoping.md` (approved; Option 1 —
vertical-extent aggregation of the ρ_L field — selected there §4, **not**
re-litigated here).
**Depends on:**

- `updates/lethal-fragment-density-field/derivation.md` — the target-independent
  ρ_L kernel, eq. (3) there (approved + implemented). **Unchanged** by this aspect.
- `updates/pkill-poisson-field/derivation.md` — the Poisson `P_k = 1 − e^{−λ}`
  transform, eq. (1)/(2) there. This aspect **replaces the mean-count `λ`** that
  feeds it; the Poisson wrapper itself is unchanged.

This aspect changes **only** how the mean lethal-hit count `λ` is formed from the
existing ρ_L field: from a single `z = 0` sample times a frozen area, to the
field integrated over the vertical column the target actually occupies. No new
kernel, no trajectory curvature, no gravity — straight-line rays throughout.

______________________________________________________________________

## 1 · The defect, stated as an integral

The shipped point-kill transform (`pkill-poisson-field` eq. 1) is

$$
P_k(x,y) = 1 - \\exp!\\big(-,\\lambda\\big), \\qquad
\\lambda\_\\text{old} = \\rho_L(x,y,,z{=}0)\\cdot A\_\\text{ref},
\\quad A\_\\text{ref}=w\_\\perp h = 0.85\\ \\text{m}^2 .
\\qquad (1)
$$

It reads the lethal-fragment areal density **only on the ground plane** and
multiplies by a frozen standing silhouette. `ρ_L` is the flux of lethal fragments
per unit area normal to the local ray (`lethal-fragment-density-field` eq. 3); it
is already a function of height `z` and is correct at every `z` — the volume view
uses exactly this. The bug is not in `ρ_L`; it is that a **standing person is a
vertical target**, and sampling the flux at `z = 0` alone discards every fragment
that crosses the column above the feet. At steep angle of fall the equatorial
cylinder belt sprays horizontally at (or near) burst height and never descends to
`z = 0` close in, so `ρ_L(z{=}0)=0` there and eq. (1) reports `P_k=0` — the false
safe ring — even though the same rays pass straight through chest height.

## 2 · Governing equation — vertical-extent flux integral

Model the person at ground location `(x,y)` as a vertical rectangular silhouette:
horizontal width `w_perp` (⊥ to the downrange azimuth) spanning the column
`z ∈ [0,h]`. The mean number of lethal fragments intercepting a horizontal strip
element `w_perp\,dz` at height `z`, sitting in flux `ρ_L(x,y,z)`, is
`ρ_L(x,y,z)\,w_perp\,dz` (frontal projection; obliquity discussed in §7). Summing
over the column gives the mean lethal-hit count

$$
\\boxed{;\\lambda(x,y) ;=; w\_\\perp \\int_0^{h} \\rho_L(x,y,z),dz;}
\\qquad (2)
$$

fed into the **unchanged** Poisson wrapper

$$
P_k(x,y) ;=; 1 - \\exp!\\big(-\\lambda(x,y)\\big) .
\\qquad (3)
$$

Equation (2) is precisely the straight-line "does a lethal ray cross the target
volume `[0,h]`?" test written as a field integral over the already-correct
`z`-resolved kernel: a cell fires when the belt illuminates **any** height the
target spans, not only its feet.

### Symbols

| Symbol       | Meaning                                                       | Unit       |
| ------------ | ------------------------------------------------------------- | ---------- |
| `ρ_L(x,y,z)` | lethal-fragment areal density (existing kernel, unchanged)    | m⁻²        |
| `w_perp`     | target horizontal width ⊥ to azimuth (`PostureParams.w_perp`) | m          |
| `h`          | target vertical extent (`PostureParams.h`)                    | m          |
| `λ(x,y)`     | mean number of lethal fragments crossing the column `[0,h]`   | – (count)  |
| `P_k(x,y)`   | standing-person ground kill probability, eq. (3)              | – (∈[0,1]) |

## 3 · Reduction to the shipped transform (fork resolution)

Scoping §4 flagged the fork: keep `A_ref` frozen, or use `w_perp∫dz`. Take the
constant-density limit of eq. (2): if `ρ_L(x,y,z) ≡ ρ_L^0` over `[0,h]`,

$$
\\lambda = w\_\\perp \\int_0^h \\rho_L^0,dz = \\rho_L^0,(w\_\\perp h) = \\rho_L^0,A_f ,
\\qquad A_f = w\_\\perp h .
\\qquad (4)
$$

This is **identical** to eq. (1) with `A_ref = A_f = 0.5·1.7 = 0.85 m²` — the
current transform is exactly the degenerate case that assumes the whole silhouette
sees the single `z = 0` density. Eq. (2) is therefore not a new model but a
generalisation that samples the density the target actually spans; it collapses to
the shipped value wherever `ρ_L` is `z`-flat over a human height.

**Fork resolved: adopt `w_perp∫dz` (eq. 2).** `A_ref = 0.85 m²` is **re-anchored
as a diagnostic default only** — it survives as the frozen scalar for the
single-height point transform (`pkill_field_3d(z, A_ref)`, "one person standing at
this exact height"), but the standing-person **ground** field switches to eq. (2)
and no longer freezes area. This is the physical choice and it costs nothing extra
in geometry (still straight-line belt flux).

## 4 · Posture re-coupling

Because eq. (2) reads `(w_perp, h)` live from `PostureParams`, posture re-enters
automatically — closing the gap where the frozen `A_ref` discarded the toggle:

| Posture  | `w_perp` [m] | `h` [m] | column integrated | `A_f = w_perp h` [m²] |
| -------- | ------------ | ------- | ----------------- | --------------------- |
| STANDING | 0.5          | 1.7     | `[0, 1.7]`        | 0.85                  |
| PRONE    | 0.5          | 0.3     | `[0, 0.3]`        | 0.15                  |

The standing column reaches into a horizontal belt at burst height that the prone
column (capped at 0.3 m) sits beneath — so the model now correctly predicts a
**standing** soldier is *more* exposed near a high–angle-of-fall low burst, which
is the whole physical point of the fix. This posture sensitivity is a bonus of
eq. (2), not a separate aspect.

**Scope limit (deferred, §7):** eq. (2) models the *frontal/vertical* silhouette
only. For PRONE the dominant exposure is the top-down footprint `w_perp·d`
(`d = 1.8 m`) seen by steeply-descending fragments — the `d\sinγ` term of
`presented_area(γ)`. Dropping it makes eq. (2) **conservative-low for prone under
steep arrival**, which does not distort the headline standing-target false-safe-zone
result. Adding the top-down patch is a documented refinement, not this minimal fix.

## 5 · Quadrature — piecewise on the belt-membership interval

### 5.1 Why a naive uniform trapezoid fails (the review defect)

`ρ_L(x,y,z)` is **not smooth in `z`**: the kernel's belt test
(`lethal_density_point`) is a hard `0/1` cutoff `|cosΘ| ≤ sinδ` that switches
`ρ_L` on/off at a definite crossing height. At fixed `(x,y)` the integrand of
eq. (2) is therefore *zero over part of the column and a smooth positive function
over the rest, with a step at the belt edge*. A composite trapezoid on a uniform
grid over the whole `[0,h]` straddles that step; its error is `O(Δz)` and
**non-monotone** in `n_z` (refining moves sample points across the discontinuity
erratically). The original §5 "varies smoothly over the column" argument is
**false** for exactly the close-in columns the fix must correct, where the belt
grazes only a thin band near the top of the silhouette.

Numerically confirmed at the §6.3 worked example (AoF `90°`, `h_b = 2.0`,
`δ = 15°`, STANDING, downrange column; reference = gate-free interior
continuation of `ρ_L` integrated at 4000 pts/segment):

| `r` [m] | belt segment `[z_lo,h]` [m] | uniform trapz rel-err vs ref |           |       |      |       |      | midpoint n=9 |
| ------- | --------------------------- | ---------------------------- | --------- | ----- | ---- | ----- | ---- | ------------ |
|         |                             | n9                           | n12       | n18   | n24  | n48   | n192 | err          |
| 1.2     | [1.678, 1.7] (22 mm)        | **395%**                     | 260%      | 133%  | 72%  | 16%   | 3.3% | 0.00%        |
| 1.5     | [1.598, 1.7]                | 5.8%                         | **23.1%** | 46.4% | 8.8% | 11.1% | 0.4% | 0.00%        |
| 2.0     | [1.464, 1.7]                | 34.3%                        | 1.5%      | 5.9%  | 9.4% | 0.3%  | 0.0% | 0.00%        |
| 3.0     | [1.196, 1.7]                | 5.4%                         | 7.1%      | 8.8%  | 4.5% | 3.0%  | 0.2% | 0.00%        |
| 5.0     | [0.660, 1.7]                | 7.7%                         | 3.2%      | 1.0%  | 3.0% | 0.8%  | 0.3% | 0.00%        |
| 7.0     | [0.124, 1.7]                | 1.1%                         | 2.9%      | 1.6%  | 0.8% | 0.1%  | 0.3% | 0.01%        |

The uniform column is not just inaccurate but **non-monotone** (n12 worse than
n9 at r=1.5; error oscillates as `n_z` climbs) — the proposed default `n_z=12`
is nowhere near converged and can be *further* from truth than `n_z=9`. No fixed
uniform `n_z` is defensible. (Reviewer independently measured 7.6%→21.7% at
n9→12, r=1.5; sign of the effect matches, magnitude differs with reference
choice — the qualitative non-monotonicity is robust.)

### 5.2 The fix: locate the belt edge analytically, integrate piecewise

The belt boundary in `z` is available in closed form. With `ζ ≡ z − h_b`,
`e_axis = (\cosα, 0, −\sinα)` and `\cosΘ = [x\cosα − ζ\sinα]/s`,
`s^2 = x^2+y^2+ζ^2`, the membership condition `\cos^2Θ ≤ \sin^2δ` becomes, after
clearing `s^2`, a **quadratic in `ζ`**:

$$
A,ζ^2 + B,ζ + C \\le 0,\\quad
\\begin{cases}
A = \\sin^2α - \\sin^2δ\\
B = -2,x\\cosα\\sinα\\
C = x^2\\cos^2α - (x^2+y^2)\\sin^2δ
\\end{cases}
\\qquad (5)
$$

Its real roots `ζ_\pm = (-B \pm \sqrt{B^2-4AC})/(2A)` map to crossing heights
`z_\pm = h_b + ζ_\pm`.

> **Implementation note — numerically-stable quadratic (src/).** The written
> form `(-B \pm \sqrt{B^2-4AC})/(2A)` is used only for exposition. The `src/`
> solver (`_stable_quadratic_roots`, `fragmentation.py`) uses the
> cancellation-free variant (Numerical Recipes §5.6):
> `q = -\tfrac12\big(B + \operatorname{sgn}(B)\sqrt{B^2-4AC}\big)`, roots `q/A`
> and `C/q`. Two failure modes of the naive form motivate this: (i) catastrophic
> cancellation when `B^2 \gg 4AC` (one root is a small difference of large
> numbers); and (ii) division by the vanishing leading coefficient
> `A = \sin^2α - \sin^2δ` as the **angle of fall approaches the spray
> half-angle** (`α → δ`) — a physically reachable low-angle-of-fall regime the
> §6.3 worked example (AoF `90°`, `δ = 15°`) never exercises. When `|A|≈0` the
> solver falls back to the linear root `ζ = -C/B`, and the four-zone belts
> (`A = \sin^2α - K^2`, `K = \cosθ^z ± \sinδ`) reuse the same stable routine.
> Verified stable at `α = 16°, δ = 15°` (`|A| ≈ 6·10^{-3}`): finite roots,
> `P_k∈[0,1]`, and no blow-up versus the naive form.

The belt-membership set within the column is found robustly
for **all** cases (steep fall `A>0` ⇒ interval between roots; shallow fall `A<0`
⇒ complement of the roots; `A≈0` linear; no real roots ⇒ whole column or none)
by: take breakpoints `\{0,h\}∪\{z_\pm∈(0,h)\}`, test the sign of the LHS of (5)
at each sub-interval midpoint, and keep the sub-intervals where it is `≤0`. Over
the *open* interior of each kept sub-interval `(a_m,b_m)` the integrand is
**continuous** — only the smooth `1/s^2` spreading and `m_\min(s)` vary — so a
composite rule with a small fixed `n_\text{seg}` converges as `O(1/n_\text{seg}^2)`.

**Sample strictly-interior nodes — never the belt-edge endpoint (revision 2).**
The endpoints `a_m,b_m` returned by eq. (5) are the analytic roots of the
membership test. `lethal_density_point` **independently re-derives** that same
`|\cosΘ|\le\sinδ` test from `(x,y,z)` (`fragmentation.py:485`), so evaluating
`ρ_L` *exactly at a root* is a floating-point coin flip: rounding can place the
node just **outside** the belt and return `0.0`, even though the interior limit
approaching from inside the segment is finite (`ρ_L` has a genuine **jump** at
the belt edge — its endpoint value is ill-defined for quadrature regardless).
A composite **trapezoid**, which weights the endpoints, therefore loses up to
`ρ_L(a_m)\,Δz/2` whenever the lower node coin-flips to zero — an
`O(1/n_\text{seg})` bias (`≈ -1/(2n_\text{seg}) ≈ -5.6\%` at `n_\text{seg}=9`),
recurring intermittently across `r` and only *halving* under an `n_\text{seg}`
doubling, so the doubling check does not flag it. The fix is the **composite
midpoint rule**, whose nodes are all strictly interior:

$$
\\lambda(x,y) ;=; w\_\\perp \\sum\_{m}\\int\_{a_m}^{b_m}!\\rho_L(x,y,z),dz
;\\approx; w\_\\perp \\sum\_{m}\\ \\frac{b_m-a_m}{n\_\\text{seg}}
\\sum\_{k=0}^{n\_\\text{seg}-1}\\rho_L!\\Big(x,y,;a_m+\\big(k+\\tfrac12\\big)\\tfrac{b_m-a_m}{n\_\\text{seg}}\\Big).
\\qquad (6)
$$

Midpoint never evaluates `ρ_L` at a belt edge, so the gate always passes and the
sampled value is always the correct smooth interior density; it retains the same
`O(1/n_\text{seg}^2)` order as the trapezoid for the smooth interior integrand.
The step is thus removed from the quadrature *domain* (eq. 5) **and** the sampled
nodes avoid the residual jump at the domain edge. A fine `r`-sweep (§5.4) confirms
`n_\text{seg}=9` midpoint is `<0.005\%` at **every** `r` — versus the trapezoid's
recurring `-5.4\%` — an order of magnitude cheaper than the `n_z≈192` a uniform
grid needs. **Adopt the composite-midpoint eq. (6) with `n_seg = 9` per belt
segment** as the default; a doubling check on `n_seg` is cheap insurance for the
steep-integrand corner (§5.3) but is no longer load-bearing.

### 5.3 Residual accuracy risk near the burst

The one place `n_seg=9` could under-resolve is a column passing **very close to
the burst** (`r→0` with `h_b∈[0,h]`), where the belt segment shrinks toward
`z=h_b` and the `1/s^2 ~ 1/(r^2+ζ^2)` spreading peaks inside it. The peak is
integrable over the finite segment and the exact `s→0` singularity is bounded by
the kernel's `s_floor` guard; the segment also narrows as `r→0`, so `λ→0`
continuously (no spurious spike). Still, for the near-ground-zero column the
`n_seg`-doubling check should be honoured and `n_seg` raised if it does not
settle. This is the correct residual caveat — see A4 in §7.

- **m_min table.** `m_\min(s)` depends only on slant range `s`, not on which `z`
  produced it, so one `s_grid`/`m_\min` table covering the whole `[0,h]` column
  is built once per column and shared across all `z`-samples (the shared-grid
  optimisation noted originally). It must span `s` from the geometric minimum
  `\max(0, h_b−h, −h_b)` (with the `s_floor`) to the column's max slant range.

**Line variant.** The app cross-sections sample a 1-D `(x,y)` line. Eq. (2)/(6)
is identical there — evaluate the piecewise column integral at each `line_coords`
point. No new physics; a Family-B line-density/pkill wrapper is a thin
implementation helper (the existing `four_zone_line_split` is the *graded*
Family-A path and is a separate aspect, §5 of scoping — do not repurpose it here).

### 5.4 Fine `r`-sweep — the trapezoid coin-flip bias and the midpoint fix

The revision-1 endpoint-inclusive trapezoid was re-tested against the gate-free
interior reference on a **dense** sweep `r = 1.2 … 7.0 m` in `0.1 m` steps (59
columns inclusive, same §6.3 config), not just the original six table points:

| method (`n_seg=9`)                   | worst \|rel-err\| over the 59-column sweep |
| ------------------------------------ | ------------------------------------------ |
| endpoint trapezoid (rev-1 eq. 6)     | **5.45 %** (intermittent)                  |
| **composite midpoint (rev-2 eq. 6)** | **0.005 %** (uniform)                      |
| composite midpoint, `n_seg=18`       | 0.001 %                                    |

The trapezoid error is **not** spread smoothly: it is `≈0` at most `r` but jumps
to `-5.4%` at the subset of columns (`r = 1.6, 1.7, 1.9, 2.3, 3.2, 4.0, 4.1, 4.5, 4.6, …`) where the lower belt-edge node `a_m = z_lo` rounds *outside* the
belt and `lethal_density_point` returns `0.0`, dropping its `Δz/2` weight — the
predicted `≈ -1/(2n_\text{seg}) = -5.6\%`. **The original six-point check
(§6.3) missed this entirely because all six of its `r` values happen to be
non-coin-flip columns** (trapezoid error `-0.00%` at each) — the exact hazard of
verifying only at hand-picked points. The midpoint rule, sampling strictly
interior nodes, is `<0.005%` at *every* column including the coin-flip ones, and
is monotone under `n_seg` refinement. This confirms the fix holds across the
domain, not merely at the tabulated points. (Harness:
`updates/target-height-intercept/_scratch/quad_check.py`, transient.)

## 6 · Checks

### 6.1 Dimensions

| Quantity        | Expression                  | Units                    | ✓                        |
| --------------- | --------------------------- | ------------------------ | ------------------------ |
| eq. (2) `λ`     | `w_perp · ∫ρ_L dz`          | `m · (m⁻² · m) = m⁰` = – | ✓ (a count)              |
| eq. (6) segment | `w_perp · midpoint[ρ_L] dz` | `m · m⁻² · m = –`        | ✓                        |
| eq. (5) LHS     | `A ζ² + B ζ + C`            | all `m²` (compared to 0) | ✓                        |
| eq. (3) `P_k`   | `1 − exp(−λ)`               | `–`, `λ≥0 ⇒ P_k∈[0,1)`   | ✓                        |
| eq. (4) `A_f`   | `w_perp · h`                | `m·m = m²`               | ✓ (matches `A_ref` unit) |

### 6.2 Degenerate-density limit (self-consistency with shipped model)

Checklist item 1. The shipped `ρ_L(z{=}0)·A_ref` transform is recovered when the
belt **floods the whole column** and the density is `z`-flat over a human height
(low angle of fall, target in the open footprint). In that regime the membership
segment of eq. (6) is the entire `[0,h]`, and with `ρ_L(z) ≡ ρ_L^0` the composite
midpoint over `[0,h]` is exact for a constant integrand:
`λ = w_perp·ρ_L^0·h = ρ_L^0·A_f`, reproducing eq. (1) with `A_ref = 0.85`
**exactly**. (The premise "`ρ_L ≡ ρ_L^0` over all of `[0,h]`" *is* the whole-column
membership case — a partially-illuminated column has `ρ_L=0` on part of `[0,h]`
and is not `z`-flat, so this limit is self-consistent.) ✓

### 6.3 False safe zone removed at AoF = 90° (the target defect)

Checklist item 3. Config: AoF `= 90°` (vertical fall ⇒ equatorial cylinder belt
horizontal), `h_b = 2.0 m` (default), `δ = 15°`, STANDING (`h = 1.7`). A fragment
leaving the belt at angle `β` below horizontal (`β ≤ δ`, no gravity so it holds a
straight ray) crosses height `z` at horizontal range `r(z) = (h_b − z)/\tanβ`.
The belt's steepest edge `β = 15°` reaches:

| target height `z`  | `r` where belt edge crosses `z` |
| ------------------ | ------------------------------- |
| head, `z = 1.7 m`  | `0.3/\tan15° ≈ 1.1 m`           |
| chest, `z = 1.0 m` | `1.0/\tan15° ≈ 3.7 m`           |
| feet, `z = 0 m`    | `2.0/\tan15° ≈ 7.5 m`           |

The old `z = 0` test lights the ground only near `r ≈ 7.5 m`; for `r < 7.5 m` it
reads `P_k = 0` (the false ring). Under eq. (2) the column `[0,1.7]` intersects the
illuminated belt band for **every** `r` from ≈1.1 m outward, so `∫₀^{1.7} ρ_L dz > 0`
and `P_k > 0` across the ring. The false safe zone is removed exactly where a
standing soldier would in fact be struck at head-to-chest height. ✓

Physical honesty check on the inner edge: for `r < 1.1 m` even the top of the head
sits below the belt's lowest ray, so eq. (2) still returns `≈0` there — correct, a
horizontal belt at 2 m genuinely passes over someone standing directly under it.
The fix fills the *reachable* ring, not a spurious blanket.

**Numeric confirmation (eq. 6 composite-midpoint quadrature, `n_seg=9`).**
Evaluating the column integral with the shipped kernel at this exact config gives
a strictly positive kill across the whole ring — the belt segment is the analytic
`[h_b−r\tanδ,\,h]∩[0,h]` (§5.2), and `P_k` is computed, not asserted. These six
`λ` values are unchanged from revision 1 because all six `r` are non-coin-flip
columns (§5.4); they are re-confirmed here against the midpoint rule to `<0.005%`:

| `r` [m] | belt segment `[z_lo, 1.7]` [m] | `λ` [count] | `P_k = 1−e^{−λ}` |
| ------- | ------------------------------ | ----------- | ---------------- |
| 1.2     | [1.678, 1.7]                   | 3.20        | 0.959            |
| 1.5     | [1.598, 1.7]                   | 9.74        | 1.000            |
| 2.0     | [1.464, 1.7]                   | 12.7        | 1.000            |
| 3.0     | [1.196, 1.7]                   | 11.9        | 1.000            |
| 5.0     | [0.660, 1.7]                   | 8.61        | 0.9998           |
| 7.0     | [0.124, 1.7]                   | 6.44        | 0.998            |

`P_k > 0` for every `r ≥ 1.2 m` (the old `z=0` transform read `0` for all
`r < 7.5 m`): the false safe ring is removed. The `P_k=0.959` at `r=1.2 m` (belt
grazing only the top 22 mm of the head) and the smooth decay toward the `r≈1.1 m`
inner edge confirm the honesty check above — the fill tapers to zero exactly where
the belt lifts off the head, not abruptly. ✓

### 6.4 Monotonicity / bounds

`ρ_L ≥ 0 ⇒ λ ≥ 0 ⇒ P_k ∈ [0,1)`; `λ` non-decreasing in `h` (extending the column
only adds non-negative flux) — so a taller silhouette is never scored less lethal,
as required. Standing (`h = 1.7`) ≥ prone (`h = 0.3`) for the same `(x,y)` flux,
consistent with §4. ✓

### 6.5 Straight-line constraint

Eq. (2) uses only the existing belt-flux `ρ_L`; no trajectory integration, no
gravity. The one added root-finding is the **closed-form** quadratic eq. (5) for
the belt-edge crossing height — an algebraic solve, not an iterative trajectory
integration — so the straight-line constraint holds. The column crossing is now
an *explicit* ray-vs-segment intercept (eq. 5), replacing the implicit
`z`-sampling. PASS.

## 7 · Assumptions and deferred refinements

- **A1 — frontal projection (no obliquity `\cosγ`).** Each strip contributes
  `w_perp\,dz`, i.e. the frontal projected area for horizontal arrival (`γ = 0`).
  This matches the shipped `A_ref = presented_area(γ=0)` convention
  (`pkill-poisson-field` §1: `P_k` deliberately abstracts arrival angle). A proper
  obliquity factor would multiply by `\cosγ(z) ≤ 1`, but that also rescales the
  `z = 0` baseline and would break the §6.2 continuity with the shipped field —
  and for the defect scenario (near-horizontal belt, `γ ≈ 0`) `\cosγ ≈ 1`, so it
  is immaterial there. Obliquity + the top-down `d\sinγ` term (§4) belong to the
  graded Family-A `presented_area(γ)` treatment (scoping §5, deferred aspect), not
  this minimal straight-line fix.
- **A2 — Poisson / binary-cut caveats inherited unchanged** from
  `pkill-poisson-field` §2 (A1/A2): independence/no shielding, sharp `E_leth`
  cut with `P_{k|hit}=1` once counted. Eq. (2) changes only the mean count `λ`,
  not these.
- **A3 — vertical target, flat ground.** The person is a vertical column at fixed
  `(x,y)`; terrain and body tilt are ignored (consistent with the rest of the
  ground-field model).
- **A4 — quadrature accuracy is bounded away from the belt edge, not at it.**
  The `ρ_L` integrand steps discontinuously at the belt boundary (`lethal_density_point`'s
  `0/1` membership cutoff); a uniform trapezoid over `[0,h]` therefore has
  `O(Δz)`, **non-monotone** error (§5.1) — refining `n_z` can *worsen* it. Eq. (6)
  removes the step from the quadrature domain by solving eq. (5) for the crossing
  height analytically and integrating the smooth belt-interior segment with a
  **composite-midpoint** rule whose nodes are all strictly interior — never the
  belt-edge endpoint, where `lethal_density_point`'s independently re-derived
  `0/1` gate coin-flips to `0.0` and biases an endpoint-weighted trapezoid by
  `O(1/n_seg)` (`-5.4%` at `n_seg=9`; §5.2, §5.4). Midpoint is `<0.005%` accurate
  at `n_seg=9` across a dense `r`-sweep (§5.4, table). The **residual** risk is the
  near-ground-zero column (`r→0`, `h_b∈[0,h]`): the `1/s²` spreading peaks inside
  a shrinking belt segment; the `s_floor` guard bounds the `s→0` singularity and
  `λ→0` continuously, but `n_seg` should be raised there if a doubling check does
  not settle (§5.3). A secondary risk is that the belt-edge sharpness itself is a
  *modelling* artifact of the hard `0/1` cutoff — a physical belt has a soft
  angular falloff — so `P_k` right at the inner ring edge is only as crisp as that
  cutoff; this is inherited from the `ρ_L` kernel, not introduced here.

## 8 · What implementation will touch (next pass, not this one)

Per scoping §4, replace the `ρ_L(z=0)·A_ref` transform with eq. (2)+(3)+(6) on the
Family-B **ground** fields: `four_zone_pkill_field` (`zones.py`) and its
single-zone twin `pkill_field_3d` (`fragmentation.py`), reading `(w_perp, h)` from
a `PostureParams` argument and integrating over `[0,h]` by the **piecewise-on-belt
quadrature** eq. (6): per column solve eq. (5) for the belt-membership segment(s)
of `[0,h]`, then composite-midpoint `ρ_L` over each with `n_seg=9` — sampling
strictly-interior nodes so the belt-edge gate never coin-flips (§5.2). Share one
`m_min(s)` table per column across `z`-samples (§5.3). Add a Family-B line helper
for the app cross-sections (thin wrapper, §5). **Do not** modify the
ρ_L kernel, the volume builders (`*_lethal_density_volume`, `*_pkill_volume` —
those remain the point-in-space diagnostic, scoping §2), or `fragment_ground_impact`
(feeds no field, scoping §1/§3). `A_ref` stays as the diagnostic default for the
single-height point transform only.
