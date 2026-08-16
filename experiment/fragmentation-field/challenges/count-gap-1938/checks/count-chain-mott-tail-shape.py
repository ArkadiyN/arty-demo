"""C3: is the single-exponential Mott form a valid extrapolation into 0.166-0.63 g?

Produces every number cited in
experiment/fragmentation-field/challenges/count-gap-1938/mott-tail-shape.md.

Method. The quantity C3 owns is the *extrapolation multiplier*
    R = N(>=0.166 g) / N(>=0.63 g),
which is independent of N0 and of M_case (those are C4's question). For the
generalised Mott family N(>=m) = N0 exp[-(m/mu)^lam] the locus of
(number fraction, mass fraction) traced as m varies depends on lam ALONE:

    Nhat(u) = exp(-u),   phi(u) = Gamma(1+1/lam, u) / Gamma(1+1/lam),
    u = (m/mu)^lam.

so lam can be fitted to Tolch's screen census without knowing a single screen
cut mass (boundary-free) and without fixing mu or N0 (scale-free). That is the
primary study. Two sensitivity rows follow: Mott's own 3D exponent lam = 1/3,
and a spliced power-law tail at tau = 1.9-2.2 (Carmona 2007 / Tavassoli 2000).

Sources
  Tolch 1938 pit census : doc-reference/wound-ballistics/
      tolch-1938-m48-panel-pit-fragmentation/tables/pit-screen-recovery.csv
  Generalised Mott (6)  : doc-reference/mott-distribution-small-fragments/
      elek-jaramaz-2009/elek-jaramaz-2009-warhead-distribution.md line 60
  Power-law tail        : .../carmona-2007/, .../tavassoli-2000/

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-mott-tail-shape.py
"""

import csv
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import gamma as Gamma
from scipy.special import gammaincc

from arty.fragmentation import gurney_velocity, mott_N, mott_params
from arty.shells import SHELLS

REPO = next(
    p for p in Path(__file__).resolve().parents if (p / "doc-reference").is_dir()
)
TABLES = (
    REPO
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)
LB_G = 453.59237
CUT_HI = 0.63e-3  # kg, Tolch's finest screen cut (thread convention)
CUT_LO = 0.166e-3  # kg, C1 sourced plug-shear threshold at the verdict row

with open(TABLES / "pit-screen-recovery.csv", newline="") as fh:
    pit = list(csv.DictReader(fh))
n_frag = np.array([float(r["n_frag"]) for r in pit])
wt_g = np.array([float(r["wt_lb"]) for r in pit]) * LB_G
screens = [r["screen"] for r in pit]
N_rec, W_rec = n_frag.sum(), wt_g.sum()

# ---------------------------------------------------------------- model side
shell = SHELLS["75mm M48 HE"]
V0 = gurney_velocity(shell)
mu, N0 = mott_params(shell, V0)
R_shipped = mott_N(np.array([CUT_LO]), N0, mu)[0] / mott_N(
    np.array([CUT_HI]), N0, mu
)[0]

print("=== (A) shipped model, 75 mm M48 ===")
print(f"  V0 = {V0:.1f} m/s   mu = {mu*1e3:.4f} g   N0 = {N0:.0f}")
for c in (CUT_HI, CUT_LO):
    print(f"  N(>= {c*1e3:5.3f} g) = {mott_N(np.array([c]), N0, mu)[0]:7.0f}")
print(f"  extrapolation multiplier R_shipped = {R_shipped:.3f}")
print(f"  Tolch pit census N_rec = {N_rec:.0f}, recovered metal {W_rec:.0f} g")


# ------------------------------------------- generalised Mott (Elek eq. (6))
def phi_of_u(u, lam):
    """Mass fraction above the mass whose number fraction is exp(-u) [-]."""
    a = 1.0 + 1.0 / lam
    return gammaincc(a, u)  # = Gamma(a,u)/Gamma(a), regularised upper


