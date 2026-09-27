# Martineau 1998 — Viscoplastic Model of Expanding Cylindrical Shells

**Source:** Los Alamos National Laboratory Technical Report LA-13424-T (April 1998)\
**Author:** Rick L. Martineau, Colorado State University / Los Alamos National Laboratory\
**Title:** A Viscoplastic Model of Expanding Cylindrical Shells Subjected to Internal Explosive Detonations (page 1)\
**Blob:** `source.pdf` (178 pp., scanned images); partial verification from pages 1, 54, 72–90\
**DOI:** https://doi.org/10.2172/663184\
**Issued:** April 1998 (page 1)\
**Report Number:** LA-13424-T, UIC-741

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

**Experimental Setup & Material (section 4.1, verified from page 81, printed page 66):**

- **Shell material:** Alloy 101 OFE copper, 99.99% pure (page 81, section 4.1; anchor: "Alloy 101 OFE copper is 99.99% pure copper")
- **Initial grain size:** 35–40 μm (page 81, section 4.1; anchor: "initial grain size in the copper tubing was 35-40 μm")
- **Initial hardness:** Rockwell F scale 80; heat-treated to 350°C for 60 min, reducing hardness to Rockwell F 23 (page 81, section 4.1; anchor: "After 60 minutes, the hardness of the material was now 23 on the Rockwell F scale")

**Diagnostic Equipment & Measurement Methods (verified from pages 88–89, printed pages 73–74):**

- **Fast framing camera:** frame interval time 2.257 microseconds, 23 images recorded for each experiment (page 89, section 4.4; anchor: "frame interval time of 2.257 microseconds were recorded")
- **Fabry-Perot interferometry:** measurement point located "exactly halfway up the cylinder at 20.32 cm" (page 88, section 4.4; anchor: "measurement point for the Fabry-Perot was located exactly halfway up the cylinder at 20.32 cm")
- **Experimental issue:** For thicker cylinder, Fabry-Perot equipment had hardware failure; only framing camera data available (page 89, section 4.4; anchor: "Fabry-Perot equipment experienced a hardware failure and as a result, was not able to record data")

## Unverified (from OSTI abstract only, not yet confirmed in source pages read)

The following claims appear in OSTI metadata but have not been verified against the actual source pages:

- Model expands shells to >200% strain at 10⁴ s⁻¹ strain rates
- Quasi-periodic instability patterns develop on shell surfaces, oriented ~45° from radial direction
- Mie-Gruneisen equation of state is used (OSTI abstract; not found in pages 54, 73–90 read)
- ABAQUS/Explicit implementation with lagrangian updating (OSTI abstract; not found in pages 54, 73–90 read)

FINDING\[note\]: Mie-Gruneisen EOS and ABAQUS/Explicit are sourced here only from the OSTI abstract; the scan has no text layer and neither was found on PDF pp. 54, 73-90 read visually 2026-09-26 (affects: doc-reference/fragmentation/martineau1998-viscoplastic-shell-expansion/card.md; since: 2026-09-26)

**Johnson-Cook yield surface:** Verified present in Table 3.2 (page 74, printed page 59; anchor: "Johnson-Cook Strength Model") as a constitutive model component alongside GTN.

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

- **`source.pdf`:** `/mnt/f/Projects/TMP/Docs/663184.pdf` (blob store); `sha256: bfbdcaf4c1956bb08dccc597b094ad49b0c43423ab136c0045d933c1c2365a72`.

- **Document:** Rick L. Martineau, *A Viscoplastic Model of Expanding Cylindrical Shells Subjected to Internal Explosive Detonations*, Los Alamos National Laboratory Technical Report LA-13424-T, April 1998, DOI https://doi.org/10.2172/663184 (verified anchor "A Viscoplastic Model of Expanding Cylindrical Shells" — `card.md:5`, title page = report p.1).

- **Retained source:** Partial extraction only — `martineau1998-viscoplastic-shell-expansion-section57-58.md` (vision-extracted sections 5.7–5.8, pages 103–105 printed pages 88–90). The full PDF is in the blob store (line above), but only sections 5.7–5.8 have a processed extraction.

- **Extraction method:** Scanned document (178 pp., OCR-untrusted); sections 5.7–5.8 extracted via vision API.

- **Visual verification (2026-09-26):** Pages cited in "Verified from Source Pages" section verified directly against PDF pages rendered as PNGs. GTN model and equation 2.50 confirmed on page 54 (printed p. 39). Material properties (Alloy 101 copper, grain size, hardness) found and verified on page 81 (printed p. 66), not page 73 as originally claimed — page citations corrected. Diagnostic equipment and measurement methods verified on pages 88–89 (printed pp. 73–74), matching the pages 87–89 range cited. Johnson-Cook model component verified in Table 3.2 on page 74 (printed p. 59). Mie-Gruneisen equation of state not found in pages 54, 73–90.

- **Verified anchor (retained sections only):** "Table 5.3 indicate the calculated values of the Gurney velocity" — `martineau1998-viscoplastic-shell-expansion-section57-58.md:13` (section 5.7, page 103 printed page 88).

- **Secondhand note:** The "Gurney Maximum Velocity Predictions" and equation 6.1 in the retained extraction directly quote/reproduce Kennedy 1970 Gurney forms — not secondhand (Martineau applies them), but the originality claim rests with Kennedy, not this source.
