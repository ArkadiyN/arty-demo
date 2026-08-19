# Review — `κ_x` at the shell's own ruled-line regime

## Pass 1 — adversarial critique (2026-08-18, @model-reviewer, Opus)

Scope: `derivation.md` (Workflow B step 3) against `scoping.md`, the prior
`breadth-variance-factor-k` and `mott-fragment-shape-closure` derivations, the
four cited check scripts, and Mott 1947 itself
(`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`).
`src/arty/` is out of scope by brief (next pass).

Open-findings register at pass start
(`collect-findings.py --for experiment/fragmentation-field/updates/kappa-x-shell-regime`):
**no open findings** on this scope. The upstream blocking marker this change
closes (`breadth-variance-factor-k/derivation.md:438`) is correctly left in
place pending the `src/arty/` pass (§6.4) — that is the right disposition.

**Verdict: FAIL** — two Blocking findings. Both are closable by text changes
plus one finding marker; **no Monte Carlo re-run is required** and no adopted
number is shown to be arithmetically wrong.

What holds up, stated first, because most of it does:

- The `Λ` derivation (§1 eq. 2) is correct and the `r_bu` cancellation is
    genuinely *derived*, not assumed. Dimensions check: `√(2σ_f/ργ')` is
    Pa·m³/kg → m²/s² → m/s, so `Λ = 2πv_bu/√(2σ_f/ργ')` is dimensionless. I
    reproduced §2's table arithmetically for all four shells (e.g. 155 mm:
    2π·975.6/61.15 = 100.2; 60 mm: 2π·988.9/65.85 = 94.4). The caliber-
    independence claim (X2) is earned.
- The "one population, three moments" constraint from §1 **is** carried into
    §4.1 — and §4.1 finds a second-order coupling (`μ₀` inside the `c` closure)
    that scoping did not name, sizes it at ≤0.8 %, and closes it self-
    consistently. That is the correct instinct and it is the strongest part of
    the pass.
- `c-at-fleet-regime.py` reads Table 3 from
    `doc-reference/fragmentation/explosion-fragment-model/tables/table-3-grady-aspect-ratio-counts.csv`,
    not a hand-typed literal array, and that table's invariant passes
    (`check-table-invariants.py … --all` → 0/3 failed). Criterion match on the
    aspect-ratio side is intact.
- Check-script hygiene is compliant with `.claude/rules/verification-scripts.md`:
    all four live in `checks/`, are named for what they check, carry
    consumer-naming docstrings, and import rather than fork the committed MC and
    closure engines.
- §5.3's absolute numbers are **right**: I ran live shipped code
    (`mott_params(SHELLS["75mm M48 HE"], 864.4)` → `μ = 1.0826 g, N₀ = 2300.0`,
    `2μN₀ = 4980 g`), reproducing the "shipped" row to 4 digits. Recomputation
    rather than scaling was genuinely done.

---

### B1 — **Blocking** — §3.1's quadrature reversal is decided by an anchor that (a) is the output of one of the two candidates and (b) lacks the resolution to separate them

Lines 132–155 (`### 3.1`), assumption **X3** (lines 310–316).

The reversal from scoping's recommendation is attributed to one new piece of
evidence: "The `Λ = 20` **regression row is new in this pass** and tips it the
other way" — because the `mott` step gives 1.556 against Mott's reported "about
1.5" while `poisson` gives 1.634, "**9 % above** what Mott reports — it does not
reproduce the one anchor available."

I read the page. `rspa.1947.0042.md` (Mott 1947, p. 305, greppable anchor
`the average length is about $1.5x_0$`, in the numbered finding (1) immediately
after `The calculations were made with $l/x_0 = 20$`) shows that number is read
off **figure 4**, a histogram drawn from *Mott's own deterministic ruled-line
procedure*, in bins of `0.4x₀`, and quoted to one significant figure with the
word "about". Two consequences:

1. **Circularity.** The criterion used to score the two schemes was *generated
    by one of them*. The `mott` step cannot lose this comparison; reproducing
    1.5 tests that `mott-ruled-line-mc.py` implements Mott's quadrature, not
    that the quadrature is the better model. Scoping said exactly this and said
    it honestly — §2: Mott's example is "a *theoretical* worked example with no
    fragment measurement attached — adopting a larger `κ_x` forfeits no
    empirical anchor". `derivation.md` §3.1 promotes the same number to "the one
    anchor available" without carrying that qualification forward. This is the
    structural shape of `.claude/incidents.md#unequal-comparison`: the scored
    dataset is not neutral between the candidates.
1. **Resolution.** "About 1.5", off a histogram binned at `0.4x₀`, cannot
    discriminate 1.556 from 1.634 — the two differ by 0.078, one-fifth of a bin,
    and both round to 1.6 at the precision Mott actually states. Reporting
    `poisson` as "9 % above what Mott reports" treats a one-significant-figure
    eyeball as a three-digit datum. On the same arithmetic the adopted `mott`
    step is 3.7 % above it.

§3.1's *second* bullet — moving the regime and the quadrature scheme in one
change would make the resulting triple non-attributable — is sound, is
sufficient on its own, and is the argument X3 should rest on. But it was
already available when scoping was written and did not tip the decision there;
what tipped it, by the derivation's own words, is the voided bullet.

Two aggravating circumstances that the derivation should be made to state:

