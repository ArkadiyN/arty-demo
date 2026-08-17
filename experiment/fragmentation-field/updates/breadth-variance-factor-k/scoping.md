# Scoping — the breadth-variance factor `k` (assumption A9.1)

**Aspect:** the second of the two factors in the Mott shape closure's
product-of-means error, `k = ⟨x²⟩/⟨x⟩²`
(`mass-dependent-fragment-shape/derivation.md` eq. (2)). `c` shipped
2026-08-16 as a per-shell number; `k` is still 1 in shipped code and is
recorded as **deferred** in `mott-fragment-shape-closure/derivation.md` §9,
assumption **A9.1**.

**Pass:** scoping only (Workflow B step 2), 2026-08-16. No derivation, no
`src/arty/`, no `.qmd`.

**Placement — fresh change-slug, `updates/breadth-variance-factor-k/`.**
`k` is an independently-validatable factor with its own PASS/FAIL surfaces
(the 155 mm B(r) fit and the 75 mm count chain), exactly as `c` was; and the
precedent is directly on point — `c` corrects the same constant `A` in the
same closure and was given its own slug (`mass-dependent-fragment-shape/`)
rather than being appended to `mott-fragment-shape-closure/`. That closure's
document is the shipped record of *its* change; its §9 assumption list is
where A9.1 gets a cross-reference, not where a new derivation lives.

---

## 1. Problem statement

The closure's mean-mass step evaluates `2μ = ρ t₀ ⟨A x²⟩` as
`ρ t₀ ⟨A⟩⟨x⟩²` with `⟨x⟩ = κ_x x₀`, `κ_x = 1.5`. The exact error factorises
(`mass-dependent-fragment-shape/derivation.md` eq. (2), verified as an
identity, `1.911879` both sides):

$$\frac{\langle A x^{2}\rangle}{\langle A\rangle\langle x\rangle^{2}}
= \underbrace{\frac{\langle A x^{2}\rangle}{\langle A\rangle\langle x^{2}\rangle}}_{c\ \text{(shipped)}}
\times \underbrace{\frac{\langle x^{2}\rangle}{\langle x\rangle^{2}}}_{k\ \text{(open)}}$$

`k > 1` is guaranteed by Jensen for any non-degenerate breadth distribution,
so **the shipped closure is known to be biased low in `μ` by a factor `k`**,
i.e. `N₀` biased high by `k`. This is the "committed artifact known to carry
a wrong number" case only in the weak sense that A9.1 already documents it;
it is a *known-open, quantified* bias, not a silent one.

**The brief's framing — "apply the per-shell `c` treatment to `k`" — is the
wrong move, and §3 is the reason.** The per-shell `k` values the prior pass
computed are, on inspection, a *discretization artefact* of the very
spectrum they are weighted by. Shipping them would ship an artefact trend.
This scoping recommends a different action.

### Fidelity target

`k` multiplies `μ` and divides `N₀` one-for-one. It drives (a) the
`count-gap-1938` PASS/FAIL arms at 75 mm (thresholds `f ≥ 1.163` for /779,
`f ≥ 1.327` for /700) and (b) the `drag-gap-1944` B(r) geo-mean ratio at
155 mm (currently 1.063 at `c` alone). **Tolerable error on `k`: ±15 %, same
as `A`** — but note that band spans the /779 threshold, so the qualitative
verdict is not robust inside it, and that is itself a result to state rather
than a target to hit.

---

## 2. What is already established (do not re-derive)

