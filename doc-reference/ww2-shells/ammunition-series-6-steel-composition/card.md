# Card: X-1340 Steel and WW2 Artillery Shell Grade Evolution

**Source:** Ammunition Series 6, §6-11 "Steel Used Early in World War II"
**Covers:** composition, hardening strategy, and process tradeoffs for WW2
forged HE shell bodies (X-1340 grade).

______________________________________________________________________

## X-1340 Steel Composition (anchor: "X-1340 Steel Specification (Original Composition)")

| Element | Range            |
| ------- | ---------------- |
| **C**   | 0.35–0.45%       |
| **Mn**  | 1.35–1.65%       |
| **P**   | ≤0.45% (maximum) |
| **S**   | 0.075–0.15%      |

Row anchor: `\| **Phosphorus** \| ≤0.45% (maximum) \|`. All four values are
verified against the printed page (PDF page 11 = printed page 6-4), which gives
them as prose, not a table — see "P ≤0.45% row" below for why the phosphorus
figure is nonetheless worth flagging to a consumer.

Design goal (anchor: "High manganese content was originally intended to secure the required physical properties"):
high Mn as substitutional hardener to reach 50,000 psi (≈345 MPa) yield
(anchor: "Yield strength target: **50,000 psi (≈345 MPa)** achievable with rapid, uniform cooling")
without heat treatment, via rapid uniform air-blast cooling from forging
temperature.

______________________________________________________________________

## Manganese Hardening Relationship (anchor: "Effect per 0.01% Mn: **100–500 psi tensile strength increase**")

Verbatim on the page (PDF page 11 = printed page 6-4, §6-11): "The amount by
which 0.01 percent manganese increases the tensile strength varies with the
carbon content from 100 to 500 psi. The increase in the yield strength is
somewhat more than this, 50,000 psi, accompanied by good ductility, being
easily attained with manganese in excess of 1.0 percent, provided the cooling
is rapid and uniform."

**That sentence is not in `ammunition-series-6-steel-composition.md`** — the
extraction renders it only as the summary bullet the anchor above points at,
with an en-dash ("100–500"), so grepping the quoted wording against the
extraction returns zero. It is a gap in the derived surface, not in the source.
Cite the quote to the PDF, and the bullet to the extraction; do not use the
extraction to establish that the source did not say something.

______________________________________________________________________

## Cooling-Rate Limit (Caliber Dependency)

- ≤105mm: air-blast cooling sufficient (anchor: "While the physical requirements were met in the smaller shells").
- 155mm: air-blast cooling insufficient — "difficulty was experienced with
    the 155-mm on account of the higher ratio of volume to heat-robbing
    surface" (anchor: "difficulty was experienced with the 155-mm on account of the higher ratio of volume to heat-robbing surface").

______________________________________________________________________

## Strategic Transition: Lower-Mn + Heat Treatment

Ordnance Department adopted lower-Mn steel with heat treatment instead of
air-cooling (anchor: "the decision of the Ordnance Department to adopt a steel with lower manganese content"):
saved manganese (anchor: "This action also saved considerable quantities of manganese"),
simplified forge work (anchor: "Simplified the work of the forge by eliminating air-blast cooling"),
but increased machine-shop work (anchor: "However, the work in the machine shop was increased.").
Successor grade's own Mn content and heat-treatment type are not given in
the source (marked "(not specified)" / "(unspecified)" in the extraction).

______________________________________________________________________

## Open Question: X-1340 ↔ WD-X1335 Relationship (anchor: "The source document does not explicitly name the successor steel grade.")

Baseline catalog (105mm M1 HE shell, 1940 Ordnance BOM) specifies steel
**WD-X1335**, spec 57-107 (anchor: "specifies steel grade **WD-X1335**").
The extraction states plainly it cannot confirm whether WD-X1335 is the
successor to X-1340 — see its own "## Open Question..." section (anchor:
"Data Gap") and "## Confidence Assessment" table (anchor: "Successor Grade Identity").
Composition/mechanical properties of WD-X1335 are not
publicly digitized (anchor: "not publicly digitized (spec 57-107 remains archived)").
Whether WD-X1335 is usable as a stand-in for X-1340 in any model is a
criterion-match question for whoever needs that grade, not settled here.

