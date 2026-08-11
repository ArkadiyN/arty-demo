# Review — count-gap-1938 C1+C2 sync of `count-chain.md` (2026-08-10)

Scope: the @modeler pass that re-closed `count-chain.md` against the
currently-shipped combined C1 (`arty.perforation.perforation_threshold_energy`)

- C2 (`arty.fragmentation.breakup_velocity_fraction`) state. Reviewed via
    `git diff main -- .../count-gap-1938/count-chain.md` (380 ins / 252 del,
    the only file this pass touched), independent re-run of all three retained
    check scripts, `grep`/`Read` of the two cited `derivation.md` files, and
    `git log`/`git diff` on `challenges/README.md` and `rebaseline-verdict.md` to
    check cross-document consistency. This is a **different artifact** from
    `review-recloser.md` in this same folder (that file reviews the earlier
    2026-08-08 post-6c1faff pass) — not touched here, per instruction.

**Note on completeness:** I was told to stop verifying and write up before
exhausting every claim in the document. What follows is fully confirmed for
the items listed under "Verified" below (re-run scripts, cross-checked
against both cited `derivation.md` files, arithmetic spot-checks). I did
**not** independently re-derive the A→D falloff-ratio arm's "still compound"
claim, did not re-verify every sentence of the "What earlier passes got
wrong" retrospective in §3, and did not re-check the `mott-fragment-shape-closure`
citation in §1's admissibility table beyond taking its stated bound at face
value. Nothing I *did* check turned up a numeric or arithmetic defect in
`count-chain.md` itself — the one Blocking finding below is about sibling
documents outside the reviewed diff, found while checking whether the
thread's overall verdict framing is internally consistent, which the task
explicitly asked me to confirm.

## Verdict: **FAIL** (one Blocking finding, cross-document — not in the diff itself)

`count-chain.md` on its own is a clean, well-evidenced re-closure — every
number I re-ran reproduces exactly, and its citations into both derivation
documents are accurate. But it is not consistent with the two sibling
documents (`challenges/README.md`, `rebaseline-verdict.md`) that present the
same thread's verdict, and those documents were not part of this pass's
diff. This reproduces, in substance, the exact defect
`review-recloser.md` caught and required fixed on 2026-08-08 (desync between
`count-chain.md` and its sibling status surfaces) — now recurred one release
later with the C2 sync.

______________________________________________________________________

## Verified (re-run / cross-checked, all sound)

- **`checks/count-chain-decomposition.py`** re-run independently: `V0=864.4 m/s`, `mu=0.929 g`, `N0=2681` at shipped `f_breakup` default (0.943 via
    `breakup_velocity_fraction()`), and every §2 table row (`E_thr` =
    1.9/3.6/78.6/126/294.5 J → `N`=2312/2227/1440/1253/888, `N/700`=3.30/3.18/
    2.06/1.79/1.27, `N/779`=2.97/2.86/1.85/1.61/1.14) reproduces `count-chain.md`
    §2's table and prose exactly, including the rounded 3.3×/3.2×/(2.1×)/1.8×/1.3×
    figures.
- **`checks/count-chain-plug-shear.py`** re-run independently: central verdict
    row `m_thr=0.166 g, N=1756, N/700=2.51, N/779=2.25` matches §2's "verdict row"
    exactly; the ∓1σ, SYP, and η=1 rigid-bound rows (0.118/0.218 g,
    1878/1652, 2.68/2.36, 2.41/2.12; 0.210 g, 1666, 2.38, 2.14; 0.370/0.474 g,
    1427/1312, 2.04/1.87, 1.83/1.68) all match the table in §2 verbatim. The
    pre-registered crossover (243 m/s) and arrival velocity (612 m/s) also
    reproduce exactly.
- **Parenthesised f=1 (pre-C2) figures**: independently re-ran the central row
    with `f_breakup=1.0` explicit → `N=1925, N/700=2.75, N/779=2.47`, matching
    the parenthesised "(2.75)"/"(2.47)" in §2's table exactly.
- **C2 sweep band**: independently re-ran the central row at `f=0.953` and
    `f=0.899` → `N/779=2.29` and `2.09` respectively, matching "2.29× at
    f=0.953 and 2.09× at f=0.899" in §2 exactly.
