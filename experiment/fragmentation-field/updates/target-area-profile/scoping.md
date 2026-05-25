# Scoping note — angle-dependent presented-area profile w(γ)

**Author:** modeler agent
**Date:** 2026-05-23
**Status:** scoping only — no code modifications made
**Related model:** `experiment/fragmentation-field/fragmentation-field.qmd`, §6

## 1. What the current model does

Section 6 of `fragmentation-field.qmd` computes lethal hits per ground patch
$(x_g, y_g)$ as

$$
N\_{\\text{eff}}(x_g, y_g)
= \\int_0^\\infty n(m),P\_{k|\\text{hit}}!\\bigl(E_k(s,m)\\bigr),
\\frac{w}{2\\pi,s\\cdot 2\\sin\\Theta,\\delta};dm
\\quad (\\text{eq. 22})
$$

The presented width is a fixed scalar `w_target = 0.5 m` (line 238) —
the cross-section a standing person presents to a horizontal fragment.
This `w` is multiplied in regardless of the fragment's elevation angle
of arrival γ at the patch. As a result:

- A near-vertical fragment landing on a standing person from above is
  charged the same `0.5 m` width as a horizontal fragment striking the
  torso side-on.
- A prone soldier is not representable at all — they have ~0 m² to
  horizontal fragments but ~0.18 m² to fragments arriving from directly
  above.
- Conclusion: the model cannot separate ground-burst from airburst
  *lethality* against either posture, even though that separation is
  the entire operational reason airburst exists.

## 2. What the geometry should look like

### 2.1 Define γ

Let γ be the **elevation angle of fragment arrival at the ground point**,
measured from horizontal:

$$
\\sin\\gamma ;=; \\frac{h_b}{s}, \\qquad
\\cos\\gamma ;=; \\frac{\\sqrt{x_g^2+y_g^2}}{s}
$$

with $\\gamma \\in [0°, 90°]$. (γ = 0 → grazing horizontal, γ = 90° → fragment
straight down from overhead.) Note γ is already implicitly available in
the §6 ray-mapping: it is the complement of the existing slant-range
elevation already computed.

### 2.2 First-principles area projection

Model the target body as two orthogonal rectangles ("box of two faces"):

| Face                                              | Area (m²)            | Normal direction |
| ------------------------------------------------- | -------------------- | ---------------- |
| **Front** $A_f$ — vertical torso silhouette       | $w\_\\perp \\cdot h$ | horizontal       |
| **Top** $A_t$ — head + shoulder + thigh footprint | $w\_\\perp \\cdot d$ | vertical         |

with $w\_\\perp$ = body width, $h$ = standing height, $d$ = body depth
(belly-to-back).

Projected area to a fragment arriving at elevation γ is:

$$
A_p(\\gamma) ;=; A_f,\\cos\\gamma ;+; A_t,\\sin\\gamma
\\quad (\\text{Lambert / flat-plate projection})
$$

Since the §6 geometry factor uses **width $w$** (not area), and the
azimuthal subtension at the patch is $w/(s \\sin\\Theta)$, the appropriate
generalisation is to keep $w$ as the *horizontal* angular extent
(unchanged) and add a **separate vertical-extent factor** $h\_\\text{eff}(\\gamma)$:

$$
\\boxed{
;A_p(\\gamma) ;=; w\_\\perp \\cdot h\_\\text{eff}(\\gamma)
;\\text{with};
h\_\\text{eff}(\\gamma) ;=; h\\cos\\gamma + d\\sin\\gamma;
}
$$

This is the **cleanest closed-form** option. It uses one extra parameter
per posture ($d$) and one trig term. No new integration variable.

### 2.3 Standard postures (NATO AEP-55 / ITOP 4-2-822 conventions, from general background knowledge — not in `doc-reference/`)

| Posture   | $w\_\\perp$ | $h$    | $d$    | $A_f$ (γ=0) | $A_t$ (γ=90°) |
| --------- | ----------- | ------ | ------ | ----------- | ------------- |
| Standing  | 0.50 m      | 1.70 m | 0.30 m | 0.85 m²     | 0.15 m²       |
| Crouching | 0.50 m      | 1.10 m | 0.45 m | 0.55 m²     | 0.23 m²       |
| Prone     | 0.50 m      | 0.30 m | 1.80 m | 0.15 m²     | 0.90 m²       |

These are not from collected literature — they are the conventional
"man-as-box" silhouettes used in NATO casualty-reduction models. Before
adopting them in the .qmd they should be sourced (see §3 below).

