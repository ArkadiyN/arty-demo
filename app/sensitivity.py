import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from arty.fragmentation import (
    FILLERS,
    PRONE,
    STANDING,
    BurstParams,
    DragParams,
    PostureParams,
    ShellParams,
    SteelParams,
    compute_frag_field_3d,
    retardation_coeff,
)
from arty.zones import (
    _four_zone_field_split,
    compute_shell_zones,
    four_zone_line_split,
    fragment_velocity,
)
from arty.shells import SHELLS

st.set_page_config(page_title="Fragmentation Field — Sensitivity", layout="wide")
st.title("Fragmentation Field Sensitivity")
st.caption(
    "HE airburst · Gurney + Mott + ES-310 Pk|hit · 3D belt spray + A_p(γ) posture model"
)

# ---------------------------------------------------------------------------
# Sidebar — all parameters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Parameters")

    model_mode = st.radio("Model", ["Single-zone (legacy)", "Four-zone (new)"])

    shell_name = st.selectbox("Shell preset", list(SHELLS.keys()))
    preset = SHELLS[shell_name]

    if model_mode == "Four-zone (new)":
        tier_label = (
            "Tier-1 · arc geometry"
            if preset.ogive_outer_R is not None
            else "Tier-2 · CRH fallback"
        )
        st.caption(tier_label)

    with st.expander("Shell & Explosive", expanded=True):
        filler_name = st.selectbox(
            "Filler type",
            list(FILLERS.keys()),
            index=list(FILLERS.keys()).index(preset.filler.name),
        )
        filler = FILLERS[filler_name]
        mass_total = st.slider(
            "Total projectile mass  [kg]", 5.0, 50.0, float(preset.mass_total), step=0.1
        )
        mass_filler = st.slider(
            "Filler mass  [kg]", 0.5, 12.0, float(preset.mass_filler), step=0.05
        )
        caliber_mm = st.slider(
            "Caliber  [mm]", 75.0, 155.0, float(preset.caliber * 1e3), step=1.0
        )
        wall_t_mm = st.slider(
            "Wall thickness  [mm]", 5.0, 25.0, float(preset.wall_t * 1e3), step=0.5
        )

    with st.expander("Mott Fragmentation"):
        gamma = st.slider(
            "γ (Mott parameter)", 53.0, 80.0, float(preset.steel.gamma), step=1.0
        )
        sigma_f = st.slider(
            "σ_F dynamic flow stress  [MPa]",
            600.0,
            1200.0,
            float(preset.steel.sigma_f / 1e6),
            step=10.0,
        )
        rho_steel = st.slider(
            "Steel density  [kg/m³]", 7600.0, 8000.0, float(preset.steel.rho), step=10.0
        )

    with st.expander("Drag"):
        C_D = st.slider(
            "C_D (drag coefficient)", 0.40, 0.90, float(DragParams().C_D), step=0.01
        )
        rho_air = st.slider(
            "Air density  [kg/m³]", 0.90, 1.40, float(DragParams().rho_air), step=0.01
        )

    with st.expander("Burst Geometry"):
        h_b = st.slider("Burst height  h_b  [m]", 0.0, 20.0, float(BurstParams().h_b), step=0.5)
        angle_of_fall = st.slider(
            "Angle of fall  [°]", 0, 90, int(BurstParams().angle_of_fall), step=5
        )
        spray_half_angle = st.slider(
            "Belt half-angle  δ  [°]", 0, 30, int(BurstParams().spray_half_angle), step=1
        )

    with st.expander("Target"):
        posture_name = st.radio("Posture", ["Standing", "Prone"], index=0)

    max_radius = st.slider(
        "Analysis radius  [m]", 40.0, 200.0, 80.0, step=10.0,
        help="Changing this reruns all field computations.",
    )

# ---------------------------------------------------------------------------
# Build param structs
# ---------------------------------------------------------------------------

steel = SteelParams(
    name=preset.steel.name,
    rho=rho_steel,
    sigma_f=sigma_f * 1e6,
    gamma=gamma,
)
# Pass ogive geometry fields from preset verbatim — drawing-derived, not slider-tweakable.
shell = ShellParams(
    caliber=caliber_mm / 1e3,
    wall_t=wall_t_mm / 1e3,
    mass_total=mass_total,
    mass_filler=mass_filler,
    mass_deductions=preset.mass_deductions,
    filler=filler,
    steel=steel,
    ogive_outer_R=preset.ogive_outer_R,
    ogive_inner_R=preset.ogive_inner_R,
    ogive_len=preset.ogive_len,
    ogive_tip_dia=preset.ogive_tip_dia,
    cylinder_len=preset.cylinder_len,
    boattail_len=preset.boattail_len,
    boattail_angle_deg=preset.boattail_angle_deg,
    boattail_inner_dia=preset.boattail_inner_dia,
    base_thickness=preset.base_thickness,
    has_boattail=preset.has_boattail,
    base_treatment=preset.base_treatment,
    ogive_crh=preset.ogive_crh,
)
drag = DragParams(C_D=C_D, rho_air=rho_air)
burst = BurstParams(h_b=h_b, angle_of_fall=float(angle_of_fall), spray_half_angle=float(spray_half_angle))
posture: PostureParams = STANDING if posture_name == "Standing" else PRONE

