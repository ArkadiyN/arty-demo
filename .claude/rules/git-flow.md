---
name: Git-Flow-Rules
description: This file contains the Git and commit workflow rules for the project
---

# Git and Commit Workflow Rules

## 1. One worktree per task

- **NEVER** commit or push directly to `main` / `master`.
- **NEVER** develop in the primary checkout (the repo root). Interactive
  sessions share its single git `HEAD`, so two sessions working there collide —
  one session's `checkout`/`commit` moves the other's branch out from under it.
  The primary checkout is for **inspection only**.
- **At the start of any task that creates or changes files, work in an isolated
  worktree.** This standing instruction is what authorizes the `EnterWorktree`
  tool (which by design fires only when the user or CLAUDE.md / memory
  explicitly calls for a worktree).

### How to enter a worktree

- **From inside a running session (agent):** call the **`EnterWorktree`** tool.
  It creates a worktree under `.claude/worktrees/<name>` on a fresh branch and
  switches *this* session's working directory into it — no relaunch, and no
  manual `cd` (which would not persist between tool calls anyway). The base
  branch follows the `worktree.baseRef` setting: `fresh` (default) branches from
  `origin/<default-branch>`; `head` branches from the current local HEAD.

- **At launch (human):** start Claude with the `--worktree` flag to begin the
  session already inside a fresh worktree.

- Leave with **`ExitWorktree`** (`keep` to preserve the branch on disk,
  `remove` to delete it). After a branch is merged, clean up any leftover
  worktree with `git worktree remove .claude/worktrees/<name>`.

- **Do NOT** use `git checkout -b` / `git switch -c` in the primary checkout to
  start work — that branch-in-place pattern is what causes the cross-session
  collisions this rule exists to prevent. Use a worktree instead.

- Branch names use `<type>/<slug>` — e.g. `feature/translate-ui`,
  `fix/mcp-playwright`, `chore/openspec-config`.

### Known bug: subagents don't reliably inherit the worktree cwd

Per [anthropics/claude-code#36182](https://github.com/anthropics/claude-code/issues/36182),
a subagent dispatched from a session that has correctly entered a worktree
(confirmed `EnterWorktree` switch, verified cwd) can still start its own Bash
subprocess outside that worktree, forcing it to discover this and `cd` back in
on every command. This is a harness bug, not a sign that `EnterWorktree` was
used wrong — do not "fix" it by re-entering or re-checking the worktree.

**Workaround (brittle, but the only one available until the bug is fixed):**
when delegating file-touching work to any subagent while in a worktree, state
the worktree's absolute path explicitly in the dispatch prompt, and instruct
the subagent to anchor every Bash command and every Read/Edit/Write call to
that absolute path — never rely on an inherited cwd.

## 2. Commit Scoping & Logical Units

- Do not make micro-commits for minor changes (e.g., saving single-line fixes sequentially).
- A commit must represent exactly **one complete, logical unit of work** (e.g., a fully functional React component, a complete translation module parser, or a fully configured MCP tool permission set).

## 3. Squashing and Cleaning History

- If your work required multiple exploratory or incremental commits to complete a single logical task, you **MUST squash** them into a single coherent commit before finalizing the task.
- Use `git rebase -i` or `git reset --soft` to clean up the branch history so that it presents a clean, single-commit logical change to the reviewer.
- The final commit message must follow the Conventional Commits format (e.g., `feat(ui): add generative status card for soviet units`).
