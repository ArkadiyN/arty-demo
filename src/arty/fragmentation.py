from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------------------
# Parameter structs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FillerParams:
    name: str
    gurney_const: float  # Gurney energy constant sqrt(2E) [m/s]


FILLERS: dict[str, FillerParams] = {
    "TNT":    FillerParams("TNT",    2440.0),
    "Comp-B": FillerParams("Comp-B", 2700.0),
    "RDX":    FillerParams("RDX",    2830.0),
}


@dataclass(frozen=True)
class SteelParams:
    name: str
    rho: float = 7850.0      # density [kg/m³]
    sigma_f: float = 800e6   # dynamic fracture stress [Pa]
    gamma: float = 65.0      # Mott fragmentation parameter [-]


STEELS: dict[str, SteelParams] = {
    # US WW2 HE shells (M1 105mm, M107 155mm): min YS 65 ksi, 15% elongation.
    # sigma_f / gamma calibrated to M1 PAFRAG fragment-count data.
    "WW2 US HE Shell": SteelParams(
        name="WW2 US HE Shell",
        rho=7850.0,
        sigma_f=800e6,
        gamma=65.0,
    ),
}


@dataclass(frozen=True)
class ShellParams:
    caliber: float = 0.105           # outer diameter [m]
    wall_t: float = 0.009208         # cylindrical wall thickness [m]
    mass_total: float = 14.97        # total projectile mass [kg]
    mass_filler: float = 2.18        # explosive filler mass [kg]
    mass_deductions: float = 0.75    # fuze + rotating band [kg]
    filler: FillerParams = FILLERS["TNT"]
    steel: SteelParams = STEELS["WW2 US HE Shell"]
    # --- Optional Tier-1 zone arc geometry (frag-field-3d-geometry update) ---
    # Present (not None) → arc-integrated zone masses; absent → Tier-2 fractions.
    ogive_outer_R: float | None = None     # outer ogive arc radius [m]
    ogive_inner_R: float | None = None     # inner ogive arc radius [m]
    ogive_len: float | None = None         # ogive axial length [m]
    ogive_tip_dia: float | None = None     # ogive tip outer diameter [m]
    cylinder_len: float | None = None      # cylindrical body axial length [m]
    boattail_inner_dia: float | None = None  # base end inner bore diameter [m]
    base_thickness: float | None = None    # base plate thickness [m]
    boattail_len: float = 0.0              # boattail axial length [m]; 0 → no boattail
    boattail_angle_deg: float = 0.0        # FULL included taper angle (drawing) [deg]
    has_boattail: bool = True              # zone-existence flag
    base_treatment: str = "dead"           # "dead" | "plate" | "mott"
    ogive_crh: float | None = None         # Tier-2 CRH override [calibers]


@dataclass(frozen=True)
class DragParams:
    C_D: float = 0.65       # drag coefficient, tumbling irregular fragment
    C_shape: float = 0.90   # presented-area shape factor
    rho_air: float = 1.225  # air density [kg/m³]


@dataclass(frozen=True)
class TargetParams:
    w: float = 0.5  # presented width of target [m]


@dataclass(frozen=True)
class BurstParams:
    h_b: float = 2.0              # burst height above ground [m]
    angle_of_fall: float = 30.0   # shell angle of fall [degrees], 0=horizontal 90=vertical
    spray_half_angle: float = 15.0  # belt half-width δ [degrees]


@dataclass(frozen=True)
class PostureParams:
    w_perp: float  # body width [m]
    h: float       # vertical extent (standing height of silhouette) [m]
    d: float       # top-down depth (belly-to-back for standing) [m]


STANDING = PostureParams(w_perp=0.5, h=1.7, d=0.3)
PRONE    = PostureParams(w_perp=0.5, h=0.3, d=1.8)


# ---------------------------------------------------------------------------
# Result structs
# ---------------------------------------------------------------------------


@dataclass
class FragField3dResult:
    field_x: np.ndarray               # 2D meshgrid X [m]
    field_y: np.ndarray               # 2D meshgrid Y [m]
    field_pk: np.ndarray              # P(kill) on 2D grid
    r_cross: np.ndarray               # cross-range distances at x=0 [m]
    pk_cross: np.ndarray              # P(kill) along cross-range slice
    r50_cross: float                  # R50 along cross-range [m]
    r_ke: np.ndarray                  # radial slant range for ke_by_mass [m]
    ke_by_mass: dict[float, np.ndarray]
    N0: float
    mu: float
    V0: float
    burst: BurstParams
    posture: PostureParams


@dataclass
class FragFieldResult:
    r: np.ndarray  # radial distance from burst [m]
    p_kill: np.ndarray  # p_kill at each r
    r50: float  # range at which p_kill = 0.5 [m]
    ke_by_mass: dict[float, np.ndarray]  # {mass_g: KE array [J]}
    field_x: np.ndarray  # 2D meshgrid X [m]
    field_y: np.ndarray  # 2D meshgrid Y [m]
    field_pk: np.ndarray  # p_kill on 2D grid
    N0: float  # total fragment count
    mu: float  # Mott half-mass [kg]
    V0: float  # initial fragment velocity [m/s]


# ---------------------------------------------------------------------------
# ES-310 Pk|hit anchors (FAS/Navy 1998)
# ---------------------------------------------------------------------------

_PK_E = np.array([100.0, 1000.0, 4000.0])  # KE anchors [J]
_PK_VAL = np.array([0.10, 0.50, 0.90])  # corresponding Pk|hit [-]


# ---------------------------------------------------------------------------
# Internal geometry helper
# ---------------------------------------------------------------------------


def _shell_geometry(shell: ShellParams) -> tuple[float, float, float, float]:
    r_outer = shell.caliber / 2.0
    r_inner = r_outer - shell.wall_t
    r_inner_bu = r_inner * np.sqrt(3.0)
    r_outer_bu = np.sqrt(r_inner_bu**2 + (r_outer**2 - r_inner**2))
    r_bu = 0.5 * (r_inner_bu + r_outer_bu)
    mass_shell = shell.mass_total - shell.mass_filler - shell.mass_deductions
    return r_outer, r_inner, r_bu, mass_shell


# ---------------------------------------------------------------------------
# Physics functions
# ---------------------------------------------------------------------------


def gurney_velocity(shell: ShellParams) -> float:
    _, _, _, mass_shell = _shell_geometry(shell)
    return shell.filler.gurney_const / np.sqrt(mass_shell / shell.mass_filler + 0.5)


def mott_params(shell: ShellParams, V0: float) -> tuple[float, float]:
    _, _, r_bu, mass_shell = _shell_geometry(shell)
    mu = (
        np.sqrt(2.0 / shell.steel.rho)
        * (shell.steel.sigma_f / shell.steel.gamma) ** 1.5
        * (r_bu / V0) ** 3
    )
    N0 = mass_shell / (2.0 * mu)
    return mu, N0


