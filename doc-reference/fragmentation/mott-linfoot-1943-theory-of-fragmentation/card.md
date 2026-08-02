# Mott & Linfoot (1943) — A theory of fragmentation

**Document:** N. F. Mott and E. H. Linfoot, "A theory of fragmentation",
Ministry of Supply, **A.C. 3348**, January 1943. Bristol University Extra-Mural
Group. Stamped `RESTRICTED` (struck) / `UNCLASSIFIED`.\
**Copy:** DTIC `ADB968781`, 13 pdf pages — report pp. 1–5 are text, pp. 6–8 are
the figure plates (figs. 3–7), the rest is cover and distribution matter.\
**Retained scan:** `source.pdf` beside this card — **not committed**
(`.gitignore:58`); re-acquire from DTIC by that accession number.

**There is no markdown extraction of this document, deliberately.** The scan
carries its own embedded OCR layer and that layer is unusable — a page of it
does not reconstruct into sentences. Every fact and digit on this card was read
off a 200–400 dpi render of the page instead, and is held admissible by the
closures below rather than by a text match. Re-extraction is not attempted
while the pipeline fix (`plan` Phase 7) is outstanding.

## Why this document is here

It is **the primary behind Gold (2017)'s Mott-1943 attributions**, and Gold is
what `updates/mott-fragment-shape-closure/` derives the shipped fragment-shape
closure from. Nothing in `src/arty/` consumes a number from this report; what it
settles is whether Gold's sentence *"According to Mott (1943), the ratio of the
fragment circumferential breadth to the length is approximately constant"*
rests on the primary it names.

**It does not.** See "What the report does not contain" below — that is the
finding this document was acquired to establish.

## Tables

| File                                               | What it holds                                                                                     | Closure            |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------ |
| `tables/section2-fragment-weight-distribution.csv` | p.3, observed vs calculated fragment counts in six weight bins, 3.7 in. A.A. shell and 3 in. U.P. | passes — see below |

```
uv run src/utils/check-table-invariants.py doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/tables --all
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-closures.py
```

Three closures hold, which is what makes a visually-read table citable:

- **The calculated column is a one-parameter fit.** It is eq. (4)
    `N(m) dm = C exp(-M/M₀) dM`, `M = m^(1/3)`, at the printed
    M₀ = 0.33 oz^(1/3). Dividing each printed count by its bin's probability
    mass must give the same `K = C·M₀` on every row — it does, to ±2%, and the
    column regenerates from that single K as 455 / 128 / 181 / 13 / 5 against
    the printed 454 / 129 / 181 / 13 / 5. A misread digit or a misread bin edge
    breaks this immediately.
- **The two column pairs sum identically** — 782 = 782 (shell) and
    1478 = 1478 (U.P.), with no free parameter, because C is fitted to the
    observed total.
- **The p.2 worked example reproduces to 4%** (below).

The U.P. column's K spreads 30% rather than 2%. That is the source's own
rounding — its M₀ is printed to two significant figures and the fit is far more
sensitive to M₀ at 0.15 than at 0.33 — not a transcription defect; the sum
closure confirms those digits independently.

## What the report contains

### 1. The mean fragment **breadth** — an energy-of-fracture theory

Anchor: `THE MEAN FRAGMENT SIZE` (p.1). Cracks start on the inside of the
casing and spread outwards (fig. 1); a splinter of cross-section `ABB'A'` flies
out, and rupture is assumed to occur once the transverse kinetic energy of the
fragment exceeds the energy `Wt` needed to open a new crack. That gives, as
eq. (2), the largest surviving breadth

```
a = ( 24 r² W / (ρ V²) )^(1/3)
```

with `r` the casing radius at rupture, `V` the fragment velocity, `W` the
rupture energy per unit area and `ρ` the metal density.

**Worked example** (anchor `For r we take 2.2 inches`, p.2): `W` = 70 ft-lb per
sq. in. — the *lower* end of Southwell's 70–800 impact range, chosen because
the metal is "very brittle" after plastic deformation — with r = 2.2 in. and
V = 2500 ft/sec for the 3.7 in. A.A. shell gives **a = 0.55 in.**, "in good
agreement with the observed value". Recomputing gives 0.529 in.; `a` goes as
`(W/ρ)^(1/3)`, so the 4% is 11% in `W/ρ` and sits inside Mott's own "our value
will be very approximate".

