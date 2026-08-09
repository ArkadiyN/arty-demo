"""Verify the greppable source anchors introduced when closing the three
bare-line-number findings (DoD-1975 in src/arty/fragmentation.py +
mach-dependent-fragment-drag/derivation.md; ES-310 in pkill-poisson-field/
derivation.md; Gold 2017 in mott-fragment-shape-closure/derivation.md and
scoping.md). Each anchor must resolve to exactly one line of its source.

Consumer: the closure notes in
experiment/fragmentation-field/challenges/source-data-audit/ledger.md,
doc-reference/wound-ballistics/fas-es310-damage-criteria/fas-es310-damage-criteria.md,
and experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]

DOD = ROOT / (
    "doc-reference/fragmentation/dod-1975-fragment-debris-hazards/"
    "10-F-0806_Fragment_and_Debris_Hazards.md"
)
ES310 = ROOT / (
    "doc-reference/wound-ballistics/fas-es310-damage-criteria/"
    "fas-es310-damage-criteria.md"
)
GOLD = ROOT / (
    "doc-reference/fragmentation/fragment-size-distribution-conwep/"
    "1-s2.0-S221491471730079X-main.md"
)

ANCHORS = [
    (DOD, "similar, the mass m and presented area A are related by"),
    (DOD, "value of 660 grains/in.3 (2.60 g/cm3) has been recommended"),
    (DOD, "take the drag coefficient as constant at its"),
    (DOD, "supersonic value of 1.28."),
    (DOD, "velocity-squared law"),
    (DOD, "the average is taken as the mean presented area"),
    (DOD, "of motion can be integrated in the case of a constant drag coefficient"),
    (DOD, "If the force of gravity is neglected, however, the equation"),
    (DOD, "considering the effects of both drag and gravity"),
    (DOD, "the value of k differs from one weapon to"),
    (ES310, "Aggregate Pk from multiple hits:"),
    (ES310, "Moderate personnel kill criterion is"),
    (GOLD, r"\tag{4}"),
    (GOLD, r"\tag{6}"),
    (GOLD, r"\tag{7}"),
    (GOLD, r"\tag{16}"),
    (GOLD, "idealized with simple geometric shapes like a parallelepiped"),
    (GOLD, "is defined as one half of the average fragment mass"),
    (GOLD, "Since the fragment distribution relationship"),
]


def main() -> int:
    failures = 0
    for path, anchor in ANCHORS:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [i + 1 for i, ln in enumerate(lines) if anchor in ln]
        status = "OK  " if len(hits) == 1 else "FAIL"
        if len(hits) != 1:
            failures += 1
        print(f"{status} {len(hits)} hit(s) {hits} {path.name}: {anchor!r}")
    print(f"\n{len(ANCHORS) - failures}/{len(ANCHORS)} anchors resolve uniquely")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
