---
name: Git-Flow-Rules
description: This file contains the Git and commit workflow rules for the project
---

# Git and Commit Workflow Rules

## 1. Branch Management

- **NEVER** commit or push directly to the `main` or `master` branch.
- **ALWAYS** use worktrees.
- Before starting any task, check the current branch. If you are on `main`, create a new feature branch using a descriptive name based on the task (e.g., `feature/translate-ui`, `fix/mcp-playwright`).
- All development, testing, and file modifications must happen exclusively on this feature branch.

## 2. Commit Scoping & Logical Units

- Do not make micro-commits for minor changes (e.g., saving single-line fixes sequentially).
- A commit must represent exactly **one complete, logical unit of work** (e.g., a fully functional React component, a complete translation module parser, or a fully configured MCP tool permission set).

## 3. Squashing and Cleaning History

- If your work required multiple exploratory or incremental commits to complete a single logical task, you **MUST squash** them into a single coherent commit before finalizing the task.
- Use `git rebase -i` or `git reset --soft` to clean up the branch history so that it presents a clean, single-commit logical change to the reviewer.
- The final commit message must follow the Conventional Commits format (e.g., `feat(ui): add generative status card for soviet units`).