- **`checks/count-chain-rebaseline.py`** re-run independently: block (A) gives
    `N_rec=779`, block (B) gives the A→D ratio 0.5570 (thread quotes 0.557),
    block (E) Tolch-13.29-lb basis gives ratios 1.99/1.84/1.70/1.59 across
    screens 2/3/4/thru4 — matching the document's "1.59–1.99×" claim exactly
    (max/min of that four-row column). Block (E)'s fuze-excluded variant
    thru4 = 1.81×, matching the C4 paragraph's "1.59× → 1.81×" claim exactly
    (not the superseded 1.19×).
- **Constants**: `sigma_f=800e6` and `gamma=54.5` in
    `src/arty/fragmentation.py` match §1's table; `M_case=4980.0` g reproduces
    via `_shell_geometry`.
- **Derivation citations, `updates/breakup-velocity-fraction/derivation.md`**:
    §5's adopted `f=0.943` (band 0.899–0.953), §6's `γ'_eq=48.5` at f=0.943 (inside
    Mott's 42–67 span), the "closing ~11% of the mean-mass gap while removing
    ~9% of the count" line, and §8's `N/779` table (2.47× at f=1 →
    2.25× at f=0.943, "realised leverage 1.096×", "22% eaten back") all appear
    verbatim in the source document and are cited accurately and without
    overstatement in `count-chain.md`.
- **Derivation citations, `updates/sourced-wood-perforation-threshold/derivation.md`**:
    §7.3's plug-shear form, τ=8.96 MPa (SPF-S, Sanborn 2019 Table 2), A8's
    η=½-is-geometry constraint, and §7.4's Check-4 table (central 2.75×/2.47× at
    f=1, "outside the 2× band... only η=1 rigid bound... lands inside") are all
    cited accurately. `count-chain.md` correctly does **not** propagate
    `derivation.md`'s own now-stale "(~2.15×)" parenthetical for block (E) (that
    number predates the pit-count re-baseline to 779); instead it recomputes
    its own fresh 1.59–1.99× figure from a live script run. Whether
    `derivation.md` §7.4's stale parenthetical should itself be updated is
    outside this diff's scope and is not flagged here as a defect of
    `count-chain.md`.
