---
name: r50-insensitive-to-steel
description: R50 barely moves with steel gamma (and is non-monotone in it) — a "steel grade does nothing" report is physics, not a bug
metadata:
  type: project
---

Changing the steel `gamma` (or `sigma_f`) moves `N_0` a lot but `R_50` almost
not at all: −38 % on N₀ shifts R₅₀ by ~+2.5 % (98.9 → 101.4 m at M1 geometry).
R₅₀ is even **non-monotone** in γ, with a broad maximum near γ ≈ 45–50 — which
is where the catalogued WDSS-1 (γ = 47) sits, so R₅₀ is *doubly* flat there.

**Why:** lower γ ⇒ fewer fragments but each heavier, so each retains lethal KE
further out. Count and per-fragment reach offset inside `P_kill(r)`.

**Gotcha:** a report that "switching steel grade does nothing to the field" is
expected behaviour, not a wiring defect — check the μ / N₀ / N(>0.5 g) readouts
before hunting a bug. Corollary for presentation: never headline R₅₀ as the
grade discriminator.

Second trap on top of it: `compute_frag_field`'s default `n_r=200` quantises
R₅₀ to 1.50 m steps — the same size as the whole grade effect. Refine the grid
(or interpolate the p=0.5 crossing) before reporting any R₅₀ delta.
See [[hard-step-fraction-grid-aliasing]].

Numbers and derivation:
`experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md` §5 C8.
