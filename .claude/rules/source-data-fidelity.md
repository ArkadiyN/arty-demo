# Source-Data Fidelity

Applies to **every agent** (main conversation and subagents). Governs any
number transcribed from an external source into a committed artifact — a
check script, a `derivation.md`, a `card.md`, a `.qmd`, a spec.

Extraction-quality scanning (`src/utils/scan-extraction-quality.py`) is a
**glyph-level** gate: PUA characters, symbol runs, short-token ratios. It
cannot see the failure this rule exists to prevent — every digit extracted
perfectly, assigned to the wrong row, column, or table.

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
- **Declared monotonicity holds** down each column.
- **A stated total equals the sum** of its parts.
- **Independently-tabulated columns agree** where they overlap.

**A table with no closure invariant is not thereby admissible** — it is
flagged for human review in the dispatch summary. Absence of a check is a
finding, not a pass.

### Why — the incident this rule is written from

The 1944 Ordnance Dept. fragment-damage tables are two-column scans where
CASUALTIES and PERFORATION OF 1/8-IN. MILD STEEL interleave row-by-row. Three
committed check scripts (`b-vs-range-{75,105,155}mm.py`) each identified the
wrong column, and so validated a casualty-lethality model against perforation
data while feeding it the casualty energy threshold.

Every digit was extracted correctly. The tables settle their own column
identity in one line — each row lists the lightest *effective* fragment
`(m, v)`, so `½mv²` must reproduce the caption's stated criterion. It does, to
within rounding, on every row of the casualties column (57.5–58.2 ft-lb
against a stated 58 ft-lb) and nowhere in the perforation column (248–1146
ft-lb, rising with range). One arithmetic identity, applied once, would have
caught all three.

Instead the column was identified from a **summary field** — `card.md`'s
stated max range — which had itself been taken from the wrong column. The
error then propagated into 14 files. Two structural lessons, both encoded
below: a lossy summary must never be the discriminator for a fact it does not
guarantee, and a series that three scripts re-type independently gets the same
transcription error three times.

## Anchors are greppable strings, never bare line numbers

Every citation into a processed source names a **stable, unique string** that
`grep` will find — a heading, a table caption, a figure number. Line numbers
may accompany an anchor as a convenience; they may never be the only anchor.

Line numbers rot silently whenever a document is re-extracted, and a rotted
anchor does not fail loudly — it lands the reader on a *different* table that
looks like the right one. All three anchors in the incident above pointed at
the wrong shell's data by the time they were used.

## Numbers are extracted once, not re-typed

A numeric series that will be cited more than once is transcribed **one time**
into a checked-in data file next to its processed source:

```
doc-reference/<topic>/<docname>/
  card.md
  <stem>.md
  tables/
    <table-slug>.csv          ← the series, extracted once
    <table-slug>.invariant    ← the closure check it must satisfy
```

Consumers read the CSV. A check script that hand-copies a series into a
literal array is reintroducing the failure mode — three independent
transcriptions of one table produced three copies of one error precisely
because each was typed fresh.

Run the check with:

```
uv run src/utils/check-table-invariants.py <path-to-.invariant>
```

Retention of these files follows `.claude/rules/verification-scripts.md` —
a `tables/` directory is a permanent artifact, committed with the document
that cites it.

## Who checks what

Two gates, neither judgment-heavy, both mechanical:

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
