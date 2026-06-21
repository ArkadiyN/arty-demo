## Agent Routing Rules

Physics modelling work in this project follows one of **two named workflows**.
Decide which one applies *before* delegating; the artifacts and "done"
conditions differ.

## Worktree precondition — always on

This gate binds the **main agent** and is checked *before* either gate below,
not just before Workflow A/B. **Invariant:** the main agent never dispatches
@modeler or @model-reviewer unless it has already entered a worktree this
session (`EnterWorktree` called, not exited).

**Why this is its own gate, not folded into "new work":** both agents carry
`memory: project` in their frontmatter, which auto-grants Write/Edit to their
own memory directory (`.claude/agent-memory/<agent>/`) regardless of the
agent's declared `tools:` line — see `model-reviewer.md`, whose only declared
tools are `Read, Bash`. Both agents are instructed to consult and update that
memory on **every pass**, including a one-line chart/new-math triage or a
correctness-question investigation that touches no model artifact. A dispatch
that looks read-only can still write to disk. Since `.claude/agent-memory/` is
a git-tracked directory, whichever checkout the main agent is sitting in when
it dispatches is where that write lands — there is no separate routing step
that could send it elsewhere.

**On trigger:** if the main agent has not entered a worktree yet, do so
(`EnterWorktree`) before sending any prompt to @modeler or @model-reviewer,
even a question with no expected file output.

## New-math gate — always on

This gate binds the **main agent**, in every flow and at every entry point: a
direct request, a new chart, or while the agent is executing an OpenSpec
`/opsx:propose` / `/opsx:apply` step. Because it constrains the agent (not a
tool), it holds even when a skill or a task says "implement" — no tool's
instructions override it.

**Invariant:** the main agent never authors or inlines a physical or derived
quantity. All such math lives in `src/arty/` and is produced by @modeler.

**Trigger (litmus):** the work needs a physical or derived quantity that an
`src/arty/` function does not already return. *Mentioning the model is not the
trigger — reuse is fine; computing a new number is.* Aggregations, unit
conversions, ratios, calibrations and "quick transforms" count as new math
when they encode a physical quantity.

**On trigger — stop and hand off:**

- If it is unclear whether new math is needed, delegate a **chart / new-math
  triage** to @modeler (describe the quantities and axes; ask the single
  yes/no). @modeler returns *no new math* or *new math needed* (naming the
  missing quantity) and STOPs.
- *No new math* → proceed: build the chart / implement the task by importing
  and calling `arty`; only layout and styling live in `app/` or the `.qmd`.
- *New math needed* → run **Workflow B** (scoping → derivation →
  @model-reviewer → `src/arty/`) first, then wire it up. The agent never
  writes the math.

**Inside an OpenSpec change** (we do not modify OpenSpec — this governs the
agent running it): detect the trigger at the **proposal/design** stage, not at
apply. OpenSpec specs and tasks reference `derivation.md` and call `arty`;
they never author physics. If a change needs math not yet in `src/arty/`, the
modeler flow runs first and `apply` is **blocked** until the quantity exists.
A new chart is just one case of this gate, not a separate rule.

## Correctness-question gate — always on

**Invariant:** the main agent never investigates or answers a physics-correctness
question inline. "Is this right / why does it do X / this is wrong" about
already-implemented physics goes to @modeler.

**Trigger (litmus):** answering would mean reading or debugging `src/arty/`.
The "let me read the implementation" reflex *is* the trigger, not an exception.

**On trigger — classify from the user's words:**

- Wrong *physical quantity, geometry, or behavior* (an angle, velocity, count,
  lethality, where fragments go) → @modeler.
- Wrong *presentation, layout, widget-state, or wiring* of otherwise-correct
  values (z-order, overlap, labels, a slider not matching the chart) → an
  app/notebook bug — fix in `app/` or the `.qmd` (calling `arty`), not @modeler.
- Needs a quantity `arty` does not return → the new-math gate above.

If the classification is clear from the prompt, route accordingly; if it is
ambiguous (is the *number* wrong, or just its *rendering*?), ask the user one
line. On a physics-correctness defect the brief to @modeler is the user's
literal report plus any chart/file they named — finding and diagnosing it is the
modeler's job. See "Briefing subagents — problems, not solutions" below: do not
read `src/arty/` first to sharpen the brief — that read is the gate violation,
not a way to satisfy it.

- @modeler investigates/answers; if a defect, fixes via the normal passes
  (derivation → src/ → notebook). @model-reviewer then independently verifies
  the fix; the modeler never signs off on its own correction.

