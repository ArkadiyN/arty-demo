# Ordnance Department Terminal Ballistic Data: Shell Fragment Damage (1944)

**Source:** US Ordnance Dept., declassified 1944. Volume II, Part 3: Shell Fragment Damage (pages 126–186 of original, pages 10–70 of this extraction).

**Key Concept:** Fragment damage tables and patterns for field artillery shells used in WWII, parameterized by distance from burst, shell type, and burst conditions.

## Definition: B (Effective Hits per Square Foot)

**Anchor:** [Line 261](ordnance-1944.md#L261)

$$B = \text{average number of effective hits per sq. ft. of target area at distance } r \text{ from burst}$$

**Validity & Caveats:**

- **Averaging:** $B$ values are averaged over different azimuthal directions from the burst
- **Applicability:** Valid only for a considerable number of bursts with random orientation of projectile axis relative to target (not for single shots)
- **Target state:** Assumes unshielded target; air bursts recommended for shielded personnel (e.g., foxholes)
- **Burst orientation:** Grazing (ground) or air burst; penetration depth depends on remaining velocity, angle of fall, soil type, and fuze type
- **Optimal burst height:** ~30 ft. for shielded personnel (practical rule: use 2× probable error in height, bounded 30–120 ft.)

## Damage Type Definitions

**Anchor:** [Lines 271–276](ordnance-1944.md#L271-L276)

- **Casualty:** Hit with ≥58 ft-lb kinetic energy (incapacitation, not necessarily fatal)
- **Perforation 1/8-in. mild steel:** Effective against aircraft on ground
- **Perforation 1/4-in. to 3/8-in. mild steel:** Effective against modern bombers
- **Perforation 1/2-in. mild steel:** Effective against trucks, light armored vehicles, rail stock

## Key Reference Shells (Project Match)

### Table 43: 75-mm H.E. Shell, M48

**Anchor:** [Lines 340–369](ordnance-1944.md#L340-L369)

- **Initial Fragment Velocity:** 3,120 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–225 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.213 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.014 oz, 2,060 f/s

### Table 51: 105-mm H.E. Shell, M1

**Anchor:** [Lines 676–709](ordnance-1944.md#L676-L709)

- **Initial Fragment Velocity:** 3,500 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–300 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.231 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.010 oz, 2,440 f/s

### Table 59: 155-mm H.E. Shell, M107

**Anchor:** [Lines 817–849](ordnance-1944.md#L817-L849)

- **Initial Fragment Velocity:** 3,500 f/s
- **Damage Parameter Table:** Casualties and 1/8-in. mild steel perforation
- **Distance Range:** 20–400 ft from burst center
- **Sample B Value (Casualties @ 20 ft):** 0.291 hits/sq ft
- **Lightest Effective Fragment (Casualties @ 20 ft):** 0.010 oz, 2,440 f/s

## Fragment Damage Patterns

**Anchor:** [Lines 263–270](ordnance-1944.md#L263-L270)

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

### Table 43 (75-mm H.E. M48) — Figures 67–73, original pages 140–143

![fig67-68](images/fig67-68_75mm-M48_casualties-ground-burst.png)
Figures 67–68 — Casualties, ground burst (shell horizontal at rest / remaining velocity 800 f/s, range 8,500 yd, 75-mm Gun M3)

![fig69-70](images/fig69-70_75mm-M48_casualties-hob30-60.png)
Figures 69–70 — Casualties, height of burst 30 ft / 60 ft (same velocity/range/gun)

![fig71-72](images/fig71-72_75mm-M48_perforation-ground-burst.png)
Figures 71–72 — Perforation of 1/8-in. mild steel, ground burst

![fig73](images/fig73_75mm-M48_perforation-hob30.png)
Figure 73 — Perforation of 1/8-in. mild steel, height of burst 30 ft

### Table 51 (105-mm H.E. M1) — Figures 93–100, original pages 154–158

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

### Table 59 (155-mm H.E. M107) — Figures 117–125, original pages 168–173

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

**Anchor:** [Lines 273–276](ordnance-1944.md#L273-L276)

Fragment velocity, retardation, shape, mass, and angular distribution measured at Army and Navy proving grounds; penetration data from controlled tests on steel targets; casualty thresholds from ballistic-medical studies (58 ft-lb minimum energy for incapacitation).

______________________________________________________________________

**Navigation:** Full text and damage patterns in `ordnance-1944.md`. Fragment damage diagrams (Figures 67–125) in `images/`.
