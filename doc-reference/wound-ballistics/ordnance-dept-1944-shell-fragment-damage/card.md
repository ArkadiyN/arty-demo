# Ordnance Department Terminal Ballistic Data: Shell Fragment Damage (1944)

**Source:** US Ordnance Dept., declassified 1944. Volume II, Part 3: Shell Fragment Damage (pages 126–186 of original, pages 10–70 of this extraction).

**Key Concept:** Fragment damage tables and patterns for field artillery shells used in WWII, parameterized by distance from burst, shell type, and burst conditions.

## Definition: B (Effective Hits per Square Foot)

**Anchor:** `number B of effective hits per sq. ft.` ([ordnance-1944.md:288](ordnance-1944.md#L288), 1 hit) — sentence defining B, matching this section's equation. PDF page 78, printed "Page 64".

$$B = \text{average number of effective hits per sq. ft. of target area at distance } r \text{ from burst}$$

**Validity & Caveats:**

- **Averaging:** $B$ values are averaged over different azimuthal directions from the burst
- **Applicability:** Valid only for a considerable number of bursts with random orientation of projectile axis relative to target (not for single shots)
- **Target state:** Assumes unshielded target; air bursts recommended for shielded personnel (e.g., foxholes)
- **Burst orientation:** Grazing (ground) or air burst; penetration depth depends on remaining velocity, angle of fall, soil type, and fuze type
- **Optimal burst height:** ~30 ft. for shielded personnel (practical rule: use 2× probable error in height, bounded 30–120 ft.)

## Damage Type Definitions

**Anchor:** `A casualty is supposed caused by a hit with at least 58 ft.-lb. of energy.` ([ordnance-1944.md:309](ordnance-1944.md#L309), 1 hit) — casualty and perforation-type definitions. PDF page 78, printed "Page 64".

- **Casualty:** Hit with ≥58 ft-lb kinetic energy (incapacitation, not necessarily fatal)
- **Perforation 1/8-in. mild steel:** Effective against aircraft on ground
- **Perforation 1/4-in. to 3/8-in. mild steel:** Effective against modern bombers
- **Perforation 1/2-in. mild steel:** Effective against trucks, light armored vehicles, rail stock

## Key Reference Shells (Project Match)

**Table numbers here are the ones printed on the page, and they will not grep.**
`ordnance-1944.md` is a flattened two-up scan that renumbers these same three
table-pairs 43/44, 51/52 and 59/60, and prints those `TABLE nn` lines detached
from the rows they label — under the 75-mm heading, for instance, the extraction
shows `TABLE 44` and `TABLE 43`. Grepping `TABLE 38` against the extraction
returns nothing useful, and grepping `TABLE 43` returns a different shell's
identity than the printed page gives. The printed numbering (38/39, 48/49,
56/57) is verified against the retained `source.pdf` by
`experiment/fragmentation-field/challenges/source-data-audit/checks/ordnance-1944-page-geometry.py`.
**Anchor on the shell-title headings below, never on a `TABLE nn` line.**

### Tables 38–39: 75-mm H.E. Shell, M48

**Anchor:** `# 75-MM H.E. SHELL, M48` ([ordnance-1944.md:381](ordnance-1944.md#L381), 1 hit) — heading governs the TABLE 38/39 casualties/perforation data beneath it (row r=20 casualties: `1,070 .213 .014 2,060`, matching this card). PDF page 84, printed "Page 70".

- **Initial Fragment Velocity:** 3,120 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–225 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.213 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.014 oz, 2,060 f/s

### Tables 48–49: 105-mm H.E. Shell, M1

**Anchor:** `# 105-MM H.E. SHELL,'Ml` ([ordnance-1944.md:725](ordnance-1944.md#L725), 1 hit; OCR-mangled, quoted exactly as stored) — heading governs the TABLE 48/49 casualties/perforation data beneath it (row r=20 casualties: `1,160 .231 .010 2,440`, matching this card). PDF page 89, printed "Page 75".

- **Initial Fragment Velocity:** 3,500 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–300 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.231 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.010 oz, 2,440 f/s

### Tables 56–57: 155-mm H.E. Shell, M107

**Anchor:** `# 155-MM N.E. SHELL, M107` ([ordnance-1944.md:874](ordnance-1944.md#L874), 1 hit; OCR-mangled "H.E." → "N.E.", quoted exactly as stored) — heading governs the TABLE 56/57 casualties/perforation data beneath it (row r=20 casualties: `1,460 .291 .010 2,440`, matching this card). PDF page 93, printed "Page 79".

- **Initial Fragment Velocity:** 3,500 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–400 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.291 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.010 oz, 2,440 f/s

## Fragment Damage Patterns

**Anchor:** `### 2. DAMAGE PATTERNS` ([ordnance-1944.md:291](ordnance-1944.md#L291), 1 hit) — heading governs the shading/density-interpretation text quoted below it in this card. PDF page 78, printed "Page 64".

The document includes 60+ damage-pattern figures (Figures 67 onward) showing fragment distribution for individual shells. Patterns vary with:

- Remaining velocity (function of range)
- Angle of fall
- Height of burst (grazing vs. air burst)

**Pattern Shading Interpretation:** Regional boundaries mark effective hit densities:

- **Unshaded (white center):** ≥1 hit per sq. ft. (highest damage)
- **Lightest shade:** ≥1 hit per 4 sq. ft.
- **Medium shade:** ≥1 hit per 10 sq. ft.
- **Darkest shade:** ≥1 hit per 25 sq. ft.
- **Regions outside darkest shade:** \<1 hit per 25 sq. ft. (no guarantee of hits)

**Assumptions:** Patterns assume grazing or air burst, unshielded target, and represent typical single-shot cases (contrast with statistical $B$ tables, which require multiple bursts).

**Saved as images only — qualitative reference, no digitization of shaded-band boundaries.**

### Tables 38–39 (75-mm H.E. M48) — Figures 67–73, original pages 140–143

![fig67-68](images/fig67-68_75mm-M48_casualties-ground-burst.png)
Figures 67–68 — Casualties, ground burst (shell horizontal at rest / remaining velocity 800 f/s, range 8,500 yd, 75-mm Gun M3)

![fig69-70](images/fig69-70_75mm-M48_casualties-hob30-60.png)
Figures 69–70 — Casualties, height of burst 30 ft / 60 ft (same velocity/range/gun)

![fig71-72](images/fig71-72_75mm-M48_perforation-ground-burst.png)
Figures 71–72 — Perforation of 1/8-in. mild steel, ground burst

![fig73](images/fig73_75mm-M48_perforation-hob30.png)
Figure 73 — Perforation of 1/8-in. mild steel, height of burst 30 ft

### Tables 48–49 (105-mm H.E. M1) — Figures 93–100, original pages 154–158

![fig93-94](images/fig93-94_105mm-M1_casualties-ground-burst.png)
Figures 93–94 — Casualties, ground burst (remaining velocity 800 f/s, range 7,000 yd charge 5, 105-mm How. M2A1)

![fig95](images/fig95_105mm-M1_casualties-hob30.png)
Figure 95 — Casualties, height of burst 30 ft

![fig96](images/fig96_105mm-M1_casualties-hob60.png)
Figure 96 — Casualties, height of burst 60 ft

![fig97-98](images/fig97-98_105mm-M1_perforation-ground-burst.png)
Figures 97–98 — Perforation of 1/8-in. mild steel, ground burst

![fig99-100](images/fig99-100_105mm-M1_perforation-hob30-60.png)
Figures 99–100 — Perforation of 1/8-in. mild steel, height of burst 30 ft / 60 ft

### Tables 56–57 (155-mm H.E. M107) — Figures 117–125, original pages 168–173

![fig117-118](images/fig117-118_155mm-M107_casualties-ground-burst.png)
Figures 117–118 — Casualties, ground burst (remaining velocity 900 f/s, range 9,000 yd charge 5, 155-mm How. M1)

![fig119-120](images/fig119-120_155mm-M107_casualties-hob30-60.png)
Figures 119–120 — Casualties, height of burst 30 ft / 60 ft

![fig121](images/fig121_155mm-M107_casualties-hob30.png)
Figure 121 — Casualties, height of burst 30 ft (remaining velocity 950 f/s, range 9,500 yd)

![fig122](images/fig122_155mm-M107_casualties-hob60.png)
Figure 122 — Casualties, height of burst 60 ft (remaining velocity 950 f/s)

![fig123-124](images/fig123-124_155mm-M107_perforation-ground-burst.png)
Figures 123–124 — Perforation of 1/8-in. mild steel, ground burst

![fig125](images/fig125_155mm-M107_perforation-hob30-60.png)
Figure 125 — Perforation of 1/8-in. mild steel, height of burst 30 ft / 60 ft

**Provenance:** extracted via local PyMuPDF full-page rasterization (`pdf-processor.py --screenshot-pages`), not vision AI — these are direct screenshots of the scanned original, cropped to nothing (full page, including the printed page number and figure captions for traceability).

## Data Sources

**Anchor:** `### 5. THE SOURCES OF DATA` ([ordnance-1944.md:307](ordnance-1944.md#L307), 1 hit) — the source's own section heading for this material.

**This section's body is displaced by the two-up flattening.** Its one sentence
sits at `ordnance-1944.md:310`, wedged between the two halves of a sentence
belonging to the preceding section ("…the most effective damage varies from
that with" / "-in. perforation to 38-in. perforation…"), which reads correctly
with line 310 removed. The heading at 307 and the body at 310 are three lines
apart but do not read as continuous text; anchor on the heading.

What the source states, in its own words (`ordnance-1944.md:310`): the damage
tables and patterns are derived "from measurements of fragment velocity,
retardation, shape, and penetration, and the mass and angular distribution of
fragments as made at the various Army and Navy proving grounds and
laboratories."

The source does **not** state where the 58 ft-lb casualty threshold came from —
it gives the threshold as a definition ("A casualty is supposed caused by a hit
with at least 58 ft.-lb. of energy", `ordnance-1944.md:309`) and attributes it
to nothing. An earlier version of this card credited it to "ballistic-medical
studies" and described the penetration data as "controlled tests on steel
targets"; neither phrase nor its substance is in the source, and both have been
struck.

**Do not use `source.pdf`'s text layer to establish that something is absent
from this document.** The layer covers the tabular pages but not these prose
pages: `pdftotext` extracts ~186 k characters and finds `SHELL` 149×,
`FRAGMENT` 206× and `Ordnance` 22×, yet returns **zero** hits for
`SOURCES OF DATA`, `retardation`, `Army`, `Navy` and `proving` — all of which
are demonstrably on the page above. A full-text search of the PDF returning
nothing is not evidence of absence here; check the extraction, or the page
image.

______________________________________________________________________

**Navigation:** Full text and damage patterns in `ordnance-1944.md`. Fragment damage diagrams (Figures 67–125) in `images/`.
