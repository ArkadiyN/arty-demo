"""Close Mott & Linfoot (1943), A.C. 3348, against itself on its two numeric claims.

Consumer: doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/card.md
and experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 18.

The report was supplied as a poor-quality scan whose embedded OCR layer is
unusable, so every digit here was read off a 400 dpi render of the page rather
than off a text layer.  These closures are what makes that visual reading
admissible under .claude/rules/source-data-fidelity.md: each is arithmetic
internal to the report, built from the report's own stated definitions.

  C1  THE DISTRIBUTION FIT (passes).  Report p.3 tabulates observed and
      calculated fragment counts in six weight bins for a 3.7 in. A.A. shell
      and a 3 in. U.P.  The calculated column is eq. (4),
      N(m) dm = C exp(-M/M_0) dM  with  M = m^(1/3), at the M_0 the page
      prints (0.33 and 0.15 oz^(1/3)).  Integrating over a bin gives
      K * [exp(-M_lo/M_0) - exp(-M_hi/M_0)] with K = C*M_0, one constant for
      the whole column -- so calc_i divided by that bracket must be the SAME
      number on every row.  For the shell it is, to +-2%.

      That is a per-digit check on a hand-read table: a misread digit, or a
      misread bin boundary, moves its row's K off the others immediately.
      (Read "1/2 - 4" as "1/2 - 1" and the row predicts 92, not the printed
      181.)  The U.P. column is looser because its M_0 is printed to two
      significant figures and the fit is far more sensitive to M_0 there --
      the residual is rounding in the source, not transcription, and the
      independent sum closure below confirms the U.P. digits regardless.

  C2  THE FITTED TOTALS (passes).  C is fitted, so the calculated column must
      carry the same total as the observed one.  Both pairs do, exactly:
      782 = 782 for the shell, 1478 = 1478 for the U.P.  This closes the two
      columns against each other with no free parameter at all.

  C3  THE MEAN-SIZE WORKED EXAMPLE (reproduces to 4%).  Report pp.1-2 derives
      a = (24 r^2 W / rho V^2)^(1/3) as the largest surviving fragment breadth
      (eq. 2), takes W = 70 ft.lb/sq.in. (the lower Southwell impact value),
      r = 2.2 in. and V = 2500 ft/sec, and concludes a = 0.55 in.  Recomputed
      it is 0.529 in.  Since a goes as (W/rho)^(1/3), 4% in a is 12% in W/rho
      -- consistent with Mott's own "our value will be very approximate", and
      well inside it.  Pinned at 5% so a future digit change fails loudly.

Nothing in src/arty consumes this report's numbers.  It is retained because it
is the primary behind Gold (2017)'s Mott-1943 attributions -- see the card and
ledger sect. 18 for what it does and does not support.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-closures.py
"""

import csv
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation"
TABLE = DOC / "tables/section2-fragment-weight-distribution.csv"

# p.3, "M_0 has respectively the values (in (ounces)1/3)".
M0 = {"shell": 0.33, "up": 0.15}

# p.1-2, anchor "For r we take 2.2 inches".
R_IN = 2.2  # casing radius at rupture [in]
V_FPS = 2500.0  # fragment velocity [ft/s]
W_FTLB_PER_IN2 = 70.0  # rupture energy per unit area, the lower Southwell value
RHO_LB_PER_IN3 = 0.283  # steel [lb/in^3]
PAGE_A_IN = 0.55  # "= 0.55 inches, in good agreement with the observed value"

# Pinned residuals. A re-read that moves a digit moves these.
EXPECTED_TOTALS = {"shell": 782.0, "up": 1478.0}
MAX_K_SPREAD = {"shell": 0.05, "up": 0.35}  # see C1 on why the U.P. is loose
A_TOL = 0.05  # C3 reproduces the page to 4%; fail at 5%


def _f(text):
    """Return the cell as a float, or None when the source leaves it blank."""
    text = (text or "").strip()
    return float(text) if text else None


def bin_fraction(lo, hi, m0):
    """Return the eq.-(4) probability mass in [lo, hi] oz; hi None = open bin."""
    a = math.exp(-(lo ** (1 / 3)) / m0)
    b = 0.0 if hi is None else math.exp(-(hi ** (1 / 3)) / m0)
    return a - b


def main():
    failures = []
    with TABLE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    # -- C1 the distribution fit -------------------------------------------
    for name in ("shell", "up"):
        m0 = M0[name]
        print(f"C1  {name}: eq. (4) with M_0 = {m0} oz^(1/3)")
        print(f"    {'bin (oz)':>14s} {'frac':>9s} {'calc':>6s} {'K=calc/frac':>12s}")
        ks = []
        for r in rows:
            lo, hi = _f(r["bin_lo_oz"]), _f(r["bin_hi_oz"])
            calc = _f(r[f"{name}_calc"])
            frac = bin_fraction(lo, hi, m0)
            label = f"{lo:g} - {hi:g}" if hi else f"> {lo:g}"
            if calc is None or calc == 0:
                print(f"    {label:>14s} {frac:9.6f} {'-':>6s} {'-':>12s}")
                continue
            k = calc / frac
            ks.append(k)
            print(f"    {label:>14s} {frac:9.6f} {calc:6.0f} {k:12.1f}")
        spread = max(ks) / min(ks) - 1
        kbar = sum(ks) / len(ks)
        pred = [round(kbar * bin_fraction(_f(r["bin_lo_oz"]), _f(r["bin_hi_oz"]), m0)) for r in rows]
        print(f"    K spread across rows = {spread * 100:+.1f}%  (mean {kbar:.0f})")
        print(f"    column regenerated from the mean K: {pred}")
        if spread > MAX_K_SPREAD[name]:
            failures.append(
                f"C1 {name}: K spread {spread * 100:.1f}% exceeds "
                f"{MAX_K_SPREAD[name] * 100:.0f}% -- a digit or a bin edge has moved"
            )
        print()

    # -- C2 the fitted totals ----------------------------------------------
    for name in ("shell", "up"):
        s_obs = sum(_f(r[f"{name}_obs"]) or 0.0 for r in rows)
        s_cal = sum(_f(r[f"{name}_calc"]) or 0.0 for r in rows)
        print(f"C2  {name}: sum(obs) = {s_obs:.0f}   sum(calc) = {s_cal:.0f}")
        if s_obs != s_cal:
            failures.append(f"C2 {name}: obs total {s_obs:.0f} != calc total {s_cal:.0f}")
        if s_obs != EXPECTED_TOTALS[name]:
            failures.append(
                f"C2 {name}: total moved to {s_obs:.0f}, recorded {EXPECTED_TOTALS[name]:.0f}"
            )

    # -- C3 the mean-size worked example -----------------------------------
    w = W_FTLB_PER_IN2 * 12.0  # ft.lbf/in^2 -> in.lbf/in^2 = lbf/in
    v = V_FPS * 12.0  # in/s
    rho = RHO_LB_PER_IN3 / 386.088  # lb/in^3 -> lbf.s^2/in^4
    a = (24 * R_IN**2 * w / (rho * v**2)) ** (1 / 3)
    err = a / PAGE_A_IN - 1
    print()
    print(f"C3  a = (24 r^2 W / rho V^2)^(1/3) = {a:.4f} in.  (page: {PAGE_A_IN})")
    print(f"    {err * 100:+.1f}% vs the page; a ~ (W/rho)^(1/3), so that is "
          f"{((1 + err) ** 3 - 1) * 100:+.0f}% in W/rho")
    if abs(err) > A_TOL:
        failures.append(f"C3: recomputed a = {a:.4f} in., page states {PAGE_A_IN}")

    print()
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
