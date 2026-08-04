# Source-Data Fidelity

Applies to **every agent** (main conversation and subagents). Governs any
number transcribed from an external source into a committed artifact — a
check script, a `derivation.md`, a `card.md`, a `.qmd`, a spec.

Extraction-quality scanning (`src/utils/scan-extraction-quality.py`) is a
**glyph-level** gate: PUA characters, symbol runs, short-token ratios. It
cannot see the failure this rule exists to prevent — every digit extracted
perfectly, assigned to the wrong row, column, or table. **A green scan is not
admissibility.** It certifies strictly less on a vision-reconstructed document
than on a transcribed one, and says nothing about which you hold: it reported
0 flags on a paper whose exponent signs are unreadable on every available
surface (`.claude/incidents.md#laundered-glyphs`).

## Invariant — a source table is inadmissible until it closes

Before any number from a source table is cited, computed with, or transcribed
into a check script, the table must be shown to satisfy a **closure
invariant**: a relation internal to the table, derived from the *source's own
stated definitions*, that must hold on every row.

A closure invariant is not a plausibility judgment. It is arithmetic with a
pass/fail answer, which is what makes it cheap, delegable, and immune to the
pattern-matching that defeats eyeballing. Typical forms:

- **The source's stated criterion closes numerically.** A table whose caption
    defines a threshold, and whose rows carry the quantities entering it,
    must reproduce that threshold on every row.
- **Declared monotonicity holds** down each column — or, in a table of
    bracketed limits, within each *group*.
- **A stated total equals the sum** of its parts.
- **Independently-tabulated columns agree** where they overlap.
- **Bracketed limits tile.** Where a source prints ranges as "Over X to Y,
    incl.", consecutive brackets must share an endpoint — that is what makes
    the table total over its stated domain. A gap is a value the table does not
    cover, an overlap is two answers for one value, and either is what a row
    read one step out of position looks like.
- **A stated equation is the substitution its source says it is.** Where a
    paper derives eq. (6) by substituting eq. (2) into eq. (4), doing that
    algebra *is* the closure. Reach for this when the quantity is an equation
    rather than a table — and note it is the only form that survives a document
    whose glyphs are unreliable, because it never reads the disputed character.

The first five are mechanical enough to delegate; the last is algebra and is
not.

**A table with no closure invariant is not thereby admissible** — it is
flagged for human review in the dispatch summary. Absence of a check is a
finding, not a pass. And *"no closure I tried worked"* is not *"no closure
exists"*: one pass swept two readings of a table and reported no closure
available, where a third closed; another reported none on a table stating its
total one line above its parts.

**A failing closure localises a table; it does not condemn it.** The verdict is
per row or per group — use the rows that close, refuse the rows that do not —
which is already how the monotonic and tiling forms read. One failing row of
four is not an unsupported series.

`monotonic: <col> <dir> by <group>` and `tiling: <group> <lo> <hi>` express the
bracketed forms directly (`check-table-invariants.py --help`). A closure the
DSL cannot express goes in a check script under the document's `checks/`,
retained per `.claude/rules/verification-scripts.md` — never left unstated.

### Why

Three committed check scripts each identified the wrong column of an
interleaved two-column scan, validating a casualty model against *perforation*
data while feeding it the casualty threshold — with **every digit extracted
correctly**, so the glyph-level scan passed. The error propagated into 14
files and into shipped `src/arty/` code. One `½mv²` identity, applied once,
would have caught all three: `.claude/incidents.md#column-inversion`.

## A search returning nothing is not evidence of absence

Every gate in this rule is a **positive** check — a closure that holds, an
anchor that resolves, a digit that matches — and that is not incidental. Across
one audit, every ruling that survived independent verification rested on an
identity or a closure; **every ruling it overturned rested on a search
returning nothing.**

A null result over a **derived** surface — an extraction `.md`, a PDF text
layer, a summarising web re-fetch — bounds that surface and nothing else.

- **Report the surface, never the source.** "Not found in `<file>`" is a
    result. "The source does not say it" is a conclusion that surface cannot
    support; only the page settles absence.
- **A null result does not become a finding on its own.** Before writing that
    an artifact fabricated, invented, or misquoted something, read the page —
    the retained `source.pdf`, or the image.
- **A summarising fetch can confirm a value present and cannot establish one
    absent**, unless it was asked about that value by name.

The gap is invisible from the derived side: a layer missing your passage still
looks healthy on a character count and on known-present words. Three surfaces,
three mechanisms, one day — two of them reaching a false fabrication verdict
against a *correct* committed card: `.claude/incidents.md#absent-from-a-copy`.

## Anchors are greppable strings, never bare line numbers

Every citation into a processed source names a **stable, unique string** that
`grep` will find — a heading, a table caption, a figure number. Line numbers
may accompany an anchor as a convenience; they may never be the only anchor.

**Run the `grep` when you write the anchor**, and confirm what it returns is
what the citation claims. This is the cheap half of the rule and the half that
was never being done: all 20 bare line-number anchors in two cards fail at
their own birth commits, against sources of unchanged length — they never
pointed at their claimed content, and checking all twenty costs 0.3 s. Rot is
the failure the greppable-string rule prevents; **fabrication is the one that
actually occurred**, and only verifying at authoring catches it.

