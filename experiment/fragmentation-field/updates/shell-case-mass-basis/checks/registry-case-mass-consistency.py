"""Registry mass-basis self-consistency + before/after V0, mu, N0 for all shells.

Consumer: experiment/fragmentation-field/updates/shell-case-mass-basis/derivation.md
sections 4 (self-consistency + unit/limit checks) and 5 (sensitivity: what the
75mm rebase actually does to N0).

Checks, for every row of arty.shells.SHELLS:
  (a) M_case = mass_total - mass_filler - mass_deductions > 0;
  (b) mass_deductions < mass_total - mass_filler  (same thing, stated as the
      physical requirement that inert deductions cannot exceed the case);
  (c) C/M = mass_filler / M_case lies in the 0.10-0.25 band normal for a
      WW2 thick-walled HE shell (a fragmentation shell, not a blast bomb);
  (d) for the 75mm M48 only, M_case agrees with Tolch's directly-stated case
      metal (round-weights.csv, loaded_unfuzed - TNT) to within 0.5 %.

Then it prints the Option-B rebase (derivation.md sect. 3) side by side with the
shipped row so the N0 shift is visible and attributable. Note (d) is the check
that FAILS on the shipped registry -- that failure is the finding this update
closes, so run this before and after the src/ pass.

Run:  uv run python experiment/fragmentation-field/updates/shell-case-mass-basis/checks/registry-case-mass-consistency.py
"""

from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path

from arty.fragmentation import gurney_velocity, mott_params
from arty.shells import SHELLS

REPO = Path(__file__).resolve().parents[5]
CSV_PATH = (
    REPO
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation"
    / "tables/round-weights.csv"
)
LB_TO_KG = 0.45359237

CM_LO, CM_HI = 0.10, 0.25
TOLCH_TOL = 0.005  # 0.5 % against a directly-stated case weight


def tolch_nominal_kg() -> dict[str, float]:
    """Round 1/2 (modal) weights from the source CSV, in kg. Never hand-typed."""
    with CSV_PATH.open() as fh:
        rows = list(csv.DictReader(fh))
    r = next(x for x in rows if x["round"] == "1")
    loaded = float(r["loaded_unfuzed_lb"])
    tnt = float(r["tnt_lb"])
    fuze = float(r["fuze_lb"])
    return {
        "mass_total": (loaded + fuze) * LB_TO_KG,   # complete fuzed round
        "mass_filler": tnt * LB_TO_KG,
        "mass_deductions": fuze * LB_TO_KG,
        "case": (loaded - tnt) * LB_TO_KG,
    }


def report(name, shell):
    m_case = shell.mass_total - shell.mass_filler - shell.mass_deductions
    cm = shell.mass_filler / m_case
    v0 = gurney_velocity(shell)
    mu, n0 = mott_params(shell, v0)
    print(f"{name:<16} M_case={m_case:8.4f} kg  C/M={cm:6.4f}  "
          f"V0={v0:7.1f} m/s  mu={mu*1e6:8.2f} mg  N0={n0:8.1f}")
    return m_case, cm, v0, mu, n0


def main() -> int:
    fails: list[str] = []
    tol = tolch_nominal_kg()

    print("=== (a)-(c) registry self-consistency, as shipped ===")
    shipped = {}
    for name, shell in SHELLS.items():
        m_case, cm, *_ = shipped.setdefault(name, report(name, shell))
        if m_case <= 0:
            fails.append(f"(a) {name}: M_case = {m_case:.4f} kg is not positive")
        if shell.mass_deductions >= shell.mass_total - shell.mass_filler:
            fails.append(f"(b) {name}: deductions exceed the case")
        if not (CM_LO <= cm <= CM_HI):
            fails.append(f"(c) {name}: C/M = {cm:.4f} outside [{CM_LO}, {CM_HI}]")

    print("\n=== (d) 75mm M48 against Tolch's directly-stated case metal ===")
    name = "75mm M48 HE"
    m_case_shipped = shipped[name][0]
    err = m_case_shipped / tol["case"] - 1.0
    print(f"Tolch case metal  = {tol['case']:.4f} kg  "
          f"(round-weights.csv rd 1: {12.50 - 1.56:.2f} lb)")
    print(f"shipped M_case    = {m_case_shipped:.4f} kg   error = {100*err:+.1f} %")
    if abs(err) > TOLCH_TOL:
        fails.append(
            f"(d) {name}: M_case {m_case_shipped:.4f} kg is {100*err:+.1f} % off "
            f"Tolch's {tol['case']:.4f} kg (tolerance {100*TOLCH_TOL:.1f} %)"
        )

    print("\n=== Option-B rebase of the 75mm row (derivation.md sect. 3) ===")
    rebased = replace(
        SHELLS[name],
        mass_total=tol["mass_total"],
        mass_filler=tol["mass_filler"],
        mass_deductions=tol["mass_deductions"],
    )
    print(f"  proposed: mass_total={tol['mass_total']:.4f}  "
          f"mass_filler={tol['mass_filler']:.5f}  "
          f"mass_deductions={tol['mass_deductions']:.5f}")
    before = shipped[name]
    after = report("  AFTER rebase", rebased)
    err_after = after[0] / tol["case"] - 1.0
    print(f"  M_case error after rebase = {100*err_after:+.4f} %  "
          f"(exact by construction)")
    lbl = ("M_case", "C/M", "V0", "mu", "N0")
    print("  deltas: " + "  ".join(
        f"{k} {100*(a/b - 1):+.1f} %" for k, b, a in zip(lbl, before, after)))
    if abs(err_after) > 1e-9:
        fails.append("Option-B rebase does not reproduce Tolch's case metal exactly")

    print("\n=== sensitivity: analytic eq. (6) vs finite difference (derivation.md sect. 5) ===")
    print("N0 ~ C*M_case/(M_case + C/2)  =>  dlnN0/dlnM = (C/M)/(2 + C/M)")
    print(f"{'shell':<16} {'C/M':>7} {'analytic':>9} {'numeric':>9} {'dlnN0/dlnC':>11}")
    for name, shell in list(SHELLS.items()) + [("75mm rebased", rebased)]:
        m_case = shell.mass_total - shell.mass_filler - shell.mass_deductions
        cm = shell.mass_filler / m_case
        analytic_m = cm / (2.0 + cm)
        analytic_c = 2.0 / (2.0 + cm)
        # finite difference in M_case, applied through mass_deductions so that
        # mass_filler (and hence C) is held fixed -- this is exactly the
        # perturbation an error in `mass_deductions` represents.
        h = 0.01
        n0s = []
        for sgn in (-1.0, +1.0):
            pert = replace(shell, mass_deductions=shell.mass_deductions - sgn * h * m_case)
            v = gurney_velocity(pert)
            n0s.append(mott_params(pert, v)[1])
        numeric_m = (n0s[1] - n0s[0]) / (2.0 * h) / mott_params(shell, gurney_velocity(shell))[1]
        print(f"{name:<16} {cm:7.4f} {analytic_m:9.4f} {numeric_m:9.4f} {analytic_c:11.4f}")
        if abs(numeric_m - analytic_m) > 0.01:
            fails.append(
                f"sensitivity {name}: analytic {analytic_m:.4f} vs numeric {numeric_m:.4f} "
                "-- eq. (6) does not describe the shipped chain"
            )

    print()
    if fails:
        print("FAILURES (expected on the shipped registry; must be empty after the src/ pass):")
        for f in fails:
            print("  -", f)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
