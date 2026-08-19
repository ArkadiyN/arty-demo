# Derivation — Mott fragment shape closure (Option A via Gold eq. 6)

Scope: the closure from Mott's fracture-spacing length `x₀` to the Mott mass
parameter `μ` in `mott_params()`. Option A is approved in `scoping.md`; this
pass settles §4's two factor questions, fixes the closed form, and runs §7's
checks. No `src/arty/` edits here.

> **As of 2026-08-09 — every 75 mm M48 number in this document is a
> record of the shape-closure transition as it stood then, not a current
> model value.** A later change (the M48 fuze/case-mass correction) re-sourced
> that shell's `mass_deductions`, moving the shipped inputs to
> `M_case = 4980.0 g`, `V₀ = 864.4 m/s`, `μ = 0.826 g`, `N₀ = 3016`
> ([`../75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py`](../75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py)).
> The historical figures below — `V₀ = 807.5 m/s` (§6 heading), the mass-closure
> integral `5755.20 g` (§7), and the `μ`: 0.235 → 0.793 g / `N₀`: 12 256 →
> 3 627 transition (§8 and its table) — are **deliberately left as recorded**.
> They document *this* change's before/after on *its own* case mass, and the
> 5755.20 g mass-closure identity is a verification that closed against that
> mass; restating either onto 4980.0 g would falsify the record of what was
> checked. The closure itself is unaffected: it is a relation between `μ`,
> `N₀` and `M_case` that holds identically on the new mass (2·3016·0.826 g =
> 4982 g ≈ `M_case`), and the shape factor `α`, the `γ = α^{-2/3}γ′`
> redefinition, and the 4–15× correction ratio are all independent of
> `M_case`. Only the absolute g/count figures moved.

## 1. Governing equations (sourced)

