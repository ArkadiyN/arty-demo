# Phase 6 — stale claims on published surfaces

Inventory only. **Nothing here is repaired by this pass** — the audit's
deliverable is a map to drive the redo (plan, "Outcome sought"). Each entry
names the surface, the claim as published, what the Phase-3 re-baseline did to
it, and the artifact carrying the corrected reading.

Ordering below is by **reader exposure**, not by size of the error: the two
`.qmd` partials are the integrated model notebook a reader actually meets, and
they are the only surfaces here that are not themselves audit artifacts.

Sources of truth for the corrections:

- `challenges/drag-gap-1944/b-vs-range-rebaseline.md`
- `challenges/count-gap-1938/rebaseline-verdict.md`
- `challenges/mott-scale-gap/rebaseline-verdict.md`
- `updates/mott-fragment-shape-closure/rebaseline-verdict.md`

______________________________________________________________________

## Tier 1 — reader-facing notebook partials

### 1a. `_validation.qmd` "Check 7" — publishes a void FAIL

Lines ~178–188. Published: *"**Verdict: FAIL** … Family B over-predicts $B(r)$
by roughly 7–34×, growing with range"*, attributed to the 1944 casualty tables
(43/51/59), and concluding *"a systematic Family B calibration gap"*.

**Void.** All three scripts compared the model against the
mild-steel-perforation column while applying the 58 ft-lb casualty criterion.
Against the genuine casualties columns Family B **passes** the factor-of-2
criterion at 8/10 (75mm), 9/11 (105mm) and 11/11 (155mm) ranges, and the
residual *inverts* sign with range — over at short range, under at long. The
"systematic calibration gap" reading dies with its premise: the pattern it
generalised from was one column-misidentification repeated three times, which
is why it looked consistent across three "independent" shells.

Also stale in the same block: the link target
`challenges/drag-gap-1944/b-vs-range.html` renders from `b-vs-range.qmd`, which
carries the same void numbers (Tier 2 below), so the surface and the page it
points at must move together.

### 1b. `_limitations.qmd` L1 addendum — publishes a void *inference*

Lines ~128–142. This is the more serious of the two, because the defect is not
a number that moved. Published: *"the Mott stage is exonerated; the residual is
localized to the fitted perforation threshold"* and, flatly, **"The gross
fragment population is not the defect."**

**Void.** `count-gap-1938/rebaseline-verdict.md` refutes exactly this with a
*threshold-free* test: matching cumulative **mass fraction** instead of imposing
a mass cut removes the threshold, the drag chain and the spray geometry from
the comparison entirely, and the model still over-counts by 1.2–2.7×. The
decomposition restates as **~2.1× threshold-fit artefact × ~1.9× genuine
count-chain excess** — so the population is *partly* the defect, and the
exoneration is withdrawn. Note the published claim was already inconsistent
with `count-chain.md` §2's own closing paragraph before any number moved; the
re-baseline is what prompted building the test that settles it.

Numbers stale in the same paragraph:

| Published                      | Corrected  | Source                             |
| ------------------------------ | ---------- | ---------------------------------- |
| 803 pit-recovered              | **779**    | `tables/pit-screen-recovery.csv`   |
| (mean 6.85 g quoted elsewhere) | **7.40 g** | `checks/count-chain-rebaseline.py` |

$N_0 = 3627$ is unaffected and still falls between Tolch's two totals, so the
bracketing argument itself survives — only the conclusion drawn from it does
not.

______________________________________________________________________

## Tier 2 — challenge write-ups carrying the void FAIL

These are permanent published verdicts, so they are restated rather than
deleted; the thread index has already been restated, these have not.

| Surface                                                     | Stale claim                                                      |
| ----------------------------------------------------------- | ---------------------------------------------------------------- |
| `challenges/drag-gap-1944/README.md:7`                      | **"Status: Closed."** + "drag was implicated"                    |
| `challenges/drag-gap-1944/README.md:21–23`                  | "residual sits at the geometric ceiling" — the closure rationale |
| `challenges/drag-gap-1944/README.md:43`                     | Row 2: "over-predicts *B(r)* by ~7–34×, growing with range"      |
| `challenges/drag-gap-1944/b-vs-range.qmd:270, :389`         | The 7–34× figure, twice, incl. the concluding verdict            |
| `challenges/count-gap-1938/count-chain.md:102, :117, :131`  | $N/803$ ratios, "803 recovered", "mean 6.85 g"                   |
| `challenges/drag-gap-1944/tolch-1938-panel-distance.md:215` | "recovered fragment mass **6.85 g**"                             |

`count-chain.md` already carries a blocking marker naming these; it is listed
here for completeness of the surface map, not as a second registration.

______________________________________________________________________

## Tier 3 — superseded magnitudes in update folders

Working folders, lower exposure, but they are what a later pass reads as
premise.

| Surface                                                      | Published                                                        | Superseded by                                   |
| ------------------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------- |
| `updates/mach-dependent-fragment-drag/scoping.md:24, :137`   | 7–34× *B(r)* gap as the **motive** for the whole update          | The gap is void — `b-vs-range-rebaseline.md`    |
| `updates/mach-dependent-fragment-drag/derivation.md:232`     | "~3× far-field reduction against a 7–34× *B(r)* over-prediction" | ditto                                           |
| `challenges/mott-scale-gap/_scale_verdict_ledger.md:42, :58` | μ = 0.235 g, N₀ = 12 256, gap **4–15×**                          | μ = 0.382 g, N₀ ≈ 7 540, gap ≈2.5–9× at γ′ = 47 |
| `updates/mott-fragment-shape-closure/scoping.md:75`          | "current (cube, α=1) 0.235 g, 4–15× low"                         | ditto                                           |

`updates/mott-fragment-shape-closure/derivation.md:184, :200` quote
0.235 → 0.793 g and 12 256 → 3 627 as a *transition*, which is a correct record
of what that change did. Those are **not** stale and must not be "corrected" —
they describe the pre- and post-state of a specific edit, not a current value.

______________________________________________________________________

## Not a surface

`experiment/fragmentation-field/fragmentation-field.html` and the per-challenge
`.html` renders do not exist in the working tree — nothing is rendered here, so
there is no stale HTML to reconcile. Re-rendering after the redo will pick up
whatever the `.qmd` files then say.

## Check scripts

Scripts that hard-code superseded values are **not** listed as stale surfaces:
a retained check script is a record of what was run, and the ones affected by
the column inversion already carry their own findings. Two do state superseded
values in *comments/labels* rather than in computation and are worth a touch
when their thread is repaired — `checks/count-chain-decomposition.py:91`
("Tolch pit: 803 recovered, mean 6.85 g") and
`updates/mach-dependent-fragment-drag/checks/tolch-count-post-shape-closure.py:28`
("pit test ~803 recovered").

FINDING\[blocking\]: \_limitations.qmd L1 addendum publishes "the Mott stage is exonerated ... The gross fragment population is not the defect", the exact inference the threshold-free cumulative-mass-fraction test in count-gap-1938/rebaseline-verdict.md refutes (model over-counts 1.2-2.7x with the threshold removed entirely); it also quotes 803 pit-recovered against the corrected 779 (affects: experiment/fragmentation-field/\_limitations.qmd; since: 2026-08-03)
