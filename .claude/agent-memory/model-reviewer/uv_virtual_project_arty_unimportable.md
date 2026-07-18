---
name: uv-virtual-project-arty-unimportable
description: pyproject.toml has no [build-system] table, so uv.lock marks the project `source = { virtual = "." }` and `uv sync`/`uv run` never installs `arty` — bare `uv run pytest` / `uv run python -c "import arty"` fail with ModuleNotFoundError even though nothing is wrong with src/arty itself
metadata:
  type: project
---

Repo-wide (confirmed present on `main`, not introduced by any reviewed branch):
`pyproject.toml` has `[tool.setuptools.packages.find] where = ["src"]` but no
`[build-system]` table. Without one, `uv` treats the project as a "virtual"
root for dependency resolution only — `uv.lock` shows
`source = { virtual = "." }` for the `arty-demo` entry — and `uv sync` /
`uv run <anything>` never builds or installs the local `arty` package into
`.venv`. Result: `uv run pytest tests/` fails at collection
(`ModuleNotFoundError: No module named 'arty'`) and even
`uv run python3 -c "import arty"` fails, on a completely clean checkout with
no code changes.

**Why this is a trap, not a code bug:** `uv pip install -e .` builds and
installs `arty-demo` fine (setuptools has no trouble with the `src` layout) —
after that one-time install, `uv run pytest tests/` passes clean (202 passed,
4 skipped, confirmed 2026-07-17). So the physics/test code is not at fault;
this is purely a `pyproject.toml` packaging-config gap (missing
`[build-system]`, or equivalently `[tool.uv] package = true`). A reviewer who
runs the standard `uv run pytest` (mandated by
`.claude/rules/subagent-harness.md`) on a fresh worktree/clone will see 100%
collection failure and could easily misdiagnose it as "the test suite is
broken" or start suspecting the physics changes under review, when the fix is
one `[build-system]` table in `pyproject.toml`.

**How to apply:** if `uv run pytest` or any `uv run python3 -c "import arty..."`
check fails with `ModuleNotFoundError: No module named 'arty'`, do not treat it
as evidence the reviewed diff broke something — first check
`uv.lock`'s `arty-demo` entry for `source = { virtual = "." }` and/or confirm
`pyproject.toml` still lacks `[build-system]`. If so, this is the known gap:
either report it as a standalone packaging finding (recommend adding
`[build-system]` with a setuptools backend, or `[tool.uv] package = true`) and
verify physics code separately via `uv pip install -e .` first, or skip
straight to `uv pip install -e .` before running any other check in the same
session. Leave the environment as found afterward (`uv pip uninstall
arty-demo`) since `.venv` is gitignored but session state may be shared with
other agents in the same worktree.
