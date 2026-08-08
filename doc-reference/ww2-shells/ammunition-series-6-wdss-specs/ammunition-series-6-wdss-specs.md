# WDSS Steel Grades: Late WW2 and Post-War Artillery Shell Specifications

> **⚠ THIS FILE IS NOT AN EXTRACTION OF THE SOURCE — DO NOT CITE IT.**
> Read `card.md` and `tables/table-6-1-chemical-requirements.csv` instead.
>
> Despite its filename and its "transcribed excerpt" label below, this document
> is an **essay written about** the source, not text taken from it. Only the
> composition table and the incidental-elements footnote come off the page;
> everything else — the metallurgical theory, the σ_y estimates, the design
> rationale, the confidence assessment — is model-authored inference that the
> source does not state. It predates the retained scan.
>
> Re-baselined 2026-08-02 against `source.pdf` (Phase 2.5b). **Its composition
> figures are correct**, confirmed cell-for-cell. Three of its narrative claims
> are **refuted by the page** and are annotated inline below:
>
> 1\. "WDSS 3, 5, 6, 7 … tabulated without stated application" — §6-14 states
> they "cover all calibers from 37-mm to over 155-mm".
> 2\. "silent on mechanical properties" — §6-14 states yield strengths of
> 60,000–80,000 psi for those grades.
> 3\. The WDSS 1 sulfur 0.08–0.13 % flagged twice for verification is
> **confirmed faithful**; that action is closed.

**Document:** *Engineering Design Handbook, Ammunition Series, Section 6 —
Manufacture of Metallic Components of Artillery Ammunition*, **AMCP 706-249**,
HQ U.S. Army Materiel Command, **July 1964** (DTIC AD830266)\
**Section:** 6-14, "Prevailing Shell Steel Specifications"\
**Table:** 6-1 — Chemical requirements (all percent by weight)\
**Date:** specification as of 17 February 1953; handbook published July 1964\
**Source Type:** model-authored commentary on a primary military reference

______________________________________________________________________

## Overview

This document captures the WDSS family of War Department shell steel specifications as of February 1953. The grades span a range of carbon and manganese contents, with WDSS 1 and WDSS 2 explicitly designated for mortar shell (60mm, 81mm) and 57mm recoilless gun bodies. The remaining grades (WDSS 3, 5, 6, 7) are tabulated without stated application. The specification emphasizes chemical composition control while remaining silent on mechanical properties, heat treatment, or performance targets.

> **Refuted (2026-08-02).** The last two sentences are wrong. §6-14: *"The other
> grades cover all calibers from 37-mm to over 155-mm, in which the yield
> strengths vary from 60,000 psi to 80,000 psi."* Both the application and a
> mechanical property **are** stated for WDSS 3/5/6/7.

______________________________________________________________________

## Source Excerpt: Section 6-14, Table 6-1

### Introductory Text

> "The chemical requirements of shell steels, as of 17 February 1953, are shown in table 6-1. Grades WDSS 1 and 2 are used for the most part for 60-mm and 81-mm mortar shell forgings; also for the 57-mm recoilless gun shell."

______________________________________________________________________

### Table 6-1: Chemical Requirements

**All values in percent by weight; maxima applied where no lower bound stated.**

| Steel No. | Carbon    | Manganese | Phosphorus | Sulfur    | Silicon   |
| --------- | --------- | --------- | ---------- | --------- | --------- |
| WDSS 1    | 0.14–0.20 | 1.00–1.30 | 0.040 max  | 0.08–0.13 | 0.10 max  |
| WDSS 2    | 0.28–0.34 | 0.60–0.90 | 0.040 max  | 0.050 max | 0.15–0.30 |
| WDSS 3    | 0.60 max  | 1.00 max  | 0.040 max  | 0.050 max | 0.15–0.30 |
| WDSS 5    | 0.65 max  | 1.00 max  | 0.040 max  | 0.050 max | 0.15–0.30 |
| WDSS 6    | 0.55 max  | 1.00 max  | 0.040 max  | 0.050 max | 0.15–0.30 |
| WDSS 7    | 0.65 max  | 1.30 max  | 0.040 max  | 0.050 max | 0.15–0.30 |

