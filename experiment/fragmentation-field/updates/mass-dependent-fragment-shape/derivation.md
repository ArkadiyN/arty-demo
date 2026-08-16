# Derivation — aspect-ratio moment correction `c` on the Mott shape constant `A`

**Aspect:** the single constant `A = l̄/x̄ = 1.6` in the Mott shape closure
(`mott-fragment-shape-closure/derivation.md` eq. (2)) is a **count-weighted**
mean where the closure requires an `x²`-weighted one. Derive the multiplicative
correction `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩)`, bound it, and re-solve its leverage on the
`count-gap-1938` residual.

**Scope:** derivation only. No `src/arty/` edit, no notebook edit in this pass.
Executes Action A of `scoping.md` §6; the scoping decision (moment correction on
one constant, **not** a per-fragment `A(m)`) is settled there and not re-opened.

**Status:** derivation pass, 2026-08-16.

Checks (both runnable standalone from the repo root, <1 s each):

- `checks/aspect-ratio-moment-correction.py` — §2, §3, §4 (derives `c`, `k`).
- `checks/aspect-ratio-moment-leverage.py` — §6 (re-solves the count chain).
- `checks/bofr-at-new-mu.py` — §5 (re-runs the `drag-gap-1944` B(r) fit at the
    corrected `μ`).

---

## 1. The exact identity being corrected

The closure's mean-fragment-mass step (`mott-fragment-shape-closure/derivation.md`
(G4), §4) is

$$2\mu \;=\; \rho\,\langle l\,x\,t\rangle \;=\; \rho\,t_0\,\langle A\,x^{2}\rangle
\qquad (l = A x)\quad (1)$$

and the shipped code evaluates it as `ρ t₀ ⟨A⟩⟨x⟩²` with `⟨A⟩ = 1.6`,
`⟨x⟩ = κ_x x₀`, `κ_x = 1.5`. The full error factorises **exactly**:

$$\frac{\langle A x^{2}\rangle}{\langle A\rangle\langle x\rangle^{2}}
\;=\;\underbrace{\frac{\langle A x^{2}\rangle}{\langle A\rangle\langle x^{2}\rangle}}_{c\;\text{(this update)}}
\;\times\;\underbrace{\frac{\langle x^{2}\rangle}{\langle x\rangle^{2}}}_{k\;\text{(assumption A9.1)}}
\quad (2)$$

Both factors multiply `μ`, and `μ ∝ A` exactly (A9.2), so a correction enters
the shipped code as `A → c·A` with no other change. `N₀ = M_case/(2μ) ∝ 1/(cA)`.

**Units.** `c` and `k` are ratios of like moments — dimensionless. ✓ Eq. (2) is
an algebraic identity, not a model step, so it introduces no new units and no
new parameter beyond the two dimensionless factors.

**Symbols**

| Symbol | Meaning | Unit |
| ------ | ------- | ---- |
| `A` | fragment length:breadth ratio `l/x` | – |
| `x` | fragment breadth | m |
| `t₀` | fragment thickness (= case wall at break-up) | m |
| `m` | fragment mass | kg (tabulated in grains, gr) |
| `c` | `x²`-weighting moment correction, eq. (2) | – |
| `k` | breadth-variance factor `⟨x²⟩/⟨x⟩²`, = A9.1 | – |

---

## 2. Item 1 — reconciliation with assumption A9.1 (and with C2)

This is Action A(i) and it had to be settled before a value for `c` was chosen.
Three same-direction corrections were in play: **A9.1** (`k`, ≤2×, uncorrected),
**C2** (break-up velocity fraction, shipped, realised 1.096×) and the new **`c`**.

### 2.1 `c` and `k` are exactly independent — they stack, they do not overlap

Eq. (2) is an identity, not an approximation: the shipped closure's total
product-of-means error is the *product* `c·k`, with no cross-term left over.
`c` is a **covariance** factor (does `A` co-vary with `x²`?); `k` is a
**variance** factor (how dispersed is `x` at fixed `A`?). Neither is defined in
terms of the other, and setting either to 1 leaves the other's definition
untouched.

Verified numerically, not asserted — `checks/aspect-ratio-moment-correction.py`
computes `⟨m⟩/(⟨A⟩⟨√(m/A)⟩²)` directly (the left side of (2)) and compares:

```
IDENTITY  <m>/(<A><sqrt(m/A)>^2) = 1.911879  vs  c*k = 1.911879   agree
```

