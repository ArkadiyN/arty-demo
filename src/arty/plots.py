"""Presentation-layer plotting for the fragmentation-field model.

Every function takes already-computed physics quantities (params + results)
and returns a matplotlib ``Figure``. No physics is computed here beyond
trivial re-evaluation of model functions already defined in
``arty.fragmentation`` / ``arty.zones`` for plotting grids.

Units: masses passed in kg unless a parameter name ends in ``_g``; ranges
in metres; energies in joules.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from arty.fragmentation import (
    DragParams,
    _PK_E,
    _PK_VAL,
    ke_at_range,
    mott_N,
    retardation_coeff,
)
from arty.zones import ShellZones, fragment_ground_impact


def apply_style() -> None:
    """Apply the notebook's standard matplotlib rcParams."""
    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.35})


def fig_mott_distribution(N0: float, mu: float) -> plt.Figure:
    """Figure 1 — Mott cumulative count and mass PDF.

    N0 : total fragment count [-]
    mu : Mott half-weight [kg]
    """
    m_range = np.logspace(-4, -1, 400)
    N_cumul = mott_N(m_range, N0, mu)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = axes[0]
    ax.loglog(m_range * 1e3, N_cumul)
    ax.axvline(mu * 1e3, color="C1", ls="--", label=f"μ = {mu*1e3:.1f} g (half-weight)")
    ax.axvline(mu / 4 * 1e3, color="C2", ls=":", label=f"μ/4 = {mu/4*1e3:.2f} g (mode)")
    ax.set_xlabel("Fragment mass [g]")
    ax.set_ylabel("N(≥m)")
    ax.legend(fontsize=8)
    ax.set_title("Cumulative Count (Mott 1947)")

    ax = axes[1]
    pdf_vals = -np.diff(N_cumul) / np.diff(m_range)
    ax.semilogx(m_range[:-1] * 1e3, pdf_vals)
    ax.axvline(mu / 4 * 1e3, color="C2", ls=":", label=f"mode = {mu/4*1e3:.2f} g")
    ax.set_xlabel("Fragment mass [g]")
    ax.set_ylabel("dN/dm [frags/g]")
    ax.legend(fontsize=8)
    ax.set_title("Mass PDF")

    fig.suptitle(
        f"105 mm M1 HE — Fragment Distribution  (N₀={N0:.0f}, μ={mu*1e3:.1f} g)",
        y=1.01,
    )
    fig.tight_layout()
    return fig


def fig_ke_vs_range(
    V0: float,
    drag: DragParams,
    rho_steel: float,
    rep_masses_g: list[float] | None = None,
    s_max: float = 300.0,
) -> plt.Figure:
    """Figure 2 — fragment kinetic energy vs distance from burst.

    V0        : initial fragment velocity [m/s]
    drag      : DragParams
    rho_steel : steel density [kg/m³]
    """
    if rep_masses_g is None:
        rep_masses_g = [0.5, 1, 5, 10, 25, 50]
    s_range = np.linspace(0, s_max, 500)

    fig, ax = plt.subplots(figsize=(8, 5))
    for mg in rep_masses_g:
        mk = mg * 1e-3
        lam = retardation_coeff(np.array([mk]), drag, rho_steel)[0]
        ax.plot(
            s_range,
            ke_at_range(np.array([mk]), V0, np.array([lam]), s_range),
            label=f"{mg} g",
        )
    for e_j, pk_v, col in zip(_PK_E, _PK_VAL, ["gold", "orange", "red"]):
        ax.axhline(
            e_j, color=col, ls="--", lw=1.2,
            label=f"ES-310: {e_j/1e3 if e_j>=1000 else e_j:.0f}{'kJ' if e_j>=1000 else 'J'} → Pk={pk_v}",
        )
    ax.set_yscale("log")
    ax.set_xlabel("Distance from burst s [m]")
    ax.set_ylabel("Kinetic energy [J]")
    ax.set_title("Fragment KE vs. Distance from Burst — 105 mm M1")
    ax.legend(title="Fragment mass", fontsize=8)
    fig.tight_layout()
    return fig


