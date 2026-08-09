"""Print the current shipped 75mm M48 HE initial-condition figures.

Single source of truth for the stale-citation propagation recorded in
experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/scoping.md §6:
every artifact listed there is brought in line with THIS script's output, not
with a number handed over in prose.

Run: uv run python experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py
"""

from arty.fragmentation import _shell_geometry, gurney_velocity, mott_params
from arty.shells import SHELLS

shell = SHELLS["75mm M48 HE"]
r_o, r_i, r_bu, M_case = _shell_geometry(shell)
V0 = gurney_velocity(shell)
mu, N0 = mott_params(shell, V0)

print("shell             = 75mm M48 HE")
print(f"M_case            = {M_case * 1e3:8.1f} g")
print(f"r_o / r_i / r_bu  = {r_o * 1e3:.2f} / {r_i * 1e3:.2f} / {r_bu * 1e3:.2f} mm")
print(f"V0 (Gurney)       = {V0:8.1f} m/s")
print(f"mu                = {mu * 1e3:8.3f} g")
print(f"2*mu (mean frag)  = {2 * mu * 1e3:8.3f} g")
print(f"N0 = M_case/(2mu) = {N0:8.0f}")

# Superseded pre-fix figures, kept for the propagation audit trail.
OLD = dict(V0=807.5, M_case=5755.2, mu=0.793, N0=3627)
print("\npre-fix -> current (ratio):")
print(f"  V0     {OLD['V0']:8.1f} -> {V0:8.1f}  ({V0 / OLD['V0']:.4f})")
print(f"  M_case {OLD['M_case']:8.1f} -> {M_case * 1e3:8.1f}  ({M_case * 1e3 / OLD['M_case']:.4f})")
print(f"  mu     {OLD['mu']:8.3f} -> {mu * 1e3:8.3f}  ({mu * 1e3 / OLD['mu']:.4f})")
print(f"  N0     {OLD['N0']:8.0f} -> {N0:8.0f}  ({N0 / OLD['N0']:.4f})")
