"""Test which reading of s_f reproduces Mott 1947 p.308's printed gamma column.

Consumer: experiment/fragmentation-field/updates/mott-fragment-shape-closure/
rebaseline-verdict.md (the gamma-column non-closure rebaseline).

The recorded finding (OPEN-FINDINGS.md, "gamma = 47 and gamma = 65 both
interpolate...") asserts that gamma ~ 160 P_y/P_f(1+s_f) "is flat (spans x1.20)
where the printed column rises x3.35".  That statement is reading-dependent:
the paper tabulates *reduction in area*, not s_f, so the closure has a free
choice of how RA maps to s_f.  This script sweeps the four candidate mappings
and reports the residual per row.

Page anchors (doc-reference/fragmentation/gurney-equations-fragmentation/
rspa.1947.0042.md, p.308 = source.pdf p.9):
  "Some values of"                          -- the table
  "For mild steel, then, according to"      -- the sentence after it
  "Thus a material with a high-stress"      -- Mott's own trend statement

Series read from the extracted-once CSV, never hand-typed.

    uv run python experiment/fragmentation-field/updates/\
mott-fragment-shape-closure/checks/mott-1947-gamma-column-strain-reading.py
"""

import csv
import math
import pathlib

REL = (
    "doc-reference/fragmentation/gurney-equations-fragmentation"
    "/tables/section3-gamma-vs-composition.csv"
)
ROOT = next(
    p for p in pathlib.Path(__file__).resolve().parents if (p / REL).exists()
)
TABLE = ROOT / REL

COEFF = 160.0  # p.308, "gamma ~ 160 P_y / P_f(1+s_f)"

# Candidate readings of the denominator factor D that stands for (1+s_f),
# built from the tabulated reduction in area RA.  Constant-volume necking gives
# l_f/l_0 = 1/(1-RA), hence engineering strain s_f = RA/(1-RA) and true strain
# s_f = ln(1/(1-RA)).
READINGS = {
    "D = 1+RA          (s_f read as RA itself)": lambda ra: 1.0 + ra,
    "D = 1+ln(1/(1-RA)) (s_f = true strain)": lambda ra: 1.0 + math.log(1.0 / (1.0 - ra)),
    "D = 1/(1-RA)       (s_f = engineering strain, 1+s_f)": lambda ra: 1.0 / (1.0 - ra),
    "D = RA/(1-RA)      (s_f = engineering strain, no +1)": lambda ra: ra / (1.0 - ra),
}


