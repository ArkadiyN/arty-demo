# Materiality: fuze-weight provenance for 105mm M1 HE / 155mm M107 HE `mass_deductions`

## Problem statement

`src/arty/shells.py` carries `mass_deductions` for two shells without a clean
source:

- **105mm M1 HE** — `mass_deductions=0.75` kg, no source comment at all.
- **155mm M107 HE** — `mass_deductions=1.5` kg, commented "fuze + rotating
    band + base plug (**estimate**)".

Two newly-processed sources give real numbers:

- `doc-reference/ww2-shells/tm-9-1901-artillery-ammunition/` — fuze-only or
    fuze+booster weights: M48/M48A1/M48A2 = 1.41 lb (fuze only), M54 = 1.42 lb
    (fuze only), M51A3 w/ M21A2 booster = 2.15 lb, M55A2 w/ M21A2 = 2.16 lb.
    Closure invariant in the card: the M21A2 booster increment closes at 0.74
    lb on **two independent pairs** (M51A3−M48A2 = 2.15−1.41 = 0.74 lb;
    M55A2−M54 = 2.16−1.42 = 0.74 lb) — the table is internally consistent.
- `doc-reference/ww2-shells/tm-9-1904-fuze-fitting/` — 105mm M1 HE is
    authorized for **M48 or M54** fuze with **M20 or M20A1** Booster (booster
    weight not in TM-9-1901); 155mm M107 HE is authorized for **M51 w/ M21**
    or **M51A1 w/ M21A1** (TM-9-1901 only tabulates the *superseding*
    M51A3/M21A2 and M55A2/M21A2 pairs, not the M51/M21 or M51A1/M21A1 pairs
    actually authorized for M107).

## 1. Spread across authorized variants

TM-9-1901's own data already answers the within-family question directly:
**M48, M48A1, and M48A2 — three mechanically different fuzes (plain
superquick, fixed 0.15s delay, switchable delay) — all weigh exactly 1.41 lb.**
M54 (a different fuze family, adds up to 25s time capability) weighs 1.42 lb —
0.01 lb (0.7%) more. Fuze mass is set by the housing/thread/body casting, not
by the internal timing mechanism, so mechanical variant letters (A1, A2, A3)
do not perturb it. By the same logic, M51 vs M51A1 vs M51A3 (which differ only
in delay-timer variant, per the M51A3 card note) are expected to weigh the
same, i.e. ≈2.15 lb w/ M21A2-equivalent booster — this is inference by
analogy, not a sourced number for M51/M21 or M51A1/M21A1 specifically.

**Verdict on part 1:** within-family fuze-variant choice is not a source of
meaningful mass uncertainty for either shell. The real gaps are (a) the M20/
M20A1 booster weight for 105mm, never tabulated in TM-9-1901, and (b) the
M51/M21 vs M51A1/M21A1 vs M51A3/M21A2 weight match for 155mm, which by the
M48-family analogy is expected to be small (≤0.01 lb) but is not directly
sourced.

## 2. Downstream N0 sensitivity

`arty.fragmentation.mott_params`: `N0 = mass_shell / (2·mu)`, where
`mass_shell = mass_total − mass_filler − mass_deductions` and
`mu ∝ (r_bu/V0)^3`. `V0` comes from `gurney_velocity`, which depends on
`mass_shell/mass_filler` — so `mass_deductions` enters **twice**, through
`mass_shell` directly and through `V0` (larger `mass_shell` → smaller `V0` →
larger `mu` → smaller `N0`). These two paths partially cancel.

Ran `checks/mass-deductions-sensitivity.py` (script below) sweeping
`mass_deductions` over the full plausible range for each shell, from the
sourced fuze-only weight up to fuze+booster-analog:

**105mm M1 HE** (current placeholder 0.75 kg = 1.653 lb, unsourced):

| mass_deductions                         | case mass | V0         | mu      | N0     | Δ N0 vs current |
| --------------------------------------- | --------- | ---------- | ------- | ------ | --------------- |
| 0.75 kg (current, unsourced)            | 12.040 kg | 994.2 m/s  | 1.538 g | 3913.3 | —               |
| 0.640 kg (M48 fuze only, 1.41 lb)       | 12.150 kg | 990.1 m/s  | 1.551 g | 3916.3 | +0.08%          |
| 0.644 kg (M54 fuze only, 1.42 lb)       | 12.146 kg | 990.2 m/s  | 1.551 g | 3916.2 | +0.08%          |
| 0.975 kg (fuze+booster-analog, 2.15 lb) | 11.815 kg | 1002.9 m/s | 1.512 g | 3907.1 | −0.16%          |

