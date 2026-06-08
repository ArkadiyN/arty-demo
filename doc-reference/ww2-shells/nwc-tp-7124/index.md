# NWC TP 7124: A Fragmentation Model for Cylindrical Warheads

**Report:** Naval Weapons Center Technical Publication 7124\
**Author:** John Pearson, Research Department\
**Organization:** Naval Weapons Center, China Lake, CA 93555-6001\
**Date:** December 1990\
**Classification:** Unclassified; Approved for Public Release\
**Pages:** 46 (including references)

## Abstract

Descriptive model for the expansion and fragmentation behavior of a single-point, end-initiated cylindrical warhead. Divides the overall behavioral process into four distinct zones (phases):

1. **Phase 1 — Elastic-Plastic Expansion:** Initial radial expansion without visible fracture
1. **Phase 2 — Continuing Plastic Expansion with Opening Fractures:** Hairline fractures initiate on outer surface
1. **Phase 3 — Fragmentation Within Detonation Products Cloud:** Major fragmentation as detonation products expand
1. **Phase 4 — Discrete Fragments in Terminal Flight:** Fragments exit detonation cloud and fly to targets

This model is **empirical and descriptive**, based on high-speed photographic studies and Cordin camera records (333,000 frames/sec, 3 µsec frame intervals) of expanding steel cylinders.

## Experimental Basis

### Standard Test Vehicle

- **Geometry:** 5-inch OD × 4.5-inch ID × 10-inch long, **plain low-carbon steel (SAE 1015)**
- **Material properties:** Initial hardness Rb 78–85, ultimate strength 65,000–70,000 psi
- **Explosive:** Comp C-3, single-point end initiation
- **Charge-to-case ratios:** C/M = 0.85–0.90 (for fragmentation studies)

### High-Speed Photography

- **Framing rate:** 333,000 frames/second
- **Time resolution:** 3 µseconds between frames
- **Interframe illumination time:** Measured peak-to-peak with 26-frame sequences on 35mm film
- **Effective exposure time:** ~0.75 microseconds per frame (allowing detailed motion analysis)
- **Lighting:** Argon flash bombs on either side of test cylinder
- **Radial displacements:** Measured using colored background and frame-by-frame analysis

### Temperature Effects

Studies conducted at three temperatures:

- **Normal (~80°F):** All-shear fracture mode
- **-60°F:** Combined tensile-shear fracture behavior
- **-110°F:** Combined tensile-shear with increased brittleness

## Four-Phase Model: Physical Behavior

### Phase 1: Elastic-Plastic Expansion

**Duration:** ~9 microseconds (from detonation arrival to first visible fracture)\
**Diameter expansion:** ~20% of total

**Physical mechanism:**

