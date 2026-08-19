"""Downstream effect of the re-solved (kappa_x, k, c) triple -- RECOMPUTED, not scaled.

Consumer: experiment/fragmentation-field/updates/kappa-x-shell-regime/
derivation.md section 5 (Action C): the 155 mm B(r) fit against FM 6-40 Table 59
and the 75 mm count-gap-1938 count arms.

mu depends on the triple only through the product (eq. 3 of derivation.md)

    mu ~ A_eff * kappa_x^2 = 1.6 * c * k * kappa_x^2 ,

so a sweep parameterised by the multiplier on the uncorrected A = 1.6, at the
registry kappa_x = 1.5, reproduces the new mu EXACTLY when driven with
    c_eff = c * k * (kappa_x_new / 1.5)^2 .
Both downstream harnesses below then re-solve the full Mott chain from that mu
(memory gotcha_mott_count_not_f_squared: never scale N, re-run it).
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]

# --- shipped triple (src/arty/fragmentation.py) ------------------------------
KX_SHIP = 1.5
K_SHIP = 1.1375
C_SHIP = {"155mm M107 HE": 1.1254, "105mm M1 HE": 1.0608,
          "75mm M48 HE": 1.0247, "60mm M49A2 HE": 1.0026}

# --- re-solved triple, l/x0 = 95, Mott step, "percell" closure ---------------
# derivation.md sections 3 (kappa_x, k) and 4 (c); checks/kx-at-fleet-regime.py
# and checks/c-at-fleet-regime.py.
KX_NEW = 1.62
K_NEW = 1.1711
C_NEW = {"155mm M107 HE": 1.1524, "105mm M1 HE": 1.0789,
         "75mm M48 HE": 1.0408, "60mm M49A2 HE": 1.0093}
# "marginal" closure, the low end of the method band (derivation.md section 4)
C_NEW_MARGINAL = {"155mm M107 HE": 1.0489, "105mm M1 HE": 0.9786,
                  "75mm M48 HE": 0.9384, "60mm M49A2 HE": 0.9581}


def c_eff(c: float, k: float, kx: float) -> float:
    """Multiplier on the uncorrected A = 1.6 that reproduces mu at breadth 1.5."""
    return c * k * (kx / KX_SHIP) ** 2


def _load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def mu_multipliers() -> None:
    print("mu multiplier vs shipped, per shell  (mu ~ 1.6 c k kappa_x^2)\n")
    print(f"{'shell':>14} {'A_eff ship':>11} {'A_eff new':>10} {'x from A_eff':>13}"
          f" {'x from kx^2':>12} {'mu x':>7} {'N0 x':>7}")
    for name in C_SHIP:
        a_s = 1.6 * C_SHIP[name] * K_SHIP
        a_n = 1.6 * C_NEW[name] * K_NEW
        f_a = a_n / a_s
        f_k = (KX_NEW / KX_SHIP) ** 2
        print(f"{name:>14} {a_s:11.4f} {a_n:10.4f} {f_a:13.4f} {f_k:12.4f}"
              f" {f_a * f_k:7.4f} {1 / (f_a * f_k):7.4f}")
    print()


def bofr_155() -> None:
    print("=" * 78)
    print("155 mm B(r) vs FM 6-40 Table 59 -- recomputed at each triple")
    print("=" * 78)
    m = _load(ROOT / "experiment/fragmentation-field/updates/"
                     "mass-dependent-fragment-shape/checks/bofr-at-new-mu.py")
    n = "155mm M107 HE"
    vals = {
        "shipped   (kx=1.50, k=1.1375, c=1.1254)": c_eff(C_SHIP[n], K_SHIP, KX_SHIP),
        "new       (kx=1.62, k=1.1711, c=1.1524)": c_eff(C_NEW[n], K_NEW, KX_NEW),
        "new, marginal closure (c=1.0489)": c_eff(C_NEW_MARGINAL[n], K_NEW, KX_NEW),
        "new, Poisson kx=1.67 band edge": c_eff(C_NEW[n], 1.1888, 1.67),
    }
    for label, v in vals.items():
        print(f"  {label:44s} c_eff = {v:.4f}")
    print()
    m.C_VALUES = tuple(round(v, 4) for v in vals.values())
    m.main()


def count_chain_75() -> None:
    print("\n" + "=" * 78)
    print("75 mm count-gap-1938 arms -- Mott chain re-solved (never scaled)")
    print("=" * 78)
    lev = _load(ROOT / "experiment/fragmentation-field/updates/"
                       "mass-dependent-fragment-shape/checks/"
                       "aspect-ratio-moment-leverage.py")
    n = "75mm M48 HE"
    cases = {
        "baseline A = 1.6 (no moment correction)": 1.0,
        "shipped   (kx=1.50, k=1.1375, c=1.0247)": c_eff(C_SHIP[n], K_SHIP, KX_SHIP),
        "new       (kx=1.62, k=1.1711, c=1.0408)": c_eff(C_NEW[n], K_NEW, KX_NEW),
        "new, marginal closure (c=0.9384)": c_eff(C_NEW_MARGINAL[n], K_NEW, KX_NEW),
        "new, Poisson kx=1.67 band edge": c_eff(C_NEW[n], 1.1888, 1.67),
    }
    print(f"{'case':46s} {'c_eff':>7} {'mu[g]':>7} {'N0':>7} {'N(>=m_thr)':>11}"
          f" {'/Tolch 700':>11} {'/Tolch 779':>11}")
    for label, ce in cases.items():
        mu, n0, nn = lev.resolve_chain(ce)
        print(f"{label:46s} {ce:7.4f} {mu:7.4f} {n0:7.1f} {nn:11.1f}"
              f" {nn / lev.TOLCH_LOW:11.2f} {nn / lev.TOLCH_HIGH:11.2f}")


if __name__ == "__main__":
    mu_multipliers()
    count_chain_75()
    bofr_155()