def fig_frag_field(
    r_vals: np.ndarray,
    N_eff: np.ndarray,
    P: np.ndarray,
    R50: float,
    N0: float,
    V0: float,
    mu: float,
) -> plt.Figure:
    """Figure 3 — expected lethal hits and P(kill) vs range.

    r_vals : range grid [m]
    N_eff  : expected lethal-hit count at each range [-]
    P      : P(kill) at each range [-]
    R50    : range where P(kill) = 0.5 [m]
    """
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].semilogy(r_vals, N_eff)
    axes[0].set_xlabel("Range r [m]")
    axes[0].set_ylabel("Expected lethal hits N_eff")
    axes[0].set_title("Expected Lethal Hits vs. Range (ES-310 Pk|hit)")

    axes[1].plot(r_vals, P * 100)
    axes[1].axhline(50, color="C1", ls="--", lw=1.2, label=f"R₅₀ = {R50:.0f} m")
    axes[1].set_xlabel("Range r [m]")
    axes[1].set_ylabel("P(kill) [%]")
    axes[1].set_title("Kill Probability — Standing Person (ES-310)")
    axes[1].legend(fontsize=8)
    axes[1].set_ylim(0, 100)

    fig.suptitle(
        f"105 mm M1 HE Ground Burst — Fragmentation Field\n"
        f"N₀={N0:.0f}, V₀={V0:.0f} m/s, μ={mu*1e3:.1f} g, R₅₀={R50:.0f} m",
        y=1.02,
    )
    fig.tight_layout()
    return fig


def fig_cross_section(h_pers: float = 1.7) -> plt.Figure:
    """Figure 4 — vertical cross-section: spray elevation vs. acceptance window.

    h_pers : standing person height [m]
    """
    r_cs = np.linspace(0.5, 200, 500)

    fig, ax = plt.subplots(figsize=(11, 5))

    # Ground fill
    ax.fill_between([0, 200], [-6, -6], [0, 0], color="#c8a97e", alpha=0.55)
    ax.axhline(0, color="#8b6914", lw=1.5)

    # Acceptance window: fragments at height 0–1.7 m can hit the standing person
    ax.fill_between([0, 200], [0, 0], [h_pers, h_pers],
                    color="green", alpha=0.12, label="Acceptance window (0–1.7 m height)")
    ax.axhline(h_pers, color="green", lw=0.8, ls="--", alpha=0.5)
    ax.text(170, h_pers + 0.4, "1.7 m (top of target)", fontsize=7.5, color="green")

    # Model trajectory: all fragments horizontal
    ax.axhline(0, color="red", lw=2.5, zorder=5,
               label="Model (Gurney cylinder): all fragments at θ = 0°")

    # Illustrative real trajectories at various elevation angles
    for theta_deg, ls, alpha in [(5, "-", 0.45), (15, "-", 0.40),
                                 (30, "-", 0.35), (60, "-", 0.30)]:
        theta_r = np.radians(theta_deg)
        ax.plot(r_cs, r_cs * np.tan(theta_r), color="steelblue",
                lw=1.1, ls=ls, alpha=alpha)
        r_label = min(60, 200 / np.tan(theta_r) * 0.3) if theta_deg < 90 else 10
        h_label = r_label * np.tan(theta_r)
        if h_label < 50:
            ax.text(r_label + 1, h_label + 0.5, f"+{theta_deg}°",
                    fontsize=7.5, color="steelblue", alpha=0.75)

    # Fragments going below horizontal enter the ground immediately
    ax.plot([0, 30], [0, 30 * np.tan(np.radians(-10))],
            color="gray", lw=1.1, ls="--", alpha=0.45, label="Into ground (θ < 0°, not lethal)")
    ax.text(12, 30 * np.tan(np.radians(-10)) - 0.8, "−10°",
            fontsize=7.5, color="gray", alpha=0.7)

    # Standing person silhouettes and acceptance-angle annotations
    for r_p in [50, 100, 150]:
        ax.add_patch(plt.Rectangle((r_p - 0.5, 0), 1.0, h_pers,
                                   facecolor="orange", edgecolor="darkorange",
                                   alpha=0.85, zorder=4))
        theta_max = np.degrees(np.arctan(h_pers / r_p))
        ax.annotate(f"θ_max = {theta_max:.1f}°",
                    xy=(r_p, h_pers), xytext=(r_p - 22, h_pers + 3.5),
                    fontsize=7.5, color="darkgreen",
                    arrowprops=dict(arrowstyle="->", color="darkgreen", lw=0.8))

    # Blue-line label
    ax.text(8, 9, "Real spray:\nfragments at\nvarious angles\n(not yet modelled)",
            fontsize=7.5, color="steelblue", alpha=0.8)

    ax.set_xlim(0, 200)
    ax.set_ylim(-6, 50)
    ax.set_xlabel("Horizontal range [m]")
    ax.set_ylabel("Height [m]")
    ax.set_title(
        "Fragment trajectory cross-section — ground burst, shell axis vertical\n"
        "Red: Gurney cylinder assumption (all fragments horizontal). "
        "Blue: illustrative real elevation spread (not modelled).\n"
        "θ_max = arctan(1.7 m / r) is the steepest angle that still hits a standing target."
    )
    ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    return fig


