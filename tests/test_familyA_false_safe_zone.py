r"""Regression tests for the Family-A false-safe-zone fix (graded ground P(kill)).

The graded Family-A ground fields (single-zone ``_expected_kills_3d_vec`` /
``compute_frag_field_3d`` and four-zone ``_four_zone_familyA_eval`` /
``four_zone_field``) evaluate the ``A_p(γ)·pk_given_hit(E)`` belt kernel on the
target's vertical column, at the lowest height the belt lights (``z_rep``), rather
than on the false-safe ground plane ``z = 0``.

Coverage (derivation.md §7 A5 / §8 required checks):
  1. Dense standing-ring sweep — EVERY r across the previously-false ring reads
     P_k > 0 (not just max()), the check that would have caught the belt-edge
     coin-flip found in review cycle 1.
  2. Feet-lit bit-exact reduction — where the belt already reaches z = 0 the
     relocated kernel reproduces the shipped z = 0 kernel to the bit.
  3. Prone-below-standing / h-monotonicity at the defect config.
  4. Off-axis single-zone axis-sign pin (AoF≠90°, x≠0) — the backward-axis (-x)
     handling, invisible at AoF=90° where B=0.

Config throughout: AoF=90° (horizontal equatorial belt), h_b=2.0 m, δ=15°, the
derivation's headline defect scenario.
"""

import numpy as np
import pytest

from arty.fragmentation import (
    PRONE,
    STANDING,
    BurstParams,
    DragParams,
    PostureParams,
    ShellParams,
    _expected_kills_3d_vec,
    _shell_axis,
    compute_frag_field_3d,
    gurney_velocity,
    mott_params,
    pk_given_hit,
    presented_area,
    retardation_coeff,
)
from arty.zones import (
    _familyA_zone_massintegral,
    _four_zone_familyA_eval,
    compute_shell_zones,
    four_zone_field,
)


@pytest.fixture(scope="module")
def shell():
    return ShellParams()


@pytest.fixture(scope="module")
def drag():
    return DragParams()


# Onset/edge radii at the defect config (derivation §5.1):
#   belt reaches height z at r = (h_b − z)/tanδ
#   standing onset r=(2−1.7)/tan15° ≈ 1.12 m; feet-lit r=2/tan15° ≈ 7.46 m
H_B = 2.0
TAN_D = np.tan(np.radians(15.0))
R_ONSET_STAND = (H_B - STANDING.h) / TAN_D   # ≈ 1.12 m
R_FEET = H_B / TAN_D                          # ≈ 7.46 m


def _single_zone_inputs(shell, drag, n_mass=300):
    """Reproduce compute_frag_field_3d's internal single-zone kernel inputs."""
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)
    m_grid = np.logspace(-6, np.log10(0.5), n_mass)
    pdf = N0 / (2.0 * np.sqrt(mu * m_grid)) * np.exp(-np.sqrt(m_grid / mu))
    lam = retardation_coeff(m_grid, drag, shell.steel.rho)
    return V0, mu, N0, m_grid, pdf, lam


def _ref_z0_single(x, y, h_b, alpha_rad, delta_rad, V0, posture, m_grid, pdf, lam):
    """Independent single-zone kernel sampled on the ground plane z = 0.

    The pre-fix ('shipped') transform, replicating the *vectorised* ground field's
    exact expression (``_expected_kills_3d_vec``: cosΘ = (x·e₀ + (−h_b)·e₂)/s, a
    multiply-then-divide, not the point kernel's r_vec/s-then-dot) so the relocated
    field reproduces it **to the bit** wherever the belt reaches the feet
    (derivation §4). compute_frag_field_3d's ground field is the vec path.
    """
    s = np.sqrt(x * x + y * y + h_b * h_b)
    if s < 1e-6:
        return 0.0
    e_axis = _shell_axis(alpha_rad)
    s_safe = s if s >= 1e-6 else 1.0
    cos_Theta = float((x * e_axis[0] + (-h_b) * e_axis[2]) / s_safe)
    if abs(cos_Theta) > np.sin(delta_rad):
        return 0.0
    sin_Theta = np.sqrt(max(0.0, 1.0 - cos_Theta**2))
    if sin_Theta < 1e-9:
        return 0.0
    gamma = np.arcsin(np.clip(h_b / s, -1.0, 1.0))
    Ap = presented_area(gamma, posture)
    E = 0.5 * m_grid * (V0 * np.exp(-lam * s)) ** 2
    integ = pdf * pk_given_hit(E) * Ap / (2.0 * np.pi * s**2 * 2.0 * sin_Theta * delta_rad)
    return float(np.trapezoid(integ, m_grid))


# ---------------------------------------------------------------------------
# 1. Dense standing-ring sweep — P_k > 0 at EVERY r, not just max()
# ---------------------------------------------------------------------------


