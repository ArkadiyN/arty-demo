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
`/tmp` is **not** allow-listed. Use `experiment/_scratch/<name>.py`.

**Never delete a check script.** Retention, naming, and where a script lands
when the pass ends are governed by `.claude/rules/verification-scripts.md` —
`experiment/_scratch/` is a *staging* area, not a wastebasket.

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

## A pass can return `completed` having produced nothing — classify before re-dispatching

`completed` in a task-notification means the invocation **terminated
normally**, which *includes hitting `maxTurns`* — there is no separate `failed`
status for turn-exhaustion. The `<result>` field is just the agent's last
assistant text block, so a pass cut off mid-work reads as a coherent-but-
truncated thought ("Let me read those entries…"), not an error. **The only
reliable success signal is the expected artifact on disk** — check it every
time (this is "a quiet return ≠ success" made concrete).

When the artifact is missing or stub-short, do **not** reflexively re-fire a
full pass. Classify first — it is nearly free:

1. **Diagnose from the cited output file.** The notification names the output
    file; open it, or just compare `tool_uses` in the usage block to the
    agent's `maxTurns`. `tool_uses ≥ maxTurns` with mostly `Read`/`grep` and no
    `Write` = **turn-exhaustion from over-reading** (the dominant mode — the
    agent spent its whole budget discovering/reading and never reached the
    write). Denial language = a permission block (see the background-mode
    section). Neither = a genuine crash / API error.

1. **Sub-classify the exhaustion — is the dead window an asset or a
    liability?** This decides the remedy, and it is the one judgment that
    cannot be skipped.

    - **Over-read exhaustion** (the dominant mode) — mostly `Read`/`grep`,
        repeated or circling reads, no `Write`, the agent never converged on
        anything. The window is a **liability**: it is full of the wrong
        material and an anchored reading of it. **Re-dispatch fresh.**
    - **Productive exhaustion** — the agent reached real results (it ran the
        computation, it states a concrete finding) and ran out of clock before
        writing them up. Often a single long tool call ate the budget. The
        window is an **asset**: it holds exactly the discovery a fresh instance
        would have to pay for again. **Resume it once** — see the next item.

1. **On over-read exhaustion, re-dispatch fresh** (Gate 4) and fix the *cause*,
    which is what the agent was pointed at — a scope too wide to close, or
    inputs that sent it hunting through sources its own artifacts already
    record. **Write-early is not the fix to add here**: it is standing
    behaviour in `librarian.md`, `modeler.md` and `model-reviewer.md`, so a
    brief that repeats it is redundant and a brief that omits it is not why the
    pass failed. Narrow the scope instead, and hand over anything the dead pass
    already discovered (an extracted file, a computed output) so the fresh one
    does not re-pay for it.

1. **On productive exhaustion with zero artifact bytes, `SendMessage`-resume
    is the cheaper move and is permitted** — narrowly, under all four
    conditions:

    - **No artifact exists.** Fresh dispatch is only cheap because it is
        "briefed from the durable artifacts"; on a zero-byte return that
        premise is exactly what failed, so restarting pays the full discovery
        cost a second time.
    - **The window is one pass, not an accreted workflow.** ~50–80k from a
        single pass is a different object from the ~268k five-pass window Gate
        4 was written from.
    - **Resume promptly, while the prompt cache is still warm.** Gate 4's
        "the TTL always lapses" premise is about *human* turnaround between
        turns; it does not hold when the orchestrator is live and the agent
        returned minutes ago. Warm, the resend is 0.1×; that is what makes the
        arithmetic favour resume.
    - **Scope the message hard** — name the artifact to write, hand it any
        results it would otherwise recompute (an output file path), and tell it
        not to re-derive. `SendMessage` resets `maxTurns`, so the turn guard is
        gone and the instruction is the only bound left.

    **Once.** A resume that again returns zero bytes is the deterministic loop
    below — escalate, do not resume twice.

1. **Cap re-dispatches at two, and use artifact growth as the loop sensor.** A
    pass that returns with **zero artifact bytes twice** is a deterministic
    read-bound loop, not bad luck — **stop and escalate to the human** with the
    classification and token cost; do not fire a third. A partial that **grows**
    each pass is converging, so a bounded continue is fine. (This is why the
    ledger matters: a heading-only skeleton gives neither cheap resumption nor a
    progress signal; a findings ledger gives both.)

Spending a second full pass blind — no diagnosis, unknown cause — is a costly
subagent delegation under `.claude/rules/significant-decisions.md`; when the
cause is unclear, or it would be the second blind attempt, surface it rather
than burn it.

## Continuing a subagent doesn't reset its context — and defeats `maxTurns`

`maxTurns` bounds a **single invocation**. `SendMessage` starts a fresh
invocation with a fresh budget **on the same, never-reset conversation** — so N
follow-ups grant N×`maxTurns` on one accumulating window. Subagents auto-compact
only near the ~1M limit, not 200k, so a threaded agent never hits it.

**Never thread a multi-pass workflow through one instance** — re-dispatch per
pass so each resume re-caches one small pass, not the whole accreted workflow.
The cost is window **size**, re-written at 1.25× on every resume, not the cheap
per-turn reads. Binding for modelling agents as `agents-routing.md` **Gate 4**;
numbers in `.claude/incidents.md#threaded-modeler`.
