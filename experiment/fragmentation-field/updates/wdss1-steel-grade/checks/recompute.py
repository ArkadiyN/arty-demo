"""Re-derive the WDSS-1 steel-grade parameters and every number in derivation.md.

Run:  uv run python experiment/fragmentation-field/updates/wdss1-steel-grade/checks/recompute.py

Kept alongside derivation.md deliberately: gamma is a *composition*-driven
parameter, so any change to a cited composition band (or to the Mott table
reading) requires re-deriving it. Edit the CARBON constants below and re-run —
every table in derivation.md is regenerated from this one script.

Sources for the inputs:
  Mott 1947 sec.3 table  -> doc-reference/fragmentation/gurney-equations-fragmentation/
                            tables/section3-gamma-vs-composition.csv,
                            anchor "Some values of" (re-extracted 2026-07-25;
                            the earlier OCR of this table was wrong -- see the
                            "Extraction note" at the top of that file)
  WDSS-1 composition     -> doc-reference/ww2-shells/ammunition-series-6-wdss-specs/
                            ammunition-series-6-wdss-specs.md  (Ammunition Series 6,
                            Table 6-1, 17 Feb 1953)
  Baseline WD-X1335      -> doc-reference/ww2-shells/ordnance-105mm-m1-1940/card.md
                            (BOM p.16, spec 57-107) + AISI 1335 equivalence,
                            doc-reference/azom-steel-grades/aisi-1335/aisi-1335.md
"""

import csv
from dataclasses import replace
from pathlib import Path

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
# READ FROM THE CSV, never hand-copied (.claude/rules/source-data-fidelity.md,
# "Numbers are extracted once, not re-typed"). gamma is dimensionless, so it is
# immune to the scan's stress-column unit ambiguity; "iron" is at 0.0 %C.
# NOTE the row spacing is NON-UNIFORM (0 / 0.1 / 0.25 / 0.45 %C) -- do not assume
# a 0.1 %C grid; the quadratic below therefore uses divided differences.
_CSV = (
    Path(__file__).resolve().parents[5]
    / "doc-reference/fragmentation/gurney-equations-fragmentation"
    / "tables/section3-gamma-vs-composition.csv"
)


def _load_mott_table() -> list[dict]:
    """Return the Mott sec.3 rows as dicts with float carbon/RA/P_F/P_2/gamma."""
    with _CSV.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("carbon_pct", "reduction_in_area", "P_F_kg_per_mm2", "P_2_kg_per_mm2", "gamma"):
            r[k] = float(r[k])
    return rows


MOTT_ROWS = _load_mott_table()
MOTT_SERIES = [(r["carbon_pct"], r["gamma"]) for r in MOTT_ROWS]

# Closure-recomputed column (rebaseline-verdict.md sect.1). Mott's own
# gamma ~ 160 P_2 / (P_F (1+s_F)) reproduces the iron/0.1C/0.25C rows to <=3.2 %
# when s_F is read as the engineering fracture strain RA/(1-RA) *without* the
# printed "+1"; the 0.45 %C row does not reproduce (55.9 vs printed 67) and its
# P_2 = 38 breaks the column's own monotone rise. Baseline WD-X1335 sits in the
# 0.25-0.45 %C segment, i.e. its upper bracket is that indicted row, so the
# baseline gamma' is re-anchored on this recomputed column (verdict sect. 3.2).
MOTT_CLOSURE_COEFF = 160.0


def _gamma_closure(row: dict) -> float:
    """Return Mott's closure-formula gamma [-] for one table row (verdict sect.1)."""
    ra = row["reduction_in_area"]
    s_f = ra / (1.0 - ra)
    return MOTT_CLOSURE_COEFF * row["P_2_kg_per_mm2"] / (row["P_F_kg_per_mm2"] * s_f)


MOTT_SERIES_RECOMPUTED = [(r["carbon_pct"], _gamma_closure(r)) for r in MOTT_ROWS]

WDSS1_CARBON = (0.14, 0.20)      # Ammunition Series 6 Table 6-1
BASELINE_CARBON = (0.33, 0.38)   # WD-X1335 ~ AISI 1335 (unconfirmed; see A8)
BASELINE_ALT_CARBON = 0.40       # SAE 1040, the equally plausible alternate analog
SIGMA_F = 800e6                  # [Pa] held; only R = sigma_f/gamma is observable
BASELINE_GAMMA_LEGACY = 65.0     # the pre-2026-08-08 catalogued value (superseded)
BASELINE_GAMMA_SHIPPED = 54.5    # as catalogued in STEELS today (sect.9 re-anchor)
N_R = 20001                      # R50 grid: the shipped default (200) quantises to 1.5 m

M_REF = 0.5e-3                   # [kg] reference mass for the N(>0.5 g) validation band


# --- gamma interpolants -----------------------------------------------------


