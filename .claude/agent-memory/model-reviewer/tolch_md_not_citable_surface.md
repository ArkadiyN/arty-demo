---
name: tolch-md-not-citable-surface
description: tolch-1938.md's own card.md bans citing it for any number; a derivation can still lean on it via an internal closure invariant alone, no CSV
metadata:
  type: project
---

`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md`
line 22 states outright: "`tolch-1938.md` is not a citable surface for any
number... a number that has no CSV has no admissible surface in this repo."
Only 4 spray-density tables (pages 40-44) were re-extracted into
`tables/*.csv` + `.invariant`; other numbers on the same page range (e.g. the
weight-row table, "Wt. empty shell & fuze") have no CSV and are still cited
directly from the markdown by check scripts, protected only by an ad-hoc
arithmetic closure written inline (not a `tables/*.invariant`).

**Why it matters:** the card's other tables were shown to have ~20/54
corrupted cells despite passing glyph-level scanning — the ban is not
boilerplate. An inline closure (e.g. `12.50-1.56+2.35=13.29` exact) is real
protection but isn't the CSV gate the rule requires, and doesn't obviously
scope-limit the card's blanket statement.

**How to apply:** any future pass citing a number from `tolch-1938.md` —
check whether it has a `tables/*.csv` backing it. If not, flag as Deferrable
(not Blocking unless the number is load-bearing for a shipped `src/` value)
and point at `experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/review.md`
for the precedent and suggested remedy (extract to CSV, or get a librarian
ruling narrowing the ban's scope).