# ---------------------------------------------------------------------------
# Compute (cached)
# ---------------------------------------------------------------------------

# Grid aligned to 2.5 m steps through 0; both models share the same grid so
# diff subtraction is exact and slider positions map 1-to-1 to grid columns.
_N_STEPS = int(max_radius / 2.5)
_N_GRID = 2 * _N_STEPS + 1  # odd → includes 0 exactly


@st.cache_data
def _compute_legacy(shell, drag, burst, posture, max_radius, n_grid):
    return compute_frag_field_3d(shell, drag, burst, posture, max_radius=max_radius, n_grid=n_grid)


@st.cache_data
def _compute_zones(
    shell_name, filler_name,
    mass_total, mass_filler, caliber_mm, wall_t_mm,
    gamma, sigma_f, rho_steel,
    C_D, rho_air,
    h_b, angle_of_fall, spray_half_angle,
    posture, max_radius, n_grid,
):
    preset_s = SHELLS[shell_name]
    steel_s = SteelParams(
        name=preset_s.steel.name,
        rho=rho_steel,
        sigma_f=sigma_f * 1e6,
        gamma=gamma,
    )
    shell_s = ShellParams(
        caliber=caliber_mm / 1e3,
        wall_t=wall_t_mm / 1e3,
        mass_total=mass_total,
        mass_filler=mass_filler,
        mass_deductions=preset_s.mass_deductions,
        filler=FILLERS[filler_name],
        steel=steel_s,
        ogive_outer_R=preset_s.ogive_outer_R,
        ogive_inner_R=preset_s.ogive_inner_R,
        ogive_len=preset_s.ogive_len,
        ogive_tip_dia=preset_s.ogive_tip_dia,
        cylinder_len=preset_s.cylinder_len,
        boattail_len=preset_s.boattail_len,
        boattail_angle_deg=preset_s.boattail_angle_deg,
        boattail_inner_dia=preset_s.boattail_inner_dia,
        base_thickness=preset_s.base_thickness,
        has_boattail=preset_s.has_boattail,
        base_treatment=preset_s.base_treatment,
        ogive_crh=preset_s.ogive_crh,
    )
    drag_s = DragParams(C_D=C_D, rho_air=rho_air)

    zones = compute_shell_zones(shell_s)

    n_mass = 200
    m_grid = np.logspace(-6, np.log10(0.5), n_mass)
    drag_lam_grid = retardation_coeff(m_grid, drag_s, rho_steel)

    X, Y, pk_total, pk_by_zone = _four_zone_field_split(
        zones, float(angle_of_fall), h_b, posture, drag_lam_grid, m_grid,
        max_r=max_radius, n_grid=n_grid, delta_deg=float(spray_half_angle),
    )

    # R50 from cross-range slice at x=0 (centre column, grid is odd so exact)
    xy = np.linspace(-max_radius, max_radius, n_grid)
    x_idx = n_grid // 2
    pk_cross = pk_total[:, x_idx]
    idx50 = np.argmin(np.abs(pk_cross - 0.5))
    r50_cross = float(np.abs(xy[idx50]))

    # KE chart using cylinder zone V0
    cyl = zones.cylinder
    r_ke = np.linspace(0, max_radius, n_grid)
    rep_masses_g = [0.5, 5.0, 50.0]
    rep_masses_kg = np.array([m * 1e-3 for m in rep_masses_g])
    lam_rep = retardation_coeff(rep_masses_kg, drag_s, rho_steel)
    ke_by_mass: dict[float, np.ndarray] = {}
    for m_g, lam_j in zip(rep_masses_g, lam_rep):
        ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (cyl.V0_ms * np.exp(-lam_j * r_ke)) ** 2

    N0_cyl = cyl.mass_kg / (2.0 * cyl.mu)

    return {
        "X": X,
        "Y": Y,
        "pk_total": pk_total,
        "pk_by_zone": pk_by_zone,
        "zones": zones,
        "r50_cross": r50_cross,
        "r_ke": r_ke,
        "ke_by_mass": ke_by_mass,
        "V0_cyl": cyl.V0_ms,
        "N0_cyl": N0_cyl,
        "mu_cyl": cyl.mu,
        "m_grid": m_grid,
        "drag_lam_grid": drag_lam_grid,
    }


