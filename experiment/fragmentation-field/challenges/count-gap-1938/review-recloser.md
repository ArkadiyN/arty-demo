# Review — count-gap-1938 re-closure against post-6c1faff shipped code (2026-08-08)

Scope: the @modeler pass that re-closed `count-chain.md` and
`rebaseline-verdict.md` against current shipped `fragmentation.py` (post
`6c1faff` / `50b734e`) and deleted the blocking-tier desync finding marker.
Reviewed via `git diff` of both files against their pre-pass state, plus
independent re-run of both retained scripts.

## Verdict: **FAIL**

One Blocking finding: the re-closure is incomplete. `count-chain.md` was
fully and correctly re-closed; `rebaseline-verdict.md` received only a
prepended banner — its own "Overall status" (§2) and "Restatement for
`challenges/README.md`" (§3) sections, and `challenges/README.md` itself,
were left stating the pre-`6c1faff` verdict framing, which `count-chain.md`'s
own new text explicitly says is superseded. Deleting the blocking-tier desync
finding marker asserted the desync was resolved; it was resolved in one of the two
named documents and not in the other, and not in the index page both
documents feed.

## Numeric verification (all sound)

Re-ran both retained scripts independently:

- `checks/count-chain-decomposition.py` → `M_case=4980.0 g, V0=864.4 m/s,   mu=0.826 g, N0=3016`, and every row of the §2 table (`E_thr` = 1.9/3.6/
    78.6/126/294.5 J → `N` = 2577/2478/1560/1346/934, `N/700` and `N/779` to
    two decimals) reproduces `count-chain.md`'s table and prose exactly,
    including the `f`-sweep in §3 C2 and the fixed-mass cuts in §2's closing
    paragraph.
- `checks/count-chain-rebaseline.py` → blocks (A)-(F) reproduce
    `rebaseline-verdict.md`'s banner figures exactly: `M_case=4980.0 g,   V0=864.4 m/s, mu=0.826 g, N0=3016`; threshold-free (E) Tolch-basis ratios
    2.24/2.07/1.92/1.78 (screens 2/3/4/thru4) bound the banner's quoted
    "1.78-2.24x"; the fuze-excluded variant's thru4 ratio (2.03x) matches the
    banner's "moves ... from 1.78x to 2.03x" claim exactly.
- `sigma_f=800e6` and `gamma'=54.5` in `src/arty/fragmentation.py` (lines 29,
    53\) confirm both parameter values `count-chain.md`'s §1 table now cites.
- Neither check script has an uncommitted diff or a new commit since
    `328e664`/`ff2961b` — both are unedited, as the task description states.
    Their own numbers were never wrong; only the documents citing them had
    gone stale.

No transcription, unit, or arithmetic defect found in any of the recomputed
figures. This is a clean, well-evidenced re-closure of `count-chain.md`
itself — the "Verdict framing" section added at the end of its §4 correctly
identifies and states the qualitative change: at a sourced `E_thr`, the count
arm of the PASS criterion moved from unambiguously-FAIL (2.2-2.5x pre-fix) to
met-or-marginal (1.7-2.2x post-fix), while the A→D falloff-ratio arm remains
unmet and compound. That is exactly the kind of change-of-direction this
project's materiality bar calls out explicitly, and `count-chain.md` states it
plainly, with the "not of any new argument in this thread" caveat correctly
attributing the change to the underlying `6c1faff`/`50b734e` commits rather
than to new reasoning here.

## Blocking finding

**`rebaseline-verdict.md` §2 "Overall status" and §3 "Restatement for
`challenges/README.md`", and `challenges/README.md` itself, were not updated
to reflect the verdict-direction change that `count-chain.md`'s own new
"Verdict framing" section (lines 334-357) states explicitly.**

- `rebaseline-verdict.md` line 160: *"The thread survives the re-baseline:
    **no verdict flips**, ... The thread's headline — C1 ... — **stands
    unchanged**."* This is now literally contradicted by `count-chain.md`
    line 128-130: *"That is a **change of verdict direction** relative to the
    pre-6c1faff numbers (2.2–2.5×, unambiguously outside)"* and lines 346-348:
    *"The thread's original FAIL-leaning framing (...) is **not supported**
    by the current numbers."*
