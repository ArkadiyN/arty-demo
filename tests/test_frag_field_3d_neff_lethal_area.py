"""FragField3dResult.n_eff_cross and .lethal_area (target-area-profile item 7, §6.6.1)."""
import numpy as np

from arty.fragmentation import (
    PRONE,
    STANDING,
    BurstParams,
    compute_frag_field_3d,
)


def _run(posture=STANDING, h_b=2.0):
    return compute_frag_field_3d(
        burst=BurstParams(h_b=h_b), posture=posture, max_radius=40.0, n_grid=41, n_mass=120
    )


def test_n_eff_cross_is_inverse_of_pk_cross():
    r = _run()
    assert r.n_eff_cross is not None
    assert r.n_eff_cross.shape == r.pk_cross.shape
    assert np.all(r.n_eff_cross >= 0.0)
    np.testing.assert_allclose(1.0 - np.exp(-r.n_eff_cross), r.pk_cross, rtol=0, atol=1e-12)


def test_lethal_area_is_pk_sum_times_cell_area():
    r = _run()
    dx = 80.0 / 40  # linspace(-40, 40, 41)
    assert abs(r.lethal_area - r.field_pk.sum() * dx * dx) < 1e-9
    assert 0.0 < r.lethal_area <= (80.0 + dx) ** 2


def test_lethal_area_prone_below_standing_near_ground_burst():
    """Near-ground burst: fragments arrive near-horizontal, prone presents less area."""
    assert _run(PRONE, h_b=0.5).lethal_area < _run(STANDING, h_b=0.5).lethal_area
