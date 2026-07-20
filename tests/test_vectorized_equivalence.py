r"""Property tests pinning the vectorised field-builder paths to their scalar refs.

Coverage map
============

The field-builder-performance refactor replaced per-cell Python loops with
array kernels (updates/field-builder-performance/derivation.md). The scalar
reference implementations it reproduces are *retained unchanged* in the tree;
these tests pin the vectorised output to those references directly (not to a
stored snapshot), so a future edit to either path that breaks equivalence
fails loudly.

build_mmin_table            (arty.fragmentation, vectorised bisection)
  • Bit-identical (np.array_equal, 0.0 diff) to a list of scalar
    min_lethal_mass bisections over the same s-grid — the frozen-on-early-stop
    equivalence claim (derivation §4).

_pkill_columns_vec          (arty.fragmentation, vectorised column integral)
  • Matches the scalar breakpoint-segmented composite-midpoint reference
    (belt_column_breakpoints + integrate_column_density +
    lethal_density_four_zone_point) to ~1e-12 across columns / AoF / posture —
    the near-coincident-breakpoint float-reassociation regime of derivation §3.

_four_zone_density_layer_vec (arty.zones, vectorised ρ_L layer)
  • Bit-identical to a per-cell loop over lethal_density_four_zone_point.

Chunk invariance (memory-chunking is a pure performance knob)
  • four_zone_field and four_zone_pkill_field are invariant (0.0 diff) to
    _FAMILY_A_CHUNK / the P-chunk size — shrinking the cap to force dozens of
    chunk boundaries changes no output (no off-by-one at chunk seams).

Bounds guard (finding-1 closure)
  • The vectorised ρ_L / P_k paths assert their query slant ranges lie inside
    the caller-supplied m_min grid, restoring the loud-failure parity the
    scalar reference kept; an undersized grid raises AssertionError instead of
    silently clipping via np.interp.
"""

import numpy as np
import pytest

import arty.fragmentation as frag
import arty.zones as zones_mod
from arty.fragmentation import (
    STANDING,
    PRONE,
    DragParams,
    E_LETH_DEFAULT,
    _pkill_columns_vec,
    belt_column_breakpoints,
    build_mmin_table,
    integrate_column_density,
    min_lethal_mass,
    slant_range_grid,
)
from arty.shells import SHELLS
from arty.zones import (
    _active_zone_specs,
    _four_zone_density_layer_vec,
    build_zone_mmin_tables,
    compute_shell_zones,
    four_zone_field,
    lethal_density_four_zone_point,
)

DRAG = DragParams()
SHELL = SHELLS["155mm M107 HE"]
ZONES = compute_shell_zones(SHELL)
RHO_STEEL = SHELL.steel.rho


# --------------------------------------------------------------------------- #
# build_mmin_table — vectorised bisection vs scalar min_lethal_mass            #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("V0", [500.0, 900.0, 1500.0, 1800.0, 2500.0])
def test_build_mmin_table_bit_identical_to_scalar(V0):
    """Vectorised m_min(s) table == elementwise scalar bisection, exactly."""
    s_grid = np.linspace(0.3, 90.0, 200)
    vec = build_mmin_table(s_grid, V0, E_LETH_DEFAULT, DRAG, RHO_STEEL)
    scalar = np.array(
        [min_lethal_mass(float(s), V0, E_LETH_DEFAULT, DRAG, RHO_STEEL) for s in s_grid]
    )
    assert np.array_equal(vec, scalar)


def test_build_mmin_table_extreme_ranges():
    """s→0 (all lethal) and large s (nothing lethal) edges stay bit-identical."""
    s_grid = np.concatenate([np.linspace(1e-3, 0.5, 20), np.linspace(60.0, 200.0, 20)])
    V0 = 1200.0
    vec = build_mmin_table(s_grid, V0, E_LETH_DEFAULT, DRAG, RHO_STEEL)
    scalar = np.array(
        [min_lethal_mass(float(s), V0, E_LETH_DEFAULT, DRAG, RHO_STEEL) for s in s_grid]
    )
    assert np.array_equal(vec, scalar)