def fig_field_map_2d(r_2d: np.ndarray, P_grid: np.ndarray, R50: float) -> plt.Figure:
    """Figure 5 — 2-D field map (axis-vertical burst → symmetric circle).

    r_2d   : radial grid [m]
    P_grid : P(kill) at each radius [-]
    R50    : range where P(kill) = 0.5 [m]
    """
    theta = np.linspace(0, 2 * np.pi, 360)
    R2D, THETA = np.meshgrid(r_2d, theta)
    P_2D = np.tile(P_grid, (360, 1))
    X, Y = R2D * np.cos(THETA), R2D * np.sin(THETA)

    fig, ax = plt.subplots(figsize=(7, 6))
    cf = ax.contourf(X, Y, P_2D * 100,
                     levels=[0, 5, 10, 25, 50, 75, 90, 95, 100], cmap="YlOrRd")
    ax.contour(X, Y, P_2D * 100, levels=[50], colors="white", linewidths=1.5)
    fig.colorbar(cf, ax=ax, label="P(hit) [%]")
    ax.set_aspect("equal")
    ax.set_xlabel("East [m]")
    ax.set_ylabel("North [m]")
    ax.set_title(
        f"Fragmentation Field — 105 mm M1 HE Ground Burst (axis-vertical)\n"
        f"R₅₀ = {R50:.0f} m  |  ES-310 Pk|hit  |  standing person"
    )
    ax.plot(0, 0, "k+", ms=10, markeredgewidth=2, label="Burst point")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(0.02, 0.04,
            "Note: symmetric pattern assumes 90° angle of fall.\n"
            "Shallower angles elongate the field along the line of fire.",
            transform=ax.transAxes, fontsize=7, color="0.4")
    fig.tight_layout()
    return fig


