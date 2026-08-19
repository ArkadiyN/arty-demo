# Derivation — the breadth-variance factor `k = ⟨x²⟩/⟨x⟩²` (assumption A9.1)

**Pass:** derivation (Workflow B step 3), 2026-08-17. Executes
[`scoping.md`](scoping.md) §5 actions A–F under its §4.1 recommendation
(attempt Option 1, fall back to Option 4).
**Revised 2026-08-17 (fix cycle 1)** against [`review.md`](review.md) Pass 1
findings **B1** (re-tier only) and **B2** (`c` re-solved on the ruled-line
population). §3, §5.1, §5.2, §5.4, §5.5 and §6 below are the post-fix state;
the pre-fix numbers they replace are named where the change is material.

**Outcome (stated up front): Option 1 — `k` is resolved and ships, as a single
caliber-independent `k = 1.14`. But `k` cannot ship alone:** eq. (2) is a
one-population identity, so `c` had to be re-solved on the same ruled-line
population (§3.0). Doing that moves `c` down by roughly as much as `k` moves
the product up, and the net effect on the 155 mm surface is **nil**. What the
change is actually worth is at the small calibers, where `A_eff` rises 16–24 %.

Action A resolved the scoping's three-route inconsistency by *reproducing*
Mott 1947's ruled-line Monte Carlo rather than bounding it verbally (§2.3).
The reproduction validates against Mott's own reported mean (`1.560x₀` vs his
"about `1.5x₀`") and his figure-4 histogram shape, and returns
**`k = 1.1375`** — near the scoping's Route-B expectation but *above* its
`[1.00, 1.11]` support bound, which was too tight because it neglected the
distribution's tail beyond `2x₀`.

Route A (`k = 2`) is **retired**: §2.1 shows it is not an independent Mott
result but the exponential-breadth *assumption* Mott & Linfoot 1943 made
before the release-wave mechanism existed, and Mott 1947's own calculation of
that mechanism contradicts it. The out-of-sample B(r) surface agrees
independently and by a wide margin (§3).

On the 155 mm B(r) surface the population-consistent pair is **indistinguishable
from what ships today** (geo-mean ratio 1.063 → 1.046, method band 1.05–1.10).
The pre-fix version of this document claimed `k = 1.14` *improves* the fit to
0.975; that number came from pairing the 1947 `k` with a `c` weighted on the
1943 spectrum, and it does not survive making the two factors consistent —
review finding **B2**. The claim is **withdrawn**. Disposition in §5.

---

## 1. What this pass does not re-derive

Cited from [`scoping.md`](scoping.md) §2, closed there:

- `c` and `k` are exact orthogonal factors of one identity — no double-count
    (`../mass-dependent-fragment-shape/derivation.md` §2.1, verified in its
    `review.md`).
- `k` and the shipped break-up-velocity item **C2** cannot double-count; `A`
    enters only via `alpha = A·κx²·t_bu/x0` while C2 acts on `x0 ∝ 1/v_bu`
    ("algebraically disjoint factors of the same product",
    `../mass-dependent-fragment-shape/review.md`). **A9.1's stated deferral
    rationale in `../mott-fragment-shape-closure/derivation.md` §9 is
    therefore void** — action E below.
- The per-shell 5-bin `k` values (1.51/1.35/1.21/1.11) are a discretization
    artefact of the Mott spectrum, converging to 1.74–1.98 and *reversing*
    their caliber trend ([`scoping.md`](scoping.md) §6,
    [`checks/k-bin-refinement.py`](checks/k-bin-refinement.py)). Option 2 is
    dead. Not revisited.

---

## 2. Action A — Mott's breadth distribution, settled from the primaries

The scoping framed this as two rival readings of Mott of equal standing. They
are not. One (1943) is a **stated modelling assumption**, adopted for
mathematical convenience *before* the release-wave mechanism was worked out;
the other (1947) is the **computed output of that mechanism**. Where they
disagree, the later paper is the primary and the earlier is superseded — and
they do disagree, by the factor `k` is precisely a measure of.

### 2.1 Mott & Linfoot 1943 §3 states the breadth law explicitly

> "The analysis will be appropriate if a shell casing is broken up by cracks
> parallel to the axis at an average distance, say, x₀ apart, and the lengths
> have an average value y₀ independent of the breadth … **the number with
> breadths between x and x + dx is proportional to exp(−x/x₀)dx**"

`doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/quotes.md`,
anchor `p. 4 — §3, the ruled-line model: breadth and length are independent`.

This is the **breadth** distribution, named as such, in the source that
supplies the shipped mass law. Exponential ⇒ `⟨x²⟩/⟨x⟩² = 2` exactly, for
every scale and therefore every caliber.

This identifies what Route A actually is. `k = 2` is **not** an independent
result that the mass spectrum `N(≥m) = N₀e^{−√(m/μ)}` happens to corroborate:
it is the *premise* Mott & Linfoot assumed in order to derive that spectrum.
Route A and the shipped mass law are one assumption counted twice, so their
agreement is vacuous — it carries no evidential weight about the real breadth
distribution.

