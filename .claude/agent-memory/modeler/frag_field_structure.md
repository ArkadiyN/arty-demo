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
use DIFFERENT `e_axis`: single-zone `_shell_axis = (−cosα,0,−sinα)` (backward),
four-zone `e_axis = (+cosα,0,−sinα)` (forward). Tests also differ: single-zone
`|cosΘ| ≤ sinδ` (θ=90 implicit, equatorial), four-zone `|cosΘ−cosθ^z| ≤ sinδ`.
They AGREE for the equatorial belt (cosθ^z=0 ⇒ |cosΘ|≤sinδ; the x-sign flip is
absorbed by the |·|). The sign only matters for non-equatorial zones, which
exist ONLY in the four-zone path. Don't "fix" the single-zone backward axis —
it's equivalent for θ=90. Full reasoning: `lethal-fragment-density-field/
derivation.md` §5.4. This is what the stuck prior pass was circling.

**E_leth for binary lethal cut = 1000 J** (ES-310 P_k=0.5 anchor), NOT 79 J.
Matches the graded `pk_given_hit` 0.5 point (`_PK_E=[100,1000,4000]`). Recorded
in `lethal-fragment-density-field/derivation.md` §3.
