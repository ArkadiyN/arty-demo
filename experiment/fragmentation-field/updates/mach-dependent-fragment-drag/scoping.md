# Scoping — fragment aerodynamic drag (`retardation_coeff`)

> ## ⚠ PARTIALLY RETIRED — 2026-08-03
>
> **Withdrawn and not to be cited:** §1 (the problem statement — its 7–34×
> *B(r)* motive is void, C1), §3a-2 and §4 Option 3's *stated reason* for
> rejecting a Mach-dependent law (C11), and §3d's use of the mixed-column
> velocity set. The Headline paragraph immediately below carries both defects:
> "Mach dependence … buys essentially nothing" is **false on the corrected
> data**, where it buys ~20–25% of RMS at equal parameter cost.
>
> **Still live:** §2 (the DoD-1975 literature audit), the geometric-envelope
> argument, and §5's recommendation to adopt the ballistic-density anchor —
> which is what shipped. The Headline's *other* claim, that the real defect was
> a constant outside the physically admissible envelope, survives every shock
> and is now the load-bearing leg of the whole update.
>
> The decision not to model $C_D(M)$ stands on architectural cost, not
> accuracy; it is published as limitation **15** in `_limitations.qmd`. See
> `derivation.md`'s banner for the full section-by-section split and
> `rebaseline-verdict.md` for the 15-claim register.

**Aspect.** The fragment retardation law in `src/arty/fragmentation.py`:
`DragParams` (`C_D`, `C_shape`) and `retardation_coeff`, which returns the
exponential decay rate λ in `v(s) = V0 · exp(−λ s)`.

**Headline.** The aspect is misnamed. The evidence says the defect is **not**
missing Mach dependence — it is that the current constant sits **outside the
physically admissible envelope** for a steel fragment. Mach dependence, when
actually integrated along the trajectory, buys essentially nothing. The
recommendation is a **one-line constant change with a literature anchor**, plus
an explicit limitation entry; the Mach-dependent option is recommended
**rejected**, not deferred.

## 1. Problem statement

`retardation_coeff` implements

$$\lambda(m) = \frac{\rho_{air}\,C_D\,C_{shape}}{2\,\rho_{steel}^{2/3}}\,m^{-1/3}
\quad (1)$$

