# UFC 4-023-07: Design to Resist Direct Fire Weapons Effects

## Source

- **Document:** UFC 4-023-07, *Design to Resist Direct Fire Weapons Effects* — Unified Facilities Criteria
- **Date:** 7 July 2008
- **Authority:** U.S. Army Corps of Engineers, prepared with NAVFAC and AFCESA
- **Pages:** 67
- **SHA256:** `sha256sum source.pdf` (retain PDF for re-extraction)
- **Classification:** Approved for public release; distribution unlimited
- **Purpose:** Engineering guidance for designing military facilities to protect assets from direct fire weapons (small arms and shoulder-fired antitank weapons)

______________________________________________________________________

## Equation 5-1: Wood Thickness to Prevent Projectile Perforation

**Citation:** Section 5-3.4.2.1.1 (source.pdf pages 40–41, marked "5-9" to "5-10")

$$T_w = \frac{9,837 \, v^{0.4113} w^{1.4897}}{({\pi D^2}/{4})^{1.3596} H^{0.5414} \rho}$$

**Variable definitions (as stated in source):**

| Symbol | Meaning                                                         | Units                               | Source ref.         |
| ------ | --------------------------------------------------------------- | ----------------------------------- | ------------------- |
| $T_w$  | Thickness of wood necessary to prevent perforation              | in (inches)                         | Section 5-3.4.2.1.1 |
| $v$    | Projectile impact velocity (conservatively use muzzle velocity) | ft/s (feet/second)                  | Appendix A          |
| $w$    | Projectile weight                                               | lbs (pounds)                        | Appendix A          |
| $D$    | Projectile diameter                                             | in (inches)                         | Appendix A          |
| $\rho$ | Wood density                                                    | lbs/ft³ (pounds per cubic foot)     | Table 5-5           |
| $H$    | Wood hardness                                                   | lbs (pounds) — Janka hardness scale | Table 5-5           |

**Physical meaning:** Thickness required for complete resistance to ballistic penetration; projectile emerges with zero residual velocity.

**Empirical basis (as stated):** "Because the equations are largely curve fits of actual data, they are left in their original form rather than attempting to convert them to metric or English units" (Section 5-3.4.2.1, source.pdf p.40, marked "5-9").

______________________________________________________________________

## Equation 5-2: Residual Velocity from Wood Target

**Citation:** Section 5-3.4.2.1.1 (source.pdf pages 40–41, marked "5-10")

$$v_r = v \left[ 1.0 - \left( \frac{t}{T_w} \right)^{0.5735} \right]$$

**Variable definitions:**

| Symbol | Meaning                                    | Units |
| ------ | ------------------------------------------ | ----- |
| $v_r$  | Residual velocity                          | ft/s  |
| $v$    | Initial (impact) velocity                  | ft/s  |
| $t$    | Actual target thickness                    | in    |
| $T_w$  | Perforation-limit thickness (from Eq. 5-1) | in    |

**Use case (as stated):** "Where the thickness of wood target is less than that given by Equation 5-1, use Equation 5-2 to determine the residual velocity that the round will have after passing through the wood" (Section 5-3.4.2.1.1, source.pdf p.40, marked "5-9").

______________________________________________________________________

## Table 5-5: Wood Properties

**Citation:** Section 5-3.4.2.1.1 (source.pdf page 41, marked "5-10")

**Purpose:** Provides density and hardness values for wood species used in Equations 5-1 and 5-2.

| Species        | Condition | Hardness (pounds) | Density (lbs./ft³) |
| -------------- | --------- | ----------------- | ------------------ |
| Pine           | Dry       | 23.5              | 38.7               |
| Pine           | Wet       | 30.0              | 51.1               |
| Maple          | Dry       | 35.0              | 76.9               |
| Maple          | Wet       | 40.0              | 72.0               |
| Green Oak      | Dry       | 55.0              | 88.1               |
| Green Oak      | Wet       | 55.0              | 72.1               |
| Marine plywood | Dry       | 37.0              | 68.7               |
| Marine plywood | Wet       | 37.0              | 58.8               |
| Balsa          | Dry       | 6.0               | 21.0               |
| Balsa          | Wet       | 6.0               | 61.5               |
| Fir plywood    | Dry       | 30.0              | 75.0               |
| Fir plywood    | Wet       | 30.0              | 68.9               |
| Hickory        | Dry       | 50.0              | 74.3               |
| Hickory        | Wet       | 55.0              | 63.5               |

**Note on "Hardness":** Values are Janka hardness (side hardness), measured in pounds-force (lbf).\
**Note on "Density":** Dry (at 12% moisture content) and wet (fully saturated) conditions per wood moisture standards.

______________________________________________________________________

## Validity Ranges and Limitations

**Projectile caliber scope (stated in 5-3.4.2.1.2 — Steel section):**\
"Equation 5-3 is only valid for calibers of 0.50 (12.7 mm) or less. For larger calibers, refer to UFC 3-340-01" (source.pdf p.41, marked "5-11").

