"""Verify that a transcribed source table satisfies its declared closure invariants.

Enforces `.claude/rules/source-data-fidelity.md`: a table extracted from an
external source is inadmissible until a relation internal to the table —
derived from the source's own stated definitions — is shown to hold on every
row. This tool carries no domain knowledge; the invariant is declared next to
the data by whoever transcribed it.

Usage:
    uv run src/utils/check-table-invariants.py <path-to-.invariant>
    uv run src/utils/check-table-invariants.py doc-reference/ --all

Exit code is 1 if any declared invariant fails, so this can gate a commit.

Spec format (`<table-slug>.invariant`, plain text, `#` comments):

    csv:     75mm-m48-casualties.csv     # relative to the spec file
    source:  ../ordnance-1944.md
    anchor:  # 75-MM H.E. SHELL, M48     # greppable string, not a line number

    # Each row's lightest effective fragment must reproduce the caption's
    # stated 58 ft-lb casualty criterion. m in oz, v in ft/s -> ft-lb.
    row:        0.5 * (m / 16 / 32.174) * v**2 == 58 within 5%
    monotonic:  r increasing
    monotonic:  N non-increasing
    monotonic:  B non-increasing   # not `decreasing` — rounded tails tie

Directives:
    csv / source / anchor  metadata; `csv` is required, the rest documentary
    row:        <expr> == <value> within <tol>[%]   evaluated per row
    monotonic:  <column> increasing | decreasing
                         | non-increasing | non-decreasing
    total:      <column> == <value> within <tol>[%]  sum over all rows
"""

import argparse
import csv
import math
import re
import sys
from pathlib import Path

_ROW_RE = re.compile(r"^(?P<expr>.+?)\s*==\s*(?P<target>\S+)\s+within\s+(?P<tol>\S+)$")
_TOTAL_RE = _ROW_RE
_MONO_RE = re.compile(
    r"^(?P<col>\w+)\s+(?P<dir>increasing|decreasing|non-increasing|non-decreasing)$"
)

_SAFE_NS = {k: getattr(math, k) for k in ("sqrt", "exp", "log", "log10", "sin", "cos", "tan", "pi", "e")}
_SAFE_NS["abs"] = abs

_COMPARATORS = {
    "increasing": lambda a, b: b > a,
    "decreasing": lambda a, b: b < a,
    "non-increasing": lambda a, b: b <= a,
    "non-decreasing": lambda a, b: b >= a,
}


class SpecError(Exception):
    """The .invariant file is malformed — distinct from a failing invariant."""


def parse_tolerance(text, target):
    """Return an absolute tolerance from '5%' or '0.5'."""
    if text.endswith("%"):
        return abs(target) * float(text[:-1]) / 100.0
    return float(text)


def parse_spec(path):
    """Parse a .invariant file into {meta, checks}."""
    meta, checks = {}, []
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.split("#")[0].strip() if not raw.strip().startswith("#") else ""
        if not line:
            continue
        if ":" not in line:
            raise SpecError(f"{path}:{lineno}: expected '<directive>: <body>'")
        key, body = (s.strip() for s in line.split(":", 1))
        if key in ("csv", "source", "anchor"):
            meta[key] = body
        elif key in ("row", "total", "monotonic"):
            checks.append((key, body, lineno))
        else:
            raise SpecError(f"{path}:{lineno}: unknown directive {key!r}")
    if "csv" not in meta:
        raise SpecError(f"{path}: missing required 'csv:' directive")
    return meta, checks


def load_rows(csv_path):
    """Read the CSV into a list of {column: float-or-str} dicts."""
    with csv_path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SpecError(f"{csv_path}: no data rows")
    out = []
    for row in rows:
        rec = {}
        for k, v in row.items():
            if k is None:
                continue
            text = (v or "").strip().replace(",", "")
            try:
                rec[k.strip()] = float(text)
            except ValueError:
                rec[k.strip()] = text
        out.append(rec)
    return out


