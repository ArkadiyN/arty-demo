# Derivation — aspect-ratio moment correction `c` on the Mott shape constant `A`

**Aspect:** the single constant `A = l̄/x̄ = 1.6` in the Mott shape closure
(`mott-fragment-shape-closure/derivation.md` eq. (2)) is a **count-weighted**
mean where the closure requires an `x²`-weighted one. Derive the multiplicative
correction `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩)`, bound it, and re-solve its leverage on the
`count-gap-1938` residual.

**Scope:** derivation only. No `src/arty/` edit, no notebook edit in this pass.
Executes Action A of `scoping.md` §6. The scoping decision — a moment
correction reported as **one number per shell**, not a fitted per-fragment
`A(m)` curve — rests on the grounds set out in `scoping.md` §2/§6 (corrected
2026-08-16 per `review.md` A2/A3); those grounds, not this document, are where
it should be challenged.

**Status:** derivation pass, 2026-08-16; revised 2026-08-16 (fix cycle) to make
`c` per-shell after `review.md`'s adversarial pass returned **FAIL** on A1.
`c` is a spectrum-weighted moment, so a single global `c` is not well-defined
(§3.3b). The headline §6/§7 count result changed as a consequence.

Checks (all runnable standalone from the repo root, <2 s each):

- `checks/aspect-ratio-moment-correction.py` — §2, §3, §4 (derives `c`, `k` at
    Table-3 weighting).
- `checks/per-shell-c-and-75mm-count-chain.py` — **§3.3b, §3.4b, §6** (per-shell
    `c` fixed point under three mass-axis treatments; re-solves the 75 mm chain).
- `checks/spectrum-weighted-c-per-shell.py`,
    `checks/spectrum-weighted-c-fixedpoint-count-chain.py` — the independent
    `review.md` A1 implementations; reproduced here as method A.
- `checks/aspect-ratio-moment-leverage.py` — the `f`-sweep of the count chain
    (§6 corner rows).
- `checks/bofr-at-new-mu.py` — §5 (re-runs the `drag-gap-1944` B(r) fit at the
    corrected `μ`; 155 mm, `A_eff = 2.00`, unchanged by the per-shell fix).

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

### 3.3 Result on Table 3's own weighting

Count-weighted over all 2415 fragments, geometric-mean bin representatives:

```
<m> = 219.04 gr    <A> = 1.5681    <m/A> = 111.361 gr
c = 219.04 / (1.5681 x 111.361) = 1.2543
```

This is **not** the number to ship. Eq. (4) is a moment of the *joint* `(A, m)`
distribution, and its `m`-marginal is the **shell's own fragment population** —
the population whose mean mass is `2μ` by construction (eq. 1). Weighting by
Felix Table 3's photographic counts (assumption A5, superseded) freezes the
mass spectrum of the one article the table was measured on. §3.3b re-weights.

### 3.3b `c` is per-shell, because its weights are the shell's Mott spectrum

`c` is a **statistic of a distribution, not a material constant.** The physical
content Table 3 supplies is the *conditional* relation `A | m` (Group 0 at
`Ā = 1.33` rising to Group 4 at `Ā = 3.00`); the *weights* come from
`N(≥m) = N₀e^{−√(m/μ)}`, and `μ` spans an order of magnitude across `SHELLS`.
Because `μ = c·μ₀` in turn, this is a one-dimensional fixed point
`c = c(c·μ₀)`; it is contractive and converges in 3–4 iterations for every
shell (`checks/per-shell-c-and-75mm-count-chain.py`, and independently
`checks/spectrum-weighted-c-fixedpoint-count-chain.py`).

Three weightings of the *identical* Table-3 aspect data are computed, all
holding each Group's own within-Group aspect mix fixed:

| | mass axis inside each Group | what it tests |
| --- | --- | --- |
| **A** | geometric-mean bin representative (as §3.3) | Group weights only |
| **B** | `E[m \| Group]` under the shell's Mott spectrum | self-consistent masses — **central** |
| **C** | continuous `Ā(m) = 0.677 m^{0.181}` fitted through the five Group centroids, clamped to `[23.7, 4330]` gr | restores the within-Group `m`–`A` covariance that A and B discard (A11) |