def fig_four_zone_field(
    X3d: np.ndarray, Y3d: np.ndarray, P3d: np.ndarray
) -> plt.Figure:
    """§6.7 — four-zone P(kill) ground field for M1, AoF = 30°, h_b = 2 m."""
    fig, ax = plt.subplots(figsize=(7, 6))
    cf = ax.contourf(X3d, Y3d, P3d * 100,
                     levels=[0, 1, 5, 10, 25, 50, 75, 90, 99], cmap="YlOrRd")
    ax.contour(X3d, Y3d, P3d * 100, levels=[50], colors="white", linewidths=1.5)
    fig.colorbar(cf, ax=ax, label="P(kill) [%]")
    ax.set_aspect("equal")
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Cross-range y [m]")
    ax.set_title(
        "Four-Zone Field — 105 mm M1 HE\n"
        "AoF = 30°, h_b = 2 m, STANDING target\n"
        "(arrow → direction of flight; forward = +x)"
    )
    ax.annotate("→ direction of fire", xy=(0.96, 0.03), xytext=(0.65, 0.03),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="0.25"), fontsize=9)
    ax.plot(0, 0, "k+", ms=10, markeredgewidth=2, label="Burst")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def fig_lethal_density_field(
    X: np.ndarray, Y: np.ndarray, rho_L: np.ndarray, title: str
) -> plt.Figure:
    """Lethal-fragment areal-density field ρ_L [m⁻²] on an (x, y) ground patch.

    Renders the target-independent kernel ρ_L (derivation eq. 3): lethal
    fragments crossing a 1 m² patch. Filled log-spaced contours of the
    already-computed field; no physics here.

    X, Y  : ground meshgrids [m] (downrange x, cross-range y)
    rho_L : lethal-density meshgrid [m⁻²]
    title : figure title (path + burst geometry, supplied by caller)
    """
    fig, ax = plt.subplots(figsize=(7, 6))
    rho_max = float(np.nanmax(rho_L))
    if rho_max <= 0.0:
        # Degenerate (all-zero) field — draw an empty frame rather than error.
        ax.text(0.5, 0.5, "ρ_L ≡ 0 over patch", ha="center", va="center",
                transform=ax.transAxes)
    else:
        # Log-spaced levels span four decades below the field peak so the
        # 1/s² falloff and finite lethal reach are both visible.
        levels = np.logspace(np.log10(rho_max) - 4, np.log10(rho_max), 9)
        cf = ax.contourf(X, Y, np.clip(rho_L, levels[0], None),
                         levels=levels, cmap="viridis",
                         norm=LogNorm(vmin=levels[0], vmax=levels[-1]))
        fig.colorbar(cf, ax=ax, label=r"$\rho_L$ [lethal frags / m$^2$]")
    ax.set_aspect("equal")
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Cross-range y [m]")
    ax.set_title(title)
    ax.annotate("→ direction of fire", xy=(0.96, 0.03), xytext=(0.65, 0.03),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="0.25"), fontsize=9)
    ax.plot(0, 0, "k+", ms=10, markeredgewidth=2, label="Burst")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def fig_pkill_volume(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    P_k: np.ndarray,
    title: str,
):
    """Interactive 3D point kill-probability field P_k(x,y,z) [-] ∈ [0,1].

    Plotly counterpart of :func:`fig_lethal_density_field` for the Streamlit
    app: renders the already-computed P_k volume (``pkill_volume_3d`` /
    ``four_zone_pkill_volume`` — see ``pkill-poisson-field`` derivation eq. 1)
    as a ``go.Volume`` trace (design.md D2, Round 2). An earlier round saw
    marching-cubes faceting ("origami crane" artifact) from anisotropic,
    over-extended sampling on the raw ρ_L field; the fix was a tighter
    burst-centered spatial extent so the grid resolution covers the field's
    interesting region densely, plus the tuned trace parameters below
    (validated empirically). With those, ``go.Volume`` renders cleanly with
    no visible faceting. Unlike ρ_L (an unbounded, multi-decade areal
    density), P_k is a bounded probability — isomin/isomax are therefore
    fixed to a [0,1]-relative range rather than computed from the field's max.
    No physics here — purely rendering the supplied (X, Y, Z, P_k) grids.

    The signature takes the plain ``(X, Y, Z, P_k)`` 3D meshgrids returned by
    ``pkill_volume_3d`` / ``four_zone_pkill_volume``, flattened here for the
    volume trace.

    X, Y, Z : coordinate meshgrids [m] (downrange x, cross-range y, height z)
    P_k     : kill-probability meshgrid [-], ∈ [0,1]
    title   : figure title (path + burst geometry, supplied by caller)

    Returns a Plotly ``go.Figure``.
    """
    import plotly.graph_objects as go

    pk_flat = P_k.ravel()
    pk_max = float(np.nanmax(P_k)) if pk_flat.size else 0.0

    fig = go.Figure()
    if pk_max > 0.0:
        fig.add_trace(
            go.Volume(
                x=X.ravel(),
                y=Y.ravel(),
                z=Z.ravel(),
                value=P_k.ravel(),
                isomin=0.05,
                isomax=1.0,
                opacity=0.2,
                surface_count=25,
                colorscale="Hot",
                colorbar=dict(title="P(kill) [-]"),
                caps=dict(x_show=False, y_show=False, z_show=False),
            )
        )
    else:
        # Degenerate (all-zero) field — annotate rather than draw an empty box.
        fig.add_annotation(
            text="P_k ≡ 0 over volume",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
        )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Downrange x [m]",
            yaxis_title="Cross-range y [m]",
            zaxis_title="Height z [m]",
            aspectmode="data",
        ),
    )
    return fig