Within-family (M48 1.41 lb vs M54 1.42 lb) N0 shift: **0.00%** (−0.12 in
3916).

**155mm M107 HE** (current 1.5 kg, commented "estimate"):

| mass_deductions                                                                 | case mass | V0         | mu      | N0     | Δ N0 vs current |
| ------------------------------------------------------------------------------- | --------- | ---------- | ------- | ------ | --------------- |
| 1.500 kg (current, "estimate")                                                  | 34.727 kg | 1034.8 m/s | 4.738 g | 3664.9 | —               |
| 0.975 kg (M51A3 fuze+booster only, 2.15 lb, no band/plug)                       | 35.252 kg | 1027.7 m/s | 4.803 g | 3669.9 | +0.13%          |
| 1.500 kg (fuze+booster 2.15 lb + current's implied band/plug residual 0.525 kg) | 34.727 kg | 1034.8 m/s | 4.738 g | 3664.9 | ~0.00%          |

**Full swing, either shell, across the entire plausible range (unsourced
placeholder ↔ sourced fuze-only ↔ sourced fuze+booster-analog): N0 shifts by
≤0.2%.** This is because the two paths by which `mass_deductions` enters
(`mass_shell` directly, and `V0` via the Gurney denominator) move `N0` in
opposite directions and nearly cancel — `mass_deductions` is a ~2-7% share of
`mass_shell`, and the two effects each individually would move N0 by a
comparable small amount, but with opposite sign. Downstream quantities
(`mott_N`, `expected_kills`, `p_kill`) are monotonic, weakly-sloped functions
of N0 near these values, so the P(kill)/R50 shift is smaller still.

## Verdict: **MOOT**

The spread across authorized fuze variants (M48 vs M54 for 105mm; M51 vs
M51A1 vs M51A3 for 155mm, by analogy) is negligible for mass purposes — TM-
9-1901 itself proves mechanical-variant letters don't move fuze weight. The
open gaps (105mm M20/M20A1 booster weight; 155mm M51/M21 vs M51A1/M21A1 vs
M51A3/M21A2 weight match) are real provenance gaps, but even the maximum
plausible correction — swapping the entire deduction from the unsourced
placeholder to a sourced-informed fuze+booster estimate — moves total
fragment count N0 by under 0.2%, well inside the model's stated fidelity bars
elsewhere (see e.g. the 75mm case, where a 16% case-mass error was flagged
`blocking` — this is two orders of magnitude smaller).

**Recommendation:** do not re-derive. Instead, as a trivial follow-up (not a
full Workflow B pass), add source citations to both `mass_deductions` comments
in `src/arty/shells.py` pointing at TM-9-1901 (fuze-weights.csv) and TM-9-1904
(fuze-fitting card.md), noting the still-open component (M20/M20A1 booster
weight unsourced for 105mm; M51/M21 vs M51A3/M21A2 weight-match assumed by
analogy for 155mm) as a comment, without changing the numeric values — the
numbers already land within the range the new sources bound, and no
downstream output crosses a materially different value.

## Check script

`checks/mass-deductions-sensitivity.py` — run with:

```
uv run python experiment/fragmentation-field/challenges/fuze-mass-deductions-range/checks/mass-deductions-sensitivity.py
```

## Open findings (real, immaterial per this triage)

FINDING\[deferrable\]: 105mm M1 HE mass_deductions booster (M20/M20A1) weight not sourced anywhere in TM-9-1901; current value bracketed by fuze-only and M21A2-booster-analog but not itself confirmed (affects: src/arty/shells.py, experiment/fragmentation-field/challenges/fuze-mass-deductions-range/materiality.md; since: 2026-08-08)

FINDING\[deferrable\]: 155mm M107 HE mass_deductions rests on M51A3/M21A2 fuze+booster weight as a stand-in for the actually-authorized-but-unsourced M51/M21 and M51A1/M21A1 pairs (affects: src/arty/shells.py, experiment/fragmentation-field/challenges/fuze-mass-deductions-range/materiality.md; since: 2026-08-08)

**Acquisition attempt, 2026-08-10.** A @librarian pass bundling both searches
ran ~19 min / 30 tool calls without producing a report, a source, or a marker
edit — it was still mid-search ("Let me search for these specific technical
manuals...") when it stopped, i.e. turn-exhaustion with nothing written.
Given both findings are already scoped above as real-but-immaterial (N0
shifts \<=0.2% across the full placeholder/sourced/analog range, this file's
own §ending "0.2%" figures above), this was not re-dispatched a second time;
both stay open for a future pass, which should split the two shells into
separate, narrower searches rather than bundling them.
