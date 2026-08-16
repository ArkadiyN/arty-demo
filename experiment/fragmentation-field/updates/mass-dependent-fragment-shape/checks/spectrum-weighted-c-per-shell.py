"""Adversarial check for review.md (mass-dependent-fragment-shape, 2026-08-16).

Per-fragment resolution (A = aspect-bin value, m = group representative),
matching derivation.md 3.3. Question: c is a SPECTRUM-WEIGHTED moment. What is
it when the Group weights come from each SHELL's own Mott spectrum rather than
from Table 3's own photographic counts (derivation A5)?
"""
import numpy as np
import csv
import pathlib
from arty.shells import SHELLS
from arty.fragmentation import gurney_velocity, mott_params

GR = 0.06479891e-3
p = pathlib.Path("doc-reference/fragmentation/explosion-fragment-model/"
                 "tables/table-3-grady-aspect-ratio-counts.csv")
edges = {0:(7.5,75.),1:(75.,150.),2:(150.,750.),3:(750.,2500.),4:(2500.,7500.)}
ratios = np.array([1.,2.,3.,4.])
G_, N_, A_, M_ = [], [], [], []
for r in csv.DictReader(p.open()):
    g = int(r["group"].split()[-1])
    for key, a in zip(("n_1to1","n_1to2","n_1to3","n_1to4plus"), ratios):
        G_.append(g)
        N_.append(float(r[key]))
        A_.append(a)
        M_.append(np.sqrt(edges[g][0]*edges[g][1]))
G = np.array(G_)
N = np.array(N_)
A = np.array(A_)
M = np.array(M_)


def c_k(w):
    w = w/w.sum()
    c = (w*M).sum()/((w*A).sum()*(w*M/A).sum())
    x2 = M/A
    k = (w*x2).sum()/((w*np.sqrt(x2)).sum())**2
    return c, k


def survival_frac(x, mu):
    return 1.0-np.exp(-np.sqrt(x/mu))


c0, k0 = c_k(N.copy())
print(f"table-count weighting: <m>={np.average(M,weights=N):.2f} gr "
      f"<A>={np.average(A,weights=N):.4f} <m/A>={np.average(M/A,weights=N):.3f} "
      f"c={c0:.4f} k={k0:.4f}   (derivation: 219.04 / 1.5681 / 111.361 / 1.2543 / 1.52)")

print("\nMott-spectrum weighting (same within-Group aspect mix, Group weights from N(>=m)):")
for name, sh in SHELLS.items():
    mu = mott_params(sh, gurney_velocity(sh))[0]/GR
    gw = {}
    for g,(lo,hi) in edges.items():
        lo_ = 0.0 if g==0 else lo
        hi_ = np.inf if g==4 else hi
        gw[g] = (1.0 if not np.isfinite(hi_) else survival_frac(hi_, mu)) - survival_frac(lo_, mu)
    w = np.array([N[i]*gw[G[i]]/max(N[G==G[i]].sum(),1e-30) for i in range(len(N))])
    c,k = c_k(w)
    print(f"{name:>14}  mu={mu:8.2f} gr  P(G0)={gw[0]/sum(gw.values()):.4f}  "
          f"<A>={np.average(A,weights=w):.4f}  c={c:.4f}  k={k:.4f}  c*k={c*k:.4f}")