| # | Equation | Source |
| --- | --- | --- |
| (G2) | `x₀ = (2σ_F/ργ′)^{1/2}·r/V`, at the instant of fracture, with `r` the ring radius **at break-up** | Gold 2017 eq. (2), `…conwep/1-s2.0-S221491471730079X-main.md:58-60`; Mott 1947 line after eq. (5), `…gurney-equations-fragmentation/`, p.304 line after eq. (5), anchor `The length` (verified against the retained scan 2026-08-02: the page reads `x₀ = (2P_F/ργ)^{1/2}·r/v`, agreeing with Gold symbol-for-symbol; the `.md` extraction of this line is corrupt — see that document's `card.md`) |
| (G4) | fragment idealised as a parallelepiped `l₀ × x₀ × t₀`; `μ = ½αρx₀³`, `α = (l₀/x₀)(t₀/x₀)`; `μ` ≡ **half** the mean fragment mass | Gold 2017 eq. (4), `…conwep/1-s2.0-S221491471730079X-main.md`, anchor `\tag{4}`; the parallelepiped premise one line above it, anchor `idealized with simple geometric shapes like a parallelepiped`; and the half-mean-mass definition of `μ`, anchor `is defined as one half of the average fragment mass` |
| (G6) | `γ ≡ α^{-2/3}γ′` — shape absorbed into a redefined constant | Gold 2017 eq. (6), anchor `\tag{6}`, introduced by `Since the fragment distribution relationship` |
| (G16) | `μ = √(2/ρ)·(σ_F/γ)^{3/2}·(r/V)³` (algebraically identical to the code, `arty.fragmentation.mott_params`) | Gold 2017 eq. (7), anchor `\tag{7}`; restated later in the paper as eq. (16) |
| (M1) | Mott's own ruled-line statistic: fragment circumferential lengths lie mostly in `x₀…2x₀`, **average ≈ 1.5x₀** | Mott 1947 finding (1), rspa line 190 |
| (A16) | fragment width:length = **1:1.6** (mean of Mott's own aspect histogram, Grady, Hiroe; corroborated by Wilson 1:1.65, Grady 1:1.5). "Aspect ratio" is defined width÷length, so length = 1.6 × width | `…explosion-fragment-model/tables/table-4-average-aspect-ratios.csv`; anchors "Approximate average ratio" (Table 4) and "aspect ratio of a fragment is defined" (§2.5) — **re-baselined against the retained scan 2026-08-02**, ledger §16 |

FINDING[deferrable]: Gold 2017 attributes to "Mott (1943)" both a constant fragment breadth:length ratio and an average cross-sectional area proportional to (r/V)^2, and this derivation inherits the first as the premise that A = l/x is one constant across shells; the primary (Mott & Linfoot, A.C. 3348, now retained at doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/) states the opposite twice ("we have not been able to find a theory to account for the average length of the splinters", p.2; "our theory ... does not account for the length of splinters from shells, but only for their breadth", p.4) and where sect. 3 treats length it makes it independent of breadth, while the (r/V)^2 area scaling is Mott 1947's, not 1943's — only the parallelepiped attribution survives, so the 1.6 VALUE is fine (it is Felix 2022 Table 4, ledger sect. 16) but the structural premise is not primary-backed and the Phase-3 pass on this thread should say so rather than repeat Gold's citation (affects: experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md, experiment/fragmentation-field/challenges/mott-scale-gap/_shape_closure_check.md, src/arty/fragmentation.py, doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/card.md; since: 2026-08-02)

**Anchors closed 2026-08-09.** Rows (G4), (G6), (G16) and `scoping.md`'s
governing-equation table now follow (G2)'s pattern — equation number plus a
grep-verified string. Gold's LaTeX equation tags are themselves the stablest
anchors available in this extraction (`\tag{4}`, `\tag{6}`, `\tag{7}`, each
matching exactly one line and immune to the C0-control-glyph problem that makes
the surrounding text unreliable), backed by a prose anchor where the claim is
prose rather than an equation: `idealized with simple geometric shapes like a
parallelepiped` for the shape premise and `is defined as one half of the
average fragment mass` for the `μ`/`N₀` convention. The attribution finding
directly above is untouched and remains open.

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
length" (Mott 1947 p.304, anchor `The length`). He then measures the average from his ruled-line Monte
Carlo and reports **1.5x₀** (Mott 1947 p.305 finding (1), anchor `The fragments have lengths most of which lie`). Gold restates the same expression but
labels it "the average circumferential length of the resulting fragments"
(conwep:58) — i.e. Gold has silently set `κ_x = 1`, dropping Mott's factor.

**Resolution: `κ_x` is Mott's, not Gold's `1`.** Mott is the primary source and
the only one who actually measures the mean; Gold is restating him and his label
conflicts with Mott's own finding (1). Note the histogram Mott averages is of
*intervals between adjacent cuts on the ruled circumference* — exactly the
circumferential breadth `x̄` that enters (G4), so the two are the same quantity.

**Value superseded, 2026-08-19: `κ_x = 1.62`, not `1.5`.** Mott's `1.5x₀` is his
statistic at the `l/x₀ = 20` *demonstration* configuration; the shipped fleet
sits at `l/x₀ = 84–100`, where re-running his own construction gives `⟨x⟩ =
1.62x₀`. `src/arty/` ships 1.62 (with the re-solved `k`, `c` of that same
population). Source:
[`../kappa-x-shell-regime/derivation.md`](../kappa-x-shell-regime/derivation.md)
§§2–3, assumption **X1**, which replaces A9.3 below.

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
contradicts his own definition of `μ` (anchor `is defined as one half of the
average fragment mass`, which states `N₀ = M/2μ` outright) and is not followed.

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
The resulting `γ` = 21.8–28.9 for the three gun shells (computed at the
then-shipped `γ′` = 65) lands inside Gold's own published 20–50 range for this
parameter (conwep lines 190, 212, 218) — but this table's `γ′` was re-anchored
to 54.5 in `updates/wdss1-steel-grade/derivation.md` §9.3 (the old 65 sat on
the one row of Mott 1947's table that fails the paper's own closure invariant;
`rebaseline-verdict.md` §3.2). At the re-anchored `γ′` = 54.5, on the
**currently shipped** shell geometry, the three gun shells read
`γ` = 24.5 / 20.7 / 19.4 (`wdss1-steel-grade/derivation.md` §9.3, regenerated by
its `checks/recompute.py`): only the 155 mm falls just below Gold's 20 floor;
the 105 mm sits inside the range. (`rebaseline-verdict.md` §3.3's
24.2 / 19.5 / 18.3 are the same quantities on the pre-2026-08-08 geometry, i.e.
before the 75 mm case-mass correction and the fuze-mass sourcing, and are
superseded.) So this is a **directional** corroboration that `α` is the right
size rather than a clean "lands inside" — a soft cross-check, not a PASS
criterion; no verdict here moves. The
60 mm falls to `γ` = 14, below Gold's range, consistent with §5.5's finding
that it is past the thin-case regime.

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
    mean is `ρAt₀⟨x²⟩`, and `⟨x²⟩ > ⟨x⟩²`. The exact error factorises as
    `c·k` with `c = ⟨Ax²⟩/⟨A⟩⟨x²⟩` and `k = ⟨x²⟩/⟨x⟩²`
    ([`../mass-dependent-fragment-shape/derivation.md`](../mass-dependent-fragment-shape/derivation.md)
    eq. (2)).

    **Both factors are now resolved; this assumption is closed.** `k` is
    settled in
    [`../breadth-variance-factor-k/derivation.md`](../breadth-variance-factor-k/derivation.md)
    at **`k = 1.1375`**, caliber-independent, by reproducing Mott 1947's
    ruled-line Monte Carlo and taking its second moment from the same
    configuration that supplies `κ_x = 1.5`. **`c` was re-solved in the same
    pass** (that derivation §3.0): eq. (2) is a *one-population* identity, and
    the `c` shipped 2026-08-16 is a moment weighted by the 1943-descended mass
    spectrum, so pairing it with a 1947 `k` is not the identity. On the
    ruled-line population `c` becomes 1.1254 / 1.0608 / 1.0247 / 1.0026
    (155 / 105 / 75 / 60 mm), and the fixed point closes as `μ = c·k·μ₀`.
    Net `A_eff = 1.6·c·k`: **+2.4 % at 155 mm, +24 % at 60 mm** — the small
    calibers are where this closure is worth anything, and the 155 mm B(r)
    surface cannot see it at all. The competing `⟨x²⟩/⟨x⟩² = 2` is
    **retired**: it is the exponential-breadth *assumption* Mott & Linfoot 1943
    §3 imported from the comminution literature in order to derive
    `N(m) ∝ e^{-√(m/μ)}`, not an independent result, and Mott's own 1947
    release-wave calculation contradicts it (negligible density below `0.4x₀`,
    because a crack is unlikely to nucleate inside a neighbour's release zone —
    the release-zone half-width is `√(τ−τ_j)`, which vanishes at nucleation, so
    the support is not strictly truncated).

    **The rationale previously given here — "doing so would double-count with
    the deferred break-up-velocity item" — was wrong and is struck.** `A`
    enters only via `alpha = A·κx²·t_bu/x0` whereas the break-up-velocity item
    C2 acts on `x0 ∝ 1/v_bu`; they are algebraically disjoint factors of the
    same product, verified against the shipped formula in
    [`../mass-dependent-fragment-shape/review.md`](../mass-dependent-fragment-shape/review.md).
1. **A9.2 Aspect ratio is caliber- and material-independent.** `A = 1.6` is a
    cross-dataset average (steel, W-alloy; cylindrical and ogival casings).
    Sensitivity: `μ ∝ A`, so the 1.5–1.65 literature spread is ±5 % on `μ`.
1. **A9.3 — SUPERSEDED by X1 (2026-08-19); its blocking finding is CLOSED.**
    `κ_x` is still read off Mott's ruled-line Monte Carlo, i.e. a moment of a
    **1-D fracture model, not a measurement of real fragments** — that standing
    objection carries over unchanged into X1. What is fixed is the *regime*: the
    shipped value is no longer 1.5, Mott's `l/x₀ = 20` demonstration
    configuration, but **`κ_x = 1.62`**, his model's own answer at `l/x₀ = 95`
    where the shipped fleet actually sits (`l/x₀ = 84–100`, and `r_bu` cancels,
    so one caliber-independent value serves — fleet spread 0.27 %). Realised
    effect: `μ` ×1.21–1.23, `N₀` ×0.81–0.83, matching the ~21 % this entry
    predicted. Residual, now carried as X3: `κ_x = 1.62` is the **low edge** of
    `[1.62, 1.67]` — exact Poisson sampling of the rate law Mott states gives
    1.67 (+6.5 % on `μ`); Mott's deterministic quadrature is retained on
    attributability, not physics. Source:
    [`../kappa-x-shell-regime/derivation.md`](../kappa-x-shell-regime/derivation.md)
    §§2–3, §6.1–6.2.
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

## 10. Gold 2017 provenance: shipped-code verification, the N₀ contradiction, and the two α's

Relocated 2026-08-03 from
`doc-reference/fragmentation/fragment-size-distribution-conwep/card.md`
(sections "The shipped code" and "The paper contradicts itself on N₀...",
plus the `γ = 50` bullet under "What is *not* certified"), per
`.claude/rules/source-data-fidelity.md` ("A card states what the source says,
not what to use it for") and the finding logged at
`experiment/fragmentation-field/challenges/source-data-audit/review-provenance.md:342`.
These are code-verification verdicts and a computed model output — correct,
but they belong in a derivation a reviewer reads, not in a reference card. Text
is moved verbatim; it was not re-derived or re-checked for this move. The card
retains only the source's own eq. (1)/eq. (17) contradiction as a fact about
the paper; what follows is the resolution — which side `src/arty` takes, and
why.

### The shipped code

- `mott_params` builds μ the long way — eq. (2) for `x₀`, eq. (6) to fold `α`
    into `γ`, eq. (16). Eq. (4) reaches the same μ in one step. **They agree to
    2 × 10⁻¹⁶** at three break-up velocities, which they can only do if the
    shipped `alpha ** (-2.0/3.0)` carries the sign the algebra demands.
- `μ_(7)` and `μ_(16)` are identical to 4 × 10⁻¹⁶ over a seven-point parameter
    sweep (the `½·2^{3/2} = √2` collapse), so citing either name is correct.
- **`N₀`**: the code uses `M/(2μ)` — eq. (1), *not* eq. (17).

### The paper contradicts itself on N₀, and the code takes the right side

Eq. (1) states `N₀ = M/2μ`; eq. (17) states `N₀ⱼ = mⱼ/μⱼ`. These differ by
exactly a factor of 2, and eq. (17) would double every fragment count. Eq. (1)
is the self-consistent one: μ is defined two sentences earlier as **half** the
average fragment mass, so total mass over μ counts half-fragments. At the
shipped M1 geometry the gap is 3 959 vs 7 918 fragments at V₀ = 1000 m/s.

`src/arty` follows eq. (1). Recorded here rather than repaired anywhere,
because there is nothing to repair — but any future pass that reads eq. (17)
off the page and "corrects" the code would be introducing the error.

### Gold's `γ = 50` is the shape-absorbed γ of eq. (6), not `γ′`

Gold never states α for Charge A, so his 50 cannot be converted to a `γ′`.
`_validation.qmd:48` already reads it correctly — as an "un-shape-corrected"
value, i.e. the cube limit α = 1 where γ = γ′ — and explicitly declines to
score the model against the resulting band. That reading is sound; a future
pass must not silently treat 50 as a `γ′` for `SteelParams`.

### Gold overloads the symbol α — two unrelated quantities

Gold 2017 uses `α` for two things that share nothing but the letter:

- **Eq. (4)'s fragment shape aspect-ratio** — `α = (l₀/x₀)(t₀/x₀)`, the
    parallelepiped shape factor this derivation's §1 (G4) uses throughout, and
    which feeds `γ = α^{-2/3}γ′` (G6). This is the only `α` this derivation
    computes with (§4, §7, `mott_params`). Anchor: `In the equation (4)` (the
    sentence defining it, `…conwep/1-s2.0-S221491471730079X-main.md`).
- **Section 4's detonation-wave incidence angle** — the angle between the
    detonation-wave front and the shell surface normal in the Charge B
    multi-region discussion, unrelated to fracture geometry. "The steeper angle
    α is, the higher parameter γ is" (Fig. 7(b) caption) — the *opposite* sign
    relation from eq. (6)'s aspect-ratio α, where **larger** α **lowers** γ.
    Anchors: `incident angle $\alpha$ between the detonation wave direction`
    (§4 prose) and `detonation shock wave incidence angle $\alpha$` (Fig. 7
    caption).

A future pass that looks up "Gold's α" and lands on Fig. 7(b) instead of eq.
(4) will take the sign of (G6) backwards. Nothing in this derivation uses the
Fig. 7 α; it is documented here only to block that mix-up.
