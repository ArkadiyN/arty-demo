---
name: gotcha-check-script-imports-shipped-constant
description: A check script that imports a shipped src/arty constant to close a source's own arithmetic validates nothing; keep the source's stated value as a separate literal
metadata:
  type: project
---

A closure script that does `from arty.fragmentation import _MOTT_BREADTH_FACTOR`
and then checks the paper's own arithmetic is **tautological** — it passes as
long as the constant equals whatever the paper used, and it breaks the moment
the constant is legitimately revised (which is what happened when κ_x moved
1.5 → 1.62).

**Why:** a paper-internal closure and a validation of a shipped constant are
two different checks. The first must run on the source's *stated* value held as
its own literal; the second is a separate assertion, and usually there is no
evidence for it at all.

**How to apply:** in `challenges/*/checks/*.py`, keep the source's number as a
named literal (`MOTT_STATED_KAPPA_X = 1.5`, anchored to its page) and import
the shipped constant only for a *pinned divergence diagnostic* that prints the
expected mismatch. Live example:
`challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`
(C1 paper-internal, C1b shipped-vs-page). Related:
[[gotcha-rebaseline-onto-validation-source]].
