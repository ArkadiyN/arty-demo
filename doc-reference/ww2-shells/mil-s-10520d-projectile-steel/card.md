# MIL-S-10520D(MU) — Steel, Forging: For Projectile Stock

## Identification

|                                |                                                                       |
| :----------------------------- | :-------------------------------------------------------------------- |
| Title                          | STEEL, FORGING: FOR PROJECTILE STOCK                                  |
| Designation                    | `MIL-S-10520D(MU)`                                                    |
| Date                           | 27 August 1975                                                        |
| Supersedes                     | `MIL-S-10520C(ORD)`, 17 February 1953                                 |
| Custodian / Preparing activity | Army — MU                                                             |
| Project number                 | 1395-A209                                                             |
| Pages                          | 14 (12 numbered + DD Form 1426)                                       |
| Local copy                     | `source.pdf` (gitignored per `.gitignore:58`), `source.md`            |
| Provenance                     | supplied by the user from `/mnt/f/Projects/TMP/Docs/MIL-S-10520D.pdf` |

Scope (§1.1): covers "hot-rolled carbon steel for forging into projectile
bodies."

## Why this document is in the repo

`ammunition-series-6-wdss-specs/card.md` records that AMCP 706-249 §6-14 names
`MIL-S-10520C (ORO)` as the governing specification behind its table 6-1 — the
WDSS grade compositions that reach `src/arty/fragmentation.py`. This document
is the **next revision** of that specification, acquired to check that
transcription against its own source.

It settles three things about the sibling document at once:

1. **Table 6-1 *is* MIL-S-10520C's Table I.** The cover page reads
    "SUPERSEDING MIL-S-10520C(ORD), 17 February 1953" — and §6-14 dates its
    table "as of 17 February 1953". Same day, same table.
1. **`(ORO)` on the AMCP page is a scan artifact for `(ORD)`**, now confirmed
    rather than inferred.
1. **WDSS grades 1–7 are MIL-S-10520 grades 1–7**, and the absent grade 4 is
    real — neither document has one.

## Revision gap — read this before citing anything here

**This is revision D (1975). The document actually cited downstream is
revision C (1953), which is not in hand.** Every number below is direct
evidence about D and only presumptive about C. Using a later revision as if it
were the cited one is the same species of error as reading the wrong column,
so the gap is carried explicitly rather than assumed away.

What the cross-document check (`experiment/fragmentation-field/challenges/source-data-audit/checks/mil-s-10520d-closures.py`) actually
found, diffing all 30 cells of Table I against AMCP's C-era table 6-1:

- **Grades 2, 3, 5, 6 and 7 are identical** across the two revisions — 26 of
    30 cells, plus the incidental-elements footnote word for word.
- **Grade 1 differs on four of five elements.** C-era WDSS 1 is C 0.14–0.20,
    Mn 1.00–1.30, S 0.08–0.13, Si 0.10 max; D's grade 1 is C 0.20 max, Mn 0.90
    max, S 0.050 max, Si 0.20 max.

The pattern — a high-manganese, high-sulfur free-machining grade replaced by a
plain low-carbon one — reads as a **grade redefinition between revisions**,
not a transcription slip. But C is not in hand, so that is evidence, not
proof.

**Consequence for shipped code:** `src/arty/fragmentation.py`'s
`"US WW2 WDSS1"` (0.14–0.20 %C) is the **1953** grade 1 — the revision AMCP
cites. The shipped number is attached to the right revision. Do **not**
"correct" it toward D.

## What this document does *not* contain

**MIL-S-10520 states no mechanical properties of its own.** §3.7.1 requires
the steel to be demonstrated "capable of being heat-treated to meet the
physical properties **specified on the drawing of the projectile for which the
steel is intended**", and §4.5.3 defines yield strength by extension-under-load
against a **specified** value supplied elsewhere.

So the lead "go to the governing specification for per-grade yield strength"
**does not deliver**. AMCP §6-14's 60,000–80,000 psi is the handbook's own
summary, not a spec value quoted from MIL-S-10520.

Two corroborations of §6-14 do fall out, both indirect:

