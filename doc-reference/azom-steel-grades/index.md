# AZoM Steel Reference Pages — Catalog Disambiguation

Topic: Steel grade identification for fragmentation-field model baseline and WD-series designation.

**Date fetched:** 2026-07-25

______________________________________________________________________

## Articles Ingested

### 1. AISI 1335 Alloy Steel (UNS G13350)

- **AZoM ArticleID:** 6667
- **URL:** https://www.azom.com/article.aspx?ArticleID=6667
- **Grade identified:** AISI 1335 / UNS G13350
- **%C composition:** 0.33–0.38% (medium-carbon; **not** ~0.45%)
- **Key properties:** Hardness 179–235 HB; Yield & UTS not provided
- **War Department (WD) nomenclature:** NOT mentioned
- **1-line summary:** Medium-manganese alloy steel for machined components; mid-range carbon.

______________________________________________________________________

### 2. AISI 1045 Steel

- **AZoM ArticleID:** 6130
- **URL:** https://www.azom.com/article.aspx?ArticleID=6130
- **Grade identified:** AISI 1045
- **%C composition:** 0.42–0.50% (matches ~0.45% baseline noted in catalog)
- **Key properties:** YS = 310 MPa / **45000 psi**; UTS = 565 MPa / 81900 psi; Hardness 163 HB
- **War Department (WD) nomenclature:** NOT mentioned
- **1-line summary:** Medium-carbon steel; exact match for "45000 psi" yield-strength figure in fragmentation catalog baseline.

______________________________________________________________________

### 3. AISI 1020 Steel

- **AZoM ArticleID:** 6114
- **URL:** https://www.azom.com/article.aspx?ArticleID=6114
- **Grade identified:** AISI 1020
- **%C composition:** 0.17–0.23% (low-carbon; significantly below AISI 1045)
- **Key properties:** YS = 294.74 MPa / 42,748 psi; UTS = 394.72 MPa / 57,249 psi; Hardness 111 HB; high ductility (36.5% elongation)
- **War Department (WD) nomenclature:** NOT mentioned
- **1-line summary:** Low-carbon steel with excellent machinability and ductility; candidate for mislabeled "WD55" if it refers to AISI 1020.

______________________________________________________________________

## Key Findings

1. **None of the three pages mention War Department (WD) nomenclature or WD-series designations.**

    - This suggests the "WD55" designation may be a data-entry error, a reference to an obsolete military standard not covered by these contemporary AZoM articles, or a misremembered specification number.

1. **AISI 1045 (45000 psi yield strength) appears to be the source of the baseline catalog entry.**

    - The exact match of 45000 psi is too precise to be coincidence.
    - %C range (0.42–0.50%) aligns with the ~0.45% noted.
    - **Recommendation:** Verify the original baseline citation; update catalog metadata if uncited.

1. **AISI 1020 vs. AISI 1335: Candidate for "WD-X1335"**

    - AISI 1335 (0.33–0.38% C) is higher-carbon than AISI 1020 (0.17–0.23% C).
    - Neither page mentions WD nomenclature or any tie to the "WD55" designation.
    - **If the "WD55" was a typo/mislabel**, AISI 1020 is a more likely candidate due to ubiquity and the "55" pattern (if it refers to a spec suffix), but this is speculative without historical WD-series documentation.

______________________________________________________________________

## Recommendation for Next Steps

To resolve the "WD55" ambiguity:

- Search for historical War Department steel specifications (WD-series) in military-standards archives or historical references.
- Cross-check the fragmentation model's baseline against metallurgy references with explicit WD nomenclature (e.g., MIL-SPEC standards, historical military manuals).
- If no WD designation is found, treat "WD55" as a documentation error and use AISI 1020 or AISI 1045 based on the intended application (high ductility vs. moderate strength).

______________________________________________________________________

## Resolution (2026-07-25)

**"WD55" was a working label, not a documented designation — none of the
candidates above are correct.** Primary WD sources since located identify the
grade as **WDSS-1**:

- `doc-reference/ww2-shells/ammunition-series-6-wdss-specs/index.md`
    (Ammunition Series 6, Table 6-1, 17 Feb 1953) — WDSS-1: 0.14–0.20% C,
    1.00–1.30% Mn, applied "for the most part" to 60mm/81mm mortar shell
    forgings.
- M49A2 (60mm mortar) drawing, parent-supplied
    (`/mnt/f/Projects/TMP/AgenticCoding/M49A2_Drawing.pdf`) — cited as
    confirming WDSS-1 application to this specific shell; doc-reference capture
    of this source is in progress.

Per parent direction, the handbook composition (0.14–0.20% C, Table 6-1)
governs over any figure implied by the drawing itself. The catalog/model
working label is being renamed from "WD55" to "WDSS1" throughout
`experiment/fragmentation-field/updates/` accordingly. The AISI candidates
above are superseded and kept here only for audit trail.
