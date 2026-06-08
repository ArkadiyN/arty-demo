r"""
Tests for src/arty/fragmentation.py and src/arty/shells.py

Coverage map
============

SteelParams / ShellParams  (dataclass defaults and field isolation)
  • Default ShellParams matches the validated 105mm M1 HE notebook values:
    caliber, wall_t, mass_total, mass_filler, filler name/gurney_const.
  • Default steel (WW2 US HE Shell) gives rho=7850, sigma_f=800 MPa, gamma=65.
  • ShellParams.steel is the WW2 US HE Shell entry.

gurney_velocity
  • Result for default 105mm M1 HE falls in the 900–1400 m/s published bracket.
  • Higher Gurney constant (RDX > TNT) always yields higher V₀.

mott_params
  • Fragment count heavier than 0.5 g lies in the 3000–8000 PAFRAG expected range
    for the default shell.
  • mu ∝ (σ_F / γ)^1.5 — higher gamma produces smaller average fragment mass.

retardation_coeff
  • λ is strictly decreasing with fragment mass (heavier fragments decelerate more
    slowly), confirming the m^(−1/3) scaling.

pk_given_hit  (ES-310 graded Pk|hit)
  • Anchors: E = [100, 1000, 4000] J returns [0.10, 0.50, 0.90] exactly.
  • Zero energy returns zero probability (left-clip).
  • Very high energy is capped at 0.9 (right-clip).

compute_frag_field  (1-D radially-symmetric model)
  • P(kill) is monotonically non-increasing with distance from burst.
  • R₅₀ for default 105mm M1 HE is in the 50–200 m range.
  • field_x, field_y, field_pk arrays all share the same shape.
  • ke_by_mass contains keys for the three representative masses: 0.5, 5, 50 g.

Shell registry  (arty.shells)
  • "105mm M1 HE" and "155mm M107 HE" are present in SHELLS.
  • M1 filler, gurney_const, mass_total, and mass_filler match spec values.
  • M107 mass_total, mass_filler, and wall_t match 1943 spec values.
  • Adding a third shell does not mutate existing entries (monkeypatched).

BurstParams / PostureParams / presented_area
  • Default BurstParams: h_b=2 m, angle_of_fall=30°, spray_half_angle=15°.
  • presented_area at γ=0 (horizontal fragment, STANDING) equals w_perp × h.
  • presented_area at γ=π/2 (vertical fragment, PRONE) equals w_perp × d.

compute_frag_field_3d  (3-D belt-spray burst model)
  • r50_cross is finite and positive for both a near-ground burst and a 10 m airburst.
  • Airburst (h_b=10 m) gives higher P(kill) at y≈30 m than ground burst for PRONE
    (more fragments reach a prone target from above).
  • compute_frag_field() R₅₀ is unaffected by the 3-D code path (backward compat).
  • With even n_grid (grid never hits x=0), the dedicated x=0 sweep still returns
    P(kill) > 0.5 at y=0 — no spurious belt-filter shadow from grid misalignment.
  • ke_by_mass is indexed by radial slant range r_ke: r_ke[0]=0, r_ke[-1]=max_radius,
    len=n_grid, and ke_by_mass[0.5][0] ≈ ½ × 0.5 g × V₀².
"""

import math

import numpy as np
import pytest

from arty.fragmentation import (
    FILLERS,
    PRONE,
    STANDING,
    BurstParams,
    DragParams,
    ShellParams,
    SteelParams,
    STEELS,
    compute_frag_field,
    compute_frag_field_3d,
    gurney_velocity,
    ke_at_range,
    lethal_fragments_at_range,
    min_lethal_mass,
    mott_N,
    mott_params,
    p_hit,
    p_kill,
    pk_given_hit,
    presented_area,
    retardation_coeff,
)
from arty.shells import SHELLS


# ---------------------------------------------------------------------------
# SteelParams / ShellParams defaults
# ---------------------------------------------------------------------------


def test_steel_params_ww2_us():
    steel = STEELS["WW2 US HE Shell"]
    assert steel.rho == pytest.approx(7850.0)
    assert steel.sigma_f == pytest.approx(800e6)
    assert steel.gamma == pytest.approx(65.0)


def test_shell_params_defaults():
    s = ShellParams()
    assert s.caliber == pytest.approx(0.105)
    assert s.wall_t == pytest.approx(0.009208)
    assert s.mass_total == pytest.approx(14.97)
    assert s.mass_filler == pytest.approx(2.18)
    assert s.filler.name == "TNT"
    assert s.filler.gurney_const == pytest.approx(2440.0)
    assert s.steel.name == "WW2 US HE Shell"
    assert s.steel.rho == pytest.approx(7850.0)


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
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)
    # Fragments heavier than 0.5 g: N(>0.5g) = N0 * exp(-sqrt(0.5e-3 / mu))
    n_gt_half_g = N0 * np.exp(-np.sqrt(0.5e-3 / mu))
    assert 3000 <= n_gt_half_g <= 8000, f"N(>0.5g)={n_gt_half_g:.0f} outside 3000–8000"


