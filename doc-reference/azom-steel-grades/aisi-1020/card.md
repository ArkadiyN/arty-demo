# AISI 1020 Steel — Card

**Source:** AZoM article "AISI 1020 Steel" (ArticleID=6114)

## Composition (anchor: "## Chemical Composition")

- **Carbon:** 0.17–0.23%
- **Manganese:** 0.30–0.60%
- **Phosphorus:** ≤0.040%
- **Sulfur:** ≤0.050%
- **Iron:** balance (99.08–99.53%)

(Silicon is not listed in the source's composition table.)

## Mechanical Properties (anchor: "## Mechanical Properties")

- **Yield Strength (YS):** 294.74 MPa (42,748 psi)
- **Ultimate Tensile Strength (UTS):** 394.72 MPa (57,249 psi)
- **Hardness (Brinell):** 111 HB
- **Elongation at Break:** 36.5%
- **Reduction of Area:** 66.0%
- **Charpy Impact:** 16.9–68.0 J (source notes: temperature-dependent)
- **Izod Impact:** 125 J
- **Modulus of Elasticity:** 200 GPa (29,000 ksi)

## Physical Properties (anchor: "## Physical Properties")

- **Density:** 7.87 g/cc

## Characteristics & Applications (anchor: "## Characteristics")

- High machinability, high strength, high ductility, good weldability
- Resists induction and flame hardening due to low carbon
- Responds to carburization for case hardening (Rc > 65)
- Used for shafts, gears, fasteners, and general structural components

## Remarks — extractor commentary, not source text (anchor: "## Remarks")

`aisi-1020.md`'s `## Remarks` section is **not** the AZoM page. Its opening
sentence — "No War Department (WD) nomenclature or historical WD-series
designation is mentioned in this reference" (anchor: "No War Department (WD) nomenclature")
— is a statement *about* the reference, which the reference cannot make about
itself. It is the extractor answering a question this repo asked, written into
a file that otherwise presents itself as the processed source, with nothing
marking the transition. The same defect is registered against the sibling
`aisi-1045.md`, whose `## Remarks` section additionally cross-references this
repo's own fragmentation catalog.

Treat nothing under that heading as the source saying anything.

**No "WD-1020" claim is supported here.** An earlier version of this card asked
"Candidate for *WD-1020*?" and answered that the composition "is consistent
with" it. Consistency with a low-carbon steel is not evidence of a
designation — no WD nomenclature appears in this reference at all, and which WD
grade (if any) corresponds to AISI 1020 is a criterion-match question,
unsettled here and not answerable from this page.

## Provenance of this card

- The document is a live AZoM web reference page (ArticleID=6114), not a paper
    or scanned report. No PDF is retained — there is nothing to archive as
    `source.pdf`; the only re-acquisition path is re-fetching the live URL.
- Citable surface for numbers: `aisi-1020.md` (the processed page text), except
    its `## Remarks` section per above. This `card.md` is a navigation index
    only — do not cite it in place of `aisi-1020.md`.
- Every value above was checked against `aisi-1020.md` on 2026-08-03 and
    matches.
- No `tables/*.csv` extraction exists for this document. Its composition and
    mechanical-property tables are short and are not cited downstream today,
    and they carry no closure invariant of their own — a tabulated materials
    datasheet has no internal relation that must hold. If this document ever
    feeds a committed artifact, extract it once per
    `.claude/rules/source-data-fidelity.md` and flag the absent invariant for
    human review rather than inventing one.
- **Comparisons to AISI 1045 have been struck.** The prior card carried "well
    below the 0.45% of AISI 1045" and "significantly higher ductility than AISI
    1045" inline among this source's own values; the AZoM page makes no such
    comparison, and a cross-source contrast belongs in whatever artifact is
    choosing between the two grades.