- **Open findings handling**: both pre-existing deferrable findings from
    `collect-findings.py` (the D-vs-E criterion mismatch; the fuze-excluded
    variant's numerator/denominator inconsistency) are correctly *referenced*
    rather than silently resolved or ignored. The D-vs-E finding is explicitly
    honoured: the verdict-row paragraph states "This row also inherits the
    standing block-(D) caveat... so the criterion-clean (E) figure remains the
    better-conditioned statement." The fuze-excluded-variant finding is named
    explicitly in the C4 paragraph and its superseded 1.19× figure is not
    quoted as valid anywhere. Both findings remain open, correctly, since this
    pass did not resolve their underlying methodological question.
- **Arithmetic spot-check**: "580 (33%) come from the 0.166–0.63 g window" —
    1756 (verdict-row N) − 1176 (N(≥0.63g) at f=0.943, from the decomposition
    script's own run) = 580, and 580/1756 = 33.0%. Checks out from numbers
    already independently reproduced above; no new script run needed.

## Blocking

**`challenges/README.md` and `rebaseline-verdict.md` were not updated by this
pass and now materially disagree with `count-chain.md`'s new verdict, in the
same document set the task asked me to check for internal consistency.**
Neither file appears in the diff (`git diff main --stat` shows only
`count-chain.md` changed), and `git log` confirms neither has been touched
since, respectively, `511377e` (C1 alone) and `5bb166c`/`ff2961b` (pre-C1).

- **`rebaseline-verdict.md`'s banner** (lines 8–48) is dated 2026-08-08 and
    states the count arm is "at or inside the 2× PASS band" using the
    since-demoted 78.6 J/126 J scalar-threshold rows (`N/779` = 2.00/1.73),
    and asserts "§4 'FAIL / count chain implicated' — no longer supported." This
    directly contradicts `count-chain.md`'s current, more authoritative
    plug-shear-based verdict: **FAIL at 2.25×**. The banner's own claim that
    "`count-chain.md` has been re-closed against current output and is the live
    document" was true on 2026-08-08 but is now itself stale, since
    `count-chain.md` has been re-closed a second time (C1 shipped, then C2) and
    `rebaseline-verdict.md` was never updated to point at the newer state or
    carry a second superseding banner.
- **`challenges/README.md`'s `count-gap-1938` status-detail paragraph** is
    internally self-contradictory: its item (3) (added by `511377e`, dated
    2026-08-10) correctly states C1 flips the arm back to FAIL at 2.47×/2.75×,
    but the paragraph immediately following it — carried over unedited from an
    earlier draft — still reads *"C1 (a sourced perforation threshold, blocked
    on @librarian) remains the recommended first move."* C1 is not blocked on
    @librarian; it shipped before this sentence's own paragraph says so two
    sentences earlier. Additionally, **README.md contains no mention of C2 at
    all** — not the `breakup_velocity_fraction` update, not the 2.47×→2.25×
    move, not the "does not clear 2× at any admissible f" conclusion. A reader
    of the project's own navigation entry point for this thread would not learn
    that C2 was ever run, and would read a self-contradictory sentence about
    C1's status.

**Impact.** This is the same failure mode `review-recloser.md` flagged
Blocking on 2026-08-08 and required (and got) fixed: a re-closure that lands
in the thread's primary document but not in the sibling surfaces that quote
its verdict. A future dispatch or a human skimming `README.md` — the
project's own index — would conclude C1 is still pending @librarian work and
would not learn the C2 change exists or that the standing verdict is FAIL at
2.25× (trending INDETERMINATE pending C5). That is a concrete risk of
redundant or misdirected work (e.g., re-dispatching @librarian for a
threshold that already shipped), which is exactly the scenario the prior
Blocking finding on this same thread was written to prevent.

**Suggested correction (not applied):** add a dated superseding banner to
`rebaseline-verdict.md` (following the pattern already used in its own file
for the 2026-08-08 supersession) pointing at `count-chain.md`'s current §4
verdict-framing note; and update `README.md`'s status-detail paragraph to (a)
delete or strike the stale "blocked on @librarian" sentence and (b) add a
dated item (4) covering C2's shipment and the 2.47×→2.25× move, matching
`count-chain.md` §4's "What stands after both" bullets.

## Notes (no action required — no numeric error, no change to the verdict)

- §2's opening banner quotes a combined band "2.09–2.41×" without flagging,
    at that point, that it unions two different sensitivity sweeps (the f-band
    gives 2.09–2.29×; the τ ±1σ band gives 2.12–2.41×; the low end comes from
    one sweep and the high end from the other). The document does disambiguate
    this later in §2's body text ("The whole η=½ band is outside... 2.12–2.41...
    so is the whole admissible f band (2.09–2.29)"), so a careful reader is not
    misled, but the headline figure alone could be read as one sweep's band.
    No effect on the verdict (both sub-bands are outside 2× regardless).
- §2's model-mass-basis discussion states "φ > 1 for every screen cut past
    the coarsest" — re-running block (E) shows φ=0.9556 (\<1) at the *second*
    screen and only exceeds 1 from the third screen on. The substantive
    conclusion (the model-mass basis is degenerate for most of the range and
    only the Tolch-13.29-lb basis is quotable) is correct and unaffected; the
    phrase is imprecise by one screen bucket.
- §4's "Outcome" paragraph states C5's ~1.22× correction "lands the arm at
    1.85× and therefore inside the band," citing only the pit denominator. §3's
    own C5 paragraph is more precise: N/779=1.85× (inside) but N/700=2.06×
    ("marginal," i.e. still nominally ≥2×). §4 does not claim a final PASS (it
    explicitly says C5 is not yet discharged and a fix "must not" be credited
    before then), so this does not change the stated verdict, but the
    restatement in §4 is less precise than §3's and could read as stronger
    support for an eventual PASS than the /700 denominator alone would justify.

## Re-review (2026-08-10) — fix for the Blocking cross-document-sync finding

**Scope, per dispatch instruction:** confirm only whether the fix
(`git diff main -- experiment/fragmentation-field/challenges/README.md experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md`)
resolves the Blocking finding above, and whether the newly-added passages are
accurate against `count-chain.md`'s current numbers. No other part of the
prior pass is re-verified here.

**Verdict: Blocking finding RESOLVED.**

- **The stale "blocked on @librarian" sentence** (`README.md`, formerly
    unqualified) is now wrapped in an inline `(*Superseded 2026-08-10:* ...)`
    parenthetical that explicitly voids it on both counts — "C1 was never
    blocked on @librarian and is no longer pending: it shipped" — and points to
    the live next-move ranking (C5 → C3 → C4). This follows the same
    superseding-banner convention already used elsewhere in these two files, so
    the stale sentence remains legible as history rather than being silently
    deleted, and is no longer readable as current status.
- **The missing C2 mention in `README.md`** is fixed: a new item (4)
    (lines 107–126) states C2 shipped
    (`arty.fragmentation.breakup_velocity_fraction`, $f$=0.943, band
    0.899–0.953), the 2.47×→2.25× move, the $f$-sweep band (2.29× / 2.09×), the
    standing FAIL verdict, and the C5-pending trend — matching
    `count-chain.md`'s current text.
- **`rebaseline-verdict.md`'s stale "at or inside 2× band" banner** is not
    deleted (consistent with the file's own established pattern of retaining
    superseded banners as a record) but is now followed by a second,
    clearly-dated "\*\*Second re-closure banner — model numbers, 2026-08-10 (post-C1
    - C2)\*\*" (lines 51–105) that explicitly states "the banner above is itself
        now partly superseded" and voids its §4 "no longer supported" bullet
        ("supported again ... the 'no longer supported' ruling in the banner above
        is void"). A second inline superseding note is also added at the file's §2
        "Overall status" (lines 243–251) and §3 restatement pointer (lines 272–281)
        is already-current text (unaffected — it already pointed at `README.md` as
        the live document, and `README.md` itself is now fixed).

**Accuracy of the newly-added passages against `count-chain.md`'s current
numbers:** independently spot-checked by grep against `count-chain.md`
(not re-run scripts — the underlying numbers were already re-run and verified
in the "Verified" section above; this pass only checks the new prose restates
them correctly):

- `count-chain.md` line 234–235: "now lands at **1.59–1.99×** ... (block (E),
    re-run 2026-08-10, was 1.78–2.24× pre-C2)" — matches both new files' "was
    1.78–2.24× at f=1" / "1.78–2.24× → 1.59–1.99×" restatements exactly.
