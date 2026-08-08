@import .claude/rules/git-flow.md
@import .claude/rules/agents-routing.md
@import .claude/rules/significant-decisions.md
@import .claude/rules/subagent-harness.md
@import .claude/rules/verification-scripts.md
@import ./project_scope.md
@import .claude/rules/source-data-fidelity.md
@import .claude/rules/deferred-findings.md

## Arguing with a rule

Every rule above states its cost in one line and links to
`.claude/incidents.md`. That file is **not** loaded — nothing pulls it in
automatically. `Read` it in exactly one situation: you are about to deviate
from a rule, override it, or judge it inapplicable to your case. The evidence
that would change your mind is there and nowhere else. Following a rule needs
no trip; breaking one does.

## Runtime environment

- This project uses `uv` for Python environment management
- Use it when need to run Python
