---
name: family-b-overprediction-three-calibers
description: Family B (four_zone_lethal_density_field) over-predicts 1944 Ordnance Dept B(r) card data by a growing factor across three calibers, not a per-shell fluke
metadata:
  type: project
---

Confirmed on 75mm/105mm/155mm independently: fragment velocity decays
several-fold too slowly vs. source's own velocity-vs-range data (V0 and
lethal-energy threshold ruled out). Prime suspect: `DragParams`
(`C_D=0.65`, `C_shape=0.90` in `src/arty/fragmentation.py`) understates drag —
previously unsourced; two literature sources now give `C_D`/`Cd` ≈1.2-1.7 for
this fragment class, but under different shape-factor parameterizations, not
drop-in values.

**How to apply:** treat as root-cause-traced already — next step is a
derivation pass recalibrating the retardation law, not a fresh hypothesis
search. See `experiment/fragmentation-field/challenges/ordnance-1944-b-vs-range.qmd`
and the per-caliber `ordnance-1944-initial-conditions-check-*.md` /
`review.md` for the full validation record.
