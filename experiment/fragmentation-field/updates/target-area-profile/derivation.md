# Derivation — angle-dependent presented-area profile $A_p(\\gamma)$

**Author:** modeler agent
**Date:** 2026-05-23
**Status:** derivation only — no code or .qmd modifications
**Related:** `experiment/fragmentation-field/fragmentation-field.qmd` §6, eq. (20)–(22)
**Companion:** `./scoping.md`

______________________________________________________________________

## 1. Purpose and scope

Replace the constant horizontal presented width $w = 0.5,\\text{m}$ in eq. (22)
of the fragmentation-field notebook with an angle-dependent presented area
$A_p(\\gamma)$ derived from a two-face "box body" model of the soldier. The
upgrade is necessary so the model can distinguish ground burst from airburst
lethality against postures of different vertical extent (standing vs prone).

The derivation is *geometric only*; it does not change any physics of fragment
flight (drag, Mott, Gurney) or lethality (ES-310 $P\_{k|\\text{hit}}$). It
changes only the **target-presentation factor** that converts a per-steradian
fragment flux into expected hits on a body.

______________________________________________________________________

## 2. Fragment-arrival elevation angle $\\gamma$

The notebook already establishes the straight-line ray from burst point
$(0, 0, h_b)$ to ground patch $(x_g, y_g, 0)$ with slant range

$$
s = \\sqrt{x_g^2 + y_g^2 + h_b^2}.
$$

Let $\\gamma$ be the elevation angle of fragment arrival at the ground patch,
measured from horizontal. From the ray geometry,

$$
\\sin\\gamma ;=; \\frac{h_b}{s}, \\qquad
\\cos\\gamma ;=; \\frac{\\sqrt{x_g^2 + y_g^2}}{s},
\\qquad \\gamma \\in [0,;\\tfrac{\\pi}{2}].
$$

Limits:

- $\\gamma \\to 0$: grazing horizontal arrival (ground burst, or large
  cross-range on a low airburst).
- $\\gamma \\to \\pi/2$: vertical descent (target directly under burst).

Note $\\gamma$ is *not* the polar spray angle $\\Theta$ from the shell axis —
$\\Theta$ is a property of the launch, $\\gamma$ is a property of the arrival
geometry at the patch. Both are derivable from $(x_g, y_g, h_b, \\alpha)$.

______________________________________________________________________

## 3. Body model — two orthogonal rectangles

Approximate the soldier as a rectangular box with three orthogonal dimensions:

| Symbol      | Meaning                            | Unit |
| ----------- | ---------------------------------- | ---- |
| $w\_\\perp$ | body width (shoulder-to-shoulder)  | m    |
| $h$         | vertical body extent               | m    |
|             | standing: head-to-foot height      |      |
|             | prone: belly-to-back thickness     |      |
| $d$         | body depth in the horizontal plane | m    |
|             | standing: belly-to-back            |      |
|             | prone: head-to-foot length         |      |

For a fragment arriving in the vertical plane that contains both the body
axis and the line-of-sight, only two faces of the box have nonzero projected
area:

| Face                                   | Real area     | Outward normal | Contributes when |
| -------------------------------------- | ------------- | -------------- | ---------------- |
| Front face $A_f$ — vertical silhouette | $w\_\\perp,h$ | horizontal     | $\\gamma < 90°$  |
| Top face $A_t$ — overhead silhouette   | $w\_\\perp,d$ | vertical (up)  | $\\gamma > 0°$   |

(The two side faces, area $h,d$, have horizontal normals perpendicular to the
ray and project to zero in the body-LOS plane. The bottom and back are
self-occluded.)

### 3.1 Lambert (flat-plate) projection

A flat plate of area $A$ with outward normal $\\hat{n}$, viewed along ray
direction $\\hat{r}$, presents area $A,|\\hat{n}\\cdot\\hat{r}|$ (assuming the
ray strikes the front of the plate; back-of-plate contributions are dropped
as self-occlusion).

