# Derivation — Family-A false safe zone (graded ground P(kill) heatmaps)

**Author:** modeler agent
**Status:** derivation pass — no `src/arty/` implementation (derivation.md only)
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Scoping:** `updates/familyA-false-safe-zone/scoping.md` (approved; **Option 2** —
relocate the Family-A belt gate + ray geometry to the illuminated column, keep the
graded `A_p(γ)·pk_given_hit(E)` kernel intact — selected §4, not re-litigated here).
**Reuses (unchanged):**
- `updates/target-height-intercept/derivation.md` — eq. (5) belt-edge quadratic
  and `belt_column_breakpoints`/`_stable_quadratic_roots` (derived, implemented,
  reviewed). This aspect **calls** that machinery; it does not modify it.
- The Family-A kernel `_four_zone_familyA_eval` / `_expected_kills_3d_point`
  (`presented_area(γ)·pk_given_hit(E)` belt integral) — **unchanged**; only the
  height at which it is evaluated moves.

This aspect changes **only** the `z`-location at which the graded Family-A kernel
reads its geometry — from the fixed ground ray (`z = 0`) to the height where the
belt actually illuminates the target column. No new kernel, no gravity,
straight-line rays throughout.

______________________________________________________________________

## 1 · The defect, Family-A specific

The shipped Family-A per-cell mean lethal-hit count (four-zone
`_four_zone_familyA_eval`; single-zone twin `_expected_kills_3d_point`) is, per
active zone with belt-centre polar cosine `cosθ^z`,

$$
N_z(x,y) \;=\; \mathbf{1}\!\big[\,|\cos\Theta-\cos\theta^z|\le\sin\delta\,\big]\;
\frac{A_p(\gamma)}{2\pi s^2\,\cdot 2\delta\,\cdot g}\;
\underbrace{\int pdf^z(m)\,pk_{|hit}\!\big(E(s)\big)\,dm}_{J^z(s)},
\qquad
P_k = 1-\exp\!\Big(-\textstyle\sum_z N_z\Big),
\tag{1}
$$

with **every geometric quantity taken on the single ray to the feet** `(x,y,-h_b)`:
`s=√(x²+y²+h_b²)`, `γ=arcsin(h_b/s)`, `cosΘ` on that ray, and `g = sinθ^z`
(four-zone) or `g = sinΘ` (single-zone legacy). `E(s)=½m(V_0 e^{-λ(m)s})²`.

**Why Family-A is a *different* defect from Family-B.** The presented area
`A_p(γ)=w_\perp(h\cos\gamma + d\sin\gamma)` (`fragmentation.py:190`) **already
carries the target's vertical extent** — the `h\cos\gamma` frontal term *is* the
standing silhouette, the `d\sin\gamma` term the top-down footprint. So Family-A is
not missing the height in the *silhouette* (Family-B's defect, fixed by
`w_\perp∫₀ʰρ_L\,dz`). It is missing the height in the **field geometry**: the belt
gate and `s,γ,cosΘ` are sampled only along the feet-ray. At steep angle of fall the
near-horizontal belt fails the `z=0` gate close in and the **whole** cell zeros —
the false ring — even though the belt crosses the ray to the chest/head.

This is exactly why a naive column integral of eq. (1) is **wrong**: `A_p` already
contains `w_\perp h`, so `∫₀ʰ A_p(γ)\dots dz` would double-count the height. The
minimal correct fix relocates *where* the kernel is read, not the silhouette size.

## 2 · Governing change — evaluate the kernel at the illuminated height

Model the target as the vertical column `z∈[0,h]` at ground `(x,y)`. A target point
at height `z` is seen along the ray from the burst `(0,0,h_b)`; with `ζ = z-h_b`,

$$
s(z)=\sqrt{x^2+y^2+\zeta^2},\quad
\cos\Theta(z)=\hat e\cdot\frac{(x,y,\zeta)}{s},\quad
\gamma(z)=\arcsin\!\frac{h_b-z}{s(z)} .
\tag{2}
$$

