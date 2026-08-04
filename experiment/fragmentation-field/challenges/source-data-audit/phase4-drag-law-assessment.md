# Phase 4 — do the two shipped drag conclusions survive the corrected column?

Ledger: [`ledger.md`](ledger.md) §1 (the discriminator), §3a/§3c (consumers),
§5 (the re-baselined tables).

Two conclusions were reached on evidence that mixed 75mm **casualties**,
105mm **perforation** and 155mm **casualties** into a single 25-point
velocity-decay set. This pass re-runs both on the corrected casualties columns.

Evidence for every number below:
[`checks/drag-law-recheck-corrected-column.py`](checks/drag-law-recheck-corrected-column.py)
(`uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/drag-law-recheck-corrected-column.py`).
It reads each series from
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/*.csv`
— no hand-typed array, which is the defect under audit. `V0` is read off
`ordnance-1944.md` at the `INITIAL FRAGMENT VELOCITY` line under each shell
heading (`# 75-MM H.E. SHELL, M48` → 3,120 f/s; `# 105-MM H.E. SHELL,'Ml` and
`# 155-MM N.E. SHELL, M107` → 3,500 f/s).

**Fidelity bar applied** (inherited from the shipped derivation §4 V2):
RMS of $\ln(v_{model}/v_{source})$ over the arrival-Mach > 0.7 subset
$\le 0.10$, i.e. ~10% on velocity in the band where arrivals are still lethal.

## Pipeline check — the old set reproduces exactly

Running the corrected pipeline on the *old mixed* row set returns the shipped
derivation's V2 numbers digit-for-digit (0.864 / 0.710 at 0.585; 0.349 /
**0.092** at 2.674; best constant 2.200 / 2.935 at RMS 0.250 / 0.047; Fig-3
0.259 / 0.072). Any change below is therefore the column correction, not a
methodological difference.

## Verdict 1 — `DragParams` in `src/arty/fragmentation.py`: **SOUND** (shifted numbers)

`C_D = 1.28`, `C_shape = c_shape_from_ballistic_density(2600, 7850)` = 2.0890,
combined 2.6739. Unchanged; no corrective action required.

| set                            | n   | n(M>0.7) | RMS @0.585 (all / M>0.7) | RMS @2.674 (all / M>0.7) | best constant (M>0.7) | implied *k* |
| ------------------------------ | --- | -------- | ------------------------ | ------------------------ | --------------------- | ----------- |
| old mixed (as shipped)         | 25  | 20       | 0.864 / 0.710            | 0.349 / **0.092**        | 2.935                 | 2261 kg/m³  |
| **corrected casualties, full** | 32  | 21       | 0.967 / 0.755            | 0.405 / **0.096**        | 2.876                 | 2331 kg/m³  |
| corrected, shipped point count | 25  | 16       | 0.989 / 0.753            | 0.439 / **0.088**        | 2.874                 | 2333 kg/m³  |
| (contrast) all perforation     | 33  | 33       | 0.679 / 0.679            | 0.098 / 0.098            | 2.983                 | 2207 kg/m³  |

Per-shell on the corrected casualties columns, RMS(M>0.7) at 2.674 is 0.113
(75mm) / 0.086 (105mm) / 0.086 (155mm); best constants 2.915 / 2.859 / 2.859.

Why it survives:

1. **The bar still passes.** 0.092 → **0.096** on the like-for-like set, and
    0.088 on a set matched to the shipped point count. Margin narrows, verdict
    does not change.
1. **The correction moves the data *towards* the adopted parameter, not away.**
    Best-fit combined constant 2.935 → **2.876** (adopted 2.674 is now 7.0%
    below the fit rather than 8.9% below); implied ballistic density
    2261 → **2331 kg/m³** against DoD-1975's recommended **2600**. The
    inverted column was making the source data look *further* from the DoD
    anchor than it is.
1. **The rejection of the pre-change 0.585 strengthens.** RMS(M>0.7) worsens
    0.710 → **0.755**, and RMS(all) 0.864 → 0.967.
1. **The parameter was never fitted to this data.** `C_shape` = 2.0890 comes
    from identity (4), $C_{shape} = (\rho_{steel}/k)^{2/3}$, with *k* = 2600
    kg/m³ read from TP-12; `C_D` = 1.28 is TP-12's stated supersonic plateau.
    The 1944 set is *validation only* (derivation §4 V2). The load-bearing
    checks — the exact λ↔*L* identity (V1), the 247 m/kg^{1/3} reproduction,
    and the geometric-admissibility argument that inverts DoD's own cube/sphere
    *k* back to 7846/7832 kg/m³ — touch no 1944 number at all and are
    untouched by the column error.

**Consequence for ledger §3c.** `C_D = 1.28` and the derived `C_shape` stand;
the three parameter-dependent scripts listed there
(`r50-drag-anchor-shift.py`, `drag-update-demo-impact.py`,
`check5b-drag-spotcheck.py`) consume `C_D·C_shape` 0.585 → 2.674 and are
**not voided** — their input parameter is unchanged. They remain in scope for
Phase 6 only if they *quote* a 1944 RMS number.

**What must be corrected (documentation, not physics).** Derivation §4 V2's
table cites 0.349 / 0.092 for a 25-point set that was a criterion mixture. The
replacement figures are 0.405 / 0.096 over 32 points, all casualties. This is
a Phase 6 surface edit, not a Workflow B change.

## Verdict 2 — rejection of Mach-dependent $C_D$ (derivation §5): **SHIFTED**

The conclusion — *do not implement a Mach-dependent $C_D$* — **stands**, but
its accuracy evidence no longer carries it. §5's numeric claim must be
restated, and the rejection now rests on the structural-cost argument.

Fig-3 $C_D(M)$ integrated along each trajectory (RK2, 4000 steps), against a
constant, on the same rows:

| set                      | law            | zero free params (at DoD *k* = 2600) all / M>0.7 | one free scale param, fitted per metric, all / M>0.7 |
| ------------------------ | -------------- | ------------------------------------------------ | ---------------------------------------------------- |
| old mixed                | constant       | 0.349 / 0.092                                    | 0.250 / **0.047** (at 2.200 / 2.935)                 |
| old mixed                | Fig-3 $C_D(M)$ | 0.259 / 0.072                                    | 0.201 / **0.034** (at $C_{shape}$ 1.810 / 2.260)     |
| **corrected casualties** | constant       | 0.405 / 0.096                                    | 0.247 / **0.069** (at 2.141 / 2.876)                 |
| **corrected casualties** | Fig-3 $C_D(M)$ | 0.300 / 0.075                                    | 0.200 / **0.050** (at $C_{shape}$ 1.760 / 2.230)     |

Two things the corrected data shows:

1. **§5's stated comparison is not reproducible as written, and was not even
    on the old data.** §5 reads: "the digitized Fig-3 $C_D(M)$ curve … scores
    RMS 0.259 / 0.072 against the best *constant*'s 0.250 / 0.047 — it does not
    beat a constant on this data." That compares a **zero-free-parameter**
    Fig-3 run against a **one-free-parameter** best constant. Given the same
    freedom, the Fig-3 law scores 0.201 / **0.034** on the old set — it *did*
    beat the best constant, on the very data §5 cites. The asymmetry is a
    pre-existing methodological defect in §5, independent of the column error.
1. **On the corrected data the accuracy comparison is a wash.** Like-for-like,
    one free scale parameter each: 0.247 / 0.069 (constant) vs 0.200 / 0.050
    (Fig-3). At zero free parameters: 0.405 / 0.096 vs 0.300 / 0.075. The Mach
    law is modestly better on every one of these four comparisons, by 0.02–0.10
    RMS — i.e. 2–10% in velocity, inside the ±10% fidelity bar and well inside
    the ±0.02 read uncertainty the digitized Fig-3 carries. **Neither law is
    distinguishable from the other on this data.**

Why the conclusion nonetheless holds: §5's second argument is untouched by any
of this and is decisive on its own. λ enters `min_lethal_mass`'s bisection and
both field builders in **closed form**; a Mach-dependent $C_D$ replaces an
algebraic λ with a per-fragment ODE integration. A change that costs the
closed-form solution across the whole field pipeline, for an accuracy
difference inside the fidelity bar and inside the source-curve read
uncertainty, is not worth making.

**What must change.** §5's numeric sentence and the `DragParams` comment at
`src/arty/fragmentation.py:182-184` both assert that Fig-3's Mach dependence
"does not beat this constant on the 1944 Ordnance velocity-decay data". That
claim is **false on both the old and the corrected data** and must be rewritten
to the defensible one: *the two laws are indistinguishable within the fidelity
bar on this data, so the constant is kept because it preserves the closed-form
λ.* Comment text only — the `C_D = 1.28` value itself is unaffected (verdict 1).

## If a corrective Workflow B change is ever raised

Neither verdict requires one. Should the Mach law be revisited, the proposal
would have to establish, in this order:

1. **A discriminating test.** Constant and Fig-3 differ by < 0.10 RMS on the
    1944 set at every parameterisation tried here. A proposal must name data
    that separates them — plausibly the transonic band alone (arrival
    M 0.8–1.4, where Fig-3 peaks at 1.40 against the 1.28 plateau), not a
    pooled RMS that averages the peak away.
1. **That the gain exceeds the digitisation uncertainty.** Fig-3 is a visual
    trace with ±0.02 in $C_D$; a 5% velocity improvement does not clear it.
1. **A closed-form or tabulated-λ path** through `min_lethal_mass` and both
    field builders, or an explicit cost budget for the per-fragment ODE.

Out of scope here, and expressly **not** a licence to re-fit `C_D`: the
combined constant is bounded below by the sphere floor (1.31) and above by the
geometric envelope noted in derivation §3, and the corrected data's best fit
(2.876) sits inside that envelope, 7% from the source-anchored 2.674.

## Scope

1944-Ordnance drag law only. The Tolch-1938 consumers (ledger §4) are a
separate pass and are untouched here.
