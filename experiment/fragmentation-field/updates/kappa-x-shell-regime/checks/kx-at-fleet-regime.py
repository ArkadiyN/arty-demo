"""kappa_x and k from Mott's ruled line at the l/x0 the shipped shells occupy.

Consumer: experiment/fragmentation-field/updates/kappa-x-shell-regime/derivation.md
section 3 (Action A) -- the adopted (kappa_x, k) triple values, their MC noise,
the fleet spread across l/x0 = 84..100, and the l/x0 = 20 regression row that
proves the re-run still reproduces Mott's own reported mean (~1.5).

Model and both nucleation schemes: see the imported
../../breadth-variance-factor-k/checks/mott-ruled-line-mc.py .
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
MC_PATH = (
    HERE.parent.parent / "breadth-variance-factor-k" / "checks" / "mott-ruled-line-mc.py"
)

_spec = importlib.util.spec_from_file_location("mott_ruled_line_mc", MC_PATH)
assert _spec is not None and _spec.loader is not None
mc = importlib.util.module_from_spec(_spec)
sys.modules["mott_ruled_line_mc"] = mc
_spec.loader.exec_module(mc)

# ~40 000 fragments per configuration (a ring of length l/x0 yields ~l/(kappa_x x0)
# fragments), so the s.e. on <x> is ~0.3 % / sqrt(40) ~ 0.05 %.
TARGET_FRAGMENTS = 40_000
SEEDS = (20260817, 5150319)


def rings_for(ell: float) -> int:
    return max(200, int(TARGET_FRAGMENTS * 1.62 / ell))


def moments(x: np.ndarray) -> tuple[float, float, float, float]:
    """Return (<x>/x0, s.e., k = <x^2>/<x>^2, bootstrap s.e. on k)."""
    m1 = float(x.mean())
    se1 = float(x.std(ddof=1) / np.sqrt(x.size))
    k = float((x**2).mean() / m1**2)
    rng = np.random.default_rng(7)
    idx = rng.integers(0, x.size, size=(200, x.size))
    s = x[idx]
    ks = (s**2).mean(axis=1) / s.mean(axis=1) ** 2
    return m1, se1, k, float(ks.std())


def row(ell: float, scheme: str, seed: int) -> None:
    x = mc.run(ell, n_rings=rings_for(ell), scheme=scheme, seed=seed)
    m1, se1, k, sek = moments(x)
    print(
        f"{scheme:8s} l/x0={ell:6.1f} seed={seed:<9d} n={x.size:7d}  "
        f"kappa_x={m1:6.4f} +/- {se1:.4f}   k={k:6.4f} +/- {sek:.4f}"
    )


if __name__ == "__main__":
    print("Mott 1947 ruled line -- breadth moments at the fleet regime\n")
    print("--- adopted regime, both seeds (Action A: MC-noise check) ---")
    for scheme in ("mott", "poisson"):
        for seed in SEEDS:
            row(95.0, scheme, seed)

    print("\n--- fleet spread (75 mm 84 .. 155 mm 100), seed 1 ---")
    for scheme in ("mott", "poisson"):
        for ell in (84.0, 100.0):
            row(ell, scheme, SEEDS[0])

    print("\n--- regression: Mott's own demonstration configuration ---")
    print("    (Mott 1947 p. 305 finding (1): mean breadth 'about 1.5 x0')")
    for scheme in ("mott", "poisson"):
        row(20.0, scheme, SEEDS[0])
