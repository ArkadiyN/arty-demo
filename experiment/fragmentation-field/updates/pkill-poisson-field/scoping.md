# Scoping — Point kill-probability field $P_k(x,y,z)$ from lethal-fragment density

**Author:** modeler agent
**Date:** 2026-06-21
**Status:** scoping pass (no derivation, no implementation)
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Aspect:** convert the target-independent lethal-fragment areal density
`ρ_L(x,y,z)` [m⁻²] into a point kill-probability field
`P_k(x,y,z) = 1 − exp(−ρ_L · A_ref)` [-], where `A_ref` is a fixed,
literature-anchored nominal personnel presented area (NOT the live
`presented_area(γ, posture)` output).
**Depends on:** `updates/lethal-fragment-density-field/derivation.md`
(ρ_L kernel; approved + implemented in `src/arty/fragmentation.py:431`
`lethal_density_point` / `compute_lethal_density_field_3d` and the four-zone
counterparts in `zones.py`).
**Drives:** OpenSpec change `pkill-3d-surface-view` — its spec currently reads
"3D volume view of **ρ_L**" and must become "3D volume view of **P_k**" (see §4).

______________________________________________________________________

## 1 · Problem

The app today renders a 3D volume of `ρ_L`, the *target-independent* areal
density of lethal fragments [m⁻²]. That number is hard for a reader to
interpret directly (it is a flux density, not a probability) and its dynamic
range spans orders of magnitude near vs. far from the burst.

We want to present instead a **point kill probability** `P_k(x,y,z)` ∈ \[0,1\]:
"if a single representative person stood at this point, what is the chance at
least one lethal fragment strikes them?" This is a monotone, bounded,
reader-legible transform of `ρ_L` that *replaces* the ρ_L volume in the app.

The transform is the standard Poisson "≥1 lethal hit" expression:

$$
P_k(x,y,z) ;=; 1 - \\exp!\\bigl(-,\\rho_L(x,y,z),\\cdot, A\_\\text{ref}\\bigr)
\\qquad (1)
$$

with `A_ref` [m²] a **fixed** reference presented area standing in for "a
target is present here." The entire modelling content of this aspect is
(a) choosing `A_ref` and (b) confirming `ρ_L` is the right kind of quantity to
feed a Poisson kill probability. Both are settled below; the derivation pass
will only formalise eq. (1), its unit/limit checks, and the validation cases.

This is genuinely **new math** (a new derived quantity `P_k` that no
`src/arty/` function returns), so it routes through derivation → review →
`src/arty/` before the app is rewired — but it is a *thin* transform on top of
the already-implemented ρ_L kernel, not a new field integral.

______________________________________________________________________

## 2 · `A_ref` — options, literature audit, recommendation

`A_ref` must be a single fixed scalar [m²]. It is the presented silhouette of a
**nominal** person — deliberately posture- and geometry-independent, because the
whole point of `P_k` is to ignore target size/orientation and ask only "how
lethal is the *field* at this point." It must NOT be `presented_area(γ, posture)`
(that varies with arrival angle and posture — exactly what we are abstracting
away).

### Literature audit (bounded — `doc-reference/` + target-area-profile derivation)

- **`presented_area(γ, posture)` in `src/arty/fragmentation.py:190`** uses the
  NATO "man-as-box" silhouette `A_p(γ) = w_⊥(h cosγ + d sinγ)`. Its parameter
  table (`updates/target-area-profile/derivation.md` §5.1) gives a **standing
  frontal area `A_f = w_⊥·h = 0.5 × 1.7 = 0.85 m²`** and a prone overhead area
  `0.90 m²`. That derivation explicitly notes (§5.1 note) `0.85 m²` "matches
  commonly quoted values for the frontal silhouette of an upright soldier
  without kit," and flags real silhouettes (helmet/armour/kit) as 10–25% larger
  → treat 0.85 as a *lower bound*.
- **Source provenance is already disclosed and audited.** The same derivation
  (§5.2 + §5 preamble) records that the canonical primary sources — **Cunniff
  (2014)** and **AEP-55 Vol. 3** — were checked against `doc-reference/`. Both
  documents ARE collected (`doc-reference/wound-ballistics/cunniff-2014/`,
  `.../aep-55-vol3/`), but **neither contains a single quotable nominal
  personnel presented-area scalar**: Cunniff's areas are *fragment* presented
  areas (Ap/m PDFs, Figure 3) and a human *phantom geometry* (Figure 7), not a
  ready-made silhouette number; AEP-55 Vol. 3 covers occupant survivability /
  vehicle Vulnerable Area, not a man-silhouette scalar. So the `0.85 m²` value
  remains an **engineering convention**, not a primary-literature citation —
  this is the same disclosure status the model already carries for posture
  areas.

