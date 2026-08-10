# Sourcing the wood perforation threshold for `min_lethal_mass` — scoping

**Status: scoping only.** No `src/arty/` change, no derivation. This pass
audits one new source (Sanborn et al. 2019) against the requirement stated in
[`../../challenges/count-gap-1938/count-chain.md`](../../challenges/count-gap-1938/count-chain.md)
§5 and returns a verdict plus a ranked set of options.

**Headline verdict: PARTIAL CLOSE, and not by the route the brief expects.**
Sanborn 2019's *own calibrated constants* cannot supply $E_{thr}$ — they carry
no identifiable fragment-mass or presented-area dependence, and their stated
validity floor is 4× thicker than Tolch's panels. What the paper *does* supply
is (a) a verbatim restatement of the **original UFC 4-023-07 wood-perforation
equation**, which is THOR-derived, calibrated on *thin solid wood*, and
explicitly mass- and diameter-dependent — i.e. the thing §5 actually asked for;
and (b) an independent, quantitative statement of that equation's known bias.
The correct close is therefore **UFC 4-023-07 as primary, with Sanborn 2019 as
the corroborating/bounding secondary**. @librarian is still needed, for one
short, freely-available document.

______________________________________________________________________

## 1. Problem statement

`min_lethal_mass` (`src/arty/fragmentation.py:412`, vectorised twin
`build_mmin_table` at :592) bisects fragment mass $m$ against a **binary
kinetic-energy threshold** $E_{thr}$:

$$\tfrac12 m\,\bigl(V_0 e^{-\lambda(m)s}\bigr)^2 \;\ge\; E_{thr}
\quad\Longrightarrow\quad m_{min}(s). \qquad (1)$$

Two distinct consumers pass different values into the same slot:

| Consumer | Value | Provenance |
| --- | --- | --- |
| Shipped demo (`E_LETH_DEFAULT`, :581) | 1000 J | ES-310 personnel-incapacitation anchor — **sourced**, not in scope here |
| `count-gap-1938` panel-perforation arm | 1.9–3.6 J | **fitted to the very falloff curve the test checks** |
| ditto, non-fitted probes | 78.6 J, 126 J | 1944 Ordnance card; Tolch hole-size bound |

The defect is confined to the second row. Tolch (1938) counted perforations of
**1″ (25.4 mm) softwood panels**; the model decides perforation by a mass-
independent KE step whose location was tuned on Tolch's own $B(r)$ falloff.
That makes the count comparison **compound** — the model is being validated
against data one of its parameters was fitted to. Sourcing $E_{thr}$
independently is what converts §4's test into a prediction with zero free
parameters.

**Standing of this pass (count-chain §4, re-closure of 2026-08-08).** The count
arm of the PASS test is already **met or marginal** at the two non-fitted
thresholds ($N/779$ = 1.73–2.00, $N/700$ = 1.92–2.23, band is 2×) under the
shipped $\gamma'$ = 54.5 and fixed $V_0$. So this is a **confirmation pass**,
not a rescue: it discharges the compound-test objection and lets the *second*
PASS condition (A→D falloff ratio within 0.10 of 0.557) stop being circular. It
is **not** licence to re-open C2 (out of scope, deferred).

Two framing corrections carried in from open findings against the surrounding
thread, which this doc does not repeat: count-chain's "essentially all of that
excess is the threshold fit" overstates the threshold-fit share (its own banner
splits 3.2–3.7× into ~1.65–2.05× threshold artefact and a comparable genuine
spectrum residual); and the criterion-clean rebaseline figure is **2.15×**
(block E), not 2.28× (block D).

### What a physically correct criterion looks like

A KE step is the wrong *functional form*, not merely a mis-set constant. Every
wood-perforation model in the literature — THOR, UFC 4-023-07, and Sanborn's
recalibrations alike — makes the ballistic limit depend on presented area and
diameter as well as mass and velocity. Reduced to the project's variables, a
perforation criterion is

$$v \;\ge\; v_{50}(m, D, t, \rho_w, H) \quad\Longleftrightarrow\quad
E_{thr} \;=\; \tfrac12 m\, v_{50}^2 \;=\; E_{thr}(m). \qquad (2)$$

