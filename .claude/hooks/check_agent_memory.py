#!/usr/bin/env python3
"""Enforce agent-memory discipline. Two entry points, one check:

1. PostToolUse hook (Write|Edit): reads a JSON payload on stdin, checks the
   single written file, exit 2 to feed stderr back to the writing agent.
2. Pre-commit / CLI: file paths passed as argv, checks each, exit 1 on any
   violation so the commit is blocked. This is the *blocking* backstop — the
   PostToolUse hook fires after the write has already landed, and a background
   subagent that ends its turn never acts on the feedback, so a git-time gate
   is what actually keeps a violation out of history.

Backs the hard-limits section of .claude/skills/agent-memory-discipline.
"""
import json
import re
import sys
from pathlib import Path

MAX_ENTRY_LINES = 30
MAX_INDEX_LINE_CHARS = 250

# A memory entry that restates a validation OUTCOME (a per-pass pass/fail
# history) is a review.md in disguise — that is the leak this project keeps
# hitting. These signals are deliberately HIGH-PRECISION: this check blocks a
# commit, so a false positive would wrongly reject a legitimate gotcha. We do
# NOT match soft vocabulary like "dense sweep" or "re-review" — those are the
# durable lessons and citations legitimate methodology memories are made of.
# The real net is the line cap: a sprawling verification narrative (the 74-line
# leak that motivated this) blows past 30 lines regardless of wording.
#
# `**Resolved/Fixed/Confirmed …` — the old task-log openers.
STATUS_RE = re.compile(r"^\s*\*\*(resolved|fixed|confirmed)\b", re.I)
# `**Pass 2 (2026-07-20) — PASS.**`, `**Pass 1 … — FAIL.**` — a per-pass log.
PASS_FAIL_RE = re.compile(r"^\s*\*\*\s*pass\s*\d", re.I)
# Filenames that announce a status/outcome rather than a durable gotcha.
STATUS_NAME_RE = re.compile(r"[_-](fail|pass|passed|failed|review|status)\b", re.I)


def check_entry(name: str, text: str) -> list[str]:
    """Return a list of discipline violations for a single memory file."""
    lines = text.splitlines()
    problems: list[str] = []
    if name == "MEMORY.md":
        for i, ln in enumerate(lines, 1):
            s = ln.rstrip()
            if not s:
                continue
            if not (s.startswith("#") or s.startswith("- ")):
                problems.append(
                    f"line {i}: index entries must be single-line '- ' bullets"
                    " (no continuation lines)"
                )
            elif len(s) > MAX_INDEX_LINE_CHARS:
                problems.append(
                    f"line {i}: index bullet is {len(s)} chars"
                    f" (max {MAX_INDEX_LINE_CHARS}) — tighten the hook text"
                )
        return problems

    if len(lines) > MAX_ENTRY_LINES:
        problems.append(
            f"entry is {len(lines)} lines (max {MAX_ENTRY_LINES} incl."
            " frontmatter) — one fact per file: compress to the gotcha plus"
            " a pointer to derivation.md/review.md, or split/delete"
        )
    stem = name[:-3] if name.endswith(".md") else name
    if STATUS_NAME_RE.search(stem):
        problems.append(
            f"filename {name!r} names a status/outcome (fail/pass/review) —"
            " a validation outcome belongs in review.md, not memory; name the"
            " entry after the durable gotcha instead"
        )
    for i, ln in enumerate(lines, 1):
        if STATUS_RE.match(ln) or PASS_FAIL_RE.match(ln):
            problems.append(
                f"line {i}: status/pass-fail paragraph ({ln.strip()[:40]!r}…)"
                " — never log a validation outcome into memory; that history"
                " belongs in review.md. Shrink to the durable gotcha or delete"
            )
    return problems


def report(path: str, problems: list[str]) -> None:
    print(f"agent-memory discipline violation in {path}:", file=sys.stderr)
    for msg in problems:
        print(f"  - {msg}", file=sys.stderr)
    print(
        "Per the agent-memory-discipline skill: fix this file"
        " (the validation record goes in review.md; memory keeps only the"
        " durable gotcha + a pointer).",
        file=sys.stderr,
    )


def is_memory_path(path: str) -> bool:
    return ".claude/agent-memory/" in path.replace("\\", "/")


def main() -> int:
    argv = sys.argv[1:]
    if argv:
        # CLI / pre-commit mode: block the commit (exit 1) on any violation.
        rc = 0
        for path in argv:
            if not is_memory_path(path):
                continue
            p = Path(path)
            if not p.is_file():
                continue
            problems = check_entry(
                p.name, p.read_text(encoding="utf-8", errors="replace")
            )
            if problems:
                report(path, problems)
                rc = 1
        return rc

    # PostToolUse mode: JSON on stdin, one file, exit 2 to nudge the agent.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not is_memory_path(path):
        return 0
    p = Path(path)
    if not p.is_file():
        return 0
    problems = check_entry(p.name, p.read_text(encoding="utf-8", errors="replace"))
    if problems:
        report(path, problems)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
