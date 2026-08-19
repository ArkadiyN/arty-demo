"""Re-solve the aspect moment c on the ruled-line population at the FLEET regime.

Consumer: experiment/fragmentation-field/updates/kappa-x-shell-regime/
derivation.md section 4 (Action B) -- the per-shell c that pairs with the
re-solved (kappa_x, k) at l/x0 = 95.

This is NOT a new closure.  It re-runs the committed
../../breadth-variance-factor-k/checks/c-on-ruled-line-population.py with
exactly ONE substitution, the one scoping.md section 5 action B names: the
breadth marginal is sampled at l/x0 = 95 (the fleet value, derivation.md
section 2) instead of Mott's own demonstration l/x0 = 20.  The substitution is
done textually on the sibling script's source so that its closure algebra,
Table-3 handling and both weighting modes stay bit-identical and un-forked.
"""

from __future__ import annotations

import pathlib
import sys
import types

HERE = pathlib.Path(__file__).resolve().parent
SRC = (
    HERE.parent.parent
    / "breadth-variance-factor-k"
    / "checks"
    / "c-on-ruled-line-population.py"
)

OLD = 'XI = mc.run(20.0, n_rings=400, scheme="mott")   # Mott\'s own l/x0 = 20 config'
NEW = 'XI = mc.run(95.0, n_rings=700, scheme="mott")   # fleet regime (derivation.md 2)'

# Second substitution: mu0 (which sets the mass scale S, hence which breadth
# interval each Table-3 mass group maps to) carries kappa_x through
# alpha = A kappa_x^2 t_bu/x0.  Leaving it at the registry default 1.5 while the
# marginal comes from l/x0 = 95 would be the same one-population-two-regimes
# error B2 was raised against, one level down.  Run BOTH so the size of the
# coupling is visible.
OLD_MU0 = "bare = dataclasses.replace(shell, aspect_ratio=_MOTT_ASPECT_RATIO)"
KAPPA_VARIANTS = (1.5, 1.62)


def run(kappa_x: float) -> None:
    src = SRC.read_text()
    for anchor in (OLD, OLD_MU0):
        if anchor not in src:
            raise SystemExit(
                f"anchor line not found in {SRC} -- the sibling script changed "
                "shape; re-read it before trusting this substitution"
            )
    src = src.replace(
        'print(f"ruled-line MC (l/x0=20, Mott step):',
        'print(f"ruled-line MC (l/x0=95, Mott step):',
    )
    src = src.replace(OLD, NEW).replace(
        OLD_MU0,
        "bare = dataclasses.replace(shell, aspect_ratio=_MOTT_ASPECT_RATIO, "
        f"breadth_factor={kappa_x!r})",
    )

    name = f"c_ruled_line_fleet_kx{str(kappa_x).replace('.', '')}"
    mod = types.ModuleType(name)
    mod.__file__ = str(SRC)  # so its HERE / relative loads still resolve
    mod.__dict__["__name__"] = "__main__"  # the sibling reports under this guard
    sys.modules[name] = mod
    print("=" * 78)
    print(f"=== breadth marginal at l/x0 = 95 ; mu0 evaluated at kappa_x = {kappa_x}")
    print("=" * 78)
    exec(compile(src, str(SRC), "exec"), mod.__dict__)


def main() -> None:
    for kx in KAPPA_VARIANTS:
        run(kx)


if __name__ == "__main__":
    main()
