"""C4 spectrum-denominator basis test for the count-gap-1938 thread.

Produces the sensitivity table in
experiment/fragmentation-field/challenges/count-gap-1938/spectrum-mass-basis.md
(section 3, "Sensitivity to 'mostly'") and the denominator-comparison figures
quoted in sections 0 and 3.

Question settled: which metal weight is the criterion-correct denominator for
the threshold-free Mott spectrum comparison -- Tolch's 10.94 lb empty *unfuzed*
shell (case metal) or his 13.29 lb "empty shell & fuze" pit-recovery basis.

All Tolch series read from the checked-in, closure-checked CSVs; nothing typed.

Run: uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-spectrum-basis.py
"""

import csv
from pathlib import Path

import numpy as np

from arty.fragmentation import _shell_geometry, gurney_velocity, mott_params
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


pit = load("pit-screen-recovery")
n_frag = np.array([float(r["n_frag"]) for r in pit])
wt_g = np.array([float(r["wt_lb"]) for r in pit]) * LB_G
screens = [r["screen"] for r in pit]

rw = load("round-weights")
loaded_unfuzed = np.array([float(r["loaded_unfuzed_lb"]) for r in rw])
fuze_lb = np.array([float(r["fuze_lb"]) for r in rw])
tnt_lb = np.array([float(r["tnt_lb"]) for r in rw])
empty_fuze_lb = np.array([float(r["empty_and_fuze_lb"]) for r in rw])

CASE_LB = (loaded_unfuzed - tnt_lb).mean()          # 10.94 lb, empty UNFUZED shell
EMPTY_FUZE_LB = empty_fuze_lb.mean()                # 13.29 lb, empty shell & fuze
FUZE_G = fuze_lb.mean() * LB_G

print("=== (A) what each Tolch metal weight is ===")
print(f"  loaded unfuzed shell   = {loaded_unfuzed.mean():.2f} lb  (case metal + TNT)")
print(f"  TNT charge             = {tnt_lb.mean():.2f} lb")
print(f"  fuze (M39 P.D.)        = {fuze_lb.mean():.2f} lb = {FUZE_G:.0f} g")
print(f"  -> case metal alone    = {CASE_LB:.2f} lb = {CASE_LB*LB_G:.0f} g   [10.94 lb]")
print(f"  -> empty shell & fuze  = {EMPTY_FUZE_LB:.2f} lb = {EMPTY_FUZE_LB*LB_G:.0f} g  [13.29 lb]")
print(f"  closure: case + fuze   = {(CASE_LB + fuze_lb.mean()):.2f} lb "
      f"(printed {EMPTY_FUZE_LB:.2f}) -> {'OK' if abs(CASE_LB+fuze_lb.mean()-EMPTY_FUZE_LB) < 0.01 else 'FAIL'}")

shell = SHELLS["75mm M48 HE"]
_, _, _, M_case = _shell_geometry(shell)
M_case_g = M_case * 1e3
V0 = gurney_velocity(shell)
mu, N0 = mott_params(shell, V0)
print("\n=== (B) model side, fuze-EXCLUDED by construction ===")
print(f"  mass_deductions (fuze+booster) = {shell.mass_deductions*1e3:.0f} g")
print(f"  M_case = {M_case_g:.1f} g   mu = {mu*1e3:.3f} g   N0 = {N0:.0f}")
print(f"  M_case vs Tolch 10.94 lb ({CASE_LB*LB_G:.0f} g): "
      f"{100*(M_case_g/(CASE_LB*LB_G) - 1):+.1f} %")
print(f"  M_case vs Tolch 13.29 lb ({EMPTY_FUZE_LB*LB_G:.0f} g): "
      f"{100*(M_case_g/(EMPTY_FUZE_LB*LB_G) - 1):+.1f} %")

# Mott mass-above-m fraction: M(>=m)/M_tot = (x^2 + 2x + 2) e^-x / 2, x = sqrt(m/mu)
x = np.linspace(0.0, 30.0, 300_001)
phi_grid = (x**2 + 2 * x + 2) * np.exp(-x) / 2.0


def invert_phi(phi):
    """x such that (x^2+2x+2)e^-x/2 == phi (vectorised, monotone interp)."""
    return np.interp(phi, phi_grid[::-1], x[::-1])