For a compact fragment $D \propto m^{1/3}$, so $E_{thr}$ is a *rising* function
of $m$, not a constant. **A constant-$E_{thr}$ step systematically over-counts
small fragments** — which is exactly the direction of the count-gap residual,
and which the current formulation cannot express. Any implementation pass must
decide whether to (i) keep the constant-$E$ step and source a single
representative value, or (ii) generalise (1) to a mass-dependent threshold.
Option (ii) is the physically right answer and is *cheap*: the bisection in
(1) is already per-mass, so `_ke(m) >= E_leth` becomes `_ke(m) >= E_thr(m)` with
no structural change. See §4.

______________________________________________________________________

## 2. Literature audit — Sanborn et al. (2019)

`doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/`.
122 shots, 0.5 in (12.7 mm) hardened S-2 tool-steel sphere, 180–1200 m/s, into
SPF-S and SYP cross-laminated timber; 63 embedded + 59 perforating.

### 2a. What transfers, and what does not

**Does not transfer — the CLT recalibrations (Tables 5–8).**

1. **No identifiable mass or area scaling.** §5.4 (source.md:160) states
    plainly: *"Because the same projectile weight was used in all tests,
    inclusion in the model simply acts as an additional constant instead of a
    calibrating parameter"* — so $w$ was **removed** from the CLT THOR model
    (Eq. 11). The same degeneracy silently afflicts the CLT UFC recalibration
    (Eq. 12, Table 8), which *retains* $w^{b}$ and $D^{c}$ with $b$ = 1.434,
    $c$ = 0.201 — but every data point shares one $w$ and one $D$, so
    $C_1 w^b / D^c$ is a single lumped constant and $b$, $c$ are **not
    identifiable from this dataset**. They are fitting artefacts, not measured
    exponents. The card's remark that the diameter exponent "changed
    substantially" from the original 1.360 to 0.201 is therefore evidence of
    non-identifiability, not of new physics. Likewise "General THOR"
    (Table 7/9, $f$=1.305, $g$=12.58, $h$=3.967, nominally in $v_s, A, w$).
    **This is the decisive objection**: (2) is exactly the mass dependence the
    project needs, and it is the one thing this dataset cannot constrain.
1. **Thickness regime is 4× off.** §6.6 / source.md:191 recommends the CLT THOR
    model for *"CLT of a thickness of greater than 4 in. (10.1 cm)"*. Tolch's
    panels are 1 in. Worse, the deficit is not a benign extrapolation: the
    paper's own $R$ = 0.67 back-face reduction factor and its scabbing/
    exit-hole dissections (Fig. 5b) say that resistance near the back face is
    materially lower than mid-depth. A 1″ panel is **all back face**, so the
    thick-target calibration is biased in a known direction there.
1. **Cross-laminated ≠ solid.** Orthogonal plies plus a polyurethane bond line
    (bond-line shear 2.75 MPa SPF-S / 6.07 MPa SYP, Table 2) are a different
    target from Tolch's single solid board.
1. **Species/velocity match is fine** and is not the problem: SPF-S
    (455 kg/m³, Janka-equivalent 605 lb) is a good stand-in for Tolch's
    softwood, and 180–1200 m/s brackets the fragment arrival velocities.

**Does transfer — three things, all of them useful.**

1. **The original UFC 4-023-07 perforation-thickness equation** (card Eq. 2):
    $T_w = 9837\, v^{0.4113} w^{1.4897} / (D^{1.3596}\rho^{0.5414} H^{2})$, with
    $T_w$ [in], $v$ [ft/s], $w$ [lb], $D$ [in], $\rho$ [lb/ft³], $H$ [lb Janka].
    Sanborn (source.md:109) records its pedigree: *"the UFC equation was
    calibrated based on data taken from the THOR experiments conducted in the
    1950′s, and … the experiments used to calibrate the existing equation were
    completed on relatively thin blocks of wood."* **That is precisely the
    regime Tolch occupies** — thin solid wood, steel fragments — and it is
    exactly count-chain §5's option 1 (a THOR-type equation carrying wood
    coefficients) arriving through a secondary. Setting $T_w$ = 1 in and
    solving for $v$ gives a ballistic-limit velocity $v_{50}(m)$ and hence
    $E_{thr}(m)$ per (2), with the mass and diameter exponents that the CLT
    refit cannot supply.
