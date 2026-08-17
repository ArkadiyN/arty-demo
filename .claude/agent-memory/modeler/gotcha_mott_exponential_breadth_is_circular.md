---
name: gotcha-mott-exponential-breadth-is-circular
description: Mott's exponential breadth law (k=2) and the shipped sqrt-exponential mass law are one assumption counted twice; their agreement is vacuous, and Mott 1947's ruled-line MC supersedes both
metadata:
  type: project
---

`⟨x²⟩/⟨x⟩² = 2` looks like independent corroboration between Mott & Linfoot
1943 §3's exponential breadth law and the shipped `N(≥m) = N₀e^{−√(m/μ)}`.
It is not — the mass law is *derived from* that exponential, which 1943
imported from the comminution literature ("the usual law", citing Lienau
1936), not from shell mechanics.

**Why:** Mott's own 1947 release-wave calculation contradicts it — a crack
cannot nucleate inside a neighbour's release zone, so the ruled-line
histogram has zero density below `0.4x₀` where an exponential peaks at 0.

**How to apply:** treat 1947 as primary for any breadth *moment*. Mott's
ruled-line Monte Carlo is fully specified in `rspa.1947.0042.md` pp. 304–305
and reproducible in ~80 lines — reproduce it rather than bounding it from
finding (1)'s prose, which is about `x₀` the release-wave scale, not a
distribution support. Full reasoning and the resulting `k = 1.14`:
`experiment/fragmentation-field/updates/breadth-variance-factor-k/derivation.md`.
