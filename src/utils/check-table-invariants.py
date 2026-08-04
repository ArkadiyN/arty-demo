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
                         [by <group-column>]        restart per group
    total:      <column> == <value> within <tol>[%]  sum over all rows
    tiling:     <group-column> <lo-column> <hi-column>

`tiling` and `by` exist for **bracketed-limit tables** — calibre classes,
velocity bands, thickness ranges — where the closure is not down the whole
column but within one group of consecutive brackets:

    tiling:     projectile_size_class yield_lo_psi yield_hi_psi
    monotonic:  coupon_diam_in non-increasing by projectile_size_class

Tiling asserts that row *i*'s upper bound equals row *i+1*'s lower bound inside
each group. When the source states brackets as "Over X to Y, incl.", sharing an
endpoint is not a formatting convention — it is what makes the table total over
its stated domain. A gap is a value the table does not cover; an overlap is two
contradictory answers for one value; and either is what a row read one step out
of position looks like. A blank bound (an open-ended first bracket) is reported
as unchecked rather than silently passed.
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
    r"^(?P<col>\w+)\s+(?P<dir>increasing|decreasing|non-increasing|non-decreasing)"
    r"(?:\s+by\s+(?P<group>\w+))?$"
)
_TILING_RE = re.compile(r"^(?P<group>\w+)\s+(?P<lo>\w+)\s+(?P<hi>\w+)$")

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
        elif key in ("row", "total", "monotonic", "tiling"):
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


def group_runs(rows, group_col):
    """Split rows into consecutive runs sharing a value of `group_col`.

    Runs, not a dict of all rows with equal keys: a bracketed table's groups are
    printed contiguously, and a group whose rows are *not* contiguous is itself
    the row-misassignment this rule is looking for. Yields (name, [(idx, row)]).
    """
    runs, current, name = [], [], object()
    for i, row in enumerate(rows):
        key = row.get(group_col)
        if key != name:
            if current:
                runs.append((name, current))
            current, name = [], key
        current.append((i, row))
    if current:
        runs.append((name, current))
    return runs


def check_monotonic(body, rows, _ns):
    """Ordering: <column> <direction> [by <group-column>].

    With `by`, the ordering must hold inside each group and is not asserted
    across a group boundary — the shape of a table whose column restarts per
    calibre class, velocity band, or thickness range.
    """
    m = _MONO_RE.match(body)
    if not m:
        raise SpecError(f"malformed monotonic check: {body!r}")
    col, direction, group_col = m["col"], m["dir"], m["group"]
    ok = _COMPARATORS[direction]
    if group_col and not any(group_col in r for r in rows):
        raise SpecError(f"monotonic: no such group column {group_col!r}")
    runs = group_runs(rows, group_col) if group_col else [(None, list(enumerate(rows)))]

    failures = []
    for name, run in runs:
        where = f" in {name!r}" if group_col else ""
        for (i, ra), (j, rb) in zip(run, run[1:]):
            a, b = ra.get(col), rb.get(col)
            if not isinstance(a, float) or not isinstance(b, float):
                failures.append((i, f"column {col!r} missing or non-numeric{where}"))
                break
            if not ok(a, b):
                failures.append((j, f"{col}: {a:g} -> {b:g} is not {direction}{where}"))
    return failures


def check_tiling(body, rows, _ns):
    """Bracket tiling: <group-column> <lo-column> <hi-column>.

    Inside each group, row i's upper bound must equal row i+1's lower bound. A
    gap leaves a value the table does not cover; an overlap gives two answers
    for one value. A blank bound (an open-ended first or last bracket, as the
    source prints it) is reported as unchecked, never silently passed.
    """
    m = _TILING_RE.match(body)
    if not m:
        raise SpecError(f"malformed tiling check: {body!r}")
    group_col, lo_col, hi_col = m["group"], m["lo"], m["hi"]
    for col in (group_col, lo_col, hi_col):
        if not any(col in r for r in rows):
            raise SpecError(f"tiling: no such column {col!r}")

    failures = []
    for name, run in group_runs(rows, group_col):
        for (i, ra), (j, rb) in zip(run, run[1:]):
            hi, next_lo = ra.get(hi_col), rb.get(lo_col)
            if not isinstance(hi, float) or not isinstance(next_lo, float):
                failures.append(
                    (j, f"bracket bound blank in {name!r} — tiling unchecked here")
                )
                continue
            if hi != next_lo:
                kind = "gap" if next_lo > hi else "overlap"
                failures.append(
                    (j, f"{name!r}: bracket ends at {hi:g}, next starts at "
                        f"{next_lo:g} — {kind}")
                )
    return failures


_HANDLERS = {
    "row": check_row,
    "total": check_total,
    "monotonic": check_monotonic,
    "tiling": check_tiling,
}


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
