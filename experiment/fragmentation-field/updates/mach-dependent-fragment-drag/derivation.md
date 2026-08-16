# Derivation — fragment retardation anchored to the DoD-1975 ballistic density

> ## ⚠ PARTIALLY RETIRED — 2026-08-03
>
> **The Mach-dependence half of this update is withdrawn and must not be
> cited. The ballistic-density anchor half remains live.**
>
> Ruled by `rebaseline-verdict.md` (15 claims: 8 sound, 4 shifted, 3 void) and
> verified in `challenges/source-data-audit/review-void-rulings.md`. The split:
>
> | Status | Sections | What it covers |
> | --- | --- | --- |
> | **LIVE** | §1–§4, §6, §8 | Identity (4) $C_\text{shape} = (\rho_\text{steel}/k)^{2/3}$, the geometric-admissibility argument, $C_D$ = 1.28 / $C_\text{shape}$ = 2.0890, and the implementation spec. This is the cited source of `src/arty/fragmentation.py:165` and change-log v0.9.0. |
> | **WITHDRAWN** | §5, §7 L3 | The rejection of a Mach-dependent $C_D(M)$ *on accuracy grounds*, and the $B(r)$ residual framing. |
>
> **Why the anchor survives.** C4 (0.585 is *geometrically impossible* — it
> implies a fragment 3.2× denser than steel presenting less area than an
> equal-mass sphere) is pure geometry plus identity (4). It consumes no velocity
> data, no $B(r)$, no $C_D(M)$ curve and no $V_0$, so neither shock reaches it.
> C5 was *confirmed* by the corrected Figure-3 CSV, which reproduces the
> source's own 1.08 / 1.40 / 1.28 to three digits.
>
> **Why the Mach half is withdrawn.** The comparison that rejected it was not
> like-for-like — it gave the constant a fitted parameter and the Fig-3 curve
> none — and it was scored on a 25-point set that was ~44% wrong-column. Given
> both laws the same single scale freedom on the corrected data, the Mach law
> **wins** by ~20–25% RMS on both columns.
>
> **The decision not to model $C_D(M)$ still stands** — on architectural cost at
> an immaterial accuracy difference, not on accuracy. That restatement now lives
> where readers see it, as limitation **15** in `_limitations.qmd`; this folder
> is not the place to look it up.
>
> No new work is planned here. Do not re-open this folder to repair §5 — if the
> Mach law is ever revisited it needs a fresh `updates/<slug>/` change scoped
> against the corrected `figure-3-drag-coefficient.csv`.

**Aspect.** `DragParams` (`C_D`, `C_shape`) and `retardation_coeff` in
`src/arty/fragmentation.py` — the exponential decay rate λ in
`v(s) = V₀·exp(−λs)`.

**What this pass settles.** `scoping.md` ranked the options and recommended
Option 1 (§4/§5): adopt the DoD-1975 anchor, reject the Mach-dependent law.
This document supplies the math that makes that a *derived* parameter rather
than a refit constant — the identity connecting arty's `C_shape` to the
source's ballistic density *k* — plus the unit/limit checks and the three
validation results scoping §5 requires. No `src/arty/` edit is made here; §6
specifies it for the implementation pass.

**Source.** `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/`
`10-F-0806_Fragment_and_Debris_Hazards.md`, sect. "Ballistic Properties"
(printed pp. 7–9) and `figure-3-digitized.md`. Passages below are cited by
greppable quoted string; the extraction is OCR-noisy, so quotes are given
exactly as stored, one line at a time.

## 1. Governing equations

