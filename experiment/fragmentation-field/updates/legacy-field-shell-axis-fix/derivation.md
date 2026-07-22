# Derivation — Legacy single-zone field forward shell-axis fix

Implements `scoping.md` §5 **Option A**: repoint the single-zone (legacy) 3-D
fragmentation kernel from the backward axis `ê_b = (−cosα, 0, −sinα)` to the
shared **forward** axis `ê_f = (+cosα, 0, −sinα)`. This doc gives the exact
corrected formulas at the four coupled spots, proves vec≡point and the reduction
to current behaviour on `x=0` / `AoF=90°`, and records the worked limit checks.
Scoping settled the problem, the option ranking, and that Option A is correct —
not re-argued here.

Symbols: `α` angle of fall [rad]; `δ` spray-belt half-width [rad]; `(x,y)` ground
column [m]; `ζ = z − h_b` [m]; `s = √(x²+y²+ζ²)` slant range [m]; `Θ` polar angle
from the shell axis to the field direction; `cosθ^z ∈ {0}` for the single equatorial
belt.

## 1 · The forward-axis single-zone kernel

The belt polar cosine is `cosΘ = r̂ · ê`, `r̂ = (x, y, ζ)/s`. With `ê_f`:

$$\cos\Theta_f = \frac{x\cos\alpha - \zeta\sin\alpha}{s},\qquad \zeta = z-h_b. \quad (1)$$

The belt-membership gate is unchanged: `|cosΘ_f − cosθ^z| ≤ sinδ`, i.e.
`|cosΘ_f| ≤ sinδ` for the equatorial belt `cosθ^z = 0`. Everything else in the
graded Family-A kernel (`A_p(γ)·pk_given_hit(E)/(2π s²·2 sinΘ·δ)`, the `z_rep`
relocation, the mass integral) is untouched — **only the axis on which `cosΘ` and
the belt breakpoints are evaluated moves.**

The belt machinery (`belt_column_breakpoints` / `_belt_breakpoints_vec` /
`_belt_column_zrep_vec`) is already written forward-native: internally
`B = −2x cosα sinα` and, at `_belt_column_zrep_vec:775`,
`cos_Theta = (xb cosα − dz sinα)/s` — exactly eq. (1) with `xb = x_axis`. So the
forward axis is obtained by feeding the **true** `x` (`x_axis = +x`, or the
default `None`), not `−x`. This is the crux the scoping/memory flag: passing
`x_axis = −x` faithfully reproduces the *backward* membership — correct code for
a wrong axis. The four corrected spots (all in `fragmentation.py`):

| # | Spot (line) | Backward (current) | **Forward (fix)** |
|---|---|---|---|
| A1 | `_expected_kills_3d_vec` belt call (1024) | `x_axis=-x_g` | `x_axis=x_g` |
| A2 | `_expected_kills_3d_vec` inline cosΘ (1036) | `(-x_g*cA - dz*sA)/s_safe` | `(x_g*cA - dz*sA)/s_safe` |
| A3 | `_expected_kills_3d_point` belt call (940) | `x_axis=np.array([-x_g])` | `x_axis=np.array([x_g])` |
| A4 | `_expected_kills_3d_point` feet-lit branch (959) | `_shell_axis(alpha_rad)` | `_forward_shell_axis(alpha_rad)` |

`cA=cos α`, `sA=sin α`. The dead backward constructor `_shell_axis`
(`fragmentation.py:381`, zero callers after A4) is deleted. All four spots must
flip **together** — flipping a subset splits the membership axis from the `cosΘ`
axis and produces an inconsistent field (see §2 vec≡point).

Feet-lit branch note (A4): `_forward_shell_axis(α) = (cosα, 0, −sinα)`, and
`r̂·ê_f = (x cosα + y·0 − ζ sinα)/s = (x cosα − ζ sinα)/s`, matching eq. (1). The
`y`-component of the axis is zero, so `y` never enters `cosΘ` — it enters only
through `s`.

## 2 · vec ≡ point, and reduction to current on x=0 / AoF=90°

**vec ≡ point (under the corrected convention).** After the fix both paths build
the belt geometry with `x_axis = +x` (A1/A3 identical), so `z_rep`, `lit`, `s`,
`γ`, `Ap` and the mass integral coincide as before. The only per-point difference
is the `cosΘ` expression on the feet-lit branch: vec computes
`(x cosα − ζ sinα)/s` (A2), point computes `r̂ · ê_f` (A4). Since the axis `y`-term
is zero these are the **same scalar**, `(x cosα − ζ sinα)/s`, so `sinΘ` — hence the
geometry factor — is bit-identical between paths. The pre-existing vec≡point
equivalence therefore carries over unchanged; both flip together.

**Slant range is flip-invariant.** In every path `s` depends on `x` only through
`x²` (`s = √(x²+y²+ζ²)`), so `x_axis = ±x` leaves `s`, and with it the drag
attenuation `V0 e^{−λs}`, `1/s²`, and `γ = arcsin((h_b−z_rep)/s)`, unchanged. The
flip moves **only which columns are belt-lit and the sign of the `x cosα` term in
`cosΘ`** — i.e. which *side* of the burst the down-range lobe sits on, never its
radial magnitude. This is the scoping "bounded blast radius" argument.

**Reduction on x=0.** At `x=0`, eq. (1) gives `cosΘ_f = −ζ sinα/s`, and the
backward axis gives `cosΘ_b = (−0·cosα − ζ sinα)/s = −ζ sinα/s`. Identical: the
`x cosα` term that distinguishes the conventions vanishes. Also `B = −2x cosα sinα
= 0`, so the belt breakpoints coincide. Hence the whole cross-range (`x=0`) slice
is **unchanged** — this is why `compute_frag_field_3d`'s `r50_cross` (read at
`x=0`) and its `50 ≤ r50 ≤ 200` range tests are invariant.

