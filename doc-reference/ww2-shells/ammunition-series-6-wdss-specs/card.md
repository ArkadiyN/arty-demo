# Card: WDSS Shell Steel Grades — AMCP 706-249 table 6-1

**Document:** *Engineering Design Handbook, Ammunition Series, Section 6 —
Manufacture of Metallic Components of Artillery Ammunition*, **AMCP 706-249**,
Headquarters, U.S. Army Materiel Command, **July 1964**. Prepared by the
Technical Writing Service of McGraw-Hill from data furnished principally by
Picatinny Arsenal.\
**Copy:** DTIC **AD830266** (zero-padded form `AD0830266`), cleared for public
release by USAMC ltr, 14 Jan 1972.\
**Retained scan:** `source.pdf` beside this card — **not committed**
(`.gitignore:58`); re-acquire from DTIC by that accession number.\
**Cited section:** §6-14 *Prevailing Shell Steel Specifications* (pdf p.10) and
**table 6-1** (pdf p.11).

**Date discipline — the handbook is 1964, the specification is 1953.** §6-14
introduces table 6-1 as "the chemical requirements of shell steels, **as of 17
February 1953**". Neither date is wartime, and the handbook says so directly:
§6-11 is titled *Steel Used Early in World War II* (that steel is X-1340) and
§6-13 *Steels Used After World War II*. **WDSS is not a WW2 shell steel.** This
matters because `src/arty` ships the grade under the identifier
`"US WW2 WDSS1"` — see "What consumes this document", below.

**Admissibility.** This scan carries a clean machine-readable text layer, so
table 6-1 was extracted by script and is verified against the page cell-for-cell
rather than by eye. Every number on this card below was read from that layer.

## Tables

| File                                         | What it holds                                                                | Closure                     |
| -------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------- |
| `tables/table-6-1-chemical-requirements.csv` | Table 6-1 — six grades × five elements, percent by weight, as of 17 Feb 1953 | **none exists** — see below |

```
uv run src/utils/check-table-invariants.py doc-reference/ww2-shells/ammunition-series-6-wdss-specs/tables --all
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/ammunition-series-6-table-6-1-fidelity.py
```

**No arithmetic closure invariant exists for this table, and that is a property
of the table.** A chemical specification's cells are independent policy limits,
not quantities related by arithmetic: nothing sums, nothing is monotonic down a
column, and no stated criterion closes on the rows. The only internal regularity
is that the phosphorus ceiling is constant on all six rows, which the
`.invariant` checks and which is far too weak alone.

What substitutes is stronger than a closure for the failure mode the rule
targets. The second script re-parses table 6-1 out of the PDF's own text layer
and diffs it against the CSV **positionally** — so it answers "was the right row
and column read?" directly, per cell, instead of inferring it from arithmetic.
The CSV was written by that same script's `--emit` mode, so no digit in it was
hand-typed. Printed precision is preserved verbatim: the source's `0.040 max.`
is a three-decimal limit and is not stored as `0.04`.

## What the source contains

### Table 6-1 — chemical requirements (all figures percent by weight)

| Grade      | Carbon    | Manganese | Phosphorus | Sulfur     | Silicon   |
| ---------- | --------- | --------- | ---------- | ---------- | --------- |
| **WDSS 1** | 0.14–0.20 | 1.00–1.30 | 0.040 max. | 0.08–0.13  | 0.10 max. |
| **WDSS 2** | 0.28–0.34 | 0.60–0.90 | 0.040 max. | 0.050 max. | 0.15–0.30 |
| **WDSS 3** | 0.60 max. | 1.00 max. | 0.040 max. | 0.050 max. | 0.15–0.30 |
| **WDSS 5** | 0.65 max. | 1.00 max. | 0.040 max. | 0.050 max. | 0.15–0.30 |
| **WDSS 6** | 0.55 max. | 1.00 max. | 0.040 max. | 0.050 max. | 0.15–0.30 |
| **WDSS 7** | 0.65 max. | 1.30 max. | 0.040 max. | 0.050 max. | 0.15–0.30 |

A `max.` entry states a ceiling with **no floor**. Do not read the absent floor
as zero — the CSV leaves those cells blank for that reason.

**No WDSS 4 appears in the source**; the skip is in the page, not an ingestion
omission (confirmed against the text layer).

Table 6-1's own footnote, verbatim: *"In the above steels, incidental elements
shall not exceed the following: nickel, 0.25 percent; chromium, 0.20 percent;
copper, 0.50 percent; molybdenum, 0.06 percent."* These are **not** the residual
limits of §6-13's post-WWII steel (nickel 0.35, chromium 0.30, copper 0.25, with
Ni+Cr+Cu ≤ 0.50) — two different specifications, easily conflated.

### §6-14 — what the prose adds beyond the table

Anchor: `Prevailing Shell Steel Specifications`.

- **Application by grade.** *"Grades WDSS 1 and 2 are used for the most part for
    60-mm and 81-mm mortar shell forgings; also for the 57-mm recoilless gun
    shell. The other grades cover all calibers from 37-mm to over 155-mm…"*
- **Yield strength — the source does state one.** …*"in which the yield
    strengths vary from **60,000 psi to 80,000 psi**."* (414–552 MPa.) This
    applies to the "other grades" — WDSS 3, 5, 6, 7 — i.e. to the grades used
    for artillery calibers, not to WDSS 1/2. Anchor: `yield`.
- **Melting practice.** *"All shell steel is made by the basic open-hearth
    process to fine grain practice, silicon 0.15 to 0.30 percent."* Bessemer
    steel *"never has been acceptable"* for shell bodies, on low notch toughness
    at subzero temperatures.
