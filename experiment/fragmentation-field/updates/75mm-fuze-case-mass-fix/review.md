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