| Fact | Where | Status |
| ---- | ----- | ------ |
| `c` and `k` are exact orthogonal factors of one identity; no double-count between them | `mass-dependent-fragment-shape/derivation.md` §2.1; `review.md` verified numerically | **closed** |
| `k` and the shipped break-up-velocity item **C2** cannot double-count | `mass-dependent-fragment-shape/derivation.md` §2.2 **and independently re-verified from the shipped formula** in its `review.md` (§"Factorisation (eq. 2) and orthogonality claims, checked against `src/`"): `A` enters only via `alpha = A·κx²·t_bu/x0`; C2 acts on `x0 ∝ 1/v_bu`; `κx` is independent of `A`, `v_bu` and the breadth distribution — "algebraically disjoint factors of the same product" | **closed — cite, do not re-litigate.** A9.1's stated deferral rationale ("would double-count with the deferred break-up-velocity item", `mott-fragment-shape-closure/derivation.md` §9) is **void**, and was wrong *in kind*, not merely superseded. C2 also realised 1.096× against a 1.2–1.8× reserve (A9.7), so even the budget-hedge reading has lapsed |
| Table-3-weighted `k = 1.5242`, 16-corner band `[1.28, 1.84]`; `c·k = 1.912` band `[1.51, 2.49]` | `mass-dependent-fragment-shape/derivation.md` §4, `checks/aspect-ratio-moment-correction.py` | reproduced by `review.md` |
| Mott-spectrum-weighted per-shell `k` = **1.5114 / 1.3494 / 1.2053 / 1.1057** (155/105/75/60 mm) at shipped `μ` | `mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py` — **runs in ~2 s, re-run rather than recompute** | computed, never shipped or interpreted |
| B(r) at 155 mm: `c=1.00 → 1.226`; `c=1.25 → 1.063`; `c·k=1.91 → 0.792` | `mass-dependent-fragment-shape/derivation.md` §5.1, `checks/bofr-at-new-mu.py` | **the binding constraint** |
| The real B(r) trade is "give up a 6 % fit for a 21 % miss", not "23 % vs 21 %" | `mass-dependent-fragment-shape/review.md` Note 3 | correction already logged; use the 6 %/21 % framing |
| Count chain at 75 mm re-solves as `N`, **not** as `1/f` | `checks/aspect-ratio-moment-leverage.py`; memory `gotcha_mott_count_not_f_squared` | method constraint |

### Open finding carried forward — not closed by this pass

The standing `[deferrable]` Mott/Linfoot structural-premise finding
(`mott-fragment-shape-closure/derivation.md`, since 2026-08-02) concerns the
premise that `A = l/x` is **one constant across shells**, attributed by Gold
2017 to Mott (1943) where the primary says the opposite. **It touches `A`,
not `k`**, and `k`'s definition (`⟨x²⟩/⟨x⟩²`) never invokes the
length–breadth relation: eq. (2) holds for any `A`-distribution whatsoever.
So this aspect neither relies on the disputed premise nor repairs it — the
marker **stays open**, unchanged, and this document does not repeat Gold's
citation. Note, though, that Mott & Linfoot's "our theory … accounts only
for their breadth" is a statement *about the breadth distribution*, i.e.
about exactly the object `k` is a moment of; §3.2 below is where that
becomes usable rather than merely an attribution defect.

---

## 3. The finding that reframes the aspect: three mutually inconsistent values of one quantity

`k` is a moment of **the model's own breadth distribution**. The model
supplies that distribution twice, from two different Mott results, and they
disagree by a factor of ~2.

### 3.1 Route A — the Mott mass spectrum ⇒ `k = 2` exactly, caliber-independent

The code's own fragment-count law is `N(≥m) = N₀ e^{−√(m/μ)}`. With
`m = ρ t₀ A x²` at fixed `A`, `√(m/μ) = x/x_s`, so

$$N(\ge x) = N_0 e^{-x/x_s}\ \Rightarrow\ x \sim \mathrm{Exp}(x_s)
\ \Rightarrow\ k = \frac{\langle x^2\rangle}{\langle x\rangle^2} = 2\ \text{exactly.}$$

This is A9.1's own upper limit, and the key structural point is that **it is
scale-free**: an exponential is a one-parameter scale family, so `k = 2`
holds for every `μ` and therefore for **every shell**. Under the model's
mass law, `k` has no caliber dependence at all.

### 3.2 Route B — Mott's ruled-line breadth statistic ⇒ `k ≈ 1.04`

`κ_x = 1.5` is not free: it is read off Mott 1947's ruled-line Monte Carlo
(`mott-fragment-shape-closure/derivation.md` (M1), A9.3) — *"fragment
circumferential lengths lie mostly in `x₀…2x₀`, average ≈ 1.5 x₀"*.
**`κ_x` and `k` are the first and second moments of one and the same
distribution**, and the closure currently takes the first from this
distribution while implicitly taking the second (via `k = 1`) from nowhere.
A distribution supported mostly on `[x₀, 2x₀]` with mean `1.5x₀` is tightly
bounded: uniform on `[1,2]` gives `⟨x²⟩/⟨x⟩² = (7/3)/2.25 = 1.037`, and no
distribution on that support can exceed `k = 1 + (0.5/1.5)² = 1.111`
(the two-point extremum at the endpoints). So **Route B gives `k ∈ [1.00,
1.11]`, with ~1.04 central** — i.e. essentially no correction.

### 3.3 Route C — Felix 2022 Table 3 ⇒ 1.11–1.52, and it is *not* an independent measurement

