import numpy as np
import plotly.graph_objects as go
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

    shell_name = st.selectbox("Shell preset", list(SHELLS.keys()))
    preset = SHELLS[shell_name]

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
            "Belt half-angle  δ  [°]", 5, 30, int(BurstParams().spray_half_angle), step=1
        )

    with st.expander("Target"):
        posture_name = st.radio("Posture", ["Standing", "Prone"], index=0)

    max_radius = st.slider("Analysis radius  [m]", 40.0, 200.0, 80.0, step=10.0)

# ---------------------------------------------------------------------------
# Build param structs
# ---------------------------------------------------------------------------

steel = SteelParams(
    name=preset.steel.name,
    rho=rho_steel,
    sigma_f=sigma_f * 1e6,
    gamma=gamma,
)
shell = ShellParams(
    caliber=caliber_mm / 1e3,
    wall_t=wall_t_mm / 1e3,
    mass_total=mass_total,
    mass_filler=mass_filler,
    mass_deductions=preset.mass_deductions,
    filler=filler,
    steel=steel,
)
drag = DragParams(C_D=C_D, rho_air=rho_air)
burst = BurstParams(h_b=h_b, angle_of_fall=float(angle_of_fall), spray_half_angle=float(spray_half_angle))
posture: PostureParams = STANDING if posture_name == "Standing" else PRONE

# ---------------------------------------------------------------------------
# Compute (cached)
# ---------------------------------------------------------------------------


@st.cache_data
def _compute(shell, drag, burst, posture, max_radius):
    return compute_frag_field_3d(shell, drag, burst, posture, max_radius=max_radius)


result = _compute(shell, drag, burst, posture, max_radius)

# ---------------------------------------------------------------------------
# Headline metrics
# ---------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)
col1.metric("R₅₀ (cross-range)", f"{result.r50_cross:.0f} m")
col2.metric("V₀", f"{result.V0:.0f} m/s")
col3.metric("N₀ (total frags)", f"{result.N0:.0f}")
col4.metric("μ (half-mass)", f"{result.mu * 1e3:.2f} g")

st.divider()

# ---------------------------------------------------------------------------
# Figures — 2×2 grid
# ---------------------------------------------------------------------------

left, right = st.columns(2)

# Figure 1 — Mott cumulative distribution
with left:
    m_vals = np.logspace(np.log10(0.01), np.log10(150), 300)  # grams, 10 mg–150 g
    n_vals = result.N0 * np.exp(-np.sqrt(m_vals * 1e-3 / result.mu))
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
            range=[0, np.log10(result.N0 * 2)],
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
    for (m_g, ke_arr), colour in zip(result.ke_by_mass.items(), colours):
        fig2.add_trace(
            go.Scatter(
                x=result.r_ke,
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
                x=[result.r_ke[0], result.r_ke[-1]],
                y=[y_ref, y_ref],
                mode="lines",
                line=dict(dash="dot", color="gray", width=1),
                showlegend=False,
            )
        )
        fig2.add_annotation(
            x=result.r_ke[-1],
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

# Figure 3 — 2D fragmentation field (asymmetric footprint)
fig3 = go.Figure()
fig3.add_trace(
    go.Heatmap(
        x=result.field_x[0],
        y=result.field_y[:, 0],
        z=result.field_pk,
        colorscale="RdYlGn_r",
        zmin=0,
        zmax=1,
        colorbar=dict(title="P(kill)"),
    )
)
fig3.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        marker=dict(symbol="cross", size=12, color="black"),
        name="Burst point",
        showlegend=False,
    )
)
fig3.update_layout(
    title=f"2D Fragmentation Field  ·  R₅₀ = {result.r50_cross:.0f} m",
    xaxis=dict(title="Downrange  x  [m]", scaleanchor="y"),
    yaxis_title="Cross-range  y  [m]",
    height=500,
    margin=dict(t=40, b=40, l=60, r=20),
)
st.plotly_chart(fig3, use_container_width=True)
