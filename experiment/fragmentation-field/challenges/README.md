# Challenges — fragmentation-field

Each subdirectory is one **investigation thread**: a question chased across
several documents, with the check scripts that produced its numbers. Threads
are permanent — they publish a verdict that informs readers, and later passes
re-read them instead of re-deriving.

Layout inside a thread:

- `README.md` — thread index and current verdict (multi-document threads only)
- `*.md` / `*.qmd` — the challenge write-ups, in the order they were run
- `checks/*.py` — the scripts that produced the numbers, kept and runnable

## Threads

| Thread                                              | Question                                                                                         | Status                                                                                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`drag-gap-1944/`](drag-gap-1944/README.md)         | Does Family B reproduce the 1944 Ordnance Dept. B-vs-range data — and if not, is drag the cause? | **Re-baselined — headline FAIL void; drag re-adjudication open.** See [`drag-gap-1944/b-vs-range-rebaseline.md`](drag-gap-1944/b-vs-range-rebaseline.md)        |
| [`mott-scale-gap/`](mott-scale-gap/)                | Is `mott_params` an order of magnitude too small?                                                | **Fix landed — revalidation open** → `updates/mott-fragment-shape-closure/`; see [`mott-scale-gap/rebaseline-verdict.md`](mott-scale-gap/rebaseline-verdict.md) |
| [`count-gap-1938/`](count-gap-1938/count-chain.md)  | Why is Tolch 1938's absolute perforating-fragment count over-predicted 4–6×?                     | **FAIL — C1–C5 all discharged, no sub-candidate remaining.** See [`count-gap-1938/count-chain.md`](count-gap-1938/count-chain.md) §4                            |
| [`gravity-ke/`](gravity-ke/gravity.qmd)             | Does omitting gravity matter for fragment KE?                                                    | **Closed** — negligible (see [`gravity.qmd`](gravity-ke/gravity.qmd))                                                                                           |
| [`source-data-audit/`](source-data-audit/README.md) | Is every external source this model rests on faithfully transcribed, and what breaks if not?     | **Audit complete, repairs open** — 62 findings, 20 blocking. Start at [`source-data-audit/remediation-plan.md`](source-data-audit/remediation-plan.md)          |

**`drag-gap-1944` status detail.** The Phase-3 re-run has ruled. The published
over-prediction verdict is **void**: all three scripts compared the model
against the mild-steel-perforation column while applying the casualty criterion
(wrong column). Against the genuine closure-checked casualties columns, Family B
**passes** the factor-of-2 criterion at nearly every tabulated range for all
three shells, and the residual *inverts* — over at short range, under at long,
not a one-directional miss (see [`drag-gap-1944/b-vs-range.qmd`](drag-gap-1944/b-vs-range.qmd)
§Verdict). The "systematic Family B calibration issue" explanation dies with its
premise. What is **not** settled: the drag chain spawned from that void gap has
now been re-adjudicated and the update **closed and half-retired** — its
ballistic-density anchor (see
[`updates/mach-dependent-fragment-drag/derivation.md`](updates/mach-dependent-fragment-drag/derivation.md)
§1–§4) survives every shock, while its Mach-dependence adjudication is
withdrawn, because the comparison that rejected a $C_D(M)$ law was scored on
the same wrong column and gave the constant a free parameter the curve did not
have (`updates/mach-dependent-fragment-drag/README.md`). The decision not to
model speed-dependent drag stands on architectural cost and is published as
limitation 15. This thread is re-baselined, not closed.

`drag-gap-1944/README.md` and `_validation.qmd` published the void "Closed —
residual sits at the geometric ceiling" verdict after the index above had
already been restated; both surfaces are now restated to match (2026-08-08).
Marker deleted.

