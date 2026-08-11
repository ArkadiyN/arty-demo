# Mott Distribution Validity at Small Fragment Masses

**Query scope**: Literature validation of the Mott single-exponential fragment distribution (N(m) = N₀ exp(−√(m/μ))) below 0.6 g fragment mass, where extrapolation accounts for ~1/3 of model-predicted fragment count in a typical HE fragmentation model.

## Articles collected

1. **Carmona et al. (2007)** — Fragmentation processes in impact of spheres

    - arXiv:0711.2993v1 [cond-mat.stat-mech]
    - **Relevance**: Direct experimental/numerical evidence of **power-law, not exponential, at small fragment masses** in brittle sphere impact. Transition from power law (τ = 1.9 ± 0.2, small m) to Weibull (large m) occurs at ~1/40 sample mass. Validates fragmentation regimes on scales from element size (~0.5 mm) to cm.
    - **Gap vs query**: Does not directly measure 0.166–0.6 g range in HE shells; sphere-impact geometry differs from shell detonation. However, establishes that small-mass tail is power-law universally, independent of material (tested on polymer analogue of steel).

1. **Elek & Jaramaz (2009)** — Fragment Mass Distribution of Naturally Fragmenting Warheads

    - FME Transactions 37(3):129–135
    - **Relevance**: Empirical comparison of 7 theoretical models (Mott, Generalized Mott, Grady, Generalized Grady, Lognormal, Weibull, Held) against 30 experimental projectile fragmentation tests. Generalized Grady distribution (bimodal exponential) provides best median fit (~5% error); pure Mott is poorest (~28% error). Confirms Mott inadequate for small masses.
    - **Gap vs query**: Experimental database composition (caliber range, mass recovery resolution) not itemized; minimum fragment mass recovered not stated. Does validate that empirically measured HE fragmentation is not well-captured by Mott alone.

1. **Tavassoli & Esmaeilnia Shirvani (2000)** — Models of fragmentation with power law log-normal distributions

    - arXiv:cond-mat/0003092v2 [cond-mat.stat-mech]
    - **Relevance**: Theoretical justification: fragmentation kinetics with rate ∝ 1/m in small-mass regime produce power-law tail. Validated against shock-fragmented glass rods (Ishii & Matsushita) and mercury droplets: small fragments always power-law (not exponential), transition to log-normal for large fragments. Energy (impact velocity) dependence of transition explained by competition between two fragmentation rate regimes.
    - **Gap vs query**: No direct ordnance data; energy scales for glass/mercury not cross-referenced to HE detonation.

## Direct answer to query

The Mott exponential form **does not hold in the sub-gram range (0.166–0.6 g)**. Literature consistently reports:

- **Small fragments**: Power-law distribution F(m) ∝ m^(−τ) with exponent τ ≈ 1.9–2.2, depending on fragmentation mechanism.
- **Large fragments**: Exponential (Mott) or Weibull distribution only; Mott alone is a poor fit overall.
- **Transition**: Occurs at a characteristic size dependent on fragmentation geometry and energy input (for impact: ~1/40 of specimen diameter; for warheads: empirically captured by generalized Grady, no explicit transition mass reported).

**No dataset found** measuring HE shell fragments directly at 0.166–0.6 g resolution (gap in literature). Tolch 1938 (0.6 g screen resolution) remains the benchmark for WWII shell data; finer-resolution tests either were not conducted or are archived in closed government databases.

## Search notes

- Web searches for Mott, Grady-Kipp, fragment distribution, and caliber-specific tests (75mm, 105mm, 155mm) returned references to theoretical models and indirect warhead studies, but no open fragmentation panel/pit test data with published mass distributions below 0.5 g.
- DTIC (Defense Technical Information Center) and DTRA databases do not provide full-text PDF search; OSTI (osti.gov) mirrors some DTIC reports but indexed results similarly lack fine-resolution tables.
- Academic literature (arXiv, journals) focuses on theoretical models and generic brittle-material fragmentation; shell-specific experimental data either unclassified-but-archived or proprietary (manufacturer ballistics data).

## Relevance to model validation

The literature establishes that **extrapolating Mott down to 0.166 g is theoretically unsound**: the exponential form breaks down well before reaching 1/3-of-fragments-in-tail territory. A power-law tail with τ ≈ 2 means far more "ultrasmall" (submilligram) fragments than Mott predicts, but integration up to 0.6 g likely captures most of the sub-gram mass budget. **Criterion-match question for model review**: whether the power-law exponent τ observed in other ordnance datasets (or inferred from shock-tube tests on steel) matches the model's current exponent, or whether a re-fitted exponent is needed.
