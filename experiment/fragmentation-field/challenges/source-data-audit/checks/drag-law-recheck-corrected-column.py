"""Re-runs the 1944-Ordnance drag-law evidence on the CORRECTED (casualties)
column.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          phase4-drag-law-assessment.md  (verdicts 1 and 2)

Every series is read from the verified CSVs under
doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/
-- no hand-typed array.  That is the defect this pass audits: the previous
scripts (drag-gap-1944/checks/drag-coefficient-calibration.py,
updates/mach-dependent-fragment-drag/checks/drag-anchor-validation.py) typed a
75-casualties / 105-PERFORATION / 155-casualties mixture into one DATA block.

Reproduces, on both the old mixed set and the corrected casualties set:
  * per-point required combined C_D*C_shape and its implied ballistic density k
  * RMS ln(v_model/v_source) at 0.585 (pre-change), 2.674 (adopted) and at the
    best-fit constant
  * the constant-vs-Fig-3-Mach-integration comparison (derivation.md sec 5)

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/drag-law-recheck-corrected-column.py
"""
import csv
import os

import numpy as np

from arty.shells import SHELLS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
while not os.path.isdir(os.path.join(REPO, "doc-reference")):
    REPO = os.path.dirname(REPO)
TABLES = os.path.join(
    REPO, "doc-reference", "wound-ballistics",
    "ordnance-dept-1944-shell-fragment-damage", "tables")

FT_TO_M = 0.3048
OZ_TO_KG = 0.028349523125
RHO_AIR = 1.225
A_SOUND = 340.3  # m/s, sea-level standard
RHO_STEEL = 7850.0

K_DOD = 2600.0   # kg/m3, DoD-1975 "Ballistic Properties", forged steel
CD_DOD = 1.28    # supersonic plateau, DoD-1975 Fig. 3
C_SHAPE = (RHO_STEEL / K_DOD) ** (2.0 / 3.0)
COMBINED_ADOPTED = CD_DOD * C_SHAPE
COMBINED_OLD = 0.65 * 0.90  # 0.585, the pre-change arty default

# V0 anchors: ordnance-1944.md, the "INITIAL FRAGMENT VELOCITY" line directly
# under each shell heading -- "# 75-MM H.E. SHELL, M48" -> 3,120 F/S;
# "# 105-MM H.E. SHELL,'Ml" -> 3,500 F/S; "# 155-MM N.E. SHELL, M107" -> 3,500.
SHELL_INFO = {
    "75mm-m48": ("75mm M48 HE", 3120.0),
    "105mm-m1": ("105mm M1 HE", 3500.0),
    "155mm-m107": ("155mm M107 HE", 3500.0),
}

# DoD-1975 Figure 3, digitized (doc-reference/fragmentation/
# dod-1975-fragment-debris-hazards/figure-3-digitized.md)
MACH = np.array([0.0, 0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.2, 2.6, 3.0, 4.0, 5.0, 7.0])
CD_CURVE = np.array([1.08, 1.09, 1.10, 1.14, 1.38, 1.40, 1.35, 1.33, 1.30, 1.29,
                     1.28, 1.28, 1.28, 1.28])


def load(slug, column):
    """Rows (r_m, m_kg, v_ms, rho_steel, V0_ms) from tables/<slug>-<column>.csv."""
    name, v0_fts = SHELL_INFO[slug]
    rho_s = SHELLS[name].steel.rho
    v0 = v0_fts * FT_TO_M
    out = []
    with open(os.path.join(TABLES, f"{slug}-{column}.csv")) as fh:
        for row in csv.DictReader(fh):
            out.append((float(row["r_ft"]) * FT_TO_M,
                        float(row["m_oz"]) * OZ_TO_KG,
                        float(row["v_fps"]) * FT_TO_M,
                        rho_s, v0))
    return out


def lam(m, combined, rho_steel=RHO_STEEL):
    """Retardation coefficient [1/m] for fragment mass m [kg] (arty form)."""
    return RHO_AIR * combined / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)


def required_combined(r, m, v, rho_steel, v0):
    """Combined C_D*C_shape that reproduces this (r, m, v) point exactly [-]."""
    return (-np.log(v / v0) / r) * 2.0 * rho_steel ** (2.0 / 3.0) / RHO_AIR * m ** (1.0 / 3.0)