### 2.4 Shape options ranked

| Option                             | Form                            | Pros                                                                            | Cons                                                               |
| ---------------------------------- | ------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **A. Cosine + sine** (recommended) | $h\\cos\\gamma + d\\sin\\gamma$ | closed-form; recovers current model at γ=0; smooth in γ; only one new parameter | rectangular-box approximation; ignores limbs                       |
| **B. Step function**               | $h$ if γ\<γ\*, else $d$         | trivially simple                                                                | discontinuous; no airburst signal in transition zone               |
| **C. ES-310 tabular**              | lookup table                    | matches doctrine                                                                | data not in `doc-reference/` and not in ES-310 source as collected |
| **D. Ellipsoidal body**            | full-body ellipsoid projection  | one curve covers all postures via axis lengths                                  | adds $\\sqrt{}$ per ray; little accuracy gain over A               |

**Recommendation: Option A.**

## 3. Literature audit — does ES-310 or Gold give us this?

I checked all docs in `doc-reference/`. Relevant findings:

- **`doc-reference/wound-ballistics/fas-es310-damage-criteria.md`**
  ES-310 defines $N\_\\text{hits} = A \\cdot N_0/(4\\pi R^2)$ where $A$ is the
  target's **frontal area**, treated as a single scalar. No angle
  dependence. The doc does not give postural areas or any $A(\\gamma)$
  table. ES-310 also gives only the three-point Pk(KE) anchors (100 J /
  1 kJ / 4 kJ) — there is no posture-resolved Pk in this source.
- **`doc-reference/wound-ballistics/lethality-threshold-critique.md`**
  Fackler 1987 — argues against KE thresholds entirely; says wound
  morphology dominates. Says nothing about presented area.
- **`doc-reference/wound-ballistics/pmc7295711-bone-fragments/`** —
  secondary-fragment bone effects; no body-area model.
- **`doc-reference/fragmentation/`** — Gold (2007 ADA462991, 2017
  PAFRAG), Felix 2020, Mott 1947, Gurney 1947, ML-warhead: all about
  warhead-side physics (V₀, Mott $\\mu$, spray angles). **None gives a
  target vulnerability or posture model.**

There is one critical reference cited *inside* the explosion-fragment-model
bibliography:

> [22] P. M. Cunniff, "A Method to Describe the Statistical Aspects of
> Armor Penetration, Human Vulnerability and Lethality due to
> Fragmenting Munitions," International Symposium on Ballistics, 2014.

This is the canonical engineering source for posture-resolved presented
area and posture-resolved Pk|hit. **It is not in `doc-reference/`.**

Also missing but likely useful:

- **NATO AEP-55 Vol. 2 (KE threats) and Vol. 3 (frag/blast threats)** —
  defines the standard prone/crouching/standing silhouettes and incident
  angle factors used across NATO casualty models.
- **JTCG/ME-77-7 (Joint Technical Coordinating Group / Munitions
  Effectiveness)** — historical primary source for personnel
  vulnerability tables; cited but not collected.
- **Driels, *Weaponeering* (2nd ed., 2013), ch. 12** — textbook
  treatment of personnel area-of-effect with postural multipliers.

If we want a *sourced* w(γ), the librarian should be asked to collect at
least Cunniff 2014 and AEP-55 Vol. 3. Without them, any w(γ) we
introduce is a justified-by-geometry approximation, not a
literature-validated curve.

## 4. Modelling cost

### 4.1 New parameters

| Symbol      | Meaning                 | Unit | Standing   | Prone   | Source needed?   |
| ----------- | ----------------------- | ---- | ---------- | ------- | ---------------- |
| $w\_\\perp$ | body width              | m    | 0.5        | 0.5     | already in model |
| $h$         | vertical extent         | m    | 1.7        | 0.3     | NATO / Cunniff   |
| $d$         | top-down extent (depth) | m    | 0.3        | 1.8     | NATO / Cunniff   |
| `posture`   | enum                    | —    | "standing" | "prone" | n/a              |

Three new scalars total (or one struct per posture). No new integration
dimension — γ is derived from existing $h_b$ and $s$.

### 4.2 Code complexity

- Replace `w_target` scalar with `presented_area(gamma, posture)`
  returning $A_p$ in m² (one helper function, ~10 lines).