For a fragment arriving from the burst toward the ground patch with elevation
$\\gamma$ above horizontal, the unit ray (from burst to target) has
$\\hat{r} = (\\cos\\gamma,\\hat{\\rho},;-\\sin\\gamma)$ in the
(horizontal, vertical) plane, where $\\hat{\\rho}$ is the horizontal direction
from burst to patch.

- Front-face normal $\\hat{n}\_f = -\\hat{\\rho}$ (faces the burst):
  $|\\hat{n}\_f\\cdot\\hat{r}| = \\cos\\gamma$.
- Top-face normal $\\hat{n}\_t = +\\hat{z}$ (faces up):
  $|\\hat{n}\_t\\cdot\\hat{r}| = \\sin\\gamma$.

Summing the two non-occluded faces gives the **total projected area** of the
box body as seen along the fragment ray:

$$
\\boxed{;
A_p(\\gamma) ;=; A_f\\cos\\gamma ;+; A_t\\sin\\gamma
;=; w\_\\perp\\bigl(h\\cos\\gamma + d\\sin\\gamma\\bigr)
;}
\\quad (\\text{eq. P1})
$$

This is the **Lambert projection of an opaque box** along a ray of elevation
$\\gamma$, summed over the two facing surfaces.

### 3.2 Factoring into width × effective vertical extent

Equation (P1) factors as

$$
A_p(\\gamma) ;=; w\_\\perp \\cdot h\_\\text{eff}(\\gamma),
\\qquad
h\_\\text{eff}(\\gamma) ;=; h\\cos\\gamma + d\\sin\\gamma.
$$

This factored form is convenient because the §6 derivation already uses
$w\_\\perp$ as the horizontal angular extent of the target (an *azimuthal*
quantity); the new factor $h\_\\text{eff}(\\gamma)$ is the *vertical* extent
along the meridional direction, and depends only on the arrival elevation.

### 3.3 Limits and sanity bounds

| Condition                       | $A_p$                                     | Interpretation                            |
| ------------------------------- | ----------------------------------------- | ----------------------------------------- |
| $\\gamma = 0$ (horizontal)      | $w\_\\perp,h = A_f$                       | Pure frontal silhouette.                  |
| $\\gamma = 90°$ (vertical)      | $w\_\\perp,d = A_t$                       | Pure overhead silhouette.                 |
| $h = d$ (cube)                  | $w\_\\perp,h,(\\cos\\gamma+\\sin\\gamma)$ | Max $A_p = \\sqrt{2},w\_\\perp h$ at 45°. |
| $d = 0$ (infinitely thin plate) | $w\_\\perp,h\\cos\\gamma$                 | Plate cosine law.                         |

$A_p$ is bounded above by $w\_\\perp\\sqrt{h^2 + d^2}$ at
$\\gamma^\* = \\arctan(d/h)$ (Cauchy–Schwarz). For standing $(h,d)=(1.7, 0.3)$
the maximum is $0.5\\cdot 1.727 = 0.864,\\text{m}^2$ at $\\gamma^\* \\approx 10°$;
for prone $(h,d)=(0.3, 1.8)$ the maximum is $0.5\\cdot 1.825 = 0.913,\\text{m}^2$
at $\\gamma^\* \\approx 80°$. Both within physical expectations.

______________________________________________________________________

## 4. Replacement of eq. (22)

### 4.1 The geometry factor changes from width/arc to area/spherical-cap

The current §6.5 derivation (notebook lines ~883–897) reasons as follows:

> Fragments per unit azimuthal angle in the belt: $N_0/(2\\pi)$. Convert to
> per-radian polar-angle density via $1/(2\\delta)$ for the belt half-width.
> A target of presented width $w$ at slant range $s$ subtends an azimuthal
> angular width $w/(s\\sin\\Theta)$. The dimensionless intercepted fraction is
> $g = w/(2\\pi,s,\\cdot 2\\sin\\Theta,\\delta)$.

