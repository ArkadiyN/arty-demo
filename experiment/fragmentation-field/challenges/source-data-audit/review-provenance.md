# Provenance Review — does the primary say what it is cited as saying?

**Pass date:** 2026-08-03
**Reviewer:** @model-reviewer
**Gate discharged:** `.claude/rules/source-data-fidelity.md` → *Provenance*
("does the primary say what it is cited as saying?"). Transcription fidelity
and criterion-match are **not** in scope for this pass.

**Excluded by brief:** the BRL-126 / NWC TP 7124 "2740 ft/s" misattribution
(covered by a concurrent pass).

Verdict vocabulary per item: **yes** / **no** / **partially**.

______________________________________________________________________

## 1. DoD-1975 Figure 3 drag coefficient

**Verdict: PARTIALLY.**

- The corrected CSV **is** what Figure 3 shows, to RMS 0.003 in $C_D$ over 76
    sampled rows — the correction it makes to `figure-3-digitized.md` is
    confirmed independently. **Two rows** depart from the page: Mach 1.00 by
    $-0.024$ and Mach 2.60 by $-0.014$.
- `card.md`'s stated $C_D(M{=}1.0) = 1.23$ is **low by ~0.025** against the
    page; the page shows ~1.257.
- `card.md` **contradicts the report's own characterisation** of the transonic
    peak, in a section that should not be making the claim at all. This is the
    material finding of item 1.
- Four of the card's anchors are bare line numbers and **three point at the
    wrong content**; the figure-caption anchor used by the card, the
    `.invariant` and the trace script **greps to zero hits**.

### 1a. Is `tables/figure-3-drag-coefficient.csv` what Figure 3 shows?

**Method.** The committed CSV is produced by
`checks/dod-1975-figure-3-trace.py`, which renders `source.pdf` p.33 at 300 dpi
and traces the stroke using **four hard-coded axis pixel constants**
(`X0, X7 = 672.5, 2770.0`, `Y10, Y15 = 1878.0, 370.5`). Those constants are the
entire calibration and they are *asserted* in that script, not derived — so the
script's own closure cannot rule on them without circularity. I re-derived the
calibration from scratch on a **different file and a different pipeline**: the
extraction's own `images/figure-3-drag-coefficient-vs-mach.png`, locating the
six horizontal and eight vertical heavy rules from their dark-pixel fraction,
then re-tracing the stroke.

Check script: `checks/dod-1975-figure-3-independent-retrace.py`
(staged at `experiment/_scratch/dod-1975-figure-3-independent-trace.py` this
pass; retain per `.claude/rules/verification-scripts.md`).

**Calibration is independently confirmed.** The PNG's rules are evenly spaced
to within 1 px (rows 55…658 at 120.6 px per 0.1 $C_D$; cols 153…991.5 at
119.8 px per Mach), so both axes are linear and the axis box is what the two
scripts assume. The two pipelines' px-per-unit ratios agree to 3 significant
figures (299.64/119.86 = 2.500 in Mach; 3015/1206 = 2.500 in $C_D$).

**Agreement with the CSV.** Comparing every CSV row against a local cubic fit
of the PNG stroke (fitting *across* gridline columns rather than sampling
beside them):

```
76 rows compared; mean -0.0006   RMS 0.0034   max|d| 0.0243
rows with |CSV - page| > 0.010:
  Mach 1.00  CSV 1.233   page 1.257   -0.024
  Mach 2.60  CSV 1.280   page 1.294   -0.014
```

**The correction the CSV makes is confirmed.** Independently of the committed
trace, the PNG gives the peak at $C_D = 1.399$ at **Mach 1.47** (committed
trace: 1.400 at Mach 1.46), and $C_D(M{=}1.0) \approx 1.257$. The superseded
`figure-3-digitized.md` claims 1.14 at Mach 1.0 and a peak at Mach 1.4. Both
of its errors are real and in the recorded direction. The `SUPERSEDED` banner
and the blocking finding on that file are **correct and should stand**.

### 1b. The Mach-1.00 row — a defect the closure invariant cannot see

**Mechanism.** `dod-1975-figure-3-trace.py` skips every pixel column within
±10 px of a **half-Mach gridline** (`grid = [X0 + 0.5*k*(X7-X0)/7 for k in range(15)]`), then `at(m)` accepts the nearest surviving column within ±12 px.
So every row at a multiple of 0.5 Mach is actually read **0.033–0.040 Mach
away** from its label. That is harmless where the curve is flat and material
only on the transonic rise, where the local slope is ~1.2 $C_D$ per Mach:
0.03 Mach of x-displacement becomes ~0.03–0.04 in $C_D$. The CSV's own
neighbours show the artifact directly — the increments 0.90→0.95→1.00→1.05
run $+0.035, +0.012, +0.057$, i.e. the 1.00 row sits off the smooth curve its
neighbours define.

