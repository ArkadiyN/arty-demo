# Derivation — `κ_x` at the shell's own ruled-line regime, and the re-solved triple `(κ_x, k, c)`

**Pass:** derivation (Workflow B step 3), 2026-08-18. Aspect: the first two
moments of Mott 1947's ruled-line breadth distribution (`κ_x = ⟨x⟩/x₀`,
`k = ⟨x²⟩/⟨x⟩²`) and the aspect covariance `c` weighted by that same
distribution, all evaluated at the `l/x₀` the shipped shells actually occupy.

**Closes** the blocking finding raised in
[`../breadth-variance-factor-k/derivation.md`](../breadth-variance-factor-k/derivation.md)
§5.3: shipped `κ_x = 1.5` is Mott's `l/x₀ = 20` demonstration value, while real
shells sit near `l/x₀ ≈ 95`.

Scoping (approved, Option 1):
[`scoping.md`](scoping.md). Nothing is implemented in `src/arty/` in this pass —
that is the next pass (scoping action E).

---

## 1. Governing relations (nothing new is postulated)

Mott 1947 ("A theory of the fragmentation of shells and bombs", §"the ruled
line") models circumferential fracture as nucleation events appearing on a line
of length `l` (the break-up circumference) at a rate that grows with the
accumulated strain, each event shielding a neighbourhood of order `x₀`. The
*only* control parameter of the resulting breadth distribution is the
dimensionless line length

$$\Lambda \equiv \frac{l}{x_0} = \frac{2\pi r_{bu}}{x_0}. \qquad (1)$$

Shipped `x₀` (Gold 2017 eq. (2); Mott 1947 after eq. (5)), as coded in
`arty.fragmentation.mott_params`:

$$x_0 = \sqrt{\frac{2\sigma_f}{\rho\,\gamma'}}\;\frac{r_{bu}}{v_{bu}}
\qquad\Longrightarrow\qquad
\Lambda = 2\pi\,v_{bu}\Big/\sqrt{\frac{2\sigma_f}{\rho\gamma'}}. \qquad (2)$$

| symbol | meaning | unit |
| ------ | ------- | ---- |
| `l` | ruled-line length = break-up circumference | m |
| `x₀` | fracture-spacing scale (Mott) | m |
| `r_bu`, `v_bu` | radius and velocity at case break-up | m, m s⁻¹ |
| `σ_f`, `ρ`, `γ'` | steel fracture stress, density, Mott strain-rate constant | Pa, kg m⁻³, – |
| `Λ = l/x₀` | ruled-line regime parameter | – |
| `κ_x = ⟨x⟩/x₀` | mean breadth in fracture spacings | – |
| `k = ⟨x²⟩/⟨x⟩²` | breadth second-moment (variance) factor | – |
| `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩)` | normalised aspect–breadth covariance | – |

**`r_bu` cancels identically in (2)** — `x₀ ∝ r_bu`, which is Mott's own finding
(2), p. 305, "`x₀` is proportional to `r`". So `Λ` is set by break-up velocity
and steel constants alone. This is a *derivation*, not an approximation, and it
is the reason a single caliber-independent `κ_x` is admissible (scoping §2,
option 2 rejected).

The coupling into the shipped model is, from `mott_params`:

$$\alpha = A_{\rm eff}\,\kappa_x^2\,\frac{t_{bu}}{x_0},\quad
A_{\rm eff}=1.6\,c\,k,\quad
\gamma=\alpha^{-2/3}\gamma',\quad
\mu \propto \gamma^{-3/2}\;\Longrightarrow\;
\boxed{\mu \propto A_{\rm eff}\,\kappa_x^{2}},\quad N_0=\frac{M}{2\mu}. \qquad (3)$$

`κ_x`, `k` and `c` are the 1st moment, the normalised 2nd moment, and a
2nd-moment covariance **of one and the same population**. Changing `Λ` therefore
re-solves all three together; solving one alone re-creates the mixed-population
error that `breadth-variance-factor-k/review.md` finding B2 was raised to fix.

## 2. Where the shipped fleet sits — `Λ` per shell

`checks/ell-over-x0-per-shell.py` reproduces `x₀` line-for-line from the shipped
registry and forms (2). Result (`f = 0.943`, the shipped break-up velocity
fraction):

| shell | `r_bu` [mm] | `v_bu` [m/s] | `√(2σ_f/ργ')` [m/s] | `x₀` [mm] | **`Λ`** |
| ----- | ----------- | ------------ | ------------------- | --------- | ------- |
| 155 mm M107 | 113.90 | 975.6 | 61.15 | 7.140 | **100.2** |
| 105 mm M1 | 77.82 | 937.4 | 61.15 | 5.077 | **96.3** |
| 75 mm M48 | 56.39 | 814.9 | 61.15 | 4.232 | **83.7** |
| 60 mm M49A2 | 41.88 | 988.9 | 65.85 | 2.789 | **94.4** |

The fleet occupies `Λ = 84–100` — a *narrower and higher* band than the
finding's verbal "50–200", and 4–5× Mott's demonstration `Λ = 20`. The residual
1.2× spread is driven by `v_bu` (i.e. C/M) and by the 60 mm's different `γ'`;
`Λ` computed the long way (`2πr_bu/x₀`) and the short way (`2πv_bu/√(2σ_f/ργ')`)
agree to the printed digit, confirming the cancellation in (2) numerically.

**Adopted regime: `Λ = 95`** — a round value inside the 84–100 band and within
6 % of every shell. (Not a weighted centre: `Λ ∝ v_bu` by eq. (2), so weighting
`Λ` by `v_bu` is not a defined operation on this set; the unweighted fleet mean
is 93.7, and §3's 0.032-per-e-fold slope makes that 0.05 % on `κ_x`.) §3 shows
the whole fleet band costs 0.3 % on `κ_x`.

**Mott's own numerical example sits in this band too**, not at 20: p. 306, 3 in.
bomb, `r ≈ 2 in.` at break-up, `x₀ = 1.6/√γ` in. `= 0.16 in.` at `γ ≈ 100`, so
`Λ = 2π(2)/0.16 ≈ 79`. He nonetheless applied the `Λ = 20` statistic (`1.5x₀`)
to it, justified by one sentence — "the distribution would not be sensibly
different for larger values" (p. 305, above figure 4). §3 measures that sentence
and finds it wrong by 4 %.

## 3. The moments at that regime (Action A)

`checks/kx-at-fleet-regime.py` runs the committed ruled-line Monte Carlo
([`../breadth-variance-factor-k/checks/mott-ruled-line-mc.py`](../breadth-variance-factor-k/checks/mott-ruled-line-mc.py),
unmodified) at ~40 000 fragments per configuration and two seeds. `mott` is
Mott's deterministic increment `Δσ = 1/(fCe^{ασ})`; `poisson` is exact
inhomogeneous-Poisson thinning of the same eq. (4) rate law.

| scheme | `Λ` | seed | `n` | `κ_x` | `k` |
| ------ | --- | ---- | --- | ----- | --- |
| mott | 95 | A | 40019 | 1.6190 ± 0.0034 | 1.1714 ± 0.0011 |
| mott | 95 | B | 40147 | 1.6138 ± 0.0034 | 1.1733 ± 0.0012 |
| poisson | 95 | A | 38772 | 1.6711 ± 0.0037 | 1.1868 ± 0.0014 |
| poisson | 95 | B | 38962 | 1.6629 ± 0.0037 | 1.1907 ± 0.0014 |
| mott | 84 | A | 40062 | 1.6166 ± 0.0033 | 1.1698 ± 0.0011 |
| mott | 100 | A | 39975 | 1.6210 ± 0.0034 | 1.1738 ± 0.0011 |
| poisson | 84 | A | 38967 | 1.6620 ± 0.0037 | 1.1886 ± 0.0014 |
| poisson | 100 | A | 38945 | 1.6639 ± 0.0037 | 1.1916 ± 0.0013 |
| **mott** | **20** | A | 41643 | **1.5561 ± 0.0029** | 1.1426 ± 0.0010 |
| poisson | 20 | A | 39649 | 1.6343 ± 0.0035 | 1.1804 ± 0.0013 |

Three things this settles (all were open in scoping):

1. **The `Λ = 95` vs `100` non-monotonicity in scoping's Poisson row was MC
    noise.** At `n ≈ 40 000` both schemes are monotone in `Λ` and the seed-to-seed
    spread (0.005 on `κ_x`, 0.002–0.004 on `k`) matches the quoted standard
    errors. No systematic seed effect.
1. **Fleet spread is 0.27 % on `κ_x` (mott, 84 → 100) and 0.11 % (poisson)** —
    an order of magnitude below the ±3 % fidelity target. **One
    caliber-independent `κ_x` is confirmed**; scoping option 2 (per-shell) stays
    rejected on physics, not on effort.
1. **The implementation reproduces Mott's own configuration**: `κ_x(Λ=20) =
    1.5561` against his "the average length is about 1.5x₀" (p. 305, finding
    (1)) — unchanged from the committed 1.5604 at lower `n`, so the
    higher-statistics re-run has not moved it. This is a **regression check on
    `mott-ruled-line-mc.py`'s implementation of Mott's quadrature, not an
    empirical anchor and not a test between quadrature schemes** — see §3.1 for
    why it cannot serve as either.

### 3.1 Quadrature sub-decision — **I deviate from scoping's recommendation**, on attributability alone

Scoping §"Sub-decision" recommended exact Poisson as the central value. I retain
the `mott` step — but **not** because it reproduces Mott's `Λ = 20` statistic.
That comparison cannot decide the question and is voided here.

- **The `Λ = 20` row is a reproduction check of the MC's implementation of
    Mott's quadrature — not evidence about which quadrature is right.** Mott's
    "the average length is about `1.5x₀`" (p. 305, finding (1), immediately after
    "The calculations were made with `l/x₀ = 20`") is read off his figure 4: a
    histogram binned at `0.4x₀` and generated by *the deterministic procedure
    itself*. The criterion is an output of one of the two candidates, so that
    candidate cannot lose the comparison. It is also below the resolution at
    which it could discriminate — 1.556 (`mott`) and 1.634 (`poisson`) differ by
    0.078, one-fifth of a bin, and both round to 1.6 at the one significant
    figure Mott states. Calling `poisson` "9 % above what Mott reports" would
    treat a one-figure eyeball as a three-digit datum; on the same arithmetic
    `mott` is 3.7 % above it. **Explicitly non-empirical:** scoping §2 said this
    correctly — Mott's example is a *theoretical* worked example with no fragment
    measurement attached — and that qualification is restored here.
- **The sole ground the decision rests on is attributability.** Every shipped
    constant in this family (`κ_x = 1.5`, `k = 1.1375`, `c = 1.1254`) was solved
    on the `mott`-step population. This change moves the **regime** (`Λ` 20 → 95)
    against that shipped baseline; moving the **quadrature scheme** in the same
    change would confound the two, and a later disagreement with data could not
    be traced to either. One variable at a time is what makes the §5.1 delta
    interpretable at all. The same argument runs upstream: the `1.6` in
    `A_eff = 1.6ck`, and the `x₀` calibration it multiplies, are Gold 2017's
    reading of Mott's deterministic construction — so a scheme change is a wider
    change than it looks.

**Adopted: `mott` step, `κ_x = 1.62` — the *low edge* of a `[1.62, 1.67]` band,
not a central estimate.** Two things must be said plainly, because the
incentives run the other way:

- **Physically, Poisson is the faithful scheme.** Mott states a *rate law* — a
    probability per unit length per unit strain increment (his eq. 4) — and
    inhomogeneous-Poisson thinning samples exactly that. The deterministic
    increment `Δσ = 1/(fCe^{ασ})` places every nucleation at exactly the mean
    waiting interval, suppressing waiting-time fluctuation; it is a
    hand-computation quadrature *of* the stated law, not the law. The band is
    therefore one-sided in a known direction: if the scheme is revisited the
    expected move is **up**, to `κ_x = 1.67`, `k = 1.189`, `μ` +6.5 %. Every
    downstream number for that edge is tabulated in §5.2–5.3, so the reversal
    costs no re-run (assumption **X3**).
- **The retained scheme is also the one that moves everything least** — `μ`
    ×1.22 vs ×1.30, FM 6-40 geo-mean 0.909 vs 0.862 (§5.2), `count-gap-1938`
    1.89× vs 1.78× (§5.3). Nothing above is a claim that 1.62 *fits* better; on
    the one empirical anchor this change touches it fits slightly worse (§5.2),
    and both edges are tabulated so the choice can be reversed on evidence rather
    than re-argued.

**Supersedes K3 (partially).** `breadth-variance-factor-k` assumption **K3**
names `(κ_x, k) = (1.67, 1.20)` — the Poisson pair at high `Λ` — as "the
physically applicable configuration". This change **meets the regime half** of
that target (`Λ = 95` is now measured, not assumed) and **declines the
quadrature half**, on the attributability ground above and not on physics. K3 is
therefore superseded rather than satisfied, and the unmet residual is precisely
the +3.2 % / +6.5 % band edge carried in X3.

Note the schemes also disagree about *how much* `Λ` matters: `mott` moves +4.0 %
from 20 → 95, `poisson` only +2.2 % (an internal-to-scheme slope in each case,
so the voided anchor above does not enter). Both agree the move is real and
upward.

## 4. `c` re-solved on the new breadth marginal (Action B)

`checks/c-at-fleet-regime.py` re-runs the committed closure
[`../breadth-variance-factor-k/checks/c-on-ruled-line-population.py`](../breadth-variance-factor-k/checks/c-on-ruled-line-population.py)
**textually un-forked**, with only the substitutions scoping named. Table 3's
conditional aspect mix `A|group`, the `m = S·A·x²` cell reading, the `⟨m⟩ = 2μ`
mass-scale bisection and the `μ = c·k·μ₀` fixed point are all bit-identical.

### 4.1 A second-order coupling scoping did not name — and its size

`μ₀` enters the closure (it fixes the mass scale `S`, hence which breadth
interval each Table-3 mass group maps to), and `μ₀` itself carries `κ_x` through
`α = A κ_x² t_bu/x₀`. Sampling the marginal at `Λ = 95` while leaving `μ₀` at
`κ_x = 1.5` would be the **same one-population-two-regimes error B2 was raised
against, one level down**. The script therefore runs both couplings:

| shell | `c` (`μ₀` at `κ_x`=1.5) | `c` (`μ₀` at `κ_x`=1.62) | shift |
| ----- | ----------------------- | ------------------------ | ----- |
| 155 mm M107 | 1.1457 | **1.1524** | +0.6 % |
| 105 mm M1 | 1.0716 | **1.0789** | +0.7 % |
| 75 mm M48 | 1.0323 | **1.0408** | +0.8 % |
| 60 mm M49A2 | 1.0051 | **1.0093** | +0.4 % |

The coupling is real but **≤ 0.8 %**, i.e. it needs no iteration to a fixed
point in `κ_x` — one self-consistent evaluation suffices. The self-consistent
column is adopted.

### 4.2 Adopted `c`, and the method band

Breadth marginal at `Λ = 95`, Mott step, `n = 41 053`, `⟨ξ⟩ = 1.6199`,
`k_MC = 1.1711` — both consistent with §3's two-seed values.

| shell | `c` **percell (adopted)** | `c` marginal (band low) | shipped `c` | `k_pop` | `A_eff = 1.6ck` | shipped `A_eff` |
| ----- | ------------------------- | ----------------------- | ----------- | ------- | --------------- | --------------- |
| 155 mm M107 | **1.1524** | 1.0489 | 1.1254 | 1.1526 | **2.1592** | 2.0482 |
| 105 mm M1 | **1.0789** | 0.9786 | 1.0608 | 1.1605 | **2.0215** | 1.9307 |
| 75 mm M48 | **1.0408** | 0.9384 | 1.0247 | 1.1814 | **1.9502** | 1.8650 |
| 60 mm M49A2 | **1.0093** | 0.9581 | 1.0026 | 1.1729 | **1.8912** | 1.8247 |

Notes.

- **`c` moves only +0.7 to +1.6 %** from the shipped (`Λ = 20`) values, far less
    than `κ_x` does. The regime change acts almost entirely through `κ_x²`; `c`
    and `k` are near-invariant to it because they are *ratios* of moments and the
    breadth distribution's *shape* barely changes with `Λ` — only its mean does.
    This is a substantive result: it says the shipped `c` table was not badly
    wrong, only the scalar `κ_x` was.
- **Closure check passes.** `k_pop`, the realised second moment of the
    reweighted cell population, is 1.153–1.181 against `k_MC = 1.1711` — a ±1.5 %
    band around the marginal it is supposed to reproduce, so the Table-3 cell
    reading is not distorting the breadth population. (At the shipped `Λ = 20`
    the same check bracketed 1.1375 comparably.)
- `c ≥ 1` on every shell and every closure except the `marginal` low end, as a
    positive `A`–`x²` correlation requires. The caliber trend that the pre-fix
    table showed is still absent — confirming it was the coarse-mass-axis
    artefact identified in `breadth-variance-factor-k`, not physics.
- The `percell`/`marginal` spread (±5 % on `c`) is unchanged in width from the
    shipped pair and remains the dominant *method* uncertainty — larger than the
    ±1.5 % quadrature band and larger than the ±0.3 % fleet-regime band.

## 5. Downstream recomputation (Action C)

`checks/downstream-at-new-triple.py`. Since `μ ∝ 1.6·c·k·κ_x²` exactly (eq. 3),
each committed downstream harness — which is parameterised by a multiplier on
the uncorrected `A = 1.6` at the registry `κ_x = 1.5` — is driven with
`c_eff = c·k·(κ_x/1.5)²`. That reproduces the new `μ` **exactly**; the harnesses
then **re-solve** `N₀`, the survival exponential and `B(r)` from it. Nothing is
scaled (memory `gotcha_mott_count_not_f_squared`).

### 5.1 The move itself

| shell | `A_eff` shipped → new | `×` from `A_eff` | `×` from `κ_x²` | **`μ ×`** | **`N₀ ×`** |
| ----- | --------------------- | ---------------- | --------------- | --------- | ---------- |
| 155 mm M107 | 2.0482 → 2.1593 | 1.0542 | 1.1664 | **1.230** | 0.813 |
| 105 mm M1 | 1.9307 → 2.0216 | 1.0471 | 1.1664 | **1.221** | 0.819 |
| 75 mm M48 | 1.8650 → 1.9502 | 1.0457 | 1.1664 | **1.220** | 0.820 |
| 60 mm M49A2 | 1.8247 → 1.8912 | 1.0364 | 1.1664 | **1.209** | 0.827 |

`μ` rises 21–23 %, `N₀` falls 17–19 %, uniformly across the fleet — the
finding's "~21 %" estimate is confirmed, and **86 % of the move is `κ_x²`**,
5–6 % is the re-solved `(c, k)`. Fleet uniformity (1.209–1.230) is the practical
expression of the caliber-independence derived in §1.

### 5.2 155 mm `B(r)` against FM 6-40 Table 59 (11 range points)

| driver | `c_eff` | `A_eff` | geo-mean ratio | in 0.5–2× band |
| ------ | ------- | ------- | -------------- | -------------- |
| shipped (`κ_x`=1.50) | 1.2801 | 2.048 | **1.046** | 11/11 |
| **new (`κ_x`=1.62, percell)** | 1.5741 | 2.519 | **0.909** | 11/11 |
| new, marginal closure | 1.4328 | 2.292 | 0.970 | 11/11 |
| new, Poisson `κ_x`=1.67 band edge | 1.6981 | 2.717 | 0.862 | 11/11 |

The fit crosses from **+4.6 % to −9.1 %** — scoping predicted ≈ −7 %, and the
extra 2 % is the re-solved `(c, k)`. **Report honestly: on this anchor alone the
new triple fits slightly *worse*** (|log| 0.095 vs 0.045). Three things bound
how much that matters:

- It stays 11/11 inside the 0.5–2× acceptance band, and the per-point spread
    (0.66–1.01) is dominated by the outermost two points (300–600 ft), where the
    card's own resolution is 1 significant figure.
- **The change is a pure level shift, not a tilt.** The normalised shape row is
    identical to 3 decimal places across all four drivers, so `B(r)` constrains
    only the *product* `1.6ckκ_x²` and cannot discriminate *which* factor is
    wrong. It is therefore not evidence against the `κ_x` regime argument, which
    rests on Mott's own model.
- The `marginal` closure (0.970) is the best-fitting of the four. That is a
    ±5 % method choice already carried as assumption K5; `B(r)` mildly prefers
    it but cannot resolve it — do **not** re-open the closure choice on this
    evidence (that would be tuning `c` to the validation target, memory
    `gotcha_rebaseline_onto_validation_source`).

### 5.3 75 mm `count-gap-1938` arms (`m_thr` = 0.166 g held fixed)

| case | `c_eff` | `μ` [g] | `N₀` | `N(≥m_thr)` | /Tolch 700 | /Tolch 779 |
| ---- | ------- | ------- | ---- | ----------- | ---------- | ---------- |
| bare `A` = 1.6 | 1.0000 | 0.929 | 2681 | 1757 | 2.51 | 2.26 |
| shipped | 1.1656 | 1.083 | 2300 | 1555 | 2.22 | 2.00 |
| **new (percell)** | 1.4217 | 1.321 | 1886 | **1323** | **1.89** | **1.70** |
| new, marginal | 1.2818 | 1.191 | 2092 | 1440 | 2.06 | 1.85 |
| new, Poisson edge | 1.5337 | 1.425 | 1748 | 1243 | 1.78 | 1.60 |

**The published challenge verdict is stale against the "shipped" row above, and
this derivation is not its owner.** `challenges/count-gap-1938/rebaseline-verdict.md`
publishes "genuine FAIL at **2.28× (/779) / 2.54× (/700)**" *as the shipped-code
verdict* — that is the file's current top-line figure (fifth banner, 2026-08-16;
review Pass 3 D4 confirms it against `rebaseline-verdict.md:11`, `count-chain.md`
and `challenges/README.md:20`). It is a **pre-`k` chain**: the fifth banner already
carries the per-shell `c` half (`aspect_ratio = 1.6·c`) but not `k`. Live
`src/arty` (`κ_x = 1.5`, `k = 1.1375`, `c = 1.0247`, i.e. `c_eff = 1.1656`)
gives **2.22× / 2.00×**; the published pair predates the `k` half of the `(c, k)`
moment correction that `breadth-variance-factor-k` shipped. (An earlier revision
of this section cited 2.25×/2.51× and called it the bare `A` = 1.6 chain — that
was a superseded quote from the fourth banner, corrected here per D4.) Fixing that committed
surface is outside this change's scope, so it is marked rather than deferred
silently; the re-close in §6.4 must start from 2.22×/2.00×, and the residual the
remaining candidates (C3, C4) must close is ~12 % smaller than the challenge
currently states.

FINDING[blocking]: count-gap-1938 publishes 2.28x (/779) / 2.54x (/700) as the shipped-code verdict (its current top-line, fifth banner 2026-08-16), but live src/arty (kappa_x=1.5, k=1.1375, c=1.0247) gives 2.22x (/700) / 2.00x (/779); the published pair is a pre-k chain, c-corrected but not yet k-corrected (affects: experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md, experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md, experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks/aspect-ratio-moment-leverage.py; since: 2026-08-18)

**Against live shipped code the challenge improves from 2.22×/2.00× to
1.89×/1.70× and stays a genuine FAIL** — as scoping predicted (~1.8×/1.6×).
This change is not a candidate
closure for `count-gap-1938`; it removes ~15 % of a ~120 % over-count. The
remaining candidates (C3, C4) are unaffected by it in kind, but their required
leverage drops accordingly — the `count-gap-1938` thread should re-close against
the new triple once `src/arty/` ships it (open item §6.4).

## 6. Adopted values, assumptions, limitations

### 6.1 The adopted triple

| constant | shipped | **adopted** | basis |
| -------- | ------- | ----------- | ----- |
| `_MOTT_BREADTH_FACTOR` (`κ_x`) | 1.5 | **1.62** | §3, `Λ = 95`, Mott `Δτ` step, two seeds, `n ≈ 40 000` |
| `MOTT_BREADTH_VARIANCE_K` (`k`) | 1.1375 | **1.1711** | §3/§4.2, same population |
| `MOTT_ASPECT_MOMENT_C` 155 / 105 / 75 / 60 mm | 1.1254 / 1.0608 / 1.0247 / 1.0026 | **1.1524 / 1.0789 / 1.0408 / 1.0093** | §4.2, `percell` closure, `μ₀` self-consistent at `κ_x` = 1.62 |

**They ship as one set.** All three are moments of the ruled-line breadth
population at `Λ = 95`; replacing any one alone re-creates the mixed-population
error of finding B2. The `src/arty/` pass (next) must move all six numbers in a
single edit.

### 6.2 Assumptions (numbering continues the family's `A9.x`/`K.x`)

- **X1 (replaces A9.3).** `κ_x = 1.62` is the mean breadth of Mott 1947's ruled
    line at `Λ = 95`, the regime the shipped fleet occupies (§2), *not* at his
    `Λ = 20` demonstration configuration. Standing objection retained from A9.3:
    this is still a moment of a **1-D fracture model, not a measurement**. What
    changed is that it is now the model's own answer *for these shells*.
- **X2.** One caliber-independent `κ_x` (and `k`). Justified, not assumed:
    `r_bu` cancels in eq. (2), and the residual fleet spread is 0.27 % on `κ_x`
    (§3) against a ±3 % target.
- **X3.** Mott's deterministic `Δσ = 1/(fCe^{ασ})` quadrature is retained over
    exact Poisson thinning of the same rate law (§3.1) — on **attributability,
    not on physics**: the shipped constant family was solved on the `mott`-step
    population, and this change moves the regime against that baseline one
    variable at a time. **The physically faithful sampling of the rate law Mott
    states is Poisson**, so `κ_x = 1.62` is the **low edge of a `[1.62, 1.67]`
    band** with a known one-sided direction, not a central estimate. Poisson
    gives `κ_x = 1.67`, `k = 1.189`, i.e. **+6.5 % on `μ`**; its `B(r)`/count
    numbers are tabulated in §5.2–5.3 so a later reversal needs no re-run. This
    supersedes `breadth-variance-factor-k` **K3**'s `(1.67, 1.20)` target on the
    quadrature half only — the regime half is met (§3.1). Mott's reported
    `1.5x₀` at `Λ = 20` plays **no part** in this choice: it is his own
    procedure's output at one significant figure and cannot discriminate the two
    schemes (§3.1).
- **X4.** `μ₀` inside the `c` closure is evaluated at the new `κ_x`
    (self-consistently). Iterating to a full fixed point is unnecessary: the
    coupling is ≤ 0.8 % on `c` (§4.1).
- **K5 (unchanged, re-measured).** The `percell` vs `marginal` closure choice
    remains the widest method band, ±5 % on `c` (±5 % on `μ`). `percell` stays
    adopted because `m = S·A·x²` is a kinematic identity.
- **Inherited (O1, scoping).** `l` = break-up circumference — purely
    circumferential cracking, no axial crack family, ogive and base excluded.
    This is Mott's own construction ("to represent the circumference of the
    cylinder"). Bounded: halving the effective `l` costs ~2 % on `κ_x` (§3's
    log slope, 0.032 per e-fold).

### 6.3 `_limitations.qmd` entry (Action F — text for the presentation pass)

> **Breadth moments and the mass law come from different vintages of Mott.**
> The fragment mass scale `μ` now carries breadth moments (`κ_x`, `k`, `c`)
> measured on Mott's *1947* ruled-line fracture model at each shell's own
> regime `l/x₀ ≈ 95`, while the mass *distribution* it feeds,
> `N(≥m) = N₀e^{−√(m/μ)}`, still descends from the *1943* exponential
> (assumption K1). The two are consistent in spirit — 1947 is Mott's own
> refinement of 1943 — but the spectrum's shape parameter has not been
> re-derived on the 1947 population. Effect is unbounded in principle; the
> shipped evidence is that the 1947 moments move `μ` by ~+22 % and leave the
> 155 mm `B(r)` fit inside its acceptance band (−9 %) and the 75 mm count
> over-prediction at 1.7–1.9× (`challenges/count-gap-1938`).

### 6.4 Open items for later passes (not blockers on this derivation)

- **Action E (next pass, `src/arty/`).** Ship the triple; fix the collateral
    claims that assume `κ_x = 1.5` — the `fragmentation.py:150-160` comment
    block (its "`1.5·1.6/√100 = 0.24` exactly" closure against Mott's p. 306
    worked example is **invalidated**: at `κ_x = 1.62` the same arithmetic gives
    0.259 in., and §2 shows that example sits at `Λ ≈ 79` where 1.62 is the
    right coefficient — i.e. Mott's own 0.24 in. is what is wrong, by his own
    model. **The primary anchors are confirmed, not inferred** (review Pass 3,
    D3): `gurney-equations-fragmentation/rspa.1947.0042.md` carries verbatim
    "The calculations were made with `l/x_0 = 20`", finding (1)'s "the average
    length is about `1.5x_0`", and "Thus if `γ ∼ 100`, the average fragment
    length is about 0.24 in." — with §3 beginning immediately after, so **no
    fragment measurement is attached to the worked example**; the
    source-absence claim inherited from scoping stands); `challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`;
    the `MOTT_BREADTH_VARIANCE_K` comment's `Λ = 20` rationale; and assumptions
    A9.3 / K3. **Only then** delete the blocking marker in
    `../breadth-variance-factor-k/derivation.md`.
- **Re-close `count-gap-1938`** against the shipped triple (§5.3 gives the
    numbers; the verdict stays FAIL, the ratios move). **Start from 2.22×/2.00×,
    not from the 2.54× (/700) / 2.28× (/779) the challenge currently publishes**
    (its top-line fifth banner, 2026-08-16) — that pair is a pre-`k` chain,
    already `c`-corrected but not yet `k`-corrected, and carries a blocking
    finding marker in §5.3. Whether the challenge re-closes before or after the `src/arty/` pass
    is the human's call, not this derivation's.
- **O2 (scoping, still open).** Whether `x₀` should carry the raw `γ'` or the
    shape-corrected `γ = α^{-2/3}γ'` (Gold 2017 eq. (6)). It moves `Λ` by
    `α^{1/3}` — <2 % on `κ_x`, so it cannot change this change's outcome — but
    it would move `x₀` and hence `μ` **directly**, which is a separate aspect.
- **O3 (scoping, still open).** `v_bu` enters `Λ` linearly through the break-up
    fraction `f = 0.943`; a revision of `f` moves `κ_x` by <2 %.
- **Not attempted here:** re-deriving the mass *law* on the 1947 population
    (see §6.3), and any empirical fit of `κ_x` to measured fragment breadths
    (scoping option 5, a different aspect requiring an @librarian pass).

### 6.5 Fidelity target (carried from scoping §7)

Drives `μ`, `N₀`, hence every fragment count, the `B(r)` lethal-radius surface
and the `P(kill)` field. **Tolerable error on `κ_x`: ±3 % (±6 % on `μ`).** The
regime band (±0.3 %) sits well inside it. **The quadrature band (±3.2 %)
marginally exceeds it** — that is the quantitative reason §3.1's scheme choice
is not free: it consumes the whole `κ_x` budget on its own, which is why 1.62 is
recorded there as the low edge of `[1.62, 1.67]` rather than as a central value.
The `percell`/`marginal` closure band (±5 % on `c`) also exceeds it and is an
inherited, separately-tracked choice (K5). The shipped
`κ_x = 1.5` was 7.4 % low on this bar, which is why the finding is blocking.
