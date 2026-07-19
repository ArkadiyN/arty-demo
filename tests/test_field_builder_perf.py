r"""Wall-clock regression budgets for the vectorised field/volume builders.

These guard the field-builder-performance refactor
(updates/field-builder-performance/derivation.md §6) against a regression back
to the old per-cell Python loops, whose cost was one to two orders of magnitude
larger on the headline cases that motivated the work: the detailed four-zone
ground field (n=300, 90 000 columns, ~10 s → ~1.2 s), the P(kill) / lethal-
density volume builders (~7.8 s → ~75 ms), and the large 2D density fields
(~0.43 s → ~5 ms).

**Opt-in.** This module is marked ``perf`` and is *deselected by default*
(``addopts = -m 'not perf'`` in pyproject.toml) so ``uv run pytest`` stays fast.
Run it explicitly with::

    uv run pytest -m perf

Budgets are set with large headroom (≈5–50×) over the refactored timings
recorded in derivation.md §6 so CI machine variance never flakes them, while
still sitting *below* the old order-of-magnitude cost so a true regression trips
them. Each case is timed after one warm-up call (excludes import / first-touch
allocation) and asserts a single-call wall-clock budget.
"""

import time

import numpy as np
import pytest

from arty.fragmentation import (
    STANDING,
    BurstParams,
    DragParams,
    pkill_volume_3d,
)
from arty.shells import SHELLS
from arty.zones import (
    compute_shell_zones,
    four_zone_lethal_density_field,
    four_zone_lethal_density_volume,
    four_zone_pkill_field,
    four_zone_pkill_volume,
)

pytestmark = pytest.mark.perf

DRAG = DragParams()
SHELL = SHELLS["155mm M107 HE"]
ZONES = compute_shell_zones(SHELL)
RHO_STEEL = SHELL.steel.rho
AOF, H_B, DELTA = 30.0, 2.0, 15.0


def _wall_clock(fn):
    """Return single-call wall-clock [s] after one warm-up call."""
    fn()  # warm-up: exclude first-touch allocation / caches
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def test_perf_four_zone_pkill_volume():
    """Four-zone P(kill) volume (the 7.8 s → 74 ms motivating case)."""
    def call():
        return four_zone_pkill_volume(
            ZONES, AOF, H_B, DRAG, RHO_STEEL,
            z_max=10.0, max_r=40.0, n_grid=40, n_z=30, delta_deg=DELTA,
        )
    dt = _wall_clock(call)
    assert dt < 3.0, f"four_zone_pkill_volume took {dt*1e3:.0f} ms (budget 3000 ms)"


def test_perf_four_zone_lethal_density_volume():
    """Four-zone lethal-density volume (7.7 s → 75 ms)."""
    def call():
        return four_zone_lethal_density_volume(
            ZONES, AOF, H_B, DRAG, RHO_STEEL,
            z_max=10.0, max_r=40.0, n_grid=40, n_z=30, delta_deg=DELTA,
        )
    dt = _wall_clock(call)
    assert dt < 3.0, f"four_zone_lethal_density_volume took {dt*1e3:.0f} ms (budget 3000 ms)"


def test_perf_single_zone_pkill_volume():
    """Single-zone P(kill) volume (2.0 s → 20 ms)."""
    burst = BurstParams(h_b=H_B, angle_of_fall=AOF, spray_half_angle=DELTA)
    def call():
        return pkill_volume_3d(
            SHELL, DRAG, burst, z_max=10.0, max_radius=40.0, n_grid=40, n_z=30,
        )
    dt = _wall_clock(call)
    assert dt < 1.0, f"pkill_volume_3d took {dt*1e3:.0f} ms (budget 1000 ms)"


def test_perf_detailed_four_zone_pkill_field():
    """Detailed four-zone ground P(kill) field, n=300 / 90 000 columns
    (the app's max-slider case, ~10 s → ~1.2 s)."""
    def call():
        return four_zone_pkill_field(
            ZONES, AOF, H_B, DRAG, RHO_STEEL, STANDING,
            max_r=60.0, n_grid=300, delta_deg=DELTA,
        )
    dt = _wall_clock(call)
    assert dt < 7.0, f"four_zone_pkill_field n=300 took {dt*1e3:.0f} ms (budget 7000 ms)"


def test_perf_four_zone_lethal_density_field():
    """Four-zone lethal-density field, n=150 (0.43 s → 4.6 ms)."""
    def call():
        return four_zone_lethal_density_field(
            ZONES, AOF, H_B, DRAG, RHO_STEEL,
            z=0.5, max_r=60.0, n_grid=150, delta_deg=DELTA,
        )
    dt = _wall_clock(call)
    assert dt < 0.3, f"four_zone_lethal_density_field took {dt*1e3:.0f} ms (budget 300 ms)"


def test_perf_default_run_excludes_this_module():
    """Sanity marker so the file self-documents its opt-in nature: this test
    only runs under `-m perf`, confirming the default suite skips the budgets."""
    assert np.True_  # trivially true; presence under `-m perf` is the point
