---
name: four-zone-test-parity-gap
description: modeler passes on zones.py tend to add a posture-sensitivity test for the four-zone path but skip an explicit headline-defect (e.g. false-safe-ring) regression test equivalent to the single-zone one, even when the four-zone path is where the reviewed generalization actually lives
metadata:
  type: project
---

First observed in the target-height-intercept src/ implementation pass
(`tests/test_pkill_field.py`, reviewed against
`experiment/fragmentation-field/updates/target-height-intercept/derivation.md`):
the single-zone path had `test_single_zone_pkill_field_posture_and_false_safe_ring`
directly asserting the headline defect is fixed, but the four-zone counterpart
only checked the weaker `P_k_stand.max() >= P_k_prone.max()` invariant, without
asserting the false-safe-ring is actually filled for the four-zone path — even
though four-zone is the one exercising the per-zone `K = cosθ^z ± sinδ`
breakpoint generalization that single-zone testing can't cover (single-zone
only ever uses `cosθ^z = 0`).

**Resolved** in the subsequent notebook-presentation pass: `tests/test_pkill_field.py`
now has `test_four_zone_pkill_field_posture_and_false_safe_ring`, asserting the
same `P_k_stand[ring].max() > 0.5` claim as the single-zone test. The general
pattern below remains useful for the *next* time a `zones.py` change mirrors a
`fragmentation.py` fix.

**How to apply:** when reviewing a `zones.py` change that mirrors a
`fragmentation.py` (single-zone) fix, check that the test file adds a
four-zone test asserting the *same specific defect-removal claim*, not just a
weaker generic invariant (bounds, monotonicity) — "posture sensitivity" is not
a substitute for "the false-safe-ring is filled." Flag this as a suggested
test addition rather than blocking on it if the underlying physics is shared
with an already-tested single-zone path and has been independently
numerically re-verified.
