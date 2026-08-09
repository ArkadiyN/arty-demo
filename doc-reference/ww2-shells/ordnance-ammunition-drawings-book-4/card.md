# Ordnance Ammunition Drawings, Book 4 — Engineering Drawings

**Source:** U.S. Ordnance Dept., Ordnance Ammunition Drawings, Book 4 (WW2-era
engineering specification and metal-parts/explosives-loading drawings).
79-page PDF; 9 pages extracted (5, 6, 9, 14, 23, 25, 53, 71, 73).

**Pages:** 5 (105mm M60 chemical shell, metal parts assembly, drawing
75-4-91A), 6 (M60 List of Parts / List of Specifications table), 9 (155mm
M107 HE shell, metal parts assembly, drawing 75-4-99A), 14 (105mm M67 HEAT
shell, List of Parts / List of Specifications, drawing 75-4-106A), 23 (75mm
M48 HE shell, explosives loading), 25 (105mm M1 HE shell, explosives
loading), 53 (155mm M107 HE shell, explosives loading), 71 (Forging for
Shell H.E., 81mm, M43A1 and Shell, Practice, M43A1, drawing 75-20-72 —
List of Specifications + Physical Properties block), 73 (Forging for Shell
H.E., 75mm, M48/M48B1 and Shell, Chemical, M64, drawing 75-20-77 — List of
Specifications + Physical Properties block).

## Extraction provenance — read this before citing anything below

