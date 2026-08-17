"""Does the aspect-ratio moment correction c move the drag-gap-1944 B(r) fit?

Consumer: section 5.1 of
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/derivation.md

scoping.md section 5 asserts that a changed mu re-weights the B(r) fit even
though the per-fragment ballistic coefficient (C_shape, in retardation_coeff)
is untouched -- because a different mass spectrum changes which fragments
dominate the hit density at range.  This script confirms that numerically
rather than asserting it.

Method: the correction enters shipped code as A -> c*A on ShellParams, so
    dataclasses.replace(shell, aspect_ratio=c*1.6)
and everything downstream (compute_shell_zones -> mu, N0 -> the four-zone
lethal-density field) re-solves itself.  B_model(r) is then computed with the
challenge's own committed reduction, imported unmodified from
experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-155mm.py
so the fit is compared like-for-like against the same Table 59 casualties CSV.

Run: uv run python experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks/bofr-at-new-mu.py
"""

import dataclasses
import importlib.util
import math
import pathlib

import numpy as np

from arty.fragmentation import _MOTT_ASPECT_RATIO
from arty.shells import SHELLS
from arty.zones import DragParams, compute_shell_zones

ROOT = pathlib.Path(__file__).resolve().parents[5]
B155 = (
    ROOT
    / "experiment/fragmentation-field/challenges/drag-gap-1944/checks"
    / "b-vs-range-155mm.py"
)

# c values reported in derivation.md section 3.3 / section 4.
C_VALUES = (1.0, 1.25, 1.91)


def _load(path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = _load(B155)
    # C_VALUES below are multipliers ON THE UNCORRECTED A = 1.6; the registry
    # now ships aspect_ratio = c*1.6, so pin the baseline back to 1.6.
    base = dataclasses.replace(SHELLS[m.SHELL_NAME],
                               aspect_ratio=_MOTT_ASPECT_RATIO)
    drag = DragParams()
    rho_steel = base.steel.rho

    print(f"Shell {m.SHELL_NAME}, Family B, ground burst, AoF="
          f"{m.AOF_PRIMARY_DEG} deg, E_leth={m.E_LETH_58FTLB_J:.1f} J")
    print("B_model(r) [ft^-2] vs Table 59 casualties, at A -> c*A\n")

    header = f"{'r(ft)':>7} {'B_card':>9}"
    for c in C_VALUES:
        header += f" {'c=' + format(c, '.2f'):>10}"
    header += "   " + "  ".join(f"ratio(c={c:.2f})" for c in C_VALUES)
    print(header)

    results = {c: [] for c in C_VALUES}
    for r_ft, b_card in zip(m.CARD_R_FT, m.CARD_B):
        line = f"{r_ft:7.0f} {b_card:9.4g}"
        ratios = []
        for c in C_VALUES:
            shell = dataclasses.replace(base, aspect_ratio=c * base.aspect_ratio)
            zones = compute_shell_zones(shell)
            b = m.b_model_at_range(
                zones, drag, rho_steel, r_ft, m.AOF_PRIMARY_DEG
            )
            results[c].append(b)
            line += f" {b:10.4g}"
            ratios.append(b / b_card if b_card else float("nan"))
        line += "   " + "  ".join(f"{x:12.3g}" for x in ratios)
        print(line)

    print("\nGeometric-mean |log| fit quality over the card's range points")
    print(f"{'c':>6} {'A_eff':>7} {'geo-mean ratio':>16} {'in 0.5-2x band':>16}")
    for c in C_VALUES:
        arr = np.array(results[c])
        card = np.array(m.CARD_B, dtype=float)
        ok = (card > 0) & (arr > 0)
        gm = math.exp(np.mean(np.log(arr[ok] / card[ok])))
        n_in = int(np.sum((arr[ok] / card[ok] >= 0.5) & (arr[ok] / card[ok] <= 2.0)))
        print(f"{c:6.2f} {c * base.aspect_ratio:7.3f} {gm:16.3f} "
              f"{str(n_in) + '/' + str(int(ok.sum())):>16}")

    # SHAPE check: is the change a pure level shift, or does it tilt B(r)?
    print("\nShape: B(r)/B(r=nearest) normalised, to separate level from tilt")
    for c in C_VALUES:
        arr = np.array(results[c])
        print(f"  c={c:.2f}  " + " ".join(f"{v / arr[0]:.3f}" for v in arr))


if __name__ == "__main__":
    main()
