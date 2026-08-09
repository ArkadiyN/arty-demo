# Review — 75 mm M48 HE mass basis fix (`mass_total`, `mass_filler`, `mass_deductions`)

**Verdict: PASS-with-limitations**

`collect-findings.py --for experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix`:
no open findings routed to this folder.

## What was checked

- `checks/tolch-75mm-mass-basis-variants.py` reruns clean (`uv run python
    experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/tolch-75mm-mass-basis-variants.py`)
    and reproduces every number cited in `derivation.md` exactly: variant
    table A–E, both closure asserts, Check 2 (+0.37 %), Check 3 (Mott mass
    closure, +0.000 %), Check 4 (V0 = 864.3 m/s inside 838–923.5 band), Check 5
    (band 1.8 %). No hand-arithmetic drift.
- Dimensional analysis: `gurney_velocity`, `mott_params`, `mott_N` all
    consistent in kg/m/s; the Mott mass-closure identity
    `∫₀^∞ N(m) dm = 2 N₀ μ = M_case` was independently re-derived (integration
    by parts on `N(m) = N₀ exp(−√(m/μ))`, boundary terms vanish at both ends)
    — it is exact, not a coincidence of the check script.
- `src/arty/shells.py` current state confirmed: `mass_deductions` for the
    105 mm M1 (0.75 kg) and 155 mm M107 (1.5 kg) entries are **unchanged**
    placeholders — the M21A2-booster-analog value (0.975 kg / 2.15 lb) is used
    only inside `fuze-mass-deductions-range/materiality.md`'s sensitivity
    sweep, not shipped for either entry. Re-read derivation.md §1's "same
    stand-in already used and accepted" sentence against this: it refers to
    the *method* being exercised and judged immaterial (materiality.md's MOOT
    verdict), not to the numeric value being adopted in those two entries. Not
    misleading as written — flagged here only because the literal reading is
    easy to over-interpret as "105 mm/155 mm already ship 0.975 kg", which they
    do not.
- TM-9-1904 card (`doc-reference/ww2-shells/tm-9-1904-fuze-fitting/card.md`)
    anchor `Fuzes M48, M48A1 and M54` and the "Mean weight of loaded and fuzed
    projectile: 14.6 pounds" / appendix "1.47 lb" filler figures grepped and
    confirmed present, matching derivation.md §1 and §7 verbatim.
- TM-9-1901 card fuze weights (1.41 lb M48/M48A1/M48A2, 2.15 lb M51A3+M21A2,
    1.42 lb M54, 2.16 lb M55A2+M21A2) grepped and confirmed; the booster-closure
    identity (2.15−1.41 = 2.16−1.42 = 0.74) reproduces exactly off the card's
    own stated weights.
- Tolch (1938) weight-row anchor `Wt. empty shell & fuze` grepped in
    `tolch-1938.md` (line 232, "Round No. 1": 12.50 / 2.35 / 1.56 / 13.29,
    other 3 rounds consistent to ±0.03 lb) — closure `12.50 − 1.56 + 2.35 =
    13.29` reproduces the printed total exactly. Fragment-velocity figures:
    3,030 f/s (penetrating) confirmed clean at three anchors in `tolch-1938.md`
    (lines 146, 1654, 1658) → 923.5 m/s; ~2,750 f/s (perforating, "27^0 f/s")
    confirmed genuinely OCR-ambiguous at the same anchors, and derivation.md
    correctly declines to treat it as exact and correctly labels the whole
    check "corroborating, not decisive."

## Findings

