r"""Tests for src/arty/zones.py

Coverage map
============

compute_shell_zones  (Tier-1: M1, M107 — Tier-2: M48, synthetic)
  • Cylinder zone spray angle is exactly 90° for M1 and M107.
  • Ogive spray angle < 90° for M1 and M107.
  • Boattail spray angle > 90° when boattail present (M1, M107).
  • Zone masses sum to total shell steel within 1% (M1, M107, M48).
  • M1 ogive mass fraction: 0.25–0.42 (short ogive, drawing geometry).
  • M1 cylinder mass fraction: 0.35–0.55.
  • M107 ogive mass fraction: 0.45–0.65 (long ogive, drawing geometry).
  • M107 cylinder mass fraction: 0.20–0.35.
  • M1 ogive spray angle in 75–88°.
  • M107 ogive spray angle in 75–88°.
  • M48 secant ogive spray angle in 83–88° (> full-tangent CRH-7.43 ~79.6°).
  • Tier-2 without boattail: boattail mass == 0, cylinder fraction ≈ 0.53.
  • Tier-2 without ogive_len: spray angle matches full-tangent formula within 0.1°.

fragment_ground_impact
  • Vertical shell (AoF=90°), 8 azimuths: ring radius == h_b × tan(theta).
  • Horizontal equatorial fragment (theta=90°, phi=0, AoF=0°): returns None.
  • AoF=30°, cylinder zone, phi=π/2: x_hit > 0 (forward hemisphere).
  • Doubling h_b doubles x_hit and y_hit within 1e-9.

four_zone_field
  • Field has non-zero values at AoF=30°.
  • Field is NOT azimuthally symmetric at AoF=30° (asymmetric physics).
  • Field IS azimuthally symmetric (pk == pk.T) at AoF=90°, within 1e-10.

_four_zone_field_split
  • pk_total matches four_zone_field output exactly (same loop body).
  • Returns dict with keys ogive/cylinder/boattail/base.
  • Each per-zone pk in [0, 1] everywhere.
  • Per-zone pk <= pk_total at every grid point.

four_zone_line_split
  • fixed_axis="x" line matches the corresponding _four_zone_field_split
    grid column (total and per-zone) at shared nodes.
  • fixed_axis="y" line matches the corresponding _four_zone_field_split
    grid row (total and per-zone) at shared nodes.
"""

import math

import numpy as np
import pytest

from arty.fragmentation import FILLERS, STANDING, DragParams, ShellParams, STEELS, retardation_coeff
from arty.shells import SHELLS
from arty.zones import (
    _four_zone_field_split,
    compute_shell_zones,
    four_zone_field,
    four_zone_line_split,
    fragment_ground_impact,
)


# ---------------------------------------------------------------------------
# Module-scoped fixtures (expensive: avoid recomputing per test)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def m1_zones():
    return compute_shell_zones(SHELLS["105mm M1 HE"])


@pytest.fixture(scope="module")
def m107_zones():
    return compute_shell_zones(SHELLS["155mm M107 HE"])


@pytest.fixture(scope="module")
def m48_zones():
    return compute_shell_zones(SHELLS["75mm M48 HE"])


@pytest.fixture(scope="module")
def field_grids():
    """Shared drag_lam_grid and m_grid for four_zone_field tests (small n for speed)."""
    m_grid = np.linspace(1e-4, 0.1, 30)
    shell = SHELLS["105mm M1 HE"]
    drag_lam = retardation_coeff(m_grid, DragParams(), shell.steel.rho)
    return drag_lam, m_grid


# ---------------------------------------------------------------------------
# compute_shell_zones — spray angles
# ---------------------------------------------------------------------------


def test_cylinder_spray_90_m1(m1_zones):
    assert m1_zones.cylinder.spray_deg == pytest.approx(90.0)


def test_cylinder_spray_90_m107(m107_zones):
    assert m107_zones.cylinder.spray_deg == pytest.approx(90.0)


def test_ogive_spray_lt_90_m1(m1_zones):
    assert m1_zones.ogive.spray_deg < 90.0


def test_ogive_spray_lt_90_m107(m107_zones):
    assert m107_zones.ogive.spray_deg < 90.0


