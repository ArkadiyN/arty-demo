"""Check: does Family B (four_zone_lethal_density_field) reproduce the 1944
Ordnance Dept. B-vs-range casualty data for the "75mm M48 HE" shell,
ground-burst geometry?

See experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.md
for the reduction formula (Section 2) and study plan (Section 3).

Data source note: the challenge brief cited ordnance-1944.md lines 340-369
for Table 43, but that range is actually the Hand Grenade Mk. II / 20-mm
H.E. Shell tables (a stale line reference). The genuine "75-MM H.E. SHELL,
M48" / "TABLE 43 CASUALTIES" block is at lines 381-411 of that file. The
page interleaves two tables (43 = casualties, 44 = perforation of 1/8-in.
mild steel) row-by-row from a two-column OCR scan; the column carrying
Table 43 is identified by its max range (225 ft), which matches the
challenge doc's statement that Table 43's max range is 225 ft (vs. 300/400
ft for the 105mm/155mm tables), and by B(r) being monotonically
non-increasing in that column -- both column-identity checks agree.

Row-swap note: at r=40 ft (lines 396-397) the two interleaved rows are
transposed relative to every other row -- "40 386 .0192 .082 2,010" (line
396) is actually Table 43 (casualties) and "40 750 .0375 .024 1,570" (line
397) is actually Table 44 (perforation), the reverse of the usual
first-line/second-line order. This is caught by the same two cross-column
invariants the 105mm script's r=100 fix relies on: taking line 397 as
casualties makes N jump 442->750 between r=30 and r=40 (violates monotonic
N-decrease) and makes B_casualties (.0375) > B_perforation (.0192), the only
row in the table where that inequality flips. Using line 396 for casualties
(N=386, B=.0192) restores both invariants across all 10 rows.
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

# Table 43 (CASUALTIES), "75-MM H.E. SHELL, M48", ordnance-1944.md lines 392-411
# (r [ft], B [effective fragments / sq ft]) -- transcribed directly, see module
# docstring; r=40 entry is 0.0192 (line 396), not 0.0375 (line 397) -- see the
# row-swap note above.
CARD_R_FT = np.array([20, 30, 40, 60, 80, 100, 130, 160, 190, 225], dtype=float)
CARD_B = np.array([0.106, 0.0391, 0.0192, 0.0066, 0.0030, 0.0016, 0.0006, 0.0003, 0.0001, 0.0001])

SHELL_NAME = "75mm M48 HE"
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
        ratio = b_primary / b_card
        band_str = f"[{min(band):.4g}, {max(band):.4g}]"
        print(f"{r_ft:8.0f} {b_primary:12.4g} {b_card:10.4g} {ratio:8.3g} {band_str:>28}")
