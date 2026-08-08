"""Materiality check for fuze-mass-deductions-range/materiality.md.

Computes case-metal mass, Mott mu, and N0 (total fragment count) for the
105mm M1 HE and 155mm M107 HE shell entries in src/arty/shells.py under (a)
the currently shipped mass_deductions placeholder and (b) candidate values
informed by TM-9-1901 sourced fuze/booster weights, to quantify the shift in
N0 the swap would cause.

Run: uv run python experiment/fragmentation-field/challenges/fuze-mass-deductions-range/checks/mass-deductions-sensitivity.py
"""
import dataclasses
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))

from arty.shells import SHELLS
from arty.fragmentation import gurney_velocity, mott_params

LB = 0.45359237  # kg per lb


def report(name, shell, label):
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)
    mass_shell = shell.mass_total - shell.mass_filler - shell.mass_deductions
    print(f"{name} [{label}]: mass_deductions={shell.mass_deductions:.4f} kg "
          f"({shell.mass_deductions/LB:.3f} lb)  case_mass={mass_shell:.4f} kg  "
          f"V0={V0:.1f} m/s  mu={mu*1000:.4f} g  N0={N0:.1f}")
    return N0


print("=" * 100)
print("105mm M1 HE — authorized fuzes M48 or M54 w/ M20 or M20A1 Booster (TM-9-1904)")
print("Sourced fuze-only weights (TM-9-1901): M48/M48A1/M48A2 = 1.41 lb, M54 = 1.42 lb")
print("Booster (M20/M20A1) weight: NOT sourced. M21A2 booster increment (closes on two")
print("independent pairs in TM-9-1901) = 0.74 lb, used here only as an order-of-magnitude stand-in.")
print("=" * 100)

shell_105 = SHELLS["105mm M1 HE"]
N0_105_current = report("105mm M1 HE", shell_105, "current: 0.75 kg placeholder, no source")

# (1) Within-family fuze-only spread: M48 (1.41 lb) vs M54 (1.42 lb) -- 0.01 lb diff
s = dataclasses.replace(shell_105, mass_deductions=1.41 * LB)
N0_105_m48 = report("105mm M1 HE", s, "M48 fuze only, no booster/band = 1.41 lb")
s = dataclasses.replace(shell_105, mass_deductions=1.42 * LB)
N0_105_m54 = report("105mm M1 HE", s, "M54 fuze only, no booster/band = 1.42 lb")

# (2) Candidate: fuze + booster (using M21A2 increment as order-of-magnitude
# stand-in for the unsourced M20/M20A1), no rotating band
s = dataclasses.replace(shell_105, mass_deductions=(1.41 + 0.74) * LB)
N0_105_fb = report("105mm M1 HE", s, "M48 fuze + booster-analog(0.74lb) = 2.15 lb")

print()
print(f"105mm within-family (M48 vs M54) N0 shift: {N0_105_m54 - N0_105_m48:.2f} "
      f"({100*(N0_105_m54-N0_105_m48)/N0_105_m48:.2f}%)")
print(f"105mm current-placeholder vs fuze-only N0 shift: {N0_105_m48 - N0_105_current:.1f} "
      f"({100*(N0_105_m48-N0_105_current)/N0_105_current:.2f}%)")
print(f"105mm current-placeholder vs fuze+booster-analog N0 shift: {N0_105_fb - N0_105_current:.1f} "
      f"({100*(N0_105_fb-N0_105_current)/N0_105_current:.2f}%)")

print()
print("=" * 100)
print("155mm M107 HE — authorized fuzes P.D. M51 w/ M21 Booster or M51A1 w/ M21A1 Booster (TM-9-1904)")
print("TM-9-1901 only tabulates the superseding pair M51A3 w/ M21A2 = 2.15 lb")
print("(sourced fuze+booster weight is available only for the LATER variant, not M51/M51A1 asked for)")
print("=" * 100)

shell_155 = SHELLS["155mm M107 HE"]
N0_155_current = report("155mm M107 HE", shell_155, "current: 1.5 kg 'estimate' (fuze+band+base plug)")

# Candidate: fuze+booster only (M51A3/M21A2 as best-available stand-in for M51/M21, M51A1/M21A1)
s = dataclasses.replace(shell_155, mass_deductions=2.15 * LB)
N0_155_fb = report("155mm M107 HE", s, "M51A3 fuze+booster (sourced stand-in) = 2.15 lb, no band/plug")

# Candidate: fuze+booster (2.15 lb) plus the current entry's implied rotating-band+base-plug
# residual (1.5 kg - naive-fuze-guess), added on top as a plausibility check
band_plug_residual_kg = shell_155.mass_deductions - 0.975  # 1.5 kg current minus ~0.975 kg (2.15 lb) fuze+booster
s = dataclasses.replace(shell_155, mass_deductions=2.15 * LB + max(band_plug_residual_kg, 0))
N0_155_full = report("155mm M107 HE", s, f"M51A3 fuze+booster (2.15lb) + current's implied band/plug residual ({band_plug_residual_kg:.3f} kg)")

print()
print(f"155mm current(1.5kg) vs fuze+booster-only(2.15lb=0.975kg) N0 shift: {N0_155_fb - N0_155_current:.1f} "
      f"({100*(N0_155_fb-N0_155_current)/N0_155_current:.2f}%)")
print(f"155mm current(1.5kg) vs fuze+booster+band/plug-residual N0 shift: {N0_155_full - N0_155_current:.1f} "
      f"({100*(N0_155_full-N0_155_current)/N0_155_current:.2f}%)")
