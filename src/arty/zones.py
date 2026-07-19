"""Four-zone (ogive / cylinder / boattail / base) shell decomposition.

Extends the single-cylinder Gurney-Mott treatment in `fragmentation.py` with
a per-zone breakdown: each zone carries its own steel mass, explosive
allocation, Gurney velocity, Mott half-mass, break-up radius and spray
elevation angle. Adds an angle-of-fall (AoF) ground projection and a
four-zone P(kill) ground field.

All quantities are SI internally (kg, m, m/s, degrees only where a field is
explicitly named ``*_deg``).

References
----------
- experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md
- experiment/fragmentation-field/updates/target-area-profile/derivation.md
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from arty.fragmentation import (
    A_REF_DEFAULT,
    DragParams,
    E_LETH_DEFAULT,
    STANDING,
    PostureParams,
    ShellParams,
    SteelParams,
    _FAMILY_A_CHUNK,
    _forward_shell_axis,
    _pkill_columns_vec,
    build_mmin_table,
    pk_given_hit,
    presented_area,
    slant_range_grid,
)

# Engineering convention for Tier-2 shells lacking drawing-derived ogive
# arc geometry; see notebook Limitations §12.
CRH_DEFAULT_TIER2 = 6.0


@dataclass(frozen=True)
class ZoneParams:
    """Per-zone fragmentation parameters."""

    mass_kg: float    # zone steel mass [kg]
    C_kg: float       # zone explosive allocation [kg]
    V0_ms: float      # zone initial fragment velocity [m/s]
    mu: float         # zone Mott half-mass [kg]
    spray_deg: float  # zone spray angle from forward axis [deg]
    r_bu: float       # zone break-up mean radius [m]
    wall_t: float     # zone effective wall thickness [m]


@dataclass(frozen=True)
class ShellZones:
    """The four zones of a decomposed shell."""

    ogive: ZoneParams
    cylinder: ZoneParams
    boattail: ZoneParams
    base: ZoneParams


def _ogive_arc_centre(R: float, D: float, L_n: float, r_tip: float) -> tuple[float, float]:
    """Return (x_c, r_c) [m]: arc centre of a circular tangent ogive.

    Tangent at the shoulder means the surface slope dr/dx = 0 at x = 0
    (matched to the parallel cylinder), so the centre lies directly
    radial-inward from the shoulder:

        x_c = 0,  r_c = D/2 - R

    The arc passes through (0, D/2) and continues to the truncation
    (L_n, r(L_n)). For drawing-derived (R, D, L_n, r_tip), the truncated
    tip radius r(L_n) should match r_tip within drawing tolerance; this
    is checked but not enforced. For secant ogives (M107 outer) the
    shoulder is not strictly tangent and r_tip is the better anchor —
    in that case the simple formula still produces a workable spray
    angle within engineering tolerance.
    """
    return 0.0, D / 2.0 - R


def _arc_centre_two_point(
    R: float, x1: float, r1: float, x2: float, r2: float
) -> tuple[float, float]:
    """Return (x_c, r_c) [m]: centre of a circular arc radius R through two points.

    The arc of radius R passes through P1=(x1, r1) and P2=(x2, r2). Both
    satisfy ``(x - x_c)^2 + (r - r_c)^2 = R^2``. Subtracting the two
    equations gives a line in (x_c, r_c):

        2(x2 - x1) x_c + 2(r2 - r1) r_c = (x2^2 + r2^2) - (x1^2 + r1^2)

    which is solved for r_c(x_c) (here x2 != x1, so divide by (r2 - r1)
    via the perpendicular-bisector parameterisation). We parameterise along
    the perpendicular bisector of P1P2: the centre lies on it at signed
    distance ``d`` from the midpoint M, where ``d^2 = R^2 - (|P1P2|/2)^2``.
    Two solutions exist (±d); we pick the one with the smaller r_c (centre
    below both endpoints) to give the convex-outward ogive arc.
    """
    mx = 0.5 * (x1 + x2)
    mr = 0.5 * (r1 + r2)
    dx = x2 - x1
    dr = r2 - r1
    chord = np.hypot(dx, dr)
    half = chord / 2.0
    # Unit perpendicular to the chord: rotate chord direction by 90 deg.
    px = -dr / chord
    pr = dx / chord
    d = np.sqrt(max(0.0, R**2 - half**2))
    # Two candidate centres
    c1 = (mx + d * px, mr + d * pr)
    c2 = (mx - d * px, mr - d * pr)
    # Pick the centre with the smaller r-coordinate (below both endpoints).
    return c1 if c1[1] <= c2[1] else c2


def _zone_gurney(M_z: float, C_z: float, V_g: float, k: float = 1.0) -> float:
    """Zone Gurney V0 [m/s] from zone-local M/C and reduction factor k [-]."""
    if C_z <= 0.0:
        return 0.0
    return k * V_g / np.sqrt(M_z / C_z + 0.5)


def _zone_mott_mu(r_bu_z: float, V0_z: float, steel: SteelParams) -> float:
    """Zone Mott half-mass [kg] from Gold (2017) eq. 16."""
    if V0_z <= 0.0:
        return float("inf")
    return (
        np.sqrt(2.0 / steel.rho)
        * (steel.sigma_f / steel.gamma) ** 1.5
        * (r_bu_z / V0_z) ** 3
    )


def _r_bu_from_inner(r_i: float, r_o: float) -> float:
    """Mean break-up radius [m] from 3x expansion + wall-volume conservation."""
    r_i_bu = r_i * np.sqrt(3.0)
    r_o_bu = np.sqrt(r_i_bu**2 + (r_o**2 - r_i**2))
    return 0.5 * (r_i_bu + r_o_bu)


def _base_k(shell: ShellParams) -> float:
    """Base-plate Gurney reduction factor k^b [-] per NWC TP 7124."""
    if shell.caliber >= 0.150:
        return 0.70   # M107 class
    return 0.75       # M1 class / Tier-2 default


def compute_shell_zones(shell: ShellParams) -> ShellZones:
    """Decompose a shell into four zones (ogive/cylinder/boattail/base).

    Tier-1 (``shell.ogive_outer_R is not None``): 200-slice midpoint
    integration of annular cross-section over each axial zone, then
    normalise to total steel mass.

    Tier-2: fixed fractions from derivation section 3.2.
    """
    D = shell.caliber
    t_w = shell.wall_t
    M_steel = shell.mass_total - shell.mass_filler - shell.mass_deductions
    C_total = shell.mass_filler
    rho_s = shell.steel.rho

    is_tier1 = shell.ogive_outer_R is not None

    # ---------------- mass and interior-volume integration ----------------
    if is_tier1:
        # Tier-1 requires the full drawing-derived arc geometry; assert the
        # invariant so the optional fields narrow to float for the branch.
        assert (
            shell.ogive_outer_R is not None
            and shell.ogive_inner_R is not None
            and shell.ogive_len is not None
            and shell.ogive_tip_dia is not None
            and shell.cylinder_len is not None
            and shell.boattail_len is not None
            and shell.base_thickness is not None
            and shell.boattail_inner_dia is not None
        ), "Tier-1 shell must carry full zone arc geometry"
        L_n = shell.ogive_len
        L_c = shell.cylinder_len
        L_t = shell.boattail_len
        t_b = shell.base_thickness
        R_o = shell.ogive_outer_R
        R_i = shell.ogive_inner_R
        r_tip_o = shell.ogive_tip_dia / 2.0
        r_tip_i = max(0.0, r_tip_o - t_w)  # inner tip ~= outer tip - wall
        d_bt_i = shell.boattail_inner_dia

        # 200-slice midpoint Riemann sum over the ogive.
        # Outer arc: shoulder-tangent (outer surface is tangent to cylinder wall).
        # Inner arc: two-point fit anchored at shoulder bore + drawing tip bore —
        # the inner cavity does not satisfy shoulder tangency; using both drawing
        # anchors gives zero tip-radius error vs. 8+ mm from shoulder tangency.
        xo_c, ro_c = _ogive_arc_centre(R_o, D, L_n, r_tip_o)
        xi_c, ri_c = _arc_centre_two_point(R_i, 0.0, D / 2.0 - t_w, L_n, r_tip_i)
        N = 200
        x_mid = (np.arange(N) + 0.5) * (L_n / N)
        r_o = ro_c + np.sqrt(np.maximum(0.0, R_o**2 - (x_mid - xo_c) ** 2))
        r_i = ri_c + np.sqrt(np.maximum(0.0, R_i**2 - (x_mid - xi_c) ** 2))
        dV_ann = np.pi * (r_o**2 - r_i**2) * (L_n / N)
        dV_int = np.pi * r_i**2 * (L_n / N)
        M_ogive_raw = rho_s * dV_ann.sum()
        V_int_ogive = dV_int.sum()
        r_i_mean_ogive = float(r_i.mean())
        r_o_mean_ogive = float(r_o.mean())

        # Cylinder: analytic
        M_cyl_raw = rho_s * np.pi * t_w * (D - t_w) * L_c
        V_int_cyl = np.pi * (D / 2.0 - t_w) ** 2 * L_c

        # Boattail: 200-slice taper (linear outer + linear inner)
        if L_t > 0.0 and shell.has_boattail:
            x_t = (np.arange(N) + 0.5) * (L_t / N)
            # Outer radius tapers from D/2 to (D/2 - L_t * tan(theta_bt_half))
            theta_half = np.radians(shell.boattail_angle_deg) / 2.0
            r_o_t = D / 2.0 - x_t * np.tan(theta_half)
            r_i_t = (D / 2.0 - t_w) + (d_bt_i / 2.0 - (D / 2.0 - t_w)) * (x_t / L_t)
            dV_t = np.pi * (r_o_t**2 - r_i_t**2) * (L_t / N)
            dV_t_int = np.pi * r_i_t**2 * (L_t / N)
            M_bt_raw = rho_s * dV_t.sum()
            V_int_bt = dV_t_int.sum()
            r_i_mean_bt = float(r_i_t.mean())
            r_o_mean_bt = float(r_o_t.mean())
        else:
            M_bt_raw = 0.0
            V_int_bt = 0.0
            r_i_mean_bt = (D / 2.0 - t_w)
            r_o_mean_bt = D / 2.0

        # Base plate: solid disk sized to the boattail inner bore at base end
        # (the plate seals the rear bore; outer cylinder/boattail steel above it
        # is counted by the cylinder and boattail integrals).
        r_base_outer = (d_bt_i / 2.0) if d_bt_i is not None else (D / 2.0 - t_w)
        M_base_raw = rho_s * np.pi * r_base_outer**2 * t_b

        # Normalise zone masses to total steel mass
        M_zones_raw = np.array([M_ogive_raw, M_cyl_raw, M_bt_raw, M_base_raw])
        scale = M_steel / M_zones_raw.sum()
        M_ogive, M_cyl, M_bt, M_base = M_zones_raw * scale

        # Explosive allocation by interior volume (base = 0 by integration)
        V_int_total = V_int_ogive + V_int_cyl + V_int_bt
        if V_int_total > 0:
            C_ogive = C_total * V_int_ogive / V_int_total
            C_cyl   = C_total * V_int_cyl   / V_int_total
            C_bt    = C_total * V_int_bt    / V_int_total
        else:
            C_ogive = C_cyl = C_bt = 0.0
        # Base equivalent column convention (derivation section 3.3)
        C_base = C_cyl * (t_b / L_c) if L_c > 0 else 0.0

        # Zone wall thicknesses
        t_w_ogive = max(1e-4, r_o_mean_ogive - r_i_mean_ogive)
        t_w_cyl = t_w
        t_w_bt = max(1e-4, r_o_mean_bt - r_i_mean_bt)
        t_w_base = t_b

        # Zone break-up radii
        rbu_ogive = _r_bu_from_inner(r_i_mean_ogive, r_o_mean_ogive)
        rbu_cyl   = _r_bu_from_inner(D / 2.0 - t_w, D / 2.0)
        rbu_bt    = _r_bu_from_inner(r_i_mean_bt, r_o_mean_bt)
        # Base plate: appropriate driving radius is the outer minus base thickness
        rbu_base  = max(1e-3, D / 2.0 - t_b / 2.0)

        # Ogive spray angle: outward surface normal at axial midpoint
        x_m = L_n / 2.0
        # Outward normal in (x, r) is parallel to (x_m - xo_c, r_o(x_m) - ro_c)
        r_o_mid = ro_c + np.sqrt(max(0.0, R_o**2 - (x_m - xo_c) ** 2))
        dx_n = x_m - xo_c
        dr_n = r_o_mid - ro_c
        # angle of normal from +x (forward) axis
        spray_ogive = np.degrees(np.arctan2(dr_n, dx_n))
        spray_ogive = float(np.clip(spray_ogive, 60.0, 89.5))

        # Boattail spray = 90 + half-taper
        spray_bt = 90.0 + 0.5 * shell.boattail_angle_deg

    else:
        # ----------------- Tier-2 fraction fallback -----------------
        if shell.has_boattail:
            fr_ogive, fr_cyl, fr_bt, fr_base = 0.42, 0.36, 0.17, 0.05
        else:
            fr_ogive, fr_cyl, fr_bt, fr_base = 0.42, 0.53, 0.00, 0.05
        M_ogive = fr_ogive * M_steel
        M_cyl   = fr_cyl   * M_steel
        M_bt    = fr_bt    * M_steel
        M_base  = fr_base  * M_steel

        # Explosive allocation: proportional to steel mass (first-order)
        # (interior volume ~= proportional to steel mass for uniform wall designs)
        # Base receives equivalent-column allocation only.
        C_ogive = C_total * fr_ogive / (fr_ogive + fr_cyl + fr_bt) if (fr_ogive + fr_cyl + fr_bt) > 0 else 0.0
        C_cyl   = C_total * fr_cyl   / (fr_ogive + fr_cyl + fr_bt) if (fr_ogive + fr_cyl + fr_bt) > 0 else 0.0
        C_bt    = C_total * fr_bt    / (fr_ogive + fr_cyl + fr_bt) if (fr_ogive + fr_cyl + fr_bt) > 0 else 0.0
        C_base  = C_cyl * 0.10  # rough equivalent-column proxy (t_b/L_c ~ 0.1)

        # Zone wall-thickness scaling
        t_w_ogive = 0.75 * t_w
        t_w_cyl   = t_w
        t_w_bt    = 2.0  * t_w
        t_w_base  = 2.5  * t_w

        # Zone inner radii
        r_i_cyl = D / 2.0 - t_w
        r_i_ogive = 0.75 * r_i_cyl
        r_i_bt    = 0.75 * r_i_cyl
        rbu_cyl   = _r_bu_from_inner(r_i_cyl, D / 2.0)
        rbu_ogive = _r_bu_from_inner(r_i_ogive, r_i_ogive + t_w_ogive)
        rbu_bt    = _r_bu_from_inner(r_i_bt, r_i_bt + t_w_bt)
        rbu_base  = max(1e-3, D / 2.0 - t_w_base / 2.0)

        # Spray angles
        crh = shell.ogive_crh if shell.ogive_crh is not None else CRH_DEFAULT_TIER2
        if shell.ogive_len is not None:
            # Secant ogive: arc tangent at shoulder, length given explicitly.
            # Midpoint at ogive_len/2 from shoulder; correct for short arcs
            # where the full-tangent assumption (below) over-estimates forward spray.
            x_m = shell.ogive_len / 2.0
            R_o = crh * D
            spray_ogive = float(np.clip(
                np.degrees(np.arctan2(np.sqrt(max(0.0, R_o**2 - x_m**2)), x_m)),
                60.0, 89.5,
            ))
        else:
            # Full tangent ogive of this CRH — midpoint at sqrt(CRH-1/4)/2 calibers
            spray_ogive = 90.0 - np.degrees(
                np.arcsin(np.sqrt(crh - 0.25) / (2.0 * crh))
            )
        spray_bt = 90.0 + 0.5 * shell.boattail_angle_deg if shell.has_boattail else 90.0

    # -------------------- Per-zone V0 and mu --------------------
    V_g = shell.filler.gurney_const
    k_base = _base_k(shell)

    V0_ogive = _zone_gurney(M_ogive, C_ogive, V_g, k=1.0)
    V0_cyl   = _zone_gurney(M_cyl,   C_cyl,   V_g, k=1.0)
    V0_bt    = _zone_gurney(M_bt,    C_bt,    V_g, k=1.0) if M_bt > 0 else 0.0
    V0_base  = _zone_gurney(M_base,  max(C_base, 1e-9), V_g, k=k_base)

    mu_ogive = _zone_mott_mu(rbu_ogive, V0_ogive, shell.steel)
    mu_cyl   = _zone_mott_mu(rbu_cyl,   V0_cyl,   shell.steel)
    mu_bt    = _zone_mott_mu(rbu_bt,    V0_bt,    shell.steel) if M_bt > 0 else float("inf")
    mu_base  = _zone_mott_mu(rbu_base,  V0_base,  shell.steel)

    return ShellZones(
        ogive   =ZoneParams(M_ogive, C_ogive, V0_ogive, mu_ogive, spray_ogive, rbu_ogive, t_w_ogive),
        cylinder=ZoneParams(M_cyl,   C_cyl,   V0_cyl,   mu_cyl,   90.0,        rbu_cyl,   t_w_cyl),
        boattail=ZoneParams(M_bt,    C_bt,    V0_bt,    mu_bt,    spray_bt,    rbu_bt,    t_w_bt),
        base    =ZoneParams(M_base,  C_base,  V0_base,  mu_base,  165.0,       rbu_base,  t_w_base),
    )


def fragment_velocity(
    theta_z_deg: float, phi_rad: float, aof_deg: float
) -> tuple[float, float, float]:
    """Unit ground-frame velocity of a fragment leaving a zone [-, -, -].

    theta_z_deg : zone spray angle from forward axis [deg]
    phi_rad     : azimuth around the shell axis [rad]
    aof_deg     : angle of fall [deg] (0 = horizontal, 90 = vertical)

    Returns the unit direction ``(v_gx, v_gy, v_gz)`` in the ground frame,
    where +x is downrange, +y is cross-range and +z is up. This is the single
    source of the AoF-rotation formula (see burst-geometry spec,
    "fragment_ground_impact implements AoF rotation correctly"); both
    ``fragment_ground_impact`` and the app's spray-cone renderers source the
    ray direction from here rather than recomputing the trig.
    """
    th = np.radians(theta_z_deg)
    aof = np.radians(aof_deg)
    cT, sT = np.cos(th), np.sin(th)
    cA, sA = np.cos(aof), np.sin(aof)
    cP, sP = np.cos(phi_rad), np.sin(phi_rad)
    vgx = cA * cT + sA * sT * sP
    vgy = sT * cP
    vgz = -sA * cT + cA * sT * sP
    return (float(vgx), float(vgy), float(vgz))


def fragment_ground_impact(
    theta_z_deg: float, phi_rad: float, aof_deg: float, h_b: float
) -> tuple[float, float, float] | None:
    """Ground impact of a fragment leaving a zone with spray angle theta_z.

    theta_z_deg : zone spray angle from forward axis [deg]
    phi_rad     : azimuth around the shell axis [rad]
    aof_deg     : angle of fall [deg] (0 = horizontal, 90 = vertical)
    h_b         : burst height above ground [m]

    Returns ``(x_hit, y_hit, gamma_rad)`` [m, m, rad] or None if the
    fragment travels upward / horizontally (v_gz >= 0) and never reaches
    the ground in the straight-line model.
    """
    vgx, vgy, vgz = fragment_velocity(theta_z_deg, phi_rad, aof_deg)
    if vgz >= -1e-6:
        return None
    t = -h_b / vgz
    return (vgx * t, vgy * t, np.arcsin(min(1.0, abs(vgz))))


# ---------------------------------------------------------------------------
# Vectorised Family-A four-zone evaluation (spray-belt kernel with graded
# A_p(γ)/pk_given_hit). The per-cell integrand depends on the ground point only
# through the slant range s (belt membership aside): γ = arcsin(h_b/s), the drag
# attenuation V0·exp(−λ(m)·s) and the 1/(2π s² · 2 sinθ^z · δ) spreading factor
# are all functions of s. So the O(n_mass) mass integral is evaluated *exactly*
# (bit-for-bit as the per-cell trapezoid) on the in-belt cells in a single
# vectorised (n_belt, n_mass) reduction, chunked only to bound memory — not via
# an s-grid interpolation table (that variant was tried and reverted for a ~1e-3
# residual error; see updates/field-builder-performance/derivation.md §1).
# ---------------------------------------------------------------------------

_ZONE_NAMES = ("ogive", "cylinder", "boattail", "base")

# _FAMILY_A_CHUNK (cap on the (n_cells × n_mass) working array) is imported from
# fragmentation.py so the single-zone and four-zone builders share one knob.


def _familyA_zone_massintegral(
    z: ZoneParams,
    drag_lam_grid: np.ndarray,
    m_grid: np.ndarray,
    s: np.ndarray,
) -> np.ndarray:
    """J^z(s) = ∫ pdf^z(m)·pk_given_hit(½ m (V0^z e^{−λ(m)s})²) dm at each s [m].

    Exact vectorised mass integral of the Family-A kernel [count] over a 1-D
    array of slant ranges ``s``; the caller multiplies by the per-cell
    geometric/presented-area factor. Processed in chunks so the (len(s), M)
    working array never exceeds ``_FAMILY_A_CHUNK`` elements.
    """
    N0_z = z.mass_kg / (2.0 * z.mu)
    pdf_z = N0_z / (2.0 * np.sqrt(z.mu * m_grid)) * np.exp(-np.sqrt(m_grid / z.mu))
    n = s.shape[0]
    out = np.empty(n, dtype=float)
    chunk = max(1, _FAMILY_A_CHUNK // m_grid.shape[0])
    for a in range(0, n, chunk):
        s_c = s[a:a + chunk]
        v = z.V0_ms * np.exp(-drag_lam_grid[None, :] * s_c[:, None])
        E = 0.5 * m_grid[None, :] * v**2
        out[a:a + chunk] = np.trapezoid(pdf_z[None, :] * pk_given_hit(E), m_grid, axis=1)
    return out


def _four_zone_familyA_eval(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    posture: PostureParams,
    drag_lam_grid: np.ndarray,
    m_grid: np.ndarray,
    delta_deg: float,
    xg: np.ndarray,
    yg: np.ndarray,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Vectorised Family-A expected-lethal-hit count on ground points (xg, yg).

    ``xg, yg`` are 1-D arrays [m] of equal length (ground plane, z = 0).
    Returns ``(field_N, field_N_by_zone)`` matching the per-cell loops of
    ``_four_zone_field_split`` / ``four_zone_line_split`` (belt gate, graded
    A_p·pk kernel); the mass integral is evaluated exactly on the in-belt cells
    (bit-for-bit as the per-cell trapezoid), not interpolated in s.
    """
    xg = np.asarray(xg, dtype=float)
    yg = np.asarray(yg, dtype=float)
    field_N = np.zeros_like(xg)
    by_zone = {name: np.zeros_like(xg) for name in _ZONE_NAMES}

    aof = np.radians(aof_deg)
    cA, sA = np.cos(aof), np.sin(aof)
    delta = np.radians(delta_deg)
    sin_delta = np.sin(delta)

    s = np.sqrt(xg**2 + yg**2 + h_b**2)
    valid = s >= 1e-3
    if not np.any(valid):
        return field_N, by_zone
    # Belt polar cosine cosΘ = (x cosα + h_b sinα)/s (forward axis (cosα,0,−sinα),
    # ground point (x, y, −h_b)); guard the divide on the invalid (s→0) cells.
    s_safe = np.where(valid, s, 1.0)
    cos_Theta = (xg * cA + h_b * sA) / s_safe
    # Exact per-cell geometric + presented-area factor (shared across zones bar
    # the 1/sinθ^z scaling): A_p(arcsin h_b/s) / (2π s² · 2 δ).
    gamma = np.arcsin(np.clip(h_b / s_safe, -1.0, 1.0))
    geom = presented_area(gamma, posture) / (2.0 * np.pi * s_safe**2 * 2.0 * delta)

    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    for name, z in zone_list:
        if z.mass_kg <= 1e-6 or z.V0_ms <= 0.0 or not np.isfinite(z.mu):
            continue
        theta_z = np.radians(z.spray_deg)
        if np.sin(aof + theta_z) <= 0.0:
            continue
        mask = valid & (np.abs(cos_Theta - np.cos(theta_z)) <= sin_delta)
        idx = np.nonzero(mask)[0]
        if idx.size == 0:
            continue
        # Exact mass integral only on in-belt cells; scatter back.
        J = _familyA_zone_massintegral(z, drag_lam_grid, m_grid, s[idx])
        val = np.zeros_like(xg)
        val[idx] = J * geom[idx] / np.sin(theta_z)
        field_N += val
        by_zone[name] = val
    return field_N, by_zone


