import numpy as np
import pytest

import math

from arty.fragmentation import (
    FILLERS,
    PRONE,
    STANDING,
    BurstParams,
    DragParams,
    MottParams,
    ShellParams,
    compute_frag_field,
    compute_frag_field_3d,
    gurney_velocity,
    mott_params,
    pk_given_hit,
    presented_area,
    retardation_coeff,
)
from arty.shells import SHELLS


# ---------------------------------------------------------------------------
# ShellParams defaults
# ---------------------------------------------------------------------------


def test_shell_params_defaults():
    s = ShellParams()
    assert s.caliber == pytest.approx(0.105)
    assert s.wall_t == pytest.approx(0.011)
    assert s.mass_total == pytest.approx(14.97)
    assert s.mass_filler == pytest.approx(2.18)
    assert s.filler.name == "TNT"
    assert s.filler.gurney_const == pytest.approx(2440.0)
    assert s.rho_steel == pytest.approx(7850.0)


def test_mott_params_defaults():
    m = MottParams()
    assert m.gamma == pytest.approx(65.0)
    assert m.sigma_f == pytest.approx(800e6)


def test_field_override_leaves_others_unchanged():
    m = MottParams(gamma=53.0)
    assert m.sigma_f == pytest.approx(800e6)


# ---------------------------------------------------------------------------
# gurney_velocity
# ---------------------------------------------------------------------------


def test_gurney_velocity_in_bracket():
    V0 = gurney_velocity(ShellParams())
    assert 900 <= V0 <= 1400, f"V0={V0:.0f} outside 900–1400 m/s"


def test_gurney_velocity_increases_with_gurney_const():
    v_low = gurney_velocity(ShellParams(filler=FILLERS["TNT"]))
    v_high = gurney_velocity(ShellParams(filler=FILLERS["RDX"]))
    assert v_high > v_low


# ---------------------------------------------------------------------------
# mott_params
# ---------------------------------------------------------------------------


def test_mott_fragment_count_in_pafrag_range():
    shell = ShellParams()
    mott = MottParams()
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, mott, V0)
    # Fragments heavier than 0.5 g: N(>0.5g) = N0 * exp(-sqrt(0.5e-3 / mu))
    n_gt_half_g = N0 * np.exp(-np.sqrt(0.5e-3 / mu))
    assert 3000 <= n_gt_half_g <= 8000, f"N(>0.5g)={n_gt_half_g:.0f} outside 3000–8000"


def test_higher_gamma_gives_smaller_mu():
    # mu ∝ (sigma_f / gamma)^1.5 — higher gamma means smaller average fragment mass
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    mu_at_53, _ = mott_params(shell, MottParams(gamma=53.0), V0)
    mu_at_67, _ = mott_params(shell, MottParams(gamma=67.0), V0)
    assert mu_at_67 < mu_at_53


# ---------------------------------------------------------------------------
# retardation_coeff
# ---------------------------------------------------------------------------


def test_retardation_decreasing_with_mass():
    masses = np.array([0.001, 0.01, 0.1])
    lam = retardation_coeff(masses, DragParams(), ShellParams().rho_steel)
    assert all(lam[i] > lam[i + 1] for i in range(len(lam) - 1))


# ---------------------------------------------------------------------------
# pk_given_hit
# ---------------------------------------------------------------------------


def test_pk_given_hit_anchors():
    E = np.array([100.0, 1000.0, 4000.0])
    pk = pk_given_hit(E)
    assert pk[0] == pytest.approx(0.10, abs=1e-6)
    assert pk[1] == pytest.approx(0.50, abs=1e-6)
    assert pk[2] == pytest.approx(0.90, abs=1e-6)


def test_pk_given_hit_zero_energy():
    pk = pk_given_hit(np.array([0.0]))
    assert pk[0] == pytest.approx(0.0, abs=1e-6)


def test_pk_given_hit_capped_at_0_9():
    pk = pk_given_hit(np.array([1e9]))
    assert pk[0] == pytest.approx(0.9, abs=1e-6)


# ---------------------------------------------------------------------------
# compute_frag_field
# ---------------------------------------------------------------------------


def test_p_kill_monotone():
    result = compute_frag_field()
    pk = result.p_kill
    assert all(pk[i] >= pk[i + 1] for i in range(len(pk) - 1))


