---
name: mott-1947-1p5x0-is-not-an-anchor
description: Mott 1947's "average length about 1.5x0" is figure-4 output of his own quadrature at 0.4x0 bins, 1 sig fig — it cannot validate or discriminate ruled-line MC schemes
metadata:
  type: project
---

Mott 1947 `rspa.1947.0042.md` p. 305 finding (1) — greppable anchor
`the average length is about $1.5x_0$` — is **read off figure 4**, a histogram
drawn from Mott's own deterministic `Δσ` ruled-line procedure at `l/x₀ = 20`,
binned at `0.4x₀`, quoted to one significant figure. His p. 306 `0.24 in.`
worked example (anchor `the average fragment length is about 0.24 in.`) carries
no fragment measurement — checked on the page, 2026-08-18.

**Why:** any derivation that scores a ruled-line sampling scheme against "1.5"
is scoring it against the output of *one of the candidates*, at a resolution
(one-fifth of a bin between 1.556 and 1.634) that cannot separate them. Both
defects at once: circular criterion, and precision claimed beyond the source.

**How to apply:** when `κ_x`, `k`, or the Mott/Poisson quadrature choice is
being justified "because it reproduces Mott's reported value", that is a
reproduction check of the MC's *implementation*, not physical validation — say
so. Full argument: `experiment/fragmentation-field/updates/kappa-x-shell-regime/review.md`
Pass 1 finding B1. Related: [[moment-correction-is-spectrum-weighted]].