def _four_zone_field_split(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    posture: PostureParams,
    drag_lam_grid: np.ndarray,
    m_grid: np.ndarray,
    max_r: float = 80.0,
    n_grid: int = 60,
    delta_deg: float = 15.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    """Like four_zone_field but also returns per-zone P(kill) grids.

    Returns ``(X, Y, pk_total, pk_by_zone)`` where ``pk_by_zone`` is a dict
    keyed by zone name ("ogive", "cylinder", "boattail", "base").

    ``pk_total`` is identical to what ``four_zone_field`` returns; the two
    functions share the same loop body so pk_total == 1 - exp(-sum(field_N_z))
    exactly.
    """
    xy = np.linspace(-max_r, max_r, n_grid)
    X, Y = np.meshgrid(xy, xy)

    field_N_flat, by_zone_flat = _four_zone_familyA_eval(
        zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, delta_deg,
        X.ravel(), Y.ravel(),
    )
    field_N = field_N_flat.reshape(X.shape)
    field_N_by_zone = {name: by_zone_flat[name].reshape(X.shape)
                       for name in _ZONE_NAMES}

    pk_total = 1.0 - np.exp(-field_N)
    pk_by_zone = {name: 1.0 - np.exp(-field_N_by_zone[name]) for name in _ZONE_NAMES}
    return X, Y, pk_total, pk_by_zone


def four_zone_line_split(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    posture: PostureParams,
    drag_lam_grid: np.ndarray,
    m_grid: np.ndarray,
    *,
    fixed_axis: str,
    fixed_coord: float,
    line_coords: np.ndarray,
    delta_deg: float = 15.0,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Per-zone + total P(kill) along a single fixed-x or fixed-y ground line.

    Evaluates the *same* governing physics as ``_four_zone_field_split`` —
    the spray-belt acceptance test, presented area A_p(gamma), drag
    attenuation and Mott mass integration — but only at the ground points of
    one 1D line, so its cost scales with ``len(line_coords)`` rather than
    ``n_grid**2``. This lets a caller sample a slice at much finer spatial
    resolution than the global square grid without paying the O(n_grid^2)
    cost of tightening that grid everywhere. (At low burst height the
    equatorial spray footprint along a slice can be narrower than the coarse
    grid step, so a row/column read off the square grid can miss the real
    non-zero band; sampling this line finely recovers it.)

    zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, delta_deg
        Identical meaning to ``four_zone_field`` / ``_four_zone_field_split``.
    fixed_axis  : "x" (fix downrange, sweep cross-range y) or
                  "y" (fix cross-range, sweep downrange x).
    fixed_coord : value [m] of the held axis.
    line_coords : 1D array [m] of the swept-axis coordinates to evaluate.

    Returns ``(pk_total, pk_by_zone)`` where each is sampled at
    ``line_coords``: ``pk_total`` is a 1D array and ``pk_by_zone`` is a dict
    keyed by zone name. For any ``line_coords`` point and ``fixed_coord`` that
    coincide with the square-grid nodes used by ``_four_zone_field_split``,
    the returned values match that grid exactly (same formula, evaluated
    off the square-mesh constraint).
    """
    if fixed_axis not in ("x", "y"):
        raise ValueError("fixed_axis must be 'x' or 'y'")
    line_coords = np.asarray(line_coords, dtype=float)
    n_line = line_coords.shape[0]

    # Ground-point coordinates along the line. The square grid uses
    # X = xy (downrange, columns) and Y = xy (cross-range, rows); a fixed-x
    # slice holds X and sweeps Y, a fixed-y slice holds Y and sweeps X — so
    # the (xg, yg) assignment below reproduces those grid nodes exactly.
    if fixed_axis == "x":
        xg_arr = np.full(n_line, fixed_coord)
        yg_arr = line_coords
    else:
        xg_arr = line_coords
        yg_arr = np.full(n_line, fixed_coord)

    field_N, field_N_by_zone = _four_zone_familyA_eval(
        zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, delta_deg,
        xg_arr, yg_arr,
    )

    pk_total = 1.0 - np.exp(-field_N)
    pk_by_zone = {name: 1.0 - np.exp(-field_N_by_zone[name]) for name in _ZONE_NAMES}
    return pk_total, pk_by_zone


def four_zone_field(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    posture: PostureParams,
    drag_lam_grid: np.ndarray,
    m_grid: np.ndarray,
    max_r: float = 80.0,
    n_grid: int = 60,
    delta_deg: float = 15.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Four-zone P(kill) field on a (n_grid x n_grid) ground patch.

    zones         : decomposed ShellZones
    aof_deg       : angle of fall [deg]
    h_b           : burst height [m]
    posture       : PostureParams
    drag_lam_grid : retardation coeff lambda [1/m] on m_grid
    m_grid        : fragment-mass grid [kg]
    max_r         : half-extent of the square ground patch [m]
    n_grid        : grid resolution per axis
    delta_deg     : spray-belt half-width delta [deg]

    Each zone contributes its own (theta^z, mu^z, V0^z, N0^z); the per-zone
    geometry factor uses g_new = Ap(gamma) / (2*pi*s^2 * 2 sin(theta^z) * delta)
    and the spray-belt acceptance test is |Theta_burst - theta^z| <= delta
    where Theta_burst is the polar angle from the shell axis to the ground
    point, given AoF. Fragments with v_gz >= 0 contribute zero.

    Returns ``(X, Y, P_kill)`` meshgrids [m, m, -].
    """
    xy = np.linspace(-max_r, max_r, n_grid)
    X, Y = np.meshgrid(xy, xy)

    field_N_flat, _ = _four_zone_familyA_eval(
        zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, delta_deg,
        X.ravel(), Y.ravel(),
    )
    field_N = field_N_flat.reshape(X.shape)
    return X, Y, 1.0 - np.exp(-field_N)


# ---------------------------------------------------------------------------
# Four-zone lethal-fragment areal density ρ_L(x, y, z) — target-independent
#   (derivation: updates/lethal-fragment-density-field/derivation.md)
# ---------------------------------------------------------------------------


def lethal_density_four_zone_point(
    zones: ShellZones,
    x: float,
    y: float,
    z: float,
    aof_deg: float,
    h_b: float,
    delta_deg: float,
    s_grids: dict[str, np.ndarray],
    mmin_grids: dict[str, np.ndarray],
) -> float:
    """Four-zone lethal-fragment areal density ρ_L [m⁻²] at (x, y, z) [m].

    Sums eq. (3) of the derivation over the four zones: each zone uses its own
    spray angle θ^z, Mott half-mass μ^z and count N0^z, the belt-acceptance
    test ``|cosΘ − cosθ^z| ≤ sinδ`` on the forward axis (+cosα, 0, −sinα), and
    its own precomputed m_min(s) table (distinct V0^z). The two target-coupled
    factors (A_p, graded pk) are divided out. Returns 0 outside every belt or
    for δ ≤ 0.

    zones      : decomposed ShellZones
    x, y, z    : field-point coordinates [m]; z is height above ground
    aof_deg    : angle of fall [deg]
    h_b        : burst height above ground [m]
    delta_deg  : spray-belt half-width δ [deg]
    s_grids    : per-zone slant-range grid [m], keyed by zone name; each grid
                 MUST cover the full range of slant ranges this point can
                 produce — np.interp below silently clips (does not
                 error/extrapolate) for s outside [s_grid[0], s_grid[-1]], so an
                 undersized grid biases m_min with no warning. The field-builder
                 callers size the grids from the same z they query; a direct
                 caller must ensure the same coverage.
    mmin_grids : per-zone m_min(s) table [kg], keyed by zone name
    """
    delta = np.radians(delta_deg)
    if delta <= 0.0:
        return 0.0

    s = np.sqrt(x**2 + y**2 + (z - h_b) ** 2)
    if s < 1e-6:
        return 0.0

    alpha_rad = np.radians(aof_deg)
    e_axis = _forward_shell_axis(alpha_rad)
    r_hat = np.array([x, y, z - h_b]) / s
    cos_Theta = float(np.dot(r_hat, e_axis))

    rho = 0.0
    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    for name, zp in zone_list:
        if zp.mass_kg <= 1e-6 or zp.V0_ms <= 0.0 or not np.isfinite(zp.mu):
            continue
        theta_z = np.radians(zp.spray_deg)
        if abs(cos_Theta - np.cos(theta_z)) > np.sin(delta):
            continue
        sin_theta_z = np.sin(theta_z)
        if sin_theta_z < 1e-9:
            continue
        N0_z = zp.mass_kg / (2.0 * zp.mu)
        # np.interp silently clips outside the grid; assert (debug-mode only,
        # off under python -O) that s is in range so an undersized
        # caller-supplied grid surfaces loudly instead of biasing m_min.
        sg = s_grids[name]
        assert sg[0] <= s <= sg[-1], (
            f"s={s:.4g} m outside {name} m_min grid [{sg[0]:.4g}, {sg[-1]:.4g}] m; "
            "np.interp would silently clip"
        )
        m_min = float(np.interp(s, sg, mmin_grids[name]))
        N_leth = N0_z * np.exp(-np.sqrt(m_min / zp.mu))
        g = 1.0 / (2.0 * np.pi * s**2 * 2.0 * sin_theta_z * delta)
        rho += g * N_leth

    return float(rho)


def build_zone_mmin_tables(
    zones: ShellZones,
    s_grid: np.ndarray,
    E_leth: float,
    drag: DragParams,
    rho_steel: float,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Per-zone (s_grid, m_min(s)) tables [m, kg] for the four-zone ρ_L field.

    Each zone has a distinct V0^z, hence a distinct m_min(s); all share the
    same s_grid. Zones with no steel / no velocity get an all-``m_hi`` table
    (their N_leth → 0). Returns ``(s_grids, mmin_grids)`` dicts keyed by zone
    name, each compatible with ``lethal_density_four_zone_point``.
    """
    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    s_grids: dict[str, np.ndarray] = {}
    mmin_grids: dict[str, np.ndarray] = {}
    for name, zp in zone_list:
        s_grids[name] = s_grid
        if zp.mass_kg <= 1e-6 or zp.V0_ms <= 0.0 or not np.isfinite(zp.mu):
            mmin_grids[name] = np.full_like(s_grid, 2.0)
            continue
        mmin_grids[name] = build_mmin_table(s_grid, zp.V0_ms, E_leth, drag, rho_steel)
    return s_grids, mmin_grids


def _four_zone_density_layer_vec(
    zones: ShellZones,
    X: np.ndarray,
    Y: np.ndarray,
    z: float,
    aof_deg: float,
    h_b: float,
    delta_deg: float,
    s_grids: dict[str, np.ndarray],
    mmin_grids: dict[str, np.ndarray],
) -> np.ndarray:
    """Vectorised four-zone ρ_L [m⁻²] on an (x, y) layer at height ``z`` [m].

    Bit-identical to a per-cell loop over :func:`lethal_density_four_zone_point`
    (same per-zone m_min tables, same belt gate) evaluated as array ops.
    ``X, Y`` are 2-D meshgrids [m]; returns ρ_L on the same shape.
    """
    rho = np.zeros_like(X)
    delta = np.radians(delta_deg)
    if delta <= 0.0:
        return rho
    alpha_rad = np.radians(aof_deg)
    e_axis = _forward_shell_axis(alpha_rad)
    s = np.sqrt(X**2 + Y**2 + (z - h_b) ** 2)
    valid = s >= 1e-6
    s_safe = np.where(valid, s, 1.0)
    cos_Theta = (X * e_axis[0] + (z - h_b) * e_axis[2]) / s_safe
    sin_delta = np.sin(delta)
    # Vectorised parity with the scalar reference (lethal_density_four_zone_point
    # asserts s_grid[0] <= s <= s_grid[-1]): np.interp silently clips out-of-grid
    # queries, so a coverage regression in slant_range_grid would go unnoticed
    # here. One cheap min/max guard over the query set catches it loudly instead
    # (s_safe sentinels invalid cells at 1.0, always inside the grid).
    q_lo, q_hi = float(s_safe.min()), float(s_safe.max())

    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    for name, zp in zone_list:
        if zp.mass_kg <= 1e-6 or zp.V0_ms <= 0.0 or not np.isfinite(zp.mu):
            continue
        theta_z = np.radians(zp.spray_deg)
        sin_theta_z = np.sin(theta_z)
        if sin_theta_z < 1e-9:
            continue
        sg = s_grids[name]
        assert q_lo >= sg[0] and q_hi <= sg[-1], (
            f"slant range [{q_lo:.4g}, {q_hi:.4g}] m outside m_min grid "
            f"[{sg[0]:.4g}, {sg[-1]:.4g}] m for zone {name}; np.interp would clip"
        )
        mask = valid & (np.abs(cos_Theta - np.cos(theta_z)) <= sin_delta)
        N0_z = zp.mass_kg / (2.0 * zp.mu)
        m_min = np.interp(s_safe, s_grids[name], mmin_grids[name])
        N_leth = N0_z * np.exp(-np.sqrt(m_min / zp.mu))
        g = 1.0 / (2.0 * np.pi * s_safe**2 * 2.0 * sin_theta_z * delta)
        rho = rho + np.where(mask, g * N_leth, 0.0)
    return rho


def four_zone_lethal_density_field(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    drag: DragParams,
    rho_steel: float,
    z: float = 0.0,
    max_r: float = 80.0,
    n_grid: int = 60,
    delta_deg: float = 15.0,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Four-zone lethal-density field ρ_L [m⁻²] on an (x, y) patch at height z.

    Evaluates eq. (3) summed over zones at fixed height ``z`` [m] above ground
    over a square (x, y) grid, using per-zone precomputed m_min(s) tables (§6).

    zones     : decomposed ShellZones
    aof_deg   : angle of fall [deg]
    h_b       : burst height above ground [m]
    drag      : DragParams (for the m_min tables)
    rho_steel : steel density [kg/m³]
    z         : field-point height above ground [m]
    max_r     : half-extent of the (x, y) box [m]
    n_grid    : grid resolution per axis
    delta_deg : spray-belt half-width δ [deg]
    E_leth    : binary lethal kinetic-energy threshold [J]
    n_s       : m_min table resolution

    Returns ``(X, Y, rho_L)`` meshgrids [m, m, m⁻²].
    """
    # This field is a single height layer (z fixed): the box spans z in [z, z],
    # so pass z as both z_max and z_min (matching the single-zone builder).
    # The earlier max(z, h_b) call collapsed the vertical offset to zero for
    # layers below the burst, so s_max under-covered the box corners (whose
    # slant range includes |z - h_b|) and tripped the np.interp range assertion
    # at the top of the grid; using the true layer height fixes both bounds.
    s_grid = slant_range_grid(max_r, h_b, z, n_s=n_s, z_min=z)
    s_grids, mmin_grids = build_zone_mmin_tables(
        zones, s_grid, E_leth, drag, rho_steel
    )

    xy = np.linspace(-max_r, max_r, n_grid)
    X, Y = np.meshgrid(xy, xy)
    rho_L = _four_zone_density_layer_vec(
        zones, X, Y, z, aof_deg, h_b, delta_deg, s_grids, mmin_grids,
    )
    return X, Y, rho_L


def four_zone_lethal_density_volume(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    drag: DragParams,
    rho_steel: float,
    z_max: float = 10.0,
    max_r: float = 80.0,
    n_grid: int = 30,
    n_z: int = 20,
    delta_deg: float = 15.0,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Four-zone lethal-density volume ρ_L [m⁻²] on an (x, y, z) grid.

    No new physics: evaluates :func:`four_zone_lethal_density_field` once per
    z-layer over ``n_z`` heights from 0 to ``z_max`` [m] and stacks the per-layer
    (X, Y, rho_L) outputs into 3D arrays. The z=0 layer is numerically identical
    to ``four_zone_lethal_density_field(z=0.0)`` for matching parameters.

    zones     : decomposed ShellZones
    aof_deg   : angle of fall [deg]
    h_b       : burst height above ground [m]
    drag      : DragParams (for the m_min tables)
    rho_steel : steel density [kg/m³]
    z_max     : top of the z-extent [m] (bottom is the ground, z=0)
    max_r     : half-extent of the (x, y) box [m]
    n_grid    : grid resolution per x/y axis
    n_z       : number of z-layers
    delta_deg : spray-belt half-width δ [deg]
    E_leth    : binary lethal kinetic-energy threshold [J]
    n_s       : m_min table resolution

    Returns ``(X, Y, Z, rho_L)`` 3D meshgrids [m, m, m, m⁻²], indexed (iz, ix, iy).
    """
    z_layers = np.linspace(0.0, z_max, n_z)
    X2d: np.ndarray | None = None
    Y2d: np.ndarray | None = None
    layers: list[np.ndarray] = []
    for z in z_layers:
        X2d, Y2d, rho_L_layer = four_zone_lethal_density_field(
            zones, aof_deg, h_b, drag, rho_steel, z=float(z),
            max_r=max_r, n_grid=n_grid, delta_deg=delta_deg,
            E_leth=E_leth, n_s=n_s,
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


def _active_zone_cos_theta(zones: ShellZones) -> list[float]:
    """cos θ^z [-] of every zone that can contribute lethal fragments.

    A belt's membership can flip at cosΘ = cosθ^z ± sinδ, so these centres seed
    the column-integral breakpoints (:func:`belt_column_breakpoints`). Zones with
    no steel / no velocity / degenerate spray are skipped (they add nothing to
    ρ_L, so their belt edges are irrelevant).
    """
    zone_list = [zones.ogive, zones.cylinder, zones.boattail, zones.base]
    cos_list: list[float] = []
    for zp in zone_list:
        if zp.mass_kg <= 1e-6 or zp.V0_ms <= 0.0 or not np.isfinite(zp.mu):
            continue
        theta_z = np.radians(zp.spray_deg)
        if np.sin(theta_z) < 1e-9:
            continue
        cos_list.append(float(np.cos(theta_z)))
    return cos_list


def _active_zone_specs(
    zones: ShellZones,
    s_grids: dict[str, np.ndarray],
    mmin_grids: dict[str, np.ndarray],
) -> tuple[list[dict], list[float]]:
    """Belt specs + centre cosines for the active zones (for _pkill_columns_vec).

    Selects exactly the zones :func:`lethal_density_four_zone_point` would sum
    (steel/velocity/finite-μ and sinθ^z ≥ 1e-9), returning one spec dict per
    active zone (``cos_tz, sin_tz, N0, mu, s_grid, mmin``) and the matching list
    of belt-centre cosines for the breakpoint solver.
    """
    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    specs: list[dict] = []
    cos_tz: list[float] = []
    for name, zp in zone_list:
        if zp.mass_kg <= 1e-6 or zp.V0_ms <= 0.0 or not np.isfinite(zp.mu):
            continue
        theta_z = np.radians(zp.spray_deg)
        sin_tz = float(np.sin(theta_z))
        if sin_tz < 1e-9:
            continue
        c = float(np.cos(theta_z))
        specs.append({
            "cos_tz": c, "sin_tz": sin_tz,
            "N0": zp.mass_kg / (2.0 * zp.mu), "mu": zp.mu,
            "s_grid": s_grids[name], "mmin": mmin_grids[name],
        })
        cos_tz.append(c)
    return specs, cos_tz


def four_zone_pkill_field(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    drag: DragParams,
    rho_steel: float,
    posture: PostureParams = STANDING,
    max_r: float = 80.0,
    n_grid: int = 60,
    delta_deg: float = 15.0,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
    n_seg: int = 9,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Four-zone ground kill probability P_k [-] ∈ [0,1] for a target at (x, y).

    P_k = 1 − exp(−λ), with the mean lethal-hit count formed by integrating the
    four-zone lethal-fragment areal density ρ_L [m⁻²] over the vertical column
    the target actually occupies (target-height-intercept derivation eq. 2/3/6):

        λ(x,y) = w_perp · ∫₀ʰ ρ_L(x,y,z) dz,

    reading (w_perp, h) live from ``posture``. This replaces the earlier
    ρ_L(z=0)·A_ref point transform, which read the flux only on the ground plane
    and reported a false safe ring wherever a near-horizontal spray belt crosses
    chest/head height but never descends to z=0 close in (derivation §1, §6.3).
    The old transform is the degenerate z-flat limit with A_ref = w_perp·h (§3),
    and posture re-couples automatically through (w_perp, h) (§4).

    The column integral is evaluated piecewise on the belt-membership segments
    (each zone's belt edge, seeded by the active zones' cosθ^z) with a
    composite-midpoint rule — strictly-interior nodes so no belt-edge 0/1 gate
    coin-flips (derivation §5) — vectorised over all (x, y) columns at once by
    :func:`arty.fragmentation._pkill_columns_vec` (breakpoints via
    ``_belt_breakpoints_vec``). The scalar per-cell reference this reproduces
    (:func:`arty.fragmentation.belt_column_breakpoints` +
    ``integrate_column_density``) is retained unchanged as the equivalence
    baseline for the regression harness and property tests. Per-zone m_min(s)
    tables spanning the whole [0, h] column are built once and shared across all
    z-samples (§5.3).

    Caveats (derivation §2/§7, A1/A2): frontal projection (γ = 0 arrival),
    Poisson independence / no shielding, and a sharp E_leth cut with
    P_k|hit = 1 once counted — more pessimistic than the ES-310 aggregate, not a
    tissue-level wound model.

    Returns ``(X, Y, P_k)`` meshgrids [m, m, -].
    """
    h = posture.h
    w_perp = posture.w_perp
    alpha_rad = np.radians(aof_deg)
    delta_rad = np.radians(delta_deg)

    # One (s_grid, per-zone m_min) covering the whole [0, h] column, shared
    # across every (x, y) column and z-sample (§5.3).
    s_grid = slant_range_grid(max_r, h_b, z_max=h, n_s=n_s, z_min=0.0)
    s_grids, mmin_grids = build_zone_mmin_tables(
        zones, s_grid, E_leth, drag, rho_steel
    )
    specs, cos_theta_z = _active_zone_specs(zones, s_grids, mmin_grids)

    xy = np.linspace(-max_r, max_r, n_grid)
    X, Y = np.meshgrid(xy, xy)
    P_k = _pkill_columns_vec(
        X.ravel(), Y.ravel(), h_b, alpha_rad, delta_rad, w_perp, 0.0, h,
        n_seg, specs, cos_theta_z,
    ).reshape(X.shape)
    assert np.all((P_k >= 0.0) & (P_k <= 1.0)), "P_k outside [0,1]"
    return X, Y, P_k


def four_zone_pkill_line(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    drag: DragParams,
    rho_steel: float,
    posture: PostureParams,
    *,
    fixed_axis: str,
    fixed_coord: float,
    line_coords: np.ndarray,
    delta_deg: float = 15.0,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
    n_seg: int = 9,
) -> np.ndarray:
    """Four-zone ground kill probability P_k [-] along a single fixed-x/-y line.

    Family-B line variant of :func:`four_zone_pkill_field`: the *same* vertical
    column-integral physics (λ = w_perp·∫₀ʰ ρ_L dz, eq. 2/6), evaluated only at
    the ground points of one 1D line so cost scales with ``len(line_coords)``
    rather than ``n_grid²``. This lets a caller sample a cross-section at much
    finer spatial resolution than the square grid — the false-safe-ring band can
    be narrower than a coarse grid step, so a row read off the square grid can
    miss it (derivation §5). For any ``line_coords``/``fixed_coord`` point that
    coincides with a square-grid node, the returned P_k matches
    :func:`four_zone_pkill_field` exactly (same integrand).

    This is the ρ_L column-integral (Family-B) path; it is distinct from
    :func:`four_zone_line_split`, the graded A_p(γ)/pk_given_hit (Family-A) line
    used by the app's per-zone cross-section — do not conflate them (derivation
    §5).

    fixed_axis  : "x" (fix downrange, sweep cross-range y) or
                  "y" (fix cross-range, sweep downrange x).
    fixed_coord : value [m] of the held axis.
    line_coords : 1D array [m] of the swept-axis coordinates to evaluate.

    Returns ``pk_total`` [-], a 1D array over ``line_coords``.
    """
    if fixed_axis not in ("x", "y"):
        raise ValueError("fixed_axis must be 'x' or 'y'")
    line_coords = np.asarray(line_coords, dtype=float)
    n_line = line_coords.shape[0]

    h = posture.h
    w_perp = posture.w_perp
    alpha_rad = np.radians(aof_deg)
    delta_rad = np.radians(delta_deg)

    if fixed_axis == "x":
        xg_arr = np.full(n_line, fixed_coord)
        yg_arr = line_coords
    else:
        xg_arr = line_coords
        yg_arr = np.full(n_line, fixed_coord)

    # m_min table spans the whole [0, h] column; the (x, y) reach of the line
    # sets the max slant range, so size s_grid from the line's own extent.
    max_r = float(max(np.max(np.abs(xg_arr)), np.max(np.abs(yg_arr)), 1.0))
    s_grid = slant_range_grid(max_r, h_b, z_max=h, n_s=n_s, z_min=0.0)
    s_grids, mmin_grids = build_zone_mmin_tables(
        zones, s_grid, E_leth, drag, rho_steel
    )
    specs, cos_theta_z = _active_zone_specs(zones, s_grids, mmin_grids)

    pk = _pkill_columns_vec(
        xg_arr, yg_arr, h_b, alpha_rad, delta_rad, w_perp, 0.0, h,
        n_seg, specs, cos_theta_z,
    )
    return pk


def four_zone_pkill_volume(
    zones: ShellZones,
    aof_deg: float,
    h_b: float,
    drag: DragParams,
    rho_steel: float,
    z_max: float = 10.0,
    max_r: float = 80.0,
    n_grid: int = 30,
    n_z: int = 20,
    delta_deg: float = 15.0,
    E_leth: float = E_LETH_DEFAULT,
    n_s: int = 400,
    A_ref: float = A_REF_DEFAULT,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Four-zone point kill probability P_k [-] ∈ [0,1] on an (x, y, z) grid.

    P_k = 1 − exp(−ρ_L·A_ref), with ρ_L [m⁻²] from
    :func:`four_zone_lethal_density_volume` and A_ref [m²] the fixed nominal
    personnel presented area (0.85 m², standing frontal — lower bound; +10–25%
    with kit). A pure elementwise transform of ρ_L; no new physics
    (pkill-poisson-field derivation eq. 1, §6). This volume builder is the
    point-in-space diagnostic — "one person standing at exactly this height z" —
    and deliberately keeps the frozen A_ref (target-height-intercept derivation
    §8); the ground field :func:`four_zone_pkill_field` instead integrates the
    ρ_L flux over the target's whole [0, h] column.

    Caveats (derivation §2, A1/A2): Poisson independence / no shielding; sharp
    E_leth threshold with P_k|hit = 1 once counted — more pessimistic than the
    ES-310 aggregate, not a tissue-level wound model.

    Returns ``(X, Y, Z, P_k)`` 3D meshgrids [m, m, m, -], indexed (iz, ix, iy).
    """
    X, Y, Z, rho_L = four_zone_lethal_density_volume(
        zones, aof_deg, h_b, drag, rho_steel, z_max=z_max,
        max_r=max_r, n_grid=n_grid, n_z=n_z, delta_deg=delta_deg,
        E_leth=E_leth, n_s=n_s,
    )
    P_k = 1.0 - np.exp(-rho_L * A_ref)
    assert np.all((P_k >= 0.0) & (P_k <= 1.0)), "P_k outside [0,1]"
    return X, Y, Z, P_k
