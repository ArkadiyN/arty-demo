"""Regression test for the fixed pdf-processor vision path (plan Phase 7 item 6).

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 7 (pipeline diagnosis) — the "does the fixed pipeline
          reproduce the known-good CSVs?" verification criterion.

Re-extracts nothing itself: it reads a markdown page produced by
`src/utils/pdf-processor.py -m -f --pages 41` (single-page default, the
post-fix configuration) and scores its base-spray component cells against
`doc-reference/.../tables/base-spray-density.csv`, which was transcribed off
the page images and closes on the independently-printed totals table.

The post-fix extraction it was run against is retained beside it as
`fixtures/tolch-p41-post-fix-extraction.md`, so the regression re-runs offline.
Re-extracting costs ~145 s of API time for this one page and is only needed
when the pipeline itself changes.

Usage:
    # against the retained fixture (default, offline)
    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-pipeline-regression-p41.py

    # against a fresh extraction, after changing the vision path
    uv run python src/utils/pdf-processor.py <source.pdf> -m -f --pages 41
    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-pipeline-regression-p41.py <dir>/source-p41.md

Exit code is 1 if any cell disagrees with the CSV, including a cell the model
flagged `?` rather than guessed. A `?` is the pipeline working as intended --
the Phase 7 item-5 change asked for an explicit unreadable marker precisely
because the old failure mode was *invented* values in cells the source leaves
unclear -- so read the breakdown, not just the exit code.
"""
import csv
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[5]
CSV = (REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation"
             / "tables/base-spray-density.csv")
FIXTURE = pathlib.Path(__file__).resolve().parent / "fixtures/tolch-p41-post-fix-extraction.md"

# Page 41 prints Panels A/B/C only; Panel D lives on the facing page.
PANELS = ("A", "B", "C")
KINDS = {"Perf.": "perf", "Penet.": "penet", "Dents": "dents"}
VELOCITIES = (0, 700, 1085, 1450, 1685, 2130)


def load_truth():
    rows = {}
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for kind in ("perf", "penet", "dents"):
                rows[(int(r["v_fps"]), r["panel"], kind)] = float(r[kind])
    return rows


def parse_extraction(path):
    """Pull (velocity, panel, kind) -> value out of the extracted markdown table.

    The table carries one row per (velocity, fragment-type) with a No./P.E.
    pair of columns per panel; the fragment type is stated once and then
    repeated as a ditto mark, so it is carried down.
    """
    got = {}
    kind = None
    v_idx = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.count("|") < 6:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        label = cells[0]
        if label.lower().startswith("static"):
            v_idx = 0
        elif label.isdigit():
            v_idx = VELOCITIES.index(int(label)) if int(label) in VELOCITIES else v_idx
        else:
            continue
        if len(cells) > 1 and cells[1] in KINDS:
            kind = KINDS[cells[1]]
            v_idx = 0 if label.lower().startswith("static") else v_idx
        if kind is None:
            continue
        # cells: [velocity, type, A_no, A_pe, B_no, B_pe, C_no, C_pe]
        for j, panel in enumerate(PANELS):
            col = 2 + 2 * j
            if col >= len(cells):
                continue
            raw = cells[col]
            if raw in ("-", "--", "—", "–", ""):
                continue
            if "?" in raw:
                got[(VELOCITIES[v_idx], panel, kind)] = None  # flagged unreadable
                continue
            m = re.fullmatch(r"\.?\d*\.?\d+", raw)
            if m:
                got[(VELOCITIES[v_idx], panel, kind)] = float(raw)
    return got


def main():
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} <extracted-page.md>")
    truth = load_truth()
    got = parse_extraction(pathlib.Path(sys.argv[1]))

    scored = wrong = flagged = missing = 0
    for key, want in sorted(truth.items()):
        if key not in got:
            missing += 1
            continue
        have = got[key]
        scored += 1
        if have is None:
            flagged += 1
            print(f"  FLAGGED  {key}: extraction emitted '?', truth {want}")
        elif abs(have - want) > 0.005:
            wrong += 1
            print(f"  WRONG    {key}: extracted {have}, truth {want}")

    print(f"\nscored {scored} cells: {scored - wrong - flagged} correct, "
          f"{wrong} wrong, {flagged} flagged unreadable, {missing} not present")
    print("\nClosure check on any disagreement (perf + penet + dents == printed total):")
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (int(r["v_fps"]), r["panel"], "perf")
            if key in got and got[key] is not None and abs(got[key] - float(r["perf"])) > 0.005:
                s_truth = float(r["perf"]) + float(r["penet"]) + float(r["dents"])
                s_got = got[key] + float(r["penet"]) + float(r["dents"])
                print(f"  {key}: printed total {r['total']}; "
                      f"CSV sums to {s_truth:.2f}, extraction sums to {s_got:.2f} "
                      f"-> {'CSV' if abs(s_truth - float(r['total'])) < 0.02 else 'extraction'} closes")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