**So the double-counting risk flagged in `scoping.md` §4(iii) does not exist
between `c` and `k`.** They are orthogonal factors of one identity. The risk was
real to raise and is now closed by the factorisation.

### 2.2 A9.1's deferral was a budget hedge against C2, and C2 did not materialise

A9.1's stated reason for not correcting `k` is verbatim: *"Not corrected — doing
so would double-count with the deferred break-up-velocity item"*
(`mott-fragment-shape-closure/derivation.md` §9), weighed against A9.7's
projected **1.2–1.8×** for that item.

That item shipped as **C2** at a **realised 1.096×** (`count-chain.md` §3, and
`updates/breakup-velocity-fraction/derivation.md`). Two things follow:

1. **C2 and `k` cannot double-count in the first place.** They enter eq. (2)
    through algebraically distinct factors: C2 multiplies `V₀ → f·V₀` inside
    `(r_bu/V₀)²`; `k` multiplies the `⟨x²⟩` moment. Neither is derived from the
    other, and C2's derivation nowhere invokes a breadth-dispersion argument.
    A9.1's stated justification was therefore **wrong in kind**, not merely
    superseded — it treated two independent factors of a product as competing
    claims on one budget.
1. **Even on its own budget logic the hedge has lapsed.** The reserved space was
    1.6–1.8×; 1.096× was consumed, leaving **1.46–1.64×** unclaimed — comparable
    to `k` itself.

**Disposition:** A9.1's bias remains **fully open**; none of it has been claimed
by C2. `c` does not consume any of it either (§2.1). The `c` derived in §3 is
therefore taken at full size on a full budget, and `k` is reported separately
in §4 as a *measurable* quantity that A9.1 had only bounded.

**This does not authorise shipping `k` in this update.** `k` belongs to
`mott-fragment-shape-closure`'s A9.1 and changing it is a separate change to
that document. §6 reports the count chain both with `c` alone and with `c·k`, so
the human can see what each buys.

---

## 3. Item 2 — deriving `c` from Felix 2022 Table 3

### 3.1 Data and the mass axis

Counts: `doc-reference/fragmentation/explosion-fragment-model/tables/table-3-grady-aspect-ratio-counts.csv`
(extracted once, carries its own `.invariant`; anchor
`The calculation of aspect ratios for Grady`, `source.pdf` p.9 = journal p.167).

Group grain-mass ranges read **directly off**
`doc-reference/fragmentation/explosion-fragment-model/images/fig10.jpeg` (they
are printed on the figure, not in the text extraction). The figure also prints
`SHELL, HE 155-MM M101` beside a shell silhouette, confirming §1.3's criterion
match, and `RAPD 167366`.

| Group | printed mass range [gr] | used here [gr] | `n` | `Ā` (count-wtd) |
| ----- | ----------------------- | -------------- | --- | --------------- |
| 0 | `0 TO 75` | 0–75 | 1368 | 1.333 |
| 1 | `75 TO 75` **(sic)** | 75–150 (**A1**) | 358 | 1.302 |
| 2 | `150 TO 750` | 150–750 | 532 | 1.992 |
| 3 | `750 TO 2500` | 750–2500 | 135 | 2.748 |
| 4 | `2500 GRAINS AND OVER` | 2500–7500 (**A2**) | 22 | 3.000 |

`⟨A⟩ = 1.5681` over all 2415 fragments with the open bin at 4.0 — reproduces
`scoping.md` §2.1's 1.568. ✓

**Two discrepancies between Fig. 10's annotations and published Table 3, noted
and not silently absorbed:** Fig. 10 prints Group 1 "Total fragments 306" where
its own bins sum to 358 (= Table 3's value, which is what the `.invariant`
closes against the published Total row), and Group 4 "Total fragments 23" where
its bins sum to 22 (= Table 3). **The CSV — i.e. published Table 3 — is used
throughout**; the figure is used only for the mass edges and for the extra
resolution noted in A4.

### 3.2 The moment that actually enters is `Cov(A, x²)`, not `Cov(A, m)`

`scoping.md` §2.1 argued `c > 1` from "`A` and fragment size are strongly
positively correlated". That argument is for the wrong pairing and would have
over-predicted `c`. Eq. (1) contains `x²` (breadth squared), and the closure's
own mass identity fixes

$$x^{2} \;=\; \frac{m}{\rho\,t_0\,A}\quad (3)$$