# Fine slice line: 10x the coarse grid step, cheap since cost is O(n_line)
# per zone rather than O(n_grid^2) — see arty.zones.four_zone_line_split.
_FINE_STEP = 0.25


@st.cache_data
def _compute_zone_line(zones, angle_of_fall, h_b, posture, drag_lam_grid, m_grid,
                        spray_half_angle, max_radius, fixed_axis, fixed_coord):
    n_fine = 2 * int(max_radius / _FINE_STEP) + 1
    line_coords = np.linspace(-max_radius, max_radius, n_fine)
    pk_total, pk_by_zone = four_zone_line_split(
        zones, float(angle_of_fall), h_b, posture, drag_lam_grid, m_grid,
        fixed_axis=fixed_axis, fixed_coord=fixed_coord, line_coords=line_coords,
        delta_deg=float(spray_half_angle),
    )
    return line_coords, pk_total, pk_by_zone


result = _compute_legacy(shell, drag, burst, posture, max_radius, _N_GRID)
result_zones = None
if model_mode == "Four-zone (new)":
    result_zones = _compute_zones(
        shell_name, filler_name,
        mass_total, mass_filler, caliber_mm, wall_t_mm,
        gamma, sigma_f, rho_steel,
        C_D, rho_air,
        h_b, angle_of_fall, spray_half_angle,
        posture, max_radius, _N_GRID,
    )

# ---------------------------------------------------------------------------
# Headline metrics
# ---------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)
if model_mode == "Four-zone (new)" and result_zones is not None:
    col1.metric("R₅₀ (cross-range)", f"{result_zones['r50_cross']:.0f} m")
    col2.metric("V₀", f"{result_zones['V0_cyl']:.0f} m/s", delta="(cyl zone)", delta_color="off")
    col3.metric("N₀ (total frags)", f"{result_zones['N0_cyl']:.0f}", delta="(cyl zone)", delta_color="off")
    col4.metric("μ (half-mass)", f"{result_zones['mu_cyl'] * 1e3:.2f} g", delta="(cyl zone)", delta_color="off")
else:
    col1.metric("R₅₀ (cross-range)", f"{result.r50_cross:.0f} m")
    col2.metric("V₀", f"{result.V0:.0f} m/s")
    col3.metric("N₀ (total frags)", f"{result.N0:.0f}")
    col4.metric("μ (half-mass)", f"{result.mu * 1e3:.2f} g")

st.divider()

# ---------------------------------------------------------------------------
# Figures — top row: Mott CDF and KE vs distance
# ---------------------------------------------------------------------------

_r_ke = result_zones["r_ke"] if result_zones else result.r_ke
_ke_by_mass = result_zones["ke_by_mass"] if result_zones else result.ke_by_mass
_mu = result_zones["mu_cyl"] if result_zones else result.mu
_N0 = result_zones["N0_cyl"] if result_zones else result.N0

left, right = st.columns(2)