Velocity-squared drag on a fragment of mass *m* with mean presented area *A*,
gravity neglected (source: "velocity-squared law"; "of motion can be integrated
in the case of a constant drag coefficient"):

$$m v \frac{dv}{ds} = -\tfrac12 \rho_{air} C_D A v^2
\;\Longrightarrow\;
v(s) = V_0 e^{-\lambda s},\qquad
\lambda = \frac{\rho_{air} C_D A}{2m}
\quad (1)$$

Two *closures* for *A* exist, and they are the whole content of this pass.

**Source closure — ballistic density.** For geometrically similar fragments
the source writes $m = kA^{3/2}$ (line 317), *k* being the ballistic density
(a.k.a. shape factor), so $A = (m/k)^{2/3}$ and

$$\lambda = \frac{\rho_{air} C_D}{2\,k^{2/3}}\,m^{-1/3},
\qquad L \equiv \lambda^{-1} = \frac{2(k^2 m)^{1/3}}{C_D \rho_{air}}
\quad (2)$$

which is the source's own eq. for *L* (line 350) verbatim.

**arty closure — normalised shape factor.** `retardation_coeff` writes
$A = C_{shape}\,(m/\rho_{steel})^{2/3}$, i.e. presented area per unit
(volume)^{2/3}, giving

$$\lambda = \frac{\rho_{air} C_D C_{shape}}{2\,\rho_{steel}^{2/3}}\,m^{-1/3}
\quad (3)$$

**The identity.** (2) and (3) are the same law iff

$$\boxed{\;C_{shape} = \left(\frac{\rho_{steel}}{k}\right)^{2/3}
\;\Longleftrightarrow\;
k = \frac{\rho_{steel}}{C_{shape}^{3/2}}\;}
\quad (4)$$

Consequence, and the reason this matters: substituting (4) into (3) cancels
$\rho_{steel}$ exactly. **Fragment retardation depends on the ballistic
density *k*, not on the steel density** — $\rho_{steel}$ appears in arty's form
only because `C_shape` is defined relative to it. `C_shape` is therefore not a
free fudge factor: it is a restatement of a *measured* quantity (icosahedron-gage
area/mass measurements on recovered fragments — "the average is taken as the
mean presented area"), and it is
**bounded** by geometry, because no body of given volume presents less area
than a sphere.

## 2. Parameters

| Symbol | Meaning | Unit | Adopted | Source |
| --- | --- | --- | --- | --- |
| $C_D$ | drag coefficient, supersonic plateau | – | **1.28** | "supersonic value of 1.28." |
| $k$ | ballistic density, forged steel projectiles & frag bombs | kg/m³ | **2600** (660 gr/in³) | "value of 660 grains/in.3 (2.60 g/cm3) has been recommended" |
| $C_{shape}$ | arty shape factor, **derived** from (4) at $\rho_{steel}$ = 7850 | – | **2.089** | identity (4) |
| $\rho_{air}$ | air density | kg/m³ | 1.225 (unchanged) | ISA sea level |
| $\rho_{steel}$ | shell steel density | kg/m³ | 7850 (registry) | `arty.shells` |
| — | combined $C_D C_{shape}$ | – | **2.674** (was 0.585) | — |

`scoping.md` §2 quotes `C_shape` = 2.084 / combined 2.67; the exact value at
$\rho_{steel}$ = 7850 is **2.0890 / 2.6739**. The difference (0.2%) is a
rounding artefact in the scoping table and changes nothing downstream; the
derived expression (4), not the decimal, is what should be implemented.

## 3. Unit and limit checks

**Dimensions of (3).** $[\rho_{air}]/[\rho_{steel}]^{2/3}\cdot[m]^{-1/3}$ =
(kg m⁻³)(kg m⁻³)^{−2/3} kg^{−1/3} = kg^{1/3} m^{−1} kg^{−1/3} = **m⁻¹** ✓.
$C_D, C_{shape}$ dimensionless ✓. λs dimensionless in the exponent ✓.

**Identity (4) is exact, not fitted.** $1/\lambda$ from (3) equals *L* from (2)
to 12 significant figures at m = 0.1 g, 1 g, 10 g, 1 kg (check V1 below).

**Geometric limits — the strongest check.** For any closed convex surface the
mean presented area is ¼ the surface area (line 326). Hence, independent of any
data: cube of side *a*, $A = \tfrac14(6a^2) = 1.5\,V^{2/3}$ → $C_{shape}$ =
1.500; sphere, $A = \pi R^2 = \pi(4\pi/3)^{-2/3}V^{2/3}$ → $C_{shape}$ = 1.209.
Inverting the source's *own* tabulated *k* for cubes and spheres (1080 and
1490 gr/in³, line 325–327) through (4) must return the density of steel:

| Geometry | $C_{shape}$ (pure geometry) | $k$ (DoD, line 325) | $\rho_{steel}$ recovered via (4) |
| --- | --- | --- | --- |
| cube | 1.500 | 4271 kg/m³ | **7846 kg/m³** |
| sphere | 1.209 | 5892 kg/m³ | **7832 kg/m³** |

Both land within 0.2% of steel (7830–7850 kg/m³). Identity (4) is confirmed
against the source with no free parameter.

**Admissibility bound.** The sphere is the minimum-area shape, so
$C_{shape} \ge 1.209$ and combined $\ge 1.209 \times 1.08 = 1.31$ (subsonic
$C_D$). The **current 0.585 is not merely low — it is geometrically
impossible**: inverted through (4) at $C_D$ = 1.28 it implies *k* =
25 400 kg/m³, i.e. a fragment 3.2× denser than steel presenting less area than
a sphere of equal mass. The adopted 2.089 sits above the cube (1.500), as it
must for an irregular, non-convex-hull-filling fragment.

**Limit behaviour of (3).** λ ∝ m^{−1/3}: large fragments decay slowly, small
ones fast ✓. λ → 0 as $\rho_{air}$ → 0 (vacuum, straight-line constant speed) ✓.
λ independent of v — the velocity-squared law is scale-free in v, which is
exactly why the exponential closed form survives (and why Mach dependence
cannot be absorbed into λ; see §5).

## 4. Validation

Numbers produced by
[`checks/drag-anchor-validation.py`](checks/drag-anchor-validation.py)
(`uv run python experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/drag-anchor-validation.py`).

### V1 — $L_1$ reproduction (scoping §5 (i)) — PASS

$L_1$ is *L* at m = 1 kg. From (2) at *k* = 2600, $C_D$ = 1.28,
$\rho_{air}$ = 1.225: **241.2 m/kg^{1/3}** against the source's quoted
**247 m/kg^{1/3}** (line 358) — a **2.4% shortfall**, and it is entirely an
air-density convention: 247 inverts to $\rho_{air}$ = 1.196 kg/m³ (≈ air at
24 °C, or the source's own rounding of *k* and the cube root). arty's
$\rho_{air}$ = 1.225 (ISA sea level) is the more defensible choice and is left
unchanged; the 2.4% in λ is ~4% in *v* at λs ≈ 1.6, well inside the ±10%
fidelity bar. For contrast the current constant gives $L_1$ = **1102**, i.e.
4.5× too far.

### V2 — Ordnance velocity decay (scoping §5 (ii)) — PASS

> **CORRECTED 2026-08-03 (C7 — shifted, the PASS survives).** The 25-point set
> below is **mixed-column**: the 105mm series is a digit-for-digit match to
> `105mm-m1-perforation-1-8in.csv`, and the 75mm series used 3 of the 10
> available casualties rows. Re-run cleanly per column
> (`checks/mach-law-rebaseline.py`), the numbers that stand are:
>
> | Combined $C_D C_{shape}$ | casualties, all (n=32) | casualties, M > 0.7 (n=21) | perforation, all = M > 0.7 (n=33) |
> | --- | --- | --- | --- |
> | 0.585 (pre-update) | 0.967 | 0.755 (≈ 2.1× error) | 0.679 |
> | **2.674 (adopted)** | 0.405 | **0.096** (10.1%) | **0.098** (10.3%) |
> | published (mixed set, below) | 0.349 | 0.092 | — |
>
> The ≤ 0.10 bar passes on **each column separately** rather than on a mixture
> — stronger in kind, weaker in margin (4% under the bar, not 8%). The
> conclusion is unchanged: 0.585 fails by ~2× in the lethal band, 2.674 lands
> inside ±10%. Caveat carried from `rebaseline-verdict.md`: $V_0$ is unverified
> and a 10% $V_0$ error is comparable to the entire 0.096 RMS, so this margin is
> not established as robust. The table below is left as published.

RMS of $\ln(v_{model}/v_{source})$ over the 25-point 1944 Ordnance set
(75mm M48 / 105mm M1 / 155mm M107, source-tabulated m(r), v(r)):

| Combined $C_D C_{shape}$ | RMS, all 25 | RMS, arrival M > 0.7 (n = 20) |
| --- | --- | --- |
| 0.585 (current) | 0.864 | 0.710 (≈ 2.0× velocity error) |
| **2.674 (adopted)** | **0.349** | **0.092** (≈ 10% velocity error) |

Bar was RMS(M > 0.7) ≤ 0.10 → **PASS at 0.092**. This test exercises the
retardation law *alone*: it consumes the source's own (m, r, v) triples, with
no Mott spectrum, no lethality threshold and no counting in the path.

### V3 — 155mm demo impact (scoping §5 (iii)) — reproduces

155mm M107, V₀ = 1000 m/s, E_leth = 79 J, post-shape-closure Mott parameters
(μ = 5.07 g, N₀ = 3423):

| s [m] | m_min old [g] | N old | m_min new [g] | N new | ΔN |
| --- | --- | --- | --- | --- | --- |
| 5 | 0.185 | 2827 | 0.295 | 2690 | −5% |
| 20 | 0.276 | 2711 | 0.888 | 2253 | −17% |
| 50 | 0.497 | 2503 | 2.897 | 1608 | −36% |
| 120 | 1.215 | 2098 | 12.081 | 731 | −65% |

Matches scoping §3c to the last digit at the exact `C_shape` = 2.0890 (scoping
used 2.67 combined). Near-field ~unchanged, far-field lethal count cut ~3× —
the right direction and magnitude for `challenges/drag-gap-1944/`, but see
limitation L3.

## 5. Why no Mach dependence (recorded, so it is not re-opened)

> **WITHDRAWN 2026-08-03 — this section's reasoning is void (C11). Do not cite
> it.** Every numeric claim below is computed from the superseded
> `figure-3-digitized.md` curve and from a velocity set that was ~44%
> wrong-column. On the corrected inputs, with one free scale each, the Fig-3
> $C_D(M)$ law **beats** the best-fit constant on both columns and in both
> bands — casualties M > 0.7: 0.052 (5.3%) vs 0.069 (7.1%); perforation: 0.036
> vs 0.045. Even with *no* fitted parameter it ties the fitted constant. The
> section's conclusion — do not implement a Mach-dependent law — survives, but
> the whole of its stated reason does not. The surviving reason is
> architectural cost at an immaterial accuracy difference; it is published as
> limitation **15** in `_limitations.qmd` and derived in `rebaseline-verdict.md`
> (C11, C12). The section is kept unedited below as the record of what was
> argued, not as a live claim.

Rejected in scoping §4 Option 3 on evidence, not convenience: the digitized
Fig-3 $C_D(M)$ curve integrated along each trajectory scores RMS 0.259 / 0.072
against the best *constant*'s 0.250 / 0.047 — it does not beat a constant on
this data, which is the source's own advice ("take the drag coefficient as
constant at its"). The structural cost
would be large: λ enters `min_lethal_mass`'s bisection and both field builders
in closed form, so a Mach-dependent $C_D$ replaces an algebraic λ with a
per-fragment ODE integration. Negative accuracy return for an architectural
change → **do not implement**.

## 6. Specification for the implementation pass

1. `DragParams`: `C_D: float = 1.28`, `C_shape: float = 2.0890`, with the
     docstring/comment naming (4), *k* = 2.60 g/cm³ and the source quotes
     "value of 660 grains/in.3 (2.60 g/cm3) has been recommended" /
     "supersonic value of 1.28."
     Do **not** leave `C_shape` documented as a "presented-area shape factor"
     with no provenance — that framing is what allowed 0.90 to persist.
1. Add a module-level helper `c_shape_from_ballistic_density(k, rho_steel)`
     returning $(\rho_{steel}/k)^{2/3}$, and set the default from it with
     `_K_BALLISTIC = 2600.0`, `_RHO_STEEL_REF = 7850.0`. Reason: (4) shows
     `C_shape` is meaningless without the $\rho_{steel}$ it is normalised to.
     Every shell in `arty.shells` is currently 7850, so the stored default is
     correct today; the helper makes the coupling explicit and re-derivable if a
     shell with a different $\rho_{steel}$ is ever added.
1. `retardation_coeff` itself is unchanged — the law (3) is already right.
1. Regression expectations: any test pinning fragment velocity, `min_lethal_mass`,
     lethal counts, R50 or *B(r)* will move (V3). Far-field lethal counts drop up
     to ~3×; near-field (s ≲ 5 m) moves < 5%. R50 shrinks. Expect golden-value
     updates, not logic changes.

## 7. Limitations (deliverables of this pass, per scoping §5)

**L1 — Tolch's absolute perforating count still over-predicts ~2.5–3.6×, and
this is not attributed to drag.** At the adopted constant, reproducing Tolch's
observed 15 ft → 120 ft perforation-density ratio (0.557) requires
$E_{thr}$ ≈ 4.6–8.6 J and yields 2.5–3.6× Tolch's measured ~700–780
perforations per shell (`scoping.md` §3d, re-run 2026-08-16). Tolch's own best
absolute agreement is near combined ≈ 1.2.

> **Re-run note (2026-08-16).** This limitation previously read "~2.8–4.1×",
> $E_{thr}$ 3–6 J. The check script (`checks/tolch-count-post-shape-closure.py`)
> calls `mott_params` with no `f_breakup` override, so its output silently
> moved a second time when the count-gap-1938 C2 pass (commit `74abdd7`,
> 2026-08-10) changed that default from the legacy terminal-velocity form to
> `f = breakup_velocity_fraction()`; nobody re-ran the script afterward until
> this restatement (`scoping.md` §3d has the full history). Direction and
> conclusion are unchanged; the numbers above are current as of 2026-08-16.
>
> **This L1 is the same quantity as `_limitations.qmd` L1** (Tolch's absolute
> perforating count), tracked independently in this update folder because it
> feeds a different question (does it veto raising drag?) than the main
> model's L1 (does the count chain need fixing?). `_limitations.qmd` L1 is now
> **closed** (2026-08-15): count-gap-1938's C1–C5 sub-candidates are all
> discharged and the count arm's standing verdict is a genuine FAIL at
> 2.25×/2.51× (plug-shear) and 1.8–2.1× (threshold-free) —
> `challenges/count-gap-1938/count-chain.md` §3. That closure is on the
> *current* drag constant (2.67); it does not change this L1's own
> conclusion, which is about the *veto direction* on drag, not the count
> chain's residual size. The prior deferrable-finding marker here (pointing at a
> since-superseded "met-or-marginal" reading of count-chain.md) is resolved by
> this cross-reference and removed.

This disagreement is recorded, not resolved, and the Ordnance anchor is
followed instead, for four reasons: (i) Tolch is a *compound* test — drag ×
Mott spectrum × a one-parameter fitted threshold × a perforate/not model — so
its residual is not attributable to drag, whereas V2 tests retardation alone;
(ii) a drag-orthogonal ~1.8–2.4× count bias was already recorded pre-closure,
and a fixed ~3× bias in the count chain leaves Tolch nearly flat over
1.7–2.67; (iii) ~700–780 is a count above Tolch's *hole-detection* threshold,
so the model is biased high at every drag value by an unquantified amount;
(iv) Tolch's preferred ≈ 1.2 lies below the geometric sphere floor of 1.31
(§3) and is not an available option at all. **Do not re-litigate this by
re-fitting drag**; the discriminating test would be an independent (THOR-type)
perforation model replacing the fitted $E_{thr}$.

**L2 — Long-range / arrival-Mach < 0.7 velocities remain unclosed by any
admissible drag law, and gravity is not the explanation.** At 75mm 400 ft and
155mm 300/400/600 ft the *required* combined constant falls to 1.76–2.07
(implied $C_D$ 0.84–0.99, below Fig-3's subsonic plateau of 1.08), and even the
full Fig-3 integration under-predicts velocity by up to 2.4× (155mm 600 ft:
49.6 vs 116.7 m/s). Free-fall terminal velocity $(gL)^{1/2}$ at these points is
20–23 m/s against observed 117–154 m/s, so the DoD gravity perturbation
("considering the effects of both drag and gravity") cannot account for it — gravity cannot hold a fragment up at
5–7× its terminal velocity. These arrivals are already below the casualty
threshold, so this is outside the fidelity bar. Leading untested candidate: the
source's tabulated m(r) at long range is set by *its own* lethality criterion
and may not be a clean ballistic observable.

**L3 — WITHDRAWN 2026-08-03 (C15).** The 7–34× *B(r)* over-prediction this
limitation is written against is **void**: it was the model's 58 ft-lb casualty
criterion compared against the mild-steel-perforation column
(`challenges/drag-gap-1944/b-vs-range-rebaseline.md`). Against the genuine
casualties columns Family B passes 8/10, 9/11 and 11/11, and the residual
*inverts* sign with range — so there is no growing-with-range gap left for this
limitation to decline to close. The ~10% headroom figure survives but its
justification does not: `C_shape` has no geometric ceiling (a sliver has
arbitrarily small *k*); the bound is empirical, from DoD's lowest tabulated
*k* = 2.33 g/cm³, which gives 7.6% above 2.674. Kept below as written.

**L3 (as published — void) — This change does not close `challenges/drag-gap-1944/`.** It delivers a
~3× far-field reduction against a 7–34× *B(r)* over-prediction that grows with
range. The residual must be attributed elsewhere (count chain, spray/belt
geometry, or the *B(r)* reduction itself), not to further drag increases —
the geometric envelope (§3) leaves at most another ~10% of headroom above 2.67
before the fragment must be denser than a solid steel cube.

## 8. Assumptions

- Geometric similarity across the fragment spectrum: a single *k* for all
  masses from one shell. This is the source's own assumption ("similar, the
  mass m and presented area A are related by") and is
  what makes λ ∝ m^{−1/3}.
- One global *k* = 2.60 g/cm³ for all calibers. The source notes "the value of
  k differs from one weapon to" another and the per-point required constants
  do show caliber structure; per-caliber *k* is deferred (scoping §6).
- Constant $\rho_{air}$ = 1.225 kg/m³ — no altitude or burst-height variation.
- Gravity neglected; trajectories treated as straight (source: "If the force of
  gravity is neglected, however, the equation").
  Justified for the lethal band by L2's terminal-velocity comparison.
- $C_D$ constant at the supersonic plateau across the whole Mach range
  ("take the drag coefficient as constant at its" / "supersonic value of
  1.28."), validated numerically in §5.
