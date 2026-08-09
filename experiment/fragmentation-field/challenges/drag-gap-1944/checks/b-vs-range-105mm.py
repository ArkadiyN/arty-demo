"""Check: does Family B (four_zone_lethal_density_field) reproduce the 1944
Ordnance Dept. B-vs-range casualty data for the "105mm M1 HE" shell,
ground-burst geometry?

See experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.md
for the reduction formula (Section 2) and study plan (Section 3). Mirrors
experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-75mm.py, adapted
for the 105mm shell.

Data source note: an earlier version of this script hand-typed a "Table 51
CASUALTIES" series that was in fact the interleaved Table 52 PERFORATION-OF-
1/8-IN-MILD-STEEL column (OPEN-FINDINGS.md's blocking B-vs-range
column-swap finding; see
experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-rebaseline.md).
This version reads the extracted-once, closure-checked genuine casualties
series directly from
doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/105mm-m1-casualties.csv
instead of hand-typing it, per .claude/rules/source-data-fidelity.md.
"""
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

from arty.shells import SHELLS
from arty.zones import DragParams, compute_shell_zones, four_zone_lethal_density_field

FT_TO_M = 0.3048
FT2_PER_M2 = 1.0 / FT_TO_M**2  # multiply rho_L [m^-2] by FT_TO_M**2 to get ft^-2

# 58 ft-lb casualty energy threshold (card's definition), converted to SI joules.
FT_LB_TO_J = 1.3558179483314004
E_LETH_58FTLB_J = 58.0 * FT_LB_TO_J  # ~78.6 J

TABLES_DIR = (
    "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"
)

# Table 51 (CASUALTIES), "105-MM H.E. SHELL, M1" -- read from the extracted-once,
# closure-checked CSV rather than hand-typed. See module docstring.
_card = pd.read_csv(f"{TABLES_DIR}/105mm-m1-casualties.csv")
CARD_R_FT = _card["r_ft"].to_numpy(dtype=float)
CARD_B = _card["B"].to_numpy(dtype=float)

SHELL_NAME = "105mm M1 HE"
H_B = 0.0  # ground burst
DELTA_DEG = 15.0
N_GRID = 121

# AoF is not carried in the shell registry for this shell (no striking-condition
# field on ShellParams); per the challenge doc's fallback instruction, sweep AoF
# over a representative WW2 gun/howitzer band and report the sensitivity band
# rather than pin one arbitrary value. AOF_PRIMARY is the single value used for
# the primary printed table.
AOF_SWEEP_DEG = [0.0, 15.0, 30.0, 45.0, 60.0]
AOF_PRIMARY_DEG = 30.0


def b_model_at_range(zones, drag, rho_steel, r_ft, aof_deg, n_phi=72):
    """Azimuthal-average B_model(r) [ft^-2] at ground range r_ft [ft], AoF [deg]."""
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
    rho_avg = rho_ring.mean()
    return rho_avg * FT_TO_M**2  # m^-2 -> ft^-2


if __name__ == "__main__":
    shell = SHELLS[SHELL_NAME]
    zones = compute_shell_zones(shell)
    drag = DragParams()
    rho_steel = shell.steel.rho

    print(f"Shell: {SHELL_NAME}, Family B, ground burst (h_b=0), "
          f"E_leth=58 ft-lb={E_LETH_58FTLB_J:.2f} J")
    print(f"Primary AoF = {AOF_PRIMARY_DEG} deg; sensitivity band over "
          f"AoF in {AOF_SWEEP_DEG} deg\n")

    print(f"{'r (ft)':>8} {'B_model':>12} {'B_card':>10} {'ratio':>8} "
          f"{'B_model band (AoF sweep)':>28}")
    for r_ft, b_card in zip(CARD_R_FT, CARD_B):
        b_primary = b_model_at_range(zones, drag, rho_steel, r_ft, AOF_PRIMARY_DEG)
        band = [
            b_model_at_range(zones, drag, rho_steel, r_ft, aof)
            for aof in AOF_SWEEP_DEG
        ]
        ratio = b_primary / b_card if b_card else float("nan")
        band_str = f"[{min(band):.4g}, {max(band):.4g}]"
        print(f"{r_ft:8.0f} {b_primary:12.4g} {b_card:10.4g} {ratio:8.3g} {band_str:>28}")
