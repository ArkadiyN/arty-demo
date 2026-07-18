## Agent Routing Gates

Physics modelling follows two named workflows — **A (assessment)** and **B
(update)**. The full choreography — workflow steps, aspect decomposition,
artifact layout, task sequencing, briefing rules, documentation surfaces —
lives in the **model-workflow** skill. **Load that skill (Skill tool) before
delegating any pass to @modeler or @model-reviewer.**

The three gates below bind the **main agent**, always — at every entry point
(direct request, new chart, or an OpenSpec `/opsx:propose` / `/opsx:apply`
step). They constrain the agent, not a tool, so they hold even when a skill or
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

Steps, sequencing, artifact paths, and briefing litmus tests: load the
**model-workflow** skill.
