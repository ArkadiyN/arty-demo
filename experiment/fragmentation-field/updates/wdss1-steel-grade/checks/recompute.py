"""Re-derive the WDSS-1 steel-grade parameters and every number in derivation.md.

Run:  uv run python experiment/fragmentation-field/updates/wdss1-steel-grade/checks/recompute.py

Kept alongside derivation.md deliberately: gamma is a *composition*-driven
parameter, so any change to a cited composition band (or to the Mott table
reading) requires re-deriving it. Edit the CARBON constants below and re-run —
every table in derivation.md is regenerated from this one script.

Sources for the inputs:
  Mott 1947 sec.3 table  -> doc-reference/fragmentation/gurney-equations-fragmentation/
                            rspa.1947.0042.md lines 305-310 (re-extracted 2026-07-25;
                            the earlier OCR of this table was wrong -- see the
                            "Extraction note" at the top of that file)
  WDSS-1 composition     -> doc-reference/ww2-shells/ammunition-series-6-wdss-specs/
                            ammunition-series-6-wdss-specs.md  (Ammunition Series 6,
                            Table 6-1, 17 Feb 1953)
  Baseline WD-X1335      -> doc-reference/ww2-shells/ordnance-105mm-m1-1940/card.md
                            (BOM p.16, spec 57-107) + AISI 1335 equivalence,
                            doc-reference/azom-steel-grades/aisi-1335/aisi-1335.md
"""

import numpy as np

from arty.fragmentation import (
    ShellParams,
    SteelParams,
    _shell_geometry,
    compute_frag_field,
    gurney_velocity,
    mott_params,
)

# --- Inputs -----------------------------------------------------------------

# Mott 1947 sec.3 p.308, after Koerber & Rohland (1924): (carbon %, gamma).
# gamma is dimensionless, so it is immune to the scan's stress-column unit
# ambiguity. "iron" is entered at 0.0 %C.
# NOTE the row spacing is NON-UNIFORM (0 / 0.1 / 0.25 / 0.45 %C) -- do not assume
# a 0.1 %C grid; the quadratic below therefore uses divided differences.
MOTT_SERIES = [(0.0, 20.0), (0.1, 42.0), (0.25, 53.0), (0.45, 67.0)]

WDSS1_CARBON = (0.14, 0.20)      # Ammunition Series 6 Table 6-1
BASELINE_CARBON = (0.33, 0.38)   # WD-X1335 ~ AISI 1335 (unconfirmed; see A8)
BASELINE_ALT_CARBON = 0.40       # SAE 1040, the equally plausible alternate analog
SIGMA_F = 800e6                  # [Pa] held; only R = sigma_f/gamma is observable
BASELINE_GAMMA_SHIPPED = 65.0    # as catalogued in STEELS today
N_R = 20001                      # R50 grid: the shipped default (200) quantises to 1.5 m

M_REF = 0.5e-3                   # [kg] reference mass for the N(>0.5 g) validation band


# --- gamma interpolants -----------------------------------------------------


def gamma_linear(c: float) -> float:
    """Return Mott gamma [-] at carbon fraction c [%] by local-linear interpolation."""
    for (c0, g0), (c1, g1) in zip(MOTT_SERIES, MOTT_SERIES[1:]):
        if c0 <= c <= c1:
            return g0 + (g1 - g0) * (c - c0) / (c1 - c0)
    # beyond the last row: extrapolate on the final segment's slope
    (c0, g0), (c1, g1) = MOTT_SERIES[-2], MOTT_SERIES[-1]
    return g1 + (g1 - g0) * (c - c1) / (c1 - c0)


def gamma_quadratic(c: float) -> float:
    """Return Mott gamma [-] at carbon c [%] via Newton quadratic on the 3 steel rows.

    Divided-difference form, because the tabulated carbon spacing is non-uniform.
    """
    (c0, g0), (c1, g1), (c2, g2) = MOTT_SERIES[1:]
    d01 = (g1 - g0) / (c1 - c0)
    d12 = (g2 - g1) / (c2 - c1)
    d012 = (d12 - d01) / (c2 - c0)
    return g0 + d01 * (c - c0) + d012 * (c - c0) * (c - c1)


def carbon_for_gamma(g: float) -> float:
    """Return the carbon fraction [%] whose local-linear Mott gamma equals g [-]."""
    for (c0, g0), (c1, g1) in zip(MOTT_SERIES, MOTT_SERIES[1:]):
        if g0 <= g <= g1:
            return c0 + (c1 - c0) * (g - g0) / (g1 - g0)
    (c0, g0), (c1, g1) = MOTT_SERIES[-2], MOTT_SERIES[-1]
    return c1 + (c1 - c0) * (g - g1) / (g1 - g0)


# --- model evaluation -------------------------------------------------------

_BASE = ShellParams()
V0 = gurney_velocity(_BASE)
_, _, R_BU, M_SHELL = _shell_geometry(_BASE)


def evaluate(gamma: float, sigma_f: float = SIGMA_F, with_r50: bool = True) -> dict:
    """Return {R [MPa], mu [g], N0 [-], n_gt [-], r50 [m]} for one steel gamma [-]."""
    shell = ShellParams(steel=SteelParams(name="x", rho=7850.0, sigma_f=sigma_f, gamma=gamma))
    mu, n0 = mott_params(shell, V0)
    out = {
        "R": sigma_f / gamma / 1e6,
        "mu": mu * 1e3,
        "N0": n0,
        "n_gt": n0 * np.exp(-np.sqrt(M_REF / mu)),
        "r50": float("nan"),
    }
    if with_r50:
        out["r50"] = compute_frag_field(shell=shell, n_r=N_R).r50
    return out


