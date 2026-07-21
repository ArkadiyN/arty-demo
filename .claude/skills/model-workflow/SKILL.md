---
name: model-workflow
description: Choreography for physics-modelling work — Workflows A (assessment) and B (update), aspect decomposition, artifact layout, task sequencing, and subagent briefing rules. Load BEFORE delegating any pass to @modeler or @model-reviewer, and whenever a gate in .claude/rules/agents-routing.md fires.
---

# Model Workflow Choreography

The always-on gates (worktree precondition, new-math, correctness routing)
live in `.claude/rules/agents-routing.md`. This skill holds everything else:
how modelling work is decomposed, sequenced, briefed, and where artifacts go.

## Two documentation surfaces — don't duplicate

- **OpenSpec specs** (`openspec/specs/`) — the behavioral contract: what each
  capability does, in testable WHEN/THEN form. Source of record for *behavior*.
- **Model artifacts** (`derivation.md`, the `.qmd` notebook, `src/arty/`) — the
  physics: why the math is what it is and how it's derived. Source of record
  for the *model*.

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
        review.md             ← REQUIRED after every review pass, written by
                                @model-reviewer (appended on re-review)
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
1. Delegate to @model-reviewer → writes `review.md` with
   PASS / PASS-with-limitations / FAIL and tagged findings (Blocking /
   Deferrable / Note, each with an impact estimate), and returns a summary.
   An inline-only verdict is not a completed review pass. **On return, the
   main agent verifies `review.md` exists on disk** — a background dispatch
   can silently drop the write (see subagent-harness gotchas); if it is
   missing, the main agent persists the returned review verbatim to
   `review.md` before acting on the verdict.
1. **PASS-with-limitations is a terminal verdict, not a FAIL** — the next
   @modeler pass logs the listed limitation entries (derivation assumptions
   and/or `_limitations.qmd`) as part of its normal work; no re-review of
   those entries is needed.
1. If FAIL: at most **two** fix cycles (@modeler fix → @model-reviewer
   re-review, scoped to the flagged items only). **Each fix and each re-review
   is a new dispatch** — the fix @modeler and the re-review @model-reviewer are
   fresh instances briefed from `review.md`, never the same instances continued
   via `SendMessage` (agents-routing.md Gate 4). Still FAIL after two cycles →
   stop looping; the main agent triages each open item — convert to a logged
   limitation, or escalate to the human with the reviewer's impact estimates.
   Do not silently start a third cycle.
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

Parent agent reviews each return before sending the next task. Each numbered
step above is a **fresh `Agent` dispatch** — "→ return" means that instance is
finished. **Never continue a modelling agent with `SendMessage` to move it to
the next step or hand it review findings** (agents-routing.md Gate 4): that
defeats the per-invocation context reset and grows one unbounded window. The
next pass reads the artifacts (`scoping.md` / `derivation.md` / `review.md`),
not the prior instance's live thread.
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

Two concrete shapes of this violation to watch for:

- **"Specifically check whether X calls the same Y as Z, or implements its
  own copy"** — that sentence names an internal mechanism and pre-answers the
  structural question before @modeler looks at anything. It is the
  investigation you are delegating; remove it and state the goal instead
  ("verify the two paths share the same fragment-physics functions").
- **A `Files to read:` list that enumerates specific function names** (e.g.
  `four_zone_field, lethal_density_*, fragment_velocity`) — those names came
  from a read you should not have done. Inputs may name top-level files
  (`zones.py`, `fragmentation.py`) but never their internals; navigating
  inside those files is @modeler's job.

**@model-reviewer.** Give it the **background** (what was added/changed and
why) and a **pointer** (the diff or function to review) — not a pre-itemized
verification checklist. The reviewer's mandate already covers dimensional
consistency, physical plausibility, boundary-condition behavior, and
literature agreement; a supplied checklist narrows review to only what the
main agent already suspected and crowds out everything else. If you enumerated
specific things to check (a formula, an internal variable, a line range),
that's the same over-read symptom as above — delete the list and point at the
diff instead.
