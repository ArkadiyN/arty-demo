"""Confirm the shipped (c, k) pair reaches ShellParams.aspect_ratio, and print
the before/after A_eff / mu / N0 table.

Consumer: experiment/fragmentation-field/updates/breadth-variance-factor-k/
derivation.md sec. 5.1 (the shipped column) and the src/ implementation pass's
before/after summary. Checks that

    ShellParams.aspect_ratio == 1.6 * MOTT_ASPECT_MOMENT_C[shell] * MOTT_BREADTH_VARIANCE_K

for every registry entry, that mu scales exactly as A_eff and N0 as 1/A_eff.

Run: uv run python experiment/fragmentation-field/updates/breadth-variance-factor-k/checks/aspect-pair-shipped-values.py
"""

from dataclasses import replace

from arty.fragmentation import (
    MOTT_ASPECT_MOMENT_C,
    MOTT_BREADTH_VARIANCE_K,
    _MOTT_ASPECT_RATIO,
    gurney_velocity,
    mott_aspect_ratio,
    mott_params,
)
from arty.shells import SHELLS

# Values shipped before this change (mass-dependent-fragment-shape update):
# c only, no k. derivation.md sec. 3.0 table, column "c shipped (1943 spectrum)".
C_PREV = {
    "155mm M107 HE": 1.2506,
    "105mm M1 HE": 1.1024,
    "75mm M48 HE": 0.9854,
    "60mm M49A2 HE": 0.9200,
}

print(f"A = {_MOTT_ASPECT_RATIO}, k = MOTT_BREADTH_VARIANCE_K = {MOTT_BREADTH_VARIANCE_K}")
print()
hdr = f"{'shell':<16} {'c_prev':>7} {'c_new':>7} {'A_prev':>7} {'A_new':>7} {'dA %':>7} " \
      f"{'mu_prev [gr]':>12} {'mu_new [gr]':>11} {'N0_prev':>8} {'N0_new':>8}"
print(hdr)
print("-" * len(hdr))

GR = 6.479891e-5  # kg per grain

for name, shell in SHELLS.items():
    c_new = MOTT_ASPECT_MOMENT_C[name]
    a_new = mott_aspect_ratio(name)
    # the registry entry must actually carry the pair
    assert abs(shell.aspect_ratio - a_new) < 1e-12, (name, shell.aspect_ratio, a_new)
    assert abs(a_new - _MOTT_ASPECT_RATIO * c_new * MOTT_BREADTH_VARIANCE_K) < 1e-12

    c_prev = C_PREV[name]
    a_prev = _MOTT_ASPECT_RATIO * c_prev

    v0 = gurney_velocity(shell)
    mu_new, n0_new = mott_params(shell, v0)[:2]
    prev_shell = replace(shell, aspect_ratio=a_prev)
    mu_prev, n0_prev = mott_params(prev_shell, gurney_velocity(prev_shell))[:2]

    # mu ~ A_eff exactly, N0 ~ 1/A_eff exactly
    assert abs(mu_new / mu_prev - a_new / a_prev) < 1e-9, name
    assert abs(n0_new / n0_prev - a_prev / a_new) < 1e-6, name

    print(f"{name:<16} {c_prev:7.4f} {c_new:7.4f} {a_prev:7.3f} {a_new:7.3f} "
          f"{100 * (a_new / a_prev - 1):+7.1f} {mu_prev / GR:12.2f} {mu_new / GR:11.2f} "
          f"{n0_prev:8.0f} {n0_new:8.0f}")

print()
print("OK: every registry aspect_ratio == 1.6 * c(shell) * k; mu ~ A_eff, N0 ~ 1/A_eff.")