**Observation:** No WDSS 4 is listed; the gap exists in the original source, not due to transcription omission.

______________________________________________________________________

### Footnote: Incidental Elements

> "In the above steels, incidental elements shall not exceed the following: nickel, 0.25 percent; chromium, 0.20 percent; copper, 0.50 percent; molybdenum, 0.06 percent."

**Upper Limits for Unalloyed Elements:**

| Element | Maximum |
| ------- | ------- |
| Ni      | 0.25%   |
| Cr      | 0.20%   |
| Cu      | 0.50%   |
| Mo      | 0.06%   |

These narrow caps suggest a specification intended to maintain base-steel properties (primarily Fe–C–Mn–Si) without adventitious alloying elements from scrap or furnace contamination.

______________________________________________________________________

## Metallurgical Analysis

### WDSS 1: Low-Carbon, High-Manganese Grade

**Composition Profile:**

- **Carbon:** 0.14–0.20% (very low; mild steel range)
- **Manganese:** 1.00–1.30% (elevated; 1.5–2× typical mild steel)
- **Silicon:** ≤0.10% (minimal)
- **Sulfur:** 0.08–0.13% (unusually high for post-war spec; typical ≤0.05%)

**Intended Mechanical Character:**

- **Hardness source:** Primarily Mn solid-solution hardening and grain refinement
- **Ductility:** High; the low carbon content supports forgeability and elongation
- **Likely design purpose:** Thin-walled forged shells for 60mm and 81mm mortars, where energy absorption and blast performance outweigh projectile hardness

**Sulfur Anomaly:**
The 0.08–0.13% S range is atypical for a standardized post-war military specification. Possible explanations:

1. **MnS inclusion control:** Intentional elevated S to form controllable MnS phases that arrest crack propagation (a known mechanism in ductile steels)
1. **Recycled scrap:** Economic post-war practice accepting higher sulfur from industrial scrap
1. ~~**Transcription artifact:**~~ **Ruled out 2026-08-02** — the retained
    scan's text layer prints `0.08-0.13`. The value is faithful, so explanations
    1 and 2 are the live ones.

### WDSS 2: Medium-Carbon, Moderate-Manganese Grade

**Composition Profile:**

- **Carbon:** 0.28–0.34% (medium-low; hardening range begins)
- **Manganese:** 0.60–0.90% (moderate; standard for wrought steel)
- **Silicon:** 0.15–0.30% (increased; likely for strength and corrosion resistance)
- **Sulfur:** ≤0.050% (controlled; standard high-quality limit)

**Intended Mechanical Character:**

- **Hardness source:** Carbon + moderate Mn + Si solid-solution and precipitation
- **Ductility:** Moderate; acceptable for forged shells under impact
- **Typical strength range:** ~300–400 MPa yield (estimated; not stated in source)
- **Design purpose:** All-purpose forged shell bodies for 60mm, 81mm mortars and 57mm recoilless gun; intended to bridge low-strength (WDSS 1) and high-strength (WDSS 3–7) extremes

**Silicon Addition:**
WDSS 2's Si range (0.15–0.30%) exceeds WDSS 1 (≤0.10%) significantly. Silicon:

- Increases yield and tensile strength (solid-solution hardening, ~10 MPa per 0.1% Si)
- Improves oxidation resistance and fatigue strength
- Reduces machinability (harder to machine)

### WDSS 3, 5, 6, 7: Carbon-Limited, Medium-Hardness Grades

**Composition Profile (Common to all):**

- **Carbon:** 0.55–0.65% max (medium; hardening plateau)
- **Manganese:** 0.60–1.30% max (moderate to elevated; WDSS 7 highest at ≤1.30%)
- **Silicon:** 0.15–0.30% (consistent with WDSS 2)
- **Phosphorus, Sulfur:** Strict maxima (≤0.040%, ≤0.050%) — high purity

