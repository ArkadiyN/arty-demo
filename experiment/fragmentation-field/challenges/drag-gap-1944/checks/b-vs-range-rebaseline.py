"""Check: re-run the b-vs-range.md / b-vs-range.qmd Family-B comparison
against the re-baselined 1944 Ordnance Dept. CASUALTIES columns (not the
PERFORATION-of-1/8-in-mild-steel columns the original b-vs-range-*.py scripts
were reading, per OPEN-FINDINGS.md's blocking finding on this thread).

Produces the numbers cited by
experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-rebaseline.md.

Reads the extracted-once series directly from
doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/
(<shell>-casualties.csv) rather than hand-typing them, per
.claude/rules/source-data-fidelity.md.
"""
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

from arty.shells import SHELLS
from arty.zones import DragParams, compute_shell_zones, four_zone_lethal_density_field

TABLES_DIR = (
    "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"
)

FT_TO_M = 0.3048
FT_LB_TO_J = 1.3558179483314004
E_LETH_58FTLB_J = 58.0 * FT_LB_TO_J  # ~78.6 J, card's casualty KE threshold

H_B = 0.0  # ground burst
DELTA_DEG = 15.0
N_GRID = 121
AOF_SWEEP_DEG = [0.0, 15.0, 30.0, 45.0, 60.0]
AOF_PRIMARY_DEG = 30.0

SHELLS_TO_CSV = {
    "75mm M48 HE": "75mm-m48-casualties.csv",
    "105mm M1 HE": "105mm-m1-casualties.csv",
    "155mm M107 HE": "155mm-m107-casualties.csv",
}


def b_model_at_range(zones, drag, rho_steel, r_ft, aof_deg, n_phi=72):
    """Azimuthally-averaged B_model(r) [ft^-2] at ground range r_ft [ft], AoF [deg]."""
    r_m = r_ft * FT_TO_M
    max_r = r_m * 1.25
    X, Y, rho_L = four_zone_lethal_density_field(
        zones,
        aof_deg=aof_deg,
        h_b=H_B,
        drag=drag,
        rho_steel=rho_steel,
        z=0.0,
        max_r=max_r,
        n_grid=N_GRID,
        delta_deg=DELTA_DEG,
        E_leth=E_LETH_58FTLB_J,
    )
    interp = RegularGridInterpolator(
        (Y[:, 0], X[0, :]), rho_L, bounds_error=False, fill_value=0.0
    )
    phis = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    xs = r_m * np.cos(phis)
    ys = r_m * np.sin(phis)
    rho_ring = interp(np.column_stack([ys, xs]))
    return rho_ring.mean() * FT_TO_M**2  # m^-2 -> ft^-2


if __name__ == "__main__":
    drag = DragParams()

    for shell_name, csv_name in SHELLS_TO_CSV.items():
        card = pd.read_csv(f"{TABLES_DIR}/{csv_name}")
        shell = SHELLS[shell_name]
        zones = compute_shell_zones(shell)
        rho_steel = shell.steel.rho

        print(f"\n=== {shell_name} (re-baselined casualties CSV: {csv_name}) ===")
        print(f"{'r (ft)':>8} {'B_model':>12} {'B_card':>10} {'ratio':>8} "
              f"{'B_model band (AoF sweep)':>28}")

        ratios = []
        b_models = []
        for r_ft, b_card in zip(card["r_ft"], card["B"]):
            b_primary = b_model_at_range(zones, drag, rho_steel, r_ft, AOF_PRIMARY_DEG)
            band = [
                b_model_at_range(zones, drag, rho_steel, r_ft, aof)
                for aof in AOF_SWEEP_DEG
            ]
            ratio = b_primary / b_card if b_card else float("nan")
            ratios.append(ratio)
            b_models.append(b_primary)
            band_str = f"[{min(band):.4g}, {max(band):.4g}]"
            print(f"{r_ft:8.0f} {b_primary:12.4g} {b_card:10.4g} {ratio:8.3g} "
                  f"{band_str:>28}")

        ratios = np.array(ratios)
        b_models = np.array(b_models)
        n_pass = np.sum((ratios >= 0.5) & (ratios <= 2.0))
        print(f"-> {n_pass}/{len(ratios)} ranges within factor-of-2 band; "
              f"ratio spans {ratios.min():.3g}x - {ratios.max():.3g}x")
        model_monotone = bool(np.all(np.diff(b_models) <= 1e-12))
        card_monotone = bool(np.all(np.diff(card["B"].to_numpy()) <= 0))
        print(f"   model monotone non-increasing = {model_monotone}, "
              f"card monotone non-increasing = {card_monotone}")