def _elevation_ray(
    ax: plt.Axes,
    x0: float,
    z0: float,
    vgx: float,
    vgz: float,
    color: str,
    ls: str,
    label: str | None,
    arrow_len: float = 25.0,
) -> None:
    """Draw one fragment ray from (x0, z0) in direction (vgx, vgz).

    Solid line to ground impact if vgz < 0; dashed upward arrow if vgz >= 0.
    """
    if vgz < -1e-6:
        t = z0 / (-vgz)
        x_hit = x0 + vgx * t
        ax.plot([x0, x_hit], [z0, 0.0], color=color, lw=1.8, ls=ls, label=label, zorder=3)
        ax.plot(x_hit, 0.0, "o", color=color, ms=5, zorder=4)
    else:
        mag = max(float(np.sqrt(vgx**2 + vgz**2)), 1e-9)
        x_end = x0 + vgx / mag * arrow_len
        z_end = z0 + vgz / mag * arrow_len
        ax.plot([x0, x_end], [z0, z_end], color=color, lw=1.5, ls="--", label=label, zorder=3)


def fig_single_zone_elevation(
    aof_deg: float = 30.0,
    h_b: float = 2.0,
    r_person: float = 30.0,
    spray_half_angle_deg: float = 15.0,
) -> plt.Figure:
    """Elevation cross-section for the single-zone belt model (x-z plane, y=0).

    Sprays a belt perpendicular to the shell axis e_axis = (−cosα, 0, −sinα).
    In the x-z plane the belt appears at two azimuths: phi=+90° giving
    (sinα, cosα) — the upper lobe (solid) — and phi=−90° giving (−sinα, −cosα)
    — the lower lobe (dashed), whose rays reach the ground behind the burst.
    Each lobe's bounding rays are ± δ from the equatorial centre. Rays with
    vz < 0 are traced to ground impact; upward rays are drawn as arrows.

    aof_deg              : shell angle of fall [degrees]
    h_b                  : burst height [m]
    r_person             : downrange person distance [m]
    spray_half_angle_deg : belt half-width δ [degrees]
    """
    aof = np.radians(aof_deg)
    cA, sA = np.cos(aof), np.sin(aof)
    delta = np.radians(spray_half_angle_deg)

    fig, ax = plt.subplots(figsize=(10, 5))

    x_max = max(r_person * 1.4, 50.0)
    x_min = -x_max * 0.35
    z_max = max(h_b + 10, 15.0)

    ax.fill_between([x_min, x_max], [-2, -2], [0, 0], color="#c8a97e", alpha=0.55)
    ax.axhline(0.0, color="#8b6914", lw=1.5, zorder=2)

    # Shell arrival arrow
    L_arr = min(z_max * 0.45, 18.0)
    ax.annotate(
        "", xy=(0.0, h_b),
        xytext=(-cA * L_arr, h_b + sA * L_arr),
        arrowprops=dict(arrowstyle="->", color="0.45", lw=1.5),
    )
    ax.text(
        -cA * L_arr - 0.5, h_b + sA * L_arr + 0.5,
        f"AoF = {aof_deg:.0f}°",
        fontsize=8, color="0.45", ha="right",
    )

    # Burst point
    ax.plot(0, h_b, "k+", ms=14, markeredgewidth=2.5, zorder=5)
    ax.plot(0, h_b, "ko", ms=4, zorder=5, label=f"Burst  (h_b = {h_b:.1f} m)")

    # Belt geometry: equatorial plane perpendicular to shell axis.
    # Shell direction in ground frame: (cA, -sA). Its perpendicular is (sA, cA),
    # corresponding to beta_c = pi/2 - aof (upper lobe, phi=+90°).
    # The opposite lobe (phi=-90°) is at beta_c + pi, direction (-sA, -cA).
    beta_c = np.pi / 2.0 - aof          # upper-lobe centre; (cos β_c, sin β_c) = (sA, cA)
    # Centre-line through both lobes (thin dotted)
    cx, cz = np.cos(beta_c), np.sin(beta_c)
    cl_len = min(z_max * 0.6, 16.0)
    ax.plot(
        [-cx * cl_len, cx * cl_len], [h_b - cz * cl_len, h_b + cz * cl_len],
        color="0.55", lw=1.0, ls=":", zorder=2, label="belt centre-line (equatorial)",
    )

    # Belt-edge rays: upper lobe (solid, phi=+90°) and lower lobe (dashed, phi=−90°)
    edge_labelled = False
    for lobe_offset, ls in [(0.0, "-"), (np.pi, "--")]:
        beta_lobe = beta_c + lobe_offset
        for sign in (+1, -1):
            beta = beta_lobe + sign * delta
            vgx, vgz = float(np.cos(beta)), float(np.sin(beta))
            lbl = f"belt edge  δ=±{spray_half_angle_deg:.0f}°" if not edge_labelled else None
            edge_labelled = True
            _elevation_ray(ax, 0.0, h_b, vgx, vgz, color="C1", ls=ls, label=lbl)

    # Annotate δ at the burst point (arc on the lower lobe, where rays reach the ground)
    arc_r = min(z_max * 0.22, 4.0)
    beta_lo = beta_c + np.pi            # lower-lobe centre
    arc_th = np.linspace(beta_lo - delta, beta_lo, 24)
    ax.plot(arc_r * np.cos(arc_th), h_b + arc_r * np.sin(arc_th),
            color="C1", lw=1.0, zorder=4)
    th_mid = beta_lo - delta / 2.0
    ax.text(arc_r * 1.25 * np.cos(th_mid), h_b + arc_r * 1.25 * np.sin(th_mid),
            f"δ={spray_half_angle_deg:.0f}°", fontsize=7.5, color="C1",
            ha="center", va="center")

    # Person silhouette
    h_pers = 1.7
    if abs(r_person) >= 2:
        ax.add_patch(plt.Rectangle(
            (r_person - 0.4, 0), 0.8, h_pers,
            facecolor="orange", edgecolor="darkorange", alpha=0.85, zorder=4,
            label=f"Person @ {r_person:.0f} m",
        ))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-2, z_max)
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Height z [m]")
    ax.set_title(
        f"Elevation cross-section — single-zone belt model\n"
        f"AoF = {aof_deg:.0f}°,  h_b = {h_b:.1f} m,  δ = {spray_half_angle_deg:.0f}°  "
        f"|  belt perpendicular to shell axis (y=0 plane)"
    )
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.35)
    fig.tight_layout()
    return fig