- **The selected scheme is the one that moves everything less.** `mott` gives
    `μ ×1.22` where `poisson` gives `×1.30`; it fits FM 6-40 Table 59 better
    (geo-mean 0.909 vs 0.862, §5.2); and it leaves the `count-gap-1938` arm
    higher (1.89× vs 1.78×, §5.3). A reversal on a circular anchor that happens
    to select the answer closest to the shipped constants is exactly the
    pattern this review step exists to catch. The derivation is not accused of
    doing this deliberately — it tabulates every alternative — but the stated
    justification does not survive, and the incentive alignment must be named.
- **It moves away from the predecessor's own stated target.** The prior
    thread's assumption **K3** (`breadth-variance-factor-k/derivation.md`) names
    "the physically applicable configuration, whose internally consistent pair
    is `(κ_x, k) = (1.67, 1.20)`" — the *Poisson* pair. Superseding that is
    permissible; doing so silently, on the voided ground, is not.

**Impact.** `κ_x` 1.62 vs 1.67 ⇒ `μ` +6.5 %, `N₀` −6 %, 155 mm `B(r)` geo-mean
0.909 → 0.862, 75 mm count arm 1.89× → 1.78×. **No band membership, no
challenge verdict, and no demo-visible surface flips** — the acceptance bands
are unchanged at 11/11 and `count-gap-1938` stays FAIL either way. It is tiered
Blocking on protocol, not on magnitude: a central value chosen by a comparison
that cannot discriminate is not a closed question, and the choice consumes the
entire ±3 % `κ_x` fidelity budget on its own (the quadrature band is ±3.2 %).

**Suggested correction (no re-run):** either

- keep `κ_x = 1.62` but rewrite §3.1/X3 so that (i) the `Λ = 20` row is
    labelled a *reproduction check of the MC's implementation of Mott's
    quadrature* — explicitly non-empirical, explicitly below the resolution at
    which it could discriminate; (ii) attributability/continuity is the sole
    stated ground; (iii) it is said plainly that the **physically faithful
    sampling is Poisson**, so 1.62 is the conservative low edge of a
    [1.62, 1.67] band rather than a central estimate; and (iv) the supersession
    of K3's (1.67, 1.20) is recorded; **or**
- adopt Poisson (1.67, 1.189) as scoping recommended — every downstream number
    is already tabulated in §5.2–5.3, so this too costs no re-run.

### B2 — **Blocking** — the committed `count-gap-1938` verdict disagrees with live shipped code, and §5.3 asserts the disagreement without noticing it

