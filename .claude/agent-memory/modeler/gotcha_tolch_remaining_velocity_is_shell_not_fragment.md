---
name: gotcha-tolch-remaining-velocity-is-shell-not-fragment
description: Tolch 1944's "remaining velocity" axis is the shell's velocity at burst, not fragment decay — its card.md wrongly sells it as a drag anchor
metadata:
  type: project
---

In `doc-reference/wound-ballistics/tolch-1944-m48-panel-pit-fragmentation/`,
"average remaining velocity when burst" is the **shell's** velocity at the
burst point (swept 0–2130 f/s by firing charge), at fixed panel radius. The
base-spray collapse and nose-spray rise across that axis are vector addition
of shell velocity onto Gurney ejection — a **burst-geometry / spray-angle**
observable, near-insensitive to drag.

**Why:** `card.md`'s "Drag Model Relevance" section recommends exactly that
collapse as the drag calibration anchor. It is the least drag-sensitive
number in the report. The card is still wrong on disk (librarian's to fix).

**How to apply:** Tolch's drag content is the **panel-radius** axis
(15/36/75/120 ft) plus the absolute fragment counts in Summary items 1/6/8 —
never the velocity sweep. Full working:
`experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1944-panel-distance.md`.
See also [[gotcha-density-falloff-shape-is-threshold-degenerate]].