def _resid(rows, combined, idx=None):
    """ln(v_model/v_source) [-]; `combined` may be an array (broadcast on a new axis)."""
    r, m, v, rho_s, v0 = _cols(rows, idx)
    return np.log(v0 * np.exp(-lam(m, combined, rho_s) * r) / v)


def rms(rows, combined, idx=None):
    """RMS of ln(v_model/v_source) [-]."""
    return float(np.sqrt(np.mean(np.square(_resid(rows, combined, idx)))))


def best_constant(rows, idx=None):
    """Combined constant minimising RMS ln-residual [-], plus that RMS."""
    grid = np.linspace(0.2, 8.0, 15601)
    vals = np.sqrt(np.mean(np.square(_resid(rows, grid[:, None], idx)), axis=1))
    i = int(np.argmin(vals))
    return float(grid[i]), float(vals[i])


def integrate_fig3(m, v0, r_end, rho_steel, c_shape, n=4000):
    """v(r_end) [m/s] with C_D = C_D(Mach) along the path (RK2, velocity-squared law).

    Fully broadcast: every argument may be an array, and the whole ensemble
    marches through the same n steps at once. A C_shape sweep is therefore one
    n-step march over a (grid x points) array, not one march per combination.
    """
    m, v0, r_end, rho_steel, c_shape = np.broadcast_arrays(
        *(np.asarray(a, dtype=float) for a in (m, v0, r_end, rho_steel, c_shape)))
    dx = r_end / n
    v = np.array(v0, dtype=float)
    base = RHO_AIR * c_shape / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)
    for _ in range(n):
        k1 = -base * np.interp(v / A_SOUND, MACH, CD_CURVE) * v
        v2 = v + 0.5 * dx * k1
        k2 = -base * np.interp(v2 / A_SOUND, MACH, CD_CURVE) * v2
        v = v + dx * k2
    return v


def _cols(rows, idx=None):
    """Columns (r_m, m_kg, v_ms, rho_steel, V0_ms) as arrays, for the selected rows."""
    idx = range(len(rows)) if idx is None else idx
    return [np.array(c, dtype=float) for c in zip(*(rows[i] for i in idx))]


def rms_fig3(rows, c_shape, idx=None):
    """RMS ln-residual [-] of the Fig-3 Mach-integrated law at shape factor c_shape."""
    r, m, v, rho_s, v0 = _cols(rows, idx)
    e = np.log(integrate_fig3(m, v0, r, rho_s, c_shape) / v)
    return float(np.sqrt(np.mean(np.square(e))))


def best_fig3(rows, idx=None):
    """C_shape minimising the Fig-3 law's RMS ln-residual [-], plus that RMS."""
    grid = np.linspace(0.5, 6.0, 551)
    r, m, v, rho_s, v0 = _cols(rows, idx)
    # one n-step march over the full (grid x points) ensemble
    vend = integrate_fig3(m, v0, r, rho_s, grid[:, None])
    vals = np.sqrt(np.mean(np.square(np.log(vend / v)), axis=1))
    i = int(np.argmin(vals))
    return float(grid[i]), float(vals[i])


def mach_subset(rows, m_min=0.7):
    return [i for i, r in enumerate(rows) if r[2] / A_SOUND > m_min]


def report(label, rows):
    sel = mach_subset(rows)
    print(f"\n### {label}   n = {len(rows)}   n(arrival M>0.7) = {len(sel)}")
    print(f"  RMS ln(v_mod/v_src)  @0.585 (pre-change) : all {rms(rows, COMBINED_OLD):.3f}"
          f"   M>0.7 {rms(rows, COMBINED_OLD, sel):.3f}")
    print(f"  RMS ln(v_mod/v_src)  @{COMBINED_ADOPTED:.3f} (adopted)  : all "
          f"{rms(rows, COMBINED_ADOPTED):.3f}   M>0.7 {rms(rows, COMBINED_ADOPTED, sel):.3f}")
    b_all, r_all = best_constant(rows)
    b_sub, r_sub = best_constant(rows, sel)
    print(f"  best constant, all    : {b_all:.3f}  (RMS {r_all:.3f})  "
          f"-> k = {RHO_STEEL / (b_all / CD_DOD) ** 1.5:.0f} kg/m3")
    print(f"  best constant, M>0.7  : {b_sub:.3f}  (RMS {r_sub:.3f})  "
          f"-> k = {RHO_STEEL / (b_sub / CD_DOD) ** 1.5:.0f} kg/m3")
    return b_all, r_all, b_sub, r_sub


