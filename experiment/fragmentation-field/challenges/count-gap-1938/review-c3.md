# Review — C3 (single-exponential Mott form in the 0.166–0.63 g sub-gram tail)

**Reviewed:** `mott-tail-shape.md`, `checks/count-chain-mott-tail-shape.py`, the
C3 banner hunk in `count-chain.md`, and two new `modeler` memory entries.
**Verdict: PASS.**

## Findings register check

`uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938/` returns 4 open
findings, all `deferrable`/`note`, none `blocking`. All four affect
`count-chain-rebaseline.py` / `rebaseline-verdict.md` / `README.md` / the C5
region of `count-chain.md` — none touch `mott-tail-shape.md` or
`checks/count-chain-mott-tail-shape.py`, and none required action from this
pass. No open finding was silently left untouched in this pass's own scope.

## Reproduction

Ran `uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-mott-tail-shape.py`
directly (0.77 s, well under the ~30 s retention budget). Every number in
`mott-tail-shape.md`'s tables (§3, §4 — R=1.493/1.127/1.370/1.756/2.062/2.357/
3.320/4.761, credits 1.324×/1.090×/0.850×/0.724×/0.633×/0.450–0.314×, the (B2)
boundary-mass table 46.649/6.552/1.882/0.840 g and its Tolch/fit/shipped-Mott
count columns, the §5 standing-residual figures 2.25× and 1.51×) matches the
script's printed output to the quoted precision. §5's derived arithmetic
(2.25×/1.324× = 1.70×, 2.51×/1.324× = 1.89×, ln(1.324)/ln(2.25) ≈ 35%) checks
out by independent recomputation.

## Findings

**1. [Note] `N(≥0.166 g)` quoted as 1756 in prose (line 25) vs. the script's
own printed 1757.** The unrounded value is 1756.50 (verified:
`mott_N([0.166e-3], N0, mu)[0] = 1756.5006`); the script's `:7.0f` format
rounds up to 1757, while the prose (and `count-chain.md`'s own pre-existing
verdict-row convention at line 203, "N = 1756") rounds down. `R_shipped = 1.493` is consistent with 1756/1176, not 1757/1176 (1.4940 vs 1.4930 —
distinguishable at 3 d.p.). Pre-existing convention, not introduced by this
pass; impact on any cited ratio is \<0.1%, changes no conclusion. No action
needed beyond noting it if the script's print format is ever touched.

**2. [Note] Table invariant and consumer check.** `pit-screen-recovery.csv`'s
`.invariant` passes (`uv run src/utils/check-table-invariants.py doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/pit-screen-recovery.invariant`
→ "ok", 0/1 failed). The check script reads the table via `csv.DictReader`
from the real CSV, not a hand-typed array — satisfies
`source-data-fidelity.md`. `cum_n`/`cum_w`/bucket-mean figures reproduce
existing project figures cited elsewhere in `count-chain.md` (e.g. the 0.61 g
finest-bucket mean, the 1.51×/779 floor) — cross-document consistency
confirmed, same underlying table and same 0.63 g convention used throughout.

**3. [Note, provenance verified] The Elek & Jaramaz quotes are faithful to the
primary.** Checked directly against
`doc-reference/mott-distribution-small-fragments/elek-jaramaz-2009/elek-jaramaz-2009-warhead-distribution.md`:
the "Mott had argued that in three-dimensional fragmentation..." quote (line
60 area) and "cannot successfully describe the HE projectile fragmentation"
(line 101) both match verbatim, and Grady = generalised-Mott at λ=1 is
confirmed at line 83. This satisfies the provenance gate directly rather than
by citation-through-citation — no secondhand-attribution risk found.

**4. [Note] Methodological honesty on the degenerate fit (B).** The
boundary-free locus fit is correctly flagged VOID and excluded from credit —
verified independently: the (number-fraction, mass-fraction) locus for the
generalised-Mott family is a legitimate scale-invariant identity (derivable
from the incomplete-gamma tail-mass relation), so fitting only that locus
cannot pin the mass scale μ. The script's own printed implied boundary masses
(87 kg / 4.6 kg / 1.46 kg / 0.93 g against bucket means 154 g…0.61 g) make the
degeneracy self-evident. The write-up does not use this fit for any credited
number — good practice, matches the new memory entry
`gotcha_count_mass_locus_not_identifying.md`.