### Options

| #      | `A_ref`                                       | Provenance                                 | Pro                                                                                                                            | Con                                                                               |
| ------ | --------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **R1** | **0.85 m² (standing frontal `A_f`)**          | NATO box-body convention, already in model | Internally consistent with `presented_area` at γ=0, standing; one number readers already see elsewhere; documented lower bound | Not a primary citation; standing-frontal is one specific orientation              |
| R2     | ~0.5–0.6 m² ("mean over orientation/posture") | Would need a new averaging argument        | Arguably more "nominal" (averages standing/prone/oblique)                                                                      | Invents a new derived value; no source; harder to defend than just picking a face |
| R3     | 1.0 m² (round "unit man")                     | Convention in some quick-kill nomograms    | Memorable, conservative-ish                                                                                                    | Untraceable to this model's own geometry; arbitrary                               |

### Recommendation — **R1: `A_ref = 0.85 m²`**

Use the standing frontal silhouette `A_f = w_⊥·h = 0.85 m²` already defined in
`src/arty/fragmentation.py` posture params. Rationale:

1. **Consistency.** It is `presented_area(γ=0, standing)` — the model's own
   geometry evaluated at the canonical "fragment arrives horizontally at a
   standing man" condition. No new constant is invented; we reuse an existing
   documented value as a *fixed scalar* (the abstraction is "freeze it," not
   "replace it with something foreign").
1. **Interpretability.** "Standing soldier, frontal" is the natural mental
   model for a kill-probability map and the easiest caption to defend.
1. **Honest provenance.** It inherits the model's existing, already-reviewed
   "engineering convention, primary source not a quotable scalar" disclosure —
   no new unsourced claim is introduced.

Implementation note for the derivation/src pass: expose `A_ref` as a **named
module constant** (e.g. `A_REF_DEFAULT = 0.85` [m²]) and as a function argument
with that default, so it is one fixed value but overridable — NOT a call into
`presented_area(...)`. Carry the "lower bound; real silhouette +10–25% with
kit" caveat into the `P_k` docstring and the app caption.

______________________________________________________________________

## 3 · Binary lethal-mass cutoff vs. Poisson kill probability

**Question (from the brief):** `ρ_L` uses a *binary* lethal-mass cut
(`𝟙[m ≥ m_min(s)]` integrated against the Mott pdf — see
`updates/lethal-fragment-density-field/derivation.md` §1, eq. (3), and
`E_LETH_DEFAULT = 1000 J` at `fragmentation.py:403`). The target-coupled path
instead uses the *graded* `pk_given_hit(E)` weighting. Is the binary-cut `ρ_L`
the right input for a Poisson `P_k = 1 − exp(−ρ_L·A_ref)`?

**Answer — yes, the binary cut is exactly the self-consistent choice; do NOT
mix in the graded weighting here.** Reasoning:

- The Poisson "≥1 event" form `1 − e^{−λ}` requires `λ` to be the **expected
  number of qualifying events** — here, the expected number of fragments that
  both (a) strike the `A_ref` silhouette and (b) are individually lethal. That
  is precisely `ρ_L · A_ref` *when `ρ_L` counts only lethal fragments*, i.e.
  with a **binary** "is this fragment lethal" indicator. `ρ_L` already does
  this: it is a count density of fragments past the lethal-mass threshold.
- Folding the **graded** `pk_given_hit(E)` into `ρ_L` and *then* exponentiating
  would be a category error / double-counting: `pk_given_hit` is itself already
  a per-hit kill *probability* (a Bernoulli weight), so
  `1 − exp(−Σ pk_given_hit)` would be "probability of ≥1 *of a Poisson number
  of already-probabilistic kills*," conflating the hit-count distribution with
  the per-hit lethality. The clean decomposition is: **Poisson hit count ×
  per-hit lethality**, and the binary cut pushes all the per-hit lethality into
  the membership test (lethal / not lethal), leaving `ρ_L·A_ref` a pure
  expected lethal-hit *count*. That is the standard Cookson/ES-310-style
  "expected lethal hits → 1 − e^{−n}" casualty expression (the ES-310
  expected-hits formula `N_hits = N₀·A/(4πδs²)` at
  `doc-reference/wound-ballistics/fas-es310-damage-criteria` §"Expected fragment
  hits" is exactly this shape with a frontal area `A`).
- The two paths therefore *should* differ: the existing target-coupled field
  uses graded `pk_given_hit` because it computes an **expected-kills integral**
  (a sum of per-hit kill weights, not exponentiated); the new `P_k` field uses
  the binary `ρ_L` because it computes a **probability of ≥1 lethal hit** (a
  Poisson tail). Each is internally consistent; combining them would not be.

**Recommendation:** keep `ρ_L` exactly as implemented (binary `m_min` cut,
`E_LETH_DEFAULT = 1000 J`) and apply eq. (1) on top unchanged. The derivation
pass should state this Poisson-independence assumption explicitly (fragments
arrive independently; arrivals on `A_ref` are Poisson with mean `ρ_L·A_ref`;
"lethal" is the binary membership already baked into `ρ_L`) and note its two
standard limitations as model caveats, NOT defects:

1. **Independence / no shielding** — overlapping fragments, body armour, and
   spatial correlation of the spray are ignored; the Poisson form is the
   conventional first-order casualty model.
1. **Sharp lethality threshold** — the binary 1000 J cut discards the soft
   transition the graded `pk_given_hit` captures. This is the deliberate
   simplification that makes `ρ_L` a clean Poisson rate; flag it so a reader
   knows `P_k` is "P(≥1 fragment above the lethal-energy threshold strikes a
   0.85 m² silhouette)," not a tissue-level wound model.