1. **An independent, signed bound on that equation's error.** The paper's whole
    motivation is that original-UFC **over-predicts required thickness** on
    CLT (source.md:102, :191). Applied to Tolch, an over-predicted $T_w$ at
    fixed $v$ inverts to an *over*-estimated $v_{50}$, hence an
    **over-estimated $E_{thr}$**, hence an **under-counted** $N(\ge m_{thr})$ —
    i.e. conservative in the direction that would make the model *agree* with
    Tolch too easily. This sign must be stated in any derivation. Magnitude is
    unquantified in the thin-panel regime; the CLT discrepancy is not a valid
    proxy for it.
1. **Corroboration that a compact steel sphere is a legitimate proxy** for a
    compact fragment against softwood over 180–1200 m/s, with 122 shots behind
    it. This retires the "does a sphere stand in for a fragment" worry that
    would otherwise attach to any THOR-form use.

### 2b. Blocking transcription defect in the card — do not use its equations as printed

Three of the card's transcribed equations fail an order-of-magnitude closure
against the paper's own experiment (0.5 in sphere, $w$ ≈ 8.4 g = 0.0186 lb,
$v_s$ ≈ 2500 ft/s, SPF-S $\rho$ = 28.4 lb/ft³, $H$ = 605 lb, 5-ply
$t$ = 6.875 in):

| Card equation | Evaluates to | Should be |
| --- | --- | --- |
| Eq. (2) original UFC, $T_w$ | 7.4 × 10⁻⁴ in | order 1–10 in |
| Eq. (11) CLT THOR, $d$ | ~1.8 × 10³ in | order 1–7 in |
| Eq. (15) $v_{per}$ | ~52 ft/s | order 10³ ft/s |

Eq. (11) and Eq. (15) are also **not mutual inverses as printed**, although the
paper states (15) *is* the zero-residual-velocity inversion of (11)
(source.md:253). Card Eq. (11) is $d = K v_s^{f}$, so inverting at $d = t$ gives
$v_{per} \propto t^{1/f} = t^{0.670}$; card Eq. (15) is **linear in $t$**. The
two agree to 14% at the one thickness the paper demonstrates (6.875 in) and
diverge away from it — **by 2.2× at $t$ = 1 in, i.e. exactly at Tolch's panel
thickness**. That is a structural exponent defect, not a rounding one, and it
would have propagated silently into any thin-panel use.

These are PDF-extraction artefacts (grouping and superscript loss), not source
errors — the claim here bounds `card.md`, not the paper. Under
`.claude/rules/source-data-fidelity.md` they make the **card's equation block
inadmissible** until re-read from the page. Both closures are mechanised in
[`checks/sanborn2019-equation-closure.py`](checks/sanborn2019-equation-closure.py)
and should be re-run against whatever re-reading produces.

### 2c. Verdict against count-chain §5

§5 asked for either (1) THOR-type wood coefficients or (2) a softwood
ballistic-limit datum, and said option 2 is the cheaper sufficient close.

- **Option 2 — not closed.** The paper tabulates no ballistic limit for a 1″
  solid softwood panel; Figs. 6–8 are scatter plots referred to the Sanborn
  (2018) dissertation and are not transcribed. There is no $v_{50}$ or $E_{50}$
  to lift.
- **Option 1 — closed *by pointer*, not *by content*.** The paper hands over the
  original UFC/THOR functional form and its provenance, and independently
  validates the projectile proxy and the direction of its bias. It does not
  itself constitute the primary.

So: **partial close.** Sanborn 2019 converts an open literature search into a
single named, freely-available document to fetch. That is real progress and it
is enough to *scope* the derivation; it is not enough to *run* it.

______________________________________________________________________

## 3. Missing references

@librarian is needed before the derivation pass, for **one** item (the first;
the rest are optional depth):

1. **UFC 4-023-07, *Design to Resist Direct Fire Weapons Effects*** (US DoD,
    2008) — Sanborn ref. [21]. Public Whole Building Design Guide document.
    **Need:** the wood-perforation equation with its stated units, coefficient
    values, validity range (thickness, velocity, projectile class) and the
    THOR test basis it cites. This is the primary for card Eq. (2) and settles
    §2b. *Citing Eq. (2) through Sanborn without this is secondhand
    attribution* (`.claude/rules/source-data-fidelity.md`).
1. *(optional)* **Greenspon, "An approximate nondimensional representation of
    the THOR equations"**, USA AMSAA, 1976 — Sanborn ref. [32]. The route to
    THOR's own non-metallic coefficients if UFC's form proves insufficient.
