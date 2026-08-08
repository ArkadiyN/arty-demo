## Agent Routing Gates

Physics modelling follows two named workflows — **A (assessment)** and **B
(update)**. The full choreography — workflow steps, aspect decomposition,
artifact layout, task sequencing, briefing rules, documentation surfaces —
lives in the **model-workflow** skill. **Load that skill (Skill tool) before
delegating any pass to @modeler or @model-reviewer.**

The three gates below bind the **main agent**, always — at every entry point
(direct request, new chart, or an OpenSpec step via the `openspec-propose` /
`openspec-apply-change` skills). They constrain the agent, not a tool, so they hold even when a skill or
task says "implement" — no tool's instructions override them.

## Gate 1 — Worktree precondition

**Invariant:** never dispatch @modeler or @model-reviewer without having
entered a worktree this session (`EnterWorktree` called, not exited) — even
for a question with no expected file output. Both agents carry
`memory: project`, which auto-grants writes to their git-tracked memory
directory (`.claude/agent-memory/<agent>/`) on **every** pass, so a
read-only-looking dispatch can still write to whatever checkout you sit in.

## Gate 2 — New math

**Invariant:** the main agent never authors or inlines a physical or derived
quantity. All such math lives in `src/arty/` and is produced by @modeler.

**Trigger (litmus):** the work needs a physical or derived quantity that an
`src/arty/` function does not already return. *Mentioning the model is not the
trigger — reuse is fine; computing a new number is.* Aggregations, unit
conversions, ratios, calibrations and "quick transforms" count as new math
when they encode a physical quantity.

**On trigger — stop and hand off:**

- Unclear whether new math is needed → delegate a **chart / new-math triage**
    to @modeler (describe the quantities and axes; ask the single yes/no).
- *No new math* → proceed by importing and calling `arty`; only layout and
    styling live in `app/` or the `.qmd`.
- *New math needed* → run **Workflow B** (model-workflow skill) first, then
    wire it up. The main agent never writes the math.
- **Inside an OpenSpec change:** detect at the **proposal/design** stage, not
    at apply. Specs reference `derivation.md` and call `arty`; they never author
    physics. `apply` is **blocked** until the quantity exists in `src/arty/`.

## Gate 3 — Correctness questions

**Invariant:** the main agent never investigates or answers a
physics-correctness question inline.

**Trigger (litmus):** answering would mean reading or debugging `src/arty/`.
The "let me read the implementation" reflex *is* the trigger, not an exception.

**On trigger — classify from the user's words:**

- Wrong *physical quantity, geometry, or behavior* (an angle, velocity, count,
    lethality, where fragments go) → @modeler. The brief is the user's literal
    report plus any chart/file they named — do **not** read `src/arty/` first to
    sharpen it; that read is the gate violation (see the model-workflow skill's
    briefing rules).
- Wrong *presentation, layout, widget-state, or wiring* of otherwise-correct
    values → an app/notebook bug — fix in `app/` or the `.qmd` (calling `arty`).
- Needs a quantity `arty` does not return → Gate 2.
- Ambiguous (is the *number* wrong, or just its *rendering*?) → ask the user
    one line.

On a defect, @modeler fixes via the normal passes; @model-reviewer then
independently verifies — the modeler never signs off on its own correction.

## Gate 4 — One dispatch per pass (never thread an instance)

**Invariant:** every @modeler / @model-reviewer pass is a **fresh `Agent`
dispatch**. Once an agent returns, that instance is **done** — never continue
it with `SendMessage` to move it to the next step, feed it review findings, or
ask for a revision. The next pass (including every fix / re-review cycle in
Workflow B) starts a **new** instance, briefed from the durable artifacts
(`scoping.md`, `derivation.md`, `review.md`), never from the prior instance's
live context.

**Trigger (litmus):** you are about to `SendMessage` a modelling agent, or
reply to one that is still open, to advance the workflow. That is the
violation — stop, let it return, and dispatch the next pass fresh with a brief
that points at the artifacts.

**Why it matters:** the cost driver is window **size**, not the cheap per-turn
cache reads — a threaded window is re-written in full at the cache-write tier
on every resume. One incident grew a single modeler to a **~268k window** and
roughly doubled the run. Threading also resets `maxTurns` on every message,
removing the last turn-count guard. Full mechanism and figures:
`.claude/rules/subagent-harness.md`.

**Boundary — this is a window-size rule, not a ban on `SendMessage`.** Gate 4
binds *advancing to the next workflow stage* on an accreted window. Re-firing
the **same** agent to finish an **incomplete single pass** while its window is
still small (~\<70k) is allowed and is *cheaper* than reloading a fresh one —
confirmed by the user 2026-07-26. A pass that returns with an open **question**
is still answered in the *next* fresh dispatch's brief, not by resuming.

## Model tier per pass

@modeler defaults to Opus; an oversized or wasted Opus pass is the most
expensive failure mode in this project. When dispatching, override the model
(Agent tool `model` parameter) by pass type:

- **Sonnet override** — chart/new-math triage, aspect-inventory, and
    correctness-classification passes that stop at a short finding.
- **Agent default (Opus)** — scoping, derivation, src/ implementation,
    notebook presentation, and any pass that writes or judges physics.

## Delegation quick reference

- **@librarian** — any external papers, references, or data lookup; check
    BEFORE building or modifying a model whether literature support is needed.
- **@modeler** — owns one model aspect end-to-end, exactly one pass per
    invocation.
- **@model-reviewer** — after every modeler pass; also checks that no physics,
    computation, or parameter values leaked into a `.qmd`.
- **Every pass is a fresh dispatch** — never continue a modelling agent via
    `SendMessage` to advance the workflow (Gate 4).

Steps, sequencing, artifact paths, and briefing litmus tests: load the
**model-workflow** skill.
