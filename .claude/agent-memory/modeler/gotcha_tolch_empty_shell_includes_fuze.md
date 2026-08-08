---
name: gotcha-tolch-empty-shell-includes-fuze
description: Tolch 1938's "Wt. empty shell & fuze" 13.29 lb is NOT case metal (10.94 lb is); its count percentages are also referenced to the fuzed weight
metadata:
  type: project
---

Tolch 1938's weight row (grep `"Pit Fragmentation Tests of 75 mm T3 Shell from 75 mm"`)
tabulates *loaded unfuzed* 12.50 lb, *fuze M39* 2.35, *TNT* 1.56, *empty shell
& fuze* 13.29. Case metal = 12.50 − 1.56 = **10.94 lb (4962 g)**. The 13.29 lb
figure includes the fuze and has been misread as case mass in at least three
committed artifacts.

**Why it keeps happening:** "empty shell" reads like bare case; the fuze is
added, not removed, by that row. The closure 12.50 − 1.56 + 2.35 = 13.29 is
what disambiguates it.

**How to apply:** use 10.94 lb for `M_case` (Gurney C/M, Mott `mu`, `N0`).
But do *not* then compare `N0` to Tolch's raw pit counts — his recovery
percentages and 60%-test are referenced to the fuzed 13.29 lb, and screen-1
fragments "are mostly pieces of fuze" (~15% of recovered weight). Full analysis
and options: `experiment/fragmentation-field/updates/shell-case-mass-basis/scoping.md`.

Related: [[gotcha-tolch-remaining-velocity-is-shell-not-fragment]].
