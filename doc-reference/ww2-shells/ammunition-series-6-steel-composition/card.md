# Card: X-1340 Steel and WW2 Artillery Shell Grade Evolution

**Source:** Ammunition Series 6, §6-11 (primary transcription)\
**Relevance:** Composition, hardening strategy, and process tradeoffs for WW2 forged HE shell bodies

______________________________________________________________________

## X-1340 Steel Composition

| Element | Range       | Section Anchor                                     |
| ------- | ----------- | -------------------------------------------------- |
| **C**   | 0.35–0.45%  | "Shells were forged from a steel known as X-1340…" |
| **Mn**  | 1.35–1.65%  | Composition table                                  |
| **P**   | ≤0.45% max  | Composition table (verify: unusually high)         |
| **S**   | 0.075–0.15% | Composition table                                  |

**Design Goal:** High Mn as substitutional hardener to achieve 50,000 psi (≈345 MPa) yield without heat treatment. Requires rapid, uniform air-cooling from forging temperature.

______________________________________________________________________

## Manganese Hardening Relationship

**Tensile strength increase per 0.01% Mn:** 100–500 psi (carbon-dependent)\
**Yield strength increase:** Greater than tensile; ductility retained at ~1.5% Mn.\
**Section:** "The amount by which 0.01 percent manganese increases the tensile strength varies with the carbon content from 100 to 500 psi."

______________________________________________________________________

## Cooling-Rate Limit (Caliber Dependency)

| Shell Caliber | Status               | Reason                                                                       | Section Anchor                                                                                                |
| ------------- | -------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **≤105mm**    | Works with air-blast | High surface-area-to-volume ratio → rapid core cooling                       | "While the physical requirements were met in the smaller shells…"                                             |
| **155mm+**    | Fails with air-blast | Lower S/V ratio → core remains austenite; outer hardened → property mismatch | "difficulty was experienced with the 155-mm on account of the higher ratio of volume to heat-robbing surface" |

______________________________________________________________________

## Strategic Transition: Lower-Mn + Heat Treatment

| Factor               | Old (X-1340, air-cooled)          | New (Successor, heat-treated)                |
| -------------------- | --------------------------------- | -------------------------------------------- |
| **Mn Content**       | 1.35–1.65%                        | Lower (not specified)                        |
| **Cooling Method**   | Air-blast furnace cooling         | Controlled heat-treatment (type unspecified) |
| **Validity Range**   | 75–105mm acceptable; ≥155mm fails | Intended for all calibers                    |
| **Forge Simplicity** | Eliminated (air-blast rig)        | Increased (oven-based)                       |
| **Machinability**    | Better                            | Reduced (harder material; tool wear)         |
| **Mn Availability**  | Consumed heavily                  | Conserved ("saved considerable quantities")  |

**Section:** "the decision of the Ordnance Department to adopt a steel with lower manganese content and to obtain the required mechanical properties by heat treatment."

______________________________________________________________________

## Open Question: X-1340 ↔ WD-X1335 Relationship

**Baseline catalog (105mm M1 BOM, 1940):** Specifies steel **WD-X1335** (spec 57-107).

**Unconfirmed:** Is WD-X1335 the heat-treated successor to X-1340? Source text does not name successor grade. See **Confidence Assessment** table in ammunition-series-6-steel-composition.md for interpretation options.

______________________________________________________________________

## Material Property Targets

- **Yield:** 50,000 psi (345 MPa) – achievable via rapid air-cooling of high-Mn steel
- **Elongation:** ~10–20% typical for normalized 1035–1045 equivalent; Mn retains ductility
- **Hardness:** ~400–500 HB (normalized state; not stated in source)

______________________________________________________________________

**Validity:** WW2 early years (≤1942); applies to 75–155mm HE shell forging standards\
**Cross-reference:** ammunition-series-6-steel-composition.md §"Open Question" for successor-grade disambiguation
