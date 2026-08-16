# Scoping — mass-dependent fragment shape / aspect ratio A(m)

**Aspect:** replace the shipped global constants `A = l̄/x̄ = 1.6` and `κ_x = 1.5`
in the Mott shape closure with a mass-dependent form `A(m)`.

**Status:** scoping pass, 2026-08-16. Recommendation in §6.

**Motivating hypothesis (to be tested here, not assumed):** large fragments
retain plate/wedge-like case-wall geometry (high aspect ratio); small fragments
tend isotropic. If so, `A(m)` rising with `m` would shrink the tail-weighted
perforating count (`count-gap-1938` residual) while leaving the mass-weighted
B(r) fit (`drag-gap-1944`) roughly intact, since most case mass is at small/mid
masses.

---

## 1. What the held literature actually says (acceptance criterion 1)

### 1.1 The one dataset that resolves aspect ratio *by size*

`doc-reference/fragmentation/explosion-fragment-model/tables/table-3-grady-aspect-ratio-counts.csv`
(Felix, Colwill & Harris 2022, Table 3; anchor `The calculation of aspect ratios for Grady`,
`source.pdf` p.9 = journal p.167). Counts of Fig. 10 fragments by aspect-ratio
bin and by the authors' five size Groups:

| Group | 1:1  | 1:2 | 1:3 | 1:4+ | total | count-wtd mean ratio* |
| ----- | ---- | --- | --- | ---- | ----- | --------------------- |
| 0     | 1003 | 274 | 91  | 0    | 1368  | 1.33                  |
| 1     | 275  | 58  | 25  | 0    | 358   | 1.29                  |
| 2     | 96   | 352 | 76  | 8    | 532   | 2.02                  |
| 3     | 8    | 21  | 103 | 3    | 135   | 2.75                  |
| 4     | 0    | 7   | 8   | 7    | 22    | 3.00                  |

