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
