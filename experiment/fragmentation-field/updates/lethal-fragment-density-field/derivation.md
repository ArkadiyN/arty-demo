# Derivation — Lethal-Fragment Density Field (target-independent, arbitrary 3D point)

**Author:** modeler agent
**Date:** 2026-06-20
**Status:** derivation pass — no implementation code (derivation.md only)
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Scoping:** `updates/lethal-fragment-density-field/scoping.md` (approved; options
A1 + B1 + C1/C2 fixed there — not re-litigated here)
**Aspect:** target-independent lethal-fragment areal density `ρ_L(x,y,z)` [m⁻²]
at an arbitrary 3D point, for BOTH the single-zone path
(`fragmentation.py:_expected_kills_3d_point`) and the four-zone path
(`zones.py:four_zone_field` / `_four_zone_field_split`).

This pass produces the exact equations, fixes the four open items scoping.md §5
listed, and runs the §6 validation checklist on paper. **No `src/arty/` edits.**

______________________________________________________________________

## 1 · Quantity and governing equation

Burst at `B = (0, 0, h_b)`, ground at `z = 0`, field point `P = (x, y, z)`.

**True 3D slant range (Option B1):**

$$
s ;=; \\lVert P - B\\rVert ;=; \\sqrt{x^2 + y^2 + (z - h_b)^2}
\\qquad (1)
$$

**Unit ray** from burst to field point:

$$
\\hat r ;=; \\frac{P - B}{s} ;=; \\frac{(x,; y,; z - h_b)}{s}
\\qquad (2)
$$

**Lethal-fragment areal density** (Option A1), per zone `z`, summed over zones:

$$
\\rho_L(P) ;=; \\sum\_{z},
\\mathbb{1}!\\bigl[,\\lvert\\cos\\Theta_z - \\cos\\theta^z\\rvert \\le \\sin\\delta,\\bigr];
\\underbrace{\\frac{1}{2\\pi s^2,\\cdot,2\\sin\\theta^z,\\delta}}_{\\text{spreading } g^z(s);[\\text{m}^{-2}]}
;\\cdot;
\\underbrace{N_0^z,\\exp!\\Bigl(-\\sqrt{m_{\\min}^z(s)/\\mu^z}\\Bigr)}\_{\\text{lethal count } N^z(s);[-]}
\\qquad (3)
$$

with the belt-acceptance polar angle

$$
\\cos\\Theta_z ;=; \\hat r \\cdot \\hat e\_{\\text{axis}}
\\qquad (4)
$$

and `m_min^z(s)` the lightest fragment still lethal at slant range `s` for that
zone (Section 2). The single-zone path is the special case of (3) with one zone,
`θ = 90°` (equatorial cylinder), `(N_0, μ, V_0)` the single-cylinder values, and
the equatorial belt test (Section 5.4).

**Unit:** lethal fragments per square metre, **m⁻²**.

This is exactly the existing field integrand with the two **target-coupled**
factors divided out — `A_p(γ)` [m²] removed, and the **graded** `pk_given_hit(E)`
weighting replaced by a **binary** mass cut `𝟙[m ≥ m_min(s)]` integrated against
the Mott pdf. Both target factors are sourced inline at `fragmentation.py:425`
and `zones.py:459/561/644`; the spreading factor `1/(2π s² · 2 sinθ^z δ)` is **not**
a separate helper — it is written together with `A_p` and `pk_given_hit`, so
isolating it is the entire content of this aspect (memory: `frag-field-structure`).

### Symbols

