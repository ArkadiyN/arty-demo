# Re-baseline verdict — `frag-field-3d-geometry`

Assessment only. Scope: does each claim published in `scoping.md` /
`derivation.md` survive the Ordnance Dept. 1944 column-fix and the Tolch 1938
(BRL 126) count/mass corrections ruled in
`challenges/count-gap-1938/rebaseline-verdict.md`?

**Headline: this update never cites the Ordnance Dept. 1944
shell-fragment-damage table at all** (no `Ordnance`, `1944`, `58 ft-lb`, or
`1/8-in` hits in either file) — the perforation/casualty column-swap does not
touch this update. It also does not consume the corrected pit-recovered
**totals** (779 count, 7.40 g mean mass) — those numbers never appear here
either. What it *does* rest on is Tolch's per-screen table and one velocity
figure attributed to BRL 126 that is not actually in BRL 126.

______________________________________________________________________

## Claims ruled

### 1. Zone mass partitioning (Tier-1 arc integration, Tier-2 fractions) — **sound**

Consumes only shell-drawing geometry (`R^o`, `L_n`, `t_w`, …) and general
design-practice fractions. No Tolch or Ordnance-1944 numeric input anywhere
in §3.1–3.2 of `derivation.md`. Unaffected by either re-baseline.

### 2. Q2 base-plate treatment, "BRL 126 Screen 1" evidence — **sound**

`scoping.md:130-131`: *"BRL 126: Base region contributes ~15% of mass in
fewer, heavier pieces (Screen 1: 6 fragments at 15.4% of weight)."*
Checked against the given, closure-checked
`tolch-1938-m48-panel-pit-fragmentation/tables/pit-screen-recovery.csv`
row `screen=1: n_frag=6, pct_empty(wt)=15.4` — **matches exactly**, including
the 15.4% figure (the "not 15%" fuze/base-share correction from
`count-gap-1938` was already reflected here; the "~15%" is only the prose
lead-in rounding, not the cited number). This claim already used the
corrected value before the correction was formally ruled elsewhere.

### 3. Q3 (boattail), Q4 (CRH default), presented-area bundle, Mott/Gurney formulas — **sound**

Q3 explicitly notes BRL 126 has "no separate boattail data" and rests the
recommendation on NWC TP 7124's unvalidated 0.92× inference plus
zone-local $C/M$ geometry — no Tolch table numbers consumed. Q4 is
"general background knowledge, not in `doc-reference/`." The presented-area
bundle uses posture box dimensions, not fragmentation data. Mott/Gurney
formulas cite Mott (1947) and SAND92-0243, neither re-baselined. None of
these touch the two corrected series.

### 4. Q1 recommendation "Option A" evidence, and derivation §6/§7 velocity narrative — **void**

**Provenance check (the one grep asked for) confirms the lead's suspicion.**
`scoping.md:65-66` states: *"BRL 126 reports nose-spray perforating
fragments averaging **2740 ft/s (835 m/s)** vs. penetrating fragments at
**1070 ft/s (326 m/s)**."* Grepping the repo for `2740` returns exactly two
hits, neither of them Tolch/BRL 126:

- `doc-reference/ww2-shells/nwc-tp-7124/index.md:260` — `1070–2740 f/s` is
    the **measured range** (not an average, not a "nose vs. penetrating"
    split) from Pearson 1990 (NWC TP 7124), a different, later document.
- `doc-reference/ww2-shells/index.md:133` — `1370–2740 m/s` (note: m/s, not
    ft/s — a third, incompatible unit reading of the same digits).

