# TM 9-1904: Fuze Fitting for 105-mm and 155-mm Howitzer Shells

## Source

- **Title:** TM 9-1904, Artillery Ammunition (U.S. Army Technical Manual)
- **Content:** U.S. Army ordnance manual on artillery ammunition design, construction, and ammunition components
- **Pages:** 952 (scanned with ABBYY FineReader, dated 2019-06-09)
- **SHA256:** `ea35cd3bfdfe0fc795b86136272dc3e4040ffdba85d6df82651fc987f19c4790`
- **Acquisition:** Local archive at `/mnt/f/Projects/TMP/Docs/TM-9-1904.pdf`

## 105-mm Howitzer Shell M1 (Semifixed, H.E.)

**Authorized Fuzes:**

- M48 Fuze (with M20 or M20A1 Booster)
- M54 Fuze (with M20 or M20A1 Booster)

**Source anchor:** Heading "SHELL, Semifixed, H.E., M1." (source.pdf p.481, printed p.473); Components line: "A complete round of M1 H.E. Ammunition consists of a loaded and fuzed (M48 or M54 Fuze) projectile" (grep: `"M48 or M54 Fuze"`).

**Booster specification:** "The M20 (or M20A1) Booster is used in the H.E. rounds with the M48 or M54 Fuzes" (source.pdf p.481, printed p.473, line preceding shell heading).

______________________________________________________________________

## 155-mm Howitzer Shell M107 (H.E., M1 Howitzer)

**Authorized Fuzes:**

- P.D. M51 Fuze with M21 Booster
- P.D. M51A1 Fuze with M21A1 Booster

**Source anchor:** Heading "SHELL, H.E., M107." (source.pdf p.529, printed p.521); Projectile line: "The projectile with P.D. M51 Fuze with M21 Booster, M51A1 Fuze with M21A1 Booster." (grep: `"P.D. M51 Fuze with M21 Booster, M51A1 Fuze with M21A1 Booster"`).

**Note:** Both fuze–booster combinations are listed as authorized; the source distinguishes the baseline M51/M21 configuration from the later M51A1/M21A1 variant.

______________________________________________________________________

## 75-mm Gun Shell M48 (H.E.)

**Authorized Fuzes:**

- M48 Fuze
- M48A1 Fuze
- M54 Fuze

**Authorized Boosters:**

- M20 Booster
- M20A1 Booster

**Source anchor:** Heading "SHELL, H.E., M48." (source.pdf p.414, printed
p.410 per user page correlation); components line: "Fuzes M48, M48A1 and
M54. Boosters M20 and M20A1." (grep: `"Fuzes M48, M48A1 and M54"`).

**Other stated data (same paragraph, source.pdf p.414):**

- Bursting charge: "1.49 pounds of TNT" — "sufficient to break the shell into
    approximately 400 effective fragments."
- Mean weight of loaded and fuzed projectile: "14.6 pounds."
- Weight zones (yellow-cross stencil below the bourrelet, fig. 165): Light
    14.22–14.52 lb, Normal 14.52–14.82 lb (row garbled in OCR — see raw text),
    Heavy 14.82–15.12 lb.
- Geometry: "streamlined type with a 9-degree tapered or boat-tailed base and
    a 7.5-caliber radius of ogive." Forged steel body, gilding-metal rotating
    band, steel base cover spot-welded to the base.
- Complete-round designation: "Shell M48"; weapon designation "75G."
- Also associated: Cartridge Cases M18/M18B1; Propelling Charges reduced/
    normal/super; Primers M22A3 (or M22-series) and M31.
- Figure 165 caption (source.pdf p.415): "SHELL, H.E., M48, for 75-mm Guns."

**Note:** the fuze family for the fielded/production Shell M48 (M48, M48A1,
M54) is the **same family already sourced in TM-9-1901**
(`doc-reference/ww2-shells/tm-9-1901-artillery-ammunition/card.md`: M48/
M48A1/M48A2 = 1.41 lb fuze only, M54 = 1.42 lb fuze only) — distinct from the
M39 P.D. fuze recorded on the 1938 T3 test article in Tolch 1938. The M20/
M20A1 booster weight is not tabulated in TM-9-1901, same gap already
recorded for the 105mm M1 shell above.

**Filler mass:** the prose above states "1.49 pounds of TNT" as the standard
bursting charge, but TM-9-1904's own appendix table gives 1.47 lb — matching
the official M48 filler mass and the shipped `src/arty/shells.py` value. The
discrepancy is internal to this source (prose vs. appendix table), not
between this source and the shipped model; 0.02 lb is immaterial for this
project's purpose either way. Not chased further.

______________________________________________________________________

## Remarks

The source lists all authorized fuze configurations for each shell without ranking or preference. Whether the M51 or M51A1 series is appropriate for a given application is a criterion-match question for the modeller and beyond the scope of this manual's stated purpose.

## Provenance of this card

- **Document:** US Army Technical Manual 9-1904, *Artillery Ammunition* (verified anchor "M48 or M54 Fuze" — `fuze-fitting-extraction.md:23`).
- **`source.pdf`:** Not retained on disk (gitignored; source listed as `/mnt/f/Projects/TMP/Docs/TM-9-1904.pdf` in card Source section).
- **Page count & SHA256:** 952 pages; `sha256: ea35cd3bfdfe0fc795b86136272dc3e4040ffdba85d6df82651fc987f19c4790` (recorded in Source section). Scanned and OCR'd with ABBYY FineReader, dated 2019-06-09 (per card Source section).
- **Note on page numbering:** Card cites "source.pdf p.NNN, printed p.NNN" anchors (e.g., p.481/473, p.529/521, p.414/410) — these reflect the OCR'd PDF's internal pagination vs. printed report numbering. Without the retained source.pdf, only the greppable text anchors in `fuze-fitting-extraction.md` are verifiable; PDF page references are retained for re-acquisition if needed.
- All fuze-to-shell assignments listed are tabulated directly from TM 9-1904's own sections; no secondhand claims.

FINDING\[deferrable\]: source.pdf not retained in doc-reference/ww2-shells/tm-9-1904-fuze-fitting/ — only fuze-fitting-extraction.md kept; a local reacquisition path is recorded but the blob itself is not retained per source-data-fidelity.md's "Keep source.pdf" (affects: doc-reference/ww2-shells/tm-9-1904-fuze-fitting; since: 2026-08-16)
