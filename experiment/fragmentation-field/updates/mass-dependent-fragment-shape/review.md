# Review — aspect-ratio moment correction `c` on the Mott shape constant `A`

**Reviewed:** `derivation.md`, 2026-08-16 pass. Scope: derivation-only review
(no `src/` or notebook changes this pass).

**Open findings check:** `collect-findings.py --for
experiment/fragmentation-field/updates/mass-dependent-fragment-shape` returns
none. The one standing `[deferrable]` marker in scope is A8 (Mott/Linfoot
structural premise, `scoping.md` §1.4) — the derivation leaves it open and
states why (§3.5 A8). Confirmed below: this pass's own math (`c` derived
purely from Table 3's empirical means, no theoretical Mott/Linfoot premise
invoked) is genuinely orthogonal to that open question, so the framing holds.

## Verdict: **PASS**

No Blocking findings. Three Note-level presentational imprecisions found,
none of which change any reported number that feeds the ship
recommendation, the PASS-band verdict, or the B(r) cross-check conclusion.
No deferrable items beyond what the derivation already logs itself (A6/A7/A8,
carried correctly).

---

## Verification performed

All three check scripts were run standalone and their output compared
digit-for-digit against what `derivation.md` reports:

- `checks/aspect-ratio-moment-correction.py` → reproduces §3.3's `c = 1.2543`,
    §3.4's full sensitivity table and 16-corner band `[1.176, 1.352]`, §3.2's
    two limit checks (`c = 1.000000` at zero aspect dispersion; `c = 0.8354`
    at zero mass–aspect correlation, the AM–HM floor), §4's `k = 1.524`
    (`[1.280, 1.839]`) and `c·k = 1.912` (`[1.506, 2.487]`), and §2.1's
    identity check (`1.911879` both sides). Exact match, no discrepancy.
- `checks/bofr-at-new-mu.py` → reproduces §5.1's table exactly: geo-mean
    `B_model/B_card` of 1.226 / 1.063 / 0.792 at `c = 1.00/1.25/1.91`, all
    11/11 rows in the 0.5–2× band, and the near-identical normalised shape
    curves (0.429/0.233/… vs 0.433/0.238/…) supporting the "level shift, not
    tilt" claim.
- `checks/aspect-ratio-moment-leverage.py` → reproduces §6's full table
    (`N`, `N/700`, `N/779` at every `f` row) and the bisected thresholds
    `f ≥ 1.163` (/779) and `f ≥ 1.327` (/700) exactly.

**Factorisation (eq. 2) and orthogonality claims, checked against `src/`:**
`grep -n aspect_ratio src/arty/zones.py src/arty/fragmentation.py` shows `A`
(`shell.aspect_ratio`) enters the shipped code in exactly one place in each
file, both times only inside `alpha = A·κx²·t_bu/x0`, which feeds `μ` and
nothing else (`μ ∝ alpha` follows from `gamma = alpha^(-2/3)·gamma'` and
`μ ∝ gamma^-1.5`, confirmed by hand). `x0 ∝ 1/v_bu` and `κx` is a fixed
calibration constant independent of `A`, `v_bu`, or the breadth
distribution — so C2's correction (`v_bu = f·V0`) and A9.1's `k` (a
replacement for `κx²`) act on algebraically disjoint factors of the same
product. §2.2's "C2 and `k` cannot double-count" claim checks out from the
formula, not just from the derivation's prose argument. C2's cited "realised
1.096×" figure matches `count-chain.md` line 230 verbatim.

**Table 3 CSV invariant:** `uv run src/utils/check-table-invariants.py
doc-reference/fragmentation/explosion-fragment-model/tables/
table-3-grady-aspect-ratio-counts.invariant` → `ok` (5 rows, 6 checks). Table
is admissible per `source-data-fidelity.md`.

**Comparison-protocol check (unequal-comparison gate):** `c` is derived
solely from Felix 2022 Table 3 (§3), with no fitting to either the count
chain or the B(r) casualty data. Both cross-checks (§5 B(r), §6 count chain)
evaluate `c` and `c·k` at their independently-derived values, out of sample.
Neither candidate is scored at a value fit to the data doing the scoring —
this is a genuine, equal-freedom cross-check, not the "rebaseline onto the
validation source" failure mode the derivation itself correctly declines in
§6.2.

**A8 framing (Mott/Linfoot):** confirmed accurate. The derivation's `c` is a
reweighting of Felix Table 3's own empirical average and never invokes the
Mott/Linfoot "one constant `A`" structural premise for its derivation of `c`
— it only inherits that premise from the fact that a single global constant
is being corrected at all (a pre-existing, separately-tracked question). No
new reliance on the disputed primary is introduced.

---

## Findings

### Note 1 — §6.1 "32%" figure for /779 excess closure is off by ~2 points

`derivation.md` §6.1: "closing about 28% of the /700 excess and 32% of the
/779 excess above 1×." Recomputing precisely from the same `resolve_chain`
values used elsewhere in the doc (`N_shipped = 1756.77`, `N_c=1.254 =
1465.75`): /700 excess reduction = 27.5% (matches the stated 28%); /779
excess reduction = `(1.2552 − 0.8816)/1.2552 = 29.8%`, not 32%. **Impact:**
none on any decision — the underlying pass/fail figures (`2.09×`, `1.88×`,
the /779-clears/`,` /700-misses verdict) are independently confirmed correct
by the check script; this is a supplementary contextualising percentage, not
load-bearing. Tag: **Note**.

### Note 2 — §3.5 A3's "±0.03" impact bound understates the floor-only sweep

