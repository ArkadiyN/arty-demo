---
title: AEP-55 Volume 3 — Procedures for Evaluating Protection Level of Armoured Vehicles, IED Threat Edition
authors: NATO Standardization Agency (NSA)
year: 2011
edition: Edition C, Volume 3 (Part I), Version 1 Ratification Draft 1
classification: NATO UNCLASSIFIED (Releasable to PFP and Australia)
source_url: NATO STANAG 4569
topic: wound-ballistics
---

## Summary

NATO AEP-55 Volume 3 establishes standardized procedures for testing the protection of armoured vehicle occupants against Improvised Explosive Device (IED) threats. While focused on vehicle armor performance, this document includes detailed anthropomorphic test dummy (ATD) specifications, seating postures, body dimensions of the 50th percentile male, and injury assessment reference values (IARVs) that are directly applicable to personnel vulnerability modeling. The document does NOT contain standalone personnel silhouette data or field-deployed personnel vulnerability models — it is centered on vehicle occupant protection under standardized test conditions. For field-deployed fragment threat models requiring posture-dependent silhouette area and angle-of-incidence factors, this document provides only the ATD anthropometry baseline; supplementary sources on open-air fragmentation effects on exposed personnel are required.

## Scope and Applicability

**This is a vehicle-centric document.** It defines:

1. **Vehicle structural integrity** testing for blast, fragmentation, and EFP threats (Annex C & D)
1. **Occupant injury assessment** using crash test dummies in seated vehicle configurations (Annex E)
1. **Pass criteria** based on measured accelerations, forces, and pressure at specific body locations

**NOT covered:**

- Standing, crouching, or prone personnel in open air
- Fragment arrival angle effects on field personnel
- Posture-specific lethal areas (AL) for unprotected personnel
- Whole-body silhouette area as a function of elevation angle γ

______________________________________________________________________

## Key Anthropomorphic Data

### ATD Standards

**Hybrid III 50th Percentile Male** (Section E2.1.1)

- Used for frontal, rear, and underbelly loading scenarios (UB1, UB2, UB3, RS1, RS2)
- Conforms to U.S. DOT Code of Federal Regulations Part 572 Subpart E and ECE Regulation No. 94
- Mass and dimensions: standard automotive crash dummy, approximately 75 kg

**ES-2re (EuroSID-2re) 50th Percentile Male** (Section E2.1.2)

- Used for lateral/side loading scenarios (RS3: roadside explosion to the side of occupant)
- Conforms to U.S. DOT Part 572, Docket No. NHTSA–2004–25441

**Military Lower Extremity (MIL-Lx)** (Section E2.1.3, E2.1.4)

- Model: Denton Model 585-0000
- Designed for **high-rate loading** in military explosive events
- Can replace standard HIII lower leg with updated pass criteria (Table E.3 footnote, E.4 footnote)
- **Required for overmatch assessment** (E2.1.4)

### Seating Posture Documentation

Section E4.4 and E4.4.4 define operational seating posture for the 50th percentile Hybrid III ATD:

**Upright Seating General** (E.4.4.1):

- Pelvis firmly into seat
- Torso in contact with seat back
- Skull base aligned as close as possible to horizontal
- Neck centerline as close as possible to vertical

**Specific ATD Posture Measurements** (E6.4.4, Figure E8):

| Measurement | Value (mm) | Description                |
| ----------- | ---------- | -------------------------- |
| A           | 110        | Head-roof distance         |
| B           | 430        | Head-wall lateral distance |
| C           | 475        | Shoulder-wall distance     |
| D           | 400        | Back-wall distance         |
| E           | 625        | Back panel height          |
| Fa          | 235        | Seat panel mid-height      |
| Fb          | 285        | Seat panel front height    |
| G           | 490        | Knee height                |
| H           | 200        | Calf-seat panel distance   |
| I           | 620        | Heel-wall distance         |
| J           | 410        | H-point (hip) height       |

**Foot Positioning** (E4.4.3):

- Driver: right foot on accelerator, left in realistic rest position
- Lower leg longitudinal axis perpendicular to footplate (worst-case)
- Use footrests per standard vehicle equipment

**Upper Extremities** (E4.4.2):

- Hybrid III: hands grip steering wheel or rest on upper legs; not fixed
- ES-2re: upper arms inclined 40° upward (operational) or directly downward (other seats)

______________________________________________________________________