so **at fixed mass, `x²` is deterministically *anti*-correlated with `A`** — a
longer, thinner fragment of the same mass has a smaller breadth. `c` is the net
of two opposing effects:

$$c \;=\; \frac{\langle A x^{2}\rangle}{\langle A\rangle\langle x^{2}\rangle}
\;=\;\frac{\langle m\rangle}{\langle A\rangle\,\langle m/A\rangle}\quad (4)$$

using (3) in both moments (`ρ t₀` cancels — this is why `c` needs no case-wall
value and is a pure property of the table).

**Limit checks on (4)** (both run in the check script):

| Limit | Expected | Computed |
| ----- | -------- | -------- |
| **No aspect dispersion** (all fragments at one `A`) — `⟨A x²⟩ = ⟨A⟩⟨x²⟩` identically, so the shipped closure is exact | `c = 1` exactly, for any masses | `c = 1.000000` ✓ |
| **`A` independent of `m`** (all Groups at one mass) | `c = 1/(⟨A⟩⟨1/A⟩) < 1` (AM–HM), **not** 1 | `c = 0.8354` ✓ |

The second limit is the non-obvious one and is the check that would have caught
the scoping's sign argument: **zero mass–aspect correlation gives `c ≈ 0.84`,
not `c = 1`.** The measured `c > 1` therefore says the positive `m`–`A`
association in Table 3 is strong enough to overcome a 16 % AM–HM floor, and the
naive covariance reading would have over-stated the correction by ~20 %.

### 3.3 Result

Count-weighted over all 2415 fragments, geometric-mean bin representatives:

```
<m> = 219.04 gr    <A> = 1.5681    <m/A> = 111.361 gr
c = 219.04 / (1.5681 x 111.361) = 1.2543
```

$$\boxed{\;c \;=\; 1.25\;,\qquad A_\text{eff} \;=\; c\,A \;=\; 2.01\;}$$

### 3.4 Uncertainty

Sensitivity to each stated assumption, one at a time (check script):

| Assumption varied | Range tried | `c` |
| ----------------- | ----------- | --- |
| Group-0 lower floor [gr] | 2.5 / 7.5 / 20 / 37.5 | 1.278 / **1.254** / 1.223 / 1.197 |
| Group-4 upper edge [gr] | 5000 / 7500 / 12500 / 25000 | 1.242 / **1.254** / 1.273 / 1.304 |
| Open aspect bin `1:4+` | 4.0 / 4.29 / 5.0 / 6.0 | **1.254** / 1.256 / 1.257 / 1.257 |
| Group-1 upper edge [gr] | 150 / 100 / 200 | **1.254** / 1.266 / 1.245 |
| Arithmetic- vs geometric-mid | — | 1.237 vs **1.254** |

Full 16-corner sweep over all four assumptions jointly:

$$c \in [1.18,\;1.35],\qquad \text{central } 1.25$$

**`c` is remarkably insensitive to the open-bin treatment** (1.254 → 1.257 as
`1:4+` moves 4 → 6), which retires the card's standing caveat on that bin *for
this quantity*: only 18 of 2415 fragments sit there. The dominant sensitivity is
the Group-0 mass floor, and it is only ±3 %.

**This is materially below `scoping.md` §4's speculative 1.4–1.9 band.** The
scoping bound was an upper envelope (`⟨A⟩_max/⟨A⟩ = 3.0/1.57 = 1.9`) built on
the wrong covariance pairing (§3.2); the derived value is smaller and the
scoping's own hedge ("realistic value is likely `c ≈ 1.3–1.6`") is still
slightly high.

### 3.5 Assumptions

- **A1 — Group 1 spans 75–150 gr.** Fig. 10 literally prints `GROUP NO 1-75 TO
    75 GRAINS`; 150 is taken from Group 2's own printed lower edge. Treated as an
    assumption, **not** a citation, per `scoping.md` §1.2a. Impact: ±0.01 on `c`
    over 100–200 gr — negligible.
- **A2 — Group 4 is truncated at 7500 gr.** The figure's bin is open
    (`2500 GRAINS AND OVER`); 3× the lower edge matches Group 3's own 750→2500
    span ratio. Impact: +0.05 on `c` if the true top is 25000 gr.
- **A3 — within-bin representative is the geometric mean of the edges**, with
    Group 0's zero lower edge floored at 7.5 gr (0.1× its upper edge). Impact:
    ±0.03 on `c`.
