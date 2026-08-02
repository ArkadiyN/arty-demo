# Derivation — Mott fragment shape closure (Option A via Gold eq. 6)

Scope: the closure from Mott's fracture-spacing length `x₀` to the Mott mass
parameter `μ` in `mott_params()`. Option A is approved in `scoping.md`; this
pass settles §4's two factor questions, fixes the closed form, and runs §7's
checks. No `src/arty/` edits here.

## 1. Governing equations (sourced)

| # | Equation | Source |
| --- | --- | --- |
| (G2) | `x₀ = (2σ_F/ργ′)^{1/2}·r/V`, at the instant of fracture, with `r` the ring radius **at break-up** | Gold 2017 eq. (2), `…conwep/1-s2.0-S221491471730079X-main.md:58-60`; Mott 1947 line after eq. (5), `…gurney-equations-fragmentation/rspa.1947.0042.md:158` |
| (G4) | fragment idealised as a parallelepiped `l₀ × x₀ × t₀`; `μ = ½αρx₀³`, `α = (l₀/x₀)(t₀/x₀)`; `μ` ≡ **half** the mean fragment mass | Gold eq. (4), lines 70-76, and line 54 |
| (G6) | `γ ≡ α^{-2/3}γ′` — shape absorbed into a redefined constant | Gold eq. (6), line 78 |
| (G16) | `μ = √(2/ρ)·(σ_F/γ)^{3/2}·(r/V)³` (algebraically identical to the coded line, `fragmentation.py:211-215`) | Gold eq. (7)≡(16) |
| (M1) | Mott's own ruled-line statistic: fragment circumferential lengths lie mostly in `x₀…2x₀`, **average ≈ 1.5x₀** | Mott 1947 finding (1), rspa line 190 |
| (A16) | fragment width:length = **1:1.6** (mean of Mott's own aspect histogram, Grady, Hiroe; corroborated by Wilson 1:1.65, Grady 1:1.5). "Aspect ratio" is defined width÷length, so length = 1.6 × width | `…explosion-fragment-model/tables/table-4-average-aspect-ratios.csv`; anchors "Approximate average ratio" (Table 4) and "aspect ratio of a fragment is defined" (§2.5) — **re-baselined against the retained scan 2026-08-02**, ledger §16 |

Working symbols: `x̄` mean circumferential breadth [m]; `l̄` mean axial length
[m]; `t₀` fragment thickness [m]; `A ≡ l̄/x̄` [-]; `κ_x ≡ x̄/x₀` [-]; `t`
as-manufactured wall [m]; `t_bu` wall at break-up [m]; `r_mean = ½(r_o+r_i)`,
`r_bu` mid-wall radius at break-up [m]; `γ′` Mott material constant (the
`SteelParams.gamma` field, unchanged); `γ` the shape-absorbed constant fed to
(G16).

## 2. Q1 — `x̄ = 1.5·x₀` (Mott, not Gold)

Read from source, not the cards. Mott introduces `x₀` as the *half-width of the
unstressed zone* round a fracture (his eq. (5) preamble), then says only that
it "is on dimensional grounds obviously proportional to the average fragment
length" (rspa:160). He then measures the average from his ruled-line Monte
Carlo and reports **1.5x₀** (rspa:190). Gold restates the same expression but
labels it "the average circumferential length of the resulting fragments"
(conwep:58) — i.e. Gold has silently set `κ_x = 1`, dropping Mott's factor.

**Resolution: `κ_x = 1.5`.** Mott is the primary source and the only one who
actually measures the mean; Gold is restating him and his label conflicts with
Mott's own finding (1). Note the histogram Mott averages is of *intervals
between adjacent cuts on the ruled circumference* — exactly the circumferential
breadth `x̄` that enters (G4), so the two are the same quantity.

Worth `κ_x² = 2.25×` on `μ` under the plate closure (`μ ∝ x̄²`).

## 3. Q2 — `t₀ = t_bu` (thinned), forced by area closure

`_shell_geometry` (`fragmentation.py:189-196`) applies the PAFRAG `V/V₀ ~ 3`
cavity-expansion rule, `r_i,bu = √3·r_i`, then conserves metal cross-section,
`r_o,bu² − r_i,bu² = r_o² − r_i²`. **The bookkeeping is sound** — that second
line *is* plane-strain incompressibility of the wall annulus (no axial
extension assumed), and it yields the exact identity

$$t_{bu}\,r_{bu} = t\,r_{mean} \qquad (1)$$

since `(r_o,bu − r_i,bu)(r_o,bu + r_i,bu) = r_o² − r_i² = t(r_o + r_i)`.
Verified numerically to machine precision on all four registry shells (§7.1).
Sanity: the implied outer-diameter expansion is 1.47–1.55×, inside Mott's own
"case bursts at 1.5–2× original diameter" regime.

The choice is then **not** a preference — it is forced by consistency with
(G2). `x̄` is defined *at break-up* (`r = r_bu`), so the fragment breadths tile
the **expanded** mid-surface, of area `2πr_bu·L`. The `N₀` fragments must tile
exactly that surface:

$$N_0\,\bar x\,\bar l \;=\; \frac{M}{\rho\,t_0}
\quad\text{(from } N_0 = M/2\mu,\ 2\mu = \rho\bar l\bar x t_0\text{)}$$

and the true break-up mid-surface area is `M/(ρ t_bu)`. So `t₀ = t_bu` is the
only choice for which the fragment tiling closes on the real case. Using the
as-manufactured `t` with a break-up breadth would require the case to have
`r_bu/r_mean = 1.63×` more steel than it has — it invents 63 % of the mass.
Checked numerically: tiling ratio 1.0000 with `t_bu`, 1.6346 with `t` (§7.1).

The engineering statement "most fragments have the same thickness as the
casing's thickness" (explosion-fragment-model:34) is not a counter-example: it
is the *thin-case 2-D modelling assumption* behind the `M_A = B_m t^{5/6}…`
correlation, which never tracks expansion — its fitted `B_m` absorbs the
thinning. It cannot be mixed with an explicitly expanded `r_bu`.

## 4. Closed form

Mean fragment mass `2μ = ρ·l̄·x̄·t₀ = ρ·A·x̄²·t_bu`, with `x̄ = κ_x x₀` and
(G2):

$$\boxed{\;\mu \;=\; A\,\kappa_x^{2}\;\frac{\sigma_F\,t_{bu}}{\gamma'}
\left(\frac{r_{bu}}{V_0}\right)^{2}\;=\;3.6\,
\frac{\sigma_F\,t_{bu}}{\gamma'}\left(\frac{r_{bu}}{V_0}\right)^{2}}
\qquad (2)$$

with `A = 1.6` (A16), `κ_x = 1.5` (M1), `A κ_x² = 3.6`. Using identity (1) this
is equivalently `μ = 3.6 (σ_F/γ′)·t·r_mean·r_bu/V₀²` — linear in the
as-manufactured wall.

**Recommended implementation form** (keeps the module visibly
Gold-eq-(16)-compatible, per scoping §3's note):

$$\alpha \;=\; A\,\kappa_x^{2}\,\frac{t_{bu}}{x_0}\;=\;3.6\,\frac{t_{bu}}{x_0},
\qquad \gamma \;=\; \alpha^{-2/3}\gamma',
\qquad \mu = \sqrt{2/\rho}\,(\sigma_F/\gamma)^{3/2}(r_{bu}/V_0)^{3}
\qquad (3)$$

`x₀` inside `α` is evaluated with `γ′` (G2) — there is no fixed-point loop:
(3) is pure algebra on (2), verified bit-identical numerically (§7.1).
`σ_F`, `γ′`, `ρ`, and `N₀ = M/2μ` are untouched. `SteelParams.gamma` keeps its
meaning as Mott's per-grade material constant `γ′`, so the `wdss1-steel-grade`
carbon interpolation survives.

### Structural consequences

- **`ρ` cancels exactly.** `x₀² ∝ 1/ρ` and the mass carries `ρ`. Old form had
    `μ ∝ ρ^{-1/2}`. Steel density is now a pure pass-through to drag/KE.
- **Only `σ_F/γ′` is identifiable**, as before (memory:
    `gotcha_steel_sigma_gamma_ratio_only`) — the existing identifiability test
    still holds.
- **Grade sensitivity weakens** from `μ ∝ γ′^{-3/2}` to `μ ∝ γ′^{-1}`: the
    WDSS1/HE-shell contrast drops from 1.63× to 1.38×. Direction unchanged
    (lower `γ′` → heavier fragments), so the sign-based grade tests still pass.
- **`r_bu` sensitivity weakens** from `r_bu³` to `r_bu¹` (via (1)), so `μ` is
    now only mildly exposed to the `V/V₀ ~ 3` rule of thumb — an error in the
    break-up radius costs 1× not 3×.
- **`V₀` sensitivity weakens** from `V^{-3}` to `V^{-2}`, so the deferred
    break-up-velocity item (scoping §5) is worth ~1.6–1.8×, not 2–3×.
- **`wall_t` is now first-order** (`μ ∝ t¹`). For the 75 mm M48 it is a
    caliber-scaled estimate (`shells.py:57`) — this is the update's largest
    unsourced lever (scoping §6 ask 2).

## 5. Unit and limit checks

1. **Units of (2).** `[σ_F t (r/V)²] = (kg·m⁻¹s⁻²)(m)(s²) = kg`. ✓ `α`, `κ_x`,
    `A`, `γ′` dimensionless. `μ` in kg with no conversion factor.
1. **Cube limit.** Set `A = 1`, `κ_x = 1`, `t₀ = x₀`. Then `α = 1`, `γ = γ′`,
    and (3) is character-for-character the current coded expression
    `√(2/ρ)(σ_f/γ)^{3/2}(r_bu/V₀)³`. ✓ The change is exactly "α = 1 → α = 3.6
    t_bu/x₀".
1. **Positivity / monotonicity.** All factors in (2) are positive.
    `∂μ/∂t_bu, ∂μ/∂σ_F, ∂μ/∂r_bu > 0`; `∂μ/∂γ′, ∂μ/∂V₀ < 0`. ✓ (scoping §7.1)
1. **`α > 1` always here** (3.4–6.1 across the registry), hence `γ < γ′`:
    3.6 t_bu/x₀ > 1 whenever the wall at break-up exceeds ~0.28 of the
    fracture spacing — true for every shell in the registry.
1. **Degenerate-shape guard.** (2) is well defined for any `t_bu > 0`; the
    physical validity of the *thin-case* idealisation degrades once
    `t_bu ≳ x̄`. Registry values `t_bu/x̄` = 0.63 (75 mm), 0.86 (105 mm), 0.95
    (155 mm), 1.14 (60 mm) — the 60 mm mortar is past the thin-case regime and
    should carry a limitation note.

## 6. Fragment dimensions produced (75 mm M48, `V₀ = 807.5 m/s`)

`x₀ = 3.91 mm` → `x̄ = 5.87 mm`, `l̄ = 9.39 mm`, `t_bu = 3.67 mm`;
`α = 3.379`, `γ = 28.9`. Compare Tolch's mean recovered fragment, estimated in
the ledger at ≈12 × 12 × 6 mm — the model prism is ~2× under on each in-plane
dimension but of the right character (a plate, not a cube).

## 7. Validation checks (scoping §7)

Script: `experiment/_scratch/mott_shape_closure.py`.

### 7.1 Identities and units — PASS

| check | result |
| --- | --- |
| `t_bu·r_bu = t·r_mean` (identity 1) | exact on all 4 shells |
| (2) vs (3) vs explicit `½ρl̄x̄t_bu` | agree to displayed precision on all 4 shells |
| tiling `N₀x̄l̄` vs `M/(ρt_bu)` | ratio **1.0000** (vs 1.6346 using `t`) |
| cube limit `A=κ_x=1, t₀=x₀` | reproduces current code |

### 7.2 Mass closure — PASS

`∫₀^∞ m·(−dN/dm)dm = 2N₀μ = M`. Numerically 5755.20 g vs `M` = 5755.20 g for
the 75 mm. Exact by construction of `N₀ = M/2μ`; Gold's eq. (17) `N₀ = m/μ`
contradicts his own line 54 and is not followed.

### 7.3 Tolch spectrum (75 mm M48) — PASS, large end essentially closed

| screen cut (g) | Tolch `N(>m)` | current | **new** | new/Tolch | old/Tolch |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 33.72 | 6 | 0.1 | **5.3** | 0.89 | 0.01 |
| 6.00 | 278 | 78.1 | **231.9** | 0.83 | 0.28 |
| 1.57 | 533 | 923.2 | **888.4** | 1.67 | 1.73 |
| 0.63 | 675 | 2382.0 | **1487.9** | 2.20 | 3.53 |

`μ`: 0.235 g → **0.793 g**; `N₀`: 12 256 → **3 627**. The heavy-fragment
deficit (the screening-immune defect signature) closes from 3.6× and 100× to
1.2× and 1.1×; the fine-end over-count improves 3.53× → 2.20×, i.e. does not
worsen. The residual crossover is Mott's known over-prediction of fines
(explosion-fragment-model:36 weakness 3), not this closure.

Against the fidelity target (scoping §8): `N(>6 g)` within 2× of 278 — **PASS**
(0.83×). `μ` inside 0.95–3.5 g — **marginal miss**, 0.79 g is 1.20× under the
floor. That residual is the right size and sign for the deferred break-up-
velocity item (§4, worth ~1.6–1.8× on its own) and per scoping §5 must be left
standing, **not** absorbed by tuning `A` or `κ_x`.

### 7.4 Transfer to 105 / 155 mm — PASS with a re-interpreted band

| shell | `α` | `γ` | `μ` old → new (g) | `N₀` old → new | `N(>0.5 g)` new |
| --- | ---: | ---: | ---: | ---: | ---: |
| 75 mm M48 | 3.38 | 28.9 | 0.235 → 0.793 | 12 256 → 3 627 | 1 640 |
| 105 mm M1 | 4.66 | 23.3 | 0.331 → 1.538 | 18 217 → 3 913 | 2 213 |
| 155 mm M107 | 5.15 | 21.8 | 0.919 → 4.738 | 18 892 → 3 665 | 2 648 |
| 60 mm M49A2 | 6.15 | 14.0 | 0.071 → 0.439 | 5 307 → 863 | 297 |

`μ` scales monotonically with caliber and stays inside Tolch's 0.95–3.5 g
bracket for 105 mm; 155 mm sits above it, as expected for a shell 6× heavier.
The resulting `γ` = 21.8–28.9 for the three gun shells lands inside Gold's own
published 20–50 range for this parameter (conwep lines 190, 212, 218) —
independent corroboration that `α` is the right size. The 60 mm falls to
`γ` = 14, below Gold's range, consistent with §5.5's finding that it is past
the thin-case regime.

**Nominal FAIL against scoping §7 check 4 as written**, and against
`tests/test_fragmentation.py::test_mott_fragment_count_in_pafrag_range[_all_grades]`:
`N(>0.5 g)` now falls **below** the 3 000–8 000 band (2 213 at M1 geometry).
This is judged the correct outcome, not a regression: that band is Gold running
the *same, un-shape-corrected* eq. (16) at `γ = 50` — a model-to-model
consistency check, as the ledger (§3) and the code comment both say. The
**data** row in the same source is arena recovery **800–3 000** for `>0.5 g`,
and the new values (1 640 / 2 213 / 2 648) sit inside it where the old ones sat
at or above its top. The src pass must therefore re-base those two tests onto
the 800–3 000 recovery band and record why in the test comment; silently
widening the old band would re-import the defect this update removes.

### 7.5 Option C cross-check (Mott `M_A` engineering form) — PASS for gun shells

`√μ = B t^{5/6} d_i^{1/3}(1 + t/d_i)`, `B = 0.0554 g^{1/2} mm^{-7/6}` (ledger
value, **uncited** — Needham's `B_m` table is not in `doc-reference/`).

| shell | Option C `μ` (g) | Option A `μ` (g) | A/C |
| --- | ---: | ---: | ---: |
| 75 mm M48 | 1.155 | 0.793 | 0.69 |
| 105 mm M1 | 2.974 | 1.538 | 0.52 |
| 155 mm M107 | 8.057 | 4.738 | 0.59 |
| 60 mm M49A2 | 1.379 | 0.439 | 0.32 |

Within the ~2× pass criterion for all three gun shells, and consistently on the
low side by a near-constant factor ≈1.8 — again the size and sign of the
deferred break-up-velocity item. The 60 mm misses at 3.1×, consistent with the
thin-case breakdown noted in §5.5.

### 7.6 Regression expectations for the src pass

- `test_mott_params_depend_only_on_sigma_f_over_gamma` — still passes: (2)
    depends on `σ_F/γ′` only.
- `test_wdss1_gives_fewer_larger_fragments_than_baseline`,
    `test_higher_gamma_gives_smaller_mu` — sign unchanged, still pass (the
    comment "`μ ∝ (σ_f/γ)^{1.5}`" in the latter needs updating to `∝ γ′^{-1}`).
- `test_mott_fragment_count_in_pafrag_range[_all_grades]` — **will fail**, must
    be re-based per §7.4.
- Field outputs: `N₀` drops 3.4–5.2×, so hit counts and `B(r)` should fall by
    roughly that factor while per-fragment reach rises (`μ` up 3.4–5.2× ⇒
    retardation `λ ∝ m^{-1/3}` down ~1.5–1.7×). R50 is expected to move little
    (memory: `gotcha_r50_insensitive_to_steel` — count and per-fragment reach
    offset); a large R50 move would be a signal to re-check, not a pass.
- The `B(r)` comparison in `b-vs-range.qmd` is expected to
    **improve on count and worsen nothing on decay shape** — that chart's
    residual is the drag gap, which this change does not touch.

## 8. `C_shape` internal-consistency note (scoping §4, third item)

`retardation_coeff` (`fragmentation.py:220-227`) encodes presented area as
`A = C_shape·(m/ρ)^{2/3}` with `C_shape = 0.90` (`fragmentation.py:113`,
already flagged as unsourced in `_limitations.qmd:99`). For a convex body the
orientation-averaged projected area is `S/4` (Cauchy). Evaluated on the
fragment this derivation now asserts (75 mm: 9.39 × 5.87 × 3.67 mm):

- tumbling-average `C_shape` for the derived **prism** = **1.61**
- tumbling-average `C_shape` for a **cube** = **1.50**
- coded value = **0.90**

**Finding: adopting an explicit prism `α` does not create a material new drag
inconsistency.** The prism and the cube differ by only 8 % in tumbling-average
presented area; the real discrepancy — a factor ≈1.7 between the coded 0.90 and
*any* compact tumbling shape — pre-exists this change and is unaffected by it.
It points in the same direction as the known velocity-decay gap (the model
under-decelerates fragments, `b-vs-range.md`).

Action for the src pass: **documentation only** — extend the existing
`_limitations.qmd` `C_shape` entry with the numbers above and the note that
`C_shape` and `α` now describe the same fragment and should be revised
together. Do **not** change `DragParams` in this update: raising `C_shape`
here would silently fold a drag correction into a mass-closure change and make
the Tolch and Ordnance-1944 residuals un-attributable (the same argument that
defers scoping §5). `explosion-fragment-model` §5's warning that cubic
assumptions corrupt drag is thereby logged, not acted on.

## 9. Assumptions

1. **A9.1 Product-of-means closure.** (G4) sets mean mass = `ρ·l̄·x̄·t₀`,
    i.e. `⟨l x t⟩ ≈ ⟨l⟩⟨x⟩⟨t⟩`. With `l ∝ x` at fixed aspect ratio the exact
    mean is `ρAt₀⟨x²⟩`, and `⟨x²⟩ > ⟨x⟩²`. Under the exponential-breadth
    distribution implied by Mott's own `N(m) ∝ e^{-√(m/μ)}` with `m ∝ x²`,
    `⟨x²⟩/⟨x⟩² = 2` — but that exponential contradicts Mott's histogram (which
    peaks near `x₀…2x₀`, not at 0), so the true factor is between 1 and 2. This
    is a known internal inconsistency of the Mott framework, not of this
    closure; it biases `μ` **low** by ≤2×, the same direction as the residual
    in §7.3/§7.5. Not corrected — doing so would double-count with the deferred
    break-up-velocity item.
1. **A9.2 Aspect ratio is caliber- and material-independent.** `A = 1.6` is a
    cross-dataset average (steel, W-alloy; cylindrical and ogival casings).
    Sensitivity: `μ ∝ A`, so the 1.5–1.65 literature spread is ±5 % on `μ`.
1. **A9.3 `κ_x = 1.5` is read off Mott's ruled-line Monte Carlo**, which is a
    1-D model of circumferential fracture, not a measurement of real fragments.
1. **A9.4 Uniform break-up state.** A single `t_bu`, `r_bu`, `V₀` is applied to
    the whole case; ogive and base regions expand less than the cylinder. Zone
    mass splitting is handled elsewhere (`zones.py`) and is unchanged.
1. **A9.5 `V/V₀ ~ 3` cavity-expansion rule** (Gold, conwep:56) is retained
    unmodified. It implies hoop true strain ≈ 0.49 at fracture, which is high
    for a hardened 0.35–0.45 %C shell steel; if break-up is in fact earlier,
    `r_bu` and `t_bu` move in opposite directions and (2) is only *linearly*
    exposed via `r_bu` (§4). Not chased.
1. **A9.6 `wall_t` for the 75 mm M48 is a caliber-scaled estimate**
    (`shells.py:57`) and is now first-order in `μ`. Optional @librarian ask
    (scoping §6.2) — this update proceeds without it; a ±20 % wall error is
    ±20 % on `μ`, inside the factor-2 fidelity target.
1. **A9.7 The break-up-velocity item (scoping §5) is deliberately left open.**
    The ~1.2–1.8× residual in §7.3/§7.5 is its predicted size; absorbing it into
    `A` or `κ_x` is forbidden.