## Two documentation surfaces — don't duplicate

Functionality is documented in two complementary places:

- **OpenSpec specs** (`openspec/specs/`) — the behavioral contract: what each
  capability does, in testable WHEN/THEN form. Source of record for *behavior*.
- **Model artifacts** (`derivation.md`, the `.qmd` notebook, `src/arty/`) — the
  physics: why the math is what it is and how it's derived. Source of record for
  the *model*.

Specs reference derivations and call `arty`; they never restate the physics. A
behavior/contract change updates the spec; a physics change updates the model
artifacts, and the spec points to the new `derivation.md`.

## Artifact layout

Everything related to a model lives under that model's folder:

```
experiment/
  <model>/
    <model>.qmd               ← integrated, reader-facing model notebook
    challenges/
      <question>.qmd          ← self-contained "does X matter?" notebooks or .md
    updates/
      <change-slug>/
        scoping.md            ← problem, options, literature audit, recommendation
        derivation.md         ← math + unit checks + self-consistency
        review.md             ← optional, written by @model-reviewer
```

- `challenges/` are permanent — they publish a verdict that informs readers.
- `updates/<change-slug>/` are working folders — once the change is integrated
  into the main `.qmd` (and the change history there links back), the folder
  can be archived or deleted.
- Do not create top-level `docs/modeler-notes/` or `experiment/<question>/`
  directories. All modelling artifacts belong with their parent model.

## Decompose first — one model aspect per change

Before delegating any modelling work, decompose the request into distinct
**model aspects**. Treat something as a *separate aspect* if it has any of:

- its own **governing-equation set** (e.g. an ogive Gurney cone vs. a
  presented-area profile A_p(gamma) are different math),
- its own **parameter group** that can be validated independently,
- a **separately checkable output** (the reviewer could PASS/FAIL it alone).

Rules:

- **One aspect = one `<change-slug>` = one `updates/<slug>/` folder = one
  modeler scoping/derivation pass.** Never bundle aspects into a single
  change "to integrate them together" — that is the main cause of oversized
  modeler outputs and tangled artifacts.
- If two aspects are **coupled**, keep them in separate folders and
  **sequence** them: derive → review → integrate → re-render aspect A, *then*
  derive aspect B on top of the updated model. Record the dependency in B's
  `scoping.md`.
- The decomposition (the aspect inventory + order) is cheap work — do it in
  the main agent, not by sending the whole bundle to the Opus modeler.
- If you are unsure how to split, delegate a **single aspect-inventory pass**
  to @modeler (it will list aspects + dependencies + order and STOP), then
  drive one aspect at a time.

## Workflow A — Assessment ("does X matter?")

A bounded question answered with a self-contained Quarto notebook. The output
is a published verdict; **the main model is not modified**.

1. Delegate to @librarian if external data is needed → returns literature.
1. Delegate to @modeler with the question + parent model path → writes
   `experiment/<model>/challenges/<question>.md` (markdown): problem
   statement, governing equations, the numerical study to run, and the verdict
   criterion. Return.
1. If the assessment needs physics not yet in `src/arty/`, delegate to
   @modeler to add it there first (src/ implementation pass). Return.
1. Delegate to @modeler (notebook pass) → writes the thin
   `challenges/<question>.qmd` that imports from `arty`, runs it, and renders.
   No physics in the `.qmd`. Return.
1. Delegate to @model-reviewer → validates the analysis and the verdict.
1. Main agent links the challenge from the parent `.qmd` "Challenges"
   section if the verdict is reader-relevant.

Done when: notebook renders, verdict is unambiguous, reviewer approves.

## Workflow B — Update ("add/change Y in the model")

A change to the integrated model. Produces a derivation, then ports the
result into the main `.qmd`. **Each change covers exactly one model aspect**
(see "Decompose first" above); a request touching N aspects becomes N changes.

1. Delegate to @librarian if literature is needed → returns sources.
1. Delegate to @modeler **scoping pass** → writes
   `experiment/<model>/updates/<change-slug>/scoping.md` (problem,
   options ranked, literature audit, recommendation). Return.
1. Main agent reviews scoping. If approved, delegate @modeler **derivation
   pass** → writes `derivation.md` (math, unit checks, self-consistency).
   Return.
1. Delegate to @model-reviewer → writes `review.md` (or returns inline) with
   PASS/FAIL and issues.
1. If FAIL, loop @modeler ↔ @model-reviewer until PASS, or escalate to human.
1. **Implement (src/)** — delegate to @modeler. It writes the derived physics
   into `src/arty/` modules (functions, parameters, geometry) via targeted
   `Edit`s. All project physics is common and lives here — never in the `.qmd`.
   Return.
