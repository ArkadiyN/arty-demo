# Independent verification — 78.6 J / 126 J criterion-match finding (tag: blocking)

**Scope.** Verifies derivation.md line 381's finding marker (tag: blocking)
against the primary source and the current text of the two published files it
names. This is a standalone verification note, not a full review of the
update.

## 1. What the primary source actually says

`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md:309`
(verified directly, PDF p. 78 / printed p. 64):

> "A casualty is supposed caused by a hit with at least 58 ft.-lb. of energy.
> It is incapacitation and not necessarily death."

Confirmed:

- This is a **personnel-casualty (incapacitation)** criterion. The same
    sentence and section define the *other* damage types the source tracks as
    perforation of **1/8-, 1/4-, 3/8- and 1/2-in. mild steel** — never wood, and
    never Tolch's 1-in. softwood panel. `card.md` transcribes the same
    definition and the same steel-perforation list, with no wood-perforation
    claim anywhere in the card.
- **No mass appears** in the sentence, its paragraph, or its section — 58
    ft-lb is stated as one constant energy applied across the fragment
    spectrum. `card.md`'s own retained CSVs close this: e.g.
    `tables/105mm-m1-casualties.invariant` reproduces `0.5*m*v² == 58 ft-lb`
    across a 31× mass span. This corroborates derivation.md §7.1(a)
    independently (I re-derived the invariant claim from the card, not just
    trusted the prose).

So derivation.md's characterization of the 78.6 J figure's *primary* meaning
is accurate: it is a mass-non-specific personnel-incapacitation threshold,
stated by its own source with zero reference to wood or panel perforation.

## 2. What the published surfaces currently claim

- `_limitations.qmd` L1 (~140–144): "at sourced (non-fitted) energy
    thresholds the model predicts $N/779$ = 1.73 (126 J) to 2.00 (78.6 J) and
    $N/700$ = 1.92 to 2.23 ... **met or marginal, not failed**."
- `challenges/README.md` (~55–58): same numbers, same "sourced-threshold rows
    move ... at or inside" framing, same verdict sentence.
- `challenges/count-gap-1938/count-chain.md` (table at ~108, prose at
    112–130, 196, 218–230): explicitly plugs 78.6 J into the same
    `E_thr` → Heaviside perforate/no-perforate step used for the fitted 1.9 J /
    3.6 J rows, computes $m_{thr}$(15 ft) = 0.359 g, $N(\ge m_{thr})$ = 1560,
    and compares that to Tolch's **panel-perforation** count (700/779). It
    calls the row "an independent cross-check, not a fit" and states "Two
    independently-sourced thresholds ... now agree with each other," treating
    numerical proximity to the 126 J row as corroboration of the perforation
    model.

This is not a hedge-and-move-on: 78.6 J is used exactly as if it were a
1-inch-softwood ballistic-limit energy, feeding the same KE-threshold
mechanism that decides whether a fragment perforates Tolch's panel. Nowhere
in the three surfaces I read is it flagged that the 58 ft-lb figure's own
source defines it as a soft-tissue casualty criterion, structurally unrelated
to wood shear-out mechanics.

## 3. Verdict on the mismatch itself

**Real, and correctly scoped to 78.6 J.** Using a personnel-incapacitation KE
threshold — a different failure mechanism (soft-tissue penetration depth vs.
wood plug shear-out), stated mass-independently by a document that never
mentions wood — as a stand-in for a wood-panel perforation threshold is a
criterion mismatch under `.claude/rules/source-data-fidelity.md`'s "criterion
match" gate, and the rule is explicit that this class of defect is Blocking
"however faithful the transcription." Here the transcription is faithful
(78.6 J = 58 ft-lb exactly), which makes it a clean instance of the gate, not
a borderline one.