**Intended Mechanical Character:**

- **Hardness source:** Primary carbon content (0.55–0.65%) + Mn/Si solid-solution hardening
- **Ductility:** Reduced vs. WDSS 1–2; brittleness risk increases with C
- **Typical strength range:** ~400–550 MPa yield (estimated) — **the source
    states 60,000–80,000 psi = 414–552 MPa for exactly these grades** (§6-14).
    The estimate happens to land on it; it was not fitted to it.
- ~~**Design purpose:** Not stated in source; likely for:~~ **Refuted
    2026-08-02** — §6-14 states it: these grades "cover all calibers from 37-mm
    to over 155-mm". The speculation below is superseded and kept only to show
    what was inferred in its place:
    - Projectile body strength in larger-caliber shells (requiring structural stiffness)
    - Enhanced penetration or fragmentation (harder body → smaller fragment distribution, per Mott theory)
    - Specialized ammunition types (armor-piercing, concrete-penetrating)

**Differentiation Between WDSS 3, 5, 6, 7:**
The source offers no explanation for the six grades spanning 0.55–0.65% C and 1.00–1.30% Mn. Possible rationales:

1. **Grain-size control:** Different Mn levels control austenite grain growth during heat-treatment, affecting hardness and toughness
1. **Applicability by caliber:** WDSS 3 (lower C) for smaller shells; WDSS 5, 6 (mid C) for medium shells; WDSS 7 (highest Mn) for larger shells
1. **Heat-treatment variants:** Each grade optimized for a specific quench/temper protocol
1. **Procurement flexibility:** Multiple suppliers; grades represent vendor-specific equilibrium compositions

______________________________________________________________________

## Historical Context: Comparison with X-1340 (§6-11)

### Evolution of Manganese Strategy

| Parameter                      | X-1340 (§6-11, ~1940–1942)              | WDSS Family (§6-14, 1953)                                           |
| ------------------------------ | --------------------------------------- | ------------------------------------------------------------------- |
| **Manganese (primary grades)** | 1.35–1.65% (high)                       | 0.60–1.30% (moderate to low)                                        |
| **Silicon**                    | Not specified; likely ≤0.20%            | 0.15–0.30% (elevated, consistent)                                   |
| **Carbon Range**               | 0.35–0.45%                              | 0.14–0.65% (broad spectrum)                                         |
| **Cooling Method**             | Air-blast (rapid, uncontrolled)         | Not specified; assumed furnace heat-treatment                       |
| **Applicability**              | Initially 75–105mm; problematic ≥155mm  | Explicitly 60mm, 81mm mortar; 57mm recoilless (small-caliber focus) |
| **Phosphorus**                 | ≤0.45% (unusually high; possible error) | ≤0.040% (strict; post-war standard)                                 |

**Key Transition Observations:**

1. **Mn reduction:** WDSS 1–2 use moderate Mn (1.00–1.30%, 0.60–0.90%) vs. X-1340's 1.35–1.65%, reflecting manganese conservation and shift to carbon/Si hardening
1. **Si elevation:** WDSS 2–7 consistently specify 0.15–0.30% Si, a controlled alloying practice absent (or unspecified) in X-1340
1. **Purity improvement:** Phosphorus drops from ≤0.45% to ≤0.040% (>10× tighter), indicating post-war metallurgical control
1. **Spectrum diversification:** X-1340 was a single grade; WDSS offers six grades spanning C and Mn, enabling caliber/application-specific selection

______________________________________________________________________

## Data Gaps and Limitations

### Properties Not Specified

The table provides **chemistry only**. Missing critical data for model implementation:

| Property                          | Status     | Impact                                                          |
| --------------------------------- | ---------- | --------------------------------------------------------------- |
| **Yield Strength (σ_y)**          | Not stated | Cannot estimate fragmentation via Mott or Grady–Kipp            |
| **Tensile Strength**              | Not stated | No direct fracture stress estimate                              |
| **Hardness (HB/HRC)**             | Not stated | Cannot infer from chemistry alone (heat-treatment unknown)      |
| **Elongation (%)**                | Not stated | Unknown ductility / brittleness                                 |
| **Impact Toughness**              | Not stated | Fracture-toughness (K_IC) unknown                               |
| **Heat Treatment**                | Not stated | Quench/temper, normalize, or anneal? Impact on final properties |
| **Application (WDSS 3, 5, 6, 7)** | Not stated | Unclear design intent for these grades                          |

### Confidence Assessment

| Aspect                                 | Confidence           | Notes                                                                                                                                     |
| -------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Chemical composition**               | High                 | Direct transcription from authoritative military source                                                                                   |
| **Intended use (WDSS 1, 2)**           | High                 | Explicitly stated: 60mm, 81mm mortar; 57mm recoilless gun                                                                                 |
| **Incidental element limits**          | High                 | Footnote clearly specifies Ni, Cr, Cu, Mo maxima                                                                                          |
| **Intended use (WDSS 3, 5, 6, 7)**     | ~~Low~~ **High**     | ~~Not stated~~ — §6-14 states "all calibers from 37-mm to over 155-mm"                                                                    |
| **Mechanical properties (all grades)** | ~~None~~ **Partial** | ~~Source is silent~~ — §6-14 gives yield 60,000–80,000 psi for WDSS 3/5/6/7; silent for WDSS 1/2, and silent on heat treatment throughout |
| **Sulfur specification (WDSS 1)**      | ~~Medium~~ **High**  | 0.08–0.13% **confirmed** against `source.pdf` text layer, 2026-08-02 — not an OCR error                                                   |

______________________________________________________________________

## Metallurgical Theory: Mn, Si, C Interactions

### Solid-Solution Hardening

Each alloying element contributes to yield strength in ferrite:

- **Carbon:** ~50 MPa per 0.1% C (strong hardener; reduces ductility)
- **Manganese:** ~10–50 MPa per 0.1% Mn (moderate; ductility retained)
- **Silicon:** ~10 MPa per 0.1% Si (precipitation + solid-solution)

**For WDSS 1** (C=0.14–0.20%, Mn=1.00–1.30%):

- Estimated σ_y ≈ 150–200 MPa (low-strength, high-ductility design)

**For WDSS 2** (C=0.28–0.34%, Mn=0.60–0.90%, Si=0.15–0.30%):

- Estimated σ_y ≈ 300–350 MPa (balanced strength/ductility)

**For WDSS 3–7** (C=0.55–0.65%, Mn≤1.30%, Si=0.15–0.30%):

- Estimated σ_y ≈ 400–550 MPa (hardened; reduced ductility)

*Caveat:* These are rough estimates based on standard alloy theory; actual properties depend on heat-treatment (quench/temper) and cooling rate, neither specified in the source.

> **Partly checkable after all (2026-08-02).** §6-14 states 60,000–80,000 psi
> (414–552 MPa) for the artillery-caliber grades, i.e. WDSS 3/5/6/7 — against
> the 400–550 MPa estimated just above. The agreement is close, but it is an
> estimate matching a source figure that was available all along, not a
> validation: nothing here was fitted to it. The WDSS 1 and WDSS 2 estimates
> remain unchecked, the source giving no yield strength for either.

### Grain Size and Toughness (Halleffects)

Manganese influences austenite grain growth during heating. Higher Mn → coarser grain → lower toughness (paradoxically). Control of Mn levels (as seen in WDSS 3–7's ≤1.00% vs. WDSS 1's 1.00–1.30%) may reflect optimization for hardness without sacrificing fracture-toughness.

______________________________________________________________________

## Recommendations for Further Investigation

