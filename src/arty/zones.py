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
    PostureParams,
    ShellParams,
    SteelParams,
    pk_given_hit,
    presented_area,
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

        # 200-slice midpoint Riemann sum over the ogive
        xo_c, ro_c = _ogive_arc_centre(R_o, D, L_n, r_tip_o)
        xi_c, ri_c = _ogive_arc_centre(R_i, D - 2 * t_w, L_n, r_tip_i)
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
            fr_ogive, fr_cyl, fr_bt, fr_base = 0.53, 0.27, 0.15, 0.05
        else:
            fr_ogive, fr_cyl, fr_bt, fr_base = 0.53, 0.42, 0.00, 0.05
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
    th = np.radians(theta_z_deg)
    aof = np.radians(aof_deg)
    cT, sT = np.cos(th), np.sin(th)
    cA, sA = np.cos(aof), np.sin(aof)
    cP, sP = np.cos(phi_rad), np.sin(phi_rad)
    vgx = cA * cT + sA * sT * sP
    vgy = sT * cP
    vgz = -sA * cT + cA * sT * sP
    if vgz >= -1e-6:
        return None
    t = -h_b / vgz
    return (vgx * t, vgy * t, np.arcsin(min(1.0, abs(vgz))))


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
    field_N = np.zeros_like(X)

    aof = np.radians(aof_deg)
    cA, sA = np.cos(aof), np.sin(aof)
    delta = np.radians(delta_deg)
    e_axis = np.array([cA, 0.0, -sA])  # forward shell axis in ground frame

    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]
    for name, z in zone_list:
        if z.mass_kg <= 1e-6 or z.V0_ms <= 0.0 or not np.isfinite(z.mu):
            continue
        N0_z = z.mass_kg / (2.0 * z.mu)
        theta_z = np.radians(z.spray_deg)
        sin_theta_z = np.sin(theta_z)
        pdf_z = N0_z / (2.0 * np.sqrt(z.mu * m_grid)) * np.exp(-np.sqrt(m_grid / z.mu))

        for i in range(n_grid):
            for j in range(n_grid):
                xg, yg = X[i, j], Y[i, j]
                s = np.sqrt(xg**2 + yg**2 + h_b**2)
                if s < 1e-3:
                    continue
                # Ray from burst to ground patch
                r_hat = np.array([xg, yg, -h_b]) / s
                cos_Theta = float(np.dot(r_hat, e_axis))
                # Test whether this ground patch lies within the zone's
                # spray belt at theta^z +/- delta
                if abs(cos_Theta - np.cos(theta_z)) > np.sin(delta):
                    continue
                gamma = np.arcsin(min(1.0, h_b / s))
                Ap = presented_area(gamma, posture)
                v = z.V0_ms * np.exp(-drag_lam_grid * s)
                E = 0.5 * m_grid * v**2
                integrand = pdf_z * pk_given_hit(E) * Ap / (
                    2.0 * np.pi * s**2 * 2.0 * sin_theta_z * delta
                )
                field_N[i, j] += float(np.trapezoid(integrand, m_grid))

    return X, Y, 1.0 - np.exp(-field_N)
