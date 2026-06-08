# Sandia SAND92-0243: Fragment Hazard Zone Analyses for Explosive Test Facilities

**Report Number:** SAND92-0243, UC-742\
**Author:** Manuel G. Vigil, Explosive Components Division\
**Organization:** Sandia National Laboratories, Albuquerque, NM 87185-5800\
**Date:** Printed May 1992\
**Classification:** Unlimited Release\
**Pages:** 63 (includes appendices with 10+ figures)

## Abstract

Analytical procedures for establishing fragment hazard zones for explosive test facilities. Presents graphical solutions for fragment trajectories resulting from cased explosive configurations. Fragment trajectory parameter data for three different fragment materials (aluminum, steel, tantalum) at velocities 0.6 mm/µs (2000 ft/sec) to 4.3 mm/µs (14,000 ft/sec).

## Scope & Purpose

This report addresses the problem of **determining safe distances or hazard zones for explosive test facilities** by calculating fragment trajectories from explosively driven casings. Methodology is demonstrated on the Sandia National Laboratories Area 2 explosive test facility.

Key design question: Given a cased explosive charge with known initial fragment velocity, effective thickness, and shape factor, what is the maximum horizontal range and hazard radius?

## Core Physics: Fragment Trajectory Model

### Fragment Initial Velocity

For **symmetric sandwich cased explosive configuration:**

$$Vm/Vg = 1/(0.5 + (C/M))^{0.5}$$

where:

- Vm = actual fragment velocity (cm/µs, ft/sec)
- Vg = Gurney characteristic velocity (cm/µs, ft/sec)
  - Vg = (2E)^0.5, E = Gurney energy (kJ/kg)
- C = explosive weight (g)
- M = casing/fragment weight (g)
- *For very thin casing: Vm approaches (1.41) × Vg*

### Fragment Geometry Factors

Two critical parameters affecting trajectory:

**Fragment Shape Factor (Re):**
$$Re = \\text{min-to-max frontal projects area ratio}$$
or
$$Re = \\text{fragment edge area / face area}$$

Typical ranges: 0 to 1.0 (assumed tumbling plate-like fragments)

**Fragment Effective Thickness Factor (Sf):**
$$Sf = \\text{Actual Volume / Maximum Frontal Projected Area}$$
or
$$Sf = \\text{Actual Volume / Face Area}$$

Typical ranges: 0 to 0.5

### Maximum Horizontal Range (Xr)

$$Xr = 0.5 W Z_t$$

where:
$$W = K Q$$
$$K = 0.262(Rhop) Sf / [Cd(Rhoa)(Re + 1)]$$
$$Q = COS(B)$$
$$Z_t = 3.474 [LOG\_{10}(F+1)]^{0.879}$$
$$F = 2(R) SIN(B)$$
$$R = Vb^2/(K)(g)$$

and:

- Rhop = fragment density (g/cc)
- Rhoa = air density (g/cc)
- Cd = drag coefficient (1.0 to 1.71 typical)
- B = launch angle (optimum ≈ 20–30° for maximum range)

### Ambient Conditions (SNL Baseline)

- Air density (Rhoa): 0.000885 g/cc (derived from pressure & temperature)
- Ambient pressure (P): 12.06 psia (SNL elevation ~5500 ft)
- Ambient temperature (To): 30° C
- **Elevation-dependent:** Range varies 2100 ft at sea level to 3600 ft at 5500 ft elevation for Vb=10,000 ft/sec

## Key Findings Addressing Your Research Questions

### Q1: Gurney Formula for Ogive vs. Cylinder Zones

**Finding:** Report treats fragment velocity as **material- and thickness-independent** once C/M ratio is known.

**Critical equation (p.16, Eq. 32):**
$$Vm/Vg = 1/(0.5 + (M/C))^{0.5}$$

For a **cylindrical casing:**