Two ways a greppable anchor still fails, both silent:

- **A string that straddles a newline is not greppable**, and nothing about
    the file looks wrong. Prefer anchors short enough to sit on one line, and
    check longer quotations against the surface as *stored*, not as rendered.
- **A `TABLE n` line is only an anchor if the extraction kept it attached to
    its own rows.** In a flattened two-up scan it is page furniture. Confirm
    the heading governs the data beneath it, or anchor on the section title
    instead.

Evidence for all three: `.claude/incidents.md#fabricated-anchors`.

## Numbers are extracted once, not re-typed

A numeric series that will be cited more than once is transcribed **one time**
into a checked-in data file next to its processed source:

```
doc-reference/<topic>/<docname>/
  card.md
  source.pdf                  ← the blob that was processed, kept (gitignored)
  <stem>.md
  tables/
    <table-slug>.csv          ← the series, extracted once
    <table-slug>.invariant    ← the closure check it must satisfy
```

Consumers read the CSV. A check script that hand-copies a series into a
literal array is reintroducing the failure mode — three independent
transcriptions of one table produced three copies of one error precisely
because each was typed fresh.

**Keep `source.pdf`.** It is gitignored (`doc-reference/**/*.pdf`), so it costs
the repo nothing, and it is what makes "go back to the page" possible at all —
without it a table that fails its closure can only be re-argued, not re-read.
Cite scanned tables by **PDF page and printed page** alongside the greppable
anchor: a processed `.md` can be re-extracted and shift, the PDF's pagination
cannot.

**`<stem>.md` is not reliably an extraction.** Its filename and location imply
it is the processed source; one such file opened with a header calling itself a
"transcribed excerpt" while containing estimated yield strengths and design
rationale found nowhere on the page. Confirm any `doc-reference/` markdown says
what it is before treating it as the source.

Run the check with:

```
uv run src/utils/check-table-invariants.py <path-to-.invariant>
```

Retention of these files follows `.claude/rules/verification-scripts.md` —
a `tables/` directory is a permanent artifact, committed with the document
that cites it.

## A card states what the source says, not what to use it for

`card.md` is a **reference document**, read by @modeler as a premise and
reviewed by nobody. A section telling a reader what a source is *good for* —
which calibration to anchor on it, which of its curves to prefer — is a
modelling claim wearing a reference doc's clothes. It belongs in
`derivation.md`, where @model-reviewer sees it.

Where a card must characterise its source, the safe shape ends in a
**referral**, not a recommendation: state the transfer question, name it as a
criterion-match question, and route it. Hedging inside a card ("presumably",
"not stated in source") is the right instinct in the wrong file — the hedge is
visible to whoever reads the card and invisible to whoever reads the artifact
citing it.

The mechanical half of a card — every table, verbatim caption, greppable
anchor, all columns with units, row count, CSV link, provenance — carries no
such risk and is safe for a cheap model to write.

Cost of getting this wrong: a card recommended, as *the* drag calibration
anchor, the one axis in its report that is near-insensitive to drag, and said
so for years with the correction stranded in agent memory. Every interpretive
defect found in a sweep of 18 cards sat in the 7 that lack a provenance
section: `.claude/incidents.md#card-as-modelling-claim`.

## Who checks what

Three gates, none judgment-heavy, all mechanical:

- **Transcription fidelity** — *is this faithful to the page?* Owned by
    @librarian, discharged by the closure invariant above. Verifying a stated
    invariant against a table is mechanical comparison and may be delegated to
    a cheap model; **deciding** what the invariant is, or repairing a table
    that fails one, may not.
- **Criterion match** — *does the cited data measure the same quantity the
    model computes?* Owned by @model-reviewer, as part of its existing
    literature-agreement mandate. A model computing one criterion validated
    against a table tabulating a different one is a Blocking finding, however
    faithful the transcription.
- **Provenance** — *does the primary say what it is cited as saying?* Also
    @model-reviewer. A claim attributed to a primary is checked against that
    primary, or **marked secondhand** in the citing artifact. Nothing else in
    this rule can catch it: the citing paper's extraction is clean, its digits
    are right, its own closures pass, and the error is entirely in what it says
    another paper says. One source checked this way was contradicted by its
    primary on one claim of three and unsupported on another
    (`.claude/incidents.md#secondhand-attribution`).

### Finding a source's consumers: grep titles, not just slugs

Any sweep asking "which sources reach shipped code" must grep **document titles
and table numbers** as well as directory slugs. A carefully written citation
names the document in prose — *Ammunition Series 6* Table 6-1 — so a slug-only
grep systematically under-tiers exactly the citations written most carefully.
That miss left a Tier-1 source sitting in Tier 2 through most of an audit.

### Triage on "no card", not on "no CSV"

A sweep for un-re-baselined sources keys naturally on a missing
`tables/*.csv`. Both documents found feeding a shipped constant turned out to
have **no `card.md` at all** — a raw extraction and nothing else — so each
scored as an ordinary gap rather than as the worst case in the set. Sweep first
for *cited by shipped code and carrying no card*: it is the smallest set, the
highest-exposure one, and not a subset of the missing-CSV one.
