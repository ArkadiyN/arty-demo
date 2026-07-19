---
name: frag-field-structure
description: Code map for the fragmentation-field 3D paths and the spreading-vs-target-coupled factor split
metadata:
  type: project
---

Single-zone 3D field: `fragmentation.py:_expected_kills_3d_point` /
`compute_frag_field_3d`. Four-zone: `zones.py:four_zone_field`,
`_four_zone_field_split`, `four_zone_line_split`. Shared integrand:
`pdf · pk_given_hit(E) · A_p(γ) / (2π·s²·2·sinθ^z·δ)`.

**Gotcha:** the spreading factor `1/(2π s²·2 sinθ^z δ)` is inlined with the
two target-coupled factors, not a separate function — a target-independent
quantity must divide out BOTH `pk_given_hit` and `A_p`, replacing the graded
kill weighting with a binary lethal-mass cut.

- `min_lethal_mass` is bisection (no closed form); it depends only on slant
  range s, so tabulate on a 1D s-grid + `np.interp` to vectorize — the key
  perf lever. See `updates/lethal-fragment-density-field/scoping.md` §4C.
- Binary-cut `E_leth = 1000 J` (ES-310 P_k|hit=0.5 anchor), NOT the 79 J
  notebook test value. `lethal-fragment-density-field/derivation.md` §3.
- `SteelParams.gamma` (Mott) is renamed `γ_M` in 3D notebooks to avoid
  clashing with γ = fragment arrival elevation.
