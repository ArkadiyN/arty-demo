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
| [`count-gap-1938/`](count-gap-1938/count-chain.md)  | Why is Tolch 1938's absolute perforating-fragment count over-predicted 4–6×?                     | **Re-baselined — verdict stands, one inference void.** See [`count-gap-1938/rebaseline-verdict.md`](count-gap-1938/rebaseline-verdict.md)                       |
| [`gravity-ke/`](gravity-ke/gravity.qmd)             | Does omitting gravity matter for fragment KE?                                                    | **Closed** — no (≤0.003 % inside the 0–100 m envelope)                                                                                                          |
| [`source-data-audit/`](source-data-audit/README.md) | Is every external source this model rests on faithfully transcribed, and what breaks if not?     | **Audit complete, repairs open** — 62 findings, 20 blocking. Start at [`source-data-audit/remediation-plan.md`](source-data-audit/remediation-plan.md)          |

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

**`count-gap-1938` status detail.** Re-baselined against the extracted-once
Tolch series: the scoping verdict survives. The pit-recovered count is **779,
not 803** — every $N/803$ figure in `count-chain.md` moves up 3.1 %, and the
mean recovered fragment mass is 7.40 g, not 6.85 g. No PASS/FAIL row changes
side. One inference is **void**: §2's "the residual is in the perforating
fraction, *not the population*" — a threshold-free cumulative-spectrum test
finds the model over-counting 1.2–2.7× with the threshold removed entirely.
The decomposition restates as ~2.1× threshold-fit artefact × ~1.9× genuine
count-chain excess. C1 (a sourced perforation threshold, blocked on
@librarian) remains the recommended first move; C4 (fuze/base mass
bookkeeping, 15.4 % of recovered metal against a 3.3 % model deduction) is
promoted from "note only" and now gates C2.

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