This treats the target as occupying the **slant range $s$** in the
polar-angle direction — i.e., $h\_\\text{eff}^\\text{old} = s$, not
$2s\\sin\\Theta,\\delta$. That is the implicit hidden assumption: the
effective vertical extent of the target equals the slant range itself, so
the formula reduces to a width/arc ratio. Under that assumption $g$ has
units (m)/(m) and is dimensionless. But for a finite target of vertical
extent $h\_\\text{eff}(\\gamma) < s$ (which is the rule, not the exception —
$s$ is typically tens of metres at operational ranges), the formula
over-counts.

The correct derivation works in **solid angle** rather than azimuthal arc.

#### 4.1.1 Per-steradian fragment flux from the belt

Total fragments $N_0$ are launched into the equatorial belt
$|\\Theta - 90°| \\le \\delta$. The solid angle of that belt on the unit sphere
is

$$
\\Omega\_\\text{belt}
= \\int\_{90°-\\delta}^{90°+\\delta}!!\\int_0^{2\\pi} \\sin\\Theta,d\\psi,d\\Theta
= 4\\pi\\sin\\delta \\approx 4\\pi\\delta \\quad (\\delta \\ll 1).
$$

Assuming uniform distribution within the belt, the per-steradian fragment
density at launch is $N_0 / (4\\pi\\sin\\delta) \\approx N_0/(4\\pi\\delta)$.

By straight-line propagation, the **fragment areal density at slant range $s$**,
on the sphere centred on the burst, is

$$
\\sigma(s) ;=; \\frac{N_0}{4\\pi\\delta;s^2}
\\quad [\\text{frag}/\\text{m}^2].
\\quad (\\text{eq. P2})
$$

(This is the "spherical shell expansion" — the same $1/s^2$ that any
inverse-square-law derivation gives. Cf. ES-310's
$N\_\\text{hits} = A N_0/(4\\pi R^2)$ form for an isotropic burst — our belt
factor $1/\\delta$ simply restricts the sphere to the equatorial slab.)

#### 4.1.2 Expected hits on a target of projected area $A_p$

A target presenting projected area $A_p$ to the radial direction at slant
range $s$ subtends solid angle $A_p/s^2$ on the burst-centred sphere
(small-angle: target subtense $\\ll s$, valid because $A_p^{1/2} \\sim 1,\\text{m}$
and $s \\gtrsim 10,\\text{m}$). The expected number of fragments hitting it is

$$
N\_\\text{hits} ;=; \\sigma(s),A_p ;=;
\\frac{N_0,A_p}{4\\pi\\delta,s^2}
;=; N_0 \\cdot \\frac{A_p}{4\\pi,s^2,\\delta}.
\\quad (\\text{eq. P3})
$$

To match the §6 notation (which distinguishes belt half-width $\\delta$ and
peels out the $1/(2\\sin\\Theta)$ from azimuthal arc-length on the belt), write
$\\Omega\_\\text{belt} = 4\\pi\\sin\\delta = 2\\pi \\cdot 2\\sin\\delta$ and recognise
that the equatorial-slab subtense for a ray at polar angle $\\Theta$ requires
the $\\sin\\Theta$ Jacobian:

$$
g\_\\text{new}(s,\\Theta;,A_p,\\delta)
;=; \\frac{A_p}{2\\pi,s^2 \\cdot 2\\sin\\Theta,\\delta}
\\quad [\\text{dimensionless}].
\\quad (\\text{eq. P4})
$$

> **Note on the $\\sin\\Theta$ factor.** $\\sin\\Theta$ is retained here to match
> the §6.5 belt-Jacobian notation of eq. (15). For the equatorial belt
> ($\\delta \\le 15°$), $\\sin\\Theta \\approx 1$ and the numerical difference
> from the pure P3 form (without $\\sin\\Theta$) is < 3.5 %. The two forms are
> equivalent at $\\Theta = 90°$.

This is the direct replacement for the old $g$ in eq. (20).

#### 4.1.3 Replacement of eq. (22)

Substituting eq. (P4) and $A_p(\\gamma) = w\_\\perp,h\_\\text{eff}(\\gamma)$ from
eq. (P1) into the mass-integrated lethal-hit expression:

$$
\\boxed{;
N\_\\text{eff}(x_g, y_g) ;=;
\\int_0^\\infty n(m),P\_{k|\\text{hit}}!\\bigl(E_k(s,m)\\bigr),
\\frac{A_p(\\gamma)}{2\\pi,s^2 \\cdot 2\\sin\\Theta,\\delta},dm
;}
\\quad (\\text{eq. 22'})
$$

with

$$
A_p(\\gamma) = w\_\\perp\\bigl(h\\cos\\gamma + d\\sin\\gamma\\bigr),
\\qquad
\\sin\\gamma = h_b/s,
\\qquad
\\cos\\gamma = \\sqrt{x_g^2+y_g^2}/s.
$$

The new (22') has the same outer structure as the old (22): a mass-distribution
integrand $n(m),P\_{k|\\text{hit}}$ multiplied by a dimensionless geometry
factor. The geometry factor has gained one power of $1/s$ and lost the
implicit "tall target" assumption.

### 4.2 Unit check

| Quantity    | Old eq. (22) factor                                                      | New eq. (22') factor                                                           |
| ----------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Numerator   | $w$ [m]                                                                  | $A_p(\\gamma)$ [m²]                                                            |
| Denominator | $(2\\pi,s,[\\text{m}]) \\cdot (2\\sin\\Theta,\\delta,[-]) = [\\text{m}]$ | $(2\\pi,s^2,[\\text{m}^2]) \\cdot (2\\sin\\Theta,\\delta,[-]) = [\\text{m}^2]$ |
| Ratio       | m/m = dimensionless ✓                                                    | m²/m² = dimensionless ✓                                                        |

The new geometry factor has units m²/m² = dimensionless as required, since
the mass integrand $n(m),P\_{k|\\text{hit}},dm$ has units of
[frag/kg]·[-]·[kg] = [frag] and $N\_\\text{eff}$ must be in [hits per target].
Confirmed.

### 4.3 Limit recovery — old vs new at $\\gamma = 0$

It is *not* true that eq. (22') reduces to eq. (22) at $\\gamma \\to 0$. The
two formulas differ by a dimensional factor. Explicitly:

- **Old factor** at $\\gamma = 0$: $g\_\\text{old} = w/(2\\pi,s\\cdot 2\\sin\\Theta,\\delta)$.
- **New factor** at $\\gamma = 0$: $A_p(0) = w\_\\perp h = A_f$, and
  $g\_\\text{new}(0) = A_f/(2\\pi,s^2\\cdot 2\\sin\\Theta,\\delta)$.

Their ratio is

$$
\\frac{g\_\\text{new}(0)}{g\_\\text{old}} ;=;
\\frac{A_f}{w,s} ;=; \\frac{w\_\\perp h}{w,s}.
$$

With $w\_\\perp = w = 0.5,\\text{m}$ and $h = 1.7,\\text{m}$ (standing) this
ratio is $1.7/s$. At $s = 10,\\text{m}$ the new model gives $\\approx 0.17\\times$
the old model's hit count; at $s = 30,\\text{m}$, $\\approx 0.057\\times$. The
new model is **smaller** in absolute terms, but its $s^{-2}$ falloff (vs the
old $s^{-1}$) is the **physically correct inverse-square law** for an
isotropic source — the old $s^{-1}$ resulted from implicitly absorbing one
factor of $s$ into the assumption that the target spans the belt.

**Interpretation.** The old formula was *not wrong* per se — it was a valid
"target tall enough to fill the belt slab" approximation. The new formula is
*more general* because it correctly handles finite-height targets at arbitrary
arrival angles. Consequence: the new model's absolute hit counts (and hence
the $R\_{50}$ lethal-area numbers) will not match the old model's — they will
generally be smaller because the old formula was over-counting tall-target
flux. Calibration against published M107 lethal-area numbers (Limitation #5
in the notebook, TM 9-1901) must be redone after the switch.

**The old model is recovered exactly** if and only if
$h\_\\text{eff}(\\gamma) \\to s$, i.e. the target's effective vertical extent
in the polar-angle direction equals the slant range itself. This is the
buried assumption that the new derivation makes explicit and discards.

### 4.4 Limit recovery — eq. (9), the 1D disk

The notebook's §6.5 closes with: "in the limit $h_b \\to 0$, $\\alpha = 0$,
ray along the $y$-axis, $2\\delta = 1,\\text{rad}$ the new eq. (22) recovers
the 1D disk formula eq. (9)." That recovery used the old width-based factor.
For the new (22') the chain is:

- $h_b \\to 0$ ⇒ $\\gamma \\to 0$ ⇒ $A_p(\\gamma) \\to A_f = w\_\\perp h$.
- $\\alpha = 0$, ray along $y$-axis ⇒ $\\Theta = 90°$, $\\sin\\Theta = 1$.
- $g\_\\text{new} \\to A_f/(2\\pi,r^2 \\cdot 2\\delta)$.

This matches eq. (9) ($w/(2\\pi r)$) only if one identifies
$A_f/(r\\cdot 2\\delta) = w$ — which is *not* an identity unless the 1D
disk model is reinterpreted as "infinitely tall target" $\\Leftrightarrow$
$h\\cdot 2\\delta\\cdot \\text{(arbitrary normalisation)}$. **The 1D disk
formula (eq. 9) is not a clean limit of (22'); it is a limit of (22) only.**

This is a documentation requirement, not a derivation bug: the 1D model
was an idealisation that hides the target's vertical structure. The 3D
model exposes it. The notebook's §6.5 recovery-of-eq.-(9) paragraph will
need to be rewritten to say "eq. (22') reduces to a 2D inverse-square
form, not the 1D disk; the 1D disk is no longer a limiting case once
finite target height is modelled."

______________________________________________________________________

## 5. Posture parameter table

The values below are the *engineering convention* used in casualty-reduction
modelling (NATO "man-as-box" silhouettes). They are **not** sourced from any
document in `doc-reference/` — the librarian audit in the scoping note
confirmed Cunniff 2014 and AEP-55 Vol. 3 (the canonical sources) are not
collected.

Disclosure pattern matches Limitation #5 in `fragmentation-field.qmd`
(TM 9-1901 numbers cited from general background, no doc in
`doc-reference/`): label as **engineering convention, source not collected**
and flag for librarian follow-up.

### 5.1 Standing and prone postures (MVP2 scope)

| Posture  | $w\_\\perp$ [m] | $h$ [m] | $d$ [m] | $A_f = w\_\\perp h$ [m²] | $A_t = w\_\\perp d$ [m²] |
| -------- | --------------- | ------- | ------- | ------------------------ | ------------------------ |
| Standing | 0.50            | 1.70    | 0.30    | 0.85                     | 0.15                     |
| Prone    | 0.50            | 0.30    | 1.80    | 0.15                     | 0.90                     |

Notes:

- Standing $A_f = 0.85,\\text{m}^2$ matches commonly quoted values for
  "frontal silhouette of an upright soldier without kit" in casualty models.
- Prone $A_t = 0.90,\\text{m}^2$ matches "overhead silhouette of a
  belly-down soldier (head-to-foot 1.8 m, shoulder width 0.5 m)."
- No helmet, body armour, kit, or limb extension is modelled — this is a
  bare box body. Real silhouettes are 10–25% larger; treat 0.85 / 0.90 as
  *lower bounds*.

### 5.2 Source disclosure (to be copy-pasted into .qmd Limitations)

> **Posture areas — source not collected.** The standing/prone box-body
> dimensions $(h, d)$ used in $A_p(\\gamma) = w\_\\perp(h\\cos\\gamma + d\\sin\\gamma)$
> are the NATO casualty-modelling engineering convention. The canonical
> sources — Cunniff, "A Method to Describe the Statistical Aspects of Armor
> Penetration, Human Vulnerability and Lethality due to Fragmenting
> Munitions" (Int. Symp. Ballistics, 2014) and AEP-55 Vol. 3 — are **not**
> present in `doc-reference/`. The values are stated from background
> knowledge and have not been validated against primary literature.
> Treat all absolute posture-resolved hit counts as ±25% engineering
> estimates until the references are collected.

______________________________________________________________________

## 6. Self-consistency check

| Check                                                                              | Result                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Units of $A_p/s^2$ are dimensionless                                               | ✓                                                                                                                                                                                                                                 |
| $A_p(0) = A_f$ (frontal silhouette)                                                | ✓                                                                                                                                                                                                                                 |
| $A_p(90°) = A_t$ (overhead silhouette)                                             | ✓                                                                                                                                                                                                                                 |
| $A_p \\ge 0$ everywhere on $\\gamma \\in [0,\\pi/2]$                               | ✓ (both terms $\\ge 0$ since $h,d \\ge 0$ and $\\cos\\gamma,\\sin\\gamma \\ge 0$ in range)                                                                                                                                        |
| $A_p$ smooth (C^∞) in $\\gamma$                                                    | ✓                                                                                                                                                                                                                                 |
| Max $A_p = w\_\\perp\\sqrt{h^2+d^2}$ at $\\gamma^\* = \\arctan(d/h)$               | ✓ (Cauchy–Schwarz)                                                                                                                                                                                                                |
| $A_p$ recovers Lambert cosine law for thin plate $d\\to 0$                         | ✓                                                                                                                                                                                                                                 |
| Total expected hits over the ground integrated to $\\infty$ stays finite           | ✓ — convergence comes from $P\_{k                                                                                                                                                                                                 |
| New eq. (22') has the inverse-square scaling expected of an isotropic point source | ✓                                                                                                                                                                                                                                 |
| Old eq. (22) recovered as a special case?                                          | **No** — old formula carries an implicit "target spans full belt slab" assumption that is geometrically invalid for finite targets; this is documented in §4.3 and is a known consequence of the upgrade, not a derivation defect |
| 1D disk eq. (9) recovered as a limit?                                              | **No** — same reason; documented in §4.4. The 1D disk is an idealisation that hides target vertical structure; the 3D-with-area model exposes it. The notebook's §6.5 paragraph claiming eq. (9) recovery will need a rewrite     |

**Verdict.** The derivation is internally self-consistent. The two
non-recoveries (old eq. 22 and 1D disk eq. 9) are not derivation errors —
they are physically correct consequences of removing a hidden assumption.
They do impose a downstream documentation cost (rewrite §6.5 recovery
paragraph) and a calibration cost (re-anchor $R\_{50}$ against TM 9-1901
once the new factor is in place).

______________________________________________________________________

## 7. Summary of changes for downstream implementation

When the modeler returns in the *Implement* phase, the following will need
to change in `fragmentation-field.qmd` §6:

1. **Add** a helper function `presented_area(gamma, posture)` returning
   $A_p$ in m² using eq. (P1).
1. **Add** a derivation of $\\gamma$ from $(x_g, y_g, h_b)$ in §6.4.
1. **Replace** eq. (20) with eq. (P4) and eq. (22) with eq. (22').
1. **Rewrite** the §6.5 "Recovery of eq. (9)" paragraph per §4.4 above.
1. **Update** `expected_kills_3d`: replace `w` argument with `posture`
   string (or struct), call `presented_area(gamma, posture)`, and change
   the `geom` line to `Ap / (2*np.pi * s**2 * 2*sinT * delta)`.
1. **Add** a Limitations entry copy-pasted from §5.2 above.
1. **Add** validation: γ-sweep plot of $A_p$ for standing and prone;
   ground-burst vs airburst hit-count ratio for both postures; expect
   ground-burst-vs-prone to drop to near-zero and airburst-vs-prone to
   stay finite — the qualitative behaviour the model currently cannot
   produce.

No changes to drag, Mott, Gurney, or $P\_{k|\\text{hit}}$ are required.
