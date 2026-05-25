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

## Workflow A — Assessment ("does X matter?")

A bounded question answered with a self-contained Quarto notebook. The output
is a published verdict; **the main model is not modified**.

1. Delegate to @librarian if external data is needed → returns literature.
1. Delegate to @modeler with the question + parent model path → writes
   `experiment/<model>/challenges/<question>.qmd` with problem statement,
   governing equations, numerical study, and a clear verdict.
1. Delegate to @model-reviewer → validates the analysis.
1. Main agent links the challenge from the parent `.qmd` "Challenges"
   section if the verdict is reader-relevant.

Done when: notebook renders, verdict is unambiguous, reviewer approves.

## Workflow B — Update ("add/change Y in the model")

A change to the integrated model. Produces a derivation, then ports the
result into the main `.qmd`.

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
1. **Integrate** — main agent (or @modeler in a dedicated integration pass)
   edits `experiment/<model>/<model>.qmd`:
   - update equations, parameters, validation
   - add an entry to the model's `## Change Log` section referencing
     `updates/<change-slug>/derivation.md`
1. Re-render the main notebook to confirm it still produces clean output.

Done when: main `.qmd` reflects the derivation, change-log entry exists,
notebook renders.

## When to delegate to @librarian

- ANY task requiring external papers, references, or data lookup.
- BEFORE building or modifying a physics model, check whether literature
  support is needed.
- When parameters need validation against sources.

## When to delegate to @modeler

- When building, modifying, or assessing physics/ballistics code.
- When experimental iteration (write → run → observe → adjust) is needed.
- When addressing @model-reviewer feedback.

## When to delegate to @model-reviewer

- When @modeler finishes an assessment, scoping doc, derivation, or
  integration pass.
- When the main model notebook is updated.

## Modeler task sequencing

Never send the modeler a compound task. Use one prompt per artifact:

1. Scoping → writes `scoping.md` → return.
1. Derivation → reads scoping, writes `derivation.md` → return.
1. Implementation (assessments only) → reads derivation, writes/extends
   `<question>.qmd` → return.
1. Validation → reads code, runs checks, writes report → return.
1. Integration (updates only) → reads approved derivation, edits main
   `<model>.qmd` + change log → return.

Parent agent reviews each return before sending the next task.
Include file paths in each prompt, not conversation summaries.