| Symbol       | Meaning                                                 | Unit |
| ------------ | ------------------------------------------------------- | ---- |
| `s`          | true 3D slant range burst→field point, eq. (1)          | m    |
| `ĥr`         | unit ray burst→field point, eq. (2)                     | –    |
| `ê_axis`     | forward shell axis in ground frame (per path, §5.4)     | –    |
| `Θ_z`        | polar angle of `ĥr` from shell axis, eq. (4)            | rad  |
| `θ^z`        | zone spray angle from forward axis (`spray_deg`)        | rad  |
| `δ`          | spray-belt half-width (`spray_half_angle`, `delta_deg`) | rad  |
| `N_0^z`      | zone total fragment count `= M^z/(2μ^z)`                | –    |
| `μ^z`        | zone Mott half-mass                                     | kg   |
| `V_0^z`      | zone initial fragment velocity                          | m/s  |
| `m_min^z(s)` | minimum lethal fragment mass at range `s`, §2           | kg   |
| `E_leth`     | binary lethal kinetic-energy threshold, §3              | J    |
| `λ(m)`       | drag retardation coefficient `= k m^{-1/3}`             | m⁻¹  |
| `ρ_L`        | lethal-fragment areal density, eq. (3)                  | m⁻²  |

______________________________________________________________________

## 2 · The lethal count `N^z(s)` and `m_min^z(s)`

`m_min^z(s)` solves, for fragment mass `m`,

$$
E^z(m, s) ;=; \\tfrac12, m, \\bigl(V_0^z, e^{-\\lambda(m),s}\\bigr)^2 ;=; E\_{\\text{leth}},
\\qquad \\lambda(m) = k,m^{-1/3}
\\qquad (5)
$$

with `k = ρ_air C_D C_shape / (2 ρ_steel^{2/3})` (`retardation_coeff`,
`fragmentation.py:180`). Eq. (5) has **no closed-form inverse** — `m` appears
both linearly (in `½m`) and inside `exp(−2k m^{−1/3} s)` — so root-finding is
genuinely required; `min_lethal_mass` bisects ~80 iterations. The Mott
cumulative count of fragments with `m ≥ m_min` is

$$
N^z(s) ;=; \\int\_{m\_{\\min}^z(s)}^{\\infty} n^z(m),dm
;=; N_0^z,\\exp!\\Bigl(-\\sqrt{m\_{\\min}^z(s)/\\mu^z}\\Bigr) ;=; \\texttt{mott_N}(m\_{\\min}, N_0^z, \\mu^z)
\\qquad (6)
$$

since the Mott pdf `n(m) = N_0/(2√(μ m)) · exp(−√(m/μ))` integrates to the
survival function `N_0 exp(−√(m/μ))` (`mott_N`, `fragmentation.py:207`). Both
`min_lethal_mass` and `mott_N` already exist and are reused unchanged.

**Edge behaviour of `m_min` (from `min_lethal_mass`):**

- `m_min = m_hi` (default 2 kg) when even the heaviest fragment is sub-lethal at
  `s` → `N^z = N_0 exp(−√(2/μ)) ≈ 0` (drives far-field decay, §5.3).
- `m_min = m_lo` (1e-6 kg) only if even the lightest fragment is lethal at `s`,
  i.e. `½ m_lo (V_0 e^{−λ s})² ≥ E_leth`. **For the default shell this branch is
  unreachable:** with `V_0 ≈ 995 m/s` (TNT, `mass_shell = 12.04 kg`), even at
  `s→0` (no drag) `½·m_lo·V_0² ≈ 0.49 J`, four orders of magnitude below
  `E_leth = 1000 J`. So near the burst `m_min(s)` is **not** clipped to `m_lo`;
  it is solved by bisection and varies smoothly (a genuinely varying, not flat,
  value) all the way down to `s_min`. The `m_lo` clip exists in
  `min_lethal_mass` for robustness but is essentially never hit at this shell's
  `(V_0, E_leth)`. Consequently there is **no flat near-burst plateau** to lean
  on in §6 — `m_min(s)` rises monotonically from `s_min` and only saturates at
  the far end (`→ m_hi`).

______________________________________________________________________

## 3 · Open item 1 — the binary lethal-energy threshold `E_leth`

**Choice: `E_leth = 1000 J` (1 kJ), the ES-310 moderate-personnel-kill /
`P_k|hit = 0.5` anchor.**

