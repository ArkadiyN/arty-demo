---
name: Deferred-Findings-Register
description: A finding you decline to fix now must be recorded with a greppable FINDING marker so it reaches the register and the next dispatch's brief — imported into CLAUDE.md so every agent receives it.
---

# Deferred Findings Must Leave the Document

Applies to **every agent**. A defect noticed while doing something else is
normally out of scope — that is fine. Recording it *only in the document you
were writing* is not: nobody reading the affected file ever sees it.

## What may not be deferred at all

**A committed artifact known to carry a wrong number — or shipped code or a
published surface resting on one — cannot be closed by an agent's deferral.**
"Out of scope" is a legitimate answer for *new work*; it is never a legitimate
answer for *existing published wrongness*. Mark it `blocking` and say so in
your return summary. Only the human decides it can wait.

## The marker

One line, anywhere in `.md` / `.qmd` / `.py`, next to what you found:

```
FINDING[blocking]: 105mm B read off the perforation column (affects: experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-105mm.py; since: 2026-08-02)
```

It must be **one line** — a wrapped marker does not parse, and the collector
fails the commit rather than silently dropping it.

`blocking` (above) · `deferrable` (real, can wait) · `note` (worth knowing) —
the same vocabulary as `review.md` tags. `affects:` is comma-separated repo
paths; those paths are what routes the finding to a future dispatch. Close a
finding by **deleting its marker** — never by editing the register.

`OPEN-FINDINGS.md` is generated from these markers and gated by pre-commit;
`uv run python src/utils/collect-findings.py --help` covers the mechanics.
Before dispatching @modeler or @model-reviewer, inject the entries matching
the pass's scope into the brief (model-workflow skill).
