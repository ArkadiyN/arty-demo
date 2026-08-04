---
name: negative-claim-by-literal-grep
description: A "this figure is not in the source" ruling built on a literal-string grep is unsound against OCR-mangled digits; check the card and unit variants before accepting it
metadata:
  type: feedback
---

A negative existence claim ("the number is not in that source, it traces
elsewhere") backed by `grep <literal digits>` does **not** close. Scanned
`doc-reference/` sources routinely lose one digit of a multi-digit figure to a
symbol — e.g. a velocity printed `27^0 f/s`, invisible to a grep for `2740`.

**Why:** one audit ruled a BRL-126 attribution void on exactly this grep; the
figure was printed three times in the source and the project's own `card.md`
had already resolved the glyph. The real defect was a wrong *category* label
(side spray read as nose spray) plus an inverted companion value — so the
prescribed repair (re-attribute to a different document) would have added a
second error. Detail: `experiment/fragmentation-field/challenges/
source-data-audit/review-void-rulings.md` §3.

**How to apply:** before accepting any "not in the source" ruling —
1. grep the `card.md` and `tables/` next to the source, not just the `<stem>.md`;
2. grep a digit-wildcard / prose anchor ("velocity of the perforating") instead
   of the literal number;
3. check unit variants (ft/s vs m/s) and thousands separators.
Related: [[interleaved-ocr-table-row-check]],
[[gap-closure-check-source-own-confidence]].
