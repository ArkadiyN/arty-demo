# Mott (1947) — Fragmentation of shell cases

**Document:** N. F. Mott, "Fragmentation of shell cases", *Proc. Roy. Soc. A*
**189** (1947) 300–308 (received 14 December 1945)\
**DOI:** https://doi.org/10.1098/rspa.1947.0042\
**Extraction:** `rspa.1947.0042.md`, figures in `images/`\
**Retained scan:** `source.pdf` beside this card, 9 pages — **not committed**
(`.gitignore:58`); re-acquire from the DOI above.

The folder name says "gurney-equations" and is wrong — this paper contains no
Gurney equation. It is Mott's fragment-length theory. The name is kept because
eight artifacts cite the path.

## Tables — read these, not the prose

| File                                       | What it holds                                      | Closure                                                                                        |
| ------------------------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `tables/section3-gamma-vs-composition.csv` | §3 p.308, the four-material composition → γ series | column orderings hold; **the paper's own γ formula does not reproduce the column** — see below |

```
uv run src/utils/check-table-invariants.py doc-reference/fragmentation/gurney-equations-fragmentation/tables --all
uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-1947-gamma-and-length-closure.py
```

## The facts this document supplies to the model

### 1. κ_x = 1.5 — mean fragment breadth in fracture spacings

Anchor: `The fragments have lengths most of which lie` (p.305 = `source.pdf`
p.6). Finding (1) of Mott's ruled-line Monte Carlo: fragment lengths *"lie
between x₀ and 2x₀, and the average length is about 1·5x₀."*
`src/arty/fragmentation.py` ships it as `_MOTT_BREADTH_FACTOR = 1.5`.

**Confirmed against Mott's own worked example, not just the sentence.** p.306
(anchor `As a numerical example`) sets x₀ = 1·6/√γ in. for a 3 in. bomb and
concludes *"if γ ~ 100, the average fragment length is about 0·24 in."* —
and 1.5 × 1.6/√100 = 0.24 exactly. The 1.5 in finding (1) is the same 1.5 Mott
used to get his printed answer.

Note the symbol is **x₀** (subscript zero), not `x_g`. Both the extraction and
`challenges/mott-scale-gap/_scale_verdict_ledger.md` render it `x_g`.

### 2. The composition → γ series

Anchor: `Some values of` (p.308 = `source.pdf` p.9), values deduced from
Körber & Rohland (1924) — *not* "Rohdal", as `fragmentation.py` had it.

| material    | reduction in area | true U.T.S. P_F (kg/mm²) | P₂  | γ   |
| ----------- | ----------------- | ------------------------ | --- | --- |
| iron        | 0·83              | 54                       | 34  | 20  |
| steel 0·1 C | 0·70              | 70                       | 42  | 42  |
| 0·25 C      | 0·63              | 80                       | 45  | 53  |
| 0·45 C      | 0·57              | 82                       | 38  | 67  |

`src/arty/fragmentation.py` reads only the γ column: γ = 47 for WDSS-1
(interpolated inside the 0.1 → 0.25 C segment) and γ = 65 for the legacy grade
(anchored just under the 0.45 C row).

**This table's γ column does not close on the paper's own formula — blocking.**
Two lines above it the page states γ ~ 160 P₂/P_F(1 + s_F), with P_F the true
stress and s_F the plastic strain at fracture (p.307, anchor `where P_F is the true stress`), and introduces the table as values *"of P₂, P_F, s_F … deduced
below"*. Feeding the tabulated columns back through that formula gives
**55.0 / 56.5 / 55.2 / 47.2** taking s_F as the reduction in area, or
**36.3 / 43.6 / 45.1 / 40.2** taking s_F = ln(1/(1−RA)), the true plastic
strain. Both are essentially **flat** (×1.20) where the printed column rises
**×3.35**.

The rising trend is exactly what this repo consumes — γ = 47 is an
interpolation *along* it. Every digit was re-read off the page at 420 dpi, so
this is not a transcription defect; it is either a fuller derivation Mott did
not print (he writes "~", and says N "can only be guessed") or an
inconsistency in the paper. Which one, and whether the series is still usable
as a calibration ladder, is a modelling question — registered as a blocking
finding against `src/arty/fragmentation.py`.