**`count-gap-1938` status detail.** Two things happened to this thread, in
order. (1) Re-baselined against the extracted-once Tolch series: pit-recovered
count and mean fragment mass were corrected. That re-baseline on its own flipped
no PASS/FAIL row. (2) **Re-closed against shipped code after `50b734e`, and
that does flip rows.** The sourced-threshold row (126 J — Tolch's own
smallest-perforating-hole bound, the only criterion-matched sourced probe) moved
inside the 2× PASS band. (A second probe, 78.6 J = 58 ft-lb, was previously
reported alongside 126 J as a sourced-threshold row. It is the Ordnance
Dept. 1944 personnel-casualty **incapacitation** criterion — not a
wood-perforation threshold — so it is criterion-mismatched for this arm and is
no longer counted as sourced:
`updates/sourced-wood-perforation-threshold/review-criterion-check.md`.) The
falloff-ratio arm is still unmet and still tied to the fitted $E_{thr}$, so the
test stays compound and C1 stays the gating item — now as *confirmation* of a
provisional PASS rather than a rescue of a FAIL.
**(3) C1 is now discharged, and it flips the count arm back to FAIL
(2026-08-10).** A sourced *mass-dependent* threshold exists — plug shear-out,
$E_{thr}(m)=\tfrac12\tau\pi D(m)t^2$, $\tau$ from Sanborn 2019 (ASTM D143),
shipped as `arty.perforation.perforation_threshold_energy`
(`updates/sourced-wood-perforation-threshold/derivation.md` §7.3). Nothing in
it is fitted to Tolch. On it the chain lands **outside** the 2× band, where
the 126 J scalar row was inside; direction pre-registered. Live text:
`count-gap-1938/count-chain.md` §2 "The criterion-correct row" and the banner
over §4 "Verdict framing"; `rebaseline-verdict.md` §2–§3 are superseded and
marked so. One inference is **void**: §2's "the residual is in the perforating
fraction, *not the population*" — a threshold-free test finds the model
over-counting above the 2× band with the threshold removed entirely. (C4's
coarsest-screen move goes *up*, not down as previously reported — that figure
came from a numerator/denominator-inconsistent variant, an open finding. C4's
live question is criterion-match, not magnitude.)
**(4) C2 is now discharged as well, and the arm still fails (2026-08-10).** A
source-defined break-up velocity fraction ships as
`arty.fragmentation.breakup_velocity_fraction` (`updates/breakup-velocity-fraction/derivation.md`
§5). Run against C1's fixed plug-shear threshold it reduces the count residual
but does **not** clear the 2× band at any admissible value. No velocity-basis
lever remains. Live text: `count-gap-1938/count-chain.md` §2 "The verdict row"
and §4 "Verdict framing after the 2026-08-10 C1+C2 re-closure".
**(5) C5 is now discharged (2026-08-10, later pass), and it does not rescue
the verdict.** The premise behind "trending INDETERMINATE pending C5" — that
Tolch's 700 column is detection-limited — does not survive: Tolch's census
grades every hit as perforation, penetration or dent, so the 700 column is
perforation-limited by construction and C5 collapses into C1, which already
models that mechanism; that census-grading argument alone discharges C5. A
secondary upper-bound reading — resting on a smallest-perforating-hole datum
that is inadmissible (`count-chain.md` §3 C5 reading (iv)) — agrees but is
supporting only. **The standing verdict is therefore a
plain, genuine FAIL — not INDETERMINATE.** The live recommendation ranking
drops C5 (discharged, no credit) and becomes **C3 next, then C4**. Live text:
`count-gap-1938/count-chain.md` §3 "C5" and §4 "The INDETERMINATE clause is
now discharged".
**(6) C3 is now discharged too (2026-08-15), real but not actionable.** The
power-law tail shape reduces the residual only when the exponent is fitted to
Tolch's own pit census — it cannot ship. Every *sourced* alternative shape
(Mott's own 3D thick-wall exponent; a power-law tail per the literature
@librarian collected) moves the residual the *wrong* way. Recorded as a
limitation, not a `src/arty/` change. Reviewed PASS
(`count-gap-1938/review-c3.md`). Live text: `count-gap-1938/mott-tail-shape.md`
and `count-gap-1938/count-chain.md` §3 "C3".
**(7) C4 is now discharged too (2026-08-15), closing the ranking — no
sub-candidate remains.** The criterion-correct spectrum denominator is Tolch's
empty unfuzed shell (case metal alone, 10.94 lb), which agrees with the model's
own fuze-excluded $M_\text{case}$ to under 1%. C4 is a criterion choice worth a
modest reduction within the correct family, not a driver, and **no `src/arty/`
change follows**. Reviewed PASS-with-limitations (`count-gap-1938/review-c4.md`).
**With C1 through C5 all discharged, the count arm's standing verdict is final:
genuine FAIL on both plug-shear and threshold-free bases — every admissible
pairing sits above the 2× acceptance band, and no further candidate is under
investigation.** Live text: `count-gap-1938/spectrum-mass-basis.md`,
`count-gap-1938/count-chain.md` §3 "C4" and
`count-gap-1938/rebaseline-verdict.md`'s fourth re-closure banner.
**(8) An out-of-band avenue was also tried and discharged (2026-08-16):
mass-dependent fragment shape.** `updates/mass-dependent-fragment-shape/` made
the aspect-ratio moment correction $c$ per-shell — each shell's own Mott
spectrum — giving a marginally worse residual on the 75 mm chain, not better.
It **shipped anyway** (`5d742b4`), because $c$ is a moment identity of the
shipped Mott shape closure and belongs in the registry. Live text:
`updates/mass-dependent-fragment-shape/derivation.md` §7 and
`updates/mass-dependent-fragment-shape/review.md`.

