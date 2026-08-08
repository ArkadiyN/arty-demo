# Figure 3: Drag Coefficient of Fragments — Digitized Curve

> **⚠ SUPERSEDED — DO NOT CITE. Use `tables/figure-3-drag-coefficient.csv`.**
> The table below was read by eye and is wrong through the transonic rise. A
> pixel trace of the retained scan
> (`experiment/fragmentation-field/challenges/source-data-audit/checks/dod-1975-figure-3-trace.py`)
> puts C_D at Mach 1.0 at **1.23**, not 1.14, and the peak at **Mach 1.46**,
> not 1.4; the table under-states C_D by up to 0.082 across Mach 1.0–2.2. The
> calibration behind that trace reproduces the source's own stated supersonic
> value (1.28) and the peak and subsonic plateau this folder's `card.md`
> reports, all to 0.001. Kept, not deleted, because its numbers were
> hand-copied into a check script that is still live; see
> `experiment/fragmentation-field/challenges/source-data-audit/ledger.md` §13b.

FINDING\[blocking\]: figure-3-digitized.md under-states C_D by up to 0.082 across Mach 1.0-2.2 and misplaces the transonic rise; its hand-copied array in required-retardation-vs-mach.py fed the rejection of Mach-dependent drag, and the error runs in the direction that weakens that candidate — read tables/figure-3-drag-coefficient.csv instead (affects: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/figure-3-digitized.md, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/required-retardation-vs-mach.py, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md, app/sensitivity.py; since: 2026-08-02)

**Source:** DOD (1975), _Fragment and Debris Hazards_, "Figure 3 Drag Coefficient of Fragments" — `source.pdf` p.33 = report page 23 (extraction: `10-F-0806_Fragment_and_Debris_Hazards.md`, lines 300–370)

**Method:** Visual reading from published plot; curve traced by eye at grid intersections. **This method is why it is wrong** — see the banner above.

## Digitized (Mach, C_D) pairs

| Mach | C_D  |
| ---- | ---- |
| 0.0  | 1.08 |
| 0.5  | 1.09 |
| 0.8  | 1.10 |
| 1.0  | 1.14 |
| 1.2  | 1.38 |
| 1.4  | 1.40 |
| 1.6  | 1.35 |
| 1.8  | 1.33 |
| 2.2  | 1.30 |
| 2.6  | 1.29 |
| 3.0  | 1.28 |
| 4.0  | 1.28 |
| 5.0  | 1.28 |
| 7.0  | 1.28 |

## Curve shape and uncertainty

The curve exhibits a subsonic plateau (C_D ≈ 1.08–1.10 for Mach 0–0.8), a sharp transonic peak near Mach 1.4 (C_D ≈ 1.40), and a supersonic asymptote converging to approximately 1.28 by Mach 3. Read uncertainty is approximately ±0.02 in C_D and ±0.1 in Mach number, limited by grid line spacing and line thickness in the source publication.
