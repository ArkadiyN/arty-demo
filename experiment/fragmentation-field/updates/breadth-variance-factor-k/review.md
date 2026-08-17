# Review — `breadth-variance-factor-k` (assumption A9.1)

## Pass 1 — adversarial critique, 2026-08-17 (@model-reviewer)

**Scope.** `derivation.md` in full; the A9.1 rewrite in
`../mott-fragment-shape-closure/derivation.md` §9 and `_limitations.qmd`
entry 18 (both read as diffs vs `HEAD`); `scoping.md` for context only.
Adversarial critique pass — arguments, protocol, and closure structure.
Full numerical reproduction of `checks/mott-ruled-line-mc.py` and
`checks/bofr-at-resolved-k.py` is Pass 2's job and was **not** performed
here; the estimates below are analytic/order-of-magnitude and are labelled
as such.

**Register state at pass start.** `collect-findings.py --for
experiment/fragmentation-field/updates/breadth-variance-factor-k/` returns
one open finding — the `kappa_x` marker this pass itself raised at
`derivation.md:306`. It is not an untouched inherited finding; it is
addressed below as **B1** (tier, not substance).

---

### Verdict: **FAIL**

Two Blocking findings. Neither disputes that `k = 2` is retired — §2.1 is
the strongest argument in the document and I think it is right. Both concern
what happens *after* that: which population the surviving moment is averaged
over (**B2**), and how the acknowledged `κ_x` defect is tiered (**B1**).

---

### B1 — **Blocking** — the `κ_x` finding is tagged `deferrable`, but it names shipped code resting on a number this pass has just shown to be wrong

`derivation.md:306` (marker), §2.4 (lines 176–184), §5.3 (lines 298–304).

The marker's own text says: shipped `κ_x = 1.5` is Mott's `l/x₀ = 20`
demonstration value; reproducing his procedure in the `l/x₀ = 50–200` regime
real shells occupy gives 1.65; `μ ∝ κ_x²` ⇒ `μ` low by ~21 %. `affects:`
includes `src/arty/fragmentation.py`.

`.claude/rules/deferred-findings.md`, "What may not be deferred at all":
*a committed artifact known to carry a wrong number — or shipped code
resting on one — cannot be closed by an agent's deferral … Mark it
`blocking` and say so in your return summary. Only the human decides it can
wait.* That is this case exactly, and it is not a borderline reading: the
derivation states the defect affirmatively (not as a suspicion), quantifies
it, and routes it at `src/arty/fragmentation.py`. The pass then closes A9.1
as **resolved** while the same section records a larger, same-signed error in
the neighbouring factor of the same product.

**Impact.** `μ` +21 %, `N₀` −21 % on every shell. On the 155 mm B(r) surface
of §3, using that section's own `A_eff → B` sensitivity (`B ∝ A_eff^−0.66`,
read off the `k = 1 → 2` rows), a 21 % `μ` rise moves the geo-mean ratio
0.975 → ≈0.86. That is inside the 0.5–2× band but outside the ±15 %
fidelity target, and it is *larger than the correction this change ships*
(14 %). Every downstream lethal-radius / fragment-count number moves by
roughly the same fraction.

**Correction (no physics change required in this pass).** Re-tier the marker
to the `blocking` tag with the same text, and name it in the pass's return
summary as a human decision. If the human elects to defer, the deferral is
theirs and the marker stays `blocking` until `κ_x` is re-derived.

---

### B2 — **Blocking** — `c` and `k` are averaged over two different, mutually inconsistent populations, and §5.2's defence does not cover it

§5.2 (lines 279–296), §5.1 (lines 251–261), K1 (line 326).

Eq. (2) of `../mass-dependent-fragment-shape/derivation.md`,
`⟨Ax²⟩/⟨A⟩⟨x⟩² = c·k`, is exact **for one distribution**. Every `⟨·⟩` in it
runs over the same population. This pass takes the two factors from two
different ones:

- `c = 1.2506` is not a raw Table-3 statistic. Per that update's review
    finding **A1** (which was *Blocking* and forced the per-shell rebuild),
    `c` is a **`μ`-weighted moment** — Table 3 re-weighted by each shell's own
    Mott spectrum `N(≥m) = N₀e^{−√(m/μ)}`, solved as the fixed point
    `μ = c·μ₀`. Its weighting population is therefore the **1943-descended
    mass spectrum**, whose own breadth statistic is the `1.74–1.98` the
    scoping computed (§1, line 45).
- `k = 1.1375` is the second moment of the **1947 ruled-line** gap
    distribution — a population with *no* mass below `0.4x₀` and a
    single interior mode.

