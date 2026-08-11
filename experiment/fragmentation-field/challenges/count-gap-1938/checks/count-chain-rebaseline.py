"""Re-run the count-gap-1938 count chain against the re-baselined Tolch-1938 CSVs.

Produces every number cited in
experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md.

All Tolch series are read from
doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/
(extracted once, closure-checked). Nothing is hand-typed.

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-rebaseline.py
"""

import csv
from pathlib import Path

import numpy as np

from arty.fragmentation import (
    DragParams,
    _shell_geometry,
    gurney_velocity,
    min_lethal_mass,
    mott_N,
    mott_params,
)
from arty.shells import SHELLS

REPO = next(
    p for p in Path(__file__).resolve().parents if (p / "doc-reference").is_dir()
)
TABLES = (
    REPO
    / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables"
)
LB_G = 453.59237


def load(name):
    with open(TABLES / f"{name}.csv", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- Tolch side
pit = load("pit-screen-recovery")
n_frag = np.array([float(r["n_frag"]) for r in pit])
wt_g = np.array([float(r["wt_lb"]) for r in pit]) * LB_G
screens = [r["screen"] for r in pit]

N_rec = n_frag.sum()
W_rec = wt_g.sum()
print("=== (A) pit-screen-recovery.csv, re-baselined ===")
print(f"recovered count      N_rec = {N_rec:.0f}   (thread + script use 803)")
print(f"recovered metal      W_rec = {W_rec:.1f} g = {W_rec/LB_G:.3f} lb")
print(f"mean recovered mass        = {W_rec/N_rec:.3f} g  (thread quotes 6.85 g)")
print(f"  same weight basis / 803  = {W_rec/803:.3f} g")
for s, n, w in zip(screens, n_frag, wt_g):
    print(f"  screen {s:>5s}: n={n:5.0f}  w={w:8.1f} g  mean={w/n:8.2f} g")

# recovery fraction the source states: 95.6 % of empty shell & fuze (13.29 lb)
PCT_METAL = wt_g.sum() / (13.29 * LB_G)
print(f"recovered / 13.29 lb       = {100*PCT_METAL:.1f} %  (source: 95.6 %)")

# --------------------------------------------------- Tolch A->D falloff ratio
# NOTE: perf(D)/perf(A) below understates the true fragment-density ratio A->D
# -- both panels apply the same fixed perforation threshold, and a fixed
# threshold rejects proportionally more of the softer (lower-energy) part of
# the spectrum at D than at A, so the perforating-count ratio is biased toward
# 1 relative to the density ratio it stands in for.
side = load("side-spray-density")
static = {r["panel"]: r for r in side if float(r["v_fps"]) == 0}
ratio_AD = float(static["D"]["perf"]) / float(static["A"]["perf"])
print("\n=== (B) side-spray-density.csv, static row, A->D perforation ratio ===")
print(
    f"perf A={static['A']['perf']}  perf D={static['D']['perf']}  "
    f"ratio = {ratio_AD:.4f}   (thread uses 0.557)"
)

# ------------------------------------------------------------------ the model
shell = SHELLS["75mm M48 HE"]
rho = shell.steel.rho
r_o, r_i, r_bu, M_case = _shell_geometry(shell)
V0 = gurney_velocity(shell)
drag = DragParams()
mu, N0 = mott_params(shell, V0)
print("\n=== (C) model, 75mm M48 HE, current src/arty ===")
print(f"M_case = {M_case*1e3:.1f} g   V0 = {V0:.1f} m/s   C_D*C_shape = {drag.C_D*drag.C_shape:.3f}")
print(f"mu = {mu*1e3:.3f} g   2mu = {2*mu*1e3:.3f} g   N0 = {N0:.0f}")

# ------------------------------- (D) threshold rows, old vs re-baselined denom
# NOTE on admissibility: only the 126 J row is a criterion-matched sourced
# perforation threshold (Tolch's own smallest perforating hole, same experiment
# the model is scored against). The 78.6 J = 58 ft-lb figure is the Ordnance
# Dept. 1944 *personnel-casualty (incapacitation)* criterion — a different
# failure mechanism, never stated for wood — so its row is printed as a
# plausibility probe only and must NOT be cited as a sourced perforation
# threshold. See ../../../updates/sourced-wood-perforation-threshold/
# review-criterion-check.md.
print("\n=== (D) E_thr rows: N vs 700 perforating and vs re-baselined 779 ===")
E_rows = [
    (1.9, "fitted lo"),
    (3.6, "fitted hi"),
    (78.6, "1944 Ordnance casualty criterion, 58 ft-lb - NOT a perforation thr"),
    (126.0, "Tolch hole-size bound (criterion-matched sourced threshold)"),
    (294.5, "pre-anchor fitted"),
]
for E_thr, label in E_rows:
    m_thr = min_lethal_mass(4.572, V0, E_thr, drag, rho)
    N = mott_N(np.array([m_thr]), N0, mu)[0]
    print(
        f"  E_thr={E_thr:7.1f} J  m_thr={m_thr*1e3:7.3f} g  N={N:7.0f}  "
        f"N/700={N/700:5.2f}  N/803(old)={N/803:5.2f}  N/779(new)={N/N_rec:5.2f}"
    )

# ---------------- (E) THRESHOLD-FREE spectrum test enabled by the pit CSV -----
# Mott: N(>=m) = N0 exp(-x), x = sqrt(m/mu);
#       mass above m:  M(>=m)/M_tot = (x^2 + 2x + 2) e^{-x} / 2.
# For each Tolch screen boundary take the observed cumulative mass fraction phi
# (of the SAME basis as the model's total case mass), invert phi -> x, and
# compare the model's predicted count above that mass with Tolch's cumulative
# count. No E_thr, no drag, no panel geometry enters.
x = np.linspace(0.0, 30.0, 300_001)
phi_grid = (x**2 + 2 * x + 2) * np.exp(-x) / 2.0  # monotonically decreasing


def invert_phi(phi):
    """x such that (x^2+2x+2)e^-x/2 == phi (vectorised, monotone interp)."""
    return np.interp(phi, phi_grid[::-1], x[::-1])


cum_n = np.cumsum(n_frag)  # screens are printed coarsest -> finest
cum_w = np.cumsum(wt_g)

# Basis 1: fraction of the *model's* total case mass (Tolch's own 95.6 % of the
# metal is recovered, so the finest cumulative point sits at phi = 0.956, not 1).
print("\n=== (E) threshold-free spectrum test: matched cumulative mass fraction ===")
print("basis: model total case mass; Tolch recovered mass is 95.6 % of the metal")
for basis_name, M_tot in (("model M_case", M_case * 1e3), ("Tolch 13.29 lb", 13.29 * LB_G)):
    phi = cum_w / M_tot
    xs = invert_phi(phi)
    N_model = N0 * np.exp(-xs)
    m_star = mu * 1e3 * xs**2
    print(f"\n  --- basis = {basis_name} ({M_tot:.0f} g) ---")
    print("  through screen | cum n | cum w [g] |   phi  | m*[g] | N_model | ratio")
    for s, cn, cw, p, ms, nm in zip(screens, cum_n, cum_w, phi, m_star, N_model):
        print(
            f"  {s:>14s} | {cn:5.0f} | {cw:9.1f} | {p:6.4f} | {ms:5.2f} | "
            f"{nm:7.0f} | {nm/cn:5.2f}x"
        )

# Same test with the No.1 screen removed (the source calls those 6 pieces
# "mostly pieces of fuze", i.e. not case metal the Mott spectrum describes).
print("\n  --- fuze-excluded variant (drop No.1 screen from both count and mass) ---")
cum_n2 = np.cumsum(n_frag[1:])
cum_w2 = np.cumsum(wt_g[1:])
phi2 = cum_w2 / (M_case * 1e3)
xs2 = invert_phi(phi2)
N_model2 = N0 * np.exp(-xs2)
for s, cn, cw, p, nm in zip(screens[1:], cum_n2, cum_w2, phi2, N_model2):
    print(f"  {s:>14s} | {cn:5.0f} | {cw:9.1f} | {p:6.4f} | {nm:7.0f} | {nm/cn:5.2f}x")

# ------------- (F) the thread's own 0.63 g cut, re-based 803 -> 779 -----------
# CRITERION NOTE (2026-08-10, C5 closure). Each cut must be quoted against the
# denominator whose OWN census floor it is:
#   * 0.63 g is the pit test's finest screen cut  -> pair with 779 (pit census)
#   * a panel hole-size floor                     -> pair with 700 (panel perf)
# Pairing a panel-side floor with the pit denominator (the 0.36 g / 779 = 1.85x
# cell, quoted as C5's headline through 2026-08-10) is the same basis mix the
# open finding raises against block (D) and must not be cited.
print("\n=== (F) thread's fixed-mass cuts, re-based ===")
for cut_g in (0.63, 0.36, 0.166, 0.13, 0.05):
    N_above = mott_N(np.array([cut_g * 1e-3]), N0, mu)[0]
    print(
        f"  cut {cut_g:5.3f} g: N={N_above:7.0f}  N/700={N_above/700:5.2f}  "
        f"N/803(old)={N_above/803:5.2f}  N/779(new)={N_above/N_rec:5.2f}"
    )

# ------------------------------ (G) C5 detection-limit bound -----------------
# C5 asks whether Tolch's observed side is DETECTION-limited. The floor the
# thread proposed is the "smallest perforating hole", m >= 0.36 g at 838 m/s
# (the 126 J row). Two things this block establishes, both cited in
# count-chain.md sec.3 C5:
#   (i) 0.36 g is an UPPER bound on any detection floor (the smallest recorded
#       hole is >= the true floor), so the count it leaves is a LOWER bound on
#       the residual -- the most favourable number C5 can ever produce.
#  (ii) Read as a *perforation* datum instead, the same 0.36 g scales to the
#       panel-arrival condition through the shipped plug-shear law
#       (E_thr ~ m^(1/3), KE = m v^2/2  =>  m_thr ~ v^-3), which is where it
#       collides with C1 rather than adding to it.
print("\n=== (G) C5 detection-floor bound, criterion-matched denominator ===")
M_DET_G = 0.36  # Tolch smallest recorded perforating hole [g]
V_DET = 838.2  # m/s, Tolch Summary item 10 sidespray velocity
N_det = mott_N(np.array([M_DET_G * 1e-3]), N0, mu)[0]
N_verdict = 1756.0  # sec.2 verdict row, plug-shear m_thr = 0.166 g
print(f"  verdict row N = {N_verdict:.0f} -> N/700 = {N_verdict/700:.2f}x")
print(f"  floor {M_DET_G} g   N = {N_det:.0f} -> N/700 = {N_det/700:.2f}x   (MAX C5 credit)")
print(f"  realised C5 leverage = {N_verdict/N_det:.3f}x  (sec.4 INDETERMINATE gate: < 1.5x)")
print(f"  mixed-basis cell NOT to be cited: N/779 = {N_det/N_rec:.2f}x")
# (ii) same datum read as a perforation observation, rescaled to 612 m/s
m_thr_verdict = 0.166  # g, plug-shear at the 15 ft panel
v_panel = 612.0  # m/s, arrival velocity of that fragment (sec.2)
m_model_at_vdet = m_thr_verdict * (v_panel / V_DET) ** 3
print(
    f"  plug-shear m_thr rescaled to {V_DET:.0f} m/s = {m_model_at_vdet:.3f} g "
    f"vs Tolch's smallest observed perforation {M_DET_G} g "
    f"-> model permissive by {M_DET_G/m_model_at_vdet:.1f}x in mass"
)
