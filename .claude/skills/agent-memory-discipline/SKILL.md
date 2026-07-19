---
name: agent-memory-discipline
description: How to use your persistent project memory — when to read it, when to write to it, and what never belongs there. Use every time you consult or update `.claude/agent-memory/<your-name>/`.
allowed-tools: Read, Write, Edit
---

# Agent Memory Discipline

Your persistent project memory (`.claude/agent-memory/<your-name>/`, indexed
by its `MEMORY.md`) survives across sessions. It is your own curated
knowledge base — separate from the project's real artifacts (`derivation.md`,
`review.md`, `src/arty/`), which remain the system of record.

## Read every time, write rarely

Consult memory before every pass — reading is cheap, do this always. **Writing
is not routine.** Update it only when something surfaces that's worth not
re-learning — a counter-intuitive trap, a recurring pitfall, a disputed
question a source settled, a parameter bound you validated. That's the same
bar this project's own memory system uses elsewhere (a correction, a
confirmation, a new durable fact) — never "I finished a pass, so I should
write something." Most passes touch memory zero times on the write side. If
nothing surfaced that you'd otherwise re-suspect or re-derive wrongly next
time, don't write an entry just to have one.

## Record the gotcha, not the mechanism

A memory entry should be the thing that's easy to re-suspect or re-derive
wrongly (a counter-intuitive code structure, a sign-convention trap, which
source settles a disputed point) plus a pointer to where the full reasoning
already lives. It should not restate a derivation's physics or a correctness/
review verdict's reasoning at length — if that explanation doesn't already
exist in the cited artifact (`derivation.md`, `review.md`, the source), the
gap is in the artifact, not in memory, and belongs there instead. Memory that
duplicates an artifact goes stale silently, since nothing re-syncs it when
the artifact changes later.

If a finding is substantial (a scoping-level conclusion, a multi-part
analysis) but has nowhere to live yet, that's a sign the pass needed a real
artifact — say so in your return summary and let the parent decide, rather
than writing the whole analysis to memory by default.

## Never log status into memory

Don't append dated "reviewed/PASS/resolved as of \<date>," a pass/fail
history across revisions, or a test-count/coverage snapshot to an entry —
that's the task-log pattern this skill exists to prevent, just arriving one
append at a time instead of all at once. Status, history, and outcomes belong
in `review.md` / the change's own artifacts, which already exist for this.
An existing entry should be **edited** to stay current (or deleted once the
gotcha no longer applies) — never grown by appending another dated paragraph
on top.

## Hard limits (hook-enforced)

A PostToolUse hook (`.claude/hooks/check_agent_memory.py`) rejects writes
that break these. They are part of the format, not advice:

- **One fact per file, ≤ 30 lines total** including frontmatter (aim for
  ~20). If an update would push an entry over the cap, delete at least as
  much as you add — or split the file.
- **`MEMORY.md` bullets are single lines** (≤ 250 chars, no continuation
  lines): title link plus a one-phrase hook, nothing more.
- **No status paragraphs.** A line starting `**Resolved` / `**Fixed` /
  `**Confirmed` is the task-log pattern arriving one append at a time and
  is rejected outright. When a gotcha closes, rewrite the entry down to the
  ≤3-line durable pattern that remains — or delete the file and its index
  line.
- **Numbers live in artifacts.** Convergence tables, sweep results, and
  verification narratives belong in `derivation.md` / `review.md`; memory
  keeps one summary sentence plus the pointer.

## GC on read

Trimming is triggered by *reading*, not only writing: when a pass consults
an entry and finds it stale, already-resolved, or over the limits above, fix
it in that same pass — edit it down or delete it, and update `MEMORY.md`.
Memory has no other maintenance schedule; this is it.
