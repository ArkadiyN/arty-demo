# TM 9-1901 Artillery Ammunition — Fuze Weights

## Source

- **Document:** TM 9-1901, Artillery Ammunition (US Army)
- **URL/DOI:** US Army Technical Manual 9-1901
- **PDF pages processed:** 249–250 (M48), 252–256 (M51A3), 257–261 (M54), 262–264 (M55A2)
- **Printed pages:** 246–248, 249–251, 255–257, 259–261
- **Page count:** 391 pages
- **SHA256:** fe509d3bb43038ee8b4507ca5046646af56aaa2566ee7bbf6947ae8f02893e3b
- **Source blob:** `source.pdf` — **not present on disk**; reacquirable via `/mnt/f/Projects/TMP/Docs/TM-9-1901.pdf` (corrected 2026-08-16; see Provenance section — the retained-on-disk claim above was wrong, only the four page-range extraction `.md` files exist)

## Fuze Data

### M48, M48A1, M48A2 — Superquick/Delay Fuze

**Weight:** 1.41 pounds (fuze only)

**Source anchor:** Section 319.b, "Data" (`grep "weight, 1.41 pounds"` in `TM-9-1901-p249to250.md`)

- **Printed page:** 246 (TM section 319)
- **Description:** "Length, visible, 3.74 inches, over-all, 4.55 inches; weight, 1.41 pounds; thread size, 1.7-14NS-1."
- **Booster:** Adapted for use with M20 Booster (made a manufacturing component of the shell).

### M51A3 with Booster M21A2 — Superquick/Time Fuze

**Weight:** 2.15 pounds (including booster)

**Source anchor:** Section 320.b, "Data" (`grep "weight, 2.15 pounds"` in `TM-9-1901-p252to256.md`)

- **Printed page:** 249 (TM section 320)
- **Description:** "Length, visible, 3.74 inches, over-all, 5.93 inches (including booster); weight, 2.15 pounds (including booster); thread size, of fuze, 1.7-14NS-1, of booster, 2-12NS-1."
- **Note:** M51A3 replaces earlier M51 (0.05 s delay) and M51A1 (0.15 s delay). M51A3 has 0.15 s delay and secured firing pin in delay assembly.

### M54 — Selective Superquick/Time Fuze (to 25 sec)

**Weight:** 1.42 pounds (fuze only)

**Source anchor:** Section 324.b, "Data" (`grep "weight, 1.42 pounds"` in `TM-9-1901-p257to261.md`)

- **Printed page:** 255 (TM section 324)
- **Description:** "Length, visible, 3.76 inches, over-all, 4.57 inches; weight, 1.42 pounds; thread size, 1.7-14NS-1."
- **Booster:** Usually used in conjunction with M20 type booster (made a manufacturing component of the shell).
- **Note:** "Same size, shape, and weight as the M48" except M54 adds time-action capability (to 25 sec).

### M55A2 with Booster M21A2 — Identical to M54 with M21A2 Booster

**Weight:** 2.16 pounds (including booster)

**Source anchor:** Section 325.b, "Data" (`grep "weight 2.16 pounds"` in `TM-9-1901-p249to251_262to264.md`)

- **Printed pages:** 259–260 (TM section 325)
- **Description:** "Length, visible, 3.76 inches, over-all, 5.95 inches (including booster); weight 2.16 pounds (including booster); thread size, of fuze, 1.7-14NS-1, of booster, 2-12NS-1."
- **Note:** Section 325 states: "The M55A2, M55A1, and M55 Fuzes are identical in every respect with M54 Fuze (par. 324) except that BOOSTER M21A2, M21A1, M21, respectively, is a manufacturing component of the fuze."

## Data Table

See `tables/fuze-weights.csv` for the tabulated series. Columns: Fuze Model, Configuration, Weight (lb), Booster Model.

## Fuze-to-Shell Compatibility

**Not in TM 9-1901.** This manual describes fuzes and their specifications but does not state which fuze (M48, M54, M51A3, M55A2, etc.) is fitted to which shell projectile (105mm M1 HE, 155mm M107 HE, etc.). Shell-to-fuze assignments are stated in TM-9-1904 (to be supplied separately).

## Closure Invariant

Weight data in `fuze-weights.csv` is a tabulation of product specifications as stated. All weights are expressed in pounds (US customary). Entries with "including booster" are total weight; entries without are fuze only.

M51A3 and M55A2 both add the same booster, M21A2, to a bare P.D./TSQ fuze
(M51A3 = M48A2 + M21A2 per §320.a; M55A2 = M54 + M21A2 per §325.a). If the
document's stated weights are self-consistent, the implied booster increment
must therefore agree between the two pairs:

- M51A3 (2.15 lb) − M48A2 (1.41 lb) = **0.74 lb**
- M55A2 (2.16 lb) − M54 (1.42 lb) = **0.74 lb**

Both pairs close on the same 0.74 lb M21A2 booster increment. This is the
closure invariant for this table.

## Provenance of this card

- **Document:** US Army Technical Manual 9-1901, *Artillery Ammunition* (verified anchor "weight, 1.41 pounds" — `TM-9-1901-p249to250.md:22`, report section 319.b).
- **`source.pdf`:** Not retained on disk (gitignored; reacquirable via `/mnt/f/Projects/TMP/Docs/TM-9-1901.pdf` per card Source section).
- **Page count & SHA256:** 391 pages; `sha256: fe509d3bb43038ee8b4507ca5046646af56aaa2566ee7bbf6947ae8f02893e3b` (recorded in Source section).
- Extraction was partial and page-range segmented (four `.md` files covering sections 319–325). Extraction method (OCR vs. vision) not stated in available metadata.
- All weights in this card are extracted from TM 9-1901's own product specifications (sections 319–325); no secondhand claims or secondary references cited within the fuze data proper.

FINDING\[deferrable\]: source.pdf not retained in doc-reference/ww2-shells/tm-9-1901-artillery-ammunition/ — only page-range extraction .md files kept; a local reacquisition path is recorded but the blob itself is not retained per source-data-fidelity.md's "Keep source.pdf" (affects: doc-reference/ww2-shells/tm-9-1901-artillery-ammunition; since: 2026-08-16)
