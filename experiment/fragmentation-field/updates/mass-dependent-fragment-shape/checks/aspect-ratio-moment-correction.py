"""Derive the aspect-ratio moment correction c = <A x^2> / (<A><x^2>).

Consumer: every number in section 3 (and the sensitivity table in section 3.4) of
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/derivation.md

Data: Felix, Colwill & Harris (2022) Table 3, transcribed once at
doc-reference/fragmentation/explosion-fragment-model/tables/
table-3-grady-aspect-ratio-counts.csv -- counts of Fig. 10 fragments by
aspect-ratio bin and by the authors' five size Groups.  The Group grain-mass
ranges are printed on the figure itself
(doc-reference/fragmentation/explosion-fragment-model/images/fig10.jpeg).

Closure identity used (mott-fragment-shape-closure/derivation.md eq. G4):
    m = rho * l * x * t0 = rho * t0 * A * x^2       with l = A x
so, at fixed rho t0,
    x^2 = m / (rho t0 A)     =>     <A x^2> = <m>/(rho t0)
and therefore
    c = <A x^2> / (<A> <x^2>) = <m> / ( <A> * <m/A> ).
All expectations are count-weighted over the 2415 tabulated fragments.
c > 1 iff A and m are positively associated (Chebyshev's sum inequality).

Run: uv run python experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks/aspect-ratio-moment-correction.py
"""

import csv
import itertools
import pathlib

CSV = (
    pathlib.Path(__file__).resolve().parents[5]
    / "doc-reference/fragmentation/explosion-fragment-model/tables"
    / "table-3-grady-aspect-ratio-counts.csv"
)

# Aspect-ratio bin representatives.  1:1, 1:2, 1:3 are closed bins and are read
# at their nominal value.  "1:4+" is open; fig10.jpeg resolves it for Group 4
# only (1:4 = 5, 1:5 = 2 -> 4.29).  Baseline uses 4.0 everywhere (the value the
# scoping pass and the card's caveat both use); A4_HIGH is the sensitivity.
BIN_RATIO = {"n_1to1": 1.0, "n_1to2": 2.0, "n_1to3": 3.0, "n_1to4plus": 4.0}

# Group grain-mass edges, printed on fig10.jpeg.  Group 1's upper edge is an
# ASSUMPTION: the figure literally prints "GROUP NO 1-75 TO 75 GRAINS"; 150 is
# taken from Group 2's own printed lower edge ("150 TO 750").
# Group 4's upper edge is unbounded on the figure; 7500 gr (3x its lower edge,
# matching Group 3's own 750->2500 span ratio) is an ASSUMPTION.
GROUP_EDGES_GR = {
    "Group 0": (0.0, 75.0),
    "Group 1": (75.0, 150.0),
    "Group 2": (150.0, 750.0),
    "Group 3": (750.0, 2500.0),
    "Group 4": (2500.0, 7500.0),
}


def geo_mean(lo, hi, lo_floor):
    """Geometric mean of a mass bin [gr]; a zero lower edge is floored."""
    return ((lo if lo > 0 else lo_floor) * hi) ** 0.5


def moment_c(m_rep, a_open, verbose=False):
    """c = <m> / (<A> <m/A>) over the tabulated fragments.

    m_rep: dict group -> representative grain mass [gr].
    a_open: aspect representative for the open "1:4+" bin [-].
    """
    ratio = dict(BIN_RATIO, n_1to4plus=a_open)
    n_tot = s_m = s_a = s_m_over_a = 0.0
    rows = []
    with CSV.open() as fh:
        for row in csv.DictReader(fh):
            g = row["group"]
            m = m_rep[g]
            n_g = sum(float(row[k]) for k in ratio)
            a_bar = sum(float(row[k]) * ratio[k] for k in ratio) / n_g
            rows.append((g, n_g, m, a_bar))
            for k, a in ratio.items():
                n = float(row[k])
                n_tot += n
                s_m += n * m
                s_a += n * a
                s_m_over_a += n * m / a
    mean_m = s_m / n_tot
    mean_a = s_a / n_tot
    mean_m_over_a = s_m_over_a / n_tot
    c = mean_m / (mean_a * mean_m_over_a)
    if verbose:
        print("  Group     n     m_rep[gr]   A_bar")
        for g, n_g, m, a_bar in rows:
            print(f"  {g:8s} {n_g:6.0f}   {m:8.1f}   {a_bar:.3f}")
        print(f"  N = {n_tot:.0f}   <m> = {mean_m:.2f} gr   <A> = {mean_a:.4f}   "
              f"<m/A> = {mean_m_over_a:.3f} gr")
    return c


def variance_k(m_rep, a_open):
    """A9.1's factor k = <x^2>/<x>^2, from the same table.

    With x^2 = m/(rho t0 A), k = <m/A> / <sqrt(m/A)>^2 -- the rho t0 cancels.
    Only BETWEEN-Group dispersion is resolved (one mass representative per
    Group), so this is a LOWER bound on k.
    """
    ratio = dict(BIN_RATIO, n_1to4plus=a_open)
    n_tot = s_q = s_sq = 0.0
    with CSV.open() as fh:
        for row in csv.DictReader(fh):
            m = m_rep[row["group"]]
            for kk, a in ratio.items():
                n = float(row[kk])
                n_tot += n
                s_q += n * (m / a)
                s_sq += n * (m / a) ** 0.5
    return (s_q / n_tot) / (s_sq / n_tot) ** 2