*taking bin centres 1,2,3 and 1:4+ ≈ 4 (the paper states no weighting rule for
the open bin — see the card's "Caveat carried with the number").

**Qualitatively the trend is exactly the hypothesised one and it is large:**
mean aspect ratio ≈ 1.3 in the two smallest Groups, ≈ 3.0 in the largest — a
factor ~2.3 across the size range, far bigger than the 1.48–1.66 spread the
shipped single constant 1.6 was averaged from.

### 1.2 Three reasons this is NOT usable as `A(m)` (the decisive finding)

**(a) The Groups have no stated mass, or size, definition.** Nothing in §4.1.2
(lines 121–130 of the extraction) defines Group 0–4 by mass, by length, or by
any dimension. They are visual size bands in one photograph. The closure needs
`A` as a function of fragment **mass** `m`; the source supplies `A` as a
function of an unquantified ordinal label. Building `A(m)` requires inventing
the mass edges — which is precisely the "unsourced spectrum shape" that
`challenges/count-gap-1938/mott-tail-shape.md` was discharged for.

**(b) The per-Group ratios are largely counting *assumptions*, not
measurements.** The paper's own method, verbatim per Group:

- Group 2: "fragments are **assumed** to have an aspect ratio of 1.2 [sic, 1:2]",
    with only 1:1, 1:3, 1:4 individually highlighted and counted;
- Group 3: "fragments are **assumed** to have an aspect ratio of 1:3", with
    1:1, 1:2, 1:4 counted;
- Group 0: the residual after counting 1:2 and 1:3 in a small red-outlined
    sub-area "are counted and **considered** to have an aspect ratio of 1:1";
- Group 1: 1:1 and 1:3 are "**estimated**".

So the modal bin of every Group is the analyst's default for that Group, not an
observation. The apparent A-vs-size trend is substantially a restatement of the
default the authors assigned to each band. The measured content is the minority
off-default bins. **This table cannot carry a fitted `A(m)` curve.**

**(c) Aspect-ratio direction is unresolvable in the source photographs.** §4.1.3
line 138: "In Figs. 10 and 11 it is impossible to differentiate fragments with
aspect ratio less than 1:1 from aspect ratios greater than 1:1 … it is assumed
that the long side of a fragment is its length." Any ratio <1:1 is folded up
into >1:1, which biases short/stubby fragments (the small end) upward and does
so *unequally across Groups* — the small-fragment Groups are exactly where the
fold-up bites hardest. The measured trend is therefore biased in the direction
that *understates* it, but by an unquantified amount, so it cannot be corrected.

### 1.3 Criterion match on shell type

Fig. 10 is Gardner (LLNL, 2000) [ref 23], reproduced in Grady's *Fragmentation
of Rings and Shells* [ref 29]; the paper calls it "the Grady paper" but the
photograph is Gardner's. §4.1.2 says only "the shell in Fig. 10"; the paper
labels the casing **ogive** (Table 4 row), which is the closest of the three
datasets to a WW2 US HE shell body. The brief's "155 mm HE M101" attribution is
**not stated in this extraction** — I could not confirm it from the retained
`.md`, and `source.pdf` is gitignored. Treat the shell identity as unverified.
It does not change the recommendation, because (a)–(c) already bind.

### 1.4 Bearing on the open finding (Mott & Linfoot primary)

The standing `[deferrable]` finding says Gold 2017's attribution to Mott (1943)
of *a constant breadth:length ratio* is not primary-backed — Mott & Linfoot
A.C. 3348 says twice that their theory does **not** account for splinter length,
only breadth, and where §3 treats length it makes length independent of breadth.

That is directly relevant here, and it cuts **both ways**:

- It removes any *primary* authority for "one constant A" — so the shipped
    `A = 1.6` rests on Felix 2022 Table 4 as an empirical average and nothing
    more. Confirmed; the value stands, the structural premise does not.
- But it equally removes any primary authority for a *mass-dependent* A. Mott
    & Linfoot's own position is that length is not predicted by the theory at
    all — the primary is silent on `A(m)`, not supportive of it. A `A(m)` built
    on Mott's breadth statistics would be extending the theory into exactly the
    region its authors disclaimed.

**I am leaving the finding marker standing.** This pass does not resolve it: it
neither repairs the derivation's citation nor closes the structural-premise
question. It should be closed by the Phase-3 pass on
`updates/mott-fragment-shape-closure/derivation.md` that the finding names.
This scoping doc is not that pass.

---

## 2. Where `A` actually enters — the brief's framing is the wrong lever

**`A` is a mass-spectrum parameter, not a drag/area parameter.** In the shipped
closure (`mott-fragment-shape-closure/derivation.md` eq. (2)):

$$\mu \;=\; A\,\kappa_x^{2}\,\frac{\sigma_F t_{bu}}{\gamma'}\Big(\frac{r_{bu}}{V_0}\Big)^{2},
\qquad N_0 = \frac{M_\text{case}}{2\mu}$$

so `μ ∝ A` and `N₀ ∝ 1/A` — **exactly** (A9.2 states the sensitivity). `A` does
not appear in the drag path at all: `retardation_coeff` uses the separate,
unsourced `C_shape = 0.90` (`fragmentation.py:113`), which §8 deliberately left
alone. So the brief's mechanism — "a mass-dependent shape shrinks the tail count
via presented area" — is not how `A` reaches the count. It reaches it through
`μ` and `N₀`, i.e. through the **whole** spectrum.

**Consequence: a literal per-fragment `A(m)` is structurally incoherent here.**
`A` enters a formula whose *output* is `μ`, the single scale parameter defining
the mass distribution `N(≥m) = N₀ e^{−√(m/μ)}`. Writing `A(m)` inside it makes
`μ` a function of the mass it is supposed to define — self-referential. Any
honest version of the idea must instead ask: **which moment of the aspect-ratio
distribution belongs in that single constant?**

That question is answerable from Table 3, and it is where the leverage is.

### 2.1 The reframed candidate: `A` is a count-weighted mean where the closure
needs an `x²`-weighted one

Eq. (2) comes from mean fragment mass `2μ = ρ·⟨l x t⟩ = ρ t₀·⟨A x²⟩` (with
`l = A x`). The shipped closure evaluates this as `ρ t₀ ⟨A⟩⟨x⟩²` — two separate
product-of-means approximations:

1. `⟨x²⟩ vs ⟨x⟩²` — **already documented** as assumption A9.1, bounded at
    1–2×, biasing `μ` low, deliberately not corrected.
2. `⟨A x²⟩ vs ⟨A⟩⟨x²⟩` — **not documented anywhere.** It is zero only if `A`
    and fragment size are uncorrelated. Table 3 says they are strongly and
    positively correlated (§1.1). So this term also biases `μ` **low**, by
    `1 + Cov(A, x²)/(⟨A⟩⟨x²⟩)`.

And the value in use is demonstrably the **count-weighted** mean: the check
script reproduces `⟨A⟩ = 1.568` over all 2415 Table-3 fragments with the open
bin at 4.0 (Felix's printed 1.58 needs the open bin near 6 — the card's caveat).
Count-weighting is dominated by Groups 0–1 (1726 of 2415 fragments, `Ā ≈ 1.3`).
An `x²`-weighted mean over the same table is pulled toward Groups 2–4
(`Ā = 2.0–3.0`).

**This is a real, sign-known, single-constant defect — and it needs no mass axis
for the Groups to establish its sign, only to pin its size.**

---

## 3. Implementation options, ranked

| # | Option | Data needed | Verdict |
| - | ------ | ----------- | ------- |
| **1** | **Moment correction on the single constant** (§2.1): replace count-weighted `A = 1.6` with the `x²`-weighted mean implied by Table 3, i.e. `A_eff = c·1.6` with `c = 1 + Cov(A,x²)/(⟨A⟩⟨x²⟩)`. Stays one constant, closed-form, no `A(m)`. | Table 3 (held) for the **sign and a bound**; Group size edges for the **point value** | **Recommended for derivation** — bounded even without the size edges. See §4. |
| 2 | Fitted per-fragment `A(m) = A₀(m/m₀)^p` in the mass closure. | mass per Group — not in any held source | Rejected: structurally incoherent (§2), and the mass axis would be invented — the same defect that discharged `mott-tail-shape.md`. |
| 3 | Two-regime step `A = 1.3 / 2.7` about a mass cut. | the cut — not in any held source | Rejected: the cut is the whole answer and it would be invented. |
| 4 | Per-fragment `A(m)` in the **drag** path via `C_shape(m)`. | as (2), plus reopens §8 | Rejected: `A` does not enter drag today (§2); this would couple two under-identified parameters (§5). |
| 5 | Physically-derived global ratio from the paper's own strain-rate argument (§4.1.1, `1/r₀ ≈ 1.22`; Morley's 1:2 hoop:longitudinal strain, line 113). | none extra | Not a mass-dependence source — both give one casing-wide ratio. Useful as an independent **cross-check on the value**, not as `A(m)`. |
| 6 | Commission @librarian for Gardner (LLNL 2000), the primary behind Fig. 10. | new acquisition | **Worth doing** — it is what turns option 1's bound into a point value. See §6. |

---

## 4. Leverage on the count-gap-1938 residual (criterion 3 — rough bound, re-solved not ratioed)

`count-chain.md` insists leverage be estimated by re-solving the chain, because
`m_thr`, `N₀` and `μ` do not move independently. Re-solved numerically in
`checks/aspect-ratio-moment-leverage.py` (run it; ~0.1 s), with `A → c·A` so
`μ → cμ` and `N₀ → N₀/c`, holding `m_thr` at the verdict row's 0.166 g:

| `c` | `μ` [g] | `N₀` | `N(≥m_thr)` | vs Tolch 700 | vs Tolch 779 |
| --- | ------- | ---- | ----------- | ------------ | ------------ |
| **1.00** (shipped) | 0.929 | 2681 | **1757** | **2.51×** | **2.26×** |
| 1.20 | 1.115 | 2234 | 1519 | 2.17× | 1.95× |
| 1.40 | 1.301 | 1915 | 1340 | 1.91× | 1.72× |
| 1.60 | 1.486 | 1676 | 1200 | 1.71× | 1.54× |
| 1.90 | 1.765 | 1411 | 1038 | 1.48× | 1.33× |
| 2.20 | 2.044 | 1219 | 916 | 1.31× | 1.18× |

The `c = 1.00` row reproduces `count-chain.md`'s verdict row (1757 vs 1756;
2.51× / 2.26× vs 2.51× / 2.25×) — the chain is correctly re-solved, not ratioed.

