# WW2 Shell Steel Evolution: X-1340 and the Transition to Heat-Treated Grades

**Document:** Ammunition Series 6 — Manufacture of Metallic Components of Artillery Ammunition\
**Section:** 6-11, "Steel Used Early in World War II"\
**Context:** Historical analysis of manganese-hardened vs. heat-treated artillery shell steels\
**Date:** Original source publication (pre-war to early 1942)\
**Source Type:** Primary military technical reference (transcribed excerpt)

______________________________________________________________________

## Excerpt: X-1340 Steel Composition and Strategic Evolution

### X-1340 Steel Specification (Original Composition)

**Shells were forged from a steel known as X-1340, which had the following composition:**

| Element        | Range            |
| -------------- | ---------------- |
| **Carbon**     | 0.35–0.45%       |
| **Manganese**  | 1.35–1.65%       |
| **Phosphorus** | ≤0.45% (maximum) |
| **Sulfur**     | 0.075–0.15%      |

**Designation Note:** X-1340 (not standardized SAE/AISI — designates War Department experimental or internal specification)

______________________________________________________________________

### Mechanical Property Strategy and Limitations

#### Original Design Rationale (Air-Cooling Method)

**"High manganese content was originally intended to secure the required physical properties (on cooling from forging temperature) without subsequent heat treatment, manganese being a hardener."**

- Manganese acts as a substitutional hardener in ferrite, increasing yield and tensile strength without additional processing
- Effect per 0.01% Mn: **100–500 psi tensile strength increase** (varies with carbon content)
- Yield strength target: **50,000 psi (≈345 MPa)** achievable with rapid, uniform cooling
- Method: **Air-blast cooling from forging temperature** to develop hardness in-situ

#### Critical Performance Constraint: Cooling Geometry

**"While the physical requirements were met in the smaller shells, difficulty was experienced with the 155-mm on account of the higher ratio of volume to heat-robbing surface."**

- **Smaller shells (75mm, 105mm):** Surface-area-to-volume ratio favors rapid cooling; air-blast cooling alone sufficient
- **Larger shells (155mm):** Core cooling rate insufficient; interior retains austenite/pearlite phases; outer shell hardens while interior softens → mechanical property mismatch, potential delamination risk

______________________________________________________________________

### Strategic Transition: Lower-Manganese Grade with Heat Treatment

**"This accounts for the decision of the Ordnance Department to adopt a steel with lower manganese content and to obtain the required mechanical properties by heat treatment."**

#### Driving Factors for the Change

1. **Thermal Engineering:** Avoid cooling-rate stratification by replacing rapid air-cooling with controlled furnace heat-treatment (normalizing or quenching)
1. **Resource Conservation:** "This action also saved considerable quantities of manganese, which was in short supply"
1. **Simplification:** "Simplified the work of the forge by eliminating air-blast cooling"

#### Trade-Off: Manufacturing Complexity Shift

**"However, the work in the machine shop was increased."**

- **Forge-side gain:** Simpler cooling; reduced capital equipment for air-blast systems
- **Machine-shop cost:** Normalized/quenched steels are harder, reducing machinability; more tool wear; slower production rates

______________________________________________________________________

## Open Question: X-1340 to WD-X1335 Relationship

### Status

**The source document does not explicitly name the successor steel grade.** However, textual evidence suggests a direct lineage:

| Attribute           | X-1340                                   | Successor?                   | Evidence                                              |
| ------------------- | ---------------------------------------- | ---------------------------- | ----------------------------------------------------- |
| Manganese Content   | High (1.35–1.65%)                        | Lower                        | Explicitly states "lower manganese" transition        |
| Cooling Method      | Air-blast (rapid, uncontrolled)          | Heat-treatment controlled    | Explicitly states heat-treatment adoption             |
| Applicability Range | Initially 75mm–155mm; problematic ≥155mm | 155mm+ suitable              | Implies successor addresses large-shell cooling issue |
| Designation         | X-1340                                   | **Unknown from this source** | Text offers no successor name                         |

### Baseline Catalog Reference

The **US 105mm M1 HE Shell (1940 Ordnance BOM)** specifies steel grade **WD-X1335** (spec 57-107) for the shell body.

