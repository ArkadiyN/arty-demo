---
name: gap-closure-check-source-own-confidence
description: when a derivation claims a literature gap is "closed" by citing two doc-reference entries together, check each entry's own confidence/data-gap section independently — one may flag the exact identification as unconfirmed even though the derivation treats it as settled
metadata:
  type: feedback
---

A derivation can cite two real `doc-reference/` documents side by side (e.g.
"document A names grade X; document B gives grade X's composition") and
present the pair as one sourced fact, when document B's own text explicitly
says the X-identification is unconfirmed/low-confidence, or a third sibling
doc-reference entry (not cited) dedicates itself to flagging exactly that
identification as an open question.

**Why:** name-coincidence linking (e.g. a War-Department internal designation
"WD-X1335" assumed equivalent to modern "AISI 1335" purely because both
contain "1335") is an easy, silent way for a derivation to upgrade an
inference to a "sourced" fact. See
`experiment/fragmentation-field/updates/wdss1-steel-grade/review.md`
(2026-07-25 re-review, finding F5) for the full case and why it stayed
Deferrable (sign-robust) rather than Blocking.

**How to apply:** whenever a derivation states a gap is "closed" via two or
more citations, open each cited doc and its confidence/gaps section, and
`grep` the doc-reference folder for sibling entries discussing the same named
identification that the derivation did *not* cite — a dedicated "is X really
Y" analysis doc is a strong signal the identification is contested.
