# Drag gap vs. the 1944 Ordnance Dept. data

**Question.** Does Family B (`four_zone_lethal_density_field`) reproduce the
1944 Ordnance Dept. *B*-vs-range casualty data — and if not, is the
retardation/drag model the cause?

**Status: Closed, on a re-baselined footing (restated 2026-08-08).** The
originally published gap — "FAIL against the factor-of-2 band, all three
shells, over-predicting 7–34×, growing with range" — was **void**: rows #2
and #5's check scripts hand-typed the mild-steel-perforation column
mislabeled as the casualty column (`b-vs-range-rebaseline.md`). Against the
genuine, closure-checked casualties columns, Family B at the current
(v0.9.0) drag calibration **passes the factor-of-2 band at nearly every
tabulated range for all three shells** (75mm 8/10, 105mm 9/11, 155mm 11/11 —
[`b-vs-range.qmd`](b-vs-range.qmd)'s Verdict). The residual pattern also
inverts: instead of a one-directional over-prediction growing with range, the
corrected comparison over-predicts at short range and *under*-predicts at
long range, worst case ~5.9× under-prediction at 75mm's r=400 ft.

Drag was still implicated by the (separately genuine) velocity-decay gap in
row #4, and has been **corrected** — see
[`../../updates/mach-dependent-fragment-drag/`](../../updates/mach-dependent-fragment-drag/)
([`scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md),
[`derivation.md`](../../updates/mach-dependent-fragment-drag/derivation.md)),
which anchors `C_D·C_shape` to the DoD-1975 ballistic density at **2.67**
(from 0.585). **That update is now closed and half-retired (2026-08-03) — read
[`its README`](../../updates/mach-dependent-fragment-drag/README.md) before
citing it.** The anchor cited here is the half that survives; the update's
*Mach-dependence* sections are withdrawn. It narrows the *B(r)*
ratio span from ~1.5–3.7× (pre-anchor, 0.585) to ~0.2–1.7× (v0.9.0, 2.674)
across all three shells (see
[`b-vs-range.qmd`](b-vs-range.qmd)'s refreshed table, and
[`checks/b-vs-range-drag-attribution.py`](checks/b-vs-range-drag-attribution.py))
— closing the gap for most of each shell's tabulated range, with a smaller
far-range residual, now in the opposite (under-prediction) direction,
remaining. Rows #5 and #6's own conclusions (drawn on the still-current 0.585
constant, before the anchor) remain superseded as marked inline; the
measurements in those rows stand.

**Closed, not chased further, for a physical reason, not a convenience one:**
the corrected constant (2.674) already sits within ~10% of the geometric
ceiling — the fragment's presented area implied by any higher constant would
require it to be denser than solid steel (`_limitations.qmd` L3). The
literature-motivated alternative to a bigger constant — a Mach-dependent
`C_D(M)` integrated along the trajectory — was built and tested, and scored no
better than the flat corrected constant on this same data
(`derivation.md` §5; `_limitations.qmd`, "Mach-dependent... rejected on
evidence"). The residual is attributed outside the retardation law — to the
count chain or spray/belt geometry (`_limitations.qmd` L1, L3) — which are
different model aspects, not more drag calibration. The third L3 candidate,
the *B(r)* reduction itself, has since been checked (#8 below): both
families' reductions are implementation-correct, ruling out a reduction bug
as the residual's cause, though not the averaging convention itself.
Continuing to tune `C_D`/`C_shape` against this one dataset past this point
would be overfitting to 1944 Ordnance data on an already-exhausted parameter.

## Reading order

| #   | Document                                                                                                                                   | What it settles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [`b-vs-range.md`](b-vs-range.md)                                                                                                           | Scoping. No new `src/arty/` math needed — *B* is a unit conversion + azimuthal average over `lethal_density_point` / `four_zone_lethal_density_field`. Sets the factor-of-2 verdict criterion.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2   | [`b-vs-range.qmd`](b-vs-range.qmd)                                                                                                         | The comparison itself. **⚠ Original verdict void, restated** — the check scripts hand-typed the perforation column mislabeled as casualties. Against the corrected casualties columns, Family B **passes** the factor-of-2 band at nearly every tabulated range across all three calibers (`b-vs-range-rebaseline.md`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 3   | [`review.md`](review.md)                                                                                                                   | **PASS-with-limitations.** Reduction formula is sound and the over-prediction is real; one 75mm r=40 ft transcription defect found (non-blocking).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 4   | [`initial-conditions-75mm.md`](initial-conditions-75mm.md) [`-105mm`](initial-conditions-105mm.md) [`-155mm`](initial-conditions-155mm.md) | Is it an input mismatch? No. V0 and thresholds match the source; feeding the source's own per-range *m(r)* into `retardation_coeff` shows velocity decay several-fold too slow in all three calibers. Localises the defect to drag.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 5   | [`drag-coefficient-calibration.md`](drag-coefficient-calibration.md)                                                                       | Does a bigger constant drag close it? **No.** Raising combined `C_D·C_shape` from 0.585 into the literature's 1.0–1.71 shrinks the ratio everywhere but closes it nowhere uniformly — the decay curve has the wrong *shape*, not just the wrong scale. **⚠ Conclusion superseded** — that sweep stopped short of the literature-admissible constant; at the DoD-1975 anchor of 2.67 the Mach>0.7 band closes (RMS 0.710 → 0.092, [`updates/mach-dependent-fragment-drag/derivation.md`](../../updates/mach-dependent-fragment-drag/derivation.md) V2). The "wrong shape, not scale" framing is exactly what motivated a Mach-dependent law, which was tested and rejected (scoping §3a, §4 option 3) — a corrected constant was the fix.                                                                                                                |
| 6   | [`tolch-1938-panel-distance.md`](tolch-1938-panel-distance.md)                                                                             | Is Tolch (1938) an independent check? Partly, and it **contradicts the remedy**: the panel-radius falloff is shape-degenerate on drag, and the absolute count rules *out* raising drag. Also surfaces a separate, larger defect — the Mott scale (→ [`../mott-scale-gap/`](../mott-scale-gap/)). **⚠ Conclusion superseded** — re-run with post-shape-closure Mott parameters ([`updates/mach-dependent-fragment-drag/scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md) §3d) reverses the sign of this test: the absolute count now vetoes the *current* 0.585 constant (1–9 perforations predicted vs. ~700–780 observed, requiring an impossible ~10.8–20.2 kJ threshold; re-run 2026-08-08 on the 779 pit count and the re-anchored Mott closure), not a raised one. The panel-radius degeneracy and the Mott-scale finding stand. |
| 7   | [`shape-closure-orthogonality.md`](shape-closure-orthogonality.md)                                                                         | Does the Mott shape-closure fix (`../mott-scale-gap/` → `updates/mott-fragment-shape-closure/`) close this thread's gap? **No.** `retardation_coeff` never calls `mott_params`; the check feeds it source-tabulated masses directly. The two aspects are structurally independent — reviewed PASS in [`review.md`](review.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 8   | [`b-vs-range-familyA.md`](b-vs-range-familyA.md)                                                                                           | Implements the Family A half of #1's reduction, deferred until now. Family A numerically **passes** the factor-of-2 band at all 33 tabulated points — but reviewed PASS-with-limitations: this is a cancellation of two threshold-confounded errors (Family B's own 2–5× card over-prediction × Family A's ES-310 curve being ~10× stricter than the card's threshold), not an independent kernel validation. Rules out a reduction-*implementation* bug as the residual's cause for both families (`review.md`'s per-zone $A_p$-inversion check); does not rule out the reduction *convention* itself.                                                                                                                                                                                                                                                 |

## Where it stands

- The velocity-decay gap rests entirely on the Ordnance checks (#4). Tolch
    neither corroborates nor contradicts its *existence* — its drag observable
    is degenerate over a 5× span of `C_D·C_shape`. **⚠ Superseded** — this holds
    for the panel-radius falloff only; post-shape-closure Tolch's *absolute
    count* is not degenerate and rejects the current constant outright
    ([`scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md) §3d).
- `retardation_coeff`'s single fixed exponential rate cannot reproduce a
    *v(r)* whose deviation changes sign with range, which is what #5 measures.
    This matches the Sandia source's own framing of 1.0–1.71 (its own
    parameter-range-list data floor/ceiling) as a *velocity-dependent*
    combined drag.
- #6 rules out simply raising the constant, so the next step is a derivation
    pass on a velocity/range-dependent retardation law — not another
    hypothesis search. **⚠ Superseded** — both halves fail: #6's veto now falls
    on the current constant, and a Mach-dependent `C_D(M)` integrated along the
    trajectory does **not** beat a plain corrected constant
    ([`scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md) §3a,
    §4 option 3 — rejected). The step actually taken was the DoD-1975 anchor at
    2.67.
- #7 closes off a tempting shortcut: the Mott shape-closure fix that resolved
    `../mott-scale-gap/` does **not** also resolve this thread — it touches a
    different quantity (`mu`/`N0`) that `retardation_coeff` never consumes.
- #8 checks the last of the three L3 candidates named above the reading-order
    table: the *B(r)* reduction itself. Both families' reductions are now
    independently verified as correct implementations (Family B in #3, Family A
    in #8's review) — so an implementation bug in the reduction is ruled out.
    What #8 does *not* rule out is the reduction *convention* (azimuthal
    averaging over the four-zone geometry) harbouring a systematic bias; nobody
    has stress-tested that. The residual's most likely locus is therefore
    narrowed to the count chain / spray-belt geometry, not eliminated to it.

## `checks/`

Scripts that produced the numbers above. All run standalone under
`uv run python <path>` and import from `arty` (no relative-path assumptions).

| Script                                                                                                                                                                     | Feeds                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [`checks/b-vs-range-75mm.py`](checks/b-vs-range-75mm.py) [`-105mm`](checks/b-vs-range-105mm.py) [`-155mm`](checks/b-vs-range-155mm.py)                                     | #2, #3 — the per-caliber *B(r)* comparison, including the OCR column-identification and transposition fixes |
| [`checks/initial-conditions-probe1.py`](checks/initial-conditions-probe1.py) [`2`](checks/initial-conditions-probe2.py) [`3`](checks/initial-conditions-probe3.py)         | #4 — early zone/V0 probes                                                                                   |
| [`checks/initial-conditions-105mm.py`](checks/initial-conditions-105mm.py) [`-ke`](checks/initial-conditions-105mm-ke.py) [`-ke2`](checks/initial-conditions-105mm-ke2.py) | #4 — 105mm initial conditions and KE-threshold cross-checks                                                 |
| [`checks/initial-conditions-155mm-decay.py`](checks/initial-conditions-155mm-decay.py)                                                                                     | #4 — 155mm velocity-decay comparison vs. Table 59                                                           |
| [`checks/drag-coefficient-calibration.py`](checks/drag-coefficient-calibration.py)                                                                                         | #5 — the `C_D·C_shape` sweep over 1.0–1.71 (SAND92-0243's own data floor/ceiling)                           |
| [`checks/shape-closure-orthogonality.py`](checks/shape-closure-orthogonality.py)                                                                                           | #7 — structural check plus a DoD-1975 reference-area `C_shape` anchor                                       |
| [`checks/b-vs-range-familyA.py`](checks/b-vs-range-familyA.py) [`-aof-ap`](checks/b-vs-range-familyA-aof-ap.py)                                                            | #8 — Family A's per-zone $B(r)$ reduction, AoF-sensitivity band, and flat-vs-graded $A_p$ sensitivity       |