`k = ⟨m/A⟩/⟨√(m/A)⟩²` evaluated on Table 3 is **not** data about breadth
dispersion. Table 3 supplies only the conditional aspect mix `A | Group`;
the mass weights are the shell's own Mott spectrum, discretized into 5 mass
groups. Since Route A shows the *undiscretized* answer is 2 for every shell,
what the 5-bin evaluation returns is `2 minus the variance the binning
threw away`. That is exactly why:

- the global value 1.52 sits below 2 and the derivation correctly calls it a
    lower bound ("discarded variance can only raise `k`",
    `mass-dependent-fragment-shape/derivation.md` §4);
- the **per-shell trend is monotone in `P(Group 0)`**, not in any physics:
    `P(G0)` = 0.58 / 0.78 / 0.90 / 0.96 gives `k` = 1.51 / 1.35 / 1.21 / 1.11.
    A shell with 96 % of its population inside one bin has 96 % of its breadth
    variance deleted by construction.

**Therefore: the per-shell `k` values are a measure of the discretization
error of the Mott spectrum, not a caliber-dependent physical quantity.**
The `c` analogy fails here — for `c` the Table-3 weights carried real
between-Group `A`-vs-`m` information that genuinely varies with which
Groups a shell populates; for `k` the table contributes essentially nothing
and the number is a property of the binning.

**Falsifiable prediction, and the one check this pass hands to the
derivation pass:** re-run the same statistic with the mass axis refined
(10, 50, 500 bins over the same range, same `A | Group` mix held piecewise
constant) — `k` must climb toward 2 for *every* shell, and the caliber
spread must collapse. If it does, Route C is retired as evidence.
See §5, verified below.

### 3.4 The discriminator is B(r), and it points at Route B

At 155 mm the independent Ordnance-1944 casualty surface gives geo-mean
`B_model/B_card` = 1.063 at `c` alone and 0.792 at `c·k = 1.91`. Route A
(`k = 2`) is worse still (`c·k ≈ 2.5`). Route B (`k ≈ 1.04`) leaves the
near-exact fit intact. **The only out-of-sample surface in play prefers the
Mott-ruled-line reading of `k` over the Mott-mass-spectrum reading**, and
does so by a wide margin (6 % vs ≥21 % miss, per `review.md` Note 3).

This is not a fitting exercise: Route B's value is derived from `κ_x`'s own
source, not from the B(r) data, so it is a genuine equal-freedom
cross-check by the same standard `review.md` applied to `c`. It also does
*not* trip `gotcha_rebaseline_onto_validation_source` — the recommendation
below adopts the value the *source* gives and reports B(r) as corroboration.

---

## 4. Options, ranked