## Injury Assessment Reference Values (IARVs) — Pass Criteria

These values represent the **10% AIS 2+ (Abbreviated Injury Score of 2 or higher) injury risk threshold** for the indicated body regions and loading scenarios.

### Table E3: Hybrid III ATD Mandatory IARVs and Pass Levels

| Body Region                      | Criterion                                        | Symbol     | IARV Pass Level | Notes                                           |
| -------------------------------- | ------------------------------------------------ | ---------- | --------------- | ----------------------------------------------- |
| **Head**                         | Head Injury Criterion                            | HIC15      | 250             | Max integral of head acceleration over 15 ms    |
| **Neck**                         | Axial compression force (immediate)              | Fz−        | 4.0 kN @ 0 ms   | Time-dependent; see Fig. E.6.5 appendix         |
|                                  | Axial compression force (sustained)              | Fz−        | 1.1 kN > 30 ms  |                                                 |
|                                  | Axial tension force (immediate)                  | Fz+        | 3.3 kN @ 0 ms   |                                                 |
|                                  | Axial tension force (35 ms)                      | Fz+        | 2.8 kN @ 35 ms  |                                                 |
|                                  | Axial tension force (sustained)                  | Fz+        | 1.1 kN > 60 ms  |                                                 |
|                                  | Shear force (immediate)                          | Fx/Fy      | 3.1 kN @ 0 ms   |                                                 |
|                                  | Shear force (sustained)                          | Fx/Fy      | 1.1 kN > 45 ms  |                                                 |
|                                  | Bending moment (flexion)                         | Mocy+      | 190 Nm          |                                                 |
|                                  | Bending moment (extension)                       | Mocy−      | 96 Nm           |                                                 |
| **Thorax**                       | Thoracic Compression Criterion (frontal)         | TCCfrontal | 30 mm           | Sternum-to-spine compression                    |
|                                  | Viscous Criterion (frontal)                      | VCfrontal  | 0.70 m/s        | Deformation velocity × deformation              |
| **Spine**                        | Dynamic Response Index                           | DRIz       | 17.7            | Thoraco-lumbar compression (dimensionless)      |
| **Upper Leg (Femur)**            | Axial compression force                          | Fz−        | 6.9 kN          | Left and right                                  |
| **Lower Leg (Tibia)**            | Axial compression force (MIL-Lx upper load cell) | Fz−        | **2.6 kN**      | **Preferred for IED testing**                   |
|                                  | Axial compression force (HIII lower load cell)   | Fz−        | 5.4 kN          | Legacy; less suitable for high-rate IED loading |
| **Non-Auditory Internal Organs** | Chest Wall Velocity Predictor (CWVP)             | CWVP       | 3.6 m/s         | Input: reflected overpressure on thorax         |

### Table E4: ES-2re ATD Mandatory IARVs and Pass Levels (Lateral Loading)

| Body Region                   | Criterion                                    | Symbol     | IARV Pass Level |
| ----------------------------- | -------------------------------------------- | ---------- | --------------- |
| **Head**                      | Head Injury Criterion                        | HIC15      | 250             |
| **Neck**                      | Axial tension force                          | Fz+        | 1.8 kN          |
| **Shoulder**                  | Compression force (impact side)              | Fy         | 1.4 kN          |
| **Ribs (upper/middle/lower)** | Rib Deflection Criterion                     | RDClateral | 28 mm           |
| **Thorax**                    | Viscous Criterion                            | VClateral  | 0.58 m/s        |
| **Abdomen**                   | Abdominal Peak Force (sum front/middle/rear) | Ftotal     | 1.8 kN          |
| **Spine**                     | Dynamic Response Index                       | DRIz       | 17.7            |
| **Pelvis**                    | Maximum Pubic Force                          | Fy         | 2.6 kN          |
| **Lower Leg (Tibia)**         | Axial compression force (MIL-Lx)             | Fz−        | 2.6 kN          |
|                               | Axial compression force (HIII)               | Fz−        | 5.4 kN          |

______________________________________________________________________

## Critical Assessment for Field Personnel Vulnerability Modeling

### What This Document Provides

1. **50th Percentile Male Anthropometry**: The Hybrid III and ES-2re are based on standardized adult male dimensions compatible with ballistic injury data literature.

1. **Seated Posture Baseline**: The documented seating geometry (Figure E8) establishes a reference frame for the head, thorax, abdomen, pelvis, and leg positions under operational conditions in vehicles.

