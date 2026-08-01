"""Drag-coefficient calibration check: does raising combined C_D*C_shape into
the 1.2-1.7 literature range (dod-1975-fragment-debris-hazards card.md ~1.28;
sandia-sand92-0243 1.2-1.7 velocity-dependent) close the model-vs-source
velocity-decay gap already found in the three ordnance-1944-initial-
conditions-check-*.md files?

Reuses arty.fragmentation.retardation_coeff verbatim (no new formula) with
substituted DragParams(C_D, C_shape) so the product equals each candidate
combined value. Reuses the (m(r), v(r), V0) triples already tabulated in the
three existing check files verbatim.
"""
import numpy as np

from arty.shells import SHELLS
from arty.fragmentation import DragParams, retardation_coeff

FT_TO_M = 0.3048
FTS_TO_MS = 0.3048
OZ_TO_KG = 0.028349523125

CANDIDATES = {
    "current (0.585)": 0.585,
    "1.2 (SAND92-0243 low)": 1.2,
    "1.7 (SAND92-0243 high)": 1.7,
}


def run(label, shell_name, v0_src_fts, r_ft, m_oz, v_fts):
    shell = SHELLS[shell_name]
    rho_steel = shell.steel.rho
    s_m = r_ft * FT_TO_M
    m_kg = m_oz * OZ_TO_KG
    v_src_ms = v_fts * FTS_TO_MS
    v0_src_ms = v0_src_fts * FTS_TO_MS

    print(f"\n=== {label} (V0_source={v0_src_fts:.0f} f/s) ===")
    header = f"{'r(ft)':>6}"
    for cname in CANDIDATES:
        header += f" {cname:>22}"
    print(header)

    results = {}
    for cname, combined in CANDIDATES.items():
        drag = DragParams(C_D=combined, C_shape=1.0)
        lam = retardation_coeff(m_kg, drag, rho_steel)
        v_model_ms = v0_src_ms * np.exp(-lam * s_m)
        ratio = v_model_ms / v_src_ms
        results[cname] = ratio

    for i in range(len(r_ft)):
        row = f"{r_ft[i]:6.0f}"
        for cname in CANDIDATES:
            row += f" {results[cname][i]:22.2f}"
        print(row)
    return results


if __name__ == "__main__":
    # 75mm M48 HE -- only the 3 range points explicitly quoted in
    # initial-conditions-75mm.md (r=20,100,400 ft),
    # reused verbatim (not re-transcribed from the fuller source table).
    run(
        "75mm M48 HE",
        "75mm M48 HE",
        3120.0,
        np.array([20, 100, 400], dtype=float),
        np.array([0.014, 0.063, 0.244]),
        np.array([2060, 972, 494], dtype=float),
    )

    # 105mm M1 HE -- full Table 51 CASUALTIES (corrected identification),
    # reused verbatim from initial-conditions-105mm.md.
    run(
        "105mm M1 HE",
        "105mm M1 HE",
        3500.0,
        np.array([20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300], dtype=float),
        np.array([0.035, 0.047, 0.061, 0.095, 0.137, 0.192, 0.255, 0.326, 0.448, 0.580, 1.05]),
        np.array([2700, 2430, 2220, 1920, 1750, 1550, 1420, 1320, 1200, 1120, 955], dtype=float),
    )

    # 155mm M107 HE -- full corrected Table 59 CASUALTIES, reused verbatim
    # from initial-conditions-155mm.md.
    run(
        "155mm M107 HE",
        "155mm M107 HE",
        3500.0,
        np.array([20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600], dtype=float),
        np.array([0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109, 0.161, 0.233, 0.402]),
        np.array([2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505, 383], dtype=float),
    )
