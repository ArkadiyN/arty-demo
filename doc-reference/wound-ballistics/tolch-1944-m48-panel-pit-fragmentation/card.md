---
title: Tolch (1944) — 75mm M48 Shell Fragmentation Effects
report: N.A. Tolch, Fragmentation Effects of the 75mm H.E. Shell T3 (M48), Ballistic Research Laboratory Report, Declassified
---

# Fragment Density: Hits per Unit Solid Angle

**Definition** ([lines 94–106](tolch-1944.md#L94-L106)): Fragment density = **number of hits per unit solid angle**, measured via semi-circular wood panel tests at varying angles from shell axis, distances (15–120 ft), and remaining velocities (static, 700–2,130 f/s). **Distinct from Ordnance Dept (1944) "effective hits per sq-ft" (B-value):** this report measures raw perforations/penetrations/dents per solid angle, preserving directional and velocity dependence without casualty weighting.

**Fragment classes:** nose spray (0–17.5° off axis), side spray (~95° static, ~55° at 2,130 f/s), base spray (162.5–180°).

**Typical battle velocity** ([line 117](tolch-1944.md#L117)): 800–900 f/s modal; extreme range 700–1,100 f/s.

______________________________________________________________________

## Velocity-Dependence Summary

Pages 40–44 (containing all four tables below) were re-extracted with vision AI after the initial heuristic pass produced scrambled/column-misaligned numbers — figures below are from that clean re-extraction and merged into `tolch-1944.md` lines 553–684, replacing the garbled block.

### Base Spray (Rear Fragments) — Velocity Opposes Ejection

Remaining velocity **opposes** rearward fragment velocity components; density collapses sharply:

- **Perforations:** ~50% drop at 1,085 f/s → ~85% drop at 1,450 f/s → "practically zero" at 2,130 f/s ([line 609](tolch-1944.md#L609))
- **Penetrations:** decrease slowly; ~1/3 remain even at 2,130 f/s ([line 611](tolch-1944.md#L611))
- **Total hits per u.s.a. (Panel A):** 9.71 (static) → 0.70 (2,130 f/s), a 93% reduction ([table, lines 617–627](tolch-1944.md#L617-L627))
- **Cumulative velocity distribution — UNVERIFIED, do not cite:** the narrative sentence giving this breakdown ([line 628](tolch-1944.md#L628)) sits on a page scanned at ~100 DPI, too degraded to transcribe reliably by any method tried so far. Two independent extractions disagree and neither is internally consistent (a "% exceeding threshold" series must be monotonically decreasing as the threshold rises):
    - Heuristic-path manual read (scrambled table, interpreted by hand): 80% > 700 f/s, 48% > 1085 f/s, 29% > 1450 f/s, 14% > 1685 f/s, ~7% > 2130 f/s — monotonic, physically sensible, but reconstructed from a garbled source.
    - Vision re-extraction: "20% ... 15% ... 25% ... 18% ... 7%" — non-monotonic (25% > 1450 f/s exceeding 15% > 1085 f/s is impossible for a cumulative distribution), so this reading is provably wrong on at least one digit.
    - Neither figure should be used for model calibration until checked against a better scan/copy of the source report.

### Nose Spray (Forward Fragments) — Velocity Adds to Ejection

Remaining velocity **adds** to forward charge velocity; density increases with velocity ([lines 665–673](tolch-1944.md#L665-L673)):

- Perforations **increase markedly** with velocity ([line 665](tolch-1944.md#L665))
- Range extends: Panel C hit density comparable to Panel A at high remaining velocity ([line 665](tolch-1944.md#L665))
- Total hits per u.s.a. (Panel A): 16.09 (static) → 21.45 (2,130 f/s); Panel B shows a larger relative rise, 2.42 → 26.31 ([table, lines 673–682](tolch-1944.md#L673-L682))

### Side Spray (Lateral Fragments) — Angular Deflection

- Static: centered ~95° off shell axis; 2,130 f/s: centered ~55° off axis ([line 570](tolch-1944.md#L570))
- Density remains ~2–6 hits/u.s.a. across velocities; minor increase at high velocity due to angular crowding ([table, lines 557–563](tolch-1944.md#L557-L563))

______________________________________________________________________

## Fragment Velocities (Charge Components)

- **Perforating fragments:** 2,750 f/s
- **Penetrating fragments:** 3,030 f/s
    ([line 96](tolch-1944.md#L96))

Higher penetrating-fragment velocity attributed to smaller size and lower ballistic coefficient.

______________________________________________________________________

## Drag Model Relevance

This document provides **direct velocity-dependence measurements** (700–2,130 f/s) for fragment density on the 75mm M48 shell. The sharp collapse of base-spray density (93% reduction, static → 2,130 f/s, table-sourced and high-confidence) and expansion of nose-spray density with increasing remaining velocity enables calibration checks on whether the project's drag model under-decelerates fragments relative to 1944 ground truth. The cumulative velocity-distribution figure that would anchor this most directly is unresolved (see above) — use the table-based density collapse instead, which does not depend on that sentence.