def test_single_zone_dense_ring_all_nonzero(shell, drag):
    """Every ground cell across the previously-false ring reads P_k > 0.

    The naive z_rep=z_lo recipe (review cycle 1) zeroed a rounding-dependent
    subset of the ring by evaluating the kernel exactly at the belt-edge root
    (coin-flip). A single max()-over-ring assertion would still pass on one lucky
    cell; this asserts the *minimum* over a fine grid, which the coin-flip fails.
    """
    V0, mu, N0, m_grid, pdf, lam = _single_zone_inputs(shell, drag)
    alpha = np.radians(90.0)
    delta = np.radians(15.0)
    # fine radial grid strictly inside the reachable ring (onset .. feet-lit)
    r = np.arange(R_ONSET_STAND + 0.01, R_FEET - 0.01, 0.02)
    N = _expected_kills_3d_vec(
        r, np.zeros_like(r), H_B, alpha, delta,
        N0, mu, V0, drag, shell.steel.rho, STANDING, m_grid, pdf, lam,
    )
    assert np.all(N > 0.0), (
        f"{int((N == 0).sum())}/{len(r)} ring cells read N=0 (false-safe/coin-flip)"
    )
    # inner dead zone r < onset genuinely stays 0 (belt overhead, §5.2)
    r_inner = np.array([0.3, 0.7, R_ONSET_STAND - 0.05])
    N_inner = _expected_kills_3d_vec(
        r_inner, np.zeros_like(r_inner), H_B, alpha, delta,
        N0, mu, V0, drag, shell.steel.rho, STANDING, m_grid, pdf, lam,
    )
    assert np.all(N_inner == 0.0)


def test_four_zone_dense_ring_all_nonzero(shell, drag):
    """Four-zone graded field fills the whole standing ring (P_k > 0 at every r)."""
    zones = compute_shell_zones(shell)
    m_grid = np.logspace(-6, np.log10(0.5), 200)
    drag_lam = retardation_coeff(m_grid, drag, shell.steel.rho)
    n_grid = 401
    max_r = 10.0
    X, Y, Pk = four_zone_field(
        zones, aof_deg=90.0, h_b=H_B, posture=STANDING,
        drag_lam_grid=drag_lam, m_grid=m_grid,
        max_r=max_r, n_grid=n_grid, delta_deg=15.0,
    )
    # central column x=0 (odd grid → exact centre); r = |y|
    col = Pk[:, n_grid // 2]
    r = np.abs(np.linspace(-max_r, max_r, n_grid))
    ring = (r > R_ONSET_STAND + 0.05) & (r < R_FEET - 0.05)
    assert np.all(col[ring] > 0.0), (
        f"{int((col[ring] == 0).sum())}/{int(ring.sum())} four-zone ring cells P_k=0"
    )


# ---------------------------------------------------------------------------
# 2. Feet-lit bit-exact reduction to the shipped z = 0 kernel
# ---------------------------------------------------------------------------


def test_feet_lit_reduction(shell, drag):
    """Where the belt reaches z=0, the relocated kernel reproduces the shipped one.

    z_rep collapses to 0 on feet-lit cells, so the relocation is algebraically
    identical to the pre-fix z=0 transform there — reproduced to floating-point
    round-off (the expression order differs, so agreement is to ~1e-15, not the
    literal bit; this is the codebase's usual vec-equivalence tolerance). The fix
    is thus strictly additive on the false ring (derivation §4).
    """
    V0, mu, N0, m_grid, pdf, lam = _single_zone_inputs(shell, drag)
    alpha = np.radians(90.0)
    delta = np.radians(15.0)
    # feet-lit cells: r > feet-lit radius ≈ 7.46 m (also off-axis y≠0)
    xs = np.array([8.0, 10.0, 12.0, 15.0, 20.0, 9.0, 11.0])
    ys = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 2.0, -3.0])
    N_new = _expected_kills_3d_vec(
        xs, ys, H_B, alpha, delta,
        N0, mu, V0, drag, shell.steel.rho, STANDING, m_grid, pdf, lam,
    )
    N_old = np.array([
        _ref_z0_single(x, y, H_B, alpha, delta, V0, STANDING, m_grid, pdf, lam)
        for x, y in zip(xs, ys)
    ])
    assert np.all(N_old > 0.0), "reference feet-lit cells must be nonzero"
    assert np.allclose(N_new, N_old, rtol=1e-12, atol=1e-13), (
        f"reduction off by more than round-off: max|Δ|={np.max(np.abs(N_new-N_old)):.3e}"
    )
    # the inner dead zone and the previously-false ring are the ONLY changes:
    # cells the old transform already fired reproduce it to round-off.
    assert np.max(np.abs(N_new - N_old)) < 1e-12


