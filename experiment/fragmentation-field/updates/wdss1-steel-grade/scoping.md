# Scoping — Second steel grade in the catalog: "US WW2 WDSS1" (0.14–0.20 % C)

**Author:** modeler agent
**Date:** 2026-07-25 (revised twice: (i) grade identity and composition confirmed as
**WDSS-1**, 0.14–0.20 % C, from *Ammunition Series 6*, Table 6-1 — the working
label "WD55" and its 0.18–0.28 % C band are superseded throughout; (ii)
**reconciled against the re-extracted Mott §3 table** — the earlier OCR reading
(γ = 32/53/67 at 0.1/0.2/0.3 % C) was an extraction artefact and is superseded
by 20/42/53/67 at 0.0/0.1/0.25/0.45 % C. Every γ figure in §3–§6 below is
restated from `derivation.md` §2/§4/C4/C7; one prose corroboration is
**withdrawn** as unsupported (§3), and the bound direction in §5/G2 **inverts**
from lower to upper. `derivation.md` is the source of truth for all of it —
nothing here is re-derived.)
**Status:** scoping pass — no derivation, no `src/arty/` edits
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Aspect:** the per-grade steel parameter pair `(sigma_f, gamma)` in
`src/arty/fragmentation.py: STEELS` — i.e. the material input to the Mott
half-mass `mu` and hence to `N_0`. Nothing else in the model is touched.

______________________________________________________________________

## 1 · Problem statement

`STEELS` (`src/arty/fragmentation.py:33–42`) holds exactly one entry,
`"WW2 US HE Shell"` (`rho = 7850`, `sigma_f = 800 MPa`, `gamma = 65`). A second
grade, **"US WW2 WDSS1"** — War Department shell steel **WDSS 1**,
**0.14–0.20 % C, 1.00–1.30 % Mn** (`doc-reference/ww2-shells/ammunition-series-6-wdss-specs/ammunition-series-6-wdss-specs.md`,
*Ammunition Series 6* §6-14 Table 6-1, 17 Feb 1953) — needs its own parameter
pair so the demo can show grade-to-grade sensitivity of the fragmentation field.

Scope boundary: this update produces **one catalog entry plus its
justification**. Wiring a grade selector into `app/sensitivity.py` (which today
rebuilds `SteelParams` from raw sliders) and into the notebook is a separate
presentation pass, not physics.

## 2 · What the model actually consumes — one identifiable DOF, not two

`sigma_f` and `gamma` enter the whole codebase in exactly one place,
`mott_params` (`fragmentation.py:169–177`):

$$ \mu = \sqrt{2/\rho}\;(\sigma_F/\gamma)^{3/2}\,(r_{bu}/V_0)^3, \qquad N_0 = M_{shell}/(2\mu) $$

(`_governing-equations.qmd` eq. 4, Gold 2017 PAFRAG eq. 16). `rho` is used
separately (here and in `retardation_coeff`), but `sigma_f` and `gamma` appear
**only as the ratio** \(R = \sigma_F/\gamma\), raised to 3/2.

**Consequence, and the single most important input to the derivation pass:** no
fragment-count, field or `P(kill)` observable can separate `sigma_f` from
`gamma`. The "parameter pair" is one identifiable degree of freedom \(R\) plus a
reporting convention for how it is split. A derivation that argues both numbers
independently is arguing about something unobservable in this model; it must
instead argue about \(R\) and state the split convention explicitly.

Baseline for scale (105 mm M1 geometry, TNT, \(V_0 = 994\) m/s):
\(R = 12.31\) MPa → \(\mu = 0.331\) g, \(N_0 = 18\,217\), \(N(>0.5\,\mathrm{g}) = 5\,324\).
Sensitivity: \(\mu \propto R^{3/2}\), \(N_0 \propto R^{-3/2}\) — a ±10 % error in
\(R\) is ±15 % in \(\mu\) and ∓14 % in \(N_0\).

## 3 · Literature audit — how far Mott (1947) carries this

Source read: `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`
(Mott, *Fragmentation of shell cases*, Proc. R. Soc. A **189**, 300–308,
doi:10.1098/rspa.1947.0042).

**What it supports (legible and citable):**

