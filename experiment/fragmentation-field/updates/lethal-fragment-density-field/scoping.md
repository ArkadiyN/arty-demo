# Scoping — Lethal-Fragment Density Field (target-independent, arbitrary 3D point)

**Author:** modeler agent
**Date:** 2026-06-20
**Status:** scoping pass — no implementation code
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Aspect:** target-independent lethal-fragment areal density (or count) field at an
arbitrary 3D point `(x, y, z)` in space, for BOTH the single-zone path
(`fragmentation.py: _expected_kills_3d_point`) and the four-zone path
(`zones.py: four_zone_field` / `_four_zone_field_split`).

______________________________________________________________________

## 1 · Problem statement

The app needs a **3D field visualization** plotting a scalar over real spatial
axes `(x downrange, y cross-range, z height above ground)` with colour =
magnitude. The rejected approach mapped `P(kill)` magnitude onto a height axis,
which is dimensionally and physically incoherent: `P(kill)` is a target-coupled
probability (depends on presented area `A_p(γ)` and posture, and on the kill-
probability weighting `pk_given_hit(E)`), and the ground plane is *already* its
natural domain — re-using its magnitude as a height has no physical meaning.

The user wants instead a **target-independent** quantity — "fragments out, target
out" — that genuinely lives in 3D space and can be sampled at any point. This
means: strip both target-coupled factors (`A_p(γ)` *and* `pk_given_hit(E)`) out
of the existing field integrand, and replace the target-coupled weighting with a
**lethality threshold on the fragment itself** (a fragment is counted iff it can
still do lethal damage when it arrives at that point). The result is the number
of *lethal* fragments crossing a unit area at the field point, set only by the
munition, the burst geometry, and air drag.

**What already exists (per prior new-math triage — context, not formula):**

- *Lethal-count logic* (`fragmentation.py`): `min_lethal_mass(s, …)` finds the
  lightest fragment still lethal at slant range `s` by **bisection** on KE;
  `lethal_fragments_at_range` maps it through the Mott CDF `mott_N` to a lethal
  count. This is **target-independent** but currently only a 1D radial total
  (no spatial spreading onto a point, no solid-angle factor).
- *Geometric spreading factor*: both 3D paths multiply a spreading term
  `1 / (2π·s²·2·sinθ·δ)` **into the same expression** as the target-coupled
  factors `A_p(γ)` and `pk_given_hit(E)` (single-zone:
  `fragmentation.py:425`; four-zone: `zones.py:459`, `:561`, `:644`). Isolating
  the spreading factor from those target terms is the gap.

So this aspect is a **recombination**, not new physics: (spreading factor, already
present) × (Mott number density above the lethal-mass threshold, already present)
→ evaluated at an arbitrary 3D point. No new governing equation is introduced.

______________________________________________________________________

## 2 · The precise quantity and its unit

Define the **lethal-fragment areal density** at a field point `P = (x, y, z)`
with the ground at `z = 0` and the burst at `(0, 0, h_b)`:

$$
\\rho_L(P) ;=; \\underbrace{\\frac{1}{2\\pi,s^2,\\cdot,2\\sin\\theta^z,\\delta}}_{\\text{spreading [m}^{-2}\\text{]}}
;\\cdot; \\underbrace{N!\\bigl(m_{\\min}(s)\\bigr)}\_{\\text{lethal count [-]}}
\\qquad\\bigl[\\text{lethal fragments} / \\text{m}^2\\bigr]
$$

where

- `s = ‖P − burst‖ = √(x² + y² + (z − h_b)²)` is the **slant range** from the
  burst to the field point (note: a *true 3D* slant range, not the ground-plane
  `√(x²+y²+h_b²)` the current code uses, because the field point now has its own
  height `z`);
- `θ^z` is the zone spray half-angle and `δ` the spray belt half-width — the
  spreading denominator and the belt-acceptance test (`|cosΘ − cosθ^z| ≤ sinδ`)
  are taken **unchanged** from the existing code, only with the field point's
  own direction replacing the ground-patch direction;
- `N(m_min(s)) = N₀·exp(−√(m_min/μ))` is the Mott count of fragments heavy
  enough to remain lethal at slant range `s` (i.e. mass ≥ `m_min(s)`), with
  `m_min(s)` from the existing `min_lethal_mass` logic. Four-zone: summed over
  zones, `Σ_z N₀^z·exp(−√(m_min(s)/μ^z))`, each with its own belt test.

**Unit:** lethal fragments per square metre, `m⁻²`. (Spreading is `m⁻²`; the
lethal count is dimensionless.)

**Why this is the right scalar.** `ρ_L` is exactly the quantity that, when
multiplied by a target's presented area `A_p` and run through Poisson, *would*
reproduce the existing `N_eff` / `P(kill)` — i.e. it is the field's
target-independent kernel. Removing `A_p(γ)·pk_given_hit(E)` and substituting a
hard lethal-mass cut is the cleanest "fragments out, target out" reduction of
the model already in the codebase. (Note: `pk_given_hit` is a *graded*
target-coupled weighting; replacing it with a binary lethal-mass threshold is
the standard target-independent counterpart — same ES-310 energy basis, just
thresholded rather than graded. See Option ranking §4.)

