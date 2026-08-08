"""Audit a Claude Code session transcript for what is actually consuming context.

Consumer: produced the figures in the 2026-08-08 context review (the ~165k
single-block `Skill(claude-api)` load, the 305,730-token request, and the
$3.08 / 57%-from-one-write cost split) and in the memory
`feedback_skill_invocation_context_cost.md`. Runnable form of the recipe in
`reference_subagent_token_audit.md`.

Answers two questions:
  1. Did context grow gradually, or did one request spike? (per-request sizes)
  2. What is physically big in the thread? (top content blocks by size)

Usage:
    uv run python .claude/scripts/context-audit.py                # newest session
    uv run python .claude/scripts/context-audit.py <session-id>
    uv run python .claude/scripts/context-audit.py <path-to.jsonl>

Notes:
  - Dedups by `message.id` — the same assistant message appears on several
    jsonl lines, and counting them all inflates every total.
  - `isSidechain` entries are subagent turns; they are reported separately
    because they do not occupy the main window.
"""

import json
import sys
from pathlib import Path

# Opus 5: $5/$25 per MTok. Cache write 1.25x input, cache read 0.1x input.
IN_PER_MTOK, OUT_PER_MTOK = 5.00, 25.00
WRITE_PER_MTOK, READ_PER_MTOK = IN_PER_MTOK * 1.25, IN_PER_MTOK * 0.10

# Claude Code reserves an autocompact buffer below the planning window.
PLANNING_WINDOW, AUTOCOMPACT_BUFFER = 200_000, 33_000
TRIGGER = PLANNING_WINDOW - AUTOCOMPACT_BUFFER


def resolve(arg: str | None) -> Path:
    """Accept a full path, a bare session id, or nothing (newest session)."""
    if arg and arg.endswith(".jsonl"):
        return Path(arg)
    projects = Path.home() / ".claude" / "projects"
    candidates = list(projects.glob(f"*/{arg}.jsonl")) if arg else list(projects.glob("*/*.jsonl"))
    if not candidates:
        sys.exit(f"no transcript found for {arg!r} under {projects}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def block_text(b: dict) -> tuple[str, str]:
    """Return (label, text) for one content block."""
    t = b.get("type")
    if t == "text":
        return t, b.get("text", "")
    if t == "thinking":
        return t, b.get("thinking", "")
    if t == "tool_result":
        return t, json.dumps(b.get("content", ""))
    if t == "tool_use":
        return f"tool_use:{b.get('name', '')}", json.dumps(b.get("input", ""))
    return str(t), json.dumps(b)


def main() -> None:
    path = resolve(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"transcript: {path}\n")

    seen: set[str] = set()
    requests: list[dict] = []
    blocks: list[tuple[int, int, str, str, str]] = []
    compactions: list[int] = []

    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue

        if d.get("isCompactSummary") or d.get("subtype") == "compact_boundary":
            compactions.append(lineno)

        msg = d.get("message") or {}

        usage, mid = msg.get("usage"), msg.get("id")
        if usage and mid and mid not in seen:
            seen.add(mid)
            requests.append(
                dict(
                    line=lineno,
                    sidechain=bool(d.get("isSidechain")),
                    write=usage.get("cache_creation_input_tokens", 0),
                    read=usage.get("cache_read_input_tokens", 0),
                    fresh=usage.get("input_tokens", 0),
                    out=usage.get("output_tokens", 0),
                )
            )

        content = msg.get("content")
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        for b in content or []:
            if isinstance(b, dict):
                label, text = block_text(b)
                blocks.append(
                    (len(text), lineno, str(d.get("type")), label, text[:110].replace("\n", " "))
                )

    for r in requests:
        r["ctx"] = r["fresh"] + r["write"] + r["read"]

    main_chain = [r for r in requests if not r["sidechain"]]
    side = [r for r in requests if r["sidechain"]]

    print(f"requests: {len(requests)} unique  (main {len(main_chain)}, sidechain {len(side)})")
    print(f"compaction markers at lines: {compactions or 'none'}\n")

    print("MAIN-CHAIN CONTEXT PER REQUEST")
    for r in main_chain:
        flag = f"   <<< over {TRIGGER:,} autocompact trigger" if r["ctx"] > TRIGGER else ""
        print(
            f"  line {r['line']:>5}  ctx={r['ctx']:>8,}"
            f"  (write {r['write']:>8,} / read {r['read']:>8,})  out={r['out']:>6,}{flag}"
        )
    if main_chain:
        print(f"\n  peak {max(r['ctx'] for r in main_chain):,}   final {main_chain[-1]['ctx']:,}")

    print("\nLARGEST CONTENT BLOCKS  (a spike here is the cause, not gradual growth)")
    for n, lineno, typ, label, preview in sorted(blocks, reverse=True)[:15]:
        print(f"  {n:>9,} chars (~{n // 4:>8,} tok)  line {lineno:>5}  {typ:<9} {label:<20} | {preview}")

    tw = sum(r["write"] for r in requests)
    tr = sum(r["read"] for r in requests)
    to = sum(r["out"] for r in requests)
    cost = tw / 1e6 * WRITE_PER_MTOK + tr / 1e6 * READ_PER_MTOK + to / 1e6 * OUT_PER_MTOK
    print(f"\ntotals  cache_write={tw:,}  cache_read={tr:,}  output={to:,}")
    print(
        f"cost at Opus 5 rates: ${cost:.2f}  "
        f"(write ${tw / 1e6 * WRITE_PER_MTOK:.2f} / "
        f"read ${tr / 1e6 * READ_PER_MTOK:.2f} / "
        f"out ${to / 1e6 * OUT_PER_MTOK:.2f})"
    )


if __name__ == "__main__":
    main()