- `rebaseline-verdict.md`'s banner (added by this pass, lines 8-38) names
    three verdicts that move (§2 Fact 2, §4 FAIL-status, §3 C4) but does not
    flag that §2 "Overall status" and §3 "Restatement" — both further down in
    the *same file*, both written in the past tense as if final — restate the
    now-superseded framing without qualification.
- `challenges/README.md` (lines 48-59, `count-gap-1938` status detail) was
    **not touched by this pass at all** (`git log` shows its last commit is
    `a01eb33`, the *pre*-`6c1faff` rebaseline). It states *"the scoping
    verdict survives... **No PASS/FAIL row changes side**"* — directly false
    against the current shipped numbers, which move the 78.6 J and 126 J rows
    from outside the 2x PASS band to at-or-inside it (`count-chain.md` lines
    126-131, 337-341). The banner in `rebaseline-verdict.md` itself claims (its
    own line 38) *"The §3 restatement below has been applied to
    `challenges/README.md`"* — that claim is now false a second time: the §3
    restatement it points to is itself stale, and README was never touched.

**Impact.** A reader or a future dispatch that opens `README.md` (the
project's own navigation entry point for this challenge thread) or skims only
`rebaseline-verdict.md`'s "Overall status" would conclude the thread is
still FAIL-leaning at the 1.7-2.3x band and that "proceed to C2" is still the
live recommendation — precisely the recommendation `count-chain.md`'s own new
text says is no longer supported and could cause *over-correction*
(`count-chain.md` lines 228-233: "an aggressive `f` now risks
over-correcting"). That is a concrete risk of a future pass implementing an
unnecessary/harmful C2 change on the strength of a stale headline in a
sibling document from the same commit. This is exactly the shape of defect
`deferred-findings.md` singles out — a known desync fixed in appearance
(marker deleted) but not in substance in every place it was published.

**Suggested correction (not applied):** add a one-line pointer at the top of
`rebaseline-verdict.md` §2 and §3 to `count-chain.md`'s "Verdict framing"
note (or inline the same three bullets there), and push a matching update to
`challenges/README.md`'s `count-gap-1938` status-detail paragraph — at
minimum striking "No PASS/FAIL row changes side" and replacing it with the
met-or-marginal framing, and updating the Threads-table one-line summary if
it is meant to track verdict direction.

## Notes (no action required)

- `count-chain.md` line 227-229: *"C2 at f≲0.8 would now push the 126 J row
    below unity"* — checking the printed sweep table, the 126 J row's `N/700`
    is still 1.26 (>1) at `f=0.8` and only drops to 0.98 at `f=0.7`; the
    crossing is closer to `f≈0.72-0.77` than `f≲0.8`. This is an imprecise
    paraphrase of a table that is itself correct and printed two lines above
    it — it does not change the qualitative "over-correction risk at low f"
    conclusion, and a reader can verify the real crossing point directly from
    the adjacent table. Note only.
- The three pre-existing deferred findings from `collect-findings.py` (D vs
    E criterion mismatch, the fuze-excluded-variant numerator/denominator
    inconsistency, and the side-spray perf(D)/perf(A) note) are all still
    present verbatim in `experiment/fragmentation-field/challenges/   source-data-audit/review-criterion-match.md` and
    `review-void-rulings.md`, correctly untouched by this pass (they are
    about a different, still-open methodological question, not the
    shipped-code desync this pass targeted). `count-chain.md`'s C4 paragraph
    (lines 258-276) explicitly references the still-open fuze-excluded-variant
    finding by name rather than silently resolving or re-closing it — correct
    handling of a finding outside this pass's scope.

______________________________________________________________________

## Re-review (2026-08-08) — scoped to the Blocking finding above

Scope, per dispatch brief: verify whether the Blocking finding (desync
between `rebaseline-verdict.md` §2/§3, `challenges/README.md`, and
`count-chain.md`) is now resolved. Read via `git diff` of the (still
uncommitted) working tree against `a01eb33`, which contains both the pass
this file's original review scored and a further @modeler pass that touched
`rebaseline-verdict.md`, `challenges/README.md`, and (on its own initiative)
`source-data-audit/ledger.md`.

### Verdict: **RESOLVED**

All three named surfaces now state the same post-6c1faff/50b734e framing,
with consistent numbers throughout:

- **`rebaseline-verdict.md` §2 "Overall status"** now carries an inline
    `> **Superseded in part (2026-08-08, post-6c1faff).**` block immediately
    above the original paragraph, stating plainly that "no verdict flips …
    stands unchanged" no longer holds for the thread as a whole, and pointing
    to `count-chain.md` §4's verdict-framing note as the live statement.
- **`rebaseline-verdict.md` §3 "Restatement for `challenges/README.md`"**
    likewise now carries a `> **Superseded (2026-08-08, post-6c1faff).**`
    block stating that `challenges/README.md` is the live text, and that the
    block below it (the original restatement) is retained only as a record of
    what the Tolch-series re-baseline alone concluded — "do not re-apply it."
- **`challenges/README.md`** (`git log` previously showed its last touch at
    `a01eb33`, pre-`6c1faff` — this pass finally edited it) now reads, in the
    Threads table, "Re-baselined, then re-closed post-6c1faff — count arm now
    met-or-marginal; one inference void", linking to `count-chain.md` §4
    rather than the stale `rebaseline-verdict.md`. Its status-detail paragraph
    was rewritten into a two-step "(1) re-baseline … (2) re-closed against
    shipped code" narrative that states the same $N/779$/$N/700$ figures as
    `count-chain.md` §4 and the `rebaseline-verdict.md` banner
    (1.73/1.92 at 126 J, 2.00/2.23 at 78.6 J; threshold-free 1.78–2.24×), no
    longer asserts "No PASS/FAIL row changes side", and updates the C4
    framing to match `count-chain.md` §4 C(ii) (975 g sourced deduction,
    1.78×→2.03× on dropping the coarsest screen, criterion-match rather than
    magnitude as the live question).
- **The self-referential false claim** flagged in the original finding —
    `rebaseline-verdict.md`'s banner asserting (its own then-line 38) that the
    §3 restatement "has been applied to `challenges/README.md`" when it had
    not — is now corrected in place: the banner explicitly says "the earlier
    claim in this banner that the §3 text had already been applied to README
    was wrong, README then still carried the pre-6c1faff wording," rather than
    silently overwriting the false claim.

Cross-file number check (all consistent, hand-verified against the diffs,
not re-run through the scripts since no arithmetic changed from the state the
original review already independently re-derived): $N/779$ = 1.73 (126 J) /
2.00 (78.6 J) and $N/700$ = 1.92 / 2.23 appear identically in `count-chain.md`
lines 337-338, the `rebaseline-verdict.md` banner, and `README.md`'s
status-detail paragraph. The threshold-free Tolch-basis band (1.78–2.24×) and
the C4 screen-drop figure (1.78×→2.03×, not 1.19×) likewise match across all
three surfaces. `uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938` now returns zero
`blocking` entries (3 open: 2 deferrable, 1 note — the pre-existing,
out-of-scope ones already noted above), consistent with `OPEN-FINDINGS.md`'s
diff dropping from 4 to 3 blocking. `count-chain.md` line 348 also now reads
"$f\approx0.7$–0.77" in place of the imprecise "f≲0.8" this review's own
Note flagged — opportunistically fixed, not scored against the Blocking item.

**No new issues found in the re-reviewed scope.** The
`source-data-audit/ledger.md` addition (a forward-pointer note on the
historical `count-gap-1938` entry, explicitly out of the dispatch's named
scope) is accurate and non-contradictory with the rest; it does not affect
this verdict either way.