1. **Injury Criteria**: The IARV pass levels are tied to published injury risk curves (Figs. E9–E23) from automotive crash research and military biomechanics, providing **quantitative relationships between kinetic loading and injury probability**.

1. **Instrumentation Standards**: Section E3 specifies how to measure accelerations, forces, and overpressure; these methods are directly applicable to fragment impact assessment on personnel.

### What This Document Does NOT Provide

1. **Standing/Crouching/Prone Silhouette Areas**: No tables of projected area (m²) vs. fragment elevation angle γ or azimuth direction.

1. **Angle-of-Incidence Vulnerability Factors**: No empirical P(kill | fragment arrival angle) relationships for unprotected personnel.

1. **Posture-Specific Lethal Areas (AL)**: The document defines vehicle occupant injury criteria, not whole-body casualty thresholds for exposed personnel.

1. **Fragment Mass/Velocity Lethality Models**: No Pk(E_kinetic) curves specific to field-deployed fragments on open-air targets.

1. **Fragmentation Distribution Patterns**: While the document references fragmentation IED testing (Annex B2.2-S, Annex C2, D2), the actual charge specifications and fragment ejection patterns are in the **NATO SECRET Annex B-S**, not this unclassified volume.

______________________________________________________________________

## Load Scenario Classification (Section E4.2, Figure E1)

The document defines **5 loading scenarios** relevant to occupant orientation:

### Underbelly (UB) Scenarios

- **UB1**: Explosion directly underneath ATD; primary vertical loading
- **UB2, UB3**: Explosion under vehicle; secondary lateral/horizontal loading to ATD

**ATD Selection**: Hybrid III

### Roadside (RS) Scenarios

- **RS1**: Explosion in front of ATD; primary horizontal, secondary vertical
- **RS2**: Explosion behind ATD; primary horizontal, secondary vertical
- **RS3**: Explosion to the side of ATD; primary lateral, secondary vertical

**ATD Selection**:

- RS1, RS2 → Hybrid III
- RS3 → ES-2re (designed for lateral impact)

**Implication for Field Model**: These 5 scenarios roughly correspond to different fragment arrival geometries relative to the occupant. However, vehicle occupants are spatially constrained and partially shielded by armor; field personnel are not. The loading directions (primary/secondary) cannot be directly transferred to exposed-personnel models without accounting for whole-body orientation and multi-hit effects.

______________________________________________________________________

## Pressure Measurement and Blast Overpressure Assessment

### Chest Wall Velocity Predictor (CWVP) Model (Section E6.3.11, Figure E7)

The document defines a **second-order nonlinear differential equation** for thoracic injury from blast overpressure:

```
M * d²x/dt² + C * dx/dt + K * x = A * [p(t) - P₀ * (V / (V - x))^γ]
```

**Parameters (70 kg male)**:

- A = 0.082 m² (effective chest area)
- M = 2.03 kg (effective mass)
- C = 696 Ns/m (damping coefficient, β_n = 0.224)
- K = 989 N/m (elasticity)
- V = 1.82 × 10⁻³ m³ (initial lung gas volume)
- P₀ = 1.0 × 10⁵ Pa (ambient pressure)
- γ = 1.2 (polytrophic exponent)

**Output**: Chest Wall Velocity (CWV), maximum velocity = 3.6 m/s for 10% AIS 2+ injury risk

**Measurement Method** (E6.1):

- Flat transducer on ATD chest surface (outside all clothing/PPE)
- Alternative: Blast Test Device (BTD) cylinder, h=762 mm, d=305 mm, transducer at half-height
- Pressure transducer specs: full scale > 300 kPa, resonance ≥ 50 kHz

**Implication**: Blast wave effects on unprotected personnel require similar overpressure measurement infrastructure and the CWVP model provides a validated framework for relating reflected overpressure to thoracic injury.

______________________________________________________________________

## Test Procedures and Threat Scenarios

### IED Threat Classification (Section 3.2)

Three categories:

1. **Blast Charges**: Bare HE charges (levels 1–7)
1. **Fragmentation Charges**: HE generating multiple high-speed fragments (levels 1–7)
1. **Projectile Forming Charges**: EFP threats (levels 1–7)

For each category, **7 protection levels** are defined separately for **roadside** and **underbelly** attack vectors.