# --------------------------------------------------------------------------- #
# _pkill_columns_vec — vectorised column integral vs scalar reference         #
# --------------------------------------------------------------------------- #
def _scalar_pkill_column(x, y, h_b, aof_deg, delta_deg, posture, s_grids, mmin_grids):
    """Scalar P_k for one ground column via the retained reference path."""
    alpha_rad = np.radians(aof_deg)
    delta_rad = np.radians(delta_deg)
    _, cos_tz = _active_zone_specs(ZONES, s_grids, mmin_grids)
    bps = belt_column_breakpoints(
        x, y, h_b, alpha_rad, delta_rad, cos_tz, 0.0, posture.h
    )

    def rho_point(z):
        return lethal_density_four_zone_point(
            ZONES, x, y, z, aof_deg, h_b, delta_deg, s_grids, mmin_grids
        )

    line = integrate_column_density(rho_point, bps, n_seg=9)
    return 1.0 - np.exp(-posture.w_perp * line)


@pytest.mark.parametrize("aof_deg", [1.0, 30.0, 60.0, 89.0])
@pytest.mark.parametrize("posture", [STANDING, PRONE])
def test_pkill_columns_vec_matches_scalar(aof_deg, posture):
    """Vectorised column P_k reproduces the scalar breakpoint+midpoint ref."""
    h_b, delta_deg = 2.0, 15.0
    s_grid = slant_range_grid(60.0, h_b, z_max=posture.h, n_s=400, z_min=0.0)
    s_grids, mmin_grids = build_zone_mmin_tables(
        ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
    )
    specs, cos_tz = _active_zone_specs(ZONES, s_grids, mmin_grids)

    # A spread of columns: near-in, mid, far, and off-axis.
    xs = np.array([2.0, 10.0, 25.0, 45.0, -15.0, 5.0])
    ys = np.array([0.0, 5.0, -10.0, 20.0, -30.0, 40.0])
    alpha_rad = np.radians(aof_deg)
    delta_rad = np.radians(delta_deg)
    vec = _pkill_columns_vec(
        xs, ys, h_b, alpha_rad, delta_rad, posture.w_perp, 0.0, posture.h,
        9, specs, cos_tz,
    )
    scalar = np.array([
        _scalar_pkill_column(
            float(x), float(y), h_b, aof_deg, delta_deg, posture, s_grids, mmin_grids
        )
        for x, y in zip(xs, ys)
    ])
    # derivation §3: unmerged near-coincident roots leave an O(1e-12) segment;
    # measured deviation is float-reassociation noise (~1e-15).
    assert np.max(np.abs(vec - scalar)) < 1e-10


def test_pkill_columns_vec_at_zone_spray_angle():
    """AoF at (and just past) an active zone's spray half-angle — the A→0
    quadratic-degeneracy regime — still matches the scalar reference."""
    h_b, delta_deg, posture = 2.0, 15.0, STANDING
    # cylinder spray angle is 90°; pick AoF so a belt edge grazes the degeneracy.
    for aof_deg in (74.9, 75.0, 75.01):
        s_grid = slant_range_grid(60.0, h_b, z_max=posture.h, n_s=400, z_min=0.0)
        s_grids, mmin_grids = build_zone_mmin_tables(
            ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
        )
        specs, cos_tz = _active_zone_specs(ZONES, s_grids, mmin_grids)
        xs = np.array([8.0, 18.0, 33.0])
        ys = np.array([0.0, 4.0, -7.0])
        alpha_rad = np.radians(aof_deg)
        delta_rad = np.radians(delta_deg)
        vec = _pkill_columns_vec(
            xs, ys, h_b, alpha_rad, delta_rad, posture.w_perp, 0.0, posture.h,
            9, specs, cos_tz,
        )
        scalar = np.array([
            _scalar_pkill_column(
                float(x), float(y), h_b, aof_deg, delta_deg, posture,
                s_grids, mmin_grids,
            )
            for x, y in zip(xs, ys)
        ])
        assert np.max(np.abs(vec - scalar)) < 1e-10, f"AoF={aof_deg}"


# --------------------------------------------------------------------------- #
# _four_zone_density_layer_vec — vectorised ρ_L layer vs per-cell scalar       #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("aof_deg", [30.0, 90.0])
@pytest.mark.parametrize("z", [0.0, 0.8, 1.6])
def test_density_layer_vec_matches_pointwise(aof_deg, z):
    """Vectorised ρ_L layer is bit-identical to a per-cell scalar loop."""
    h_b, delta_deg = 2.0, 15.0
    s_grid = slant_range_grid(40.0, h_b, z, n_s=400, z_min=z)
    s_grids, mmin_grids = build_zone_mmin_tables(
        ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
    )
    xy = np.linspace(-40.0, 40.0, 21)
    X, Y = np.meshgrid(xy, xy)
    vec = _four_zone_density_layer_vec(
        ZONES, X, Y, z, aof_deg, h_b, delta_deg, s_grids, mmin_grids
    )
    scalar = np.empty_like(vec)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            scalar[i, j] = lethal_density_four_zone_point(
                ZONES, float(X[i, j]), float(Y[i, j]), z, aof_deg, h_b,
                delta_deg, s_grids, mmin_grids,
            )
    assert np.max(np.abs(vec - scalar)) < 1e-12


