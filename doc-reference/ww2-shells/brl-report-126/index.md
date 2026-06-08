# BRL Report 126: Fragmentation Effects of the 75mm H.E. Shell T3 (M48)

**Report:** Ballistic Research Laboratory Report No. 126\
**Authors:** N.A. Tolch (Principal)\
**Date:** December 2, 1938\
**Institution:** U.S. Army Aberdeen Research and Development Center, Ballistic Research Laboratories, Aberdeen Proving Ground, Maryland\
**Classification:** Originally CONFIDENTIAL; now declassified (available archive.org)\
**Pages:** ~40 pages (scanned document with OCR issues on fragment photos)

## Abstract

Experimental fragmentation testing of the 75mm H.E. Shell T3 (M48) conducted via panel and pit fragmentation tests. Testing determined fragment density distribution as a function of:

- Direction from burst (nose, side, base spray)
- Distance from burst
- Remaining shell velocity at burst

Key finding: Fragment distribution concentrates into three main spray classes. Total fragment count in panel tests ≈ 5000; pit fragmentation tests averaged ≈ 780 fragments recovered.

## Scope & Test Methodology

### Test Configuration

- **Shell:** 75mm T3 (M48) HE shell, loaded complete rounds, Lot 2761-3
- **Fuze:** M39 P.D. (point detonating)
- **Explosive charge:** TNT (quantity ~0.68 kg based on existing data)
- **Empty shell + fuze mass:** 13.26–13.33 lbs (~6.0 kg)
- **Total loaded projectile:** 12.47–12.53 lbs (~5.68 kg reported as "unfuzed shell")

### Panel Tests

Four panels at radii: 15 ft, 36 ft, 75 ft, 120 ft

- Panel A (15 ft, 100° arc): Captured side spray and dense fragments
- Panels B & C (36–75 ft): Recorded fragment density attenuation
- Panel D (120 ft): Extended range data

Fragment separation by screening (4 mesh sizes):

- Screen 1: 0.16" diameter wire (0.71 sq in openings)
- Screen 2: 0.14" diameter wire (0.36 sq in openings)
- Screen 3: 0.10" diameter wire (0.053 sq in openings)
- Screen 4: 0.08" diameter wire (0.017 sq in openings)

### Pit Tests

Sand pit burial tests to capture fragments. Four complete rounds detonated.

- Fragments recovered from sand pit with hand screening
- Largest fragments picked out selectively until 60% shell weight obtained
- Final weight distribution captured

## Key Findings Directly Addressing Your Research Questions

### Q1: Which Gurney Formula for Ogive Zone (Cylinder vs. Cone)?

**Finding:** The 75mm M48 exhibits asymmetric fragmentation with distinct nose and side spray zones.

- **Nose spray:** Concentrated, higher velocity fragments (reported to average 2740 f/s for perforating fragments at side panels)
- **Side spray:** Dominant fragment population; fragments concentrated radially from burst axis
- **Base spray:** Less dense; velocity averages lower than side spray

**Implication for model:** The ogive (nose cone) and cylindrical body produce measurably different fragment trajectories. The nose spray is narrower/more forward-directed than side spray. A single Gurney formula (cylinder) is insufficient; ogive and cylinder zones should be modeled separately.

**Data quote (p.5):** "...fragments are concentrated in three main classes...with regard to the variable of distance, the density decreases with the distance, the decrease in total number of hits in the side spray averaging about 55% between the 15 and 120 ft. panels."

### Q2: Base Plate "Dead" Mass, Single Intact Fragment, or Mott-Fragmented?

**Finding:** Base fragments were recovered in pit tests but represent a small, non-dominant population.

From data table (p.5):

- Screen No. 1: 6 fragments at 15.4% of shell weight
- Screen No. 2: 272 fragments at 34.0% of shell weight
- Screen No. 3: 255 fragments at 32.7% of shell weight
- Screen No. 4: 142 fragments at 18.2% of shell weight

"...fragments caught on No. 1 screen are few in number but an appreciable part of the original shell weight, about 15%. These fragments are mostly pieces of fuze. **The most numerous and by far the heaviest group of fragments is retained on the No. 2 screen comprising about 35% of the number and 65% of the weight of metal.**"

