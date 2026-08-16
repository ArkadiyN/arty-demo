# Martineau 1998 — Viscoplastic Model of Expanding Cylindrical Shells

**Source:** Los Alamos National Laboratory Technical Report LA-13424-T (April 1998)\
**Author:** Rick L. Martineau, Colorado State University / Los Alamos National Laboratory\
**Title:** A Viscoplastic Model of Expanding Cylindrical Shells Subjected to Internal Explosive Detonations (page 1)\
**Blob:** `source.pdf` (178 pp., scanned images); partial verification from pages 1, 54, 72–90\
**DOI:** https://doi.org/10.2172/663184\
**Issued:** April 1998 (page 1)\
**Report Number:** LA-13424-T, UIC-741

FINDING\[deferrable\]: source.pdf not retained in doc-reference/fragmentation/martineau1998-viscoplastic-shell-expansion/ — only partial extraction (sections 5.7-5.8, pages 103-105) kept; card claims verification from pages 54, 73-75 which are not in retained files (affects: doc-reference/fragmentation/martineau1998-viscoplastic-shell-expansion; since: 2026-08-16)

## Verified from Source Pages

**Title page (page 1):** Confirms "A Viscoplastic Model of Expanding Cylindrical Shells Subjected to Internal Explosive Detonations" by Rick L. Martineau; issued April 1998; Los Alamos National Laboratory; unlimited distribution.

**Constitutive Model Components (verified from page 54):**

- **Gurson-Tvergaard-Needleman (GTN) yield model** (page 54, text confirms: "this model has been referred to as the Gurson-Tvergaard-Needleman (GTN) model")
- **Yield criterion** (page 54, equation 2.50):
    $$\phi = \left(\frac{\sigma}{\sigma_f}\right)^2 + 2q_1 f^* \cosh\left(\frac{3q_2 P}{2\sigma_f}\right) - (1 + q_3 f^{*2}) = 0$$

where:

- $\sigma = \sqrt{\frac{3}{2}S_{ij}S_{ij}}$ is effective Mises stress (eq. 2.51)
- $S_{ij} = \sigma_{ij} - \frac{1}{3}\sigma_{ij}\delta_{ij}$ is deviatoric stress (eq. 2.52)
- $P = -\frac{1}{3}\sigma_{ii}$ is hydrostatic pressure (eq. 2.53)
- $\sigma_f$ is flow stress, $q_1, q_2, q_3$ are material parameters
- $f^*$ is damage parameter (void fraction, modified for coalescence)

**Experimental Setup & Material (verified from pages 73–75, 87–89):**

- **Shell material:** Alloy 101 OFE copper, 99.99% pure (page 73, text: "Alloy 101 OFE copper is 99.99% pure copper")
- **Initial grain size:** 35–40 μm (page 73, text: "initial grain size in the copper tubing was 35-40 μm")
- **Initial hardness:** Rockwell F scale 80 (page 73); heat-treated to 350°C for 60 min, reducing hardness to Rockwell F 23 (page 73)
- **Measurement methods** (verified from section 4.4, pages 74–75):
    - Fast framing camera: frame interval time 2.257 microseconds, 23 images recorded for each experiment (page 74)
    - Fabry-Perot interferometry: measurement point located "exactly halfway up the cylinder at 20.32 cm" (page 73)
    - **Experimental issue:** For thicker cylinder, Fabry-Perot equipment had hardware failure; only framing camera data available (page 74, text: "The Fabry-Perot equipment experienced a hardware failure and as a result, was not able to record data")

**Results — Expansion Sequence (verified from page 75, Figure 4.7):**

- **Experimental observation:** Frame-by-frame images of thin cylinder expansion (Figure 4.7, page 75, caption: "Framing Camera Images for the Thin Cylinder (Times in Microseconds)")
- **Time range observed:** 0.0 to 49.654 microseconds
- **Frame times (microseconds, extracted from Figure 4.7):**
    - 0.0, 2.257, 4.514, 6.771, 9.028
    - 11.285, 13.542, 15.799, 18.056, 20.313
    - 22.57, 24.827, 27.084, 29.341, 31.598
    - 33.855, 36.112, 38.369, 40.626, 42.883
    - 45.14, 47.397, 49.654

## Unverified (from OSTI abstract only, not yet confirmed in source text)

The following claims appear in OSTI metadata but have not yet been verified against the actual source pages:

- Model expands shells to >200% strain at 10⁴ s⁻¹ strain rates
- Quasi-periodic instability patterns develop on shell surfaces, oriented ~45° from radial direction
- Mie-Gruneisen equation of state is used (referenced in OSTI, confirmed model type on page 54)
- Johnson-Cook yield surface is used (OSTI abstract names it; page 54 confirms GTN model, which may include JC, not explicitly verified yet)
- ABAQUS/Explicit implementation with lagrangian updating
- "Strong correlation between numerical results and experimental data"

