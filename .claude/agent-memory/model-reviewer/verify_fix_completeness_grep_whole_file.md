---
name: verify-fix-completeness-grep-whole-file
description: when re-checking that a previously-flagged wording/finding fix was applied, grep the whole file (and sibling files) for the flagged phrase and any new forward-reference the fix introduces — a fix often lands at the headline location but leaves stale echoes elsewhere
metadata:
  type: feedback
---

A dispatched "apply this wording correction" pass tends to fix the one
location it was pointed at (e.g. a derivation's source-list header) but leave
the same overstated language standing in a later section (a "Checks" or
"Ordering" paragraph) that draws the same conclusion in different words. Worse,
the fix can introduce a **new forward reference** ("see A8") to a numbered
assumption-log entry that never actually gets written — the reference appears
in multiple files (derivation, scoping, and the shipped code comment) while
the target section stops at A7.

**Why:** the review checklist's "source attribution" and "limitations" items
ask whether the *document* is internally consistent, not just whether the one
cited line changed. See
`experiment/fragmentation-field/updates/wdss1-steel-grade/review.md`
(2026-07-25 src/ pass review, finding F12) for the full case — three files
referenced a nonexistent "A8", and the derivation's own C3 still said
"no longer an assumption" after the header above it had been corrected.

**How to apply:** after confirming a flagged phrase was fixed at its cited
line, `grep -rn` the whole aspect folder (+ the shipped `src/` file) for (a)
the original flagged phrase/keyword and (b) any new anchor/entry-number the
fix introduces, to confirm every echo was updated and every new reference
resolves to real content.