def _ref_z0_fourzone(xg, yg, zones, aof_deg, h_b, posture, drag_lam, m_grid, delta_deg):
    """Independent OLD four-zone kernel sampled on the ground plane z = 0.

    Replicates the pre-relocation ``_four_zone_familyA_eval`` body (shared geom at
    z=0, per-zone belt gate) directly from ``presented_area`` /
    ``_familyA_zone_massintegral`` — no relocated code — so the relocated field
    must reproduce it wherever every contributing zone's belt already reaches the
    feet (derivation §4/§5.4). Returns the total expected-count array [-].
    """
    xg = np.asarray(xg, dtype=float)
    yg = np.asarray(yg, dtype=float)
    field_N = np.zeros_like(xg)
    aof = np.radians(aof_deg)
    cA, sA = np.cos(aof), np.sin(aof)
    delta = np.radians(delta_deg)
    sin_delta = np.sin(delta)
    s = np.sqrt(xg**2 + yg**2 + h_b**2)
    valid = s >= 1e-3
    s_safe = np.where(valid, s, 1.0)
    cos_Theta = (xg * cA + h_b * sA) / s_safe
    gamma = np.arcsin(np.clip(h_b / s_safe, -1.0, 1.0))
    geom = presented_area(gamma, posture) / (2.0 * np.pi * s_safe**2 * 2.0 * delta)
    for z in (zones.ogive, zones.cylinder, zones.boattail, zones.base):
        if z.mass_kg <= 1e-6 or z.V0_ms <= 0.0 or not np.isfinite(z.mu):
            continue
        theta_z = np.radians(z.spray_deg)
        if np.sin(aof + theta_z) <= 0.0:
            continue
        mask = valid & (np.abs(cos_Theta - np.cos(theta_z)) <= sin_delta)
        idx = np.nonzero(mask)[0]
        if idx.size == 0:
            continue
        J = _familyA_zone_massintegral(z, drag_lam, m_grid, s[idx])
        val = np.zeros_like(xg)
        val[idx] = J * geom[idx] / np.sin(theta_z)
        field_N += val
    return field_N


def test_four_zone_feet_lit_reduction(shell, drag):
    """Four-zone relocated field reproduces the shipped z=0 kernel where feet-lit.

    Locks the reduction identity for _four_zone_familyA_eval too (not just the
    single-zone path) — closing the four-zone/single-zone test-parity gap. Points
    are chosen at large r (incl. off-axis y≠0) where every AoF=90° contributing
    zone (ogive, cylinder) already lights z=0, so z_rep=0 for all and the
    relocation is algebraically identical to the old transform (to round-off).
    """
    zones = compute_shell_zones(shell)
    m_grid = np.logspace(-6, np.log10(0.5), 200)
    drag_lam = retardation_coeff(m_grid, drag, shell.steel.rho)
    xs = np.array([15.0, 20.0, 25.0, 18.0, 22.0])
    ys = np.array([0.0, 0.0, 0.0, 6.0, -8.0])
    N_new, _ = _four_zone_familyA_eval(
        zones, 90.0, H_B, STANDING, drag_lam, m_grid, 15.0, xs, ys,
    )
    N_old = _ref_z0_fourzone(xs, ys, zones, 90.0, H_B, STANDING, drag_lam, m_grid, 15.0)
    assert np.all(N_old > 0.0), "reference feet-lit four-zone cells must be nonzero"
    assert np.allclose(N_new, N_old, rtol=1e-12, atol=1e-13), (
        f"four-zone reduction off by more than round-off: "
        f"max|Δ|={np.max(np.abs(N_new - N_old)):.3e}"
    )


# ---------------------------------------------------------------------------
# 3. Prone-below-standing / h-monotonicity
# ---------------------------------------------------------------------------


