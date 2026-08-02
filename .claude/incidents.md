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
