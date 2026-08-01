"""Check: does Family B (four_zone_lethal_density_field) reproduce the 1944
Ordnance Dept. B-vs-range casualty data for the "105mm M1 HE" shell,
ground-burst geometry?

See experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.md
for the reduction formula (Section 2) and study plan (Section 3). Mirrors
experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-75mm.py, adapted
for the 105mm shell.

Data source note: "TABLE 51 CASUALTIES" / "105-MM H.E. SHELL, M1" is at
ordnance-1944.md lines 725-759 (page 133), interleaved row-by-row with
"TABLE 52" (perforation of 1/8-in. mild steel) from the same two-column OCR
scan, exactly as found for the 75mm Table 43/44 pair. The two tables have
different range grids (casualties: 20-300 ft in 11 rows; perforation:
20-500 ft in 11 rows) that happen to coincide at every r <= 100 ft, which
identifies the columns: casualties is the column with max range 300 ft
(matching this shell's ~300 ft max range per the scoping doc), monotonically
non-increasing B, and B_casualties <= B_perforation at each shared r -- all
of which hold except at r=100 ft, where the two columns' (N, B, m, v)
values are transposed in the raw scan (a one-row column swap: without the
swap, B_casualties(.0070) > B_perforation(.0037), the sole violation of the
casualties<=perforation and increasing-effective-mass-with-range trends
elsewhere in both tables). Corrected here by swapping in the perforation
column's r=100 row (N=470, B=.0037, m=.192, v=1550) for the casualties
table's r=100 entry, restoring both trends.
"""
import numpy as np
from scipy.interpolate import RegularGridInterpolator

from arty.shells import SHELLS
from arty.zones import DragParams, compute_shell_zones, four_zone_lethal_density_field

FT_TO_M = 0.3048
FT2_PER_M2 = 1.0 / FT_TO_M**2  # multiply rho_L [m^-2] by FT_TO_M**2 to get ft^-2

# 58 ft-lb casualty energy threshold (card's definition), converted to SI joules.
FT_LB_TO_J = 1.3558179483314004
E_LETH_58FTLB_J = 58.0 * FT_LB_TO_J  # ~78.6 J

# Table 51 (CASUALTIES), "105-MM H.E. SHELL, M1", ordnance-1944.md lines 725-759
# (r [ft], B [effective fragments / sq ft]) -- transcribed with the r=100 column-swap
# fix, see module docstring.
CARD_R_FT = np.array([20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300], dtype=float)
CARD_B = np.array(
    [0.194, 0.0816, 0.0424, 0.0155, 0.0071, 0.0037, 0.0022, 0.0014, 0.0007, 0.0004, 0.0001]
)

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
