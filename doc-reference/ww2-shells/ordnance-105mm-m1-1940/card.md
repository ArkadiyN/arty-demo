# US 105mm M1 HE Shell — Description of Manufacture (1940)

**Document:** "Description of Manufacture, Shell, H.E. 105 mm., M1, From Forging"\
**Author:** Office of the Chief of Ordnance, U.S. Army\
**Date:** August 30, 1940 — 183 pages\
**Original:** https://www.bulletpicker.com/pdf/Shell-HE-105mm-M1.pdf\
**Retained scan:** `source.pdf` beside this card — **not committed**
(`.gitignore:58`); re-acquire from the URL above.\
**Classification:** Unclassified (historical)

## Tables — read these, not the prose

| File                          | What it holds                                                   | Closure                                                                  |
| ----------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `tables/bill-of-material.csv` | the 8-row BILL OF MATERIAL, `source.pdf` p.16 (document page 7) | per-shell × 100,000 = per-100,000-shell, on all three rows carrying both |

Transcription verified cell-by-cell against the page's text layer by
[`ordnance-105mm-bom-page-fidelity.py`](../../../experiment/fragmentation-field/challenges/source-data-audit/checks/ordnance-105mm-bom-page-fidelity.py).
Run the closure with:

```
uv run src/utils/check-table-invariants.py doc-reference/ww2-shells/ordnance-105mm-m1-1940/tables/bill-of-material.invariant
```

## The one fact this document supplies to the model

Anchor: `Steel WD-X1335` — the **Body, Shell** row of the BILL OF MATERIAL.

| Column                               | Value              |
| ------------------------------------ | ------------------ |
| Material                             | Steel **WD-X1335** |
| Spec.                                | **57-107**         |
| Commercial form                      | Forging            |
| Average amount of material per shell | 53.9 lbs (24.4 kg) |

`src/arty/fragmentation.py` quotes the material/spec pair as the identity of
the `"WW2 US HE Shell"` steel entry. That grade **name** is the entire
contribution of this document to the model — the composition read behind it,
and every mechanical property, come from elsewhere. See
`experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md`.

**Composition, yield, tensile, hardness and heat treatment are NOT in this
document.** It defers all of them to specification **57-107**, which is not
reproduced in the drawing set and is not digitized in open sources. Anything
quoting this card for a mechanical property is quoting something that was
never here.

Corroboration on a second page: the LIST OF PARTS table (`source.pdf` p.9)
independently pairs the shell body with the same grade and spec. The OCR on
that page is poor (`AO-X/335` / `37-/07`); it is a cross-check, not a
transcription source.

## What else is in the document, not extracted

- **Dimensioned shell drawings** (`source.pdf` pp.7–8, anchors
    `MEAN VOLUME OF CAVITY` and `TOLERANCE ON CAPACITY`) — the full finished-shell
    dimension set, plus a stated mean cavity volume to overflowing of 91 cu. in.
    and the concentricity tolerances. Deliberately **not extracted**: no current
    model needs shell geometry from this source, and the text layer on these
    blueprint pages is heavily corrupted, so extraction is a vision job with a
    real cost. Recorded here so a future pass knows the geometry exists rather
    than re-searching for it.
- **LIST OF OPERATIONS** (pp.10–15) and ~150 pages of tooling, gage and
    fixture drawings — manufacturing process, no model relevance.
- **Government / contractor inspection procedure** (pp.17, 19).

## Provenance of this card

Re-baselined 2026-08-02 against `source.pdf` p.16 under
`.claude/rules/source-data-fidelity.md`. The prior version of this card was
written without the page and carried four transcription errors (`5,290,000`
for `5,390,000` and mislabelled as a per-contract total rather than the
per-100,000-shell column; `Gliding` for `Gilding` Metal; band O.D. `4.58"` for
`4.56"`; specs `3-87`/`35-2` for `3-67`/`36-2`), none of which any model
consumed. It also carried an "Inferred typical range" of mechanical properties
(250–350 MPa yield, 400–500 HB) attributed to no source and mutually
inconsistent — **removed**, per the finding that this document supplies no
mechanical data at all. Detail:
`experiment/fragmentation-field/challenges/source-data-audit/ledger.md` §15.