- **A4 — the open aspect bin `1:4+` is read at 4.0.** Fig. 10 resolves it for
    Group 4 only (`1:4 = 5`, `1:5 = 2` → 4.29); Table 3 lumps these into the CSV's
    `n_1to4plus = 7`. Immaterial here (§3.4).
- **A5 — `c` is count-weighted over Table 3's own fragment counts**, i.e. the
    same weighting the shipped `⟨A⟩ = 1.6` uses. This is what makes `c` a pure
    reweighting and keeps `A → cA` the only code change.
- **A6 — Table 3's modal bins are the analysts' per-Group counting defaults, not
    measurements** (`scoping.md` §1.2b). This is the binding limitation on `c`:
    the `A`-vs-mass trend that produces `c > 1` is substantially the default the
    authors assigned to each band. `c` inherits that. It is not correctable from
    the held data and the direction of the bias is unknown.
- **A7 — aspect ratios <1:1 are folded up into >1:1** in the source photographs
    (`scoping.md` §1.2c), biasing the small Groups' `Ā` upward and therefore
    biasing the measured `m`–`A` correlation, hence `c`, **downward**. `c = 1.25`
    is thus more likely a floor than a ceiling on that account.
- **A8 — the Mott/Linfoot structural premise is unresolved.** The standing
    `[deferrable]` finding (`scoping.md` §1.4) notes that "one constant `A`
    across shells" is not primary-backed. This derivation neither relies on
    Mott/Linfoot for it nor repairs it: `c` is a reweighting of Felix 2022's own
    empirical average and stands or falls with that table. The finding marker
    stays.
- **A9 — `c` narrows the evidentiary base it corrects, and is applied across
    all calibers.** `A = 1.6` is a mean over three datasets/casing types (Grady
    ogive, Hiroe cylindrical, Mott cylindrical — `explosion-fragment-model/card.md`
    Table 4) plus two further corroborating materials; `c = 1.25` is derived
    from exactly one of those (Grady's Fig. 10) and one test article (155mm HE
    M101). It is then applied as a single global multiplier on `A_eff` across
    `SHELLS`' four calibers (60/75/105/155mm) through the same pre-existing
    single-`A`-across-shells premise A8 flags. Neither this pass nor its review
    evaluated whether the mass–aspect-ratio trend generalizes past 155mm.

FINDING[deferrable]: c=1.25 is derived from a single 155mm HE M101 test article (Grady Fig. 10 only), narrower than the 3-dataset/casing-type base it corrects, and is applied as one global multiplier across all four SHELLS calibers with no evidence the mass-aspect-ratio trend generalizes beyond 155mm (affects: experiment/fragmentation-field/updates/mass-dependent-fragment-shape/derivation.md, experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md; since: 2026-08-16)

---

## 4. `k` (assumption A9.1) is measurable on the same table

A9.1 bounds `k = ⟨x²⟩/⟨x⟩² ∈ (1, 2)` from theory and never evaluates it. Eq. (3)
makes it computable from Table 3 by the same route as `c`:

$$k \;=\; \frac{\langle m/A\rangle}{\big\langle \sqrt{m/A}\big\rangle^{2}}$$

giving **`k = 1.52`** (16-corner sweep `[1.28, 1.84]`). This sits inside A9.1's
theoretical (1, 2) band, near its midpoint, and is the first *data-side* value
for it.

**It is a lower bound.** Only *between*-Group dispersion is resolved (one mass
representative per Group); all within-Group spread is discarded, and discarded
variance can only raise `k`. The true `k` is therefore ≥1.52 and plausibly
nearer A9.1's upper limit of 2.

Combined, `c·k = 1.91` (corner sweep `[1.51, 2.49]`).

---

## 5. Item 3 — the `drag-gap-1944` B(r) fit at the corrected `μ`

`scoping.md` §5 asserts that a changed `μ` re-weights the B(r) fit even though
`C_shape` is untouched, and asks for numerical confirmation rather than
assertion. `checks/bofr-at-new-mu.py` applies the correction the way shipped
code would (`dataclasses.replace(shell, aspect_ratio=c·1.6)`), re-solves
`compute_shell_zones`, and feeds the challenge's **own committed reduction**
(`drag-gap-1944/checks/b-vs-range-155mm.py`, imported unmodified) so the
comparison is like-for-like against the same Table 59 casualties CSV.
155 mm M107, ground burst, AoF 30°, `E_leth = 78.6 J`.

### 5.1 Result — the fit moves, and `c = 1.25` improves it

