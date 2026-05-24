---
title: Wound Ballistics & Fragment Lethality Reference Library
topic: wound-ballistics
date-created: 2026-05-24
---

# Wound Ballistics References

A collection of scientific and technical references on fragment armor penetration, human vulnerability modeling, and lethality assessment for fragmentation weapons.

## Collected Articles

### 1. Cunniff, Philip M. — "A Method to Describe the Statistical Aspects of Armor Penetration, Human Vulnerability and Lethality due to Fragmenting Munitions"

**Year:** 2014\
**Type:** Technical Report\
**DOI:** (not available)\
**File:** `/doc-reference/wound-ballistics/cunniff-2014/`

**Summary:** Establishes dimensionless areal density (Ad·Ap/mp) as the unifying parameter for armor penetration, tissue penetration, and environmental drag. Demonstrates that fragment presented area per unit mass follows munition-specific probability distributions independent of individual fragment mass—enabling statistical lethality modeling. Includes Sturdivan tissue penetration model, drag coefficient variability analysis, and computational framework for human phantom vulnerability assessment.

**Key Data:**

- Fragment presented area PDFs for 155 mm M107, 76 mm MK165, MK84 (Figure 3)
- Gelatin and wallboard penetration fits via Ad·Ap/mp parameter (Figures 5–6)
- Human phantom computational method with orientation-dependent impact zones (Figure 7)
- Fragment mass distribution laws (Mott, Grady, Weibull, Log-Normal, etc.; Table 1)

**Relevance to Model:** Directly addresses posture-independent target area variability via munition-specific orientation PDFs; provides unified penetration model across armor, tissue, and reference materials; enables Bayesian posterior updating of fragment threat parameters.

______________________________________________________________________

### 2. Federation of American Scientists / U.S. Navy — "Damage Criteria — ES310 Naval Weapons Engineering"

**Year:** 1998\
**Type:** DoD Training / Reference Document\
**Source:** https://man.fas.org/dod-101/navy/docs/es310/dam_crit/dam_crit.htm\
**File:** `/doc-reference/wound-ballistics/fas-es310-damage-criteria/`

**Summary:** Establishes probabilistic damage criteria for fragmentation warheads using Pk (Probability of Kill) framework. Personnel lethality thresholds: 100 J (Pk = 0.1, light damage), 1,000 J (Pk = 0.5, moderate), 4,000 J (Pk = 0.9, heavy). Formalizes fragment count, mass, velocity, and range integration into expected-hits model. Clarifies why fixed-energy thresholds (e.g., 79 J) misrepresent the probabilistic nature of fragment casualty.

**Key Equations:**

- Pk = P_hit × Pk|hit (conditional kill)
- Nhits = A × (N₀ / 4πR²) (expected hits on area A at range R)
- Pk_multi = 1 − (1 − Pk|hit)^Nhits (aggregate kill from multiple hits)

**Relevance to Model:** Defines the Pk|hit framework; provides baseline energy thresholds for validation; clarifies why Bayesian probabilistic approach is superior to binary kill criteria.

______________________________________________________________________

### 3. U.S. Army/ARL (Misc.) — "Army Equipment Publication 55-Vol. 3: Casualty Criteria"

**Year:** ~1995–2010 (multiple editions)\
**Type:** Military Casualty Assessment Standard\
**File:** `/doc-reference/wound-ballistics/aep-55-vol3/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 4. PMC7295711 — Bone Fragments in Blast Injury

**Year:** (Pending metadata)\
**Type:** Journal Article / Systematic Review\
**File:** `/doc-reference/wound-ballistics/pmc7295711-bone-fragments/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

### 5. Lethality Threshold Critique

**Year:** (Pending metadata)\
**Type:** (Pending classification)\
**File:** `/doc-reference/wound-ballistics/lethality-threshold-critique/`

**Summary:** (Pending detailed extraction)

______________________________________________________________________

## Cross-Reference Index

### By Topic

**Fragment Armor Penetration:**

- Cunniff (2014) — Figure 1, ballistic limit model; Figure 3, presented area PDFs

**Human Vulnerability & Pk|hit:**

- FAS ES-310 (1998) — Damage criteria table, Pk thresholds
- Cunniff (2014) — Sturdivan tissue penetration model, Figures 5–6

**Statistical Methods:**

- Cunniff (2014) — Bayesian posterior framework, munition threat PDFs, Monte Carlo approach

**Casualty Assessment:**

- AEP-55 Vol. 3 (TBD)
- PMC7295711 (TBD)

______________________________________________________________________

## Usage Notes

### For Fragmentation Lethality Model Development

1. **Start with Cunniff (2014):**

   - Import Figure 3 munition-specific presented area distributions
   - Use Driels equation (p. 35) for velocity-reduction-in-flight calculations
   - Apply Sturdivan model (pp. 49–51) for tissue penetration depth

1. **Validate Against FAS ES-310:**

   - Compare computed Pk vs. tabulated energy thresholds (100 J, 1 kJ, 4 kJ)
   - Verify Pk|hit assignment per fragment kinetic energy

1. **Extend to Posture & Presented Area:**

   - Cunniff's human phantom method (Figure 7) computes area as f(burst location, posture)
   - No explicit standing/crouching/prone dimensions given; recommend fitting to geometric silhouette model (e.g., NATO "man-as-box")

______________________________________________________________________

**Last updated:** 2026-05-24\
**Maintained by:** @librarian\
**Source repository:** https://github.com/[project]/doc-reference/