def fig_zone_elevation(
    zones: ShellZones,
    aof_deg: float = 30.0,
    h_b: float = 2.0,
    r_person: float = 30.0,
) -> plt.Figure:
    """Elevation cross-section for the four-zone model (x-z plane, y=0).

    For each zone draws the phi=+90° (solid) and phi=-90° (dashed) rays —
    the only two azimuths with vgy=0, bounding the spray cone in elevation.
    Rays reaching the ground are drawn to their impact point; upward /
    horizontal rays are drawn as dashed arrows annotated "↑ excl."
    """
    zone_colours = {"ogive": "C0", "cylinder": "C1", "boattail": "C2", "base": "C3"}
    zone_list = [
        ("ogive",    zones.ogive),
        ("cylinder", zones.cylinder),
        ("boattail", zones.boattail),
        ("base",     zones.base),
    ]

    aof = np.radians(aof_deg)
    cA, sA = np.cos(aof), np.sin(aof)

    fig, ax = plt.subplots(figsize=(10, 5))

    x_max = max(r_person * 1.4, 50.0)
    x_min = -x_max * 0.4
    z_max = max(h_b + 10, 15.0)

    ax.fill_between([x_min, x_max], [-2, -2], [0, 0], color="#c8a97e", alpha=0.55)
    ax.axhline(0.0, color="#8b6914", lw=1.5, zorder=2)

    # Shell arrival arrow
    L_arr = min(z_max * 0.45, 18.0)
    ax.annotate(
        "", xy=(0.0, h_b),
        xytext=(-cA * L_arr, h_b + sA * L_arr),
        arrowprops=dict(arrowstyle="->", color="0.45", lw=1.5),
    )
    ax.text(
        -cA * L_arr - 0.5, h_b + sA * L_arr + 0.5,
        f"AoF = {aof_deg:.0f}°",
        fontsize=8, color="0.45", ha="right",
    )

    # Burst point
    ax.plot(0, h_b, "k+", ms=14, markeredgewidth=2.5, zorder=5)
    ax.plot(0, h_b, "ko", ms=4, zorder=5, label="Burst")

    # Per-zone fragment rays (phi=+90° solid, phi=-90° dashed)
    for name, z in zone_list:
        if z.mass_kg <= 1e-6:
            continue
        color = zone_colours[name]
        th = np.radians(z.spray_deg)
        cT, sT = float(np.cos(th)), float(np.sin(th))
        for phi_sign, ls, first in [(1, "-", True), (-1, "--", False)]:
            vgx = cA * cT + sA * sT * phi_sign
            vgz = -sA * cT + cA * sT * phi_sign
            lbl = f"{name}  θ={z.spray_deg:.0f}°" if first else None
            _elevation_ray(ax, 0.0, h_b, float(vgx), float(vgz),
                           color=color, ls=ls, label=lbl)

    # Person silhouette
    h_pers = 1.7
    if abs(r_person) >= 2:
        ax.add_patch(plt.Rectangle(
            (r_person - 0.4, 0), 0.8, h_pers,
            facecolor="orange", edgecolor="darkorange", alpha=0.85, zorder=4,
            label=f"Person @ {r_person:.0f} m",
        ))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-2, z_max)
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Height z [m]")
    ax.set_title(
        f"Elevation cross-section — four-zone model\n"
        f"AoF = {aof_deg:.0f}°,  h_b = {h_b:.1f} m  |  solid=φ+90°, dashed=φ−90°  (y=0 plane)"
    )
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    ax.grid(alpha=0.35)
    fig.tight_layout()
    return fig


