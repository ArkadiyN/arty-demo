"""Check: does Family B (four_zone_lethal_density_field) reproduce the 1944
Ordnance Dept. B-vs-range casualty data for the "155mm M107 HE" shell,
ground-burst geometry?

See experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.md
for the reduction formula (Section 2) and study plan (Section 3). Mirrors
experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-105mm.py, adapted
for the 155mm shell.

Data source note: "155-MM N.E. SHELL, M107" (OCR mangles "H.E." as "N.E.") at
ordnance-1944.md lines 874-907 (page 131), interleaved row-by-row with
"TABLE 60" (perforation of 1/8-in. mild steel) from the same two-column OCR
scan, exactly as found for the 75mm/105mm table pairs. Here the header block
itself is scrambled too -- the table-number lines read "TABLE 60" then
"TABLE 59" (line 877-878), i.e. reversed relative to the "CASUALTIES" /
"PERFORATION..." lines that follow (879-880) -- so table numbering order is
not trustworthy; column identity is resolved from the data alone. The two
interleaved r-grids are: {20,30,40,60,80,100,150,200,300,400,600} (max range
600 ft) and {20,30,40,60,80,100,120,140,170,200,300,400} (max range 400 ft).
Per the scoping doc, the 155mm casualties table's max range is ~400 ft, which
identifies the second grid as TABLE 59 CASUALTIES; the first (600 ft) grid is
TABLE 60 PERFORATION. Cross-check: at every one of the 9 ranges shared by both
grids (20-400 ft), B_casualties <= B_perforation and both columns are
independently monotonically non-increasing in B and monotonically increasing
in m -- unlike the 105mm case, no single-row transposition is present here
(all rows are internally consistent), so no correction is needed.
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

# Table 59 (CASUALTIES), "155-MM H.E. SHELL, M107", ordnance-1944.md lines 874-907
# (r [ft], B [effective fragments / sq ft]) -- transcribed from the 400-ft-max-range
# interleaved column, see module docstring.
CARD_R_FT = np.array([20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300, 400], dtype=float)
CARD_B = np.array(
    [0.247, 0.104, 0.0547, 0.0209, 0.0102, 0.0057, 0.0036, 0.0024, 0.0014, 0.0009, 0.0002, 0.0001]
)

SHELL_NAME = "155mm M107 HE"
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