1. *(optional)* Project THOR Report No. 47 (BRL, 1961) — still the ideal
    primary; still not in `doc-reference/`. Superseded in priority by item 1,
    which carries the same coefficients in a document that is actually
    obtainable.
1. *(optional)* Janka hardness $H$ and density $\rho$ for the species Tolch
    actually used. Tolch's panel wood must be confirmed from the 1938 report,
    not assumed; SPF-S values (28.4 lb/ft³, 605 lb) are the fallback and are
    defensible for generic softwood.

______________________________________________________________________

## 4. Options, ranked

**A — (recommended) Mass-dependent threshold from the original UFC/THOR form,
Sanborn as bounding secondary.**
Fetch UFC 4-023-07; verify Eq. (2) closes on the Sanborn sphere case (§2b
arithmetic, now with correct units); invert at $T_w$ = 1 in for
$v_{50}(m, D(m))$ with $D(m) = (6m/\pi\rho_{steel})^{1/3}$; feed
$E_{thr}(m) = \tfrac12 m v_{50}(m)^2$ into (1) by replacing the scalar
compare with a callable. Cite Sanborn for the projectile-proxy validity and
for the sign of the bias. *Cost:* one librarian fetch + one derivation pass +
a small `src/arty/` change (new `perforation_threshold_energy(m, target)`;
`min_lethal_mass`/`build_mmin_table` take a threshold callable or a target
spec, defaulting to today's constant so the ES-310 personnel path is
untouched). *Why first:* it is the only option that fixes the functional form
as well as the constant, and the functional-form error biases in the same
direction as the residual.

**B — Constant $E_{thr}$ evaluated from option A at a single representative
mass.** Same fetch, same inversion, then freeze $E_{thr}$ at the mass that
dominates $N(\ge m)$ near 15 ft. Sourced, minimal code change, keeps the step.
*Take this if* the reviewer judges the callable change too invasive for a
confirmation pass. Loses the small-fragment correction.

**C — Sanborn CLT-THOR/CLT-UFC constants applied directly.** **Rejected**, on
§2a items 1–3: no identifiable mass scaling (fatal — the model needs
$E_{thr}(m)$), plus a 4× thickness extrapolation into the regime the paper's
own back-face physics says is least like its calibration.

**D — Do nothing; log the constant-$E$ step as a limitation.** Legitimate under
the project's "a logged assumption is a valid closure" rule *only if* the
count arm's provisional PASS is accepted as-is. **Not recommended**: the whole
value of this thread is retiring the compound-test objection, and A/B are
cheap now that the source is named.

______________________________________________________________________

## Validation checks the derivation pass must run

1. **Closure on the source's own experiment** (§2b table): the chosen equation,
    in its stated units, must reproduce order-correct $T_w$ / $d$ / $v_{per}$
    for the 0.5 in sphere at 2500 ft/s into SPF-S. A retained script under
    `checks/`.
1. **Monotonicity and limits:** $E_{thr}(m)$ rising in $m$; $v_{50}$ falling in
    $m$ at fixed $t$; $v_{50} \to \infty$ as $m \to 0$.
1. **Bracket the two existing non-fitted probes:** the derived $E_{thr}$ at the
    mass scale of Tolch's finest screen cut (0.63 g) should sit in the same
    decade as 78.6 J / 126 J. A result 100× away means a units error, not a
    discovery.
1. **Re-run count-chain §4 as a prediction:** $N(\ge m_{thr})$ at 15 ft against
    700 / **779**, and the A→D falloff ratio against 0.557 ± 0.10. Both arms,
    zero free parameters.
1. **Regression:** `E_LETH_DEFAULT` = 1000 J personnel path unchanged — no
    shipped `p_kill` / casualty-area number may move.

## Fidelity target

This aspect drives the **absolute lethal/perforating fragment count** at the
Tolch validation point, and through it the credibility of every casualty-area
number in the demo. Tolerable error: **a factor of 2 on absolute count** against
1938-era recovered-fragment data (inherited from count-chain's fidelity target),
and **±50% on $E_{thr}$** — the count is only logarithmically sensitive to the
threshold ($N$ moves 2.8× over a 155× span in $E_{thr}$, §2 of count-chain), so
a half-decade error in the threshold is a ~15% error in the count. What matters
is that the value be *sourced*, not that it be precise.