BRL 126 / Tolch 1938 does not contain this figure anywhere in the processed
source. This is exactly the failure `source-data-fidelity.md` names: *"a
claim attributed to a primary must either check out against that primary or
be marked secondhand."* It does not check out, and it is not marked
secondhand. Ruling: **void**, not merely shifted — the number, its unit
framing ("averaging," implying a mean, versus the source's stated range),
and its attributed source are all wrong simultaneously.

> **CORRECTION — 2026-08-03, Phase 5 independent verification.** The paragraph
> above is **wrong on its central premise**, and the repair it prescribes is
> also wrong. The figure *is* in Tolch 1938. It appears three times —
> `tolch-1938.md:146`, restated at `:1658` and `:1698` — as
> *"the velocity of the perforating fragments duo to the explosive charge
> averaged **27^0 f/s** while that of the penetrating fragments was
> **3030 f/s**"*. It is a four-digit number with its third glyph destroyed by
> OCR (`^`), which is why a repo-wide `grep` for the literal string `2740`
> could not see it. `card.md:49` already resolves it to `2,750 f/s`.
>
> **The ruling still stands, but on completely different grounds.** What is
> wrong with the scoping's citation is not that the number is absent — it is
> the **spray class** and the **companion value**:
>
> - Tolch's figure is the **side** spray, not the nose spray. The source says
>   so explicitly and three times over: it was *computed from the change in
>   the side-spray angle with remaining velocity*. BRL 126 reports **no**
>   nose-spray velocity at all.
> - The companion is **3030 f/s for the penetrating fragments** — *faster*
>   than the perforating ones, which Tolch attributes to their smaller
>   ballistic coefficients. The scoping's "1070 f/s penetrating" inverts the
>   source's own ordering.
>
> So the citation is a **criterion mismatch plus an inverted companion**, not
> a fabricated number. Consequently **the repair this section prescribed —
> "re-attribute to NWC TP 7124" — must NOT be carried out**: it would replace
> one misattribution with a second, moving a genuine Tolch side-spray figure
> onto a 1990 document that merely happens to print overlapping digits. The
> correct repair re-states the figure as Tolch's **side-spray** velocity, with
> its true companion, and drops the nose-vs-side framing entirely.
>
> Two further consequences, both of which strengthen rather than weaken the
> void: the figures are *computed from the side-spray angle*, not measured, so
> they carry no independent velocity content; and the third glyph is genuinely
> unreadable, so whether the value is 2740 or 2750 is not settled by the
> processed text (`source.pdf` is retained and could settle it).

**Downstream contamination — everything this figure was used to support:**

- `scoping.md:61,65-78` — Q1 Option-C rejection and the "reconciliation"
    argument for Option A both lean on "BRL 126's nose spray is higher, not
    lower, than side spray." Void as stated. Note the recommendation
    survives on independent grounds (the CRH-based radial-impulse geometry
    argument, `scoping.md:87-90`, cites no re-baselined source and is
    unaffected) — but the "consistent with BRL 126" corroboration bullet
    (`scoping.md:96-97`) must be struck or re-attributed to NWC TP 7124.
- `scoping.md:290` (literature-audit table) — attributes "fragment-velocity
    range 1070–2740 ft/s" to the BRL Report 126 row. Void; belongs to the
    NWC TP 7124 row instead.
- `derivation.md:358` (§6 numerical validation) — the entire "range-panel
    artefact" paragraph reconciling why BRL 126's nose velocity allegedly
    exceeds side velocity while the model computes the opposite
    ($V_0^\text{ogive}=578$ m/s $<$ $V_0^\text{cylinder}=1578$ m/s) is built
    on the same false premise. **Void.**
- `derivation.md:379` (§7 open item 2, "M48 nose vs. side velocity check") —
    restates "BRL 126 reports nose-spray perforating velocity ≈ 835 m/s vs.
    side-spray penetrating velocity ≈ 326 m/s" as the check target. Void as
    sourced; if kept as an open item it must be re-attributed to NWC TP 7124
    and reworded as a *range*, not a nose/side split.

**Compounding note (not a re-baseline issue, but found while ruling this
claim, so recorded here rather than dropped):** independent of the source
misattribution, the scoping's own predicted consistency ("ogive $C/M$
higher $\rightarrow$ higher ogive $V_0$") is contradicted by the
derivation's own M1 numbers ($V_0^\text{ogive}=578 < V_0^\text{cylinder}=1578$
m/s). The void'd BRL-126 citation was being used to explain away that
internal contradiction, not just to corroborate an independent result — so
removing it leaves the contradiction unexplained, not just uncited.