def retardation_coeff(m: np.ndarray, drag: DragParams, rho_steel: float) -> np.ndarray:
    return (
        drag.rho_air
        * drag.C_D
        * drag.C_shape
        / (2.0 * rho_steel ** (2.0 / 3.0))
        * m ** (-1.0 / 3.0)
    )


def presented_area(gamma: float, posture: PostureParams) -> float:
    """Projected target area [m²] for fragment arriving at elevation angle gamma (radians)."""
    return posture.w_perp * (posture.h * np.cos(gamma) + posture.d * np.sin(gamma))


def pk_given_hit(E: np.ndarray) -> np.ndarray:
    logE = np.log10(np.clip(np.asarray(E, dtype=float), 1e-3, None))
    return np.interp(logE, np.log10(_PK_E), _PK_VAL, left=0.0, right=0.9)


# ---------------------------------------------------------------------------
# Mott distribution / kinematic helpers
#   (single-cylinder convenience functions used by the notebook presentation
#    layer; the heavier integral lives in `expected_kills`)
# ---------------------------------------------------------------------------


def mott_N(m: np.ndarray, N0: float, mu: float) -> np.ndarray:
    """Cumulative fragment count N(m) — fragments with mass >= m [count].

    m  : fragment mass [kg]
    N0 : total fragment count [-]
    mu : Mott half-weight [kg]
    """
    return N0 * np.exp(-np.sqrt(m / mu))


def ke_at_range(
    m: np.ndarray, V0: float, lam: np.ndarray, s: np.ndarray
) -> np.ndarray:
    """Fragment kinetic energy [J] at range s [m].

    m   : fragment mass [kg]
    V0  : initial fragment velocity [m/s]
    lam : drag retardation coefficient [1/m]
    s   : range from burst [m]
    """
    return 0.5 * m * (V0 * np.exp(-lam * s)) ** 2


def min_lethal_mass(
    s: float,
    V0: float,
    E_leth: float,
    drag: DragParams,
    rho_steel: float,
    m_lo: float = 1e-6,
    m_hi: float = 2.0,
    tol: float = 1e-9,
) -> float:
    """Minimum lethal fragment mass [kg] at range s [m] via bisection on KE.

    s       : range from burst [m]
    V0      : initial fragment velocity [m/s]
    E_leth  : lethal kinetic-energy threshold [J]
    drag    : DragParams
    rho_steel : steel density [kg/m³]

    Returns m_hi if even the heaviest fragment is sub-lethal at this range,
    or m_lo if even the lightest fragment is lethal (very close range).
    """

    def _ke(m: float) -> float:
        lam = retardation_coeff(np.array([m]), drag, rho_steel)[0]
        return ke_at_range(np.array([m]), V0, np.array([lam]), np.array([s]))[0]

    if _ke(m_hi) < E_leth:
        return m_hi
    if _ke(m_lo) >= E_leth:
        return m_lo

    lo, hi = m_lo, m_hi
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if _ke(mid) >= E_leth:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def lethal_fragments_at_range(
    r: np.ndarray,
    N0: float,
    mu: float,
    V0: float,
    E_leth: float,
    drag: DragParams,
    rho_steel: float,
) -> np.ndarray:
    """Number of lethal fragments [count] at each ground range r [m]."""
    out = np.empty_like(r, dtype=float)
    for i, ri in enumerate(r):
        m_min = min_lethal_mass(ri, V0, E_leth, drag, rho_steel)
        out[i] = mott_N(np.array([m_min]), N0, mu)[0]
    return out


def p_hit(r: np.ndarray, N_leth: np.ndarray, w: float) -> np.ndarray:
    """Hit probability at range r (Poisson, binary-threshold version).

    r      : range from burst [m]
    N_leth : lethal fragment count [-]
    w      : presented target width [m]
    """
    return 1.0 - np.exp(-N_leth * w / (2.0 * np.pi * r))


def p_kill(N_eff: np.ndarray) -> np.ndarray:
    """P(kill) [-] from expected lethal-hit count N_eff (Poisson)."""
    return 1.0 - np.exp(-N_eff)


def expected_kills(
    r: np.ndarray,
    N0: float,
    mu: float,
    V0: float,
    drag: DragParams,
    rho_steel: float,
    w: float,
    n_mass: int = 300,
) -> np.ndarray:
    m_grid = np.logspace(-6, np.log10(0.5), n_mass)
    pdf = N0 / (2.0 * np.sqrt(mu * m_grid)) * np.exp(-np.sqrt(m_grid / mu))
    lam = retardation_coeff(m_grid, drag, rho_steel)
    out = np.empty_like(r, dtype=float)
    for i, ri in enumerate(r):
        E = 0.5 * m_grid * (V0 * np.exp(-lam * ri)) ** 2
        integrand = pdf * pk_given_hit(E) * w / (2.0 * np.pi * ri)
        out[i] = np.trapezoid(integrand, m_grid)
    return out


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------


def compute_frag_field(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    target: TargetParams = TargetParams(),
    max_radius: float = 300.0,
    n_r: int = 200,
) -> FragFieldResult:
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)

    r = np.linspace(1.0, max_radius, n_r)
    N_eff = expected_kills(r, N0, mu, V0, drag, shell.steel.rho, target.w)
    pk = 1.0 - np.exp(-N_eff)

    idx50 = np.argmin(np.abs(pk - 0.5))
    r50 = float(r[idx50])

    rep_masses_g = [0.5, 5.0, 50.0]
    rep_masses_kg = np.array([m * 1e-3 for m in rep_masses_g])
    lam_rep = retardation_coeff(rep_masses_kg, drag, shell.steel.rho)
    ke_by_mass: dict[float, np.ndarray] = {}
    for m_g, lam_j in zip(rep_masses_g, lam_rep):
        ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (V0 * np.exp(-lam_j * r)) ** 2

    grid_n = 120
    xy = np.linspace(-max_radius, max_radius, grid_n)
    X, Y = np.meshgrid(xy, xy)
    R_grid = np.sqrt(X**2 + Y**2)
    pk_grid = np.interp(R_grid.ravel(), r, pk, left=float(pk[0]), right=0.0)
    field_pk = pk_grid.reshape(R_grid.shape)

    return FragFieldResult(
        r=r,
        p_kill=pk,
        r50=r50,
        ke_by_mass=ke_by_mass,
        field_x=X,
        field_y=Y,
        field_pk=field_pk,
        N0=N0,
        mu=mu,
        V0=V0,
    )


# ---------------------------------------------------------------------------
# 3D burst geometry helpers
# ---------------------------------------------------------------------------


def _shell_axis(alpha_rad: float) -> np.ndarray:
    return np.array([-np.cos(alpha_rad), 0.0, -np.sin(alpha_rad)])


def _forward_shell_axis(alpha_rad: float) -> np.ndarray:
    """Forward shell axis in the ground frame [-]: ``(+cosα, 0, −sinα)``.

    Canonical axis for the lethal-density field (derivation §5.4); both the
    single-zone and four-zone ρ_L paths use this convention so they agree
    pointwise off the x=0 plane. ``alpha_rad`` is the angle of fall [rad].
    """
    return np.array([np.cos(alpha_rad), 0.0, -np.sin(alpha_rad)])