def test_boattail_spray_gt_90_m1(m1_zones):
    assert m1_zones.boattail.spray_deg > 90.0


def test_boattail_spray_gt_90_m107(m107_zones):
    assert m107_zones.boattail.spray_deg > 90.0


def test_m1_ogive_spray_angle_range(m1_zones):
    assert 75.0 <= m1_zones.ogive.spray_deg <= 88.0


def test_m107_ogive_spray_angle_range(m107_zones):
    assert 75.0 <= m107_zones.ogive.spray_deg <= 88.0


def test_m48_secant_spray_angle_range(m48_zones):
    # Full-tangent CRH 7.43 gives ≈79.6°; secant midpoint at 0.59 cal gives ≈85.4°
    assert 83.0 <= m48_zones.ogive.spray_deg <= 88.0, (
        f"M48 secant spray {m48_zones.ogive.spray_deg:.1f}° outside 83–88°"
    )


# ---------------------------------------------------------------------------
# compute_shell_zones — zone masses
# ---------------------------------------------------------------------------


def test_zone_masses_sum_m1(m1_zones):
    s = SHELLS["105mm M1 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    zone_sum = (m1_zones.ogive.mass_kg + m1_zones.cylinder.mass_kg
                + m1_zones.boattail.mass_kg + m1_zones.base.mass_kg)
    assert zone_sum == pytest.approx(total, rel=0.01)


def test_zone_masses_sum_m107(m107_zones):
    s = SHELLS["155mm M107 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    zone_sum = (m107_zones.ogive.mass_kg + m107_zones.cylinder.mass_kg
                + m107_zones.boattail.mass_kg + m107_zones.base.mass_kg)
    assert zone_sum == pytest.approx(total, rel=0.01)


def test_zone_masses_sum_m48(m48_zones):
    s = SHELLS["75mm M48 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    zone_sum = (m48_zones.ogive.mass_kg + m48_zones.cylinder.mass_kg
                + m48_zones.boattail.mass_kg + m48_zones.base.mass_kg)
    assert zone_sum == pytest.approx(total, rel=0.01)