| shell | `μ₀` [gr] | `P(Group 0)` | A | **B (central)** | C | **`A_eff = c·1.6`** |
| ----- | --------- | ------------ | - | --------------- | - | ------------------- |
| 155 mm M107 | 98.1 | 0.54 | 1.262 | **1.251** | 1.173 | **2.00** |
| 105 mm M1 | 31.9 | 0.77 | 1.099 | **1.102** | 1.090 | **1.76** |
| 75 mm M48 | 14.3 | 0.90 | 0.970 | **0.985** | 1.013 | **1.58** |
| 60 mm M49A2 | 7.6 | 0.96 | 0.906 | **0.920** | 0.950 | **1.47** |

$$\boxed{\;c = 1.25 \;/\; 1.10 \;/\; 0.99 \;/\; 0.92 \quad (155/105/75/60\ \text{mm})\;}$$

**Method B is adopted as central**: it is the only one of the three whose mass
axis and weights come from the same distribution, and it uses nothing the table
does not resolve. The A–C spread is carried as the method band (§3.4b).

Three readings, and they cut in different directions:

1. **155 mm is unchanged.** `c = 1.251` (B) against §3.3's 1.2543 — 0.3 % apart,
    `A_eff = 2.001` vs 2.00. Table 3's photographic sample (`⟨m⟩ = 219 gr`) is an
    excellent proxy for the 155 mm model spectrum (`2μ = 196 gr`), which is *why*
    §3.3 worked and why the §5 B(r) cross-check — also 155 mm — corroborates it.
    **§5's result therefore stands verbatim: the shipped 155 mm `A_eff` is
    2.00 either way.**
1. **The correction shrinks monotonically with caliber and reaches ~1 at
    75 mm.** The mechanism is transparent: 90 % of the 75 mm Mott population
    falls inside Group 0, where Table 3 resolves no `A`-vs-`m` trend at all, so
    the between-Group covariance that generates `c > 1` is barely sampled and
    the AM–HM floor of §3.2 (`c = 0.835` at zero `m`–`A` correlation) takes
    over. At 60 mm the floor wins outright and `c < 1`.
1. **At 75 mm the correction is nil, not negative.** The three methods bracket
    `c₇₅ ∈ [0.970, 1.013]` — straddling 1. The sign is set by whether the
    within-Group-0 `m`–`A` trend is resolved (method C) or discarded (A, B), and
    the table cannot settle that. The defensible statement is
    `c₇₅ = 0.99 ± 0.02`: **the aspect-ratio moment correction does essentially
    nothing at 75 mm.** §6 is rewritten on that basis.

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

**It is a lower bound, for the same structural reason `k` is one (§4).** `c`
is built from the identical Group-discretized table: every fragment in a
Group is assigned that Group's single representative mass, so the entire
measured `⟨A x²⟩` covariance comes from *between*-Group variation only — any
mass–aspect correlation *within* a Group is structurally invisible to the
calculation (within a Group, `m` is constant by construction, so its
within-Group covariance with `A` is exactly zero in the computed statistic).
By the law of total covariance, `Cov_true(A,m) = Cov_between + E[Cov_within]`;
if the omitted within-Group term shares the sign of the measured
between-Group trend — the physically likely case, since the motivating
hypothesis (large fragments retain plate-like geometry) is a claim about a
continuous relationship, not a step function at the Group boundaries — then
`c = 1.25` is *also* a lower bound on the true correction, plausibly sitting
back toward the `1.3–1.6` band this section just called "still slightly
high." Unlike `k`'s bound this is not a mathematical certainty — it depends
on the sign of a covariance the table cannot resolve — so it is carried as a
directional caveat, not a revised corner band. The 16-corner sweep above
varies bin edges and conventions, never the group-discretization itself, so
it does not capture this source of error.

**Revised 2026-08-16 — the lower-bound direction is caliber-dependent, not
uniform.** §3.3b method C restores exactly the omitted within-Group covariance
(a continuous `Ā(m)` through the Group centroids) and the result does **not**
move `c` uniformly upward: it gives `1.173 / 1.090 / 1.013 / 0.950` against
method A's `1.262 / 1.099 / 0.970 / 0.906`, i.e. **down** at 155 mm and **up**
at 75/60 mm. The reason is that the collapse does two things at once —
it deletes within-Group covariance (which depresses `c`) *and* it evaluates the
`A`-trend at five widely separated Group centroids rather than at the masses
the spectrum actually populates (which inflates `c` when the spectrum straddles
several Groups). The first dominates when the spectrum sits inside one Group
(75/60 mm); the second dominates when it straddles many (155 mm). So the
group-discretization error **compresses the caliber spread** rather than
biasing every shell one way, and "`c` is a lower bound" is true only for the
sub-105 mm shells. The `k` analogy in §4 is not transferable.

