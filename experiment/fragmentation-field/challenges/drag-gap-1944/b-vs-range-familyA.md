# Family A vs. the 1944 Ordnance Dept. B-vs-range casualty data

Companion to `b-vs-range.md` / `b-vs-range.qmd`, which answered the same
question for **Family B** only (the Poisson binary-cut `lethal_density_point` /
`four_zone_lethal_density_field` kernel) and returned a FAIL. This document
closes the deferred half: **Family A**, the graded ES-310
$P_{k|\text{hit}}(E)\cdot A_p(\gamma)$ mass-integral kernel
(`_four_zone_familyA_eval`), reduced to the card's $B$ per `b-vs-range.md` §2.

**Headline.** Family A **PASSES** the §4 factor-of-2 criterion at every
tabulated range, for all three registry shells (33/33 points, 0.51×–1.45×),
and its $B(r)$ is monotonically non-increasing as §4 requires. But the two
families **disagree with each other** by more than the same 2× band at 26/33
points (Family A runs 0.19×–0.71× of Family B) — a §4 family-divergence
finding. That divergence is **threshold-confounded** (§4 below), and the
same confound means Family A's agreement with the card is a *cancellation of
two offsetting errors*, not an independent validation. See §5.

## 1. What was run

Script: `checks/b-vs-range-familyA.py` (its docstring carries the exact
reduction). Family B numbers are not re-derived — the script imports the three
published per-caliber modules `checks/b-vs-range-{75,105,155}mm.py` and calls
their own `b_model_at_range`, so both families run at identical ranges, AoF,
posture and drag calibration.