**Two non-obvious things this re-solve shows, both of which a ratio argument
would have got wrong:**

1. **`N` does not scale as `1/c`.** `N₀` falls as `1/c` but the survival factor
    `e^{−√(m_thr/μ)}` *rises* with `μ`, partly cancelling — `c = 1.9` gives a
    1.69× count reduction, not 1.9×. (Same structure as `count-chain.md`'s own
    "`N` does not move as `f^{-2}`" note, memory:
    `gotcha_mott_count_not_f_squared`.)
2. **`m_thr = 0.166 g ≪ μ = 0.929 g`** — `√(m_thr/μ) = 0.42`, so **66 % of all
    fragments perforate**. There *is no perforating tail*: the perforating
    population is essentially the whole population. This kills the brief's
    premise that a tail-only shape change could move the count while leaving the
    mass-weighted fit alone — and it is consistent with `count-chain.md`'s
    finding that "no mass cut at all already reproduces most of the 2.25×".

**Leverage verdict.** Sign is known and favourable: `Cov(A, x²) > 0` (§2.1), so
`c > 1` and the count goes **down**. Magnitude is bounded by Table 3 at
`1 < c ≤ ⟨A⟩_max/⟨A⟩ ≈ 3.0/1.57 ≈ 1.9`. Over that range the gap moves from
2.25×/2.51× to as far as 1.33×/1.48×. **`c ≥ ~1.4` puts the /779 arm inside the
within-2× PASS band; `c ≥ ~1.5` puts both arms inside it.** That is genuine
gap-closing leverage, unlike the ~1.35–1.6× ceiling a per-fragment area argument
would have given.