**Reduction at AoF=90°.** At `α = 90°`, `cosα = 0`, so both conventions give
`cosΘ = −ζ·1/s` and `B = 0` for **all** `x`. The field is identical everywhere,
which is exactly why the backward sign survived every `AoF=90°` regression test
(the standing config in `test_familyA_false_safe_zone.py`).

## 3 · Worked unit / limit checks (scoping §5 step 3)

Reference config `h_b = 8 m, AoF = 40°, δ = 30°`, standing target, on the `y=0`
line. Belt centre (where `cosΘ_f = 0`) is `ζ/x = cotα`, projecting to
`x = −h_b tanα = −8·tan40° = −6.71 m` on the ground. Numerically verified with a
standalone forward reference kernel (belt geometry with `x_axis=+x`, eq. (1)
inline cosΘ, `_forward_shell_axis` feet-lit) against the shipped backward kernel
and `four_zone_field`; results:

| Check | Result | Verdict |
|---|---|---|
| Direction flip | backward lit `x∈[+2, +21]`; **forward lit `x∈[−21, −2]`** (all x<0) | PASS — lobe moved to the backward-ground side |
| Belt-centre coincidence | single-zone belt centre `x=−6.71 m` lies inside the four-zone lit band `x∈[−21.5, +0.5]` (negative side) | PASS — same side as four-zone equatorial lobe |
| `r50_cross` invariance | max\|N_fwd − N_bwd\| on the `x=0` cross-range slice `= 4.4e−16` | PASS — machine zero, R₅₀ unchanged |
| AoF=90° invariance | max\|N_fwd − N_bwd\| at `α=90°` `= 8.9e−16` | PASS — sign-blind, as predicted |
| Exact mirror | `N_fwd(x) = N_bwd(−x)` to `0.0` | PASS — confirms a pure `x→−x` reflection |
| Diff-map co-location | forward single-zone lit `[−21,−2]` **overlaps** four-zone `[−21.5,+0.5]`; backward `[+2,+21]` was **disjoint** from it | PASS — diff becomes overlapping attribution, not a mirror sum |

Diff-map note: the "Four-zone − Single-zone" map is not identically zero on the
equatorial belt (four-zone carries four belts with distinct per-zone
`N0,μ,V0`, so magnitudes differ), but the fix converts it from a **disjoint sum of
two mirror-opposite lobes** (off-axis garbage, `_limitations.qmd` #12) into a
**co-located per-zone residual** — the clean attribution the feature intends.
That directional recovery, not numerical nullity, is the acceptance bar.

## 4 · Test-rewrite reference (scoping §3, for the implementation pass)

`test_offaxis_single_zone_axis_sign` + `_ref_relocated_single_offaxis` currently
pin the **backward** axis and probe `x<0` points, enforcing the bug. Rewrite to
the forward convention, preserving the wrong-sign-catching intent (must probe
`AoF≠90°` and the now-lit region).

**Forward reference formula** for `_ref_relocated_single_offaxis` (brute column
scan, no `belt_column_breakpoints`):

```
zs = linspace(0, posture.h, nz); dz = zs - h_b; s = sqrt(x² + y² + dz²)
cosT = (x*cos(α) - dz*sin(α)) / s            # FORWARD axis, eq. (1)
active = |cosT| <= sin(δ)                     # equatorial belt gate
j = first active index (lowest column height); z_rep = zs[j]; sj = s[j]
sinT = sqrt(max(0, 1 - cosT[j]²))
gamma = arcsin(clip((h_b - z_rep)/sj, -1, 1)); Ap = presented_area(gamma, posture)
E = 0.5*m_grid*(V0*exp(-lam*sj))²
return trapezoid(pdf * pk_given_hit(E) * Ap / (2π sj² · 2 sinT · δ), m_grid)
```

The only change from the current helper is the `cosT` sign:
`-(x cosα + dz sinα)/s → (x cosα − dz sinα)/s`.

**Probe points** must move to the lit (backward-ground, `x<0`) region and keep
`AoF≠90°` so `B≠0` makes a wrong `+x`/backward sign detectable. Suggested:
`AoF=60°, δ=15°`, points e.g. `(−3,1), (−5,0.5), (−2,2), (−6,0), (−4,−1.5)`
(the current test's points already sit at `x<0`; under the forward fix these lie
in the lit lobe, so the same points work — only the reference `cosT` sign flips).
A wrong-sign (backward, or unflipped `x_axis`) implementation would relocate
`z_rep` to the mirror column and disagree in both lit/unlit membership and
magnitude, exactly as the current test catches for the opposite sign.

## 5 · Assumptions / scope

- Straight-line rays only (inherited; unchanged by this aspect).
- The off-belt `sinΘ`-normalisation residual vs ρ_L (`_limitations.qmd` #12, the
  separate `1/sin(90°−δ)` note) is **unrelated to the axis** and stays as a logged
  limitation — out of scope here.
- `_limitations.qmd` #12 axis/diff-map bullets and the modeler memory
  `shell-axis-sign-convention` are updated by the implementation pass (§3 scoping).

**Fidelity target (inherited from scoping):** drives the "2D Fragmentation Field"
P(kill) heatmap and the "Four-zone − Single-zone" diff map. Hard *directional* bar
— single-zone down-range lobe must sit on the same side as the four-zone
equatorial lobe (met: both on `x<0`); `r50_cross` magnitude unchanged (met:
machine-zero on `x=0`).
