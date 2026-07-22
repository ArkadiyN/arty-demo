---
name: shell-axis-sign-convention
description: Legacy single-zone shell axis is a backward x-mirror sign error (not a benign convention) — forward axis is correct
metadata:
  type: project
---

Correct shell axis is FORWARD `_forward_shell_axis=(+cosα,0,−sinα)` — used by
`fragment_velocity`, four-zone, and `lethal_density_point`. Legacy single-zone
`_shell_axis=(−cosα,0,−sinα)` is NOT a valid alternative and NOT an axis
reversal (reversal flips z too); it flips only x, an x-mirror across x=0 → a
shell "travelling backward". It puts the whole single-zone down-range hazard
lobe on the WRONG side of the burst (confirmed defect; the older "deliberate
standardisation, don't reconcile" framing was WRONG).

**Why the mirror hides:** backward and forward agree exactly on x=0 (flip is a
no-op) and at AoF=90° (cosα=0, B=0, sign-blind). Every on-axis and every 90°
test passes with the wrong sign — an axis change needs an off-axis, AoF≠90°
regression. Cross-range r50 (read at x=0) is mirror-invariant; only the
down-range heatmap side and the four-zone−single-zone diff map change.

**Trap reusing forward-native belt machinery** (`belt_column_breakpoints` /
`_belt_column_zrep_vec`, `B=−2x cosα sinα`): passing `x_axis=−x` faithfully
reproduces the BACKWARD membership — correct code for a wrong axis. The fix is
to pass `+x` and flip the inline cosΘ, not to compensate. Scoping + fix plan:
`updates/legacy-field-shell-axis-fix/scoping.md`; wrong-sign-catching test
`tests/test_familyA_false_safe_zone.py::test_offaxis_single_zone_axis_sign`.