- **The mortar/artillery grade split is real.** §3.7.2(b) exempts grades 1 and
    2 from the heat-treat demonstration entirely, and §4.5.1 selects coupons
    "from each heat of grades 3, 5, 6, and 7". Independent of AMCP, and matching
    it.
- **The yield envelope.** Table X brackets run 60,000–85,000 psi across 37 mm
    to over 155 mm. §6-14 says 60,000–80,000 psi over the same caliber span:
    lower bound exact, upper bound plausibly extended between 1953 and 1975.

## Tables

Transcribed once into `tables/`, per `.claude/rules/source-data-fidelity.md`.
Consumers read the CSVs; nothing re-types these series.

| Table                                            | CSV                                       | Closure                                                                                                                                                                     |
| :----------------------------------------------- | :---------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I — Chemical Requirements                        | `table-1-chemical-requirements.csv`       | cross-document diff vs AMCP table 6-1 (`experiment/fragmentation-field/challenges/source-data-audit/checks/mil-s-10520d-closures.py`); column-identity sums in `.invariant` |
| II — Permissible Variations for Product Analysis | `table-2-product-analysis-variations.csv` | bracket tiling + over/under symmetry (same script)                                                                                                                          |
| X — Size and Heat Treatment of Test Coupons      | `table-10-coupon-selection.csv`           | bracket tiling + coupon-diameter monotonicity (same script)                                                                                                                 |
| X — hold times (second panel)                    | `table-10-hold-times.csv`                 | `table-10-hold-times.invariant`                                                                                                                                             |

Tables III–IX (dimensional tolerances) and XI (corner radii) carry no physics
and are not transcribed; they are in `source.md`.

Anchors are the printed table captions — `Table I - Chemical Requirements`,
`Table II - Permissible Variations for Product Analysis`, `Table X - Size and Heat Treatment of Test Coupons` — all greppable in `source.md`. No bare line
numbers.

### Irregularities recorded as printed, not repaired

- **Table X, the "Over 105mm to 155mm, incl." class opens with a bare
    `65,000`** where the other two classes print a range. By analogy with the
    over-155 mm row it should read "60,000 to 65,000, incl."; as printed, that
    caliber has no bracket below 65,000. Both independent readings of the page
    (300-dpi direct read and the vision extraction) show the bare value, so this
    is the source's own irregularity.
- **Sulfur is printed "0.050 max" in Table I but bracketed "To 0.05" in
    Table II** — differing precision within one document.
- **Leading zeros are dropped inconsistently** (`.65 max` beside `0.60 max` in
    one column). A typewriter artifact, not a precision claim; the CSVs carry the
    normalised `0.65` form and the decimal places are untouched.

## Provenance of this card

Every number here has **two independent readings that agree**, which is what
stands in for the text-layer diff the sibling document could use and this one
cannot.

1. **Direct read** of 300-dpi page renders
    (`experiment/fragmentation-field/challenges/source-data-audit/checks/mil-s-10520d-page-render.py`).
1. **Vision extraction** through `src/utils/pdf-processor.py`
    (`--analyze-formulas`), producing `source.md`.
1. **Cross-document agreement** with AMCP 706-249 table 6-1 on 26 of 30 Table I
    cells and the footnote.

Legs 1 and 2 agree cell-for-cell on Tables I, II and X — including the
inconsistent leading zeros and the bare `65,000`, which is what makes the
agreement meaningful rather than two readers smoothing the same page the same
way.

**This document is also the regression case that exposed a silent failure in
the extraction pipeline.** Its first run through `pdf-processor.py` produced 14
copies of an everyspec watermark, 66 lines, and exit 0 reporting success: the
scan stores each page as 43–58 horizontal strips (largest 3.4% of the page), so
the ">50% of page area in one image rect" test called every page text-based,
while a 41-character watermark made the `bool(text.strip())` scanned-document
guard true on every page. Both gates failed at once, in the same direction.
Diagnosis and the before/after routing are in
`experiment/fragmentation-field/challenges/source-data-audit/checks/vision-gating-probe.py`; the fix is in `src/utils/pdf-processor.py`.