### 3.4b Method band on the per-shell values

The §3.4 16-corner sweep varies bin edges and conventions at Table-3
weighting; the per-shell values carry a second, larger uncertainty — the
choice of mass axis inside each Group (§3.3b A/B/C). Taking the min–max over
the three methods as the band:

| shell | band | central (B) | relative half-width |
| ----- | ---- | ----------- | ------------------- |
| 155 mm M107 | [1.173, 1.262] | 1.251 | ±3.6 % |
| 105 mm M1 | [1.090, 1.102] | 1.102 | ±0.6 % |
| 75 mm M48 | [0.970, 1.013] | 0.985 | ±2.2 % |
| 60 mm M49A2 | [0.906, 0.950] | 0.920 | ±2.4 % |

All four bands sit inside the ±15 % fidelity target (§7). The band that
matters qualitatively is 75 mm's, because it straddles `c = 1`.

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
- **A5 — SUPERSEDED 2026-08-16.** *Was:* "`c` is count-weighted over Table 3's
    own fragment counts, i.e. the same weighting the shipped `⟨A⟩ = 1.6` uses."
    That justified consistency with `⟨A⟩` but not with eq. (1), whose average
    runs over the *shell's* fragment population. **Replaced by A5′.**
- **A5′ — `c` is weighted by the shell's own Mott spectrum** (§3.3b), solved as
    the fixed point `c = c(c·μ₀)`. `A → c(shell)·A` is still the only code
    change and `ShellParams.aspect_ratio` is still one number per shell, so no
    new functional degree of freedom is introduced. The Table-3-weighted 1.2543
    survives only as the 155 mm value (to 0.3 %).
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
- **A9 — REVISED 2026-08-16. What transfers across calibers is the conditional
    `A | m` relation, not `c` itself.** `A = 1.6` is a mean over three
    datasets/casing types (Grady ogive, Hiroe cylindrical, Mott cylindrical —
    `explosion-fragment-model/card.md` Table 4); the mass-resolved `A | Group`
    mix behind `c` comes from exactly one of those (Grady's Fig. 10, 155mm HE
    M101). §3.3b no longer applies a single global multiplier — each shell gets
    its own `c` from its own spectrum — so the *weights* are now shell-specific
    and the only thing assumed caliber-independent is the within-Group aspect
    mix `A | Group`. That is a **strictly weaker** assumption than a global `c`
    (which required the mass marginal to transfer too), but it is still
    unevidenced: no second casing type or caliber in the held literature
    resolves aspect ratio by mass. Wall-thickness-to-caliber ratio differs
    across `SHELLS`, and `A | Group` plausibly does too. Published to readers of
    the model as limitation 16 in `experiment/fragmentation-field/_limitations.qmd`
    (2026-08-16); the finding marker is closed on that basis.
- **A10 — RESOLVED 2026-08-16 by the per-shell fix.** The prior version noted
    that §5's B(r) cross-check (155mm) and §6's count chain (75mm M48) were not
    caliber-matched, so the /700 shortfall might be a caliber-transfer artifact
    of applying a 155mm `c` at 75mm. That mechanism is now eliminated by
    construction: §6 runs at `c₇₅`, derived from the 75mm shell's own spectrum,
    and §5 runs at `c₁₅₅`. The two surfaces are each self-consistent, and the
    transfer doubt has been given a value and a sign (§3.3b) rather than left
    unquantified. What survives is A9's narrower `A | Group` assumption.