**This is not the scaling `src/arty` uses, and it is not the 1947 scaling.**
Eq. (2) makes breadth go as `(r/V)^(2/3)`. Mott (1947) instead gives
`x₀ = (2P_F/ργ)^(1/2)·r/v`, i.e. `(r/V)^1`, from a different (Mott-wave,
statistical) argument. The repo's closure descends from the 1947 form via Gold
eq. (2). The two theories are alternatives, not a chain.

### 2. The fragment-weight distribution — the origin of the Mott exponential

Anchor: `DISTRIBUTION OF FRAGMENT WEIGHTS` (p.2). Attributed to a private
communication from Dr. D. L. Welch dated 24 Sept 1941: with `M = m^(1/3)`,

```
N(m) dm = C exp(-M/M₀) dM                                   (4)
```

M₀ = **0.33** (3.7 in. shell) and **0.15** (3 in. U.P.), in oz^(1/3); total
number `C·M₀`, total weight `6M₀⁴C`, mean weight `6M₀³` = **0.21 oz** for the
shell. The counts are in `tables/`. For the heavier fragments the report
prefers `N dm = C exp(-α m^(1/2)) d(m^(1/2))` (6), which fits Payman's model-bomb
data better (figs. 3–4).

### 3. Why the exponential should hold — the ruled-line argument

Anchor: `MATHEMATICAL DISCUSSION OF THE DISTRIBUTION LAW` (p.4). A sheet cut by
two sets of parallel lines gives fragments of breadth `x` and length `y` drawn
from `exp(-x/x₀)` and `exp(-y/y₀)`; the number with area above `a²` then goes as
`z K₀(z)` with `z = 2a/√(x₀y₀)`. Cutting instead by lines of random direction is
shown to give a straighter `log ν` vs `a` plot, and `ν(a)` is proved to tend to
a non-zero constant as `a → 0`.

This is where the rectangular-prism idealization actually lives.

## What the report does **not** contain — the finding

Gold (2017) makes three attributions to "Mott (1943)"
(`fragment-size-distribution-conwep/1-s2.0-S221491471730079X-main.md`, anchor
`A series of engineering assumptions`). Against the page:

| Gold's attribution to Mott (1943)                             | Verdict against the primary         |
| ------------------------------------------------------------- | ----------------------------------- |
| the fragment breadth:length ratio "is approximately constant" | **contradicted**                    |
| average cross-sectional area ∝ `(r/V)²`                       | **wrong paper** — that is Mott 1947 |
| fragments idealized as a **parallelepiped**                   | **supported** (sect. 3)             |

The report states the opposite of the first, twice and unambiguously:

- p.2, anchor `We have not been able to find a theory`: *"We have not been able
    to find a theory to account for the average **length** of the splinters in
    this type of shell."*
- p.4, anchor `our theory is incomplete`: *"…our theory is incomplete, as it
    does not account for the length of splinters from shells, but only for
    their **breadth**…"*

And where sect. 3 does treat length at all, it makes it *independent* of
breadth — anchor `the lengths have an average value`: cracks run parallel to
the axis at average spacing `x₀`, *"and the lengths have an average value `y₀`
**independent of the breadth**"*. Two independent exponential parameters is the
opposite of a fixed ratio.

The second attribution belongs to the 1947 paper: `(r/V)²` area follows from
`x₀ ∝ r/v` there, whereas eq. (2) here gives `(r/V)^(4/3)`.

**What this does and does not affect.** The shipped
`_MOTT_ASPECT_RATIO = 1.6` takes its *value* from Felix, Colwill & Harris
(2022) Table 4 (`explosion-fragment-model`, re-baselined — ledger sect. 16), not
from Mott 1943, so no shipped number is wrong. What is unsupported is the
*structural premise* — that one constant length:breadth ratio applies across
shells — which Gold presents as primary-backed and `mott-fragment-shape-closure`
inherits. Registered as a deferrable finding for the Phase-3 pass on that
thread; it is a question about the premise, not a wrong digit.

## Content this document does *not* settle

- **No γ, and no composition table.** The 1943 theory has no `γ`; its material
    input is the rupture energy `W`. It therefore cannot adjudicate the Mott
    1947 sect. 3 γ-column non-closure (ledger sect. 17b) — that finding stands.
- **No breadth:length ratio value**, per above.
- **Figures 3–7** (pdf pp. 10–12) are plates with no text layer and were not
    digitized; nothing cites them.

## Provenance of this card

Written 2026-08-02 during the Phase-2.5 source admissibility gate, from a scan
supplied by the user. Detail:
`experiment/fragmentation-field/challenges/source-data-audit/ledger.md` sect. 18.
