"""Attribute the B(r) ratio change to the drag anchor alone.

Consumer: the refreshed ratio table in
experiment/fragmentation-field/challenges/drag-gap-1944/README.md and the
"Ratio range (model/card)" table in b-vs-range.qmd (Key findings).

Re-runs the three per-caliber B-vs-range checks at the pre-update drag
constants (C_D=0.65, C_shape=0.90; combined 0.585) and at the shipped
DoD-1975-anchored defaults (C_D=1.28, C_shape=2.089; combined 2.674), holding
everything else at current src/arty state. The difference between the two
columns is the drag-only effect; the difference between the "old drag" column
and the ratios originally published in b-vs-range.qmd (7-34x) is what the
Mott shape closure (v0.8.0) already removed.

Run: uv run python experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-drag-attribution.py
"""
import importlib.util
from pathlib import Path

from arty.zones import DragParams

CHECKS = Path(__file__).resolve().parent
CALIBERS = ["75mm", "105mm", "155mm"]

OLD_DRAG = DragParams(C_D=0.65, C_shape=0.90)
NEW_DRAG = DragParams()


def load(caliber):
    """Import the per-caliber b-vs-range check module by path."""
    path = CHECKS / f"b-vs-range-{caliber}.py"
    spec = importlib.util.spec_from_file_location(f"bvr_{caliber}", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ratios(mod, drag):
    """Return the model/card B ratios [-] at the primary AoF for one drag setting."""
    from arty.shells import SHELLS
    from arty.zones import compute_shell_zones

    shell = SHELLS[mod.SHELL_NAME]
    zones = compute_shell_zones(shell)
    return [
        mod.b_model_at_range(zones, drag, shell.steel.rho, r_ft, mod.AOF_PRIMARY_DEG) / b_card
        for r_ft, b_card in zip(mod.CARD_R_FT, mod.CARD_B)
    ]


if __name__ == "__main__":
    print(f"old combined C_D*C_shape = {OLD_DRAG.C_D * OLD_DRAG.C_shape:.4f}")
    print(f"new combined C_D*C_shape = {NEW_DRAG.C_D * NEW_DRAG.C_shape:.4f}\n")
    print(
        f"{'shell':>8} {'old drag ratio span':>24} {'new drag ratio span':>24}"
        f" {'far-field cut':>14} {'new in [0.5,2]':>15}"
    )
    for caliber in CALIBERS:
        mod = load(caliber)
        old = ratios(mod, OLD_DRAG)
        new = ratios(mod, NEW_DRAG)
        cut = old[-1] / new[-1]
        in_band = sum(1 for x in new if 0.5 <= x <= 2.0)
        print(
            f"{caliber:>8} {min(old):>10.1f}x - {max(old):<11.1f}"
            f" {min(new):>10.1f}x - {max(new):<11.1f} {cut:>13.1f}x"
            f" {in_band:>10d}/{len(new)}"
        )