# ---------------------------------------------------------------------------
# Lethal-fragment areal density ρ_L(x, y, z) — target-independent kernel
#   (derivation: updates/lethal-fragment-density-field/derivation.md)
# ---------------------------------------------------------------------------

# Default binary lethal kinetic-energy threshold [J]: the ES-310 (FAS/Navy
# 1998) P_k|hit = 0.5 "moderate personnel kill" anchor, matching the 0.5 point
# of the graded pk_given_hit weighting it replaces (derivation §3).
E_LETH_DEFAULT = 1000.0

# Fixed nominal personnel presented area [m²] for the point kill-probability
# transform P_k = 1 − exp(−ρ_L·A_ref) (pkill-poisson-field derivation §1 eq. 2,
# §6). The standing frontal silhouette A_f = w_perp·h = 0.5·1.7 = 0.85 m²
# (STANDING posture, line 96), frozen as a posture/angle-independent scalar —
# NOT a live presented_area(γ, posture) call: P_k deliberately abstracts away
# arrival angle and posture. This is an engineering convention and a LOWER
# bound; real silhouettes with helmet/armour/kit run 10–25% larger.
A_REF_DEFAULT = 0.85


def build_mmin_table(
    s_grid: np.ndarray,
    V0: float,
    E_leth: float,
    drag: DragParams,
    rho_steel: float,
) -> np.ndarray:
    """Minimum lethal fragment mass m_min(s) [kg] on a 1D slant-range grid [m].

    Precomputes m_min by bisection once per grid node so the 3D field can
    ``np.interp`` instead of root-finding per point (derivation §6). m_min
    depends on slant range s only (per the zone's V0), not on direction or
    (x,y,z) separately, which is why a 1D table suffices.

    s_grid    : monotone slant-range grid [m]
    V0        : zone initial fragment velocity [m/s]
    E_leth    : binary lethal kinetic-energy threshold [J]
    drag      : DragParams
    rho_steel : steel density [kg/m³]

    Vectorised bisection over all grid nodes at once; bit-identical to the
    per-node scalar :func:`min_lethal_mass` (same [m_lo, m_hi] bracket, same
    80-iteration / tol early stop, replicated per element by freezing a node
    once its bracket narrows below ``tol``).
    """
    s = np.asarray(s_grid, dtype=float)
    m_lo, m_hi, tol = 1e-6, 2.0, 1e-9
    # KE(m; s) = ½ m (V0 e^{−λ(m)s})², λ(m) = C m^{−1/3} — monotone in m.
    C = drag.rho_air * drag.C_D * drag.C_shape / (2.0 * rho_steel ** (2.0 / 3.0))

    def ke(m: float) -> np.ndarray:
        lam = C * m ** (-1.0 / 3.0)
        return 0.5 * m * (V0 * np.exp(-lam * s)) ** 2

    hi_sub = ke(m_hi) < E_leth      # heaviest fragment sub-lethal → m_hi
    lo_leth = ke(m_lo) >= E_leth    # lightest fragment lethal → m_lo
    lo = np.full_like(s, m_lo)
    hi = np.full_like(s, m_hi)
    active = ~(hi_sub | lo_leth)
    for _ in range(80):
        if not active.any():
            break
        mid = 0.5 * (lo + hi)
        ge = ke(mid) >= E_leth
        hi = np.where(active & ge, mid, hi)
        lo = np.where(active & ~ge, mid, lo)
        active = active & ((hi - lo) >= tol)
    out = 0.5 * (lo + hi)
    out = np.where(hi_sub, m_hi, out)
    out = np.where(lo_leth, m_lo, out)
    return out


def lethal_density_point(
    x: float,
    y: float,
    z: float,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    N0: float,
    mu: float,
    s_grid: np.ndarray,
    mmin_grid: np.ndarray,
) -> float:
    """Lethal-fragment areal density ρ_L [m⁻²] at field point (x, y, z) [m].

    Single-zone (equatorial cylinder, θ = 90°) evaluation of eq. (3) of the
    derivation: spreading factor 1/(2π s² · 2 sinθ^z · δ) with sinθ^z = sin90° = 1,
    times the closed-form
    Mott lethal count N0·exp(−√(m_min(s)/μ)), with the two target-coupled
    factors (A_p, graded pk) divided out. Returns 0 outside the spray belt or
    for δ ≤ 0 (Dirac-ring limit).

    x, y, z   : field-point coordinates [m]; z is height above ground
    h_b       : burst height above ground [m]
    alpha_rad : angle of fall [rad]
    delta_rad : spray-belt half-width δ [rad]
    N0, mu    : total fragment count [-] and Mott half-mass [kg]
    s_grid    : slant-range grid [m] for the m_min table; MUST cover the full
                range of slant ranges this point can produce — np.interp below
                silently clips (does not error/extrapolate) for s outside
                [s_grid[0], s_grid[-1]], so an undersized grid biases m_min with
                no warning. The field-builder callers size s_grid from the same
                z they query; a direct caller must ensure the same coverage.
    mmin_grid : m_min(s) [kg] tabulated on s_grid (from build_mmin_table)
    """
    if delta_rad <= 0.0:
        return 0.0

    s = np.sqrt(x**2 + y**2 + (z - h_b) ** 2)
    if s < 1e-6:
        return 0.0

    e_axis = _forward_shell_axis(alpha_rad)
    r_vec = np.array([x, y, z - h_b]) / s
    cos_Theta = float(np.dot(r_vec, e_axis))
    # Equatorial belt: θ = 90°, cosθ = 0, so the test is |cosΘ| ≤ sinδ.
    if abs(cos_Theta) > np.sin(delta_rad):
        return 0.0

    # Spreading factor uses the *zone* spray angle θ^z, not the field point's
    # own polar angle Θ: the belt solid angle is 2π·2·sinθ^z·δ, a fixed
    # property of where the belt sits (frag-field-3d-geometry derivation §3.8),
    # so the same belt area spreads the fragments regardless of where inside the
    # belt the point falls. For the single-zone equatorial cylinder θ^z = 90°,
    # hence sinθ^z = 1. (Using sinΘ — the legacy _expected_kills_3d_point
    # convention — only happens to ~agree here because the narrow belt keeps
    # Θ ≈ 90°; it inflates ρ_L by O(δ²) off the belt centre and breaks the
    # single-vs-four-zone consistency check, which uses sinθ^z.)
    sin_theta_z = 1.0  # sin(90°), equatorial cylinder

    # np.interp silently clips outside the grid; assert (debug-mode only, off
    # under python -O) that s is in range so an undersized caller-supplied grid
    # surfaces loudly instead of biasing m_min.
    assert s_grid[0] <= s <= s_grid[-1], (
        f"s={s:.4g} m outside m_min grid [{s_grid[0]:.4g}, {s_grid[-1]:.4g}] m; "
        "np.interp would silently clip"
    )
    m_min = float(np.interp(s, s_grid, mmin_grid))
    N_leth = N0 * np.exp(-np.sqrt(m_min / mu))
    g = 1.0 / (2.0 * np.pi * s**2 * 2.0 * sin_theta_z * delta_rad)
    return float(g * N_leth)