| Setting     | Value                                                                                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Drag        | `DragParams()`, $C_D = 1.28$, $C_\text{shape} = 2.0890$, combined $2.674$ (current calibration, commit `e8c9602`)                                                                           |
| Burst       | $h_b = 0$ (ground burst, matching the card's ground-burst tables)                                                                                                                           |
| Spray belt  | $\delta = 15°$ half-width (four-zone default)                                                                                                                                               |
| Posture     | `STANDING` ($w_\perp = 0.5$, $h = 1.7$, $d = 0.3$ m)                                                                                                                                        |
| Primary AoF | 30°; sensitivity sweep 0/15/30/45/60°                                                                                                                                                       |
| Sampling    | 200-point log mass grid; 72 azimuthal ring points, evaluated **directly** by `_four_zone_familyA_eval` (no grid interpolation, unlike the Family B checks, which read a 121×121 field grid) |

**Per-zone $A_p$ inversion.** `b-vs-range.md` §2 says to divide out "the
$A_p(\gamma)$ the builder already computes." Family A relocates each zone's
belt to its own representative height $z_\text{rep}$, so there is no single
$A_p$ at a ground point — each zone carries its own $\gamma_z$. The script
therefore inverts **per zone**,
$\rho_L = \sum_z N_z / A_p(\gamma_{z})$, recomputing $\gamma_z$ from the same
`_belt_column_zrep_vec` call with the same arguments the builder makes, so the
division is exact rather than approximate. This is a faithful reading of §2,
not an extension of it.

## 2. Per-shell results ($B$ in effective hits / sq ft, AoF = 30°)

### 75 mm M48 HE (Table 43)

| $r$ (ft) |     $B_A$ |     $B_B$ | $B_\text{card}$ | A/card | B/card |   A/B |         $B_A$ AoF band |
| -------: | --------: | --------: | --------------: | -----: | -----: | ----: | ---------------------: |
|       20 |    0.1201 |    0.3230 |          0.1060 |   1.13 |   3.05 | 0.372 |       [0.1033, 0.3025] |
|       30 |   0.04301 |    0.1263 |          0.0391 |   1.10 |   3.23 | 0.341 |       [0.0394, 0.1011] |
|       40 |   0.01973 |   0.06273 |          0.0192 |   1.03 |   3.27 | 0.314 |     [0.01772, 0.04169] |
|       60 |  0.006604 |   0.02191 |          0.0066 |   1.00 |   3.32 | 0.301 |    [0.006021, 0.01274] |
|       80 |  0.002583 |   0.00977 |          0.0030 |  0.861 |   3.26 | 0.264 |   [0.002583, 0.005025] |
|      100 |  0.001254 |  0.004989 |          0.0016 |  0.784 |   3.12 | 0.251 |   [0.001254, 0.002445] |
|      130 | 0.0004888 |  0.002125 |          0.0006 |  0.815 |   3.54 | 0.230 | [0.0004888, 0.0009774] |
|      160 | 0.0002172 |   0.00102 |          0.0003 |  0.724 |   3.40 | 0.213 |  [0.0002172, 0.000427] |
|      190 | 0.0001095 | 0.0005302 |          0.0001 |   1.10 |   5.30 | 0.207 | [0.0001095, 0.0002076] |
|      225 | 5.144e-05 | 0.0002658 |          0.0001 |  0.514 |   2.66 | 0.194 | [5.144e-05, 9.723e-05] |

A/card 0.51×–1.13×, **10/10 in band**. B/card 2.66×–5.30×, 0/10. A/B
0.19×–0.37×, 0/10. $B_A(r)$ monotone non-increasing: yes.

### 105 mm M1 HE (Table 51)

| $r$ (ft) |     $B_A$ |     $B_B$ | $B_\text{card}$ | A/card | B/card |   A/B |         $B_A$ AoF band |
| -------: | --------: | --------: | --------------: | -----: | -----: | ----: | ---------------------: |
|       20 |    0.2326 |    0.4600 |          0.1940 |   1.20 |   2.37 | 0.506 |       [0.1987, 0.5833] |
|       30 |   0.08367 |    0.1898 |          0.0816 |   1.03 |   2.33 | 0.441 |      [0.08033, 0.2019] |
|       40 |   0.04263 |   0.09929 |          0.0424 |   1.01 |   2.34 | 0.429 |     [0.04109, 0.09403] |
|       60 |   0.01495 |   0.03830 |          0.0155 |  0.964 |   2.47 | 0.390 |     [0.01495, 0.03112] |
|       80 |  0.006478 |   0.01875 |          0.0071 |  0.912 |   2.64 | 0.345 |    [0.006478, 0.01368] |
|      100 |  0.003475 |   0.01047 |          0.0037 |  0.939 |   2.83 | 0.332 |    [0.003475, 0.00714] |
|      120 |  0.002022 |  0.006350 |          0.0022 |  0.919 |   2.89 | 0.319 |   [0.002022, 0.004152] |
|      140 |  0.001255 |  0.004079 |          0.0014 |  0.896 |   2.91 | 0.308 |    [0.001255, 0.00251] |
|      170 | 0.0006595 |  0.002265 |          0.0007 |  0.942 |   3.24 | 0.291 |  [0.0006595, 0.001304] |
|      200 | 0.0003728 |  0.001342 |          0.0004 |  0.932 |   3.35 | 0.278 | [0.0003728, 0.0007101] |
|      300 | 7.426e-05 | 0.0003093 |          0.0001 |  0.743 |   3.09 | 0.240 | [7.426e-05, 0.0001409] |

A/card 0.74×–1.20×, **11/11 in band**. B/card 2.33×–3.35×, 0/11. A/B
0.24×–0.51×, 1/11. Monotone: yes.

### 155 mm M107 HE (Table 59)

| $r$ (ft) |     $B_A$ |     $B_B$ | $B_\text{card}$ | A/card | B/card |   A/B |         $B_A$ AoF band |
| -------: | --------: | --------: | --------------: | -----: | -----: | ----: | ---------------------: |
|       20 |    0.3406 |    0.4786 |          0.2470 |   1.38 |   1.94 | 0.712 |        [0.278, 0.8113] |
|       30 |    0.1289 |    0.2047 |          0.1040 |   1.24 |   1.97 | 0.630 |       [0.1171, 0.2968] |
|       40 |   0.06492 |    0.1109 |          0.0547 |   1.19 |   2.03 | 0.586 |      [0.06248, 0.1375] |
|       60 |   0.02599 |   0.04577 |          0.0209 |   1.24 |   2.19 | 0.568 |      [0.02482, 0.0503] |
|       80 |   0.01253 |   0.02394 |          0.0102 |   1.23 |   2.35 | 0.523 |     [0.01253, 0.02391] |
|      100 |  0.007163 |   0.01426 |          0.0057 |   1.26 |   2.50 | 0.502 |    [0.007163, 0.01339] |
|      120 |  0.004513 |  0.009224 |          0.0036 |   1.25 |   2.56 | 0.489 |   [0.004513, 0.008431] |
|      140 |  0.003013 |  0.006313 |          0.0024 |   1.26 |   2.63 | 0.477 |   [0.003013, 0.005627] |
|      170 |  0.001768 |  0.003850 |          0.0014 |   1.26 |   2.75 | 0.459 |   [0.001768, 0.003184] |
|      200 |  0.001037 |  0.002502 |          0.0009 |   1.15 |   2.78 | 0.414 |   [0.001037, 0.001943] |
|      300 | 0.0002899 | 0.0007803 |          0.0002 |   1.45 |   3.90 | 0.371 | [0.0002899, 0.0005383] |
|      400 | 0.0001037 | 0.0003071 |          0.0001 |   1.04 |   3.07 | 0.338 | [0.0001037, 0.0001926] |

A/card 1.04×–1.45×, **12/12 in band**. B/card 1.94×–3.90×, 2/12. A/B
0.34×–0.71×, 6/12. Monotone: yes.

## 3. Robustness of the verdict

**AoF sensitivity** (`checks/b-vs-range-familyA-aof-ap.py`). $B_A$ rises
monotonically with angle of fall above ~15° — a steeper trajectory tips more of
each spray belt onto the near ground. The AoF band's lower edge is at 0–30°,
its upper edge always at 60°. The factor-of-2 verdict per AoF:

| Shell       | 0°                 | 15°                | 30°                | 45°                | 60°               |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ----------------- |
| 75 mm M48   | 0.62–1.28× (10/10) | 0.65–1.34× (10/10) | 0.51–1.13× (10/10) | 0.66–1.61× (10/10) | 0.97–2.85× (6/10) |
| 105 mm M1   | 0.89–1.07× (11/11) | 0.90–1.16× (11/11) | 0.74–1.20× (11/11) | 0.95–1.77× (11/11) | 1.41–3.01× (7/11) |
| 155 mm M107 | 1.13–1.62× (12/12) | 1.14–1.61× (12/12) | 1.04–1.45× (12/12) | 1.33–1.87× (12/12) | 1.93–3.28× (1/12) |

So the PASS is **not** an artefact of picking AoF = 30°: it holds unmodified
across 0°–45°, and only breaks at the 60° edge of the swept band (worst at
155 mm, 1/12). Since AoF is not carried in the shell registry, the honest
statement is "PASS for angle of fall up to ~45°, marginal at 60°."

**$A_p$ treatment.** Dividing by the flat head-on $A_p(0)$ everywhere instead
of the graded per-zone $A_p(\gamma_z)$ changes $B_A$ by **\<1%** at every probed
point (flat/graded 0.990–1.000). At $h_b = 0$ every relocation height sits
within the standing target's own height, so $|\gamma_z|$ stays small and the
smallest $A_p$ encountered anywhere in the reduction is 0.7831 m² against
$A_p(0) = 0.8500$ m² — the inversion is nowhere near ill-conditioned. The §2
reduction is therefore insensitive to which $A_p$ convention is used, which
removes the main "did the inversion introduce the answer?" objection.

## 4. Family divergence — and why it is threshold-confounded

$B_A / B_B$ runs **0.19×–0.71×** and sits outside the 2× band at 26 of 33
points, worst for the smallest shell (75 mm: 0.19×–0.37×, 0/10) and mildest
for the largest (155 mm: 0.34×–0.71×, 6/12). §4 of `b-vs-range.md` says to
report this as a finding in its own right. **Reported.**

**Caveat — this comparison is not like-for-like.** The two families are run
against *different casualty definitions*, exactly as `b-vs-range.md` §2's
"Casualty threshold" paragraph specifies:

- **Family B** is fed the card's own **58 ft-lb** (≈78.6 J) threshold as an
    explicit `E_leth` override — a hard binary cut at the historical definition.
- **Family A** uses its ES-310 `pk_given_hit(E)` curve **as-is**, a *graded*
    kill probability anchored at `E_LETH_DEFAULT` = 1000 J ≈ 737 ft-lb (the
    $P_{k|hit} = 0.5$ "moderate personnel kill" point) — roughly an order of
    magnitude stricter, applied as a soft weight rather than a cut.

The divergence's **sign is therefore expected** ($A < B$) and its **magnitude
is not attributable** to any geometric or kinematic difference between the two
kernels on this evidence alone: the threshold difference and the graded-vs-
binary difference are fully confounded with whatever else differs. Nothing
here supports a claim that one kernel's *geometry* is wrong.

**Out-of-scope follow-up (named, not implemented here):** a
*threshold-matched* Family A variant — the same `_four_zone_familyA_eval`
reduction run with the ES-310 curve re-anchored to the card's 58 ft-lb, or with
`pk_given_hit` replaced by a 58 ft-lb step — would decouple the two effects and
turn this into a real kernel-vs-kernel comparison. That is a separate aspect
(it touches the lethality-criterion definition, the same axis as
`_limitations.qmd` #14) and is deliberately not attempted in this pass.

## 5. Verdict

**PASS** against `b-vs-range.md` §4's quantitative criterion, for all three
shells: $0.5 \le B_A / B_\text{card} \le 2$ at 33/33 tabulated ranges
(0.51×–1.45×) at the primary AoF, holding across AoF 0°–45°, with a
monotonically non-increasing $B(r)$ and no spurious plateau or ring. Family A
therefore lands inside the band that Family B misses by 2–5×.

**Do not read this as an independent confirmation of Family A.** The near-unity
ratio is arithmetically the product of two offsetting factors, both visible in
the tables above:

$$
\frac{B_A}{B_\text{card}} \;=\; \underbrace{\frac{B_A}{B_B}}_{0.19\text{–}0.71}\;\times\;\underbrace{\frac{B_B}{B_\text{card}}}_{1.94\text{–}5.30} .
$$

Family B, evaluated at the card's *own* 58 ft-lb definition, says this
project's fragment field delivers **2–5× too many** effective fragments to the
ground (the FAIL in `b-vs-range.qmd` §"Key findings", traced there to residual
drag/velocity-decay under-prediction). Family A then applies a lethality
criterion that is ~10× stricter in energy, discarding roughly the same factor.
The two errors have opposite signs and comparable size, so their product lands
near 1. The right conclusion is **not** "Family A is validated and Family B is
broken" but: *the card cannot discriminate the two kernels while they run at
different thresholds.* The threshold-matched variant in §4 is what would.

A secondary, weaker observation survives the confound: $B_A/B_B$ **drifts
systematically with range** within each shell (75 mm: 0.372 → 0.194 from 20 to
225 ft; 155 mm: 0.712 → 0.338 from 20 to 400 ft) and with caliber. A pure
threshold offset would produce a range-*dependent* ratio too (fragments soften
with range, so a stricter threshold bites harder far out), so this drift is
also consistent with the confound and is **not** on its own evidence of a
geometric defect — it is simply the sharpest thing the threshold-matched
follow-up should be asked to explain.

## Scripts

- `checks/b-vs-range-familyA.py` — the per-shell tables of §2 and the
    factor-of-2 / divergence counts. Ran clean as written; no fix was needed.
- `checks/b-vs-range-familyA-aof-ap.py` — the AoF-per-angle verdict table and
    the graded-vs-flat $A_p$ comparison of §3.
- `checks/b-vs-range-{75,105,155}mm.py` — imported unchanged for the Family B
    column and for the card's transcribed `CARD_R_FT` / `CARD_B` arrays.