# Figure 1 — Mott cumulative distribution
with left:
    m_vals = np.logspace(np.log10(0.01), np.log10(150), 300)  # grams, 10 mg–150 g
    n_vals = _N0 * np.exp(-np.sqrt(m_vals * 1e-3 / _mu))
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=m_vals,
            y=np.maximum(n_vals, 0.5),
            mode="lines",
            line=dict(color="#1f77b4", width=2),
            name="N(≥m)",
        )
    )
    fig1.update_layout(
        title="Mott Cumulative Fragment Count",
        xaxis=dict(title="Fragment mass  [g]", type="log", tickformat=".2g"),
        yaxis=dict(
            title="Fragments with mass ≥ m  [count]",
            type="log",
            range=[0, np.log10(_N0 * 2)],
            tickformat=".2g",
        ),
        height=340,
        margin=dict(t=40, b=40, l=70, r=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

# Figure 2 — KE vs distance from burst
with right:
    fig2 = go.Figure()
    colours = ["#2ca02c", "#ff7f0e", "#d62728"]
    for (m_g, ke_arr), colour in zip(_ke_by_mass.items(), colours):
        fig2.add_trace(
            go.Scatter(
                x=_r_ke,
                y=ke_arr,
                mode="lines",
                line=dict(color=colour, width=2),
                name=f"{m_g} g",
            )
        )
    for y_ref, label in [
        (100, "100 J (ES-310 light)"),
        (1000, "1 kJ (ES-310 moderate)"),
    ]:
        fig2.add_trace(
            go.Scatter(
                x=[_r_ke[0], _r_ke[-1]],
                y=[y_ref, y_ref],
                mode="lines",
                line=dict(dash="dot", color="gray", width=1),
                showlegend=False,
            )
        )
        fig2.add_annotation(
            x=_r_ke[-1],
            y=np.log10(y_ref),
            text=label,
            xanchor="right",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=10, color="gray"),
            yref="y",
        )
    fig2.update_layout(
        title="Fragment KE vs Distance from Burst",
        xaxis_title="Slant range  s  [m]",
        yaxis=dict(
            title="Kinetic energy  [J]",
            type="log",
            range=[-1, 5],
            tickformat=".2g",
        ),
        height=340,
        margin=dict(t=40, b=40, l=60, r=20),
        legend=dict(title="Mass"),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# 2D fragmentation field heatmap(s)
# ---------------------------------------------------------------------------

def _hex_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _spray_cone(
    h_b: float,
    aof_deg: float,
    spray_deg: float,
    delta_deg: float,
    phi_sign: int,
    color: str,
    name: str | None,
    n_arc: int = 16,
    max_len: float = 30.0,
) -> go.Scatter:
    """Filled sector polygon for one spray lobe in the elevation (x-z) plane.

    Sweeps theta from spray_deg-delta to spray_deg+delta (angle from shell axis)
    at fixed phi_sign (±90° azimuth). All rays are capped at max_len slant
    distance; ground-hitting rays are additionally clipped at z=0.
    """
    phi_rad = phi_sign * (np.pi / 2.0)
    xs: list[float] = [0.0]
    zs: list[float] = [h_b]
    for th_deg in np.linspace(spray_deg - delta_deg, spray_deg + delta_deg, n_arc):
        vgx, _vgy, vgz = fragment_velocity(float(th_deg), phi_rad, aof_deg)
        # cap all rays at max_len slant distance
        if h_b > 0.01 and vgz < -1e-6:
            t = min(h_b / (-vgz), max_len)
        else:
            t = max_len
        xs.append(float(vgx * t))
        zs.append(float(h_b + vgz * t))
    xs.append(0.0)
    zs.append(h_b)
    return go.Scatter(
        x=xs, y=zs,
        fill="toself",
        fillcolor=_hex_rgba(color, 0.20),
        mode="lines",
        line=dict(color=color, width=1.5),
        name=name or "",
        showlegend=(name is not None),
        hoverinfo="skip",
    )


def _spray_cone_across(
    h_b: float,
    aof_deg: float,
    spray_deg: float,
    delta_deg: float,
    y_sign: int,
    color: str,
    name: str | None,
    n_arc: int = 16,
    max_len: float = 30.0,
) -> go.Scatter:
    """Filled sector polygon in the across (y-z) plane at phi=0/π.

    At phi=0 (y_sign=+1) / phi=π (y_sign=-1): vy = ±sin(theta), vz = -sA*cos(theta).
    y_sign=+1 draws the right lobe, y_sign=-1 the left (mirror).
    """
    phi_rad = 0.0 if y_sign > 0 else np.pi
    ys: list[float] = [0.0]
    zs: list[float] = [h_b]
    for th_deg in np.linspace(spray_deg - delta_deg, spray_deg + delta_deg, n_arc):
        _vgx, vy, vz = fragment_velocity(float(th_deg), phi_rad, aof_deg)
        if h_b > 0.01 and vz < -1e-6:
            t = min(h_b / (-vz), max_len)
        else:
            t = max_len
        ys.append(float(vy * t))
        zs.append(float(h_b + vz * t))
    ys.append(0.0)
    zs.append(h_b)
    return go.Scatter(
        x=ys, y=zs,
        fill="toself",
        fillcolor=_hex_rgba(color, 0.20),
        mode="lines",
        line=dict(color=color, width=1.5),
        name=name or "",
        showlegend=(name is not None),
        hoverinfo="skip",
    )


_ZONE_COLOURS_ELEV = {
    "ogive": "#1f77b4",
    "cylinder": "#ff7f0e",
    "boattail": "#2ca02c",
    "base": "#d62728",
}


def _plotly_elevation(
    zones_or_none,
    aof_deg: float,
    h_b: float,
    x_person: float,
    spray_half_angle_deg: float = 15.0,
) -> go.Figure:
    """Plotly elevation cross-section (x-z plane).

    Draws filled cone polygons (phi=+90° and phi=−90° lobes) for each zone,
    each spanning ± spray_half_angle_deg around the zone's spray_deg from the
    shell axis. Both models respond to the spray_half_angle_deg slider.

    zones_or_none=None → single-zone equatorial belt at spray_deg=90°.
    ShellZones object  → four-zone variant (per-zone cones).
    """
    aof = np.radians(aof_deg)
    cA, sA = float(np.cos(aof)), float(np.sin(aof))

    x_max = max(abs(x_person) * 1.5, 50.0)
    x_min = -x_max * 0.4
    z_max = max(h_b + 10, 15.0)

    traces: list = []

    # Ground fill (rectangle)
    traces.append(go.Scatter(
        x=[x_min, x_max, x_max, x_min, x_min],
        y=[-2, -2, 0, 0, -2],
        fill="toself", fillcolor="rgba(200,169,126,0.45)",
        line=dict(color="rgba(139,105,20,1)", width=1.5),
        mode="lines", showlegend=False, hoverinfo="skip",
    ))

    # Shell arrival arrow (drawn as two scatter points + annotation)
    L_arr = min(z_max * 0.45, 18.0)
    ax_x0, ax_z0 = -cA * L_arr, h_b + sA * L_arr
    traces.append(go.Scatter(
        x=[ax_x0, 0.0], y=[ax_z0, h_b],
        mode="lines",
        line=dict(color="gray", width=2),
        showlegend=False, hoverinfo="skip",
    ))

    # Burst point
    traces.append(go.Scatter(
        x=[0], y=[h_b], mode="markers+text",
        marker=dict(symbol="cross", size=14, color="black", line=dict(width=2.5, color="black")),
        text=[f"Burst h_b={h_b:.1f} m"], textposition="top right",
        showlegend=False,
    ))

    if zones_or_none is None:
        # Single-zone: equatorial belt at spray_deg=90° from shell axis
        for phi_sign in (+1, -1):
            traces.append(_spray_cone(
                h_b, aof_deg,
                spray_deg=90.0,
                delta_deg=spray_half_angle_deg,
                phi_sign=phi_sign,
                color="#ff7f0e",
                name=f"belt  δ=±{spray_half_angle_deg:.0f}°" if phi_sign == +1 else None,
            ))
    else:
        zone_list = [
            ("ogive",    zones_or_none.ogive),
            ("cylinder", zones_or_none.cylinder),
            ("boattail", zones_or_none.boattail),
            ("base",     zones_or_none.base),
        ]
        for name, z in zone_list:
            if z.mass_kg <= 1e-6:
                continue
            color = _ZONE_COLOURS_ELEV[name]
            for phi_sign in (+1, -1):
                traces.append(_spray_cone(
                    h_b, aof_deg,
                    spray_deg=float(z.spray_deg),
                    delta_deg=spray_half_angle_deg,
                    phi_sign=phi_sign,
                    color=color,
                    name=f"{name}  θ={z.spray_deg:.0f}°" if phi_sign == +1 else None,
                ))

    fig = go.Figure(data=traces)
    mode_label = "single-zone (legacy)" if zones_or_none is None else "four-zone"
    fig.update_layout(
        title=f"Elevation cross-section — {mode_label}  ·  AoF={aof_deg:.0f}°, h_b={h_b:.1f} m",
        xaxis=dict(title="Downrange x [m]", range=[x_min, x_max]),
        yaxis=dict(title="Height z [m]", range=[-2, z_max]),
        height=320,
        margin=dict(t=45, b=40, l=60, r=20),
        legend=dict(orientation="h", y=-0.22),
    )
    # Annotate shell arrival direction
    fig.add_annotation(
        x=ax_x0, y=ax_z0,
        text=f"AoF={aof_deg:.0f}°",
        showarrow=False, font=dict(size=10, color="gray"),
        xanchor="right",
    )
    return fig


def _plotly_elevation_across(
    zones_or_none,
    aof_deg: float,
    h_b: float,
    y_person: float,
    spray_half_angle_deg: float = 15.0,
) -> go.Figure:
    """Across cross-section (y-z plane, looking downrange).

    Draws spray fans at phi=±90° for each zone. Unlike the elevation view the
    two lobes are symmetric about y=0 (AoF only tilts the x-z plane). The
    equatorial belt (theta=90°) has vgz=0 and fans are horizontal — most
    interesting for off-equatorial zones (ogive, boattail, base).
    """
    y_max = max(abs(y_person) * 1.5, 50.0)
    z_max = max(h_b + 10, 15.0)
    # Rays should extend past the plot boundary so axes do the clipping, not the
    # slant-range cap (which would create a visible hard stop mid-plot for
    # horizontal rays like the equatorial belt).
    max_ray = y_max + z_max

    traces: list = []

    # Ground fill
    traces.append(go.Scatter(
        x=[-y_max, y_max, y_max, -y_max, -y_max],
        y=[-2, -2, 0, 0, -2],
        fill="toself", fillcolor="rgba(200,169,126,0.45)",
        line=dict(color="rgba(139,105,20,1)", width=1.5),
        mode="lines", showlegend=False, hoverinfo="skip",
    ))

    # Burst point
    traces.append(go.Scatter(
        x=[0], y=[h_b], mode="markers+text",
        marker=dict(symbol="cross", size=14, color="black", line=dict(width=2.5, color="black")),
        text=[f"h_b={h_b:.1f} m"], textposition="top right",
        showlegend=False,
    ))

    if zones_or_none is None:
        for y_sign in (+1, -1):
            traces.append(_spray_cone_across(
                h_b, aof_deg,
                spray_deg=90.0,
                delta_deg=spray_half_angle_deg,
                y_sign=y_sign,
                color="#ff7f0e",
                name=f"belt  δ=±{spray_half_angle_deg:.0f}°" if y_sign == +1 else None,
                max_len=max_ray,
            ))
    else:
        zone_list = [
            ("ogive",    zones_or_none.ogive),
            ("cylinder", zones_or_none.cylinder),
            ("boattail", zones_or_none.boattail),
            ("base",     zones_or_none.base),
        ]
        for name, z in zone_list:
            if z.mass_kg <= 1e-6:
                continue
            color = _ZONE_COLOURS_ELEV[name]
            for y_sign in (+1, -1):
                traces.append(_spray_cone_across(
                    h_b, aof_deg,
                    spray_deg=float(z.spray_deg),
                    delta_deg=spray_half_angle_deg,
                    y_sign=y_sign,
                    color=color,
                    name=f"{name}  θ={z.spray_deg:.0f}°" if y_sign == +1 else None,
                    max_len=max_ray,
                ))

    fig = go.Figure(data=traces)
    mode_label = "single-zone (legacy)" if zones_or_none is None else "four-zone"
    fig.update_layout(
        title=f"Across cross-section — {mode_label}  ·  AoF={aof_deg:.0f}°, h_b={h_b:.1f} m",
        xaxis=dict(title="Cross-range y [m]", range=[-y_max, y_max]),
        yaxis=dict(title="Height z [m]", range=[-2, z_max]),
        height=320,
        margin=dict(t=45, b=40, l=60, r=20),
        legend=dict(orientation="h", y=-0.22),
    )
    return fig


def _r50_contour(x, y, z):
    """White R₅₀ iso-contour overlay (P(kill) = 0.5)."""
    return go.Contour(
        x=x, y=y, z=z,
        contours=dict(start=0.5, end=0.5, size=1.0, coloring="none"),
        line=dict(color="white", width=2.0),
        showscale=False, showlegend=True, hoverinfo="skip",
        name="R₅₀  (P=0.5)",
    )

if model_mode == "Single-zone (legacy)":
    fig3 = go.Figure()
    fig3.add_trace(go.Heatmap(
        x=result.field_x[0], y=result.field_y[:, 0], z=result.field_pk,
        colorscale="YlOrRd", zmin=0, zmax=1,
        colorbar=dict(title="P(kill)"),
    ))
    fig3.add_trace(_r50_contour(result.field_x[0], result.field_y[:, 0], result.field_pk))
    fig3.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
        marker=dict(symbol="cross", size=12, color="black"), showlegend=False))
    fig3.update_layout(
        title=f"2D Fragmentation Field  ·  R₅₀ = {result.r50_cross:.0f} m",
        xaxis=dict(title="Downrange  x  [m]", scaleanchor="y"),
        yaxis_title="Cross-range  y  [m]",
        height=700,
        margin=dict(t=40, b=40, l=60, r=20),
    )
    st.plotly_chart(fig3, use_container_width=True)
    _elev_col, _ = st.columns(2)
    with _elev_col:
        st.plotly_chart(
            _plotly_elevation(None, float(angle_of_fall), h_b, float(result.r50_cross),
                              spray_half_angle_deg=float(spray_half_angle)),
            use_container_width=True,
        )