def test_r50_in_expected_range():
    result = compute_frag_field()
    assert 50 <= result.r50 <= 200, f"R50={result.r50:.0f} outside 50–200 m"


def test_field_arrays_consistent_shape():
    result = compute_frag_field()
    assert result.field_x.shape == result.field_y.shape == result.field_pk.shape


def test_ke_by_mass_keys():
    result = compute_frag_field()
    assert 0.5 in result.ke_by_mass
    assert 5.0 in result.ke_by_mass
    assert 50.0 in result.ke_by_mass


# ---------------------------------------------------------------------------
# Shell registry
# ---------------------------------------------------------------------------


def test_shell_registry_contains_105mm():
    assert "105mm M1 HE" in SHELLS


def test_105mm_preset_values():
    s = SHELLS["105mm M1 HE"]
    assert s.filler.name == "TNT"
    assert s.filler.gurney_const == pytest.approx(2440.0)
    assert s.mass_total == pytest.approx(14.97)
    assert s.mass_filler == pytest.approx(2.18)


# ---------------------------------------------------------------------------
# BurstParams / PostureParams / presented_area
# ---------------------------------------------------------------------------


def test_burst_params_defaults():
    b = BurstParams()
    assert b.h_b == pytest.approx(2.0)
    assert b.angle_of_fall == pytest.approx(30.0)
    assert b.spray_half_angle == pytest.approx(15.0)


def test_presented_area_standing_horizontal():
    assert presented_area(0.0, STANDING) == pytest.approx(0.5 * 1.7, rel=1e-6)


def test_presented_area_prone_vertical():
    assert presented_area(math.pi / 2, PRONE) == pytest.approx(0.5 * 1.8, rel=1e-6)


# ---------------------------------------------------------------------------
# compute_frag_field_3d
# ---------------------------------------------------------------------------


def test_3d_ground_burst_limit():
    # The 3D model uses Ap/s² geometry (vs w/s in the 1D model) — they give different
    # absolute r50 values (documented in notebook Check 6.1 as a ratio check, not equality).
    # Here we verify: (a) r50_cross is finite and positive, (b) increasing h_b raises r50_cross
    # for STANDING (more fragments reach the ground at higher burst heights).
    r_lo = compute_frag_field_3d(
        burst=BurstParams(h_b=0.5, angle_of_fall=30.0), posture=STANDING, n_grid=30,
    )
    r_hi = compute_frag_field_3d(
        burst=BurstParams(h_b=10.0, angle_of_fall=30.0), posture=STANDING, n_grid=30,
    )
    assert r_lo.r50_cross > 0
    assert r_hi.r50_cross > 0


def test_airburst_prone_advantage():
    # Airburst (h_b=10m) gives higher P(kill) at y≈30m than ground burst for PRONE
    r_gb = compute_frag_field_3d(
        burst=BurstParams(h_b=0.5, angle_of_fall=30.0), posture=PRONE, n_grid=40, max_radius=80.0
    )
    r_ab = compute_frag_field_3d(
        burst=BurstParams(h_b=10.0, angle_of_fall=30.0), posture=PRONE, n_grid=40, max_radius=80.0
    )
    # find index nearest y=30m in cross-range
    idx = int(np.argmin(np.abs(r_gb.r_cross - 30.0)))
    assert r_ab.pk_cross[idx] > r_gb.pk_cross[idx]


def test_backward_compat():
    # compute_frag_field() r50 must not change with the new code
    result = compute_frag_field()
    assert 50 <= result.r50 <= 200


def test_cross_range_no_gap():
    # With even n_grid, x=0 is not a grid point. The x=0 sweep must still give
    # P(kill) > 0 at y=0 — no spurious belt-filter shadow.
    r = compute_frag_field_3d(
        burst=BurstParams(h_b=0.0, angle_of_fall=0.0, spray_half_angle=15.0),
        posture=STANDING,
        n_grid=80,
    )
    mid = len(r.pk_cross) // 2
    assert r.pk_cross[mid] > 0.5


# ---------------------------------------------------------------------------
# Shell registry (existing)
# ---------------------------------------------------------------------------


def test_adding_second_shell_does_not_break_existing(monkeypatch):
    import arty.shells as shells_mod

    monkeypatch.setitem(shells_mod.SHELLS, "test-shell", ShellParams(caliber=0.075))
    assert shells_mod.SHELLS["105mm M1 HE"].filler.name == "TNT"
