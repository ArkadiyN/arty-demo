# Models of fragmentation with power law log-normal distributions

**Tavassoli & Esmaeilnia Shirvani, arXiv:cond-mat/0003092v2 [cond-mat.stat-mech] (2000)**

**Source**: Theoretical models of binary fragmentation with time-dependent transition size between two regimes. Validated against experimental fragmentation data from shock-fragmented glass rods and mercury droplets.

## Theoretical model: two regimes with transition

Introduces bilinear fragmentation kinetics (section II, model A):

- **Small fragments** (m < y_m): Fragmentation rate ∝ 1/m → produces **power-law distribution** F(m) ∼ m^(-τ)
- **Large fragments** (m > y_m): Fragmentation rate ∝ 1/m + logarithmic term → produces **log-normal distribution**

Transition size y_m(t) is time-dependent; the two regions evolve independently but coupled through the largest fragment.

## Experimental validation

Section on shock fragmentation of long thin glass rods (Ishii & Matsushita, cited as ref. 20):

> "The results of fragment size and mass distributions at small falling heights showed a log-normal form for larger fragments and a power law form for smaller fragments. The crossover was seen to be at length scales around the rod diameter."

With increasing falling height (impact energy), the distribution transitions to power-law across entire mass range. This indicates that power-law in small-mass tail is a **robust, energy-dependent feature**, not an artifact.

Mercury droplet rupture experiments show similar transition: log-normal at small falling heights shifts to power-law as height increases.

## Interpretation

The model supports that **fragmentation rate dependence on fragment size (1/m vs log(m)) determines whether exponential, power-law, or log-normal emerges**. For high-energy impact or detonation (relevant to HE fragmentation), the 1/m regime dominates small fragments, yielding power law.

## Coverage

Theoretical and semi-empirical. Direct experimental data cited from glass-rod and droplet fragmentation; caliber/mass ranges not stated. **No direct measurement of sub-gram ordnance fragments**, but provides fundamental kinetic justification for power-law at small m in impact/shock fragmentation regimes relevant to shell detonation.

## Note on extraction quality

File flagged for short-token-ratio (0.47); indicative of OCR/symbol rendering issues in parts of the mathematical exposition. Extracted equations and section headings are reliable; some mathematical derivations in sections II–IV may have character-set artifacts. Core narrative (introduction, experimental citations, conclusions) verified readable.

## Source

`Introduction` (power-law regime statement); `section on shock fragmentation of glass rods` (experimental validation, ~page 2); `Figure citations for glass rod and mercury droplet experiments`.

**PDF**: source.pdf (22 pages, arXiv preprint)

## Provenance of this card

- **Document:** S. Tavassoli and A. Esmaeilnia Shirvani, "Models of fragmentation with power law log-normal distributions," arXiv:cond-mat/0003092v2 [cond-mat.stat-mech], 2000 (verified anchor "Models of fragmentation with power law log-normal distributions" — `tavassoli-2000-power-law.md:1`).
- **`source.pdf`:** NOT RETAINED (gitignored). Document is retrievable from arXiv as arXiv:cond-mat/0003092. Reacquire if mathematical derivations in sections II–IV require verification against primary (see extraction quality note above).
- **Extraction:** tavassoli-2000-power-law.md is an OCR/heuristic extraction. The extraction-quality check flagged a short-token-ratio of 0.47, consistent with symbol/formula rendering issues common in scanned or poorly-OCR'd math-heavy PDFs. Core narrative text (introduction, experimental discussion, conclusions) is readable and was verified by grep. Mathematical derivations in sections II–IV may have OCR artifacts and should be checked against source.pdf if cited numerically.
- **Secondhand vs. primary:** This paper is primarily theoretical (models of binary fragmentation). The experimental validation section cites two published experimental studies: (1) Ishii & Matsushita (reference 20) on shock-fragmented glass rods; (2) mercury droplet rupture experiments (reference 19). Tavassoli & Esmaeilnia Shirvani do not re-conduct these experiments — they re-analyze and compare the published data to their theoretical predictions. The fragmentation kinetics theory (rate ∝ 1/m produces power-law, rate ∝ 1/m + log term produces log-normal) is the authors' own derivation, primary to this paper.
- **Experimental data verified as secondhand citations:**
    - Glass-rod experiments (Ishii & Matsushita): Tavassoli cites results showing "log-normal form for larger fragments and a power law form for smaller fragments" (verified anchor on line 20: "The results of fragment size and mass distributions at small falling heights showed a log-normal form for larger fragments and a power law form for smaller fragments. The crossover was seen to be at length scales around the rod diameter."). This is Tavassoli's paraphrase of reference 20, not a direct re-measurement.
    - Mercury droplet experiments: Similarly cited, not re-measured.
- **Key finding relevant to HE fragmentation:** The theoretical model shows that fragmentation kinetics — specifically the functional form of the fragmentation *rate* (1/m vs. 1/m + log term) — determines whether the mass distribution is power-law (small fragments) or log-normal (large fragments). This kinetic argument is primary theory and directly applicable to HE detonation regimes, though Tavassoli does not claim direct experimental validation on ordnance.
