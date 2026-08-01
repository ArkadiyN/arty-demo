# Review — WD55 steel grade derivation

**Reviewer:** model-reviewer agent
**Date:** 2026-07-25
**Scope:** `updates/wd55-steel-grade/derivation.md` (cites `scoping.md`, both
read in full). Pre-implementation: no `src/arty/` edits exist yet, so this is
a physics/math review, not a code review. Layering check is N/A this pass
(nothing has leaked into `.qmd`/`app/` because nothing has been ported yet —
§6/§8 of the derivation correctly scope that to the next pass).

**Verification method:** re-derived every printed number in derivation.md §4,
§5 (C2, C6, C7, C8) independently against the *shipped* `mott_params`,
`gurney_velocity`, `compute_frag_field` in `src/arty/fragmentation.py` (not
against the derivation's own arithmetic) via a scratch script, since the
derivation isn't in `src/` yet to diff against. All reproduced to the
reported precision. Script deleted after use.

## Verdict: **PASS-with-limitations**

The physics (Mott composition-series interpolation, R-identifiability, unit
handling, numerics) is sound and every printed number is independently
reproducible from the shipped code. The one substantive issue is an
unresolved **input-provenance risk** — flagged below — that the derivation's
own assumption log (A6/gap G2) already gestures at but does not fully cover.
It does not rise to Blocking because the more metallurgically plausible
reading of the new evidence actually corroborates the derivation's premise
rather than contradicting it — but the ambiguity must be logged and closed
via G2 before this is relied on for a sign claim.

---

## Findings

### F1 — Parent-supplied static min-YS figures: ambiguous bearing on the carbon-ranking premise (Deferrable, elevated priority)

**The new fact:** baseline min YS = 65,000 psi; WD55 min YS = 35,000 psi,
framed as "the lower-carbon baseline" (65 ksi) vs. "the higher-carbon WD55"
(35 ksi) — i.e., more carbon → *lower* minimum yield, called out as an
inversion of the ordinary carbon-strength correlation.

Taken **literally**, this labels WD55 as the higher-carbon grade of the
pair. That directly conflicts with the derivation's own composition
assignment: WD55 is fixed at 0.18–0.28 %C (parent-supplied, both here and in
scoping §1), and the baseline is treated throughout (derivation §6a comment,
scoping §3 "defect", assumption A5/C7) as the *higher*-carbon grade (~0.45 %C
SAE 1045 per the notebook, itself flagged uncited — gap G2). If baseline is
in fact the *lower*-carbon member of the pair (as the literal wording says),
Mott's composition series (§2, table) would require baseline γ to sit
**below** WD55's γ = 57, not at 65 — reversing the sign of every headline
number in the derivation's §4 table: μ would *decrease* for WD55 relative to
baseline instead of increasing, N₀ and N(>0.5 g) would *increase* instead of
decrease, and the direction check in C3 ("lower carbon → lower γ → fewer,
larger fragments" for WD55) would be backward.

**But** taken under the derivation's own stated composition bands (baseline
≈0.45 %C > WD55 0.18–0.28 %C, i.e. WD55 *is* the lower-carbon grade), the
same two numbers (65 ksi > 35 ksi) are the **ordinary**, not inverted,
carbon-strength correlation: more carbon (baseline) → higher strength floor;
less carbon (WD55) → lower floor. This reading is also the metallurgically
more plausible one — quench-and-tempered ~0.45 %C forging steel reaching a
65 ksi minimum, and a lower-carbon, less-heat-treated "economy" WWII
substitute steel (a well-documented wartime practice) reaching only 35 ksi,
is an unremarkable pairing. It is also the reading consistent with the
derivation's own **A4** (Mott's quasi-static stress column *rises* with
carbon — the same direction as "more carbon → higher yield"), so the
"inverted" framing is in tension with the very source table (Mott 1947 §3)
the derivation already cites for A4.

**Impact if the literal (WD55-is-higher-carbon) reading is correct:** full
sign flip of the derivation's headline contrast — μ +21.8 %→ negative,
N₀ −17.9 %→ positive, N(>0.5 g) −7.8 %→ positive, i.e. the demo would show
WD55 producing *more, smaller* fragments than baseline instead of *fewer,
larger* ones. That is exactly the "trend reverses" case the review rubric
treats as qualitative.
**Impact if the ordinary-correlation reading is correct:** zero — it is
independent corroboration of the existing direction, no numbers change.