- **A11 — `c` is a lower bound for the sub-105mm shells only.** `c` is built
    from the same Group-discretized table as `k`; collapsing each Group to one
    representative mass makes within-Group mass–aspect covariance invisible.
    §3.4b's method C restores it, and the correction is **not** one-signed:
    `c` moves down at 155mm and up at 75/60mm (§3.4, "Revised"). So the
    lower-bound reading holds where the spectrum sits inside one Group and
    reverses where it straddles several. Unlike `k`'s bound this was never a
    mathematical certainty, and it is now known not to be uniform. The
    residual uncertainty is carried as the §3.4b method band. Published to
    readers of the model as limitation 17 in
    `experiment/fragmentation-field/_limitations.qmd` (2026-08-16); the finding
    marker is closed on that basis.

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

**Unaffected by the per-shell fix.** This surface is 155 mm, and the 155 mm
per-shell value is `c₁₅₅ = 1.251` → `A_eff = 2.001` against the 2.00 the check
was run at (§3.3b). The table below stands as computed; no re-run was needed.

### 5.1 Result — the fit moves, and `c₁₅₅ = 1.25` improves it

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

**This chain runs on 75mm M48 HE** (`count-chain.md:144`), so the value that
enters it is **`c₇₅`, not `c₁₅₅`** — that is the substantive change in this
revision. §5's B(r) check is 155 mm and runs at `c₁₅₅`; the two surfaces are
each internally caliber-consistent now (A10).

`checks/per-shell-c-and-75mm-count-chain.py` (headline rows) and
`checks/aspect-ratio-moment-leverage.py` (the `f`-sweep and corner rows). The
chain is **re-solved**, not ratioed: `μ = f·μ₀`, `N₀ = N₀₀/f`,
`N = N₀ e^{−√(m_thr/μ)}` with `m_thr = 0.166 g` held (correct — `A` does not
enter the perforation path, §5's orthogonality; confirmed by the shape result
in §5.1 that the change is a pure level shift).

| correction | `f` | `μ` [g] | `N₀` | `N(≥m_thr)` | vs Tolch 700 | vs Tolch 779 |
| ---------- | --- | ------- | ---- | ----------- | ------------ | ------------ |
| shipped | 1.000 | 0.929 | 2681 | 1757 | **2.51×** | **2.26×** |
| `c₇₅` method A (band low) | 0.970 | 0.901 | 2765 | 1800 | 2.57× | 2.31× |
| **`c₇₅` method B (central)** | **0.985** | **0.915** | **2721** | **1777** | **2.54×** | **2.28×** |
| `c₇₅` method C (band high) | 1.013 | 0.941 | 2647 | 1739 | 2.48× | 2.23× |
| *superseded:* global `c` = `c₁₅₅` | 1.254 | 1.165 | 2138 | 1466 | 2.09× | 1.88× |
| `k` alone (A9.1) | 1.524 | 1.416 | 1759 | 1249 | 1.78× | 1.60× |
| *superseded:* `c₁₅₅·k` | 1.912 | 1.776 | 1402 | 1033 | 1.48× | 1.33× |

**Limit check.** The `f = 1.000` row returns `N = 1757`, `2.51× / 2.26×` against
`count-chain.md` §5's verdict row `1756`, `2.51× / 2.25×` — agreement to the
rounding of the cached `μ₀`, `N₀₀` inputs. `f = 1` recovers the shipped closure
exactly. ✓

The two superseded rows are retained only because they are what the
pre-revision text quoted; **`f = 1.254` is the 155 mm correction and has no
standing on a 75 mm chain.**

**Thresholds** (bisection on the re-solved chain, *not* a `1/f` scaling — `N`
does not move as `1/f`, memory `gotcha_mott_count_not_f_squared`):

- `f ≥ 1.163` clears the **/779** arm to 2.00×.
- `f ≥ 1.327` clears the **/700** arm to 2.00×.

### 6.1 Does this clear the within-2× PASS band?

**No — and the honest result is that at 75 mm this correction does nothing.**

- **Both arms FAIL, essentially unmoved.** `2.54× / 2.28×` at the central
    `c₇₅ = 0.985`, against a 2.00× band, versus `2.51× / 2.26×` shipped. The
    entire method band `c₇₅ ∈ [0.970, 1.013]` gives `2.48×–2.57×` /
    `2.23×–2.31×`: **every corner is outside the band on both arms, and every
    corner is within 3 % of the shipped count.**
- **Thresholds unchanged and unreached** (bisection on the re-solved chain,
    *not* a `1/f` scaling — memory `gotcha_mott_count_not_f_squared`):
    `f ≥ 1.163` clears /779, `f ≥ 1.327` clears /700. `c₇₅ ≈ 0.99` reaches
    neither; it is on the wrong side of 1 at the band's lower corner.
