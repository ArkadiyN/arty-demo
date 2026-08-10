#!/usr/bin/env python3
"""
Verify Table 5-5 closure invariants.

Consumer: doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/
card.md (Table 5-5) and experiment/fragmentation-field/updates/
sourced-wood-perforation-threshold/derivation.md §1.1 — settles the
density/hardness column-transposition finding without the source image.

Confirms that the corrected density/hardness column assignment satisfies:
1. Density (wet >= dry) for all species
2. Hardness (wet <= dry) for hardwoods only
"""

import csv
from pathlib import Path

# Repo root is six levels up from this file:
# experiment/fragmentation-field/updates/<slug>/checks/<this file>
REPO_ROOT = Path(__file__).resolve().parents[5]
csv_path = (
    REPO_ROOT
    / "doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects"
    / "tables/table-5-5-wood-properties.csv"
)

data = {}
with open(csv_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = row["species"]
        data.setdefault(key, {})
        cond = row["condition"]
        data[key][cond] = {
            "density": float(row["density_lbs_per_ft3"]),
            "hardness": float(row["hardness_pounds"]),
        }

# Hardwoods (per source: Maple, Green Oak, Hickory)
hardwoods = {"Maple", "Green Oak", "Hickory"}

print("=" * 60)
print("Table 5-5 Closure Invariant Verification")
print("=" * 60)

# Check 1: Density (wet >= dry) for all species
print("\n[1] Density invariant: wet >= dry (all species)")
density_pass = True
for species in sorted(data.keys()):
    dry_d = data[species]["Dry"]["density"]
    wet_d = data[species]["Wet"]["density"]
    ok = "✓" if wet_d >= dry_d else "✗"
    status = "PASS" if wet_d >= dry_d else "FAIL"
    if wet_d < dry_d:
        density_pass = False
    print(f"  {ok} {species:18} Dry={dry_d:5.1f}  Wet={wet_d:5.1f}  [{status}]")

# Check 2: Hardness (wet <= dry) for hardwoods only
print("\n[2] Hardness invariant: wet <= dry (hardwoods only)")
hardness_pass = True
for species in sorted(data.keys()):
    dry_h = data[species]["Dry"]["hardness"]
    wet_h = data[species]["Wet"]["hardness"]
    is_hardwood = species in hardwoods
    status = "N/A" if not is_hardwood else ("PASS" if wet_h <= dry_h else "FAIL")
    marker = "(hardwood)" if is_hardwood else "(softwood/engineered)"
    ok = "✓" if not is_hardwood or wet_h <= dry_h else "✗"
    if is_hardwood and wet_h > dry_h:
        hardness_pass = False
    print(
        f"  {ok} {species:18} Dry={dry_h:5.1f}  Wet={wet_h:5.1f}  "
        f"[{status:4}] {marker}"
    )

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
overall = density_pass and hardness_pass
print(f"Density invariant (all species):    {'PASS' if density_pass else 'FAIL'}")
print(f"Hardness invariant (hardwoods):     {'PASS' if hardness_pass else 'FAIL'}")
print(f"\nOverall closure:                    {'PASS ✓' if overall else 'FAIL ✗'}")
print("=" * 60)

exit(0 if overall else 1)