**(9) The thread was re-closed against that shipped `c` (2026-08-16); the
verdict direction is unchanged.** `arty.shells.SHELLS` now carries
`aspect_ratio = 1.6 * MOTT_ASPECT_MOMENT_C[<shell>]`, so $\mu$ and $N_0$ shift
slightly for the 75 mm M48. Every count in items (1)–(7) above therefore reads
slightly higher (the smaller $\mu$ eats part of the larger $N_0$ through the
survival factor). **No verdict flips: still FAIL, still outside the 2× band on
both denominators, still no sub-candidate remaining.** Live text:
`count-gap-1938/count-chain.md` (re-closed throughout),
`count-gap-1938/rebaseline-verdict.md`'s fifth re-closure banner, script
`count-gap-1938/checks/count-chain-aspect-moment-reclosure.py`.

## `mott-scale-gap/`

Three working notes, run in order:

- [`mott-scale-gap/_params_provenance_note.md`](mott-scale-gap/_params_provenance_note.md) — what `mott_params` is and where its values came from
- [`mott-scale-gap/_scale_verdict_ledger.md`](mott-scale-gap/_scale_verdict_ledger.md) — the gap is real; γ/σ_f is *not* the cause; localises it to the mass closure
- [`mott-scale-gap/_shape_closure_check.md`](mott-scale-gap/_shape_closure_check.md) — verdict **NO**: the cube closure is the model author's simplification, not the cited literature's

**Status detail.** The scale gap is confirmed real and localised to the cube
mass closure (α = 1 imposed where Gold 2017 eq. (4) requires
α = (l₀/x₀)(t₀/x₀)); γ/σ_f is excluded as the cause. The α closure has since
landed in `src/arty/fragmentation.py`, so this is not "correction open" — but
it is not resolved either: `_shape_closure_check.md` §5 leaves a residual x₀
gap that α cannot absorb, and `_scale_verdict_ledger.md` §4 leaves break-up
velocity unquantified and the constant B of Mott's engineering closed form
blocked on @librarian. All magnitudes in the two notes are superseded by the
γ′ rebaseline — `updates/mott-fragment-shape-closure/rebaseline-verdict.md`.

No `checks/` directory: the scripts behind these notes
(`mott_scale_check.py`, `mott_shape_closure.py`) were written before the
retention rule and were never committed — they are lost. The numbers survive
only as reported in the notes. Reproducing them means rewriting the scripts,
which is exactly the cost the retention rule exists to prevent.