def check_row(body, rows, ns):
    """Per-row closure: <expr> == <target> within <tol>."""
    m = _ROW_RE.match(body)
    if not m:
        raise SpecError(f"malformed row check: {body!r}")
    target = float(m["target"])
    tol = parse_tolerance(m["tol"], target)
    failures = []
    for i, row in enumerate(rows):
        try:
            value = eval(m["expr"], {"__builtins__": {}}, {**ns, **row})  # noqa: S307
        except Exception as exc:  # noqa: BLE001
            failures.append((i, f"could not evaluate: {exc}"))
            continue
        if abs(value - target) > tol:
            failures.append((i, f"got {value:.6g}, expected {target:g} ± {tol:.3g}"))
    return failures


def check_total(body, rows, ns):
    """Column sum: <column> == <target> within <tol>."""
    m = _TOTAL_RE.match(body)
    if not m:
        raise SpecError(f"malformed total check: {body!r}")
    col = m["expr"].strip()
    target = float(m["target"])
    tol = parse_tolerance(m["tol"], target)
    missing = [i for i, r in enumerate(rows) if not isinstance(r.get(col), float)]
    if missing:
        return [(missing[0], f"column {col!r} missing or non-numeric")]
    total = sum(r[col] for r in rows)
    if abs(total - target) > tol:
        return [(None, f"sum({col}) = {total:.6g}, expected {target:g} ± {tol:.3g}")]
    return []


def check_monotonic(body, rows, _ns):
    """Ordering: <column> increasing|decreasing|non-increasing|non-decreasing."""
    m = _MONO_RE.match(body)
    if not m:
        raise SpecError(f"malformed monotonic check: {body!r}")
    col, direction = m["col"], m["dir"]
    ok = _COMPARATORS[direction]
    failures = []
    for i in range(len(rows) - 1):
        a, b = rows[i].get(col), rows[i + 1].get(col)
        if not isinstance(a, float) or not isinstance(b, float):
            failures.append((i, f"column {col!r} missing or non-numeric"))
            break
        if not ok(a, b):
            failures.append((i + 1, f"{col}: {a:g} -> {b:g} is not {direction}"))
    return failures


_HANDLERS = {"row": check_row, "total": check_total, "monotonic": check_monotonic}


def check_spec(spec_path):
    """Run every check in one spec. Returns (n_checks, [(kind, body, failures)])."""
    meta, checks = parse_spec(spec_path)
    rows = load_rows((spec_path.parent / meta["csv"]).resolve())
    results = []
    for kind, body, lineno in checks:
        try:
            failures = _HANDLERS[kind](body, rows, _SAFE_NS)
        except SpecError as exc:
            raise SpecError(f"{spec_path}:{lineno}: {exc}") from exc
        results.append((kind, body, failures))
    return len(rows), results


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", help="a .invariant file, or a directory to scan")
    parser.add_argument(
        "--all",
        action="store_true",
        help="scan PATH recursively for *.invariant instead of treating it as one file",
    )
    args = parser.parse_args()

    target = Path(args.path)
    specs = sorted(target.rglob("*.invariant")) if args.all or target.is_dir() else [target]
    if not specs:
        print(f"no .invariant files found under {target}")
        return

    failed = 0
    for spec in specs:
        try:
            n_rows, results = check_spec(spec)
        except (SpecError, FileNotFoundError) as exc:
            print(f"{spec}\n    SPEC ERROR: {exc}")
            failed += 1
            continue
        bad = [r for r in results if r[2]]
        status = "FAIL" if bad else "ok"
        print(f"{spec}  ({n_rows} rows, {len(results)} checks) {status}")
        for kind, body, failures in bad:
            print(f"    {kind}: {body}")
            for idx, detail in failures:
                where = "total" if idx is None else f"row {idx}"
                print(f"        {where}: {detail}")
        if bad:
            failed += 1

    print(f"\n{failed} / {len(specs)} table(s) failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