**Why the `.invariant` passes anyway.** Its three pinned features — subsonic
plateau ($M \le 0.45$), peak ($1.40 \le M \le 1.55$), supersonic plateau
($M \ge 3.0$) — all sit where $\mathrm{d}C_D/\mathrm{d}M \approx 0$. **A
closure pinned only on flat segments of a curve is blind to an
x-displacement defect**, which is exactly the defect present. The invariant's
claim that "a calibration error large enough to matter cannot leave all three
intact" is true for a *calibration* error and false for this one; the
`.invariant` overstates what it certifies.

**Impact.** 0.024 in $C_D$ at one Mach point = **1.9%**, against a superseded
error of 0.082 (6.6%) that it replaced. It does not reverse any conclusion:
both 1.233 and 1.257 refute the eyeballed 1.14 and both support the same
transonic-rise shape. But it is a wrong number in a committed artifact, and the
published band `cd_lo..cd_hi = 1.222..1.243` **excludes** the page value 1.257,
so the band is wrong there too and cannot be read as covering it.

FINDING\[blocking\]: figure-3-drag-coefficient.csv row mach=1.00 reads cd=1.233 where the page shows ~1.257, and its cd_lo..cd_hi band excludes the page value; cause is the trace's +-10px half-Mach-gridline exclusion sampling ~0.035 Mach off-label on the steepest part of the curve, and the .invariant is blind to it because all three pinned features sit on flat segments (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/figure-3-drag-coefficient.csv, doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/figure-3-drag-coefficient.invariant, doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md, experiment/fragmentation-field/challenges/source-data-audit/checks/dod-1975-figure-3-trace.py; since: 2026-08-03)

**Suggested correction (do not apply here).** In `at(m)`, interpolate across
the excluded gridline band from clean columns on both sides instead of
snapping to the nearest surviving column; regenerate with `--write`. Add a
fourth invariant row pinned on a **steep** segment — e.g.
`row: (cd if 0.98 <= mach <= 1.02 else 1.257) == 1.257 within 0.015` — so the
closure can see an x-shift at all. Update `card.md`'s "At M = 1.0 the curve is
at **1.23**" to the corrected value.

### 1c. Does `card.md` carry interpretive / recommendation material?

**Yes — and one sentence contradicts the primary it cites.**

Section **"Data Content"**, the *Peak* bullet:

> **Peak (M = 1.46):** $C_D = 1.400$ — the local peak near sound speed
> mentioned in the text is a real ~9% bump above the supersonic plateau, **not
> a minor wiggle**.

The report's own text, `10-F-0806_Fragment_and_Debris_Hazards.md` (greppable
anchor: `supersonic value of 1.28`; the sentence immediately preceding it),
says the opposite:

> "A plot of drag coefficient C_D against Mach number appears in Figure 3. Its
> variation with Mach number between subsonic and supersonic speeds is seen to
> be **rather modest despite a peak near the sound speed**. A useful
> approximation for many applications is to take the drag coefficient as
> constant at its supersonic value of 1.28."

This is the `#card-as-modelling-claim` shape in its most damaging form: the
card cites the text ("mentioned in the text") while asserting the **negation**
of the text's characterisation. The arithmetic is fine — 1.400/1.280 = 1.094,
so "~9%" is right — but "a real … bump, not a minor wiggle" is a *materiality
judgement* about whether Mach-dependent drag is worth modelling. That judgement
belongs in `derivation.md`, where @model-reviewer sees it, not in a reference
card that @modeler inherits as a premise and nobody reviews.

**Impact.** `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/`
is a live thread that decided exactly this question. A premise document that
tells the reader the source's peak is "not a minor wiggle", when the source
calls the variation "rather modest", biases that decision in one direction
while appearing to be transcription. It does not change a rendered number
today, because the thread landed on constant $C_D = 1.28$ — the direction the
*source* favours — but it is a wrong attribution in a committed artifact.

FINDING\[blocking\]: card.md's Peak bullet says the transonic peak is "not a minor wiggle" and attributes it to the text, but the source says its variation with Mach is "rather modest despite a peak near the sound speed" - the card asserts the negation of the sentence it cites, and the materiality judgement belongs in derivation.md not a reference card (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md; since: 2026-08-03)

**Suggested correction.** Reduce the bullet to what the page shows — "Peak
($M = 1.46$): $C_D = 1.400$, 9.4% above the supersonic plateau. The report
characterises the whole subsonic-to-supersonic variation as 'rather modest
despite a peak near the sound speed' and recommends the constant 1.28." Move
any argument about whether 9.4% is material into
`updates/mach-dependent-fragment-drag/derivation.md`.

Two lesser instances in the same file, both **Note** tier:

- **"Applicability & Caveats" → Use:** *"this 1.28 value and curve are standard
    reference for 1970s–era U.S. military ordnance hazard assessment;
    applicability to naturally-fragmenting artillery shells depends on fragment
    geometry assumption validation."* This is a "what it is good for" section,
    but it ends in a **referral** rather than a recommendation, which is the
    safe shape the rule allows. Leave it.