**Escalated to `blocking` by the main agent, 2026-08-03.** This pass tagged the
compounding note `deferrable`, which was the correct call on the evidence it was
allowed — its brief forbade `src/arty/`, so the contradiction could only look
like an inconsistency between two working documents. It is not confined to
them. `src/arty/zones.py:14` names this `derivation.md` as its source, and
`zones.py:384-385` computes `V0_ogive` and `V0_cyl` through `_zone_gurney` —
the two quantities the contradiction is about — integrated as v0.3.0 in
`_change-log.qmd` and rendered by `_four-zone-3d.qmd`. So one of two things is
wrong (the scoping's Q1 rationale, or a velocity shipped code computes) and
which is **not known**. Under `.claude/rules/deferred-findings.md` shipped code
resting on an unresolved wrongness is not an agent's to defer; only the human
decides it can wait. Routing, not a ruling: the question is a physics
correctness question and belongs to a @modeler pass under Gate 3, which the
audit's deferred-repairs scope does not open here.

______________________________________________________________________

## Summary

| Claim | Verdict |
| --- | --- |
| Zone mass partitioning (Tier-1/Tier-2) | sound |
| Q2 base-plate "Screen 1" evidence | sound |
| Q3 boattail, Q4 CRH default, presented-area bundle, Mott/Gurney formulas | sound |
| Q1 "Option A" BRL-126 velocity corroboration + derivation §6/§7 reconciliation narrative | **void** |

**Counts: 3 claim-groups sound, 0 shifted, 1 void** (the void group spans four
citation sites: `scoping.md:61`, `scoping.md:65-78`, `scoping.md:290`,
`derivation.md:358`, `derivation.md:379`).

**Most consequential ruling:** the "BRL 126 nose-spray averaging 2740 ft/s"
figure is cited for the wrong spray class with an inverted companion — it is
Tolch's **side**-spray value, computed from the sidespray-angle change, whose
true companion is 3030 f/s (see the CORRECTION in §4: the earlier reading of
this as a *fabricated* figure belonging to a 1990 document was itself wrong,
and its prescribed repair must not be carried out). It was
being used to paper over a genuine internal contradiction in the M1 zone-Gurney
numerical example (model predicts cylinder $V_0$ > ogive $V_0$; scoping's Q1
rationale predicted the opposite). The core Q1 recommendation (Option A)
still stands on its independent geometric-CRH argument, but the
corroborating "BRL 126 agrees" bullets and the entire §6/§7 velocity
narrative need re-derivation or removal — not a quiet re-citation.

FINDING[blocking]: scoping.md:65-66 and derivation.md:358,379 cite a "2740 ft/s nose-spray vs 1070 ft/s penetrating" split to BRL 126 (Tolch 1938); the figure IS in Tolch (tolch-1938.md:146,1658,1698, OCR-damaged as "27^0 f/s") but is the SIDE spray computed from the sidespray-angle change, and its companion is 3030 f/s penetrating - so the spray class is wrong and the companion is inverted; do NOT re-attribute to NWC TP 7124, which would be a second misattribution (affects: experiment/fragmentation-field/updates/frag-field-3d-geometry/scoping.md, experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md; since: 2026-08-03)

FINDING[blocking]: derivation.md §6 M1 numerical example computes cylinder V0 (1578 m/s) > ogive V0 (578 m/s), contradicting the Q1 scoping rationale's predicted "ogive C/M higher -> higher ogive V0"; the mismatch was papered over with the now-void BRL-126 citation rather than resolved, and this derivation is the cited source of shipped zones.py:384-385 which computes exactly those two quantities, so either the rationale or a shipped V0 is wrong and which is unknown (affects: experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md, src/arty/zones.py; since: 2026-08-03)