**Alternative unit, if a volumetric density is preferred:** dividing `ρ_L` by an
assumed belt radial thickness gives `m⁻³`, but that introduces an arbitrary
thickness and is not recommended — areal density `m⁻²` is the physically
meaningful "how many lethal fragments would cross a target-sized patch here"
and needs no extra assumption.

______________________________________________________________________

## 3 · Literature audit

The physics required is **entirely already cited** for this model. No new
references are needed.

| Ingredient                                 | Source already in `doc-reference/`                                                                                                                                                                                                               |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Gurney `V₀`, Mott `μ, N₀`, break-up radius | `fragmentation/` cards + `_governing-equations.qmd` §1–3 (Gold 2017 / PAFRAG, Mott 1947)                                                                                                                                                         |
| Drag retardation `λ(m)`, KE decay          | `_governing-equations.qmd` §4–5 (Driels / Cunniff 2014)                                                                                                                                                                                          |
| Lethal-energy threshold `E_leth`           | `wound-ballistics/fas-es310-damage-criteria` — ES-310 (FAS/Navy 1998). The existing model already uses ES-310 anchors; the binary lethal cut is the ES-310 50%/1 kJ point (or whatever `E_leth` the caller already passes to `min_lethal_mass`). |
| Spreading / solid-angle belt geometry      | `updates/frag-field-3d-geometry/derivation.md` §3.7–3.8 (internal, PASS)                                                                                                                                                                         |

**Decision needed at derivation time (not a literature gap):** which scalar
`E_leth` defines "lethal" for the binary cut. The existing `min_lethal_mass`
takes `E_leth` as a caller-supplied argument; the notebook validation uses 79 J
only as a *bisection test reference*, explicitly "not the model threshold"
(`_validation.qmd:94`). The natural choice is the ES-310 `P_k|hit = 0.5` energy
(1 kJ), making `ρ_L` "density of fragments each ≥50% lethal on a hit." This is a
modelling choice grounded in already-cited ES-310 — **flag it for the derivation
pass to fix explicitly**, do not invent a new value here.

No `## Missing References` — nothing to collect.

______________________________________________________________________

## 4 · Options for defining/computing the field (both paths)

Three orthogonal decisions: **(A) what scalar**, **(B) how to handle the 3D
height axis**, **(C) how to evaluate cheaply**. Ranked within each.

### A · Definition of the scalar

**A1 (recommended) — Lethal-fragment areal density `ρ_L` [m⁻²]**, spreading ×
Mott-count-above-lethal-mass, as in §2. Pros: genuinely target-independent;
reuses both existing pieces unchanged; physically the field's own kernel; same
`m⁻²` units everywhere so colour scale is interpretable. Cons: requires a binary
`E_leth` choice (see §3).

**A2 — Total fragment areal density (no lethality cut) [m⁻²]**, i.e. integrate
the full Mott density `∫n(m)dm = N₀` instead of only `m ≥ m_min`. Pros: needs no
`E_leth`; purest "fragments out." Cons: counts spent, sub-lethal fragments
equally — far-field density never decays to zero, so the visualization would not
show the lethal *reach* the user cares about; loses the drag physics that makes
the field interesting. **Rejected as the primary scalar** but trivial to expose
as a toggle alongside A1 (same code path, skip the `m_min` cut).

**A3 — Lethal kinetic-energy flux [J·m⁻²]**, weight each fragment by its arrival
KE. Pros: also target-independent, smooth. Cons: not a "count," harder to read,
and conflates the threshold with the magnitude. Not recommended.

### B · Handling the height axis `z`

**B1 (recommended) — True 3D slant range.** Use `s = √(x²+y²+(z−h_b)²)` so the
field point's own height enters drag attenuation and inverse-square spreading,
and the belt-acceptance direction `r̂ = (P − burst)/s` uses the 3D vector. This
is the minimal, correct generalisation: the existing ground code is exactly the
`z = 0` slice of it. The spray-belt cone, AoF rotation, and `1/(2π s² · 2 sinθ δ)`
all already work for an arbitrary direction — only the point coordinates change.
Limit check to record in derivation: at `z = 0`, `ρ_L` must reduce to the
existing ground-field integrand with `A_p` and `pk_given_hit` removed.

**B2 — Evaluate ground field then extrude.** Compute the existing 2D field and
copy it up the `z` axis. Rejected: physically wrong (ignores that a point above
the ground is closer to / differently angled from the burst), and reproduces the
rejected "magnitude-on-height" incoherence.

### C · Evaluation strategy (performance — the flagged bottleneck)

The lethal-mass threshold `m_min(s)` is the cost centre. Setting
`E(m)=½m V₀²e^{−2λ(m)s} = E_leth` with `λ(m)=k m^{−1/3}` has **no closed-form
inverse** (m appears both linearly and inside `exp(−2k m^{−1/3}s)`), so it
genuinely needs root-finding. The existing `min_lethal_mass` does ~80 bisection
iterations **per call**. On a dense 3D grid (e.g. 80³ ≈ 5×10⁵ points, ×4 zones)
a naive per-point bisection is ~10⁸ KE evaluations — too slow for an interactive
Streamlit app. **This is a real bottleneck and is flagged here as the user
requested.** It does **not** change the recommended physics (A1+B1); it changes
*how* we evaluate it. Options, cheapest-first:

**C1 (recommended) — Precompute `m_min(s)` on a 1D slant-range grid, then
interpolate.** `m_min` depends *only* on `s` (and per-zone `V₀^z`), not on
direction or `(x,y,z)` separately. So tabulate `m_min(s)` once over a 1D `s`-grid
spanning the field (per zone, since `V₀^z` differs), then every grid point does a
cheap `np.interp`. This collapses the 3D root-finding to one 1D solve of modest
size and makes the field embarrassingly vectorizable. Strongly preferred: it is
both the simplest *and* the fastest, and keeps the exact physics.

**C2 — Vectorize the belt test + spreading + interpolated lookup over the whole
grid** (NumPy broadcasting over the `(x,y,z)` arrays), layered on top of C1.
Removes the Python double/triple loop entirely. Recommended as the
implementation form of C1.

**C3 — Numba JIT the per-point kernel.** A fallback if, after C1+C2, the belt
test or per-zone accumulation is still the cost. Keep in reserve; likely
unnecessary once `m_min` is tabulated.

**C4 — Naive per-point bisection (status quo extended to 3D).** Correct but too
slow for interactive use. Rejected for the app; acceptable only as a
correctness oracle in validation (spot-check that C1's interpolated `m_min`
matches a direct bisection at a handful of points).

The user is open to vectorization / Numba, so the performance concern does not
block the physically-correct option — **recommend A1 + B1 + C1/C2**, with C3 in
reserve and C4 as the validation oracle.

______________________________________________________________________

## 5 · Recommendation

Define the field quantity as the **lethal-fragment areal density `ρ_L(x,y,z)`
[m⁻²]** (Option **A1**), evaluated at the **true 3D slant range** (Option **B1**),
by isolating the already-present geometric spreading factor
`1/(2π s² · 2 sinθ^z δ)` from the target-coupled `A_p(γ)·pk_given_hit(E)` terms
and multiplying it by the already-present Mott lethal-count
`N(m_min(s)) = N₀ exp(−√(m_min(s)/μ))` (four-zone: summed over zones, each with
its own belt-acceptance test and `(V₀^z, μ^z, θ^z)`).

Apply the **same derivation step to both paths** — single-zone
(`_expected_kills_3d_point`) and four-zone (`four_zone_field` /
`_four_zone_field_split`) — since they share the identical spreading kernel and
belt test; this is one aspect, not two.

For performance (Option **C1/C2**): precompute `m_min(s)` on a 1D slant-range
grid per zone and interpolate over the vectorized 3D grid; hold Numba (**C3**) in
reserve and use a direct-bisection spot check (**C4**) as the validation oracle.
Expose the no-lethality-cut total density (**A2**) as a cheap optional toggle
(same code path without the `m_min` cut) if the app wants it.

**Open items to resolve in the derivation pass (do not pre-decide here):**

1. The binary lethal-energy threshold `E_leth` (recommend the ES-310 1 kJ /
   `P_k|hit=0.5` point; confirm against the value the app currently passes to
   `min_lethal_mass`).
1. The exact `z = 0` limit check tying `ρ_L` back to the existing ground-field
   integrand (with `A_p` and `pk_given_hit` divided out).
1. Whether the four-zone belt-acceptance test, written for ground points,
   needs any change for points at `z > 0` (expected: none — it is already a
   3D-direction test — but confirm).
1. Slant-range grid extent/resolution for the `m_min(s)` table such that
   interpolation error stays below the field's display tolerance.

______________________________________________________________________

## 6 · Acceptance / validation checks to run (for later passes)

- **Dimensional:** `ρ_L` in `m⁻²` (spreading `m⁻²` × dimensionless count). ✓ by
  construction.
- **`z = 0` reduction:** `ρ_L(x,y,0)` × `A_p(γ)` × (graded→binary correction)
  reproduces the existing ground `N_eff` structure up to the `pk_given_hit`-vs-
  threshold difference; at minimum the spreading-only part must match the
  current integrand's spreading-only part exactly.
- **Far-field decay:** `ρ_L → 0` as `s → ∞` (drag pushes `m_min` past the
  heaviest fragment → `N(m_min) → 0`). Distinguishes A1 from A2.
- **Belt geometry:** points outside the spray belt (`|cosΘ − cosθ^z| > sinδ`)
  return zero — same guard as the existing field.
- **Interpolation oracle:** C1's interpolated `m_min(s)` agrees with a direct
  `min_lethal_mass(s)` bisection at sampled `s` within tolerance.
- **Single- vs four-zone consistency:** collapsing the four zones to one
  equivalent cylinder recovers the single-zone `ρ_L` within Mott-`μ` tolerance
  (mirrors the existing four-zone derivation §5 self-consistency check).
