# Card: Centrifugal Casting Adaptability to High Explosive Steel Shells (Paine, 1929)

**Document:** "Centrifugal Casting: Adaptability to High Explosive Steel Shells"\
**Author:** Roy E. Paine\
**Date:** September-October 1929, Army Ordnance, Vol. 10, No. 56, pp. 117–124\
**Published by:** National Defense Industrial Association\
**Original:** JSTOR, Stable URL https://www.jstor.org/stable/45481566 (login required)

**Retained scan:** `source.pdf` beside this card — **not committed** (`.gitignore:58`); re-acquire from JSTOR.\
**Page count:** 9 pages\
**SHA256:** `8376756a843b1b9707a58ff6cea9390dae91f2c386cc3d0dbb6745a13977e882`

## Summary

A 1929 technical paper by Roy Paine (Stanford metallurgist, awarded first prize in an Army Ordnance Association essay contest) proposing centrifugal casting as a manufacturing method for high-explosive shell bodies, which were traditionally forged or sand-cast. The paper gives historical context on centrifugal casting processes, mathematical principles of the rotating-mold parabola, and a tabulated set of steel compositions and mechanical properties suitable for shell manufacture (including carbon steels, nickel-chrome steels, and steel castings).

**Key context:** During WW1, US shells were cast from "semi-steel." By 1929, rising HE explosive power made wall strength critical, necessitating stronger materials than cast-iron. The paper argues centrifugal casting can meet mechanical, metallurgical, and economic requirements for shells. The tabulated steel grades include both wrought steels (W.D. grades, likely "War Department") and cast variants.

## Table 1 — Steel Grades and Mechanical Properties

**Source reference:** Anchor: `TABLE I. Properties ofSteels Suitable forShell Manufacture.` (paine-1929.md, line 985)

**Data file:** `tables/table-1-shell-steel-properties.csv`

The table lists 28 steel designations with their chemical composition (C, Mn, P, S, Si, Ni, Cr, Cu in percent by weight) and physical properties (Ultimate Strength, Elastic Limit, Yield Point, Elongation, Reduction of Area, in lbs/in² and percent). Each row carries footnote letter references (e.g., "(a, d)") linking to Army specifications and published metallurgy texts.

**Columns:**

- Designation and Form (e.g., "W.D. 1045, Carbon Steel (a, d)")
- C, Mn, P, S, Si, Ni, Cr, Cu (% by weight; many cells empty when alloy element not used)
- Ultimate Strength (lbs/in²)
- Elastic Limit (lbs/in²)
- Yield Point (lbs/in²)
- Elongation (%)
- Reduction of Area (%)

**Noteworthy entries:**

- **W.D. 1045, 1050, 1055, 1065** — four carbon steel grades, 0.40–0.70 % C, Mn 0.40–0.80 %, Ultimate Strength 70,000–80,000 lbs/in² (except 1065: 80,000 lbs/in² solid)
- **Common Steel Shell, under 8 in. / 8 in. and larger** — specifications that show two treatment routes (annealed vs. quenched and drawn), with properties ranging 75,000–100,000 lbs/in² ultimate
- **W.D. 3250, Nickel-Chrome Steel** — alloyed with 1.50–2.00 % Ni and 0.90–1.25 % Cr; highest strength tabulated: 170,000 lbs/in² ultimate, 140,000 elastic limit
- **Steel Castings (various)** — multiple sources tabulated; annealed castings around 80,000–115,000 lbs/in², electric-melted castings higher (~102,000–104,000 lbs/in²)

**Footnote references code the source standards:**

- (a) U.S. Army Specifications No. 57-107A, July 1927, "Steel Bars, Carbon and Alloy"
- (c) U.S. Army Ordnance Department Metal Specifications No. 57-104-1, Apr 21, 1924, "Cast Steel Ingots and Steel, Rolled or Forged, for U.S. Common Steel Shell and Shrapnel"
- (d) Ordnance Department Document No. 2050, Nov 18, 1924, "Notes on the Selection and use of Metals in Ordnance Design"
- (m) S. L. Hoyt, *Metallography—The Metals and Common Alloys* (1921)
- (n), (o), (e), (h), (k), (f), (g), (p) — refer to other published metallurgy and materials texts

**Strength term definitions (as source uses them, not reinterpreted):**

- **Ultimate Strength** — stress at rupture, lbs/in²
- **Elastic Limit** — stress at which permanent deformation begins (offset measure), lbs/in²
- **Yield Point** — stress at onset of plastic flow, lbs/in²
- **Elongation** — percent increase in gage length at rupture
- **Reduction of Area** — percent decrease in cross-section at rupture