**Implication for model:** The base plate region does NOT remain as dead mass or a single intact fragment. Instead, it fragments into a dispersed population across multiple size bins. However, the base region produces proportionally **fewer and heavier fragments** compared to the side cylinder. This suggests:

- Base plate fractures but produces larger, heavier pieces
- Fragmentation pattern differs from cylinder (possibly less energetic expansion in rear)
- Should be modeled as a distinct Mott zone with lower γ (fewer fragments) or as a single large fragment + small Mott tail

### Q3: Should Boattail be Separate Gurney Zone or Merged with Cylinder?

**Finding:** Report does not explicitly distinguish boattail from cylindrical body. The 75mm M48 is described as a standard field artillery round with typical ballistic profile, but no separate data for rear taper region.

**Implication for model:** Insufficient evidence in this report to separate boattail as independent zone. The panel/pit fragmentation data treat the round as integral nose + side + base. Recommend:

- Model boattail as **merged with cylinder** (same Gurney zone) unless later testing (NWC TP 7124 or Sandia) provides specific boattail behavior
- Monitor other documents for dedicated boattail velocity data

### Q4: Validation Data for Complete Model (Polar Distribution, Lethal Area vs. AoF)

**Finding:** YES. Panel test data provide quantitative polar fragment distribution.

From page 15 layout diagram and pages 15-16 fragment density maps:

- **Panel C (75 ft radius):** Maps fragment hit density per unit solid angle
- **Axial distribution:** Side spray dominates 0°–180° (relative to burst axis)
- **Nose/base concentration:** Concentrated forward and aft
- Density maps show gradient from dense near axis to sparse at periphery

**Quantitative validation data available:**

- Fragment count vs. panel distance (15, 36, 75, 120 ft)
- Fragment count vs. angle (relative to shell axis)
- Fragment size distribution (4-bin histogram via screening)
- Pit fragmentation count distribution

**Fragment velocity data:**
From abstract (p.1): "velocity of the perforating fragments due to the explosive charge averaged 2740 f/s, while that of the penetrating fragments was 1070 f/s."

**Implication:** This data set can directly validate:

- Polar fragment distribution model predictions (compare predicted density per steradian vs. measured hits per panel area)
- Fragment velocity ranges (measured perforating vs. penetrating velocities can anchor initial velocity distributions)
- However: **Angle of fall (AoF) not explicitly addressed**; this data is from static/low-velocity burst geometry

## Material & Metallurgical Data

No explicit steel grade or Mott γ data provided in this report. The round designation "T3 (M48)" indicates the standard WW2 US 75mm HE shell, likely low-carbon steel per contemporary military specs.

## Limitations

1. **OCR quality:** Fragment photograph pages (7–10) heavily degraded; visual interpretation difficult
1. **No dynamic velocity measurement:** Fragment velocities inferred from ballistic performance in panels, not directly measured
1. **No angle-of-fall study:** All tests assume near-vertical burst geometry
1. **No material property data:** Steel specification, hardness, grain size not documented
1. **Small sample size:** 4 complete rounds in pit tests (statistical confidence limited)

## Cross-Reference to Other Documents

- See **Sandia SAND92-0243** for modern fragment trajectory analysis and hazard zone calculations
- See **NWC TP 7124** for cylindrical warhead fragmentation physics (expansion phases, fracture modes)

## Recommendations for Model Development

1. **Use this data to validate base-case fragmentation distribution** for 75mm M48
1. **Implement separate Gurney zones:** Ogive (nose), cylinder (side), base; weight each per experimental mass fractions
1. **Test boattail hypothesis** against refined panel data if available
1. **Fragment velocity ranges:** Adopt measured 1070–2740 f/s bounds for initial velocity distribution
1. **Angle-of-fall correction:** Recognize that static burst geometry differs from impact-fuze scenarios; apply trajectory model to predict AoF-dependent lethal radius

______________________________________________________________________

**File:** `/home/arkadiy/arty_demo/doc-reference/ww2-shells/brl-report-126/index.md`\
**Processed:** May 25, 2026
