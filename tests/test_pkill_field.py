r"""Tests for the Poisson kill-probability transform P_k = 1 − exp(−ρ_L·A_ref).

Coverage map
============

pkill_field_3d / pkill_volume_3d            (arty.fragmentation, single-zone)
four_zone_pkill_field / four_zone_pkill_volume (arty.zones, four-zone)

  • ρ_L=0 ⇒ P_k=0           — empty field maps to zero kill probability.
  • monotone in ρ_L         — denser lethal field never lowers P_k.
  • bounds P_k ∈ [0, 1]     — the saturating exponential stays in range.
  • volume z=0 point-transform — the (unchanged) *_pkill_volume ground layer
                              reproduces the frozen-A_ref point transform of the
                              ground-plane ρ_L bit-for-bit (point-in-space
                              diagnostic; target-height-intercept derivation §8).
  • ground-field column integral — the *_pkill_field ground fields now form
                              λ = w_perp·∫₀ʰ ρ_L dz (posture-coupled) instead of
                              the ρ_L(z=0)·A_ref point transform, so a standing
                              target is never scored less lethal than a prone one
                              and the AoF=90° close-in false safe ring is filled
                              (derivation §4, §6.3).

The volume builders (*_pkill_volume) keep the frozen A_ref point transform and
are the point-in-space diagnostic; the ground fields (*_pkill_field) switched to
the vertical-column integral. The ρ_L kernel itself is *not* re-tested here (see
test_lethal_density_volume.py).
"""

import numpy as np
import pytest

from arty.fragmentation import (
    A_REF_DEFAULT,
    PRONE,
    STANDING,
    BurstParams,
    DragParams,
    E_LETH_DEFAULT,
    ShellParams,
    compute_lethal_density_field_3d,
    pkill_field_3d,
    pkill_volume_3d,
)
from arty.shells import SHELLS
from arty.zones import (
    compute_shell_zones,
    four_zone_lethal_density_field,
    four_zone_pkill_field,
    four_zone_pkill_volume,
)

# Small, fast grids shared between volume and single-z reference calls.
N_GRID = 12
N_Z = 5
MAX_R = 50.0
Z_MAX = 8.0


@pytest.fixture
def shell():
    return ShellParams()


@pytest.fixture
def drag():
    return DragParams()


@pytest.fixture
def burst():
    return BurstParams()


@pytest.fixture
def zones_m1():
    return compute_shell_zones(SHELLS["105mm M1 HE"])


def _pk(rho_L, A_ref=A_REF_DEFAULT):
    return 1.0 - np.exp(-rho_L * A_ref)


# ---------------------------------------------------------------------------
# Transform invariants (geometry-independent)
# ---------------------------------------------------------------------------


def test_transform_zero_density_gives_zero_pkill():
    """ρ_L = 0 ⇒ P_k = 0 everywhere."""
    rho_L = np.zeros((4, 4))
    np.testing.assert_array_equal(_pk(rho_L), np.zeros((4, 4)))


def test_transform_monotone_in_density():
    """P_k is non-decreasing in ρ_L for any A_ref > 0."""
    rho_L = np.linspace(0.0, 5.0, 50)
    P_k = _pk(rho_L)
    assert np.all(np.diff(P_k) >= 0.0)


def test_transform_bounds():
    """P_k ∈ [0, 1] even for very large ρ_L (saturates, never exceeds 1)."""
    rho_L = np.array([0.0, 1e-3, 1.0, 1e3, 1e6])
    P_k = _pk(rho_L)
    assert np.all((P_k >= 0.0) & (P_k <= 1.0))


# ---------------------------------------------------------------------------
# Single-zone wrappers
# ---------------------------------------------------------------------------


def test_single_zone_pkill_field_bounds(shell, drag, burst):
    """pkill_field_3d returns P_k ∈ [0, 1] on a real field."""
    _, _, P_k = pkill_field_3d(
        shell=shell, drag=drag, burst=burst,
        max_radius=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k >= 0.0) & (P_k <= 1.0))


def test_single_zone_pkill_volume_z0_is_point_transform(shell, drag, burst):
    """Volume's z=0 layer equals the frozen-A_ref point transform of ρ_L(z=0).

    The volume builder is the unchanged point-in-space diagnostic (still
    P_k = 1 − exp(−ρ_L·A_ref)); its ground layer must reproduce that transform
    of the ground-plane density exactly. (It no longer matches pkill_field_3d,
    which now integrates the vertical column — derivation §8.)
    """
    _, _, _, P_k_vol = pkill_volume_3d(
        shell=shell, drag=drag, burst=burst,
        z_max=Z_MAX, max_radius=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, rho_L0 = compute_lethal_density_field_3d(
        shell=shell, drag=drag, burst=burst,
        z=0.0, max_radius=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k_vol >= 0.0) & (P_k_vol <= 1.0))
    np.testing.assert_allclose(P_k_vol[0], _pk(rho_L0), rtol=0.0, atol=0.0)


