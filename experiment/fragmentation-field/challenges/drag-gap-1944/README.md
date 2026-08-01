# Drag gap vs. the 1944 Ordnance Dept. data

**Question.** Does Family B (`four_zone_lethal_density_field`) reproduce the
1944 Ordnance Dept. *B*-vs-range casualty data — and if not, is the
retardation/drag model the cause?

**Status: open, but narrowed.** The gap is real and reproducible. Drag is
implicated and has since been **corrected** — see
[`../../updates/mach-dependent-fragment-drag/`](../../updates/mach-dependent-fragment-drag/)
([`scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md),
[`derivation.md`](../../updates/mach-dependent-fragment-drag/derivation.md)),
which anchors `C_D·C_shape` to the DoD-1975 ballistic density at **2.67**
(from 0.585). That update **supersedes the inferences drawn in rows #5 and #6 below, and two
of the "Where it stands" bullets** (marked ⚠ inline; the measurements in those
rows stand, the conclusions drawn from them do not). It narrows the *B(r)*
over-prediction from ~2.1–27.3× (pre-anchor) to ~1.9–5.3× (see
[`b-vs-range.qmd`](b-vs-range.qmd)'s refreshed table, and
[`checks/b-vs-range-drag-attribution.py`](checks/b-vs-range-drag-attribution.py))
but does **not** close it; the residual must be sought outside the
retardation law.

## Reading order

| #   | Document                                                                                                                                   | What it settles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [`b-vs-range.md`](b-vs-range.md)                                                                                                           | Scoping. No new `src/arty/` math needed — *B* is a unit conversion + azimuthal average over `lethal_density_point` / `four_zone_lethal_density_field`. Sets the factor-of-2 verdict criterion.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 2   | [`b-vs-range.qmd`](b-vs-range.qmd)                                                                                                         | The comparison itself. Family B over-predicts *B(r)* by ~7–34×, growing with range, across all three calibers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 3   | [`review.md`](review.md)                                                                                                                   | **PASS-with-limitations.** Reduction formula is sound and the over-prediction is real; one 75mm r=40 ft transcription defect found (non-blocking).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 4   | [`initial-conditions-75mm.md`](initial-conditions-75mm.md) [`-105mm`](initial-conditions-105mm.md) [`-155mm`](initial-conditions-155mm.md) | Is it an input mismatch? No. V0 and thresholds match the source; feeding the source's own per-range *m(r)* into `retardation_coeff` shows velocity decay several-fold too slow in all three calibers. Localises the defect to drag.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 5   | [`drag-coefficient-calibration.md`](drag-coefficient-calibration.md)                                                                       | Does a bigger constant drag close it? **No.** Raising combined `C_D·C_shape` from 0.585 into the literature's 1.2–1.7 shrinks the ratio everywhere but closes it nowhere uniformly — the decay curve has the wrong *shape*, not just the wrong scale. **⚠ Conclusion superseded** — that sweep stopped short of the literature-admissible constant; at the DoD-1975 anchor of 2.67 the Mach>0.7 band closes (RMS 0.710 → 0.092, [`updates/mach-dependent-fragment-drag/derivation.md`](../../updates/mach-dependent-fragment-drag/derivation.md) V2). The "wrong shape, not scale" framing is exactly what motivated a Mach-dependent law, which was tested and rejected (scoping §3a, §4 option 3) — a corrected constant was the fix.                                      |
| 6   | [`tolch-1938-panel-distance.md`](tolch-1938-panel-distance.md)                                                                             | Is Tolch (1938) an independent check? Partly, and it **contradicts the remedy**: the panel-radius falloff is shape-degenerate on drag, and the absolute count rules *out* raising drag. Also surfaces a separate, larger defect — the Mott scale (→ [`../mott-scale-gap/`](../mott-scale-gap/)). **⚠ Conclusion superseded** — re-run with post-shape-closure Mott parameters ([`updates/mach-dependent-fragment-drag/scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md) §3d) reverses the sign of this test: the absolute count now vetoes the *current* 0.585 constant (4–31 perforations predicted vs. ~700–800 observed, requiring an impossible ~6.5–12 kJ threshold), not a raised one. The panel-radius degeneracy and the Mott-scale finding stand. |
| 7   | [`shape-closure-orthogonality.md`](shape-closure-orthogonality.md)                                                                         | Does the Mott shape-closure fix (`../mott-scale-gap/` → `updates/mott-fragment-shape-closure/`) close this thread's gap? **No.** `retardation_coeff` never calls `mott_params`; the check feeds it source-tabulated masses directly. The two aspects are structurally independent — reviewed PASS in [`review.md`](review.md).                                                                                                                                                                                                                                                                                                                                                                                                                                               |

## Where it stands

- The velocity-decay gap rests entirely on the Ordnance checks (#4). Tolch
    neither corroborates nor contradicts its *existence* — its drag observable
    is degenerate over a 5× span of `C_D·C_shape`. **⚠ Superseded** — this holds
    for the panel-radius falloff only; post-shape-closure Tolch's *absolute
    count* is not degenerate and rejects the current constant outright
    ([`scoping.md`](../../updates/mach-dependent-fragment-drag/scoping.md) §3d).
- `retardation_coeff`'s single fixed exponential rate cannot reproduce a
    *v(r)* whose deviation changes sign with range, which is what #5 measures.
    This matches the Sandia source's own framing of 1.2–1.7 as a
    *velocity-dependent* combined drag.
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

## `checks/`

Scripts that produced the numbers above. All run standalone under
`uv run python <path>` and import from `arty` (no relative-path assumptions).

| Script                                                                                                                                                                     | Feeds                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [`checks/b-vs-range-75mm.py`](checks/b-vs-range-75mm.py) [`-105mm`](checks/b-vs-range-105mm.py) [`-155mm`](checks/b-vs-range-155mm.py)                                     | #2, #3 — the per-caliber *B(r)* comparison, including the OCR column-identification and transposition fixes |
| [`checks/initial-conditions-probe1.py`](checks/initial-conditions-probe1.py) [`2`](checks/initial-conditions-probe2.py) [`3`](checks/initial-conditions-probe3.py)         | #4 — early zone/V0 probes                                                                                   |
| [`checks/initial-conditions-105mm.py`](checks/initial-conditions-105mm.py) [`-ke`](checks/initial-conditions-105mm-ke.py) [`-ke2`](checks/initial-conditions-105mm-ke2.py) | #4 — 105mm initial conditions and KE-threshold cross-checks                                                 |
| [`checks/initial-conditions-155mm-decay.py`](checks/initial-conditions-155mm-decay.py)                                                                                     | #4 — 155mm velocity-decay comparison vs. Table 59                                                           |
| [`checks/drag-coefficient-calibration.py`](checks/drag-coefficient-calibration.py)                                                                                         | #5 — the `C_D·C_shape` sweep over 1.2–1.7                                                                   |
| [`checks/shape-closure-orthogonality.py`](checks/shape-closure-orthogonality.py)                                                                                           | #7 — structural check plus a DoD-1975 reference-area `C_shape` anchor                                       |
