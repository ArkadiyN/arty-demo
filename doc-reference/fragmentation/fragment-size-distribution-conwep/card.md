# Gold (2017), PAFRAG-Mott large-L/D fragmentation model — Card

## Identification

|            |                                                                                                                         |
| :--------- | :---------------------------------------------------------------------------------------------------------------------- |
| Title      | Fragmentation model for large L/D explosive fragmentation warheads                                                      |
| Author     | Vladimir M. Gold, US Army RDECOM-ARDEC, Picatinny Arsenal                                                               |
| Published  | *Defence Technology* **13**(4), 300–309, August 2017 — open access, CC BY-NC-ND 4.0                                     |
| DOI        | [10.1016/j.dt.2017.05.007](https://doi.org/10.1016/j.dt.2017.05.007)                                                    |
| Extraction | `1-s2.0-S221491471730079X-main.md` — prose from the text layer, **equations reconstructed as LaTeX by the vision pass** |
| Scan       | `source.pdf`, retained on disk, gitignored per `doc-reference/**/*.pdf` — 10 pp., text layer on every page              |
| Verified   | 2026-08-03, equation chain against the retained scan                                                                    |

**The directory slug is misleading.** `fragment-size-distribution-conwep`
suggests a ConWep document; this is Gold 2017, and it is what the repo cites as
"Gold (2017)" throughout. `challenges/mott-scale-gap/_shape_closure_check.md`
already flags the mismatch. The slug is not renamed here — that would rot every
existing citation — but no future citation should read the slug as provenance.

## What this repo takes from it

**Equations, not data.** Gold 2017 supplies the PAFRAG-Mott closure chain that
`src/arty/fragmentation.py:mott_params` and `src/arty/zones.py:_zone_mott_mu`
implement, plus two prose facts (`γ = 50`, and the three-volume-expansion
break-up rule of thumb). Its one numeric table is cited nowhere.

That makes the fidelity question different in kind from every other document in
this audit: not *was the right cell read*, but **was the right formula read** —
and the answer had to come from algebra, because neither the extraction nor
the scan's text layer can settle it. See Closure below.

| Cited as                              | Consumer                                                                                                               |
| :------------------------------------ | :--------------------------------------------------------------------------------------------------------------------- |
| eq. (2) — Mott fracture spacing `x₀`  | `fragmentation.py:307`, `zones.py:143`, `_governing-equations.qmd:74`                                                  |
| eq. (4) — parallelepiped shape factor | `fragmentation.py:95`, `_governing-equations.qmd:82`                                                                   |
| eq. (6) — shape absorbed into γ       | `fragmentation.py:97,316`, `zones.py:148`                                                                              |
| eq. (7) ≡ eq. (16) — half-mass μ      | `_governing-equations.qmd:59`, `_four-zone-3d.qmd:88`, `zones.py:134`, `wdss1-steel-grade/`, `frag-field-3d-geometry/` |
| eq. (5) — μ ∝ (r/V)³                  | `_limitations.qmd:72,75` (error-propagation argument)                                                                  |
| `γ = 50`                              | `_validation.qmd:48` (the Mott-self-consistency band)                                                                  |
| 3-volume-expansion rule               | `fragmentation-field.qmd:17`                                                                                           |
| §2 multi-region zoning                | `_limitations.qmd:14`                                                                                                  |

## Anchors

Greppable, unique in `1-s2.0-S221491471730079X-main.md`, and verified present
on the scan by the check script. **Use these, not line numbers** — the
extraction has already been re-run once, and `mott-fragment-shape-closure`
still carries three bare-line-number citations into this file (registered
finding, `derivation.md`).

| Equation  | Anchor (the sentence introducing it)                                | Scan  |
| :-------- | :------------------------------------------------------------------ | :---- |
| (1)       | `represents total number of fragments of mass greater than`         | p.302 |
| (2)       | `the average circumferential length of the resulting fragments is`  | p.302 |
| (4)       | `the average fragment mass takes the following form`                | p.303 |
| (5)       | `Substituting equation (2) into equation (4) results in`            | p.303 |
| (6)       | `warrants knowledge of the average fragment mass but not the shape` | p.303 |
| (7)       | `allows equation (5) to be put in a simpler and more useful form`   | p.303 |
| (16),(17) | `the resulting fragment size distributions in each segment`         | p.303 |
| γ = 50    | `All of these models employ the same value for`                     | p.306 |
| V/V₀ ~ 3  | `criterion is accepted as a rule of thumb`                          | p.301 |

Anchors are introducing *sentences*, deliberately: formulae render differently
in every extractor and would not survive a re-extraction as match keys, prose
does.

## Equations as printed

- **(1)** `N(m) = N₀ e^{-(m/μ)^{1/2}}`, with **μ defined as one half of the
    average fragment mass**, `N₀ = M/2μ`, `M` the total mass of the fragments.
- **(2)** `x₀ = (2σ_F/ργ′)^{1/2} · r/V` — `r` the ring radius and `V` the
    outward shell velocity *at the instant of fracture*; `γ′` "a semi-empirical
    statistical constant determining the dynamic fracture properties".
- **(4)** `μ = ½ α ρ x₀³`, with `α = (l₀/x₀)(t₀/x₀)` — the fragment idealised as
    a parallelepiped of length `l₀`, breadth `x₀`, thickness `t₀`.
- **(5)** = (2) substituted into (4): `μ = ½ (2σ_F/(ρ^{1/3} α^{-2/3} γ′))^{3/2} (r/V)³`.
- **(6)** `γ = α^{-2/3} γ′` — the shape factor absorbed into the material
    constant, because (1) "warrants knowledge of the average fragment mass but
    not the shape".
- **(7)** `μ = ½ (2σ_F/(ρ^{1/3} γ))^{3/2} (r/V)³`.
- **(16)** `μⱼ = √(2/ρ) (σ_F/γ)^{3/2} (rⱼ/Vⱼ)³` — **the same formula as (7)**,
    written per ring segment. The repo cites both names for it.
- **(17)** `N₀ⱼ = mⱼ/μⱼ`. **This contradicts (1)** by exactly a factor of 2 —
    a fact about the paper, not resolved here. The resolution (which side
    `src/arty` takes, and why) is in
    `experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`
    §10.

**Gold overloads the symbol α.** Eq. (4)'s α above (`= (l₀/x₀)(t₀/x₀)`, the
parallelepiped shape factor feeding eq. (6)/(7)/(16)) is unrelated to a
second, unconnected use later in the paper: §4's detonation-wave incidence
angle (anchor `incident angle $\alpha$ between the detonation wave direction`)
and its Fig. 7(b) caption (anchor `detonation shock wave incidence angle $\alpha$`), where "the steeper angle α is, the higher parameter γ is" — the
*opposite* sign relation from eq. (6)'s aspect-ratio α, where larger α lowers
γ. Do not conflate the two when reading "Gold's α" off this document.

