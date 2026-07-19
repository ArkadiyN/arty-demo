---
name: revert-probe-use-stash
description: For revert-based verification probes use git stash push/pop, never git checkout -- <file>
metadata:
  type: project
---

`git checkout -- <file>` discards the file's ENTIRE uncommitted working-tree
diff, not just a scratch edit layered on top — if the file under an
empirical probe (e.g. reverting to a pre-fix formula) already carries
uncommitted approved changes, checkout silently reverts past them to HEAD.

Bracket revert-based experiments with `git stash push -- <file>` /
`git stash pop`, and re-diff against the recorded approved diff afterwards
to confirm nothing beyond the intentional probe was undone.