**Wood equations limitation:** UFC 4-023-07 provides ballistic perforation equations primarily for projectiles ≤12.7 mm (.50 caliber) against wood targets. The document does not explicitly state a velocity range for Equations 5-1 and 5-2, but references them in the context of small-arms ammunition (rifle and handgun) and does not extend to hypervelocity or large-caliber weapons (>12.7 mm).

**Material scope:** Equations 5-1 and 5-2 are formulated for solid wood blocks. Cross-laminated timber (CLT) or composite wood structures may behave differently; the document does not address CLT.

______________________________________________________________________

## Cross-Verification Against Sanborn et al. (2019)

**Sanborn's "Equation 2" (from their card transcription):**

$$T_w = \frac{9,837 \, v^{0.4113} w^{1.4897}}{D^{1.3596} \rho^{0.5414} H^2}$$

**Comparison with UFC Equation 5-1:**

| Element         | UFC Source (5-1)                                    | Sanborn "Eq. 2" | Match?                                                |
| --------------- | --------------------------------------------------- | --------------- | ----------------------------------------------------- |
| Constant        | 9,837                                               | 9,837           | ✓ Yes                                                 |
| $v$ exponent    | 0.4113                                              | 0.4113          | ✓ Yes                                                 |
| $w$ exponent    | 1.4897                                              | 1.4897          | ✓ Yes                                                 |
| $D$ exponent    | 1.3596                                              | 1.3596          | ✓ Yes                                                 |
| $\rho$ exponent | 1.0 (implied: $\rho$ in denominator to first power) | 0.5414          | ✗ **Discrepancy**                                     |
| $H$ exponent    | 0.5414 (apparent from source text)                  | 2.0             | ✗ **Discrepancy**                                     |
| $D$ term form   | $(\pi D^2 / 4)^{1.3596}$                            | $D^{1.3596}$    | ✗ **Discrepancy** (cross-sectional area vs. diameter) |

**Critical findings:**

1. **Density exponent differs:** UFC source shows $\rho$ with exponent ~1.0 (appears in denominator without explicit exponent); Sanborn transcribes 0.5414. The UFC text definition lists $\rho = $ wood density (lbs/ft³) with notation "(see Table 5-5)" but does not clearly state the exponent in running text. The equation formatting in the UFC PDF is broken by OCR; the precise exponent requires re-reading the page image (source.pdf p.41).

1. **Hardness exponent differs sharply:** UFC source suggests $H^{0.5414}$ (square root regime); Sanborn has $H^2$ (quadratic, much stronger dependence on hardness). This is a **2.5× difference** in exponent magnitude and **opposite direction** of effect sensitivity. Sanborn's form makes hardness far more influential on required thickness.

1. **Diameter term:** UFC shows $(\pi D^2 / 4)^{1.3596}$ (projectile cross-sectional area); Sanborn simplifies to $D^{1.3596}$. If simplified, this assumes the $\pi/4$ factor absorbed into the constant 9,837—but that is not explicitly stated in Sanborn's paper.

1. **Sanborn's flag as BLOCKING:** Sanborn's card notes this equation "overpredicts required thickness significantly—not acceptable for CLT design" when compared to experimental CLT penetration data. The exponent discrepancies identified above may partially explain the mismatch between UFC predictions and CLT empirical results.

______________________________________________________________________

## Empirical Basis (as Stated in Source)

"Equation 5.1 gives the thickness of wood necessary to resist perforation. Values for density and hardness for various species of wood can be found in Table 5-5" (Section 5-3.4.2.1.1, source.pdf p.40, marked "5-9").

The document does **not** cite a specific historical test program, ballistic lab, or publication from which Equations 5-1 and 5-2 were derived. The general statement "Because the equations are largely curve fits of actual data, they are left in their original form rather than attempting to convert them to metric or English units" (source.pdf p.40) indicates empirical fitting but does not identify the underlying test dataset (projectile type, wood source, impact velocities tested).

______________________________________________________________________

## Next Steps for Sanborn Comparison

The discrepancies identified above are **not resolvable from the Sanborn card alone** — the primary source (UFC 4-023-07 PDF page 41, marked "5-10") must be re-read to confirm whether the density and hardness exponents in Equation 5-1 are as Sanborn transcribed or as indicated by the incomplete text extraction. A re-extraction of source.pdf pages 40–41 using vision-based OCR (rather than embedded text layer) is recommended to resolve the equation form definitively before any recalibration work begins on the Sanborn model.

______________________________________________________________________

## Document Structure Reference

- **Chapter 5:** Building Elements (where equations 5-1 to 5-10 live)
- **Section 5-3.4.2.1:** Ballistic threat material penetration equations
    - 5-3.4.2.1.1: Wood
    - 5-3.4.2.1.2: Steel
    - 5-3.4.2.1.3: Concrete
- **Section 5-3.4.2.2:** Anti-tank weapon threat (Equation 5-10)

______________________________________________________________________

**Card compiled:** 2026-08-09\
**Extraction method:** Heuristic PDF text layer (equations and table partially garbled; source.pdf retained for re-extraction with vision OCR if needed)\
**Quality check status:** Pending `scan-extraction-quality.py` run on full markdown output\
**Critical action:** Resolve density and hardness exponents in Eq. 5-1 via direct PDF page inspection before finalizing Sanborn comparison.