## Sections 5.7–5.8: Radial Velocity Results (Extracted 2026-08-09)

**Gurney Maximum Velocity Predictions (from Table 5.3, page 103, printed page 88):**

| Shell Thickness | M/C Ratio | V_max (m/s) |
| --------------- | --------- | ----------- |
| 2.54 mm         | 0.498     | 2902        |
| 5.08 mm         | 1.02      | 2351        |

**Governing Equation (page 103, equation 6.1):**\
Gurney equation: $V_{\max} = \sqrt{2E\left(\frac{M}{C} + \frac{1}{2}\right)^{-1/2}}$ where $\sqrt{2E} = 2900$ m/s for PBX-9501.

**Figure 5.7: Radial Velocity vs Time for 2.54 mm Cylinder (source.pdf p.104, printed p.89):**

- Time range: 0–40 microseconds
- Velocity range: 0–3000 m/s
- Three curves: Numerical Results (solid), Gurney Velocity (dashed ~2900 m/s), Experimental Data (Fabry-Perot, solid with markers)
- Acceleration phase: 25–30 μs
- Peak velocity reached: ~2750–2800 m/s
- **Finding:** Excellent agreement between experimental (Fabry-Perot) data and numerical model through acceleration phase; both plateau below Gurney prediction

**Figure 5.8: Radial Velocity vs Time for 5.08 mm Cylinder (source.pdf p.104, printed p.89):**

- Time range: 0–65 microseconds
- Velocity range: 0–2500 m/s
- Two curves: Numerical Results (solid), Gurney Velocity (dashed ~2350 m/s)
- *No experimental data:* Fabry-Perot equipment hardware failure (noted page 103–104)
- Acceleration phase: ~50 microseconds (longer than thin cylinder due to increased mass ratio M/C = 1.02)
- Peak velocity reached: ~2300–2350 m/s
- **Finding:** Numerical model aligns with Gurney prediction for thick cylinder

**Table 5.4: Instability Count (source.pdf p.105, printed p.90):**

- 2.54 mm cylinder: 298 instabilities (circumferential, from framing camera)
- 5.08 mm cylinder: 343 instabilities

**Text statements on agreement (source.pdf p.104–105, printed p.89–90):**

- "Figures 5.7 and 5.8 show the velocity of the cylinder wall for the 2.54 and 5.08 mm thick cylinders" (p.104)
- "The plots shown in Figure 5.7 include the velocities from the empirical Gurney equation, the Fabry-Perot instrumentation, and the numerical model" (p.104)
- "The plots shown in Figure 5.8 only include the velocities from the empirical Gurney equation and the numerical model" (p.104)
- "However, good agreement with the available data is shown in both figures" (p.104)
- "In Figures 5.7, excellent correlation exists between the radial velocity obtained from the experimental data and the predictions from [model]" (p.105)

**Full extraction:** See `martineau1998-viscoplastic-shell-expansion-section57-58.md` for complete transcription of sections 5.7–5.8, including equation derivation, table structure with all columns (Mass of HE, Mass of Shell, M/C ratio), and extended discussion through Figure 5.8 validation.

## Provenance of this card

- **Document:** Rick L. Martineau, *A Viscoplastic Model of Expanding Cylindrical Shells Subjected to Internal Explosive Detonations*, Los Alamos National Laboratory Technical Report LA-13424-T, April 1998, DOI https://doi.org/10.2172/663184 (verified anchor "A Viscoplastic Model of Expanding Cylindrical Shells" — `card.md:5`, title page = report p.1).
- **Retained source:** Partial extraction only — `martineau1998-viscoplastic-shell-expansion-section57-58.md` (vision-extracted sections 5.7–5.8, pages 103–105 printed pages 88–90). **`source.pdf` not retained** — only sections 5.7–5.8 can be re-verified. **Card claims in "Verified from Source Pages" (lines 11–48) cite pages 54, 73–75, 87–89; these pages are not in retained extraction files and cannot be re-verified.**
- **Extraction method:** Scanned document (178 pp., OCR-untrusted); sections 5.7–5.8 extracted via vision API. Material property claims (Alloy 101 copper, grain size, hardness) span pages 73–75, constitutive model claims span page 54 — **these sections not retained and not re-verifiable against current artifact**.
- **Verified anchor (retained sections only):** "Table 5.3 indicate the calculated values of the Gurney velocity" — `martineau1998-viscoplastic-shell-expansion-section57-58.md:13` (section 5.7, page 103 printed page 88).
- **Secondhand note:** The "Gurney Maximum Velocity Predictions" and equation 6.1 in the retained extraction directly quote/reproduce Kennedy 1970 Gurney forms — not secondhand (Martineau applies them), but the originality claim rests with Kennedy, not this source.
