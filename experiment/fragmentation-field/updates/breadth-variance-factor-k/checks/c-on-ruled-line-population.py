"""Re-solve the aspect moment c on the SAME population k is derived from.

Consumer: experiment/fragmentation-field/updates/breadth-variance-factor-k/
derivation.md sections 3, 5.1, 5.2 (fix cycle 1, review.md finding B2).

Background.  eq. (2) of ../mass-dependent-fragment-shape/derivation.md,
    <A x^2> / (<A><x>^2) = c * k ,
is exact only when BOTH moments are averaged over ONE population.  The shipped
c = 1.2506 (155 mm) is a mu-weighted Table-3 moment whose weighting population
is the 1943-descended Mott mass spectrum N(>=m) = N0 exp(-sqrt(m/mu)); the
resolved k = 1.1375 is the second moment of Mott 1947's ruled-line breadth
distribution.  Two populations, one identity -> review.md B2 (Blocking).

This script re-solves c on the ruled-line population:

  * A fragment is (aspect A, breadth x) with mass m = rho t A x^2, so with
    S = rho t x0^2 the single unknown mass scale [grains] and xi = x/x0,
    m = S * A * xi^2.  A Table-3 cell (mass group g, aspect bin A) is therefore
    the breadth interval xi in [sqrt(lo_g/(A S)), sqrt(hi_g/(A S))].
  * Table 3 supplies the CONDITIONAL aspect mix A|g (the physical input the
    prior update showed transfers across calibers).  Mott 1947 supplies the
    breadth MARGINAL, sampled from checks/mott-ruled-line-mc.py (not re-derived
    here).  This is exactly the shipped construction of
    ../mass-dependent-fragment-shape/checks/spectrum-weighted-c-per-shell.py
    with ONE substitution: the group weight is the ruled line's probability of
    the mass bracket instead of the Mott spectrum's survival difference.
  * Cell moments are the ruled-line moments TRUNCATED to that cell's xi
    interval, so no point-mass representative is needed and the 5-group mass
    axis stops being a resolution floor.
  * S is fixed by the closure's own mean-mass identity <m> = 2 mu (the Mott
    spectrum's mean), and mu is the fixed point mu = c * k * mu0 -- note the
    factor k, which the shipped fixed point mu = c * mu0 omits.

Outputs: per-shell c on the ruled-line population, A_eff = 1.6*c*k, and the
realised k of the reweighted cell population (a closure check: it should
reproduce the MC's k if the marginal match is faithful).
"""

from __future__ import annotations

import csv
import dataclasses
import importlib.util
import pathlib
import sys

import numpy as np

from arty.fragmentation import (
    _MOTT_ASPECT_RATIO,
    MOTT_ASPECT_MOMENT_C,
    gurney_velocity,
    mott_aspect_ratio,
    mott_params,
)
from arty.shells import SHELLS

GR = 0.06479891e-3  # 1 grain [kg]
HERE = pathlib.Path(__file__).resolve().parent


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mc = _load(HERE / "mott-ruled-line-mc.py", "mott_ruled_line_mc")

# ---------------------------------------------------------------- Table 3 cells
TABLE3 = pathlib.Path(
    "doc-reference/fragmentation/explosion-fragment-model/"
    "tables/table-3-grady-aspect-ratio-counts.csv"
)
EDGES = {0: (7.5, 75.0), 1: (75.0, 150.0), 2: (150.0, 750.0),
         3: (750.0, 2500.0), 4: (2500.0, 7500.0)}
RATIOS = np.array([1.0, 2.0, 3.0, 4.0])

_g, _n, _a = [], [], []
for row in csv.DictReader(TABLE3.open()):
    g = int(row["group"].split()[-1])
    for key, a in zip(("n_1to1", "n_1to2", "n_1to3", "n_1to4plus"), RATIOS):
        _g.append(g)
        _n.append(float(row[key]))
        _a.append(a)
G = np.array(_g)
N = np.array(_n)          # Table-3 count in cell (group, aspect bin)
A = np.array(_a)          # aspect ratio of the bin
# aspect mix CONDITIONAL on group -- the only Table-3 input retained
NG = np.array([N[G == g].sum() for g in G])
P_A_GIVEN_G = N / NG
# mass bracket of each cell [grains]; group 0 opened down to 0 and group 4 up
# to infinity, matching the shipped spectrum-weighted script
LO = np.array([0.0 if g == 0 else EDGES[g][0] for g in G])
HI = np.array([np.inf if g == 4 else EDGES[g][1] for g in G])

# ------------------------------------------------- ruled-line breadth marginal
XI = mc.run(20.0, n_rings=400, scheme="mott")   # Mott's own l/x0 = 20 config
K_MC = (XI**2).mean() / XI.mean() ** 2
XI2 = XI**2


P_A_MARGINAL = np.array([N[(A == a)].sum() / N.sum() for a in A])