def test_standing_not_less_than_prone_everywhere(shell, drag):
    """A standing target is never scored less lethal than a prone one (per cell)."""
    burst = BurstParams(angle_of_fall=90.0, spray_half_angle=15.0, h_b=H_B)
    stand = compute_frag_field_3d(shell, drag, burst, posture=STANDING,
                                  max_radius=10.0, n_grid=121)
    prone = compute_frag_field_3d(shell, drag, burst, posture=PRONE,
                                  max_radius=10.0, n_grid=121)
    assert np.all(stand.field_pk >= prone.field_pk - 1e-12)
    # in the mid ring (onset_stand < r < onset_prone) standing fires, prone dark
    r = np.abs(np.linspace(-10.0, 10.0, 121))
    onset_prone = (H_B - PRONE.h) / TAN_D    # ≈ 6.34 m
    mid = (r > R_ONSET_STAND + 0.3) & (r < onset_prone - 0.3)
    col_s = stand.field_pk[:, 121 // 2]
    col_p = prone.field_pk[:, 121 // 2]
    assert np.all(col_s[mid] > 0.0)
    assert np.all(col_p[mid] == 0.0)


def test_h_monotonic(shell, drag):
    """N is non-decreasing in target height h (extending the column only adds flux)."""
    V0, mu, N0, m_grid, pdf, lam = _single_zone_inputs(shell, drag)
    alpha = np.radians(90.0)
    delta = np.radians(15.0)
    r = np.array([2.0, 3.0, 5.0, 7.0])
    prev = np.zeros_like(r)
    for h in [0.3, 0.6, 1.0, 1.7, 2.5]:
        post = PostureParams(w_perp=0.5, h=h, d=0.3)
        N = _expected_kills_3d_vec(
            r, np.zeros_like(r), H_B, alpha, delta,
            N0, mu, V0, drag, shell.steel.rho, post, m_grid, pdf, lam,
        )
        assert np.all(N >= prev - 1e-12), f"N decreased when h grew to {h}"
        prev = N


# ---------------------------------------------------------------------------
# 4. Off-axis single-zone axis-sign pin (AoF≠90°, x≠0)
# ---------------------------------------------------------------------------


def _ref_relocated_single_offaxis(x, y, h_b, alpha_rad, delta_rad, V0, posture,
                                   m_grid, pdf, lam, nz=20001):
    """Independent relocated single-zone kernel — no belt_column_breakpoints.

    Brute-force scan the column [0, h] for the lowest height whose backward-axis
    belt gate holds, then evaluate the kernel there. A wrong-sign (+x) breakpoint
    implementation would relocate z_rep elsewhere and disagree materially
    (derivation §5.5 / §7 A3). Backward axis: cosΘ = −(x cosα + (z−h_b) sinα)/s.
    """
    zs = np.linspace(0.0, posture.h, nz)
    dz = zs - h_b
    s = np.sqrt(x * x + y * y + dz * dz)
    cosT = -(x * np.cos(alpha_rad) + dz * np.sin(alpha_rad)) / s
    active = np.abs(cosT) <= np.sin(delta_rad)
    if not np.any(active):
        return 0.0
    j = int(np.argmax(active))          # lowest active grid height
    z_rep = zs[j]
    sj = s[j]
    if sj < 1e-6:
        return 0.0
    sinT = np.sqrt(max(0.0, 1.0 - cosT[j] ** 2))
    if sinT < 1e-9:
        return 0.0
    gamma = np.arcsin(np.clip((h_b - z_rep) / sj, -1.0, 1.0))
    Ap = presented_area(gamma, posture)
    E = 0.5 * m_grid * (V0 * np.exp(-lam * sj)) ** 2
    integ = pdf * pk_given_hit(E) * Ap / (2.0 * np.pi * sj**2 * 2.0 * sinT * delta_rad)
    return float(np.trapezoid(integ, m_grid))


def test_offaxis_single_zone_axis_sign(shell, drag):
    """Off-axis (AoF=60°, x<0) single-zone matches a backward-axis brute reference.

    Pins the -x fed to the belt geometry. At AoF=90° B=0 and the sign is
    consequence-free, so this MUST be checked off-axis (§7 A3); with +x the
    breakpoints (and thus z_rep / lit) are materially wrong (§5.5).
    """
    V0, mu, N0, m_grid, pdf, lam = _single_zone_inputs(shell, drag)
    alpha = np.radians(60.0)
    delta = np.radians(15.0)
    pts = [(-3.0, 1.0), (-5.0, 0.5), (-2.0, 2.0), (-6.0, 0.0), (-4.0, -1.5)]
    xs = np.array([p[0] for p in pts])
    ys = np.array([p[1] for p in pts])
    N_impl = _expected_kills_3d_vec(
        xs, ys, H_B, alpha, delta,
        N0, mu, V0, drag, shell.steel.rho, STANDING, m_grid, pdf, lam,
    )
    N_ref = np.array([
        _ref_relocated_single_offaxis(x, y, H_B, alpha, delta, V0, STANDING,
                                      m_grid, pdf, lam)
        for x, y in pts
    ])
    # lit/unlit agreement (a wrong sign flips membership at these points)
    assert np.all((N_impl > 0.0) == (N_ref > 0.0)), (
        f"lit/unlit mismatch vs backward-axis reference: impl={N_impl}, ref={N_ref}"
    )
    # magnitude agreement on lit cells (brute z_rep → true edge as grid→fine;
    # a wrong-sign impl would be off by a large factor)
    lit = N_ref > 0.0
    if np.any(lit):
        assert np.allclose(N_impl[lit], N_ref[lit], rtol=0.02), (
            f"impl={N_impl[lit]} vs ref={N_ref[lit]}"
        )