- **"Velocity range:** … figure **presumably** covers ~0–Mach 7." The hedge is
    unnecessary and is the "hedging inside a card" pattern — the axis is
    printed 0 to 7 and I verified it. Replace "presumably covers" with "is
    plotted over".

### 1d. Prose claims that DO check out

Verified against the extraction, all faithful:

| Card claim                                                                                                      | Source                                                                                                                                                                                         | OK                                              |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| method: fragments recovered from detonation tests fired from a smooth-bore launcher, velocity decay vs distance | "determined experimentally as a function of Mach number by firing fragments recovered from detonation tests from a smooth-bore launcher, and observing the decrease of velocity with distance" | yes ("static" is the card's addition; harmless) |
| $k = 2.6$ g/cm³ = forged-steel projectile/bomb average                                                          | "for forged steel projectiles and fragmentation bombs the average value of 660 grains/in.3 (2.60 g/cm3) has been recommended"                                                                  | yes                                             |
| icosahedron gage / mean presented area = ¼ surface area for convex bodies                                       | present verbatim in the same section                                                                                                                                                           | yes                                             |
| $L = 2k^{2/3}m^{1/3}/(C_D\rho)$                                                                                 | source prints $L = 2(k^2m)^{1/3}/(C_D\rho)$ — algebraically identical                                                                                                                          | yes                                             |
| $L_1 = 247$ m/kg^{1/3} for $k=2.6$, $C_D=1.28$                                                                  | stated verbatim                                                                                                                                                                                | yes                                             |
| 1.28 is what the report recommends as a simplification                                                          | "A useful approximation for many applications is to take the drag coefficient as constant at its supersonic value of 1.28"                                                                     | yes                                             |
| original data = ref 10 = Dunn & Porter, *Air Drag Measurements of Fragments*, BRL MR 915, Aug 1955              | footnote marker `10` on the method sentence; reference list entry matches verbatim                                                                                                             | yes — but see below                             |

**Secondhand marking.** Everything the card says about *how* the drag curve was
measured is DoD-1975 paraphrasing **Dunn & Porter, BRL MR 915 (1955)**, which
is not in `doc-reference/`. The card presents it as method fact. Per the
provenance gate this must be **marked secondhand** in the card ("as reported by
DoD-1975 from ref. 10; BRL MR 915 not held"), not corrected — the attribution
chain is internally consistent, it is simply unverified at the primary.

FINDING\[note\]: card.md states Figure 3's experimental method and shape-factor provenance as fact, but all of it is DoD-1975 paraphrasing Dunn and Porter BRL MR 915 (1955), which is not held in doc-reference; mark the Source and Test Conditions section secondhand rather than correcting it (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md; since: 2026-08-03)

### 1e. Anchors

The rule requires greppable strings and says to run the grep at authoring time.
Neither was done here.

| Anchor as written                                                                                                                              | Where it actually is                                                                | Status          |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------- |
| `Figure 3  Drag Coefficient of Fragments` (double space) — in `card.md`, `figure-3-drag-coefficient.invariant`, and the trace script docstring | extraction has `### Figure 3 Drag Coefficient of Fragments`, **single** space, L728 | **0 grep hits** |
| `anchor L320–L327` for the Ballistic Properties method                                                                                         | method sentence is L331–339; L320/L327 land in the shape-factor paragraph           | wrong           |
| `L293–L315` for $m = kA^{3/2}$ / icosahedron gage                                                                                              | L293 is the FRAGMENT BALLISTICS intro; the gage text is L302–L314                   | partly wrong    |
| `p. 9, L346` for $L_1 = 247$                                                                                                                   | L346 is the exponential `v = V exp(-R/L)`; the 247 statement is **L358**            | wrong           |
| `(L550)` for the Dunn & Porter reference — **bare line number, no page**                                                                       | the reference is at **L575**                                                        | wrong, and bare |

`supersonic value of 1.28` (L339) is the one anchor in the folder that is a
real greppable string and resolves correctly. Use it as the model.

FINDING\[deferrable\]: DoD-1975 card.md uses four bare line-number anchors (L293-L315, L320-L327, L346, L550) of which three point at the wrong content, and the figure-caption anchor "Figure 3 Drag Coefficient of Fragments" is written with a double space and greps to zero hits in the extraction - it is repeated verbatim in the .invariant and in dod-1975-figure-3-trace.py's docstring (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/card.md, doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/figure-3-drag-coefficient.invariant, experiment/fragmentation-field/challenges/source-data-audit/checks/dod-1975-figure-3-trace.py; since: 2026-08-03)

______________________________________________________________________

## 2. Gold 2017 eq. (6) shape-absorbed γ

**Verdict: YES.** The card's claim —

> **Gold's `γ = 50` is the shape-absorbed γ of eq. (6), not `γ′`.** Gold never
> states α for Charge A, so his 50 cannot be converted to a `γ′`.
> (`card.md`, "What is *not* certified")

— is **exactly what the primary says**, on all three of its parts: the
definition, the slot the 50 enters, and the unavailability of the conversion.

### 2a. The substitution closure

Check script: `checks/gold-2017-eq6-substitution-closure.py`
(staged at `experiment/_scratch/gold-2017-eq6-substitution-closure.py`;
retain per `.claude/rules/verification-scripts.md`). Runtime \<1 s.

The paper states the two substitutions verbatim (greppable anchors, both in
`1-s2.0-S221491471730079X-main.md`):

- `Substituting equation (2) into equation (4) results in` → eq. (5)
- `allows equation (5) to be put in a simpler and more useful form` → eq. (7),
    via eq. (6)

Performing them, evaluated at 2000 random positive parameter points so a
coincidence at one point cannot pass:

```
eq (2) into eq (4)  ==  eq (5) as printed    PASS   worst rel. residual 1.09e-15
eq (6) into eq (5)  ==  eq (7) as printed    PASS   worst rel. residual 6.92e-16
eq (7)              ==  eq (16) as printed   PASS   worst rel. residual 5.93e-16
```

By hand, the first one: eq. (2) gives
$x_0^3 = (2\sigma_F/\rho\gamma')^{3/2}(r/V)^3$; eq. (4) is
$\mu = \tfrac12\alpha\rho x_0^3$, so
$\mu = \tfrac12\alpha(2\sigma_F)^{3/2}\rho^{-1/2}\gamma'^{-3/2}(r/V)^3$. The
printed eq. (5),
$\tfrac12\big(2\sigma_F/(\rho^{1/3}\alpha^{-2/3}\gamma')\big)^{3/2}(r/V)^3$,
expands to $\tfrac12\,\alpha\,(2\sigma_F)^{3/2}\rho^{-1/2}\gamma'^{-3/2}(r/V)^3$
— **identical**, with the $\alpha^{-2/3}$ raised to the $3/2$ producing exactly
the $\alpha^{+1}$ that eq. (4) contributes. This is the closure form the rule
prescribes for an unreliable-glyph document: it never reads a disputed
character, and a vision error in **any one** of eqs. (2), (4), (5), (6), (7),
(16) would break the identity. All six are therefore mutually certified.

### 2b. Is `γ = 50` the eq.-(6) γ or the bare γ′?

Three independent lines all say the eq.-(6) γ:

1. **The paper's own motivation for eq. (6)**, verbatim: *"Since the fragment
    distribution relationship (see equation (1)) warrants knowledge of the
    average fragment mass **but not the shape**, introducing [γ = α^{-2/3}γ′]
    allows equation (5) to be put in a simpler and more useful form."* The
    whole purpose of γ is to be the constant that no longer carries α.
1. **Where the 50 is used.** `γ = 50` occurs at exactly two places in the
    document (L190 and L220), both feeding the multi-region model eq. (19)/(21).
    Eq. (21) is $\mu_{kj} = \sqrt{2/\rho}\,(\sigma_{Fk}/\gamma_k)^{3/2}(r_j/V_j)^3$
    — the eq. (16) ≡ eq. (7) form, i.e. the **shape-absorbed slot**. There is no
    equation in the paper into which a γ′ could be substituted numerically.
1. **γ′ is never given a value.** It occurs exactly **4 times** in the whole
    document (L58 eq. 2, L60 its definition, L74 eq. 5, L78 eq. 6) and carries
    a number at none of them. Likewise the shape α: it occurs at L70, L72, L74,
    L78 and is never assigned a value. So the conversion
    $\gamma' = \alpha^{2/3}\gamma$ is genuinely unavailable, as the card says.

Corroborating: ref. [18] is titled *"An effect of the explosive detonation
pressures on the PAFRAG-Mott fragmentation parameter **γ**"*, and Fig. 7(a)
plots *"Empirical **γ** versus explosive detonation pressures"* — the
empirically-tabulated family that 50 belongs to is the γ family.

**Magnitude of getting this wrong.** With $\gamma = \alpha^{-2/3}\gamma'$,
misreading 50 as a γ′ is exact only at the cube limit α = 1. At α = 2 it
understates γ′ by 37%; at α = 0.5 it overstates by 59%. The shape-closure
derivation's own registry runs α = 3.4–6.1
(`updates/mott-fragment-shape-closure/derivation.md:140`), i.e. a factor
$\alpha^{2/3}$ of 2.3–3.3 — so the confusion would be a **2–3× error in γ′**,
not a rounding matter. The card's guardrail is load-bearing and correct.

The descendant derivation reads it correctly: `(G6) γ ≡ α^{-2/3}γ′ — shape absorbed into a redefined constant` and the cube-limit sanity check
(`α = 1 → γ = γ′`) at `derivation.md:134`. No defect found downstream.

### 2c. New trap: the paper uses **α for two different quantities**

This is not currently flagged anywhere in `card.md` (grep for `incidence`
returns nothing) and it is the kind of thing that produces a sign flip.

- **§2, eq. (4):** $\alpha = (l_0/x_0)\cdot(t_0/x_0)$ — a dimensionless
    **shape** aspect-ratio product of the idealised parallelepiped. Enters eq.
    (6) as $\gamma = \alpha^{-2/3}\gamma'$, so **larger α → smaller γ**.
- **§4, L212 and the Fig. 7 caption L218:** α is the *"incidence angle between
    the detonation wave direction and the shell surface normal"*, and the
    caption reads *"Parameter γ is a function of the detonation shock wave
    incidence angle α, and varies along the shell. **The steeper angle α is,
    the higher parameter γ is.**"* — so **larger α → larger γ**.

Same symbol, unrelated quantity, **opposite** stated sense of the γ–α
dependence. A future pass grepping Gold for "α" to find a shape factor lands on
Fig. 7(b), reads a stated γ(α) relation, and would take the sign of eq. (6)
backwards. The card's "Gold never states α for Charge A" is true of the *shape*
α and false-looking of the §4 α; it needs the disambiguation to be safe as a
premise.

FINDING\[deferrable\]: Gold 2017 uses the symbol alpha for two unrelated quantities - eq.(4)'s fragment shape aspect-ratio (larger alpha lowers gamma) and section 4's detonation-wave incidence angle (Fig. 7 caption: steeper alpha raises gamma) - and card.md does not disambiguate them, so a future pass looking for "Gold's alpha" can land on Fig. 7(b) and take the sign of eq. (6) backwards (affects: doc-reference/fragmentation/fragment-size-distribution-conwep/card.md, experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md; since: 2026-08-03)

### 2d. Card-as-modelling-claim check on this card

`card.md` here is unusually disciplined — it labels its uncertified regions and
declines to recommend a calibration. Three passages are nonetheless the wrong
shape for a reference doc. All three are, as far as I can check, **factually
correct**; the objection is structural (they are reviewed by nobody), so
**Note** tier:

- **"### The shipped code"** — describes `mott_params`' internal call chain and
    reports agreement to $2\times10^{-16}$. That is a code-verification result,
    not a statement about the source.
- **"### The paper contradicts itself on N₀, and the code takes the right
    side"** — *"At the shipped M1 geometry the gap is 3 959 vs 7 918 fragments
    at V₀ = 1000 m/s"* is a **computed model output** sitting in a reference
    card, and *"there is nothing to repair"* is a correctness verdict. The
    underlying observation (eq. 1 `N₀ = M/2μ` vs eq. 17 `N₀ⱼ = mⱼ/μⱼ`) is a
    genuine, correctly-identified internal contradiction of the source and
    **should stay** — it is what the source says. Its resolution and the
    fragment counts belong in `derivation.md`.
- *"That reading is sound"* (of `_validation.qmd:48`) — a card endorsing
    another artifact's interpretation. `.qmd` files are outside this pass's read
    set, so I did not verify the cited line; the endorsement itself is the
    misplaced claim.

FINDING\[note\]: Gold card.md sections "The shipped code" and "The paper contradicts itself on N0..." carry code-verification verdicts and a computed model output (3959 vs 7918 fragments at V0=1000 m/s), and the "What is not certified" bullet endorses \_validation.qmd:48's reading as sound - all correct but reviewed by nobody in a card; move the resolutions to derivation.md and leave only the source's own eq.(1)/eq.(17) contradiction in the card (affects: doc-reference/fragmentation/fragment-size-distribution-conwep/card.md; since: 2026-08-03)

## 3. Tolch 1938 "Drag Model Relevance"

**Verdict: NO.** The primary does not say what the card cites it as saying. The
card recommends, as the anchor for a *drag* calibration check, the one axis of
the report that the report itself attributes to **vector addition of the
shell's own velocity** — while the axis the report explicitly attributes to
**air resistance** (panel radius) is the one the card does not mention.

The section must **move out of `doc-reference/`**. Its destination already
exists: `experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md`,
which holds the correct assessment of both axes. What may remain in `card.md`
is a **referral**, not a recommendation.

### 3a. What the card claims

`card.md:57–59`, the whole of section **"Drag Model Relevance"** (the heading
is itself a what-it-is-good-for framing):

> **Drag Model Relevance**
>
> This document provides **direct velocity-dependence measurements**
> (700–2,130 f/s) for fragment density on the 75mm M48 shell. The sharp
> collapse of base-spray density (93% reduction, static → 2,130 f/s,
> table-sourced and high-confidence) and expansion of nose-spray density with
> increasing remaining velocity **enables calibration checks on whether the
> project's drag model under-decelerates fragments relative to this report's
> ground truth**. The cumulative velocity-distribution figure that would anchor
> this most directly is unresolved (see above) — **use the table-based density
> collapse instead**, which does not depend on that sentence.

Three separable claims: (i) the velocity axis is a *fragment* velocity-
dependence measurement; (ii) the base-spray collapse can calibrate fragment
drag; (iii) an imperative telling the reader which observable to use.

### 3b. Claim (i) — the axis is the *shell's* velocity, and the source says so twice

The report states its independent variable in its own methods section
(greppable anchor: `the direction from the burst, the distance, and the remaining velocity of the shell`, `tolch-1938.md:158`; restated at `:152`):

> "determining the fragment density as a function of three variables, namely,
> the direction from the burst, the distance, and **the remaining velocity of
> the shell**. […] The variable of remaining velocity as regards fragment
> density was measured by **bursting the shell within the panels at various
> remaining velocities**."

`:182` fixes it as a firing condition, not a fragment property: *"The remaining
velocity of shell used in battle will in most instances be around 800 to 900
f/s."* The folder's own `tables/base-spray-density.invariant` already records
this in capitals — *"`v_fps` is the shell's AVERAGE REMAINING VELOCITY AT BURST
(a firing condition), NOT a fragment velocity"* — so the card contradicts a
sibling file in its own directory.

Claim (i) is **false as written**. "Direct velocity-dependence measurements"
for *fragment density* is true; the reader inference the section then builds on
it — that the velocity is a fragment velocity subject to drag — is not.

### 3c. Claim (ii) — the source attributes the collapse to vector addition, not drag

`tolch-1938.md:853–857` (anchor: `have the same line of action`):

> "For all practical purposes, the velocity component of the base fragments due
> to the explosive charge and the velocity component due to the remaining
> velocity of the projectile **have the same line of action**, and hence the
> resultant fragment velocity is simply the **algebraic sum** of the two
> components. Since the two components are of opposite sign, as the remaining
> velocity becomes large, a great many of the fragments lose their ability to
> mark the panels because of their **reduced resultant velocity**."

There is no drag term in the source's explanation of the 93% collapse. The
mirror statement for the nose spray is at `:913` ("arithmetic sum"), and the
side-spray forward sweep 95° → 55° is the same vector sum resolved in angle
(`:849`).

Meanwhile the source *does* name an air-resistance axis, and it is a different
one — `tolch-1938.md:804` (anchor: `Since the fragments lose velocity in flight due to air resistance`):

> "Since the fragments lose velocity in flight due to air resistance, their
> ability to mark the panels decreases with **the distance**."

So the card has **swapped the report's own two attributions**: it recommends
the velocity axis (which the source explains by vector addition) for drag, and
is silent on the distance axis (which the source explains by air resistance).
That is the provenance failure, and it is not a matter of emphasis — both
attributions are explicit, one sentence each.

**The degeneracy is exact, not merely "near-".** This sharpens the existing
finding. Under the constant-$C_D$ exponential decay the project uses,
$v(R) = V\exp(-R/L(m))$ with $L$ a function of fragment mass alone. Tolch's
velocity sweep is taken at **fixed panel radius** (Panel A, 15 ft). The drag
factor $\exp(-R/L(m))$ therefore takes the *same value at every point of the
sweep* — it is independent of the shell's remaining velocity, because
exponential decay in $R$ carries no velocity dependence. It folds entirely into
the effective marking-threshold mass $m_{\text{thr}}$, which is a fitted
quantity (the 1"-spruce ballistic limit is not in `doc-reference/`). Hence the
predicted collapse curve $\sigma(V_{\text{rem}})/\sigma(0)$ is **invariant
under any rescaling of $C_D C_{\text{shape}}$** once the threshold is refitted.
No amount of data quality on this axis can calibrate drag. By contrast the
lever the axis *does* pull is large: the base-spray resultant runs
$V_{\text{charge}} - V_{\text{rem}} \approx 838 \to 189$ m/s, a factor 4.4.

This is consistent with, and stronger than, the empirical result on the axis
that *does* carry drag: `challenges/drag-gap-1944/tolch-1938-panel-distance.md`
Result 1 found the panel-radius falloff already degenerate over a 5× span of
$C_D C_{\text{shape}}$ (residuals flat at −0.10/−0.08). If the source's own
air-resistance axis cannot discriminate drag, the vector-addition axis
certainly cannot.

**The one nuance, so a future pass does not over-swing.** `tolch-1938.md:1371`
is the single place the report attaches a drag-flavoured reading to the
velocity axis: *"Since small fragments have small ballistic coefficients, it is
assumed that as the fragments lose velocity due to shell velocity, the smaller
base fragments are no longer able to mark the panel."* That is a claim about
the **fragment-size distribution of surviving marks** (Plots 45/46), not about
the density collapse — a different observable, which the card neither cites nor
recommends, and whose drag content is the same fixed-$R$ factor shown degenerate
above. It does not rescue claim (ii).

**Confirming from the third direction.** The report's own fragment velocities
were themselves *computed from* this geometry (`:146`, `:1658`, `:1698`), so
the report contains no independently-measured fragment velocity anywhere on
this axis. Note the geometric inference reads a spray *angle*, and drag
decelerates along the velocity vector without rotating it — so that inference
is drag-free by construction. Every number the card draws from the velocity
sweep is therefore drag-free at the source.

### 3d. Claim (iii) and the structural ruling — this section cannot live in a card

Independently of being wrong, the section is the `#card-as-modelling-claim`
shape in its most explicit form. `.claude/rules/source-data-fidelity.md`: *"A
section telling a reader what a source is good for — which calibration to
anchor on it, which of its curves to prefer — is a modelling claim wearing a
reference doc's clothes."* The card contains all three prohibited moves:

- a **purpose framing** in the heading itself — "Drag Model Relevance";
- a **capability assertion** about *this project's* model — "enables
    calibration checks on whether the project's drag model under-decelerates
    fragments relative to this report's ground truth". `card.md` is not
    supposed to know that the project has a drag model;
- an **imperative choosing between the source's observables** — "**use the
    table-based density collapse instead**".

The third is the sentence that did the damage: it is read by @modeler as a
premise, and it is reviewed by nobody. Note the section is *load-bearing in the
wrong direction* — it correctly withholds the unresolved cumulative
distribution (a genuine caution) and then redirects the reader to a
substitute that cannot answer the question at all, which reads as
conservatism while removing the reader's chance to notice the axis is wrong.

**Where it belongs.** The assessment already exists, correctly, at
`experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md`
(Finding 1 rules the velocity axis out; Finding 2 identifies the panel-radius
axis as the usable one). Nothing needs to be re-derived — the card's section
should be **deleted**, not corrected in place, and replaced with a referral of
the shape the rule permits:

> **## Transfer question**
>
> This report's independent variables are direction from burst, panel radius,
> and the **shell's remaining velocity at burst** (a firing condition — see
> `tables/base-spray-density.invariant`). The report attributes density change
> along the velocity axis to algebraic addition of shell velocity to charge
> velocity (anchor: `have the same line of action`) and density change along
> the radius axis to air resistance (anchor: `Since the fragments lose velocity in flight due to air resistance`). Which — if either — matches a given model
> quantity is a **criterion-match question**, not settled here; see
> `experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md`.

**Impact.** No rendered output changes today: the panel-distance assessment
already reached the right answer independently and did not act on the card's
recommendation. The exposure is forward-looking and real — the card is the
premise document for the next `mott-scale-gap` / drag pass, and it currently
instructs that pass to spend itself on an exactly-degenerate observable.

### 3e. The existing register entry — upheld, not duplicated

`OPEN-FINDINGS.md` already carries, from 2026-08-02
(`ledger.md:585`), a **blocking** marker for the axis error itself:

> *(blocking; quoted here without its marker syntax so the collector does not
> double-register it — the live marker is at `ledger.md:585`)*
> card.md's "Drag Model Relevance" section recommends the
> velocity-sweep density collapse as the drag calibration anchor, but that axis
> is the shell's velocity at burst — a burst-geometry observable,
> near-insensitive to fragment drag

That marker is **correct and must stand**; §3b–3c above are its independent
confirmation at the primary, and §3c upgrades "near-insensitive" to *exactly
degenerate at fixed panel radius under constant $C_D$*. I do not re-register
it. The marker below is the **structural** ruling it does not contain — that
the section cannot remain in `doc-reference/` even once its physics is
corrected, and where it goes instead.

Likewise **not** re-registered here: the bare-line-number anchors (the
2026-08-03 20-anchor entry covers this card; I confirmed the pattern holds in
the section under review — `card.md:8` cites "lines 94–106" where L94/L96/L106
are the title-page headings `## AD` / `## REPORT NO. 126` / `## December 1938`, and `card.md:12` cites "line 117" for battle velocity where L117 is
`### U.S. ARMY ABERDEEN RESEARCH AND DEVELOPMENT CENTER` and the claim is at
**L182**), and the `2,750 f/s` OCR glyph at `card.md:49` (covered by
`review-void-rulings.md`).

FINDING\[blocking\]: the Tolch card's entire "Drag Model Relevance" section (card.md:57-59) is a modelling recommendation in a reference document - it frames the source by purpose, asserts a capability about this project's drag model, and issues the imperative "use the table-based density collapse instead" - so it must be deleted from doc-reference/ and replaced by a referral naming the criterion-match question and routing to experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md, which already holds the correct two-axis assessment; this is the structural ruling that the 2026-08-02 axis-correctness marker does not cover (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md, experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md; since: 2026-08-03)

### 3f. Two collateral provenance defects in the same section

**Wrong surface behind "high-confidence".** The card sources the collapse as
*"table-sourced and high-confidence"*, citing `[table, lines 617–627](tolch-1938.md#L617-L627)`
(`card.md:26`). That surface is the folder's own declared-corrupted extraction:
`tables/base-spray-density.invariant` states *"the values in `../tolch-1938.md`
are OCR output and are WRONG in ~20 of 54 component cells […] the markdown is
the corrupted copy."* It is wrong in **this very table** — the markdown at
`tolch-1938.md:898–905` prints Panel B at 2 130 f/s as **3.12** where
`tables/base-spray-density.csv` has **1.12**, and Panel C at 1 085 f/s as
**0.65** where the CSV has **0.85**. The 3.12 also breaks the source's own
stated trend (`:1682`, *"Most of the base spray drops out"*), rising above the
1 085 f/s value. The two Panel-A digits the card actually quotes — 9.71 and
0.70 — **are** correct against the CSV, so no number changes; the defect is
that a confidence label is attached to a surface the same folder certifies as
unreliable, and the citation points away from the authoritative CSV. Adjacent
to but distinct from the existing "tolch-1938.md remains a citable surface"
entry, which is about the file, not about a card claiming confidence in it.

FINDING\[deferrable\]: Tolch card.md:26 calls the base-spray collapse "table-sourced and high-confidence" while anchoring it at tolch-1938.md#L617-L627 rather than tables/base-spray-density.csv, and that markdown is the surface base-spray-density.invariant declares corrupted in ~20 of 54 cells - it misprints two cells of this same table (2130 f/s Panel B 3.12 vs CSV 1.12, breaking the source's own stated monotone drop-out; 1085 f/s Panel C 0.65 vs CSV 0.85); the two Panel A values the card quotes, 9.71 and 0.70, are correct so no downstream number moves (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md; since: 2026-08-03)

**The 2 750 / 3 030 f/s are computed, and the card presents them as measured.**
`card.md:47–53` heads them *"Fragment Velocities (Charge Components)"* with a
bare citation, no statement of how they were obtained. The source is explicit
three times (`:146`, `:1658`, `:1698`) that they were *computed from the change
in the angle of the sidespray with remaining velocity* — a geometric inference
from the same axis §3b concerns, not an independent velocity measurement. The
omission has already propagated: `challenges/drag-gap-1944/tolch-1938-panel-distance.md:134`
uses 838.2 m/s as *"Tolch's own **measured** perforating-fragment velocity"*.
Impact is bounded — that check's own Result 1 found all three $V_0$ candidates
indistinguishable, so no conclusion moves — but the value is not what it is
labelled, and a future pass could treat it as an independent Gurney check,
which it is not. Distinct from the `card.md:49` glyph finding, which concerns
the third digit; this concerns the derivation chain behind all four.

FINDING\[deferrable\]: Tolch card.md:47-53 presents 2,750 / 3,030 f/s under "Fragment Velocities (Charge Components)" without recording that the source states three times (tolch-1938.md:146, :1658, :1698) that they were computed from the change in the sidespray angle with remaining velocity, not measured - so they are a geometric inference off the burst-geometry axis and carry no drag or independent-Gurney content; challenges/drag-gap-1944/tolch-1938-panel-distance.md:134 already calls the 838.2 m/s value "Tolch's own measured perforating-fragment velocity" (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md, experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md; since: 2026-08-03)

### 3g. What in the section does check out

- The 93% figure itself: 1 − 0.70/9.71 = 92.8% against
    `tables/base-spray-density.csv`. Correct.
- The nose-spray rise 16.09 → 21.45 direction is what the source states
    (`:944`, *"The perforations per unit solid angle increase markedly with
    increase in remaining velocity"*). Correct in direction.
- The card's decision to **withhold** the cumulative velocity distribution
    (`card.md:27–30`) is right and well argued: the vision reading at
    `tolch-1938.md:907` is "20% … 15% … 25% … 18% … 7%", non-monotonic and
    therefore provably wrong on at least one digit for a cumulative
    distribution. This is the one place in the section behaving as a reference
    document should — it states what the source shows, states why it cannot be
    trusted, and does not recommend. It is the model for the rest.

______________________________________________________________________

## Pass summary

| Item                                  | Verdict   | Must move out of `doc-reference/`?                                                                                             |
| :------------------------------------ | :-------- | :----------------------------------------------------------------------------------------------------------------------------- |
| 1. DoD-1975 Figure 3 drag coefficient | PARTIALLY | yes — the *Peak* bullet's materiality judgement → `updates/mach-dependent-fragment-drag/derivation.md`                         |
| 2. Gold 2017 eq. (6) shape-absorbed γ | YES       | partly — code-verification verdicts and computed counts → `derivation.md`; the source's own eq.(1)/eq.(17) contradiction stays |
| 3. Tolch 1938 "Drag Model Relevance"  | **NO**    | **yes — whole section** → `challenges/drag-gap-1944/tolch-1938-panel-distance.md`, leaving a referral                          |
