---
title: Extension of the Gurney Equations to Two Dimensions for a Cylindrical Charge
authors: Benjamin A. Breech
date: 2011-03-01
origin: DTIC ADA540284 / ARL-TR-5467
pages: 21
---

## Source

**DTIC Accession:** ADA540284\
**Title:** Extension of the Gurney Equations to Two Dimensions for a Cylindrical Charge\
**Author:** Breech, Benjamin A. (U.S. Army Research Laboratory, Weapons & Materials Research Directorate)\
**Date:** March 2011\
**Pages:** 21\
**SHA256:** (retained in source.pdf, gitignored)

## Key Contribution

Extends 1D Gurney equations to 2D cylindrical charge with top/bottom plates. Assumes uniform acceleration of detonation products and derives explicit velocity formulas for radial (shell) and axial (plate) fragments.

## Velocity-During-Expansion: Linear Profile Model

**Yes, source provides explicit velocity profile during expansion as function of radial and axial position.**

### 1. Cylindrical Charge Only (Section 2.1, Eq. 1)

Linear velocity profile in radial direction:

```
v(r) = (r/R) * v_s
```

**Where:**

- r = radial position from center axis (0 ≤ r ≤ R)
- R = cylinder radius
- v_s = gas velocity at shell (radius R)

**Interpretation:** Blast wave originates at r=0 with zero velocity, reaches maximum v_s at the shell (r=R). Intermediate velocities scale linearly with radius.

**Section 2.1, lines 107-111:**\
"The blast wave accelerates gases outward. We take the velocity of the gases when they reach the shell to be vs. The blast then fragments the shell and pushes the fragments outward. We will assume the fragments move at the same velocity as the gases, i.e., vs."

**Kinetic energy integral** (Eq. 2):

```
T_c = (1/2) * C/2 * v_s²
```

Derived by integrating (1/2)ρv²(r) over charge volume with linear profile.

### 2. 2D Cylindrical with Top/Bottom Plates (Section 3, Eq. 12)

Combines radial and axial components:

```
v(r,z) = (r/R) * v_s * r̂ + [(v₁ + v₂) * z/H - v₂] * ẑ
```

**Where:**

- r, z = cylindrical coordinates (r radial, z axial)
- R = cylinder radius, H = cylinder height
- v_s = radial velocity at shell
- v₁ = axial velocity of top plate (z=H)
- v₂ = axial velocity of bottom plate (z=0)
- Minus sign on v₂ because bottom plate moves opposite direction

**Section 3, lines 287-297, Figure 3:**\
"As before, we assume the blast pushes gases outward with a velocity that varies linearly. In the radial direction, the velocity varies with distance from the center line. Along the height of the cylinder, the velocity varies linearly between −v₂ and v₁."

### 3. Time Evolution of Expansion State

**Section 3.1, "Relating v1 to vs"** ("One approach to relate v1 and vs is to assume the detonation wave accelerates the gases uniformly"):

Assumes **uniform acceleration a** of gases during detonation:

```
v_s = a * t_s                           (Eq. 16a)
R = (1/2) * a * t_s²                    (Eq. 16b)
```

**Solving for acceleration:**

```
a = v_s² / (2R)
```

**For axial direction:** Detonation point at z=z₀ where v_z(z₀) = 0:

```
z₀ = [v₂ / (v₁ + v₂)] * H
```

Distance gases travel upward to top plate: H - z₀. With same acceleration a:

```
v₁ = a * t₁
H - z₀ = (1/2) * a * t₁²
```

**Relation between axial and radial velocities** (Eq. 22):

```
v₁² = (H/R) * [(A+1)/2] * v_s²
```

Where A = [1 + 2(M₁/C)] / [1 + 2(M₂/C)] (from momentum conservation, Eq. 13)

**Constraint:** This assumes uniform acceleration in all directions. Time to reach shell and plates is **not explicitly parametrized** — the relation is implicit in the assumption that same acceleration governs both radial and axial motion.

## Terminal Fragment Velocities

Section 3, Equations 23-25 give terminal velocities of shell and plates in closed form:

**Shell (radial) velocity:**

```
v_s = √(2E) * √(α_s)  where  α_s⁻¹ = [coefficient function of geometry and masses]
```

**Top plate velocity:**

```
v₁ = √(2E) * √(α₁)
```

**Bottom plate velocity:**

```
v₂ = √(2E) * √(α₂)
```

(Full expressions in source Eqs. 23-25, p.8-10)

## Limitations and Applicability

**Section 3.3, "Discussion of Differences and Limitations" (lines 565-575):**

Method assumes:

1. Uniform acceleration throughout expansion
1. Detonation point at center axis (azimuthal symmetry)
1. No reflection or deflection of gases after impact

**Stated validity range:** Most reliable when **H ≈ 2R** with equal top/bottom plates (symmetric sandwich component).\
"The most applicable cylindrical charge configuration for this method is one where the height is twice the radius, a detonation point located at the center (e.g., r = 0,z = H/2) and whose top and bottom plates have the same mass."

Expected to remain reasonable for H moderately different from 2R (up to ~3-4R, uncertain). Breaks down for H >> R or H \<< R where gas dynamics cannot maintain uniform acceleration assumption.

## Comparison with Tie-peng et al. Method

Section 3.2 compares with alternative 2D derivation that assumes detonation wave reaches top plate and shell at **same time** (not Breech's uniform-acceleration assumption).

**Key difference:** Tie-peng requires pressure-dependent factors; Breech's uniform-acceleration approach avoids difficult-to-measure pressures.

**Agreement condition:** When H = 2R and M₁ = M₂, both methods give identical result (Eq. 30).

## Not in Source

- No time-dependent trajectory r(t) or z(t) for fragment motion
- No explicit v(time) for fragments after leaving charge
- Velocity profile (Eq. 1, Eq. 12) applies during detonation phase only; assumes fragments move at gas velocity once contacted

## Provenance of this card

- **Document:** Breech, Benjamin A., *Extension of the Gurney Equations to Two Dimensions for a Cylindrical Charge*, Technical Report ARL-TR-5467, March 2011 (DTIC Accession ADA540284; 21 pages; U.S. Army Research Laboratory, Weapons & Materials Research Directorate).
- **`source.pdf`:** NOT RETAINED in directory — was never downloaded after extraction.
- **Extraction method:** PDF with vision processing applied; `ADA540284.md` includes image references (though images referenced with `.jpx` extension suggest an extraction tool artifact). All quoted anchors verified by `grep` against `ADA540284.md`.
- **Key verified anchors:**
    - "The blast wave accelerates gases outward. We take the velocity of the gases when they reach the" — `ADA540284.md:107`, Section 2.1, 1D velocity profile derivation
    - "we will assume the fragments move at the same velocity as the gases, i.e., vs" — `ADA540284.md:111`, same section
    - "As before, we assume the blast pushes gases outward with a velocity that varies linearly" — `ADA540284.md:287`, Section 3, 2D cylindrical extension
- **No numeric data tables in source:** All equations are analytical derivations with symbolic parameters (velocity, mass, radius). No numeric values are tabulated; validity claims are stated qualitatively (e.g., "most reliable when H ≈ 2R"). Fragment from this source cannot fail a closure invariant because no invariant-checkable numeric series is presented.
- `FINDING[deferrable]: source.pdf should be retained per .claude/rules/source-data-fidelity.md § "Retain the source blob" (affects: doc-reference/fragmentation/ada540284-gurney-2d-extension/; since: 2026-08-16)`