def gamma_linear(c: float, series: list | None = None) -> float:
    """Return Mott gamma [-] at carbon fraction c [%] by local-linear interpolation."""
    series = MOTT_SERIES if series is None else series
    for (c0, g0), (c1, g1) in zip(series, series[1:]):
        if c0 <= c <= c1:
            return g0 + (g1 - g0) * (c - c0) / (c1 - c0)
    # beyond the last row: extrapolate on the final segment's slope
    (c0, g0), (c1, g1) = series[-2], series[-1]
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


def reanchor_report() -> None:
    """Print sect.9: the baseline gamma' re-anchor onto the closure-recomputed column."""
    b_lo, b_hi = BASELINE_CARBON
    b_mid = 0.5 * (b_lo + b_hi)

    print("=== sect.9  Baseline gamma' re-anchor (rebaseline-verdict sect.3.2) ===\n")
    print("Mott sec.3 column: printed vs closure-recomputed 160 P_2/(P_F s_F), s_F=RA/(1-RA)")
    for (c, g_p), (_, g_r) in zip(MOTT_SERIES, MOTT_SERIES_RECOMPUTED):
        print(f"  c={c:5.2f} %C   printed={g_p:6.2f}   recomputed={g_r:6.2f}"
              f"   dev={100 * (g_r / g_p - 1):+6.1f} %")

    print("\nlocal-linear interpolation of each column:")
    for c in (b_lo, b_mid, b_hi):
        print(f"  c={c:.3f} %C   printed-col={gamma_linear(c):6.2f}   "
              f"recomputed-col={gamma_linear(c, MOTT_SERIES_RECOMPUTED):6.2f}")
    c_wd = 0.5 * sum(WDSS1_CARBON)
    print(f"  (WDSS-1 {c_wd:.3f} %C  printed-col={gamma_linear(c_wd):6.2f}   "
          f"recomputed-col={gamma_linear(c_wd, MOTT_SERIES_RECOMPUTED):6.2f}"
          f"  -> both round to {round(gamma_linear(c_wd, MOTT_SERIES_RECOMPUTED)):.0f})")

    print(f"\nAdopted baseline gamma' = {BASELINE_GAMMA_SHIPPED} "
          f"(was {BASELINE_GAMMA_LEGACY}); composition band "
          f"{gamma_linear(b_lo, MOTT_SERIES_RECOMPUTED):.1f}-"
          f"{gamma_linear(b_hi, MOTT_SERIES_RECOMPUTED):.1f}")
    print(f"  R = sigma_F/gamma' : {SIGMA_F / BASELINE_GAMMA_LEGACY / 1e6:.3f} -> "
          f"{SIGMA_F / BASELINE_GAMMA_SHIPPED / 1e6:.3f} MPa "
          f"({100 * (BASELINE_GAMMA_LEGACY / BASELINE_GAMMA_SHIPPED - 1):+.1f} %)")

    print("\nPer-shell effect of the re-anchor (all four catalog shells):")
    from arty.shells import SHELLS

    hdr = f"{'shell':16s} {'alpha':>6s} {'gamma old':>9s} {'gamma new':>9s} " \
          f"{'mu old':>8s} {'mu new':>8s} {'N0 old':>8s} {'N0 new':>8s} " \
          f"{'N>0.5g old':>10s} {'N>0.5g new':>10s}"
    print(hdr)
    for name, base_shell in SHELLS.items():
        row = [name]
        vals = {}
        for tag, g in (("old", BASELINE_GAMMA_LEGACY), ("new", BASELINE_GAMMA_SHIPPED)):
            steel = SteelParams(name="x", rho=7850.0, sigma_f=SIGMA_F, gamma=g)
            sh = replace(base_shell, steel=steel)
            v0 = gurney_velocity(sh)
            mu, n0 = mott_params(sh, v0)
            r_o, r_i, r_bu, _ = _shell_geometry(sh)
            t_bu = sh.wall_t * 0.5 * (r_o + r_i) / r_bu
            x0 = np.sqrt(2.0 * SIGMA_F / (7850.0 * g)) * r_bu / v0
            alpha = sh.aspect_ratio * sh.breadth_factor**2 * t_bu / x0
            vals[tag] = (alpha, alpha ** (-2 / 3) * g, mu * 1e3, n0,
                         n0 * np.exp(-np.sqrt(M_REF / mu)))
        o, n = vals["old"], vals["new"]
        print(f"{row[0]:16s} {n[0]:6.2f} {o[1]:9.1f} {n[1]:9.1f} "
              f"{o[2]:8.3f} {n[2]:8.3f} {o[3]:8.0f} {n[3]:8.0f} "
              f"{o[4]:10.0f} {n[4]:10.0f}")
    print()


def main() -> None:
    print(f"Geometry: V0={V0:.4f} m/s  r_bu={R_BU:.6f} m  M_shell={M_SHELL:.4f} kg\n")
    reanchor_report()

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
