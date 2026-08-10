"""Plug-shear wood-perforation threshold: src/arty/perforation.py.

Pins arty.perforation to the table printed by the independently-verified check
script
``experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/checks/plug-shear-perforation-threshold.py``
and reproduced in that update's ``derivation.md`` §7.4, and pins the
threshold-callable plumbing added to arty.fragmentation (§7.6) to be a no-op at
its default.
"""

import numpy as np
import pytest

from arty.fragmentation import DragParams, build_mmin_table, min_lethal_mass
from arty.perforation import (
    TAU_SPFS,
    TAU_SYP,
    WoodPanelTarget,
    ballistic_limit_velocity,
    compact_fragment_diameter,
    perforation_threshold_energy,
)

# derivation.md §7.4 check 2 / check-script §3: m [g], D [mm], v50 [m/s], E_thr [J]
TABLE_7_4 = [
    (0.05, 2.30, 914.1, 20.9),
    (0.10, 2.90, 725.5, 26.3),
    (0.63, 5.35, 392.8, 48.6),
    (2.00, 7.87, 267.3, 71.4),
    (10.0, 13.45, 156.3, 122.2),
    (50.0, 23.00, 91.4, 208.9),
]


@pytest.mark.parametrize("m_g,d_mm,v50,e_thr", TABLE_7_4)
def test_matches_derivation_table(m_g, d_mm, v50, e_thr):
    m = m_g / 1000.0
    assert compact_fragment_diameter(m) * 1e3 == pytest.approx(d_mm, abs=0.005)
    assert perforation_threshold_energy(m) == pytest.approx(e_thr, abs=0.05)
    assert ballistic_limit_velocity(m) == pytest.approx(v50, abs=0.05)


def test_scaling_exponents_and_limits():
    """E_thr ∝ m^(1/3) rising, v50 ∝ m^(-1/3) falling — derivation §7.3 eq. (10)."""
    m = np.array([m_g / 1000.0 for m_g, *_ in TABLE_7_4])
    e = perforation_threshold_energy(m)
    v = ballistic_limit_velocity(m)
    assert np.all(np.diff(e) > 0)
    assert np.all(np.diff(v) < 0)
    # doubling mass multiplies E_thr by 2^(1/3) exactly
    assert perforation_threshold_energy(2e-3) / perforation_threshold_energy(1e-3) == (
        pytest.approx(2.0 ** (1.0 / 3.0))
    )
    assert ballistic_limit_velocity(1e-9) > ballistic_limit_velocity(1e-6)


def test_linear_in_tau_and_quadratic_in_thickness():
    """Sensitivity claim of §7.4: E_thr enters tau at power 1 (not 4.86)."""
    m = 0.63e-3
    base = perforation_threshold_energy(m)
    doubled = perforation_threshold_energy(m, WoodPanelTarget(tau=2 * TAU_SPFS))
    assert doubled / base == pytest.approx(2.0)
    thick = perforation_threshold_energy(m, WoodPanelTarget(t=2 * 0.0254))
    assert thick / base == pytest.approx(4.0)


def test_syp_band_and_check1_forward_clt_panel():
    """§7.4 check 1: forward-apply eq. (9) to Sanborn's own 6.875 in CLT panel.

    The check script feeds Sanborn's *nominal* 12.7 mm sphere diameter; this
    module always derives D from the mass, which for the same 8.4 g steel sphere
    gives 12.683 mm. The two agree to 0.14% in D, hence 0.09% in E_thr — the
    rel=0.002 below is that closure, not slack.
    """
    m_sphere, t_clt = 0.0084, 6.875 * 0.0254
    assert compact_fragment_diameter(m_sphere) * 1e3 == pytest.approx(12.7, abs=0.02)
    spfs = WoodPanelTarget(t=t_clt)
    syp = WoodPanelTarget(tau=TAU_SYP, t=t_clt)
    assert perforation_threshold_energy(m_sphere, spfs) == pytest.approx(5453, rel=0.002)
    assert perforation_threshold_energy(m_sphere, syp) == pytest.approx(6711, rel=0.002)
    assert ballistic_limit_velocity(m_sphere, spfs) == pytest.approx(1139, abs=1.0)
    assert ballistic_limit_velocity(m_sphere, syp) == pytest.approx(1264, abs=1.0)


def test_threshold_callable_default_is_unchanged():
    """E_thr=None must reproduce today's scalar >= E_leth path bit-identically."""
    drag, rho, V0, E = DragParams(), 7850.0, 1200.0, 1000.0
    s_grid = np.linspace(1.0, 120.0, 40)
    ref = build_mmin_table(s_grid, V0, E, drag, rho)
    same = build_mmin_table(s_grid, V0, E, drag, rho, E_thr=None)
    assert np.array_equal(ref, same)
    explicit = build_mmin_table(s_grid, V0, E, drag, rho, E_thr=lambda m: E * np.ones_like(m))
    assert np.array_equal(ref, explicit)
    for s in (5.0, 40.0, 100.0):
        assert min_lethal_mass(s, V0, E, drag, rho) == min_lethal_mass(
            s, V0, E, drag, rho, E_thr=lambda m: E
        )


def test_threshold_callable_scalar_matches_vectorised():
    """Scalar bisection and the vectorised table agree under the plug-shear criterion."""
    drag, rho, V0 = DragParams(), 7850.0, 1200.0
    s_grid = np.array([5.0, 20.0, 60.0, 120.0])
    table = build_mmin_table(
        s_grid, V0, 1000.0, drag, rho, E_thr=perforation_threshold_energy
    )
    for s, m_tab in zip(s_grid, table):
        m_sc = min_lethal_mass(
            float(s), V0, 1000.0, drag, rho, E_thr=perforation_threshold_energy
        )
        assert m_sc == pytest.approx(m_tab, rel=1e-9, abs=1e-12)
    # the wood criterion is more permissive than the 1000 J personnel scalar
    assert np.all(table <= build_mmin_table(s_grid, V0, 1000.0, drag, rho))


def test_crossover_against_the_78_6_j_probe():
    """§7.4: eq. (9) and a constant 78.6 J cross at v = 243 m/s (m_min crossover)."""
    # E_thr(m) = 78.6 J  =>  m at which the two criteria pick the same fragment
    m_star = (78.6 / perforation_threshold_energy(1.0)) ** 3.0
    v_star = np.sqrt(2.0 * 78.6 / m_star)
    assert v_star == pytest.approx(243.0, abs=1.0)