- Explosive-to-case weight ratio (C/M) determines Vm
- Thinner cases → higher C/M → higher velocity ratio
- Assumed **symmetric stress field** (spherical or cylindrical geometry)

**For ogive vs. cylinder distinction:**
Report does **not differentiate** ogive geometry. However, **theoretical discussion (p.10–11) notes:**

- Spherical config: velocity ratio (Vm/Vg) = 1.2 for C/M=10
- Cylinder config: velocity ratio (Vm/Vg) = 1.0 for C/M=10
- Asymmetric sandwich (N/C ratio tamping): (Vm/Vg) ≤ 1.53 for N/C ≥ 4

**Implication:** Ogive zone (conical geometry) should produce **lower velocity ratio** than cylindrical section. Report suggests using **cylindrical baseline** and applying **conservative reduction factor** for nose region.

**Data Table I (p.23):** Launch velocities for steel casing, HMX explosive (Vg = 0.294 cm/µs = 9650 ft/sec):

- 0.125 in casing: Vm = 7377 ft/sec, (C/M) = 0.828
- 0.250 in casing: Vm = 6461 ft/sec, (C/M) = 0.578
- 0.394 in casing: Vm = 5275 ft/sec, (C/M) = 0.352

**Recommendation:** Use **Table I interpolation** to estimate ogive velocity with adjusted C/M (reduced to account for conical taper geometry).

### Q2: Base Plate "Dead" Mass or Fragmented?

**Finding:** Report assumes all fragments are **tumbling plate-like or disk geometries** with effective thickness Sf = 0–0.5.

From **Section 5. Fragment Size (p.11):**

> "The fragments are generally assumed to be the thickness of the explosive casing, plate or disk-like, and irregular in geometry... The more ductile materials will show the above behavior the most. The more brittle material should show less of this cross linkage effect, with the major fragments separating more quickly. **End effects may already have produced smaller fragments at both ends of the cylinder.**"

**SNL Area 2 Example (p.17):**

- Charge: 1 pound HMX (453.6 g)
- Steel casing: 0.381 cm (0.150 in) thick
- Casing mass: 718.2 g
- Fragment shape factor Re = 0.6
- Fragment effective thickness Sf = 0.15
- **Resulting Vm = 6000 ft/sec, max range = 680 feet**

**Implication:** Base end **produces secondary fragmentation** not treated as single "dead plate." The model assumes base-region fragments follow plate trajectory physics. However, **no explicit base-mass term** is separated in the formulation.

**Missing data:** Report does not provide mass fraction or velocity reduction for base vs. side fragments. Recommend using **BRL Report 126 mass distribution** (base ~15% of total) with **reduced velocity** (apply ~0.7–0.8 factor to Vm).

### Q3: Boattail Separate Zone or Merged?

**Finding:** Report addresses **cylindrical and barrel-tamped casing geometries only.** No boattail-specific analysis.

**Discussion (p.10):** Lists seven cased explosive geometries:

1. Grazing detonation
1. Spherical
1. **Cylindrical** (primary focus)
1. Open sandwich
1. Symmetric sandwich
1. Asymmetric sandwich (N/C=2.0)
1. Barrel-tamped

**Recommendation:** Model boattail as **merged with cylinder** using baseline Vm from Table I. If later testing shows boattail produces distinct velocity signature, apply **empirical correction** to Vm (estimate +5% to +10% velocity increase due to reduced mass in taper section).

### Q4: Validation Data for Polar Distribution & Lethal Radius

**Finding:** YES. Report provides **quantitative trajectory data** for fragment range vs. launch velocity and geometry factors.

**Appendices A–C:** Graphical data showing maximum horizontal range (Xr) vs. effective fragment thickness (Sf) and shape factor (Re):

- Appendix A: Aluminum fragments (density 2.70 g/cc)
- Appendix B: Steel fragments (density 7.85 g/cc)
- Appendix C: Tantalum fragments (density 16.6 g/cc)

**Appendix D:** Fragment flight time (tx) vs. Sf and Re

