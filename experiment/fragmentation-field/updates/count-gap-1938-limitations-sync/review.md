# Review — `_limitations.qmd` L1 resync to count-gap-1938 re-closure (2026-08-09)

**Scope.** `git diff` of `experiment/fragmentation-field/_limitations.qmd`
against its last-committed state (`cf402a8`) is a single hunk (`git diff
--unified=1 | grep -c '^@@'` → 1), confined entirely to the L1 bullet under
"What remains open". Nothing else in the file changed. Reviewed the resynced
L1 text against `challenges/count-gap-1938/count-chain.md` §4 ("Verdict
framing after the 2026-08-08 re-closure"), `challenges/README.md`'s
`count-gap-1938` status-detail paragraph, and `rebaseline-verdict.md`'s
current (superseded-banner-carrying) text. `collect-findings.py --for
experiment/fragmentation-field/_limitations.qmd` returns 2 open findings, both
pre-existing and unrelated to L1 (belt half-angle δ>15° bound on L-something,
and a Cunniff-2014 secondhand-citation gap) — not touched by this diff, not
re-raised here.

**Not fully checked, by explicit scope instruction:** cross-references from
other rendered surfaces (`_validation.qmd`, app notebooks) into the old L1
framing were not swept — out of scope for this pass per the coordinator.

## Verdict: **PASS-with-limitations**

No Blocking findings. The resync is a faithful, non-inventive documentation
sync: every number in the new L1 paragraph traces verbatim to
`count-chain.md` §4's "Verdict framing" note —

- `N/779` = 1.73 (126 J) / 2.00 (78.6 J), `N/700` = 1.92 / 2.23 — matches
    `count-chain.md` lines 337–339 exactly, and matches `challenges/README.md`
    lines 56–57 and the `rebaseline-verdict.md` banner exactly (cross-checked
    by the prior `review-recloser.md` re-review, "RESOLVED", which independently
    re-ran the retained scripts against these same figures).
- "3.2–3.7× at a fitted threshold" — matches `count-chain.md` line 16 (top
    banner) and line 346 (Verdict framing) exactly.
- The historical "~4–6×" and "1.2–2.7×" figures are explicitly marked stale
    ("Both headline numbers are now stale") rather than restated as current —
    correct framing, matches the withdrawal history in `rebaseline-verdict.md`.
- "the falloff-ratio arm ... is still tied to the fitted $E_{thr}$" and "C1
    ... remains the gating item, now as confirmation of a provisional PASS
    rather than a rescue of a FAIL" — matches `count-chain.md` lines 340–356
    and `challenges/README.md` lines 57–63 in substance and in the specific
    wording used.
- No new computation, no new parameter value, and no physics appears anywhere
    in the diff — this is a pure re-statement of an already-adjudicated verdict,
    as the task described.

**Marker deletion.** No blocking finding marker was ever present in
`_limitations.qmd` itself (`git log --all -p` on the file has zero hits for
the pattern) — the blocking marker this task's background refers to lived in
`count-chain.md` and was deleted in the prior, already-committed and
already-reviewed commit `5bb16cc` (see
`challenges/count-gap-1938/review-recloser.md`, verdict RESOLVED on
re-review). `collect-findings.py` confirms zero open blocking findings remain
anywhere under `count-gap-1938/`. The deletion pre-dates this diff and was
warranted per that prior review; nothing about it is reopened by this pass.

## Findings

**[Deferrable] "essentially all of it the threshold fit" (L1, current text
lines 145–146) is a verbatim quote of `count-chain.md`'s own "Verdict
framing" note (line 346), but is in tension with the same source document's
own top-of-file banner (`count-chain.md` lines 4–12), which decomposes the
same 3.2–3.7× fitted-threshold total as a threshold-fit artefact (~1.65–2.05×)
*multiplied by* a genuine, non-threshold fragment-spectrum residual
(~1.7–2.0× — numerically the same as the sourced-threshold value 1.7–2.2× the
paragraph itself states two sentences earlier). Those two components are
comparable in magnitude, so "essentially all" overstates the threshold-fit's
share and understates the still-standing, sourced-threshold residual (up to
~2.2×, i.e. at the PASS/FAIL boundary) that the same L1 paragraph already
discloses numerically. This is not a new claim invented by the resync — it
reproduces its cited source's own wording exactly — but it propagates an
internal inconsistency in `count-chain.md` (introduced in the already-reviewed
`5bb16cc` pass, not this diff) into a second, more visible surface.
**Impact:** narrative-only; the correct sourced-threshold figures (1.73–2.23)
are printed in the same sentence, so a reader who does the division is not
misled, and no computed/rendered physics quantity changes. Recommend either
(a) tightening the phrase in `_limitations.qmd` to something like "roughly
half the log-excess is threshold-fit, with a comparable genuine residual
(~1.7–2.2×) persisting even at a sourced threshold," or (b) fixing the root
inconsistency in `count-chain.md`'s Verdict-framing note against its own
banner. Log as a limitation if not fixed; does not block this pass.

**[Deferrable] `updates/mach-dependent-fragment-drag/derivation.md` §7's own
L1 text (lines 275–299, "~3–4×", $E_{thr}$≈3–6 J, 2.8–4.1×) was not resynced
and has no forward-pointer to the newer count-gap-1938 re-closure.**
`_limitations.qmd`'s "What remains open" intro (line 126–128, unchanged by
this diff) frames the whole L1–L3 list as "carried from that update's own
limitations (`derivation.md` §7), not re-opened here" — true for L2/L3, but
L1 has now been substantially rewritten with numbers and a conclusion
("count arm now met-or-marginal") that do not appear in `derivation.md` §7 at
all. A reader who follows that specific pointer finds an older, compound-only
framing with no mention of the sourced-threshold PASS-band finding.
**Impact:** documentation-consistency only, no rendered chart or physics
output changes; the numeric ranges themselves are not grossly contradictory
(2.8–4.1× vs 3.2–3.7×), only the overall verdict framing has moved on one side
and not the other. Recommend a short "see the newer count-gap-1938 re-closure"
pointer added to `derivation.md` §7, or logging this as a known
cross-document staleness limitation.

**[Note]** The intro sentence "carried from that update's own limitations
..., not re-opened here" (line 126–128, unchanged) is technically inaccurate
for L1 specifically, since L1 was in fact substantially reworked relative to
its `derivation.md` §7 source. No action required — L1's own body text
already makes clear it is citing `count-chain.md` §4, not `derivation.md` §7,
so no reader is actually misdirected; flagged only for wording precision.

## What should go in `_limitations.qmd` (or a sibling limitations note) if the
deferrable items above are logged rather than fixed

- A one-line caveat that the "essentially all ... threshold fit" framing
    in L1 should be read alongside the sourced-threshold figures in the same
    sentence, since the two are in tension with `count-chain.md`'s own
    decomposition.
- A pointer from `mach-dependent-fragment-drag/derivation.md` §7 to
    `challenges/count-gap-1938/count-chain.md` §4 for the current L1 verdict.

## Suggested corrections (not applied)

1. Reword the "essentially all of it the threshold fit" clause in
     `_limitations.qmd` L1, or fix the underlying tension in `count-chain.md`'s
     Verdict-framing note against its own top banner.
1. Add a forward-pointer in `mach-dependent-fragment-drag/derivation.md` §7 to
     the count-gap-1938 re-closure.