Scoping-grade caveats on the bound, flagged as such: (i) `m_thr` is held fixed —
correct, since `A` does not enter the drag/perforation path (§2), but a
derivation pass should confirm nothing else re-enters; (ii) the upper end `c =
1.9` assumes the `x²` weight concentrates entirely on Group 4, which it will
not — the realistic value is likely `c ≈ 1.3–1.6`, i.e. the gap lands around
1.5–1.9× on /779 and 1.7–2.1× on /700; (iii) this correction is of the **same
sign and the same family** as assumption A9.1's uncorrected 1–2× `⟨x²⟩/⟨x⟩²`
factor, so a derivation must treat both together or it will double-count.
**(iii) is the main risk to this candidate** and is the first thing a derivation
pass should settle.

---

## 5. Interaction with drag / `C_shape` / the B(r) fit (criterion 4)

`mott-fragment-shape-closure/derivation.md` §8 already flagged that `C_shape`
and the drag `B` are not independently identified, and deferred it.

**The recommended option 1 avoids that coupling; the rejected options 2 and 4
reopen it.** The distinction is sharp and is why the reframing matters:

- **Option 1 (moment correction on the constant) does not touch `C_shape` at
    all.** `A` and `C_shape` are *separate* parameters in the shipped code — `A`
    lives in `mott_params` (`μ`), `C_shape = 0.90` lives in `retardation_coeff`
    (`fragmentation.py:113`). Rescaling `A` by `c` changes the mass **spectrum**,
    not the per-fragment ballistic coefficient. §8's deferral is untouched.
- **But it is not free of the B(r) surface.** A different `μ` re-weights which
    fragments dominate the hit density at range, so `drag-gap-1944`'s B(r) fit
    sees a changed mass mix even with `B(m)` per-fragment unchanged. A derivation
    pass **must** re-run the B(r) check at the new `μ` and report it; the fit is
    not invariant, only the parameter is.
- **Options 2/4 (per-fragment `A(m)`) would be strictly worse.** A constant `A`
    is absorbable into a calibrated `B` up to a rescaling; `A(m)` changes the
    *mass-dependence* of the ballistic coefficient — a re-fit, not a re-scale.
    And memory/`gotcha_density_falloff_shape_is_threshold_degenerate` records
    that a hits-vs-range curve cannot discriminate drag (the threshold absorbs
    it), so B(r) could not validate the new degree of freedom either. That is an
    independent reason to prefer option 1 over 2/4 even if the data appeared.

---

## 6. Recommendation (criterion 5)

**Pursue — but as the reframed option 1 (aspect-ratio moment correction on the
single constant `A`), NOT as the mass-dependent `A(m)` the brief proposed.**
Reject `A(m)` outright; open a Workflow B derivation on option 1.

Reasoning a reviewer can check:

1. **`A(m)` as literally proposed is rejected on three independent grounds:**
    the data has no mass axis and the Groups' modal bins are the analysts' own
    counting defaults, not measurements (§1.2a–b — the same defect that
    discharged `mott-tail-shape.md`); `A` does not enter the drag/area path the
    brief's mechanism assumes (§2); and it is structurally self-referential
    inside `μ` (§2).
2. **The brief's premise of a separable "perforating tail" is false.**
    `m_thr = 0.166 g` against `μ = 0.929 g` means 66 % of fragments perforate
    (§4). There is no tail to treat separately from the bulk.
