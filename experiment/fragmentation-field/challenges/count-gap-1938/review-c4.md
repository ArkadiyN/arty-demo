# Review: C4 (mass-bookkeeping/spectrum-denominator) closure — count-gap-1938

**Verdict: PASS-with-limitations.** The physics/comparison content (criterion
match, reproduced numbers, ill-conditioning caveat, citations) is sound and
fully reproduces — no Blocking physics/output finding. One finding (#1) is a
false completeness claim in the committed banner text (README.md was not
actually synced despite the banner saying it was); it changes no physics
number and so does not meet this project's Blocking bar (no rendered/physics
output changes), but it should be fixed — either sync README.md or strike the
false sentence — before this change is considered closed, since it leaves the
thread's own navigation surface stale and misleading for future triage.

## Open findings register (context)

- `[deferrable]` headline 1.221x/2.05x C5 figures rest on inadmissible 0.36g/838m/s datum — affects count-chain.md, rebaseline-verdict.md, README.md. Not in this pass's scope (C4, not C5); spectrum-mass-basis.md does not touch the C5 figures.
- `[note]` C1 plug-shear threshold rescale — not in scope for C4.

## Disposition of Finding 1

Addressed immediately, not deferred: `README.md`'s `count-gap-1938` row and
its status-detail section (item (7)) were updated in the same pass that
folded this review's findings back in, so `rebaseline-verdict.md`'s banner
claim is now true rather than struck. No open-finding marker was needed.

## Reproduction

Both scripts run standalone under 30s (`uv run python checks/count-chain-spectrum-basis.py`, `uv run python checks/count-chain-rebaseline.py`) and their printed numbers match the
write-up exactly:

- §1 table (10.94 lb / 13.29 lb / 12.50 lb): script (A) prints identical
    figures, plus the closure `10.94 + 2.35 = 13.29 → OK`.
- §2's "M_case vs Tolch 10.94 lb: +0.4%": script (B) prints `+0.4 %` exactly.
- §3's fuze-excluded band 1.81–1.93× (screens 2/3/4/thru4): script (C) and
    `count-chain-rebaseline.py`'s new "fuze-excluded variant: CRITERION-MATCHED"
    block both print 1.89/1.93/1.88/1.81× — matches.
- §3's f-sensitivity table (rows f=0.70, 0.846, 0.90, 0.95, 1.00): script (F)
    reproduces every cell to 2 decimal places, including the f=0.70
    φ≥1-degenerate flag and the screen-2 well-conditioned band "1.89x - 2.10x".
- §5's residual table: `count-chain-rebaseline.py` block (F) reproduces
    0.166 g → N/779=2.25×, N/700=2.51×, and 0.630 g → N/779=1.51×, N/700=1.68×
    exactly as quoted.

## Source citations (tolch-1938.md)

- `tolch-1938.md:232` — "Wt. loaded unfuzed shell" row carries 12.50 / 2.35 /
    1.56 / 13.29 for round 1, matching §1's table. Confirmed by grep.
- `tolch-1938.md:329` — "These fragments are mostly pieces of fuze." confirmed
    verbatim by grep, in the sentence describing screen-1 recovery (6 pieces,
    ~15% of shell weight). Matches the write-up's quote and its citation
    (screen 1 count/weight against this sentence).
- `tables/round-weights.invariant` passes
    (`uv run src/utils/check-table-invariants.py … round-weights.invariant` →
    `ok`, 4 rows). The closure `loaded_unfuzed − tnt + fuze == empty_and_fuze`
    is the source's own stated relation and the 10.94 lb figure is arithmetic
    on it, not a fabricated number (this table/invariant predates this pass —
    committed under the `shell-case-mass-basis` update — and was not
    re-authored here, but it backs the §1 numbers cited).

## Criterion-match soundness

The fuze-excluded pairing (case-metal census minus screen 1, vs
`M_case` = 4980 g) is the correct criterion match: `mott_params` builds its
spectrum from `mass_shell = mass_total − mass_filler − mass_deductions`
(`src/arty/shells.py`), i.e. explicitly fuze/booster-excluded case metal, and
Tolch's own text identifies screen 1 as fuze pieces. Pairing a fuze-excluded
model quantity against a fuze-included census (the "mixed" row) drives
φ = 1.16 > 1, which is a correct and decisive tell of a basis mix — verified
independently in script (E)'s printed `phi = 1.1575`. The alternative
fuze-inclusive-consistent pairing (13.29 lb, full census) is also internally
consistent and is reported for contrast (1.58–1.99×), and both bracket the
same FAIL conclusion. This is sound; **no criterion-match defect found.**

