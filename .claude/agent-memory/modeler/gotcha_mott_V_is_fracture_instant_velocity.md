---
name: gotcha-mott-V-is-fracture-instant-velocity
description: V in the Mott/Gold x0 formula is the shell velocity at the instant of fracture (not terminal Gurney) — and Mott 1943's own worked example uses the terminal one, which is the trap
metadata:
  type: project
---

`x_0 = sqrt(2σ_F/ργ')·r/V` — the `V` is defined by Gold 2017 immediately before
its eq. (2) as "the velocity with which the shell is moving outwards" **at the
instant of fracture**, and PAFRAG supplies it per segment from a CALE hydrocode.
It is *not* the terminal Gurney velocity, and `r/V` is a reciprocal hoop strain
rate, not a launch condition.

**Why it's easy to get backwards:** Mott/Linfoot 1943's own worked example pairs
the burst radius with "V, the velocity of the fragments, 2500 ft/sec" — i.e. the
terminal value — so the two papers behind one formula disagree on the pairing.
Whether the tabulated γ' absorbs the difference is the double-count question.

Kennedy 1970 is what makes this a live defect for shells rather than a
non-issue: acceleration completes at V/V₀ = 2 for **normal** incidence but 7 for
**grazing** — and an end-fuzed shell is grazing, so Mott's break-up at V/V₀ = 3
sits mid-acceleration.

**How to apply:** any pass touching `mott_params` velocity handling starts from
`experiment/fragmentation-field/updates/breakup-velocity-fraction/scoping.md`
(§2–3 carry the verbatim source quotes and anchors). Do not replace terminal
`gurney_velocity` globally — it is separately validated as the fragment launch
velocity. See [[gotcha-mott-mu-scale-not-fixable-by-gamma]],
[[gotcha-gold2017-dir-misnamed]].