3. **But the investigation surfaced a real, distinct, sign-known defect in the
    shipped constant** (§2.1): eq. (2) needs an `x²`-weighted mean aspect ratio
    and is using a count-weighted one, and Table 3 shows `A` and size are
    strongly positively correlated, so the shipped `μ` is biased **low** —
    i.e. `N₀` biased **high**, the direction of the residual.
4. **Re-solving the chain (not ratioing) gives material leverage**: `c` in
    1.4–1.9 moves the gap from 2.25×/2.51× to 1.72×/1.91× … 1.33×/1.48×, i.e.
    plausibly inside the within-2× PASS band (§4). No prior discharged candidate
    on this thread had a sourced, sign-known lever of this size.
5. **It is a single-constant change** — closed-form, one line in `mott_params`,
    no new functional degrees of freedom, and it leaves §8's `C_shape` deferral
    untouched (§5).

**Main risk to state up front:** this correction is the same sign and family as
assumption **A9.1** (the uncorrected 1–2× `⟨x²⟩/⟨x⟩²` product-of-means factor).
A derivation that applies both without reconciling them will double-count.
Settling that is the derivation pass's first task, before any value is chosen.

**Actions, in order:**

- **A. Open a Workflow B derivation on option 1** in this same update folder
    (`derivation.md` beside this file). Its job: (i) reconcile with A9.1; (ii)
    derive `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩)` and bound it from Table 3 under an explicit,
    stated assumption about the Group size ladder — declared as an assumption,
    **not** presented as sourced; (iii) re-run the `drag-gap-1944` B(r) check at
    the new `μ` (§5); (iv) re-solve the count chain with
    `checks/aspect-ratio-moment-leverage.py`.
- **B. @librarian request — Gardner, S., *Analysis of fragmentation and
    resulting shrapnel penetration of naturally fragmenting cylindrical bombs*,
    Lawrence Livermore National Laboratory, 2000** (Felix 2022 ref [23]), the
    primary behind Fig. 10. Wanted specifically: fragment **mass** tabulated
    alongside fragment dimensions, and the shell identity (the brief's "155 mm
    M101" is unverified, §1.3). This is what turns (ii) above from a bounded
    assumption into a sourced point value, so it is **worth doing before the
    derivation if cheap** — but the derivation can proceed with a bound if not.
- **C. Do not open a challenge thread on `count-gap-1938` or edit
    `count-chain.md`** or its siblings. This is a new update; it references
    count-chain.md's 2.25×/2.51× FAIL as the residual it acts on. If the
    derivation lands, re-closing that thread is a *separate*, later decision for
    the human.
- **D. Leave the `[deferrable]` Mott/Linfoot finding standing** (§1.4). Not
    resolved by this pass.

**Fidelity target.** This aspect drives the perforating-fragment count
(`count-gap-1938`, currently FAIL at 2.25×) and, via `C_shape`, the mass-weighted
B(r) drag fit (`drag-gap-1944`). Tolerable error on a single global `A`: the
shipped 1.6 sits inside a 1.48–1.66 literature spread, so **±15% on `A`** is
acceptable — which propagates to ~±5% on presented area (`A^(1/3)`) and is well
inside both surfaces' noise. The unrepresented mass-dependence is a factor ~2.3
on `A` at the extremes, i.e. **outside** that band, which is why it is logged as
a limitation rather than declared immaterial.

---

## Verification status of this doc

- Table 3 values read from the checked-in CSV, which carries its own `.invariant`
    (row sums and published Total row); not re-typed from prose.
- §1.2 quotes are from the extraction
    `1-s2.0-S221491472030502X-main.md` lines 125–129 and 138.
- §4 is a scoping-grade symbolic bound, explicitly flagged as such; it was not
    computed from a ratio of published N values (the failure mode `count-chain.md`
    names) — `checks/aspect-ratio-moment-leverage.py` was run (verified
    2026-08-16, reproduces this table exactly) and re-solves `μ`, `N₀` and the
    survival factor from `c`, not just a scaled ratio. What it does **not** do is
    re-derive the baseline `μ₀ = 0.929 g`, `N₀ = 2681` from shell geometry — those
    are read from `count-chain.md`'s already-computed verdict row, not
    re-produced from `src/arty/fragmentation.py`'s own functions. If this
    candidate is ever revived, a derivation pass should re-run the full shipped
    chain end-to-end rather than reuse the cached baseline.