def test_single_zone_pkill_field_posture_and_false_safe_ring(shell, drag):
    """Column-integral field: standing ≥ prone, and AoF=90° close-in ring filled.

    The vertical-column λ = w_perp·∫₀ʰ ρ_L dz re-couples posture (taller column
    never scores lower) and fills the false safe ring — under a horizontal belt
    (AoF=90°) a standing target close in is struck at chest/head height where the
    old ρ_L(z=0) transform read zero (derivation §4, §6.3).
    """
    burst = BurstParams(angle_of_fall=90.0, spray_half_angle=15.0, h_b=2.0)
    _, _, P_k_stand = pkill_field_3d(
        shell=shell, drag=drag, burst=burst, posture=STANDING,
        max_radius=20.0, n_grid=41, E_leth=E_LETH_DEFAULT,
    )
    _, _, P_k_prone = pkill_field_3d(
        shell=shell, drag=drag, burst=burst, posture=PRONE,
        max_radius=20.0, n_grid=41, E_leth=E_LETH_DEFAULT,
    )
    assert P_k_stand.max() >= P_k_prone.max()
    # Close-in ring (r ≈ 2–7 m, well inside the old 7.5 m z=0 edge) is now lethal.
    r = np.hypot(*np.meshgrid(np.linspace(-20, 20, 41), np.linspace(-20, 20, 41)))
    ring = (r > 2.0) & (r < 7.0)
    assert P_k_stand[ring].max() > 0.5


# ---------------------------------------------------------------------------
# Four-zone wrappers
# ---------------------------------------------------------------------------


def test_four_zone_pkill_field_bounds(zones_m1, drag):
    """four_zone_pkill_field returns P_k ∈ [0, 1] on a real field."""
    rho_steel = ShellParams().steel.rho
    _, _, P_k = four_zone_pkill_field(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        max_r=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k >= 0.0) & (P_k <= 1.0))


def test_four_zone_pkill_volume_z0_is_point_transform(zones_m1, drag):
    """Four-zone volume's z=0 layer equals the A_ref point transform of ρ_L(z=0).

    The four-zone volume builder is the unchanged point-in-space diagnostic; its
    ground layer reproduces P_k = 1 − exp(−ρ_L·A_ref) of the ground-plane
    density (no longer the column-integral four_zone_pkill_field — derivation §8).
    """
    rho_steel = ShellParams().steel.rho
    _, _, _, P_k_vol = four_zone_pkill_volume(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z_max=Z_MAX, max_r=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, rho_L0 = four_zone_lethal_density_field(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z=0.0, max_r=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k_vol >= 0.0) & (P_k_vol <= 1.0))
    np.testing.assert_allclose(P_k_vol[0], _pk(rho_L0), rtol=0.0, atol=0.0)


def test_four_zone_pkill_field_posture_and_false_safe_ring(zones_m1, drag):
    """Four-zone column-integral field: standing ≥ prone, and AoF=90° ring filled.

    The column integral reads (w_perp, h) live from posture, so extending the
    column (standing) only adds non-negative flux (derivation §4, §6.4). As in
    the single-zone counterpart, the vertical column also fills the close-in
    false safe ring: under a horizontal belt (AoF=90°) a standing target close
    in is struck at chest/head height where the old ρ_L(z=0) transform read zero
    (derivation §1, §6.3) — this test locks in that the four-zone K-generalized
    path fills it, not just that standing ≥ prone.
    """
    rho_steel = ShellParams().steel.rho
    X, Y, P_k_stand = four_zone_pkill_field(
        zones_m1, aof_deg=90.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        posture=STANDING, max_r=30.0, n_grid=31, E_leth=E_LETH_DEFAULT,
    )
    _, _, P_k_prone = four_zone_pkill_field(
        zones_m1, aof_deg=90.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        posture=PRONE, max_r=30.0, n_grid=31, E_leth=E_LETH_DEFAULT,
    )
    assert P_k_stand.max() >= P_k_prone.max()
    # Close-in ring (r ≈ 2–7 m, well inside the old z=0 edge) is now lethal.
    r = np.hypot(X, Y)
    ring = (r > 2.0) & (r < 7.0)
    assert P_k_stand[ring].max() > 0.5
