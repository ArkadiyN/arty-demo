"""Per-shell aspect-ratio moment correction c(shell), and the 75mm count chain at it.

Consumer: experiment/fragmentation-field/updates/mass-dependent-fragment-shape/
derivation.md sections 3.3b, 3.4b, 6, 7 (per-shell c table, band, 75mm count chain).

Supersedes the single global c of derivation.md 3.3 (review.md finding A1).
c = <m>/(<A><m/A>) is a moment of the joint (A,m) distribution; its m-marginal
is the SHELL's own Mott spectrum, not Felix Table 3's photographic sample.
Three weightings of the same Table-3 aspect data are computed:

  A  group-collapsed, geometric-mean bin representative   (review.md A1 method)
  B  group-collapsed, Mott-conditional mean bin mass      (self-consistent masses)
  C  continuous Abar(m) power law through the group centroids, clamped outside
     the sampled span -- restores the within-group mass-aspect covariance that
     A and B discard by construction (derivation.md A11 lower-bound structure)

All three keep the identical within-group aspect-ratio mix from Table 3 and
solve the fixed point c = c(c*mu0), since mu = c*mu0 sets the weights.
"""
import csv
import dataclasses
import pathlib

import numpy as np

from arty.shells import SHELLS
from arty.fragmentation import _MOTT_ASPECT_RATIO, gurney_velocity, mott_params

GR = 0.06479891e-3  # kg per grain
CSV = pathlib.Path("doc-reference/fragmentation/explosion-fragment-model/"
                   "tables/table-3-grady-aspect-ratio-counts.csv")
EDGES = {0: (7.5, 75.0), 1: (75.0, 150.0), 2: (150.0, 750.0),
         3: (750.0, 2500.0), 4: (2500.0, 7500.0)}
RATIOS = np.array([1.0, 2.0, 3.0, 4.0])
KEYS = ("n_1to1", "n_1to2", "n_1to3", "n_1to4plus")

# ---- Table 3 ---------------------------------------------------------------
counts = np.zeros((5, 4))
for row in csv.DictReader(CSV.open()):
    g = int(row["group"].split()[-1])
    counts[g] = [float(row[k]) for k in KEYS]

n_g = counts.sum(axis=1)                       # fragments per Group
mix = counts / n_g[:, None]                    # within-Group aspect mix
m_geo = np.array([np.sqrt(lo * hi) for lo, hi in EDGES.values()])   # gr
Abar_g = mix @ RATIOS                          # Group mean aspect ratio

n_j = counts.sum(axis=0)                       # per-aspect-bin totals
w_j = n_j / n_j.sum()
A_table = float(w_j @ RATIOS)                  # 1.5681
floor = 1.0 / (A_table * float(w_j @ (1.0 / RATIOS)))   # AM-HM floor, 0.8354

# ---- Mott moments: N(>=m)=N0 exp(-sqrt(m/mu)) => <g(m)> = int g(mu u^2) e^-u du
U, W = np.polynomial.laguerre.laggauss(120)


def mott_mean(g, mu):
    """<g(m)> over the Mott number distribution of mean mass 2*mu [same unit as mu]."""
    return float(W @ g(mu * U**2))


def group_weights(mu):
    """P(fragment in Group g) under the Mott spectrum; Group 0 absorbs all m<75gr."""
    u = np.array([0.0] + [np.sqrt(EDGES[g][1] / mu) for g in range(4)] + [np.inf])
    lo, hi = u[:-1], u[1:]
    return np.exp(-lo) - np.where(np.isfinite(hi), np.exp(-hi), 0.0)


def group_cond_mass(mu):
    """E[m | Group g] under the Mott spectrum [gr]."""
    u = np.array([0.0] + [np.sqrt(EDGES[g][1] / mu) for g in range(4)] + [np.inf])

    def antideriv(x):
        # int u^2 e^-u du = -(u^2+2u+2) e^-u
        return -(x**2 + 2 * x + 2) * np.exp(-x) if np.isfinite(x) else 0.0

    num = np.array([antideriv(u[i + 1]) - antideriv(u[i]) for i in range(5)]) * mu
    return num / group_weights(mu)


def c_collapsed(mu, m_rep):
    w = (group_weights(mu)[:, None] * mix).ravel()
    m = np.repeat(m_rep, 4)
    A = np.tile(RATIOS, 5)
    w = w / w.sum()
    return float((w @ m) / ((w @ A) * (w @ (m / A))))


# ---- continuous Abar(m): power law through the Group centroids --------------
p_fit, a_fit = np.polyfit(np.log(m_geo), np.log(Abar_g), 1)