No physics defect here — the binary cut and the Poisson reading are the
*matched* pair.

______________________________________________________________________

## 4 · OpenSpec / app impact (note only — not this pass's work)

The existing change `openspec/changes/pkill-3d-surface-view/` and its spec
`specs/lethal-density-3d-view/spec.md` currently specify a **3D volume view of
ρ_L**. With this aspect, that requirement must be restated as a **3D volume
view of `P_k`**:

- Requirement "App shows an interactive 3D volume view of ρ_L" →
  "...of `P_k`," rendering `1 − exp(−ρ_L·A_ref)` over the (x,y,z) grid.
- The colour scale becomes a bounded [0,1] probability (legible advantage over
  the multi-decade ρ_L scale) — design.md's trace-type tuning likely still
  applies but the value range/colourbar caption changes.
- The "reuses existing per-z ρ_L functions, no new physics" requirement is
  superseded: `P_k` IS new math (eq. 1 + `A_ref`), so it lives in `src/arty/`
  as a new function wrapping the existing ρ_L grid builders. The spec's
  "no new physical quantity" clause must be relaxed to "the `P_k` transform of
  the existing ρ_L grid," pointing at this `pkill-poisson-field` derivation.
- The z=0-slice numerical-identity scenario should be re-expressed against the
  `P_k` 2D field (still derivable from the same ρ_L slice).

This spec edit is for the main agent to drive through the normal OpenSpec
flow **after** derivation → review → `src/arty/`; recorded here only so the
dependency is not lost.

______________________________________________________________________

## 5 · @librarian needed?

**No.** A representative personnel presented area (`A_ref = 0.85 m²`) already
exists in the model and in `updates/target-area-profile/derivation.md`, with
its provenance already audited against `doc-reference/` (Cunniff 2014 and
AEP-55 Vol. 3 are collected but contain no quotable man-silhouette scalar; the
value stays an engineering convention). No new external lookup is required for
this aspect. If the project later wants to *upgrade* `A_ref` from engineering
convention to a primary-source citation, that is a separate, optional librarian
task (find a quotable standing-soldier silhouette area in a primary casualty-
modelling reference) — not a blocker for this `P_k` work.

______________________________________________________________________

## 6 · Recommendation summary (for the derivation pass)

1. `P_k(x,y,z) = 1 − exp(−ρ_L·A_ref)`, eq. (1), with **`A_ref = 0.85 m²`**
   (standing frontal `A_f`) as a fixed, overridable module constant — never a
   live `presented_area(...)` call.
1. Feed the **binary-cut `ρ_L`** exactly as implemented; do **not** reintroduce
   the graded `pk_given_hit`. State the Poisson-independence + sharp-threshold
   assumptions as caveats.
1. New `src/arty/` function wraps the existing ρ_L grid builders
   (`compute_lethal_density_field_3d` / `compute_lethal_density_volume_3d` and
   the four-zone equivalents) and maps them through eq. (1); no change to the
   ρ_L kernel itself.
1. Validation cases for the derivation: `ρ_L→0 ⇒ P_k→0`; `ρ_L→∞ ⇒ P_k→1`;
   `P_k ∈ [0,1]` everywhere; monotone increasing in `ρ_L`; small-`ρ_L`
   linearisation `P_k ≈ ρ_L·A_ref` matches the expected lethal-hit count; z=0
   `P_k` slice consistent with the 2D ρ_L slice through eq. (1).
1. OpenSpec change `pkill-3d-surface-view` spec must shift ρ_L → `P_k` (§4) —
   main-agent task after src/.