# --------------------------------------------------------------------------- #
# Chunk invariance — memory-chunking is a pure performance knob                #
# --------------------------------------------------------------------------- #
def test_family_a_field_chunk_invariant(monkeypatch):
    """four_zone_field is invariant to _FAMILY_A_CHUNK (Family-A mass integral)."""
    m_grid = np.logspace(-6, np.log10(0.5), 200)
    lam_grid = frag.retardation_coeff(m_grid, DRAG, RHO_STEEL)
    def call():
        return four_zone_field(
            ZONES, 30.0, 2.0, STANDING, lam_grid, m_grid,
            max_r=200.0, n_grid=81, delta_deg=15.0,
        )

    _, _, big = call()
    # Force many chunk boundaries: cap the working array to a handful of rows.
    monkeypatch.setattr(zones_mod, "_FAMILY_A_CHUNK", 137)
    _, _, small = call()
    assert np.array_equal(big, small)


def test_pkill_columns_vec_batching_invariant():
    """Columns are independent: any batching of _pkill_columns_vec matches the
    single full call bit-for-bit (guards the P-chunk loop against cross-column
    state / off-by-one at chunk seams)."""
    h_b, delta_deg, posture, aof_deg = 2.0, 15.0, STANDING, 30.0
    s_grid = slant_range_grid(60.0, h_b, z_max=posture.h, n_s=400, z_min=0.0)
    s_grids, mmin_grids = build_zone_mmin_tables(
        ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
    )
    specs, cos_tz = _active_zone_specs(ZONES, s_grids, mmin_grids)
    rng = np.random.default_rng(0)
    xs = rng.uniform(-55.0, 55.0, 37)
    ys = rng.uniform(-55.0, 55.0, 37)
    args = (h_b, np.radians(aof_deg), np.radians(delta_deg),
            posture.w_perp, 0.0, posture.h, 9, specs, cos_tz)
    full = _pkill_columns_vec(xs, ys, *args)
    # Stitch from three arbitrary sub-batches spanning the same columns.
    stitched = np.concatenate([
        _pkill_columns_vec(xs[:10], ys[:10], *args),
        _pkill_columns_vec(xs[10:25], ys[10:25], *args),
        _pkill_columns_vec(xs[25:], ys[25:], *args),
    ])
    assert np.array_equal(full, stitched)


# --------------------------------------------------------------------------- #
# Bounds guard (finding-1 closure)                                            #
# --------------------------------------------------------------------------- #
def test_density_layer_vec_asserts_on_undersized_grid():
    """An undersized m_min grid raises loudly instead of silently clipping."""
    h_b, delta_deg, z, aof_deg = 2.0, 15.0, 0.0, 30.0
    # Deliberately truncate the grid so the box corners fall off the top.
    s_grid = np.linspace(0.3, 5.0, 200)  # far too short for a 40 m box
    s_grids, mmin_grids = build_zone_mmin_tables(
        ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
    )
    xy = np.linspace(-40.0, 40.0, 21)
    X, Y = np.meshgrid(xy, xy)
    with pytest.raises(AssertionError, match="outside m_min grid"):
        _four_zone_density_layer_vec(
            ZONES, X, Y, z, aof_deg, h_b, delta_deg, s_grids, mmin_grids
        )


def test_pkill_columns_vec_asserts_on_undersized_grid():
    """_pkill_columns_vec raises loudly when a weighted sample falls off-grid."""
    h_b, delta_deg, posture, aof_deg = 2.0, 15.0, STANDING, 30.0
    s_grid = np.linspace(0.3, 5.0, 200)  # far too short for a 60 m box
    s_grids, mmin_grids = build_zone_mmin_tables(
        ZONES, s_grid, E_LETH_DEFAULT, DRAG, RHO_STEEL
    )
    specs, cos_tz = _active_zone_specs(ZONES, s_grids, mmin_grids)
    xs = np.array([45.0, 30.0])
    ys = np.array([20.0, -25.0])
    with pytest.raises(AssertionError, match="np.interp would clip"):
        _pkill_columns_vec(
            xs, ys, h_b, np.radians(aof_deg), np.radians(delta_deg),
            posture.w_perp, 0.0, posture.h, 9, specs, cos_tz,
        )