def Abar(m):
    """Mean aspect ratio at mass m [gr], clamped outside Table 3's sampled span."""
    return np.exp(a_fit) * np.clip(m, m_geo[0], m_geo[-1]) ** p_fit


def c_continuous(mu):
    num = mott_mean(lambda m: m, mu)
    d1 = mott_mean(Abar, mu)
    d2 = mott_mean(lambda m: m / Abar(m), mu)
    return float(num / (d1 * d2)) * floor


def fixed_point(fn, mu0, tol=1e-6):
    c = 1.0
    for _ in range(60):
        c_new = fn(c * mu0)
        if abs(c_new - c) < tol:
            return c_new
        c = c_new
    return c


print(f"Table 3: <A>={A_table:.4f}  AM-HM floor 1/(<A><1/A>)={floor:.4f}")
print(f"Abar(m) power-law fit over Group centroids: Abar = {np.exp(a_fit):.4f} "
      f"m[gr]^{p_fit:.4f}   (Abar_g = {np.round(Abar_g,3).tolist()})")
w_tab = (counts / counts.sum()).ravel()
m_tab = np.repeat(m_geo, 4)
A_tab = np.tile(RATIOS, 5)
c_tab = (w_tab @ m_tab) / ((w_tab @ A_tab) * (w_tab @ (m_tab / A_tab)))
print(f"table-count weighting (derivation 3.3 regression): <m>={w_tab@m_tab:.2f} gr  "
      f"<A>={w_tab@A_tab:.4f}  c={c_tab:.4f}   (expect 219.04 / 1.5681 / 1.2543)")

print("\nper-shell spectrum-consistent c (fixed point c = c(c*mu0)):")
print(f"{'shell':>15} {'mu0[gr]':>8} {'P(G0)':>7} {'A: geo-rep':>11} "
      f"{'B: cond-m':>10} {'C: cont A(m)':>13} {'A_eff=cA (C)':>13}")
res = {}
for name, sh in SHELLS.items():
    # mu0 is the UNCORRECTED Mott mass parameter: the registry now ships
    # aspect_ratio = c*1.6, and the fixed point below applies c itself, so the
    # baseline must be pinned back to the bare count-weighted A or c is
    # double-counted.
    sh = dataclasses.replace(sh, aspect_ratio=_MOTT_ASPECT_RATIO)
    mu0 = mott_params(sh, gurney_velocity(sh))[0] / GR
    cA = fixed_point(lambda mu: c_collapsed(mu, m_geo), mu0)
    cB = fixed_point(lambda mu: c_collapsed(mu, group_cond_mass(mu)), mu0)
    cC = fixed_point(c_continuous, mu0)
    res[name] = (mu0, cA, cB, cC)
    print(f"{name:>15} {mu0:8.2f} {group_weights(cA*mu0)[0]:7.3f} "
          f"{cA:11.4f} {cB:10.4f} {cC:13.4f} {1.6*cC:13.3f}")

print("\n75mm M48 count chain, re-solved (mu0=0.929 g, N0=2681, m_thr=0.166 g;")
print("  count-chain.md verdict row = f 1.000 -> 1756, 2.51x / 2.25x):")
mu0g, N00, m_thr = 0.929, 2681.0, 0.166
mu0_75, cA75, cB75, cC75 = res["75mm M48 HE"]
rows = [("shipped (c=1)", 1.0),
        ("global c (derivation 3.3)", 1.2543),
        ("per-shell A: geo-rep", cA75),
        ("per-shell B: cond-m", cB75),
        ("per-shell C: continuous A(m)", cC75)]
print(f"{'row':>30} {'f':>7} {'mu[g]':>7} {'N0':>7} {'N':>7} {'/700':>7} {'/779':>7}")
for lbl, f in rows:
    mu = f * mu0g
    N0 = N00 / f
    N = N0 * np.exp(-np.sqrt(m_thr / mu))
    print(f"{lbl:>30} {f:7.3f} {mu:7.3f} {N0:7.0f} {N:7.0f} "
          f"{N/700:6.2f}x {N/779:6.2f}x")

print("\n155mm M107 (the B(r) cross-check caliber): per-shell c vs the global 1.2543")
mu0_155, cA155, cB155, cC155 = res["155mm M107 HE"]
for lbl, c in (("A geo-rep", cA155), ("B cond-m", cB155), ("C cont A(m)", cC155)):
    print(f"  {lbl:>12}: c={c:.4f}  A_eff={1.6*c:.3f}  "
          f"delta vs 1.2543 = {(c/1.2543-1)*100:+.1f}%")
