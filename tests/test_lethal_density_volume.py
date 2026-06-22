r"""Tests for the 3D lethal-density volume builders (pkill-3d-surface-view).

Coverage map
============

compute_lethal_density_volume_3d  (arty.fragmentation)
  • z=0 layer (rho_L[0]) is numerically identical to
    compute_lethal_density_field_3d(z=0.0) for matching parameters — confirms
    the volume builder is a pure per-z stacking wrapper with no new physics.
  • Returned X, Y, Z, rho_L all share shape (n_z, n_grid, n_grid); Z[0] == 0.

four_zone_lethal_density_volume  (arty.zones)
  • z=0 layer (rho_L[0]) is numerically identical to
    four_zone_lethal_density_field(z=0.0) for matching parameters.
  • Returned X, Y, Z, rho_L all share shape (n_z, n_grid, n_grid); Z[0] == 0.

These guard the no-new-physics contract: the volume is exactly the single-z
field stacked over heights, so the ground (z=0) slice must reproduce the
existing single-z function bit-for-bit (same code path, same s_grid).
"""

import numpy as np
import pytest

from arty.fragmentation import (
    BurstParams,
    DragParams,
    E_LETH_DEFAULT,
    ShellParams,
    compute_lethal_density_field_3d,
    compute_lethal_density_volume_3d,
)
from arty.shells import SHELLS
from arty.zones import (
    compute_shell_zones,
    four_zone_lethal_density_field,
    four_zone_lethal_density_volume,
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


# ---------------------------------------------------------------------------
# Single-zone volume builder
# ---------------------------------------------------------------------------


def test_single_zone_volume_z0_matches_single_z_field(shell, drag, burst):
    """rho_L[0] of the volume equals the single-z field at z=0 exactly."""
    _, _, _, rho_L_vol = compute_lethal_density_volume_3d(
        shell=shell, drag=drag, burst=burst,
        z_max=Z_MAX, max_radius=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, rho_L_ref = compute_lethal_density_field_3d(
        shell=shell, drag=drag, burst=burst,
        z=0.0, max_radius=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    np.testing.assert_allclose(rho_L_vol[0], rho_L_ref, rtol=0.0, atol=0.0)


def test_single_zone_volume_shapes_and_ground_layer(shell, drag, burst):
    """X, Y, Z, rho_L share the (n_z, n_grid, n_grid) shape; Z[0] is the ground."""
    X, Y, Z, rho_L = compute_lethal_density_volume_3d(
        shell=shell, drag=drag, burst=burst,
        z_max=Z_MAX, max_radius=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    expected_shape = (N_Z, N_GRID, N_GRID)
    assert X.shape == Y.shape == Z.shape == rho_L.shape == expected_shape
    np.testing.assert_array_equal(Z[0], np.zeros((N_GRID, N_GRID)))
    assert Z[-1].max() == pytest.approx(Z_MAX)


# ---------------------------------------------------------------------------
# Four-zone volume builder
# ---------------------------------------------------------------------------


def test_four_zone_volume_z0_matches_single_z_field(zones_m1, drag):
    """rho_L[0] of the four-zone volume equals the four-zone field at z=0 exactly."""
    rho_steel = ShellParams().steel.rho
    _, _, _, rho_L_vol = four_zone_lethal_density_volume(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z_max=Z_MAX, max_r=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, rho_L_ref = four_zone_lethal_density_field(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z=0.0, max_r=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    np.testing.assert_allclose(rho_L_vol[0], rho_L_ref, rtol=0.0, atol=0.0)


def test_four_zone_volume_shapes_and_ground_layer(zones_m1, drag):
    """X, Y, Z, rho_L share the (n_z, n_grid, n_grid) shape; Z[0] is the ground."""
    rho_steel = ShellParams().steel.rho
    X, Y, Z, rho_L = four_zone_lethal_density_volume(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z_max=Z_MAX, max_r=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    expected_shape = (N_Z, N_GRID, N_GRID)
    assert X.shape == Y.shape == Z.shape == rho_L.shape == expected_shape
    np.testing.assert_array_equal(Z[0], np.zeros((N_GRID, N_GRID)))
    assert Z[-1].max() == pytest.approx(Z_MAX)