A second non-closure, consumed by nothing: p.308 states that for mild steel the
§2 bomb gives fragments of average length 0·6 in., which implies γ = 16 — below
even the iron row.

## Extraction defects found while re-baselining

The 2026-07-25 re-extraction (after the `google_timeout_ms` fix) is **correct**
on the two points its own header flags: γ(0.1 C) = 42, and the third row is
0.25 C. Remaining defects in `rspa.1947.0042.md`, none of them consumed:

| Location             | Extraction                         | Page                                                        |
| -------------------- | ---------------------------------- | ----------------------------------------------------------- |
| p.304, after eq. (5) | `x_0 = (2P_y/\rho v)^{1/2} r/v`    | **`x₀ = (2P_F/ργ)^{1/2} r/v`** — two corruptions, see below |
| p.305                | `x_0(\Delta\sigma)^4`              | `x₀(Δσ)^{1/2}`                                              |
| p.306                | `x_g = 1.6/\sqrt\gamma`            | `x₀ = 1·6/√γ`                                               |
| p.305                | image tagged `fig3.jpx`            | the figure is **FIGURE 4**                                  |
| abstract             | "shell of a cylindrical ring-form" | "metal case of a cylindrical ring-bomb"                     |

`ρ = 480 lb./cu.in.` on p.306 is on the page as printed — it is Mott's own
slip for lb./cu.ft. The extraction is faithful there.

**The eq.-(5) corruption is the serious one.** The page defines the fracture
spacing as x₀ = (2P_F/ρ**γ**)^{1/2}·r/v; the extraction renders the
denominator `ρv` and the numerator `P_y`. That drops the **γ** dependence
entirely — the dependence the whole of §3 exists to quantify, and the one that
makes p.306's x₀ = 1·6/√γ true. Anyone deriving from the extracted line rather
than the page would lose it. Nothing did: `updates/mott-fragment-shape-closure/ derivation.md` (G2) carries the correct form, having taken it via Gold 2017
eq. (2), which agrees with the page symbol-for-symbol (σ_F ↔ P_F, γ′ ↔ γ).

**The header note in `rspa.1947.0042.md` is stale.** It says
`updates/wdss1-steel-grade/derivation.md` still interpolates on the old wrong
bracketing points; that derivation was in fact redone and now uses 0.1 C → 42
and 0.25 C → 53. The note is corrected in place.

## Other content cited elsewhere in this repo

- **x₀ = (2P_F/ργ)^{1/2}·r/v**, the fracture spacing, p.304 after eq. (5) —
    cited by `updates/mott-fragment-shape-closure/derivation.md` (G2) alongside
    Gold 2017 eq. (2).
- **Findings (2) and (3)** — x₀ ∝ r and x₀ ∝ 1/v, p.305 — the scaling
    arguments behind `challenges/mott-scale-gap/`.
- **γ = 2 log(NV)·(1/n)·(P₂/P_F)·1/(1+s_F)** with n = ½, p.307, anchor
    `If the stress-strain curve for large strains`. This is the relation the
    p.308 table fails to satisfy.
- **No "assume γ = 40" sentence was found** — `updates/wdss1-steel-grade/   review.md` asked for that to be confirmed against a clean scan, and the
    claim was withdrawn there. Corroborated here, at two strengths: the string
    `40` does not occur anywhere in `source.pdf`'s text layer, and pages
    304–308 (the whole of §2's conclusion and §3) were read at 200–420 dpi —
    p.306 says "if γ ~ 100", p.308 quotes a fragment length and no γ. Pages
    300–303 were checked only via the text layer, which on this scan is poor,
    so treat the absence as strong but not exhaustive.

## Provenance of this card

Written 2026-08-02 during the Phase-2.5 source admissibility gate; this
document previously had **no card at all** despite feeding two shipped
constants. Detail:
`experiment/fragmentation-field/challenges/source-data-audit/ledger.md` §17.