Source: `doc-reference/wound-ballistics/fas-es310-damage-criteria` (FAS/Navy
ES-310, 1998), read directly: the document tabulates personnel kill criteria at
100 J (`P_k = 0.1`, light), **1000 J (`P_k = 0.5`, moderate, ".357 jacketed
soft-point" equivalent)**, and 4000 J (`P_k = 0.9`, heavy), and formally defines
"lethal range" as the standoff at which `P_k = 0.50` against personnel.

**Why 1 kJ and not 79 J.** The 79 J value in `_validation.qmd:94` is labelled in
the code itself as "used only as a bisection validation reference, **not the
model threshold**." ES-310 states 79 J sits *below* the DoD's own 100 J light
floor (`P_k = 0.1`) — it is a minimum-incapacitation hazard floor, not a
lethality criterion; using it as a binary kill cut overestimates lethality.
The binary cut should match the same `P_k = 0.5` energy that the *graded*
`pk_given_hit` it replaces returns 0.5 at — and `pk_given_hit` is anchored at
exactly `_PK_E = [100, 1000, 4000] J → [0.1, 0.5, 0.9]` (`fragmentation.py:140`).
So `E_leth = 1000 J` makes `ρ_L` read as "areal density of fragments each ≥50%
lethal on a hit," the clean binary counterpart of the graded weighting on the
**same ES-310 energy basis**. This is the self-consistent choice; the value is
not invented here, it is the existing `_PK_VAL = 0.5` anchor.

**Self-consistency check (graded ↔ binary at the anchor).** At the range where
`pk_given_hit(E) = 0.5`, the fragment KE equals 1000 J, which is precisely the
`m_min` boundary; so the binary cut's 50% boundary coincides with the graded
weighting's 50% point by construction. The two models differ only away from the
anchor (the binary is a step where the graded is a logE ramp) — expected and
acceptable for a "fragments out, target out" kernel.

`E_leth` remains a caller-supplied argument to `min_lethal_mass` (not hard-coded
in physics); 1000 J is the **default the field evaluator should pass**, recorded
here so the src/ pass uses it deliberately.

______________________________________________________________________

## 4 · Dimensional analysis (acceptance criterion 1)

| Equation                               | LHS     | RHS                                  | OK? |
| -------------------------------------- | ------- | ------------------------------------ | --- |
| (1) `s = √(x²+y²+(z−h_b)²)`            | m       | √(m²) = m                            | ✓   |
| (2) `ĥr = (P−B)/s`                     | –       | m / m                                | ✓   |
| (4) `cosΘ = ĥr·ê_axis`                 | –       | (–)·(–)                              | ✓   |
| (5) `E = ½ m (V₀ e^{−λs})²`            | J       | kg·(m/s)² = J                        | ✓   |
| `λ s = k m^{−1/3} s`                   | –       | (m⁻¹)·m = – (exponent dimensionless) | ✓   |
| (6) `N^z = N₀ exp(−√(m_min/μ))`        | –       | – · exp(√(kg/kg)) = –                | ✓   |
| spreading `g^z = 1/(2π s² · 2 sinθ δ)` | m⁻²     | 1/(m²·–·–) = m⁻²                     | ✓   |
| (3) `ρ_L = g^z · N^z`                  | **m⁻²** | m⁻² · – = m⁻²                        | ✓   |

`δ` enters as radians (a dimensionless arc measure), consistent with its role as
the belt fractional half-width; `2 sinθ^z δ` is the dimensionless solid-angle
fraction of the belt (frag-field-3d-geometry/derivation §3.8). **`ρ_L` is m⁻² by
construction** — spreading (m⁻²) × dimensionless lethal count.

______________________________________________________________________

## 5 · Self-consistency and limit checks (acceptance criteria 2–5)

### 5.1 `z = 0` reduction with target terms divided out (criterion 2)

Set `z = 0`. Then eq. (1) gives `s = √(x² + y² + h_b²)` and eq. (2) gives
`ĥr = (x, y, −h_b)/s` — **exactly** the slant range and ray hard-coded at
`fragmentation.py:407,412` and `zones.py:448,451`. So the geometry of `ρ_L(x,y,0)`
is identical to the existing ground evaluator's geometry; B1 is a strict
generalisation whose `z=0` slice is the current code (no behaviour change on the
ground plane).

The existing per-point ground integrand (single-zone, `:425`) is

$$
I\_{\\text{old}}(s) ;=; \\int \\underbrace{n(m)}_{\\text{pdf}};\\underbrace{p_{k|h}(E)}_{\\text{target}};\\underbrace{A_p(\\gamma)}_{\\text{target}};\\frac{1}{2\\pi s^2,2\\sin\\theta^z,\\delta},dm .
$$

Dividing out **both** target-coupled factors means (i) removing `A_p(γ)` [m²] and
(ii) replacing the graded `p_{k|h}(E)` by the binary `𝟙[m ≥ m_min(s)]`:

$$
\\rho_L(x,y,0)
;=; \\int n(m),\\mathbb{1}[m\\ge m\_{\\min}(s)],\\frac{dm}{2\\pi s^2,2\\sin\\theta^z,\\delta}
;=; \\frac{N_0,e^{-\\sqrt{m\_{\\min}/\\mu}}}{2\\pi s^2,2\\sin\\theta^z,\\delta},
$$

which is eq. (3). **The spreading-only part matches exactly** — same
`1/(2π s² · 2 sinθ^z δ)`, same `s`, same belt test, same `θ` — confirming the
isolation is clean. The only intended differences from `I_old` are the two
removed target factors. Equivalently, the reconstruction identity holds:

$$
\\boxed{;\\rho_L(x,y,0)\\cdot A_p(\\gamma);\\Big|_{\\text{binary}\\to\\text{graded}}
;=; I_{\\text{old}}(s);}
$$

i.e. multiply `ρ_L` by a target presented area `A_p` and swap the binary cut back
for the graded weighting and the existing ground `N_eff` integrand is recovered.
This is the precise sense in which `ρ_L` is the field's **target-independent
kernel**. (At minimum — the criterion's floor — the spreading factors match
exactly; the integrand identity above is the stronger statement and also holds.)

### 5.2 `A_p → 1 m²` interpretation note

Numerically, "divide out `A_p`" is equivalent to evaluating the existing
integrand with `A_p` replaced by a **unit area of 1 m²**. Then the result already
carries the right unit (m⁻²) and reads as "lethal fragments crossing a 1 m² patch
here." This is the cleanest framing for the src/ pass: same code path, `A_p ← 1`,
`pk_given_hit ← 𝟙[m≥m_min]`.

### 5.3 Far-field decay (criterion 3)

As `s → ∞`, drag attenuation `e^{−λ(m)s} → 0` for every finite `m`, so eq. (5)
forces `E^z(m,s) < E_leth` even for the heaviest fragment → `m_min^z(s) → m_hi`
→ `N^z(s) = N_0 exp(−√(m_hi/μ)) → 0`. Hence **`ρ_L → 0`**, even though the bare
spreading factor only decays as `1/s²`. This is the distinguishing behaviour vs.
the rejected no-cut total density A2 (whose `N → N_0` constant never vanishes):
the lethal *reach* is finite and visible. ✓

### 5.4 Belt-geometry guard (criterion 4) — Open item 3 resolved

**The belt-acceptance test needs NO change for `z > 0`.** It is already a test on
the 3D direction `ĥr`; B1 only replaces the ground ray `(x,y,−h_b)/s` with the
general ray `(x,y,z−h_b)/s`. Points outside the belt return zero exactly as on
the ground. What *does* need resolving is which **axis convention** eq. (3)
standardises on — the two existing paths differ, and the prior pass flagged it:

|               | single-zone (`fragmentation.py`) | four-zone (`zones.py`)          |
| ------------- | -------------------------------- | ------------------------------- |
| axis `ê_axis` | `(−cosα, 0, −sinα)` (`:382,411`) | `(+cosα, 0, −sinα)` (`:429`)    |
| spray angle   | implicit `θ = 90°` (equatorial)  | per-zone `θ^z` (cylinder = 90°) |
| accept test   | \`                               | cosΘ                            |

The two axes differ by a sign flip on the **x-component only**, not the whole
vector. For a general ray `ĥr = (rx, ry, rz)`,

$$
\\cos\\Theta\_{\\text{single}} = -r_x\\cos\\alpha - r_z\\sin\\alpha, \\qquad
\\cos\\Theta\_{\\text{four}} = +r_x\\cos\\alpha - r_z\\sin\\alpha .
$$

These are **not** negatives of each other in general: `cosΘ_single = −cosΘ_four` holds only when `rz = 0` (the `x=0` line of the field has `rx=0`,
not `rz=0`). So the `|cosΘ| ≤ sinδ` single-zone guard and the `|cosΘ| ≤ sinδ`
four-zone equatorial guard accept **different point sets** whenever the AoF
`α ≠ 0` and the point is off the `y–z` plane (`rx ≠ 0`) — i.e. across the
entire interesting downrange region. Worked counter-example (`α = 30°`, field
point `(20, 0, 2)` rel. burst ⇒ `s ≈ 20.1`, `ĥr ≈ (0.995, 0, −0.0995)`):
`|cosΘ_single| ≈ 0.812` vs `|cosΘ_four| ≈ 0.912`. The earlier "identical in
magnitude" claim was **false** off the `x=0` plane.

**Resolution — deliberately standardise both paths on the four-zone
forward-axis convention `ê_axis = (+cosα, 0, −sinα)`.** This is an
**implementation choice**, not a corollary of any invariance argument. The two
existing conventions are *genuinely different* for every `α ≠ 0`: flipping only
the x-component of `ê_axis` (leaving the z-component `−sinα` untouched) is **not**
the same as negating the whole vector, so it does **not** leave `|cosΘ|`
invariant off the `x=0` plane. The worked example above is the proof of
non-equivalence: `|cosΘ_single| ≈ 0.812 ≠ |cosΘ_four| ≈ 0.912` at a single
off-axis point. The transformation that *would* be a harmless fore/aft
relabeling of a symmetric equatorial belt is `ê → −ê` (all three components,
giving `cosΘ → −cosΘ` and hence `|cosΘ|` exactly invariant for any ray); the
x-only flip is a *different* operation and changes the accepted point set
wherever `α ≠ 0`, `rx ≠ 0`, `rz ≠ 0`. We therefore make **no** claim that the
flip is physics-neutral.

What we do instead: pick **one** convention and write it into both paths.
Whether the single-zone path historically used `(−cosα,…)` is irrelevant once
we overwrite it — after standardising, the single-zone equatorial test and the
four-zone equatorial test use the *same* `ê_axis = (+cosα, 0, −sinα)` formula
and therefore accept the *same* point set **by construction** (they are
literally the same expression), not by any proven equivalence between the two
old formulas. For **non-equatorial** zones (`θ^z ≠ 90°`, four-zone path only)
the forward-axis convention is moreover *required*: a zone spraying forward at
`θ^z < 90°` must be tested against the forward axis, and the `|cosΘ − cosθ^z|`
test is sign-sensitive. The forward convention is thus the natural one to make
canonical — mandatory for the non-equatorial zones, and freely adoptable for
the equatorial single-zone path (we overwrite its historical axis). **eq. (3) is
written with `ê_axis = (+cosα, 0, −sinα)` throughout**, and the src/ field
evaluator must apply this convention to the single-zone path too, replacing its
historical `(−cosα,…)`.

**What this is, and is not, evidence of.** Standardising on one formula
makes the two paths identical *by construction*, which is a trivially true
statement about the code we will write — it is **not** itself evidence that the
single-zone path computes the same `ρ_L` as the four-zone path at an arbitrary
3D point. That pointwise agreement (across the rest of `ρ_L` — masses, Mott
collapse, spreading) is established **only** by the numerical spot-check planned
in §8, never by an analytical claim in this document. Do not skip that check on
the assumption that this section proved equivalence.

**Guard behaviour:** `ρ_L = 0` outside the belt, both paths, ground and `z>0`
alike. ✓ (After the standardisation above, both paths share one `ê_axis`
formula; the off-`x=0` pointwise agreement is the subject of the §8 numerical
spot-check.)

**`δ → 0` guard.** At `δ = 0` the belt collapses to a Dirac ring no finite grid
point lies on, and `1/δ` diverges; `_expected_kills_3d_point` already returns 0
for `δ ≤ 0` (`:404`). `ρ_L` inherits this — return 0, do not evaluate the
spreading factor. ✓ (Self-consistent with the existing single-zone guard.)

### 5.5 Single-zone ↔ four-zone consistency (criterion 5)

Collapse the four zones to one **equivalent cylinder**: a single zone with the
total steel mass `M = Σ_z M^z`, the mass-weighted Mott half-mass, a single
`V_0`, and `θ = 90°`. With both paths now written on the **same** `ê_axis`
formula (§5.4 standardisation, an implementation choice — not a proven
invariance), the consistency statement is:

- when all four zones share the common spray angle `θ^z = 90°`, every per-zone
  belt test becomes the equatorial test `|cosΘ| ≤ sinδ` using the
  `ê_axis = (+cosα,0,−sinα)` formula — which is, *by construction*, the very
  same formula the standardised single-zone path now uses. The two belt tests
  are thus the same expression on the same ray, so they accept the same point
  set. This is a statement about writing one formula in two places, **not** a
  claim that the single-zone path's *old* `(−cosα,…)` axis was equivalent to it
  (§5.4 shows it was not);
- `Σ_z N_0^z = Σ_z M^z/(2μ^z) → N_0 = M/(2μ)` when the `μ^z` are collapsed to a
  common `μ` (the standard Mott-`μ` collapse);
- `Σ_z g^z N^z → g·N` with the common `(θ=90°, μ, V_0)`.

So eq. (3) for the four-zone path reduces to eq. (3) for the single-zone path
**within Mott-`μ` tolerance** — the same self-consistency statement as the
existing four-zone derivation §5 (frag-field-3d-geometry). The belt-test
component of that reduction holds *by construction* (one shared `ê_axis`
formula); the remaining components (the Mott-`μ` collapse and the spreading)
carry the same tolerance the prior derivation established for the
aggregate/merged field *magnitude*. The tolerance is set by the spread of
per-zone `μ^z` about the collapsed `μ`: identical zones recover the single-zone
field exactly; realistic zones agree to the `μ`-spread (a few percent on the
integrated count), as the prior derivation already validated for the
target-coupled field. Because `ρ_L` differs from that field only by the two
divided-out target factors (which are common to both paths and cancel in the
ratio), the consistency margin is **unchanged** from the validated case.

This collapse is a *paper* check of the parameter/mass collapse only. It does
**not** by itself establish that the two code paths return the same `ρ_L` at an
arbitrary off-`x=0` 3D point — that is established **solely** by the numerical
spot-check planned in §8, which is the sole evidence for pointwise agreement and
must not be skipped. ✓

______________________________________________________________________

## 6 · Open item 4 — slant-range table for `m_min(s)` (criterion 6)

**Strategy (C1/C2):** `m_min^z` depends on `s` only (and per-zone `V_0^z`), not on
direction or `(x,y,z)` separately. Precompute `m_min^z(s)` on a **1D `s`-grid per
zone**, then `np.interp` at every grid point's `s` — collapsing 3D root-finding
to one 1D solve per zone and making the field vectorizable.

### 6.1 Grid extent

`s` ranges over the 3D field box. With half-extent `L` (e.g. `max_radius`) and
burst height `h_b`, the **maximum** slant range to any box corner at height `z_max`
is `s_max = √(2 L² + (z_max − h_b)²)`; the **minimum** is `s_min ≈ h_b` (point
directly under/over the burst) but can approach 0 if the box contains the burst,
so floor at `s_min = 0.5 m`. (This floor is a *numerical* guard against the
`1/s²` spreading singularity at the burst, **not** a region where `m_min`
flattens — per §2, `m_min` does not clip to `m_lo` for this shell, so it keeps
varying down to `s_min`.) Recommended: `s ∈ [0.5, s_max]` with `s_max` computed
from the actual box, plus a small margin (×1.05) so no grid point extrapolates.

### 6.2 Resolution — justification against display tolerance

`m_min(s)` is smooth and **monotone increasing** in `s` (more drag → heavier
minimum lethal fragment), with **no flat plateau** at either end for the default
shell (§2): it varies continuously from `s_min` and only saturates as it
approaches the `m_hi` clip at the far lethal edge. Linear interpolation error on a
smooth monotone function scales as `ε ≈ (Δs)²/8 · max|m_min''|`. The display
tolerance is set by the colour map: a typical field render resolves ~256 colour
levels over the dynamic range of `ρ_L`, i.e. a per-point relative tolerance of
~0.4%. Because `ρ_L`'s `s`-dependence is dominated by the *smooth*
`N(m_min(s)) = N_0 exp(−√(m_min/μ))` and the spreading `1/s²` (both gentle), and
`m_min(s)` enters only through that exponential, a **uniform grid of `n_s = 400`
points** over `[s_min, s_max]` gives `Δs ≈ s_max/400` (≈ 0.3 m for an 80 m box
at AoF, `z_max ≈ 40 m`), which is **expected** to keep the interpolated
`exp(−√(m_min/μ))` error well under the ~0.4% display tolerance. Near the far
lethal edge `m_min` rises steeply toward `m_hi`, but there `N → 0` regardless, so
the absolute error in `ρ_L` is negligible (small number × small error). A
**log-spaced** grid is *not* needed because `m_min` is not multiscale in `s`;
uniform is simplest.

This resolution argument is **not** backed by an actual `max|m_min''(s)|`
estimate — it is a qualitative expectation. The **acceptance gate is the §6.3
interpolation oracle**, not this paragraph: `n_s = 400` is a starting point to be
**confirmed empirically** by the oracle's `<1%` assertion in the src/ pass, and
raised if that assertion fails. **Choice recorded (provisional, oracle-gated):
uniform `s`-grid, `n_s = 400`, `s ∈ [0.5, 1.05·s_max]`, per zone (distinct
`V_0^z`).**

### 6.3 Interpolation oracle (criterion: C1 vs direct bisection)

Validation must spot-check that the interpolated `m_min(s)` matches a direct
`min_lethal_mass(s)` bisection at a handful of `s` (the C4 oracle). With
`n_s = 400` the agreement is bounded by 6.2; the src/ and notebook passes should
assert `|m_min_interp − m_min_bisect| / m_min_bisect < 1%` at, e.g., 10 sampled
`s` spanning `[s_min, s_max]`, and additionally that `ρ_L` from the table matches
a fully-direct per-point `ρ_L` at a few 3D points within the same 1% — confirming
no accuracy was traded for the C1 speed-up.

______________________________________________________________________

## 7 · Validation checklist status (scoping §6)

| Check                                        | Where resolved | Status                                                                                                                                                                                  |
| -------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dimensional: `ρ_L` in m⁻²                    | §4             | ✓ by construction                                                                                                                                                                       |
| `z = 0` reduction (target terms divided out) | §5.1           | ✓ spreading matches exactly; reconstruction identity holds                                                                                                                              |
| Far-field decay `ρ_L → 0`                    | §5.3           | ✓ via `m_min → m_hi` ⇒ `N → 0`                                                                                                                                                          |
| Belt geometry guard returns 0 outside belt   | §5.4           | ✓ both paths, `z>0`; both standardised on one `ê_axis = (+cosα,…)` formula (deliberate choice, not a proven-neutral relabel)                                                            |
| `δ → 0` guard                                | §5.4           | ✓ return 0 (matches existing)                                                                                                                                                           |
| Single- vs four-zone consistency             | §5.5           | paper: parameter/Mott-`μ` collapse ✓; belt test identical *by construction*. Pointwise `ρ_L` agreement is **not** proven here — deferred to the §8 numerical spot-check (sole evidence) |
| Interpolation oracle (C1 vs bisection)       | §6.3           | ✓ assert \<1% at sampled `s` (for later pass)                                                                                                                                           |
| `E_leth` value chosen + why                  | §3             | ✓ 1000 J (ES-310 `P_k=0.5`) recorded                                                                                                                                                    |

**Items to leave to later passes (not derivable here):** the numeric oracle
assertions (§6.3) run in the src/ implementation and notebook validation passes;
this derivation fixes their tolerances and rationale.

______________________________________________________________________

## 8 · Implementation notes for the src/ pass (not code)

- Reuse `min_lethal_mass` (`fragmentation.py:230`) and `mott_N` (`:207`)
  unchanged; build the per-zone `m_min(s)` table over the §6 grid and `np.interp`.
- `ρ_L` = existing per-point integrand with **`A_p ← 1 m²`** and
  **`pk_given_hit(E) ← 𝟙[m ≥ m_min(s)]`** (equivalently the closed-form `N^z(s)`
  of eq. 6, avoiding the mass-grid trapezoid entirely on the hot path).
- **Axis convention (§5.4):** use `ê_axis = (+cosα, 0, −sinα)` for **both**
  paths. The single-zone path must be normalised off its historical
  `(−cosα, 0, −sinα)` to this convention so the two paths agree pointwise off the
  `x=0` plane. Add a test asserting four-zone (all `θ^z=90°`, collapsed
  parameters) `ρ_L` matches single-zone `ρ_L` at off-`x=0` 3D points, not just on
  the `x=0` line.
- Single-zone: one zone, `θ = 90°`, `|cosΘ| ≤ sinδ` guard, `(N_0, μ, V_0)`.
- Four-zone: loop zones with `(θ^z, μ^z, V_0^z, N_0^z)` and the
  `|cosΘ − cosθ^z| ≤ sinδ` guard; sum `ρ_L` over zones.
- General ray uses the field point's own `z`: `s` and `ĥr` from eqs. (1)–(2).
- Optional A2 toggle = same path with the `m_min` cut removed (`N → N_0`).
- Default `E_leth = 1000 J` (§3).

______________________________________________________________________

## 9 · Observation — pre-existing legacy spreading inconsistency (out of scope)

While implementing/validating `ρ_L`, the src/ pass surfaced a **pre-existing**
inconsistency in the legacy target-coupled field evaluator
`_expected_kills_3d_point` (`fragmentation.py`): its spreading denominator uses
`sin_Theta` — the *field point's own* polar angle `Θ` from the shell axis
(`sin_Theta = √(1−cos²Θ)`) — rather than the *zone* spray angle `sinθ^z`. Per
eq. (3) and frag-field-3d-geometry §3.8, the belt solid-angle fraction is
`2·sinθ^z·δ`, a fixed property of where the belt sits, so the correct spreading
factor uses `sinθ^z` (for the equatorial cylinder `sinθ^z = sin90° = 1`). Using
`sinΘ` only ~agrees because the narrow belt keeps `Θ ≈ 90°`; it inflates the
result by `O(δ²)` off the belt centre. The new `lethal_density_point` /
`lethal_density_four_zone_point` paths correctly use `sinθ^z`, which is what made
the single-vs-four-zone consistency oracle (§5.5 / §8) pass to machine precision.

**This is recorded as an observation only — the legacy `_expected_kills_3d_point`
is NOT fixed here**, as it is the target-coupled `P(kill)` field, outside this
aspect's target-independent `ρ_L` scope. A separate change should correct it (and
@model-reviewer re-verify) if the legacy field's off-belt-centre accuracy matters.

### Validation oracle results (src/ pass, this aspect)

All §5–§6 oracles run against the implemented `src/arty/` code pass:

| Oracle                                                                | Result | Max rel error |
| --------------------------------------------------------------------- | ------ | ------------- |
| `z=0` reduction (264 belt pts; interp vs direct bisection)            | PASS   | 1.1e-06       |
| `m_min(s)` interp vs bisection (10 sampled `s`)                       | PASS   | 6.3e-07       |
| `ρ_L` table vs fully-direct (6 off-`x=0` 3D pts)                      | PASS   | 9.7e-07       |
| Far-field decay (`ρ_L → 0`, monotone; `R=800 m` → 4.4e-09)            | PASS   | —             |
| Belt guard (out-of-belt → 0) & `δ=0` guard (→ 0)                      | PASS   | exact 0       |
| Single-vs-four-zone consistency (collapsed cylinder, 6 off-`x=0` pts) | PASS   | 0.0 (exact)   |

The single-vs-four-zone check — which **failed before the `sinΘ → sinθ^z` fix**
in `lethal_density_point` — now agrees to machine precision, confirming the fix.
