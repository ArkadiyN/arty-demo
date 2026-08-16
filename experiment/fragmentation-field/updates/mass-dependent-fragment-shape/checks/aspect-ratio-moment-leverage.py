"""Leverage of an aspect-ratio moment correction on the count-gap-1938 residual.

Produces the table in
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/scoping.md
section 4.  Re-solves the Mott chain (mu, N0, survival) rather than scaling a
ratio of published N values, per count-chain.md's own warning.

Baseline (count-chain.md section 5, verdict row): mu = 0.929 g, N0 = 2681,
m_thr(15 ft) = 0.166 g, N(>=m_thr) = 1756, vs Tolch 700 / 779.
Closure (mott-fragment-shape-closure/derivation.md eq. 2): mu proportional to A.
"""

import csv
import math
import pathlib

MU0_G = 0.929  # g, count-chain.md section 5
N0_0 = 2681  # -, count-chain.md section 5
M_THR_G = 0.166  # g, SPF-S eta=1/2 verdict row, 15 ft
TOLCH_LOW = 700
TOLCH_HIGH = 779

CSV = (
    pathlib.Path(__file__).resolve().parents[5]
    / "doc-reference/fragmentation/explosion-fragment-model/tables"
    / "table-3-grady-aspect-ratio-counts.csv"
)
BIN_RATIO = {"n_1to1": 1.0, "n_1to2": 2.0, "n_1to3": 3.0, "n_1to4plus": 4.0}


def group_stats():
    """Per-Group count-weighted mean aspect ratio from Felix 2022 Table 3."""
    out = []
    with CSV.open() as fh:
        for row in csv.DictReader(fh):
            n = {k: float(row[k]) for k in BIN_RATIO}
            tot = sum(n.values())
            mean = sum(n[k] * BIN_RATIO[k] for k in n) / tot if tot else float("nan")
            out.append((row["group"], tot, mean))
    return out


def resolve_chain(c):
    """Re-solve (mu, N0, N) for a multiplicative correction c on A (mu ~ A)."""
    mu = MU0_G * c
    n0 = N0_0 / c  # N0 = M_case / (2 mu)
    n = n0 * math.exp(-math.sqrt(M_THR_G / mu))
    return mu, n0, n


if __name__ == "__main__":
    rows = group_stats()
    grand_n = sum(r[1] for r in rows)
    grand_mean = sum(r[1] * r[2] for r in rows) / grand_n
    print("Felix 2022 Table 3 -- per-Group count-weighted mean aspect ratio")
    for g, tot, mean in rows:
        print(f"  {g:8s} n={tot:6.0f}  A_bar={mean:.2f}")
    print(f"  ALL      n={grand_n:6.0f}  A_bar={grand_mean:.3f}  (open bin at 4.0)")
    print()
    print("Re-solved chain vs correction factor c on A  (mu ~ A, N0 ~ 1/A)")
    print("  c      mu[g]   N0     N(>=m_thr)  N/700   N/779")
    for c in (1.0, 1.2, 1.4, 1.6, 1.9, 2.2):
        mu, n0, n = resolve_chain(c)
        print(
            f"  {c:4.2f}  {mu:6.3f}  {n0:6.0f}   {n:7.0f}    "
            f"{n / TOLCH_LOW:5.2f}x  {n / TOLCH_HIGH:5.2f}x"
        )
    print()
    print("baseline check c=1.0 should reproduce N=1756, 2.51x, 2.25x")
