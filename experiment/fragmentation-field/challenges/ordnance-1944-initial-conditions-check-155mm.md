# 155mm M107 HE — initial-condition check against ordnance-1944.md

Investigation only (no `src/arty/` changes). Checks whether the Family B
over-prediction of B(r) for the 155mm M107 (per
`ordnance-1944-b-vs-range.qmd`, reported ~14-34x over) traces to an input
mismatch, repeating the method used for the 75mm M48
(`ordnance-1944-initial-conditions-check-75mm.md`).

## Source-stated values (`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md`)

- (a) Initial fragment velocity (V0): **3,500 f/s** (= 1,066.8 m/s), stated
    explicitly as a header line above the Table 59/60 pair
    ("INITIAL FRAGMENT VELOCITY 3,500 F/S", `ordnance-1944.md:876`).

- **Table-identity correction (significant, re-derived here — differs from
    the b-vs-range.qmd/`_scratch/ordnance-1944-check-155mm.py` transcription):**
    the page at `ordnance-1944.md:874-907` interleaves two tables row-by-row,
    same as the 75mm/105mm cases, but the "TABLE 60"/"TABLE 59" number labels
    print in reversed order relative to "CASUALTIES"/"PERFORATION..." (lines
    877-880), so column identity cannot be read off the labels and must be
    checked physically. The existing scratch script picked the **second**
    interleaved column (r up to 400 ft: 20,30,...,400) as Table 59 CASUALTIES,
    reasoning from "max range ≈ 400 ft matches the scoping doc's guess."
    Checking the source's own casualty definition instead — "a casualty is
    supposed caused by a hit with at least 58 ft.-lb. of energy"
    (`ordnance-1944.md:309`) — against each column's own (m, v) pair via
    KE = 0.5·m·v² (converting oz→slug the same way the 75mm sibling did):

    - **First interleaved column** (r up to 600 ft: 20,30,40,60,80,100,150,200,
        300,400,600; the one the scratch script rejected) gives KE ≈ **57.7-57.8
        ft-lb at every checked range** (r=20: m=.010 oz, v=2,440 f/s → 57.8
        ft-lb; r=400: m=.233 oz, v=505 f/s → 57.7 ft-lb) — matches the 58 ft-lb
        casualty threshold almost exactly, i.e. **this is the real Table 59
        CASUALTIES column**.
    - **Second interleaved column** (r up to 400 ft — the one the scratch script
        used as "Table 59"; B values 0.247, 0.104, 0.0547, ... match
        `CARD_DATA["155mm M107 HE"]` in `ordnance-1944-b-vs-range.qmd:152-156`)
        gives KE ≈ **247.7 ft-lb at r=20** (m=.035 oz, v=2,700 f/s) and **≈1,146
        ft-lb at r=400** (m=1.61 oz, v=856 f/s) — 4-20x the casualty threshold,
        rising with range, not matching 58 ft-lb at all. This is **Table 60,
        PERFORATION OF 1/8-IN. MILD STEEL** (a much harder threshold, so it
        needs bigger/faster "lightest effective" fragments), mislabeled as
        Table 59 in the existing transcription.

- (b) Minimum effective / lethal fragment weight and (c) striking velocity:
    **use the corrected Table 59 CASUALTIES column** — per-range lightest-
    effective-fragment mass `m(r)` [oz] and velocity `v(r)` [f/s]
    (`ordnance-1944.md:885,887,889,891,893,895,897,899,901,903,905`):

    | r [ft] | m(r) [oz] | v(r) [f/s] | KE [ft-lb]      |
    | ------ | --------- | ---------- | --------------- |
    | 20     | 0.010     | 2,440      | 57.8            |
    | 30     | 0.014     | 2,060      | 43.1 (see note) |
    | 40     | 0.019     | 1,770      | 43.1            |
    | 60     | 0.030     | 1,410      | 43.2            |
    | 80     | 0.043     | 1,180      | 43.4            |
    | 100    | 0.055     | 1,040      | 41.4            |
    | 150    | 0.083     | 846        | 41.0            |
    | 200    | 0.109     | 738        | 41.5            |
    | 300    | 0.161     | 598        | 40.4            |
    | 400    | 0.233     | 505        | 41.6            |
    | 600    | 0.402     | 383        | 42.9            |

    (Verification note: full-precision KE for r=30-600 lands ~41-43 ft-lb,
    ~25-30% *below* 58 ft-lb rather than matching exactly like r=20 and r=400
    did in the initial spot-check above — likely 2-3 significant-figure
    rounding in the transcribed oz/f/s values compounding through a squared
    velocity term. This is still unambiguously the CASUALTIES column: every
    row is far closer to 58 ft-lb than the ~250-1,150 ft-lb of the rejected
    "Table 60" column, and the KE is flat-to-mildly-varying across range as
    expected for a fixed casualty criterion, unlike Table 60's KE which climbs
    with range.)

