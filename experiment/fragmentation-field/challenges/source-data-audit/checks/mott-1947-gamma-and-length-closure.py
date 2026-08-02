"""Close Mott (1947) against itself on the two facts src/arty takes from it.

Consumer: doc-reference/fragmentation/gurney-equations-fragmentation/card.md and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 17.

Three closures, of which one passes and two do not. All three are arithmetic
internal to the paper, built from the paper's own stated definitions -- the
form .claude/rules/source-data-fidelity.md asks for.

  C1  WORKED EXAMPLE (passes).  p.306 sets up a 3 in. bomb, states
      x0 = 1.6/sqrt(gamma) in., and concludes "if gamma ~ 100, the average
      fragment length is about 0.24 in."  p.305 finding (1) states the average
      fragment length is 1.5 x0.  Those three numbers close on each other:
      1.5 * 1.6/sqrt(100) = 0.24 exactly.

      This is the closure that matters most, because it validates the shipped
      constant.  src/arty/fragmentation.py takes kappa_x = 1.5 from finding
      (1); C1 shows that 1.5 is the same 1.5 Mott used to get his own printed
      answer, rather than a number read off an adjacent sentence.

  C2  THE GAMMA COLUMN (fails).  p.308 states gamma ~ 160 P_2/P_F(1+s_F) and
      then tabulates P_2, P_F and reduction in area against gamma for four
      materials.  The formula does not reproduce the column under either
      reading of s_F -- see the printout.  Digits are confirmed against the
      page at 420 dpi, so this is not a transcription defect.

  C3  MILD-STEEL LENGTH (fails).  p.308: "For mild steel, then, according to
      the formulae of sect. 2, a bomb of the design suggested there would give
      fragments of average length 0.6 in."  Same bomb as C1, so
      1.5 * 1.6/sqrt(gamma) = 0.6 implies gamma = 16 -- below the iron row (20)
      and far below any steel row.  Nothing in this repo consumes the 0.6 in.

C2 and C3 are pinned as expected residuals rather than left to fail: the point
of retaining them is that a future re-extraction which moves a digit moves the
residual too, and the script then fails loudly.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py
"""

import csv
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/gurney-equations-fragmentation"
TABLE = DOC / "tables/section3-gamma-vs-composition.csv"

sys.path.insert(0, str(ROOT / "src"))

# p.306, anchor "As a numerical example". Both are quoted on the page.
X0_COEFF_IN = 1.6  # x0 = 1.6/sqrt(gamma), inches
WORKED_GAMMA = 100.0  # "Thus if gamma ~ 100"
WORKED_LENGTH_IN = 0.24  # "the average fragment length is about 0.24 in."

# p.308, anchor "For mild steel, then, according to the formulae".
MILD_STEEL_LENGTH_IN = 0.6

# p.308, two lines above the table, anchor "Some values of".
GAMMA_COEFF = 160.0

# Pinned residuals for C2/C3. Recomputed below; a digit change breaks these.
EXPECTED_C2_RA = [55.0, 56.5, 55.2, 47.2]
EXPECTED_C2_LN = [36.3, 43.6, 45.1, 40.2]
EXPECTED_C3_GAMMA = 16.0


def main():
    failures = []

    with TABLE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    # -- C1 worked example ------------------------------------------------
    from arty.fragmentation import _MOTT_BREADTH_FACTOR as kappa_x

    x0 = X0_COEFF_IN / math.sqrt(WORKED_GAMMA)
    length = kappa_x * x0
    print(f"C1  x0 = {X0_COEFF_IN}/sqrt({WORKED_GAMMA:.0f}) = {x0:.4f} in.")
    print(f"C1  kappa_x (src/arty) = {kappa_x}")
    print(f"C1  {kappa_x} * {x0:.4f} = {length:.4f} in.  (page: {WORKED_LENGTH_IN})")
    if abs(length - WORKED_LENGTH_IN) > 5e-3:
        failures.append(
            f"C1: 1.5*1.6/sqrt(100) = {length:.4f}, page states {WORKED_LENGTH_IN}"
        )

    # -- C2 the gamma column ----------------------------------------------
    print()
    print("C2  gamma ~ 160 P_2 / P_F (1 + s_F), against the printed column:")
    print(f"    {'material':13s} {'printed':>8s} {'s_F=RA':>8s} {'s_F=ln':>8s}")
    got_ra, got_ln = [], []
    for r in rows:
        ra = float(r["reduction_in_area"])
        pf = float(r["P_F_kg_per_mm2"])
        p2 = float(r["P_2_kg_per_mm2"])
        g = float(r["gamma"])
        a = GAMMA_COEFF * p2 / (pf * (1 + ra))
        b = GAMMA_COEFF * p2 / (pf * (1 + math.log(1 / (1 - ra))))
        got_ra.append(round(a, 1))
        got_ln.append(round(b, 1))
        print(f"    {r['material']:13s} {g:8.0f} {a:8.1f} {b:8.1f}")

    if got_ra != EXPECTED_C2_RA:
        failures.append(f"C2: s_F=RA residuals moved: {got_ra} != {EXPECTED_C2_RA}")
    if got_ln != EXPECTED_C2_LN:
        failures.append(f"C2: s_F=ln residuals moved: {got_ln} != {EXPECTED_C2_LN}")

    printed = [float(r["gamma"]) for r in rows]
    span_printed = max(printed) / min(printed)
    span_ra = max(got_ra) / min(got_ra)
    print(
        f"    printed column spans x{span_printed:.2f}; "
        f"the formula spans x{span_ra:.2f} -- it does not reproduce the trend."
    )
    if span_ra > 1.5:
        failures.append(
            "C2: the formula now spans >1.5x; the recorded finding assumed it was flat"
        )

    # -- C3 mild-steel length ---------------------------------------------
    print()
    implied = (kappa_x * X0_COEFF_IN / MILD_STEEL_LENGTH_IN) ** 2
    lo = min(printed)
    print(
        f"C3  average length {MILD_STEEL_LENGTH_IN} in. implies gamma = "
        f"{implied:.1f}; lowest tabulated gamma is {lo:.0f} (iron)."
    )
    if abs(implied - EXPECTED_C3_GAMMA) > 0.5:
        failures.append(f"C3: implied gamma moved to {implied:.1f}")
    if implied >= lo:
        failures.append(
            f"C3: implied gamma {implied:.1f} is no longer below the table; "
            "the recorded finding assumed it was"
        )

    print()
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    print(
        "NOTE: C2 and C3 are known non-closures in the 1947 paper, pinned here, "
        "not defects introduced by this repo. See ledger sect. 17."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
