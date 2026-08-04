# AISI 1045 Steel — Card

**Source:** AZoM article "AISI 1045 Steel" (ArticleID=6130)

## Composition (anchor: "## Chemical Composition")

- **Carbon:** 0.42–0.50%
- **Manganese:** 0.60–0.90%
- **Phosphorus:** ≤0.040%
- **Sulfur:** ≤0.050%
- **Iron:** balance (98.51–98.98%)

(Silicon is not listed in the source's composition table.)

## Mechanical Properties (anchor: "## Mechanical Properties")

- **Yield Strength (YS):** 310 MPa (45000 psi)
- **Ultimate Tensile Strength (UTS):** 565 MPa (81900 psi)
- **Hardness (Brinell):** 163 HB
- **Elongation at Break:** 16.0%
- **Reduction of Area:** 40.0%
- **Modulus of Elasticity:** 200 GPa (29000 ksi)
- **Shear Modulus:** 80 GPa (11600 ksi)
- **Poisson's Ratio:** 0.290

## Physical Properties (anchor: "## Physical Properties")

- **Density:** 7.87 g/cc (0.284 lb/in³)

## Remarks — extractor commentary, not source text (anchor: "## Remarks")

`aisi-1045.md`'s `## Remarks` section is **not** the AZoM page. Both its
sentences are the extractor's own answers to questions this repo asked, written
into a file that otherwise presents itself as the processed source, with
nothing marking the transition:

- "No War Department (WD) nomenclature or historical WD-series designation is
    mentioned in this reference" (anchor: "No War Department (WD) nomenclature")
    is a statement *about* the reference, which the reference cannot make about
    itself.
- "The 45000 psi yield strength value matches the figure cited in the
    fragmentation catalog baseline" (anchor: "45000 psi yield strength value matches")
    names *this repo's* fragmentation catalog. An AZoM article on AISI 1045
    cannot have said it.

Neither may be cited as the source saying anything. The only claim the AZoM
page supports is the tabulated 310 MPa / 45000 psi yield above. **Whether that
figure is the provenance of any specific number in `src/arty/` is a
criterion-match question, unsettled here and not answered by this file.**

FINDING\[note\]: aisi-1045.md interleaves extractor commentary with processed source text under a "## Remarks" heading and marks neither — its two sentences are a meta-statement about the reference and a cross-reference to this repo's own fragmentation catalog, neither of which the AZoM page can have contained, and a card built on it attributed both to the source (affects: doc-reference/azom-steel-grades/aisi-1045/aisi-1045.md, doc-reference/azom-steel-grades/aisi-1045/card.md; since: 2026-08-03)

## Provenance of this card

- The document is a live AZoM web reference page (ArticleID=6130), not a
    paper or scanned report. No PDF is retained — there is nothing to archive
    as `source.pdf`; the only re-acquisition path is re-fetching the live URL.
- Citable surface for numbers: `aisi-1045.md` (the processed page text, 1.5K),
    anchors above point into it. This `card.md` is a navigation index only —
    do not cite it in place of `aisi-1045.md`.
- No `tables/*.csv` extraction exists for this document (out of scope for
    this pass; the composition/mechanical tables are short enough to read
    directly from `aisi-1045.md` and are not cited downstream today).
