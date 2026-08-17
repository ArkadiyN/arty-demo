"""Shipped per-shell A_eff = c*1.6 vs derivation.md sec. 7, and its effect on mu / N0.

Consumer: experiment/fragmentation-field/updates/mass-dependent-fragment-shape/
derivation.md sec. 7 (implementation pass) -- confirms that arty.shells.SHELLS
ships the method-B ("cond-m") per-shell aspect-ratio moment correction and that
the resulting Mott mu / N0 move exactly as 1/(c) and c predict.

The c values themselves are produced by checks/per-shell-c-and-75mm-count-chain.py
(column "B: cond-m"); this script only checks that what is SHIPPED equals them
and that nothing else in the chain moved.
"""
import dataclasses

from arty.fragmentation import (
    _MOTT_ASPECT_RATIO,
    MOTT_ASPECT_MOMENT_C,
    gurney_velocity,
    mott_params,
)
from arty.shells import SHELLS

# derivation.md sec. 3.3b table, method B (central), and sec. 7's A_eff column.
EXPECT_C = {"155mm M107 HE": 1.2506, "105mm M1 HE": 1.1024,
            "75mm M48 HE": 0.9854, "60mm M49A2 HE": 0.9200}
EXPECT_A_EFF = {"155mm M107 HE": 2.00, "105mm M1 HE": 1.76,
                "75mm M48 HE": 1.58, "60mm M49A2 HE": 1.47}

GR = 0.06479891e-3  # kg per grain

print(f"{'shell':>15} {'c':>7} {'A_eff':>7} {'sec.7':>6} "
      f"{'mu0[gr]':>8} {'mu[gr]':>8} {'N0_0':>7} {'N0':>7} {'N0 ratio':>9}")
ok = True
for name, sh in SHELLS.items():
    c = MOTT_ASPECT_MOMENT_C[name]
    a_eff = sh.aspect_ratio
    sh0 = dataclasses.replace(sh, aspect_ratio=_MOTT_ASPECT_RATIO)

    mu0, _ = mott_params(sh0, gurney_velocity(sh0))
    mu, _ = mott_params(sh, gurney_velocity(sh))
    m_case = sh.mass_total - sh.mass_filler - sh.mass_deductions
    n0_0, n0 = m_case / (2 * mu0), m_case / (2 * mu)

    ok &= abs(a_eff - c * _MOTT_ASPECT_RATIO) < 1e-12          # ships c*A
    ok &= abs(c - EXPECT_C[name]) < 5e-5                       # method B value
    ok &= abs(a_eff - EXPECT_A_EFF[name]) < 5e-3               # sec. 7 table
    ok &= abs(mu / mu0 - c) < 1e-9                             # mu ~ A exactly
    ok &= abs(n0 / n0_0 - 1 / c) < 1e-9                        # N0 ~ 1/(cA)

    print(f"{name:>15} {c:7.4f} {a_eff:7.3f} {EXPECT_A_EFF[name]:6.2f} "
          f"{mu0 / GR:8.2f} {mu / GR:8.2f} {n0_0:7.0f} {n0:7.0f} "
          f"{n0 / n0_0:8.3f}x")

print("\nlimit checks: c=1 must reproduce the pre-update model exactly")
sh = SHELLS["105mm M1 HE"]
mu_c1, _ = mott_params(dataclasses.replace(sh, aspect_ratio=_MOTT_ASPECT_RATIO),
                       gurney_velocity(sh))
print(f"  105mm mu at A=1.6 = {mu_c1 / GR:.4f} gr  (shipped mu / c = "
      f"{mott_params(sh, gurney_velocity(sh))[0] / GR / MOTT_ASPECT_MOMENT_C['105mm M1 HE']:.4f} gr)")
ok &= abs(mu_c1 / mott_params(sh, gurney_velocity(sh))[0]
          * MOTT_ASPECT_MOMENT_C["105mm M1 HE"] - 1.0) < 1e-12

print("\nPASS" if ok else "\nFAIL")