if __name__ == "__main__":
    cas = {s: load(s, "casualties") for s in SHELL_INFO}
    perf = {s: load(s, "perforation-1-8in") for s in SHELL_INFO}

    print("=" * 78)
    print("A. Per-point required combined C_D*C_shape, corrected CASUALTIES column")
    print("=" * 78)
    for slug in SHELL_INFO:
        print(f"\n-- {SHELL_INFO[slug][0]}  (V0 = {SHELL_INFO[slug][1]:.0f} f/s)")
        print(f"{'r(ft)':>6} {'m(g)':>8} {'v(m/s)':>8} {'M_arr':>6} "
              f"{'req comb':>9} {'k(kg/m3)':>9}")
        for row in cas[slug]:
            r, m, v, rho_s, v0 = row
            rq = required_combined(r, m, v, rho_s, v0)
            print(f"{r / FT_TO_M:6.0f} {m * 1e3:8.3f} {v:8.1f} {v / A_SOUND:6.2f} "
                  f"{rq:9.3f} {RHO_STEEL / (rq / CD_DOD) ** 1.5:9.0f}")

    print("\n" + "=" * 78)
    print("B. Constant-drag fits: old mixed set vs corrected casualties set")
    print("=" * 78)

    # the set the shipped derivation actually used: 75mm 3 casualty points,
    # 105mm PERFORATION (11), 155mm casualties (11)
    old_mixed = ([r for r in cas["75mm-m48"] if round(r[0] / FT_TO_M) in (20, 100, 400)]
                 + perf["105mm-m1"] + cas["155mm-m107"])
    report("OLD mixed set (75 cas x3 / 105 PERF / 155 cas) - reproduces shipped V2",
           old_mixed)

    all_cas = cas["75mm-m48"] + cas["105mm-m1"] + cas["155mm-m107"]
    report("CORRECTED: all three casualties columns (full)", all_cas)

    cas_3pt75 = ([r for r in cas["75mm-m48"] if round(r[0] / FT_TO_M) in (20, 100, 400)]
                 + cas["105mm-m1"] + cas["155mm-m107"])
    report("CORRECTED, same point count as shipped (75mm restricted to 3 pts)",
           cas_3pt75)

    all_perf = perf["75mm-m48"] + perf["105mm-m1"] + perf["155mm-m107"]
    report("CONTRAST: all three PERFORATION columns", all_perf)

    for slug in SHELL_INFO:
        report(f"per-shell, casualties: {SHELL_INFO[slug][0]}", cas[slug])

    print("\n" + "=" * 78)
    print("C. Constant C_D vs Fig-3 Mach-dependent C_D(M)  (derivation.md sec 5)")
    print("=" * 78)
    for label, rows in [("OLD mixed set", old_mixed),
                        ("CORRECTED casualties (full)", all_cas)]:
        sel = mach_subset(rows)
        b_all, rc_all = best_constant(rows)
        b_sub, rc_sub = best_constant(rows, sel)
        cs_all, rm_all = best_fig3(rows)
        cs_sub, rm_sub = best_fig3(rows, sel)
        print(f"\n-- {label}   n = {len(rows)}, n(M>0.7) = {len(sel)}")
        print("  zero free parameters (both laws at the DoD anchor k = 2600):")
        print(f"    constant C_D=1.28, combined {COMBINED_ADOPTED:.3f} : "
              f"all {rms(rows, COMBINED_ADOPTED):.3f}   M>0.7 {rms(rows, COMBINED_ADOPTED, sel):.3f}")
        print(f"    Fig-3 C_D(M), C_shape = {C_SHAPE:.3f}         : "
              f"all {rms_fig3(rows, C_SHAPE):.3f}   M>0.7 {rms_fig3(rows, C_SHAPE, sel):.3f}")
        print("  one free scale parameter each, fitted on the metric reported:")
        print(f"    best constant  {b_all:.3f} (all) / {b_sub:.3f} (M>0.7) : "
              f"all {rc_all:.3f}   M>0.7 {rc_sub:.3f}")
        print(f"    best Fig-3     C_shape {cs_all:.3f} / {cs_sub:.3f}     : "
              f"all {rm_all:.3f}   M>0.7 {rm_sub:.3f}")
