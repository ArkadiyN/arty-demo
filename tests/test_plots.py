r"""Tests for src/arty/plots.py

plots.py is a thin presentation layer: it computes no physics beyond trivial
re-evaluation of functions defined elsewhere in arty. These tests therefore
split into two goals:

Delegation guard (fig_zone_elevation projection)
================================================
fig_zone_elevation once inlined its own AoF velocity-projection trig instead
of calling arty.zones.fragment_velocity (the single source of the ray-direction
formula). This was a layering / duplication defect, NOT a numerical one: the
inlined expression was bit-identical to fragment_velocity's output at φ=±90°,
so it produced exactly the same rendered rays. A test that merely compares the
drawn impacts to a fresh fragment_velocity call therefore cannot tell "calls
fragment_velocity" apart from "duplicates the identical formula inline" — it
passes either way.

The guard that actually enforces the invariant monkeypatches
arty.plots.fragment_velocity with a sentinel and checks the rendered rays flow
through it:

  • test_..._delegates_to_fragment_velocity — patch fragment_velocity to a
    constant sentinel direction; the projection is sourced from that patched
    function (it is called with φ=±90° and the caller's AoF, and every drawn
    ray reflects the sentinel). Re-inlining the trig ignores the patch and
    breaks this — which the pure-number comparison could not detect.
  • test_..._impacts_consistent_with_fragment_velocity — a correctness (not
    delegation) check: drawn impacts equal fragment_velocity's prediction.
    On its own it would pass against an inline duplicate; it guards numeric
    correctness, not layering.
  • Doubling h_b doubles every drawn impact x-coordinate (straight-line
    kinematics: x_hit = vgx · h_b / (−vgz)).

Smoke coverage (all chart-producing functions)
==============================================
Every fig_* entry point is called with minimal valid inputs and asserted to
return a Figure without raising, so a future change that breaks a chart is
caught rather than silently shipped.
"""

import matplotlib

matplotlib.use("Agg")  # headless: no display needed for figure construction

import matplotlib.pyplot as plt
import numpy as np
import pytest

from arty import plots
from arty.fragmentation import DragParams
from arty.shells import SHELLS
from arty.zones import compute_shell_zones, fragment_velocity


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def m1_zones():
    return compute_shell_zones(SHELLS["105mm M1 HE"])


@pytest.fixture(autouse=True)
def _close_figs():
    """Free every figure a test creates so the suite does not leak memory."""
    yield
    plt.close("all")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _drawn_impact_xs(fig: plt.Figure) -> list[float]:
    """Ground-impact x-coords of the elevation rays drawn on a figure.

    Elevation impact rays are the only Line2D artists that start at the burst
    point (0, h_b) and terminate on the ground (z ≈ 0). The ground fill,
    axhline, burst markers and dashed upward arrows are excluded by that
    two-endpoint signature.
    """
    ax = fig.axes[0]
    xs = []
    for line in ax.lines:
        xd, yd = np.asarray(line.get_xdata()), np.asarray(line.get_ydata())
        if len(xd) != 2:
            continue
        # starts at burst (x=0, z=h_b>0), ends on the ground (z≈0)
        if abs(xd[0]) < 1e-9 and yd[0] > 1e-6 and abs(yd[1]) < 1e-9:
            xs.append(float(xd[1]))
    return sorted(xs)


def _expected_impact_xs(zones, aof_deg: float, h_b: float) -> list[float]:
    """Impact x-coords predicted by fragment_velocity for the φ=±90° rays."""
    xs = []
    for z in (zones.ogive, zones.cylinder, zones.boattail, zones.base):
        if z.mass_kg <= 1e-6:
            continue
        for phi_sign in (1, -1):
            vgx, _vgy, vgz = fragment_velocity(z.spray_deg, phi_sign * np.pi / 2, aof_deg)
            if vgz < -1e-6:  # only downward rays reach the ground
                xs.append(vgx * h_b / (-vgz))
    return sorted(xs)


# ---------------------------------------------------------------------------
# Delegation guard — fig_zone_elevation must SOURCE its projection from
# fragment_velocity, not re-derive it inline
# ---------------------------------------------------------------------------


def _nonempty_zone_count(zones) -> int:
    return sum(
        1
        for z in (zones.ogive, zones.cylinder, zones.boattail, zones.base)
        if z.mass_kg > 1e-6
    )


def test_zone_elevation_delegates_to_fragment_velocity(m1_zones, monkeypatch):
    """fig_zone_elevation's projection must flow through fragment_velocity.

    This is the real regression guard for the b37d515-class duplication bug.
    We patch arty.plots.fragment_velocity with a constant downward sentinel
    (vgx, vgy, vgz) = (1, 0, −1); every ray then lands at
    x = vgx·h_b/(−vgz) = h_b. If the projection is re-inlined the patch is
    ignored and the drawn impacts revert to the real, per-zone-varied values —
    which a plain number-vs-fragment_velocity comparison could not catch,
    because the inline formula is bit-identical to fragment_velocity's output.
    """
    aof_deg, h_b = 30.0, 2.0
    calls: list[tuple[float, float, float]] = []

    def sentinel_fv(theta_z_deg, phi_rad, aof):
        calls.append((theta_z_deg, phi_rad, aof))
        return (1.0, 0.0, -1.0)

    monkeypatch.setattr(plots, "fragment_velocity", sentinel_fv)
    fig = plots.fig_zone_elevation(m1_zones, aof_deg=aof_deg, h_b=h_b, r_person=30.0)

    # (1) It is actually called — once per (zone, φ=±90°) ray.
    assert calls, "fig_zone_elevation must call fragment_velocity, not inline the trig"
    assert len(calls) == 2 * _nonempty_zone_count(m1_zones)

    # (2) Called with the right arguments: φ=±90° and the caller's AoF verbatim.
    for _theta, phi_rad, aof in calls:
        assert abs(abs(phi_rad) - np.pi / 2) < 1e-12
        assert aof == aof_deg

    # (3) The rendered output flows through the patched function: with the
    #     sentinel direction every drawn impact sits at x = h_b.
    drawn = _drawn_impact_xs(fig)
    assert drawn, "sentinel direction is downward — impacts must be drawn"
    np.testing.assert_allclose(drawn, [h_b] * len(drawn), rtol=1e-9, atol=1e-9)


