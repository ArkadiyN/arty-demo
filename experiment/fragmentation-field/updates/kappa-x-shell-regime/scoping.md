# Scoping — `κ_x` at the shell's own ruled-line regime (`l/x₀`), assumption A9.3

**Pass:** scoping (Workflow B step 2), 2026-08-17. Aspect: the **first moment of
Mott 1947's ruled-line breadth distribution**, `κ_x = x̄/x₀`, and the two
constants that are moments of the same population (`k`, `c`).

**Trigger — open blocking finding** (raised in
[`../breadth-variance-factor-k/derivation.md`](../breadth-variance-factor-k/derivation.md)
§5.3, re-tiered by that thread's `review.md` B1):

> shipped `κ_x = 1.5` (A9.3) is Mott 1947's `l/x₀ = 20` demonstration value;
> reproducing his procedure at the `l/x₀ = 50–200` regime real shells occupy
> gives 1.65, i.e. `μ` low by ~21 %.

Nothing is implemented in this pass.

---

## 1. What is coupled to what (do not move `κ_x` alone)

`arty.fragmentation.mott_params` uses `κ_x` in exactly one place:

```
alpha = A_eff · κ_x² · t_bu/x0 ;  gamma = alpha^(-2/3)·γ' ;  μ ∝ gamma^(-3/2) ⇒ μ ∝ A_eff·κ_x²
```

with `A_eff = 1.6·c(shell)·k` (`mott_aspect_ratio`). So `μ ∝ κ_x²` **exactly**,
and `N₀ = M/2μ` moves inversely.

`κ_x = ⟨x⟩/x₀` and `k = ⟨x²⟩/⟨x⟩²` are the first and second moments of **one**
distribution, and `c = ⟨Ax²⟩/(⟨A⟩⟨x²⟩)` is a normalised covariance **weighted by
that same distribution** (that thread's review finding B2). The shipped triple
`(κ_x, k, c) = (1.5, 1.1375, per-shell)` was deliberately solved on Mott's
`l/x₀ = 20` configuration *as a set*. **Moving the regime therefore re-solves
all three**, or it re-creates the mixed-population error B2 was raised to fix.
This is the single most important constraint on the change.

## 2. The regime parameter is caliber-independent — derived, not assumed

The brief asks whether `l/x₀` is properly one number or a per-shell one. It is
one number, and the reason is an exact cancellation, not a small spread.

Shipped `x₀` (Gold 2017 eq. (2) / Mott 1947 after eq. (5), `fragmentation.py`):

$$x_0 = \sqrt{\frac{2\sigma_f}{\rho\,\gamma'}}\;\frac{r_{bu}}{v_{bu}}
\qquad\Rightarrow\qquad
\frac{l}{x_0}=\frac{2\pi r_{bu}}{x_0}
= 2\pi\, v_{bu}\Big/\sqrt{\tfrac{2\sigma_f}{\rho\gamma'}} \quad (1)$$

**`r_bu` cancels identically.** The ruled line is the circumference, and `x₀` is
itself proportional to `r` (Mott's own finding (2), p. 305: "`x₀` is proportional
to `r`"). The regime is set by break-up velocity and steel constants only — not
by caliber. Numbers, from the shipped registry
([`experiment/_scratch/ell-over-x0-per-shell.py`](../../../_scratch/ell-over-x0-per-shell.py),
to be retained under `checks/` by the derivation pass):

| shell | `r_bu` [mm] | `v_bu` [m/s] | `x₀` [mm] | **`l/x₀`** |
| ----- | ----------- | ------------ | --------- | ---------- |
| 155 mm M107 | 113.9 | 975.6 | 7.14 | **100.2** |
| 105 mm M1 | 77.8 | 937.4 | 5.08 | **96.3** |
| 75 mm M48 | 56.4 | 814.9 | 4.23 | **83.7** |
| 60 mm M49A2 | 41.9 | 988.9 | 2.79 | **94.4** |

So the fleet sits at `l/x₀ = 84–100`, a narrower and higher band than the
finding's verbal "50–200". The residual 1.2× spread is driven by `v_bu` (i.e.
C/M) and by the 60 mm's different `γ'`, **not** by caliber.

**Mott's own numerical example sits in the same regime.** p. 306: 3 in. bomb,
`r ≈ 2 in.` at break-up, `x₀ = 1.6/√γ` in. `= 0.16 in.` at `γ ~ 100` ⇒
`l/x₀ = 2π(2)/0.16 = 79`. He then applied the `l/x₀ = 20` statistic (`1.5x₀`)
to it, on the strength of "the distribution would not be sensibly different for
larger values" (p. 305, above figure 4). **That sentence is the defect**, and
the existing Monte Carlo measures its size. Note also that his "0.24 in." is a
*theoretical* worked example with no fragment measurement attached — adopting a
larger `κ_x` forfeits no empirical anchor, only agreement with Mott's own
rounding. (It does invalidate the closure asserted in `fragmentation.py:156-159`
and in `challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`
— action E.)

## 3. How fast does `κ_x` move with `l/x₀`? (weakly — this is what makes it cheap)

From the committed MC table
([`../breadth-variance-factor-k/derivation.md`](../breadth-variance-factor-k/derivation.md)
§2.4), `⟨x⟩/x₀` runs 1.5604 → 1.6005 → 1.6444 over `l/x₀` = 20 → 50 → 200
(Mott's deterministic `Δτ` step), i.e. ≈ **+0.032 per e-fold** — logarithmic.
Consequences:

- **Across the fleet (84 → 100): 0.3 % on `κ_x`, 0.7 % on `μ`.** Against a
    ±15 % fidelity target this is invisible. A per-shell `κ_x` is not worth a
    shell-indexed constant.
- **20 → ~95: +8 to +11 % on `κ_x` ⇒ +17 to +23 % on `μ`.** That is the whole
    finding, and it is 5–10× what the `(c,k)` pair shipped.
- Robustness: eq. (1) gives `l/x₀ ∝ √γ' · v_bu`, so even a factor-2 error in
    `γ'` or a 30 % error in `v_bu` moves `κ_x` by <2 %. The regime conclusion
    does not depend on the accuracy of `x₀`, only on it being ≫ 20.

**Measured, not interpolated** — the MC was run at the fleet regime in this
pass ([`experiment/_scratch/kx-at-fleet-regime.py`](../../../_scratch/kx-at-fleet-regime.py),
`n ≈ 12 000` each, ~40 s), so Option 1's target values are already known and the
derivation pass is confirming, not discovering:

| scheme | `l/x₀ = 84` | `l/x₀ = 95` | `l/x₀ = 100` |
| ------ | ----------- | ----------- | ------------ |
| Mott `Δτ` | `κ_x` 1.6151, `k` 1.1674 | **1.6210, 1.1722** | 1.6206, 1.1720 |
| exact Poisson | 1.6552, 1.1908 | **1.6689, 1.1858** | 1.6617, 1.1934 |

Fleet spread on `κ_x`: **0.4 %** (Mott step, 84 → 100) — below the MC's own
bootstrap noise on `k`. This is the quantitative answer to the brief's per-shell
question: **one caliber-independent value.** Target triple for Option 1:
`κ_x ≈ 1.62` (Mott step) or `1.67` (Poisson), `k ≈ 1.17`/`1.19`, `c` re-solved.
`μ` multiplier from `κ_x` alone: **×1.17 to ×1.23**.

**No fixed point is needed.** `x₀` is evaluated with the raw steel `γ'`,
upstream of `alpha`, so `l/x₀` does not depend on `κ_x`. (Open question O2
below: *should* `x₀` use the shape-corrected `γ`? If yes, `l/x₀` moves by
`alpha^{1/3}` — and by §3 that is still <2 % on `κ_x`, so it cannot change this
change's outcome. Out of scope here.)

## 4. Options, ranked

| # | Option | Cost | Verdict |
| - | ------ | ---- | ------- |
| **1** | **Re-solve the triple at one fleet-representative `l/x₀` (≈95, the `v_bu`-weighted fleet value), single caliber-independent `κ_x` and `k`, per-shell `c` as now.** Re-run `mott-ruled-line-mc.py` at that `l/x₀`, then `c-on-ruled-line-population.py` on the resulting breadth marginal. | ~1 pass; both scripts already parameterised | **Recommended.** Closes the blocking finding, keeps the one-population identity intact, adds no new constant shape. |
| 2 | Per-shell `κ_x(l/x₀(shell))` and `k(shell)`, computed from eq. (1) inside `mott_params` | +1 MC run per shell (or a fitted `κ_x(ln l/x₀)` curve), a second shell-indexed table, and a `k`/`c` pair that must move with it | **Rejected on physics, not on effort.** §3: 0.3 % across the fleet. It would ship a shell dependence the model cannot resolve, and invites the per-shell-`k` binning trap already retired in `../breadth-variance-factor-k/scoping.md` §6. Record eq. (1) and the fleet spread as a *derived* justification for one value (assumption), not as a mechanism. |
| 3 | Adopt the fully converged `l/x₀ → ∞` limit (use the `l/x₀ = 200` row, `κ_x = 1.64/1.67`) | free (rows exist) | **Acceptable fallback, ~1 % above Option 1.** Defensible as "converged", but it is a limit the shells do not occupy; Option 1 costs one MC run and is honest. Use only if the MC at 95 proves noisy. |
| 4 | Keep `κ_x = 1.5`, log a limitation | free | **Not permissible.** `.claude/rules/deferred-findings.md`: shipped code resting on a number shown to be wrong cannot be closed by agent deferral, and the effect (+17–23 % on `μ`) is outside the ±15 % target. Only the human may elect this. |
| 5 | Fit `κ_x` empirically to fragment data instead of Mott's MC | @librarian pass + a criterion-match argument | Out of scope. A9.3's standing objection ("a 1-D model, not a measurement") is real but is a *different* aspect; resolving the regime inside Mott's own model is the minimal fix to the stated finding. |

### Sub-decision inside Option 1 — Mott's `Δτ` quadrature vs exact Poisson

At `l/x₀ = 200` the two schemes give `κ_x` = 1.644 vs 1.669 (1.5 %), `k` = 1.180
vs 1.195. The exact inhomogeneous-Poisson thinning samples the model Mott
*states* (eq. (4) rate law); his `Δσ = 1/(fCe^{ασ})` increment is 1947 hand
quadrature of it. **Recommendation: adopt exact Poisson as the central value and
carry the Mott step as the low end of the band** — but note the counter-argument
honestly in `derivation.md`: the deterministic step is what reproduces Mott's
*reported* mean (1.560 vs "about 1.5") and figure-4 shape at `l/x₀ = 20`, so
adopting Poisson weakens the reproduction's validation anchor. Either choice is
±1.5 %, i.e. ≪ the 8–11 % move being made; do not spend the pass on it.

## 5. Actions for the derivation pass

- **A.** Confirm §3's table at higher `n` (and a second seed — the `l/x₀ = 95`
    vs `100` non-monotonicity in the Poisson row is MC noise, ±0.002 on `k`,
    and should be shown to be), plus an `l/x₀ = 20` regression row proving the
    reproduction of Mott's own reported mean is unchanged by the re-run.
- **B.** Re-solve `c` per shell on the new breadth marginal via
    `c-on-ruled-line-population.py` (change `XI = mc.run(20.0, ...)` only),
    keeping both `percell` (adopted) and `marginal` closures as the band.
- **C.** Recompute — never scale — the downstream effects: 155 mm B(r) via
    `bofr-at-consistent-population.py` (expect geo-mean ratio 1.046 → ≈0.93,
    i.e. the fit crosses from +5 % to −7 %: comparable magnitude, still 11/11
    inside the 0.5–2× band), and the 75 mm count arms via
    `../mass-dependent-fragment-shape/checks/aspect-ratio-moment-leverage.py`
    (`N₀ ∝ 1/μ`, so `count-gap-1938` improves toward ~1.8×/1.6× but stays
    FAIL — memory `gotcha_mott_count_not_f_squared`: re-run `N`, do not scale).
- **D.** `git mv` both scoping scripts into this update's `checks/`:
    `experiment/_scratch/ell-over-x0-per-shell.py` (produces §2's table) and
    `experiment/_scratch/kx-at-fleet-regime.py` (produces §3's table; replace
    its `importlib` shim with a clean import path if the hyphenated MC filename
    allows).
- **E.** Fix the collateral claims that assume `κ_x = 1.5`: the
    `fragmentation.py:150-160` comment block ("confirmed against Mott's own
    worked example… `1.5·1.6/√100 = 0.24` exactly"), the check script
    `challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`,
    the `MOTT_BREADTH_VARIANCE_K` comment's `l/x₀ = 20` rationale, and
    assumptions **A9.3** and **K3** in the two derivations. Delete the
    blocking marker on `κ_x=1.5` (`breadth-variance-factor-k/derivation.md`)
    only once `src/arty/` ships the new triple.
- **F.** `_limitations.qmd`: one entry — the breadth moments now come from
    Mott 1947's ruled line at the shell's own regime while the mass *law*
    `N(≥m) = N₀e^{−√(m/μ)}` still descends from the 1943 exponential (existing
    assumption K1, now sharper).

## 6. Open questions (log, do not chase)

- **O1.** `l` = circumference assumes fracture is purely axial cracking around
    a full ring; ogive/base regions and the axial crack family are excluded.
    Mott rules the line "to represent the circumference of the cylinder", so
    this is his assumption, inherited. Effect bounded by §3's slope: halving
    the effective `l` costs 2 % on `κ_x`.
- **O2.** Whether `x₀` should carry the raw `γ'` or the shape-corrected
    `gamma = alpha^{-2/3}γ'` (Gold 2017 eq. (6) absorbs the shape into `γ`).
    Affects `l/x₀` by `alpha^{1/3}` and `κ_x` by <2 %; **but it would also
    change `x₀` and hence `μ` directly**, which is a separate aspect — flag for
    a later pass, do not fold into this one.
- **O3.** `v_bu` enters eq. (1) linearly; it is itself the shipped break-up
    fraction `f = 0.943` (item C2). A future revision of `f` shifts the regime
    but, again, by <2 % on `κ_x`.

## 7. Fidelity target

This aspect drives `μ` and `N₀` — hence every fragment count, the `B(r)` lethal-
radius surface, and the `P(kill)` field. **Tolerable error on `κ_x`: ±3 %
(±6 % on `μ`)**, which the `l/x₀`-regime and quadrature bands (±1.5 % each)
sit inside. The shipped value is ~9 % low on this bar, which is why the finding
is blocking; a per-shell `κ_x` (0.3 % of spread) is far below it and is not
warranted.