- **`k` (A9.1) is the only factor here with real leverage.** `k = 1.524` alone
    gives `1.78× / 1.60×` — both arms inside. But `k` is a separate assumption
    belonging to `mott-fragment-shape-closure`, is not derived per-shell here,
    and §6.2 explains why stacking it is not free.

**Net movement attributable to this update at 75 mm: none.** `2.51×/2.26×` →
`2.54×/2.28×` (central), a `+1 %` count change — inside the rounding of the
cached chain inputs. The pre-revision claim that `c` "removes ~17 % of the
count" and closes "28 %/32 % of the excess" was the **155 mm** correction
applied to a **75 mm** chain and is withdrawn.

### 6.2 What the per-shell result actually shows

The pre-revision reading — "the count surface wants the larger correction, the
drag surface wants the smaller, and `c` alone is the honest compromise" — was
built on a comparison between two calibers. With `c` per-shell it collapses:

| surface | caliber | `c` used | result |
| ------- | ------- | -------- | ------ |
| `drag-gap-1944` B(r) | 155 mm M107 | `c₁₅₅ = 1.25` | 1.23× → **1.06×** — a real, near-exact improvement |
| `count-gap-1938` chain | 75 mm M48 | `c₇₅ = 0.99` | 2.51× → **2.54×** — no movement |

**These are no longer in tension; they are answering different questions.** The
aspect-ratio moment is a genuine, measurable, ~25 % correction *on 155 mm*, and
it is confirmed on an independent 155 mm surface (Ordnance Dept. 1944
casualties, a different dataset from Felix 2022 Table 3). At 75 mm the same
physics predicts no correction at all, because the shell's fragment spectrum
lies almost entirely inside the one mass Group over which Table 3 resolves no
aspect trend. **Both are outputs of one model, not a compromise between two.**

The consequence for `count-gap-1938` is unambiguous and negative: **the count
residual at 75 mm is not a shape-moment artefact.** This is now a *positive*
result rather than the unattributed shortfall the pre-revision §6.2 recorded —
the caliber-transfer doubt (A10) that made it unattributable has been given a
value and a sign, and the answer is that the correction at this caliber is nil.
Whatever drives the 2.5× 75 mm count excess, it is not the `⟨A x²⟩` weighting.

Stacking `c₇₅·k = 1.50` would put both arms inside the band (`1.80×/1.62×`),
but that is `k` doing all the work, and `k = 1.524` is itself Table-3-weighted
and would need the same per-shell treatment before it could be quoted on a
75 mm chain. Forcing the count arms with a factor whose 155 mm B(r) surface
rejects it (`c₁₅₅·k → 0.79×`, 26 % under) remains the "rebaseline onto the
validation source" failure mode (memory
`gotcha_rebaseline_onto_validation_source`) and this derivation still declines
it.

---

## 7. Conclusion and what this update should ship

**Ship a per-shell `c`** as a multiplicative correction on the single constant
`A`, i.e. `ShellParams.aspect_ratio = c(shell)·1.6`:

| shell | `c` (central, method B) | `A_eff` |
| ----- | ----------------------- | ------- |
| 155 mm M107 HE | 1.25 | **2.00** |
| 105 mm M1 HE | 1.10 | **1.76** |
| 75 mm M48 HE | 0.99 | **1.58** |
| 60 mm M49A2 HE | 0.92 | **1.47** |

Still one number per shell, still no new functional degree of freedom, still
one field in an existing dataclass; `C_shape` and §8's deferral untouched. What
changed from the pre-revision recommendation is that the number is no longer
shared across calibers — `c` is a moment of the shell's own fragment spectrum,
not a material constant (§3.3b).

Grounds a reviewer can check:

1. `c = ⟨A x²⟩/(⟨A⟩⟨x²⟩) = ⟨m⟩/(⟨A⟩⟨m/A⟩)` (eq. 4), evaluated on Felix 2022
    Table 3's `A | Group` mix with Group weights and Group mean masses from each
    shell's own `N(≥m) = N₀e^{−√(m/μ)}`, solved as the fixed point
    `c = c(c·μ₀)` (§3.3b). Method band `±0.6–3.6 %` (§3.4b).