## Mechanical Property Context — from Source Text

Anchor: `It has been shown that an increase of from 25 per cent to 100 per cent can be obtained in the physical properties of metals cast centrifugally over the same metals cast in sand.` (paine-1929.md, near line 822)

The source states that centrifugal casting yields 25–100 % improvement in physical properties vs. sand-casting of the same composition. The paper illustrates this with a worked example (Paine's own experimental data):

**Sand-cast vs. centrifugal-cast comparison (Paine's test specimen):**

- Tensile Strength: 24,000 lbs/in² (sand) → 39,200–40,000 lbs/in² (centrifugal) = 63.4–67.6 % increase
- Elongation: 9 % (sand) → 14–15 % (centrifugal) = 55.5–67.7 % increase
- Ultimate Strength: 112,500 lbs/in² (centrifugal), Elastic Limit: 56,250 lbs/in²

This context explains why Table 1 exists: the paper is arguing that centrifugal casting can meet the tabulated shell-steel specifications more consistently than traditional methods.

## Full Markdown

Extracted text in `paine-1929.md` (note: heavy line duplication due to two-column scan layout; deduplication would reduce to ~364 unique lines of 9 pages).

**Grep gotcha:** stray non-breaking-space bytes in the repeated JSTOR footer
("This content downloaded from...") make `file` classify `paine-1929.md` as
binary `data`, which makes plain `grep` silently return zero hits on searches
that should match (including both anchors above) — not evidence the text is
absent. Use `grep -a` against this file.

## Not Extracted

- **Mathematical derivation of centrifugal parabola** (paine-1929.md, lines ~300–450) — equations for the free surface of molten metal in rotating molds; relevant to physics of the process but not to steel selection
- **Figure 1: The Centrifugal Parabola** — diagram showing parabolic surface in rotating mold
- **Figure 2: General Outline of Methods for Producing Shell Bodies** — flowchart comparing ingot casting, casting+forging, and other routes for shell blank production (two diagrams included in output/images but not separately transcribed)
- **Historical sections on centrifugal casting development** (Eckhardt 1809, Lovegrove 1848, Bessemer 1859, Shanks, Whitley, Lewicki, etc.) — developmental history, not material property data

## Provenance and Reliability

This paper is a historical technical essay published in a peer-reviewed professional journal (*Army Ordnance*) and won a prize; the author was affiliated with Stanford University. The tabulated steels cite contemporary (1920s) U.S. Army Ordnance specifications and published metallurgical texts as their sources — i.e., Table 1 compiles data from standard specs and handbooks, not raw experimental data.

**Extraction correction (2026-08-09):** the original extraction pass dropped
the "Yield Point" cell on 14 of 28 rows instead of preserving it as blank,
left-shifting Elongation into the Yield Point column and Reduction of Area
into Elongation, and losing Reduction of Area off the end. Confirmed against
`source.pdf` p.121 (Table I) row by row and corrected in the CSV. The
extraction pass's own first-draft `.invariant` (checking only
Ultimate Strength >= Elastic Limit) did not catch this — those two columns
were never the ones that shifted — and was additionally unparseable by
`check-table-invariants.py` (wrong directive names), so it never actually ran.
Replaced with `checks/verify-table-1-closures.py`, which closes row shape (the
check that would have caught the shift) plus the ordering and percent-bound
relations; see that script's docstring for why a standalone script was used
instead of the shared `.invariant` DSL. Run:
`uv run python doc-reference/ww2-shells/paine-1929-centrifugal-casting/checks/verify-table-1-closures.py`

**Important caveat — applicability to WW2 modeling:** This paper is from *1929*, before U.S. entry into World War II (1941) and before the main weapons-production ramp (1942–1945). It proposes centrifugal casting as a future method; there is no explicit statement that centrifugally-cast shell bodies were actually used operationally in WW2 or in which calibers. The steels tabulated may or may not match the steels that were eventually chosen for mass-production WW2 shells. A later source (e.g., 1942–1945 technical manual, production records, or metallurgical survey) would be needed to confirm whether this proposal was adopted.

**Whether this source bears on the model:** The table supplies a reference set of ordnance steels from the U.S. circa 1929, including yield/ultimate strength ranges. Whether any of these grades match the steel(s) in the model's WW2 HE shell is a criterion-match question for @model-reviewer.

## Source

**DOI:** Not assigned; JSTOR Stable ID https://www.jstor.org/stable/45481566\
**Pages:** 117–124 in Army Ordnance, Vol. 10, No. 56\
**PDF file:** source.pdf (1.7 MB, 9 pages, native text layer, OpenPDF 1.3.43 producer)