# ---------------------------------------------------------------------------
# Vertical-column lethal-hit count λ(x,y) = w_perp ∫₀ʰ ρ_L dz  (eq. 2)
#   Target-height intercept fix — replaces the ρ_L(z=0)·A_ref point transform
#   with the flux integrated over the column the target actually occupies.
#   (derivation: updates/target-height-intercept/derivation.md §2, §5)
# ---------------------------------------------------------------------------


def _stable_quadratic_roots(A: float, B: float, C: float) -> list[float]:
    """Real roots of ``A ζ² + B ζ + C = 0`` [ζ-units], cancellation-free.

    Uses the numerically-stable form (Numerical Recipes §5.6):
    ``q = −½(B + sgn(B)·√(B²−4AC))``, roots ``q/A`` and ``C/q``. This avoids
    the catastrophic cancellation of the naive ``(−B ± √(B²−4AC))/(2A)`` when
    ``B²≫4AC``, and the division-by-near-zero of that form as ``A → 0`` — the
    physically reachable regime where the belt-edge leading coefficient
    ``A = sin²α − K²`` vanishes (angle of fall near the belt half-cone),
    handled here as a linear solve. Returns 0, 1, or 2 real roots.
    """
    eps = 1e-14
    if abs(A) < eps:
        # Degenerate to linear B ζ + C = 0.
        if abs(B) < eps:
            return []
        return [-C / B]
    disc = B * B - 4.0 * A * C
    if disc < 0.0:
        return []
    sq = float(np.sqrt(disc))
    # copysign(sq, B): +sq when B ≥ 0 (incl. B = +0). q is nonzero unless the
    # discriminant is zero AND B is zero, i.e. a double root at ζ = 0.
    q = -0.5 * (B + np.copysign(sq, B))
    if q == 0.0:
        return [0.0]
    return [q / A, C / q]


def belt_column_breakpoints(
    x: float,
    y: float,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    cos_theta_z: list[float] | tuple[float, ...],
    z_lo: float,
    z_hi: float,
) -> list[float]:
    """Sorted z-breakpoints [m] of the spray-belt membership over ``[z_lo,z_hi]``.

    The kernel's belt test ``|cosΘ − cosθ^z| ≤ sinδ`` is a hard 0/1 gate that
    switches ρ_L on/off at definite crossing heights, so the column integrand
    of eq. (2) is piecewise-smooth with steps at those heights (derivation
    §5.1). Each belt (centre polar cosine ``c ∈ cos_theta_z``) crosses the gate
    where ``cosΘ = c ± sinδ``; with ``ζ = z − h_b`` and
    ``cosΘ = (x cosα − ζ sinα)/s``, ``s² = x²+y²+ζ²``, that boundary is the
    quadratic ``A ζ² + B ζ + C = 0`` (derivation eq. 5, generalised per belt):

        A = sin²α − K²,  B = −2 x cosα sinα,  C = x² cos²α − K² (x²+y²),
        K = c ± sinδ.

    Squaring ``cosΘ = K`` can admit the spurious ``cosΘ = −K`` root; that only
    adds a redundant breakpoint (subdividing an already-smooth interval), which
    the composite-midpoint integrator handles harmlessly. Every *true* membership
    flip is captured, so between consecutive returned breakpoints the active-belt
    set — and hence ρ_L — is smooth. Returns ``[z_lo, …interior roots…, z_hi]``.

    x, y        : column ground coordinates [m]
    h_b         : burst height above ground [m]
    alpha_rad   : angle of fall [rad]
    delta_rad   : spray-belt half-width δ [rad]
    cos_theta_z : belt-centre polar cosines [-] (``[0.0]`` for the single-zone
                  equatorial cylinder; ``cos θ^z`` per active zone for four-zone)
    z_lo, z_hi  : column bounds [m] (typically 0 and the target height h)
    """
    sin_delta = float(np.sin(delta_rad))
    cA = float(np.cos(alpha_rad))
    sA = float(np.sin(alpha_rad))
    B = -2.0 * x * cA * sA
    x2c2 = x * x * cA * cA
    r2 = x * x + y * y
    bps = [z_lo, z_hi]
    for c in cos_theta_z:
        for K in (c - sin_delta, c + sin_delta):
            A = sA * sA - K * K
            C = x2c2 - K * K * r2
            for zeta in _stable_quadratic_roots(A, B, C):
                zc = h_b + zeta
                if z_lo < zc < z_hi:
                    bps.append(zc)
    bps.sort()
    # Dedupe near-coincident breakpoints (spurious/duplicate roots).
    out = [bps[0]]
    for zc in bps[1:]:
        if zc - out[-1] > 1e-12:
            out.append(zc)
    return out


def _vec_quadratic_roots(A: float, B: np.ndarray, C: np.ndarray) -> list[np.ndarray]:
    """Vectorised real roots of ``A ζ² + B ζ + C = 0`` per element of B, C.

    Scalar-``A`` array counterpart of :func:`_stable_quadratic_roots` (same
    cancellation-free Numerical-Recipes form). Returns a list of up to two
    root arrays; entries with no real root at that element are NaN. Matches the
    scalar routine element-for-element (including the A→0 linear degeneracy and
    the double-root-at-0 case) so the breakpoints reproduce those of
    :func:`belt_column_breakpoints`.
    """
    eps = 1e-14
    B = np.asarray(B, dtype=float)
    C = np.asarray(C, dtype=float)
    if abs(A) < eps:
        # Degenerate linear B ζ + C = 0 (no root where B ≈ 0).
        r = np.where(np.abs(B) < eps, np.nan, -C / np.where(np.abs(B) < eps, 1.0, B))
        return [r]
    disc = B * B - 4.0 * A * C
    ok = disc >= 0.0
    sq = np.sqrt(np.where(ok, disc, 0.0))
    q = -0.5 * (B + np.copysign(sq, B))
    qz = q == 0.0
    q_safe = np.where(qz, 1.0, q)
    r1 = np.where(ok, np.where(qz, 0.0, q / A), np.nan)
    r2 = np.where(ok, np.where(qz, np.nan, C / q_safe), np.nan)
    return [r1, r2]