- §3 table, p. 308 (md lines 305–310, re-extracted 2026-07-25), after Körber &
  Rohland (1924): γ = 20 (iron), **42 (0.1 % C)**, **53 (0.25 % C)**,
  **67 (0.45 % C)**, with reduction-in-area falling 0.83 → 0.57 across the same
  series. Note the carbon spacing is **non-uniform**. This is a direct
  **composition → γ** map, dimensionless, and it **brackets the WDSS1 band** —
  the confirmed 0.14–0.20 % C sits *strictly interior* to the single 0.1–0.25 % C
  segment, bounded above and below by measured rows, so WDSS1's γ is an
  *interpolation*, not an extrapolation. That is the strongest single fact this
  source gives us.
- Qualitative closure, p. 308: a rapid rate of hardening near fracture (large
  $P_y$) → small fragments, and $P_y$ maps to γ through Mott's own
  $\gamma \sim 160\,P_y/[P_f(1+s_f)]$ on the same page, so larger γ → smaller
  fragments. This fixes the **sign** of every composition move.
- **No prose γ anchor exists.** An earlier revision of this section cited a
  p. 308 sentence "for mild steel … assume γ = 40" as an independent low-carbon
  anchor; that sentence is **not in the source** (a whole-file search for the
  value returns nothing) and the claim is **withdrawn** — see `derivation.md`
  §2/A9. Nothing depends on it: the corrected table brackets the whole WDSS1
  band between two measured rows, which is a stronger position than a prose
  value from the same author would have been.

**Where it falls short:**

1. **No σ_f we can use.** The re-extraction resolves the *unit* objection this
   item originally raised — the two stress columns are true U.T.S. $P_f$
   (54/70/80/82) and yield $P_y$ (34/42/45/38) in **kg mm⁻²**, i.e. 530–805 MPa
   — but not the *physical* one: they are *quasi-static*, while the model needs a
   *dynamic* flow stress at fracture (`_governing-equations.qmd:80` puts the
   dynamic value at 800–1000 MPa vs ~600 MPa quasi-static), which Mott does not
   give for any composition. See `derivation.md` §3.1.
1. **OCR degradation (partly resolved).** Equations (1)–(12) in the held markdown
   remain badly garbled (e.g. eq. 2 renders as `s² = 2 P_f ρ/ρ_s`). The μ closure
   must continue to be cited from Gold 2017 PAFRAG eq. 16 as it already is —
   **do not attempt to re-derive μ from this file.** The p. 308 fragment-length
   formula and the γ ∼ 160 P_y/[P_f(1+s_f)] relation *are* now legible and are
   used as an independent exponent check (`derivation.md` C3).
1. **Provenance mismatch of the γ values.** They come from 1924 German
   *annealed plain-carbon laboratory tensile bars*, not a forged, heat-treated
   US WW2 shell body, and are quasi-static. Transferring them to an ordnance
   forging at ε̇ ~ 10⁴ s⁻¹ is an assumption, unquantified by this source.
1. **Nothing on the US ordnance specs themselves.** Mott gives composition → γ
   but names no ordnance grade. The two compositions come from elsewhere, and
   they sit at **different confidence tiers**:
   - **WDSS 1, 0.14–0.20 % C — sourced.** *Ammunition Series 6* Table 6-1,
     `doc-reference/ww2-shells/ammunition-series-6-wdss-specs/ammunition-series-6-wdss-specs.md`: a
     direct, high-confidence transcription of the grade's chemistry of record.
   - **Baseline — grade *name* sourced, composition inferred.** The 105 mm M1
     bill of material (`doc-reference/ww2-shells/ordnance-105mm-m1-1940/card.md`,
     p. 16) reliably establishes the body steel as **WD-X1335, spec 57-107** —
     that name is the sourced part. Reading WD-X1335 *as* AISI 1335
     (**0.33–0.38 % C**, `doc-reference/azom-steel-grades/aisi-1335/aisi-1335.md`)
     is a separate, **unconfirmed name-similarity inference**: spec 57-107 is
     not digitised, the AISI 1335 card states it carries no WD-series linkage,
     and the project's own analysis
     (`doc-reference/ww2-shells/ammunition-series-6-steel-composition/ammunition-series-6-steel-composition.md`)
     rates this identity *"Low confidence — inferred, not confirmed"* and offers
     SAE 1040 as an equally plausible analog. Treat 0.33–0.38 % C as a working
     value, not a fact.

   It is still an improvement on the notebook's uncited "SAE 1045 (≈ 0.45 % C)"
   (`_governing-equations.qmd:79`), which had no citation at all. Gap **G2** is
   thereby closed **for WDSS-1**; on the baseline side only the grade name is
   established.
