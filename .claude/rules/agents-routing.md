## Agent Routing Rules

### When to delegate to @librarian

- ANY task requiring external papers, references, or data lookup
- BEFORE building or modifying a physics model, always check
  if literature support is needed
- When parameters need validation against sources

### When to delegate to @modeler

- When building, modifying, or validating physics/ballistics code
- When experimental iteration (write → run → observe → adjust)
  is needed on a model
- When addressing @model-reviewer feedback

### When to delegate to @model-reviewer

- When @modeler finishes building and documenting a model
- When a model is updated

### Workflow: New Physics Model

1. Delegate to @librarian → returns list of literature
1. Delegate to @modeler with folder of literature + modelling goal → returns
   model + code (quarto notebook)
1. @model-reviewer validates the model documentation and provides feedback for @modeler
1. If modeler and model-reviewer cannot agree, escalate to the human
1. Main agent integrates into project

## Modeler Task Sequencing

Never send the modeler a compound task. Break into:

1. Derive → writes to file → return
1. Implement → reads derivation, writes code → return
1. Validate → reads code, runs checks, writes report → return

Parent agent reviews each return before sending next task.
Include file paths in each prompt, not conversation summaries.
