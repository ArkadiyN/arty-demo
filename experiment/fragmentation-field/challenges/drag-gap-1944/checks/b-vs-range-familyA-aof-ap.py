"""Attribution probe for the Family A B-vs-range check: which AoF sits at each
end of the sensitivity band, how much of B_A depends on the per-zone A_p
treatment (graded A_p(gamma_z) vs. flat head-on A_p(0)), and whether the
factor-of-2 verdict survives at the band edges rather than only at AoF = 30 deg.

Consumer: the "AoF sensitivity" and "A_p treatment" paragraphs of
experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-familyA.md.
Reuses b-vs-range-familyA.py's own reduction -- nothing is re-derived here.

Run: uv run python experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-familyA-aof-ap.py
"""
import importlib.util
from pathlib import Path

import numpy as np

from arty.fragmentation import DragParams, retardation_coeff
from arty.shells import SHELLS
from arty.zones import compute_shell_zones

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "bvr_familyA", HERE / "b-vs-range-familyA.py"
)
assert _spec is not None and _spec.loader is not None
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)

PROBE_R_FT = {"75mm M48 HE": [20.0, 100.0], "105mm M1 HE": [20.0, 100.0],
              "155mm M107 HE": [20.0, 100.0]}

if __name__ == "__main__":
    drag = DragParams()
    m_grid = np.logspace(-6, np.log10(0.5), A.N_MASS)
    phis = np.linspace(0.0, 2 * np.pi, A.N_PHI, endpoint=False)

    print("--- B_A [ft^-2] per AoF (primary = 30 deg) ---")
    hdr = " ".join(f"{a:11.0f}" for a in A.AOF_SWEEP_DEG)
    print(f"{'shell':>16} {'r (ft)':>7} {hdr}")
    for name, rs in PROBE_R_FT.items():
        shell = SHELLS[name]
        zones = compute_shell_zones(shell)
        for r_ft in rs:
            vals = [A.b_model_familyA(zones, drag, shell.steel.rho, r_ft, a)[0]
                    for a in A.AOF_SWEEP_DEG]
            print(f"{name:>16} {r_ft:7.0f} " + " ".join(f"{v:11.4g}" for v in vals))

    print("\n--- A_p treatment: graded A_p(gamma_z) vs flat A_p(0), AoF=30 deg ---")
    print(f"{'shell':>16} {'r (ft)':>7} {'graded':>12} {'flat':>12} {'flat/graded':>12}")
    for name, rs in PROBE_R_FT.items():
        shell = SHELLS[name]
        zones = compute_shell_zones(shell)
        lam = retardation_coeff(m_grid, drag, shell.steel.rho)
        for r_ft in rs:
            r_m = r_ft * A.FT_TO_M
            xg, yg = r_m * np.cos(phis), r_m * np.sin(phis)
            g, _ = A.rho_L_familyA(zones, A.AOF_PRIMARY_DEG, lam, m_grid, xg, yg)
            f, _ = A.rho_L_familyA(zones, A.AOF_PRIMARY_DEG, lam, m_grid, xg, yg,
                                   flat_Ap=True)
            gb, fb = g.mean() * A.FT_TO_M**2, f.mean() * A.FT_TO_M**2
            print(f"{name:>16} {r_ft:7.0f} {gb:12.4g} {fb:12.4g} "
                  f"{(fb / gb if gb > 0 else float('nan')):12.4g}")

    print("\n--- Does the factor-of-2 verdict survive the AoF band edges? ---")
    print(f"{'shell':>16} {'AoF':>5} {'ratio to card':>18} {'in [0.5,2]':>12}")
    for name in PROBE_R_FT:
        shell = SHELLS[name]
        zones = compute_shell_zones(shell)
        modB = A.load_familyB(A.CALIBERS[name])
        for aof in A.AOF_SWEEP_DEG:
            ratios = [
                A.b_model_familyA(zones, drag, shell.steel.rho, r_ft, aof)[0] / b_card
                for r_ft, b_card in zip(modB.CARD_R_FT, modB.CARD_B)
            ]
            n_in = sum(A.in_band(x) for x in ratios)
            print(f"{name:>16} {aof:5.0f} {min(ratios):8.2f}x -{max(ratios):7.2f}x "
                  f"{n_in:6d}/{len(ratios)}")