Lines 268–283 (`### 5.3`) and line 355 (§6.4, "Re-close `count-gap-1938`
against the shipped triple").

Verified against live code, not inferred:

| source | `μ` [g] | `N₀` | `N(≥0.166 g)` | /700 | /779 |
| --- | --- | --- | --- | --- | --- |
| live `src/arty` (`mott_params(75 mm, 864.4)`) | 1.0826 | 2300.0 | 1554.8 | **2.22×** | **2.00×** |
| `derivation.md` §5.3 "shipped" row | 1.083 | 2300 | 1555 | 2.22× | 2.00× |
| `derivation.md` §5.3 "bare `A` = 1.6" row | 0.929 | 2681 | 1757 | 2.51× | 2.26× |
| committed `challenges/count-gap-1938/rebaseline-verdict.md` (published as the **shipped-code** verdict) | 0.826 (f=1) | 3016 | — | **2.51×** | **2.25×** |

The published challenge verdict — "genuine FAIL at 2.25× (/779) / 2.51× (/700)"
(`rebaseline-verdict.md:134`, `:167`, `:353`) — reproduces the **bare `A` = 1.6**
row, not the shipped one. `aspect-ratio-moment-leverage.py`'s own docstring
confirms it: "baseline check c=1.0 should reproduce N=1756, 2.51x, 2.25x", and
`0.929 × c·k(75 mm) = 0.929 × 1.1656 = 1.083` = live `μ`. The challenge's
published figures are stale by exactly the shipped `(c, k)` moment correction
from `breadth-variance-factor-k`.

The derivation's own numbers are correct; the defect is that it prints both
rows in one table, states "The challenge improves from 2.22×/2.00× to
1.89×/1.70×", and hands those numbers forward in §6.4 as the basis for
re-closing the challenge — without observing that the challenge currently
publishes 2.25×/2.51× for the state the derivation calls 2.22×/2.00×. A
committed, published surface is carrying a wrong number, and
`.claude/rules/deferred-findings.md` is explicit that an agent may not close
that by deferral.

**Impact.** The published `/779` arm moves 2.25× → 2.00×, i.e. from
"**outside** the 2× PASS band" (the challenge's own language,
`rebaseline-verdict.md:82`) to sitting *on* the band edge — a near-qualitative
change in a published verdict. `/700` moves 2.51× → 2.22×. The FAIL survives on
`/700`, so nothing in the demo flips, but the residual the remaining candidates
(C3, C4) must close is ~12 % smaller than the challenge states.

**Suggested correction:** one sentence in §5.3 recording the discrepancy, plus a
one-line marker next to it:

*(Suggested marker text enacted verbatim at `derivation.md` §5.3 in the fix pass
— the copy that stood here has been removed so the register does not carry the
same blocking finding twice.)*

Whether the challenge re-closes now or after the `src/arty` pass is the human's
call, not this derivation's.

### D1 — **Deferrable** — `A_eff = 1.6·c·k` is still a mixed pair, and only its *second* moment was checked

Lines 189–215 (§4.2, second bullet).

`k = 1.1711` is the marginal of the ruled-line MC; `c` is a ratio of moments of
the **reweighted per-cell** population, whose realised second moment `k_pop` is
1.153–1.181 — 155 mm is 1.6 % *below* the `k` that ships beside it. §4.2 calls
this "closure check passes"; it is more accurately a measured residual of the
same species as the prior thread's finding B2, one level down.

The gap I would rather see closed is the *first* moment. The prior thread's
assumption **K6** records that the same `⟨m⟩ = 2μ` reweighting shifts the
population's first moment to `⟨x⟩ = 1.60x₀` against the MC's 1.5604 — a 2.5 %
distortion. `κ_x` **is** a first moment, and §4.2 checks only `k_pop`. If the
same ~2.5 % distortion persists at `Λ = 95`, the shipped `κ_x` is that far off
the population `c` was measured on.

**Impact.** ≤1.6 % on `μ` from the `k`/`k_pop` mismatch alone; up to ~5 % on `μ`
if the first-moment distortion is K6-sized. Individually inside the ±6 % `μ`
target, which is why this is deferrable — but it is the third appearance of this
pattern in this constant family and should be logged, not re-discovered.

**Suggested resolution (a logged limitation, not a fix):** have
`c-at-fleet-regime.py` print `⟨x⟩_pop` beside `k_pop`, and add one assumption
line: *"`A_eff` pairs the MC-marginal `k` with a `c` measured on the
mass-reweighted cell population; the two populations' second moments differ by
≤1.6 % and their first moments by ~2.5 % (inherited K6). The residual is carried,
not corrected."*

### D2 — **Deferrable** — §5.2 reports the worse `B(r)` fit but then argues it away, and leans on an acceptance band too wide to say anything

Lines 248–266.

The reporting itself is honest — "**Report honestly: on this anchor alone the
new triple fits slightly *worse***", |log| 0.095 vs 0.045 — and that deserves
credit. The three bounding bullets that follow do not all hold:

- "It stays 11/11 inside the 0.5–2× acceptance band" is near-vacuous as
    reassurance. That band spans a factor of 4 on `B`; a 22 % move in `μ` (and
    even the 30 % Poisson move) cannot be scored by it. All four drivers,
    including the shipped one and the band edge, are 11/11. A test that every
    candidate passes bounds nothing.
- "It is therefore **not** evidence against the `κ_x` regime argument"
    over-claims. B(r) cannot apportion the discrepancy among the factors of
    `1.6ckκ_x²` — that part is right, and the identical normalised shape row
    demonstrates it. But this change moves *only* that product, so B(r) is a
    direct test of exactly what the change does, and the agreement worsens by a
    factor 2 in |log|. The correct statement is that B(r) is weak, ambiguous
    evidence *against the product*, not that it is not evidence.
- The bullet declining to re-open the `percell`/`marginal` choice on B(r)
    grounds is **right** and well-reasoned; keep it verbatim.

**Impact.** No number changes. It matters because §5.2 is the only empirical
contact this change makes, and the argument as written would let a future pass
believe the change was empirically neutral when it was mildly adverse — which is
also a second, independent reason to state B1's Poisson edge (0.862) as what it
is rather than as a merely-tabulated alternative.

**Suggested correction:** replace the second bullet with — *"`B(r)` constrains
only the product `1.6ckκ_x²` and cannot say which factor is responsible; it is,
however, a direct test of that product, and the product's agreement worsens
(|log| 0.045 → 0.095). The 0.5–2× band is too wide to make either result
decisive — all four drivers pass it."*

### D3 — **Deferrable** — a source-absence claim was inherited from scoping without the page check, and is used to direct the deletion of a committed closure check

Lines 348–353 (§6.4, Action E): "Mott's own `0.24 in.` is what is wrong, by his
own model", used to justify changing
`challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`.

The claim rests on there being no measurement attached to Mott's p. 306 worked
example — a **negative** claim about a source, which
`.claude/rules/source-data-fidelity.md` forbids resting on a derived surface or
an inherited assertion. `derivation.md` inherits it from `scoping.md` §2 without
going to the page.

I checked, so this one closes in my favour: `rspa.1947.0042.md` p. 306, anchor
`Thus if $\gamma \sim 100$, the average fragment length is about 0.24 in.`,
is the terminal sentence of the numerical example and is followed immediately by
`## 3. A THEORETICAL ESTIMATE OF THE CONSTANT $\gamma$`. No measurement is
attached, and the `1.5x₀` it uses is figure 4's own output. **The claim stands.**

**Impact.** None numerically — the conclusion is correct. Deferrable because the
*method* was not: had the page said otherwise, Action E would have deleted a
correct closure check on a false premise. Record the anchor above in §6.4 so the
`src/arty` pass does not re-litigate it.

### N1 — **Note** — which run each adopted digit comes from

`κ_x = 1.62` sits at the top of the two-seed spread (§3: 1.6190 seed A, 1.6138
seed B, mean 1.6164; §4.2's third run: 1.6199). `k = 1.1711` is taken from §4.2's
run while §3's two seeds give 1.1714/1.1733 (mean 1.1724). Everything is inside
MC noise (+0.22 % on `κ_x`, +0.45 % on `μ` against the seed mean), so no number
should change — but §6.1's "basis" column should name the specific run each
adopted digit is read from, since three runs of the same configuration are in
play.

### N2 — **Note** — §6.5 arithmetic

"The regime band (±0.3 %) and the quadrature band (±3.2 %) sit **at or inside**"
the ±3 % `κ_x` target. 3.2 % > 3 %. Say "marginally exceeds"; this is also the
quantitative reason B1 is not a free choice.

### N3 — **Note** — "`Λ = 95`, the fleet's `v_bu`-weighted centre" (line 86)

`Λ ∝ v_bu` by eq. (2), so weighting `Λ` by `v_bu` is not a defined operation on
this set; the unweighted fleet mean is 93.7. Immaterial (0.05 % on `κ_x` by §3's
0.032-per-e-fold slope). Say "a round value inside the 84–100 band, within 6 % of
every shell" — which is what §2 goes on to justify anyway.

### N4 — **Note** — layering and scripts

No `.qmd` or `src/arty/` change in this pass, so there is nothing for the
no-physics-in-notebooks check to bite on. The four `checks/` scripts import the
committed MC and closure engines rather than forking them, read Table 3 from the
CSV rather than a literal array, and name their consumer in the docstring. The
`downstream-at-new-triple.py` literals (`C_SHIP`, `K_SHIP`) are shipped model
constants, not a re-typed source series, so the extract-once rule is not
engaged.

---

### Summary of required actions

| # | Tier | Action |
| - | ---- | ------ |
| B1 | Blocking | Rewrite §3.1/X3: the `Λ = 20` row is a reproduction check of Mott's own quadrature, non-empirical and below discriminating resolution; rest X3 on attributability alone; state Poisson as the physically faithful scheme and 1.62 as the low edge of [1.62, 1.67]; record the supersession of K3's (1.67, 1.20). *Or* adopt Poisson. Either costs no re-run. |
| B2 | Blocking | Add the §5.3 sentence and the blocking finding marker (text quoted above) on the stale `count-gap-1938` published verdict (2.25×/2.51× vs live 2.22×/2.00×). Human decides when the challenge re-closes. |
| D1 | Deferrable | Log the mixed-pair residual as an assumption; print `⟨x⟩_pop` beside `k_pop`. |
| D2 | Deferrable | Re-word §5.2's second bullet; drop "11/11 in band" as a bound. |
| D3 | Deferrable | Record the p. 306 anchor confirming the absence claim in §6.4. |
| N1–N4 | Note | Name the source run per adopted digit; fix §6.5's "at or inside"; drop "`v_bu`-weighted"; no action on N4. |

**Verdict: FAIL** (B1, B2). Both are text-and-marker fixes; the physics, the
`Λ` derivation, the caliber-independence argument, the `μ₀` self-consistency
catch, and every recomputed downstream number survive review.

---

## Pass 2 — re-review of fix cycle 1 (2026-08-18, @model-reviewer, Opus)

Scope by brief: **B1 and B2 only**, plus the N2/N3 folds and the `review.md`
marker-hygiene edits. D1–D3, N1, N4 are not re-litigated (correctly deferred to
fix cycle 2). No MC re-run, no number re-derived from scratch.

Register at pass start:
`collect-findings.py --for experiment/fragmentation-field/updates/kappa-x-shell-regime`
→ **no open findings on this scope** (the new marker at `derivation.md:336`
points *outward* at `count-gap-1938`, which is why it does not report here —
that is the correct routing, see B2 below). The upstream marker in
`breadth-variance-factor-k/derivation.md:438` is still open and still correctly
held pending the `src/arty/` pass.

**Verdict: PASS-with-limitations.** B1 **closed**, B2 **closed**. No Blocking
finding remains on this derivation. The limitations still to be logged are
Pass 1's D1–D3 (unchanged text), which fix cycle 1 was not scoped to touch.

### B1 — **closed**

`derivation.md` §3 item 3 (lines 130–136), §3.1 (138–201), X3 (371–384), §6.5
(439–449). Checked against each of the four conditions Pass 1 set:

1. **`Λ = 20` relabelled as a reproduction check.** §3 item 3 now reads "a
    **regression check on `mott-ruled-line-mc.py`'s implementation of Mott's
    quadrature, not an empirical anchor and not a test between quadrature
    schemes**" and forwards to §3.1. §3.1's first bullet states the circularity
    ("the criterion is an output of one of the two candidates, so that candidate
    cannot lose"), the resolution limit (0.078 = one-fifth of a `0.4x₀` bin,
    both round to 1.6 at Mott's one significant figure), and retires the "9 %
    above" phrasing explicitly, noting `mott` is itself 3.7 % above on the same
    arithmetic. Scoping's non-empirical qualification is restored in substance.
1. **Attributability is the sole stated ground.** §3.1's second bullet is the
    only load-bearing argument, and X3 says so in bold ("on **attributability,
    not on physics**"). I grepped the whole derivation for residual reliance on
    the voided comparison: the only remaining mentions of `1.5x₀` are §2's
    narrative of what Mott did (line 94), §3's relabelled regression row (131),
    §3.1's own voiding bullet (146–157), and X3's "plays **no part** in this
    choice" (382). **Nothing in the decision chain leans on it.** §3.1's closing
    paragraph pre-empts the obvious objection by flagging the `Λ` slopes (+4.0 %
    `mott`, +2.2 % `poisson`) as internal-to-scheme so the voided anchor does not
    re-enter through the back door — that is the right catch and was not asked
    for.
1. **Poisson named as the physically faithful scheme; 1.62 framed as a low
    edge.** §3.1's adoption line ("the *low edge* of a `[1.62, 1.67]` band, not a
    central estimate") and X3 both carry it, with the direction of the one-sided
    band stated (+6.5 % on `μ`) and both edges tabulated in §5.2–5.3 so the
    reversal costs no re-run. The incentive alignment Pass 1 asked to be named
    *is* named ("The retained scheme is also the one that moves everything
    least"), with the disclaimer that this is not a fitness claim.
1. **K3 supersession recorded and accurate.** Checked the primary wording:
    `breadth-variance-factor-k/derivation.md:464` — K3 says the consistency
    preserved is with "the **shipped legacy constant** `κ_x = 1.5`, **not** with
    the physically applicable configuration — real shells sit at `l/x₀ = 50–200`,
    whose internally consistent pair is `(κ_x, k) = (1.67, 1.20)`", and names
    *both* deviations (`l/x₀ = 20`, and "Mott's deterministic `Δτ` over exact
    Poisson"). §3.1's "meets the regime half, declines the quadrature half" is a
    faithful split of exactly those two clauses. (The brief pointed at
    `mott-fragment-shape-closure/derivation.md`; K3 does not live there — it is
    `breadth-variance-factor-k`, which is what the derivation cites. The citation
    is right.)

**Downstream consistency with the new framing** — the second thing the brief
asked. §5.2, §5.3 and §4.2 all carry an explicit "Poisson band edge" row;
§6.1's adopted table names the `Mott Δτ step` in its basis column; §6.5 now
states the quadrature band "marginally exceeds" the ±3 % target and ties that
back to §3.1. I found **one** residual of the old central-estimate framing
(N5 below), which is a ranking sentence with no numeric consequence.

### B2 — **closed**

`derivation.md` §5.3 (324–336) and §6.4's re-close bullet (423–428).

- The new §5.3 paragraph states the discrepancy in the terms Pass 1 verified:
    the published `2.25×/2.51×` pair reproduces the **bare `A` = 1.6** row, live
    `src/arty` gives `2.22×/2.00×`, and the gap is exactly the shipped `(c, k)`
    moment correction. It also says whose problem it is ("this derivation is not
    its owner") rather than closing it by deferral, which is what
    `.claude/rules/deferred-findings.md` requires.
- The marker at line 336 **parses**. `collect-findings.py --for
    …/count-gap-1938/rebaseline-verdict.md` returns it as
    `[blocking] … raised 2026-08-18 (0d) in …/kappa-x-shell-regime/derivation.md:336`,
    and it appears in `OPEN-FINDINGS.md:17–19`. One line, brackets intact, three
    `affects:` paths, all three of which exist on disk. The routing is outward to
    the challenge that owns the wrong number — correct, and the reason the
    aspect-scoped collector reports "no open findings" here.
- The marker text matches the B2 finding: same two ratio pairs, same causal
    attribution (pre-`(c,k)` bare `A` = 1.6 chain), same three consumers
    (`rebaseline-verdict.md`, `count-chain.md`, `aspect-ratio-moment-leverage.py`
    — the last being the script whose docstring baseline confirmed the diagnosis
    in Pass 1).
- §6.4's re-close bullet now starts from `2.22×/2.00×`, names the published pair
    as stale, points at the §5.3 marker, and leaves the timing to the human.

Nothing about B2's closure required re-running live code; Pass 1's live-code
table is the evidence and it is unchanged by a text edit.

### N2 / N3 folds — both correct

- §6.5 line 443: "**The quadrature band (±3.2 %) marginally exceeds it**" —
    N2 folded, and it now carries the load Pass 1 wanted it to (it is cited as
    the quantitative reason the scheme choice is not free). The trailing "the
    shipped `κ_x = 1.5` was 7.4 % low" is arithmetically right against 1.62.
- §2 lines 86–90: the `v_bu`-weighted framing is gone, replaced by "a round
    value inside the 84–100 band and within 6 % of every shell", with an explicit
    parenthetical explaining *why* a `v_bu` weighting is undefined and giving the
    unweighted mean 93.7 and its 0.05 % cost. N3 folded, better than suggested.

### N5 — **Note** (new, minor) — §4.2's third bullet still ranks the quadrature band as the small one

Lines 259–261: "The `percell`/`marginal` spread (±5 % on `c`) … remains the
dominant *method* uncertainty — larger than the ±1.5 % quadrature band and
larger than the ±0.3 % fleet-regime band."

The three bands are measured on three different quantities (±5 % on `c`, ±1.5 %
is the quadrature effect on `k`, ±0.3 % is the fleet spread on `κ_x`), so the
comparison does not close. Put on a common footing — the effect on `μ` — the
quadrature band is **+6.5 %** (X3) against the closure band's ±5 %, i.e. the
quadrature choice is now the *larger* of the two, which is precisely what §6.5
says two pages later ("marginally exceeds" the target while the closure band
"also exceeds it"). This is a leftover of the pre-fix framing in which 1.62 was
central.

**Impact.** No number changes; no rendered output moves. It matters only in that
a later pass reading §4.2 alone would mis-prioritise which band to close first.

**Suggested correction (one sentence):** "…remains the widest *closure*-method
band (±5 % on `c`, hence on `μ`); the quadrature choice is comparable or larger
(+6.5 % on `μ`, X3), and the fleet-regime band (±0.3 % on `κ_x`) is negligible
beside both."

### N6 — **Note** (new, hygiene) — dangling forward-reference left by the marker-copy removal

`review.md:302` (Pass 1's summary table, B2 row) still reads "Add the §5.3
sentence and the blocking finding marker **(text quoted above)**", but the
quoted marker text at `:165–170` was replaced by the parenthetical explaining
its removal. The pointer now resolves to nothing.

Content check on the hygiene edits themselves: I read the full Pass 1 section.
The two edits are (i) `:168–170`, the marker copy replaced by a parenthetical
stating it was enacted verbatim at `derivation.md` §5.3, and (ii) `:302`, the
bare token de-fanged. **No substantive Pass 1 content was lost** — every
finding, number, anchor, impact estimate and suggested correction is intact, and
the removed marker text now exists verbatim at `derivation.md:336` (I compared
them). Removing the duplicate was the right call: two live markers would have
double-registered one finding.

**Suggested correction:** change "(text quoted above)" to "(text now at
`derivation.md:336`)".

### N7 — **Note** (new, minor) — K3's `k` half is ~1 % short of "precisely"

§3.1's supersession paragraph says the unmet residual is "**precisely** the
+3.2 % / +6.5 % band edge carried in X3". Exact on `κ_x` (1.62 → 1.667). K3's
stated pair is `(1.67, **1.20**)` while this pass measures the Poisson `k` at
**1.189** — so on the `k` half the residual is the band edge *plus* ~0.9 %,
which is inside K3's own lower-`n` noise. Immaterial (`k` enters `μ` linearly,
0.9 % against a ±6 % `μ` target); worth one word ("essentially") if the
paragraph is touched again.

### Standing limitations for fix cycle 2 (unchanged from Pass 1)

- **D1** — log the mixed-pair residual: `A_eff` pairs the MC-marginal `k` with a
    `c` measured on the mass-reweighted cell population; second moments differ by
    ≤1.6 %, first moments by ~2.5 % (inherited K6); residual carried, not
    corrected. Have `c-at-fleet-regime.py` print `⟨x⟩_pop` beside `k_pop`.
- **D2** — re-word §5.2's second bullet (`B(r)` is a direct test of the product
    and the product's agreement worsens, |log| 0.045 → 0.095; the 0.5–2× band is
    too wide to be decisive — all four drivers pass it). Still present verbatim
    at lines 303–307.
- **D3** — record the p. 306 anchor confirming the source-absence claim in §6.4
    Action E, so the `src/arty/` pass does not re-litigate it.

### Verdict

**PASS-with-limitations.** Fix cycle 1 closed both Blocking findings on the
terms Pass 1 set, introduced no new Blocking or Deferrable defect, and did not
lose Pass 1 content in the marker-hygiene edits. Three new Notes (N5–N7), none
of which changes a number. Remaining work is the D1–D3 limitation entries and
Pass 1's N1 (name the source run per adopted digit in §6.1).

---

## Pass 3 — mechanical verification (2026-08-19, @model-reviewer, Sonnet)

Scope by brief: reproduce the four check scripts standalone, trace
`mott_params` against §1 eq. (3), confirm §6.1's adopted triple against script
output, confirm the `derivation.md:336` marker parses and its cited numbers
against the actual `count-gap-1938` files, spot-check the Mott 1947 primary
anchors, and confirm D1/D2/D3/N1/N5/N6/N7 are accurately characterized (not
re-resolved). No re-litigation of B1/B2's judgment.

Register at pass start: `collect-findings.py --for
experiment/fragmentation-field/updates/kappa-x-shell-regime/` → **no open
findings on this scope** (consistent with Pass 1/2).

**Verdict: PASS-with-limitations, unchanged from Pass 2, plus one new
Deferrable finding (D4) this pass adds.**

### Check-script reproduction — all four match derivation.md verbatim

- `checks/ell-over-x0-per-shell.py` → `Λ` = 100.2 / 96.3 / 83.7 / 94.4 for
    155/105/75/60 mm, `f = 0.9428` — matches §2's table exactly, including the
    long-way/short-way agreement claim.
- `checks/kx-at-fleet-regime.py` → seed A `κ_x = 1.6190`, seed B `1.6138`
    (mott, `Λ = 95`); `Λ = 20` regression row gives mott `1.5561`, poisson
    `1.6343` — matches §3's "1.556" / "1.634" and B1's "9 %"/"3.7 %" arithmetic
    exactly. Poisson at `Λ = 95` gives `1.6711`/`1.6629`, consistent with the
    adopted `1.67` (rounded) cited in X3/§5.2–5.3.
- `checks/c-at-fleet-regime.py` → `k_MC = 1.1711` at `n = 41053`, `<xi> =
    1.6199` — matches §4.2's cited `k = 1.1711` and N1's "third run: 1.6199".
    `percell` closure at `κ_x = 1.62`: `c_ruled` = 1.0789/1.1524/1.0408/1.0093
    for 105/155/75/60 mm — matches §6.1's adopted-`c` row digit-for-digit.
- `checks/downstream-at-new-triple.py` → 75 mm count-gap-1938 arms: bare
    `A=1.6` gives `μ=0.929, N₀=2681, 2.51×/2.26×`; shipped gives `μ=1.083,
    N₀=2300, 2.22×/2.00×`; new (percell) gives `μ=1.321, N₀=1886, 1.89×/1.70×`;
    Poisson edge gives `μ=1.425, N₀=1748, 1.78×/1.60×`. All four rows match
    §5.3's table exactly. The 155 mm `B(r)` geo-mean ratios (1.046/0.909/0.970/
    0.862) match §5.2 exactly, including the "worsens 0.045→0.095" `|log|` claim.

No transcription drift found anywhere in §2–§5's tables against live script
output.

### `mott_params` vs §1 eq. (3) — confirmed accurate

`src/arty/fragmentation.py:454-499`. `alpha = shell.aspect_ratio *
shell.breadth_factor**2 * t_bu / x0`, `gamma = alpha**(-2/3) * gamma'`, `mu =
sqrt(2/rho) * (sigma_f/gamma)**1.5 * (r_bu/v_bu)**3`, `N0 = mass_shell /
(2*mu)` — an exact match to eq. (3)'s `α = A_eff·κ_x²·t_bu/x₀`, `γ =
α^{-2/3}γ'`, `μ ∝ γ^{-3/2}`, `N₀ = M/2μ`. `shell.breadth_factor` is
`_MOTT_BREADTH_FACTOR = 1.5` (= shipped `κ_x`, `fragmentation.py:160`).
`shell.aspect_ratio` is set per-shell in `src/arty/shells.py` to
`mott_aspect_ratio(name)`, which returns `_MOTT_ASPECT_RATIO *
MOTT_ASPECT_MOMENT_C[name] * MOTT_BREADTH_VARIANCE_K` (`fragmentation.py:
232-234`) — i.e. `A_eff = 1.6·c·k` exactly as eq. (3) states, with the current
`(c, k)` pair already shipped (`shells.py:37,68,107,128` comments: e.g. 75 mm
`c=1.0247, k=1.1375 → A_eff=1.865`). §1's characterization of shipped code is
accurate on every symbol.

### §6.1 adopted triple vs script output — no drift

`κ_x=1.62`, `k=1.1711`, and the four per-shell `c` values all trace to the
runs reproduced above (see the check-script bullets). The "shipped" column of
§6.1 (`c` = 1.1254/1.0608/1.0247/1.0026) matches `shells.py`'s current
per-shell comments digit-for-digit — confirmed by direct grep of
`src/arty/shells.py`, not by trusting the check script's own diagnostic
columns (see D4 below, which is exactly why this distinction matters).

### `derivation.md:336` marker — parses, and its live-code number is right

`collect-findings.py --for
experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md`
returns the marker as `[blocking] … raised 2026-08-18 (1d) in
…/kappa-x-shell-regime/derivation.md:336`, one line, brackets intact, three
`affects:` paths (all exist on disk) — confirms Pass 2's parse check still
holds. The marker's live-code figure, `2.22× (/700) / 2.00× (/779)` at
`κ_x=1.5, k=1.1375, c=1.0247`, is exactly what `downstream-at-new-triple.py`
prints for the "shipped" row — correct.

### D4 — **Deferrable** (new) — the marker's *published* figure (2.25×/2.51×)
is itself stale; the actual current headline is 2.28×/2.54×, and the causal
label "bare `A` = 1.6" no longer describes it

`derivation.md` lines 326–334 (§5.3 prose), 336 (the marker), 423–428 (§6.4
re-close bullet) all cite `challenges/count-gap-1938` as currently publishing
"2.25× (/779) / 2.51× (/700)" and attribute that pair to the **pre-`(c,k)`
bare `A=1.6`** chain. I checked all three consumer surfaces directly, not the
derivation's word for it:

- `rebaseline-verdict.md:11` (top-of-file **Status** line, the file's own
    current authoritative headline): "genuine **FAIL at 2.28× (/779) / 2.54×
    (/700)**".
- `count-chain.md` (11 separate occurrences, e.g. lines 59, 584, 669, 723):
    "genuine FAIL at 2.28× (/779) and 2.54× (/700)" — the file's live standing
    verdict.
- `challenges/README.md:20`: "count arm FAILs at **2.28×/2.54×** (plug-shear)".

All three agree: the file's *current* published pair is **2.28×/2.54×**, not
2.25×/2.51×. The 2.25×/2.51× figure `derivation.md` quotes (with anchors
`:134`, `:167`, `:353`) is a *superseded* quote from `rebaseline-verdict.md`'s
fourth re-closure banner (2026-08-15) — and that very passage is followed two
lines later, in the same banner, by "(**restated 2.28× / 2.54× by the fifth
banner below**)" (line 168). The fifth banner (2026-08-16, dated *before*
this derivation's 2026-08-18 pass) already ships a per-shell `c`-only
correction (`aspect_ratio = 1.6·c`, no `k`) that moves the published pair from
2.25×/2.51× to 2.28×/2.54× — so the currently-published figure is **not** the
bare `A=1.6` chain the derivation calls it; it is a `c`-corrected,
`k`-uncorrected intermediate state one revision closer to live than the
derivation assumes.

**Impact.** No physics or shipped number changes; the marker's core
instruction — re-close starting from live `2.22×/2.00×` — is unaffected and
still correct regardless of which stale figure is named as the target. The
inaccuracy is confined to the *diagnostic* text: the specific "published"
number is off by 1.2–1.3 % (2.25→2.28, 2.51→2.54) and the causal label ("bare
`A`=1.6") misdescribes the current top-of-file state (which already has the
`c` half). Below the ±3 % `κ_x` fidelity target and immaterial to any
acceptance-band or FAIL/PASS conclusion — hence Deferrable, not Blocking. It
matters because a future pass re-closing `count-gap-1938` off this marker
alone, without independently reading `rebaseline-verdict.md`'s own top line,
would cite the wrong "before" figure by ~1.3 % and the wrong reason for it.

**Suggested correction:** in `derivation.md` §5.3, the marker, and §6.4,
replace "2.25× (/779) / 2.51× (/700)" / "the challenge currently publishes"
with "2.28× (/779) / 2.54× (/700), the file's current top-line verdict (fifth
banner, 2026-08-16 — already `c`-corrected, not yet `k`-corrected)"; drop "bare
`A`=1.6 chain" and replace with "pre-`k` chain" (the `c` half is already
shipped in the cited pair).

### D5 — **Deferrable** (new) — one check script's own "shipped" comparison
column is a hand-typed, already-stale literal, though it does not feed any
number `derivation.md` adopts

`experiment/fragmentation-field/updates/breadth-variance-factor-k/checks/
c-on-ruled-line-population.py:184-185` (executed by `c-at-fleet-regime.py`,
which patches and `exec`s this file's source rather than importing it) prints
"`c_ship`"/"`A_ship`" columns from a **hand-typed dict literal**,
`shipped_c = {"155mm M107 HE": 1.2506, …, "75mm M48 HE": 0.9854, "60mm
M49A2 HE": 0.9200}` (line 184), not read from `arty.shells.SHELLS` or
`arty.fragmentation.MOTT_ASPECT_MOMENT_C`. Current live `MOTT_ASPECT_MOMENT_C`
(confirmed against `src/arty/shells.py`'s own per-shell comments) is
1.1254/1.0608/**1.0247**/1.0026 for 155/105/75/60 mm — i.e. the hardcoded
`shipped_c` dict (0.9854 for 75 mm) is stale by the same `c`-revision gap D4
describes, and is exactly the "hand-copies a series into a literal array"
anti-pattern `.claude/rules/source-data-fidelity.md` warns reintroduces
transcription error.

**Impact.** None on any number `derivation.md` reports: I confirmed §6.1's
"shipped" `c` column (1.1254/1.0608/1.0247/1.0026) matches `shells.py`
directly, not this script's stale `c_ship`/`A_ship` columns, which are printed
diagnostics internal to the check script's own console output and are not
quoted anywhere in `derivation.md`. Deferrable, and cheap: replace the literal
dict with a live read of `arty.shells.SHELLS[name].aspect_ratio` /
`arty.fragmentation.MOTT_ASPECT_MOMENT_C[name]` so the column can't drift again
un-noticed.

### Primary-citation spot check — Mott 1947, confirmed

`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`
greps confirm, verbatim: line 197 "The calculations were made with `l/x_0 =
20`"; line 200 "(1) The fragments have lengths most of which lie between `x_0`
and `2x_0`, and that the average length is about `1.5x_0`"; line 215 "Thus if
`γ ∼ 100`, the average fragment length is about 0.24 in."; line 217 begins "##
3. A THEORETICAL ESTIMATE OF THE CONSTANT `γ`…" immediately after. This
confirms both B1's circularity argument (the `1.5x₀` anchor is Mott's own
model output, one significant figure) and D3's disposition (no measurement is
attached to the 0.24 in. worked example — the source-absence claim stands).

### D1, D2, D3, N1, N5, N6, N7 — characterization confirmed, not re-resolved

- **D1** — spot-checked against `c-at-fleet-regime.py`'s live output: `percell`
    `k_pop` for 155 mm at `κ_x=1.62` is 1.1526 vs adopted `k=1.1711`, a 1.58 %
    gap — matches D1's "155 mm is 1.6 % below" claim closely. Accurately
    characterized.
- **D2, N5, N7** — re-read against current `derivation.md` text (lines
    248–266 for D2, 259–261 for N5, the X3 supersession paragraph for N7);
    all three still describe the text as it currently stands (D2's and N5's
    target sentences are verbatim unchanged from Pass 2's quotes; N7's "1.20 vs
    1.189" arithmetic reproduces from this pass's own `kx-at-fleet-regime.py`
    run, `k=1.1868/1.1907` at `Λ=95` poisson, mean ≈1.189). Accurate.
- **D3** — independently re-verified against the primary above (see previous
    section); Pass 2's disposition (claim stands) is confirmed a second time.
- **N1, N6** — textual/hygiene notes, re-read in place; both still describe
    the document accurately (N1's "which run" ambiguity is unchanged; N6's
    dangling-pointer text at line 302 is unchanged from Pass 2's finding).

### Verdict

**PASS-with-limitations.** No Blocking finding. All four check scripts
reproduce `derivation.md` §2–§5 exactly; `mott_params` matches §1 eq. (3) on
every symbol; §6.1's adopted triple is drift-free against live script output
and against `src/arty/shells.py` directly; the `:336` marker parses and its
live-code figure is correct. Two new Deferrable findings this pass (D4, D5),
both citation/hygiene issues with no effect on any physics number, acceptance
band, or FAIL/PASS conclusion. Standing limitations to log (Pass 1's D1–D3,
Pass 2's N1/N5/N6/N7, and this pass's D4/D5) are listed above with impact
estimates; none blocks.