**Why this stays Deferrable rather than Blocking:** I have not found grounds
to conclude the derivation's direction *is* wrong — the more plausible
metallurgical reading supports it, and the yield-strength spec is in any
case a weak proxy for %C (min-YS depends heavily on heat treatment/temper,
not raw carbon content alone — the same caution the derivation's own scoping
§3.1 already applies to Mott's *quasi-static* UTS column). But the ambiguity
is squarely load-bearing for the demo's sign, so it cannot be silently
folded into the existing A6/G2 wording as-is.

**Required limitation-log addition (not a fix to the derivation itself):**
extend A6 / gap G2 to explicitly state: *"A parent-supplied static
minimum-yield-strength pair (65 ksi baseline / 35 ksi WD55) is consistent
with, and does not contradict, the assumed baseline > WD55 carbon ranking —
but only under the standard heat-treatment-driven reading of yield-strength
specs, not a literal 'higher-carbon WD55' reading of that same data. The
relative carbon ranking between the two catalog grades is the single most
consequential unresolved fact in this aspect: gap G2 (period spec sourcing
for both grades) must close this before the sign of the grade contrast is
treated as final."* This should be surfaced prominently, not buried, in
`_limitations.qmd` when the presentation pass runs.

### F2 — All numeric claims independently reproduced (Note)

Recomputed against the shipped `src/arty/fragmentation.py` (not the
derivation's own arithmetic): γ interpolation (48.8/57.2/64.2), R
(16.33/14.04/12.50 MPa), μ (0.5049/0.4024/0.3382 g), N₀
(11923/14960/17798), N(>0.5 g) (4408/4907/5277), R₅₀ sweep across γ
(101.15→101.42→100.57→98.94→93.96 m for γ=42/49/57/65/88, confirming the
claimed non-monotonicity in C8), C2 identifiability (bit-identical μ/N₀ at
k=0.5/2/137, exact 0.0 deviation), C6 quadratic-interpolant sensitivity
(57.94/49.36/64.76 vs. local-linear 57.2/48.8/64.2, max ≈1.3 % — matches the
claimed "within 1.4 %"), and C7's alternate-baseline contrast table
(−17.9 %/−33.7 %/−47.9 % at baseline γ=65/75/88) — all matched to reported
precision. C1's dimensional analysis (Pa^1.5 · m^1.5 kg^−0.5 · s^3 = kg)
checks out algebraically. No action needed.

### F3 — Fidelity target and scope correctly bounded (Note)

Scoping §7 fidelity target (±30 % on N₀ acceptable, sign + visibility is the
bar) is met with wide margin at the adopted point (μ +21.8 %, N₀ −17.9 %) and
even at the composition-band extremes. The R₅₀-is-not-the-right-readout
finding (C8) is well-supported (non-monotone in γ, near-cancellation between
fragment count and per-fragment reach) and correctly flagged as a
presentation-pass instruction rather than something this derivation needs to
fix.

### F4 — Assumption log is otherwise thorough (Note)

A1–A5, A7 are well-scoped, correctly signed (A3/A4 explicitly noted as
pulling in opposite, non-resolvable directions), and each has a stated
"why". C7's self-critical check (baseline γ possibly underestimated relative
to a consistent extrapolation rule) is a good-faith robustness check — note
it only stress-tests *magnitude* of the baseline-higher-carbon assumption,
not the *direction* (that gap is F1).

---

## Checklist pass-through

- **Dimensional analysis:** correct (C1, independently re-derived above).
- **Boundary cases:** composition-band endpoints (0.18/0.28 %C) computed and
  shown to stay inside the existing N(>0.5 g) validation band; γ→∞ / σ_F→0
  limits checked (C5), monotone, no singularity.
- **Parameter ranges:** γ=57 (49–64 band) sits inside Mott's tabulated
  0.1–0.3 %C range — interpolation, not extrapolation, as claimed. σ_F held
  at the existing baseline value with an explicit, honest "convention not
  claim" justification (§3).
- **Numerical stability:** none of the new entry's operations introduce
  division-by-zero or sign changes; C2's identifiability test is bit-exact.
- **Physical plausibility:** N(>0.5 g) values (4408–5277) sit centrally in
  the existing 3000–8000 validated band; fragment mass/count order of
  magnitude is unchanged from the already-validated baseline family.
- **Source attribution:** Mott 1947 §3 table cited with page/line-in-scan
  precision; μ closure correctly deferred to Gold 2017 PAFRAG (not
  re-derived from the OCR-damaged Mott equations, which is the right call —
  C3 correctly flags and works around the OCR sign inversion). The new
  parent-supplied MYS figures are (correctly) not cited as if sourced —
  they aren't in `doc-reference/`, and the derivation doesn't reference
  them (they were given to this review out-of-band, not to the derivation
  pass) — see F1 for how they should feed back in.
- **Layering:** N/A this pass — no `src/arty/` or `.qmd` edits exist yet;
  §6 records the intended comment/entry text for the next pass, correctly
  kept out of any notebook.
- **Limitations/constraints:** A1–A7 are honest and mostly complete; F1
  identifies the one gap (carbon-ranking direction, not just "WD55 identity
  unverified") that should be added before the next pass treats the sign as
  settled.
- **Data-driven analysis:** strong — full parameter table, sensitivity to
  interpolation scheme (C6), sensitivity to baseline γ choice (C7), R₅₀
  sweep (C8), all independently reproduced.

---

## Suggested corrections (not applied)

1. Extend assumption **A6** / gap **G2** in `derivation.md` §7 with the F1
   wording above (or equivalent), naming the yield-strength evidence
   explicitly and stating which reading it supports.
2. Before the implementation pass ports this to `src/arty/fragmentation.py`,
   get either (a) an explicit parent confirmation of which grade has more
   carbon (independent of the %C bands already given, since those two facts
   are currently in tension under the literal MYS reading), or (b) a citable
   period source resolving G2 for both grades. This does not have to block
   *this* derivation pass's acceptance — Option A's direction is still the
   better-supported reading — but it should block treating the direction as
   settled fact in the notebook's finished framing.
3. No changes needed to §1–§6 arithmetic, the interpolation, the σ_F
   convention, or the checks — all independently verified correct.

---
---

# Re-review — 2026-07-25 (revised derivation: WDSS-1 identity confirmed, G2 closure)

**Reviewer:** model-reviewer agent
**Scope:** the revised `derivation.md` and `scoping.md` in this same folder
(grade renamed WD55 → **WDSS-1**, composition corrected to **0.14–0.20 %C**
from *Ammunition Series 6* Table 6-1; baseline re-attributed from the
notebook's uncited "SAE 1045 ≈0.45 %C" to **WD-X1335 ≈ AISI 1335,
0.33–0.38 %C**). Per the dispatch brief, this pass (a) independently
re-verifies gap-G2 closure sourcing and (b) independently re-derives every
printed number in `derivation.md`, rather than trusting the file's own
arithmetic or its shipped `recompute.py`.

**Verification method:** wrote a fresh scratch script
(`experiment/_scratch/wdss1_review_check.py`, deleted after use) importing
`ShellParams`, `SteelParams`, `_shell_geometry`, `gurney_velocity`,
`mott_params`, `compute_frag_field` directly from the shipped
`src/arty/fragmentation.py` — built independently of the derivation's own
`recompute.py`, not by running that script. Also read every `doc-reference/`
file the derivation cites for gap G2 (both WDSS-spec docs, the 105 mm M1 BOM
doc + its `index.md`, the AISI 1335 card, the M49A2 drawing entry, and the
newly-added `doc-reference/ww2-shells/index.md §2.3/§2.4` excerpts) in full,
rather than trusting the derivation's characterization of them.

## Verdict: **PASS-with-limitations**

Every recomputed number in `derivation.md` §2, §4, §5 (C2–C8) is
independently reproduced bit-for-bit / to reported precision from the shipped
code. The WDSS-1 side of gap G2 (the aspect's actual subject grade) is now
genuinely closed by a legible, high-confidence primary-source table. But the
**baseline** side of the same "G2 closed for both grades" claim is overstated:
the WD-X1335 → AISI 1335 identification that the derivation now treats as
sourced fact is not established by any cited document — the two documents
that discuss it explicitly flag it as an unconfirmed, low-confidence
inference. This does not flip the sign of the reported contrast (see impact
below) so it stays Deferrable, but the "closed" / "no longer an assumption"
language must be corrected before this is presented as settled.

---

## Findings

### F5 — Baseline "WD-X1335 = AISI 1335" identification is not sourced; "G2 closed for both grades" is overstated (Deferrable, elevated priority)

**What the derivation claims.** `derivation.md`'s primary-sources list and §5
C3 state the baseline composition (0.33–0.38 %C) as established, citing the
105 mm M1 BOM (`ordnance-105mm-m1-1940/card.md`, "WD-X1335, spec 57-107") "with"
the AISI 1335 card (`azom-steel-grades/aisi-1335/aisi-1335.md`). C3: *"The
carbon ranking itself is now sourced on both sides ... so the direction is no
longer an assumption."* `scoping.md` §5 G2: *"CLOSED for composition (both
grades)."*

**What the cited documents actually say, independently checked:**

- `ordnance-105mm-m1-1940/card.md` (BOM, p.16 / doc "page 7") **does**
  reliably establish that the 105 mm M1 shell body is "Steel WD-X1335, spec
  57-107" — confirmed directly in `shell-he-105mm-m1.md`'s Bill of Material
  table ("Body, Shell ... Steel WD-X1335 ... 57-107"). This half is solid.
- But that same `index.md`'s own confidence table rates "Composition Data" as
  **"Not Found — Spec 57-107 not digitized in public sources"**, and its
  "Recommendations for Follow-Up" suggests comparing to **SAE 1040**, not AISI
  1335, as the closest analog.
- The AISI 1335 card itself states in its own "Remarks": *"No War Department
  (WD) nomenclature or historical WD-series designation is mentioned in this
  reference. The steel is identified solely by AISI 1335 / UNS G13350
  designations."* — i.e. the card supplies no linkage to WD-X1335 at all.
- `ammunition-series-6-steel-composition/ammunition-series-6-steel-composition.md` (which the derivation does
  **not** cite, but which is the project's own dedicated analysis of exactly
  this question) rates "Successor Grade Identity" confidence as **"Low —
  ... WD-X1335 is inferred, not confirmed"** and lists WD-X1335=X-1340-successor
  as one of four open hypotheses.
- The newly-added `doc-reference/ww2-shells/index.md §2.3` (added in this same
  update, part of the git diff) is consistent with this: it lists WD-X1335 as
  only "possibly" the X-1340 successor and repeats "Data Gap: WD-X1335
  composition ... not digitized."

So the **only** thing actually confirmed by a primary source is the *name*
"WD-X1335, spec 57-107" on the BOM line; the 0.33–0.38 %C figure attached to
it is a **numeral-coincidence inference** ("X1335" ~ "1335") that the
project's own source documents explicitly decline to endorse and flag as
low-confidence. This is a materially different epistemic status from the
WDSS-1 side, where *Ammunition Series 6* Table 6-1 is a direct, high-confidence
transcription of the actual grade's chemistry.

**Impact if the AISI-1335 attribution is wrong (e.g. the true analog is SAE
1040, ≈0.37–0.44 %C, or genuinely unknown):** none on the *sign* of the
contrast — every plausible WW2 medium/heavy artillery-shell steel composition
in this range (0.33–0.45 %C) is still well above WDSS-1's independently
confirmed 0.14–0.20 %C "mild steel" mortar-body chemistry, and the derivation's
own C7 already brackets a baseline-γ sensitivity range (65/71.7/74.7) whose
lower bound (the shipped 65) is *below* even a same-rule 0.355 %C extrapolation
— i.e. the shipped catalog entry already under-states, not over-states, the
plausible contrast, so drifting the true baseline composition higher (as SAE
1040 would) only widens that existing conservative margin. Magnitude: if
baseline %C is nudged from 0.355 to, say, 0.40 (SAE 1040 midpoint), the
same-rule extrapolated γ moves to roughly 78–82 (vs. the already-computed
71.7–74.7 at 0.355 %C) — inside the same qualitative conclusion as C7 already
states, not a new regime. **No printed number in §4/§5 needs to change.**

**Why Deferrable, not Blocking:** the sign of the grade contrast (WDSS-1 =
fewer, larger fragments) is robust to this ambiguity for the reason above, and
every quantitative check (C2–C8) reproduces correctly regardless of which
baseline-composition hypothesis is true, since the *catalogued* baseline
γ = 65 is unchanged either way. What is wrong is the **confidence language**
("closed," "no longer an assumption"), not any number.

**Required limitation-log addition** (not a fix to the arithmetic): extend gap
G2 in both `scoping.md` §5 and `derivation.md` §7 (A6, or a new A8) to state:
*"G2 is closed only for WDSS-1's composition (Ammunition Series 6 Table 6-1,
high-confidence direct transcription). The baseline's WD-X1335 → AISI 1335
identification is an unconfirmed name-based inference; the BOM confirms only
the grade name 'WD-X1335, spec 57-107' for the 105 mm M1 shell body, not its
composition — spec 57-107 is not digitized, the AISI 1335 card explicitly
states it carries no WD-series linkage, and the project's own dedicated
analysis (ammunition-series-6-steel-composition/ammunition-series-6-steel-composition.md) rates this
identification 'Low confidence, not confirmed' and suggests SAE 1040 as an
equally plausible alternative. This does not change the sign of the WDSS-1
vs. baseline contrast (§5 C7's sensitivity range already covers plausible
alternatives) but the composition figure 0.33–0.38 %C attached to the baseline
should be read as a plausible working value, not a sourced fact."* This should
carry into `_limitations.qmd` at the same priority as A5/A6.

**Suggested correction (not applied):** reword `scoping.md` §5 G2 from
"CLOSED for composition (both grades)" to "closed for WDSS-1; the baseline's
composition is a plausible but unconfirmed inference from grade-name
similarity, not a primary-sourced fact" and soften `derivation.md` C3's "no
longer an assumption" accordingly. Also (minor) suggest not citing the AISI
1335 card in the same source-list bullet as the BOM entry — presented
together, the two look like a single sourced fact rather than a fact
(WD-X1335 name) plus a distinct, unconfirmed hypothesis (its composition).

### F6 — Every recomputed number independently reproduced against a freshly-written script, not the derivation's own `recompute.py` (Note)

γ-interpolation (40.4/46.7/53.0), geometry constants (V0=994.2274 m/s,
r_bu=77.818 mm, m_shell=12.0400 kg), the §4 table (μ 0.3305/0.5375/0.6845/
0.4488 g, N₀ 18217/11201/8794/13413, N(>0.5 g) 5324/4269/3741/4668, R₅₀
98.937/101.449/100.821/101.105 m), the headline contrast (+62.6 % / −38.5 % /
−19.8 % / +2.51 m / +2.54 %), C2 identifiability (bit-exact, 0.000e+00 at
k=0.5/2/137), C4 band membership (all four PASS against [3000, 8000]), C6
quadratic-vs-linear sensitivity (γ_quad 41.24/47.44/53.00 vs. linear
40.4/46.7/53.0; μ −2.32 % quad vs. unrounded linear), C7's alternate-baseline
table (γ 65/71.72/74.70 → N₀ contrast −38.5 %/−46.9 %/−50.1 %), C8's R₅₀-vs-γ
sweep (99.34→101.45 m non-monotone, γ=47 at the stationary point), and C5's
brittle limit (μ=1.732e-7 g, N₀=3.476e10 at γ=1e6) — all matched to reported
precision. C1's dimensional analysis checks out algebraically. No action
needed.

### F7 — WDSS-1 side of gap G2 genuinely closed, and honestly scoped (Note)

`ammunition-series-6-wdss-specs/ammunition-series-6-wdss-specs.md` Table 6-1 is a direct, itemized
transcription with an explicit high-confidence rating for "Chemical
composition" and "Intended use (WDSS 1, 2)" in the source's own confidence
table; the 0.14–0.20 %C WDSS-1 band and its 60 mm/81 mm mortar/57 mm
recoilless application are both legibly and specifically stated. A6's honest
treatment of the M49A2 drawing (correctly declines to claim it "confirms" the
grade, since page 57 is illegible in the held OCR) and of the superseded
0.18–0.28 %C figure (flagged, not used) both hold up under independent
reading of those source files. No issues found on this side of G2.

### F8 — Minor: baseline provenance-comment blending of sourced and unsourced figures (Note)

The proposed §6(a) comment text — *"WD-X1335, spec 57-107 ... read as AISI
1335 -> 0.33-0.38 %C, min YS 65 ksi, 15 % elong"* — reads as one continuous
attribution chain, but "min YS 65 ksi, 15 % elong" is not in the AISI 1335
card (which explicitly states YS/UTS are not provided) nor in any newly-cited
source; it is carried over unchanged from the pre-existing (already uncited,
pre-dating this update — `git log` shows it introduced in `116a0f6`) `STEELS`
comment. Not a new defect introduced by this pass and not a numeric issue, but
the comment's phrasing invites a reader to believe AISI 1335 supplies the
yield/elongation figures too. Cosmetic wording fix only, no output changes.

---

## Checklist pass-through (this pass)

- **Dimensional analysis:** unchanged from prior pass, correct.
- **Boundary cases:** re-verified — composition-band endpoints (0.14/0.20 %C)
  computed and confirmed inside the N(>0.5 g) band; γ→∞ limit confirmed
  monotone with no singularity.
- **Parameter ranges:** γ=47 (band 40–53) is an interpolation, not
  extrapolation, over Mott's 0.1–0.2 %C segment — re-confirmed. σ_F convention
  unchanged and still correctly framed as a convention, not a claim.
- **Numerical stability:** C2 identifiability re-confirmed bit-exact at
  k=0.5/2/137.
- **Physical plausibility:** N(>0.5 g) 3741–5324 across all four table rows,
  centrally inside the validated 3000–8000 band.
- **Source attribution:** WDSS-1 side solid (F7). **Baseline side is the one
  finding of this pass (F5)** — a real sourcing gap in the "closed" claim,
  not in the arithmetic.
- **Layering:** N/A — still no `src/arty/` or `.qmd` edits; §6/§8 correctly
  scope the implementation to a future pass.
- **Limitations/constraints:** A1–A7 otherwise thorough; F5's addition is the
  one required extension.
- **Data-driven analysis:** strong, independently reproduced end-to-end
  (F6).

---

## Suggested corrections (not applied)

1. Reword `scoping.md` §5 gap G2 and `derivation.md` §5 C3 / §7 to state gap
   G2 is closed for **WDSS-1 only**; the baseline's WD-X1335→AISI 1335
   composition attribution is a plausible, unconfirmed inference (F5), not a
   second sourced fact — add the wording drafted in F5 to the assumption log.
2. Optional/cosmetic: separate the BOM citation (grade name, solid) from the
   AISI 1335 citation (composition guess) in the derivation's source list so
   they read as two different confidence tiers, not one.
3. Optional/cosmetic: in the §6(a) provenance comment, put a citation boundary
   between "0.33-0.38 %C" (AISI-1335-sourced, itself an inference — see #1)
   and "min YS 65 ksi, 15 % elong" (pre-existing, still uncited, unrelated to
   this update) so they don't read as one attribution chain (F8).
4. No changes needed anywhere in §1–§6 arithmetic, the γ-interpolation, the
   σ_F convention, or the C2/C4/C5/C6/C7/C8 checks — all independently
   re-derived and matched to reported precision this pass.

---
---

# Review — src/ implementation pass — 2026-07-25

**Reviewer:** model-reviewer agent
**Scope:** `git diff src/arty/fragmentation.py tests/test_fragmentation.py` (the
implementation pass that ports the revised WDSS-1 derivation into code), plus
consistency check of the F5/F8 wording corrections claimed to have been
applied to `derivation.md` and `scoping.md` in this same pass, against the
re-review findings above.

**Verification method:** read the full diff; independently recomputed every
number in the diff (μ, N₀, N(>0.5 g) for both grades, and the C2
identifiability check at k = 0.5/2/137) via a fresh scratch script
(`experiment/_scratch/wdss1_srcpass_check.py`, deleted after use) importing
`STEELS`, `ShellParams`, `gurney_velocity`, `mott_params`, `SteelParams`
directly from the shipped `src/arty/fragmentation.py`; ran the full
`tests/test_fragmentation.py` suite; grepped the whole repo for `WDSS1` /
`gamma=47` outside `src/`+`tests/` to check for layering leaks; grepped both
`derivation.md` and `scoping.md` for the F5 (`CLOSED`/"sourced on both
sides"/"no longer an assumption") and F8 (blended attribution-chain comment)
language flagged in the prior pass.

## Verdict: **PASS-with-limitations**

The `src/arty/fragmentation.py` diff itself is correct and well-scoped: the
new `"US WW2 WDSS1"` entry is dimensionally consistent, every number
independently reproduces to full float precision, the new tests correctly
pin the C2/C3/C4 checks from `derivation.md`, and no physics/parameter values
leaked outside `src/arty/`. The two claimed wording corrections (F5, F8) were
applied **correctly to the shipped code comment** but only **partially** to
`derivation.md` itself — leaving an internal contradiction and three dangling
references to a "A8" assumption-log entry that was never written. None of
this changes any computed number or the sign of the grade contrast, so it
stays Deferrable, but it should be closed before this derivation is treated
as a finished record.

---

## Findings

### F9 — Numbers, formula, and tests: fully verified (Note)

Recomputed independently from the shipped code (not `derivation.md`'s own
`recompute.py`): WDSS-1 (γ=47) → μ=0.5375 g, N₀=11 201, N(>0.5 g)=4 269;
baseline (γ=65) → μ=0.3305 g, N₀=18 217, N(>0.5 g)=5 324 — both match
`derivation.md` §4's table bit-for-bit at reported precision. `mott_params`
(`fragmentation.py:211–217`) matches derivation eq. (1) term-for-term:
`sqrt(2/rho) * (sigma_f/gamma)**1.5 * (r_bu/V0)**3`; dimensional check
Pa^1.5 · (m³/kg)^0.5 · s³ = kg holds. C2 identifiability re-confirmed
bit-exact (0.0 diff in μ and N₀) at k = 0.5, 2, 137 using a scaled
`SteelParams` built directly from the shipped `STEELS["US WW2 WDSS1"]`. Full
suite: `uv run pytest tests/test_fragmentation.py -q` → **53 passed**. The
four new tests (`test_steel_params_wdss1`,
`test_mott_fragment_count_in_pafrag_range_all_grades`,
`test_mott_params_depend_only_on_sigma_f_over_gamma`,
`test_wdss1_gives_fewer_larger_fragments_than_baseline`) correctly cover C2,
C3, and C4 as `derivation.md` §8 required, and only the pre-existing
`STEELS["WW2 US HE Shell"]` comment changed — no value changed on the
baseline entry, confirming §6(a)'s "comment edit only" claim. Physical
plausibility: γ=47 sits mid-Mott's tabulated 20–67 range, N(>0.5 g)=4 269 is
centrally inside the validated 3000–8000 PAFRAG band, and 47 < 65 correctly
gives fewer/larger fragments for the lower-carbon mortar-body grade — no
issues.

### F10 — Layering: clean, no leakage outside `src/arty/` (Note)

`git status`/`git diff` for this pass touch only `src/arty/fragmentation.py`
and `tests/test_fragmentation.py` (plus `doc-reference/`, agent-memory, and
the `updates/wdss1-steel-grade/` artifacts, all out of scope for this
checklist item). Grepped `app/` and every `.qmd` for `WDSS1`, `gamma=47`, and
`47.0` in a fragmentation context: the only hit is a pre-existing,
unrelated Mott-1947 citation line in `fragmentation-field.qmd`'s source
table. No physics, computation, or parameter values leaked into a notebook or
app file.

### F11 — Shipped code comments correctly apply F5 and F8 in substance (Note)

The new baseline-entry comment (`fragmentation.py:34–47`) explicitly
separates the sourced fact ("Grade NAME is sourced... that is the only
sourced fact") from the unsourced inference ("Composition is NOT sourced...
a plausible but UNCONFIRMED inference... Working value, not a sourced one"),
and further separates out the unrelated legacy "min YS 65 ksi, 15 % elong"
figure as "NOT supplied by the AISI 1335 card or any other source... nothing
here depends on it." This is a correct, faithful application of both F5
(don't overstate the baseline's composition as sourced) and F8 (don't
conflate the two unrelated provenance figures) to the code that actually
ships. No issues with the WDSS-1 entry's own comment either — it correctly
attributes 0.14–0.20 %C to *Ammunition Series 6* Table 6-1 and states the
γ-interpolation and σ_F-convention reasoning concisely.

### F12 — `derivation.md` itself was only partially updated to match: dangling "A8" reference, unresolved C3 contradiction (Deferrable)

Three files now say "see ... A8" as if `derivation.md` §7 contains an
assumption **A8** carrying the F5 caveat:

- `derivation.md:34` ("...not a second sourced fact — see A8.")
- `scoping.md:198` ("see derivation A5/A8: the shipped catalogued...")
- `src/arty/fragmentation.py:42` ("...Working value, not a sourced one --
  see derivation.md A8.")

But `derivation.md` §7's assumption log only runs **A1–A7**
(`derivation.md:308,313,315,324,328,333,347`) — there is no A8 bullet. The
content that would belong there (the F5-required statement that the
baseline's 0.33–0.38 %C is an unconfirmed name-similarity inference, not a
second sourced fact) exists informally in the source-list prose
(`derivation.md:29–34`, correctly updated) but was never formalized as a
numbered assumption, and the **"Limitations-page entries" list**
(`derivation.md:354–358`) — which review.md's prior pass explicitly asked to
carry this "at the same priority as A5/A6" — still only names A5 and A6, not
this item.

Compounding this, `derivation.md`'s own **C3** (`derivation.md:187–188`)
still reads: *"The carbon ranking itself is now sourced on both sides
(WDSS-1 0.14–0.20 % C vs WD-X1335 0.33–0.38 % C), so the direction is no
longer an assumption."* This is the exact language the re-review's F5 asked
to be softened, and it directly contradicts the pass's own corrected
source-list header three sections earlier ("*Not a source, listed separately
on purpose*... this is an inference from grade-name similarity, not a second
sourced fact") and the shipped code's own comment ("Composition is NOT
sourced... UNCONFIRMED inference"). A reader who reaches C3 without having
read the header would come away believing the baseline composition is
sourced, which is false per the project's own cited documents (F5's original
finding, re-verified again this pass by re-reading
`ordnance-105mm-m1-1940/card.md`, the AISI 1335 card, and
`ammunition-series-6-steel-composition/ammunition-series-6-steel-composition.md` — nothing has changed since
the prior pass's reading of those sources).

**Impact:** zero on any computed number — C3's ordering conclusion
(γ=47<65 ⇒ μ up, N₀ down) is unaffected by which composition-sourcing
sentence follows it, and the shipped `(sigma_f, gamma)` values are unchanged
either way. This is a documentation-consistency/completeness gap, not a
physics or numerics defect: three cross-references point at content that
doesn't exist, and one paragraph (C3) still overstates confidence in a way
the rest of the same document (and the shipped code) correctly avoids.

**Why Deferrable, not Blocking:** no output, test, or sign changes; the
correct, careful version of this caveat is present and correct in the parts
of `derivation.md` that matter most (§0 source list) and in the shipped code
comment (F11), so a reader who checks either of those gets the right
answer — only C3 and the "Limitations-page entries" list are stale.

**Required limitation-log addition / suggested correction (not applied):**

1. Add an **A8** bullet to `derivation.md` §7 with the wording the prior
   review already drafted for F5 (or a close paraphrase), so the three
   existing "see A8" references resolve to real content.
2. Reword `derivation.md:187–188` (C3's closing sentence) to drop "now
   sourced on both sides... no longer an assumption" and instead say
   something like "WDSS-1's composition is now directly sourced; the
   baseline's is an unconfirmed but plausible inference (A8) that does not
   change the sign of this ordering — see A8" — consistent with the
   document's own header and the shipped code.
3. Add the new A8 item to the "Limitations-page entries" list
   (`derivation.md:354–358`), alongside A5/A6, per the prior review's
   explicit instruction.
4. Optional/cosmetic: `derivation.md` §6(a)'s proposed comment text
   (`derivation.md:266–280`) still shows the pre-fix, blended
   "AISI 1335 -> 0.33-0.38 %C, min YS 65 ksi, 15 % elong" wording that F8
   flagged — it was superseded by the actually-shipped, better-organized
   comment (`fragmentation.py:34–47`) without `derivation.md` §6(a) being
   updated to match. Since `derivation.md` is the durable record of what was
   implemented, a future reader diffing "proposed vs. shipped" would see a
   mismatch. No functional impact (the shipped code is correct); resync
   §6(a)'s quoted block with the shipped comment, or add a one-line note
   that §6(a) was superseded by an improved version at implementation time.

---

## Checklist pass-through (this pass)

- **Dimensional analysis:** correct, re-verified against shipped `mott_params`.
- **Boundary cases:** N/A new this pass — this aspect only adds a catalog
  entry, no new geometry/grazing-angle path; the composition-band endpoints
  were already checked in the prior derivation pass and are unchanged.
- **Parameter ranges:** γ=47 within Mott's tabulated 20–67; σ_F/ρ unchanged
  from the validated baseline family.
- **Numerical stability:** no division-by-zero/negative-sqrt paths touched;
  C2 identifiability bit-exact.
- **Physical plausibility:** N(>0.5 g)=4 269 centrally inside the validated
  3000–8000 band; fewer/larger fragments for the lower-carbon grade is the
  physically expected ordering and is test-pinned (F9).
- **Source attribution:** the shipped code comments are honest and correctly
  scoped (F11); `derivation.md` itself has the one gap above (F12) — three
  dangling "A8" references and one stale-confidence sentence (C3) that were
  not brought in line with the pass's own corrections elsewhere in the same
  file.
- **Layering:** clean — confirmed no physics/computation/parameter values
  outside `src/arty/` (F10).
- **Limitations/constraints check:** F5's required limitation-log addition
  was only partially carried through — present in `scoping.md` G2 and in
  `derivation.md`'s header/source-list, but not in `derivation.md`'s
  "Limitations-page entries" list or as a formal assumption-log entry (F12).
- **Data-driven analysis:** strong — every number independently reproduced
  bit-for-bit/to reported precision (F9).

---

## Suggested corrections (not applied)

1. Add assumption **A8** to `derivation.md` §7 (content: F5's caveat about
   the baseline's unconfirmed composition inference); resolve the three
   existing "see A8" references.
2. Reword `derivation.md:187–188` (C3) to remove "no longer an assumption"
   and instead point at the new A8.
3. Add A8 to the "Limitations-page entries" list (`derivation.md:354–358`).
4. Optional: resync or annotate `derivation.md` §6(a)'s quoted comment block,
   which still shows pre-F8 wording superseded by the shipped code.

None of the above requires touching `src/arty/fragmentation.py` or
`tests/test_fragmentation.py` — both are correct as shipped.

---
---

# Re-review — 2026-07-25 (Mott table re-extraction: OCR-timeout fix, fabricated-citation withdrawal, cross-section reconciliation)

**Reviewer:** model-reviewer agent
**Scope:** `derivation.md` and `recompute.py` in this same folder, as revised
after `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`
was re-extracted (OCR/vision-timeout fix changed the Mott §3 composition→γ
table). Per the dispatch brief, particular attention to internal
self-consistency: do the interpolation table, assumption log, numerical
checks, and §6 code-comment blocks agree with each other and cite only claims
that actually exist in the source. `scoping.md`, `src/arty/fragmentation.py`,
and `tests/test_fragmentation.py` were read as necessary cross-references
(they are directly cited by, or claimed to already match, `derivation.md`)
but are not this pass's primary subject.

**Verification method:** read the re-extracted source
(`rspa.1947.0042.md`, the §3 table and surrounding prose in full, including
its own "Extraction note" / "Downstream impact" header); ran
`uv run python experiment/fragmentation-field/updates/wdss1-steel-grade/checks/recompute.py`
directly (not trusting the derivation's transcription of its output) and
independently re-derived by hand the local-linear and Newton-quadratic
interpolants, the C7 alternate-baseline table, the C4 floor-margin
calculation, and the eq. (2) scaling-law cross-check; wrote a small scratch
script (`experiment/_scratch/wdss1_c8_check.py`, deleted after use) to
evaluate two γ points (50, 75) that appear in `derivation.md`'s C8 table but
not in `recompute.py`'s own printed C8 sweep, using `recompute.py`'s own
`evaluate()`. Grepped `derivation.md`, `scoping.md`,
`src/arty/fragmentation.py`, and `tests/test_fragmentation.py` for the
specific figures the header claims were corrected or withdrawn (`γ=40`,
`0.2 %C`/`0.2C` bracket, `72-75`/`72–75`, `0.3 C` row, `smallest`/`largest`,
`lower bound`/`upper bound`) to check whether the correction actually landed
everywhere it needed to.

## Verdict: **PASS-with-limitations**

Every recomputed number in `derivation.md` §2, §4, §5 (C2–C8) is
independently reproduced to reported precision from the corrected Mott table
and the shipped code — the physics and arithmetic of this revision are sound,
and the γ=47 adopted value is correct (and, per the derivation's own honest
account, unchanged from before the OCR fix by a genuine numerical
coincidence). However, the reconciliation the header claims was done is
**incomplete**: two internal contradictions and one dangling cross-reference
survive within `derivation.md` itself, and the specific fabricated citation
this revision withdraws in §2/A9 is still asserted as fact in three sibling
files (`scoping.md` twice, and — more seriously — in the comment block
**currently shipped** in `src/arty/fragmentation.py`). None of this changes
any computed μ/N₀/N(>0.5 g)/R₅₀ value, so nothing here meets the Blocking bar,
but the pattern (this is the third consecutive pass to leave a stale
cross-reference or contradicted claim behind a numeric fix — cf. F1/F5/F12
above) means this should not be treated as finished until the items below are
closed.

---

## Findings

### F13 — The withdrawn "γ = 40" citation is still asserted as fact in three places outside `derivation.md`, including the currently-shipped `src/arty/fragmentation.py` (Deferrable, elevated priority)

**What `derivation.md` does correctly.** §2 explicitly checked the source and
found the quote does not exist: *"An earlier revision of this section claimed
a second, table-free anchor: a Mott prose statement on p. 308 reading 'for
mild steel … assume γ = 40'... That sentence does not exist in the source...
The claim is withdrawn."* I independently re-read the full p. 308 prose in
`rspa.1947.0042.md` and confirm: no "assume γ = 40" sentence exists anywhere
in the file; the only "mild steel" sentence quotes no γ and concerns fragment
length. This part of the derivation is correct and the withdrawal is
warranted.

**What is still live elsewhere.** The identical fabricated quote is asserted
as a real, corroborating source fact in:

- `scoping.md:70`: *"Text, p. 308 (md 289): 'for mild steel … assume γ = 40'
  — a period sanity anchor for the low-carbon end."*
- `scoping.md:139`: *"...('for mild steel … assume γ = 40', p. 308) lands on
  the band's low end independently."*
- `src/arty/fragmentation.py:65–66` (the **currently shipped** comment on the
  `STEELS["US WW2 WDSS1"]` entry): *"Mott's own 'for mild steel assume gamma =
  40' (p.308) reproduces the band-low value independently."*

The third is the important one: this is not a draft or a proposed edit, it is
the live comment in the file that ships today. `derivation.md`'s own Status
line ("no `src/arty/` edits (this file only)") and §8 ("append the §6(b)
entry to `STEELS`") both describe the `STEELS["US WW2 WDSS1"]` entry as
**not yet created** — but it already exists (confirmed by reading
`src/arty/fragmentation.py:62–79` directly), with the numerically-correct
`gamma=47.0` (this is the coincidence §2 documents: 46.7 old-linear and 47.13
new-linear both round to 47) but the **stale, pre-fix comment**, including the
fabricated quote and the old table's now-wrong bracket (`gamma = 32` for
0.1 %C, a `0.2 %C` segment boundary, `gamma = 40/53` band endpoints — the
corrected values used throughout `derivation.md` §2/§4 are 42, 0.25 %C, and
45/49 respectively). A companion, non-fabricated staleness sits in
`tests/test_fragmentation.py:155–157`'s comment: *"its 0.14 %C band endpoint
(gamma=40) gives ~3740, only ~25 % above the 3000 floor"* — the corrected
figures (matching `derivation.md`'s own C4) are γ=45 → N(>0.5 g)=4126, ≈38 %
above the floor. The test's *assertions* are unaffected either way (both old
and new figures satisfy the [3000, 8000] bound), only the comment is wrong.

**Impact:** zero on any computed μ, N₀, N(>0.5 g), or R₅₀ value — `gamma=47.0`
in the shipped `SteelParams` is correct and untouched by this finding. This is
a source-attribution/provenance defect, not a physics defect. But it is a
live, shipped, false attribution to a real, cited scientific paper — exactly
the class of problem this revision's §2/A9 was written to eliminate, and the
elimination did not reach the file where the same sentence is actually
shipped to users (as a code comment) or the sibling planning document
(`scoping.md`) that `derivation.md`'s own header cites as "approved."

**Why Deferrable, not Blocking:** no demo output, test result, or sign
changes; the numeric value in the shipped code is already correct.

**Suggested corrections (not applied):**

1. Replace `src/arty/fragmentation.py:62–73`'s `STEELS["US WW2 WDSS1"]`
   comment with the corrected block `derivation.md` §6(b) already drafts
   (which is clean — no fabricated quote, uses `gamma=42`/`0.25 %C`/`45–49`).
   Since the entry already exists, this is a **replace**, not the "append"
   `derivation.md` §8 currently describes — §8 should be corrected to say so,
   or a future implementation pass may see the key already present and skip
   the fix.
2. Update `tests/test_fragmentation.py:155–157`'s comment to the corrected
   γ=45 / N(>0.5 g)=4126 / ≈38 % figures.
3. Refresh `scoping.md:70,139` (and, more broadly, `scoping.md`'s whole "What
   it supports" section, §2 — see F16 below) to remove the fabricated quote
   rather than presenting it as a "period sanity anchor."

### F14 — Assumption **A5** and the "Limitations-page entries" list restate the pre-fix conclusion, directly contradicting §4/C3/C7 in the same document (Deferrable, elevated priority)

**The contradiction.** `derivation.md`'s header (lines 13–17) explicitly
claims this was fixed: *"the shipped baseline γ = 65 therefore **overstates**
rather than understates the grade contrast — A5."* But A5 itself
(`derivation.md:446–450`) still reads:

> The catalogued pair gives the **smallest** defensible contrast (−38.5 % on
> N₀ against −47 %/−50 % for rule-consistent baselines). Direction is robust;
> **magnitude is a lower bound**.

and the "Limitations-page entries" list (`derivation.md:490`) repeats it:
*"A5 (contrast is a lower bound)."* Both are the **opposite** of what the
same document's own corrected analysis concludes. C7's own recomputed table
(`derivation.md:316–322`, independently reproduced by me above) shows every
rule-consistent alternative baseline (γ=63.5, 60.45, 60.35) gives a
**smaller**-magnitude contrast (−36.3 %, −31.4 %, −31.3 %) than the shipped
γ=65 (−38.5 %) — i.e. the shipped value is the **largest**-contrast choice,
an **upper** bound, exactly as §4 (line 208–214), C3 (line 266), and C7
(line 323–324) each independently and correctly state elsewhere in the same
file. The "−47 %/−50 %" figures quoted in A5 do not appear anywhere else in
the revised document — they are a stale carry-over from the pre-fix version's
extrapolation-based reasoning (`γ≈72–75` at the old, misread table), which
the revised C7 (an interpolation now, not an extrapolation) explicitly
supersedes.

**Impact:** zero on any computed number — this is purely a direction-of-bound
claim, and every other instance of the same claim in the document is correct.
But A5 is precisely the item flagged for `_limitations.qmd` in the
"Limitations-page entries" list, so as currently worded the eventual
limitations page would tell a reader the model **understates** the grade
contrast (true effect could be as large as −50 %) when the document's own
corrected analysis says the opposite (the shipped −38.5 % is itself the upper
bound; a rule-consistent baseline would shrink it to ≈−31 %). This is a
narrative/confidence-direction reversal about to ship into user-facing
documentation, not a numeric one.

**Why Deferrable, not Blocking:** no output changes; the correct statement of
this fact is present and correct three times elsewhere in the same document
(§4, C3, C7), so a reader who reaches any of those gets the right answer —
only A5 and its Limitations-page echo are stale.

**Suggested correction (not applied):** reword `derivation.md:446–450` and
`:490` to match C7's actual conclusion: *"The catalogued pair gives the
**largest** defensible contrast (−38.5 % on N₀, against −31 %/−36 % for
rule-consistent baselines). Direction is robust; **magnitude is an upper
bound**"* — consistent with the header's own claim of having already made
this fix, and with §4/C3/C7.

### F15 — Dangling **A9** cross-references: three places cite it, but the assumption log runs only A1–A8 (Deferrable)

`derivation.md:18` ("...does not exist in the source (§2, A9)"),
`:34` ("...no γ value for any grade — see A9"), and `:124` ("...that is
sufficient (A9)") all point to an assumption **A9** that would formalize the
§2 withdrawal of the fabricated citation. But §7's assumption log
(`derivation.md:426–487`) runs only **A1–A8** — there is no A9 bullet, and it
is not in the "Limitations-page entries" list either. This is the same defect
class the prior review pass already caught once, one increment earlier
(review.md's F12, dangling "A8" references before A8 existed) — it has now
recurred for A9. Impact: zero on any computed number; the correct substance
(the citation doesn't exist, the withdrawal costs nothing) is present in §2's
prose, just never promoted to a numbered, citable assumption entry.

**Suggested correction (not applied):** add an **A9** bullet to §7 with the
content already drafted in §2 ("the withdrawn Mott prose citation; costs
nothing because the interior-segment interpolant no longer needs an external
anchor"), and add it to the "Limitations-page entries" list — or remove the
three "A9" cross-references if no such bullet is intended.

### F16 — `scoping.md` was not updated for the OCR re-extraction and is now comprehensively stale relative to `derivation.md` (Deferrable, out-of-scope-adjacent — flagged because `derivation.md` cites it as "approved")

`scoping.md`'s modification time predates this revision, and it still
presents the **pre-fix** table throughout as current fact: γ = 20/32/53/67 at
0/0.1/0.2/0.3 %C (`scoping.md:61`, cf. the corrected 20/42/53/67 at
0/0.1/0.25/0.45 %C in `derivation.md` §2); reduction-in-area "falling
0.83 → 0.45" (`scoping.md:62`, a *third*, different pair from both the
corrected table and `derivation.md` A3's own "0.75 → 0.55" — see F17); the
withdrawn γ=40 quote as a supporting anchor (F13); an ambiguous
tons/in²-vs-kg/mm² stress-unit question (`scoping.md:75–77`) that the
re-extraction has since resolved (the units are legibly kg/mm², per
`derivation.md` §3); the recommendation text's own band endpoints "γ ≈
40/53" (`scoping.md:168`); and the same stale "smallest defensible contrast"
framing as F14, repeated independently at `scoping.md:198–199`. None of this
changes Option A's selection or any shipped number, but a reader who opens
`scoping.md` (which `derivation.md`'s own header calls "approved" and directs
readers to for "the label crosswalk") would see the withdrawn table, the
fabricated quote, and the inverted-bound framing presented as current,
uncontradicted fact. Suggest a follow-up pass refresh `scoping.md` §2–§5 to
match `derivation.md`'s corrected table and C7 conclusion, or at minimum add
a header note analogous to `derivation.md`'s own revision note pointing
readers to the corrected numbers.

### F17 — A3's reduction-in-area figures do not match the (corrected) source table (Deferrable, low priority)

`derivation.md:433–435` (A3): *"the same table shows reduction-in-area
falling 0.75 → 0.55 across 0.1–0.2 % C."* The corrected table (§2, and
independently re-read from `rspa.1947.0042.md` directly) gives reduction in
area 0.70 at the 0.1 %C row and 0.63 at the 0.25 %C row (linearly interpolated
≈0.65 at 0.2 %C) — neither endpoint matches 0.75 or 0.55, and no combination
of tabulated rows produces that pair. Unlike the other now-superseded figures
in this document, this one is not marked as an "earlier revision" artifact,
so a reader would take it as a checked, current fact. Impact: zero — A3's
qualitative conclusion (the μ closure has no ductility term, and the omitted
effect pushes in the same direction as the γ-channel, i.e. *understates* the
WDSS-1 contrast) does not depend on the specific numeric pair quoted.

**Suggested correction (not applied):** correct to the table's actual values
(0.70 → ≈0.65 across the WDSS-1 band's bracketing rows, or 0.83 → 0.57 if the
intent was the full iron-to-0.45 %C range) or drop the specific numbers and
keep only the qualitative "falls with carbon" claim, which is supported.

### F18 — All numeric claims in §1–§5 independently re-verified (Note)

Ran `recompute.py` directly and independently re-derived by hand: local-linear
γ (44.933/47.133/49.333 at 0.14/0.17/0.20 %C) and Newton-quadratic γ
(44.975/47.187/49.381) via divided differences on the corrected
`(0.0,20),(0.1,42),(0.25,53),(0.45,67)` series — both match `derivation.md`
§2/C6 to reported precision. §4's table (μ 0.3305/0.5375/0.5737/0.5049 g, N₀
18217/11201/10494/11923, N(>0.5 g) 5324/4269/4126/4408, R₅₀
98.937/101.449/101.404/101.419 m) and the headline contrast (+62.6 %/−38.5 %/
−19.8 %/+2.51 m) reproduce exactly. C2 identifiability re-confirmed bit-exact
(0.000e+00) at k=0.5/2/137. C4's floor-margin claims independently re-derived
by root-finding: the N(>0.5 g)=3000 floor is crossed at γ≈31.41 (matches "γ ≈
31"), requiring R to grow 43.26 % from the band-low case (matches "43 %"). C5's
brittle limit (μ=1.732e-7 g, N₀=3.476e10 at γ=1e6) reproduces exactly. C7's
alternate-baseline table (N₀ 18217/17590/16336/16297 at γ=65/63.5/60.45/60.35,
contrasts −38.5 %/−36.3 %/−31.4 %/−31.3 %) reproduces exactly — confirming
the *magnitudes* in F14 are correct even though the *bound-direction wording*
around them is stale. C8's R₅₀ sweep reproduces at every γ `recompute.py`
itself prints (35/40/45/47/49/53/57/65/72), and I independently computed the
two extra points `derivation.md`'s table quotes but `recompute.py`'s own
sweep does not print (γ=50 → R₅₀=101.359 m, matches "101.36"; γ=75 →
R₅₀=97.054 m, matches "97.05") using `recompute.py`'s own `evaluate()`
function. Eq. (2)'s scaling law (δμ/μ = 1.5 δR/R) cross-checks exactly against
the table: (65/47)^1.5 = 1.6265 → +62.6 % on μ, 1/1.6265 = 0.6148 → −38.5 % on
N₀, both bit-consistent with the independently-computed table. C1's
dimensional analysis is algebraically correct. No action needed on any of
these.

### F19 — Source re-reading confirms the corrected table and the two quoted equations are transcribed accurately (Note)

Independently re-read `rspa.1947.0042.md`'s §3 table and surrounding prose in
full. Confirmed exact matches to `derivation.md`: the table
(iron/0.1C/0.25C/0.45C rows, reduction-in-area 0.83/0.70/0.63/0.57, $P_f$
54/70/80/82, $P_y$ 34/42/45/38, γ 20/42/53/67); the $P_f$/$P_y$→MPa conversion
(530–805 MPa via the standard kgf/mm² factor, used only for A4, never as
$\sigma_F$); the exact quote used in C3 ("a rapid rate of hardening near the
fracture point (i.e. a large value of $P_y$) will lead to small fragments");
and eq. (5)'s fragment-length relation
($\ell\propto P_f\sqrt{(1+s_f)/(\rho P_y)}$), whose reduction to
$\ell\propto\gamma^{-1/2}$ via $\gamma\sim160P_y/[P_f(1+s_f)]$ I re-derived
algebraically and confirms the derivation's claimed exponent match against
the implemented $\mu\propto\gamma^{-3/2}$ closure. No misquotes or fabricated
content found in any of the *currently retained* citations (only the
already-identified, already-withdrawn "γ=40" sentence was fabricated, and it
is correctly absent from `derivation.md`'s own body text — see F13 for where
it still lingers elsewhere).

### F20 — Out-of-scope observation: the source doc's own "flagged, not yet fixed" note is itself now stale (Note)

`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`'s
header carries a "Downstream impact — flagged, not yet fixed" note stating
that `derivation.md` §2 still interpolates using "the old, now-known-wrong
bracketing points (0.1 %C→32, 0.2 %C→53)." That is no longer true —
`derivation.md` §2 has in fact been corrected to the right bracket (0.1 %C→42,
0.25 %C→53). This is a `doc-reference`/librarian-owned file, out of this
review's primary scope, but flagged since a future reader or automated
extraction-quality check could be misled into re-flagging an already-resolved
item, or conversely into missing that `derivation.md` needed the correction
this note describes (it did, and got it).

### F21 — Minor stale line-number citation (Note)

`derivation.md:269` (C4) cites `tests/test_fragmentation.py:141` for the
N(>0.5 g)∈[3000, 8000] assertion; the actual assertions currently sit at line
149 (single-grade test) and line 162 (the parametrized all-grades test C4 is
actually describing). Cosmetic, no output impact.

---

## Checklist pass-through (this pass)

- **Dimensional analysis:** correct, re-verified (C1, F18).
- **Boundary cases:** composition-band endpoints (0.14/0.20 %C) and the
  baseline midpoint (0.355 %C) all re-confirmed strictly interior to their
  respective Mott segments (no extrapolation on either side, a genuine
  improvement from the pre-fix version where the baseline was extrapolated);
  γ→∞ / σ_F→0 limits re-confirmed monotone, no singularity.
- **Parameter ranges:** γ=47 (band 45–49) sits inside Mott's 0.1–0.25 %C
  segment; the rule-consistent baseline range (60.35–63.5) sits inside the
  0.25–0.45 %C segment — both interpolations, re-confirmed.
- **Numerical stability:** C2 identifiability re-confirmed bit-exact at
  k=0.5/2/137; no division-by-zero or sign-change paths touched.
- **Physical plausibility:** N(>0.5 g) 4126–4408 (WDSS-1 band) and 5324
  (baseline) all centrally inside the validated 3000–8000 band; γ=47 sits
  mid-range of Mott's tabulated 20–67.
- **Source attribution:** the *physics* citations (table values, the P_y
  quote, the fragment-length equation) are accurate and independently
  re-verified against the source (F19). The *specific fabricated citation*
  this revision set out to remove is correctly removed from `derivation.md`'s
  own body text, but is **not** removed from `scoping.md` (×2) or from the
  comment currently shipped in `src/arty/fragmentation.py` (F13) — the one
  real gap in this checklist item.
- **Layering:** N/A for `derivation.md` itself (still a documentation-only
  pass, no new `src/`/`.qmd` edits made *by this revision*). Note in passing
  (F13) that `src/arty/fragmentation.py` already contains both `STEELS`
  entries from an earlier implementation pass, which `derivation.md`'s
  Status line and §8 do not accurately reflect.
- **Limitations/constraints check:** the *content* of A1–A8 is otherwise
  sound and thorough. Two of the entries meant to feed `_limitations.qmd`
  (A5, and the dangling A9) need correction/completion before that page is
  written (F14, F15).
- **Data-driven analysis:** strong — every printed number independently
  reproduced end-to-end, including two C8 points not in `recompute.py`'s own
  printed sweep (F18).

---

## Suggested corrections (not applied)

1. Replace the stale `STEELS["US WW2 WDSS1"]` comment in
   `src/arty/fragmentation.py:62–73` with `derivation.md` §6(b)'s corrected
   text (F13); correct `derivation.md` §8's "append" framing to "replace" and
   note the entry already exists.
2. Update `tests/test_fragmentation.py:155–157`'s stale γ=40/~3740/~25 %
   comment to γ=45/4126/≈38 % (F13).
3. Remove the fabricated "assume γ = 40" quote from `scoping.md:70,139`
   (F13), and refresh `scoping.md` §2–§5 more broadly to match the corrected
   table and C7's conclusion (F16).
4. Reword `derivation.md` A5 (`:446–450`) and its Limitations-page echo
   (`:490`) from "smallest contrast / lower bound" to "largest contrast /
   upper bound," consistent with §4/C3/C7 and the header's own claim of
   having already made this fix (F14).
5. Add a formal **A9** bullet to §7 (or remove the three dangling
   cross-references) covering the withdrawn-citation content already drafted
   in §2 (F15).
6. Correct or drop the specific "0.75 → 0.55" reduction-in-area figures in A3
   (F17).
7. Optional/cosmetic: fix the `tests/test_fragmentation.py:141` line
   reference in C4 (F21); note to @librarian that
   `rspa.1947.0042.md`'s own "flagged, not yet fixed" header note is now
   resolved and can be updated or removed (F20).

None of the above requires changing any numeric parameter, test bound, or
computed output — every recomputed value in `derivation.md` and
`recompute.py` is independently confirmed correct (F18, F19). This is a
documentation/cross-reference reconciliation gap, not a physics or numerics
defect.

---
---

# Re-review — 2026-07-25 (partials reconciliation pass)

**Reviewer:** model-reviewer agent
**Scope:** `git diff -- experiment/fragmentation-field/ src/arty/fragmentation.py
tests/test_fragmentation.py` — the follow-up pass that reconciled the notebook
partials (`_change-log.qmd`, `_governing-equations.qmd`, `_implementation.qmd`,
`_limitations.qmd`, `_parameters.qmd`), the shipped `STEELS` comments, and
`tests/test_fragmentation.py` against the corrected `derivation.md` (post
Mott-table re-extraction). Per the dispatch brief this is a
consistency-and-correctness check on a reconciliation fix, using
`derivation.md` and `recompute.py` as source of truth — not a re-derivation.
Cross-checked against the specific items the prior re-review (F13–F21 above)
left open.

**Verification method:** read every hunk of the diff in full; ran
`uv run python experiment/fragmentation-field/updates/wdss1-steel-grade/checks/recompute.py`
directly and diffed its output against every number quoted in the diff
(§4 table, C2, C5, C6, C7, C8 all match to reported precision); independently
evaluated the two C8 points (γ=50, γ=75) that appear in `derivation.md`'s
table but not in `recompute.py`'s own printed sweep, via `recompute.py`'s own
`evaluate()` (101.359 m, 97.054 m — both match); ran
`uv run pytest tests/test_fragmentation.py -q` (53 passed); grepped the
diffed files for the specific fabricated/stale strings the prior re-review
flagged (`assume gamma`/`assume γ`, `gamma = 40`/`γ = 40`, `0.2 %C`/`0.2C`,
`gamma = 32`/`γ = 32`, `smallest defensible`, `understate[s]` in a steel
context); read `scoping.md` in full (not part of this diff — untracked,
unchanged by this pass) to confirm it was correctly left out of this pass's
scope rather than silently skipped.

## Verdict: **PASS-with-limitations**

The reconciliation is complete and correct for everything this pass actually
touched. Every number in the six notebook partials, the `STEELS` comments in
`src/arty/fragmentation.py`, and the new/updated tests now agrees with
`derivation.md`'s corrected Mott table (0.0→20, 0.1→42, 0.25→53, 0.45→67) and
its corrected C7/A5 conclusion (shipped baseline γ=65 gives the **largest**,
not smallest, grade contrast — an upper bound). The fabricated "assume γ=40"
citation and the reversed "understates"/"smallest defensible contrast"
wording that the prior re-review (F13, F14) found live in the shipped code
comment and the test comment are both gone and replaced with the corrected
figures. No physics, computation, or parameter values leaked into the `.qmd`
partials. Full test suite passes (53/53). Two items remain open, both
pre-existing and explicitly Deferrable already in the prior re-review passes
(F13/F16, F12) — this pass did not introduce them and was not scoped to fix
them, but they should be closed in a follow-up housekeeping pass since this
is now the fourth review pass to note at least one of them.

---

## Findings

### G1 — Notebook partials, `STEELS` comments, and tests: fully reconciled (Note)

Checked every diffed number against `recompute.py`'s live output:

- `_change-log.qmd` v0.7.0 row: "N₀ by 38.5 %... R₅₀ moves only +2.5 %" — matches
  recompute (`-38.5%`, `+2.51 m / +2.5%`). The γ-sensitivity note rewrite
  ("R₅₀ barely moves... ≈2 m: 101.1 m at γ=53 vs 98.9 m at γ=65") matches the
  corrected table's `0.25–0.45 %C → γ=53/67` bracketing and the C8 sweep
  values (101.105, 98.937 m).
- `_governing-equations.qmd`: "γ = 53 for 0.25%C steel and γ = 67 for
  0.45%C steel" and the new $(k\sigma_F,k\gamma)$ identifiability paragraph
  both match `derivation.md` §1/§2 exactly (non-uniform row spacing correctly
  stated).
- `_implementation.qmd`'s new grade-contrast cell calls `mott_params`/`mott_N`
  directly on `STEELS.items()` — no inline physics — and its prose ("−38 %
  swing in N₀ shifts R₅₀ by only ≈+2.5 %... non-monotone... maximum at γ=47")
  matches C8.
- `_limitations.qmd`'s revised "γ, σ_F ~25% uncertainty" paragraph now cites
  §3, 0.25–0.45%C/53–67 (previously the stale 0.2%C/0.3%C, 53–67 pairing) —
  correct under the corrected table. New Limitation 13 correctly summarizes
  A5 (upper bound, −38.5% vs −31%/−36%), A6/A8 (baseline composition
  unconfirmed), and C8 (R₅₀ +2.5% for a −38.5% N₀ move) with all figures
  matching `derivation.md`.
- `_parameters.qmd`'s new catalog table and print cell are presentation-only
  (calls `STEELS`, formats `rho`/`sigma_f/1e6`/`gamma` — no derived physics).
- `src/arty/fragmentation.py`'s `STEELS["WW2 US HE Shell"]` comment now reads
  "steel 0.45 C" (not the stale "0.3 C") and "OVERstates rather than
  understates... A5" (not the withdrawn "understates"/"~72-75") — this is the
  corrected text and it is now internally consistent with the rest of the
  document's C7/A5 conclusion. The `STEELS["US WW2 WDSS1"]` comment has no
  trace of the fabricated "assume γ=40" quote flagged in the prior re-review's
  F13 — it correctly cites only the table interpolation (γ=42→0.25%C→53).
- `tests/test_fragmentation.py`'s new comment on
  `test_mott_fragment_count_in_pafrag_range_all_grades` reads "γ=45... ~4126,
  about 38% above the 3000 floor" — the corrected figures (F13's flagged stale
  values were γ=40/~3740/~25%) — matches `derivation.md` C4 exactly.
- Full suite: `uv run pytest tests/test_fragmentation.py -q` → 53 passed.

No dimensional, sign, or magnitude discrepancies found anywhere in the
reviewed diff. Composition-band boundary cases (0.14/0.20 %C) and the γ→∞
brittle limit are unchanged from the already-verified `derivation.md` and
remain physically sound (N(>0.5 g) centrally inside the validated 3000–8000
band throughout).

### G2 — `scoping.md` still carries the fabricated γ=40 quote and the reversed "smallest defensible contrast" wording (out-of-scope for this pass; pre-existing, already logged — Deferrable, unchanged status)

`scoping.md` is untracked and was not touched by this diff, so it is correctly
out of this pass's stated scope ("notebook partials... and
`src/arty/fragmentation.py`"). But it still contains, unchanged:

- `scoping.md:70,139` — the fabricated "for mild steel … assume γ = 40, p.
  308" quote, presented as a real corroborating source fact. §2/A9 of
  `derivation.md` has independently confirmed (twice, across two review
  passes) that this sentence does not exist anywhere in
  `rspa.1947.0042.md`.
- `scoping.md:198–199` — "the shipped catalogued baseline γ = 65 already
  gives the smallest defensible contrast" — the reversed conclusion; C7 in
  the current `derivation.md` shows 65 gives the **largest** contrast (an
  upper bound), and this exact discrepancy was already flagged as F14 in the
  prior re-review pass above.
- `scoping.md:61–62` still presents the pre-fix table (γ=20/32/53/67 at
  0/0.1/0.2/0.3 %C, RA falling 0.83→0.45) as current fact, superseded by
  `derivation.md`'s corrected 20/42/53/67 at 0/0.1/0.25/0.45 %C.

**Impact:** zero on any computed number, test, or rendered output — nothing
in `scoping.md` is imported or executed, and `derivation.md`/the shipped code
already carry the corrected values. This is the same item the prior re-review
flagged as F13 (scoping.md component) and F16, both explicitly Deferrable
there; nothing here elevates it. Flagging again only because this is now the
third consecutive review pass to note it un-closed, and because a reader who
opens `scoping.md` after this reconciliation pass (which fixed everything
downstream of it) would still see the withdrawn table and the fabricated
quote presented as settled fact, immediately upstream of the now-correct
`derivation.md`.

**Suggested correction (not applied):** in a follow-up housekeeping pass,
refresh `scoping.md` §3 (table, quote) and §5/G2 (bound direction) to match
`derivation.md`'s corrected table and C7 conclusion, per F13/F16/F14's
original suggested wording above.

### G3 — `derivation.md`'s own §6(a) "text as shipped" block and Status line are stale relative to the code this same reconciliation pass just shipped (out-of-scope for this pass; pre-existing, already logged — Note)

Two residual self-inconsistencies inside `derivation.md` itself (not in the
reviewed diff, but worth flagging since `derivation.md` is the review's stated
source of truth):

1. `derivation.md`'s header **Status** line (line 19) still reads "derivation
   pass — no `src/arty/` edits (this file only)", and §8 (line 520 area)
   still frames the `STEELS["US WW2 WDSS1"]` entry as something "the next
   pass" will append — but `src/arty/fragmentation.py` already carries both
   entries (confirmed above), and this very diff just edited them. Same
   defect class the prior re-review flagged as part of F13.
2. `derivation.md` §6(a)'s quoted "the block below is the text **as
   shipped**" code block (lines 376–400) still shows the **pre-fix** wording
   — `"steel 0.3 C"` (not `"0.45 C"`) and `"understates... ~72-75"` (not
   `"OVERstates... ~60.4"`) — while the code that is *actually* shipped (and
   verified correct in G1 above) has the corrected text. A reader who diffs
   §6(a)'s quote against the real file would see a mismatch and could
   mistakenly conclude the shipped code is wrong, when in fact the code is
   right and the quote is stale. This is exactly suggested-correction #4 from
   the "src/ implementation pass" review above (F12), still open.

**Impact:** zero — both are `derivation.md`-internal documentation drift; the
shipped code and every downstream `.qmd`/test file are correct (G1). Not
introduced by this pass, not in its stated scope, and does not change the
verdict.

---

## Checklist pass-through (this pass)

- **Dimensional analysis:** unchanged, re-confirmed correct via `recompute.py`.
- **Boundary cases:** composition-band endpoints and γ→∞ limit unchanged from
  the already-verified `derivation.md`; nothing new introduced by this diff.
- **Parameter ranges:** γ=47 (band 45–49) within Mott's 0.1–0.25 %C segment;
  σ_F/ρ unchanged. All within the fidelity bar.
- **Numerical stability:** C2 identifiability bit-exact at k=0.5/2/137
  (re-confirmed via `recompute.py`); no new division-by-zero/sign-change paths.
- **Physical plausibility:** N(>0.5 g) 4126–4408 (WDSS-1 band) and 5324
  (baseline) all centrally inside the validated 3000–8000 band; fewer/larger
  fragments for the lower-carbon grade, test-pinned and correctly signed.
- **Source attribution:** the fabricated "assume γ=40" citation and the
  reversed "understates" wording are fully removed from every file in this
  diff's scope (G1). They persist only in the untracked, unmodified
  `scoping.md` (G2), which is outside this pass's stated scope.
- **Layering:** clean — the new `_implementation.qmd`/`_parameters.qmd` cells
  call `mott_params`/`mott_N`/`STEELS` only; no physics, formula, or
  parameter value is computed or hard-coded inline in any `.qmd`.
- **Limitations/constraints check:** new `_limitations.qmd` Limitation 13
  correctly and completely carries A5/A6/A8/C8 forward with matching figures;
  nothing required by `derivation.md`'s "Limitations-page entries" list (§7)
  is missing from it.
- **Data-driven analysis:** strong — every number in the diff independently
  reproduced against a live `recompute.py` run plus a full green test suite
  (53/53).

---

## Suggested corrections (not applied)

1. (Deferrable, pre-existing, not this pass's scope) Refresh `scoping.md` per
   G2 — remove the fabricated γ=40 quote (`:70,139`), fix the pre-fix Mott
   table (`:61–62`), and correct the reversed "smallest defensible contrast"
   wording (`:198–199`) to match `derivation.md`'s corrected C7/A5.
2. (Note, pre-existing, not this pass's scope) Update `derivation.md`'s own
   Status line/§8 framing to reflect that the `src/arty/` edits already
   exist, and resync §6(a)'s quoted "as shipped" code block with the actually
   shipped comment (G3).
3. No changes needed to any file actually in this diff's scope — every number,
   citation, and test in the six `.qmd` partials, `src/arty/fragmentation.py`,
   and `tests/test_fragmentation.py` is correct and consistent with
   `derivation.md` (G1).