def test_zone_elevation_impacts_consistent_with_fragment_velocity(m1_zones):
    """Correctness (not delegation) check: drawn impacts equal fragment_velocity.

    On its own this would pass against an inline duplicate of the formula; it
    guards numeric correctness of the rendered rays, while
    test_zone_elevation_delegates_to_fragment_velocity guards the layering.
    """
    aof_deg, h_b = 30.0, 2.0
    fig = plots.fig_zone_elevation(m1_zones, aof_deg=aof_deg, h_b=h_b, r_person=30.0)

    drawn = _drawn_impact_xs(fig)
    expected = _expected_impact_xs(m1_zones, aof_deg, h_b)

    assert expected, "test setup: expected at least one downward ray"
    assert len(drawn) == len(expected)
    np.testing.assert_allclose(drawn, expected, rtol=1e-9, atol=1e-9)


def test_zone_elevation_impacts_scale_linearly_with_h_b(m1_zones):
    aof_deg = 30.0
    xs_1 = _drawn_impact_xs(plots.fig_zone_elevation(m1_zones, aof_deg=aof_deg, h_b=2.0))
    xs_2 = _drawn_impact_xs(plots.fig_zone_elevation(m1_zones, aof_deg=aof_deg, h_b=4.0))

    assert xs_1 and len(xs_1) == len(xs_2)
    np.testing.assert_allclose(xs_2, [2.0 * x for x in xs_1], rtol=1e-9, atol=1e-9)


# ---------------------------------------------------------------------------
# Smoke coverage — every chart-producing function returns a Figure
# ---------------------------------------------------------------------------


def test_apply_style_runs():
    plots.apply_style()  # mutates rcParams; must not raise


def test_fig_mott_distribution(m1_zones):
    fig = plots.fig_mott_distribution(N0=1000.0, mu=5e-3)
    assert isinstance(fig, plt.Figure)


def test_fig_ke_vs_range():
    fig = plots.fig_ke_vs_range(V0=1200.0, drag=DragParams(), rho_steel=7850.0)
    assert isinstance(fig, plt.Figure)


def test_fig_frag_field():
    r = np.linspace(1.0, 200.0, 40)
    N_eff = 500.0 * np.exp(-r / 50.0)
    P = 1.0 - np.exp(-N_eff / 100.0)
    fig = plots.fig_frag_field(r, N_eff, P, R50=60.0, N0=1000.0, V0=1200.0, mu=5e-3)
    assert isinstance(fig, plt.Figure)


def test_fig_cross_section():
    fig = plots.fig_cross_section()
    assert isinstance(fig, plt.Figure)


def test_fig_field_map_2d():
    r_2d = np.linspace(0.5, 150.0, 60)
    P_grid = 1.0 - np.exp(-((150.0 - r_2d) / 60.0))
    fig = plots.fig_field_map_2d(r_2d, P_grid, R50=60.0)
    assert isinstance(fig, plt.Figure)


def test_fig_four_zone_field():
    x = np.linspace(-40.0, 40.0, 25)
    y = np.linspace(-40.0, 40.0, 25)
    X, Y = np.meshgrid(x, y)
    P = 0.5 * np.exp(-(X**2 + Y**2) / 400.0)
    fig = plots.fig_four_zone_field(X, Y, P)
    assert isinstance(fig, plt.Figure)


def test_fig_lethal_density_field():
    x = np.linspace(-40.0, 40.0, 25)
    y = np.linspace(-40.0, 40.0, 25)
    X, Y = np.meshgrid(x, y)
    rho = 10.0 * np.exp(-(X**2 + Y**2) / 200.0)
    fig = plots.fig_lethal_density_field(X, Y, rho, title="test field")
    assert isinstance(fig, plt.Figure)


def test_fig_lethal_density_field_all_zero():
    """Degenerate all-zero field draws an empty frame rather than raising."""
    X, Y = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
    fig = plots.fig_lethal_density_field(X, Y, np.zeros_like(X), title="zero")
    assert isinstance(fig, plt.Figure)


def test_fig_pkill_volume():
    go = pytest.importorskip("plotly.graph_objects")
    ax = np.linspace(-20.0, 20.0, 8)
    X, Y, Z = np.meshgrid(ax, ax, np.linspace(0.0, 10.0, 6), indexing="ij")
    P_k = 0.5 * np.exp(-(X**2 + Y**2 + Z**2) / 200.0)
    fig = plots.fig_pkill_volume(X, Y, Z, P_k, title="test volume")
    assert isinstance(fig, go.Figure)


def test_fig_single_zone_elevation():
    fig = plots.fig_single_zone_elevation()
    assert isinstance(fig, plt.Figure)


def test_fig_zone_elevation(m1_zones):
    fig = plots.fig_zone_elevation(m1_zones)
    assert isinstance(fig, plt.Figure)


def test_fig_zone_footprint(m1_zones):
    fig = plots.fig_zone_footprint(m1_zones)
    assert isinstance(fig, plt.Figure)