def main():
    with TABLE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    ra = [float(r["reduction_in_area"]) for r in rows]
    pf = [float(r["P_F_kg_per_mm2"]) for r in rows]
    py = [float(r["P_2_kg_per_mm2"]) for r in rows]  # the page's P_y column
    gp = [float(r["gamma"]) for r in rows]
    names = [r["material"] for r in rows]

    print(f"printed gamma column: {gp}  (spans x{max(gp)/min(gp):.2f})")
    print()
    best = None
    for label, D in READINGS.items():
        got = [COEFF * py[i] / (pf[i] * D(ra[i])) for i in range(len(rows))]
        err = [100.0 * (got[i] - gp[i]) / gp[i] for i in range(len(rows))]
        worst3 = max(abs(e) for e in err[:3])
        print(f"{label}")
        print(f"    {'material':13s} {'printed':>8s} {'formula':>8s} {'err %':>8s}")
        for i in range(len(rows)):
            print(f"    {names[i]:13s} {gp[i]:8.0f} {got[i]:8.1f} {err[i]:+8.1f}")
        print(
            f"    span x{max(got)/min(got):.2f}; "
            f"worst error on rows 1-3 = {worst3:.1f} %"
        )
        print()
        if best is None or worst3 < best[1]:
            best = (label, worst3, got, err)

    assert best is not None, "READINGS is empty -- no candidate to rank"
    label, worst3, got, err = best
    print(f"BEST READING: {label}")
    print(f"  rows 1-3 (iron, 0.1C, 0.25C) close to within {worst3:.1f} %")
    print(f"  row 4 (0.45C) residual {err[3]:+.1f} % -- formula {got[3]:.1f} vs printed {gp[3]:.0f}")

    # Row 4 is also the row where the tabulated P_y breaks its own monotone rise.
    print()
    print(f"  tabulated P_y column: {py} -- rises then drops at 0.45C")
    py4 = gp[3] * pf[3] * (ra[3] / (1 - ra[3])) / COEFF
    print(
        f"  P_y that WOULD reproduce the printed 67 under the best reading: "
        f"{py4:.1f} (printed 38)"
    )

    # Mott's own trend statement, p.308 anchor "Thus a material with a
    # high-stress": average fragment length is proportional to
    # P_f*sqrt((1+s_f)/(rho*P_y)).  Check whether the printed gamma column and
    # this proportionality rank the four materials the same way.
    print()
    print("  Mott's stated length proportionality vs the printed column:")
    print(f"    {'material':13s} {'L~Pf*sqrt((1+sf)/Py)':>22s} {'L~sqrt(Pf/gamma)':>18s}")
    for i in range(len(rows)):
        sf = ra[i] / (1 - ra[i])
        l_prop = pf[i] * math.sqrt((1.0 + sf) / py[i])
        l_gamma = math.sqrt(pf[i] / gp[i])
        print(f"    {names[i]:13s} {l_prop:22.3f} {l_gamma:18.3f}")
    print(
        "    (both should fall monotonically with carbon if the column is "
        "consistent with the paper's own trend statement)"
    )

    # What the interpolation rule the registry uses gets from each segment.
    print()
    print("  carbon interpolation of the printed column (the registry's rule):")
    for c in (0.17, 0.355):
        for j in range(len(rows) - 1):
            c0 = float(rows[j]["carbon_pct"])
            c1 = float(rows[j + 1]["carbon_pct"])
            if c0 <= c <= c1:
                g = gp[j] + (gp[j + 1] - gp[j]) * (c - c0) / (c1 - c0)
                g_alt = got[j] + (got[j + 1] - got[j]) * (c - c0) / (c1 - c0)
                print(
                    f"    {c:.3f} %C in [{c0}, {c1}]: printed-column gamma = "
                    f"{g:.1f}; best-reading-recomputed gamma = {g_alt:.1f}"
                )

    # ---- downstream exposure of the shape closure -----------------------
    # alpha, mu and N(>0.5 g) below are this repo's own numbers, transcribed
    # from updates/mott-fragment-shape-closure/derivation.md sect. 7.3/7.4/7.5
    # (not source data).  The closure gives gamma = alpha^(-2/3)*gamma_prime
    # and mu ∝ gamma_prime^(-1), so a rebaselined gamma_prime propagates
    # analytically -- no re-run of src/arty needed, and none is made here.
    print()
    print("  exposure of the shape closure to a rebaselined gamma_prime:")
    G_SHIPPED = 65.0  # SteelParams "WW2 US HE Shell"
    shells = [  # name, alpha, gamma(7.4), mu_new g (7.4), N(>0.5 g) (7.4), OptionC mu g (7.5)
        ("75 mm M48", 3.38, 28.9, 0.793, 1640, 1.155),
        ("105 mm M1", 4.66, 23.3, 1.538, 2213, 2.974),
        ("155 mm M107", 5.15, 21.8, 4.738, 2648, 8.057),
    ]
    for g_new, why in ((55.9, "recomputed 0.45C row"), (54.5, "0.355 %C on recomputed column")):
        k = G_SHIPPED / g_new  # mu multiplier, since mu ∝ 1/gamma_prime
        print(f"    gamma_prime {G_SHIPPED:.0f} -> {g_new:.1f} ({why}): mu x{k:.3f}")
        print(
            f"      {'shell':12s} {'gamma':>7s} {'mu (g)':>8s} "
            f"{'N(>0.5g)':>9s} {'A/C':>6s}"
        )
        for name, alpha, gam, mu, n05, muc in shells:
            gam2 = gam * g_new / G_SHIPPED
            mu2 = mu * k
            n2 = n05 * (1 / k) * math.exp(-math.sqrt(0.5 / mu2)) / math.exp(
                -math.sqrt(0.5 / mu)
            )
            print(
                f"      {name:12s} {gam2:7.1f} {mu2:8.3f} {n2:9.0f} {mu2/muc:6.2f}"
            )
        print(
            "      (shipped: gamma 21.8-28.9, mu 0.793-4.738, N 1640-2648, "
            "A/C 0.52-0.69)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