| `c` | `A_eff` | geometric-mean `B_model/B_card` over the 11 card ranges | rows inside the 0.5–2× band |
| --- | ------- | ------------------------------------------------------ | --------------------------- |
| 1.00 (shipped) | 1.60 | **1.226** | 11/11 |
| **1.25 (derived)** | 2.00 | **1.063** | 11/11 |
| 1.91 (`c·k`) | 3.06 | **0.792** | 11/11 |

**Three findings, all of which needed the numbers:**

1. **The fit is not invariant — `scoping.md` §5 is confirmed.** `B_model` moves
    by −18 % at `c = 1.25` and −44 % at `c = 1.91`, with `C_shape` and
    `retardation_coeff` untouched. A changed `μ` genuinely re-weights the hit
    density. Asserting invariance would have been wrong.
1. **The change is a level shift, not a tilt.** Normalising each curve by its own
    20 ft value, the range shape is nearly identical across `c` (`0.429/0.233/…`
    at `c = 1` vs `0.433/0.238/…` at `c = 1.91`). So `c` re-scales the drag
    surface without re-fitting its range dependence — consistent with memory
    `gotcha_density_falloff_shape_is_threshold_degenerate` (the shape carries
    little information; the absolute level does) and with `scoping.md` §5's
    argument that only per-fragment `A(m)` would force a re-fit.
1. **`c = 1.25` is an independent improvement on this surface.** The shipped
    model over-predicts B(r) by 1.23×; `c = 1.25` takes that to **1.06×** —
    essentially exact. This is a *second*, independent surface agreeing with the
    correction, derived from a different dataset (Ordnance Dept. 1944 casualties)
    than the one `c` came from (Felix 2022 Table 3). **`c·k = 1.91` over-shoots
    it to 0.79×**, i.e. under-predicting by 26 %.

**This is the sharpest constraint in the derivation and it did not exist before
this pass:** the B(r) surface prefers `c` **alone** over `c·k`. It is a genuine
cross-check because `A` reaches B(r) only through `μ`, never through the drag
coefficient (§5's orthogonality, `drag-gap-1944/shape-closure-orthogonality.md`).

---

## 6. Item 4 — re-solved count-chain leverage

`checks/aspect-ratio-moment-leverage.py` (extended in place this pass; the
`c = 1.00` row still reproduces the shipped baseline — see the limit check
below). The chain is **re-solved**, not ratioed: `μ = c·μ₀`, `N₀ = N₀₀/c`,
`N = N₀ e^{−√(m_thr/μ)}` with `m_thr = 0.166 g` held (correct — `A` does not
enter the perforation path, §5's orthogonality; confirmed by the shape result
in §5.1 that the change is a pure level shift).

| correction | `f` | `μ` [g] | `N₀` | `N(≥m_thr)` | vs Tolch 700 | vs Tolch 779 |
| ---------- | --- | ------- | ---- | ----------- | ------------ | ------------ |
| shipped | 1.000 | 0.929 | 2681 | 1757 | **2.51×** | **2.26×** |
| `c` low (corner) | 1.176 | 1.093 | 2280 | 1544 | 2.21× | 1.98× |
| **`c` derived** | **1.254** | **1.165** | **2138** | **1466** | **2.09×** | **1.88×** |
| `c` high (corner) | 1.352 | 1.256 | 1983 | 1379 | 1.97× | 1.77× |
| `k` alone (A9.1) | 1.524 | 1.416 | 1759 | 1249 | 1.78× | 1.60× |
| `c·k` low (corner) | 1.506 | 1.399 | 1780 | 1261 | 1.80× | 1.62× |
| **`c·k` derived** | **1.912** | **1.776** | **1402** | **1033** | **1.48×** | **1.33×** |
| `c·k` high (corner) | 2.487 | 2.310 | 1078 | 825 | 1.18× | 1.06× |

**Limit check.** The `f = 1.000` row returns `N = 1757`, `2.51× / 2.26×` against
`count-chain.md` §5's verdict row `1756`, `2.51× / 2.25×` — agreement to the
rounding of the cached `μ₀`, `N₀₀` inputs. `c = 1` recovers the shipped closure
exactly. ✓

**Thresholds** (bisection on the re-solved chain, *not* a `1/f` scaling — `N`
does not move as `1/f`, memory `gotcha_mott_count_not_f_squared`):

- `f ≥ 1.163` clears the **/779** arm to 2.00×.
- `f ≥ 1.327` clears the **/700** arm to 2.00×.

### 6.1 Does this clear the within-2× PASS band?

**Partly — `c` alone clears one arm and misses the other by 4.5 %.**

- **/779 arm: PASSES.** `1.88×` at `c = 1.254`, needing only `f ≥ 1.163`. The
    entire derived corner band `[1.176, 1.352]` clears it (`1.98×`–`1.77×`).
- **/700 arm: FAILS, narrowly.** `2.09×` against a 2.00× band, needing
    `f ≥ 1.327`. The derived `c = 1.254` is **5.5 % short in `f`** (equivalently
    the count is 4.5 % above the band). Only the top of the corner band
    (`c = 1.352`) reaches `1.97×`.
- **With `k` (A9.1) also applied, both arms pass comfortably** — `c·k = 1.912`
    gives `1.48× / 1.33×`, and even the bottom of the `c·k` corner band
    (`1.506`) gives `1.80× / 1.62×`, inside on both arms.

**Net movement attributable to this update alone:** `2.51×/2.26×` →
`2.09×/1.88×`, i.e. `c` removes **~17 % of the count**, closing about **28 % of
the /700 excess** and **32 % of the /779 excess** above 1×.

### 6.2 The two corrections are cross-constrained, and that is the result

`c` alone and `c·k` cannot both be preferred, and the two surfaces disagree
about which:

| | count-gap-1938 | drag-gap-1944 B(r) |
| --- | --- | --- |
| `c = 1.25` alone | 2.09× / 1.88× — one arm short | **1.06×** — near-exact |
| `c·k = 1.91` | **1.48× / 1.33×** — both pass | 0.79× — 26 % under |

Neither choice is dominated. The count surface wants the larger correction; the
drag surface wants the smaller. **The honest reading is that `c ≈ 1.25` is what
this update's data supports, and that the remaining /700 shortfall is real and
not closed by this aspect** — the count residual is not fully a shape-moment
artefact. Applying `c·k` to force both count arms inside the band would trade a
23 % over-prediction on B(r) for a 21 % under-prediction, i.e. spend a genuinely
independent cross-check to buy a target. That is the "rebaseline onto the
validation source" failure mode (memory
`gotcha_rebaseline_onto_validation_source`) and this derivation declines it.