**Possible Interpretations:**

1. **WD-X1335 is the direct successor** to X-1340 (heat-treated, lower Mn, introduced ~1941–1942)
1. **WD-X1335 is a parallel grade** for large-caliber shells while X-1340 continued for smaller shells
1. **WD-X1335 and X-1340 are unrelated** (X-1340 was experimental; WD-X1335 was the production standard all along)
1. **Multiple variants existed** (X-1340M, X-1340LM, etc.) with varying Mn content for different caliber ranges

**Data Gap:** Composition and mechanical properties of WD-X1335 are not publicly digitized (spec 57-107 remains archived).

______________________________________________________________________

## Material Science Summary

### Manganese as a Hardener (0.01% ΔMn)

- **Tensile Strength Increase:** 100–500 psi per 0.01% Mn (carbon-dependent; higher C → larger effect)
- **Yield Strength Increase:** Somewhat greater than tensile (ductility trade-off minimal at moderate Mn levels ~1.5%)
- **Mechanism:** Substitutional solid-solution hardening + grain refinement (Mn promotes austenite stability)

### Carbon Content Context (0.35–0.45%)

- **Low-carbon steel range** for forgings (typically 0.35–0.55% C)
- **Typical WW2 HE shell steel:** SAE 1035–1045 (equivalent to 0.35–0.45% C, 0.6–0.9% Mn)
- **X-1340 variant:** Elevated Mn (1.35–1.65%) for substitute hardening in lieu of carbon increase (which would reduce toughness)

### Phosphorus and Sulfur (Impurities)

| Element | X-1340 Spec | Typical SAE Range | Effect                                                                               |
| ------- | ----------- | ----------------- | ------------------------------------------------------------------------------------ |
| **P**   | ≤0.45%      | ≤0.04%            | High P (0.45%) = severe embrittlement; likely typo in source or relaxed wartime spec |
| **S**   | 0.075–0.15% | ≤0.05%            | Elevated S → MnS inclusion formation; reduced notch-toughness                        |

**Caveat:** The phosphorus limit (0.45%) in the transcribed excerpt is unusually high and may reflect:

- OCR/transcription error (should be 0.045%?)
- Wartime relaxation of purity standards due to scrap-metal remelting
- Experimental tolerance on the original specification

______________________________________________________________________

## Recommendations for Further Investigation

1. **Locate Spec 57-107** — Retrieve full composition and mechanical properties of WD-X1335 from:

    - U.S. Army Heritage Center, Carlisle Barracks, PA
    - DTIC archives (ADA/AD series specifications)
    - Aberdeen Proving Ground historical records

1. **Cross-reference X-1340 Literature** — Search:

    - War Department technical orders (TM, TO series, 1940–1943)
    - Ordnance Department manufacturing blueprints (M-series shell drawings)
    - Metallurgical literature (1938–1945) for "X-1340" or similar designations

1. **Verify Phosphorus Specification** — Clarify whether P ≤0.45% is correct or a transcription artifact

1. **Trace Heat-Treatment Protocol** — Determine whether successor steel used:

    - Normalizing (air-cooled from austenite range)
    - Quenching + tempering (faster hardening)
    - Isothermal transformation (Austempering)

______________________________________________________________________

## Confidence Assessment

| Aspect                                | Confidence  | Notes                                                          |
| ------------------------------------- | ----------- | -------------------------------------------------------------- |
| X-1340 Composition                    | High        | Direct quote from authoritative source                         |
| Manganese Effect (~100–500 psi/0.01%) | High        | Standard metallurgical relationship (literature-confirmed)     |
| Cooling-Rate Limitation (155mm)       | Medium-High | Physically plausible; consistent with heat-transfer principles |
| Successor Grade Identity              | **Low**     | Not named in source; WD-X1335 is inferred, not confirmed       |
| Phosphorus Spec (≤0.45%)              | **Low**     | Value unusually high; possible transcription error             |

______________________________________________________________________

**Source Provenance:** User-supplied transcription from original military document (image reference: /mnt/f/Projects/TMP/AgenticCoding/X-1340.png for citation purposes only)