- Rewrite eq. (22) factor from
  $w/(2\\pi s \\cdot 2\\sin\\Theta,\\delta)$ to
  $A_p(\\gamma)/(s^2 \\cdot 2\\pi \\cdot 2\\sin\\Theta,\\delta)$ — this is a
  **dimensional change**: we move from "width / arc" to
  "area / spherical-cap-area" = solid-angle fraction. This is actually
  more rigorous (the current width-based formula implicitly assumes the
  target spans the full vertical thickness of the belt $2s\\sin\\Theta,\\delta$,
  which is only true at γ ≈ 0).
- Re-derive eq. (20) so units stay consistent. Sanity check: recover the
  current eq. (22) in the limit $h \\gg d$, γ → 0.

### 4.3 Validation cost

- Limit check: γ = 0, prone posture → $A_p \\to 0.15$ m² (recovers
  current "0.5 m × 0.3 m torso depth" cross-section that the qmd
  Caveat #8 already notes).
- Limit check: γ = 0, standing → $A_p \\to 0.85$ m², larger than current
  $w \\cdot h\_\\text{torso}$ ≈ 0.5 × 0.5 = 0.25 m². The eq. (22) factor
  must be re-normalised so total ground-integrated hits is unchanged in
  the γ → 0 / $h_b → 0$ limit — i.e. the conversion from width-based to
  area-based must conserve the existing $R\_{50}$ at $h_b = 0$. This is
  the most error-prone step.
- Spot check: ground burst (γ ≈ 0) vs airburst at $h_b$ = 10 m,
  cross-range 30 m (γ ≈ 18°). Against prone target the airburst should
  give roughly a $\\sin 18° / \\sin 0° \\to \\infty$ improvement in $A_p$
  — i.e. ground burst is *essentially zero* against prone, airburst is
  finite. This is the qualitative behaviour the model is missing.
- Reproduce a published lethal-area number from a 155 mm M107 against
  prone targets (if one exists in literature we collect).

### 4.4 Risks

1. **Dimensional re-derivation** of eq. (22) is non-trivial — the
   geometry factor changes from $1/s$ to $1/s^2$. Easy to mis-derive;
   the modeler must show the unit check and recover the 1D disk in the
   limit, or the reviewer will (rightly) reject.
1. **Unsourced numbers** for $h$ and $d$ per posture. Either accept as
   "engineering geometry" or block on librarian.
1. **Ground ricochet** — fragments grazing at γ ≈ 0 may bounce up; the
   current model already ignores this and adding a γ profile makes the
   gap more visible (caveat #8.c). Out of scope for this change but
   should be re-flagged.

## 5. Recommendation

**Include in MVP2 of the 3D geometry extension.** Three reasons:

1. **It is the single biggest physical effect missing from §6.** The
   qmd's own "Why $h_b$ doesn't matter much in this model" passage
   (line 1268) explicitly identifies "obliquity-dependent target
   presentation" as the gap blocking a non-trivial optimal $h_b$.
   Without it the model literally cannot answer "why airburst?" which
   is the operational question.
1. **Modelling cost is low** — one helper function, three new
   parameters, one re-derivation of eq. (22). Closed-form. No new
   integral. Computationally free.
1. **Doctrinal credibility** — any defence reader will look for posture
   factors first. Their absence makes the model look like an academic
   toy. Their presence (even with approximate values) makes the model
   credible *and* lets us answer the airburst question directly.

**Pre-requisite before implementation:** ask librarian to collect
**Cunniff 2014** (Int. Symp. Ballistics) and **AEP-55 Vol. 3**. If those
can't be obtained, fall back to Option A with the NATO box-model values
documented as "engineering convention, source not collected" — the qmd
already has this disclosure pattern (cf. Limitation #5 for TM 9-1901).

**Sequencing within MVP2:**

1. (librarian) collect Cunniff 2014 + AEP-55 Vol. 3 if available.
1. (modeler / Derive) re-derive eq. (22) with $A_p(\\gamma)$
   replacing $w$; unit check; recover §6.5 in γ → 0 limit.
1. (modeler / Implement) add `presented_area(gamma, posture)`;
   parameterise sims by posture.
1. (modeler / Validate) ground vs airburst lethal-area sweep for
   standing and prone; expect ~3–5× airburst gain vs prone, ~1× vs
   standing.
1. (model-reviewer) verify dimensional consistency and limit recovery.

**Defer** ground ricochet, body armour, and partial-cover factors —
those are scalar multipliers on $A_p$ that fit cleanly *after* the γ
profile is in place.