1. **Ductility is not in the model.** Mott says ductility raises fragment size,
   and carbon reduces it (0.83 → 0.57 RA over the table). The
   implemented μ closure carries no ductility term, so a γ-only shift captures
   part, not all, of the composition effect. This must be a logged assumption.

**Defect found while auditing (small, documentation-level, for the derivation
pass to settle):** `src/arty/fragmentation.py:34–35` comments that
`sigma_f / gamma` is "calibrated to M1 PAFRAG fragment-count data", while
`_governing-equations.qmd:78–81` documents γ = 65 as a **Mott-table
extrapolation** to 0.45 % C and σ_f = 800 MPa as a **literature range midpoint**
— not a fit. These cannot both be true. I believe the notebook is correct (γ = 65
is not reachable by fitting: any fitted value would move \(R\); it reads as a
bracket-anchored estimate sitting just below the corrected table's 0.45 % C row,
γ = 67 — see `derivation.md` C7).
The new entry must not be documented against a calibration that never happened.

## 4 · Options for the parameter pair, ranked

**A. γ-only transfer along Mott's carbon series; σ_f held at 800 MPa. — recommended.**
Interpolate the §3 table between the bracketing rows and keep the baseline's
dynamic flow stress. Uses only the legible, *dimensionless*, unit-ambiguity-free
column. Needs no new literature. Local-linear interpolation over the confirmed
0.14–0.20 % C band — which lies wholly inside the single 0.1–0.25 % C segment —
gives γ(0.14 %) ≈ 45, **γ(0.17 %) ≈ 47**, γ(0.20 %) ≈ 49, i.e. \(R = 17.0\) MPa
(band 16.3–17.8), \(\mu = 0.538\) g (+63 %), \(N_0 = 11\,201\) (−39 %),
\(N(>0.5\,\mathrm{g}) = 4\,269\). Both band endpoints are bracketed by measured
rows, so the estimate needs no external anchor (`derivation.md` §2/§4).
*Weakness (log it):* σ_f is not really composition-independent — Mott's stress
column rises with carbon, so σ_f and γ move together and **partially cancel in
\(R\)**. Option A therefore likely *overstates* the γ-channel grade difference.
It is directionally right and honest.

**B. Ratio transfer using both table columns from the same rows.**
\(R_{WDSS1} = R_{base} \times [(P_f/\gamma)_{0.17C} / (P_f/\gamma)_{0.355C}]\) —
the stress column's unit ambiguity cancels inside a ratio, which is elegant.
*Both original blockers are now gone:* the re-extracted table runs to 0.45 % C,
so the baseline's 0.355 % C is interior (no extrapolation), and the columns are
identified ($P_f$, $P_y$ in kg mm⁻²). What still blocks it is **physical, not
legibility**: those are quasi-static stresses and (1) needs a dynamic flow
stress, so a $P_f$-based ratio would import a quasi-static composition trend
into a dynamic quantity (`derivation.md` §3.1). Retained as the natural
successor if a dynamic composition→σ_F source arrives (gap G3), not G1.

**C. Absolute derivation of σ_f from a composition → dynamic-flow-stress
correlation** (e.g. Johnson–Cook / Cowper–Symonds parameters vs % C) with γ from
Mott. Gives genuinely per-composition physics, but needs new literature (G3) and
would move the *absolute* level of the whole steel family, putting the existing
`N(>0.5 g) ∈ [3000, 8000]` validation band at risk for no demo benefit. Reject
unless the parent explicitly wants absolute rather than relative grade physics.

**D. Calibrate to WDSS-1-specific fragmentation-trial data** (a period arena test
of a shell body made of that steel). Highest fidelity if it exists; realistically
unobtainable and disproportionate to a catalog entry. Reject.

## 5 · Recommendation for the derivation pass

1. **Adopt Option A.** Derive γ by local-linear interpolation of Mott §3 over
   the bracketing rows at the band midpoint 0.17 % C; carry the band endpoints
   (0.14/0.20 % C → γ ≈ 40/53) as the stated parameter uncertainty, not as
   separate entries.
1. **Hold `sigma_f = 800e6` and say why in the entry comment**, together with
   the identifiability statement from §2 (only \(R = \sigma_F/\gamma\) is
   observable; the split is a convention inherited from the baseline entry).
