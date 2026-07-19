---
name: four-zone-test-parity-gap
description: When a zones.py change mirrors a fragmentation.py fix, require a four-zone test asserting the SAME defect-removal claim, not a weaker invariant
metadata:
  type: project
---

Observed pattern: a modeler pass adds a direct headline-defect regression
test for the single-zone path but only a weak generic invariant (bounds,
monotonicity, "standing ≥ prone") for the four-zone counterpart — even when
four-zone is where the reviewed generalization actually lives and
single-zone testing cannot cover it (e.g. `cosθ^z ≠ 0` breakpoints).

**How to apply:** check the test file asserts the same specific
defect-removal claim on both paths (e.g. `P_k_stand[ring].max() > 0.5`).
Suggest rather than block if the shared physics was independently
re-verified numerically.