A3 bundles two choices (geometric- vs arithmetic-mid representative, and the
Group-0 zero-edge floor) under one stated impact of "±0.03 on `c`." The
geometric/arithmetic swap alone is `1.254 → 1.237` (−0.017, within the
stated bound), but the floor sweep table two lines above it shows floor=37.5
gr giving `c = 1.197`, a swing of −0.057 from baseline — nearly double the
stated ±0.03. **Impact:** none on the shipped conclusion — the authoritative
band reported downstream (`[1.18, 1.35]`, used in §5 and §6) comes from the
joint 16-corner sweep, which does include the full floor range
`{2.5, 37.5}` and therefore already captures this swing correctly. Only the
prose one-line characterisation of A3's isolated impact is loose. Tag: **Note**.

### Note 3 — §6.2's "23% over-prediction" framing compares the wrong baseline

§6.2: "Applying `c·k` … would trade a 23% over-prediction on B(r) for a 21%
under-prediction." The 23% figure is the *shipped* (`c = 1.00`) B(r)
over-prediction (geo-mean ratio 1.226), not `c = 1.25`'s actual result
(1.063, i.e. a 6.3% over-prediction) — which is the fit actually being given
up if `c·k` is chosen instead of `c`. The real trade is "give up a
near-exact fit (6%) for a 21% miss," a more lopsided case against `c·k` than
the "23% vs 21%" phrasing suggests. **Impact:** none on the conclusion —
if anything this understates (rather than inflates) the case the derivation
is making for preferring `c` alone; the recommendation and both cited ratios
(1.063, 0.792) elsewhere in the document are correct. Tag: **Note**.

---

## Checklist items specifically addressed

- **Dimensional analysis:** `c`, `k` are dimensionless ratios of like
    moments (§1); eq. (2) introduces no new units. Confirmed via the
    `ρt₀`-cancellation in eq. (3)/(4), itself checked against the shipped
    `mu ∝ alpha` chain in `fragmentation.py`.
- **Boundary cases:** the two limit checks in §3.2 (`c → 1` at zero aspect
    dispersion, `c → AM/HM < 1` at zero mass–aspect correlation) both
    verified numerically and algebraically sound (Chebyshev's sum
    inequality / AM–HM inequality respectively).
- **Numerical stability:** no division by zero or negative sqrt paths in any
    of the three scripts; `resolve_chain` and `moment_c` are well-behaved
    over the full corner-sweep domain.
- **Criterion match:** Table 3's admissibility confirmed via its
    `.invariant` (passes). The B(r) cross-check reuses
    `drag-gap-1944/checks/b-vs-range-155mm.py` **unmodified**, which itself
    reads the closure-checked genuine-casualties CSV (not the historically
    mis-swapped perforation column) — criterion match for that surface was
    already settled in that challenge's own review; this pass does not
    reopen or weaken it.
- **Comparison protocol:** verified equal-freedom, out-of-sample cross-check
    (see above) — no rebaseline-onto-validation-source violation.
- **Provenance:** A9.7's "1.2–1.8×" and C2's "1.096×" figures both verified
    against their primaries (`mott-fragment-shape-closure/derivation.md`
    line 357–358, `count-chain.md` line 230) rather than taken on the
    derivation's word.
- **Layering:** `derivation.md` contains no `src/arty/` edits this pass
    (explicitly out of scope, confirmed); all physics stays in the
    derivation/check scripts, none leaked into a `.qmd` (none touched).
- **Limitations captured:** A6 (modal bins are analyst defaults, direction
    of residual bias unknown, "binding limitation," not correctable) and A7
    (aspect-ratio fold-up biases `c` downward, unquantified) are both
    appropriately flagged as open, uncorrected limitations rather than
    silently absorbed. A8 (Mott/Linfoot) correctly left standing per the
    dispatch brief's ask.

---

## Pass 2 — adversarial / theory-critique review, 2026-08-16

**Distinct from the pass above.** That pass verified arithmetic and internal
consistency (every check script reproduced digit-for-digit, `A → μ` traced by
hand through `src/`, cited numbers checked against primaries) and is not
redone here. This pass's only job is to try to break the *theory* — evidentiary
scope, hidden assumptions, whether the two cross-checks are genuinely
independent, whether confidence outruns what the inputs support — even though
the math underneath is sound.

**Open findings re-examined, not treated as pre-settled:** the standing
`[deferrable]` marker (line 265) — `c` from one 155mm test article, applied
globally across four calibers — was independently re-derived below rather
than taken on trust. It holds, and finding H1 sharpens it with a concrete
mechanism the marker's text does not itself name.

### Verdict: **PASS-with-limitations**

No finding below changes the shipped recommendation (`c = 1.25` as the single
best point estimate; count-gap-1938 not closed) or introduces a wrong number,
unstable numeric, or out-of-bounds probability. Both findings are about
**unwarranted precision/independence framing** in the derivation's own prose,
not about the arithmetic, which the prior pass already cleared. Neither
finding has a hard quantitative impact estimate strong enough to force a
number to move, which is exactly why both are tiered Deferrable rather than
Blocking (per the materiality rule: a finding without a quantified impact
cannot block). Two limitation entries should be logged; see below.

### H1 — the two "independently corroborating" cross-checks are not
matched in caliber, and the derivation's own text never says so [Deferrable]

`c = 1.25` is derived entirely from Felix 2022 Fig. 10 / Table 3, a **155 mm
HE M101** test article (§3.1, confirmed on the figure). The two surfaces used
to corroborate/adjudicate it are:

- **§5, B(r) fit:** `drag-gap-1944/checks/b-vs-range-155mm.py`, **155 mm
    M107**, ground burst — same caliber family as the source data.
