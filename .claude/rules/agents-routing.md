## Agent Routing Rules

Physics modelling work in this project follows one of **two named workflows**.
Decide which one applies *before* delegating; the artifacts and "done"
conditions differ.

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