Note also the surrounding text: the exponential is introduced with "the
lengths have an average value `y₀` **independent of the breadth** and are
distributed according to **the usual law**". "The usual law" is a citation to
the crushing/comminution literature (Lienau 1936, cited in the same
paragraph), i.e. an imported convention, not a derivation from the shell
mechanics. §3 of that paper is a *mathematical* discussion — its object is to
get a closed-form area distribution (the Bessel `zK₀(z)` result on p. 4), for
which exponentials are the tractable choice.

### 2.2 Mott 1947's ruled line supersedes it, and its second moment is recoverable

`κ_x = 1.5` comes from Mott 1947 finding (1) (`rspa.1947.0042.md`, anchor
`The fragments have lengths most of which lie`). The scoping read "lengths
mostly in `x₀…2x₀`, average 1.5x₀" as a *tight* distribution and inferred
`k ∈ [1.00, 1.11]`. Two things break that inference:

1. **`x₀` in the 1947 paper is not the mean breadth.** It is the release-wave
    length scale `x₀ = (2P_y/ρv)^{1/2} r/v` (eq. (5) preamble), i.e. the
    *shielding radius per unit √σ*. Mott states only that it is "on
    dimensional grounds obviously proportional to the average fragment
    length"; finding (1) is what fixes the constant of proportionality at
    ~1.5. So `x₀` is a **model parameter, not a distribution mean**, and
    "most lie between x₀ and 2x₀" is *not* a support statement of the form
    the scoping's two-point extremum argument requires.
1. **The 1947 histogram is a Monte-Carlo *output* whose second moment can be
    recomputed**, and Mott's procedure is fully specified in the text. §2.3
    does exactly that, rather than bounding it from a verbal description.

### 2.3 Reproducing Mott's ruled-line Monte Carlo

Algorithm as stated (`rspa.1947.0042.md` p. 304–305). With `σ = γs`, eq. (4)
normalised by `(lC/γ)e^{σ₀} = 1` and `τ ≡ σ − σ₀`, the model is scale-free:

| Element | Mott's text | Scaled form used |
| ------- | ----------- | ---------------- |
| nucleation rate | `dn/dσ = (lfC/γ)e^{ασ}` (4) | `dn/dτ = f e^{τ}`; per unit *unshielded* length, `e^{τ}/l` |
| release zone half-width | `x₀(σ − σ₁)^{1/2}` (5) | `√(τ − τ_j)`, in units `x₀ = 1` |
| first crack | at `σ₀`, i.e. when expected count = 1 | `τ = 0` |
| step rule | "the increase in σ is unity" then `Δσ = 1/(fCe^{ασ})` | `Δτ = 1/(f e^{τ})` |
| ring | `l = 20 x₀`, "would not be sensibly different for larger values" | periodic, `l/x₀ ∈ {20, 50, 200}` |
| stop | "repeated until the whole line was covered" | `f = 0` |
| fragments | "lengths of the intervals between adjacent cuts" | gaps between consecutive cuts |

`α = 1` in `σ`-units: eq. (3) is `dn/ds = lfCe^{γs}` and `σ = γs`, which is
also what makes Mott's own worked step "the increase in σ is unity" come out
right (at `τ=0`, `f=1`, `Δτ = 1/1 = 1`, so the second cut's neighbour zone is
`x₀√1 = x₀` — exactly the width Mott marks off).

Script: [`checks/mott-ruled-line-mc.py`](checks/mott-ruled-line-mc.py).
Two independent implementations of the nucleation step are run — Mott's
deterministic `Δτ = 1/(f e^τ)` increment, and an exact inhomogeneous-Poisson
thinning — as a cross-check that the answer is Mott's model and not Mott's
quadrature.

### 2.4 Results

Run 2026-08-17, ~20 s. Lengths in units of `x₀`; `n` = fragments sampled.

| scheme | `l/x₀` | `⟨x⟩/x₀` | `⟨x²⟩/x₀²` | **`k`** | frac. in `[x₀, 2x₀]` |
| ------ | ------ | -------- | ---------- | ------- | -------------------- |
| Mott (deterministic `Δτ`) | **20** | **1.5604** | 2.7694 | **1.1375** ± 0.0028 | 0.600 |
| Mott | 50 | 1.6005 | 2.9732 | 1.1607 ± 0.0030 | 0.559 |
| Mott | 200 | 1.6444 | 3.1910 | 1.1801 ± 0.0014 | 0.525 |
| exact Poisson | 20 | 1.6430 | 3.1793 | 1.1777 ± 0.0036 | 0.528 |
| exact Poisson | 50 | 1.6472 | 3.2347 | 1.1922 ± 0.0035 | 0.507 |
| exact Poisson | 200 | 1.6694 | 3.3313 | 1.1954 ± 0.0018 | 0.501 |