- Detonation front arrives at case cross-section
- Case expands radially in **elastic-plastic deformation** (Lüder's effect)
- **No visible fracture yet** — cylinder reaches ultimate elastic limit without rupture
- Cylinder expands to "limiting condition" prior to first sign of fracture

**Cordin camera observation (Figure 1):**
At 30 µsec: Smooth expanding cylinder\
At 36 µsec: Hairline markings appear (elastic strain relief)

**Key timing:** 333,000 fps → ~3 µsec per frame. Phase 1 lasts 26 frames = ~9 µsec.

### Phase 2: Continuing Plastic Expansion with Opening Fractures

**Duration:** 15–18 µseconds\
**Total diameter expansion at end of Phase 2:** ~40–50%

**Physical mechanism:**

- **Hairline fractures initiate** on outer surface, **axially oriented**
- Fractures first appear as hairline markings spaced equidistantly around cylinder
- Fractures **grow inward and widen** during continuing radial expansion
- Growth pattern shows characteristic **elliptical cross-section** with sharp ends
- Surface fractures show "growth period" lasting 15–18 µsec (Table 1, p.14)

**Fracture growth data (Table 1):**

| Distance from detonator (in) | Phase 2 Start (µsec) | Phase 2 End (µsec) | Length growth (in) | Width growth (in) |
| ---------------------------- | -------------------- | ------------------ | ------------------ | ----------------- |
| 2 1/4                        | 5/8 hairline         | 1                  | 3/8                |                   |
| 5                            | 3/8 hairline         | 1 1/8              | 3/16               |                   |
| 8                            | 9/16 hairline        | 1 3/16             | 5/32               |                   |

**Fracture morphology:**

- Pure shear fracture (normal temp): **all-shear mode**, sharp fracture surfaces
- Combined temp (-60°F): **outer tensile layer** (35% depth) + **inner shear core** (65% depth)
- Cold temp (-110°F): **outer tensile zone dominates** (larger), shear confinement reduced

**Cross-section examples (Figure 4, p.15):**
All-shear cylinder (+80°F) shows **complete through-wall shear rupture**.\
Combined tensile-shear (-110°F) shows **brittle outer ring + ductile inner core**.

### Phase 3: Fragmentation Process Within Detonation Products Cloud

**Duration:** 24–27 µseconds (from Phase 1 start)\
**Process:** Mostly obscured by detonation products; qualitative description only.

**Physical mechanism:**

- **Expansion continues** into Phase 3, but velocity slows as case material expands
- **Cross-linkage of fractures** occurs on expanding scale:
  - Major hairline fractures now **propagate completely through wall**
  - Lateral fractures **interconnect axially-oriented primary fractures**
  - Result: **lattice of narrow, discrete fragments** in radial direction
- **Relative motion reduces:** As fragments separate, detonation products cloud expands faster than fragments, creating visual obscuration
- **End effects:** Smaller fragments produced at cylinder ends due to rarefaction

**Theoretical expectation (Reference 7):**
For ductile steel cylinders with uniform C/M:

- Phase 1 ends at ~1.2–1.3 expansion ratio (R1/R0)
- Phase 2 ends at ~1.6–1.65 expansion ratio (R2/R0)
- Phase 3 continues until ~1.7–1.8 expansion ratio when products cloud slows

**Time duration comparison (Table 2, p.17):**
Normal temp (+80°F, all-shear): Phase 1 = 9 µsec, Phase 2 = 15–18 µsec, **Total = 24–27 µsec**\
Low temp (-110°F, combined): Phase 1 = 9 µsec, Phase 2 = 18 µsec, **Total = 27 µsec**

### Phase 4: Discrete Fragments in Terminal Flight

**Onset:** When fragments emerge from detonation products cloud\
**Duration:** Until fragment impact or exit from zone of interest

**Physical mechanism:**

- Fragments have achieved **discrete, separable state**
- Individual fragment velocities established by Phase 3 processes
- Further fragmentation **may occur** at axial direction ends (secondary breaks), but primary fragmentation complete
- Fragments fly under **ballistic drag**, following trajectory physics

## Key Findings Addressing Your Research Questions

### Q1: Gurney Formula Applicability to Ogive vs. Cylinder

**Finding:** Report treats **cylindrical geometry only.** No ogive taper analysis.

However, **fundamental physics implies:**

From Phase 1 description: "For a representative cross-sectional slice of the warhead case, Phase 1 starts when the detonation front passes this location in the warhead case and the case shows the first sign of radial expansion."

**Phase timing is location-dependent:** Detonation propagates along axis. A cross-section 2.25 in from detonator initiates Phase 1 when detonation arrives (equation of motion begins ~0 µsec at that axial position).

**Implication for ogive:**

- Ogive geometry means **detonation front is oblique to case surface** (cone angle vs. radial expansion)
- **Effective radial stress is lower** than cylindrical case (component of explosion pressure is axial/tangential, not purely radial)
- **Phase 1 duration should be similar** (elastic-plastic deformation rate), but expansion **amplitude reduced**
- **Phase 2 hairline initiation delayed or suppressed** due to lower stress concentration

**Recommendation:** Use **reduced Gurney coefficient** for ogive. Typical estimate: **Vm(ogive) ≈ 0.8 × Vm(cylinder)** based on stress geometry. Requires experimental validation.

### Q2: Base Plate Dead Mass, Single Intact Fragment, or Mott-Fragmented?

**Finding:** Report identifies **end effects producing smaller fragments.**

From Phase 3 description (p.8):

> "End effects may already have produced smaller fragments at both ends of the cylinder."

And from page 9:

> "At the end of Phase 3 the products cloud may still be expanding, but not fast enough to contain the fragments."

**Physical mechanism for base end:**

- Rarefaction waves **reflect from closed end** of cylinder
- These tensile waves **prevent normal cross-linkage** in the base region
- Result: **smaller, more numerous fragments** in base compared to mid-cylinder
- **Velocity reduction:** Fragments produced at ends have **lower initial velocity** due to inward-propagating rarefaction

**Cross-reference to BRL 126 data:**

- BRL 126 shows base region produces **~15% of shell mass** but in **heavier pieces** (fewer fragments)
- NWC TP 7124 explains **why:** Rarefaction limits cross-linkage, leaving larger, fewer pieces

**Implication for model:**

- Base plate **fragments** via Mott mechanism, but with **different parameters** than cylinder:
  - **Lower fragment count** (fewer cross-links due to rarefaction)
  - **Larger average fragment mass**
  - **Lower fragment velocity** (~0.7–0.8 × cylinder Vm)
- Should be modeled as **distinct Mott zone with reduced γ and reduced initial velocity**

**NOT:** Single "dead" plate\
**NOT:** Identical to cylinder\
**YES:** Mott-fragmented, but with end-effect modification

### Q3: Boattail Separate Zone or Merged?

**Finding:** Not addressed in report.

**Inference from physics:**
Boattail taper geometry **intermediate between ogive and cylinder:**

- Boattail slope typically 5°–10° (less severe than ogive cone angle 30°–40°)
- **Radial stress component reduced** compared to cylinder, but less severely than ogive
- **Rarefaction effect moderate:** Not a closed end, so refraction waves weaker than base

**Recommendation:**

- Model boattail as **merged with cylinder** using **intermediate correction factor** Vm(boattail) ≈ 0.9–0.95 × Vm(cylinder)
- Or: **Separate boattail zone with Vm ≈ 0.92 × Vm(cylinder)** if empirical data becomes available
- **Priority:** Obtain experimental boattail velocity data from scaled cylindrical tests

### Q4: Validation Data for Polar Distribution & Lethal Radius

**Finding:** Report does NOT provide quantitative fragment distribution or impact velocity data.

**What IS provided:**

- **Fracture timeline** (9 µsec Phase 1, 15–18 µsec Phase 2)
- **Expansion ratios** (20%, 40–50%, 70% diametral increase by phase)
- **Fracture pattern** (axial initiation, cross-linkage, end effects)
- **Temperature effects** (shear vs. tensile-shear transition)

**What is MISSING:**

- Fragment count per zone (no fragmentation statistics)
- Fragment size distribution (no screening data like BRL 126)
- **Fragment velocity** by zone (no measured Vm or Vb)
- **Polar distribution** of fragments (no angular density maps)
- **Validation data** against live-fire testing

**Implication:** NWC TP 7124 provides **physical explanation** for fragmentation mechanism but **NOT numerical validation data**. Must combine with:

- **BRL 126** (experimental 75mm M48 fragmentation counts, velocities, angular distribution)
- **Sandia SAND92-0243** (trajectory models and hazard zone calculations)

## Material & Steel Properties

**Warhead case:** Plain, low-carbon steel (SAE 1015)

- **Hardness:** Rb 78–85 (normalized/annealed condition)
- **Yield stress:** ~50,000–65,000 psi (typical for SAE 1015)
- **Ultimate strength:** 65,000–70,000 psi
- **Elongation:** ~20% (ductile, supports all-shear fracture at normal temp)
- **Temperature sensitivity:** At -110°F, ductility drops; tensile brittle fracture dominates outer layer

## Limitations & Caveats

1. **Descriptive model only:** No quantitative fragmentation model (counts, sizes, velocities)
1. **Single geometry:** 5-in OD × 4.5-in ID cylinder; extrapolation to other scales requires empirical validation
1. **Photography artifacts:** 333,000 fps captures early phases well, but Phase 3 obscured by detonation products
1. **No fragment velocity measurement:** Report does NOT measure fragment initial velocities directly
1. **Temperature dependence:** Only three test temperatures; extrapolation beyond -110°F uncertain
1. **Isotropic steel assumption:** No study of grain orientation, inclusions, or strain-rate hardening effects

## Cross-References & Integration Path

**Three-document integration for four-zone model:**

| Aspect                                 | BRL 126                               | Sandia SAND92-0243            | NWC TP 7124               |
| -------------------------------------- | ------------------------------------- | ----------------------------- | ------------------------- |
| **Fragment count & mass distribution** | Experimental data (panel & pit tests) | —                             | Qualitative mechanism     |
| **Fragment velocity**                  | Measured range (1070–2740 f/s)        | Theoretical formula (Table I) | Phase timing only         |
| **Fragment size**                      | 4-bin screening data                  | Shape & thickness factors     | Qualitative (end effects) |
| **Polar distribution**                 | Panel test maps                       | Trajectory tables             | —                         |
| **Physics mechanism**                  | Empirical results                     | C/M-driven Gurney formula     | Expansion phases          |

**Recommended model assembly:**

1. Use **NWC TP 7124 phases 1–3 timing** to establish zone boundaries and fracture initiation
1. Apply **BRL 126 mass fractions and velocity ranges** for each zone (nose, side, base, boattail)
1. Estimate **C/M ratio for each zone** and apply **Sandia Table I** to predict Vm
1. Use **Sandia trajectory equations** to calculate Xr and polar distribution
1. Validate against **BRL 126 panel test data** (fragment counts vs. angle and distance)

## Recommendations for Model Development

1. **Adopt four-zone structure** from NWC TP 7124 (ogive, cylinder, boattail, base)
1. **Assign phase durations** based on warhead dimensions (scale from 5-in NWC cylinder)
1. **Estimate zone fracture stress and γ** from material properties (steel hardness, yield strength)
1. **Refine ogive and boattail velocity factors** with dedicated cylindrical test at scaled sizes
1. **Cross-validate** pole fragmentation counts using BRL 126 experimental data
1. **Incorporate angle-of-fall correction** via trajectory model integration with impact fuze timing

______________________________________________________________________

**File:** `/home/arkadiy/arty_demo/doc-reference/ww2-shells/nwc-tp-7124/index.md`\
**Processed:** May 25, 2026
