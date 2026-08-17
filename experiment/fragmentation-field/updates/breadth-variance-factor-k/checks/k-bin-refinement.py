"""Produces scoping.md 6.1 (breadth-variance-factor-k): is the per-shell k trend
(1.51/1.35/1.21/1.11 for 155/105/75/60 mm) physics, or an artefact of Felix 2022
Table 3's 5-group mass discretization?

Method: k = <m/A>/<sqrt(m/A)>^2 with the mass axis integrated against the model's
OWN Mott spectrum N(>=m) = N0 exp(-sqrt(m/mu)), i.e. u = sqrt(m/mu) ~ Exp(1),
m = mu*u^2. The Table-3 aspect mix A|Group is held piecewise constant (identical
data to mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py);
only the number of mass nodes changes. Analytic limit: at constant A,
k = <m>/<sqrt(m)>^2 = 2*mu/mu = 2 exactly, for every shell (scale-free).
"""
import csv
import dataclasses
import pathlib

import numpy as np

from arty.fragmentation import _MOTT_ASPECT_RATIO, gurney_velocity, mott_params
from arty.shells import SHELLS

GR = 0.06479891e-3
CSV = pathlib.Path(
    "doc-reference/fragmentation/explosion-fragment-model/"
    "tables/table-3-grady-aspect-ratio-counts.csv"
)
EDGES = {0: (0.0, 75.0), 1: (75.0, 150.0), 2: (150.0, 750.0),
         3: (750.0, 2500.0), 4: (2500.0, np.inf)}
REPR = {0: (7.5, 75.0), 1: (75.0, 150.0), 2: (150.0, 750.0),
        3: (750.0, 2500.0), 4: (2500.0, 7500.0)}  # derivation A2/A3 reps
RATIOS = np.array([1.0, 2.0, 3.0, 4.0])

# aspect mix p(A | Group), from Table 3 counts
mix = {}
counts5 = {}
for row in csv.DictReader(CSV.open()):
    g = int(row["group"].split()[-1])
    n = np.array([float(row[k]) for k in
                  ("n_1to1", "n_1to2", "n_1to3", "n_1to4plus")])
    counts5[g] = n
    mix[g] = n / n.sum()


def group_of(m):
    """Group index [-] for grain masses m [gr]."""
    return np.digitize(m, [75.0, 150.0, 750.0, 2500.0])


def k_of(w, m, A):
    """Breadth-variance factor k = <x^2>/<x>^2 [-] from weights w, mass m [gr], aspect A [-]."""
    w = w / w.sum()
    x2 = m / A
    return (w * x2).sum() / ((w * np.sqrt(x2)).sum()) ** 2


def k_five_bin(mu):
    """k [-] at the shipped 5-group discretization (reproduces the prior pass)."""
    m, A, w = [], [], []
    for g, (lo, hi) in EDGES.items():
        pg = np.exp(-np.sqrt(lo / mu)) - (0.0 if not np.isfinite(hi)
                                          else np.exp(-np.sqrt(hi / mu)))
        rep = np.sqrt(REPR[g][0] * REPR[g][1])
        for a, p in zip(RATIOS, mix[g]):
            m.append(rep)
            A.append(a)
            w.append(pg * p)
    return k_of(np.array(w), np.array(m), np.array(A))


def k_refined(mu, n_nodes, m_cap=np.inf):
    """k [-] with the mass axis integrated over the Mott spectrum on n_nodes [-],
    optional upper mass truncation m_cap [gr] (derivation A2)."""
    # midpoint nodes in u = sqrt(m/mu), density exp(-u): equal-probability strata
    q = (np.arange(n_nodes) + 0.5) / n_nodes
    u = -np.log(1.0 - q)
    m = mu * u ** 2
    keep = m <= m_cap
    m = m[keep]
    g = group_of(m)
    P = np.array([mix[gi] for gi in g])           # (n, 4)
    mm = np.repeat(m, 4)
    AA = np.tile(RATIOS, m.size)
    return k_of(P.ravel(), mm, AA)


print("Analytic limit at constant A:  k = <m>/<sqrt(m)>^2 = 2 exactly (any mu)")
print(f"  numeric, 200k nodes, A==1:   {k_refined(100.0, 200_000):.4f}"
      "   <- uses the real A-mix, so >1 spread is the A-mix effect only\n")

hdr = f"{'shell':>15} {'mu[gr]':>8} {'5-bin':>7} " + \
      " ".join(f"{n:>7}" for n in (10, 50, 200, 2000, 50000)) + f" {'cap7500':>8}"
print(hdr)
for name, sh in SHELLS.items():
    sh = dataclasses.replace(sh, aspect_ratio=_MOTT_ASPECT_RATIO)
    mu = mott_params(sh, gurney_velocity(sh))[0] / GR
    row = [k_refined(mu, n) for n in (10, 50, 200, 2000, 50000)]
    print(f"{name:>15} {mu:8.2f} {k_five_bin(mu):7.4f} "
          + " ".join(f"{v:7.4f}" for v in row)
          + f" {k_refined(mu, 50000, m_cap=7500.0):8.4f}")