§5.2 defends the mismatch by saying Table 3 "does not measure the breadth
distribution", so its apparent `k` may be discarded while its `c` is kept.
That is true of the *numerator* of `c` and false of its *weighting*. `c − 1 =
Cov(A, x²)/(⟨A⟩⟨x²⟩)` is a normalised covariance, and a normalised
covariance is a functional of the spread of `x²` in the population it is
averaged over. Swap the population and `c` moves — necessarily, and toward 1
as the population narrows, because `Cov → 0` as the distribution collapses to
a point. The two populations here differ in exactly that spread, and by a
large factor: `CV_x = √(k−1)` is 0.37 for the ruled line against ~0.95 for
the Mott spectrum, so `CV_{x²}` differs by ~2.5×.

**This is finding A1 recurring in a new coordinate.** A1 established that
this `c` inherits its weighting population and does not transfer; §5.2
asserts the opposite for the one transfer this pass performs, and the
assumption is not logged in K1–K4.

**Impact (analytic estimate, direction certain, magnitude approximate).**
Scaling `c − 1` by the ratio of `CV_{x²}` gives `c₁₅₅ ≈ 1.10` on the
ruled-line population instead of 1.2506, so `c·k ≈ 1.10 × 1.14 = 1.25`
against the pass's `1.426` — `A_eff` −12 %, i.e. ~2.0 rather than 2.28,
which is the **shipped** value. Propagating through §3's `B ∝ A_eff^−0.66`
puts the geo-mean ratio back at ≈1.06 — the shipped row. So the headline
"the resolved `k` **improves** the fit, 1.063 → 0.975, there is no trade"
(§3, abstract line 24) does not survive making the two factors consistent:
it reverses to "no measurable change". That is a qualitative reversal of an
in-scope conclusion, which is the Blocking tier.

Note the fixed point also moves: with `k` in the chain the closure is
`μ = c·k·μ₀`, not `μ = c·μ₀`, so `c` must be re-solved at the new `μ` even
if the population question is set aside. That part is small (~2 % on `μ`, by
the `c`-vs-`μ` slope implied by the four shipped per-shell `c` values) and is
*not* what makes this Blocking.

**The two self-consistent options both miss 0.975; only the mixed pair hits
it.** Spelling out the fork makes the exposure concrete:

| population for **both** moments | `c₁₅₅` | `k` | `A_eff = 1.6·c·k` | §3 geo-mean `B_model/B_card` |
| ------------------------------- | ------ | --- | ----------------- | ---------------------------- |
| 1943 spectrum (as `c` is weighted today) | 1.2506 | ~1.9 | ~3.8 | ~0.67 (interpolating §3's `k=2` row) |
| 1947 ruled line (as `k` is derived today) | ~1.10 est. | 1.1375 | ~2.0 | ~1.06 |
| **mixed — what this pass ships** | 1.2506 | 1.1375 | 2.276 | 0.975 |

The row that "improves the fit" is the only one that averages its two
factors over different populations. That is not a proof the mixed pair is
wrong — but it is precisely why the B(r) agreement cannot be offered as
corroboration of it, and it is what makes the finding Blocking rather than a
logged assumption.

**The prior update anticipated this standard and applied it to `k` only.**
`../mass-dependent-fragment-shape/derivation.md` §6 (the `c₇₅·k = 1.50`
paragraph) declines to quote `k = 1.524` on a 75 mm chain because "`k = 1.524`
is itself Table-3-weighted and would need the same per-shell treatment before
it could be quoted". This pass correctly re-derived `k` off Table 3 — and
then left `c` on the Table-3/1943-spectrum weighting the same paragraph
identifies as the problem. The `±0.6–3.6 %` method band on the per-shell `c`
(that derivation §3.4b) does **not** cover this: it sweeps the Table-3 mass
axis at a fixed spectrum family, not a change of population.

**Correction.** Re-run
`../mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py`
with the weighting population induced by the ruled-line breadth
distribution (`m ∝ A x²`, `x` sampled from `mott-ruled-line-mc.py`) rather
than by `N(≥m) = N₀e^{−√(m/μ)}`, and re-solve the fixed point as
`μ = c·k·μ₀`. If that is out of scope for this change, the alternative
closure is to **withdraw the "improves the fit" claim** in §3, the abstract,
and `_limitations.qmd` entry 18, and log the mixed-population assumption
explicitly with the bound above — but the claim cannot stand as written,
because entry 18 currently offers the B(r) improvement as the evidence that
the practical exposure of mixing 1943 and 1947 objects "is bounded", and
that improvement is the quantity the mixing produces.

---

### D1 — **Deferrable** — both configuration choices that fix `k` push it to the low end, and both are justified by consistency with the constant §5.3 flags as wrong

§2.4 (lines 137–184), K3 (line 328).

The MC table offers six values of `k` spanning 1.1375–1.1954. The pass ships
the **smallest**, via two independent choices:

1. `l/x₀ = 20` rather than the converged 50–200 — justified as internal
    consistency with `κ_x = 1.5`. But §2.4 and §5.3 simultaneously say real
    shells sit at `l/x₀ = 50–200` and that `κ_x = 1.5` is therefore ~10 %
    low. So the consistency being preserved is with a **shipped legacy
    constant**, not with the physical configuration; the internally
    consistent *physical* pair is `(κ_x, k) = (1.67, 1.20)`, which the pass
    names and declines.
1. Mott's deterministic `Δτ` increment rather than the exact
    inhomogeneous-Poisson thinning — even though the derivation itself
    describes the deterministic step as "a small bias" (line 179) and ran the
    Poisson scheme precisely to expose it.

Neither choice is a fit, and §3.2's disclaimer that `k` was computed without
reference to the casualty card is accepted — the value does not come from the
card. But the *selection among computed candidates* is not similarly
insulated: the selected row is also the one closest to the B(r) optimum
(0.975), and §3 then presents the card's approval of that row as independent
corroboration. It is weaker evidence than §3 claims, because the choice rule
and the scored quantity both favour low `A_eff`.

**Impact.** `k` 1.14 → 1.20 alone is +5 % on `μ` — inside the fidelity bar,
which is why this is Deferrable and not Blocking. Combined with B1's `κ_x`
it is +27 %, but that is B1's impact, not double-counted here.

**Correction.** Either adopt the converged pair (which entails B1) or keep
`k = 1.14` and state in K3 that the choice is consistency with the *shipped*
`κ_x`, not with the physically applicable configuration — and soften §3's
"corroboration" to "not rejected by".

---

### D2 — **Deferrable** — `_limitations.qmd` entry 18 asserts a bound it does not establish

`_limitations.qmd` new entry 18, "The practical exposure is bounded and was
checked out of sample".

The B(r) check varies `k` only. It cannot bound the exposure of the
1943/1947 mixing, because the mass law — the object entry 18 says is
inherited from 1943 — is held fixed in every row of that sweep. A sweep that
does not vary the quantity in question has no power over it (same shape as
the fixed-geometry/drag-degenerate pattern). What the check does establish is
narrower and true: at fixed mass law, the 1947 second moment fits the card
better than the 1943 one.

**Impact.** No number changes; it is a claim-strength defect in a published
surface. Reword to: "the surface that can see the *breadth moment* prefers
the 1947 value; the exposure of retaining the 1943 *mass law* is not
bounded by this or any check performed."

---

### N1 — **Note** — "no fragments below `0.4x₀`" is a bin-resolution statement, not a hard support cutoff

§2.4 item 3 (lines 159–163), repeated in the A9.1 rewrite and in entry 18.

The release-zone half-width is `√(τ − τ_j)`, which is **zero** at the instant
a crack nucleates, so a subsequent crack may form arbitrarily close to an
existing one and the gap density is positive-but-vanishing near 0, not
identically zero. The MC's empty first bin is a statement about `0.4x₀`
bin resolution at the sampled `n`, not about the support. The physical
argument (shielding suppresses short gaps, unlike an exponential whose mode
is at 0) is unaffected and correct.

**Impact.** None on any number. Prefer "negligible density below `0.4x₀`".

---

### N2 — **Note** — the `α = 1` identification is a genuine closure and should be labelled one

§2.3 (lines 124–127). `dn/ds = lfCe^{γs}` with `σ = γs` gives
`dn/dσ = (lfC/γ)e^{σ}`, so `α = 1` follows by substitution rather than by
assumption — this is the strongest form of source closure available
(`source-data-fidelity.md`, "a stated equation is the substitution its source
says it is") and the cross-check against Mott's own worked "the increase in
σ is unity" step is exactly right. Worth marking as a closure invariant in
§4's table rather than leaving it as prose, so Pass 2 re-runs it.

---

### What I checked and did not find fault with

- **Dimensional analysis.** `k` is a ratio of like moments — dimensionless.
    `A_eff = 1.6·c·k` is dimensionless throughout. §4's table is correct as
    far as it goes.
- **§2.1 — the retirement of `k = 2`.** The circularity argument (the 1943
    exponential is the *premise* of the mass law, so the mass law's agreement
    with it is vacuous) is sound and is the correct reading of the quoted
    passage. This is the finding of the pass and I would not weaken it.
- **Jensen floor / exponential limit.** `k > 1` strictly, and `k → 2` when
    shielding is switched off, correctly recovering Route A as the
    no-shielding limit. Both right.
- **Caliber independence (§5.1).** Correctly derived rather than assumed —
    the scaled model has no caliber parameter and `x₀` divides out of a moment
    ratio. This is a stronger justification than the scoping's and I accept
    it.
- **Layering.** No physics, constants, or computation leaked into a `.qmd`.
    Entry 18 is prose plus already-derived numbers; `MOTT_BREADTH_VARIANCE_K`
    is correctly deferred to the `src/arty/` pass.
- **Script retention.** All three scripts named in §6 are present in
    `checks/`; `bofr-at-resolved-k.py` re-executes the committed
    `bofr-at-new-mu.py` by module load rather than re-typing its series, which
    is the right shape.

- **Source-data gate (mine, not Pass 2's) — passes.** `bofr-at-resolved-k.py`
    loads `bofr-at-new-mu.py` as a module, which loads
    `b-vs-range-155mm.py`, which reads `CARD_R_FT` / `CARD_B` via
    `pd.read_csv` from
    `doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/155mm-m107-casualties.csv`
    — no hand-typed literal array anywhere in the chain.
    `check-table-invariants.py <that dir> --all` returns **0 / 6 failed**
    (155 mm casualties: 11 rows, 6 checks, ok).
- **Criterion match — correct table.** The check scores against the
    *casualties* CSV, not the `-perforation-1-8in` sibling that sits beside
    it in the same directory. `B` is the fragment-density quantity the model
    computes. (This is the exact confusion the open register entry on the
    105 mm perforation column records elsewhere; it is not present here.)

**Not checked (Pass 2 scope):** numerical reproduction of the §2.4 moment
table, the §3 B(r) table, or the figure-4 histogram shape.

---

### Summary of required actions

1. **B1** — re-tier the `derivation.md:306` marker to `blocking`; surface to
    the human. No physics change in this pass.
1. **B2** — either re-solve `c` on the ruled-line population (and the fixed
    point as `μ = c·k·μ₀`), or withdraw the "improves the fit" claim from the
    abstract, §3, and `_limitations.qmd` entry 18 and log the
    mixed-population assumption with its ~12 % `A_eff` bound.
1. **D1** — record in K3 that the configuration choice is consistency with
    the shipped `κ_x`, not with the physical regime; soften §3's
    "corroboration".
1. **D2** — reword entry 18's "exposure is bounded and was checked".
1. **N1/N2** — optional wording / closure-labelling.

---

## Pass 1 re-review (fix cycle 1) — 2026-08-17

Scope: verification of the required actions B1, B2, D1, D2, N1/N2 from the
Pass 1 section above, plus anything downstream of them. Not a fresh full
review.

**Verdict: (pending — see below)**

### Check-script reproduction (independent re-run, worktree repo root)

Both new scripts run standalone under `uv run python <path>` and their
printed output matches what `derivation.md` cites.

- `checks/c-on-ruled-line-population.py` — prints
    `k_MC = 1.1375` (n=5127, `<xi>` = 1.5604, `l/x₀ = 20`); `percell` row for
    155 mm M107: `c_ruled = 1.1254`, `k_pop = 1.1227`, `A_eff = 2.0482`.
    Matches §3.0 table line 244/257 and §5.1 exactly. The `marginal` closure
    row (`c = 1.0372`, `A_eff = 1.888`) matches §3.1 line 297 and K5.
    The four-shell §5.1 table (155/105/75/60 mm `c` = 1.1254 / 1.0608 /
    1.0247 / 1.0026, `A_eff` = 2.048 / 1.931 / 1.865 / 1.825) reproduces
    row-for-row. ✓
- `checks/bofr-at-consistent-population.py` — prints the geo-mean fit table:
    `c=1.28, A_eff=2.048 → 1.046, 11/11`; `c=1.25 (shipped) → 1.063, 11/11`;
    `c=1.42 (pre-fix mixed) → 0.975, 11/11`; `c=1.18 (marginal) → 1.104`.
    Matches §3.1 lines 296–298 and the abstract's "1.063 → 1.046". ✓
    Note the script's `c` column is the *product* `c·k` (1.1254 × 1.1375 =
    1.280), which is what §5.2 line 396 states — no double-count.
- Runtime for both is a few seconds; retention and naming conform to
    `verification-scripts.md`.

### Required actions — disposition

**B1 — satisfied.** The marker moved to `derivation.md:438` (§5.3), tier
`blocking`, text "shipped kappa_x=1.5 (A9.3) …".
`collect-findings.py --for .../breadth-variance-factor-k/` returns it as the
one open finding on this scope, tier `blocking`, `affects:` naming
`src/arty/fragmentation.py` and the `mott-fragment-shape-closure` derivation.
The escalation is also carried in prose in two places a reader will meet it:
§5.3 ("stays blocking until `κ_x` is re-derived or a human elects to defer")
and A9.3 of `../mott-fragment-shape-closure/derivation.md:368-375`, which now
says **Open blocking finding** and quantifies ~21 % on `μ`. This is the
correct disposition under `deferred-findings.md` — an agent may not close it,
and it is not closed. ✓

**B2 — satisfied, and by the stronger of the two options offered.** `c` was
re-solved on the ruled-line population rather than the claim being withdrawn:

- §3.0 states the one-population argument correctly —
    `c − 1 = Cov(A,x²)/(⟨A⟩⟨x²⟩)` is a *normalised* covariance and therefore a
    functional of the spread of `x²` in whatever population it is averaged
    over, so a population swap **must** move `c`. That is the right reason,
    not a hand-wave.
- The fixed point is corrected to `μ = c·k·μ₀` (the shipped `μ = c·μ₀` omitted
    `k`) — `c-on-ruled-line-population.py:172`. I checked the moment algebra:
    `c = ⟨Aξ²⟩/(⟨A⟩⟨ξ²⟩)` and `k_pop = ⟨ξ²⟩/⟨ξ⟩²` with the mass scale `S`
    cancelling out of both, so `S` enters only through which mass bracket a
    cell lands in. Dimensionally clean; both quantities dimensionless.
- The mixed-population claim is withdrawn *everywhere it appeared*: abstract
    (lines 34–37), §3.1 item 1, §5.2 ("that defence was wrong and is
    withdrawn"), §5.4 (`drag-gap-1944` now "no measurable change"). The 0.975
    row survives only as the labelled *mixed* row, with the reason it hits.
- Non-uniqueness of the reconstruction is logged as **K5** with an honest band
    (`c₁₅₅ ∈ [1.037, 1.125]`, `A_eff ∈ [1.888, 2.048]`) that is explicitly
    wider than the shipped `c`'s ±0.6–3.6 % method band and **straddles** the
    shipped `A_eff` — which is exactly why §3.1 now reports a null. **K6** logs
    the `S` anchoring choice and its 2.5 % reweighting distortion. Both are new
    and both are the right things to have logged.
- A new closure was added and passes: `k_pop ≈ k_MC` (the reconstruction must
    reproduce the marginal it was handed), §4 row 7.
- Downstream consistency holds. `../mott-fragment-shape-closure/derivation.md`
    A9.1 (lines 337–357) carries the new per-shell `c`, the `μ = c·k·μ₀` fixed
    point, and the +2.4 %/+24 % framing. `_limitations.qmd` entry 18 (lines
    682–688) carries `1.2506 → 1.1254` and `2.001 → 2.048`. No stale
    "improves the fit to 0.975" survives anywhere I grepped. ✓

**Comparison-protocol re-check (the thing B2 was an instance of).** §3.1's
bottom row is now the 1943 population supplying *both* moments
(`c = 1.2404`, `k = 1.5114`), so Route A is scored apples-to-apples rather
than at a hybrid. That is the correct repair of the protocol defect. See N4
below for a residual asymmetry that does not change the conclusion. ✓

**D1 — satisfied.** K3 (`derivation.md:464`) now says in terms: "The
consistency being preserved is with the **shipped legacy constant**
`κ_x = 1.5`, **not** with the physically applicable configuration — real
shells sit at `l/x₀ = 50–200`, whose internally consistent pair is
`(κ_x, k) = (1.67, 1.20)`." §3's "corroboration" language is gone: §3.1 item 2
now reads "the card was free to reject the pair and did not — but 'did not
reject' is now the whole of the claim." ✓

**D2 — satisfied.** `_limitations.qmd:696-704` now reads "**The exposure of
that retention is not bounded by any check performed here**", followed by the
narrower true statement (fixed mass law; the surface that can see the breadth
moment prefers 1947). This is the correction verbatim in intent. ✓

**N1 — addressed.** "negligible density below `0.4x₀`" in both
`_limitations.qmd:678` and `mott-fragment-shape-closure` A9.1, with the
release-zone half-width `√(τ−τ_j)` vanishing-at-nucleation caveat spelled out.

**N2 — addressed.** The `α = 1` substitution is now a labelled row in §4's
closure table (line 348) rather than prose.

### New findings (this cycle, all downstream of the B2 fix)

**N3 — Note — `k_pop` range understated by rounding.** §3.0 line 263 and §4
line 347 quote `k_pop = 1.121–1.144`; the script's `percell` minimum is
**1.1227** (155 mm), not 1.121. Impact: none — the closure passes either way
(~1.5 % vs `k_MC`). Suggest `1.123–1.144`.

**N4 — Note — the 1943 comparison row is not evaluated at its own fixed
point.** `bofr-at-consistent-population.py:39` hand-types
`c = 1.2404, k = 1.5114`; I re-ran
`../mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py` and
those are indeed its 155 mm outputs — but they are evaluated at `μ = μ₀ =
98.10 gr`, i.e. *without* the `μ = c·k·μ₀` update that the 1947 row does get
(`μ = 125.58 gr`). Strictly the two sides are not given identical freedom.
**It does not threaten the conclusion, and the direction matters:** raising
`μ` for the 1943 population moves weight out of Group 0 (`P(G0) = 0.583`),
and both `c` and `k` rise with `μ` in that script's own caliber series, so a
self-consistent 1943 row would sit *above* `c·k = 1.875` and score *worse*
than 0.803. The asymmetry is therefore conservative against the row it
rejects. Impact on any shipped number: zero. Suggest one clause in §3.1 item 3
saying the 1943 row is evaluated at `μ₀` and that closing its fixed point
would move it further from the card, alongside the existing bin-convergence
remark. Also worth naming the producing script *and* that these are its
`μ₀`-row values, since 1.2404 matches neither the shipped 1.2506 nor the
converged 1.2620 quoted in `mass-dependent-fragment-shape/review.md:490` and
a reader cannot otherwise tell which of the three it is.

**Deferrable-1 — the small-caliber content of the change has no out-of-sample
surface, and entry 18 does not say so.** §5.1 ships `A_eff` +18.3 % (75 mm)
and +24.0 % (60 mm); §3.1 establishes that the only out-of-sample surface
available is 155 mm B(r), where the change is a null. So the part of this
change that *does* move the demo is the part nothing checks. `_limitations.qmd`
entry 18 states the magnitudes (lines 686–688) but leaves the reader to infer
the absence of validation from the preceding paragraph, which is about the
mass law rather than about the calibers. Impact: `μ ∝ A_eff`, so 60 mm `μ`
+24 % and 75 mm +18 % — fragment mass/velocity and hence lethal radii at the
small calibers move by that much on an unvalidated basis; at 155 mm nothing
moves. Resolution is a **logged limitation**, not a fix. Suggested clause for
entry 18: "the 155 mm casualty card is the only out-of-sample surface
available, and it is the one caliber at which this change is a null — the
+18 %/+24 % at 75/60 mm is unchecked against any measurement."

### Verdict — PASS-with-limitations

No Blocking findings. All four required actions (B1, B2, D1, D2) are
satisfied, both optional Notes were taken up, the two new check scripts run
standalone and reproduce every number the derivation cites from them, and the
B1 marker is present, correctly tiered `blocking`, and surfaced in prose in
both affected derivations rather than only in the register.

To log: **Deferrable-1** (one clause in `_limitations.qmd` entry 18 on the
absence of an out-of-sample surface at 75/60 mm). N3 and N4 are wording
improvements with no numeric effect.

Out-of-scope observation (not this cycle, not blocking): the assumption rows
in §5.5 run K1, K2, K3, K5, K6, K4 — K4 sits last, after K6. Cosmetic.

---

## Pass 2 — verification — 2026-08-17

Scope: mechanical verification of the settled (post-fix) `derivation.md`
against its check scripts and primaries. Not a re-run of the adversarial
theory critique (Pass 1, already PASS-with-limitations above).

**Verdict: PASS-with-limitations**

### 1. Check-script reproduction (independent re-run, worktree repo root)

All five scripts under `checks/` reproduced standalone, output matched
against `derivation.md`'s cited numbers verbatim (to the printed decimal):

- `mott-ruled-line-mc.py` — §2.4 table reproduces exactly, all six rows
    (`k = 1.1375 / 1.1607 / 1.1801 / 1.1777 / 1.1922 / 1.1954`,
    `n = 5127` for the adopted `l/x₀=20` Mott row), and the figure-4 histogram
    (`0.000 / 0.083 / 0.217 / 0.262 / 0.215 / 0.137 / 0.061 / 0.019 / 0.006 /
    0.001`) matches §2.4 point 2 exactly. ~7 s runtime.
- `c-on-ruled-line-population.py` — `percell` and `marginal` rows for all
    four shells match §3.0's table and §5.1's table to 4 significant figures
    (`c_ruled`: 155/105/75/60 mm = 1.1254/1.0608/1.0247/1.0026 `percell`,
    1.0372/0.9568/0.9449/0.9890 `marginal`; `A_eff` 2.048/1.931/1.865/1.825).
    ~2 s.
- `bofr-at-consistent-population.py` — reproduces §3.1's five-row table
    exactly (geo-mean ratios 1.063/0.975/1.046/1.104/0.803, all 11/11 in
    band). ~1 s.
- `bofr-at-resolved-k.py` (retained, superseded) — its `c=1.42` row matches
    the "mixed" row of the current script (`c*k=1.4226`, ratio `0.975`),
    confirming the pre-fix number the document says is withdrawn is exactly
    reproduced by the pre-fix script, not silently changed. ~1 s.
- `k-bin-refinement.py` — 5-bin column (`1.5114/1.3494/1.2053/1.1057` for
    155/105/75/60 mm) matches §1's "1.51/1.35/1.21/1.11", and the
    large-`n_bins` columns bracket "1.74–1.98" as §1 states. ~0.4 s.

All well under the ~30 s retention target.

### 2. Code-path trace — genuine reuse, not re-typed constants

- `c-on-ruled-line-population.py:64` loads `mott-ruled-line-mc.py` via
    `importlib.util.spec_from_file_location` + `exec_module`, then calls
    `mc.run(20.0, n_rings=400, scheme="mott")` and computes
    `K_MC = (XI**2).mean() / XI.mean()**2` from the returned sample array
    (line 95) — `k=1.1375` is **derived from the loaded module's output**,
    not hand-typed. Confirmed by reading the source and by the standalone
    run printing `k_MC = 1.1375` from that exact call path.
- `bofr-at-consistent-population.py:44-53` loads
    `../mass-dependent-fragment-shape/checks/bofr-at-new-mu.py` the same way,
    sets `mod.C_VALUES` to the five `(c, k)` products, and calls `mod.main()`
    — it does not reimplement or re-type the B(r) series; it drives the
    existing committed sweep. Confirmed by reading the source.

### 3. Cited-number verification against primaries

- **Mott 1947 quotes** (§2.2, §2.3, §2.4) — checked against
    `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`.
    Finding (1) ("most of which lie between x₀ and 2x₀ ... about 1.5x₀"),
    the eq.(3)/(4)/(5) formulas, the worked "the increase in σ is unity" step,
    and "the distribution would not be sensibly different for larger values"
    all match the extraction verbatim, at the anchors the derivation cites.
- **One transcription wrinkle, immaterial to the shipped number.** §2.3's
    prose (line 135) and the §4 "Substitution closure, α=1" row write eq.(3)
    as `dn/ds = lfCe^{γs}`. The primary extraction literally prints
    `dn/ds = lfCe^{αs}` (line 154) — using `α`, not `γ` — while eq.(4) and
    Mott's own worked step both print `e^{ασ}` (lines 162, 178), and earlier
    eq.(1) uses `Ce^{γs}` (line 88). Substituting eq.(3) *as literally
    extracted* (`e^{αs}`) through `σ=γs` does **not** algebraically produce
    eq.(4) as literally extracted (`e^{ασ}`) unless `γ≡α`, in which case the
    exponent should reduce to `e^{σ}`, not `e^{ασ}` — the extraction is
    internally inconsistent on this point regardless of which of the two
    documents is read. This looks like a genuine α/γ glyph ambiguity in the
    scanned source (or its OCR/vision extraction), not something either
    document invented; the derivation silently resolves it in `γ`'s favour
    without flagging the ambiguity. It is also the case that the specific
    worked-step check offered as confirmation ("at τ=0, f=1, Δτ=1/(f·e^τ)=1")
    holds trivially at τ=0 for *any* exponent coefficient, so it does not by
    itself discriminate `α=1` from `α≠1`. **Materiality: zero on the shipped
    number.** `k=1.1375` and `κ_x=1.560` are validated empirically against
    Mott's own reported mean (4% agreement) and histogram shape (§2.4 points
    1–2), independent of how the eq.(3)→eq.(4) substitution is read — the MC
    algorithm's `Δτ=1/(f·e^τ)` step is what's actually run, and it is pinned
    to Mott's own worked numeric example either way. **Tag: Note** (raise to
    Deferrable only if the primary's actual typeset PDF, not the OCR/vision
    extraction, is later found to disambiguate α vs γ and it turns out to
    matter for some other derivation reusing this extraction). Suggested
    correction: soften the §4 "derived not assumed" claim to acknowledge the
    extraction's α/γ ambiguity, or verify against `source.pdf` directly.
- **Minor rounding slip, immaterial.** §3.0 (line 263) and §4 (line 347)
    state the reweighted population's `k_pop` range as "1.121–1.144". The
    script's actual `percell` `k_pop` values are 1.1227 (155 mm), 1.1368
    (105 mm), 1.1440 (75 mm), 1.1375 (60 mm) — min 1.1227 rounds to 1.123,
    not 1.121. **Tag: Note.** The stated "~1.5%" closure-check conclusion is
    unaffected either way ((1.1375−1.1227)/1.1375 ≈ 1.3%).
- **§3.0/§3.1 B(r) and §5.1 four-shell tables** — every number checked
    against script output in §1 above; no discrepancies found.

### 4. Cross-document agreement

- `../mott-fragment-shape-closure/derivation.md` §9 A9.1 (lines 337–364) and
    A9.3 (lines 368–375) restate `k=1.1375`, the four `c` values
    (1.1254/1.0608/1.0247/1.0026), `+2.4%`/`+24%` at 155/60 mm, and the
    `κ_x≈1.65x₀`/`~21%` finding — all match `breadth-variance-factor-k/
    derivation.md` exactly. A9.1 is correctly marked **closed**; A9.3 is
    correctly marked **Open blocking finding**, cross-referencing the marker
    at `breadth-variance-factor-k/derivation.md:438`.
- `_limitations.qmd` entry 18 (lines ~665–695) restates the same numbers
    (`1.2506→1.1254`, `2.001→2.048`, `+2.4%`, `+18%`/`+24%`) and correctly
    scopes what remains open (the mass law still descends from the 1943
    exponential) without re-claiming what §9/A9.1 has closed.
- **No stale pre-fix numbers found outside labeled context.** Grepped
    `0.975`, `1.2506`, `1.912` across `experiment/fragmentation-field/**/*.md`
    and `*.qmd`: every hit is either (a) explicitly labeled
    pre-fix/mixed/withdrawn/superseded within `breadth-variance-factor-k/`,
    (b) the `mass-dependent-fragment-shape` update's own historical
    "superseded" row (a different document's own record, correctly labeled,
    out of this pass's scope to alter), or (c) an unrelated quantity in the
    `75mm-fuze-case-mass-fix` thread (a fuze+booster mass in kg that happens
    to share the digits `0.975`/`0.97522`, not the B(r) fit ratio).

### 5. Housekeeping

- `git status --short` shows the new `updates/breadth-variance-factor-k/`
    directory as untracked (expected, not yet committed) and modifications to
    `_limitations.qmd` and `mott-fragment-shape-closure/derivation.md` (the
    fix-cycle-1 cross-document edits, already covered by §4 above). No
    leftover files in `experiment/_scratch/` beyond its permanent `README.md`.
    Unrelated modified/untracked files under `.claude/agent-memory/model-reviewer/`
    and `.claude/agent-memory/modeler/` predate this pass and are not this
    change's concern.
- All five scripts named in `derivation.md` §6's "Scripts retained in
    `checks/`" table exist at the paths given.
- **Pre-existing, non-blocking artifact glitch (not from this pass):**
    `collect-findings.py --for
    experiment/fragmentation-field/updates/breadth-variance-factor-k` reports
    one malformed marker at `review.md:336` — a quoted excerpt in the Pass-1
    re-review prose (naming the marker's tier and text inline, in a form that
    happens to match the collector's loose marker syntax) that is truncated
    with an ellipsis and is not itself a live finding (the real, well-formed
    marker is at `derivation.md:438` and is collected correctly under its own
    scope). **Tag: Note.** No open finding is lost — collection against the
    real marker succeeds — but the false-positive parse noise is worth fixing
    by rewording that sentence in `review.md` to describe the marker instead
    of quoting its literal bracket syntax, so future `collect-findings.py`
    runs on this scope don't report a phantom malformed marker.

### Verdict rationale

No Blocking findings. The check scripts reproduce every cited number exactly,
the two load-bearing reuse paths (`c-on-ruled-line-population.py` →
`mott-ruled-line-mc.py`, `bofr-at-consistent-population.py` →
`../mass-dependent-fragment-shape/checks/bofr-at-new-mu.py`) are genuine
module loads rather than re-typed series, and both sibling documents
(`mott-fragment-shape-closure/derivation.md` §9, `_limitations.qmd` entry 18)
agree with this derivation's numbers with no stale survivors found. The two
items above (the eq.(3)/(4) α/γ transcription wrinkle and the "1.121" rounding
slip) are transcription-level Notes with zero effect on the shipped `k`,
`c`, or `A_eff` values — they do not change any rendered output and do not
rise to Deferrable. **PASS-with-limitations** reflects the standing Blocking
finding already correctly logged and open at `derivation.md:438` (A9.3,
`κ_x`) — which this pass reconfirms is present, well-formed, and not closed
by this document — not any new defect found in this verification pass.

**Not independently re-run in this pass** (time-budget constraint, no
evidence of a problem): the full `Table 3` CSV closure invariant
(`table-3-grady-aspect-ratio-counts.csv`) was not re-checked against
`check-table-invariants.py` here — it was in scope for the
`mass-dependent-fragment-shape` update's own review and is only consumed,
not re-derived, by this pass's scripts.

