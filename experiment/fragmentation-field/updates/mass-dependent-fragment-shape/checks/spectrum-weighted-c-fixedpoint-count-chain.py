"""Fixed-point stability of the spectrum-weighted c (review.md 2026-08-16 pass).
mu depends on c (mu = c*mu0) and c's Group weights depend on mu. Iterate.
Also: count-chain re-solve at the 75mm spectrum-consistent c.
"""
import numpy as np
import csv
import pathlib
from arty.shells import SHELLS
from arty.fragmentation import _MOTT_ASPECT_RATIO, gurney_velocity, mott_params
import dataclasses

GR = 0.06479891e-3
p = pathlib.Path("doc-reference/fragmentation/explosion-fragment-model/tables/table-3-grady-aspect-ratio-counts.csv")
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


def survival_frac(x, mu):
    return 1.0-np.exp(-np.sqrt(x/mu))


def c_of(mu):
    gw = {g: ((1.0 if g==4 else survival_frac(hi, mu)) - (0.0 if g==0 else survival_frac(lo, mu)))
          for g,(lo,hi) in edges.items()}
    w = np.array([N[i]*gw[G[i]]/N[G==G[i]].sum() for i in range(len(N))])
    w = w/w.sum()
    return (w*M).sum()/((w*A).sum()*(w*M/A).sum())


for name,sh in SHELLS.items():
    # pin back to the uncorrected A: the registry now ships aspect_ratio = c*1.6
    sh = dataclasses.replace(sh, aspect_ratio=_MOTT_ASPECT_RATIO)
    mu0 = mott_params(sh,gurney_velocity(sh))[0]/GR
    c = 1.0
    hist = []
    for _ in range(12):
        c = c_of(c*mu0)
        hist.append(c)
    print(f"{name:>14} mu0={mu0:7.2f}gr  iterates: "+" ".join(f"{h:.4f}" for h in hist[:5])+f" ... converged c={hist[-1]:.4f}")

print("\n75mm count chain re-solve (mu0=0.929 g, N0=2681, m_thr=0.166 g, count-chain.md verdict row):")
mu0, N0, mt = 0.929, 2681., 0.166
for lbl,f in [("shipped c=1",1.0),("derivation c=1.254",1.254),("spectrum-consistent 75mm",c_of(1.0*14.33))]:
    mu = f*mu0
    n = N0/f*np.exp(-np.sqrt(mt/mu))
    print(f"  {lbl:>26}  f={f:.3f}  mu={mu:.3f}g  N={n:.0f}  vs700={n/700:.2f}x  vs779={n/779:.2f}x")
