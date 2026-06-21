---
name: Subagent-Harness-Rules
description: Known Claude Code harness gotchas that affect any dispatched subagent (cwd inheritance, background execution, Bash permissions) — imported into CLAUDE.md so every subagent receives it automatically.
---

# Subagent Harness Gotchas

These are harness-level quirks, not project conventions — they apply to any
subagent dispatch (modeler, model-reviewer, librarian, general-purpose, etc.)
regardless of task. Documented once here so every subagent gets it via the
CLAUDE.md import, instead of being duplicated into each agent's `.md`.

## Always invoke Python via `uv run`, never bare `python`/`python3`

This project's `Bash` permission allow-list only covers `Bash(uv run *)` and
`Bash(uv *)` (`.claude/settings.json`). A bare `python3 -c "..."` or
`python3 <<EOF ... EOF` does **not** match either glob and requires a
permission prompt — which, per the background-execution gotcha below, often
cannot be granted and fails **silently**. When you need an ad-hoc check
(unit conversion, quick numerical sanity check, anything not worth a test
file), always run it as `uv run python3 -c "..."` or write it to a file and
run `uv run python3 <path>` — never bare `python`/`python3`/`pip`.

**The scratch file itself must land under an allow-listed `Write` path** —
`/tmp` is **not** in the allow-list (only `Write(.claude/worktrees/*)`,
`Write(src/arty/**)`, `Write(experiment/**)`, `Write(doc-reference/**)`,
`Write(openspec/**)`; `.claude/settings.json` /
`.claude/settings.local.json`). A `Write` to `/tmp/check.py` is denied exactly
like a bare `python3` Bash call, and under background-mode dispatch fails
silently with no fallback — forcing the agent into one giant inline `-c`
string instead, which is harder to debug and more likely to be denied itself
on size/quoting grounds. Use `experiment/_scratch/<name>.py` instead (under
the model folder you're already working in is fine too); delete the file when
the check is done since it isn't a real artifact.

## Known bug: subagents don't reliably inherit the worktree cwd

Per [anthropics/claude-code#36182](https://github.com/anthropics/claude-code/issues/36182),
a subagent dispatched from a session that has correctly entered a worktree
(confirmed `EnterWorktree` switch, verified cwd) can still start its own Bash
subprocess outside that worktree, forcing it to discover this and `cd` back in
on every command. This is a harness bug, not a sign that `EnterWorktree` was
used wrong — do not "fix" it by re-entering or re-checking the worktree.

**Workaround (brittle, but the only one available until the bug is fixed):**
when delegating file-touching work to any subagent while in a worktree, state
the worktree's absolute path explicitly in the dispatch prompt, and instruct
the subagent to anchor every Bash command and every Read/Edit/Write call to
that absolute path — never rely on an inherited cwd.

## Known bug: subagent foreground/background mode is undocumented and unreliable

Per [anthropics/claude-code#69691](https://github.com/anthropics/claude-code/issues/69691),
whether a dispatched subagent runs synchronously (foreground, blocking,
permission prompts pass through) or asynchronously (background, no prompt
channel) is **session-host-dependent, not controllable, and not documented**
— identical version and flags have produced different sync/async behavior
across sessions, and even within one session, otherwise-identical dispatches
to the same agent type can differ. Treat every subagent dispatch as
**potentially background**: a background subagent auto-denies any tool call
that would otherwise need a permission prompt, with no chance to approve it
— even a harmless command can get flagged (e.g. a `grep` pattern containing
backticks or `$` has been observed denied despite being correctly quoted) and
silently auto-denied instead of prompted.

**Mitigation:**

- Stick to command shapes that cleanly match an allow-listed glob (see above
  for `uv run`); avoid shell metacharacters (backticks, `$`) in `grep`/`sed`
  patterns where a plain-text alternative exists.
- Have subagents write nontrivial verification/check code to a file under an
  allow-listed `Write` path (e.g. `experiment/_scratch/check.py` — see above,
  never `/tmp`) and run it with a short, single-line command (e.g. `uv run python experiment/_scratch/check.py`) instead of inline multi-line `-c "..."`.
- Never assume a quiet subagent return means full success. A subagent that hit
  a permission denial should say so in its return summary (the harness's denial
  message is explicit) — the orchestrating agent must check returned summaries
  for denial language, not just treat "it returned" as "it succeeded."
