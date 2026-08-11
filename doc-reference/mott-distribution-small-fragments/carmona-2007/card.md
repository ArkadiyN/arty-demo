# Fragmentation processes in impact of spheres

**Carmona et al., arXiv:0711.2993v1 [cond-mat.stat-mech] (2007)**

**Source**: Computational Physics simulations (3D Discrete Element Model) of brittle sphere impact fragmentation. Material: polymers (PMMA, PA, nylon analogue). Sphere diameter D = 16 mm; impact velocity range: 115–140 m/s.

## Fragment mass distribution: small vs large

**Critical finding for sub-gram validation**: Fragment distribution exhibits **two regimes** (see `V. RESULTING FRAGMENT MASS DISTRIBUTION`):

- **Small fragments (m < m_transition)**: Power law `F(m) ∼ m^(-τ)` with **τ = 1.9 ± 0.2** (also reported as 2.2 ± 0.02 with exponential cutoff included)
- **Large fragments (m > m_transition)**: Two-parameter Weibull distribution `Q₃(s) = 1 − exp[−(s/s_c)^k_s]` with s_c = 0.75, k_s = 5.8

**Transition mass**: m ≈ 1/40 of sample mass (~550 elements out of ~22,000), normalized m̄₀ = 0.004 ± 0.001

## Key equations

Small fragment regime (normalized mass m < 1/40):

```
F(m) ∼ m^(-τ) f(m/m̄₀)    where f contains exp(-m/m̄₀)
τ = 2.2 ± 0.02 (with cutoff)
or τ = 1.9 ± 0.2 (power law only)
```

Large fragment regime (m > 1/40):

```
F(m) = k_l (m/m̄_l)^(k_l-1) exp(-(m/m̄_l)^k_l)
m̄_l = 0.3 ± 0.02, k_l = 1.9 ± 0.1
```

## Mott vs observed

The paper invokes "Mott's fragmentation theory for expanding rings" to explain meridional crack formation (`zone, that we observe to be the onset of the meridional cracks when we trace them back...could be explained by the basic ideas of Mott's fragmentation theory for expanding rings`) but explicitly notes that the resulting small-fragment distribution is **power law, not exponential**.

## Coverage

Direct measurement of fragmentation from ~550 elements up to sample-scale (22,000 total). The transition at ~1/40 sample mass maps to a characteristic length ~4× the element diameter (0.5 mm → ~2 mm equivalent fragment size). **Does not directly probe the 0.166–0.6 g range**, but establishes power-law form in small-mass tail; extrapolation to sub-gram would follow the same exponent unless a break occurs at even finer scales.

## Source

Pages 8–9 (`V. RESULTING FRAGMENT MASS DISTRIBUTION`, `Figure 10`, `Figure 11`, `Eq. 7`); confirmed page 296 (Conclusions).

**PDF**: source.pdf (11 pages, arXiv preprint)