**This card was rewritten from scratch (2026-08-09) after the automated
extraction pass proved unreliable on every one of the 7 pages.**
`generate_markdown(..., analyze_formulas=True)` used this project's default
vision provider (`vision_provider = "google"`, model `gemma-4-31b-it` — see
`src/utils/settings.py`), which is the *free* tier, not Claude vision;
cost was never the concern. On this document Gemma produced wrong drawing
numbers, swapped/mislabeled rows, wrong digits throughout, and on page 53 an
entirely fabricated table structure (an invented "155–163 lb, mark A–H"
weight-zone scheme with no resemblance to the source). The prompt itself
(`_DOC_VISION_PROMPT` in `pdf-processor.py`) already carries explicit
anti-fabrication rules (blank cell → `-`, unreadable cell → `?`, "never
substitute a plausible number") added after an earlier incident, and the raw
output does use those markers 243+3 times across the 7 pages — so this was
not the model ignoring the instruction wholesale. It confidently produced
*wrong* values in cells it evidently felt sure about, rather than marking
them uncertain. That raw transcript is retained, unmodified, at
`../Ordnance Ammunition Drawings, Book 4-p5_6_9_14_23_25_53.md` **for
reference only — do not cite any number from it.** Every table below was
independently re-transcribed by direct human/model reads of page rasters
(`--screenshot-pages`, local, no vision API) against the same source pages,
and is committed because it closes arithmetically (see Verification below) —
not because it was extracted by any particular tool.

**Images `fig1.jpeg`–`fig5.jpeg`** (the librarian's auto-detected figures) are
confirmed via `md5sum` byte-identical to full-page rasters of pages 5, 9, 23,
25, 53 respectively — these were not affected by the table-transcription
failure and are trustworthy as-is. Pages 6 and 14 (pure List-of-Parts/List-
of-Specifications tables, no illustration) were never auto-captured; added
manually as `fig6-page6-m60-specs.jpeg` and `fig7-page14-m67-heat-specs.jpeg`.

**Page 71** (`fig8-page71-81mm-mortar-specs.jpeg`) was added later
(2026-08-09), never went through the automated `--analyze-formulas` pass at
all, and is not part of the extraction-failure narrative above — it was
rendered directly from `source.pdf` at 300 dpi (`pdftoppm`) and read straight
off the raster in response to a specific user claim, cross-checked at 2x zoom
crops of the specification table and the physical-properties block before
transcription. First-pass transcription, no automated draft to distrust.

**Page 73** (`fig9-page73-75mm-m48-specs.jpeg`) was added the same way,
immediately after page 71, in response to a direct user correction of this
card's own prior claim that the 75mm M48 was not covered by any primary
source in this repo — it is, on the next populated page of the same book.
Same method: rendered from `source.pdf` at 300 dpi, read full-page first,
then cross-checked at 2x zoom crops of the List of Specifications table and
the Physical Properties block before transcription. Also first-pass, no
automated draft to distrust.

## Headline finding — WD.SS-3 steel, spec 57-104-2, 65,000 psi minimum yield

The user's premise for pulling this volume: "minimum 65,000 psi yield
strength for 105mm/155mm shell bodies is specified, and no steel grade is
named anywhere except the 105mm HEAT shell (page 14), which explicitly names
WD-SS-3." Both parts confirmed directly against the primary drawings:

**Table:** `tables/body-shell-steel-specs.csv`

| Shell                          | Drawing   | Part                | Material/Grade                         | Spec        | Related Spec                                                                          | Min Y.S. (psi)           | Min Elong (%) | Min R.A. (%) | Source                      |
| ------------------------------ | --------- | ------------------- | -------------------------------------- | ----------- | ------------------------------------------------------------------------------------- | ------------------------ | ------------- | ------------ | --------------------------- |
| 105mm M60 (Chemical)           | 75-4-91A  | Body Shell          | STEEL (no grade named on this drawing) | 57-104-2    | —                                                                                     | 65,000                   | 15            | 30           | p.5 (properties)/p.6 (spec) |
| 105mm M60 (Chemical)           | 75-4-91D  | Adapter             | STEEL WDX1314 or WDX1315               | 57-107      | —                                                                                     | — (T.S. 60,000 min)      | 15            | 35           | p.5                         |
| 105mm M67 (HEAT/AT)            | 75-4-106A | Body Shell          | **WD.SS-3**                            | 57-104-2    | 57-104-1 (mandatory for material for forging — note b)                                | not printed on this page | —             | —            | p.14                        |
| 155mm M107 (HE)                | 75-4-99A  | Body Shell          | STEEL (no grade named on this drawing) | 57-104-2    | —                                                                                     | 65,000                   | 15 (in 2 in.) | 30           | p.9                         |
| 81mm M43A1 HE / Practice M43A1 | 75-20-72  | Forging (Type I/II) | STEEL (no grade named on this drawing) | **50-37-1** | 57-104-1 (listed directly on the same List of Specifications table, no footnote link) | **35,000**               | 15            | 30           | p.71                        |
| 75mm M48/M48B1 HE and M64 Chem | 75-20-77  | Forging             | STEEL (no grade named on this drawing) | 57-104-2    | 57-104-1 (listed directly, same List of Specifications table, both titled distinctly) | 65,000                   | 15            | 30           | p.73                        |

- Page 14 (M67 HEAT List of Parts/Specifications, drawing 75-4-106A) is where
    **WD.SS-3** is explicitly printed against the Body Shell line, tied to
    **spec 57-104-2**, with a footnote (b) making spec 57-104-1 mandatory for
    the forging material. This page carries no "MINIMUM PHYSICAL PROPERTIES"
    block — the Y.S./elongation/reduction-of-area figures are not stated here,
    only the grade+spec identity.
- Pages 5 and 9 (M60 and M107 metal-parts-assembly drawings) both print a
    "MINIMUM PHYSICAL PROPERTIES" block against the Body Shell dimension
    callout: min Yield Strength 65,000 psi, min Elongation 15%, min Reduction
    of Area 30%, tied to spec 57-104-2 — but neither drawing names a steel
    *grade* the way page 14 does for the HEAT shell.
- The M60 (page 6) List of Specifications table lists **57-104-1** ("STEEL,
    FORGING; FOR SHELL STOCK") as a specification invoked by drawing 75-4-91,
    without the explicit "(mandatory for forging material)" footnote link that
    page 14 prints for the HEAT shell's Body Shell row. Recorded as printed;
    not assumed identical in relationship to page 14's note (b).
- **WD.SS-3 (this drawing) and WDSS-3** (`../ammunition-series-6-wdss-specs/   card.md`, AMCP 706-249 Table 6-1) are the same designation under two
    different punctuation conventions, ~20 years apart — not a criterion-match
    question.
- **Page 71 corroborates a two-tier spec structure directly from a second,
    independent drawing in this same book — not inferred, printed.** The 81mm
    mortar forging drawing (75-20-72) lists **50-37-1** ("SHELL, STEEL FOR
    SMOOTH-BORE MORTARS, MANUFACTURED FROM FORGINGS") and **57-104-1**
    ("STEEL, FORGING; FOR SHELL STOCK") as the two specs this drawing directly
    requires, with a stated minimum yield strength of **35,000 psi** — roughly
    half of the 65,000 psi minimum the 105mm/155mm Body Shell drawings require
    under spec 57-104-2. **57-104-2 itself is not among the specs this 81mm
    drawing lists as required by the drawing** — its only appearance on page 71
    is one row down, as the "Required By" entry for a *different* spec,
    QQ-M-151 ("METALS, GENERAL SPECIFICATION FOR INSPECTION OF"), meaning
    57-104-2 pulls in QQ-M-151 somewhere in its own text, not that this drawing
    invokes 57-104-2 directly. Structurally, this is exactly the split
    hypothesized from page 14's note (b): **57-104-1 is the shared raw-forging-
    stock spec** (required directly by both the 81mm mortar drawing here and
    the 105mm M60 drawing, page 6), while **57-104-2 is a separate,
    higher-strength finished-part acceptance spec specific to the gun-launched
    (105mm/155mm) Body Shell drawings** and does not govern this mortar
    forging. The 35,000 psi / 65,000 psi split also lines up with
    `../ammunition-series-6-wdss-specs/card.md` §6-14, which states WDSS 1/2
    are the grades used "for the most part for 60-mm and 81-mm mortar shell
    forgings" while a separate, higher 60,000–80,000 psi yield band applies to
    the artillery-caliber grades WDSS 3/5/6/7 — consistent with, though not
    direct proof of, WDSS-1/2 being the grade meeting 57-104-1 + 50-37-1 here
    and WDSS-3 being the grade meeting 57-104-1 + 57-104-2 on page 14. **No
    steel grade name (WDSS or otherwise) is printed anywhere on page 71** — the
    grade-to-spec mapping for the 81mm forging is inference from the
    Ammunition Series 6 card's caliber statement, not a direct read off this
    drawing, and should be read as such.
- **Page 73 (75mm M48/M48B1 HE and M64 Chem forging, drawing 75-20-77)
    corroborates the same 65,000 psi / spec 57-104-2 figure the 105mm and
    155mm Body Shell drawings carry — this corrects an earlier claim in this
    conversation that the 75mm M48 wasn't covered by any primary source in
    this repo.** It is, on the very next populated page of this same book.
    The 75mm M48 forging (drawing 75-20-77) lists both **57-104-1** ("STEEL,
    FORGING FOR SHELL STOCK") and **57-104-2** ("FORGINGS FOR COMMON STEEL
    SHELL AND SHRAPNEL") directly in its List of Specifications table, and its
    Physical Properties block states Yield Strength not less than **65,000
    psi**, Elongation 15%, Reduction of Area 30% — printed as
    "PHYSICAL PROPERTIES OF TEST SPECIMEN (SEE SPEC. 57-104-2) AND FINISHED
    MACHINED SHELL," i.e. the drawing itself ties the 65,000 psi figure to
    57-104-2 by name, not just by table position as on pages 5/9. This is now
    a fourth, independently-drawn caliber (75mm, alongside 105mm M60, 105mm
    M67 HEAT, and 155mm M107) landing on the identical spec/figure pair, and
    the 65,000 psi vs. 35,000 psi split is now evidenced on both sides by a
    drawing that prints both spec numbers with distinct titles side by side,
    not just by table position — strengthening the two-tier reading above
    from "structurally consistent" to "directly titled as two different
    documents on the same page."
- **New, unresolved wrinkle from page 73's title text:** page 73 titles spec
    **57-104-2** as "FORGINGS FOR COMMON STEEL SHELL AND SHRAPNEL." That title
    closely echoes the title Paine 1929 (`../paine-1929-centrifugal-casting/card.md` footnote 17) gives for the *1924-dated* spec **57-104-1** — "Cast
    Steel Ingots and Steel, Rolled or Forged, for U.S. Common Steel Shell and
    Shrapnel." Same subject ("common steel shell and shrapnel"), same rough
    era, but attached to different basic numbers (57-104-1 in 1924 vs.
    57-104-2 on this WW2-era drawing) — raising an open question of whether
    the 57-104-1/57-104-2 numbering was reassigned or renumbered between the
    two eras/documents, rather than being stable across them. Not
    investigated further here — flagged, not resolved; does not change
    anything about the WW2-era two-tier reading above, which rests entirely on
    what this book's own pages print.
- **Still open, but not model-relevant today:** whether spec 57-104-2 as cited
    here is the same document as the 1924-dated spec 57-104-2 in
    `../paine-1929-centrifugal-casting/card.md` footnote 17 — now sharpened by
    the title-echo wrinkle immediately above, which suggests the answer may be
    "no, and the WW2-era 57-104-1 is the closer match to Paine's 1924
    57-104-2" rather than a straightforward same-document identity. Moot for
    now:
    `src/arty/shells.py` sources the 105mm M1/155mm M107/75mm M48 HE shells'
    steel from `STEELS["WW2 US HE Shell"]` (sigma_f=800 MPa, gamma=54.5, a
    Mott-closure fit — not sourced from spec 57-104-2 or any yield-strength
    figure). The only WDSS-grade steel actually wired into the model is
    `STEELS["US WW2 WDSS1"]` (grade **1**, not 3), used solely for the 60mm
    M49A2 mortar shell — a different caliber (60mm, not 81mm) and a different
    Ammunition Series 6 table entry, unrelated to this drawing's Body Shell
    rows. The 35,000 psi figure on page 71 and the 65,000 psi figure on page
    73 (now directly confirmed for 75mm M48, one of the three calibers
    actually drawing on `STEELS["WW2 US HE Shell"]`) are both additional
    evidence for the open deferred finding already recorded on
    `../ammunition-series-6-wdss-specs/card.md` that shipped
    `sigma_f = 800 MPa` (≈116,000 psi) has never been compared against any
    source-stated static yield figure for a WDSS-family grade — neither
    changes that finding's disposition (still a criterion-match question
    for @model-reviewer: static yield vs. dynamic fracture stress are not the
    same quantity) and no new finding is opened here. This card remains
    provenance for the user's claims, not an input the model currently
    consumes.

## 81mm M43A1 HE / Practice M43A1 — Forging Specification (page 71, drawing 75-20-72)

**Title block:** "FORGING FOR SHELL, H.E., 81MM, M43A1 AND SHELL, PRACTICE,
M43A1", Class 75, Division 20, Drawing 72 (i.e. 75-20-72), dated July 6, 1933,
revised through Aug. 15, 1945 (revision 8). Two forging types shown, both
STEEL: "Forging, Shell, Type I" (75-20-72 A8) and "Forging, Shell, Type II"
(75-20-72 B8) — dimensional forging blanks, not the finished machined shell.

**List of Specifications table** (only 4 of 10 numbered lines are populated;
blank lines transcribed as blank, not omitted):

| Line | Specification                                                    | Spec Number | Required By  |
| ---- | ---------------------------------------------------------------- | ----------- | ------------ |
| 1    | AMMUNITION, EXCEPT SMALL ARMS AMM. GENERAL SPEC. FOR             | 50-0-1      | DRG.75-20-72 |
| 4    | SHELL, STEEL FOR SMOOTH-BORE MORTARS, MANUFACTURED FROM FORGINGS | **50-37-1** | DRG.75-20-72 |
| 7    | STEEL, FORGING; FOR SHELL STOCK.                                 | 57-104-1    | DRG.75-20-72 |
| 8    | METALS, GENERAL SPECIFICATION FOR INSPECTION OF                  | QQ-M-151    | 57-104-2     |

**CSV:** `tables/page71-81mm-spec-list.csv`. Row 8's "Required By" column
reads **57-104-2**, not the drawing number — read literally, that means spec
QQ-M-151 is invoked *by* spec 57-104-2, not directly by this drawing. Every
other populated row's "Required By" is the drawing itself (DRG.75-20-72).
Confirmed at 2x zoom crop against `source.pdf`; the table's own footnote
reads: "THE SPECIFICATION NUMBERS SHOWN ARE BASIC NUMBERS ONLY. WHEN A
SPECIFICATION IS REVISED A LETTER IS AFFIXED TO ITS BASIC NUMBER.
SPECIFICATIONS REFERRED TO IN THESE SPECIFICATIONS AND NOT LISTED HEREON
SHALL NOT APPLY."

**Physical Properties block** (printed once, governs both forging types):

- Yield Strength — not less than **35,000 lbs. per sq. in.**
- Elongation in 2 inches — not less than 15%
- Reduction of Area — not less than 30%

**Table of Weights:** Forging, Type I — 6.88 lb max.; Forging, Type II — 6.38
lb max. (forging blank weight, not finished/loaded shell weight; no
arithmetic closure applies — single independent figures, not components of a
stated total).

**Image:** `images/fig8-page71-81mm-mortar-specs.jpeg` (full-page raster,
300 dpi).

## 75mm M48/M48B1 HE and M64 Chem — Forging Specification (page 73, drawing 75-20-77)

**Title block:** "FORGING FOR SHELL, H.E., 75MM, M48 AND M48B1 AND SHELL,
CHEM., M64", Class 75, Division 20, Drawing 77 (i.e. 75-20-77), dated Jan. 4,
1937, supersedes an old tracing per a revision dated Apr. 10, 1940, revised
through 8-15-45 (revision 12). Single forging, STEEL — a dimensional forging
blank, not the finished machined shell.

**List of Specifications table** (only 4 of 10 numbered lines are populated;
blank lines transcribed as blank, not omitted — note this drawing populates
line 3 where page 71's table populates line 4 for its finished-part spec;
the two tables are not laid out identically, only analogous in structure):

| Line | Specification                                        | Spec Number  | Required By  |
| ---- | ---------------------------------------------------- | ------------ | ------------ |
| 1    | AMMUNITION, EXCEPT SMALL ARMS AMM. GENERAL SPEC. FOR | 50-0-1       | DRG.75-20-77 |
| 2    | STEEL, FORGING FOR SHELL STOCK                       | 57-104-1     | DRG.75-20-77 |
| 3    | FORGINGS FOR COMMON STEEL SHELL AND SHRAPNEL         | **57-104-2** | DRG.75-20-77 |
| 8    | METALS, GENERAL SPECIFICATION FOR INSPECTION OF      | QQ-M-151     | 57-104-2     |

**CSV:** `tables/page73-75mm-spec-list.csv`. Unlike page 71 (where 57-104-2
appears only indirectly, as the "Required By" value for QQ-M-151), this
drawing lists **57-104-2 directly** as a specification required by the
drawing itself — printed with its own distinct title, "FORGINGS FOR COMMON
STEEL SHELL AND SHRAPNEL," alongside 57-104-1's "STEEL, FORGING FOR SHELL
STOCK" on the same table. Both titles confirmed at 2x zoom crop against
`source.pdf`.

**Physical Properties block** (printed once, captioned "PHYSICAL PROPERTIES
OF TEST SPECIMEN (SEE SPEC. 57-104-2) AND FINISHED MACHINED SHELL"):

- Yield Strength — not less than **65,000 lbs. per sq. in.**
- Elongation in 2 inches — not less than 15%
- Reduction of Area — not less than 30%

Identical figures to the 105mm M60 (p.5/6) and 155mm M107 (p.9) Body Shell
requirements, and explicitly captioned as governed by spec 57-104-2 — the
same spec number those two drawings cite, and the same one page 71's 81mm
mortar forging does *not* invoke directly.

**Table of Weights:** Forging — 20 lb. max. (single line, forging blank
weight, not finished/loaded shell weight; no arithmetic closure applies).

**Image:** `images/fig9-page73-75mm-m48-specs.jpeg` (full-page raster,
300 dpi).

## 105mm M60 (Chemical) — Metal Parts Assembly (page 5, drawing 75-4-91A)

**WEIGHTS table:**

| Part                            | Weight (lb) |
| ------------------------------- | ----------- |
| Body Shell                      | 24.24       |
| Band, Rotating                  | 0.47        |
| Adapter                         | 1.86        |
| **Total Weight, Empty (±0.60)** | **26.57**   |

**CSV:** `tables/m60-metal-parts-weights.csv`

**DESIGN DATA table** (loaded assembly):

| Part                        | Weight (lb) | Note |
| --------------------------- | ----------- | ---- |
| Shell, Empty (with Adapter) | 26.58       | Y    |
| Charge (Smoke), WP          | 4.08        | Z    |
| Charge, Burster, M5         | 0.36        |      |
| Casing, Burster, M5         | 1.11        |      |
| Cup, Fuze Well              | 0.02        |      |
| Booster, M22                | 0.73        |      |
| Fuze, M57                   | 1.41        |      |
| **Total**                   | **34.31**   |      |

**CSV:** `tables/m60-design-data.csv`

Booster **M22 = 0.73 lb** and rotating band **= 0.47 lb** both match the
user's own pre-extraction tally exactly.

## 155mm M107 (HE) — Metal Parts Assembly (page 9, drawing 75-4-99A)

**WEIGHTS table:**

| Part                                        | Weight (lb) |
| ------------------------------------------- | ----------- |
| Body Shell                                  | 76.12       |
| Band, Rotating                              | 1.20        |
| Cover, Base                                 | 0.14        |
| **Total Weight, Empty (±1.35)**             | **77.46**   |
| Plug, Lifting                               | 1.75        |
| Grommet                                     | 0.49        |
| **Shipping Weight of Metal Parts Assembly** | **78.70**   |

**CSV:** `tables/m107-metal-weights.csv`

**KNOWN DISCREPANCY:** Total Weight Empty (77.46) + Plug Lifting (1.75) +
Grommet (0.49) sums to 79.70, not the printed 78.70 — see
`checks/verify-weight-table-closures.py` output. The Plug Lifting figure
(1.75) was carried from a pre-compaction transcription pass and was **not**
re-verified against `source.pdf` at high zoom in this pass; the sum closes
exactly (78.70) if Plug Lifting were **0.75** instead. **Do not cite Plug
Lifting = 1.75 for page 9 without re-checking the raster** — flagged per
`source-data-fidelity.md` rather than silently "corrected" on arithmetic
alone.

**DESIGN DATA table** (loaded assembly, closes exactly):

| Part             | Weight (lb) |
| ---------------- | ----------- |
| Body Shell       | 76.12       |
| Band, Rotating   | 1.20        |
| Cover, Base      | 0.14        |
| Charge, Cast TNT | 15.13       |
| Cup, Fuze Well   | 0.02        |
| Fuze, P.D. M51   | 2.14        |
| **Total**        | **94.75**   |

**CSV:** `tables/m107-metal-design-data.csv`

Rotating band **= 1.20 lb**, matching the user's pre-extraction tally.

## 75mm M48 (HE) — Explosives Loading (page 23)

**Weight zones:**

| Zone | Over (lb) | Up to and incl. (lb) | Mark       |
| ---- | --------- | -------------------- | ---------- |
| L    | 11.80     | 12.12                | (unmarked) |
| 1    | 12.08     | 12.42                | +          |
| 2    | 12.38     | 12.72                | ++         |
| 3    | 12.68     | 13.00                | +++        |

**CSV:** `tables/m48-75mm-weight-zones.csv`

Note: each zone's "Over" value sits exactly 0.04 lb below the previous zone's
"Up to and including" value (12.12→12.08, 12.42→12.38, 12.72→12.68) — a
uniform, two-decimal-precise offset repeated at all three boundaries. Given
the consistency, read as a deliberate small overlap/tolerance band in the
source's own weight-sorting classification, not a transcription artifact.
The same pattern (with a different offset) appears in the 105mm and 155mm
zone tables below — see notes there.

**Charge weights:**

| Component                               | TNT (lb)  | Amatol (lb) |
| --------------------------------------- | --------- | ----------- |
| Shell Weight, Empty (±0.30)             | 10.97     | 10.97       |
| Charge, Bursting                        | 1.49      | 1.36        |
| Surround, Booster (Amatol loading only) | —         | 0.11        |
| **Total Weight, Unfuzed**               | **12.46** | **12.44**   |
| **Shipping Weight**                     | **12.46** | **12.44**   |

**CSV:** `tables/m48-75mm-charge-weights.csv`. Closes exactly on both
columns (`checks/verify-weight-table-closures.py`).

## 105mm M1 (HE) — Explosives Loading (page 25)

**Charge weights:**

| Component                               | TNT (lb)  | Amatol (lb) |
| --------------------------------------- | --------- | ----------- |
| Metal Parts Shipping Assembly (±0.60)   | 26.04     | 26.04       |
| Charge, Bursting                        | 4.84      | 4.57        |
| Surround, Booster (Amatol loading only) | —         | 0.18        |
| **Total Weight, Unfuzed**               | **30.88** | **30.79**   |
| Plug, Closing                           | 0.37      | 0.37        |
| **Shipping Weight**                     | **31.25** | **31.16**   |

**CSV:** `tables/m1-105mm-charge-weights.csv`. Closes exactly on both
columns. Charge Bursting (4.84/4.57) and Surround Booster (0.18) match the
user's own pre-extraction tally exactly.

**Weight zones:**

| Zone | Over (lb) | Up to and incl. (lb) | Mark                             |
| ---- | --------- | -------------------- | -------------------------------- |
| 1    | 29.9      | 30.6                 | uncertain (small stamped symbol) |
| 2    | 30.6      | 31.2                 | uncertain (small stamped symbol) |
| 3    | 31.1      | 31.8                 | uncertain (small stamped symbol) |

**CSV:** `tables/m1-105mm-weight-zones.csv`. Zone 1→2 tiles cleanly (30.6 =
30.6). Zone 2→3 does not (31.2 vs 31.1) — a smaller, non-uniform gap than the
75mm table's consistent 0.04 lb pattern, so here treated as a possible digit
misread rather than a confirmed source feature; not re-verified against
`source.pdf` at higher zoom. Mark symbols (small embossed/stamped icons) were
not confidently legible and are not transcribed as specific glyphs.

## 155mm M107 (HE) — Explosives Loading (page 53)

**Charge weights:**

| Component                 | Weight (lb) |
| ------------------------- | ----------- |
| Shell, Empty (±1.35)      | 77.46       |
| Charge, Bursting          | 14.61       |
| Liner                     | 0.035       |
| Charge, Supplementary     | 0.365       |
| **Total Weight, Unfuzed** | **92.47**   |
| Grommet                   | 0.49        |
| Plug, Lifting             | 1.75        |
| Spacer                    | 0.011       |
| **Shipping Weight**       | **94.72**   |

**CSV:** `tables/m107-155mm-charge-weights.csv`. Closes exactly (first sum)
and to 0.001 lb (second sum, rounding from the 3-decimal Spacer figure).

**Weight zones:**

| Zone | Over (lb)                    | Up to and incl. (lb)         | Mark        |
| ---- | ---------------------------- | ---------------------------- | ----------- |
| 1    | not legible in source raster | not legible in source raster | —           |
| 2    | 90.0                         | 91.3                         | two marks   |
| 3    | 91.1                         | 92.4                         | three marks |
| 4    | 92.2                         | 93.5                         | four marks  |
| 5    | 93.3                         | 94.6                         | five marks  |

**CSV:** `tables/m107-155mm-weight-zones.csv`. Same non-tiling pattern as the
105mm table (each "Over" trails the previous "Up to" by ~0.1–0.2 lb); not
re-verified at higher zoom. This table **replaces** the librarian's entirely
fabricated "155–163 lb, mark A–H" version — the actual source table has
weights in the 90–95 lb range with box-icon marks, not letter marks.

## Verification

**Script:** `checks/verify-weight-table-closures.py` — sums each charge-
weight/metal-weight table's component rows against its stated
Total/Shipping-Weight row. All closures pass exactly or within 0.005 lb
except the flagged M107 (page 9) Plug Lifting discrepancy above, which is
reported but not counted as a hard failure (documented, not silently
resolved). Run:

```
uv run python doc-reference/ww2-shells/ordnance-ammunition-drawings-book-4/checks/verify-weight-table-closures.py
```

The steel-spec identity tables (`body-shell-steel-specs.csv`,
`page71-81mm-spec-list.csv`, `page73-75mm-spec-list.csv`) carry no arithmetic
closure — they are identity/specification data, not a summable series — and
are admissible on direct-read provenance alone, consistent with
`../ammunition-series-6-wdss-specs/card.md`.

## Not extracted / out of scope

- Detailed dimensional drawings (contours, radii, thread callouts) on pages
    5, 9, 23, 25, 53 — the user flagged these as very hard to extract reliably
    from complex engineering drawings; only labeled discrete values (weights,
    spec numbers, yield strengths) were transcribed.
- The full List of Parts / List of Specifications tables on pages 6 and 14
    (screws, adhesives, minor hardware) beyond the Body Shell steel-spec rows
    captured above.
- Page 71's forging dimensional callouts (radii, thicknesses, die-relief
    geometry) and the six blank numbered lines (2, 3, 5, 6, 9, 10) of its List
    of Specifications table — only the populated rows and the Physical
    Properties block were transcribed.
- Page 73's forging dimensional callouts and the six blank numbered lines
    (4, 5, 6, 7, 9, 10) of its List of Specifications table — only the
    populated rows and the Physical Properties block were transcribed.
- Pages other than 5, 6, 9, 14, 23, 25, 53, 71, 73 (70 of 79 pages).

## Source

**Origin:** Ordnance Ammunition Drawings, Book 4 (U.S. Army Ordnance Dept.,
WW2 era)
**File:** originally at `/mnt/f/Projects/TMP/Docs/Ordnance Ammunition Drawings, Book 4.pdf`; retained as `source.pdf` beside this card (176 MB,
gitignored per `.gitignore:58` — re-acquire from the original location)
**Pages:** 79 total; 9 extracted (5, 6, 9, 14, 23, 25, 53, 71, 73)
**SHA256:** `0e5a061d0319e7dd19e0ab644ae83392b44de20226dad62fa5f9feaf35da1c5c`
**Images:** `images/fig1.jpeg`–`fig9-page73-75mm-m48-specs.jpeg` (9 total;
see Extraction provenance above)