| # | Option | Effect at 155 mm B(r) | Effect on 75 mm count arms | Verdict |
| - | ------ | --------------------- | -------------------------- | ------- |
| **1** | **Resolve `k` against Mott's ruled-line breadth distribution (Route B)** — the same distribution `κ_x = 1.5` comes from; expected `k ≈ 1.0–1.11`, caliber-independent; retire A9.1's deferral by *settling* it, not by correcting `A` | 1.063 → ~1.02–1.06, preserved | 2.54×/2.28× → ~2.4×/2.2×, still FAIL | **Recommended.** Only option that makes `κ_x` and `k` moments of one distribution, and the only one the B(r) surface accepts |
| 2 | Ship per-shell `k` from Table 3 (the brief's proposal): 1.51/1.35/1.21/1.11 | `c₁₅₅·k₁₅₅ = 1.87` → ~0.80, a 20 % miss replacing a 6 % fit | `f₇₅ ≈ 1.19` (pre-fixed-point) → straddles the /779 threshold 1.163 | **Reject — falsified in §6.1.** The trend is a binning artefact of the wrong sign, understating the same statistic by 15–79 % |
| 3 | Ship the spectrum-consistent `k` (Route A as corrected for the `A`-mix): **1.74 / 1.82 / 1.91 / 1.98** (§6.1) | `c·k₁₅₅ = 2.17` → ≈0.72, a ~28 % miss replacing a 6 % fit | `f₇₅ ≈ 1.88` — both arms pass (~1.5×/1.3×) | **Reject on evidence, retain as the stated internal inconsistency.** It is what the model's own mass law implies; adopting it to pass the count arms while breaking the only out-of-sample surface is `gotcha_rebaseline_onto_validation_source` |
| 4 | Leave `k = 1`, restate A9.1 with the void rationale replaced and the three-route inconsistency logged | unchanged | unchanged | **Acceptable fallback** if §5's checks do not resolve Route B. Strictly better than the status quo because A9.1's *reason* is currently wrong |
| 5 | Fit `k` per shell to the count arms | — | passes by construction | **Reject** — `gotcha_rebaseline_onto_validation_source` |

Options 1 and 4 differ only in whether a number ships; both require the same
§5 work, so the derivation pass should attempt 1 and fall back to 4.

### 4.1 Recommendation

**Run Option 1, fall back to Option 4. Do not ship a per-shell `k`.**

Stated against the brief's three asks:

- **Per-shell `k` (or `c·k`): no.** Not because it is hard, but because §6.1
    shows the per-shell numbers that motivated the ask are a discretization
    artefact whose caliber trend has the wrong sign. `k` is scale-free under
    the model's own mass law (§3.1); what caliber dependence survives
    (1.74→1.98) is the `A`-mix effect already carried by `c`, and it spans
    only 14 % — inside the ±15 % fidelity target, so **one `k` for all shells
    is defensible in a way one `c` was not.** This is the substantive
    difference between this aspect and `mass-dependent-fragment-shape`, and
    it is why the brief's "same treatment" premise does not carry over.
- **The B(r) trade-off (`mass-dependent-fragment-shape/review.md` Note 3):
    factored in, not re-derived.** The correct framing is *give up a 6 % fit
    for a ≥21 % miss*, not "23 % vs 21 %". Every candidate `k > 1.2` loses
    that trade at 155 mm. Since the B(r) surface is the only out-of-sample
    validation the closure has, and `k`'s two candidate sources disagree by
    1.9×, **B(r) is admissible as a tie-breaker between two independently
    derived values** — that is a discriminator, not a fit, and it points at
    Route B (`k ≈ 1.04`). It would *not* be admissible to tune `k` freely.
- **The C2 double-count concern (`updates/breakup-velocity-fraction/`):
    closed, cited, not re-litigated.** `mass-dependent-fragment-shape/`'s
    `derivation.md` §2.2 argues it and its `review.md` independently verifies
    it from the shipped formula (`A` enters only through
    `alpha = A·κx²·t_bu/x0`; C2 acts on `x0 ∝ 1/v_bu`) — "algebraically
    disjoint factors of the same product". A9.1's stated deferral rationale
    is therefore void, and the derivation pass should **replace** that
    sentence in `mott-fragment-shape-closure/derivation.md` §9 rather than
    leave a wrong reason standing next to a still-open assumption. That edit
    is in scope for this change even though the assumption's *disposition*
    may not change.

**What the human is choosing between**, stated plainly, because the
derivation pass cannot decide it alone: the closure is internally
inconsistent about its own breadth distribution. Mott's ruled-line result
(source of `κ_x = 1.5`, shipped) implies `k ≈ 1.04`; Mott's mass spectrum
(source of `N(≥m)`, shipped) implies `k ≈ 1.9`. Both are shipped and used.
`k = 1` is within 4 % of the first and 47 % low against the second. Option 1
resolves this in favour of the ingredient `k` is definitionally a moment of
(`κ_x`'s own distribution) and is corroborated out of sample by B(r);
Option 4 ships nothing and logs the inconsistency. **Neither closes
`count-gap-1938`** — and per §6.2 of the prior derivation that thread's 75 mm
residual has already been shown not to be a shape-moment artefact, so `k`
should not be recruited to close it.

**Expected outcome for `count-gap-1938`: no change** (Option 1) — arms stay
at ~2.4×/2.2×, still FAIL. That is the honest result and should be stated as
one, not hedged.

---

## 5. Actions for the derivation pass

- **A — settle Mott's breadth distribution.** Read Mott 1947 finding (1)
    (`doc-reference/fragmentation/…gurney-equations-fragmentation/`, rspa line
    ~190, anchor per `mott-fragment-shape-closure/derivation.md` (M1)) and
    Mott & Linfoot 1943 sect. 3 (retained at
    `doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/`,
    which explicitly *does* treat breadth — see §2's finding note). Recover the
    ruled-line breadth histogram or its analytic form; compute `⟨x²⟩/⟨x⟩²`
    from the same object that yields `1.5`. If neither source resolves the
    second moment, **@librarian is needed** for Mott's ruled-line appendix;
    otherwise report Route B as the `[1.00, 1.11]` support bound, which is
    already decision-sufficient.
- **B — DONE this pass.** `checks/k-bin-refinement.py`, results in §6.1.
    Option 2 is falsified; the derivation pass does not need to revisit it.
- **C — re-run `checks/bofr-at-new-mu.py` at the chosen `k`** (it already
    parameterises `A_eff`) rather than interpolating the three published rows.
- **D — do not re-derive** the `c`/`k` orthogonality or the C2 double-count
    question; cite §2's table.
- **E — edit `mott-fragment-shape-closure/derivation.md` §9 A9.1** to strike
    the void double-count rationale (§4.1) and point at this folder. Whatever
    Option lands, that sentence must not survive.
- **F — `_limitations.qmd` entry** on the two-Mott-distributions inconsistency
    (§3.1 vs §3.2), regardless of Option. This is the reader-facing content of
    this aspect and is owed even under Option 4. A logged assumption is a valid
    closure here: the shipped `k = 1` sits within 4 % of Route B, so under
    Option 4 nothing the demo shows moves.

---

## 6. Verified: the per-shell `k` trend is a binning artefact

Run 2026-08-16, [`checks/k-bin-refinement.py`](checks/k-bin-refinement.py)
(this folder, ~3 s). Same Table-3 `A | Group` mix, same shipped `μ`, same
`_MOTT_ASPECT_RATIO` pin-back as the prior pass; only the **number of mass
nodes** changes. Mass axis integrated against the model's own spectrum via
equal-probability strata in `u = √(m/μ) ~ Exp(1)`, `m = μu²` (midpoint nodes
— memory `gotcha_belt_gate_quadrature_endpoint`).

`k` by number of mass nodes:

| shell | `μ` [gr] | **5-bin (shipped groups)** | 10 | 50 | 200 | 2000 | 50000 | 50000, capped at 7500 gr (A2) |
| ----- | -------- | -------------------------- | -- | -- | --- | ---- | ----- | ----------------------------- |
| 155 mm M107 | 98.10 | **1.5114** | 1.6041 | 1.7145 | 1.7264 | 1.7359 | **1.7374** | 1.7321 |
| 105 mm M1 | 31.85 | **1.3494** | 1.7189 | 1.8115 | 1.8008 | 1.8153 | **1.8166** | 1.8166 |
| 75 mm M48 | 14.33 | **1.2053** | 1.8647 | 1.8718 | 1.8985 | 1.9054 | **1.9051** | 1.9051 |
| 60 mm M49A2 | 7.62 | **1.1057** | 1.8576 | 1.9109 | 1.9719 | 1.9744 | **1.9761** | 1.9761 |

**Limit check.** The 5-bin column reproduces
`mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py`'s
per-shell `k` to 4 decimals (1.5114 / 1.3494 / 1.2053 / 1.1057) — the
refinement is the *only* difference between the two computations. ✓

**Verdict — §3.3 confirmed, and more strongly than predicted.**

1. **`k` converges to 1.73–1.98, not to 1.1–1.5.** The 5-bin values understate
    the same statistic by 15 % (155 mm) to **79 %** (60 mm). Convergence is
    reached by ~200 nodes; the open-bin truncation at 7500 gr (A2) moves it by
    ≤0.3 %.
1. **The caliber trend does not merely vanish — it reverses.** 5-bin gives
    `k` *falling* with caliber (1.51→1.11); converged gives it *rising*
    (1.74→1.98). Shipping the per-shell 5-bin values would have shipped a
    trend of the wrong sign, on top of a level error of up to 79 %.
1. **The residual spread below `k = 2` is the aspect mix, not the caliber.**
    Route A's `k = 2` is exact only at constant `A`; here `x² = m/A` and `A`
    rises with `m`, which damps the breadth variance. That damping is largest
    for 155 mm, whose spectrum straddles the most Groups — the same mechanism
    that makes `c` largest there. The converged numbers are Route A **as
    corrected for `c`'s own physics**, and they are ~2, not ~1.

**Consequence for the options.** Option 2 (ship the per-shell 5-bin `k`) is
**dead** — it is a discretization artefact of known sign and size. The live
choice is Options 1 vs 3: Mott's ruled-line breadth distribution
(`k ≈ 1.04`) against the Mott mass spectrum (`k ≈ 1.74–1.98`), which differ
by ~1.9× and cannot both be right, since the closure uses both objects.
`c·k` at the converged values would be **2.17 / 2.00 / 1.88 / 1.82**
(155/105/75/60), which on the 155 mm B(r) surface is a ≳25 % under-prediction
against `c`-alone's 6 % over-prediction — so the discriminator in §3.4 is
unchanged and, if anything, sharper.