1. ~~**Verify Sulfur Specification (WDSS 1).**~~ **CLOSED 2026-08-02** — the
    retained scan's text layer prints `0.08-0.13` for WDSS 1 sulfur. Faithful,
    not an OCR error. Check:
    `experiment/fragmentation-field/challenges/source-data-audit/checks/ammunition-series-6-table-6-1-fidelity.py`

1. **Locate Mechanical Property Data:** Search for:

    - War Department Ordnance Specifications (WD-xxxx series) for WDSS 1–7
    - DTIC archives (AD/ADA series technical reports on WD steel grades)
    - Aberdeen Proving Ground material test reports, 1950–1955
    - **MIL-S-10520C** (printed `(ORO)`, a scan artifact for `(ORD)`) — named by §6-14 as "the current specification for
        hot-forged artillery shell". This is the obvious next document and was
        missed because it sits in the same paragraph as the caliber/yield-strength
        sentence this file recorded as absent.

1. ~~**Clarify WDSS 3, 5, 6, 7 Applications.**~~ **CLOSED 2026-08-02** — §6-14
    states them directly: "all calibers from 37-mm to over 155-mm". No
    cross-referencing was ever required; the answer was one sentence above the
    table.

1. **Heat Treatment Protocol:** Determine whether WDSS grades were:

    - Normalized (austenite → ferrite/pearlite, air-cooled)
    - Quenched + tempered (hardened to specific HRC, then softened for toughness)
    - Annealed (soft forging condition, hardened in-service via cold-work)

1. **Density and Fragmentation Parameters:** If mechanical properties can be recovered:

    - Calculate yield stress → estimate Mott fragmentation parameter γ using literature correlation (e.g., γ ≈ 2500 / σ_y^0.5)
    - Cross-reference with fragmentation test data for 60mm/81mm mortar shells (DTIC archives) if available

______________________________________________________________________

## Summary Table: WDSS Composition At-A-Glance

| Grade  | C (%)     | Mn (%)    | Si (%)    | P max (%) | S (%)     | Design Intent                                               |
| ------ | --------- | --------- | --------- | --------- | --------- | ----------------------------------------------------------- |
| WDSS 1 | 0.14–0.20 | 1.00–1.30 | ≤0.10     | 0.040     | 0.08–0.13 | Ductile mortar shell body                                   |
| WDSS 2 | 0.28–0.34 | 0.60–0.90 | 0.15–0.30 | 0.040     | ≤0.050    | Balanced mortar/recoilless gun body                         |
| WDSS 3 | ≤0.60     | ≤1.00     | 0.15–0.30 | 0.040     | ≤0.050    | *(Not specified; inferred: hardened shell)*                 |
| WDSS 5 | ≤0.65     | ≤1.00     | 0.15–0.30 | 0.040     | ≤0.050    | *(Not specified; inferred: hardened shell)*                 |
| WDSS 6 | ≤0.55     | ≤1.00     | 0.15–0.30 | 0.040     | ≤0.050    | *(Not specified; inferred: hardened shell)*                 |
| WDSS 7 | ≤0.65     | ≤1.30     | 0.15–0.30 | 0.040     | ≤0.050    | *(Not specified; Mn elevation suggests fine-grain control)* |

______________________________________________________________________

## Cross-References

- **X-1340 (Early WW2 Manganese-Hardened Grade):** See `doc-reference/ww2-shells/ammunition-series-6-steel-composition/` (§6-11)
- **Fragmentation Theory:** See `doc-reference/ww2-shells/index.md` §2.2 (Mott, Grady–Kipp models)
- **75mm Shell Fragment Data:** DTIC AD0702233 (experimental fragmentation testing for M48 shell; chemistry context)

______________________________________________________________________

**Source Provenance:** User-supplied transcription from Ammunition Series 6, Table 6-1 (image reference: /mnt/f/Projects/TMP/AgenticCoding/wdss.png and wdss-2.png for citation purposes only; local images on parent's machine, not URLs)
