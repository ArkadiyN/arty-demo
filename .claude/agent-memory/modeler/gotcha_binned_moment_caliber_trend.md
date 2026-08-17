---
name: gotcha-binned-moment-caliber-trend
description: A per-shell trend in a variance/moment statistic computed over Felix Table 3's 5 mass groups is a binning artefact — refine the mass axis before reading physics off it
metadata:
  type: project
---

A moment statistic (`k = ⟨x²⟩/⟨x⟩²`, and any variance-like quantity) evaluated
with the mass axis collapsed to Felix 2022 Table 3's **5 groups** measures the
discretization error, not the shell. Refining the mass axis against the Mott
spectrum moves `k` from 1.51/1.35/1.21/1.11 to 1.74/1.82/1.91/1.98
(155/105/75/60 mm) — up to **79 % low, and the caliber trend reverses sign**.

**Why:** small shells put 90–96 % of their population inside Group 0, so nearly
all within-group variance is deleted by construction; the apparent trend just
tracks `P(Group 0)`. `c` (a *covariance* between groups) survives the same
binning because the table really does carry between-group `A`-vs-`m` info —
so the `c` precedent does **not** transfer to variance factors.

**How to apply:** before shipping any per-shell moment off that table, run
`experiment/fragmentation-field/updates/breadth-variance-factor-k/checks/k-bin-refinement.py`
(the node-count sweep). Under the model's own `N(≥m)=N₀e^{−√(m/μ)}`, breadth is
exponential, so `k = 2` exactly and scale-free — any caliber spread you see
below that is the `A`-mix, not the caliber. Reasoning:
`.../breadth-variance-factor-k/scoping.md` §3, §6.1.
See also [[gotcha-count-mass-locus-not-identifying]].