def u_of_phi(phi, lam):
    """Invert phi_of_u (monotone decreasing in u)."""
    return np.array(
        [brentq(lambda uu: phi_of_u(uu, lam) - p, 1e-12, 400.0) for p in np.atleast_1d(phi)]
    )


# Tolch cumulative census, coarsest -> finest.
cum_n = np.cumsum(n_frag)
cum_w = np.cumsum(wt_g)

# The fit uses only the four screen-boundary points (screens 1..4). The
# through-screen-4 row is the census-incomplete bucket (open finding: mean
# 0.61 g sits at the detection floor) and is EXCLUDED from the fit; it is
# reported as a held-out check.
FIT = slice(0, 4)


def fit_N_tot(lam, M_tot):
    """Best-fit total count N_tot at fixed lam, plus the log-residual cost.

    u depends on lam alone, so log N_tot enters the log-residuals linearly and
    its optimum is closed-form: log N_tot = mean(log n_i + u_i).
    """
    u = u_of_phi(cum_w[FIT] / M_tot, lam)
    log_N = float(np.mean(np.log(cum_n[FIT]) + u))
    cost = float(np.sum((log_N - u - np.log(cum_n[FIT])) ** 2))
    return np.exp(log_N), cost


def fit_lambda(M_tot):
    """Least-squares lam over log-count residuals at the 4 screen boundaries."""
    r = minimize_scalar(
        lambda lam: fit_N_tot(lam, M_tot)[1], bounds=(0.12, 1.6), method="bounded"
    )
    lam = float(r.x)
    return lam, fit_N_tot(lam, M_tot)[0], float(r.fun)


def R_of_lambda(lam, M_tot, N_tot):
    """Extrapolation multiplier N(>=0.166)/N(>=0.63) for exponent lam.

    Scale mu is set by the same (M_tot, N_tot) closure the fit used:
    M_tot = N_tot * mu * Gamma(1+1/lam).
    """
    mu_l = M_tot / (N_tot * Gamma(1.0 + 1.0 / lam))
    n_hi = N_tot * np.exp(-((CUT_HI / mu_l) ** lam))
    n_lo = N_tot * np.exp(-((CUT_LO / mu_l) ** lam))
    return n_lo / n_hi, n_lo, n_hi, mu_l


print("\n=== (B) generalised Mott exponent fitted to Tolch's resolved census ===")
print("  (boundary-free: only cumulative count vs cumulative mass is used)")
# Two mass bases, per the thread's open C4 question. N_tot is the total count
# the form implies; it is a free parameter of the fit here, taken as the count
# that best matches -- we scan it jointly on a coarse grid.
# NOTE the shipped M_case (4980 g) basis is omitted: it is BELOW Tolch's
# recovered metal (5764 g), so phi > 1 at the fine screens and the inversion
# has no root -- the degeneracy count-chain.md Sec.2 already records.
for basis, M_tot in (
    ("Tolch 13.29 lb metal", 13.29 * LB_G),
    ("Tolch recovered metal", W_rec),
):
    lam, N_tot, cost = fit_lambda(M_tot)
    R_a, n_lo, n_hi, mu_l = R_of_lambda(lam, M_tot, N_tot)
    u = u_of_phi(cum_w[FIT] / M_tot, lam)
    pred = N_tot * np.exp(-u)
    print(f"\n  --- basis = {basis} ({M_tot:.0f} g) ---")
    print(f"  best lam = {lam:.3f}   N_tot = {N_tot:.0f}   mu = {mu_l*1e3:.4f} g")
    print("   thru screen | Tolch cum n | fitted N | resid")
    for s, cn, p in zip(screens[:4], cum_n[FIT], pred):
        print(f"   {s:>11s} | {cn:11.0f} | {p:8.0f} | {p/cn:5.2f}x")
    # held-out: the census-incomplete through-screen-4 row
    u4 = u_of_phi(np.array([cum_w[4] / M_tot]), lam)
    print(
        f"   {'thru4 (held out)':>11s} | {cum_n[4]:11.0f} | "
        f"{N_tot*np.exp(-u4)[0]:8.0f} | {N_tot*np.exp(-u4)[0]/cum_n[4]:5.2f}x"
    )
    print(
        f"  N(>=0.63 g) = {n_hi:7.0f}   N(>=0.166 g) = {n_lo:7.0f}   "
        f"R_alt = {R_a:.3f}   credit = {R_shipped/R_a:.3f}x"
    )
    # IDENTIFIABILITY CHECK: what absolute mass does this fit assign to each
    # screen boundary? If those are not near Tolch's bucket means the fit has
    # matched the (count, mass) locus at the wrong mass scale and is void.
    m_impl = mu_l * u ** (1.0 / lam)
    print(
        "  implied boundary masses [g]: "
        + ", ".join(f"{v*1e3:.3f}" for v in m_impl)
        + f"   (bracketing bucket means: {', '.join(f'{v:.2f}' for v in wt_g/n_frag)})"
    )