At `z=0` (2) reduces to the shipped feet-ray values. The belt-membership set of the
column, `\{z\in[0,h]:|\cos\Theta(z)-\cos\theta^z|\le\sin\delta\}`, is the **already
derived** piecewise set: its edges are the roots of the belt-edge quadratic
(`target-height-intercept` eq. 5), returned by `belt_column_breakpoints(x,y,h_b,
α,δ,[\cosθ^z],0,h)` — no new geometry.

**The fix.** For each active zone: (i) gate on the belt illuminating the column,
`belt∩[0,h]≠∅`; (ii) evaluate the *unchanged* kernel of eq. (1) at a
**representative illuminated height** `z_{rep}` in place of `z=0`:

$$
\boxed{\;N_z(x,y)=\mathbf{1}\!\big[\text{belt}\cap[0,h]\neq\varnothing\big]\;
\frac{A_p(\gamma(z_{rep}))}{2\pi s(z_{rep})^2\,2\delta\,g(z_{rep})}\,
J^z\!\big(s(z_{rep})\big)\;}
\tag{3}
$$

with `g=sinθ^z` (four-zone, fixed) or `g=sinΘ(z_{rep})` (single-zone). `P_k` and the
Poisson wrapper are unchanged. The graded weighting — `pk_{|hit}(E)`, the obliquity
in `A_p(γ)`, the per-zone `J^z`, the diff map, the per-zone attribution — all
survive untouched; only the evaluation height moves.

**Qualification (the `cosΘ` handling is *not* verbatim-unchanged).** The membership
in eq. (3) is decided by `belt_column_breakpoints`, so the kernel's **own internal
belt gate must be bypassed** at `z_{rep}` — it must not re-test `|cosΘ-cosθ^z|≤sinδ`
from scratch, because `z_{rep}` is by construction an exact root of that inequality
and recomputing `cosΘ` there is a floating-point coin-flip (§3.1). For the single-zone
legacy kernel, whose magnitude also carries `1/\sinΘ(z_{rep})`, `cosΘ` at the belt
edge is the **analytically known** value `cosθ^z±\sinδ`; use it directly rather than
recomputing from `(x,y,z_{rep})`. The four-zone kernel uses `1/\sinθ^z` (fixed) and
`cosΘ` **only** in the gate, so once the gate is bypassed it needs no `cosΘ` at all
and is coin-flip-free. So "only the height moves" holds for the *magnitude physics*,
but the gate/`cosΘ` plumbing at `z_{rep}` needs the bespoke treatment specified in
§3.1 — not a verbatim call to the shipped per-point kernel.

### Symbols

| Symbol | Meaning | Unit |
| --- | --- | --- |
| `z_{rep}` | representative illuminated height (fork 1) | m |
| `belt_column_breakpoints` | reused belt∩[0,h] edge finder (eq. 5) | — |
| `A_p(γ)=w_⊥(h\cosγ+d\sinγ)` | lumped presented area, **unchanged** | m² |
| `J^z(s)` | zone mass integral `∫pdf·pk_{|hit}(E(s))dm`, **unchanged** | count |

## 3 · Fork resolutions

### 3.1 Representative height (fork 1) — `z_{rep}=` lowest lit edge, evaluated coin-flip-free

Take `z_{rep}` = the **lower edge of the lowest belt-active sub-interval of `[0,h]`**
(nearest the feet). Membership of each candidate sub-interval is tested at its
**midpoint** (never an endpoint), the same interior-sampling guard the sibling
quadrature uses. Rationale for the *lowest lit edge*:

