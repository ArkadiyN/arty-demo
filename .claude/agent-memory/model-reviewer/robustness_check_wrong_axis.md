---
name: robustness-check-wrong-axis
description: A derivation's own sensitivity/robustness check can vary the magnitude of an assumption while leaving its direction/ordering fixed, silently missing a sign-flip risk
metadata:
  type: project
---

`wdss1-steel-grade/derivation.md` C7 stress-tests the baseline steel's γ
value (65 vs. 75 vs. 88, all "is baseline more brittle than assumed?") but
every alternate still assumes baseline is the *higher*-carbon of the two
catalogued grades. It never tests the case where that ordering itself is
backward — which an out-of-band fact (parent-supplied min-yield-strength
specs, ambiguously readable either way) turned out to put in genuine doubt.
A check that only perturbs magnitude within a fixed ordering assumption
cannot catch a wrong ordering, however thorough it looks (see
`wdss1-steel-grade/review.md`, F1).

**How to apply:** when a derivation compares two catalog entries (grades,
materials, configurations) and claims "direction is robust" from a
sensitivity sweep, check whether the sweep ever flips which entry has the
larger value of the driving input — not just how far one side's value
moves. If it doesn't, the robustness claim covers magnitude only, and the
underlying ordering assumption is an unexamined single point of failure.
