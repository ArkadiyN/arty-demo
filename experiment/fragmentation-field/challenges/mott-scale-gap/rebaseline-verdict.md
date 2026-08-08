# Rebaseline verdict: `mott-scale-gap` challenge thread

Judgment pass. Re-reads this thread's three working notes
(`_params_provenance_note.md`, `_scale_verdict_ledger.md`,
`_shape_closure_check.md`) against the Phase-3 γ′ rebaseline recorded in
`experiment/fragmentation-field/updates/mott-fragment-shape-closure/rebaseline-verdict.md`.
No `src/arty/` reads, no re-derivation, no scripts run. Assessment only —
nothing outside this file is changed.

Rebaseline inputs taken as given: Mott 1947 p.308's γ column closes on 3 of its
4 rows under `s_F = RA/(1−RA)`; the non-closure localises to the 0.45 %C row,
which is independently indicted; **γ′ = 47 is sound, γ′ = 65 is shifted**
(it anchors on that one failing row), with the grade *ordering* surviving
either reading; the shape closure's own content is γ′-independent and sound;
and Mott & Linfoot (A.C. 3348) twice disclaims having a theory of fragment
*length*.

## 1. Ledger localisation (γ/σ_f excluded, mass closure indicted) — **sound**

The ledger's §1 exclusion argument does not rest on γ = 65 being the right
value; it rests on the *width of the admissible γ box*. It states that the
whole admissible σ_f × γ range moves μ by only ≈1.5–2×, against a 4–15× gap.
The rebaseline's move, γ′ 65 → 47, is exactly such a move: μ ∝ γ^{−3/2}, so
(65/47)^{3/2} = **1.63×**, sitting inside the bound the ledger already priced.
So the conclusion survives its own justification being replaced — the ledger
justified γ = 65 by reading Mott's 0.45 %C row (§1, "γ = 65 is on the correct
table row"), and that row is precisely the one the rebaseline indicts; but the
bracket-wide closure argument never used the row. Quantitatively the
localisation **re-sizes and does not move**: at γ′ = 47, μ goes 0.235 → 0.382 g
and N₀ 12 256 → ≈7 540, so the residual gap against Tolch (μ 0.95–3.5 g,
N₀ 1 000–3 200) narrows from 4–15× to **≈2.5–9×**, and the shape factor needed
to close it drops from α ≈ 4 to **α ≈ 2.5**. That residual is still far outside
anything γ or σ_f can reach, and the ledger's strongest evidence — the
*screening-immune* heavy-fragment deficit (N(>6 g) = 78 model vs 278 observed,
100× short above 34 g) — is untouched by any γ move, since a γ change is a pure
rescale of μ and cannot remove a crossover. σ_f = 800 MPa likewise stands on
Mott's own worked example (p.306, "flow stress in the work-hardened state of
50 tons/sq.in." = 772 MPa), which the rebaseline does not touch. One residual
the rebaseline does *not* repair and the ledger itself flags (§2, "No single μ
fits all four points and the mass budget"): the observed spectrum is steeper at
the fine end than Mott, so even a correctly-closed α leaves a
distribution-*shape* residual, not merely a scale one. Classification: **sound**
(localisation intact), with the magnitudes above superseding the ledger's §3
table.

## 2. Shape-closure verdict NO — **survives, and is strengthened**

(The verdict under review: the cube closure is the model author's
simplification, not the cited literature's.)

Its load-bearing claim is read directly off Gold 2017's own equations, not off
any γ value: eq. (4) closes x₀ into a mass as μ = ½·α·ρ·x₀³ with
α = (l₀/x₀)(t₀/x₀), and eq. (6) then *absorbs* α by defining γ ≡ α^{−2/3} γ′.
Taking the shape-absorbed eq. (16) while supplying γ′ from a composition table
therefore asserts α = 1 — a cube — which neither source states. Rebaseline
item 4 confirms this content is γ′-independent, so shifting γ′ 65 → 47 changes
what α must be worth (≈2.5, per §1) but not *that* an unstated α = 1 was
imposed. Rebaseline item 5 sharpens rather than undermines it: the note's §3
carries a "further 1.5× per linear dimension" from Mott 1947 p.305's average
length ≈ 1.5 x₀, and A.C. 3348's double disclaimer ("we have not been able to
find a theory to account for the average length of the splinters"; the theory
"does not account for the length of splinters … but only for their breadth")
means that length dimension is **empirical only** — there is no theory of l₀ in
the literature at all. That is exactly why Gold calibrates γ (Fig. 7, against
explosive CJ pressure) instead of predicting it, and it converts the note's §5
caution into a requirement: α is a free parameter to be fixed against data,
never read off a composition table. Two qualifications. (a) The note's §1 frames
the defect as symbol confusion (γ vs γ′); after the rebaseline that is now the
*second* of two independent defects, the first being that γ′ = 65 reads a row
that fails the source's own closure — both are real, and the note should not be
read as having covered the row problem. (b) The note's §3 sub-claim that "Mott
never converts x₀ to a mass in this paper" is a claim about the 1947 paper only;
whether A.C. 3348 does so **cannot be ruled from these three files** and was not
attempted here.

## 3. `challenges/README.md` status "Resolved" — **wrong word; replace**

The thread's own artifacts carry live open items, independently of the
rebaseline: `_shape_closure_check.md` §5 has an explicit "Open, for the
derivation pass" (predicted x₀ ≈ 3.9 mm is ~3× below Tolch's recovered breadth,
which α cannot absorb) and instructs that α ≈ 4 not be treated as calibrated;
`_scale_verdict_ledger.md` §4 leaves item 2 (break-up velocity ≠ terminal
Gurney V₀) unquantified and item 3 (Mott's engineering closed form, constant B)
blocked on @librarian, since B is not in the digitized copy. A thread that
diagnoses a defect and hands its correction to a later pass is not resolved; it
is diagnosed. Replacement wording proposed by this pass — **superseded by the
paragraph below it**, which resolves the conditional the pass could not:

> **Diagnosed — correction open.** Scale gap confirmed real and localised to
> the cube mass closure (α = 1 imposed where Gold 2017 eq. (4) requires
> α = (l₀/x₀)(t₀/x₀)); γ/σ_f excluded as cause. Magnitudes superseded by the
> γ′ = 47 rebaseline — see
> `challenges/mott-scale-gap/rebaseline-verdict.md` and
> `updates/mott-fragment-shape-closure/rebaseline-verdict.md`.

**Resolved by the main agent, 2026-08-03.** The pass could not rule whether the
α / shape correction had landed in shipped code, and made the status word
conditional on it. It has: `src/arty/fragmentation.py:320-323` computes
`alpha = shell.aspect_ratio * shell.breadth_factor**2 * t_bu / x0` and applies
`gamma = alpha**(-2/3) * shell.steel.gamma`, i.e. Gold 2017 eq. (6) with α
carried rather than set to 1. So the "fix landed" branch of this section is the
live one, and `challenges/README.md` has been restated as **"Fix landed —
revalidation open"** with the §5 x₀-vs-breadth and break-up-velocity items named
as what is still open. The blocking finding this section raised is closed by
that edit.

FINDING\[deferrable\]: the ledger's Tolch-comparison tables (§2, §3) cite mott_scale_check.py / mott_shape_closure.py, which were never committed and are permanently lost — those numbers are unauditable and unre-runnable, so any pass relying on them must regenerate the check under checks/ (affects: experiment/fragmentation-field/challenges/mott-scale-gap/\_scale_verdict_ledger.md, experiment/fragmentation-field/challenges/mott-scale-gap/\_shape_closure_check.md; since: 2026-08-03)