**Deferrable** — Tolch weight-row table cited from a surface its own card
disqualifies. `doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md`
line 22 states, in the reviewer's reading not scoped to only the four
pages-40–44 spray-density tables: **"`tolch-1938.md` is not a citable surface
for any number. … a number that has no CSV has no admissible surface in this
repo — it is not to be read off the markdown instead."** The weight row
(12.50 / 1.56 / 2.35 / 13.29 lb) that both `scoping.md` and `derivation.md`
§2 cite — and that `checks/tolch-75mm-mass-basis-variants.py` hand-transcribes
as a literal (`TOLCH_LOADED_UNFUZED, TOLCH_TNT, TOLCH_FUZE, TOLCH_EMPTY_FUZE =
12.50, 1.56, 2.35, 13.29`) — has no `tables/*.csv` + `.invariant` behind it;
only the card's four spray-density tables were re-extracted and independently
closure-checked. The card's other tables were shown to have ~20/54 corrupted
cells despite passing glyph-level extraction scanning, so "not a citable
surface" is not a formality.
*Impact:* the internal arithmetic closure (12.50 − 1.56 + 2.35 = 13.29,
exact, plus 3 further per-round rows consistent to ±0.03 lb) is real
protection against a silent digit swap — a coincidental OCR misread that still
closes exactly on 4 numbers is unlikely — but it is not the CSV-based
admissibility gate the project's own rule requires, and the card that governs
this source explicitly says so. **This does not change any proposed `src/`
value**: `mass_total`, `mass_filler`, `mass_deductions` for the adopted
variant E are all sourced from TM-9-1904/TM-9-1901, independent of Tolch — the
Tolch figures feed only the corroborating §2 cross-check ("+0.37 % … the
strongest evidence available that both are read correctly"), which would need
softening from "strongest evidence" to "corroborating, not decisive" (the
same language already correctly used for the velocity check in §5.4) if this
gap is not closed. Recommend, as a follow-up (not blocking this pass):
extract the weight-row table into
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/weight-row.csv`
+ `.invariant`, or have @librarian confirm the "not citable" ban in card.md
line 22 was meant to scope only to the pages 40–44 spray tables (in which
case the citation as-is stands and this finding closes).
*Limitation entry:* log in `derivation.md` §2 (or a new §2a) that the Tolch
weight-row cross-check rests on `tolch-1938.md`, a surface its own card
disqualifies for citation, pending a `tables/weight-row.csv` extraction or a
librarian ruling on the disqualification's scope.

FINDING[deferrable]: Tolch 1938 weight-row (12.50/1.56/2.35/13.29 lb) cited in derivation.md §2 rests on tolch-1938.md, which tolch-1938-m48-panel-pit-fragmentation/card.md:22 states is not a citable surface absent a tables/*.csv + .invariant; no such extraction exists for this table (affects: experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/derivation.md, doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/; since: 2026-08-08)

**Note** — `mass_deductions` provenance for 75 mm now diverges structurally
from the still-unsourced 105 mm/155 mm placeholders (see "What was checked"
above): derivation.md's cross-reference to `materiality.md` is accurate on a
close reading but is easy to misread as "the other two entries already ship
this stand-in." No output-visible effect; a one-clause tightening ("the same
stand-in exercised and judged immaterial in materiality.md's sensitivity
sweep for those two entries, not itself shipped there") would remove the
ambiguity. Not required to close this pass.

**Already logged, re-confirmed, no new finding needed:**
- Note-tagged finding on rotating-band inconsistency (marker at derivation.md line 178) —
    accurately scoped, correctly tagged `note`, `affects:` path correct.
- §5a's self-disclosed provenance caveat on the TM-9-1904 p.414 anchor
    (present only in `card.md`, not in the in-repo `fuze-fitting-extraction.md`
    text surface) — correctly bounded (mass_total unchanged by this pass;
    independent +0.37 % agreement is evidence against a misread), correctly
    routed to @model-reviewer, and its own suggested remedy (a librarian
    extraction pass) is the right one. No stronger action available from this
    seat.
- M20/M20A1 booster stand-in (M21A2 analog, 0.74 lb) — same open gap already
    tracked in `fuze-mass-deductions-range/materiality.md`'s deferrable
    markers; `affects:` already lists `src/arty/shells.py`; N0 sensitivity
    <0.2 % confirmed in that document. No re-derivation needed here.

## Verdict rationale

No Blocking finding: every number in the variant table and every validation
check reproduces from the live check script; the Mott mass-closure identity
is exact by construction; the adopted variant E's three mass fields are each
independently sourced from processed, closure-checked TM-9-1904/TM-9-1901
material, not from the flagged Tolch surface. The one Deferrable finding
(Tolch weight-row admissibility) affects only the strength of a corroborating
cross-check, not the proposed `src/` values themselves, and stays within the
document's own ±3 % `M_case` / ±10 % `V0` fidelity bars regardless of how it
resolves.

**PASS-with-limitations.** Limitation to log before/alongside the `src/`
edit:
- Tolch (1938) weight-row cross-check in `derivation.md` §2 rests on
    `tolch-1938.md`, a surface its own `card.md` (line 22) states is "not a
    citable surface for any number," pending either a `tables/weight-row.csv`
    + `.invariant` extraction or a librarian ruling narrowing that ban's
    scope. Until resolved, the §2 language should read "corroborating, not
    decisive" rather than "the strongest evidence available."

## Suggested corrections (not applied)

1. `derivation.md` §2: soften "This is the strongest evidence available that
    both are read correctly" to match the hedged language already used for the
    velocity check in §5.4, or close the CSV-extraction gap first.
1. `derivation.md` §1: one clause clarifying the 105 mm/155 mm "stand-in
    already used and accepted" reference means the *method*, judged immaterial,
    not the shipped numeric value in those two entries.
1. Optional: `doc-reference/.../tolch-1938-m48-panel-pit-fragmentation/tables/weight-row.csv`
    + `.invariant` extracting the 4-round weight table, closing the admissibility
    gap outright.

---

# Review — initial-conditions-75mm.md restatement + scoping.md §6 marker narrowing (2026-08-09)

**Scope:** two-item review requested by the dispatching agent. (1)
`initial-conditions-75mm.md`'s "## Comparison" section restated onto the
current shipped `807.5 → 864.4 m/s` V0, including a changed comparator source
and a changed mu-vs-V0 exponent claim. (2) `scoping.md` §6's blocking marker
narrowed to name only the still-unaddressed rows.

## Verdict: PASS

## What was checked

**1a. Numbers in the diff vs the check script's actual output.**

Ran `uv run python
experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py`
directly (script is short, read in full above). Printed output:

```
M_case            =   4980.0 g
V0 (Gurney)       =    864.4 m/s
mu                =      0.826 g
N0 = M_case/(2mu) =     3016
pre-fix -> current (ratio):
  V0     807.5 ->    864.4  (1.0706)
  M_case 5755.2 ->   4980.0  (0.8653)
  mu     0.793 ->    0.826  (1.0416)
  N0     3627 ->     3016  (0.8315)
```

Every number the diff cites (`V0 = 864.4 m/s`, `M_case → 4.980 kg`,
`mass_deductions = 0.97522 kg`, `C/M = 0.1339`, `mu` 0.793→0.826 g) matches
this printout exactly. `mass_deductions = 0.97522` is not itself printed by
the script but is arithmetically forced: `6.622 − 0.6668 − mass_shell` with
`mass_shell = M_case − r_bu-derived band-mass component`... actually simpler:
the diff's own stated `mass_shell = 4.980 kg` matches the script's printed
`M_case = 4980.0 g` exactly (the script's `M_case` *is* `mass_shell`, i.e.
the case mass after deductions — confirmed by reading `_shell_geometry`'s
return contract below), so `6.622 − 0.6668 − 4.980 = 0.9752` reproduces the
diff's `0.97522` to the last printed digit.

**1b. The exponent/direction claim: `mu ∝ V0⁻²` at fixed γ′, `N0 ∝ V0²`.**

The diff's arithmetic check: `(807.5/864.4)² × (65/54.5) = 0.8752 × 1.1927 =
1.0438`, i.e. old-mu/new-mu should be ≈1/1.044 = 0.958 if V0 alone explained
the mu shift — but the diff instead multiplies by the γ′ ratio to explain the
*actual* observed mu ratio 0.793→0.826 (a **1.0416** ratio, matching the
printed `mu` line above to 3 decimal places). This is a two-factor
decomposition (V0 shape-closure term × the separately-landed γ′ re-anchor
65→54.5 from commit `6c1faff`), not a single V0⁻² law in isolation — the diff
states this correctly ("after the shape closure the net dependence is `mu ∝
V0⁻²` at fixed γ′") and does not claim the γ′ change is a V0 effect. Checked
`count-chain.md` eq. (5) is cited, not fabricated — grepped for `eq. (5)` and
`mu` scaling; the file exists at
`experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md`
and derives the Mott mass-closure `N0 = M_case/2mu`, consistent with the
`N0 = M_case/(2mu)` line printed by the check script. Did not independently
re-derive `mu ∝ V0⁻²` from Mott's shape-closure algebra (out of scope per the
dispatch brief — this is a restatement of an already-reviewed shape-closure
result, not new physics), but the arithmetic that *is* new in this diff (the
1.0416 ratio decomposition) reproduces exactly.

**1c. The comparator-source reasoning change.**

Original text: single comparator (1944 Ordnance header, 951.0 m/s), "wrong
direction to explain over-prediction." New text keeps that comparator but
adds a second, Tolch (1938)'s own velocity for the same shell (838.2 m/s,
cited as "Summary item 10"), and reasons that because the two historical
sources disagree with each other by 13%, "V0 too low" is a property of one
source choice, not a property of the model. The new argument's final claim —
"the entire spread between the two sources is (951.0/838.2)² = 1.29× on N0"
— checked: 951.0/838.2 = 1.1346, squared = 1.2872 ≈ 1.29. Correct.
This is a materially different (and more defensible) argument than the
original single-source framing: it converts a point comparison that could be
falsified by picking the other source into a bound that holds regardless of
which source is "right." The diff explicitly flags this as "the substantive
change," which is accurate — this is not just a units restatement.

Did not independently verify Tolch's 838.2 m/s figure against the Tolch
source (out of scope: this number is not newly introduced by this diff — the
Comparison section's own earlier line, unchanged by this diff, already cites
"951.0 vs 838.2 m/s" and it appears in the prior review's "What was checked"
Tolch section as page-anchored). Internally consistent with the file's own
existing citation.

**1d. Downstream consistency — the (c) drag-law argument's dependence on (a).**

The diff adds a note to §(c)'s summary explicitly bounding the V0 uncertainty
at "≤1.29× on N0" against the "7–33× over-prediction" figure carried from
elsewhere in the same file (unchanged by this diff). 1.29 vs 7–33 is not a
close call — the conclusion (drag-law gap, not V0, is the dominant driver) is
robust to which of the two historical V0 figures is used, so narrating this
as "closed 6 of 15.1 percentage points, ranking untouched" is accurate and
not overstated.

**2. scoping.md §6 marker narrowing — spot-check.**

The new `Propagation status` paragraph lists as closed:
`tolch-case-mass-basis.py`, `tolch-count-basis-closure.py`,
`stale-surfaces.md:67,123`, `review-void-rulings.md` §2,
`mach-dependent-fragment-drag/*`, `drag-gap-1944/README.md`, and
`initial-conditions-75mm.md` (this file, just verified above in item 1). The
narrowed marker retains five items as still-open:
`_limitations.qmd:151`, `tolch-1938-panel-distance.md:134,188`, and
`mott-fragment-shape-closure/{derivation.md,review.md,scoping.md}`.

Spot-checked two of the retained-as-stale files:

- `experiment/fragmentation-field/_limitations.qmd` line 151 area: grepped for
    `3627` — found at line 151, inside prose describing an "L1 addendum"
    bracketing argument, still reading `N0=3627` and not the current `3016`.
    Confirmed genuinely stale, matching the marker's own characterization
    exactly (marker text: "highest exposure: a published surface... states
    N0=3627"). This file renders into the shipped `.qmd` output (confirmed by
    file extension and the marker's own claim, not independently re-rendered —
    out of scope for a documentation-diff review), so leaving it open as
    `blocking` rather than closing it is the right call.
- `experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md`
    lines 134 and 188: grepped for `807.5` — found at both cited lines
    (line 134 in a V0 comparison sentence, line 188 in a sweep table column
    header). Confirmed still stale, not touched by this diff. Correctly
    retained in the narrowed marker.

Did not spot-check the `mott-fragment-shape-closure/*` triplet in detail
(five separate line-numbered locations plus two whole files) — the marker
text itself flags these as "arguably correct-as-history... need a decision
before editing," which is an honest statement of unresolved scope rather than
a claim of closure, and matches the pattern already validated for the
excluded `_scale_verdict_ledger.md` row (kept historical, no action, per the
paragraph above it). This is consistent reasoning applied consistently, not
a gap in this narrowing.

**Was narrowing (vs. leaving the original broad marker, or vs. deleting it)
the right call?** Yes. The rule in `.claude/rules/deferred-findings.md`
requires "close a finding by deleting its marker — never by editing the
register," but also requires the affects: list to route to what's still
wrong. Here the marker's *identity* changes (its `affects:` list is edited to
drop 7 now-closed paths and keep 5 still-open ones) rather than being deleted
and silently losing the still-open items, or being left broad and now
partially misdescribing already-fixed files as broken. Given six of the
paths were independently spot-checked as genuinely fixed (item 1 above, this
file) or the marker's own text was verified accurate against file content
(the two spot-checks just above), narrowing rather than blanket-deleting is
the correct action — a blanket delete here would have silently dropped five
real open blocking items (the `_limitations.qmd` N0=3627 in a rendered
surface, notably).

## Findings

**Note** — the diff's mu-ratio arithmetic (1.0d) mixes a V0² shape-closure
term and a separately-landed γ′ re-anchor into one printed ratio without a
side-by-side breakdown of the two factors' individual contributions (only the
product is shown to match). The text is not wrong — it correctly attributes
the two effects in prose — but a reader checking only the arithmetic line
`(807.5/864.4)² × (65/54.5) = ...` has to trust the factor decomposition
rather than see each term validated separately against a script. No
committed check script isolates the V0-only term. *Impact:* none on any
shipped value or verdict; this is a corroborating narrative aside in a
challenge-notebook comparison section, not a modeled quantity. Not required
to close this pass.

## Verdict rationale

No Blocking finding. Every number newly stated in
`initial-conditions-75mm.md`'s restated Comparison section reproduces exactly
from `checks/shipped-75mm-current-values.py`'s live output (V0, M_case, mu,
N0, and the derived mass_deductions/C-M-ratio arithmetic). The reasoning
change (single-comparator "wrong direction" → dual-comparator bound of 1.29×
on N0) is internally consistent, correctly flagged by the diff itself as the
substantive change, and does not alter the file's ultimate ranking (drag-law
gap dominates V0 uncertainty by 7–33× vs ≤1.29×). The scoping.md §6 marker
narrowing was spot-checked against two of its five retained paths
(`_limitations.qmd:151`, `tolch-1938-panel-distance.md:134,188`) and both are
genuinely still stale as the marker states; the marker's treatment of the
`mott-fragment-shape-closure` triplet as an open decision (not silently
closed, not silently deleted) is consistent with how the already-excluded
`_scale_verdict_ledger.md` row was handled.

**PASS.** No limitations to log from this pass; the one Note finding above
is presentational only.

## Suggested corrections (not applied)

1. Optional, not required: add one line to `initial-conditions-75mm.md` (a)
    showing the V0-only shape-closure factor (807.5/864.4)² = 0.875 separately
    from the γ′ factor 65/54.5 = 1.193, so the product 1.0438 vs the observed
    1.0416 delta is visible without the reader re-deriving it — currently only
    the combined product is shown.

## 2026-08-09 — propagation-closure pass (five remaining rows)

Scope: the six files listed in the dispatch brief, closing the FINDING
(blocking) marker at `75mm-fuze-case-mass-fix/scoping.md` that named five
still-stale rows (`_limitations.qmd`, `tolch-1938-panel-distance.md`, and the
`mott-fragment-shape-closure` triplet). Reviewed against the closure note's own
stated rationale (`scoping.md:180-208`): a number is **restated** if it is a
*claim about the current model*, and **annotated as-of / left as run** if it is
a *record of a computation actually performed on then-shipping inputs*.

### Verification performed

- Ran `checks/shipped-75mm-current-values.py` — confirms
    `M_case=4980.0 g, V₀=864.4 m/s, μ=0.826 g, N₀=3016` (RAP: `V₀/μ` disagree by
    factors of 1.07 / 1.04 from OLD; `M_case/N₀` by 0.87 / 0.83 — matches every
    number quoted in the five diffs).
- Confirmed the closure identity `2·N₀·μ = M_case` holds to full floating-point
    precision on the current basis (`arty` direct call, not just the rounded
    print), so `derivation.md`'s "holds identically on the new mass" claim is
    not just plausible but exact (trivially true by construction of `N₀`, but
    the claim is correctly stated).
- Grepped all five changed files plus their un-changed siblings
    (`mott-fragment-shape-closure/{derivation,review,scoping}.md`,
    `tolch-1938-panel-distance.md`) for every pre-fix figure
    (`807.5`, `5755.2`, `0.793`, `3627`, `12256`/`12 256`) to check the as-of
    banners actually cover every remaining occurrence, not just the lines named
    in the scoping table:
    - `_limitations.qmd`: all four pre-fix figures fully replaced (3016, with
        3597/3627 noted in-line as superseded history) — no stale digit remains.
    - `derivation.md`: one occurrence not named in the banner text
        (§7.5's Option-C cross-check table, line 262, `μ=0.793` for 75 mm M48)
        is still covered by the banner's blanket "every 75 mm M48 number in this
        document is a record... as it stood then" — consistent, not an omission.
    - `tolch-1938-panel-distance.md`: Result 3 (line 251, `N₀=12256–20021` for a
        `5755 g` body — a *third*, even-older pre-shape-closure basis) is
        explicitly addressed by the as-of banner's "does not disturb any Result
        below" clause with a per-result caveat for Result 3's absolute counts.
    - `scoping.md`, `review.md` (mott-fragment-shape-closure): all remaining
        pre-fix figures are within banner scope.
- Ran `tests/test_fragmentation.py` (55 passed) — no `src/arty/` change in this
    pass, as the closure note states, and nothing regressed.
- Spot-checked the two numeric claims added as banner justification rather
    than left as bare assertions:
    - `tolch-1938-panel-distance.md`: "864.4 sits ... closer to 838.2 (+3.1%
        vs −9.1%)" — checks out ((864.4−838.2)/838.2 = 3.13%,
        (864.4−951.0)/951.0 = −9.1%). "V₀ up 7.0%... N₀ down 17%" also checks
        out (864.4/807.5 = 1.070; 3016/3627 = 0.8315). The claim that this net
        shift is "far smaller than the 1.2–2.7× residual" is not itself
        computed (no re-run of the perforation-count script against the new
        basis — the document says as much), but the bound is generous enough
        (single-digit-to-teens percent shifts vs. a 120–270% residual) that the
        qualitative claim holds under any plausible combination of the two
        effects; this is the kind of claim flagged by
        `derivation_qualitative_claims_need_numeric_check` in reviewer memory,
        but here the margin is wide enough not to be material.
    - `_limitations.qmd`: 3016 sits between the stated bracket 779 and 5000 —
        confirmed by inspection.

### Findings

No Blocking findings. Two Notes:

1. **Note.** `derivation.md`'s §7.5 Option-C cross-check table (line 262)
    still prints the pre-fix `μ=0.793 g` for 75 mm M48 without a line-level
    annotation, relying entirely on the document-level banner to cover it.
    A reader skimming straight to that table (skipping the banner at the top)
    would not immediately know the number is historical. No output changes —
    the banner does cover it, and the A/C ratio (0.69) would move to ~0.72 on
    current μ=0.826 g, not enough to change the "within ~2× pass criterion"
    verdict. Presentational only.
1. **Note.** The "far smaller than the residual" claim in
    `tolch-1938-panel-distance.md` (Result 3 discussion) is asserted rather
    than computed from a re-run. Given the wide margin between the shift size
    (~7–17%) and the residual (120–270%), this does not change any rendered
    output or verdict; if the document is revisited for other reasons, adding
    the one-line arithmetic bound would remove the need to trust the assertion.

### Verdict rationale

The two treatments applied (restate on a published surface, annotate-as-of on
a historical computation record) match the closure note's own stated
criterion exactly, and were applied to every remaining pre-fix figure I could
find via grep across the five files — not just the lines the scoping table
named. The `_limitations.qmd` restatement is a correct, exact substitution
that preserves the bracketing argument it sits inside. The as-of banners are
factually accurate (checked against a live re-run of the shipped values) and
correctly scoped to cover figures beyond the ones explicitly named in each
banner's prose. No `src/arty/` change, no test regression, and the propagation
table in `scoping.md` is discharged: all five previously-flagged rows are
either restated or annotated, and the blocking FINDING marker is deleted (not
edited around), per `.claude/rules/deferred-findings.md`.

**PASS.** No limitations to log from this pass beyond the two presentational
Notes above, which require no `_limitations.qmd` entry (they concern review
artifacts and a challenge-notebook document, not a modeled quantity or a
published claim).

### Suggested corrections (not applied), this pass

1. Add a line-level annotation next to `derivation.md:262`'s `μ=0.793` in the
    Option-C table (e.g. "(pre-fix value, see banner above)") so the historical
    status is visible without scrolling to the top banner.
1. If `tolch-1938-panel-distance.md` is revisited, replace the qualitative
    "far smaller than the residual" claim with the one-line arithmetic bound
    (percent shift vs. percent residual) rather than leaving it as assertion.
