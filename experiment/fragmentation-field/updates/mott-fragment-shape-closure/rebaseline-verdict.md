# Rebaseline verdict — does the γ calibration survive the Mott 1947 non-closure?

Scope: the blocking `OPEN-FINDINGS.md` entry beginning *"gamma = 47 and gamma =
65 both interpolate along the rising trend of Mott 1947 p.308's gamma column…"*,
assessed against this update's `derivation.md` and against the shipped
`SteelParams.gamma` values. **Assessment only — no `src/arty/` change is made
here.** Evidence script:
`experiment/fragmentation-field/updates/mott-fragment-shape-closure/checks/mott-1947-gamma-column-strain-reading.py`.

______________________________________________________________________

## 1. Headline — the finding's premise is over-broad, and the column does close

The finding states the closure formula "is flat (spans ×1.20) where the printed
column rises ×3.35". That is true of **one** reading of `s_f` and not of the
reading the page supports.

Mott p.308 (anchor `Some values of`) tabulates **reduction in area**, not `s_f`.
The closure `γ ~ 160 P_y/P_f(1+s_f)` therefore has a free choice of how RA maps
to the strain factor. Sweeping the four candidates:

| denominator factor `D` standing for `(1+s_f)` | iron | 0.1 C | 0.25 C | 0.45 C | span |
| --- | ---: | ---: | ---: | ---: | ---: |
| printed column | **20** | **42** | **53** | **67** | ×3.35 |
| `1+RA` (the finding's reading) | +175 % | +34 % | +4 % | −30 % | ×1.20 |
| `1+ln(1/(1−RA))` (true strain) | +82 % | +4 % | −15 % | −40 % | ×1.24 |
| `1/(1−RA)` (engineering strain, `1+s_f`) | −14 % | −31 % | −37 % | −52 % | ×1.94 |
| **`RA/(1−RA)` (engineering strain, no `+1`)** | **+3.2 %** | **−2.0 %** | **−0.3 %** | −16.5 % | ×2.71 |

Under the last reading the paper's own formula reproduces **three of its four
printed rows to ≤3.2 %**, two of them to ≤2 %. Three consecutive rows agreeing
that closely on a formula with no free parameter is not coincidence: the column
**is** computed from the tabulated `P_y`, `P_f`, RA, and the only genuine
non-closure is the **0.45 C row** (55.9 computed vs 67 printed).

`RA/(1−RA)` is the engineering strain at fracture under constant volume
(`l_f/l_0 = A_0/A_f = 1/(1−RA)`, so `s_f = RA/(1−RA)`). The reading that closes
is therefore Mott evaluating the denominator as `s_f` where the printed formula
reads `(1+s_f)` — a one-symbol slip in a formula the page itself labels with `~`
and whose coefficient is already loose (`2 log(NV)/n` with `n = ½`, `N = 10¹³`
gives ≈120, not 160). This is an internal arithmetic inconsistency in the 1947
paper, **not** evidence that the column is arbitrary.

### The 0.45 C row is independently indicted, by Mott himself

Two facts, neither dependent on the fit above:

1. The tabulated `P_y` column runs 34, 42, 45, **38** — it breaks its own
    monotone rise at exactly the row that fails. The `P_y` that would reproduce
    the printed γ = 67 under the closing reading is **45.5**, which is what a
    monotone continuation of 34/42/45 would give.
1. Mott's closing paragraph (anchor `Thus a material with a high-stress`) states
    average fragment length `∝ P_f√((1+s_f)/ρP_y)`. Evaluated on the printed
    rows this runs 22.46, 19.72, 19.61, **20.29** — it *rises* at 0.45 C, while
    `√(P_f/γ)` from the printed γ column falls monotonically (1.64, 1.29, 1.23,
    1.11). **The printed 0.45 C row contradicts the paper's own stated trend
    law.** Rows 1–3 do not.

So the defect is localised to one row, and it is the row the repo's *top-end*
anchor sits on.

______________________________________________________________________

## 2. The judgment the finding was escalated for

> Is a printed column that does not reproduce from its own paper's stated
> closure still usable as a calibration series, and under what caveat?

**Yes — bracketed, not extrapolated, and row-by-row rather than wholesale.**

The general answer is not "a failing table is unusable"; it is that a closure
failure **localises** where the table may be trusted. A closure invariant that
fails on one row of four is a *per-row* verdict, and the correct response is to
use the rows that close and refuse the row that does not — exactly as the
tiling/monotonicity forms in `.claude/rules/source-data-fidelity.md` are read
per group rather than per table.

The stated caveat that must accompany any use of this series:

> Mott 1947 §3's γ column reproduces from the paper's own
> `γ ~ 160 P_y/P_f(1+s_f)` to ≤3.2 % on the iron, 0.1 C and 0.25 C rows when
> `s_f` is taken as the engineering fracture strain `RA/(1−RA)`; the 0.45 C row
> does not reproduce (computed 55.9 vs printed 67) and its `P_y` = 38 breaks the
> column's own monotone trend. Interpolations bracketed by two closing rows are
> sourced; anything anchored on or above the 0.45 C row is a **working value**,
> not a sourced one.

______________________________________________________________________

## 3. Verdicts

### 3.1 `γ′ = 47` — "US WW2 WDSS1" — **SOUND**

Covers: `src/arty/fragmentation.py` `SteelParams("US WW2 WDSS1")`;
`updates/wdss1-steel-grade/derivation.md`; the 60 mm M49A2 row of this update's
§7.4 (`α = 6.15`, `γ = 14.0`).

47 is a local-linear interpolation at 0.17 %C **inside** the 0.1 C → 0.25 C
segment. Both bracketing rows close (−2.0 % and −0.3 %). Recomputing the column
from the paper's formula and interpolating the *recomputed* values gives
**46.6** against the shipped 47.1 — a 1 % shift, an order of magnitude inside
the ±(45–49) band the entry already declares as its own parameter uncertainty.
No downstream number moves measurably. Unaffected.

### 3.2 `γ′ = 65` — "WW2 US HE Shell" — **SHIFTED**

Covers: `src/arty/fragmentation.py` `SteelParams("WW2 US HE Shell")` and its
comment block; `updates/wdss1-steel-grade/derivation.md` check C7 / assumption
A5; the 75 mm / 105 mm / 155 mm rows of this update's §7.3–§7.5.

65 is anchored as "just under Mott's 0.45 C row (γ = 67)" — the **one row that
does not close**, and the top row, so there is no bracketing row above it. Under
the closing reading that row is 55.9, and the 0.355 %C interpolation the entry
cites as its cross-check drops from **60.4 → 54.5** (−9.8 %). The shipped 65
then sits *above the entire recomputed series*, inverting the entry's own
justification ("sitting just under the 0.45 C row").

The conclusion — that this grade is harder/more brittle than WDSS1 and therefore
carries a higher γ′ — **survives**: the ordering 47 < γ′(0.355 %C) is preserved
under both readings (46.6 < 54.5). Only the number shifts, and it shifts in the
direction the existing code comment already anticipates ("the shipped 65
OVERstates rather than understates the grade contrast"). This is *shifted*, not
*void*: same conclusion, different number.

**Not fixed here, per the assess-only scope.** The re-anchor is a
`wdss1-steel-grade` registry question, not a shape-closure one. Whoever takes it
should note that only `σ_F/γ′` is identifiable, so a γ′ move is a `σ_F/γ′` move
and must be argued as such.

### 3.3 The shape closure itself — **SOUND**

Covers: `updates/mott-fragment-shape-closure/derivation.md` §§1–5, §7.1–7.3,
§7.5, and the shipped `_MOTT_BREADTH_FACTOR` / `aspect_ratio` / `breadth_factor`
constants.

The closure's own content is **γ′-independent**. `γ = α^{-2/3}γ′` and
`μ = A κ_x² (σ_F t_bu/γ′)(r_bu/V₀)²` are structural: `α`, the cube limit
(`A = κ_x = 1`, `t₀ = x₀` ⇒ `α = 1`, `γ = γ′`), the mass closure, the unit
checks, and the weakening of grade sensitivity from `μ ∝ γ′^{-3/2}` to
`μ ∝ γ′^{-1}` all hold for any γ′. Nothing in §§1–5 reads the Mott γ column at
all — that column enters only through the registry values used to *evaluate* the
validation tables.

Propagating the two candidate rebaselines analytically (`μ ∝ γ′^{-1}`,
`γ = α^{-2/3}γ′`; script §"exposure of the shape closure"):

| claim | shipped (γ′ = 65) | γ′ = 55.9 | γ′ = 54.5 | verdict |
| --- | --- | --- | --- | --- |
| §7.3 `μ` vs Tolch 0.95–3.5 g (75 mm) | 0.793 g, 1.20× under floor | 0.922 g | 0.946 g | **improves** (miss → 1.03×) |
| §7.3 `N(>6 g)` within 2× of 278 | 0.83× | tracks `μ` up, stays inside | " | **holds** |
| §7.4 `N(>0.5 g)` inside arena 800–3000 | 1640 / 2213 / 2648 | 1494 / 1984 / 2332 | 1470 / 1947 / 2282 | **holds** |
| §7.5 Option C `A/C` within ~2× | 0.69 / 0.52 / 0.59 | 0.80 / 0.60 / 0.68 | 0.82 / 0.62 / 0.70 | **improves** |
| §7.4 `γ` = 21.8–28.9 inside Gold's 20–50 | inside | 24.9 / 20.0 / **18.7** | 24.2 / 19.5 / **18.3** | **weakened** |

Every validation that is a *fidelity* check either holds or moves toward its
target. The single claim that weakens is the §7.4 corroboration sentence: at a
rebaselined γ′ the 155 mm falls to γ ≈ 18.7, just below Gold's 20 floor, and the
105 mm sits on the floor. That sentence is a soft cross-check ("independent
corroboration that `α` is the right size"), not a PASS criterion, and one shell
of three grazing the edge of a published *range* does not overturn it — but it
should stop being written as a clean "lands inside".

**One sentence to soften in `derivation.md` §7.4** (record only, not applied):
after "lands inside Gold's own published 20–50 range", add that this rests on
`γ′ = 65`, whose Mott anchor row is the one row of that table that fails the
paper's own closure; at a rebaselined `γ′ ≈ 55` the 155 mm drops to γ ≈ 19, i.e.
the corroboration is directional, not tight.

### 3.4 What is **void** — nothing

No claim in this update is overturned. The one artifact statement that is
straightforwardly *wrong* is in the finding itself and in anything that repeats
it: the assertion that the formula "is flat" and therefore that the column's
rising trend is unsupported. It is not flat under the closing reading (span
×2.71 against the printed ×3.35), and the trend is supported on three rows.

`challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`
should keep its pinned C2 residuals (they are correct for the readings it
tests) but its docstring claim that the formula "does not reproduce the column
under either reading of `s_F`" is now known to be a statement about *those two*
readings only. Its C3 (mild-steel length ⇒ γ = 16) is untouched by this work and
remains an open non-closure.

______________________________________________________________________

## 4. Secondary — the Gold 2017 "Mott (1943)" attribution

Per the `OPEN-FINDINGS.md` entry beginning *"Gold 2017 attributes to 'Mott
(1943)'…"*. `derivation.md` is **not rewritten here**; this records what it
should say. Affected rows: (G4), (G6), and assumption A9.2.

What the primary (Mott & Linfoot, A.C. 3348) actually supports:

| element | current attribution | correct attribution |
| --- | --- | --- |
| fragment idealised as a parallelepiped `l₀ × x₀ × t₀` | Gold eq. (4) → "Mott (1943)" | **survives** — Mott & Linfoot 1943 |
| `A ≡ l̄/x̄` constant across shells | inherited from Gold's "Mott (1943)" | **not primary-backed.** The primary disclaims it twice: "we have not been able to find a theory to account for the average length of the splinters" (p. 2) and "our theory … does not account for the length of splinters from shells, but only for their breadth" (p. 4); its §3 treats length as *independent* of breadth. Restate as an **empirical closure**, valued from Felix, Colwill & Harris (2022) Table 4 (already row (A16)), with Gold's citation marked **secondhand and contradicted by its primary**. |
| mean cross-sectional area `∝ (r/V)²` | Gold → "Mott (1943)" | **Mott 1947**, not 1943 — it is this repo's own row (G2), `x₀ ∝ r/V` |

Consequences to record, none of which change a number:

- The **value** `A = 1.6` is unaffected — it was never Gold's; it is Felix 2022
    Table 4 (ledger §16), and row (A16) already cites it correctly.
- What changes is the **status** of A9.2. It is currently written as a
    caliber-/material-independence assumption on a theoretically-motivated
    constant. It should be written as: *the Mott framework supplies no theory of
    fragment length at all, so `A` is a purely empirical cross-dataset regularity
    imported from outside Mott; the framework's silence, not a competing theory,
    is what licenses treating it as constant.* That strengthens rather than
    weakens the case for its ±5 % sensitivity note (`μ ∝ A`), because a
    measured spread is the whole of the evidence rather than a perturbation on a
    theory.
- Rows (G4)/(G6) should cite **Gold 2017** for the algebra (which is Gold's own)
    and stop routing the parallelepiped premise through Gold's "Mott (1943)"
    label except for the one element that survives. Do this in the same edit that
    closes the sibling bare-line-number finding on (G4)/(G6)/(G16).

______________________________________________________________________

## 5. Evidence paths

- Strain-reading sweep, per-row residuals, interpolation and downstream
    exposure —
    `experiment/fragmentation-field/updates/mott-fragment-shape-closure/checks/mott-1947-gamma-column-strain-reading.py`
    (`uv run python …`, < 1 s)
- Series (extracted once) —
    `doc-reference/fragmentation/gurney-equations-fragmentation/tables/section3-gamma-vs-composition.csv`
- Source page — `…/gurney-equations-fragmentation/rspa.1947.0042.md`, p. 308
    (`source.pdf` p. 9), anchors `Some values of`,
    `For mild steel, then, according to`, `Thus a material with a high-stress`
- Prior closure check (C1/C2/C3) —
    `experiment/fragmentation-field/challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py`
- Downstream tables rebaselined —
    `experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`
    §§7.3, 7.4, 7.5
