# Workflow Incidents

The evidence behind `.claude/rules/`. **Not loaded into context** — each rule
carries its imperative and one compressed consequence line, and links here.

Read a section when you want the numbers behind a rule, when you are about to
argue with one, or when you are writing a new rule and want the house style:
*the rule states what to do; this file states what it cost when nobody did.*

## threaded-modeler

*Behind:* `agents-routing.md` Gate 4, `subagent-harness.md` "Continuing a
subagent doesn't reset its context".

`maxTurns` bounds a **single invocation**. Continuing an agent with
`SendMessage` starts a fresh invocation with a fresh `maxTurns` budget **on the
same, never-reset conversation** — so N follow-ups grant up to N×`maxTurns`
turns piled onto one accumulating window.

Subagents *do* auto-compact — same logic and trigger as the main conversation,
and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` applies to them
([docs](https://code.claude.com/docs/en/sub-agents#auto-compaction)). But
compaction only fires near the model's window limit, which for Opus 4.8 is the
~1M tier, **not** 200k — so a threaded agent grows into the hundreds of
thousands of tokens long before compaction (a lossy last resort that can drop
mid-derivation intermediates) would ever engage. The 200k figure is a
per-request window size, not a usage cap and not Opus 4.8's limit.

**The dominant cost is window re-caching, not the reads.** Each turn re-reads
the window (cheap, 0.1×), but every resume after the ~5-min cache TTL lapses
**re-writes the entire window at 1.25×**. On the Pro plan the usage cap parks
the session for hours between turns, so these full-window re-caches are
*structural*, not avoidable by working faster — their cost is set purely by how
big the window is at resume. That is why window **size** is the only lever.

The incident: one modeler threaded across five passes grew to a **~268k**
window (74k → 125k → 175k → 268k). **~84% of its cache-write spend** was
full-window idle re-caches. Output tokens — the intrinsic work, derivation plus
review cycles — were unaffected by any of it, and would have been identical
under fresh dispatch. Re-dispatching fresh per pass caps each resume at one
pass (~40k, reloaded from the compact `derivation.md`) and roughly halves the
run. Threading also resets `maxTurns` on every message, removing the last
turn-count guard.

## column-inversion

*Behind:* `source-data-fidelity.md`.

The 1944 Ordnance Dept. fragment-damage tables are two-column scans where
CASUALTIES and PERFORATION OF 1/8-IN. MILD STEEL interleave row-by-row. Three
committed check scripts (`b-vs-range-{75,105,155}mm.py`) each identified the
wrong column, and so validated a casualty-lethality model against perforation
data while feeding it the casualty energy threshold.

**Every digit was extracted correctly.** Glyph-level extraction-quality
scanning (`src/utils/scan-extraction-quality.py`) passes a clean table of
wrong numbers — it cannot see this class of defect, and a green scan must never
be read as admissibility.

The tables settle their own column identity in one line — each row lists the
lightest *effective* fragment `(m, v)`, so `½mv²` must reproduce the caption's
stated criterion. It does, to within rounding, on every row of the casualties
column (57.5–58.2 ft-lb against a stated 58 ft-lb) and nowhere in the
perforation column (248–1146 ft-lb, rising with range). One arithmetic
identity, applied once, would have caught all three.

Instead the column was identified from a **summary field** — `card.md`'s stated
max range — which had itself been taken from the wrong column. The error then
propagated into 14 files, including shipped `src/arty/` code.

Three structural lessons, all now encoded in the rule:

1. A lossy summary must never be the discriminator for a fact it does not
    guarantee.
1. A series that three scripts re-type independently gets the same
    transcription error three times — so extract once, into a checked-in CSV.
1. All three anchors involved were bare line numbers, and by the time they were
    used they pointed at a different shell's data.

## deferred-and-forgotten

*Behind:* `deferred-findings.md`.

The column inversion above was **correctly diagnosed twice** — in
`initial-conditions-105mm.md` §(b)/(c) and `initial-conditions-155mm.md`. Both
ran the energy closure, both concluded the b-vs-range scripts had used the
wrong column, and both deferred the fix with the same phrase: *"out of scope —
flagged for a follow-up fix."* The follow-up never happened, and the wrong
numbers stayed in committed artifacts and in shipped code.

Nothing was hidden and nobody was wrong: each pass correctly judged the repair
out of its scope. The defect is purely one of *routing* — a finding recorded
only in the document that found it never reaches the pass that later edits the
affected file. That is the gap `OPEN-FINDINGS.md` closes.

A second-order instance, worth recording because it is the same shape one level
up: the first version of `collect-findings.py` matched `FINDING[...]` only in
its unescaped form. `mdformat` rewrites that to `FINDING\[...\]` in every `.md`
it touches, so on the very first commit all six seeded findings dropped out of
the register **and the staleness hook passed**. A register that can be silently
zeroed is worse than none.

## lost-check-scripts

*Behind:* `verification-scripts.md`.

Nine scripts were written, cited by permanent documents, never committed, and
are permanently lost: `mott_scale_check.py`, `mott_shape_closure.py`,
`tolch-panel-distance-check.py`, `bench.py`, the three `wdss1_*_check.py`,
`quad_check.py`, `verify_familyA_fix.py`. Their numbers now survive only as
claims — a reader cannot check them, only trust them.

The loss leaves **no trace in history**, which is what makes it insidious: a
commit that adds a verdict without the script that produced it looks exactly
like a commit that never had one. That is why retention is enforced at commit
time rather than by review.

## numpy-scalar-sweep

*Behind:* `verification-scripts.md` "Requirements on a retained script".

A Phase-4 drag-law re-check swept 551 shape factors, re-integrating a 4000-step
RK2 ODE per data point with two scalar `np.interp` calls per step — ~4×10⁸
numpy round-trips, measured at 10.8 ms per integration, **~9 minutes** total.
Vectorised, the identical script runs in **2.5 s** with byte-identical output.

The cost was not patience. The run consumed most of its dispatch's wall clock,
the pass hit `maxTurns` mid-analysis, and it returned **zero artifact bytes**
after ~78k tokens. A slow check script spends the turn budget of the dispatch
that runs it.

## fabricated-anchors

*Behind:* `source-data-fidelity.md` "Anchors are greppable strings".

The rule's stated reason for banning bare line numbers is that they **rot** on
re-extraction. Measured, that is not what happened here.

**All 20 bare line-number anchors** across the `ordnance-1944` and
`tolch-1938` cards fail to resolve to the content they claim — and they fail
**identically at each card's birth commit**, against sources whose line counts
are unchanged since (1466 and 1715 lines). The Tolch card cites 9.71 at "lines
617–627"; 9.71 has always been at line 900. Nothing rotted. They were written,
plausibly formatted, and never once checked. Verifying all twenty costs 0.3 s
(`challenges/source-data-audit/checks/card-anchor-claim-verification.py`).

So greppable strings are half the fix. Fabrication is only caught by running
the `grep` **when the anchor is written** — which is why the rule now says so
explicitly rather than leaving it implied.

Two further ways a greppable anchor still fails:

- **Line breaks.** Two of Mott & Linfoot's nine anchors failed their first
    `grep` because the quoted paragraph wrapped mid-phrase. A string straddling
    a newline is not greppable and nothing about the file looks wrong; any
    markdown re-flow can create one.
- **Table numbers that aren't headings.** `ordnance-1944.md` is a flattened
    two-up scan, so its `TABLE n` lines are page furniture rather than headings
    over the rows beneath. The nearest preceding heading implies TABLE 43/51/59
    for three shells where the page prints 38/39, 48/49, 56/57 — which is
    exactly what the card asserts, so the card was not guessing, it was reading
    a surface that lies. This also disqualifies the obvious repair: anchor on
    the shell title, not the table number.

A near-miss worth recording, from the pass that found all this. A mechanical
check run against the convenient artifact — the flattened `.md` — instead of
the source concluded the card's labels were *correct* and was one step from
retracting a registered blocking finding. Reading the retained scan pages
overturned it. The convenient surface reproduced the original defect.

## card-as-modelling-claim

*Behind:* `source-data-fidelity.md` "A card states what the source says".

`doc-reference/**/card.md` is read by @modeler as reference material and is
reviewed by nobody. A section in one that tells a reader *what to use the
source for* therefore enters every downstream brief as an unexamined premise.

Tolch-1938's "Drag Model Relevance" recommended the velocity-sweep density
collapse as **the** drag calibration anchor. The axis is the *shell's* velocity
at burst — a burst-geometry observable, and the least drag-sensitive number in
the report. The correction was found and written into modeler memory
(`gotcha_tolch_remaining_velocity_is_shell_not_fragment.md`); the card went on
saying it for years, because agent memory is not a surface anyone reviews
either.

The distribution is structural, not coincidental. Of 18 cards, 11 carry a
provenance section (all written during the source-data audit) and 7 do not —
and **every interpretive defect found in the sweep sits in those 7**. Four
sections assert what their source does not say; two of the four hedge inside
the card ("not stated in source", "presumably"), which is the right instinct
landing in a file where nobody downstream sees the hedge.

## secondhand-attribution

*Behind:* `source-data-fidelity.md` "Who checks what" — the provenance gate.

Gold 2017 attributes three claims to Mott (1943). Against the primary: one is
**contradicted**, one is **not in the paper at all**, one holds.

This defect class defeats every mechanism the rule otherwise relies on. The
citing paper's extraction is clean, its digits are correct, and its own closure
invariants pass — the error is entirely in what it says another paper says. No
glyph scan, no closure invariant, and no CSV can see it. The only detector is
reading the primary, which is cheap when it is in hand and expensive when it is
not: this one cost a scan the user happened to have.

## laundered-glyphs

*Behind:* `source-data-fidelity.md` preamble.

`scan-extraction-quality.py` flags Private Use Area glyphs (U+E000–F8FF). Gold
2017's font maps its unmapped glyphs into the **C0 control range** instead — 61
of them in the raw text layer, 0 PUA — and the scanner runs on the `.md`, which
the vision pass has already laundered to zero control characters. It reports
0/2 flagged on a document whose sign information is unreadable on both
surfaces.

The consequence is that a green scan certifies **strictly less** on a
vision-reconstructed document than on a transcribed one, and nothing in the
output says which you are holding. Gold's eq. (6) `α^(-2/3)` is settled only by
substituting eq. (2) into eq. (4) — algebra that never reads the disputed
character. That is why the rule lists substitution as a closure form.

## absent-from-a-copy

*Behind:* `source-data-fidelity.md`, "A search returning nothing is not
evidence of absence"; `librarian.md` card step.

The pattern was measured before it was named. Of the rulings an independent
verification pass examined, **every one that survived rested on an identity or
a closure, and every one it overturned rested on a search returning nothing.**
Three instances, three surfaces, all on 2026-08-03:

1. **A PDF text layer covering the tabular pages and not the prose pages.** A
    pass searched `ordnance-dept-1944`'s retained `source.pdf` for `Army`,
    `Navy`, `proving ground`, `laborator`, `retardation` and
    `angular distribution`, got **zero hits on all six**, and concluded the
    card's "Data Sources" passage "is not present anywhere in the retained
    scan" — a fabricated-content verdict on a correct committed card. The
    passage is the body of the source's own `### 5. THE SOURCES OF DATA`,
    displaced by two-up flattening. `pdftotext` pulls ~186 k characters from
    that PDF and resolves `SHELL` 149×, `FRAGMENT` 206×, `Ordnance` 22× — so
    neither a size check nor a spot-check of known-present words detects the
    gap.