## Closure

Script:
`experiment/fragmentation-field/challenges/source-data-audit/checks/gold-2017-equation-provenance.py`
(runs in ~0.3 s; skips the page comparison cleanly when the gitignored scan is
absent).

### The sign no surface in this repo can give you

Everything turns on one character: the minus in eq. (6)'s `α^{-2/3}`. Take it
wrong and μ is off by a factor of **α²** — 14× to 32× across the break-up
velocities this model runs at — in the direction that makes fragments smaller
and more numerous. Neither available surface settles it.

**The `.md`'s equations are reconstructed, not transcribed.** They are LaTeX;
the raw text layer contains no LaTeX at all. So the minus in
`\alpha^{-2/3} \gamma'` is a *vision model's reading* of the page — and Phase 7
of this audit established that this pipeline invents values. Nothing exempts an
exponent from that.

**The raw text layer cannot arbitrate either.** `source.pdf` has a clean text
layer on all 10 pages, so by the `sandia-cd-provenance.py` pattern the lines
could simply be printed — except that this PDF encodes the minus as the
**unmapped control character `\x04`, which it also uses for hyphens**:

| On the page                   | Extracts as                          |
| :---------------------------- | :----------------------------------- |
| eq. (5) `ρ^{1/3} α^{-2/3} γ'` | `r1=3a\x042=3g0`                     |
| eq. (6) `γ = α^{-2/3} γ'`     | `g ¼ a\x042=3g0`                     |
| eq. (11) `Θj − π/2N`          | `Qj \x04 p`                          |
| prose "Θ-angle"               | `the Q\x04angle that corresponds to` |

The same byte is a minus in eq. (6) and a hyphen in "Θ-angle" — it carries no
sign identity. Being non-printable, it is also dropped by any
printable-character filter, which silently turns `α^{-2/3}` into `α^{2/3}`:
the wrong-sign reading, with no glyph-level trace.

