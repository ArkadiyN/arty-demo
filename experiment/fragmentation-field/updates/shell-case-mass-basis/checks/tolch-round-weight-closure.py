"""Closure + derived case-metal mass for Tolch 1938's four-round weight table.

Consumer: experiment/fragmentation-field/updates/shell-case-mass-basis/derivation.md
sections 2 and 3 (the 10.94 lb / 4.9623 kg case-metal basis for the 75mm M48
registry row, and the 14.85 lb / 1.56 lb / 2.35 lb triple that Option B writes
into src/arty/shells.py).

Two things happen here that the .invariant DSL cannot express on its own:

  1. it re-runs the declared row closure
     (loaded_unfuzed - tnt + fuze == empty_and_fuze) via the shared checker, so
     this script is the single command that reproduces derivation.md sect. 2;
  2. it derives case metal = loaded_unfuzed - tnt per round, which is NOT a
     transcribed column and therefore must not live in the CSV.

Run:  uv run python experiment/fragmentation-field/updates/shell-case-mass-basis/checks/tolch-round-weight-closure.py
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
TABLES = (
    REPO
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)
CSV_PATH = TABLES / "round-weights.csv"
INV_PATH = TABLES / "round-weights.invariant"

LB_TO_KG = 0.45359237  # exact, NIST


def main() -> int:
    rc = subprocess.run(
        [sys.executable, str(REPO / "src/utils/check-table-invariants.py"), str(INV_PATH)],
        cwd=REPO,
    ).returncode

    with CSV_PATH.open() as fh:
        rows = [{k: v for k, v in r.items()} for r in csv.DictReader(fh)]

    print("\nDerived case metal (= loaded unfuzed - TNT; NOT a source column)")
    print(f"{'rd':>3} {'loaded':>8} {'TNT':>6} {'fuze':>6} "
          f"{'case_lb':>8} {'case_kg':>8} {'fuzed_lb':>9} {'C/M':>7}")
    case_kg = []
    for r in rows:
        loaded = float(r["loaded_unfuzed_lb"])
        tnt = float(r["tnt_lb"])
        fuze = float(r["fuze_lb"])
        case = loaded - tnt
        case_kg.append(case * LB_TO_KG)
        print(f"{r['round']:>3} {loaded:8.2f} {tnt:6.2f} {fuze:6.2f} "
              f"{case:8.2f} {case*LB_TO_KG:8.4f} {loaded+fuze:9.2f} {tnt/case:7.4f}")

    lo, hi = min(case_kg), max(case_kg)
    spread = (hi - lo) / (sum(case_kg) / len(case_kg))
    print(f"\nlot spread on case metal: {100*spread:.2f} %  "
          f"(derivation.md sect. 6 assumption: < 5 % => round 1/2 nominal is fine)")
    if spread >= 0.05:
        print("FAIL: lot spread exceeds the 5 % fidelity bar")
        rc |= 1

    # Round 1/2 is the modal round and the nominal the registry is rebased on.
    nominal_case = (12.50 - 1.56) * LB_TO_KG
    print(f"\nNOMINAL (rd 1/2): case metal = {nominal_case:.4f} kg  "
          f"total fuzed = {14.85*LB_TO_KG:.4f} kg  "
          f"TNT = {1.56*LB_TO_KG:.5f} kg  fuze = {2.35*LB_TO_KG:.5f} kg")

    # The "empty shell & fuze" trap: 13.29 lb is NOT case metal.
    empty_and_fuze_kg = 13.29 * LB_TO_KG
    print(f"NOT case metal: empty shell & fuze = {empty_and_fuze_kg:.4f} kg "
          f"({100*(empty_and_fuze_kg/nominal_case - 1):.1f} % above case metal)")

    print("\nOK" if rc == 0 else "\nFAILED")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