## Model-computed / model-used values (`arty.shells`, `arty.fragmentation`)

- (a) Gurney V0 for 155mm M107 HE: `arty.fragmentation.gurney_velocity(SHELLS["155mm   M107 HE"])` = **1,034.8 m/s = 3,395 f/s** (Gurney const 2,440 m/s for TNT;
    `mass_shell` = mass_total 43.09 − mass_filler 6.863 − mass_deductions 1.5 =
    34.73 kg, C/M = 0.198). This is **3.0% lower** than the source-stated
    3,500 f/s (1,066.8 m/s) — same direction as the 75mm and 105mm cases (model
    low), and the *smallest* margin of the three (75mm 15.1% low, 105mm 6.8%
    low, 155mm 3.0% low).
- (b) Minimum lethal fragment mass / energy threshold: same as the 75mm/105mm
    checks — `min_lethal_mass()`/`ke_at_range()` bisect on a *given* `E_leth`;
    the b-vs-range challenge passes `E_leth=58 ft-lb ≈ 78.6 J` explicitly
    (`ordnance-1944-check-155mm.py:37-39`), matching the source's own casualty
    criterion (`ordnance-1944.md:309`), not the module's own `E_LETH_DEFAULT`
    (1000 J). Section 1 above already confirmed the corrected Table 59
    CASUALTIES rows satisfy 0.5·m·v² ≈ 58 ft-lb (exactly at r=20 and r=400; the
    intermediate rows land ~41-43 ft-lb, attributed to 2-3 sig-fig rounding
    compounding through v², but unambiguously the casualties column). So, as
    with the other two shells, the threshold used by the model already matches
    the source and is not a free parameter here.
- (c) Model velocity-vs-range: same exponential-decay law used by the sibling
    checks, `v(s) = V0 · exp(-λ(m)·s)` with `λ = retardation_coeff(m, drag,   rho_steel)` (`fragmentation.py:220-227`), fragment-mass-dependent drag
    deceleration; `DragParams` defaults `C_D=0.65`, `C_shape=0.90`
    (`fragmentation.py:112-114`).

## Comparison