- `count-chain.md` line 384: "moves the threshold-free population residual
    *up* (1.59× → 1.81× at the through-screen-4 row)" — matches both new files'
    "1.59× → 1.81×" (and README's "1.78× → 2.03× becomes 1.59× → 1.81×")
    exactly; the "1.78×→2.03×" half is the pre-C2 historical figure and is not
    independently re-confirmed here (it is presented as historical, and its
    ratio to the new figures, ×1.14, is internally consistent with the E-basis
    and C4-basis scaling shown elsewhere).
- `count-chain.md` lines 155, 411–412: "$N/700 = 2.06\times$ and
    $N/779 = 1.85\times$" and "~1.22× detection-limit correction" — matches
    both new files' "1.85× on /779 (2.06× on /700, still marginal)" and "~1.22×"
    detection-cutoff figures exactly.
- `count-chain.md` §2 verdict row (already independently re-run and verified
    above): $N/779$=2.47 (f=1) → 2.25 (f=0.943), $N/700$=2.75→2.51, f-sweep
    2.29×/2.09×, τ±1σ band 2.12–2.41× — all appear correctly in both new
    passages, matching the already-verified figures exactly.

No new arithmetic or unit defect found in the added text; no new Blocking
finding.

**New Note (not blocking):** `rebaseline-verdict.md`'s original 2026-08-08
banner (lines 9–49) is now nested two superseding-banners deep on some claims
(a 2026-08-08 banner partially superseding the base text, itself partially
superseded by the 2026-08-10 banner). This is readable — each banner is
clearly dated and each superseding note names exactly which bullet it voids —
but a third re-closure would make this file's superseding-banner stack
three-deep and harder to skim in one pass. Worth considering, next time this
thread's model numbers move, whether to fold the fully-voided 2026-08-08
bullets into the historical record (e.g. a compact changelog table) rather
than appending a fourth prose banner. No action required now; no effect on
current correctness.

## Review (2026-08-10) — C5 closure ("detection-limited, not physics-limited")

**Scope:** the uncommitted C5-discharge diff across `count-chain.md` §3/§4 and
top-of-doc banner, `checks/count-chain-rebaseline.py` block (G) and block (F)'s
new dual-denominator prints, `rebaseline-verdict.md`'s third stacked banner,
and `challenges/README.md` item (5). Verdict reached: FAIL at 2.25×(/779) /
2.51×(/700), INDETERMINATE clause discharged, C5 dropped from the ranking
without credit.

**Disclosure — partial verification, stopped on coordinator instruction.** I
did not get to: independently re-deriving §3's C3/C4 leverage figures (1.49×,
etc. — unchanged by this diff, not re-checked here); a full re-read of C1/C2's
own derivations (out of this diff's scope, already reviewed in the section
above); or a boundary/grazing-case sweep of the plug-shear rescaling in note
(v) (checked the one printed value only, see below). What follows is what I
did complete.

