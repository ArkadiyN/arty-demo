r"""Tests for the Poisson kill-probability transform P_k = 1 − exp(−ρ_L·A_ref).

Coverage map
============

pkill_field_3d / pkill_volume_3d            (arty.fragmentation, single-zone)
four_zone_pkill_field / four_zone_pkill_volume (arty.zones, four-zone)

  • ρ_L=0 ⇒ P_k=0           — empty field maps to zero kill probability.
  • monotone in ρ_L         — denser lethal field never lowers P_k.
  • bounds P_k ∈ [0, 1]     — the saturating exponential stays in range.
  • z=0 slice consistency   — the volume's ground layer reproduces the field
                              P_k bit-for-bit (inherited from the ρ_L kernel
                              through the deterministic elementwise transform).

These are deliberately thin: P_k is a pure elementwise transform of ρ_L, so the
ρ_L kernel itself is *not* re-tested here (see test_lethal_density_volume.py).
The ρ_L=0 and monotonicity invariants are checked directly on the transform to
keep them independent of any particular field geometry, then the four wrapper
functions are spot-checked for bounds and z=0 consistency on small grids.
"""

import numpy as np
import pytest

from arty.fragmentation import (
    A_REF_DEFAULT,
    BurstParams,
    DragParams,
    E_LETH_DEFAULT,
    ShellParams,
    pkill_field_3d,
    pkill_volume_3d,
)
from arty.shells import SHELLS
from arty.zones import (
    compute_shell_zones,
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
        z=0.0, max_radius=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k >= 0.0) & (P_k <= 1.0))


def test_single_zone_pkill_volume_z0_matches_field(shell, drag, burst):
    """Volume's z=0 layer equals the single-z P_k field exactly."""
    _, _, _, P_k_vol = pkill_volume_3d(
        shell=shell, drag=drag, burst=burst,
        z_max=Z_MAX, max_radius=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, P_k_ref = pkill_field_3d(
        shell=shell, drag=drag, burst=burst,
        z=0.0, max_radius=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k_vol >= 0.0) & (P_k_vol <= 1.0))
    np.testing.assert_allclose(P_k_vol[0], P_k_ref, rtol=0.0, atol=0.0)


# ---------------------------------------------------------------------------
# Four-zone wrappers
# ---------------------------------------------------------------------------


def test_four_zone_pkill_field_bounds(zones_m1, drag):
    """four_zone_pkill_field returns P_k ∈ [0, 1] on a real field."""
    rho_steel = ShellParams().steel.rho
    _, _, P_k = four_zone_pkill_field(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z=0.0, max_r=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k >= 0.0) & (P_k <= 1.0))


def test_four_zone_pkill_volume_z0_matches_field(zones_m1, drag):
    """Four-zone volume's z=0 layer equals the four-zone P_k field exactly."""
    rho_steel = ShellParams().steel.rho
    _, _, _, P_k_vol = four_zone_pkill_volume(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z_max=Z_MAX, max_r=MAX_R, n_grid=N_GRID, n_z=N_Z,
        E_leth=E_LETH_DEFAULT,
    )
    _, _, P_k_ref = four_zone_pkill_field(
        zones_m1, aof_deg=30.0, h_b=2.0, drag=drag, rho_steel=rho_steel,
        z=0.0, max_r=MAX_R, n_grid=N_GRID, E_leth=E_LETH_DEFAULT,
    )
    assert np.all((P_k_vol >= 0.0) & (P_k_vol <= 1.0))
    np.testing.assert_allclose(P_k_vol[0], P_k_ref, rtol=0.0, atol=0.0)
