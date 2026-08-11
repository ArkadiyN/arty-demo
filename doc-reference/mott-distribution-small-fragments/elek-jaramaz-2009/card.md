# Fragment Mass Distribution of Naturally Fragmenting Warheads

**Elek & Jaramaz, FME Transactions 37(3):129–135 (2009)**

**Source**: Experimental database of 30 fragmenting projectiles (warheads and test cylinders) compiled from five published fragmentation test series. Comparison of 7 theoretical distribution models against measured data.

## Seven distribution models reviewed

All fitted to experimental fragment mass distributions; parameters optimized by least-squares against cumulative number N(m) and cumulative mass M(m). See `Table 1. Fragment mass distribution laws and their properties` (lines 104–191).

| Model             | Formula                                   | Parameters             | Fit quality on 30 projectiles              |
| ----------------- | ----------------------------------------- | ---------------------- | ------------------------------------------ |
| Mott              | `N(m) = exp(-(m/μ)^(1/2))`                | μ (scale)              | Poor (R² avg ~0.94)                        |
| Generalized Mott  | `N(m) = exp(-(m/μ)^λ)`                    | μ, λ                   | **R² avg ~0.994** (best)                   |
| Grady             | `N(m) = exp(-m/μ)` (linear exponential)   | μ                      | Moderate (R² avg ~0.93)                    |
| Generalized Grady | Bimodal: two exponentials                 | f, μ₁, μ₂              | **R² avg ~0.997** (best); median error ~5% |
| Lognormal         | Multiplicative model                      | μ, σ                   | Good (R² avg ~0.99)                        |
| Weibull           | `N(m)` implicit in `M(m) = exp(-(m/μ)^λ)` | μ, λ                   | **R² avg ~0.996** (best); median error ~6% |
| Held              | `M(n) = 1 − exp(−Bn^λ)`                   | B, λ (cumulative form) | Good (R² avg ~0.98)                        |

## Key finding: Mott inadequate at small masses

Per `3. COMPARISONS WITH EXPERIMENTS`: "The Mott formula is generally recognized to be quite poor in matching the smallest fragment sizes." Generalized Mott (allowing λ ≠ 1/2) and especially **Generalized Grady distribution** provide best overall agreement.

**Generalized Grady is bimodal**: fits fragment distribution as superposition of two exponential regimes with distinct scale parameters μ₁, μ₂. Physical interpretation (`Figure 3`): finer fragments (central cylinder) and coarser fragments (residual casing) from distinct formation mechanisms.

## Median-based ranking (Table 3)

Against 30 experimental projectiles, median fragment mass M_median:

- Generalized Grady: median relative error ~5.3% (rank 1, preferred)
- Weibull: median relative error ~8.7% (rank 2)
- Generalized Mott: median relative error ~28.4% (rank 3)

## Coverage

Experimental data on 30 projectiles of unspecified mass/caliber range (drawn from five sources; not itemized per projectile). The paper does **not** report measured fragment mass resolution or minimum recovery size. Coefficients of determination indicate good fit to whatever mass range was recovered in source experiments, but lower-mass tail behavior not explicitly stated.

## Note on power-law claim

The paper cites a "widely applicable power-law distribution" for small fragments but notes it "cannot successfully describe the HE projectile fragmentation" overall (`line 101`), implying power law alone is insufficient for the full mass range in warhead fragmentation (a finding consistent with Carmona et al.'s bimodal power-law + Weibull model).

## Source

`Section 3. COMPARISONS WITH EXPERIMENTS` (lines 101–213); `Table 2` goodness of fit (line 227); `Table 3` median errors (line 236).

**PDF**: source.pdf (7 pages, FME Transactions)