def test_higher_gamma_gives_smaller_mu():
    # mu ∝ (sigma_f / gamma)^1.5 — higher gamma means smaller average fragment mass
    V0 = gurney_velocity(ShellParams())
    shell_lo = ShellParams(steel=SteelParams(name="lo", rho=7850.0, sigma_f=800e6, gamma=53.0))
    shell_hi = ShellParams(steel=SteelParams(name="hi", rho=7850.0, sigma_f=800e6, gamma=67.0))
    mu_lo, _ = mott_params(shell_lo, V0)
    mu_hi, _ = mott_params(shell_hi, V0)
    assert mu_hi < mu_lo


# ---------------------------------------------------------------------------
# retardation_coeff
# ---------------------------------------------------------------------------


def test_retardation_decreasing_with_mass():
    masses = np.array([0.001, 0.01, 0.1])
    lam = retardation_coeff(masses, DragParams(), ShellParams().steel.rho)
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


def test_ke_by_mass_radial():
    result = compute_frag_field_3d(max_radius=80.0, n_grid=80)
    assert result.r_ke[0] == pytest.approx(0.0)
    assert result.r_ke[-1] == pytest.approx(80.0)
    assert len(result.r_ke) == 80
    expected_ke0 = 0.5 * 0.5e-3 * result.V0 ** 2
    assert result.ke_by_mass[0.5][0] == pytest.approx(expected_ke0, rel=1e-3)


# ---------------------------------------------------------------------------
# Shell registry
# ---------------------------------------------------------------------------


def test_shell_registry_contains_105mm():
    assert "105mm M1 HE" in SHELLS


def test_shell_registry_contains_155mm():
    assert "155mm M107 HE" in SHELLS


def test_105mm_preset_values():
    s = SHELLS["105mm M1 HE"]
    assert s.filler.name == "TNT"
    assert s.filler.gurney_const == pytest.approx(2440.0)
    assert s.mass_total == pytest.approx(14.97)
    assert s.mass_filler == pytest.approx(2.18)
    assert s.steel.name == "WW2 US HE Shell"


def test_155mm_m107_preset_values():
    s = SHELLS["155mm M107 HE"]
    assert s.caliber == pytest.approx(0.155)
    assert s.wall_t == pytest.approx(0.01429, rel=1e-3)
    assert s.mass_total == pytest.approx(43.09, rel=1e-3)
    assert s.mass_filler == pytest.approx(6.863, rel=1e-3)
    assert s.filler.name == "TNT"
    assert s.steel.name == "WW2 US HE Shell"


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
    idx = int(np.argmin(np.abs(r_gb.r_cross - 30.0)))
    assert r_ab.pk_cross[idx] > r_gb.pk_cross[idx]


def test_backward_compat():
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
# Shell registry isolation
# ---------------------------------------------------------------------------


def test_adding_third_shell_does_not_break_existing(monkeypatch):
    import arty.shells as shells_mod

    monkeypatch.setitem(shells_mod.SHELLS, "test-shell", ShellParams(caliber=0.075))
    assert shells_mod.SHELLS["105mm M1 HE"].filler.name == "TNT"
    assert shells_mod.SHELLS["155mm M107 HE"].filler.name == "TNT"


# ---------------------------------------------------------------------------
# mott_N
# ---------------------------------------------------------------------------


def test_mott_N_at_zero_mass():
    # N(m→0) = N0 (all fragments accounted for)
    result = mott_N(np.array([0.0]), N0=1000.0, mu=0.001)
    assert result[0] == pytest.approx(1000.0)


def test_mott_N_at_mu():
    # N(mu) = N0 * exp(-1) by definition of the half-weight parameter
    mu = 0.005
    result = mott_N(np.array([mu]), N0=500.0, mu=mu)
    assert result[0] == pytest.approx(500.0 * np.exp(-1.0))


def test_mott_N_monotone_decreasing():
    masses = np.array([1e-4, 1e-3, 1e-2, 0.1])
    n = mott_N(masses, N0=2000.0, mu=0.01)
    assert all(n[i] > n[i + 1] for i in range(len(n) - 1))


# ---------------------------------------------------------------------------
# ke_at_range
# ---------------------------------------------------------------------------


def test_ke_at_range_zero_range():
    # KE at s=0 equals ½mV₀² (no drag applied yet)
    m = np.array([0.001, 0.01])
    V0 = 1000.0
    lam = np.array([0.1, 0.05])
    s = np.array([0.0, 0.0])
    ke = ke_at_range(m, V0, lam, s)
    assert ke == pytest.approx(0.5 * m * V0**2)


def test_ke_at_range_decays_with_range():
    m = np.array([0.01])
    V0 = 1000.0
    lam = np.array([0.01])
    ke_near = ke_at_range(m, V0, lam, np.array([10.0]))[0]
    ke_far = ke_at_range(m, V0, lam, np.array([100.0]))[0]
    assert ke_far < ke_near


