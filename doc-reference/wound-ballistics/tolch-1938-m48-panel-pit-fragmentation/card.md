---
title: Tolch (1938) — 75mm M48 Shell Fragmentation Effects
report: N.A. Tolch, Fragmentation Effects of the 75mm H.E. Shell T3 (M48), Ballistic Research Laboratory Report No. 126, Aberdeen Proving Ground, December 1938, Declassified
---

# Fragment Density: Hits per Unit Solid Angle

**Definition** (`tolch-1938.md`, grep `"the results were expressed in terms of hits per unit solid angle"`, line 613): a unit solid angle is the solid angle subtended by 1/100 of a unit spherical surface at unit radius — equivalently, the solid angle subtended by 1 sq. yd. at 10 yd. distance. Fragment density = hits per unit solid angle, measured via semi-circular wood panel tests at varying angles from the shell axis, panel distances (15–120 ft), and shell remaining-velocity-at-burst conditions (static, 700–2,130 f/s). **Distinct from Ordnance Dept (1944) "effective hits per sq-ft" (B-value):** this report measures raw perforations/penetrations/dents per solid angle, preserving directional and velocity dependence without casualty weighting.

**Fragment classes and their angular windows** (grep `"0 and 17.5 deg"` line 915; `"162.5 and 180 deg"` line 859; `"76 and 111 deg"` line 804): nose spray 0–17.5° off axis; side spray averaged over a 35° window centered on its densest region (76–111° static, sweeping forward as remaining velocity rises); base spray 162.5–180°.

**Typical battle velocity** (grep `"remaining velocity of shell used in battle"`, line 182): 800–900 f/s modal ("S00" in the OCR — read as 800 from context); rarely below 700 or above 1,100 f/s.

**What "remaining velocity" is** — anywhere this card gives a value keyed to "average remaining velocity," that is the **shell's own velocity at the burst point**, a firing condition set by charge/range and swept 0 (static) → 2,130 f/s across rounds at *fixed* panel radius (`tables/base-spray-density.invariant`, `tables/nose-spray-density.invariant`). It is not a fragment velocity and is not derived from fragment drag or decay.

______________________________________________________________________

## Velocity-Dependence Summary

Pages 40–44 (containing all four tables below) were re-extracted with vision AI after the initial heuristic pass produced scrambled/column-misaligned numbers. **The re-extraction still has errors** (see Base Spray below) — the authoritative source for these four tables is the `tables/*.csv` files, each read directly off the page images and each checked against a stated closure invariant (`tables/*.invariant`), not `tolch-1938.md`.

**`tolch-1938.md` is not a citable surface for any number.** The page-stacking defect that produced it is recorded in `.claude/incidents.md`; it is retained for navigation and for greppable anchors only. Every quantity this card cites is anchored to a `tables/*.csv`, and a number that has no CSV has no admissible surface in this repo — it is not to be read off the markdown instead.

### Base Spray (Rear Fragments) — Velocity Opposes Ejection