def band(cum_n, cum_w, M_tot):
    """Return (ratios, phi) for a cumulative census against total metal M_tot [g]."""
    phi = cum_w / M_tot
    return N0 * np.exp(-invert_phi(phi)) / cum_n, phi


print("\n=== (C) fuze-consistent pairing: census minus screen 1 vs case metal ===")
cum_n2 = np.cumsum(n_frag[1:])
cum_w2 = np.cumsum(wt_g[1:])
for label, M_tot in (
    ("model M_case      4980 g", M_case_g),
    ("Tolch 10.94 lb    4962 g", CASE_LB * LB_G),
):
    r, phi = band(cum_n2, cum_w2, M_tot)
    cells = "  ".join(f"{s}:{v:.2f}x" for s, v in zip(screens[1:], r))
    print(f"  {label} -> {cells}   band {r.min():.2f}-{r.max():.2f}x")

print("\n=== (D) fuze-inclusive consistent pairing: full census vs 13.29 lb ===")
r, phi = band(np.cumsum(n_frag), np.cumsum(wt_g), EMPTY_FUZE_LB * LB_G)
cells = "  ".join(f"{s}:{v:.2f}x" for s, v in zip(screens, r))
print(f"  {cells}\n  band over screens 2..thru4 = {r[1:].min():.2f}-{r[1:].max():.2f}x")

print("\n=== (E) INADMISSIBLE mixed basis: full census vs fuze-excluded M_case ===")
r, phi = band(np.cumsum(n_frag), np.cumsum(wt_g), M_case_g)
print(f"  phi at finest cut = {phi[-1]:.4f}  (> 1 => the mix is self-evident)")

# ---- sensitivity: Tolch says screen 1 is "mostly" fuze, not entirely --------
print("\n=== (F) sensitivity to 'mostly': f = fuze fraction of screen-1 mass ===")
W1, N1 = wt_g[0], n_frag[0]
W_case_rec = wt_g[1:].sum()  # recovered mass on screens 2..thru4, all case metal
# Mass closure: recovered case metal cannot exceed the case. That bounds f.
f_min = 1.0 - (M_case_g - W_case_rec) / W1
print(f"  recovered case metal (screens 2..thru4) = {W_case_rec:.1f} g of "
      f"M_case {M_case_g:.0f} g")
print(f"  mass closure requires f >= {f_min:.3f}  "
      f"(else recovered case metal exceeds the case)")
print(f"  screen-1 mass {W1:.1f} g vs whole fuze {FUZE_G:.0f} g: f = 1.0 is "
      f"physically available")
print("\n  f     w_fuze[g]  case added back[g]  phi(thru4)  ratios (scr 2,3,4,thru4)      band")
for f in (0.70, 0.85, f_min, 0.90, 0.95, 1.00):
    w_fuze = min(f * W1, FUZE_G)
    w_back = W1 - w_fuze
    n_back = (1.0 - f) * N1
    cn = np.cumsum(np.concatenate(([n_back], n_frag[1:])))
    cw = np.cumsum(np.concatenate(([w_back], wt_g[1:])))
    with np.errstate(divide="ignore", invalid="ignore"):
        r, phi = band(cn, cw, M_case_g)
    cells = " ".join(f"{v:5.2f}x" for v in r[1:])
    flag = "  <- phi>=1, degenerate" if phi[-1] >= 1.0 else ""
    print(f"  {f:4.3f}  {w_fuze:8.1f}  {w_back:17.1f}  {phi[-1]:9.4f}   {cells}   "
          f"{r[1:].min():.2f}-{r[1:].max():.2f}x{flag}")

print("\n  CONDITIONING: the finest cut sits at phi -> 1, where dx/dphi diverges,")
print("  so its ratio is ill-conditioned in f. The screen-2 cut (phi ~ 0.77) is")
print("  the well-conditioned anchor; over the closure-admissible f in [%.2f, 1.0]" % f_min)
rs = []
for f in np.linspace(f_min, 1.0, 21):
    w_back = W1 - min(f * W1, FUZE_G)
    n_back = (1.0 - f) * N1
    cn = np.cumsum(np.concatenate(([n_back], n_frag[1:])))
    cw = np.cumsum(np.concatenate(([w_back], wt_g[1:])))
    with np.errstate(divide="ignore", invalid="ignore"):
        r, _ = band(cn, cw, M_case_g)
    rs.append(r[1])
print(f"  it moves only {min(rs):.2f}x - {max(rs):.2f}x.")