Note for precision on the FINDING's own wording: the marker and derivation.md
§7.1(b) bundle **126 J** into the same "criterion mismatch" charge. That
bundling is not well supported — 126 J ("Tolch's own smallest-hole bound,
$m\ge0.36$ g at 838 m/s") is computed directly from Tolch's *own* observed
perforating fragment, i.e. it already **is** a wood-perforation-criterion
quantity, sourced from the same experiment the model is tested against. It has
a different, narrower admissibility concern — circularity as an *anchor*
(using Tolch's own data to fix a parameter that is then scored against Tolch's
own totals), which derivation.md §7.1(b) itself raises only in the context of
setting $e_a$ for the superseded Option A′ areal model, not as a reason to
discard the count-chain.md table row. This is a scope-precision note on the
FINDING's text, not a reason to downgrade it — 78.6 J alone is sufficient to
sustain a Blocking finding.

## 4. Impact on the published PASS-arm verdict

Does "the count arm of the PASS test is now met or marginal, not failed" need
to be walked back? **No — it is independently supported by the 126 J row
alone**, which is not criterion-mismatched:

| threshold | $N/779$ | $N/700$ | within 2×? |
| --- | --- | --- | --- |
| 126 J (Tolch hole-size, criterion-matched) | 1.73 | 1.92 | yes, both |
| 78.6 J (casualty, criterion-mismatched) | 2.00 | 2.23 | 2.00 borderline, 2.23 no |

Removing 78.6 J from the admissible set does not flip the verdict — it
removes the *weaker* of the two supporting rows (the one sitting at/outside
the 2× band) and leaves the *stronger* one (126 J, cleanly inside 2× on both
denominators). If anything, the bottom-line conclusion becomes more
comfortably "met" rather than "marginal" once 78.6 J is dropped, not less.

What **does** need correction on the three published surfaces:

1. The characterization of 78.6 J as a "sourced (non-fitted) **energy
    threshold**" for the perforation count arm is inadmissible as stated and
    should either be removed from that role or explicitly re-labeled as an
    unvalidated plausibility cross-check (which is exactly how §7.4 of
    derivation.md itself now treats it, correctly, after finalising A″).
2. The "two independently-sourced thresholds ... agree with each other"
    corroboration narrative in `count-chain.md` (~112–130) overstates what is
    actually two probes of different physical quantities converging by
    coincidence to within ~15%; with 78.6 J excluded there is only one
    admissible sourced row (126 J), not a converging pair. This is an
    evidentiary-strength loss (the argument goes from "two independent
    measurements agree" to "one measurement, unconfirmed"), not a verdict
    flip.
3. `_limitations.qmd` L1 and `challenges/README.md`'s ranges ("1.73 to 2.00",
    "1.92 to 2.23") should collapse to point values (1.73, 1.92) once 78.6 J
    is dropped, which is a presentation fix, not a substantive one.

## 5. Classification

**Blocking**, on the narrow, correctly-diagnosed claim: 78.6 J is
mischaracterized as a sourced, non-fitted wood-panel perforation threshold on
three published surfaces (`_limitations.qmd`, `challenges/README.md`,
`count-gap-1938/count-chain.md`), when its own primary source defines it as a
personnel-casualty criterion unrelated to wood. This is Blocking per
`source-data-fidelity.md`'s criterion-match gate regardless of downstream
numeric impact, and per `deferred-findings.md` it may not be closed by
deferral since it rests on a currently-published verdict.

**Not Blocking on the bottom-line PASS-arm conclusion itself** — "met or
marginal, not failed" survives on the 126 J row alone and does not need to be
walked back; it needs its supporting citation narrowed from two rows to one,
and the 78.6 J row's role demoted from "sourced threshold" to "plausibility
probe" (which derivation.md §7.3–7.4 has already done for the *replacement*
model — the outstanding work is updating the three named published surfaces
to match, which the FINDING marker's `affects:` list already scopes
correctly).

## Suggested corrections (not applied — verification pass only)

- In `_limitations.qmd` L1 and `challenges/README.md`: drop 78.6 J from the
    "sourced (non-fitted)" threshold list; report the count-arm result at 126 J
    alone (1.73× / 1.92×, both inside the 2× band), and keep 78.6 J only as a
    labeled plausibility cross-check if retained at all.
- In `count-gap-1938/count-chain.md`: relabel the 78.6 J table row's "source
    of the value" column to note it is a personnel-casualty criterion, not a
    perforation criterion, and remove or qualify the "two independently-sourced
    thresholds ... agree with each other" language accordingly.
- Cross-reference derivation.md §7.3's A″ plug-shear result ($\tau$ = 8.96 MPa,
    Sanborn 2019) as the criterion-correct replacement once Check 4 (§7.4,
    "still NOT RUN") is executed against shipped code.
