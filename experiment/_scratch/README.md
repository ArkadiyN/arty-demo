# `_scratch/` — staging, not a wastebasket

This is the **only** staging area for in-flight check scripts. It exists
because `/tmp` is not an allow-listed Write path for subagents (see
`.claude/rules/subagent-harness.md`).

**It is deliberately not gitignored.** Anything left here shows up as untracked
in `git status` — that is the prompt to resolve it.

**Before a pass ends, this directory must be empty again.** Every script is
resolved one of two ways:

- It produced a number now cited in a committed artifact → `git mv` it to that
    artifact's `checks/` folder and commit it *with* the artifact.
- It produced nothing that got cited → delete it. Only this case.

Full rule, including naming and runnability requirements:
`.claude/rules/verification-scripts.md`.

## Already lost — the reason this rule exists

These nine scripts produced numbers that appear in committed artifacts. They
were written here (or in a since-removed second staging dir), cited by path,
never committed, and are gone. The documents below still reference them; the
paths do not resolve and will not. Their numbers survive only as claims — to
re-check any of them, the script has to be written again from scratch.

| Lost script                     | Cited by                                                                         |
| ------------------------------- | -------------------------------------------------------------------------------- |
| `tolch-panel-distance-check.py` | `fragmentation-field/challenges/drag-gap-1944/tolch-1944-panel-distance.md`      |
| `mott_scale_check.py`           | `fragmentation-field/challenges/mott-scale-gap/_scale_verdict_ledger.md`         |
| `mott_shape_closure.py`         | `fragmentation-field/updates/mott-fragment-shape-closure/{derivation,review}.md` |
| `bench.py`                      | `fragmentation-field/updates/field-builder-performance/{derivation,review}.md`   |
| `quad_check.py`                 | `fragmentation-field/updates/target-height-intercept/derivation.md`              |
| `verify_familyA_fix.py`         | `fragmentation-field/updates/familyA-false-safe-zone/review.md`                  |
| `wdss1_c8_check.py`             | `fragmentation-field/updates/wdss1-steel-grade/review.md`                        |
| `wdss1_review_check.py`         | `fragmentation-field/updates/wdss1-steel-grade/review.md`                        |
| `wdss1_srcpass_check.py`        | `fragmentation-field/updates/wdss1-steel-grade/review.md`                        |

Do not add a tenth. If one of these is ever rewritten, commit it to the citing
artifact's `checks/` folder and strike its row here.
