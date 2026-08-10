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

| Thread                                              | Question                                                                                         | Status                                                                                                                                                                     |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`drag-gap-1944/`](drag-gap-1944/README.md)         | Does Family B reproduce the 1944 Ordnance Dept. B-vs-range data — and if not, is drag the cause? | **Re-baselined — headline FAIL void; drag re-adjudication open.** See [`drag-gap-1944/b-vs-range-rebaseline.md`](drag-gap-1944/b-vs-range-rebaseline.md)                   |
| [`mott-scale-gap/`](mott-scale-gap/)                | Is `mott_params` an order of magnitude too small?                                                | **Fix landed — revalidation open** → `updates/mott-fragment-shape-closure/`; see [`mott-scale-gap/rebaseline-verdict.md`](mott-scale-gap/rebaseline-verdict.md)            |
| [`count-gap-1938/`](count-gap-1938/count-chain.md)  | Why is Tolch 1938's absolute perforating-fragment count over-predicted 4–6×?                     | **Re-baselined, then re-closed post-6c1faff — count arm now met-or-marginal; one inference void.** See [`count-gap-1938/count-chain.md`](count-gap-1938/count-chain.md) §4 |
| [`gravity-ke/`](gravity-ke/gravity.qmd)             | Does omitting gravity matter for fragment KE?                                                    | **Closed** — no (≤0.003 % inside the 0–100 m envelope)                                                                                                                     |
| [`source-data-audit/`](source-data-audit/README.md) | Is every external source this model rests on faithfully transcribed, and what breaks if not?     | **Audit complete, repairs open** — 62 findings, 20 blocking. Start at [`source-data-audit/remediation-plan.md`](source-data-audit/remediation-plan.md)                     |

**`drag-gap-1944` status detail.** The Phase-3 re-run has ruled. The published
"FAIL — over-predicts by 7–34×, growing with range" is **void**: all three
scripts compared the model against the mild-steel-perforation column while
applying the 58 ft-lb casualty criterion (digit-for-digit match to
`*-perforation-1-8in.csv`, wrong r-grid included). Against the genuine
closure-checked casualties columns, Family B **passes** the factor-of-2
criterion at 8/10, 9/11 and 11/11 ranges, and the residual *inverts* — over at
short range, under at long, not a one-directional miss. The "systematic
Family B calibration issue" explanation dies with its premise. What is **not**
settled: the drag chain spawned from that void gap has now been re-adjudicated
and the update **closed and half-retired** — its ballistic-density anchor
(the shipped $C_D$ = 1.28, $C_\text{shape}$ = 2.0890) survives every shock,
while its Mach-dependence adjudication is withdrawn, because the comparison
that rejected a $C_D(M)$ law was scored on the same wrong column and gave the
constant a free parameter the curve did not have
(`updates/mach-dependent-fragment-drag/README.md`). The decision not to model
speed-dependent drag stands on architectural cost and is published as
limitation 15. This thread is re-baselined, not closed.

`drag-gap-1944/README.md` and `_validation.qmd` published the void "Closed —
residual sits at the geometric ceiling" verdict after the index above had
already been restated; both surfaces are now restated to match (2026-08-08).
Marker deleted.

