---
title: Picatinny Arsenal Cylinder Expansion Test and Mathematical Examination of the Expanding Cylinder
authors: Brian Edward Fuchs
date: 1995-10-01
origin: DTIC ADA300526 / ARAED-TR-95014
pages: 33
---

## Source

**DTIC Accession:** ADA300526\
**Title:** Picatinny Arsenal Cylinder Expansion Test and a Mathematical Examination of the Expanding Cylinder\
**Author:** Fuchs, Brian E.\
**Date:** October 1995\
**Pages:** 31\
**SHA256:** `99b97a2989c770127fb272726978bf722c835f1ba12a56df94a1ea2c3fbc05d8`

## Key Contribution

Experimental cylinder expansion test methodology using streak camera to record wall motion vs. time, with polynomial fitting for velocity estimation. Develops modified Gurney equation accounting for wall thinning during expansion ("Gurney Relationship for Thick Cylinders").

## Velocity-vs-Expansion-State Relation

**Does NOT provide explicit analytical function.** Instead, provides measurement and analysis methodology:

1. **Position-time measurement** (Section "Analysis", line 169-170):\
    "The streak photograph records the position of the wall with time (fig. 4). By scaling the photograph, the position time history in full scale is obtained."

1. **Polynomial fitting** (Section "Analysis", source.pdf p.6 / "The second program analyzes the scaled data"):\
    "This program performs a least-mean-square that fits the data to a fourth order polynomial."\
    Fitted form: `r(t) = a₀ + a₁t + a₂t² + a₃t³ + a₄t⁴`

1. **Velocity by differentiation** (Same section):\
    "From the differential of the fitted equation, the velocity can be obtained at any point in time up to break-up."\
    Result: `v(t) = a₁ + 2a₂t + 3a₃t² + 4a₄t³`

1. **Volume expansion ratio** computed from measured radius (Appendix, line 371):\
    `volexp[i] = (π(r_outer(t)² + r_outer,initial²) - π*r_inner,initial²) / (π*r_inner,initial²)`

**Implicit relation available:** Velocity can be expressed as function of expansion ratio via the polynomial fit, but source does not provide closed-form analytical expression. Velocity evolution is *data-dependent* (specific to each test).

## Modified Gurney Equation (Wall-Thinning Correction)

**Section: "Gurney Relationship for Thick Cylinders"** (p.12-14, Eq. 22)

Standard Gurney assumes constant wall velocity. This derivation accounts for radial velocity variation due to wall thinning via conservation of mass:

```
V = √(2E) / √[1 + (1/2) * (C/M)_initial * 
    (ln(r_outer/√(r_outer² - r_inner²)) + 1/4) / 
    (ln(r_outer_initial/√(r_outer_initial² - r_inner_initial²)) + 1/4)]
```

Simplified form (Eq. 22) written as function of outer radius r_o and initial conditions:

```
V = √(2E) * √[(r_o² - r_i²)_initial / (r_o² - r_i²)_current] / 
    √[1 + (1/2) * (C/M)_initial * (r_o²_initial - r_i²_initial) / 
      (r_o² - r_i²)_current * (ln(...) terms)]
```

Velocity is function of **instantaneous outer radius**, not time explicitly. Wall-thinning effect is **largest at early expansion** (Figure 7, showing ratio of modified to conventional Gurney decreasing with expansion ratio).

## Measurement & Analysis Method

**Geometry tested:** Picatinny Arsenal cylinder — reduced scale

- Inner diameter: 3/4 in (19.05 mm)
- Outer diameter: ~1 in (25.4 mm)
- Length: 10 in (254 mm)
- Charge-to-mass ratio: ~0.25

**Measurement technique:** Streak camera

- Writing rate: 1 mm/μs
- Position resolution: ~100-200 readings per test

**Velocity extraction:** Least-mean-square polynomial fit (4th order) to raw position-time data, differentiated to yield velocity.

## Momentum and Kinetic-Energy Averaging

Wall velocity varies radially due to conservation of mass (inner wall moves faster). Section "Momentum Average Velocity" and "Kinetic Energy Average Velocity" (Eqs. 9, 15) provide relations for radially-averaged velocities as fractions of outer-wall velocity. For expansions of interest (~2-7 volume ratios), these averages approach outer-wall velocity.

## Not in Source

- No explicit time-dependent formula for velocity during expansion
- No analytic closure form for v(expansion_ratio) independent of specific test data
- Terminal velocity (constant velocity region) treated separately

## Provenance of this card

- **Document:** Fuchs, Brian E., *Picatinny Arsenal Cylinder Expansion Test and a Mathematical Examination of the Expanding Cylinder*, Technical Report ARAED-TR-95014, October 1995 (DTIC Accession ADA300526; 31 pages).
- **`source.pdf`:** NOT RETAINED in directory — was never downloaded after extraction.
- **Extraction method:** OCR scanning of DTIC source PDF; `ADA300526.md` is the full-document transcription. All quoted anchors verified by `grep` against `ADA300526.md`.
- **Key verified anchors:**
    - "The streak photograph records the position of the wall with time" — `ADA300526.md:219`, Section "Analysis"
    - "This program performs a least-mean-square that fits the data to a fourth order polynomial" — `ADA300526.md:222`, same section
    - "From the differential of the fitted equation, the velocity can be obtained at any point in time" — `ADA300526.md:222`, same section
- **Limitation:** No numeric data tables in source; all method is descriptive. Fragment from this source cannot fail a closure invariant because no invariant-checkable series is tabulated.
- \`FINDING\[deferrable\]: source.pdf should be retained per .claude/rules/source-data-fidelity.md § "Retain the source blob" (affects: doc-reference/fragmentation/ada300526-picatinny-cylinder-test/; since: 2026-08-16)
