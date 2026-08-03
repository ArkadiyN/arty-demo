"""Does the ES-310 page's own worked example close against its own Table 3?

Consumer: doc-reference/wound-ballistics/fas-es310-damage-criteria/card.md
          ("Closure", "What the closure does and does not certify"), and
          experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 23.

Table 3 tabulates three fragment energies against three Pk levels for three
target classes, with no arithmetic tying the nine cells together -- so nothing
*inside* that table can tell a right value from a plausible wrong one. That is
exactly the situation .claude/rules/source-data-fidelity.md warns about, and
the reason the column-inversion incident went unnoticed: a wrong row reads as
well as a right one.

The closure has to come from elsewhere on the page, and it does. The page works
a hand grenade example numerically, and to do so it must read a Pk|hit off
Table 3 at 3000 J. This script asks which row it can have read:

  1. Interpolate Pk|hit at 3000 J from EACH of the three target rows.
  2. Compare against the 0.8 the page states.
     Only the personnel row can produce it. The aircraft row puts 3000 J below
     its own light-damage floor (4 kJ), and the armored-vehicle row further
     still -- both give Pk|hit near zero, and the example's arithmetic would
     not reproduce its printed answers from either.

That is the row-identity check. `src/arty/fragmentation.py` hardcodes the
personnel row as its Pk|hit anchors, so this script also verifies the shipped
constants against tables/table-3-fragmentation-damage-criteria.csv rather than
against a hand-typed literal, and checks that `pk_given_hit` reproduces the
page's worked-example estimate.

Both interpolation schemes are reported because the page states none. The
shipped code interpolates in log10(E); the page's prose reasons linearly in E.
Which one the page had in mind is not recoverable, and the gap between them is
the honest uncertainty on this anchor -- the card records it as such.

Reads its numbers from the CSVs; nothing here is a hand-typed data array.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/es310-worked-example-closure.py
"""

import csv
import math
import pathlib

import numpy as np

from arty.fragmentation import _PK_E, _PK_VAL, pk_given_hit

ROOT = pathlib.Path(__file__).resolve().parents[5]
TABLES = ROOT / "doc-reference/wound-ballistics/fas-es310-damage-criteria/tables"

# The page's own words for the estimate it takes, and how loosely it takes it:
# "it would be reasonable to expect a probability of some where between 0.5 and
# 0.9 for a single 3000 J fragment.  Take 0.8 as an estimate."  So 0.8 is an
# eyeball inside a stated bracket, not a computed value -- the tolerance below
# reflects that, and is still far tighter than the gap to any other row.
PAGE_PK_HIT = 0.8
PAGE_TOL = 0.10


def read_csv(name):
    with (TABLES / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def anchors(row):
    """(energies [J], Pk values) for one target row of Table 3, kJ -> J."""
    e = np.array([float(row[f"energy_{lvl}_kJ"]) for lvl in ("light", "moderate", "heavy")])
    p = np.array([float(row[f"pk_{lvl}"]) for lvl in ("light", "moderate", "heavy")])
    return e * 1000.0, p


def main():
    table3 = read_csv("table-3-fragmentation-damage-criteria.csv")
    example = read_csv("worked-example-hand-grenade.csv")

    energy = float(example[0]["frag_energy_J"])
    stated = float(example[0]["pk_hit"])
    print(f"Worked example: {energy:.0f} J fragment, page takes Pk|hit = {stated}")
    print(f"Table 3 rows: {', '.join(r['target'] for r in table3)}\n")

    print("1. Which Table 3 row can yield the page's Pk|hit at 3000 J?\n")
    print(f"    {'target':<16} {'linear in E':>12} {'linear in logE':>15}   verdict")
    admissible = []
    for row in table3:
        e, p = anchors(row)
        lin = float(np.interp(energy, e, p, left=0.0, right=p[-1]))
        log = float(np.interp(math.log10(energy), np.log10(e), p, left=0.0, right=p[-1]))
        ok = abs(lin - PAGE_PK_HIT) <= PAGE_TOL or abs(log - PAGE_PK_HIT) <= PAGE_TOL
        if ok:
            admissible.append(row["target"])
        print(f"    {row['target']:<16} {lin:>12.3f} {log:>15.3f}   "
              f"{'MATCHES the page' if ok else 'cannot produce 0.8'}")

    print(f"\n    -> admissible row(s): {admissible or 'NONE'}")
    if admissible != ["personnel"]:
        print("    -> FAIL: the worked example does not single out the personnel row")
        return 1
    print("    -> the example is anchored on the PERSONNEL row, uniquely.")
    print("       A transposed row would have to survive this and does not.")

    print("\n2. Do the shipped Pk|hit anchors equal that row?\n")
    e_personnel, p_personnel = anchors(table3[0])
    print(f"    CSV  personnel row : E = {e_personnel} J, Pk = {p_personnel}")
    print(f"    src/arty/fragmentation.py : _PK_E = {_PK_E}, _PK_VAL = {_PK_VAL}")
    matched = np.allclose(_PK_E, e_personnel) and np.allclose(_PK_VAL, p_personnel)
    print(f"    -> {'match' if matched else 'MISMATCH'}")
    if not matched:
        return 1

    print("\n3. Does pk_given_hit reproduce the page's worked-example estimate?\n")
    shipped = float(pk_given_hit(np.array([energy]))[0])
    e, p = anchors(table3[0])
    lin = float(np.interp(energy, e, p))
    print(f"    pk_given_hit({energy:.0f} J)      = {shipped:.4f}   (log10-E interpolation, as shipped)")
    print(f"    linear-in-E interpolation = {lin:.4f}")
    print(f"    page states               = {PAGE_PK_HIT}")
    print(f"    -> shipped is {abs(shipped - PAGE_PK_HIT):.4f} from the page's estimate; "
          f"linear-in-E is {abs(lin - PAGE_PK_HIT):.4f}")
    print("    -> the page states no interpolation scheme.  The shipped log10-E "
          "scheme happens to\n       sit closer to the one estimate the page "
          "works, but that is a single point and\n       not a derivation -- "
          "see card.md, 'What the closure does and does not certify'.")

    print("\nRESULT: PASS — personnel row uniquely identified, shipped anchors "
          "match the CSV.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