def fig_zone_footprint(
    zones: ShellZones, aof_deg: float = 30.0, h_b: float = 2.0, n_phi: int = 60
) -> plt.Figure:
    """§6.8 — per-zone ground footprint from deterministic azimuthal rays."""
    fig, ax = plt.subplots(figsize=(7, 6))
    zone_colours = {"ogive": "C0", "cylinder": "C1", "boattail": "C2", "base": "C3"}
    for name, z in [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                    ("boattail", zones.boattail), ("base", zones.base)]:
        if z.mass_kg <= 1e-6:
            continue
        xs, ys = [], []
        for phi in np.linspace(0, 2 * np.pi, n_phi, endpoint=False):
            res = fragment_ground_impact(z.spray_deg, phi, aof_deg=aof_deg, h_b=h_b)
            if res is not None:
                x, y, _ = res
                xs.append(x)
                ys.append(y)
        ax.scatter(xs, ys, c=zone_colours[name], s=14, alpha=0.7,
                   label=f"{name} (θ={z.spray_deg:.1f}°)")
    ax.plot(0, 0, "k+", ms=12, markeredgewidth=2, label="Burst")
    ax.set_aspect("equal")
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Cross-range y [m]")
    ax.set_title(f"Per-zone ground-impact ring — M1 105 mm, AoF = {aof_deg:.0f}°, h_b = {h_b} m")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.35)
    fig.tight_layout()
    return fig