1. **Exact reduction, by continuity.** When the belt reaches the feet, `z=0` lies in
   the lowest active segment, so `z_{rep}=0` and eq. (3) is *algebraically
   identical* to the shipped eq. (1) — reproduced to floating-point round-off in
   §4/§5 (the relocated expression order differs, so agreement is `~10^{-15}`, the
   codebase's usual vec-equivalence tolerance, not the literal bit). `z_{rep}(r)`
   is continuous (a
   moving quadratic root), so the relocated field joins the shipped field with **no
   seam** at the feet-lit boundary.
2. **Conservative flux among lit heights — *for `h_b>h`*.** When the burst is above
   the head (`h_b>h`), `s(z)=√(r²+(h_b-z)²)` is largest at the lowest lit height, so
   `z_{rep}` reads the *smallest* `1/s²` flux of any lit height — the least-aggressive
   representative, partially offsetting the lumped over-count of §7 A1. **This
   ordering does not hold for `h_b≤h`** (low airburst, burst inside the column,
   reachable on the app's `h_b∈[0,20]` slider): there `s` is minimised near `z=h_b`
   inside the column and `z_{rep}` is not guaranteed least-aggressive — the fix is
   still correct (the gate/reduction of §2/§4 is unconditional on the `h_b`–`h`
   ordering), only the A1 bias-*direction* narrative is unproven there (§7 A1).
3. **Robust to spurious/duplicate breakpoints.** Spurious `\cosΘ=-K` roots only
   subdivide an already-active region into adjacent active sub-intervals of the same
   membership; the lowest active sub-interval's lower edge is still the true lower
   belt edge.

**Evaluating the kernel at `z_{rep}` — the numerically-safe rule (revision 1).** The
original claim that "evaluating on the belt edge is safe because membership is already
established" was **wrong as stated** and is corrected here. Unless `z_{rep}=0` (feet
lit), `z_{rep}` is by construction an exact root of the gate inequality
`|\cosΘ-\cosθ^z|=\sinδ`. Re-computing `\cosΘ` from `(x,y,z_{rep})` reproduces that
boundary to `~10^{-16}`, and whether it lands inside or outside the strict `≤` gate is
pure rounding luck — a **floating-point coin-flip** that silently returns `N=0` (the
unfixed false-safe defect) on a rounding-dependent subset of the ring. Executed on the
§5.1 config this zeroed **4 of the 6** worked points and **54 of 316** dense-sweep
cells (§5). This is the *same* coin-flip the sibling aspect recorded for `ρ_L`
evaluated at a breakpoint (`target-height-intercept` §5.2); §3.1 correctly applied the
interior-midpoint guard to the *membership test* but then reintroduced it by choosing
the *evaluation point itself* to be the root. The rule that removes it:

- **Bypass the kernel's internal belt gate at `z_{rep}`** — membership is already
  decided by `belt_column_breakpoints`; do not re-test `|\cosΘ-\cosθ^z|≤\sinδ`.
- **Four-zone:** the magnitude is `A_p(γ)\,J^z/(2π s²\,2δ\,\sinθ^z)` — `\cosΘ` appears
  **only** in the (now-bypassed) gate, so no `\cosΘ` is computed and the path is
  coin-flip-free by construction (verified: relocated four-zone fires with `N=182` at
  `r=2` m where the old `z=0` read 0, §5).
- **Single-zone (legacy `1/\sinΘ` factor):** at a belt-edge `z_{rep}` the boundary
  value is the **analytically known** `\cosΘ=\cosθ^z±\sinδ` (`=±\sinδ` for the
  equatorial belt, `\cosθ^z=0`), so use `\sinΘ(z_{rep})=\sqrt{1-(\cosθ^z±\sinδ)^2}`
  (`=\cosδ` equatorial) directly instead of recomputing `\cosΘ` numerically — exact by
  construction, no rounding introduced. At the feet-lit case `z_{rep}=0`, `\cosΘ(0)` is
  strictly interior to the belt and is computed normally (this is the reduction case).
  Either this analytic-`K` substitution *or* nudging `z_{rep}` a tiny interior `ε` off
  the root before recomputing `\cosΘ` closes all 6 worked points and the full dense
  sweep (both verified, §5); the analytic-`K` form is preferred as it is exact and
  introduces no tunable `ε`.

Note `\sinΘ(z_{rep})≥\cosδ>0` (equality only at a genuine belt-edge root; strictly
`>\cosδ` at the interior feet-lit `z_{rep}=0`), so the single-zone `1/\sinΘ` divide is
always finite.

### 3.2 Fraction weighting (fork 2) — **rejected**

Scoping flagged scaling `A_p` by the lit column fraction `f=(z_{hi}-z_{lo})/h`.
**Reject it.** A lumped lethal silhouette is killed by *any* lethal intercept: a
chest-band hit is as lethal as a whole-body spray. `f`-weighting would score a
chest-only illumination at `f·A_p` — spuriously **discounting a lethal hit**, biasing
`P_k` **downward** (the unsafe direction for a hazard model). It also would break the
exact-reduction identity on partially-lit-but-feet-lit cells. Keeping the full `A_p`
whenever `belt∩[0,h]≠∅`:

- gives **exact** reduction to the shipped value on *every* feet-lit cell (stronger
  than a flooded-limit-only reduction; §4);
- yields a sharp onset at the belt-lift-off radius `r=(h_b-h)/\tanδ` (person's head
  entering the lethal belt) which is **physically correct** for a lumped lethal
  silhouette and **matches the reviewed Family-B behaviour** — Family-B jumps from
  `P_k=0` (`r<1.12` m) to `P_k=0.959` at `r=1.2` m (`target-height-intercept`
  derivation §6.3), i.e. a near-step, not a gentle ramp. A smooth `f`-taper would
  *disagree* with the reviewed sibling.

The cost is a bounded, **conservative-high** over-count in the thin grazing ring
(full standing `A_p` scored when only the head band is lit) — logged as a limitation
(§7 A1), the safe error direction, and preferred to `f`-weighting's under-count.

## 4 · Reduction to the shipped kernel (self-consistency)

For any cell where the belt already crosses the feet (`z=0∈`belt, i.e.
`r≥h_b/\tanδ` at AoF 90°), the lowest active segment includes `z=0`, so `z_{rep}=0`
(the column bound, strictly interior to the belt — not a belt-edge root), and eq. (3)
evaluates the identical `s,γ,cosΘ,A_p,J^z,g` of eq. (1) at the identical point —
**an algebraic identity, `N_z^{new}=N_z^{old}`**, not an approximation. The
implementation realises it to **floating-point round-off** (the relocated vectorised
expression order differs from the shipped one, so the two agree to `~10^{-15}`, the
same round-off the codebase accepts for its vec/scalar equivalences — not the literal
bit). **Confirmed this pass** (executed: feet-lit cells at `r=7.5,8,12,20` m reproduce
the shipped kernel with `max|Δ|≈1.8·10^{-15}`, §5.4), locked by a src/ property test
(`tests/test_familyA_false_safe_zone.py::test_feet_lit_reduction`). The fix therefore
changes **only** the cells the old `z=0` sampling zeroed — strictly additive on the
previously-false ring; every already-firing cell is unchanged to round-off and the
inner dead zone stays exactly `0`.

## 5 · Checks — executed against the shipped `arty` code

All checks below were **run** against the current `src/arty` machinery
(`belt_column_breakpoints`, `presented_area`, `pk_given_hit`, `_shell_axis`,
`_familyA_zone_massintegral`, `_four_zone_familyA_eval`) via `uv run python`
(numpy 2.4.6 — the earlier §7 A5 "numpy unavailable" premise was wrong and is
corrected), mirroring the sibling aspect's executed §5.4 sweep. Config of the defect:
AoF `=90°` (horizontal equatorial belt), `h_b=2.0` m, `δ=15°`. The belt reaches height
`z` at horizontal range `r(z)=(h_b-z)/\tanδ`; the lowest lit height is
`z_{rep}(r)=\max(0,\,h_b-r\tanδ)`. `belt∩[0,h]≠∅ ⇔ r≥(h_b-h)/\tanδ`.

### 5.0 The coin-flip, and the fix (executed)

The naive recipe (`z_{rep}=` lowest edge, recompute `\cosΘ`, re-gate) vs. the
revision-1 rule (§3.1: bypass gate, analytic-`K`), single-zone, standing:

| `r` [m] | `z_{rep}` | `N` naive (recompute+gate) | `N` fixed (analytic-`K`) |
| --- | --- | --- | --- |
| 1.2 | 1.678 | **0** (coin-flip) | 510.7 |
| 1.5 | 1.598 | **0** | 324.1 |
| 2.0 | 1.464 | **0** | 181.4 |
| 3.0 | 1.196 | **0** | 79.3 |
| 5.0 | 0.660 | 27.8 (passes by luck) | 27.8 |
| 7.0 | 0.124 | 13.8 (luck) | 13.8 |

The naive rule zeros 4 of 6 worked points (reproducing the reviewer's finding) and
**54 of 316** cells on a dense sweep `r∈[1.13,7.45)` step 0.02 m. The fixed rule zeros
**0 of 316**, with `min N=12.1 ⇒ min P_k=0.999995` across the whole ring. ✓

### 5.1 False safe ring removed (checklist: the target defect)

| feature (standing, `h=1.7`) | radius |
| --- | --- |
| head enters belt → **onset** `r=(h_b-h)/\tanδ` | **1.12 m** |
| chest (`z=1.0`) in belt | 3.73 m |
| feet (`z=0`) in belt → reduction regime `r=h_b/\tanδ` | 7.46 m |

The old `z=0` kernel lights the ground only at `r≳7.46` m and reads `P_k=0` for all
`r<7.46` m (the false ring). Under eq. (3) the column `[0,1.7]` intersects the belt
for **every** `r≥1.12` m, so `z_{rep}∈(0,1.7)` there, the gate passes, and `N_z>0`
(the kernel is strictly positive when the gate holds and `A_p,\,J^z>0`). The ring
`1.12 m ≤ r < 7.46 m` flips from `P_k=0` to `P_k>0` — the false safe zone is removed
exactly where a standing soldier is in fact struck at head-to-chest height. ✓

The `z_{rep}(r)` values are, by construction, the **same belt segments** the reviewed
Family-B fix tabulates (`target-height-intercept` §6.3): `r=1.2→1.678`,
`1.5→1.598`, `2.0→1.464`, `3.0→1.196`, `5.0→0.660`, `7.0→0.124` — identical, since
both families share the one belt gate; only the weighting on each segment differs.
This cross-checks the geometry against an already-reviewed result.

### 5.2 Inner-edge honesty (checklist)

For `r<1.12` m even the top of the head sits below the belt's lowest ray, so
`belt∩[0,1.7]=∅` and eq. (3) returns `N=0` → `P_k=0`. Correct: a horizontal belt at
2 m genuinely passes over someone standing directly under it. The fill covers the
*reachable* ring, not a spurious blanket; the onset at `r=1.12` m is the physical
head-enters-belt transition (§3.2). ✓

### 5.3 Standing vs prone (executed)

Prone (`h=0.3`): onset `r=(2-0.3)/\tanδ=6.34` m. So for `1.12 m ≤ r < 6.34 m` the
standing column reaches the belt while the prone column (capped at 0.3 m) sits
entirely beneath it → **standing fires, prone reads `P_k=0`**. Executed (single-zone,
AoF 90°): `P_k(\text{stand})=1.000, P_k(\text{prone})=0.000` at `r=2,4,6` m; prone
switches on just past its onset (`P_k(\text{prone})=0.999` at `r=6.4` m); and
`P_k(\text{stand})≥P_k(\text{prone})` at **every** sampled `r` (and `N` non-decreasing
in `h` across `h∈[0.3,2.5]`). The model correctly predicts a standing soldier is
*more* exposed near a high-AoF low burst — the physical point, consistent with the
Family-B result (`target-height-intercept` §4). ✓

### 5.4 Reduction and four-zone parity (executed)

- **Reduction (§4):** feet-lit cells `r=7.5,8,12,20` m reproduce the shipped z=0
  kernel to floating-point round-off (`max|Δ|≈1.8·10^{-15}` on `N≈1–10`). The fix is
  strictly additive on the previously-false ring. ✓
- **Four-zone relocated:** the four-zone path carries `\cosΘ` **only** in the gate
  (magnitude uses `1/\sinθ^z`, fixed), so once the gate is replaced by
  `belt_column_breakpoints` membership it is coin-flip-free with no `\cosΘ` needed.
  Executed (AoF 90°, standing): the old `z=0` four-zone reads `N=0` at `r=2,3` m
  (false ring); the relocated evaluation at `z_{rep}` reads `N=182.7, 79.5` there
  (`P_k=1.0`), matching the single-zone magnitudes to the zone-decomposition
  difference. ✓

### 5.5 Off-axis axis-sign trap (executed, A3)

At AoF `=60°`, `x<0`, calling `belt_column_breakpoints` with the **wrong** sign
(`+x`, the natural un-flipped call) vs. the required `-x` (single-zone backward axis,
§7 A3): the wrong call **fabricates a spurious interior breakpoint** — e.g.
`x=-3,y=1`: `-x → [0, 1.7]` (no crossing) vs. `+x → [0, 1.24, 1.7]`; `x=-5,y=0.5`:
`[0,1.7]` vs. `[0, 0.667, 1.7]`. Not a mere sign flip on an existing root — a wrong
sign would gate cells on/off incorrectly for essentially all `AoF≠90°`. A required
off-axis regression test is specified in §8. ✓

## 6 · Dimensions, bounds, straight-line

- **Dimensions.** Eq. (3) is eq. (1) evaluated at a different height — units
  unchanged: `A_p [m²]·J^z[count]/(s²[m²]·δ[-]·g[-]) = [count]`; `P_k=1-e^{-N}∈[0,1)`. ✓
- **Bounds / monotonicity.** `N_z≥0 ⇒ P_k∈[0,1)`. `N` non-decreasing in `h`
  (extending the column can only enlarge `belt∩[0,h]`, never shrink it) — a taller
  silhouette is never scored less lethal. ✓
- **Straight-line constraint.** The only added computation is the **closed-form**
  belt-edge quadratic (eq. 5, reused) — an algebraic solve, not a trajectory
  integration. No gravity, no curvature. The column crossing is now an *explicit*
  ray-vs-segment intercept. PASS.

## 7 · Assumptions and deferred refinements

- **A1 — lumped-silhouette over-count (the family's dual tradeoff).** Family-A
  applies the full lumped `A_p` whenever the belt lights *any* part of the column
  (§3.2). When the belt grazes only a thin band (e.g. the head at `r≈1.2` m), this
  over-counts relative to a flux-resolved model — a **bounded, conservative-high**
  error confined to the thin inner grazing ring, in the safe direction. This is the
  dual of Family-B's tradeoff: Family-A resolves the graded energy/obliquity
  weighting but lumps the vertical flux; Family-B resolves the vertical flux but uses
  a binary lethal-mass cut. Removing it would require the full graded flux integral
  (scoping Option 3), a separate future aspect, not this minimal fix.
- **A2 — representative-height approximation.** Reading `s,γ` at `z_{rep}` rather than
  integrating the graded kernel over the lit band is exact in the far/mid field
  (`s(z)≈s(0)` across the sub-metre column) and reduces exactly on feet-lit cells
  (§4); the residual is the sub-metre `s,γ` variation over the lit band, immaterial
  except very close in where `P_k` is already saturated.
- **A3 — single-zone axis-sign (implementation note).** The single-zone legacy
  kernel uses the *backward* axis `(-\cosα,0,-\sinα)` (`_shell_axis`), which flips the
  sign of `B` in the belt-edge quadratic (eq. 5) relative to the *forward*-axis
  four-zone path; equivalently, call `belt_column_breakpoints` with `-x`. At the
  defect config (AoF 90°, `\cosα=0`) `B=0` and the two coincide, so §5 is unaffected;
  the src/ pass must handle the sign for general AoF. The four-zone Family-A path
  already uses the forward axis and reuses `belt_column_breakpoints` directly.
- **A4 — obliquity / Poisson caveats inherited unchanged** from the Family-A kernel
  and `pkill-poisson-field`: frontal `A_p(γ)` as shipped, sharp `E_leth`/`pk_{|hit}`
  cut, Poisson independence / no shielding. Eq. (3) changes only the evaluation
  height, none of these.
- **A5 — what was executed here, what the src/ pass still owns.** `numpy` (2.4.6) is
  available via `uv run python`, and every function this fix reuses is callable today,
  so §5 was **executed this pass** against the shipped `arty` code, not just derived
  analytically: the coin-flip and its fix (§5.0, 4/6 worked points and 54/316 sweep
  cells zeroed by the naive rule, 0/316 by the corrected rule), the false-ring removal
  and Family-B §6.3 geometry cross-check (§5.1), standing-vs-prone and `h`-monotonicity
  (§5.3), the reduction identity (§5.4, to floating-point round-off), four-zone
  parity (§5.4), and the
  off-axis axis-sign trap (§5.5). What remains genuinely for the src/ pass is **not**
  first-time verification but **permanent regression coverage**: property tests in
  `tests/` that lock these results against future edits — specifically a **dense**
  standing ring sweep asserting `P_k>0` (indeed `≈1`) at **every** `r` on a fine grid
  in `[1.13, 7.4]` m (not a single `max`-over-ring point, which a single lucky cell
  can satisfy while the rest of the ring is silently zero — the exact hole the naive
  rule fell through), the feet-lit reduction to round-off, prone-below-standing,
  and an **off-axis** (`AoF≠90°, x≠0`) single-zone regression pinning the `-x`
  axis-sign (A3) against an independent per-point reference.

## 8 · What implementation will touch (next pass, not this one)

Per scoping §4, relocate the evaluation height in the **Family-A** ground path only:
`_four_zone_familyA_eval` (`zones.py`) and the single-zone twin
`_expected_kills_3d_point`/`_expected_kills_3d_vec` (`fragmentation.py`), and thereby
the field/line wrappers that call them (`_four_zone_field_split`,
`four_zone_line_split`, `four_zone_field`, `compute_frag_field_3d`). Per zone: gate on
`belt_column_breakpoints(x,y,h_b,α,δ,[\cosθ^z],0,h)` non-empty (forward axis;
single-zone `-x`, §7 A3), take `z_{rep}` = lower edge of the lowest active
sub-interval (midpoint membership test). Evaluate the kernel's **magnitude physics**
(`s,γ,A_p,J^z`) at `z_{rep}` — but **do not** call the shipped per-point kernel
verbatim: it re-tests its own belt gate at `z_{rep}`, which is a belt-edge root, and
recomputing `\cosΘ` there is the floating-point coin-flip §3.1/§5.0 documents (4/6
worked points and 54/316 sweep cells falsely zeroed). Instead, per §3.1 revision 1:
**bypass the internal gate** (membership is already decided by the breakpoints); the
four-zone path then needs no `\cosΘ` (its magnitude uses fixed `1/\sinθ^z`), and the
single-zone path substitutes the **analytic** belt-edge `\sinΘ(z_{rep})=\cosδ`
(`\cosΘ=\cosθ^z±\sinδ`) rather than recomputing it — except at the feet-lit reduction
case `z_{rep}=0`, where `\cosΘ(0)` is interior and evaluated normally (giving the
reduction of §4). Keep the full `A_p` (no fraction weighting, §3.2). Add the
regression tests listed in §7 A5 (dense ring sweep, reduction bit-equality,
prone-below-standing, off-axis A3). **Do not** change the kernel magnitude formulas,
the Family-B ρ_L/Poisson fields or their volume builders, or `fragment_ground_impact`
(scoping §5).
