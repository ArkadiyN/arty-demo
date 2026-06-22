---
name: frag-field-structure
description: Where the fragmentation-field 3D field code lives and the spreading-vs-target-coupled factor split inside its integrand
metadata:
  type: project
---

Fragmentation-field model (`experiment/fragmentation-field/`). Single-zone 3D
field: `src/arty/fragmentation.py:_expected_kills_3d_point` / `compute_frag_field_3d`.
Four-zone: `src/arty/zones.py:four_zone_field`, `_four_zone_field_split`,
`four_zone_line_split`. Both share the SAME per-point integrand shape:
`pdf · pk_given_hit(E) · A_p(γ) / (2π·s²·2·sinθ^z·δ)`.

**Gotcha for any target-independent quantity:** the geometric spreading factor
`1/(2π s² · 2 sinθ^z δ)` is NOT a separate function — it is written inline,
multiplied together with the two *target-coupled* factors `pk_given_hit(E)`
(graded kill weighting) and `A_p(γ)=presented_area` (presented area) in the same
expression. To get "fragments out, target out" you must divide out BOTH target
factors and replace the graded `pk_given_hit` with a binary lethal-mass cut.

**Lethal-mass logic is root-finding, not closed form.** `min_lethal_mass(s,…)`
bisects (~80 iters) on KE because `E(m)=½m V₀²e^{−2λ(m)s}` with `λ=k m^{−1/3}`
has no closed-form inverse (m both linear and inside the exp). BUT `m_min`
depends only on slant range `s` (per zone `V₀^z`) → tabulate on a 1D `s`-grid
and `np.interp` to vectorize over a dense 3D grid. This is the key perf lever
for an interactive Streamlit field. Full reasoning:
`updates/lethal-fragment-density-field/scoping.md` §4C.

**Lethality threshold source:** ES-310 (FAS/Navy 1998),
`doc-reference/wound-ballistics/fas-es310-damage-criteria`. `E_leth` is a
caller-supplied arg, NOT hard-coded; notebook's 79 J is only a bisection test
reference (`_validation.qmd:94`), explicitly not the model threshold. ES-310
1 kJ = P_k|hit 0.5 is the natural binary cut.

**Mott constant name collision:** `SteelParams.gamma` (Mott material param) is
renamed `γ_M` / `gamma_M` in the 3D notebook to avoid clashing with `γ` =
fragment arrival elevation angle. Watch this in any 3D-geometry derivation.

**Belt-test sign-convention trap (single-zone vs four-zone).** The two paths
use DIFFERENT `e_axis`: legacy single-zone `_shell_axis = (−cosα,0,−sinα)`
(backward), four-zone `e_axis = (+cosα,0,−sinα)` (forward). These are **not**
provably pointwise-equivalent off the `x=0` plane — a partial (x-only) sign
flip is not the same as negating the whole vector, and a hand-checked
off-axis point falsifies the naive "they agree at the equatorial belt"
argument. Do not re-derive or re-assert an analytical equivalence claim here;
the resolved framing is "deliberate standardisation by construction, verified
empirically," not "provably equivalent." The new single-zone
`lethal_density_point` uses a separate `_forward_shell_axis = (+cosα,0,−sinα)`
for this reason; the legacy `_shell_axis`/`_expected_kills_3d_point` pair is
untouched and intentionally not reconciled. Full reasoning + the counterexample:
`lethal-fragment-density-field/derivation.md` §5.4, `review.md`.

**E_leth for binary lethal cut = 1000 J** (ES-310 P_k=0.5 anchor), NOT 79 J.
Matches the graded `pk_given_hit` 0.5 point (`_PK_E=[100,1000,4000]`). Recorded
in `lethal-fragment-density-field/derivation.md` §3.