def _line(label: str, gamma: float, **kw) -> dict:
    v = evaluate(gamma, **kw)
    print(
        f"{label:30s} gamma={gamma:6.2f}  R={v['R']:6.3f} MPa  mu={v['mu']:.4f} g  "
        f"N0={v['N0']:8.0f}  N(>0.5g)={v['n_gt']:7.0f}  R50={v['r50']:7.3f} m"
    )
    return v


def main() -> None:
    print(f"Geometry: V0={V0:.4f} m/s  r_bu={R_BU:.6f} m  M_shell={M_SHELL:.4f} kg\n")

    c_lo, c_hi = WDSS1_CARBON
    c_mid = 0.5 * (c_lo + c_hi)
    b_lo, b_hi = BASELINE_CARBON
    b_mid = 0.5 * (b_lo + b_hi)

    print("gamma interpolation (Mott sec.3, local-linear / quadratic):")
    for c in (c_lo, c_mid, c_hi, b_mid):
        print(f"  c={c:.3f} %C   linear={gamma_linear(c):6.3f}   quad={gamma_quadratic(c):6.3f}")

    gamma_adopted = round(gamma_linear(c_mid))
    print(f"\nAdopted WDSS-1 gamma = {gamma_adopted:.0f} (band "
          f"{round(gamma_linear(c_lo)):.0f}-{round(gamma_linear(c_hi)):.0f})\n")

    print("Sec.4 parameter table:")
    base = _line("baseline WD-X1335 (shipped)", BASELINE_GAMMA_SHIPPED)
    ad = _line(f"WDSS-1 {c_mid:.2f} %C adopted", gamma_adopted)
    _line(f"WDSS-1 band low {c_lo:.2f} %C", round(gamma_linear(c_lo)))
    _line(f"WDSS-1 band high {c_hi:.2f} %C", round(gamma_linear(c_hi)))

    print(
        f"\nContrast vs shipped baseline: mu {100 * (ad['mu'] / base['mu'] - 1):+.1f}%  "
        f"N0 {100 * (ad['N0'] / base['N0'] - 1):+.1f}%  "
        f"N(>0.5g) {100 * (ad['n_gt'] / base['n_gt'] - 1):+.1f}%  "
        f"R50 {ad['r50'] - base['r50']:+.2f} m ({100 * (ad['r50'] / base['r50'] - 1):+.1f}%)"
    )

    print("\nC6 - interpolant / rounding sensitivity:")
    for lbl, g in (
        ("local-linear unrounded", gamma_linear(c_mid)),
        ("Newton quadratic", gamma_quadratic(c_mid)),
        ("adopted (rounded)", float(gamma_adopted)),
    ):
        v = evaluate(g, with_r50=False)
        print(f"  {lbl:24s} gamma={g:6.3f}  mu={v['mu']:.4f} g  N0={v['N0']:8.0f}")

    print(f"\nC7 - rule-consistent baseline gamma (WD-X1335 midpoint {b_mid:.3f} %C;"
          f" both brackets are INTERPOLATION on the 0.25-0.45 %C row pair):")
    print(f"  gamma = {BASELINE_GAMMA_SHIPPED:.0f} implies carbon "
          f"{carbon_for_gamma(BASELINE_GAMMA_SHIPPED):.3f} %C by the same rule")
    for lbl, g in (
        ("shipped (catalogued)", BASELINE_GAMMA_SHIPPED),
        ("quadratic @0.355 %C", gamma_quadratic(b_mid)),
        ("linear @0.355 %C", gamma_linear(b_mid)),
        ("linear @0.40 %C (SAE 1040)", gamma_linear(BASELINE_ALT_CARBON)),
    ):
        v = evaluate(g, with_r50=False)
        print(
            f"  {lbl:28s} gamma={g:6.2f}  N0={v['N0']:8.0f}  N(>0.5g)={v['n_gt']:7.0f}"
            f"   -> WDSS-1 N0 contrast {100 * (ad['N0'] / v['N0'] - 1):+.1f}%"
        )

    print("\nC2 - identifiability, (k*sigma_f, k*gamma) invariance:")
    for k in (0.5, 2.0, 137.0):
        v = evaluate(k * gamma_adopted, sigma_f=k * SIGMA_F, with_r50=False)
        print(
            f"  k={k:6.1f}  d(mu)={abs(v['mu'] - ad['mu']) / ad['mu']:.3e}"
            f"  d(N0)={abs(v['N0'] - ad['N0']) / ad['N0']:.3e}"
        )

    print("\nC5 - brittle limit:")
    v = evaluate(1e6, with_r50=False)
    print(f"  gamma=1e6:  mu={v['mu']:.3e} g   N0={v['N0']:.3e}")

    print("\nC8 - R50 vs gamma sweep:")
    for g in (35.0, 40.0, 45.0, 47.0, 49.0, 53.0, 57.0, 60.0, 65.0, 72.0):
        print(f"  gamma={g:5.1f}   R50={evaluate(g)['r50']:7.3f} m")


if __name__ == "__main__":
    main()