1. **An extraction that dropped a sentence the page carries verbatim.** A pass
    found the Mn-hardening quote absent from
    `ammunition-series-6-steel-composition.md` (0 hits for "amount by which
    0.01", 0 for "100 to 500") and downgraded a genuine verbatim quote in the
    card to "paraphrase, not a quote". The sentence is on PDF page 11; the
    extraction renders it only as a summary bullet with an en-dash.
1. **A summarising web re-fetch.** `aisi-1335`'s first re-fetch returned a
    complete-looking property list that silently omitted
    `Hardness, Rockwell C: 15`, briefly read as a disagreement with the stored
    extraction. A second fetch asking for that value by name confirmed it is on
    the page.

Two of the three produced a **false fabrication verdict against a correct
committed artifact**, and in both the search itself was sound — only the corpus
was not. This is the cheapest check the workflow has and its least reliable, in
exactly that order.

## unequal-comparison

*Behind:* `model-reviewer.md`, "Comparison protocol".

A Mach-dependent fragment drag law was rejected because it "buys nothing" over
a constant $C_D$. It had been scored at its **derived** $k$ = 2600 — zero
fitted parameters — against a constant **fitted to the very data doing the
scoring**. Given both laws the same single scale parameter, the Mach law wins
on both columns and in both velocity bands, a consistent 20–25 % reduction in
RMS log-residual; in the lethal band the Mach law with *no* fitted parameter
(0.068) already ties the best *fitted* constant (0.069).

Two things make this worth a rule. First, the dataset it was scored on was
~44 % wrong-column, and preferentially so — all 33 perforation rows sit in the
band the verdict leaned on, against 21 of 32 casualties rows. Second, and the
actual lesson: the wrong *number* in that chain (a digitized figure understating
$C_D$) had been registered as a finding months earlier and accounts for only
~10 % of the reversal. The wrong *comparison protocol* accounted for the rest
and had no finding at all, because nothing in the review checklist was pointed
at it.

The decision survived on other grounds — both laws sit inside the ±10 %
fidelity bar, so architectural cost carries it alone — but the published reason
was void.

## capped-severity

*Behind:* `deferred-findings.md`, "The dispatcher re-tiers".

A re-baseline pass on `frag-field-3d-geometry` was briefed to stay inside the
update folder and not read `src/arty/`. It found a contradiction between the Q1
rationale and a velocity derivation, and tagged it `deferrable` — from inside
that folder it reads as two working documents disagreeing.

`src/arty/zones.py:14` names that `derivation.md` as its source, and
`zones.py:384-385` computes the velocities, shipped as v0.3.0 and rendered in
the notebook. So either the rationale is wrong or a shipped velocity is, and
which is unknown — `blocking`, and the human's call.

The restriction was correct: it is what kept the pass to nine turns. Widening
the brief would have bought the right tier at the cost of the cheapness that
made the pass worth running. Re-tiering on return costs one `grep`.