---

## 7. Conclusion and what this update should ship

**Ship `c = 1.25`** as a multiplicative correction on the single constant `A`,
i.e. `A_eff = 2.00` in `mott_params`/`ShellParams.aspect_ratio`. One constant,
one line, no new degrees of freedom, `C_shape` and §8's deferral untouched.

Grounds a reviewer can check:

1. `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩) = ⟨m⟩/(⟨A⟩⟨m/A⟩) = 1.254`, corner band `[1.18, 1.35]`,
    from Felix 2022 Table 3 weighted by Fig. 10's own printed grain ranges (§3).
1. Both limit checks pass: no aspect dispersion → `c = 1.000000` exactly;
    `f = 1` reproduces `count-chain.md`'s verdict row (§3.2, §6).
1. It is **independently corroborated on a second surface**: B(r) fit quality
    1.23× → 1.06× (§5.1). No prior candidate on this thread had that.
1. It moves the count residual `2.51×/2.26×` → `2.09×/1.88×` (§6).

**Verdict on the PASS band, stated plainly:** this does **not** by itself return
`count-gap-1938` to PASS. The **/779 arm clears (1.88×)**; the **/700 arm misses
at 2.09×**, short by 4.5 %. Whether that reopens the thread is the human's call
per `scoping.md` §6 Action C — this pass does not edit `count-chain.md`.

**Follow-up passes (not this one):**

- **`src/arty/` implementation** of `A_eff = 2.00`, plus a `_limitations.qmd`
    entry for A6 (the modal bins are the analysts' counting defaults).
- **A9.1 / `k` is now a live, measurable item** for
    `mott-fragment-shape-closure`: `k ≥ 1.52` from data, vs its
    theory-only `(1,2)` bound, and its stated deferral rationale is void (§2.2).
    That is a change to *that* document and its `derivation.md` §9 — flagged
    here, not made here. Its interaction with the B(r) over-shoot (§6.2) is the
    open question that pass must answer.
- The `[deferrable]` Mott/Linfoot structural-premise finding stays open (A8).

**Fidelity target** (carried from `scoping.md` §6): tolerable error on a single
global `A` is ±15 %. The derived `c`'s own corner band is `±7 %` — inside it.
The unrepresented within-Group mass dependence (A6, A7) is not.
