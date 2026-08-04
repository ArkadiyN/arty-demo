---
name: Verification-Script-Retention
description: Check/verification scripts are permanent artifacts — never deleted, always committed next to the document that cites them. Imported into CLAUDE.md so every agent receives it automatically.
---

# Verification Scripts Are Artifacts, Not Debris

Applies to **every agent** (main conversation and subagents). A script written
to produce a number that lands in a permanent document is itself permanent.

## Invariant — never delete a check script

If a script produced a number, table, or verdict that appears in any committed
artifact (`challenges/**`, `updates/**/derivation.md`, `review.md`, a `.qmd`,
a spec), that script **must be committed**. It is not scratch, not temporary,
and not "done" once its results are folded in.

**Why.** The next pass re-runs or re-reads the script instead of re-deriving it
cold — that reuse is the whole point. A verdict whose script is gone is also
unauditable: a reader can only trust the number. **Nine cited scripts have
already been lost this way**, and the loss leaves no trace in history:
`.claude/incidents.md#lost-check-scripts`.

## Where a script lives

**`experiment/_scratch/` is a staging area — the only one.** Write in-flight
check code there (it is the allow-listed Write path, see
`.claude/rules/subagent-harness.md`). It is **not** gitignored, precisely so
that anything left behind shows up as untracked in `git status`.

**Before a pass ends, every script in staging is resolved one of two ways:**

- **It produced a number that is now in a committed artifact** → `git mv` it
    into that artifact's own folder, under `checks/`:
    - `experiment/<model>/challenges/<thread>/checks/<name>.py`
    - `experiment/<model>/updates/<change-slug>/checks/<name>.py`
- **It produced nothing that got cited** (a dead end, a throwaway probe) →
    it may be deleted. Only this case.

Do not create a second staging directory. `experiment/<model>/_scratch/` and
`updates/<slug>/_scratch/` are **not** valid locations — a script either sits
in the one staging area or in a `checks/` folder next to its artifact.

## Requirements on a retained script

- **Runnable standalone**: `uv run python <path>` from the repo root, with no
    relative-path assumptions and no dependency on the cwd. Import from `arty`.
- **Named for what it checks**, not for when it was written —
    `initial-conditions-155mm-decay.py`, never `check2.py` / `tmp_ke.py`.
- **Docstring names its consumer**: one line saying which document's numbers it
    produced, so the script and the claim can be matched back up.
- **Cited by path from the artifact** it feeds, so the reference survives
    review.
- **Fast enough to re-run — target under ~30 s.** Retention exists so the next
    pass *re-runs* the script; a check nobody will wait for is retained in name
    only. Before running a sweep, estimate its cost: grid points × rows ×
    inner steps. If that product exceeds ~10⁶, vectorise it or cut the grid.

### The performance trap: numpy as a scalar calculator

The recurring shape is a `numpy` import used for scalar math *inside* a Python
loop — `np.interp(v / a, MACH, CD)` on one float, per step, per row, per grid
point. Each such call pays full array-protocol overhead (~µs) to do ~ns of
arithmetic, so the script runs 100–1000× slower than the same arithmetic
vectorised, with no change in results.

Fix: march the whole sweep as one array through the same steps. A parameter
grid whose points take identical, independent steps is one vector operation,
not N loops. Reach for `np.interp` on a *vector* of Machs, not a scalar.

**It is not merely slow — it spends the turn budget of the dispatch that runs
it.** One such sweep took **~9 minutes** where the vectorised form takes 2.5 s
with identical output; the pass hit `maxTurns` mid-analysis and returned zero
artifact bytes after ~78k tokens:
`.claude/incidents.md#numpy-scalar-sweep`.

## Committing

Commit retained scripts in the **same commit** as the document that cites
them. A commit that adds a verdict without the script that produced it is the
failure mode this rule exists to prevent — and it is invisible afterwards,
because the loss leaves no trace in history.