1. **Present (notebook)** — delegate to @modeler (notebook pass). It edits the
   relevant section **partial** `experiment/<model>/_<section>.qmd` (or adds a
   new partial + `{{< include >}}` line) to import the new `src/arty/` code and
   render results, and adds a `## Change Log` entry (major.minor) referencing
   `updates/<change-slug>/derivation.md`. Edit, never rewrite. Re-render to
   confirm clean output. Because the notebook carries no physics, this pass is
   small — the modeler is calling its own `src/arty/` code, so no handoff.

Done when: physics is in `src/arty/`, the notebook reflects it, change-log
entry exists, notebook renders.

## When to delegate to @librarian

- ANY task requiring external papers, references, or data lookup.
- BEFORE building or modifying a physics model, check whether literature
  support is needed.
- When parameters need validation against sources.

## When to delegate to @modeler

The modeler owns a model aspect **end-to-end** (one pass per invocation):

- **Physics reasoning** — which model applies, governing equations, parameters,
  validation criteria → markdown (`scoping.md` / `derivation.md` /
  `challenges/<question>.md`).
- **src/ implementation** — write/edit the `src/arty/` modules from an approved
  derivation. All project physics is common and lives in `src/arty/`, never in
  a `.qmd`.
- **Notebook presentation** — edit the thin `.qmd`/partial to import from
  `src/arty/`, render, add prose / change-log, and `quarto render`. No physics
  in the `.qmd`; if a needed function/constant isn't in `src/arty/` yet, add it
  there (a src/ pass) first.
- Addressing @model-reviewer feedback.

## When to delegate to @model-reviewer

- When @modeler finishes a scoping doc or derivation.
- When @modeler finishes a src/ implementation or a notebook presentation pass.
- When the main model notebook is updated. **Also check that no physics,
  computation, or parameter values leaked into the `.qmd`** — everything must
  be imported from `src/arty/`.

## Task sequencing

Never send a compound task. "Compound" means **both** more than one artifact
*and* more than one model aspect — one prompt covers one pass on one aspect.
All passes go to @modeler (it owns the aspect end-to-end). Edit, never rewrite,
in every pass:

1. Scoping → @modeler reads cards, writes `scoping.md` → return.
1. Derivation → @modeler reads scoping, writes `derivation.md` → return.
1. src/ implementation → @modeler edits `src/arty/` from the approved
   derivation → return.
1. Notebook presentation → @modeler edits the `.qmd`/partial to import from
   `arty`, render, add the change-log entry, and re-render → return.

Parent agent reviews each return before sending the next task.
Include file paths in each prompt, not conversation summaries.

## Briefing subagents — problems, not solutions

This applies to both @modeler (investigation/derivation) and @model-reviewer
(review): they are the experts; handing them the answer wastes that and
propagates your errors.

**@modeler.** Give it only: the **goal** (what to produce and why); the
**constraints** (prior decisions referenced by file — "implement what
`scoping.md` resolves" — not re-derived); the **acceptance criteria** (specs,
limiting cases, the verdict question — not the expected answer); and the
**inputs** (files to read + external facts it cannot derive: drawing
dimensions, the user's literal question, which paper holds what).

Do **not** put the formula, the algorithm, the target number, or the code in
the prompt — that is the work you are delegating. **Litmus test:** say *what*
and *why*; let the modeler decide *how* and *what-value*. If you have written a
formula, algorithm, number, or code into the prompt, delete it and state the
goal instead. (Exception: an implementation/presentation pass may reference a
prior pass's recorded decision in `derivation.md` — reference, don't re-derive.)

The same litmus applies to a correctness-investigation brief: give the
**observable symptom**, the **question**, and **file pointers** — never a
pre-built hypothesis or conditional answer tree. If writing the brief required
reading `src/arty/` internals closely enough to name a variable or mechanism
(an azimuth angle, a helper's internal loop), that read was the gate
violation, not preparation for satisfying it — delete the specifics and let
@modeler discover the mechanism cold.

**@model-reviewer.** Give it the **background** (what was added/changed and
why) and a **pointer** (the diff or function to review) — not a pre-itemized
verification checklist. The reviewer's mandate already covers dimensional
consistency, physical plausibility, boundary-condition behavior, and
literature agreement; a supplied checklist narrows review to only what the
main agent already suspected and crowds out everything else. If you enumerated
specific things to check (a formula, an internal variable, a line range),
that's the same over-read symptom as above — delete the list and point at the
diff instead.
