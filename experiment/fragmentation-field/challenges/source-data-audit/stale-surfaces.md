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

## Added after the final two Phase-3 verdicts landed

The sweep above was written when four threads had ruled. `mach-dependent-fragment-drag`
(ledger §34) and `frag-field-3d-geometry` (§33) have since ruled and add the
following. Two of them outrank everything in Tier 1, because they sit in
**shipped code** rather than in a notebook.

| Surface                                                              | Stale claim                                                                                                                                                                           | Exposure                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `src/arty/fragmentation.py:201-203`                                  | Comment on `DragParams.C_D`: the Mach dependence "does not beat this constant on the 1944 Ordnance velocity-decay data" — **false**; the value 1.28 is sound, only the reason is void | shipped                                |
| `src/arty/zones.py:384-385` (via `derivation.md`)                    | Computes `V0_ogive` / `V0_cyl` from a derivation whose own §6 example contradicts its scoping rationale, previously reconciled by a citation now void                                 | shipped, **which is wrong is unknown** |
| `updates/frag-field-3d-geometry/scoping.md:61, :65-78, :96-97, :290` | "BRL 126 reports nose-spray fragments averaging 2740 ft/s" — the figure **is** Tolch's, but it is the **side** spray and its companion is 3030 f/s, not 1070 (see below)              | working folder                         |
| `src/arty/shells.py:58-60`                                           | 75 mm M48 `mass_deductions=0.200` kg is a placeholder against Tolch's stated 2.35 lb M39 P.D. fuze; case metal 5755 g vs the source's 4962 g, ~16% high, and `N0 = M_case/2μ` uses it | shipped                                |
| `updates/frag-field-3d-geometry/derivation.md:358, :379`             | §6 "range-panel artefact" reconciliation and §7 open-item 2, both built on the same void citation                                                                                     | cited by shipped `zones.py:14`         |
| `updates/mach-dependent-fragment-drag/derivation.md` §5              | The rejection of the Mach-dependent law, decided by a comparison giving the constant a fitted parameter and the Mach law none                                                         | working folder                         |

The `src/arty/` rows are **not repairs this audit performs** — the plan
scopes `src/arty/` to assess-only, and the `zones.py` one is a physics
correctness question that belongs to @modeler under Gate 3. All carry blocking
findings so the decision to defer stays with the human.

______________________________________________________________________

## Added after Phase 5 verification — one row here was itself wrong

Phase 5 overturned the reading behind the `frag-field-3d-geometry` row above.
The "2740 ft/s" figure **is** in Tolch 1938 (`tolch-1938.md:146`, `:1658`,
`:1698`), OCR-damaged to `27^0 f/s`, which is why a literal `grep` for `2740`
found nothing and the absence was misread as fabrication.

**The repair this map previously implied — re-attribute to NWC TP 7124 — must
not be carried out.** It would move a genuine Tolch side-spray value onto a
1990 document that merely prints overlapping digits. The correct repair
restates the figure as Tolch's **side-spray** velocity with its true companion
(3030 f/s penetrating, *faster*), and drops the nose-vs-side framing.

Two further surfaces enter the map from Phase 5:

| Surface                                      | Stale claim                                                                                                                                                                                                                                    | Exposure                           |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Tolch `card.md:57-59` "Drag Model Relevance" | Recommends the velocity-sweep collapse as the drag anchor; the axis is **exactly** degenerate in `C_D·C_shape`, not merely insensitive. Section must leave `doc-reference/` for `challenges/drag-gap-1944/`, leaving a referral                | premise doc for the next drag pass |
| Tolch `card.md:26` + `#L617-L627` anchor     | Calls the collapse "table-sourced and high-confidence" while anchoring at a bare line range that lands on solid-angle prose; that surface misprints two cells of the same table (Panel B @2130: 3.12 vs CSV 1.12; Panel C @1085: 0.65 vs 0.85) | reference doc                      |

Also newly mapped, and *not* stale so much as unsettled: the two retained
DoD-1975 tracing scripts disagree on the true Figure-3 value at Mach 1.00
(~1.257 vs 1.274). Both agree the CSV's 1.233 is wrong; the size of the
correction is not yet settled and is registered as a `note`.

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
