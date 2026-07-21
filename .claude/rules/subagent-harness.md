---
name: Subagent-Harness-Rules
description: Known Claude Code harness gotchas that affect any dispatched subagent (cwd inheritance, background execution, Bash permissions) — imported into CLAUDE.md so every subagent receives it automatically.
---

# Subagent Harness Gotchas

Harness-level quirks, not project conventions — they apply to any subagent
dispatch (modeler, model-reviewer, librarian, general-purpose, …).

## Python via `uv run`, never bare `python`/`python3`/`pip`

Only `Bash(uv run *)` / `Bash(uv *)` are allow-listed; anything else needs a
permission prompt, which a background subagent cannot receive — the call is
auto-denied **silently**. Ad-hoc checks: `uv run python3 -c "..."`, or a
scratch file. The scratch file must land under an allow-listed Write path —
`/tmp` is **not** allow-listed. Use `experiment/_scratch/<name>.py` (or under
the model folder you're working in); delete it when the check is done.

## Known bug: subagents don't reliably inherit the worktree cwd

([anthropics/claude-code#36182](https://github.com/anthropics/claude-code/issues/36182))
A subagent dispatched from a worktree session can still start outside the
worktree. This is a harness bug — do not "fix" it by re-entering or
re-checking the worktree. **Workaround:** when delegating file-touching work
from a worktree, state the worktree's absolute path in the dispatch prompt and
instruct the subagent to anchor every Bash command and every Read/Edit/Write
call to that absolute path — never rely on an inherited cwd.

## Known bug: foreground/background subagent mode is unreliable

([anthropics/claude-code#69691](https://github.com/anthropics/claude-code/issues/69691))
Whether a dispatch runs foreground (permission prompts pass through) or
background (prompts auto-denied, silently) is session-host-dependent and not
controllable. Treat **every** dispatch as potentially background:

- Stick to command shapes that cleanly match an allow-listed glob; avoid
  backticks and `$` in `grep`/`sed` patterns where plain text works — such
  patterns have been observed auto-denied even when correctly quoted.
- Write nontrivial check code to `experiment/_scratch/check.py` and run it
  with a short single-line `uv run python experiment/_scratch/check.py` —
  not a multi-line inline `-c "..."`.
- A quiet return ≠ success: the orchestrating agent must check returned
  summaries for permission-denial language, not just treat "it returned" as
  "it succeeded."

## Continuing a subagent doesn't reset its context — and defeats `maxTurns`

`maxTurns` bounds a **single invocation**. Continuing an agent with
`SendMessage` starts a fresh invocation with a fresh `maxTurns` budget **on the
same, never-reset conversation** — so N follow-ups grant up to N×`maxTurns`
turns piled onto one accumulating window, and every turn re-sends the whole
window (cache-read burn that grows with each pass).

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
unavoidable — their cost is set purely by how big the window is at resume. In
one incident ~84% of the cache-write spend was full-window idle re-caches of a
window that grew to ~268k; output (intrinsic work) was untouched by any of it.

**Consequence for orchestration:** never thread a multi-pass workflow through
one instance — re-dispatch a fresh agent per pass so each resume re-caches one
small pass, not the whole accreted workflow. For modelling agents this is
binding as `.claude/rules/agents-routing.md` **Gate 4**.