else:  # Four-zone (new)
    assert result_zones is not None
    xy_grid = result_zones["X"][0]
    yy_grid = result_zones["Y"][:, 0]

    hmap_l, hmap_r = st.columns(2)
    with hmap_l:
        fig_leg = go.Figure()
        fig_leg.add_trace(go.Heatmap(
            x=result.field_x[0], y=result.field_y[:, 0], z=result.field_pk,
            colorscale="YlOrRd", zmin=0, zmax=1,
            colorbar=dict(title="P(kill)"),
        ))
        fig_leg.add_trace(_r50_contour(result.field_x[0], result.field_y[:, 0], result.field_pk))
        fig_leg.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
            marker=dict(symbol="cross", size=12, color="black"), showlegend=False))
        fig_leg.update_layout(
            title=f"Single-zone (legacy)  ·  R₅₀ = {result.r50_cross:.0f} m",
            xaxis=dict(title="Downrange  x  [m]", scaleanchor="y"),
            yaxis_title="Cross-range  y  [m]",
            height=600,
            margin=dict(t=40, b=40, l=60, r=20),
        )
        st.plotly_chart(fig_leg, use_container_width=True)

    with hmap_r:
        fig_4z = go.Figure()
        fig_4z.add_trace(go.Heatmap(
            x=xy_grid, y=yy_grid, z=result_zones["pk_total"],
            colorscale="YlOrRd", zmin=0, zmax=1,
            colorbar=dict(title="P(kill)"),
        ))
        fig_4z.add_trace(_r50_contour(xy_grid, yy_grid, result_zones["pk_total"]))
        fig_4z.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
            marker=dict(symbol="cross", size=12, color="black"), showlegend=False))
        fig_4z.update_layout(
            title=f"Four-zone (new)  ·  R₅₀ = {result_zones['r50_cross']:.0f} m",
            xaxis=dict(title="Downrange  x  [m]", scaleanchor="y"),
            yaxis_title="Cross-range  y  [m]",
            height=600,
            margin=dict(t=40, b=40, l=60, r=20),
        )
        st.plotly_chart(fig_4z, use_container_width=True)

    # Difference map — both grids share linspace(-max_radius, max_radius, _N_GRID)
    diff_pk = result_zones["pk_total"] - result.field_pk
    fig_diff = go.Figure()
    fig_diff.add_trace(go.Heatmap(
        x=xy_grid, y=yy_grid, z=diff_pk,
        colorscale="RdBu_r",
        zmid=0,
        colorbar=dict(title="ΔP(kill)"),
    ))
    fig_diff.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
        marker=dict(symbol="cross", size=12, color="black"), showlegend=False))
    fig_diff.update_layout(
        title="Difference: Four-zone − Single-zone  (red = four-zone more lethal, blue = less)",
        xaxis=dict(title="Downrange  x  [m]", scaleanchor="y"),
        yaxis_title="Cross-range  y  [m]",
        height=700,
        margin=dict(t=40, b=40, l=60, r=20),
    )
    st.plotly_chart(fig_diff, use_container_width=True)

    # ---------------------------------------------------------------------------
    # Zone Breakdown
    # ---------------------------------------------------------------------------

    st.divider()
    st.subheader("Zone Breakdown")

    zones_obj = result_zones["zones"]
    zone_names = ["ogive", "cylinder", "boattail", "base"]
    zone_obj_list = [zones_obj.ogive, zones_obj.cylinder, zones_obj.boattail, zones_obj.base]

    v0_vals = [z.V0_ms for z in zone_obj_list]

    _zone_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # ogive/cylinder/boattail/base = C0/C1/C2/C3
    fig_bar = make_subplots(
        rows=1, cols=2,
        subplot_titles=["V₀ [m/s]", "N(>m) fragments"],
    )
    for idx, (zn, v0) in enumerate(zip(zone_names, v0_vals)):
        c = _zone_colors[idx]
        fig_bar.add_trace(go.Bar(x=[zn], y=[v0], name=zn, marker_color=c, showlegend=False), row=1, col=1)

    _mu_max = max(
        (z.mu for z in zone_obj_list if np.isfinite(z.mu) and z.mu > 0),
        default=0.01,
    )
    _m_g = np.linspace(0.0, min(5.0 * _mu_max * 1e3, 200.0), 300)  # grams
    for idx, (zn, z) in enumerate(zip(zone_names, zone_obj_list)):
        if not (np.isfinite(z.mu) and z.mu > 0 and z.mass_kg > 1e-6):
            continue
        N0_z = z.mass_kg / (2.0 * z.mu)
        n_gt_m = N0_z * np.exp(-np.sqrt(_m_g * 1e-3 / z.mu))
        fig_bar.add_trace(go.Scatter(
            x=_m_g, y=n_gt_m,
            name=zn, line=dict(color=_zone_colors[idx], width=2),
            showlegend=True,
        ), row=1, col=2)
    fig_bar.update_xaxes(title_text="m [g]", row=1, col=2)
    fig_bar.update_yaxes(title_text="frags heavier than m", row=1, col=2)
    fig_bar.update_layout(
        title="Zone Properties",
        height=360,
        margin=dict(t=60, b=40, l=60, r=20),
        legend=dict(orientation="v", x=1.02, y=1.0, xanchor="left"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Grid columns are exactly the 2.5 m steps, so slider options == grid columns.
    xy_arr = np.linspace(-max_radius, max_radius, _N_GRID)
    slider_opts = [round(v, 10) for v in xy_arr.tolist()]

    zone_colors = {
        "ogive": "#1f77b4",
        "cylinder": "#ff7f0e",
        "boattail": "#2ca02c",
        "base": "#d62728",
    }

    # --- Two-column slice charts ---
    sl_left, sl_right = st.columns(2)

    with sl_left:
        x_slice = st.select_slider(
            "Downrange x [m]",
            options=slider_opts,
            value=0.0,
            format_func=lambda v: f"{v:+.1f} m",
            key="x_slice",
        )
        line_y, pk_total_x, pk_by_zone_x = _compute_zone_line(
            result_zones["zones"], angle_of_fall, h_b, posture,
            result_zones["drag_lam_grid"], result_zones["m_grid"],
            spray_half_angle, max_radius, fixed_axis="x", fixed_coord=float(x_slice),
        )
        fig_pk = go.Figure()
        for zn, pk_line in pk_by_zone_x.items():
            fig_pk.add_trace(go.Scatter(
                x=line_y, y=pk_line,
                mode="lines",
                line=dict(color=zone_colors.get(zn, "#888"), width=1.5, dash="dash"),
                name=zn,
            ))
        fig_pk.add_trace(go.Scatter(
            x=line_y, y=pk_total_x,
            mode="lines",
            line=dict(color="black", width=2.5),
            name="total",
        ))
        fig_pk.update_layout(
            title=f"P(kill) vs Cross-range  (x = {x_slice:+.1f} m)",
            xaxis_title="Cross-range  y  [m]",
            yaxis=dict(title="P(kill)", range=[0, 1]),
            height=360,
            margin=dict(t=40, b=40, l=60, r=20),
            legend=dict(title="Zone"),
        )
        st.plotly_chart(fig_pk, use_container_width=True)

    with sl_right:
        y_slice = st.select_slider(
            "Cross-range y [m]",
            options=slider_opts,
            value=0.0,
            format_func=lambda v: f"{v:+.1f} m",
            key="y_slice",
        )
        line_x, pk_total_y, pk_by_zone_y = _compute_zone_line(
            result_zones["zones"], angle_of_fall, h_b, posture,
            result_zones["drag_lam_grid"], result_zones["m_grid"],
            spray_half_angle, max_radius, fixed_axis="y", fixed_coord=float(y_slice),
        )
        fig_pk_down = go.Figure()
        for zn, pk_line in pk_by_zone_y.items():
            fig_pk_down.add_trace(go.Scatter(
                x=line_x, y=pk_line,
                mode="lines",
                line=dict(color=zone_colors.get(zn, "#888"), width=1.5, dash="dash"),
                name=zn,
            ))
        fig_pk_down.add_trace(go.Scatter(
            x=line_x, y=pk_total_y,
            mode="lines",
            line=dict(color="black", width=2.5),
            name="total",
        ))
        fig_pk_down.update_layout(
            title=f"P(kill) vs Downrange  (y = {y_slice:+.1f} m)",
            xaxis_title="Downrange  x  [m]",
            yaxis=dict(title="P(kill)", range=[0, 1]),
            height=360,
            margin=dict(t=40, b=40, l=60, r=20),
            legend=dict(title="Zone"),
        )
        st.plotly_chart(fig_pk_down, use_container_width=True)

    # --- Two-column cross-sections ---
    xsec_left, xsec_right = st.columns(2)
    with xsec_left:
        st.plotly_chart(
            _plotly_elevation_across(zones_obj, float(angle_of_fall), h_b, float(y_slice),
                                     spray_half_angle_deg=float(spray_half_angle)),
            use_container_width=True,
        )
    with xsec_right:
        st.plotly_chart(
            _plotly_elevation(zones_obj, float(angle_of_fall), h_b, float(x_slice),
                              spray_half_angle_deg=float(spray_half_angle)),
            use_container_width=True,
        )
