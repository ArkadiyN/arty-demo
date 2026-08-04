# Source-data audit — thread index

A comprehensive audit of every external source feeding this model, run after
three committed check scripts were found validating a casualty model against
*perforation* data — every digit extracted correctly, assigned to the wrong
column. Eight phases: re-baseline the sources, classify every downstream claim,
fix the workflow that allowed it. **Repairs were deferred by design** — the
deliverable is a map, not a redo.

**Status: the audit is complete. Its repairs are not.** 62 findings are open in
`OPEN-FINDINGS.md`, 20 of them blocking.

## If you are here to do work

Read **`remediation-plan.md`** and nothing else first. It is written for a
session with no prior context and tells you what to read, in what order, and
what to leave alone.

**Do not read `ledger.md` end to end.** It is a 242 KB evidence file, section-
numbered for citation, not for sequential reading. Every other document here
cites it by section (`§17b`, `§34a`); `grep -n '^#' ledger.md` gets you the map.

## What each file is

| file                                    | what it is                                                                                       |
| :-------------------------------------- | :----------------------------------------------------------------------------------------------- |
| `remediation-plan.md`                   | **the entry point for doing work** — the queue, the ordering, the gates                          |
| `ledger.md`                             | the evidence, §1–35, one section per finding or phase; cited by everything else                  |
| `stale-surfaces.md`                     | Phase 6 — published claims known stale, ordered by reader exposure, with their corrected reading |
| `review-criterion-match.md`             | Phase 5 — does the cited data measure what the model computes?                                   |
| `review-provenance.md`                  | Phase 5 — does the primary say what it is cited as saying?                                       |
| `review-void-rulings.md`                | Phase 5 — adversarial re-check of every claim the audit ruled void                               |
| `phase4-drag-law-assessment.md`         | Phase 4 — the two shipped drag constants, assessed not changed                                   |
| `phase4b-tolch-mach-drag-assessment.md` | Phase 4 — the Tolch-based calibrations                                                           |
| `checks/`                               | 36 retained scripts; every number in the documents above came from one                           |

## What the audit changed

Nothing in `src/arty/` — it was assessed, never modified. What it did change is
the workflow that produced the defects: `.claude/rules/source-data-fidelity.md`
(the closure-invariant gate, greppable anchors, the card split, the
absence-of-evidence gate), `.claude/rules/deferred-findings.md`, the
`FINDING` marker system and `OPEN-FINDINGS.md`, `librarian.md`,
`model-reviewer.md`, `check-table-invariants.py`, and the vision extraction
pipeline. Evidence for each sits in `.claude/incidents.md`.
