---
name: sensitivity-physics-leakage
description: Recurring layering violation — fragment ray trig inlined in app/plots instead of calling zones.fragment_velocity; equivalence tests can't catch it
metadata:
  type: project
---

Recurring pattern: chart helpers (`app/sensitivity.py` `_spray_cone` /
`_spray_cone_across`, `plots.py:fig_zone_elevation`) inline the fragment
ray-projection trig instead of calling `zones.fragment_velocity`. Known
instances are fixed; re-open whenever a NEW spray-cone-like helper appears
with inlined trig. Flag as secondary/low-severity, recommend delegation.

**Durable lesson — numeric-equivalence tests cannot catch bit-identical
duplication:** a test comparing outputs to a fresh `fragment_velocity` call
passes against duplicated-but-correct code; only re-inlining that also gets
the formula wrong would fail. To enforce "calls the helper", assert the call
itself — reference pattern:
`tests/test_plots.py::test_zone_elevation_delegates_to_fragment_velocity`
(monkeypatch sentinel; assert calls + args + output reaches the rays).
Verify a regression test's protection claim by reverting the fix and running
it — don't take the docstring's framing at face value.

`fig_single_zone_elevation`'s belt-edge-ray trig (beta_c/beta rotation) has
no equivalent `arty` helper yet — still flag as physics-in-plots if touched.