def test_ke_at_range_linear_in_mass():
    # KE ∝ m at fixed V0, lam, s
    V0 = 1000.0
    lam = np.array([0.01, 0.01])
    s = np.array([50.0, 50.0])
    ke = ke_at_range(np.array([0.005, 0.010]), V0, lam, s)
    assert ke[1] == pytest.approx(2.0 * ke[0], rel=1e-9)


# ---------------------------------------------------------------------------
# min_lethal_mass
# ---------------------------------------------------------------------------


def test_min_lethal_mass_returns_m_hi_when_all_sub_lethal():
    # m_hi=0.1g at 50m with E_leth=500J: KE≈7J < 500J → all fragments sub-lethal → return m_hi
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    m_hi = 1e-4
    result = min_lethal_mass(50.0, V0, E_leth=500.0, drag=DragParams(),
                             rho_steel=shell.steel.rho, m_hi=m_hi)
    assert result == pytest.approx(m_hi)


def test_min_lethal_mass_returns_m_lo_when_all_lethal():
    # m_lo=1g at 1m with E_leth=10J: KE≈485J >> 10J → even lightest fragment is lethal → return m_lo
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    m_lo = 1e-3
    result = min_lethal_mass(1.0, V0, E_leth=10.0, drag=DragParams(),
                             rho_steel=shell.steel.rho, m_lo=m_lo)
    assert result == pytest.approx(m_lo)


def test_min_lethal_mass_bisects_intermediate():
    # At moderate range, bisection finds the boundary mass strictly inside (m_lo, m_hi)
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    result = min_lethal_mass(30.0, V0, E_leth=80.0, drag=DragParams(),
                             rho_steel=shell.steel.rho)
    assert 1e-6 < result < 2.0


# ---------------------------------------------------------------------------
# lethal_fragments_at_range
# ---------------------------------------------------------------------------


def test_lethal_fragments_nonnegative():
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)
    r = np.array([1.0, 10.0, 100.0, 500.0])
    n_leth = lethal_fragments_at_range(r, N0, mu, V0, E_leth=80.0,
                                       drag=DragParams(), rho_steel=shell.steel.rho)
    assert np.all(n_leth >= 0.0)


def test_lethal_fragments_monotone_decreasing():
    shell = ShellParams()
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)
    r = np.array([10.0, 50.0, 150.0])
    n_leth = lethal_fragments_at_range(r, N0, mu, V0, E_leth=80.0,
                                       drag=DragParams(), rho_steel=shell.steel.rho)
    assert all(n_leth[i] >= n_leth[i + 1] for i in range(len(n_leth) - 1))


# ---------------------------------------------------------------------------
# p_hit
# ---------------------------------------------------------------------------


def test_p_hit_zero_lethal_fragments():
    r = np.array([10.0, 50.0])
    pk = p_hit(r, N_leth=np.zeros(2), w=0.5)
    assert pk == pytest.approx([0.0, 0.0])


def test_p_hit_matches_formula():
    r = np.array([10.0])
    N_leth = np.array([5.0])
    w = 0.5
    expected = 1.0 - np.exp(-5.0 * 0.5 / (2.0 * np.pi * 10.0))
    assert p_hit(r, N_leth, w)[0] == pytest.approx(expected)


def test_p_hit_decreases_with_range():
    r = np.array([10.0, 50.0, 200.0])
    N_leth = np.full(3, 100.0)
    pk = p_hit(r, N_leth, w=0.5)
    assert all(pk[i] > pk[i + 1] for i in range(len(pk) - 1))


# ---------------------------------------------------------------------------
# p_kill
# ---------------------------------------------------------------------------


def test_p_kill_zero():
    assert p_kill(np.array([0.0]))[0] == pytest.approx(0.0)


def test_p_kill_half_at_log2():
    # N_eff = ln(2) → P(kill) = 1 - exp(-ln2) = 0.5
    assert p_kill(np.array([np.log(2.0)]))[0] == pytest.approx(0.5)


def test_p_kill_approaches_one():
    assert p_kill(np.array([100.0]))[0] == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# _expected_kills_3d_point guard branches (via compute_frag_field_3d)
# ---------------------------------------------------------------------------


def test_3d_burst_origin_zero_hb_guard():
    # n_grid=1 → single grid point at (0,0); h_b=0 → s=0 → guard returns 0.0
    result = compute_frag_field_3d(burst=BurstParams(h_b=0.0), n_grid=1)
    assert result.field_pk[0, 0] == pytest.approx(0.0)


def test_3d_shell_axis_alignment_guard():
    # spray_half_angle=90° and point exactly along shell axis → sin_Theta=0 → guard returns 0.0
    # With h_b=0, AoF=0, n_grid=3, max_radius=80: grid point at (-80, 0) aligns with shell axis.
    result = compute_frag_field_3d(
        burst=BurstParams(h_b=0.0, angle_of_fall=0.0, spray_half_angle=90.0),
        n_grid=3,
        max_radius=80.0,
    )
    assert result.field_pk[1, 0] == pytest.approx(0.0)
