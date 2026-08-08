---
name: gotcha-rebaseline-onto-validation-source
description: Rebaselining a shell's parameters onto the same source you validate against makes the cross-check tautological — prefer an independent basis that agrees
metadata:
  type: project
---

Do not rebaseline a registry entry's parameters onto the *same* source the
model is validated against, if an independent basis exists that lands inside
the fidelity bar.

**Why:** the "does M_case match the source?" check then holds by construction
and carries zero information. The 75 mm M48 case went the other way: a
production basis assembled from TM-9-1904 + TM-9-1901 (numbers Tolch 1938
never saw) reproduced Tolch's independently-stated case metal to 0.37 %,
turning a tautology into real corroboration of both sources. See
`experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/derivation.md`
§1–2.

**How to apply:** when a scoping pass recommends "rebaseline everything onto
the validation dataset", check first whether a disjoint source chain gets you
there too. Also watch the second-order trap: near-identical numbers can differ
entirely in *provenance* quality (variants D and E there differ by 18 g but
only one has a traceable fuze+booster decomposition).

Related: [[gotcha_n0_insensitive_to_case_mass]] — N0 barely moves across a
16 % case-mass change, so never validate such a fix on fragment counts.