def _belt_breakpoints_vec(
    x: np.ndarray,
    y: np.ndarray,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    cos_theta_z: list[float] | tuple[float, ...],
    z_lo: float,
    z_hi: float,
) -> np.ndarray:
    """Vectorised belt-membership breakpoints for many columns (x, y).

    Array counterpart of :func:`belt_column_breakpoints`: returns a sorted
    ``(P, M)`` array of per-column z-breakpoints [m] padded with ``+inf`` (so
    NaN/out-of-range candidates sort to the end and yield zero-width segments).
    Column ``p`` always begins with ``z_lo`` and ``z_hi``; interior belt-edge
    roots (``cosΘ = c ± sinδ``) strictly inside ``(z_lo, z_hi)`` follow. Near-
    coincident breakpoints are *not* merged — an extra O(1e-12)-wide segment is
    numerically negligible under the midpoint rule (see derivation §3.2).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    P = x.shape[0]
    sin_delta = float(np.sin(delta_rad))
    cA = float(np.cos(alpha_rad))
    sA = float(np.sin(alpha_rad))
    B = -2.0 * x * cA * sA
    x2c2 = x * x * cA * cA
    r2 = x * x + y * y

    cols = [np.full(P, z_lo), np.full(P, z_hi)]
    for c in cos_theta_z:
        for K in (c - sin_delta, c + sin_delta):
            A = sA * sA - K * K
            C = x2c2 - K * K * r2
            for root in _vec_quadratic_roots(A, B, C):
                zc = h_b + root
                # keep only interior real roots; else push to +inf (sorts last)
                keep = np.isfinite(zc) & (zc > z_lo) & (zc < z_hi)
                cols.append(np.where(keep, zc, np.inf))
    bp = np.stack(cols, axis=1)
    bp.sort(axis=1)
    return bp


def _pkill_columns_vec(
    x: np.ndarray,
    y: np.ndarray,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    w_perp: float,
    z_lo: float,
    z_hi: float,
    n_seg: int,
    zone_specs: list[dict],
    cos_theta_z: list[float],
) -> np.ndarray:
    """Vectorised column-integral P_k [-] for many ground columns (x, y).

    Reproduces the per-cell breakpoint-segmented composite-midpoint integral of
    :func:`pkill_field_3d` / four-zone equivalent: ``λ = w_perp·∫ρ_L dz`` with
    strictly-interior midpoint nodes on each belt-membership segment, then
    ``P_k = 1 − exp(−λ)``. ``zone_specs`` is a list of dicts with keys
    ``cos_tz, sin_tz, N0, mu, s_grid, mmin`` (one per active belt). Columns are
    processed in memory-bounded chunks. Matches the scalar path to ~1e-12
    (float reassociation; near-coincident breakpoints unmerged, derivation §3).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    P = x.shape[0]
    out = np.zeros(P, dtype=float)
    if delta_rad <= 0.0 or not zone_specs:
        return out
    sin_delta = float(np.sin(delta_rad))
    cA = float(np.cos(alpha_rad))
    sA = float(np.sin(alpha_rad))

    # Cap the (chunk × n_z_samples) working set; n_z_samples = (M-1)*n_seg.
    n_bp = 2 + 2 * 2 * len(cos_theta_z)  # z_lo, z_hi + 2 edges × 2 roots per belt
    n_zs = max(1, (n_bp - 1)) * n_seg
    chunk = max(1, 2_000_000 // max(1, n_zs))

    for a in range(0, P, chunk):
        xc = x[a:a + chunk]
        yc = y[a:a + chunk]
        bp = _belt_breakpoints_vec(
            xc, yc, h_b, alpha_rad, delta_rad, cos_theta_z, z_lo, z_hi,
        )
        za = bp[:, :-1]                     # (p, M-1)
        zb = bp[:, 1:]
        good = np.isfinite(za) & np.isfinite(zb) & (zb > za)
        za_s = np.where(good, za, h_b)      # collapse padded segments to zero width
        width = np.where(good, zb - za_s, 0.0)
        step = width / n_seg
        # midpoint sample offsets (k + 0.5)/n_seg
        frac = (np.arange(n_seg) + 0.5) / n_seg          # (n_seg,)
        z = za_s[:, :, None] + width[:, :, None] * frac[None, None, :]  # (p, M-1, n_seg)
        wt = step[:, :, None] * np.ones(n_seg)[None, None, :]           # (p, M-1, n_seg)
        z = z.reshape(z.shape[0], -1)                    # (p, Q)
        wt = wt.reshape(wt.shape[0], -1)

        dz = z - h_b
        s = np.sqrt(xc[:, None] ** 2 + yc[:, None] ** 2 + dz ** 2)
        valid = s >= 1e-6
        s_safe = np.where(valid, s, 1.0)
        cos_Theta = (xc[:, None] * cA - dz * sA) / s_safe
        # Vectorised parity with the scalar reference (lethal_density_*_point
        # asserts s_grid[0] <= s <= s_grid[-1] before np.interp): guard the query
        # range so a slant_range_grid coverage regression fails loudly here
        # instead of silently clipping. Only the *weighted* samples matter —
        # collapsed padded segments (width 0, wt 0) force z=h_b, giving a spurious
        # s=horizontal-radius below the grid floor that carries zero weight and is
        # never evaluated by the scalar path; excluding them keeps the check
        # faithful (checking all samples would false-fire on those artifacts).
        weighted = wt > 0.0
        if np.any(weighted):
            sw = s_safe[weighted]
            q_lo, q_hi = float(sw.min()), float(sw.max())
        else:
            q_lo, q_hi = np.inf, -np.inf  # nothing queried; skip below

        rho = np.zeros_like(s)
        for spec in zone_specs:
            sg = spec["s_grid"]
            assert q_hi < q_lo or (q_lo >= sg[0] and q_hi <= sg[-1]), (
                f"slant range [{q_lo:.4g}, {q_hi:.4g}] m outside m_min grid "
                f"[{sg[0]:.4g}, {sg[-1]:.4g}] m; np.interp would clip"
            )
            mask = valid & (np.abs(cos_Theta - spec["cos_tz"]) <= sin_delta)
            m_min = np.interp(s_safe, spec["s_grid"], spec["mmin"])
            N_leth = spec["N0"] * np.exp(-np.sqrt(m_min / spec["mu"]))
            g = 1.0 / (2.0 * np.pi * s_safe ** 2 * 2.0 * spec["sin_tz"] * delta_rad)
            rho = rho + np.where(mask, g * N_leth, 0.0)

        col = np.sum(rho * wt, axis=1)
        out[a:a + chunk] = 1.0 - np.exp(-w_perp * col)
    return out


def integrate_column_density(rho_point, breakpoints: list[float], n_seg: int) -> float:
    """Composite-midpoint ∫ρ_L dz [m⁻¹] over the belt-segmented column (eq. 6).

    Integrates ``rho_point(z)`` [m⁻²] piecewise over the sub-intervals defined
    by ``breakpoints`` (from :func:`belt_column_breakpoints`), sampling ``n_seg``
    **strictly-interior** midpoints per sub-interval. Midpoint (never an
    endpoint) is required because the kernel independently re-derives the belt
    gate from (x,y,z): evaluating ρ_L exactly at a breakpoint is a floating-point
    coin flip that can return 0.0, so an endpoint-weighted rule (trapezoid) loses
    ρ_L·Δz/2 intermittently — an O(1/n_seg) bias. Midpoint avoids the belt edge
    entirely and keeps O(1/n_seg²) accuracy on the smooth interior
    (derivation §5.2, §5.4). Returns the areal-density line integral [m⁻¹];
    the caller multiplies by w_perp to get the mean lethal-hit count λ.

    rho_point   : callable z [m] → ρ_L [m⁻²]
    breakpoints : sorted column breakpoints [m]
    n_seg       : midpoint nodes per sub-interval (default caller: 9)
    """
    total = 0.0
    for za, zb in zip(breakpoints[:-1], breakpoints[1:]):
        width = zb - za
        if width <= 0.0:
            continue
        step = width / n_seg
        for k in range(n_seg):
            zc = za + (k + 0.5) * step
            total += rho_point(zc) * step
    return total


def _expected_kills_3d_point(
    x_g: float,
    y_g: float,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    N0: float,
    mu: float,
    V0: float,
    drag: DragParams,
    rho_steel: float,
    posture: PostureParams,
    m_grid: np.ndarray,
    pdf: np.ndarray,
    lam: np.ndarray,
) -> float:
    # delta->0 limit: the spray collapses to a Dirac delta on the equatorial
    # ring. On a finite discrete grid no point lies exactly on that ring, so
    # N_eff -> 0 everywhere. Guard the 1/delta_rad denominator below.
    if delta_rad <= 0.0:
        return 0.0

    s = np.sqrt(x_g**2 + y_g**2 + h_b**2)
    if s < 1e-6:
        return 0.0

    e_axis = _shell_axis(alpha_rad)
    r_vec = np.array([x_g, y_g, -h_b]) / s
    cos_Theta = np.dot(r_vec, e_axis)
    if abs(cos_Theta) > np.sin(delta_rad):
        return 0.0

    sin_Theta = np.sqrt(max(0.0, 1.0 - cos_Theta**2))
    if sin_Theta < 1e-9:
        return 0.0

    gamma = np.arcsin(np.clip(h_b / s, -1.0, 1.0))
    Ap = presented_area(gamma, posture)

    E = 0.5 * m_grid * (V0 * np.exp(-lam * s)) ** 2
    integrand = pdf * pk_given_hit(E) * Ap / (2.0 * np.pi * s**2 * 2.0 * sin_Theta * delta_rad)
    return float(np.trapezoid(integrand, m_grid))


# Cap on the (n_cells × n_mass) working array for the vectorised Family-A mass
# integral; in-belt cells are processed in chunks no larger than this so peak
# memory stays bounded regardless of grid size / belt width. Canonical
# definition — zones.py imports this so the single-zone and four-zone builders
# share one tuning knob.
_FAMILY_A_CHUNK = 2_000_000


def _expected_kills_3d_vec(
    x_g: np.ndarray,
    y_g: np.ndarray,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    N0: float,
    mu: float,
    V0: float,
    drag: DragParams,
    rho_steel: float,
    posture: PostureParams,
    m_grid: np.ndarray,
    pdf: np.ndarray,
    lam: np.ndarray,
) -> np.ndarray:
    """Vectorised single-zone Family-A expected lethal-hit count on (x_g, y_g).

    ``x_g, y_g`` are 1-D ground-point arrays [m] (z = 0). Bit-identical to a
    per-cell loop over :func:`_expected_kills_3d_point`: the mass integral is
    evaluated exactly on in-belt cells only, then scaled by the direction-
    dependent A_p/(2π s²·2 sinΘ·δ) factor (here sinΘ is the point's own polar
    angle, not a fixed belt sinθ^z). Returns the expected-count array [-].
    """
    x_g = np.asarray(x_g, dtype=float)
    y_g = np.asarray(y_g, dtype=float)
    out = np.zeros_like(x_g)
    if delta_rad <= 0.0:
        return out

    s = np.sqrt(x_g**2 + y_g**2 + h_b**2)
    e_axis = _shell_axis(alpha_rad)
    s_safe = np.where(s >= 1e-6, s, 1.0)
    cos_Theta = (x_g * e_axis[0] + (-h_b) * e_axis[2]) / s_safe
    sin_Theta = np.sqrt(np.maximum(0.0, 1.0 - cos_Theta**2))
    mask = (s >= 1e-6) & (np.abs(cos_Theta) <= np.sin(delta_rad)) & (sin_Theta >= 1e-9)
    idx = np.nonzero(mask)[0]
    if idx.size == 0:
        return out

    s_b = s[idx]
    gamma = np.arcsin(np.clip(h_b / s_b, -1.0, 1.0))
    Ap = presented_area(gamma, posture)
    geom = Ap / (2.0 * np.pi * s_b**2 * 2.0 * sin_Theta[idx] * delta_rad)

    n = s_b.shape[0]
    J = np.empty(n, dtype=float)
    chunk = max(1, _FAMILY_A_CHUNK // m_grid.shape[0])
    for a in range(0, n, chunk):
        s_c = s_b[a:a + chunk]
        E = 0.5 * m_grid[None, :] * (V0 * np.exp(-lam[None, :] * s_c[:, None])) ** 2
        J[a:a + chunk] = np.trapezoid(pdf[None, :] * pk_given_hit(E), m_grid, axis=1)
    out[idx] = J * geom
    return out


# ---------------------------------------------------------------------------
# 3D top-level entry point
# ---------------------------------------------------------------------------


def slant_range_grid(
    max_radius: float,
    h_b: float,
    z_max: float,
    n_s: int = 400,
    s_min: float = 0.5,
    margin: float = 1.05,
    z_min: float | None = None,
) -> np.ndarray:
    """Uniform slant-range grid [m] spanning a 3D field box (derivation §6.1).

    The maximum slant range to any box corner at height z_max is
    √(2·max_radius² + (z_max − h_b)²). The minimum is the closest the box gets
    to the burst at (0, 0, h_b): 0 in (x, y) at the origin column, and
    max(0, h_b − z_max, z_min − h_b) in z when h_b lies outside [z_min, z_max].
    That geometric minimum (not a fixed floor) is the grid's lower bound, so the
    m_min table always covers every point the field-builder can query — the
    origin column at a z-layer near h_b can reach a slant range below the old
    fixed 0.5 floor, which silently clipped (or, in debug, tripped the
    ``lethal_density_point`` range assertion). The lower bound is still floored
    above the 1/s² singularity guard (``lethal_density_point`` early-returns for
    s < 1e-6) by ``s_floor``. A ×margin factor on s_max ensures no field point
    extrapolates off the top of the grid.

    max_radius : half-extent of the (x, y) box [m]
    h_b        : burst height above ground [m]
    z_max      : top of the evaluated height range [m]
    n_s        : number of grid points
    s_min      : legacy fixed floor [m]; used only as an upper cap on the
                 geometric lower bound so the grid never starts *above* the
                 achievable minimum (kept for API compatibility)
    margin     : multiplicative headroom on s_max [-]
    z_min      : bottom of the evaluated height range [m] (default 0, the
                 ground); the box spans z in [z_min, z_max]
    """
    if z_min is None:
        z_min = 0.0
    # The farthest box corner from the burst at height h_b is at whichever of
    # z_min, z_max is more distant from h_b — not always z_max. For a vertical
    # column [0, h] with h_b above the column top, z_min=0 is the far extreme,
    # so s_max must use max(|z_min−h_b|, |z_max−h_b|) or the m_min grid
    # under-covers the near-ground corners and trips the range assertion. For a
    # single layer (z_min=z_max) this is identical to the old (z_max−h_b)² form.
    dz2 = max((z_max - h_b) ** 2, (z_min - h_b) ** 2)
    s_max = margin * np.sqrt(2.0 * max_radius**2 + dz2)
    # Closest approach of the box to the burst: 0 in (x, y), and the gap in z
    # only if h_b is outside [z_min, z_max]. Inside that span the origin column
    # passes through the burst height, so the geometric minimum is 0.
    s_geo_min = max(0.0, h_b - z_max, z_min - h_b)
    # Floor above the singularity guard; never start above the achievable min.
    s_floor = 1e-3
    s_lo = min(s_min, max(s_floor, s_geo_min))
    return np.linspace(s_lo, s_max, n_s)


def _lethal_density_layer_vec(
    X: np.ndarray,
    Y: np.ndarray,
    z: float,
    h_b: float,
    alpha_rad: float,
    delta_rad: float,
    N0: float,
    mu: float,
    s_grid: np.ndarray,
    mmin_grid: np.ndarray,
) -> np.ndarray:
    """Vectorised single-zone ρ_L [m⁻²] on an (x, y) layer at height ``z`` [m].

    Bit-identical to a per-cell loop over :func:`lethal_density_point` (same
    m_min table, same belt gate) but evaluated as array ops. ``X, Y`` are 2-D
    meshgrids [m]; returns ρ_L on the same shape.
    """
    rho = np.zeros_like(X)
    if delta_rad <= 0.0:
        return rho
    s = np.sqrt(X**2 + Y**2 + (z - h_b) ** 2)
    valid = s >= 1e-6
    s_safe = np.where(valid, s, 1.0)
    cos_Theta = (X * np.cos(alpha_rad) - (z - h_b) * np.sin(alpha_rad)) / s_safe
    mask = valid & (np.abs(cos_Theta) <= np.sin(delta_rad))
    m_min = np.interp(s_safe, s_grid, mmin_grid)
    N_leth = N0 * np.exp(-np.sqrt(m_min / mu))
    g = 1.0 / (2.0 * np.pi * s_safe**2 * 2.0 * delta_rad)
    return np.where(mask, g * N_leth, 0.0)


def compute_lethal_density_field_3d(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    burst: BurstParams = BurstParams(),
    z: float = 0.0,
    max_radius: float = 80.0,
    n_grid: int = 80,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Single-zone lethal-density field ρ_L [m⁻²] on an (x, y) patch at height z.

    Evaluates eq. (3) of the derivation (single equatorial cylinder) over a
    square (x, y) grid at a fixed height ``z`` [m] above ground, using a
    precomputed per-zone m_min(s) table interpolated per point (§6). All
    physics is target-independent: A_p and the graded weighting are divided
    out (§5.1).

    Returns ``(X, Y, rho_L)`` meshgrids [m, m, m⁻²].
    """
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)

    alpha_rad = np.radians(burst.angle_of_fall)
    delta_rad = np.radians(burst.spray_half_angle)

    # This field is a single height layer (z fixed): the box spans z in [z, z],
    # so pass z as both bounds. The closest the (x, y) patch gets to the burst
    # at (0, 0, h_b) is |z - h_b| at the origin, which slant_range_grid uses as
    # the table's true lower bound (covering the case z ≈ h_b, where |z - h_b|
    # falls below the old fixed 0.5 floor and tripped the range assertion).
    s_grid = slant_range_grid(max_radius, burst.h_b, z, n_s=n_s, z_min=z)
    mmin_grid = build_mmin_table(s_grid, V0, E_leth, drag, shell.steel.rho)

    xy = np.linspace(-max_radius, max_radius, n_grid)
    X, Y = np.meshgrid(xy, xy)
    rho_L = _lethal_density_layer_vec(
        X, Y, z, burst.h_b, alpha_rad, delta_rad, N0, mu, s_grid, mmin_grid,
    )
    return X, Y, rho_L


def compute_lethal_density_volume_3d(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    burst: BurstParams = BurstParams(),
    z_max: float = 10.0,
    max_radius: float = 80.0,
    n_grid: int = 30,
    n_z: int = 20,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Single-zone lethal-density volume ρ_L [m⁻²] on an (x, y, z) grid.

    No new physics: evaluates :func:`compute_lethal_density_field_3d` once per
    z-layer over ``n_z`` heights from 0 to ``z_max`` [m] and stacks the per-layer
    (X, Y, rho_L) outputs into 3D arrays. The z=0 layer is numerically identical
    to ``compute_lethal_density_field_3d(z=0.0)`` for matching parameters.

    z_max      : top of the z-extent [m] (bottom is the ground, z=0)
    max_radius : half-extent of the (x, y) box [m]
    n_grid     : grid resolution per x/y axis
    n_z        : number of z-layers

    Returns ``(X, Y, Z, rho_L)`` 3D meshgrids [m, m, m, m⁻²], indexed (iz, ix, iy).
    """
    z_layers = np.linspace(0.0, z_max, n_z)
    X2d: np.ndarray | None = None
    Y2d: np.ndarray | None = None
    layers: list[np.ndarray] = []
    for z in z_layers:
        X2d, Y2d, rho_L_layer = compute_lethal_density_field_3d(
            shell=shell, drag=drag, burst=burst, z=float(z),
            max_radius=max_radius, n_grid=n_grid, E_leth=E_leth, n_s=n_s,
        )
        layers.append(rho_L_layer)

    rho_L = np.stack(layers, axis=0)
    assert X2d is not None and Y2d is not None
    X = np.broadcast_to(X2d, rho_L.shape).copy()
    Y = np.broadcast_to(Y2d, rho_L.shape).copy()
    Z = np.broadcast_to(
        z_layers[:, np.newaxis, np.newaxis], rho_L.shape
    ).copy()
    return X, Y, Z, rho_L


def pkill_field_3d(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    burst: BurstParams = BurstParams(),
    posture: PostureParams = STANDING,
    max_radius: float = 80.0,
    n_grid: int = 80,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
    n_seg: int = 9,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Single-zone ground kill probability P_k [-] ∈ [0,1] for a target at (x, y).

    P_k = 1 − exp(−λ), with the mean lethal-hit count formed by integrating the
    lethal-fragment areal density ρ_L [m⁻²] over the vertical column the target
    actually occupies (target-height-intercept derivation eq. 2/3/6):

        λ(x,y) = w_perp · ∫₀ʰ ρ_L(x,y,z) dz,

    reading (w_perp, h) live from ``posture``. This replaces the earlier
    ρ_L(z=0)·A_ref point transform, which read the flux only on the ground plane
    and reported a false safe ring wherever a near-horizontal spray belt crosses
    chest/head height but never descends to z=0 close in (derivation §1, §6.3).
    The old transform is the degenerate z-flat limit of this integral with
    A_ref = w_perp·h (derivation §3).

    The column integral is evaluated piecewise on the belt-membership segments
    (single equatorial belt cosθ^z = 0) with a composite-midpoint rule —
    strictly-interior nodes so the belt-edge 0/1 gate never coin-flips
    (derivation §5) — vectorised over all (x, y) columns at once by
    :func:`_pkill_columns_vec` (breakpoints via ``_belt_breakpoints_vec``). The
    scalar per-cell reference this reproduces (:func:`belt_column_breakpoints` +
    ``integrate_column_density``) is retained unchanged as the equivalence
    baseline for the regression harness and property tests. One m_min(s) table
    spanning the whole [0, h] column is built once and shared across all
    z-samples (§5.3).

    Caveats (derivation §2/§7, A1/A2): (A1) frontal projection — each strip
    contributes w_perp·dz (γ = 0 arrival), matching the shipped A_ref
    convention; obliquity is deferred. (A2) Poisson independence / no shielding,
    and a sharp E_leth cut with P_k|hit = 1 once counted; more pessimistic than
    the ES-310 aggregate, not a tissue-level wound model.

    Returns ``(X, Y, P_k)`` meshgrids [m, m, -].
    """
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)

    alpha_rad = np.radians(burst.angle_of_fall)
    delta_rad = np.radians(burst.spray_half_angle)
    h_b = burst.h_b
    h = posture.h
    w_perp = posture.w_perp

    # One m_min(s) table spanning the whole [0, h] column, shared across every
    # (x, y) column and every z-sample within it (§5.3).
    s_grid = slant_range_grid(max_radius, h_b, z_max=h, n_s=n_s, z_min=0.0)
    mmin_grid = build_mmin_table(s_grid, V0, E_leth, drag, shell.steel.rho)

    xy = np.linspace(-max_radius, max_radius, n_grid)
    X, Y = np.meshgrid(xy, xy)
    # Single equatorial belt (θ^z = 90°, cosθ^z = 0, sinθ^z = 1).
    zone_specs = [{
        "cos_tz": 0.0, "sin_tz": 1.0, "N0": N0, "mu": mu,
        "s_grid": s_grid, "mmin": mmin_grid,
    }]
    P_k = _pkill_columns_vec(
        X.ravel(), Y.ravel(), h_b, alpha_rad, delta_rad, w_perp, 0.0, h,
        n_seg, zone_specs, [0.0],
    ).reshape(X.shape)
    assert np.all((P_k >= 0.0) & (P_k <= 1.0)), "P_k outside [0,1]"
    return X, Y, P_k


def pkill_volume_3d(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    burst: BurstParams = BurstParams(),
    z_max: float = 10.0,
    max_radius: float = 80.0,
    n_grid: int = 30,
    n_z: int = 20,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
    A_ref: float = A_REF_DEFAULT,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Single-zone point kill probability P_k [-] ∈ [0,1] on an (x, y, z) grid.

    P_k = 1 − exp(−ρ_L·A_ref), with ρ_L [m⁻²] from
    :func:`compute_lethal_density_volume_3d` and A_ref [m²] the fixed nominal
    personnel presented area (0.85 m², standing frontal — lower bound; +10–25%
    with kit). A pure elementwise transform of ρ_L; no new physics
    (pkill-poisson-field derivation eq. 1, §6). This volume builder is the
    point-in-space diagnostic — "one person standing at exactly this height z" —
    and deliberately keeps the frozen A_ref (target-height-intercept derivation
    §8); the ground field :func:`pkill_field_3d` instead integrates the ρ_L flux
    over the target's whole [0, h] column.

    Caveats (derivation §2, A1/A2): Poisson independence / no shielding; sharp
    E_leth threshold with P_k|hit = 1 once counted — more pessimistic than the
    ES-310 aggregate, not a tissue-level wound model.

    Returns ``(X, Y, Z, P_k)`` 3D meshgrids [m, m, m, -], indexed (iz, ix, iy).
    """
    X, Y, Z, rho_L = compute_lethal_density_volume_3d(
        shell=shell, drag=drag, burst=burst, z_max=z_max,
        max_radius=max_radius, n_grid=n_grid, n_z=n_z, E_leth=E_leth, n_s=n_s,
    )
    P_k = 1.0 - np.exp(-rho_L * A_ref)
    assert np.all((P_k >= 0.0) & (P_k <= 1.0)), "P_k outside [0,1]"
    return X, Y, Z, P_k


def compute_frag_field_3d(
    shell: ShellParams = ShellParams(),
    drag: DragParams = DragParams(),
    burst: BurstParams = BurstParams(),
    posture: PostureParams = STANDING,
    max_radius: float = 80.0,
    n_grid: int = 80,
    n_mass: int = 300,
) -> FragField3dResult:
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, V0)

    alpha_rad = np.radians(burst.angle_of_fall)
    delta_rad = np.radians(burst.spray_half_angle)

    m_grid = np.logspace(-6, np.log10(0.5), n_mass)
    pdf = N0 / (2.0 * np.sqrt(mu * m_grid)) * np.exp(-np.sqrt(m_grid / mu))
    lam = retardation_coeff(m_grid, drag, shell.steel.rho)

    xy = np.linspace(-max_radius, max_radius, n_grid)
    X, Y = np.meshgrid(xy, xy)
    N_eff = _expected_kills_3d_vec(
        X.ravel(), Y.ravel(), burst.h_b, alpha_rad, delta_rad,
        N0, mu, V0, drag, shell.steel.rho, posture, m_grid, pdf, lam,
    )
    field_pk = (1.0 - np.exp(-N_eff)).reshape(X.shape)

    N_eff_cross = _expected_kills_3d_vec(
        np.zeros_like(xy), xy, burst.h_b, alpha_rad, delta_rad,
        N0, mu, V0, drag, shell.steel.rho, posture, m_grid, pdf, lam,
    )
    pk_cross = 1.0 - np.exp(-N_eff_cross)
    r_cross = np.abs(xy)
    idx50 = np.argmin(np.abs(pk_cross - 0.5))
    r50_cross = float(np.abs(xy[idx50]))

    rep_masses_g = [0.5, 5.0, 50.0]
    rep_masses_kg = np.array([m * 1e-3 for m in rep_masses_g])
    lam_rep = retardation_coeff(rep_masses_kg, drag, shell.steel.rho)
    r_ke = np.linspace(0, max_radius, n_grid)
    ke_by_mass: dict[float, np.ndarray] = {}
    for m_g, lam_j in zip(rep_masses_g, lam_rep):
        ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (V0 * np.exp(-lam_j * r_ke)) ** 2

    return FragField3dResult(
        field_x=X,
        field_y=Y,
        field_pk=field_pk,
        r_cross=r_cross,
        pk_cross=pk_cross,
        r50_cross=r50_cross,
        r_ke=r_ke,
        ke_by_mass=ke_by_mass,
        N0=N0,
        mu=mu,
        V0=V0,
        burst=burst,
        posture=posture,
    )