**`count-gap-1938` status detail.** Two things happened to this thread, in
order. (1) Re-baselined against the extracted-once Tolch series: the
pit-recovered count is **779, not 803** — every $N/803$ figure in
`count-chain.md` moves up 3.1 %, and the mean recovered fragment mass is
7.40 g, not 6.85 g. That re-baseline on its own flipped no PASS/FAIL row.
(2) **Re-closed against shipped code after 6c1faff / `50b734e`, and that
does flip rows.** With $M_\text{case}$ = 4980 g, $V_0$ = 864.4 m/s,
$N_0$ = 3016, the *sourced*-threshold row moves from outside §4's 2× PASS
band (2.2–2.5×) to inside it: 126 J — Tolch's own smallest-perforating-hole
bound, the only criterion-matched sourced probe — gives $N/779$ = 1.73 /
$N/700$ = 1.92. **The count arm of the PASS test is now
met or marginal, not failed**, so §4's published "FAIL — count chain
implicated, proceed to C2" is no longer supported and an aggressive C2 would
over-correct. (A second probe, 78.6 J = 58 ft-lb, was previously reported
alongside 126 J as a sourced-threshold row at 2.00 / 2.23. It is the Ordnance
Dept. 1944 personnel-casualty **incapacitation** criterion — not a
wood-perforation threshold — so it is criterion-mismatched for this arm and is
no longer counted as sourced:
`updates/sourced-wood-perforation-threshold/review-criterion-check.md`. It was
the weaker of the two rows; dropping it does not move the verdict.) The
falloff-ratio arm (A→D within 0.10 of 0.557) is still
unmet and still tied to the fitted $E_{thr}$, so the test stays compound and
C1 stays the gating item — now as *confirmation* of a provisional PASS rather
than a rescue of a FAIL.
**(3) C1 is now discharged, and it flips the count arm back to FAIL
(2026-08-10).** A sourced *mass-dependent* threshold exists — plug shear-out,
$E_{thr}(m)=\tfrac12\tau\pi D(m)t^2$, $\tau$ = 8.96 MPa from Sanborn 2019
(ASTM D143), shipped as `arty.perforation.perforation_threshold_energy`
(`updates/sourced-wood-perforation-threshold/derivation.md` §7.3). Nothing in
it is fitted to Tolch. On it the chain gives $N/779$ = **2.47** / $N/700$ =
**2.75** (§7.4 Check 4, direction pre-registered; script
`count-gap-1938/checks/count-chain-plug-shear.py`) — **outside** the 2× band,
where the 126 J scalar row was inside at 1.73 / 1.92. The $\eta$ = ½ band
spans 2.32–2.65 on /779; only the $\eta$ = 1 rigid geometric bound
(1.82–1.98) lands inside, and $\eta$ is not free to be tuned. So the
"provisional PASS" reading in (2) does not survive: the residual is larger
than the 126 J row implied, and it relocates to $f$ / Mott $\mu$ / the
recovery census. Live text: `count-gap-1938/count-chain.md` §2 "The
criterion-correct row" and the banner over §4 "Verdict framing";
`rebaseline-verdict.md` §2–§3 are superseded and marked so.
One inference is **void**: §2's "the residual is in the perforating
fraction, *not the population*" — a threshold-free cumulative-spectrum test
finds the model over-counting **1.78–2.24×** (Tolch-metal basis, current
shipped parameters) with the threshold removed entirely. The decomposition of
the ~3.3–3.7× fitted-threshold over-count restates as ~1.65–2.05×
threshold-fit artefact × ~1.7–2.0× genuine count-chain excess. C1 (a sourced perforation threshold, blocked on
@librarian) remains the recommended first move. C4 (fuze/base mass
bookkeeping) was promoted from "note only" to "gates C2" by the re-baseline
and has since been **demoted again**: `50b734e` sourced the deduction
(200 g → 975 g, TM-9-1901 / TM-9-1904) so it is no longer a free knob, and
dropping the coarsest recovery screen now moves the threshold-free residual
1.78× → 2.03× (*up*, not down to the 1.19× previously reported — that figure
came from a numerator/denominator-inconsistent variant, an open finding).
C4's live question is criterion-match (which metal weight is the right
spectrum denominator), not magnitude.

## `mott-scale-gap/`

Three working notes, run in order:

- [`mott-scale-gap/_params_provenance_note.md`](mott-scale-gap/_params_provenance_note.md) — what `mott_params` is and where its values came from
- [`mott-scale-gap/_scale_verdict_ledger.md`](mott-scale-gap/_scale_verdict_ledger.md) — the gap is real; γ/σ_f is *not* the cause; localises it to the mass closure
- [`mott-scale-gap/_shape_closure_check.md`](mott-scale-gap/_shape_closure_check.md) — verdict **NO**: the cube closure is the model author's simplification, not the cited literature's

**Status detail.** The scale gap is confirmed real and localised to the cube
mass closure (α = 1 imposed where Gold 2017 eq. (4) requires
α = (l₀/x₀)(t₀/x₀)); γ/σ_f is excluded as the cause. The α closure has since
landed in `src/arty/fragmentation.py`, so this is not "correction open" — but
it is not resolved either: `_shape_closure_check.md` §5 leaves predicted
x₀ ≈ 3.9 mm about 3× below Tolch's recovered breadth, which α cannot absorb,
and `_scale_verdict_ledger.md` §4 leaves break-up velocity unquantified and the
constant B of Mott's engineering closed form blocked on @librarian. All
magnitudes in the two notes are superseded by the γ′ = 47 rebaseline —
`updates/mott-fragment-shape-closure/rebaseline-verdict.md`.

No `checks/` directory: the scripts behind these notes
(`mott_scale_check.py`, `mott_shape_closure.py`) were written before the
retention rule and were never committed — they are lost. The numbers survive
only as reported in the notes. Reproducing them means rewriting the scripts,
which is exactly the cost the retention rule exists to prevent.