with defaults `C_D = 0.65`, `C_shape = 0.90` → combined **0.585**.
`challenges/drag-gap-1944/` established that Family B over-predicts casualty
density *B(r)* by 7–34×, growing with range; that the cause localises to drag
(#4); and that a larger constant in 1.2–1.7 "closes it nowhere uniformly" (#5).
That thread's standing conclusion was that a *velocity-dependent* law was the
surviving candidate. This pass tests that conclusion directly against the
digitized DoD-1975 Figure 3 curve, and re-tests the Tolch objection (#6) that
was used to veto raising the constant — which was computed with the
now-superseded Mott closure.

## 2. Literature audit — DoD (1975), *Fragment and Debris Hazards*

`doc-reference/fragmentation/dod-1975-fragment-debris-hazards/10-F-0806_Fragment_and_Debris_Hazards.md`,
"Ballistic Properties" (lines 299–373) and `figure-3-digitized.md`.

| Item | Source | Value |
| --- | --- | --- |
| Mass–area law $m = kA^{3/2}$, $k$ = ballistic density | lines 315–318 | — |
| $k$, forged steel projectiles & frag bombs (**recommended**) | line 321 | 660 gr/in³ = **2.60 g/cm³** |
| $k$, demolition bombs | line 322 | 590 gr/in³ = 2.33 g/cm³ |
| $k$, steel **cubes** / **spheres** (geometric limits) | lines 325–327 | 1080 / 1490 gr/in³ = **4.27 / 5.89 g/cm³** |
| $C_D(M)$ curve; "useful approximation … constant at its supersonic value" | lines 334–339, Fig. 3 | subsonic 1.08–1.10, transonic peak **1.40**, supersonic **1.28** |
| Exponential solution, gravity neglected: $v = V\exp(-R/L)$, $L = 2(k^2m)^{1/3}/C_D\rho$ | lines 342–350 | same form as (1) |
| $L_1$ (unit-mass 1/e distance) at $k$=2.6, $C_D$=1.28 | line 358 | **247 m/kg^{1/3}** |
| Gravity handled as a perturbation; impact result governed by $(gL)^{1/2}/V$ | lines 360–373 | — |

**Mapping to arty.** Equating (1) with the source's $L$ gives the exact
identity

$$C_{shape} = \left(\frac{\rho_{steel}}{k}\right)^{2/3}
\quad (2)$$

so arty's `C_shape` is *not* a free shape fudge — it is a restatement of the
ballistic density. This makes the DoD numbers directly usable and, more
importantly, **bounds the coefficient**:

| Fragment geometry | $k$ [g/cm³] | $C_{shape}$ | combined at $C_D$ = 1.08 / 1.28 / 1.40 |
| --- | --- | --- | --- |
| steel sphere (densest possible) | 5.89 | 1.211 | 1.31 / 1.55 / 1.70 |
| steel cube | 4.27 | 1.500 | 1.62 / 1.92 / 2.10 |
| **forged steel projectile (DoD recommended)** | **2.60** | **2.084** | **2.25 / 2.67 / 2.92** |
| **arty current (0.585)** | **19.7 – 29.1** | 0.90 | — |

The current 0.585 implies a ballistic density of 20–29 g/cm³ — **2.5–3.7× the
density of solid steel**, i.e. a fragment with less presented area than a
sphere of the same mass. It is not a defensible calibration choice; it is
geometrically impossible. `L1` = 1102 m/kg^{1/3} against the source's 247.

**Admissible envelope: combined ∈ [1.31, 2.92], nominal 2.67.**

## 3. Evidence

Scripts (runnable standalone, `uv run python <path>`) in
`experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/`.

### 3a. Velocity decay vs. 1944 Ordnance — `required-retardation-vs-mach.py`

25 (m, r, v, V0) points across 75mm M48 / 105mm M1 / 155mm M107. Metric is
RMS of $\ln(v_{model}/v_{source})$; the "arrival Mach > 0.7" subset (n = 20) is
the lethal-relevant band (below it, fragments are already sub-lethal).

| Law | RMS, all 25 | RMS, M > 0.7 (n=20) |
| --- | --- | --- |
| current constant 0.585 | 0.864 | 0.710 |
| constant 1.2 | 0.570 | — |
| constant 1.7 | 0.358 | — |
| **DoD constant 1.28 × 2.084 = 2.67** | **0.349** | **0.092** |
| numeric best-fit constant | 0.250 (at 2.20) | 0.047 (at 2.94) |
| **digitized Fig-3 $C_D(M)$ integrated, k = 2.60** | 0.259 | 0.072 |

Two conclusions, both load-bearing:

1. **The DoD constant is the fix.** Over the lethal-relevant band it cuts the
     typical velocity error from ~2.0× ($e^{0.710}$) to **10%** ($e^{0.092}$).
1. **Mach dependence buys nothing.** The full Fig-3 curve, numerically
     integrated along each trajectory, does not beat the best *constant* —
     0.259 vs 0.250 over all points, 0.072 vs 0.047 over M > 0.7. This is the
     source's own advice (line 338: "a useful approximation for many
     applications is to take the drag coefficient as constant at its supersonic
     value of 1.28") confirmed numerically on this data. The challenge README's
     surviving hypothesis — a velocity-dependent law — is **not supported**.

Corroboration: the two numeric best-fit constants, inverted through (2) at
$C_D$ = 1.28, imply $k$ = 3.48 and 2.26 g/cm³ — bracketing the DoD recommended
2.60 g/cm³ from an entirely independent dataset.

### 3b. The unclosed long-range residual — `long-range-residual-diagnosis.py`

Nothing closes the low-arrival-Mach tail (75mm 400 ft; 155mm 300/400/600 ft),
where the required constant falls to 1.76–2.07 (implied $C_D$ 0.84–0.99, below
the Fig-3 subsonic plateau of 1.08) and the Fig-3 integration under-predicts
velocity by up to 2.4× (155mm 600 ft: 49.6 vs 116.7 m/s).

**It is not gravity.** Free-fall terminal velocity $(gL)^{1/2}$ at these points
is 20–23 m/s against observed arrival velocities of 117–154 m/s — gravity
cannot hold a fragment *up* at 5–7× its terminal velocity. The DoD
gravity-perturbation treatment (lines 360–373) would therefore change nothing
here. Left as an **open question** (§6), not a blocker: these points are
already below the casualty threshold.

### 3c. Demo-visible impact — `drag-update-demo-impact.py`

155mm M107, V0 = 1000 m/s, E_leth = 79 J, post-shape-closure Mott parameters
(μ = 5.07 g, N₀ = 3423):

| s [m] | m_min old [g] | N_leth old | m_min new [g] | N_leth new | ΔN |
| --- | --- | --- | --- | --- | --- |
| 5 | 0.185 | 2827 | 0.294 | 2690 | −5% |
| 20 | 0.276 | 2711 | 0.886 | 2254 | −17% |
| 50 | 0.497 | 2503 | 2.890 | 1609 | −36% |
| 120 | 1.215 | 2098 | 12.050 | 733 | −65% |

Near-field essentially unchanged, far-field lethal count cut by up to 3×. The
change is visible and in the right direction for `challenges/drag-gap-1944/`
(over-prediction growing with range) — but a ~3× far-field effect against a
7–34× *B(r)* gap means **this aspect does not close that challenge on its own**
and must not be scoped as if it does.

### 3d. Tolch (1938) absolute count — `tolch-count-post-shape-closure.py`

Re-run of the objection in `challenges/drag-gap-1944/tolch-1938-panel-distance.md`
Result 2, with post-shape-closure Mott parameters. Method: $E_{thr}$ is the one
free parameter, fitted per drag constant so the model reproduces Tolch's
observed Panel A (15 ft) → Panel D (120 ft) perforation-density ratio 0.557;
the absolute count at 15 ft is then a prediction against Tolch's measured
~700–800 perforations/shell. 75mm M48, three candidate V₀.

| combined $C_D C_{shape}$ | fitted $E_{thr}$ [J] | $m_{thr}$(15 ft) [g] | N/observed |
| --- | --- | --- | --- |
| **0.585 (current)** | **6500 – 12100** | **14.9 – 38.0** | **0.0 (4–31 counts)** |
| 1.20 | 140 – 245 | 0.39 – 0.90 | 1.7 – 2.9 |
| 1.70 | 24 – 42 | 0.09 – 0.19 | 3.0 – 4.5 |
| 2.20 | 5.9 – 10.8 | 0.03 – 0.07 | 3.6 – 5.3 |
| **2.67 (DoD)** | **1.9 – 3.6** | **0.018 – 0.035** | **3.9 – 5.6** |

**This overturns the challenge README's line #6.** With the superseded Mott
closure, current drag over-counted by 1.8–2.4× and raising drag made it worse,
so "the absolute count rules *out* raising drag". Post-shape-closure the whole
family has shifted: the current constant now fails Tolch **catastrophically and
in the physically impossible direction** — it needs a 6.5–12 kJ threshold to
perforate 1″ spruce (≈4× a rifle bullet's muzzle energy) and predicts 4–31
perforations against ~700–800. Tolch is now a **veto on the status quo**, not on
raising drag. `challenges/drag-gap-1944/README.md` row #6 and its "Where it
stands" bullets are stale and should be corrected.

**But Tolch does not endorse 2.67 either, and this must not be papered over.**
Its best absolute agreement is at combined ≈ 1.2 (1.7–2.9×), degrading
monotonically to 3.9–5.6× at 2.67; and the implied $E_{thr}$ at 2.67 is 2–4 J
(a ~4–14 mg, ~1 mm fragment perforating 1″ spruce), which the original Tolch
analysis argued is physically impossible — Tolch's smallest recorded
perforations have cross-sections ≥ 0.02 in² ≈ 12.9 mm². So Tolch pulls toward
~1.2–1.7 while the Ordnance velocity data and the geometric envelope both pull
toward 2.2–2.9. That is a genuine factor-~2 disagreement.

**Weighing them.** Four reasons to follow the Ordnance data and treat Tolch as
non-discriminating rather than contradicting:

1. **Test cleanliness.** The Ordnance check tests the retardation law *alone*,
     against the source's own tabulated (m, r, v) — no Mott spectrum, no
     threshold, no counting. Tolch's count is a compound test that multiplies
     drag by the Mott closure, a one-parameter threshold fit, and a
     perforate/not model; its residual is not attributable to drag.
1. **A known, drag-orthogonal count bias.** The pre-closure analysis already
     recorded a ~1.8–2.4× count over-prediction "not a drag effect". A fixed
     ~3× bias in the count chain absorbs most of the 2.67 residual and leaves
     Tolch nearly flat over 1.7–2.67 — while nothing absorbs a 20–200×
     shortfall at 0.585.
1. **An observational cutoff on the observed side.** ~700–800 is a count above
     Tolch's hole-detection threshold, not above a physical one. The model
     counts fragments Tolch could not have recorded, so it is biased high at
     *every* drag value by an unquantified amount.
1. **Admissibility.** Tolch's preferred 1.2 lies *below* the steel-sphere floor
     of 1.31 (§2) — it is not an available option regardless.

## 4. Options considered, ranked

| # | Option | Verdict |
| --- | --- | --- |
| **1** | **Adopt the DoD-1975 anchor: `C_D` = 1.28, `C_shape` = $(\rho_{steel}/k)^{2/3}$ with $k$ = 2.60 g/cm³ → 2.084 (combined 2.67).** One-line parameter change; closed-form λ preserved; both constants individually citable; RMS(M>0.7) 0.710 → 0.092. | **Recommended** |
| 2 | Numeric best-fit constant (2.20 all-points / 2.94 on M>0.7). RMS marginally better (0.047 vs 0.092), but it is a fit with no citation, and the improvement is inside the ±0.02/±0.1 read uncertainty of the digitized curve and the transonic $C_D$ spread (2.25–2.92). Loses the anchor to buy noise. | Rejected |
| 3 | Mach-dependent $C_D(M)$ from Fig-3, integrated along the trajectory. **Does not beat a constant** (§3a) while replacing a closed-form exponential with a per-fragment ODE integration — λ is consumed in closed form throughout (`min_lethal_mass` bisection, both field builders), so this is an architectural change, not a parameter change, for a *negative* accuracy return. | **Rejected — do not derive** |
| 4 | Keep 0.585, treat the gap as a limitation. Fails the Ordnance check (2× velocity error in the lethal band), fails Tolch by 20–200× with an impossible 12 kJ threshold, and implies a fragment 3× denser than steel. | Rejected |
| 5 | Add a gravity correction (DoD perturbation, lines 360–373) to close the long-range tail. §3b shows the tail is 5–7× above terminal velocity — gravity is not the mechanism. | Rejected |

## 5. Recommendation

**Carry Option 1 into a derivation pass**, scoped tightly:

- Change `DragParams` defaults to `C_D = 1.28`, `C_shape = 2.084`, and document
    (2) — `C_shape` is the ballistic-density restatement $(\rho_{steel}/k)^{2/3}$
    at $k$ = 2.60 g/cm³ — in the derivation, so the parameter is no longer read
    as a free fudge factor. Cite lines 321, 339, 350, 358.
- Validation checks for the derivation pass: (i) $L_1$ = 247 m/kg^{1/3} at
    $\rho_{air}$ = 1.225 (identity (2) reproduces 242, within the source's own
    rounding); (ii) RMS $\ln(v_{model}/v_{source})$ ≤ 0.10 on the 25-point
    Ordnance set restricted to arrival Mach > 0.7; (iii) the §3c 155mm
    m_min/N_leth table reproduces.
- Do **not** implement a Mach-dependent or trajectory-integrated drag law.

**Two limitation entries are part of the deliverable, not deferrals:**

1. Tolch's absolute perforating count still over-predicts by ~4–6× at the
     adopted constant; the residual is attributed to the Mott count chain and
     Tolch's hole-detection cutoff, not to drag (§3d). Record with the
     weighing, so the next reader does not re-litigate it.
1. Long-range / arrival-Mach < 0.7 velocities remain unclosed by any admissible
     drag law and are not explained by gravity (§3b).

**Also required (not a physics pass):** `challenges/drag-gap-1944/README.md` is
now factually stale — row #6's "the absolute count rules out raising drag" and
the "velocity/range-dependent retardation law is the surviving candidate"
bullet are both contradicted here.

## 6. Open questions (deliberately not chased this pass)

- What sets the long-range residual? Candidate not tested: the source's
    tabulated m(r) at long range is fixed by *its own* lethality criterion, so
    the far points may not be a clean ballistic observable at all.
- Does the ~3–6× Tolch count over-prediction persist under an independent
    perforation model (THOR-type) rather than a fitted single $E_{thr}$? That
    would convert Tolch from non-discriminating to a real second anchor.
- Is a per-caliber $k$ warranted? DoD notes $k$ "differs from one weapon to
    another" (line 319); the per-point required constants do show caliber
    structure. Out of scope — one global anchor first.

## Fidelity target

This aspect drives the lethal-fragment count vs. range in the 155mm demo (and
*B(r)* in the drag-gap challenge). Tolerable error: **±10% on arrival velocity
for arrival Mach > 0.7**, which is what the adopted constant achieves; the
resulting lethal-count error is the bar @model-reviewer should judge
materiality against. Sub-Mach-0.7 arrivals and Tolch's absolute count are
explicitly outside the bar.
