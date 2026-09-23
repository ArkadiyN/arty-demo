---
name: finding-token-in-review-prose
description: Writing the literal FINDING+bracket token in review.md prose registers as a malformed marker and fails collect-findings.py and the commit
metadata:
  type: feedback
---

Never write the bare marker token (the word FINDING immediately followed by a
square-bracketed tier) inside `review.md` prose — not even quoted in backticks,
not even as `[...]` placeholder, and not when quoting the collector's own error
output. `src/utils/collect-findings.py` scans for the token textually, reports
it as *malformed*, and returns an error **instead of the scope's register**;
the pre-commit gate then rejects the file.

**Why:** the mandatory first step of every review pass is
`collect-findings.py --for <scope>`. One such token in an earlier pass's prose
makes that step error out for every later pass on that scope — the register
becomes unreadable exactly where deferred findings are supposed to surface.
Observed in `experiment/_smoketest-pendulum/updates/pendulum-period/review.md`
(line 172), which broke the check for two subsequent passes.

**How to apply:** when discussing markers, describe them
("a deferred-findings marker", "the bracketed marker token") rather than
reproducing the literal form. If you must show one, break the adjacency between
the word and the bracket. Re-run the collector after appending your section —
it is the only way to see that you added a new malformed marker.