______________________________________________________________________

## Extraction's own confidence ratings (anchor: "## Confidence Assessment")

Per the extraction's own table: X-1340 composition — High; Mn effect — High;
155mm cooling limitation — Medium-High; successor grade identity — Low;
**phosphorus spec (≤0.45%) — Low, "value unusually high; possible
transcription error"**.

______________________________________________________________________

## P ≤0.45% row — resolved at the page

**The printed page says 0.45 percent.** §6-11 gives the composition as a run of
prose, not a table: "carbon, 0.35 to 0.45 percent; manganese, 1.35 to 1.65
percent; phosphorus, 0.45 percent maximum; sulfur, 0.075 to 0.15 percent" (PDF
page 11 = printed page 6-4, in the retained blob named under Provenance below).
The extraction is faithful and so is this card's table.

What the extraction's own caveat (anchor: "OCR/transcription error (should be 0.045%?)")
and its Low-confidence rating actually recorded was **doubt about the printed
value**, not a suspected transcription slip — and that doubt is reasonable:
0.45% phosphorus is roughly ten times the level normal for shell steel, and the
same passage calls the manganese and sulfur figures "relatively high
percentages" without remarking on the phosphorus. Whether the page itself
carries a typo is not something this card can settle, and it is not a fidelity
question — every surface between the page and here agrees.

**Do not "correct" the figure to 0.045% anywhere.** A consumer that needs a
phosphorus limit for this grade should treat the source's own number as
suspect on metallurgical grounds and say so, not silently substitute a
plausible one.

______________________________________________________________________

## Provenance of this card

- **The source blob is retained — under the sibling directory, not this one.**
    `../ammunition-series-6-wdss-specs/source.pdf` is the same book: 59 pages,
    `sha256: 84a1d8af5d2d336df4deee10d0e587622355c8f09ae9fecbd846dc46c074b089`,
    gitignored (`doc-reference/**/*.pdf`). §6-11 "Steel Used Early in World War
    II" — everything this card covers — is on **PDF page 11 = printed page
    6-4**, alongside §6-12 (sulfur objections), §6-13 (the post-WWII
    replacement composition) and §6-14 (which points at table 6-1 and names
    MIL-S-10520C). The page has a working text layer; `X-1340` returns 2 hits
    and `heat-robbing` 1.
- `ammunition-series-6-steel-composition.md` labels itself
    (anchor: "**Source Type:** Primary military technical reference (transcribed excerpt)")
    and closes with (anchor: "**Source Provenance:**"): "User-supplied
    transcription from original military document (image reference:
    /mnt/f/Projects/TMP/AgenticCoding/X-1340.png for citation purposes only)".
    That image path is on a machine outside this repo and is not retained here
    — but it is **not** the only path back to the page, and treating it as such
    is what left this document recorded as un-re-baselineable. Go to the PDF
    above.
- The file is not a clean OCR/API extraction: it interleaves quoted sentences
    (many marked with quotation marks and matched by anchors above) with
    synthesized commentary the transcriber added (its "Material Science
    Summary", "Recommendations for Further Investigation", and "Confidence
    Assessment" sections are analysis, not source text).
- **Citable for numbers:** only the quoted sentences and the composition
    table, and only with the caveat above for the P value. **Not citable as
    a primary:** any section of `ammunition-series-6-steel-composition.md`
    that is the transcriber's own synthesis (Material Science Summary,
    Recommendations, and the interpretive columns of the Open Question /
    Cooling-Rate tables) — these read as analysis of the primary, not the
    primary itself.
- No `tables/*.csv` extraction exists for this document (out of scope for the
    migration pass; not cited downstream today). §6-11 states its composition
    as prose rather than a table, so the natural CSV here is the four-element
    composition row plus §6-13's replacement composition — a small extraction,
    and now an unblocked one.

**Closed 2026-08-10.** The Provenance section above now states the sibling
`source.pdf` location, page, and sha256 directly and says explicitly that the
`/mnt/f/...` image path "is **not** the only path back to the page" — so this
card no longer reads as un-re-baselineable to anyone who reaches it.
