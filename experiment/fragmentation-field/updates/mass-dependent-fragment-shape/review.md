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