# ---------------- (B2) absolute-mass-anchored fit -- the identifying one -----
# The locus fit above fixes only the SHAPE; mu is then set by mass closure and
# can land far from the real screen masses. Anchor it: take each screen
# boundary mass as the geometric mean of the two bucket means it separates
# (the standard binned estimator; Tolch does not publish mesh openings).
means = wt_g / n_frag * 1e-3  # kg, coarsest -> finest
m_bnd = np.sqrt(means[:-1] * means[1:])  # 4 boundaries, coarsest -> finest
n_above = cum_n[:4]

print("\n=== (B2) absolute-mass-anchored generalised-Mott fit ===")
print("  boundary masses [g]: " + ", ".join(f"{v*1e3:.3f}" for v in m_bnd))
print("  cumulative counts  : " + ", ".join(f"{v:.0f}" for v in n_above))


def fit_abs(lam):
    """At fixed lam, closed-form (log N_tot, mu) LS fit to log n vs m^lam."""
    x = m_bnd**lam
    y = np.log(n_above)
    A = np.vstack([np.ones_like(x), -x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    logN, inv_mu_lam = coef
    if inv_mu_lam <= 0:
        return np.inf, None
    resid = float(np.sum((A @ coef - y) ** 2))
    return resid, (np.exp(logN), inv_mu_lam ** (-1.0 / lam))


r = minimize_scalar(lambda L: fit_abs(L)[0], bounds=(0.15, 1.5), method="bounded")
lam_a = float(r.x)
N_a, mu_a = fit_abs(lam_a)[1]
print(f"  best lam = {lam_a:.3f}   N_tot = {N_a:.0f}   mu = {mu_a*1e3:.4f} g")
print(f"  implied mean fragment mass = {mu_a*Gamma(1+1/lam_a)*1e3:.2f} g "
      f"(Tolch recovered mean {W_rec/N_rec:.2f} g)")
print(f"  implied total metal = {N_a*mu_a*Gamma(1+1/lam_a)*1e3:.0f} g "
      f"(Tolch 13.29 lb = {13.29*LB_G:.0f} g, recovered {W_rec:.0f} g)")
print("    m [g] | Tolch n | fit n | shipped Mott n")
for m_b, cn in zip(m_bnd, n_above):
    fit_n = N_a * np.exp(-((m_b / mu_a) ** lam_a))
    sh_n = mott_N(np.array([m_b]), N0, mu)[0]
    print(f"   {m_b*1e3:6.3f} | {cn:7.0f} | {fit_n:5.0f} | {sh_n:7.0f}")
n_hi_a = N_a * np.exp(-((CUT_HI / mu_a) ** lam_a))
n_lo_a = N_a * np.exp(-((CUT_LO / mu_a) ** lam_a))
print(
    f"  N(>=0.63 g) = {n_hi_a:7.0f}   N(>=0.166 g) = {n_lo_a:7.0f}   "
    f"R_alt = {n_lo_a/n_hi_a:.3f}   credit = {R_shipped/(n_lo_a/n_hi_a):.3f}x"
)
print("  fixed-lam comparison at the same anchors:")
print("    lam  |  N_tot | mu [g] | N>=0.63 | N>=0.166 |  R    | credit")
for lam in (1.0 / 3.0, 0.5, lam_a):
    out = fit_abs(lam)[1]
    if out is None:
        continue
    N_t, mu_t = out
    hi = N_t * np.exp(-((CUT_HI / mu_t) ** lam))
    lo = N_t * np.exp(-((CUT_LO / mu_t) ** lam))
    print(
        f"   {lam:5.3f} | {N_t:6.0f} | {mu_t*1e3:6.3f} | {hi:7.0f} | "
        f"{lo:8.0f} | {lo/hi:5.3f} | {R_shipped/(lo/hi):5.3f}x"
    )

print("\n=== (C) sensitivity: fixed exponents at the same mass closure ===")
M_tot = 13.29 * LB_G
print(f"  basis = Tolch 13.29 lb ({M_tot:.0f} g); N_tot re-fit per lam")
print("    lam  |  N_tot | mu [g] | N>=0.63 | N>=0.166 |  R    | credit")
for lam in (1.0 / 3.0, 0.4, 0.5, 0.6, 0.75, 1.0):
    N_tot, _ = fit_N_tot(lam, M_tot)
    R_a, n_lo, n_hi, mu_l = R_of_lambda(lam, M_tot, N_tot)
    print(
        f"   {lam:5.3f} | {N_tot:6.0f} | {mu_l*1e3:6.3f} | {n_hi:7.0f} | "
        f"{n_lo:8.0f} | {R_a:5.3f} | {R_shipped/R_a:5.3f}x"
    )

# ------------------------------------------------- power-law tail sensitivity
print("\n=== (D) spliced power-law tail (Carmona 2007 tau=1.9-2.2) ===")
print("  n(m) ~ m^-tau below the splice mass, matched in value at the splice;")
print("  R_pl = 1 + [N(splice) - N(0.63)] ... integrated from the splice down.")
for m_splice in (CUT_HI, 3.0e-3):
    n_hi = mott_N(np.array([CUT_HI]), N0, mu)[0]
    n_sp = mott_N(np.array([m_splice]), N0, mu)[0]
    # density of the shipped Mott at the splice [count / kg]
    dens = n_sp / (2.0 * np.sqrt(m_splice * mu))
    for tau in (1.9, 2.2):
        # N_pl(>=m) = n_sp + dens*m_splice/(tau-1) * [(m_splice/m)^(tau-1) - 1]
        def N_pl(m):
            return n_sp + dens * m_splice / (tau - 1.0) * (
                (m_splice / m) ** (tau - 1.0) - 1.0
            )

        lo, hi = N_pl(CUT_LO), (N_pl(CUT_HI) if m_splice > CUT_HI else n_hi)
        print(
            f"  splice {m_splice*1e3:5.2f} g, tau={tau:.1f}: "
            f"N(>=0.63)={hi:7.0f}  N(>=0.166)={lo:8.0f}  R={lo/hi:6.3f}  "
            f"credit={R_shipped/(lo/hi):6.3f}x"
        )

print("\n=== (E) verdict arithmetic ===")
print(f"  standing residual   N(>=0.166)/779 = "
      f"{mott_N(np.array([CUT_LO]), N0, mu)[0]/N_rec:5.2f}x")
print(f"  above-0.63 g floor  N(>=0.63)/779  = "
      f"{mott_N(np.array([CUT_HI]), N0, mu)[0]/N_rec:5.2f}x")
print(f"  C3 max conceivable credit (empty window) = {R_shipped:.3f}x")
