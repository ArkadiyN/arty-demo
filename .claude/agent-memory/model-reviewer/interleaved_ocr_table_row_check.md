---
name: interleaved-ocr-table-row-check
description: OCR-interleaved reference tables need a full-row monotonicity/cross-column check, not just the rows the modeler already flagged as swapped
metadata:
  type: feedback
---

When a doc-reference source interleaves two tables row-by-row from a
two-column OCR scan (seen in `ordnance-1944.md`: casualties vs. perforation
tables sharing overlapping range grids), a modeler's transcription may
document and fix *one* row-swap (e.g. 105mm at r=100) while missing another
in a sibling shell's table (75mm at r=40 was found still wrong on review —
see `experiment/fragmentation-field/challenges/review.md` finding 1).

**Why:** the modeler checks monotonicity/cross-column invariants (N
decreasing with r; smaller-threshold-table B ≤ larger-threshold-table B)
opportunistically once a swap looks suspicious, not row-by-row across every
table. A single missed swap survives silently — ratios stay wrong but not
enough to flip the verdict, so it's easy to miss without redoing the check.

**How to apply:** whenever a challenge notebook cites this kind of
transcription fix, recompute the monotonicity/cross-column invariants for
*every* row of *every* interleaved table yourself, not just the flagged one —
don't stop once you've confirmed the modeler's own documented fix is right.