### Verified

- **Arithmetic reproduces.** Ran
    `uv run python checks/count-chain-rebaseline.py`; block (G) prints
    `N/700 = 2.05x` at the 0.36 g floor, realised leverage `1756/1438 =   1.221x`, matching every quoted figure in `count-chain.md` §3/§4,
    `rebaseline-verdict.md`'s third banner, and `README.md` item (5) exactly.
    Block (F)'s new `N/700` column at each cut (0.63→1.68, 0.36→2.05,
    0.166→2.51) is internally consistent with block (G).
- **Block (G) uses the same live model state as the rest of the script** — it
    calls `mott_N(..., N0, mu)` with the `N0, mu` computed once near the top
    from `mott_params(shell, V0)`, which defaults `f_breakup=None` →
    `breakup_velocity_fraction()` = 0.943 (C2 active). No hand-typed
    duplicate of `N0`/`mu`.
- **Plug-shear rescaling in note (v) checked by hand.** $E_{thr}\propto
    m^{1/3}$, $\mathrm{KE}=\tfrac12 mv^2$ ⇒ solving for $m$ gives $m_{thr}
    \propto v^{-3}$ (not $v^{-2}$, since the threshold energy itself depends on
    $m$) — algebra is correct, and $0.166\times(612/838.2)^3 = 0.065$ g
    matches the printed value; direction (higher $v$ → lower $m_{thr}$) is
    physically right.
- **Claim (i)'s factual premise — that Tolch's table grades every hit into
    perforation/penetration/dent columns rather than a binary
    detected/not-detected — is confirmed against the closure-checked table,
    not just against `card.md`'s prose.** Re-ran
    `uv run src/utils/check-table-invariants.py   doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/base-spray-density.invariant`:
    `perf+penet+dents==total` passes on all 17 rows. This is the load-bearing
    fact under (i)'s argument that the 700 column is perforation-limited by
    construction (a fragment too weak to perforate lands in an adjacent
    column, it is not dropped from the census), and it is admissible —
    CSV-backed, invariant-checked, not a `tolch-1938.md` read.
- **Criterion-match correction is real and correctly applied.** The
    diff's central move — quoting C5's bound against `N/700` (panel floor vs.
    panel perforation count) instead of the pre-existing `N/779` (panel floor
    vs. pit sand-recovery census) — is the right fix and is explicitly
    self-flagged as voiding the document's own earlier-same-day 1.85× figure.
    This is the same basis-mix pattern as the two standing open findings
    against block (D) and block (E)'s fuze-excluded variant (confirmed both
    markers are still present, untouched by this diff, at
    `source-data-audit/review-criterion-match.md` and
    `.../review-void-rulings.md` — this diff does not close them and does not
    claim to).
- **§4's INDETERMINATE gate is applied correctly.** The gate's own stated
    firing condition ("cannot be bounded below ~1.5×") is compared against the
    newly bounded 1.221×; 1.221 < 1.5, so non-firing is the right call given
    that pre-existing threshold. I did not re-derive why 1.5× was chosen (set
    in an earlier pass, not part of this diff).
- **Datum admissibility (point iv) is handled correctly, not overclaimed.**
    `card.md` line 22 does say `tolch-1938.md` "is not a citable surface for
    any number" and that a number without a CSV "has no admissible surface in
    this repo" — grepped and confirmed. The diff's own point (iv) discloses
    this about the 0.36 g / 838.2 m/s datum used in block (G), states the
    finding is "flagged, not a fabrication verdict" per
    `source-data-fidelity.md`'s own rule that a null result on a
    known-unreliable extraction bounds the surface, not the source, and does
    not hide the caveat in `card.md` — it sits in `count-chain.md`, which is
    the correct location per that rule's "interpretive claims must not live
    in `doc-reference/`" clause.

### Findings