**Validation against Mott's own reported outputs** — the row in bold is
Mott's exact configuration (`l/x₀ = 20`, his own deterministic `Δσ` step):

1. **Mean.** `⟨x⟩ = 1.560 x₀` against Mott's finding (1) "the average length
    is about `1.5x₀`" — 4 % agreement on a hand-drawn 1947 histogram. ✓
1. **Shape.** The 0.4`x₀`-binned histogram (Mott's own bin width, "between
    `0.4x₀` and `0.8x₀`, and so on") comes out `0.000 / 0.083 / 0.217 /
    0.262 / 0.215 / 0.137 / 0.061 / 0.019 / 0.006 / 0.001` over `0–4x₀`:
    **zero density in the first bin**, single interior mode at `1.2–1.6x₀`,
    60 % of fragments inside `[x₀, 2x₀]`. That is finding (1)'s "most of which
    lie between `x₀` and `2x₀`" reproduced as a shape, not just as a mean. ✓
1. **Not exponential.** An exponential has its mode at 0 and 63 % of its mass
    *below* the mean; the ruled-line distribution has **negligible** mass below
    `0.4x₀`, because a crack is unlikely to nucleate inside a neighbour's
    release zone. (Not a hard support cutoff: the release-zone half-width
    `√(τ − τ_j)` is zero at the instant a crack nucleates, so the gap density
    near 0 is positive-but-vanishing, and the MC's empty first bin is a
    resolution statement at the sampled `n`. The physical contrast with an
    exponential, whose mode is *at* 0, is unaffected.) This is the physical
    content that 1943's "usual law" omits, and it is exactly what suppresses
    `k` from 2 to ~1.14.

**`k` from the same object that yields `κ_x = 1.5`: `k = 1.1375`.**

**Which row to adopt.** `κ_x` and `k` are the first and second moments of one
distribution, so they must be taken from **one** configuration. Mott's
`l/x₀ = 20` row is the one whose first moment *is* the shipped `κ_x = 1.5`
(1.560, rounded by Mott to 1.5); adopting `k` from the converged `l/x₀ = 200`
row while keeping `κ_x` from `l/x₀ = 20` would mix configurations. So
**`k = 1.14`** ships, with the `l/x₀` and quadrature spread `[1.14, 1.20]`
carried as its uncertainty band — 5 % wide, comfortably inside the ±15 %
fidelity target.

**Finite-size caveat, logged not acted on.** Mott's "the distribution would
not be sensibly different for larger values [of `l/x₀`]" is *approximately*
true for `k` (1.138 → 1.180, +4 %) but less so for the mean (1.560 → 1.644,
+5 %); and his deterministic `Δτ` step is itself a small bias (at `l/x₀ = 20`
it gives 1.560/1.138 where exact Poisson gives 1.643/1.178). Real shells sit
at `l/x₀ = 2πr/x₀ ≈ 50–200`, not 20. The converged pair is therefore
`(κ_x, k) ≈ (1.67, 1.20)`, i.e. **the shipped `κ_x = 1.5` may itself be ~10 %
low**, worth ~21 % on `μ` since `μ ∝ κ_x²`. That is a finding against **A9.3**,
not against `k`, and it is out of scope here — see the marker in §5.3.

---
## 3. `c` on the same population, and what the pair does to B(r)

### 3.0 Why `c` had to move (review finding B2)

`../mass-dependent-fragment-shape/derivation.md` eq. (2),
`⟨Ax²⟩/(⟨A⟩⟨x⟩²) = c·k`, is exact **for one distribution** — every `⟨·⟩` in it
runs over the same population. The shipped `c = 1.2506` is not a raw Table-3
statistic: it is a **`μ`-weighted** moment, Table 3 re-weighted by the shell's
own Mott spectrum `N(≥m) = N₀e^{−√(m/μ)}` and solved as the fixed point
`μ = c·μ₀` (that update's review finding A1, which forced the per-shell
rebuild). Its weighting population is therefore the **1943-descended mass
spectrum**. `k = 1.1375` is a moment of the **1947 ruled line**. Pairing them
is not the identity; and because `c − 1 = Cov(A, x²)/(⟨A⟩⟨x²⟩)` is a
*normalised* covariance, it is a functional of the spread of `x²` in whichever
population it is averaged over — so the swap moves `c`, necessarily, toward 1.

**Re-solve.** [`checks/c-on-ruled-line-population.py`](checks/c-on-ruled-line-population.py)
re-runs the shipped construction with exactly one substitution: the mass-group
weight comes from the ruled-line breadth marginal (`x` sampled from
[`checks/mott-ruled-line-mc.py`](checks/mott-ruled-line-mc.py), not re-derived)
instead of from the Mott spectrum. Mechanics:

- a fragment is `(A, x)` with `m = S·A·x²`, `S = ρt x₀²` the one unknown mass
    scale [grains], so a Table-3 cell (group `g`, aspect bin `A`) *is* the
    breadth interval `x/x₀ ∈ [√(lo_g/(A S)), √(hi_g/(A S))]`;
- Table 3 keeps supplying the **conditional aspect mix `A|g`** — the one input
    the prior update established transfers across calibers — and Mott 1947
    supplies the **breadth marginal**;
- cell moments are the ruled-line moments *truncated* to that interval, so the
    5-group mass axis stops being a resolution floor (it was: with point-mass
    group representatives the 60 mm shell has no reachable mean);
- `S` is fixed by the closure's own mean-mass identity `⟨m⟩ = 2μ`, and `μ` by
    the fixed point **`μ = c·k·μ₀`** — note the `k`, which the shipped fixed
    point `μ = c·μ₀` omits.

**Two weighting closures, reported as a band.** Table 3's conditional `A|m` and
Mott's breadth marginal *over-determine* the joint, so the reconstruction is not
unique. Two natural closures bracket it:

| closure | group weight | `c₁₅₅` |
| ------- | ------------ | ------ |
| **`percell`** (adopted) | ruled-line probability of the cell's *own* bracket, `P(A\|g)·P_ruled(m∈g \| A)` | **1.1254** |
| `marginal` | aspect marginalised out first, so the group weight is `A`-independent exactly as in the shipped script | 1.0372 |

`percell` is adopted because `m = S·A·x²` is a kinematic identity, not a
modelling choice: at fixed breadth a 4:1 fragment *is* four times the mass of a
1:1 one, so which mass bracket a cell falls in genuinely depends on its aspect.
`marginal` discards that dependence and is carried as the low end of the method
band. Neither is exact; the spread is the honest uncertainty and it is **larger
than the ±0.6–3.6 % method band** the shipped `c` carries (that band sweeps the
Table-3 mass axis at *fixed* spectrum family, not a change of population).

| shell | `c` shipped (1943 spectrum) | `c` ruled line, `percell` | band (`marginal`) | `k` | `A_eff = 1.6·c·k` | `A_eff` shipped |
| ----- | ------- | ------ | ------ | --- | ------ | ------ |
| 155 mm M107 | 1.2506 | **1.1254** | 1.0372 | 1.1375 | **2.048** [1.888] | 2.001 |
| 105 mm M1 | 1.1024 | **1.0608** | 0.9568 | 1.1375 | **1.931** [1.741] | 1.764 |
| 75 mm M48 | 0.9854 | **1.0247** | 0.9449 | 1.1375 | **1.865** [1.720] | 1.577 |
| 60 mm M49A2 | 0.9200 | **1.0026** | 0.9890 | 1.1375 | **1.825** [1.800] | 1.472 |

**Closure check on the reconstruction.** The reweighted cell population's own
`k_pop = ⟨x²⟩/⟨x⟩²` comes out 1.121–1.144 (`percell`) against the MC's
`k = 1.1375` — i.e. the construction reproduces the breadth marginal it was
given to within ~1.5 %, which is the residual of the 5-group discretisation.
Under the pre-fix (spectrum-weighted) population the same statistic was 1.51 at
155 mm. That gap **is** finding B2, measured.

**Two structural consequences, both reported as they came out.**

1. **`c`'s caliber trend nearly collapses.** Shipped `c` falls 1.25 → 0.92
    across the four shells; on the ruled-line population it is 1.13 → 1.00,
    and never drops below 1. The shipped sub-unity values at 75/60 mm were the
    AM–HM floor `1/(⟨A⟩⟨1/A⟩) = 0.835` taking over once ~90 % of the spectrum
    weight sits inside Group 0 — the same coarse-axis collapse `scoping.md` §6
    diagnosed for the per-shell `k`. On the ruled line, cells within one group
    are resolved by their differing breadth brackets, so the covariance does not
    collapse and `c ≥ 1` as a positive `A`–`m` correlation requires.
1. **The change's value moves from 155 mm to the small calibers.** `A_eff`
    moves +2.4 % at 155 mm but +9.4 / +18.3 / +24.0 % at 105 / 75 / 60 mm.

### 3.1 Action C — the 155 mm B(r) surface

Run 2026-08-17,
[`checks/bofr-at-consistent-population.py`](checks/bofr-at-consistent-population.py),
which re-runs the committed sweep
`../mass-dependent-fragment-shape/checks/bofr-at-new-mu.py` unmodified with
`C_VALUES = c·k` for each `(c, k)` **pair**, against the same `drag-gap-1944`
Table 59 casualty card. The pre-fix
[`checks/bofr-at-resolved-k.py`](checks/bofr-at-resolved-k.py) is retained but
superseded: it varied `k` at a frozen `c = 1.2506`, which is the mixed pair.

| population for **both** moments | `c₁₅₅` | `k` | `A_eff = 1.6·c·k` | geo-mean `B_model/B_card` | in 0.5–2× band |
| ------------------------------- | ------ | --- | ----------------- | ------------------------- | -------------- |
| shipped today (A9.1 open, `k = 1`) | 1.2506 | 1.00 | 2.001 | 1.063 (+6.3 %) | 11/11 |
| **1947 ruled line, `percell`** | **1.1254** | **1.1375** | **2.048** | **1.046 (+4.6 %)** | **11/11** |
| 1947 ruled line, `marginal` | 1.0372 | 1.1375 | 1.888 | 1.104 (+10.4 %) | 11/11 |
| *mixed — what the pre-fix pass shipped* | *1.2506* | *1.1375* | *2.276* | *0.975* | *11/11* |
| 1943 spectrum, both moments | 1.2404 | 1.5114 | 3.000 | 0.803 (−20 %) | 11/11 |

Three things follow, two of them different from the pre-fix version.

1. **The resolved pair is a null on this surface — there is no improvement to
    claim.** 1.063 → 1.046 is a 1.6 % move on a quantity whose method band here
    is ±6 %. The "`k` improves the fit, there is no trade" headline is
    **withdrawn**; the honest statement is *the 155 mm surface cannot see this
    change*. It equally cannot be offered as corroboration of the value — the
    row that hits 0.975 is the only row that averages its two factors over
    different populations, which is precisely why it hits.
1. **This is still not a fit, and still does not trip
    `gotcha_rebaseline_onto_validation_source`.** `k = 1.1375` is computed from
    Mott's 1947 procedure and `c` from Table 3's aspect mix, neither with any
    reference to the casualty card. The card was free to reject the pair and did
    not — but "did not reject" is now the whole of the claim.
1. **Route A is still independently rejected out of sample, and now
    self-consistently.** The bottom row is the 1943 population supplying *both*
    moments (`c = 1.2404`, `k = 1.5114`, both from
    `../mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py`),
    so it is an apples-to-apples comparison the pre-fix table did not make: it
    misses by −20 %, against +4.6 % for the 1947 pair. And 1.5114 is itself the
    5-bin discretised value; at the bin-converged `k = 1.74–1.98`
    ([`scoping.md`](scoping.md) §6) that row would sit at `A_eff ≈ 3.5–3.9` and
    miss further. Combined with §2.1 (an imported convention, superseded by the
    same author four years later), Route A is retired on two independent
    grounds. **This is the surviving out-of-sample result of the pass.**

**Tilt vs level.** The normalised `B(r)/B(r₀)` rows are identical to three
decimals across `k = 1.25 → 1.50` (`1.000 0.431 0.236 0.099 …`), so `k` acts
as a near-pure **level** shift on B(r) and does not re-tilt the range
dependence. Consistent with `k` entering only through `μ`, and it means the
B(r) evidence here is about magnitude, which is exactly the quantity `k`
claims to correct.

---

## 4. Unit and limit checks

| Check | Expectation | Result |
| ----- | ----------- | ------ |
| **Dimensions** | `k = ⟨x²⟩/⟨x⟩²` is a ratio of a length² to a length² | dimensionless ✓ |
| **Jensen floor** | `k > 1` strictly for any non-degenerate breadth distribution | 1.1375 > 1 ✓ |
| **Degenerate limit** | all fragments identical ⇒ `k → 1` | as `l/x₀ → 0` only one cut fits, gap distribution collapses ✓ (not swept; structural) |
| **Exponential limit** | if the release zone is switched off (`x₀ → 0`), cuts become a Poisson process and gaps become `Exp` ⇒ `k → 2` | recovers Route A as the *no-shielding* limit — confirms the two routes differ by exactly the release-wave physics ✓ |
| **Scale-freeness** | Mott's model in `τ`-units has no caliber-dependent parameter, so `k` is caliber-independent | one `k` for all four shells ✓ (§5.1) |
| **Reproduction closure** | the MC's own first moment must equal the independently-shipped `κ_x` | 1.560 vs Mott's stated 1.5 ✓ (4 %) |
| **Identity closure (one population)** | eq. (2) `⟨Ax²⟩/(⟨A⟩⟨x⟩²) = c·k` is exact only when both moments run over one population | enforced by re-solving `c` on the ruled line (§3.0) ✓ |
| **Marginal-reproduction closure** | the reweighted Table-3 cell population must reproduce the breadth marginal it was given: `k_pop ≈ k_MC` | 1.121–1.144 vs 1.1375, ~1.5 % ✓ (§3.0) |
| **Substitution closure, `α = 1`** | eq. (3) `dn/ds = lfCe^{γs}` with `σ = γs` gives `dn/dσ = (lfC/γ)e^{σ}` by substitution, so `α = 1` is derived not assumed | matches Mott's own worked "the increase in σ is unity" step ✓ (§2.3) |
| **Order of magnitude on `μ`** | the pair `(c, k)` re-solved together raises `μ` by 2.4 % at 155 mm, 24 % at 60 mm | 155 mm inside the ±15 % fidelity target; 60 mm outside it, and that is the change's real content (§3.0) |

---

## 5. Disposition

### 5.1 What ships — Option 1

**The `(c, k)` pair ships together, not `k` alone.** `k = 1.1375` (one
caliber-independent value) and a **re-solved per-shell `c`**, applied the way
`c` already is — as a multiplier on the registry's `aspect_ratio`, so
`A_eff = 1.6·c(shell)·k`.

| shell | `c` (re-solved, `percell`) | `k` | `A_eff = 1.6·c·k` | vs shipped `A_eff` | Δ |
| ----- | ------------- | --- | ----------------- | ------------------ | - |
| 155 mm M107 | 1.1254 | 1.1375 | 2.048 | 2.001 | +2.4 % |
| 105 mm M1 | 1.0608 | 1.1375 | 1.931 | 1.764 | +9.4 % |
| 75 mm M48 | 1.0247 | 1.1375 | 1.865 | 1.577 | +18.3 % |
| 60 mm M49A2 | 1.0026 | 1.1375 | 1.825 | 1.472 | +24.0 % |

**Scope note — this exceeds A9.1.** A9.1 is the assumption `k = 1`; resolving
it is Option 1 and that part is unchanged. But the one-population identity
(§3.0) means the shipped `MOTT_ASPECT_MOMENT_C` table — owned by the
`mass-dependent-fragment-shape` update, not by this one — **must be replaced in
the same edit**. Shipping `k` on top of the existing `c` is exactly the mixed
pair review finding B2 rejects, so there is no smaller consistent change. The
`src/arty/` pass should touch both constants or neither.

**Caliber-independent, and this is a derived result, not a simplification.**
Mott's ruled-line model in scaled `τ`-units contains no caliber-dependent
parameter — `x₀` is the only scale and it divides out of a moment *ratio*.
Whatever caliber dependence the breadth statistic appears to have in the
Table-3 evaluation is the discretization artefact
([`scoping.md`](scoping.md) §6). **The scoping's "one `k` for all shells is
defensible in a way one `c` was not" is upheld, for a stronger reason than it
gave:** not that the spread is small, but that the model generating `k` has no
caliber input at all.

**Not shipped in this pass** — this is a derivation pass; the `src/arty/`
edit (`MOTT_BREADTH_VARIANCE_K` alongside `MOTT_ASPECT_MOMENT_C` in
`arty.fragmentation`, consumed by `mott_aspect_ratio`) is the next pass.

### 5.2 The `c·k` identity — what it does and does not mean

`../mass-dependent-fragment-shape/derivation.md` eq. (2) is exact:
`⟨Ax²⟩/(⟨A⟩⟨x⟩²) = c·k`. Its raw Table-3-count evaluation gives `c·k = 1.912`;
the spectrum-weighted 155 mm evaluation gives `1.2404 × 1.5114 = 1.875`. What
ships here is `1.1254 × 1.1375 = 1.280`.

**The pre-fix version of this section defended taking `c` and `k` from
different populations. That defence was wrong and is withdrawn** (review B2).
Its argument was that Table 3 "does not measure the breadth distribution", so
its apparent `k` may be discarded while its `c` is kept. That is true of the
*numerator* of `c` and false of its *weighting*: `c − 1 = Cov(A,x²)/(⟨A⟩⟨x²⟩)`
is a normalised covariance, hence a functional of the spread of `x²` in the
population it is averaged over. The two populations differ in exactly that
spread — `CV_x = √(k−1)` is 0.37 for the ruled line against ~0.71 for the
spectrum-weighted Table 3 (`k = 1.5114`) — so `c` moves when the population is
swapped, and it did: 1.2506 → 1.1254 at 155 mm.

What survives, and is the whole content of the change:

- `A|m`, the **conditional aspect mix**, is what Table 3 measures directly and
    well, and it is the only Table-3 input retained (§3.0). This is the same
    input the prior update showed transfers across calibers.
- The **weighting population** for both moments is now Mott 1947's ruled line,
    not the 1943-descended spectrum. `k` and `c` are moments of one object.

**The identity still holds; what changed is which distribution supplies every
`⟨·⟩` in it.** Anyone re-checking eq. (2) against the raw Table-3 counts will
still get 1.912 and should — that check tests the algebra, not the physics
input.

### 5.3 Out-of-scope finding raised, not fixed

§2.4's converged rows put Mott's own model at `⟨x⟩ ≈ 1.65x₀` in the
`l/x₀ = 50–200` regime real shells occupy, against the shipped `κ_x = 1.5`
read off his `l/x₀ = 20` demonstration. Since `μ ∝ κ_x²`, that is ~21 % on
`μ` — **an order larger than the +2.4 % this change ships at 155 mm**. It
belongs to **A9.3**, not A9.1, and no physics is changed here.

Review finding **B1** re-tiers it: the marker names shipped `src/arty/` code
resting on a number this pass has itself shown to be wrong, which
`.claude/rules/deferred-findings.md` says an agent may not close by deferral.
It is therefore `blocking` below, and stays blocking until `κ_x` is re-derived
or a human elects to defer. On this change's own §3.1 sensitivity a 21 % `μ`
rise moves the 155 mm geo-mean ratio 1.046 → ≈0.93 — outside the ±15 %
fidelity target and, again, larger than what this change ships.

**CLOSED 2026-08-19** — the blocking `FINDING` marker that stood here is
deleted: `src/arty/` now ships `κ_x = 1.62` (with the re-solved `k` and `c` of
the same population) from
[`../kappa-x-shell-regime/derivation.md`](../kappa-x-shell-regime/derivation.md)
§6.1, measured at the fleet's own regime `l/x₀ = 95` rather than at Mott's
`l/x₀ = 20` demonstration. The realised move is `μ` ×1.21–1.23, `N₀` ×0.81–0.83
(that change's §5.1) — close to the ~21 % this section estimated. The 155 mm
`B(r)` geo-mean ratio went 1.046 → 0.909, i.e. the fit crosses from +4.6 % to
−9.1 % and stays 11/11 inside the acceptance band (§5.2 there).

### 5.4 Effect on the open threads — stated, not claimed as a closure

- **`drag-gap-1944` (155 mm B(r))**: **no measurable change**, 1.063 → 1.046
    (method band 1.05–1.10). §3.1. The pre-fix "improves to 0.975" is
    withdrawn — that thread gains nothing from this change and loses nothing.
- **`count-gap-1938` (75 mm counts)**: the estimate **grows** relative to the
    pre-fix version, because at 75 mm the pair moves `A_eff` +18.3 % (not the
    +14 % `k` alone gave). `μ` up ~18 %, `N₀` down ~15 %, moving the arms from
    ~2.54×/2.28× to roughly ~2.15×/1.93×. **Still FAIL on both arms.** This is
    the honest result and is stated as one. Per
    [`scoping.md`](scoping.md) §4.1 that thread's 75 mm residual has already
    been shown not to be a shape-moment artefact, and `k` should not be
    recruited to close it. Not re-run this pass — the count chain re-solves as
    `N`, not as `1/f` (memory `gotcha_mott_count_not_f_squared`), so the
    figures above are indicative and the fix pass should re-run
    `../mass-dependent-fragment-shape/checks/aspect-ratio-moment-leverage.py`
    rather than scale.

### 5.5 Assumptions logged

| # | Assumption | Basis / risk |
| - | ---------- | ------------ |
| K1 | Mott 1947's ruled-line distribution, not M&L 1943's exponential, is the model's breadth distribution | Later primary, and the one `κ_x` already comes from. Risk: the shipped mass law `N(≥m) = N₀e^{−√(m/μ)}` descends from the 1943 exponential, so the closure now takes its first two breadth moments from 1947 and its mass *law* from 1943. See `_limitations.qmd` (action F) |
| K2 | `k` is caliber-independent | Derived (§5.1), not assumed — Mott's model has no caliber parameter in scaled units |
| K3 | `(κ_x, k)` taken from Mott's `l/x₀ = 20` configuration, not the converged one | §2.4. The consistency being preserved is with the **shipped legacy constant** `κ_x = 1.5`, **not** with the physically applicable configuration — real shells sit at `l/x₀ = 50–200`, whose internally consistent pair is `(κ_x, k) = (1.67, 1.20)`. Both configuration choices (`l/x₀ = 20`, and Mott's deterministic `Δτ` over exact Poisson) push `k` to the low end of the computed range `[1.14, 1.20]`. Costs ~4 % on `k`; the ~10 % on `κ_x` was the blocking finding in §5.3. **SUPERSEDED (partially), 2026-08-19** — `../kappa-x-shell-regime/derivation.md` §3.1 / assumption X3 splits K3 in two and closes only one half. **Regime half: met.** The applicable configuration is no longer assumed but *measured*: the shipped fleet sits at `l/x₀ = 84–100` (not the verbal 50–200), and `src/arty/` now ships the triple solved at `l/x₀ = 95` — `(κ_x, k) = (1.62, 1.1711)` with the matching per-shell `c`. **Quadrature half: declined.** Mott's deterministic `Δτ` step is retained over exact Poisson thinning on **attributability, not physics** — the whole shipped constant family was solved on that population, so moving regime and scheme together would confound them. K3's `(1.67, 1.20)` pair is the Poisson high edge; the residual is carried as the one-sided band `κ_x ∈ [1.62, 1.67]` (+6.5 % on `μ`), whose downstream numbers are pre-tabulated there so a reversal needs no re-run. Note K3's `k = 1.20` is itself ~1 % high: the Poisson runs at `l/x₀ = 95` give `k ≈ 1.189` |
| K5 | The reconstruction of the joint `(A, x)` distribution is not unique — Table 3's conditional `A|m` and Mott's breadth marginal over-determine it | §3.0. Bracketed by two closures (`percell` adopted, `marginal` low end): `c₁₅₅ ∈ [1.037, 1.125]`, `A_eff ∈ [1.888, 2.048]`. This band is wider than the ±0.6–3.6 % method band the shipped `c` carries, and it **straddles** the shipped `A_eff = 2.001` — which is why §3.1 reports a null rather than a correction at 155 mm |
| K6 | `S = ρt x₀²` is fixed by the mean-mass identity `⟨m⟩ = 2μ`, not from `x₀` directly | §3.0. Consequence: the reweighted population's own first moment is `⟨x⟩ = 1.60 x₀` rather than the MC's 1.5604 (a ~2.5 % reweighting distortion). Anchoring on `x₀` instead would import the `κ_x` defect of §5.3 into `c`; the mean-mass anchor is the one the shipped fixed point already uses |
| K4 | Fragment breadth is the circumferential dimension; Mott's "lengths of the intervals" on the ruled circumference are breadths in the closure's sense | Mott rules the line to "represent the circumference of the cylinder"; M&L 1943 §3 names the same axial-crack spacing "breadth" |

---

## 6. Pass record — actions A–F

| Action ([`scoping.md`](scoping.md) §5) | Status |
| -------------------------------------- | ------ |
| **A** settle Mott's breadth distribution | **Done, §2.** Resolved by reproducing the 1947 ruled-line MC, not by bounding it verbally. @librarian **not** needed — both primaries were already retained and sufficient |
| **B** bin refinement | Already done in scoping §6; not revisited |
| **C** re-run `bofr-at-new-mu.py` at the chosen `k` | **Done, §3.1**, via [`checks/bofr-at-consistent-population.py`](checks/bofr-at-consistent-population.py), which sweeps `(c, k)` *pairs*. [`checks/bofr-at-resolved-k.py`](checks/bofr-at-resolved-k.py) (fixed `c`, swept `k`) is retained but superseded — it evaluates the mixed pair |
| **D′** *(added, fix cycle 1)* re-solve `c` on the ruled-line population | **Done, §3.0**, via [`checks/c-on-ruled-line-population.py`](checks/c-on-ruled-line-population.py). Not in the scoping's action list — forced by [`review.md`](review.md) B2 |
| **D** do not re-derive `c`/`k` orthogonality or C2 | Cited only, §1 |
| **E** strike A9.1's void double-count rationale | **Done** — `../mott-fragment-shape-closure/derivation.md` §9 A9.1 rewritten; the assumption is now marked **closed**, not deferred |
| **F** `_limitations.qmd` entry | **Done** — entry **18**, `experiment/fragmentation-field/_limitations.qmd`. Note it supersedes the scoping's framing: the two-Mott-distributions question is *resolved* for the breadth moments; what is logged as open is the narrower residue that the shipped **mass law** still descends from the retired 1943 exponential |

### Scripts retained in `checks/`

| Script | Produces |
| ------ | -------- |
| `k-bin-refinement.py` | scoping §6 convergence table (pre-existing, re-used unchanged) |
| `mott-ruled-line-mc.py` | §2.4 moment table and figure-4 histogram |
| `c-on-ruled-line-population.py` | §3.0 re-solved `c` table and the `percell`/`marginal` band |
| `bofr-at-consistent-population.py` | §3.1 B(r) table |
| `bofr-at-resolved-k.py` | pre-fix §3 B(r) table (mixed pair); retained, superseded |

### Next pass (`src/arty/`)

Ship the **pair** (§5.1 scope note — `k` alone would re-create the mixed
population):

1. `MOTT_BREADTH_VARIANCE_K = 1.1375` in `arty.fragmentation`, next to
    `MOTT_ASPECT_MOMENT_C`, folded into `mott_aspect_ratio()` so
    `A_eff = 1.6·c(shell)·k`.
1. `MOTT_ASPECT_MOMENT_C` **replaced** with the ruled-line-population values —
    155 mm 1.1254, 105 mm 1.0608, 75 mm 1.0247, 60 mm 1.0026 — and its long
    docstring rewritten: the weighting population is Mott 1947's ruled line,
    the fixed point is `μ = c·k·μ₀`, and the caliber trend (`c` falling through
    1 near 75 mm) is **gone** — that trend was the Group-0 AM–HM collapse, §3.0.
1. The four `aspect_ratio=` comments in `arty.shells` (§5.1 table).

Then re-run the `count-gap-1938` chain properly (§5.4) rather than relying on
this pass's indicative scaling, and re-run the `drag-gap-1944` thread's own
numbers — it moves 1.063 → 1.046, i.e. nothing, so its verdict does not change.

**Blocked-on note for whoever picks that pass up:** §5.3's `κ_x` finding is
`blocking` and is ~10× the size of what ships here. Landing this change does not
make the closure right; it makes it self-consistent.