The ill-conditioning caveat (finest cut sits at φ→1, where dx/dφ diverges) is
independently confirmed: differentiating the Mott survivor function
φ(x) = (x²+2x+2)e⁻ˣ/2 gives dφ/dx = −(x²/2)e⁻ˣ, which is 0 at x=0 (φ=1) —
so dx/dφ genuinely diverges there. The caveat is not glossed over: it is
stated in §3, carried into §4/§5's "not a point estimate" framing, and
repeated in the `rebaseline-verdict.md` banner text. Good.

## Findings

### Finding 1 — Material but deferrable (false completeness claim; zero physics/output impact, but must be actioned)

`rebaseline-verdict.md`'s new banner states: *"`challenges/README.md` was
restated to match on 2026-08-15."* This is false: `git status --porcelain`
shows `experiment/fragmentation-field/challenges/README.md` is **not** in the
diff (no `M`, no `??`) — it was last touched by the prior C3 commit
(`dc330aa`) and still reads *"C3 restates it to 1.70×/1.89× but is unsourced
so no PASS follows; C4 is what remains"* (README.md:20) and repeats "C4 is
what remains" in the status-detail section (README.md:144). Both are now
stale: this pass's own conclusion is that C4 is discharged and **no
sub-candidate remains** (count arm final FAIL). Every prior closure in this
thread (C1+C2, C5, C3) synced README.md in the same commit — this is the
first one that claims the sync happened without doing it.

**Impact.** Not a physics/rendered-output change — README.md is a navigation/
triage surface, not `src/`/`app/`. But it is now actively misleading: a
future agent or human using README.md's per-thread table to decide what to
work on next would see "C4 is what remains" and could re-dispatch a modeler
onto an already-closed candidate, or fail to notice the thread's count arm is
now finally closed — the exact "deferred and forgotten" failure mode
`deferred-findings.md` exists to prevent, except here it's a false
"resolved" claim rather than a silent omission.

**Suggested correction.** Either (a) update README.md's `count-gap-1938` row
and its status-detail section to state C4 discharged / count arm finally
FAIL (matching the pattern of the three prior sync commits), or (b) if that
sync is intentionally deferred to a follow-up commit, strike the "was
restated to match on 2026-08-15" sentence from the banner — it must not
claim a completed action that didn't happen.

### Finding 2 — Note (internal wording imprecision, zero output impact)

§4(ii) of `spectrum-mass-basis.md` says the corrected band "1.8–2.1×… contains
it [the superseded 2.15× figure]." 2.15× is not actually inside [1.8, 2.1] —
it sits ~2.4% above the upper bound. The 2.15× figure was itself computed on
the *fuze-inclusive* 13.29 lb basis pre-`50b734e`; re-running that same
basis today (script section D) gives 1.59× at the finest cut, so the old
number is doubly superseded (basis changed, `M_case` changed) and isn't cited
anywhere in current artifacts. No output depends on this sentence being
precisely true — it's a disposition-footnote imprecision, not a citation or
computation used downstream. No action required beyond a wording fix if
convenient.

### Verified non-findings

- `src/` and `app/` are untouched (`git status --porcelain -- src/ app/`
    empty) — correctly a Workflow A assessment, no shipped-model change.
- `count-chain-rebaseline.py` diff is comment/label-only (22 insertions, no
    logic change) — the block-E computation itself is unmodified; only
    labeling of which rows are quotable changed. Verified line-by-line against
    `git diff`.
- Both deferrable-finding-marker deletions in `review-criterion-match.md:337`
    and `review-void-rulings.md:204` are earned: both findings' stated conditions
    (block D/E basis mismatch; the pre-`50b734e` 200 g placeholder producing a
    spurious "fuze-inclusive M_case" denominator) are confirmed resolved by
    reading the surrounding context (the `50b734e` mass_deductions fix,
    `updates/75mm-fuze-case-mass-fix/derivation.md`) and by reproduction above.
    Both markers were the *sole* content removed in their respective diffs (no
    other findings collaterally deleted).
- Mott survivor-function boundary behaviour (x=0→φ=1, x→∞→φ=0, monotone) and
    the M_case/N0 relation (N0 = M_case/2μ = 4980/1.858 = 2680.3 ≈ 2681) check
    out dimensionally and numerically.
- No open findings from `collect-findings.py --for count-gap-1938` fall
    inside this pass's scope (both remaining open items concern C5's
    0.36 g/838 m/s datum, untouched by this C4 pass).