**Deferrable — headline verdict numbers partly rest on an admittedly
inadmissible datum, presented alongside a clean argument that doesn't need
it.** Point (ii)'s 2.05×/1.221× figures — which are quoted as *the* bound in
the top-of-document status paragraph, `rebaseline-verdict.md`'s banner, and
`README.md` item (5) — derive from `M_DET_G = 0.36` g, a value point (iv) itself
says has no CSV and isn't anchored beyond a reconstructed-not-read 126 J
figure. Argument (i) (perf/penet/dent grading, CSV-confirmed above) is
structurally sufficient on its own to discharge the INDETERMINATE clause and
does not depend on the weak datum, and the document says so ("readings (i) and
(ii) bracket the answer") — but three of the four surfaces citing this closure
lead with the numeric 1.221×/2.05× figures rather than with (i)'s
census-grading argument. Impact: none on the verdict itself (FAIL stands on
(i) alone), but a reader skimming any of the three status surfaces sees an
inadmissible-datum-derived number presented with equal prominence to the
admissible one. Suggested fix: lead each of the three status surfaces with
argument (i) and demote (ii)'s figures to "even on the weaker, inadmissible
reading" phrasing (`count-chain.md` top banner lines 40–48, `rebaseline-verdict.md`
third banner, `README.md` item (5)).

**Deferrable — note (v) (C1 threshold "permissive by 5.6× in mass" at
near-burst velocity) has no deferred-finding marker.** It's a genuine model-side
observation touching shipped `arty.perforation`, explicitly caveated as
resting on the same unanchored 0.36 g datum as above, and explicitly "recorded
as a note, not actioned here" in the prose — but per
`.claude/rules/deferred-findings.md` even note-tier items get a one-line
marker so `collect-findings.py` surfaces them to a future pass; a prose-only
note in `count-chain.md` won't be found by that mechanism. Impact: no effect
on any current output or the verdict; risk is this specific observation being
re-discovered from scratch (or silently dropped) rather than routed, the same
failure shape `deferred-findings.md` names in its own motivating incident.
Suggested fix: add a note-tier marker reading "C1 plug-shear threshold rescales
to 0.065 g at 838 m/s vs. Tolch's smallest observed perforation 0.36 g (5.6x
permissive in mass); rests on an unanchored datum (affects:
experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md)"
using the tag-and-severity format from `.claude/rules/deferred-findings.md`.

**Note — third stacked banner in `rebaseline-verdict.md` matches the
documentation-debt concern already flagged in this file's 2026-08-10
re-review** (see above: "a third re-closure would make this file's
superseding-banner stack three-deep and harder to skim"). That has now
happened. Still no effect on correctness — every banner is dated and states
exactly what it supersedes — but the changelog-table suggestion from the prior
pass is worth acting on before a fourth banner is needed. No action required
now.

**Note — small (0.06%) discrepancy between block (G)'s hardcoded
`N_verdict = 1756.0` and block (F)'s computed value at the same nominal cut
(1757 at `cut=0.166` g).** Traced to `N_verdict` being taken from §2's verdict
row (computed from the full model chain's un-rounded $m_{thr}$) versus block
(F) recomputing from the literal rounded `0.166` g. Immaterial (both round to
the same quoted 2.51× figure) — flagged only so a future reader doesn't
mistake it for a discrepancy worth chasing.

### Verdict: **PASS-with-limitations**

No Blocking finding. The closure's central physics claim (Tolch's census is
graded perforation/penetration/dent, not a detection-limited binary) is
correct and CSV-verified; the arithmetic reproduces exactly; the
criterion-match self-correction (N/700 vs. the voided N/779) is the right fix
and is properly disclosed as voiding the document's own same-day earlier
figure; the INDETERMINATE-gate application is correct against its own
pre-existing threshold. The two deferrable items above should be logged as
limitations:

- Log that the C5 closure's headline 1.221×/2.05× figures rest on a datum
    (0.36 g / 838 m/s) with no CSV backing per `card.md`'s own admissibility
    rule, and that the closure's real load-bearing argument is (i)
    (perf/penet/dent census grading), not the numeric bound — the three status
    surfaces should be reordered to lead with (i).
- Add the missing note-tier deferred-finding marker for the
    C1-threshold-permissiveness observation in note (v) so it is tracked by
    `collect-findings.py` rather than living only in prose.