def test_m1_ogive_mass_fraction(m1_zones):
    s = SHELLS["105mm M1 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    frac = m1_zones.ogive.mass_kg / total
    assert 0.25 <= frac <= 0.42, f"M1 ogive fraction {frac:.3f} outside 0.25–0.42"


def test_m1_cylinder_mass_fraction(m1_zones):
    s = SHELLS["105mm M1 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    frac = m1_zones.cylinder.mass_kg / total
    assert 0.35 <= frac <= 0.55, f"M1 cylinder fraction {frac:.3f} outside 0.35–0.55"


def test_m107_ogive_mass_fraction(m107_zones):
    s = SHELLS["155mm M107 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    frac = m107_zones.ogive.mass_kg / total
    assert 0.45 <= frac <= 0.65, f"M107 ogive fraction {frac:.3f} outside 0.45–0.65"


def test_m107_cylinder_mass_fraction(m107_zones):
    s = SHELLS["155mm M107 HE"]
    total = s.mass_total - s.mass_filler - s.mass_deductions
    frac = m107_zones.cylinder.mass_kg / total
    assert 0.20 <= frac <= 0.35, f"M107 cylinder fraction {frac:.3f} outside 0.20–0.35"


# ---------------------------------------------------------------------------
# compute_shell_zones — Tier-2 edge cases
# ---------------------------------------------------------------------------


def _tier2_shell(**kwargs) -> ShellParams:
    return ShellParams(
        caliber=0.105,
        wall_t=0.009208,
        mass_total=14.97,
        mass_filler=2.18,
        mass_deductions=0.0,
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
        **kwargs,
    )


def test_tier2_no_boattail_zero_mass():
    zones = compute_shell_zones(_tier2_shell(has_boattail=False))
    assert zones.boattail.mass_kg == pytest.approx(0.0)


def test_tier2_no_boattail_cylinder_fraction():
    shell = _tier2_shell(has_boattail=False)
    zones = compute_shell_zones(shell)
    total = shell.mass_total - shell.mass_filler - shell.mass_deductions
    assert zones.cylinder.mass_kg / total == pytest.approx(0.53, rel=0.01)


def test_tier2_with_boattail_masses_sum():
    shell = _tier2_shell(has_boattail=True)
    zones = compute_shell_zones(shell)
    total = shell.mass_total - shell.mass_filler - shell.mass_deductions
    zone_sum = (zones.ogive.mass_kg + zones.cylinder.mass_kg
                + zones.boattail.mass_kg + zones.base.mass_kg)
    assert zone_sum == pytest.approx(total, rel=0.01)


def test_tier2_full_tangent_spray_angle():
    # Without ogive_len, full-tangent CRH-6 formula applies.
    shell = _tier2_shell(ogive_crh=6.0)
    zones = compute_shell_zones(shell)
    expected = 90.0 - math.degrees(math.asin(math.sqrt(6.0 - 0.25) / (2.0 * 6.0)))
    assert zones.ogive.spray_deg == pytest.approx(expected, abs=0.1)


# ---------------------------------------------------------------------------
# fragment_ground_impact
# ---------------------------------------------------------------------------


def test_vertical_shell_ring_radius():
    # AoF=90°: 8 azimuths all land at h_b * tan(theta) from burst nadir
    theta_deg = 80.0
    h_b = 5.0
    expected_r = h_b * math.tan(math.radians(theta_deg))
    phis = np.linspace(0, 2 * math.pi, 8, endpoint=False)
    for phi in phis:
        result = fragment_ground_impact(theta_deg, phi, aof_deg=90.0, h_b=h_b)
        assert result is not None, f"phi={phi:.2f} returned None"
        x, y, _ = result
        assert math.hypot(x, y) == pytest.approx(expected_r, abs=1e-3)


def test_horizontal_equatorial_returns_none():
    # Horizontal shell (AoF=0), spray at 90°, phi=0 → fragment goes horizontally, never hits ground
    result = fragment_ground_impact(90.0, 0.0, aof_deg=0.0, h_b=2.0)
    assert result is None


def test_forward_hit_positive_x():
    # theta=70° (forward-biased spray), phi=0, AoF=30° → vgz<0 (reaches ground) and vgx>0
    # Note: cylinder zone (90°) at AoF=30° cannot hit forward — vgz = cos(AoF)*sin(phi) > 0.
    result = fragment_ground_impact(70.0, 0.0, aof_deg=30.0, h_b=2.0)
    assert result is not None
    x_hit, _, _ = result
    assert x_hit > 0


def test_hb_doubling_doubles_hit_coords():
    theta, phi, aof = 70.0, 0.0, 30.0
    r1 = fragment_ground_impact(theta, phi, aof, h_b=2.0)
    r2 = fragment_ground_impact(theta, phi, aof, h_b=4.0)
    assert r1 is not None and r2 is not None
    x1, y1, _ = r1
    x2, y2, _ = r2
    assert abs(x2 - 2 * x1) < 1e-9
    assert abs(y2 - 2 * y1) < 1e-9


# ---------------------------------------------------------------------------
# four_zone_field
# ---------------------------------------------------------------------------


def test_four_zone_field_nonzero(m1_zones, field_grids):
    drag_lam, m_grid = field_grids
    _, _, pk = four_zone_field(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    assert pk.max() > 0.0


def test_four_zone_field_asymmetric_at_30deg(m1_zones, field_grids):
    # At AoF=30°, swapping x↔y changes the physics (line-of-fire vs cross-range)
    drag_lam, m_grid = field_grids
    _, _, pk = four_zone_field(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=21,
    )
    assert pk.max() > 0.0
    assert not np.allclose(pk, pk.T, atol=1e-4), "Field should be asymmetric at AoF=30°"


def test_four_zone_field_symmetric_at_90deg(m1_zones, field_grids):
    # At AoF=90° (vertical shell), acceptance test depends only on slant range → pk[i,j] == pk[j,i]
    drag_lam, m_grid = field_grids
    _, _, pk = four_zone_field(
        m1_zones, aof_deg=90.0, h_b=5.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=21,
    )
    np.testing.assert_allclose(pk, pk.T, atol=1e-10)


# ---------------------------------------------------------------------------
# _four_zone_field_split
# ---------------------------------------------------------------------------


def test_split_total_matches_four_zone_field(m1_zones, field_grids):
    # The two functions share the same loop body; pk_total must be bit-for-bit equal.
    drag_lam, m_grid = field_grids
    _, _, pk_ref = four_zone_field(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    _, _, pk_tot, _ = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    np.testing.assert_array_equal(pk_ref, pk_tot)


def test_split_returns_four_zone_keys(m1_zones, field_grids):
    drag_lam, m_grid = field_grids
    _, _, _, pk_by_zone = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    assert set(pk_by_zone.keys()) == {"ogive", "cylinder", "boattail", "base"}


def test_split_per_zone_in_unit_interval(m1_zones, field_grids):
    drag_lam, m_grid = field_grids
    _, _, _, pk_by_zone = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    for name, pk_z in pk_by_zone.items():
        assert np.all(pk_z >= -1e-12), f"{name} has negative P(kill)"
        assert np.all(pk_z <= 1.0 + 1e-12), f"{name} P(kill) exceeds 1"


def test_split_per_zone_leq_total(m1_zones, field_grids):
    drag_lam, m_grid = field_grids
    _, _, pk_tot, pk_by_zone = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, n_grid=15,
    )
    for name, pk_z in pk_by_zone.items():
        assert np.all(pk_z <= pk_tot + 1e-10), f"{name} zone P(kill) exceeds total"


def test_base_zone_skipped_when_all_fragments_go_upward(m1_zones, field_grids):
    """Base zone spray=165° at AoF=30°: sin(30+165)=sin(195°)<0, all fragments
    go upward (vgz>=0 for all azimuths).  The guard must zero the base-zone
    contribution in the backward ground region."""
    drag_lam, m_grid = field_grids
    # Without the guard, a backward point at x=-50 would receive false base-zone pk.
    _, _, _, pk_by_zone = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, max_r=80.0, n_grid=15,
    )
    assert np.all(pk_by_zone["base"] == 0.0), (
        "base zone must contribute zero pk when no fragment can reach the ground"
    )


# ---------------------------------------------------------------------------
# four_zone_line_split
# ---------------------------------------------------------------------------


def test_line_split_matches_grid_fixed_x(m1_zones, field_grids):
    # fixed_axis="x" holds the grid's column (downrange) index and sweeps
    # cross-range y — must reproduce that column of the square grid exactly.
    drag_lam, m_grid = field_grids
    max_r, n_grid = 80.0, 15
    xy = np.linspace(-max_r, max_r, n_grid)
    j_fixed = n_grid // 2 + 2

    _, _, pk_grid, pk_by_zone_grid = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, max_r=max_r, n_grid=n_grid,
    )
    pk_line, pk_by_zone_line = four_zone_line_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid,
        fixed_axis="x", fixed_coord=xy[j_fixed], line_coords=xy,
    )
    np.testing.assert_array_equal(pk_line, pk_grid[:, j_fixed])
    for name in pk_by_zone_grid:
        np.testing.assert_array_equal(pk_by_zone_line[name], pk_by_zone_grid[name][:, j_fixed])


def test_line_split_matches_grid_fixed_y(m1_zones, field_grids):
    # fixed_axis="y" holds the grid's row (cross-range) index and sweeps
    # downrange x — must reproduce that row of the square grid exactly.
    drag_lam, m_grid = field_grids
    max_r, n_grid = 80.0, 15
    xy = np.linspace(-max_r, max_r, n_grid)
    i_fixed = n_grid // 2 - 3

    _, _, pk_grid, pk_by_zone_grid = _four_zone_field_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid, max_r=max_r, n_grid=n_grid,
    )
    pk_line, pk_by_zone_line = four_zone_line_split(
        m1_zones, aof_deg=30.0, h_b=2.0, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid,
        fixed_axis="y", fixed_coord=xy[i_fixed], line_coords=xy,
    )
    np.testing.assert_array_equal(pk_line, pk_grid[i_fixed, :])
    for name in pk_by_zone_grid:
        np.testing.assert_array_equal(pk_by_zone_line[name], pk_by_zone_grid[name][i_fixed, :])