**Key parameter ranges tabulated:**

- Initial fragment velocity: 2,000–14,000 ft/sec (2000 ft/sec intervals)
- Material: tantalum, steel, aluminum
- Launch angle: 0–45°
- Fragment geometry (Re): 0–1.0, (Sf): 0–0.5

**Fragment trajectory altitude (p.13, Eq. 20):**
$$y = TAN(B)(1 - E_x/F)X$$

where elevation (y) vs. horizontal distance (X) captured for all velocity/geometry combinations.

**SNL Area 2 application example (p.17–20):**

- Hazard zone established at **680 ft radius** for 1 lb HMX explosive in steel casing
- Maximum vertical altitude at max range: Ym ≈ 0.76 × Xf (76% of max range)
- Flight time to max range: ≈ 5.8 seconds (conservative, based on 10,000 ft/sec velocity)

**Implication:** This data **directly validates** four-zone fragmentation model:

1. Extract Vm for each zone from C/M ratio
1. Apply measured Sf and Re from test data (BRL 126 fragment screening)
1. Calculate Xr, Ym, and tx for each zone
1. Superpose hazard envelopes to obtain total lethal area
1. Compare predicted range vs. field test lethal radius

## Material & Fragment Properties

**Table I: Launch Velocities (HMX Explosive, Vg = 0.294 cm/µs = 9,650 ft/sec)**

| Casing Material | Thickness (in) | (C/M) | Vm/Vg | Vm (ft/sec) |
| --------------- | -------------- | ----- | ----- | ----------- |
| **Tantalum**    | 0.125          | 0.570 | 0.666 | 6,422       |
|                 | 0.250          | 0.273 | 0.490 | 4,726       |
|                 | 0.394          | 0.167 | 0.393 | 3,805       |
| **Steel**       | 0.125          | 0.828 | 0.765 | 7,377       |
|                 | 0.250          | 0.578 | 0.670 | 6,461       |
|                 | 0.394          | 0.352 | 0.547 | 5,275       |
| **Aluminum**    | 0.125          | 3.430 | 1.124 | 10,839      |
|                 | 0.250          | 1.640 | 0.950 | 9,161       |
|                 | 0.394          | 1.000 | 0.817 | 7,874       |

**Critical observation:** For **equal C/M ratios**, aluminum produces highest velocity (low density), steel intermediate, tantalum lowest (high density).

## Limitations & Caveats

1. **Drag coefficient:** Assumes tumbling plate-like fragments; Cd = 1.0–1.71. Real fragments may be irregular, altering drag.
1. **Material properties:** Does not account for temperature-dependent fragment density or velocity degradation at high altitudes.
1. **Angle of fall:** Tables assume launch angle B = 20° (optimum for range). Real detonations are typically vertical or low-angle; actual range may differ.
1. **Cross-coupling:** No interaction between fragment zones (assumes independent trajectories).
1. **Scaling:** Derived for small charges (≤ 1 lb); extrapolation to larger charges requires verification.

## Cross-References

- **BRL Report 126:** Experimental fragmentation data for 75mm M48 (validates fragment size/velocity ranges)
- **NWC TP 7124:** Cylindrical warhead expansion phases and fracture mechanics (refines C/M ratio prediction)

## Recommendations for Four-Zone Model

1. **Use Table I to establish baseline Vm for each zone** based on estimated C/M ratio
1. **Apply BRL 126 mass fractions** to weight each zone contribution
1. **Estimate Re and Sf** from BRL 126 fragment screening data
1. **Calculate Xr, Ym per Appendix curves** for each zone
1. **Superpose hazard envelopes** (combine polar distributions)
1. **Validate against field lethal radius data** (if available from 75mm testing)

______________________________________________________________________

**File:** `/home/arkadiy/arty_demo/doc-reference/ww2-shells/sandia-sand92-0243/index.md`\
**Processed:** May 25, 2026
