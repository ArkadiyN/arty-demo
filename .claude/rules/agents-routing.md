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

### Workflow: New Physics Model

1. Delegate to @librarian → returns list of literature
1. Delegate to @modeler with folder of literature + modelling goal → returns
   model + code (quarto notebook)
1. Main agent integrates into project
