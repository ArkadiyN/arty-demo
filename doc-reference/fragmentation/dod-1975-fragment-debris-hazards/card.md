# DoD Explosives Safety Board, Technical Paper 12 (1975) — Fragment Drag Coefficient

**Extract Card: Figure 3 (report p.23) & Section "Ballistic Properties" (report pp. 7–9)**

## Tables — read these, not the prose

| File | What it holds | Closure |
| ---- | ------------- | ------- |
| `tables/figure-3-drag-coefficient.csv` | $C_D$(Mach), 140 rows at 0.05 Mach, traced off the scan at 300 dpi | plateau reproduces the source's stated 1.28 |
| `tables/ballistic-constants.csv` | $k$, $C_D$, $\rho$, $L_1$ — the trio the report ties together on p.9 | $L_1 = 2k^{2/3}/(C_D\rho)$ reproduces the stated 247 |

`figure-3-digitized.md` is **superseded** — it was read by eye and is wrong
through the transonic rise. See its banner and
`experiment/fragmentation-field/challenges/source-data-audit/ledger.md` §13.

## Data Content

Figure 3 plots drag coefficient $C_D$ (dimensionless) vs. Mach number; the
traced curve (`tables/figure-3-drag-coefficient.csv`) covers Mach 0.00–7.00,
matching the printed axis. (image: `images/figure-3-drag-coefficient-vs-mach.png`;
caption anchor "Figure 3 Drag Coefficient of Fragments" — single space, verified
`grep` hit at `10-F-0806_Fragment_and_Debris_Hazards.md:728` — `source.pdf`
p.33 = report p.23). Read off the traced curve:

- **Subsonic (M ≤ 0.6):** flat at $C_D = 1.079$.
- **Transonic (M ≈ 0.7–1.15):** steep rise, 1.09 → 1.32.
    **Known CSV defect:** the mach=1.00 row (cd=1.233, band 1.222–1.243)
    undershoots the page value (~1.257) by ~0.024 and the band excludes it —
    see the blocking finding on `tables/figure-3-drag-coefficient.csv` and its
    `.invariant`. Do not cite a specific C_D at M=1.0 from this CSV pending
    correction; the shape of the rise (steep, ending above 1.3 by M≈1.15) is
    not in question, only the exact value at this one point.
- **Peak (M = 1.46):** $C_D = 1.400$, ≈9.4% above the supersonic plateau.
    The report itself characterises the whole subsonic-to-supersonic variation
    as "rather modest despite a peak near the sound speed" (verified anchor
    "rather modest despite a peak near the so~nd speed" —
    `10-F-0806_Fragment_and_Debris_Hazards.md:337`, report p.8 = `source.pdf`
    p.18, OCR mangles "sound" as "so~nd"). Whether 9.4% is material to a
    constant-$C_D$ approximation is a modelling question, not a transcription
    one — see `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md`.
- **Supersonic plateau (M ≳ 2.9):** settles to $C_D = 1.280$, flat out to
    M = 7 — this is the constant value the report recommends as a
    simplification (verified anchor "supersonic value of 1.28" —
    `10-F-0806_Fragment_and_Debris_Hazards.md:339`, report p.8 = `source.pdf`
    p.18).

## Source & Test Conditions

**Secondhand.** Everything in this section is DoD-1975 paraphrasing its
reference 10 (Dunn & Porter, BRL MR 915, 1955 — see below), which is not
held in `doc-reference/`. Reported as DoD-1975's method description, not
verified against the primary.

**Experimental method:** fragments recovered from detonation tests were fired
from a smooth-bore launcher; velocity decrease with distance observed to
determine drag coefficient as a function of Mach number (verified anchor
"smooth-bore launcher" — `10-F-0806_Fragment_and_Debris_Hazards.md:333`,
report p.8 = `source.pdf` p.18, Section "Ballistic Properties").

**Fragment type:** treated as geometrically similar bodies with relation
$m = k A^{3/2}$, $k = 2.6~\text{g/cm}^3$ average "for forged steel projectiles
and fragmentation bombs" (verified anchor "shape factor or ballistic density"
— `10-F-0806_Fragment_and_Debris_Hazards.md:317`, report p.7 = `source.pdf`
p.17); mean presented area measured by an "icosahedron gage" (verified anchor
"hedron gage" — `10-F-0806_Fragment_and_Debris_Hazards.md:306`, same page) or,
for regular shapes, one-fourth the surface area.

