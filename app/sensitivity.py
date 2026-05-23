import numpy as np
import plotly.graph_objects as go
import streamlit as st

from arty.fragmentation import (
    DragParams,
    MottParams,
    ShellParams,
    TargetParams,
    compute_frag_field,
)
from arty.shells import SHELLS

st.set_page_config(page_title="Fragmentation Field — Sensitivity", layout="wide")
st.title("Fragmentation Field Sensitivity")
st.caption("105 mm HE ground burst · Gurney + Mott + ES-310 Pk|hit · flat trajectory")

# ---------------------------------------------------------------------------
# Sidebar — all parameters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Parameters")

    shell_name = st.selectbox("Shell preset", list(SHELLS.keys()))
    preset = SHELLS[shell_name]

    with st.expander("Shell & Explosive", expanded=True):
        gurney_const = st.slider(
            "Gurney constant √(2E)  [m/s]",
            2000.0,
            3200.0,
            float(preset.gurney_const),
            step=10.0,
        )
        mass_total = st.slider(
            "Total projectile mass  [kg]", 5.0, 50.0, float(preset.mass_total), step=0.1
        )
        mass_charge = st.slider(
            "Charge mass  [kg]", 0.5, 12.0, float(preset.mass_charge), step=0.05
        )
        caliber_mm = st.slider(
            "Caliber  [mm]", 75.0, 155.0, float(preset.caliber * 1e3), step=1.0
        )
        wall_t_mm = st.slider(
            "Wall thickness  [mm]", 5.0, 25.0, float(preset.wall_t * 1e3), step=0.5
        )

    with st.expander("Mott Fragmentation"):
        gamma = st.slider(
            "γ (Mott parameter)", 53.0, 80.0, float(MottParams().gamma), step=1.0
        )
        sigma_f = st.slider(
            "σ_F dynamic flow stress  [MPa]",
            600.0,
            1200.0,
            float(MottParams().sigma_f / 1e6),
            step=10.0,
        )
        rho_steel = st.slider(
            "Steel density  [kg/m³]", 7600.0, 8000.0, float(preset.rho_steel), step=10.0
        )

    with st.expander("Drag"):
        C_D = st.slider(
            "C_D (drag coefficient)", 0.40, 0.90, float(DragParams().C_D), step=0.01
        )
        rho_air = st.slider(
            "Air density  [kg/m³]", 0.90, 1.40, float(DragParams().rho_air), step=0.01
        )

    with st.expander("Target"):
        posture = st.radio("Posture", ["Standing (0.5 m)", "Prone (0.25 m)", "Custom"])
        if posture == "Standing (0.5 m)":
            w = 0.5
        elif posture == "Prone (0.25 m)":
            w = 0.25
        else:
            w = st.slider(
                "Presented width  [m]", 0.05, 1.5, float(TargetParams().w), step=0.05
            )

    r_max = st.slider("Max range  [m]", 100.0, 500.0, 300.0, step=10.0)

# ---------------------------------------------------------------------------
# Build param structs
# ---------------------------------------------------------------------------

shell = ShellParams(
    caliber=caliber_mm / 1e3,
    wall_t=wall_t_mm / 1e3,
    mass_total=mass_total,
    mass_charge=mass_charge,
    mass_deductions=preset.mass_deductions,
    gurney_const=gurney_const,
    rho_steel=rho_steel,
)
mott = MottParams(gamma=gamma, sigma_f=sigma_f * 1e6)
drag = DragParams(C_D=C_D, rho_air=rho_air)
target = TargetParams(w=w)

# ---------------------------------------------------------------------------
# Compute (cached)
# ---------------------------------------------------------------------------


@st.cache_data
def _compute(shell, mott, drag, target, r_max):
    return compute_frag_field(shell, mott, drag, target, r_max=r_max)


result = _compute(shell, mott, drag, target, r_max)

# ---------------------------------------------------------------------------
# Headline metrics
# ---------------------------------------------------------------------------

mass_shell = shell.mass_total - shell.mass_charge - shell.mass_deductions
col1, col2, col3, col4 = st.columns(4)
col1.metric("R₅₀", f"{result.r50:.0f} m")
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
    m_vals = np.logspace(-4, np.log10(500), 300)  # grams
    n_vals = result.N0 * np.exp(-np.sqrt(m_vals * 1e-3 / result.mu))
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=m_vals,
            y=n_vals,
            mode="lines",
            line=dict(color="#1f77b4", width=2),
            name="N(>m)",
        )
    )
    fig1.update_layout(
        title="Mott Cumulative Fragment Count",
        xaxis=dict(title="Fragment mass  [g]", type="log"),
        yaxis=dict(title="N fragments with mass ≥ m", type="log"),
        height=340,
        margin=dict(t=40, b=40, l=60, r=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

# Figure 2 — KE vs range
with right:
    fig2 = go.Figure()
    colours = ["#2ca02c", "#ff7f0e", "#d62728"]
    for (m_g, ke_arr), colour in zip(result.ke_by_mass.items(), colours):
        fig2.add_trace(
            go.Scatter(
                x=result.r,
                y=ke_arr,
                mode="lines",
                line=dict(color=colour, width=2),
                name=f"{m_g} g",
            )
        )
    fig2.add_hline(
        y=100,
        line=dict(dash="dot", color="gray"),
        annotation_text="100 J (ES-310 light)",
    )
    fig2.add_hline(
        y=1000,
        line=dict(dash="dot", color="gray"),
        annotation_text="1 kJ (ES-310 moderate)",
    )
    fig2.update_layout(
        title="Fragment KE vs Range",
        xaxis_title="Range  [m]",
        yaxis=dict(title="Kinetic energy  [J]", type="log"),
        height=340,
        margin=dict(t=40, b=40, l=60, r=20),
        legend=dict(title="Mass"),
    )
    st.plotly_chart(fig2, use_container_width=True)

left2, right2 = st.columns(2)

# Figure 3 — p_kill vs range
with left2:
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=result.r,
            y=result.p_kill,
            mode="lines",
            line=dict(color="#9467bd", width=2),
            name="P(kill)",
        )
    )
    fig3.add_vline(
        x=result.r50,
        line=dict(dash="dash", color="#9467bd"),
        annotation_text=f"R₅₀ = {result.r50:.0f} m",
        annotation_position="top right",
    )
    fig3.add_hline(y=0.5, line=dict(dash="dot", color="gray"))
    fig3.update_layout(
        title="P(kill) vs Range",
        xaxis_title="Range  [m]",
        yaxis=dict(title="P(kill)", range=[0, 1]),
        height=340,
        margin=dict(t=40, b=40, l=60, r=20),
    )
    st.plotly_chart(fig3, use_container_width=True)

# Figure 4 — 2D fragmentation field
with right2:
    fig4 = go.Figure()
    fig4.add_trace(
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
    fig4.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(symbol="cross", size=12, color="black"),
            name="Burst point",
            showlegend=False,
        )
    )
    fig4.update_layout(
        title=f"2D Fragmentation Field  ·  R₅₀ = {result.r50:.0f} m",
        xaxis=dict(title="East  [m]", scaleanchor="y"),
        yaxis_title="North  [m]",
        height=340,
        margin=dict(t=40, b=40, l=60, r=20),
    )
    st.plotly_chart(fig4, use_container_width=True)