(The plus in eq. (11) maps to a *different* character, `þ` — so plus and minus
are not literally identical strings. They are simply both unreadable as signs
without knowing the font's private mapping.)

**And the extraction-quality gate cannot see any of it, twice over.**
`scan-extraction-quality.py` flags Private Use Area glyphs (U+E000–F8FF); this
font maps its unmapped glyphs into the **C0 control range** instead — 61 of
them in the text layer, 0 PUA — so the detector's range misses every one. It
also runs on the `.md`, which the vision pass has already laundered to zero
control characters. It reports `0 / 2 file(s) flagged` for this document. That
is a second structural blind spot in that gate, distinct from the
column-inversion one: here the reconstruction *removes* the evidence rather
than the gate merely failing to interpret it.

**The source closes it itself.** Eq. (5) is stated to be eq. (2) substituted
into eq. (4), and only one exponent makes that substitution true. Solving for
it numerically at five values of α:

```
   alpha   mu via eq. (4)   exponent s
    0.25     2.241808e-06    -0.666667
    0.50     4.483615e-06    -0.666667
    2.00     1.793446e-05    -0.666667
    3.60     3.228203e-05    -0.666667
   10.00     8.967231e-05    -0.666667
```

`s = -2/3`, uniquely. This is a closure invariant in the sense the rule means —
arithmetic internal to the source, derived from the source's own stated
relations, with a pass/fail answer — it just happens to close a formula rather
than a table.

The extraction carries `\alpha^{-2/3} \gamma'` in both eq. (5) and eq. (6), so
the vision reconstruction agrees with the algebra. **That agreement is what
promotes it from an unchecked model reading to a checked one** — read on its
own it would be evidence of nothing, since it is the reading under test.

The paper's own eq. (1)/eq. (17) contradiction on N₀ — and which side
`src/arty` takes, and why — is resolved in
`experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`
§10, not here (relocated 2026-08-03, `.claude/rules/source-data-fidelity.md`).

## Tables

| Table                                       | CSV                             | Closure                                                 |
| :------------------------------------------ | :------------------------------ | :------------------------------------------------------ |
| Table 1 — Charge B 100 % recovery, ±booster | `table-1-charge-b-recovery.csv` | the source's own `N/N*` normalisation, + P_CJ constancy |

Two rows, **cited nowhere in this repo**. Transcribed so the document stops
reading as "carries numbers, no CSV" in the Phase 2.5c sweep and so a future
consumer reads a file rather than re-typing prose. Verified against the scan
(p.308).

Figures 1–11 are curves; **none is digitized anywhere in this repo**, and no
number in `src/arty` or any `.qmd` was read off one. That is the finding for
this document's `images/` directory — not that they were checked, but that
nothing rests on them. Should a future pass want `N(m)` off Fig. 5 or 8, it is
a fresh digitization job with its own closure, and the DoD-1975 Figure-3
incident (ledger §13b) is the warning about doing it by eye.

## What is *not* certified

- **Whether Gold's `γ = 50` is `γ′` or the shape-absorbed γ of eq. (6)** is a
    criterion-match question, resolved (not just flagged) in
    `experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`
    §10 — relocated there 2026-08-03, `.claude/rules/source-data-fidelity.md`.
- **The attribution of eq. (3)/(4) to "Mott (1943)"** is Gold's, and it does not
    survive contact with the primary. Registered as a deferrable finding on
    `mott-fragment-shape-closure/derivation.md:19` (ledger §16): Mott & Linfoot
    A.C. 3348 states the opposite twice, and only the parallelepiped idealisation
    survives.
- **Nothing about the multi-region model** (eqs. 18–26, §3–4). The repo uses the
    one-region chain only; `_limitations.qmd:14` cites §2 for the zoning
    *concept*, not for any of its equations.
- **Every other equation in the `.md`.** All of its LaTeX is vision-model
    output, and the closure covers only eqs. (1), (2), (4), (5), (6), (7),
    (16), (17) — the chain the repo actually consumes. The remaining ~18
    equations are *unverified reconstructions*, indistinguishable on the page
    from the certified ones. A future pass that reaches for eq. (20) because
    "the equations in this document were checked" is reading this card wrong:
    the check was per-equation and drew its authority from the substitution
    eqs. (2)/(4)/(5) happen to admit, not from the extraction being trustworthy.

## Why this document had no card until now

Found by the Phase 2.5c admissibility sweep
(`checks/doc-reference-admissibility-sweep.py`) as the widest-footprint source
reaching shipped `src/arty/` with no card, no closure, no retained scan, and
every citation into it a bare line number. It was the registered blocker on
Phase 3 for `mott-fragment-shape-closure` and `mott-scale-gap`. The scan was
supplied by the user on 2026-08-03; the equation chain closed the same day.
