"""Survey every Claude Code session for a project: compaction count, peak
context, cost split, and what the largest injected block was.

Consumer: produced the cross-session figures in the 2026-08-08 long-session
strategy review (compaction frequency, cost-per-compaction, and the share of
cache-write spend attributable to post-compaction cold re-caches).

Companion to `context-audit.py`, which drills into one session.

Usage:
    uv run python .claude/scripts/session-survey.py            # arty_demo
    uv run python .claude/scripts/session-survey.py <substr>   # match project dirs
"""

import json
import sys
from pathlib import Path

IN_PER_MTOK, OUT_PER_MTOK = 5.00, 25.00
WRITE_PER_MTOK, READ_PER_MTOK = IN_PER_MTOK * 1.25, IN_PER_MTOK * 0.10


def scan(path: Path) -> dict | None:
    seen: set[str] = set()
    reqs: list[dict] = []
    compactions = 0
    biggest = (0, "", "")

    for line in path.read_text(errors="replace").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("isCompactSummary") or d.get("subtype") == "compact_boundary":
            compactions += 1
        msg = d.get("message") or {}
        u, mid = msg.get("usage"), msg.get("id")
        if u and mid and mid not in seen:
            seen.add(mid)
            reqs.append(
                dict(
                    side=bool(d.get("isSidechain")),
                    w=u.get("cache_creation_input_tokens", 0),
                    r=u.get("cache_read_input_tokens", 0),
                    o=u.get("output_tokens", 0),
                )
            )
        content = msg.get("content")
        if isinstance(content, list):
            for b in content:
                if not isinstance(b, dict):
                    continue
                t = b.get("type")
                s = b.get("text") or b.get("thinking") or ""
                if t in ("tool_result", "tool_use"):
                    s = json.dumps(b.get("content") or b.get("input") or "")
                # Base64 image payloads are huge on disk but cheap in context —
                # an image costs (w*h)/750 tokens, capped ~4784 on Opus 5, not
                # len/4. Counting them as text wildly overstates their cost.
                if '"type": "image"' in s[:200] or '"type":"image"' in s[:200]:
                    continue
                if len(s) > biggest[0]:
                    biggest = (len(s), f"{t}:{b.get('name', '')}".rstrip(":"), s[:70].replace("\n", " "))

    if not reqs:
        return None
    main = [q for q in reqs if not q["side"]]
    ctxs = [q["w"] + q["r"] for q in main]
    tw = sum(q["w"] for q in reqs)
    tr = sum(q["r"] for q in reqs)
    to = sum(q["o"] for q in reqs)
    # A cold write (read==0) means the whole prefix was re-cached from scratch:
    # session start, or the request right after a compaction.
    cold = sum(q["w"] for q in reqs if q["r"] == 0)
    return dict(
        name=path.stem[:8],
        reqs=len(reqs),
        side=len(reqs) - len(main),
        comp=compactions // 2,  # boundary + summary line per event
        peak=max(ctxs) if ctxs else 0,
        w=tw,
        r=tr,
        o=to,
        cold=cold,
        cost=tw / 1e6 * WRITE_PER_MTOK + tr / 1e6 * READ_PER_MTOK + to / 1e6 * OUT_PER_MTOK,
        big=biggest,
    )


def main() -> None:
    key = sys.argv[1] if len(sys.argv) > 1 else "arty"
    files = sorted(
        (Path.home() / ".claude" / "projects").glob(f"*{key}*/*.jsonl"),
        key=lambda p: p.stat().st_mtime,
    )
    rows = [r for r in (scan(f) for f in files) if r and r["reqs"] >= 5]
    if not rows:
        sys.exit(f"no sessions with >=5 requests matching {key!r}")

    print(f"{len(rows)} sessions (>=5 requests), oldest first\n")
    hdr = f"{'session':<9}{'reqs':>6}{'sub':>5}{'comp':>6}{'peak ctx':>11}{'write':>11}{'read':>11}{'out':>9}{'cold w':>10}{'$':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(
            f"{r['name']:<9}{r['reqs']:>6}{r['side']:>5}{r['comp']:>6}{r['peak']:>11,}"
            f"{r['w']:>11,}{r['r']:>11,}{r['o']:>9,}{r['cold']:>10,}{r['cost']:>8.2f}"
        )

    tot = {k: sum(r[k] for r in rows) for k in ("reqs", "comp", "w", "r", "o", "cold", "cost")}
    print("-" * len(hdr))
    print(
        f"{'TOTAL':<9}{tot['reqs']:>6}{'':>5}{tot['comp']:>6}{'':>11}"
        f"{tot['w']:>11,}{tot['r']:>11,}{tot['o']:>9,}{tot['cold']:>10,}{tot['cost']:>8.2f}"
    )

    print("\nCOST SHARE")
    for label, val in (
        ("cache write", tot["w"] / 1e6 * WRITE_PER_MTOK),
        ("cache read", tot["r"] / 1e6 * READ_PER_MTOK),
        ("output", tot["o"] / 1e6 * OUT_PER_MTOK),
    ):
        print(f"  {label:<12} ${val:>7.2f}   {val / tot['cost'] * 100:>5.1f}%")
    print(
        f"\n  cold (from-scratch) writes: {tot['cold']:,} tok = "
        f"{tot['cold'] / max(tot['w'], 1) * 100:.1f}% of all cache-write, "
        f"${tot['cold'] / 1e6 * WRITE_PER_MTOK:.2f}"
    )
    print(f"  compaction events: {tot['comp']}")

    print("\nLARGEST SINGLE BLOCK PER SESSION (top 10)")
    for r in sorted(rows, key=lambda r: -r["big"][0])[:10]:
        n, kind, prev = r["big"]
        print(f"  {r['name']}  {n:>9,} chars (~{n // 4:>7,} tok)  {kind:<18} | {prev}")


if __name__ == "__main__":
    main()
