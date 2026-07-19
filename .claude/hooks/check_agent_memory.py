#!/usr/bin/env python3
"""PostToolUse hook: enforce agent-memory size discipline (Write|Edit).

Backs the hard-limits section of .claude/skills/agent-memory-discipline.
Exit 2 feeds stderr back to the agent that wrote the file.
"""
import json
import re
import sys
from pathlib import Path

MAX_ENTRY_LINES = 30
MAX_INDEX_LINE_CHARS = 250
STATUS_RE = re.compile(r"^\s*\*\*(resolved|fixed|confirmed)\b", re.I)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if ".claude/agent-memory/" not in path.replace("\\", "/"):
        return 0
    p = Path(path)
    if not p.is_file():
        return 0
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    problems = []
    if p.name == "MEMORY.md":
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
    else:
        if len(lines) > MAX_ENTRY_LINES:
            problems.append(
                f"entry is {len(lines)} lines (max {MAX_ENTRY_LINES} incl."
                " frontmatter) — one fact per file: compress to the gotcha plus"
                " a pointer to derivation.md/review.md, or split/delete"
            )
        for i, ln in enumerate(lines, 1):
            if STATUS_RE.match(ln):
                problems.append(
                    f"line {i}: status paragraph ({ln.strip()[:40]!r}…) — never"
                    " log status into memory; when a gotcha closes, shrink the"
                    " entry to the durable pattern or delete it"
                )
    if problems:
        print(f"agent-memory discipline violation in {path}:", file=sys.stderr)
        for msg in problems:
            print(f"  - {msg}", file=sys.stderr)
        print(
            "Per the agent-memory-discipline skill: fix this file now"
            " (the write already landed).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