**Original data source:** reference 10 = D. J. Dunn, Jr. and W. R. Porter,
*Air Drag Measurements of Fragments*, BRL MR 915, August 1955 (verified anchor
"Dunn, Jr. and W. R. Porter" — `10-F-0806_Fragment_and_Debris_Hazards.md:575`,
report p.17 = `source.pdf` p.27, reference list). Not held in
`doc-reference/`.

## Trajectory Model Integration

Velocity decay formula with constant $C_D$ (verified anchor "parameter L is
defined by" — `10-F-0806_Fragment_and_Debris_Hazards.md:349`, report p.8 =
`source.pdf` p.18):\
$$v = V_0 \exp(-R/L)$$
where $L = 2(k^{2/3} m^{1/3})/(C_D \rho) = L_1 m^{1/3}$ (distance for 1/e decay).
For $k = 2.6~\text{g/cm}^3$, $C_D = 1.28$: $L_1 = 247~\text{m/kg}^{1/3}$
(verified anchor "L1 = 247" — `10-F-0806_Fragment_and_Debris_Hazards.md:358`,
report p.9 = `source.pdf` p.19).

## Applicability & Caveats

**Shape-factor $k$ is weapon-class-specific, per the source's own text:**
$k = 2.6~\text{g/cm}^3$ (660 grains/in³) is the recommended average "for forged
steel projectiles and fragmentation bombs" (verified anchor "for forged steel
projectiles and fragmentation bombs" — `10-F-0806_Fragment_and_Debris_Hazards.md:320`,
report p.7 = `source.pdf` p.17); a distinct value, $k = 2.33~\text{g/cm}^3$
(590 grains/in³), is stated "for demolition bombs" (verified anchor "590
grains" — `10-F-0806_Fragment_and_Debris_Hazards.md:322`, same page). The
source gives no separate value for artillery-shell fragments as a class.

**Velocity range:** the traced curve (`tables/figure-3-drag-coefficient.csv`)
spans Mach 0.00–7.00, matching the printed axis — see "Data Content" above;
this is a claim about the figure image, not a textual anchor.

**Whether this $k$/$C_D$ pair is the correct calibration anchor for this
project's naturally-fragmenting-shell fragments is a criterion-match question,
and it is adjudicated elsewhere — start at
`experiment/fragmentation-field/updates/mach-dependent-fragment-drag/README.md`,
which separates that update's live half (the ballistic-density drag anchor)
from its retired half. Do not read its `derivation.md` §5 without reading that
README first; §5 is withdrawn. This card does not repeat or summarize the
adjudication.**

## Provenance of this card

- **Document:** Department of Defense Explosives Safety Board, *Technical
    Paper No. 12 — Fragment and Debris Hazards*, July 1975 (verified anchor
    "TECHNICAL PAPER NO. 12" — `10-F-0806_Fragment_and_Debris_Hazards.md:1`,
    report title page = `source.pdf` p.1).
- **`source.pdf`:** 42 pages; `sha256:
    9ff9e66f43b6ecf08598bfcc23ec3b729b0e3b5466d146a99b775df331393903`.
    Gitignored (`doc-reference/**/*.pdf`) — it does **not** survive a fresh
    clone.
- The "Source & Test Conditions" section above is **secondhand**: it reports
    DoD-1975's own paraphrase of its reference 10 (Dunn & Porter, BRL MR 915,
    1955), which is not held in `doc-reference/` and has not been checked
    against the primary.
- `10-F-0806_Fragment_and_Debris_Hazards.md` is a general OCR/vision
    transcription of the whole report; `figure-3-digitized.md` (the
    hand-read-off-Figure-3 table) is superseded and known wrong through the
    transonic rise — treat `tables/figure-3-drag-coefficient.csv` and
    `tables/ballistic-constants.csv`, each with a stated closure invariant, as
    the source of numbers for those two tables, not either markdown file.