**Note**: Full threat specifications (charge mass, fragment count, velocities, standoff distances) are in the **NATO SECRET Annex A-S and B-S**, not this unclassified volume.

### Structural Integrity Testing (Annex C1–C3, D1–D3)

- **Phase 1**: Tests on plates/components/engineered targets to assess ballistic resistance
- **Fragment test targets**: Minimum 1000 mm × 1000 mm to capture all fragments generated
- **EFP test targets**: Minimum 600 mm × 600 mm
- **Pass criterion**: Absence of Behind Armour Effects (BAE), verified with witness plate per AEP-55 Vol. 1

### Occupant Survivability Testing (Annex C4–C6, D4–D6)

- **Phase 2**: Full vehicle tests with instrumented ATDs
- **Phase 3**: Optional overmatch assessment (one level above qualification threat)
- **Pass criteria** (Para. 6.5):
  1. All occupant injury criteria (Table E.3 or E.4) within pass levels
  1. No hull rupture allowing penetration of injurious blast/ejecta
  1. No injurious secondary fragments from vehicle components/stowage
  1. Seat and restraint systems remain intact

______________________________________________________________________

## Injury Risk Curves (Figures E9–E23, Section E6.3)

The document includes **empirical injury risk functions** for each IARV:

- **HIC15** (Head Injury): NHTSA 1995 curve; 10% risk of serious head injury at HIC = 250
- **Neck Forces/Moments** (Figs. E10–E13): Mertz 1978, 2002; duration-dependent tolerance curves
- **Thoracic Compression (TCC)** (Fig. E15): Sternal deflection vs. AIS 3+ thoracic injury (Mertz et al. 1991)
- **Viscous Criterion (VC)** (Figs. E17–E18): Lau & Viano 1986 (frontal); Lowne & Janssen 1990 (lateral)
- **Rib Deflection (RDC)** (Fig. E16): Lowne & Janssen 1990; AIS 3+ risk vs. lateral rib deflection
- **Dynamic Response Index (DRIz)** (Fig. E20): Spinal compression; Brinkley 1970 + F-4 operational data
- **Femur Compression** (Fig. E22): Kuppa 2001; knee/femur/hip AIS 2+ and 3+ curves
- **Tibia Compression (MIL-Lx)** (Fig. E23): McKay & Bir 2009; AFIS 4+ injury logistic regression; valid up to 6 kN

**Reference Set**: All curves referenced in Annex G (References 18–30), with full citations to published biomechanics literature.

______________________________________________________________________

## Data Acquisition and Signal Processing Standards (Section E6.2)

**Sampling Rate**:

- Minimum 10 kHz per SAE J211 (automotive standard)
- **100 kHz or higher recommended** for IED loading (high-frequency acceleration peaks)
- Structural and pressure measurements: 100 kHz to 1 MHz

**Anti-Aliasing Filter**:

- Analog filter in data-acquisition system
- Recommended cut-off: ≥ 10 kHz

**Digital Resolution**:

- Minimum 12 bits (including sign) per SAE J211
- Higher word lengths (14–16 bits) recommended for low-amplitude signals at high gain

**Trigger**:

- Recommended: explosive charge initiation (T₀)
- Pre-trigger storage: ~100 ms for signal zeroing

**Signal Zeroing**:

- Average zero offset from minimum 100 ms of pre-trigger data

**Signal Filtering**:

- ATD measurements filtered per SAE J211/1 Channel Frequency Class (CFC) specifications
- Pressure and structural acceleration: preferably unfiltered (or only anti-aliasing filter)

______________________________________________________________________

## Limitations and Gaps for Field Personnel Modeling

1. **Vehicle Constraint**: All testing assumes occupants are seated, restrained, and inside a protective hull. Field personnel are unconfined and may adopt dynamic postures during threat engagement.

1. **Multi-Fragment Interactions**: This volume focuses on vehicle structural integrity and occupant injury in situ. It does not model cumulative effects of multiple overlapping fragment clouds or fragmentation patterns typical of dispersed open-air explosions.

1. **Clothing/Armor**: ATDs are dressed in operational clothing per E2.3, but the document does not quantify clothing material properties or body armor interaction. Fragment penetration of fabrics/body armor is not assessed.

1. **Posture Dynamics**: Seating posture is static and specified per E4.4. No assessment of postural shifts during the transient loading phase (milliseconds after detonation).