- **§6, count chain:** `MU0_G = 0.929`, `N0_0 = 2681`
    (`checks/aspect-ratio-moment-leverage.py`, sourced from `count-chain.md`
    §5's verdict row). That verdict row is the **75 mm M48 HE** Tolch (1938)
    chain — confirmed by grep: `count-chain.md:144` "75 mm M48 HE, DoD anchor
    `C_D C_shape = 2.674`, 15 ft panel station," and the `V0`/`M_case`
    provenance lines around it (`864.4 m/s`, `4980 g`) match the 75mm M48
    entries traced elsewhere in this project (`updates/75mm-fuze-case-mass-fix/`).
    **`derivation.md` never states this** — §5 names its shell explicitly
    ("155 mm M107, ground burst, AoF 30°"), §6 names none.

**Why this matters.** §7's ship rationale, point 3, calls the B(r) result
"independently corroborated on a second surface... derived from a different
dataset... than the one `c` came from." That is true of the *dataset*
(Ordnance Dept. 1944 casualties vs. Felix Table 3) but the *shell* is
essentially the same caliber family the correction was measured on — so a
near-exact B(r) fit is materially weaker evidence that the aspect-ratio
moment trend **generalizes across calibers** than the "second, independent
surface" framing implies; it is closer to confirming internal consistency on
the same 155mm population `c` was fit to. Conversely, §6.2 treats the
count-chain's residual /700 shortfall (2.09× vs. the 2.00× band, "4.5%
short") as **"real and not closed by this aspect"** — but that chain runs on
a **75 mm** shell, precisely the caliber the derivation's own A9 finding says
is unvalidated for this trend (line 263: "Neither this pass nor its review
evaluated whether the mass–aspect-ratio trend generalizes past 155mm"). A
75mm shell's wall-thickness-to-caliber ratio and case geometry differ enough
from a 155mm shell that a caliber-transfer error of a few percent in the
effective `c` for 75mm is at least as plausible an explanation for the 4.5%
miss as "the count residual isn't fully a shape-moment artefact" — and the
derivation asserts the latter without considering the former.

**Impact.** No shipped number moves — `c = 1.25` remains the single global
recommendation either way, and the document already declines to force `c·k`
to close the count band (correctly, per the rebaseline-avoidance argument).
What changes is the confidence a reader should place in §7 point 3's
"independently corroborated" language and in §6.2's "the honest reading is
that the remaining /700 shortfall is real" claim — both currently read as
stronger, caliber-blind statements than the underlying checks support.
**Suggested correction (not applied):** name each cross-check's shell/caliber
explicitly next to its result in §5.1 and §6, and qualify §7 point 3 and
§6.2's closing sentence to note that the B(r) agreement is same-caliber-family
evidence while the count-chain disagreement is cross-caliber and therefore
cannot be cleanly attributed to "real, uncorrected shape-moment residual"
versus "correction doesn't transfer to 75mm" without further data. This is a
prose/limitation fix, not a recomputation.

### H2 — `c`'s own discretization bias is directionally identical to `k`'s
disclosed one, but is never disclosed for `c` [Deferrable]

§4 states, of `k`: *"It is a lower bound. Only between-Group dispersion is
resolved (one mass representative per Group); all within-Group spread is
discarded, and discarded variance can only raise `k`."* This is a correct,
mathematically forced statement (law of total variance: discarding
within-group spread can only understate `⟨x²⟩`, so a variance-ratio computed
this way is a lower bound).

`c` is built from **the identical group-discretized table**
(`checks/aspect-ratio-moment-correction.py`, `moment_c`): every fragment in a
Group is assigned that Group's single representative mass `m_g`, regardless
of which aspect-ratio bin it falls in, so the entire measured `⟨A x²⟩`
covariance comes from **between-Group** variation of `(Ā_g, m_g)` — any
correlation between fragment mass and aspect ratio *within* a Group is
structurally invisible to the calculation (within a Group, `m` is constant by
construction, so its within-group covariance with `A` is exactly zero in the
computed statistic, by construction, not by measurement). By the law of total
covariance, `Cov_true(A,m) = Cov_between + E[Cov_within]`; if the omitted
within-group term carries the **same sign** as the measured between-Group
trend — the physically likely case, since the motivating hypothesis (large
fragments retain plate-like geometry) is a claim about a continuous
relationship, not a step function at the Group boundaries — then `c = 1.25`
as computed is **also a lower bound** on the true `x²`-weighted correction,
for the same structural reason `k` is flagged as one from the same table.

**This caveat is never applied to `c`.** §3.4's characterization ("materially
below `scoping.md` §4's speculative 1.4–1.9 band... the scoping's own hedge
('`c ≈ 1.3–1.6`') is still slightly high") and §7's closing line ("the
derived `c`'s own corner band is `±7%` — inside [the ±15% fidelity target]")
both read as confident, complete uncertainty statements. Neither the prose
nor the 16-corner sweep (which varies only bin edges, the open-bin value, and
the arithmetic/geometric midpoint convention — never the group-discretization
itself) captures this source of error.

**Note on strength.** Unlike `k`'s bound, this is not a mathematical
certainty — it depends on the sign of a covariance the table cannot resolve,
so it is a plausibility argument, not a proof. But it is the *same*
plausibility argument the derivation itself treats as decisive enough to
publish a directional, "not correctable from the held data" caveat for `k`
just one section later, from the same data structure — the asymmetry is the
finding.

**Impact.** If the omitted within-Group covariance is real and positive, the
true moment correction sits somewhere above 1.25, plausibly back toward the
`c ≈ 1.3–1.6` band the derivation quotes from `scoping.md` §4 and calls
"still slightly high" (§3.4) — i.e., the same magnitude range the document
explicitly considered and set aside. That would not flip the qualitative
recommendation (still one global multiplicative constant on `A`, still short
of fully closing count-gap-1938 without help from `k`), but it would move the
stated corner band `[1.18, 1.35]` and the "±7%, inside the ±15% target"
framing in a direction the document does not currently disclose is possible.
**Suggested correction (not applied):** either extend the `k`-style
"lower-bound, direction-known" caveat to `c` explicitly in §3.4/§3.5, or state
why it does not apply (e.g. if there is a reason to expect the within-Group
covariance is near zero or negative that the derivation has simply not
argued).

### Findings considered and set aside

- **A6 (modal-bin defaults as a competing, simpler explanation for `c > 1`):**
    already the derivation's own "binding limitation" (§3.5 A6, "not
    correctable... direction unknown"), carried into the follow-up list and
    into the `_limitations.qmd` action item. Re-derived independently here and
    found to be accurately and honestly stated — no sharpening needed beyond
    what's already logged.
- **Comparison-protocol / rebaseline-onto-validation-source risk (§6.2):**
    checked and found to be the opposite of the failure mode named in
    `.claude/incidents.md#unequal-comparison` — `c` is fit to neither
    cross-check dataset, and the derivation explicitly declines the move that
    would constitute gaming the B(r) surface. Confirmed sound; H1 above
    qualifies the *strength* of the resulting corroboration claim, not its
    validity as a protocol.
- **Eq. (3)'s constant-`t₀`, constant-`ρ` premise** (the closure's own `l =
    A x`, uniform-thickness flake model): a real physical simplification, but
    inherited unchanged from `mott-fragment-shape-closure`'s own closure, not
    introduced or leaned on more heavily by this update in any new way beyond
    what that document already carries. Out of this pass's scope.

### Limitation entries this PASS-with-limitations should log

1. **H1** — `_limitations.qmd` or `derivation.md` should note that the B(r)
    and count-chain cross-checks used to corroborate/adjudicate `c` in §5–§6
    run on different-caliber shells (155mm, same family as the source data,
    vs. 75mm, cross-caliber), so their agreement/disagreement is not the
    caliber-blind, equal-strength pair of "independent surfaces" §7 currently
    presents.
1. **H2** — note that `c`, like `k`, is a lower bound on the true
    `x²`-weighted moment correction under the (plausible but unproven)
    assumption that within-Group mass–aspect covariance shares the sign of
    the measured between-Group trend; the stated corner band `[1.18, 1.35]`
    does not include this source of uncertainty.

Both fold naturally into A9's existing evidentiary-scope caveat and the
already-flagged A6 limitation; neither requires reopening the arithmetic this
pass was told not to redo.

---

# Adversarial review pass — 2026-08-16 (single-constant vs `A(m)` premise)

**Scope of this pass (only):** is the scoping decision "moment correction on a
single constant `A`, not a per-fragment `A(m)`" defensible on its own terms?
Does its rejection reasoning foreclose *every* mass-dependent formulation or
only the literal one considered? Does collapsing to one global constant lose
something load-bearing across `SHELLS`' four calibers or across the mass
spectrum within one shell?

Not re-litigated here: H1/H2 (evidentiary scope, cross-check independence), the
math-verification section, or the three standing `[deferrable]` findings already
in the register.

**Verdict: FAIL** — one Blocking finding (A1). The single-constant *form* is
sound and the value is right for 155 mm; what is not defensible is that the
constant is **global**. `c` is a spectrum-weighted moment, not a material
constant, and the update's headline count result is computed on the one caliber
where the spectrum-consistent value is on the wrong side of 1.

Checks written this pass, retained per `.claude/rules/verification-scripts.md`:

- `checks/spectrum-weighted-c-per-shell.py` — reproduces `derivation.md` §3.3
    exactly (`⟨m⟩=219.04 gr`, `⟨A⟩=1.5681`, `⟨m/A⟩=111.361 gr`, `c=1.2543`,
    `k=1.5242`) then re-weights the identical Table-3 aspect mix by each
    `SHELLS` entry's own Mott spectrum.
- `checks/spectrum-weighted-c-fixedpoint-count-chain.py` — iterates the
    `μ ↔ c` fixed point to convergence and re-solves the 75 mm count chain.

---

## A1 — **Blocking** — `c` is a spectrum-weighted moment, so a *global* `c` is not well-defined; at 75 mm the consistent value is 0.97, which reverses this update's headline count result

**What the derivation assumes.** A5 (`derivation.md:258`) fixes the weighting:
"`c` is count-weighted over Table 3's own fragment counts, i.e. the same
weighting the shipped `⟨A⟩ = 1.6` uses." That justifies *consistency with `⟨A⟩`*
and is the right choice for making `A → cA` a pure reweighting. It does **not**
establish that the resulting moment ratio is the one eq. (1) calls for.

**What eq. (1) calls for.** `2μ = ρ t₀ ⟨A x²⟩`, where `⟨·⟩` runs over *the
shell's own fragment population* — the population whose mean mass is `2μ` by
construction. `c = ⟨m⟩/(⟨A⟩⟨m/A⟩)` (eq. 4) is therefore a functional of the
**joint** distribution of `(A, m)`, and the `m`-marginal of that joint is the
shell's Mott spectrum. The `A|m` relation may plausibly be caliber-transferable
(that is the physical claim); the *weights* are not — `μ` varies by an order of
magnitude across `SHELLS`. Freezing `c` freezes the 155 mm spectrum.

**Numbers.** `checks/spectrum-weighted-c-per-shell.py` reproduces §3.3 to all
printed digits under table weighting, then applies the identical within-Group
aspect mix with Group weights taken from each shell's own
`N(≥m) = N₀e^{−√(m/μ)}`.
`checks/spectrum-weighted-c-fixedpoint-count-chain.py` iterates the
`μ = c·μ₀` ↔ `c(μ)` loop (it converges in 3–4
iterations — the "self-reference" of `scoping.md` §2 is contractive here, see A2):

| shell | model `μ` [gr] | `P(Group 0)` | spectrum-consistent `c` |
| ----- | -------------- | ------------ | ----------------------- |
| 155 mm M107 | 98.1 | 0.583 | **1.262** |
| 105 mm M1 | 31.9 | 0.784 | **1.099** |
| 75 mm M48 | 14.3 | 0.899 | **0.970** |
| 60 mm M49A2 | 7.6 | 0.957 | **0.906** |

Two things follow, and they cut in opposite directions:

1. **The derived value is vindicated for 155 mm.** 1.262 vs the shipped 1.254 —
    0.6 % apart. This is a *self-consistency check the derivation should have
    made and would have passed*: the Table-3 sample's `⟨m⟩ = 219.0 gr` sits
    within 12 % of the 155 mm model's own `2μ = 196.2 gr`. Table 3's photographic
    weighting is an excellent proxy for the 155 mm spectrum. That is why `c`
    works and why the §5 B(r) check (155 mm M107) corroborates it.
1. **It does not survive transfer to the smaller calibers, and the failure is
    not a small percentage.** At 75 mm the same table gives `c = 0.970` — below
    1, i.e. the *opposite sign of correction*. The mechanism is transparent:
    89.9 % of the 75 mm Mott population falls inside Group 0, where Table 3
    resolves no `A`-vs-`m` trend at all, so the between-Group covariance that
    generates `c > 1` is simply not sampled, and the AM–HM floor the derivation
    itself identified in §3.2 (`c = 0.835` at zero `m`–`A` correlation) takes
    over.

**Observable output that changes.** `derivation.md` §6 — the update's headline
result — runs the count chain on **75 mm M48** at `f = c = 1.254`.
Re-solving that same chain (`checks/spectrum-weighted-c-fixedpoint-count-chain.py`, `μ₀ = 0.929 g`, `N₀ = 2681`,
`m_thr = 0.166 g`; the `f = 1` row reproduces `count-chain.md`'s 1757 /
2.51× / 2.26×):

| | `f` | `N(≥m_thr)` | vs 700 | vs 779 |
| --- | --- | --- | --- | --- |
| shipped | 1.000 | 1757 | 2.51× | 2.26× |
| `derivation.md` §6 | 1.254 | 1466 | 2.09× | **1.88× (claimed PASS)** |
| spectrum-consistent 75 mm | 0.970 | **1795** | **2.56×** | **2.30×** |

So §6.1's "**/779 arm: PASSES**" (`derivation.md:415`) and §7's "the /779 arm
clears (1.88×)" (`derivation.md:482`) **reverse**: at the weighting eq. (1)
requires, this update moves the 75 mm count *away* from the band by ~2 %, not
into it. The direction of the whole update flips on its stated surface. That is
an in-scope outcome changing qualitatively — Blocking, not deferrable.

Note this is *not* the already-logged A10/H1 caliber-matching caveat restated.
A10 says the two cross-checks are not caliber-matched and that the 4.5 % /700
miss might be a transfer artifact. This finding is stronger and different: it
gives the transfer error a **derived value and a sign** from the update's own
data, and that value takes the /779 arm from PASS to FAIL. A10 flagged an
unquantified doubt; this quantifies it and the answer changes the verdict.

**Suggested correction (do not apply).** Do not weaken `c` — make it per-shell.
The change is small and stays inside the update's own machinery: compute
`c(μ)` from the same CSV by eq. (4) with Group weights from the shell's Mott
spectrum, and solve the one-dimensional fixed point `c = c(c·μ₀)` (3–4
iterations, <1 ms). `ShellParams.aspect_ratio` stays one number *per shell*, so
nothing about "one constant, no new functional degrees of freedom" is lost —
`A_eff` becomes 2.02 (155 mm), 1.76 (105 mm), 1.55 (75 mm), 1.45 (60 mm).
Alternatively, if a per-shell `c` is judged out of scope for this update, then
`c = 1.25` must be scoped **to 155 mm only** in `src/arty/`, and §6/§7's count
claims — which are 75 mm — withdrawn. What is not available is shipping 1.25
globally while quoting a 75 mm PASS obtained with it.

Caveats on my own numbers, stated so they are not over-read: (i) the Group
collapse means these `c` values inherit A11's lower-bound structure exactly as
the derivation's does — the *ordering* across calibers is the robust content,
not the third digit; (ii) they assume the `A|Group` conditional mix is
caliber-independent, which is a **weaker** assumption than the derivation's
(which requires the full joint, mass marginal included, to transfer);
(iii) A6/A7 apply unchanged to both.


---

## A2 — **Deferrable** — the "structurally self-referential" ground for rejecting `A(m)` is refuted by this update's own §3.2–§3.3, and by a convergent fixed point

`scoping.md` §2 (lines 143–148) is the load-bearing structural objection, and it
is recited as ground 1 of the §6 recommendation (line 287) and as the settled
premise `derivation.md:11` refuses to reopen:

> Writing `A(m)` inside it makes `μ` a function of the mass it is supposed to
> define — self-referential.

Two independent reasons this does not hold as stated:

1. **The derivation already does the thing the objection forbids.**
    `derivation.md` §3.2 eq. (3) `x² = m/(ρ t₀ A)` is a *per-fragment* relation
    evaluated with a *per-fragment, mass-dependent* `A`; eq. (4) and §3.3 then
    evaluate `⟨m⟩`, `⟨A⟩` and `⟨m/A⟩` over a joint distribution in which `A`
    varies with `m` (Group 0 at 1.33 → Group 4 at 3.00). The adopted option
    **is** a mass-dependent formulation of `A`; it differs from the rejected one
    only in that its result is reported as a scalar. Self-reference was never
    the discriminator.
1. **Where genuine self-reference does appear, it is benign.** `c` depends on
    `μ` through the weighting (A1) and `μ = c·μ₀` — a real fixed point. It
    converges monotonically in 3–4 iterations for every `SHELLS` entry
    (`checks/spectrum-weighted-c-fixedpoint-count-chain.py`: 155 mm 1.2404 → 1.2606 → 1.2619 → 1.2620). A
    contractive one-dimensional fixed point is a solved equation, not an
    incoherence. The objection would, applied consistently, condemn the shipped
    option too.

**Impact.** Zero on any current rendered number — this is about the *reason*, not
the value. It matters because a future pass reading `scoping.md` §2 will treat a
whole class of formulations as structurally closed when it is not, and because
under A1 the correct fix *is* in that class. Downgraded from Blocking on that
basis: no output moves until A1 is acted on.

**Suggested correction.** Amend `scoping.md` §2 to say what is actually true:
substituting `A(m)` *pointwise inside* the closed-form eq. (2) is a category
error, because eq. (2) is a mean-value expression; a mass-dependent `A` enters
legitimately through the moment `⟨A x²⟩`, which is exactly what option 1 does.
Then restate the real ground for preferring one constant — parsimony and the
data's inability to support a fitted curve (§1.2b) — which is defensible.

---

## A3 — **Deferrable** — the §6 recommendation recites a ground its own §1.2a retracts, and the two options were not given equal freedom

**(a) A retracted objection is still doing work.** `scoping.md` §1.2a (line 44,
"CORRECTED 2026-08-16") states plainly: "This is a real, sourced mass axis — the
'no mass axis' objection to a mass-resolved treatment does not hold." Yet §6
ground 1 (line 283) rejects `A(m)` because "**the data has no mass axis** and the
Groups' modal bins are the analysts' own counting defaults", citing §1.2a–b. The
first clause is the retracted claim, cited to the section that retracts it. It is
also the ground with the most rhetorical weight in the summary a later reader
will actually read.

**(b) The surviving objections do not discriminate.** Of the three §6 grounds:

| ground | status |
| ------ | ------ |
| "no mass axis" | retracted by §1.2a (above) |
| "modal bins are analyst defaults" (§1.2b) | **applies equally to `c`** — `derivation.md` A6 (line 260) concedes it verbatim as "the binding limitation on `c`" |
| "`A` does not enter the drag/area path" (§2) | **verified true** (see A4) but it refutes the *brief's mechanism* and option 4; it says nothing about option 2 |
| "structurally self-referential" (§2) | refuted (A2) |

That leaves no objection that separates the two options. The genuine
discriminator — a fitted `A(m) = A₀(m/m₀)^p` curve has free parameters the data
cannot identify, whereas a moment is a statistic of that same data — is real,
sufficient, and is nowhere stated.

**(c) Comparison protocol.** Option 1 received a full derivation: a value, a
16-corner sensitivity sweep, two limit checks and two cross-check surfaces.
Option 2 was rejected a priori and never evaluated at any parameterisation. The
checklist's equal-freedom test is not met; the conclusion "reject `A(m)`
outright" (`scoping.md:278`) rests on a comparison that was never run. As it
happens the outcome may well survive an equal comparison (per (b) above, on the
parsimony ground) — which is why this is Deferrable rather than Blocking.

**Impact.** No rendered number moves. The cost is directional: `derivation.md:11`
declares the scoping decision "settled there and not re-opened", so the
unevaluated option is now insulated from review by a chain of citations to a
ground that was withdrawn.

**Suggested correction.** In `scoping.md` §6 ground 1, delete the "no mass axis"
clause and replace the §2 self-reference clause with the parameter-identifiability
argument. In `derivation.md`, soften line 11 from "settled there and not
re-opened" to a pointer at the (corrected) grounds.

---

## A4 — **Note** — the "`A` reaches the count only through `μ`" claim is verified, and it is what makes the single-constant *form* correct within one shell

Checked independently, since three other conclusions rest on it (`scoping.md` §2,
§5; `derivation.md` §6's holding of `m_thr` fixed). `grep -rn "aspect_ratio"
src/arty/` returns exactly four hits: the dataclass field
(`fragmentation.py:198`), a comment (`:135`), and the two `alpha = shell.
aspect_ratio * shell.breadth_factor**2 * t_bu/x0` lines (`fragmentation.py:410`,
`zones.py:149`) that feed `μ` alone. It appears nowhere in `retardation_coeff`,
in any presented-area computation, or in the perforation path. Confirmed.

The consequence is worth stating explicitly because it is the strongest part of
the single-constant case and the scoping never makes it: **given this code
structure, `A` has exactly one scalar channel into the model, so any
mass-dependence of `A` within one shell is *fully absorbed* into the single
moment `⟨A x²⟩` — nothing is lost by collapsing it.** Within-shell, "one
constant" is not an approximation, it is exact. That answers half the question
this pass was asked, in the single constant's favour. What it does not cover is
the *across-shell* axis, because the moment's weights are shell-dependent —
which is A1.

---

## Verdict and what to do

**FAIL** on A1. Not because `c = 1.25` is wrong — it is right, to 0.6 %, for the
caliber it was measured on and for the caliber its B(r) cross-check runs on —
but because it is presented and scheduled to ship as a caliber-independent
constant, and on the 75 mm chain that carries the update's headline claim the
consistent value is 0.97, turning a claimed `1.88×` PASS into a `2.30×` FAIL.

Ranked, for whoever takes the next pass:

1. **A1 (Blocking)** — either make `c` per-shell via the `μ`-weighted moment
    (recommended; ~10 lines, no new degrees of freedom, `A_eff` = 2.02 / 1.76 /
    1.55 / 1.45 for 155/105/75/60 mm), or scope `c = 1.25` to 155 mm and withdraw
    §6/§7's 75 mm count claims. Do not ship 1.25 globally alongside a 75 mm PASS.
1. **A2, A3 (Deferrable)** — repair the stated grounds in `scoping.md` §2/§6.
    If A1 is resolved the per-shell way, this is not optional bookkeeping: the
    fix *is* a mass-dependent formulation, and the document currently declares
    that class structurally closed.
1. **A4 (Note)** — no action; consider promoting the within-shell exactness
    argument into `derivation.md` §1, where it strengthens the case.

**Limitation entries, if the human elects to defer A1 rather than fix it**
(which would require an explicit human call — an agent may not close a shipped
global constant known to be spectrum-inconsistent by deferral,
`.claude/rules/deferred-findings.md`):

- `c = 1.25` is the `x²`-weighting moment of the Felix Table-3 joint `(A, m)`
    distribution **weighted by that sample's own mass spectrum**, which matches
    155 mm M107's model spectrum (`⟨m⟩ = 219 gr` vs `2μ = 196 gr`) and no other
    `SHELLS` entry. Re-weighted by each shell's own Mott spectrum the same table
    gives `c` = 1.26 / 1.10 / 0.97 / 0.91 for 155 / 105 / 75 / 60 mm. Applying
    1.25 to the sub-105 mm shells over-corrects `μ` by up to ~38 %, and reverses
    the sign of the correction at 75 mm and below.
- The 75 mm count-chain result in `derivation.md` §6 (`2.09× / 1.88×`) is
    computed at the 155 mm value of `c`; at the 75 mm spectrum-consistent value
    it is `2.56× / 2.30×`, i.e. marginally worse than shipped.

## Out-of-scope observations

None. All findings above lie inside the premise this pass was asked to
stress-test.

---

# Re-review — fix cycle 1, 2026-08-16 (verifying commit `b2f4c5b`)

**Scope of this pass:** verify the fix for A1 (Blocking) committed in
`b2f4c5b`, and check whether its handling of A2/A3 (Deferrable) actually
resolves them and is internally consistent. Per the re-review rule, no
new-scope findings are raised; anything noticed outside A1/A2/A3 is flagged
as out-of-scope below, not adjudicated.

**Open findings check.** `collect-findings.py --for
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/`
returns exactly the two `[deferrable]` markers quoted in this pass's brief
(the A|Group-transfer caveat at `derivation.md:398`, and the
caliber-dependent-sign caveat at `derivation.md:417`). Both are pre-existing,
both are the *narrower* successors of the pre-fix A9/A11 (A10 was deleted —
see below, correctly) and both are carried forward, not newly forgotten.
`OPEN-FINDINGS.md` was regenerated by the fix commit and matches
(`collect-findings.py` with no args reports "already current — 32 open").

## Verdict: **PASS**

The per-shell fixed-point construction genuinely resolves A1 rather than
merely narrowing it, A2 and A3 are correctly repaired in `scoping.md`, and the
document is internally consistent — every surviving reference to the
withdrawn 1.88× / "PASS" claim is explicitly labeled superseded. No Blocking
findings. No new Deferrable items beyond the two already logged (see above).

---

## Verification performed

**Script reproduction.** `checks/per-shell-c-and-75mm-count-chain.py` was run
standalone (`uv run python`, ~1 s) and its output compared digit-for-digit
against `derivation.md` §3.3b, §3.4b, §6:

- Per-shell `c` table: `155/105/75/60 mm` → A/B/C = `1.262/1.251/1.173`,
    `1.099/1.102/1.090`, `0.970/0.985/1.013`, `0.906/0.920/0.950` — exact match,
    including `P(Group 0)` (0.541/0.769/0.902/0.963) and `A_eff` (2.00/1.76/
    1.58/1.47 after rounding).
- 75 mm count chain: `N`/`/700`/`/779` for method A (1800/2.57×/2.31×), B
    (1777/2.54×/2.28×), C (1739/2.48×/2.23×), and the shipped (1757/2.51×/
    2.26×) and superseded-global-`c` (1466/2.09×/1.88×) rows — exact match.
- Cross-check against my own prior-pass scripts
    (`spectrum-weighted-c-fixedpoint-count-chain.py`): the converged
    fixed-point `c` values (105/155/75/60 mm = 1.0985/1.2620/0.9697/0.9058)
    reproduce the new script's method-A column to 4 significant figures
    exactly — two independent implementations of the fixed point agree.
- `checks/bofr-at-new-mu.py` re-run: 155 mm B(r) table unchanged
    (1.226/1.063/0.792, 11/11 band membership at `c` = 1.00/1.25/1.91) — matches
    the derivation's claim that this surface is untouched by the per-shell fix.
- `table-3-grady-aspect-ratio-counts.invariant` still passes (5 rows, 6
    checks, `check-table-invariants.py`) — the source table this pass's new
    weighting is built on remains admissible.
- Independently re-derived `group_weights()`/`group_cond_mass()` (the Mott
    Group-probability and conditional-mean-mass functions) by numerical
    quadrature in `u = √(m/μ)` space (avoids the `m→0` density singularity a
    naive linear-mass grid hits). `P(Group)` sums to 1.0000 for all four
    shells and matches the script's un-iterated `P(Group 0)` (e.g. 0.5829 at
    `μ₀ = 98.10` gr for 155 mm) exactly — confirms the analytic antiderivative
    in the script is correct, not just self-consistent.

## Findings

### A1 — resolved, not merely narrowed

The pre-fix defect was precise: a single global `c` is the `x²`-weighted
moment of Table 3's aspect data taken over *Table 3's own* mass marginal
(Felix's 155 mm photographic sample), then applied to shells whose mass
marginal (`N(≥m) = N₀e^{−√(m/μ)}`) differs by an order of magnitude. The fix
replaces the weights with each shell's *own* Mott spectrum and solves the
resulting self-reference as a genuine one-dimensional fixed point
`c = c(c·μ₀)`, holding fixed only the conditional `A | Group` mix (which
Table 3 does supply). This is a strictly weaker transfer assumption than the
pre-fix version required (which needed the full joint distribution — marginal
included — to transfer), and the document says so explicitly and correctly
(A9, revised). That is elimination of the specific mechanism A1 identified,
not a narrowing of its magnitude: the caliber that drove the reversal (75 mm)
now gets its own `c ≈ 0.99` from its own spectrum, rather than inheriting
155 mm's 1.25.

What remains open is a different, narrower, already-logged assumption (the
`A | Group` mix's caliber-transferability, and the Group-discretization
sign-dependence) — both are the two findings quoted in this pass's brief, and
neither is a restatement of A1's mechanism. Confirmed by reproduction (above)
that the numbers behind this claim are real, not just asserted.

**Minor, non-blocking observation on method C.** `c_continuous()` computes a
"trend" ratio from a continuous `Ā(m)` power-law fit and then multiplies by
the AM–HM floor (`1/(⟨A⟩⟨1/A⟩)` on Table 3's marginal) to reconstitute a
dispersion contribution. This is a reasonable but undisclosed decomposition —
it is exact only under an implicit assumption (the *relative* dispersion of
`A` about its mass-trend is mass-independent) that `derivation.md` §3.3b/3.4b
does not state; the text only says method C "restores... covariance." Impact:
none on the shipped numbers — method B (not C) is adopted as central
everywhere, and even without method C, methods A and B alone already bracket
75 mm's `c` at `[0.970, 0.985]`, straddling 1 and giving the same "no PASS"
conclusion the derivation reaches. This does not change the headline result
by any measurable amount and does not reach the Blocking bar (no output
changes). **Tag: Note** — if acted on, the fix is one sentence in §3.3b
naming the assumption behind the floor-multiplication in method C.

### A2 — resolved

`scoping.md` §2 (diff in `b2f4c5b`) replaces the "structurally
self-referential" objection with the correct framing: eq. (2) is a mean-value
expression, so a per-fragment `A(m)` substituted pointwise is a type
mismatch, not an incoherence, while a mass-dependent `A` entering through the
moment `⟨A x²⟩` (what option 1 does) is legitimate. It also states plainly
that where genuine self-reference occurs (`c` through `μ`), it is a
contractive fixed point, confirmed convergent in 3–4 iterations for every
`SHELLS` entry — verified above by reproduction. This is exactly the repair
A2 asked for, sourced to `review.md` A2 by an explicit "(CORRECTED
2026-08-16 per `review.md` A2)" marker.

### A3 — resolved

`scoping.md` §6's option-2 rejection ground is rewritten from the retracted
"no mass axis" claim to the parameter-identifiability argument A3(b)
identified as the real, unstated discriminator: a fitted `A(m) = A₀(m/m₀)^p`
has two free parameters fit to five Group means the analysts chose as
counting defaults, whereas the adopted option is a statistic (no fitted
parameter) of that same data. The retracted clause is deleted, not just
appended-around. `derivation.md:11` is also softened from "settled... not
re-opened" to a pointer at the (now-corrected) grounds — matching A3's
suggested correction exactly.

### Internal consistency — checked directly, no residual contradictions found

Grepped the full `derivation.md` for every surviving instance of "1.88",
"PASSES", "clears", and the withdrawn "~17%/28%/32%" leverage language: every
occurrence left in the document is inside a row or sentence explicitly marked
`*superseded:*` or "withdrawn" / "was the 155 mm correction... withdrawn".
`OPEN-FINDINGS.md`'s A10 entry (caliber-mismatch between the B(r) and
count-chain surfaces) was deleted, not merely reworded — correctly, since the
per-shell fix eliminates that specific mechanism by construction (each surface
now runs at its own caliber's `c`); what A10 pointed at is fully subsumed by
the surviving A9 (narrower transfer assumption). §6.1/§6.2/§7's "no PASS,
correction is nil at 75 mm" conclusion is stated once and carried consistently
through the abstract, the headline ship-table, and the fidelity-target
paragraph — no stale "PASS" or "clears" language survives outside a
superseded/withdrawn tag.

## Checklist items specifically addressed this pass

- **Criterion match / comparison protocol:** not re-litigated (out of this
    pass's scope per the re-review rule); H1/H2 stand from the original PASS
    review.
- **Numerical stability:** the Picard fixed point (`c_{n+1} = c(c_n·μ₀)`,
    tol `1e-6`, cap 60 iterations) converges in 3–4 iterations for all four
    `SHELLS` entries with no divergence risk observed at current parameter
    values; not stress-tested for calibers outside `SHELLS` (immaterial to
    this fix, since no such caliber is shipped).
- **Source-data fidelity / table closure:** `table-3-grady-aspect-ratio-counts`
    invariant re-verified passing; no new table introduced by this fix.
- **Layering:** no `src/arty/` or notebook edit in this pass (`derivation.md`
    line 9 states so, confirmed by `git show --stat`: only `derivation.md`,
    `scoping.md`, `OPEN-FINDINGS.md`, and one new `checks/*.py` touched).

## Out-of-scope observations

None found that reach the Blocking bar. One presentational gap noted above
(method C's floor-multiplication assumption undisclosed) is tagged Note and
sits inside this pass's own A1 scope, not a new-scope finding.