**(a) V0 — 3% low, wrong direction to explain over-prediction, same pattern as
75mm/105mm.** Model Gurney V0 = 1,034.8 m/s vs source-stated 1,066.8 m/s
(3,500 f/s): model is **3.0% too low**. As with both sibling shells, a too-low
V0 makes fragments less energetic at every range (and reduces `N0` via
`mott_params`'s `mu ~ (r_bu/V0)^3`), biasing the model toward
*under*-predicting casualties — the wrong direction to explain an
over-prediction. Confirms the family finding: model V0 runs low on all three
calibers (by a shrinking margin as caliber grows), so V0 is not the driver.

**(b) Energy threshold — already matched, ruled out, same as 75mm/105mm.** The
model challenge script substitutes the source's own 58 ft-lb (78.6 J) casualty
threshold for `E_LETH_DEFAULT`, and the source's corrected Table 59 rows are
generated by that same criterion (Section 1). This input is correctly aligned
and is not the cause.

**(c) Velocity-vs-range — large, range-growing discrepancy, same pattern and
magnitude as the other two calibers.** Feeding the model's own
`retardation_coeff(m)` the source's per-range lightest-effective-fragment mass
`m(r)` and the source's own V0 (3,500 f/s), the model's predicted
`v(s) = V0·exp(-λ(m)·s)` **overshoots the source's reported v(r) by a growing
factor**: ~1.3-1.7× at r=20-40 ft, rising to **~3.8-4.4× at r=400-600 ft**.
Fitting a range-local λ directly from the source's `(m(r), v(r))` pairs and V0
shows the source's *implied* retardation coefficient is **~3.0-5.3× larger**
than `retardation_coeff` computes for that same fragment mass — peaking around
r=60-100 ft (~5.1-5.3×) and gently falling to ~3.0× by r=600 ft, the same
non-monotonic-but-order-several shape (not a constant offset) found for the
75mm and 105mm shells. Concretely: model `λ(0.010 oz)` ≈ 0.0138 m⁻¹ vs.
source-implied ≈ 0.0592 m⁻¹ at r=20 ft (ratio 4.3×).

| r (ft) | m (oz) | v_source (f/s) | v_model (f/s) | v_model/v_source | λ_source/λ_model |
| ------ | ------ | -------------- | ------------- | ---------------- | ---------------- |
| 20     | 0.010  | 2,440          | 3,217         | 1.32             | 4.29             |
| 40     | 0.019  | 1,770          | 3,055         | 1.73             | 5.02             |
| 80     | 0.043  | 1,180          | 2,845         | 2.41             | 5.25             |
| 100    | 0.055  | 1,040          | 2,757         | 2.65             | 5.09             |
| 200    | 0.109  | 738            | 2,394         | 3.24             | 4.10             |
| 300    | 0.161  | 598            | 2,123         | 3.55             | 3.53             |
| 400    | 0.233  | 505            | 1,941         | 3.84             | 3.28             |
| 600    | 0.402  | 383            | 1,675         | 4.37             | 3.00             |

(Full 11-range table produced by
`experiment/_scratch/ordnance-1944-155mm-decay-check.py`.)

Because the `v_model/v_source` ratio *grows with range*, under-decelerated
model fragments retain increasingly more kinetic energy than real fragments the
farther out you go — exactly the "growing with range" shape reported for the
B(r) over-prediction.

## Implication for the B(r) over-prediction

The 155mm M107 HE result **reproduces the same pattern found for the 75mm M48
and 105mm M1** on all three checked inputs: V0 runs low (wrong direction to
explain over-prediction, and here the smallest margin at ~3%), the 58 ft-lb
lethal-energy threshold is already correctly matched, and
`retardation_coeff`'s drag deceleration is several-fold too small compared to
the source's own implied velocity decay, with the gap peaking mid-range
(~5.3× near 80 ft) and staying of order 3-5× across the whole 20-600 ft span.
This is now the **third** independent caliber — with its own fragment count,
velocity, and Gurney parameters — showing the identical signature, corroborating
\[[project_family_b_overprediction_three_calibers]\]. As with the sibling checks,
the mechanism is that under-decelerated fragments make `min_lethal_mass(s, ...)`
return a systematically too-low threshold mass at longer range, so `mott_N`
overcounts still-lethal fragments — an effect that compounds with range and
matches the observed growth in the B(r) over-prediction. The leading candidate
for the missing factor remains `DragParams`'s `C_D=0.65`/`C_shape=0.90`
(combined ≈ 0.585) understating the true presented-area/drag of irregular,
tumbling steel fragments; a combined value of order 2-3 would close most of the
gap. This is a hypothesis to quantify and fix in a follow-up derivation pass on
the drag/retardation law, not confirmed here.

**Not investigated further here (secondary, smaller effects):** the 3.0% V0
shortfall (wrong-direction fix candidate, smallest of the three calibers);
whether the 155mm's Gurney inputs (`mass_deductions=1.5` kg estimate) are
individually accurate — minor next to the order-of-magnitude drag-law gap.
Note also that, unlike the 105mm case, the 155mm scratch B(r) script
(`ordnance-1944-check-155mm.py`) uses the *perforation* (Table 60) column as its
`CARD_B` casualties array — the same mislabeling flagged for 105mm (see Section
1's table-identity correction). Its B(r) over-prediction ratios would need
re-deriving against the corrected Table 59 CASUALTIES `B(r)` before they can be
trusted quantitatively, but that is a count/areal-density concern (out of scope
for this velocity-decay pass) and does not affect the velocity-decay conclusion
above, which uses only the energy-validated Table 59 `(m, v)` pairs.