1. **Fragmentation Distribution**: The actual fragment ejection patterns, count, size, and velocity distributions from IED charges are in the NATO SECRET Annex B-S. This volume cannot be used standalone to model fragment threats on field personnel.

1. **Overpressure Spatial Variation**: Pressure measurement guidance (E6.1) addresses transducer mounting on the ATD chest and BTD cylinder, but does not provide a field-specific blast wave propagation model to estimate pressure at distance or angle from a detonation.

______________________________________________________________________

## Extracted Tables and Key Equations

### Dynamic Response Index (DRIz) Calculation (E6.3.3)

```
DRIz = 2 * ω_n * δ_max / g
```

Where:

- δ_max = maximum spine deflection (compression) [m]
- ω_n = 52.9 rad/s (circular natural frequency)
- g = 9.81 m/s² (gravitational acceleration)
- Pass threshold: DRIz ≤ 17.7 for 10% AIS 2+ spine injury risk

### Viscous Criterion (VC) Calculation (E6.3.4)

```
VC = D_max × (dD/dt) / C_scale × D_const
```

Where:

- D = thoracic deformation [m]
- dD/dt = deformation velocity [m/s]
- C_scale = scaling factor (1.3 for HIII male, 1.0 for ES-2re)
- D_const = deformation constant (0.229 m for HIII, 0.140 m for ES-2re)
- Pass thresholds: VCfrontal ≤ 0.70 m/s (HIII), VClateral ≤ 0.58 m/s (ES-2re)

### Head Injury Criterion (HIC15) (E6.3.1)

```
HIC15 = max_{t1,t2 | t2-t1 ≤ 15ms} [(t2 - t1) * (∫_{t1}^{t2} a(t) dt / (t2 - t1))^2.5]
```

Where:

- a(t) = resultant head acceleration [g], filtered CFC1000
- Pass threshold: HIC15 ≤ 250

### Occipital Condyle Moment (Moc) for Neck Bending (E6.3.2)

```
M_OCy = M_y + F_x * d
```

Where:

- M_y = neck moment in y-direction at upper neck load cell [Nm]
- F_x = upper neck shear force (anterior-posterior) [N]
- d = distance from load cell origin to occipital condyles [m] (Table E.5: 0.01778 m for Hybrid III 1716-series load cell)
- Pass thresholds: Mocy+ ≤ 190 Nm (flexion), Mocy− ≤ 96 Nm (extension)

______________________________________________________________________

## References to Supplementary Ballistics Standards

The document references related NATO standards relevant to personnel and vehicle protection:

1. **STANAG 4569**: Protection Levels for Occupants of Armoured Vehicles (overarching standard)
1. **AEP-55 Volume 1**: KE and Artillery Threat (kinetic energy and fragment threats)
1. **AEP-55 Volume 2**: Mine Threat (underbelly blast and fragmentation)

For field-deployed personnel vulnerability models, AEP-55 Volume 1 (KE threat) may contain fragment sizing and energy specifications relevant to open-air fragmentation effects.

______________________________________________________________________

## Summary: Use in Fragmentation-Field Model

**Directly Applicable**:

- 50th percentile male body dimensions (Hybrid III ATD)
- Seated posture reference geometry (for vehicle-occupant scenarios only)
- Injury assessment reference values (head, neck, thorax, spine, limbs) at 10% AIS 2+ risk
- Blast overpressure injury model (CWVP)
- Injury risk curves (Figures E9–E23) for converting kinetic loading to injury probability

**Not Applicable Without Supplementary Data**:

- Personnel silhouette area vs. elevation/azimuth angle
- Angle-of-incidence vulnerability factors for fragments
- Posture-specific lethal areas (AL) for field-deployed personnel
- Fragment distribution and ejection patterns for IEDs
- Multi-hit casualty assessment for clusters of fragments

**Recommended Next Steps**:

1. Cross-reference injury thresholds (Table E.3) with fragment kinetic energy lethality data from wound-ballistics or military medical literature.
1. Extract NATO-grade fragment specifications from AEP-55 Volume 1 (KE threat) to establish fragment mass/velocity baselines.
1. Combine ATD anthropometry with published data on posture-dependent silhouette area (e.g., military vulnerability assessment reports, DoD MIL-STD documents on target models) to parameterize P_hit for standing, crouching, prone personnel.
1. Validate injury probability models against historical casualty data or published military medical studies.