**5. [Note] (B2) is a 3-parameter fit to 4 anchored points (1 residual DOF) —
near-exact reproduction of the fitted rows is expected regardless of whether
the generalised-Mott family is the right shape; the real validating evidence
is the three *held-out* closures (mean mass 6.71 g vs 7.40 g, 9%; total metal
5632 g vs 5764 g, 2%; N(≥0.166 g) 784 vs 779, 0.6%).** These are correctly
described as "not used in the fit," though they are deterministic functions
of the same fitted triple applied to different statistics, so they are
partially rather than fully independent checks. This is an inherent
data-scarcity limitation (Tolch publishes only 5 screen buckets), already
implicitly acknowledged by the write-up's "it is a *fitted* exponent, not a
*derived* one" framing in §5(iii) and its explicit refusal to ship a
`src/arty/` change on this basis. No stronger validation is available from
this census; not blocking, no different outcome achievable with more rigor
here given the data.

**6. [Note] Power-law splice arithmetic (block D) verified by hand.** The
density-matching condition `dens = n_sp/(2·√(m_splice·μ))` is exactly
`n(m_splice) = N(m_splice)/(2√(μm))`, the correct derivative of the shipped
λ=1/2 Mott form at the splice point, and the analytic integral of the spliced
power-law tail matches the script's closed form term-by-term. Confirmed
dimensionally consistent (count/kg density × kg = count).

## Criterion match / comparison protocol

The C3 credit compares the shipped Mott shape and every alternative (B2,
λ=1/3, power-law) against the *same* quantity R = N(≥0.166 g)/N(≥0.63 g), an
extrapolation ratio explicitly chosen (§1) to be independent of N₀ and
M_case — correctly isolating C3's question from C4's. All rows in §4's table
are computed on the same 4-boundary Tolch anchor set (m_bnd), so the
comparison across λ values is apples-to-apples: no candidate is evaluated at a
derived parameter set while a rival gets to fit the scoring data — here *all*
candidates including the shipped one are evaluated at the same anchored
masses in the fixed-λ comparison (script block after B2). The one candidate
that *is* fitted to Tolch's own census (B2, λ=0.759) is explicitly and
correctly disclosed as unsourced and non-actionable in §5(iii) rather than
being shipped or credited as a validated correction — this is the right
disposition given the standing project incident on rebaselining onto the
validation source (`gotcha_rebaseline_onto_validation_source.md`,
cross-referenced correctly).

## Layering / src/app check

`git diff --stat -- src/ app/` and `git status --porcelain -- src/ app/` both
empty — confirmed no `src/arty/` or `app/` changes, consistent with this being
a Workflow-A assessment pass with an explicit "no src/arty/ change" verdict.

## Memory entries

Both new `modeler` entries (`gotcha_count_mass_locus_not_identifying.md`,
`gotcha_powerlaw_tail_sign_wrong_for_shells.md`) are within the 30-line cap,
state a durable counter-intuitive gotcha (not a status log), and are correctly
indexed in `MEMORY.md` with one-line hooks. No issue.

## Verdict

**PASS.** No Blocking findings. All findings above are Note-tier
(pre-existing rounding convention carried forward, or acknowledged/flagged
methodological caveats that the write-up itself already discloses) — none
change the C3 credit (1.324×), the restated residual (2.25×→1.70×/779,
2.51×→1.89×/700), or the "not sourced, no src/ change" disposition. The
write-up's own honesty about (B)'s degeneracy, (B2)'s fitted-not-derived
status, and the sign-trap resolution against (not with) the librarian's
`index.md` headline is a genuine strength of this pass, not merely a
disclosure formality — each of those claims was independently verified above
rather than taken on faith.

No corrections suggested; nothing to log as a new limitation beyond what §5
already states.
