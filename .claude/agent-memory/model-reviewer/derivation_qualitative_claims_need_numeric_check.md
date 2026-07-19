---
name: derivation-qualitative-claims-need-numeric-check
description: A derivation's qualitative fraction-of-field claim can pass all formal checks and be empirically false — compute the actual fraction
metadata:
  type: project
---

`pkill-poisson-field/derivation.md` §4.7 predicted a "mostly saturated" P_k
footprint; review "confirmed" it from ONE near-peak spot check. The notebook
later computed the real fraction: fringe-dominated (~1–3% of lethal cells
above P_k=0.95) — the opposite. Dimensional/limit/monotonicity checks are
about the function's shape, not where the field's actual values fall on it;
that second question is empirical.

**How to apply:** any "most of the field / much of the belt" claim is
unverified until the actual fraction is computed (a couple of
`np.mean(field > threshold)` lines) — a representative-point spot check does
not exercise it. If a notebook's printed diagnostic contradicts the
working-folder derivation/review docs, flag the stale doc — until archived
it is one hyperlink away from the reader.