Table criterion (source's own words, grep `"Total hits per unit solid angle of the base spray."`, line 896), summed from the component table at grep `"Number of perforations, penetrations, and dents of the base spray per unit solid angle."` (line 861). Columns: `v_fps` (shell remaining velocity at burst), `panel` (A/B/C at 15/36/75 ft), `perf`/`penet`/`dents`/`total` (hits per unit solid angle). Full series: `tables/base-spray-density.csv` (17 rows); closure `perf+penet+dents==total` holds exactly on all 17 cells (`tables/base-spray-density.invariant`).

- **Perforations (Panel A):** ~50% drop at 1,085 f/s → ~85% drop at 1,450 f/s → "practically zero" at 2,130 f/s (grep `"perforations per unit solid angle are reduced by about 50%"`, line 888)
- **Penetrations (Panel A):** decrease slowly; ~1/3 remain even at 2,130 f/s (grep `"almost one third as many penetrations per unit solid angle"`, line 890)
- **Total hits per u.s.a. (Panel A):** 9.71 (static) → 0.70 (2,130 f/s), a 93% reduction. Both figures agree between `tolch-1938.md` line 900/905 and `tables/base-spray-density.csv`.
- **`tolch-1938.md`'s own table is corrupted in ~20 of 54 component cells** — do not read totals off it. Two examples caught by the CSV's closure invariant: the 2,130 f/s Panel B row prints total 3.12 in `tolch-1938.md` line 905 vs. 1.12 in the CSV (perf+penet+dents = 0.00+0.71+0.41 = 1.12); the 1,085 f/s Panel C row prints 0.65 in `tolch-1938.md` line 902 vs. 0.85 in the CSV (0.24+0.53+0.08 = 0.85). Use `tables/base-spray-density.csv` for any cell not already quoted above.
- **Cumulative fragment-velocity distribution — unresolved, do not cite.** This is a permanent state of this source at its current scan quality, not a pending action. The narrative sentence giving this breakdown (grep `"about 20% of the base fragments have velocity greater than 700 f/s"`, line 907) sits on a page scanned at ~100 DPI. Two independent extractions disagree and neither is fully self-consistent for a "% exceeding threshold" series, which must be monotonically decreasing as the threshold rises:
    - Pre-re-extraction heuristic-path manual read (scrambled table, interpreted by hand; **superseded, no longer present verbatim in `tolch-1938.md`**): 80% > 700 f/s, 48% > 1,085 f/s, 29% > 1,450 f/s, 14% > 1,685 f/s, ~7% > 2,130 f/s — monotonic and physically sensible, but reconstructed from a garbled source, not a direct transcription.
    - Current vision re-extraction (`tolch-1938.md` line 907, anchor above): 20% > 700 f/s, 15% > 1,085 f/s, 25% > 1,450 f/s, 18% > 1,685 f/s, 7% > 2,130 f/s — non-monotonic (25% at 1,450 f/s exceeds 15% at 1,085 f/s, impossible for a cumulative distribution), so this reading is provably wrong on at least one digit.
    - Neither figure should be used for model calibration; no better scan has been located within the audits performed so far.

### Nose Spray (Forward Fragments) — Velocity Adds to Ejection

Table criterion (grep `"Total number of hits in the nose spray per unit solid angle."`, line 952; components at grep `"Number of perforations, penetrations, and dents of the nose spray per unit solid angle."`, line 917). Same columns as the base-spray table. Full series: `tables/nose-spray-density.csv` (17 rows); closure holds exactly on 16 cells and to 0.01 (rounding) on the 17th (`tables/nose-spray-density.invariant`).

- Perforations **increase markedly** with velocity (grep `"the fragment densities of the nose spray are rather erratic"` for the surrounding discussion, line 944)
- Range extends: Panel C hit density becomes comparable to Panel A at high remaining velocity (same anchor)
- Total hits per u.s.a. (Panel A): 16.09 (static) → 21.45 (2,130 f/s); Panel B shows a larger relative rise, 2.42 → 26.31 (`tables/nose-spray-density.csv`, matches `tolch-1938.md` line 956/961)

### Side Spray (Lateral Fragments) — Angular Deflection

Table criterion (grep `"Total number of hits per unit solid angle in side spray."`, line 836; components at grep `"Number of perforations, penetrations, and dents per unit solid angle of the sidcspray."`, line 813). Columns as above, plus `angle` (deg. off shell axis, the 35°-wide window the row's density is averaged over — not tabulated in the CSV, see below). Full series: `tables/side-spray-density.csv` (20 rows); closure exact on all 20 cells (`tables/side-spray-density.invariant`).

- Static: window centered ~93.5° off shell axis (76–111°); 2,130 f/s: window centered ~53.5° off axis (36–71°) — grep `"the sidespray is moved forward due to remaining velocity"`, line 804.
- Density remains roughly 2–6 hits/u.s.a. across velocities and panels; see `tables/side-spray-density.csv` for exact cells.
- **`tolch-1938.md`'s totals table (line 838 ff.) disagrees with the CSV at 1,085 f/s** — it prints Panel A/B/C 4.26/3.56/1.90 vs. the CSV's 4.06/3.42/1.96 (`tables/side-spray-density.invariant` documents this as a known corrupted reading; the CSV is the vision-path re-extraction and is the one to cite).

______________________________________________________________________

## Fragment Velocities (Charge Components)

**Not directly measured** — both figures are a geometric inference, not a drag or independent-Gurney measurement. The source states three times that they were computed from the change in the side-spray angle with remaining velocity (grep `"duo to the explosive charge averaged"` line 146; grep `"computed from the change in the sldespray angle Is"` line 1658; grep `"computed velocity of the perforating fragments due to the ex"` line 1698):

- **Perforating fragments:** printed "27^0 f/s" at all three locations above — **the third digit is unreadable on this scan surface**; commonly read as 2,750 f/s but that reading is not certain. Do not treat 2,750 as an exact source value.
- **Penetrating fragments:** 3,030 f/s (clean at all three anchors, and independently at the "Ave. 3030" line in the underlying per-round table, grep `"Ave. 3030"`, line 1654).

Higher penetrating-fragment velocity is attributed by the source to smaller size and lower ballistic coefficient (same anchors).

______________________________________________________________________

## Drag-model transfer question — see the assessment, not this card

Whether any part of this report is a usable independent check on the project's fragment-drag model is a criterion-match question (does the report's velocity axis measure fragment deceleration, or something else?), and it has already been answered: `experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md`. Read that document for the transfer analysis (which axis is/is not drag-sensitive, what it does and does not corroborate). This card does not repeat or summarize that conclusion.

______________________________________________________________________

## Provenance of this card

- **Document:** N.A. Tolch, *Fragmentation Effects of the 75mm H.E. Shell T3 (M48), as Determined by Panel and Pit Fragmentation Tests*, Ballistic Research Laboratory Report No. 126, Aberdeen Proving Ground, **December 1938** (declassified; DTIC AD0702233).
- **`source.pdf`:** 89 pages; `sha256: 13e110d70b1cb686771d6f2e36523d9c9201551d41c7b3b9eb27685d71f90c92`. Gitignored (`doc-reference/**/*.pdf`) — it does **not** survive a fresh clone; re-fetch from DTIC AD0702233 if missing.
- Tables were re-extracted from the PDF page images directly into `tables/*.csv`, each with a stated closure invariant in the matching `.invariant` file (`uv run src/utils/check-table-invariants.py <path>`). `tolch-1938.md` is a general-purpose OCR/vision transcription of the whole document and is known to be wrong in a large fraction of cells in the base-, nose-, and side-spray component tables (see per-table notes above) — treat the CSVs, not the markdown, as the source of numbers for these four tables.