1. All limit checks pass: no aspect dispersion → `c = 1.000000` exactly; zero
    `m`–`A` correlation → `c = 0.835` (AM–HM floor, §3.2); Table-3 weighting
    reproduces `⟨m⟩ = 219.04 gr`, `⟨A⟩ = 1.5681`, `c = 1.2543` (§3.3); `f = 1`
    reproduces `count-chain.md`'s verdict row (§6).
1. It is corroborated on an independent surface **at the caliber it is largest
    on**: 155 mm B(r) fit quality 1.23× → 1.06× (§5.1), from the Ordnance Dept.
    1944 casualty data rather than Felix Table 3. `c₁₅₅ = 1.251` is 0.3 % from
    the value that check was run at.
1. It leaves the 75 mm count residual where it was: `2.51×/2.26×` →
    `2.54×/2.28×` (§6).

**Verdict on the PASS band, stated plainly:** this update does **not** move
`count-gap-1938`, on either arm. The **/700 arm stays at 2.54×** and the
**/779 arm at 2.28×** — both outside the 2× band, both within 3 % of shipped,
across the whole `c₇₅` method band. The pre-revision claim that the /779 arm
cleared at 1.88× is **withdrawn**: it was the 155 mm correction evaluated on a
75 mm chain (`review.md` A1). This aspect is therefore *not* a candidate
explanation for the 75 mm count excess, and §6.2 states that as a positive
finding rather than an open doubt. Whether that reopens the thread is the
human's call per `scoping.md` §6 Action C — this pass does not edit
`count-chain.md`.

**Shipped, 2026-08-16:** `src/arty/shells.py`'s `SHELLS` registry now carries
`aspect_ratio = mott_aspect_ratio(shell)` (method B, `MOTT_ASPECT_MOMENT_C` in
`src/arty/fragmentation.py`) for all four shells — the `A_eff` column above is
live, not a recommendation. Confirmed against the registry by
[`checks/shipped-aspect-moment-correction.py`](checks/shipped-aspect-moment-correction.py):
shipped `c` and `A_eff` match this table to 5e-3/5e-5, `mu`/`N0` move exactly as
`c` and `1/c` predict, and the `c = 1` (bare `A = 1.6`) limit reproduces the
pre-update model exactly. The 75 mm count-chain and 155 mm `B(r)` numbers in
items 3–4 above are unaffected — they were already computed against the
shipped-registry values, not the pre-implementation table.

**Follow-up passes (not this one):**

- ~~**`src/arty/` implementation** of the per-shell `A_eff` (2.00 / 1.76 / 1.58 /
    1.47 for 155/105/75/60 mm)~~ — done, see above. Still owed: a
    `_limitations.qmd` entry covering A6
    (modal bins are analyst defaults, not measurements), A9 (the `A | Group`
    mix is from one 155 mm test article and is assumed caliber-independent),
    and A11 (the group-discretization bias is caliber-dependent in sign, not a
    uniform lower bound).
- **A9.1 / `k` is now a live, measurable item** for
    `mott-fragment-shape-closure`: `k ≥ 1.52` from data, vs its
    theory-only `(1,2)` bound, and its stated deferral rationale is void (§2.2).
    That is a change to *that* document and its `derivation.md` §9 — flagged
    here, not made here. **`k` is Table-3-weighted exactly as `c` was, so it
    inherits A1's defect**: `k = 1.52` is the 155 mm value (the same script
    returns 1.51 / 1.35 / 1.21 / 1.11 for 155/105/75/60 mm under Mott
    weighting). Any pass that quotes `k` on a non-155 mm chain must re-weight it
    first. Its interaction with the B(r) over-shoot (§6.2) is the open question.
- The `[deferrable]` Mott/Linfoot structural-premise finding stays open (A8).

**Fidelity target** (carried from `scoping.md` §6): tolerable error on `A` is
±15 %. The per-shell method band is `±0.6–3.6 %` (§3.4b) and the Table-3-level
16-corner band is `±7 %` (§3.4) — both inside it. The unrepresented within-Group
mass dependence (A6, A7) is not covered by either, and the group-discretization
bias (A11) is covered only to the extent method C bounds it; the bands cover
the assumptions they were swept over, not those two sources of error.