1. **Correct the baseline entry's provenance comment** (§3 defect) so the new
   entry is documented consistently — a comment edit, not a value change.
1. **Log the assumptions:** 1924 annealed lab bars → forged ordnance body;
   quasi-static γ used at ε̇ ~ 10⁴ s⁻¹; no ductility term in the μ closure;
   σ_f treated as composition-independent (understates cancellation in \(R\));
   **the baseline's now-cited 0.33–0.38 % C is not the carbon its catalogued
   γ = 65 corresponds to under the same interpolation rule** (that rule gives
   γ ≈ 60.4 at 0.355 % C; γ = 65 answers to ≈ 0.42 % C) — the two entries are on
   different rules, which bounds the contrast from **above** (`derivation.md`
   C7/A5).

### Literature gaps — name only, do not fill in this pass

Hand to @librarian **only** if the parent wants Option B/C or wants the spec
identity confirmed; Option A as recommended needs none of them.

- **G1** — clean scan of Mott 1947 (doi:10.1098/rspa.1947.0042), specifically the
  §3 table on p. 307–308: unambiguous column headers and units. Unblocks B.
- **G2 — CLOSED for WDSS-1's composition only**, by *Ammunition Series 6*
  Table 6-1 (WDSS 1, 0.14–0.20 % C). On the **baseline** side the 105 mm M1 BOM
  closes only the grade *name* (**WD-X1335**, spec 57-107); its composition
  remains open — reading it as AISI 1335 (0.33–0.38 % C) is a plausible but
  unconfirmed inference from grade-name similarity, not a primary-sourced fact
  (spec 57-107 is not digitised; the AISI 1335 card disclaims any WD-series
  linkage; the project's own analysis rates the identity low-confidence and
  offers SAE 1040 as an alternative). Also still open for **both** grades:
  **mechanical properties and heat treatment** — Table 6-1 is chemistry-only.
  Neither residue blocks Option A (see derivation A5/A8 and check C7: the
  shipped catalogued baseline γ = 65 already gives the **largest** defensible
  contrast, so the reported −38.5 % on N₀ is an **upper** bound — every
  candidate baseline analog sits *below* γ = 65 on WDSS-1's own interpolation
  rule (0.355 % C → γ ≈ 60.4; 0.40 % C → γ ≈ 63.5) and would only shrink the
  margin, to ≈ −31 %, never flip its sign or hide the effect); they matter if
  Option C is ever pursued.
- **G3** — (Option C only) composition → dynamic flow stress at ε̇ ~ 10⁴ s⁻¹ for
  plain-carbon steels; Johnson–Cook parameter compilations indexed by % C.

## 6 · Checks the derivation pass must run

- **Units:** μ must remain a mass — \((\mathrm{Pa})^{3/2}\,(\mathrm{m^3/kg})^{1/2}\,\mathrm{s^3} = \mathrm{kg}\).
  The pair enters as Pa / dimensionless, so the new entry cannot break this; state it, don't belabour it.
- **Identifiability (new test):** `SteelParams(sigma_f=k*σ, gamma=k*γ)` yields
  identical μ and N_0 for any k > 0. This pins the §2 claim in code.
- **Ordering:** μ(WDSS1) > μ(baseline) and N_0(WDSS1) < N_0(baseline) — lower
  carbon → lower γ → fewer, larger fragments (Mott p. 308).
  `tests/test_fragmentation.py:144` already covers the mechanism at γ = 53/67.
- **Existing band:** with M1 geometry the new grade must keep
  `N(>0.5 g) ∈ [3000, 8000]` (`test_fragmentation.py:141`). Computed: 4 269 at
  γ = 47, and 3 741 / 4 668 at the band endpoints — passes throughout, but the
  low end now has appreciably less margin than before.
- **Limits:** γ → ∞ ⇒ μ → 0, N_0 → ∞ (perfectly brittle); σ_f → 0 same. Sanity only.
- **Field level:** report the R50 shift for the new grade so the reviewer can
  confirm it is *visible but not dominant* relative to the μ change.

## 7 · Fidelity target

This aspect drives the per-grade half-mass μ and count N_0 — i.e. the
**magnitude, not the shape**, of the lethal-density and P(kill) fields. **±30 %
on N_0 (≈ ±20 % on σ_F/γ) is acceptable.** The demo outcome is that switching
steel grade moves the field by a visible and correctly-signed amount; WDSS-1's
absolute fragment count being right is not the bar.