# Which of the two natural weighting closures to use.  They differ only in
# whether the ruled line's probability of a cell's mass bracket is taken at that
# cell's own aspect ("percell", the joint is P(A|g) x P_ruled(m in g | A)) or
# with the aspect marginalised out ("marginal", the group weight is
# A-independent exactly as in the shipped spectrum-weighted script).  Reported
# as a band in derivation.md sect. 3 -- neither is exact, because Table 3's
# conditional A|m and Mott's breadth marginal over-determine the joint.
MODE = "percell"


def cell_stats(S: float, mode: str | None = None):
    """Per-cell (weight, <xi>, <xi^2>) under the ruled-line marginal at scale S."""
    mode = mode or MODE
    w = np.zeros(len(N))
    m1 = np.zeros(len(N))
    m2 = np.zeros(len(N))
    p_cell = np.zeros(len(N))
    for i in range(len(N)):
        lo = np.sqrt(LO[i] / (A[i] * S))
        hi = np.inf if not np.isfinite(HI[i]) else np.sqrt(HI[i] / (A[i] * S))
        sel = (XI >= lo) & (XI < hi)
        n = int(sel.sum())
        if n == 0:
            continue
        p_cell[i] = n / XI.size
        m1[i] = XI[sel].mean()
        m2[i] = XI2[sel].mean()
    if mode == "percell":
        w = P_A_GIVEN_G * p_cell
    else:  # "marginal": group weight = sum_A P(A) P_ruled(m in g | A)
        p_g = np.array([(P_A_MARGINAL * p_cell)[G == g].sum() for g in G])
        w = P_A_GIVEN_G * p_g
    return w, m1, m2


def population(S: float):
    """Return (c, k_pop, <m>[grains], weights) of the ruled-line cell population."""
    w, m1, m2 = cell_stats(S)
    tot = w.sum()
    if tot <= 0:
        return np.nan, np.nan, np.nan, w
    w = w / tot
    A_bar = (w * A).sum()
    x2_bar = S * (w * m2).sum()                 # <x^2> in grain units
    x_bar = np.sqrt(S) * (w * m1).sum()         # <x>
    m_bar = S * (w * A * m2).sum()              # <m> = <A x^2>
    return m_bar / (A_bar * x2_bar), x2_bar / x_bar**2, m_bar, w


def solve_shell(shell):
    """Fixed point (mu0, mu, S, c, k_pop, w) for one shell on the ruled line."""
    bare = dataclasses.replace(shell, aspect_ratio=_MOTT_ASPECT_RATIO)
    mu0 = mott_params(bare, gurney_velocity(bare))[0] / GR   # [grains], A = 1.6
    mu = mu0
    c = k_pop = np.nan
    w = np.zeros(len(N))
    S = 1.0
    for _ in range(100):
        # bisect S on <m>(S) = 2 mu  (m_bar is monotone increasing in S)
        lo_s, hi_s = 1e-6, 1e6
        for _ in range(80):
            S = np.sqrt(lo_s * hi_s)
            m_bar = population(S)[2]
            if not np.isfinite(m_bar):
                break
            if m_bar < 2.0 * mu:
                lo_s = S
            else:
                hi_s = S
        S = np.sqrt(lo_s * hi_s)
        c_new, k_pop, m_bar, w = population(S)
        mu_new = c_new * K_MC * mu0
        done = abs(mu_new / mu - 1) < 1e-8
        mu, c = mu_new, c_new
        if done:
            break
    return mu0, mu, S, c, k_pop, w


if __name__ == "__main__":
    print(f"ruled-line MC (l/x0=20, Mott step): n={XI.size}  <xi>={XI.mean():.4f}  "
          f"k_MC={K_MC:.4f}\n")
    # Read the shipped comparison column LIVE, never hand-typed: a literal dict
    # here silently went stale by a whole c-revision and had to be caught in
    # review (updates/kappa-x-shell-regime/review.md Pass 3, D5), which is the
    # "hand-copies a series into a literal array" anti-pattern of
    # .claude/rules/source-data-fidelity.md.
    shipped_c = dict(MOTT_ASPECT_MOMENT_C)
    for mode in ("percell", "marginal"):
        MODE = mode
        print(f"--- weighting closure: {mode} ---")
        print(f"{'shell':>14} {'mu0[gr]':>9} {'mu[gr]':>9} {'S[gr]':>8} "
              f"{'c_ruled':>8} {'c_ship':>7} {'k_pop':>7} {'A_eff':>7} {'A_ship':>7}")
        for name, sh in SHELLS.items():
            mu0, mu, S, c, k_pop, w = solve_shell(sh)
            a_eff = _MOTT_ASPECT_RATIO * c * K_MC
            print(f"{name:>14} {mu0:9.2f} {mu:9.2f} {S:8.4f} {c:8.4f} "
                  f"{shipped_c[name]:7.4f} {k_pop:7.4f} {a_eff:7.4f} "
                  f"{mott_aspect_ratio(name):7.4f}")
            ww = w / w.sum()
            pg = [ww[G == g].sum() for g in range(5)]
            print("      group weights G0..G4: " + " ".join(f"{v:.4f}" for v in pg)
                  + f"   <A>={(ww * A).sum():.4f}")
        print()