if __name__ == "__main__":
    base_rep = {
        g: geo_mean(lo, hi, lo_floor=7.5)  # Group 0 floor: 0.1 x its upper edge
        for g, (lo, hi) in GROUP_EDGES_GR.items()
    }
    print("BASELINE -- geometric-mean bin representatives, open aspect bin = 4.0")
    c0 = moment_c(base_rep, 4.0, verbose=True)
    print(f"  => c = {c0:.4f}\n")

    print("SENSITIVITY (c)")
    print("  Group-0 floor [gr] : ", end="")
    for floor in (2.5, 7.5, 20.0, 37.5):
        rep = dict(base_rep, **{"Group 0": geo_mean(0.0, 75.0, floor)})
        print(f"{floor:5.1f}->{moment_c(rep, 4.0):.3f}  ", end="")
    print()

    print("  Group-4 top  [gr]  : ", end="")
    for top in (5000.0, 7500.0, 12500.0, 25000.0):
        rep = dict(base_rep, **{"Group 4": geo_mean(2500.0, top, 0.0)})
        print(f"{top:7.0f}->{moment_c(rep, 4.0):.3f}  ", end="")
    print()

    print("  Open aspect bin    : ", end="")
    for a4 in (4.0, 4.29, 5.0, 6.0):
        print(f"{a4:5.2f}->{moment_c(base_rep, a4):.3f}  ", end="")
    print()

    print("  Group-1 upper edge : ", end="")
    for hi in (150.0, 100.0, 200.0):
        rep = dict(base_rep, **{"Group 1": geo_mean(75.0, hi, 0.0)})
        print(f"{hi:6.0f}->{moment_c(rep, 4.0):.3f}  ", end="")
    print()

    print("  Arithmetic-mid reps: ", end="")
    arith = {g: (lo + hi) / 2 for g, (lo, hi) in GROUP_EDGES_GR.items()}
    print(f"{moment_c(arith, 4.0):.3f}")

    # Full corner sweep over the four stated assumptions -> reported band.
    corners = []
    for floor, top, a4, hi1 in itertools.product(
        (2.5, 37.5), (5000.0, 25000.0), (4.0, 6.0), (100.0, 200.0)
    ):
        rep = dict(
            base_rep,
            **{
                "Group 0": geo_mean(0.0, 75.0, floor),
                "Group 4": geo_mean(2500.0, top, 0.0),
                "Group 1": geo_mean(75.0, hi1, 0.0),
            },
        )
        corners.append(moment_c(rep, a4))
    print(f"\n  corner sweep over all four assumptions: "
          f"c in [{min(corners):.3f}, {max(corners):.3f}], baseline {c0:.3f}")

    # LIMIT CHECK 1: no aspect-ratio dispersion (every fragment at A = 1.6) ->
    # <A x^2> = <A><x^2> identically, so c must be exactly 1 whatever the
    # masses.  This is the "c = 1 recovers the shipped closure" limit.
    saved = dict(BIN_RATIO)
    BIN_RATIO.update({k: 1.6 for k in saved})
    print(f"\nLIMIT CHECK 1  no aspect dispersion -> c = "
          f"{moment_c(base_rep, 1.6):.6f}  (must be 1.000000)")
    BIN_RATIO.update(saved)

    # LIMIT CHECK 2: A independent of mass (same mass in every Group).  c is
    # then 1/(<A><1/A>) < 1, NOT 1 -- because x^2 = m/(rho t0 A) is
    # deterministically anti-correlated with A at fixed m.  See derivation
    # section 3.2: the moment that enters is Cov(A, x^2), not Cov(A, m).
    flat = {g: 300.0 for g in GROUP_EDGES_GR}
    print(f"LIMIT CHECK 2  A independent of m -> c = {moment_c(flat, 4.0):.4f} "
          "(= 1/(<A><1/A>) < 1, the AM-HM floor -- not 1)")

    # A9.1's factor, measured on the same table (between-Group dispersion only).
    k0 = variance_k(base_rep, 4.0)
    k_corners = []
    for floor, top, a4, hi1 in itertools.product(
        (2.5, 37.5), (5000.0, 25000.0), (4.0, 6.0), (100.0, 200.0)
    ):
        rep = dict(
            base_rep,
            **{
                "Group 0": geo_mean(0.0, 75.0, floor),
                "Group 4": geo_mean(2500.0, top, 0.0),
                "Group 1": geo_mean(75.0, hi1, 0.0),
            },
        )
        k_corners.append(variance_k(rep, a4))
    print(f"\nA9.1 factor  k = <x^2>/<x>^2 = {k0:.3f}  "
          f"(corner sweep [{min(k_corners):.3f}, {max(k_corners):.3f}]; "
          "LOWER bound -- within-Group spread unresolved)")
    print(f"combined     c * k = {c0 * k0:.3f}   "
          f"(corner sweep [{min(corners) * min(k_corners):.3f}, "
          f"{max(corners) * max(k_corners):.3f}])")

    # IDENTITY CHECK: c * k must equal <A x^2>/(<A><x>^2) = <m>/(<A><sqrt(m/A)>^2)
    # computed directly, i.e. the full product-of-means error of the shipped
    # closure factorises exactly into (this update's c) x (A9.1's k).
    ratio = dict(BIN_RATIO)
    n_tot = s_m = s_a = s_root = 0.0
    with CSV.open() as fh:
        for row in csv.DictReader(fh):
            m = base_rep[row["group"]]
            for kk, a in ratio.items():
                n = float(row[kk])
                n_tot += n
                s_m += n * m
                s_a += n * a
                s_root += n * (m / a) ** 0.5
    direct = (s_m / n_tot) / ((s_a / n_tot) * (s_root / n_tot) ** 2)
    print(f"IDENTITY     <m>/(<A><sqrt(m/A)>^2) = {direct:.6f} vs c*k = "
          f"{c0 * k0:.6f}  (must agree)")
