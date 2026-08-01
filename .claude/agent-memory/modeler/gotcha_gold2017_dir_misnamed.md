---
name: gold2017-dir-misnamed
description: Gold (2017) — the PAFRAG-Mott source for the fragment-mass formula — sits in doc-reference dir "fragment-size-distribution-conwep", easy to conclude it is missing
metadata:
  type: reference
---

The cited "Gold 2017, eq. 16" (PAFRAG-Mott μ formula) **is** in the repo:
`doc-reference/fragmentation/fragment-size-distribution-conwep/1-s2.0-S221491471730079X-main.md`
= Gold, *Fragmentation Model for Large L/D Explosive Fragmentation Warheads*,
Defence Technology 13(4) 300–309. The directory slug mentions neither Gold nor
2017 nor PAFRAG, so a name-based search concludes "not collected" and wrongly
escalates to @librarian. Grep `doc-reference` for a distinctive **equation or
phrase** ("PAFRAG-Mott", "parallelepiped") rather than the author/year.

Its eqs. 1–7 are the load-bearing ones: the shape factor alpha and the
`gamma = alpha^(-2/3) gamma'` substitution — see
[[mott-mu-scale-not-fixable-by-gamma]].