- **Governing specification.** *"The current specification for hot-forged
    artillery shell is identified as MIL-S-10520C (ORO)."* Quoted as printed:
    the text layer reads `(ORO)`, near-certainly a scan artifact for `(ORD)`
    (Ordnance), but it is not silently corrected here. Not digitised; it is the
    obvious next document if per-grade mechanical properties are ever needed.

### §6-11 / §6-13 — the lineage this grade replaced

- **§6-11, early WW2:** X-1340 — carbon 0.35–0.45 %, manganese 1.35–1.65 %,
    sulfur 0.075–0.15 %. High Mn was intended to reach properties on cooling from
    forging temperature **without heat treatment**; it failed on the 155-mm for
    volume-to-surface reasons, which is why lower-Mn heat-treated steel was
    adopted. Anchor: `Steel Used Early in World War`.
- **§6-13, post-WWII replacement:** carbon 0.60 % max, silicon 0.15–0.35 %,
    manganese 1.00 % max, sulfur 0.06 % max. Anchor:
    `Steels Used After World War II`.

## Internal inconsistencies in the source

Both readings below were confirmed against the text layer. They are the
**source's own** inconsistencies and must not be "corrected" in the CSV.

1. **Silicon.** §6-14 states all shell steel is made "silicon 0.15 to 0.30
    percent", which matches table 6-1 on five of six rows and **contradicts WDSS
    1's tabulated `0.10 max.`** The table and the prose disagree about WDSS 1.
1. **X-1340 phosphorus.** §6-11 prints *"phosphorus, 0.45 percent maximum"*.
    That is an order of magnitude above any plausible shell-steel P limit
    (table 6-1 uses 0.040) and is almost certainly a typo or scan defect for
    **0.045**. Nothing in this repo cites it; flagged so nobody does.

## What consumes this document

`src/arty/fragmentation.py` catalogues a `SteelParams` entry
`"US WW2 WDSS1"`, whose comment cites this table for the **0.14–0.20 %C,
1.00–1.30 %Mn** band; its 0.17 % midpoint drives `gamma = 47.0`. **That
composition band is a faithful transcription** — verified cell-for-cell by the
fidelity script. Published caveats are `_limitations.qmd` §13; the derivation is
`experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md`.

Two things the page says that a consumer of that entry should read:

- **The identifier `US WW2 WDSS1` is contradicted by its own source** on the
    dating grounds at the top of this card. Applicability is already recorded
    correctly elsewhere (`_parameters.qmd` lists it as 60/81 mm mortar, 57 mm
    recoilless), so this is a naming defect, not a misapplied number.
- **"Table 6-1 is chemistry-only" is true; "the source states no yield
    strength" is not.** §6-14 gives 60,000–80,000 psi for the artillery-caliber
    grades. Whether that bears on the shipped `sigma_f = 800 MPa` (116,000 psi)
    is a criterion-match question — a static yield range and a dynamic fracture
    stress are not the same quantity — and is @model-reviewer's call, not this
    card's.

FINDING\[deferrable\]: AMCP 706-249 §6-14 states yield strengths of 60,000-80,000 psi for artillery-caliber shell steels; `_limitations.qmd` §13 (A6) and prior cards asserted the source gives none, so shipped `sigma_f = 800 MPa` has never been compared against it (affects: experiment/fragmentation-field/\_limitations.qmd, src/arty/fragmentation.py, experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md; since: 2026-08-02)

FINDING\[note\]: `src/arty/fragmentation.py` names the grade `US WW2 WDSS1`, but AMCP 706-249 dates table 6-1 to 17 Feb 1953 and titles §6-11/§6-13 "Steel Used Early in World War II" (X-1340) / "Steels Used After World War II" - WDSS is post-war, so the identifier misdates the grade (affects: src/arty/fragmentation.py, experiment/fragmentation-field/\_parameters.qmd, experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md; since: 2026-08-02)

## What this card deliberately does not do

An earlier version of this card carried three interpretive sections — "Carbon
Content Strategy", "Manganese and Silicon Hardening", "Impurity Control" —
reading design intent into the composition ranges ("likely for projectile body
strength", "possible wartime relaxation"). **None of that is in the source.**
Per the audit's narrative-admissibility finding, a reference card does not tell
a reader what to conclude from a source; that is a modelling claim, and it
belongs in a `derivation.md` where @model-reviewer sees it. They are removed
rather than relocated because nothing cited them.

The same version's **"Data Gaps" section was wrong** where it counted: it listed
*yield strength* and *applicable shell calibers for WDSS 3, 5, 6, 7* among
things the source does **not** state. §6-14 states both, in one sentence. A card
that tells a reader a source lacks something it has is why nobody went looking —
which is the whole failure mode this audit exists to catch.

What the source genuinely does not give, for any WDSS grade: tensile strength,
hardness, elongation, impact toughness, or heat-treatment schedule. Nor does it
give a yield strength for WDSS 1 or 2 specifically.

## Provenance of this card

Rewritten 2026-08-02 during the Phase-2.5b source admissibility gate, against
the retained scan. It supersedes a version transcribed from two screenshots
(`wdss.png`, `wdss-2.png`) with no retained source. Every composition figure in
that version proved correct — including the WDSS 1 sulfur 0.08–0.13 that
`ammunition-series-6-wdss-specs.md` twice flagged as "unusually high; verify
against original image", now **confirmed**. The defects were all narrative.
Detail: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
sect. 19.
