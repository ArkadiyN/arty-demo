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

## Review (2026-09-22) — maintenance banner pass (aspect_ratio 1.950 re-closure)

**Reviewer:** model-reviewer (Sonnet 4.6)
**Scope:** the @modeler maintenance pass that added correction banners to
`count-chain.md` and `rebaseline-verdict.md` reflecting live `aspect_ratio = 1.950` (kappa_x/k/c re-solved at the shell's own ruled-line regime,
`630dac8`/`18cd069`), and a cosmetic label fix in
`checks/count-chain-aspect-moment-reclosure.py`.

**Verdict: FAIL**

### Open findings at pass entry

`collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938`
returned exit 1 with malformed-marker errors before listing findings (see
Finding 1 below). Informational register from the brief:

- [blocking] count-gap-1938 publishes 2.28x/2.54x as shipped-code verdict — affects rebaseline-verdict.md, count-chain.md (raised 2026-08-18)
- [deferrable] 1.221x/2.05x C5 figures on inadmissible datum — pre-existing, out of scope
- [note] C1 plug-shear threshold 0.065 g — pre-existing, out of scope

### Finding 1 — BLOCKING: prose blocking-marker references trigger malformed-marker parse failure

**Files:** `count-chain.md` line 33, `rebaseline-verdict.md` line 240
**Impact:** `collect-findings.py --check` exits 1 before any checking logic
runs. The pre-commit hook uses this exact entry point; the staged files
cannot be committed as written. Blocks the entire pass.

Both banners added by the modeler reference the existing marker in prose
using backtick inline code naming the blocking marker literally. The
parser's LOOSE regex `r"FINDING\\?\["` matches these lines and flags them as
malformed markers that "do not parse" because they lack the required `:`,
`affects:`, and `since:` fields. The LOOSE match exits early with return
code 1 before the `--check`/`--scope` branches run.

Observed output from `uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938`:

```
Malformed FINDING markers (fix or the finding is lost):
  experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md:33: ...
  experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md:240: ...
```

**Suggested correction (not applied):** replace both literal blocking-marker
strings in the banner prose with neutral phrasing that does not contain the
marker-prefix substring, such as "the open blocking finding" or "the
blocking marker". The meaning is preserved; the parser is not triggered.

### Finding 2 — PASS: numeric reproduction exact

`uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-aspect-moment-reclosure.py`
independently produces:

```
shipped A=1.950  mu = 1.321 g   N0 = 1886   V0 = 864.4 m/s   M_case = 4980 g
SPF-S eta=1/2 (VERDICT) shipped: N = 1322  /700 = 1.89  /779 = 1.70
```

All five parameters match the modeler's report exactly. The banners in both
files quote these numbers correctly. No discrepancy.

### Finding 3 — Note: label fix is cosmetic, not a data change

The change in `checks/count-chain-aspect-moment-reclosure.py` replaces the
hardcoded string `"shipped A=1.577"` with the computed expression
`f"shipped A={shipped.aspect_ratio:.3f}"`. The data row always called
`mott_params(shipped, V0)` on the live `SHELLS` object; only the column
header label was stale. This is a cosmetic fix. No impact on any printed
number.

### Finding 4 — Deferrable: blocking marker at `updates/kappa-x-shell-regime/derivation.md:341` left with stale interim numbers

The modeler correctly left the blocking marker in place (did not delete it)
since the full re-closure of `count-chain.md`'s ~20 verdict statements had
not happened yet at this pass. The marker's own text cites "correct" live
values of 2.22x(/700)/2.00x(/779), but the actual live values are now
1.89x(/700)/1.70x(/779) — the marker's interim figures are themselves stale.

**Impact:** the marker is directionally correct (flags that count-gap-1938
carries stale verdict numbers) but its quoted "live" pair is wrong by ~15%.
This is within the 2x band and doesn't flip any safety judgment, so it's
deferrable. The correct resolution is a full §1/§2/§4/§5 re-closure pass
that rewrites the body text, at which point the marker can be deleted
cleanly.

### Finding 5 — Note: scope call on not rewriting ~20 body statements is correct

The modeler's decision to add banners rather than rewrite the body text of
`count-chain.md` is defensible for a maintenance pass. The banner is placed
at the top of both files and explicitly warns readers. The compound §4 PASS
test caveat (A→D falloff arm not retouched) is correctly stated. No
misleading conclusions result from leaving the body stale when the banner is
present and prominent.

### Summary

**FAIL** — one blocking finding: prose references to the literal blocking
marker in both banners match the parser's LOOSE regex and cause
`collect-findings.py` to exit 1, which the pre-commit hook will reject. Fix:
replace both instances with neutral phrasing to remove the marker-prefix
substring from prose. The numeric work is otherwise correct: the parameter
chain (aspect_ratio=1.950, mu=1.321g, N0=1886, V0=864.4 m/s) is confirmed by
running the check script against live arty, the 1.70x/1.89x verdict pair is
reproduced exactly, the label fix is cosmetic, and the scope calls (banners
not body rewrite, marker not deleted) are appropriate for a maintenance
pass.

______________________________________________________________________

## 2026-09-23 — Pass 1 (adversarial critique): compound-verdict re-closure (count arm 1.70×/1.89×, "INDETERMINATE")

Scope: the uncommitted re-closure diff to `count-chain.md` (current-verdict
banner + inline supersessions), `rebaseline-verdict.md` (sixth re-closure and
verdict-direction banners), and the deletion of the blocking marker at
`updates/kappa-x-shell-regime/derivation.md:341`. Register pre-check
(`collect-findings.py --for …/count-gap-1938`): 2 open, both 2026-08-10 (C5
datum deferrable, C1 0.065 g note) — neither is touched by this re-closure and
neither is blocking; their non-action is fine.

New probe for this pass:
`experiment/_scratch/count-gap-1938-falloff-arm-reachability.py` (to be
`git mv`'d to `challenges/count-gap-1938/checks/` by the caller — it produced
the F1 numbers below; runs in ~2 s).

### Verdict: **FAIL** (one Blocking finding, F1)

The count-arm arithmetic is sound and independently corroborated (below), and
the refusal to call the compound test PASS is correct. What fails is the
*reason* given for "INDETERMINATE": the claim that the falloff arm is
unreachable from this chain and untouched by the commits is false, and when
the arm is run with the chain's own functions it lands outside its tolerance.

### F1 — Blocking — the falloff arm is reachable, was moved by the commits, and fails its 0.10 tolerance

`count-chain.md` current-verdict banner (lines ~44–58), the §4 supersession
note (~line 706–711), the "What stands" bullet (~757–767), the §4 closing
bullet (~789–794), and `rebaseline-verdict.md` lines ~250–258 all assert: (a)
"no `arty` function reachable from this count chain predicts" the A→D ratio,
(b) the model-side falloff is "the `../drag-gap-1944/` $B(r)$ aspect, walled
off from this thread by construction", (c) the two commits "leave the falloff
arm untouched — they rescale count magnitude, not the spatial falloff".

All three are wrong:

- **(a)** The observable is the per-unit-solid-angle ratio
    $N(\ge m_{thr}(r_D))/N(\ge m_{thr}(r_A))$ — $N_0$ and $1/r^2$ cancel; only
    drag, $E_{thr}(m)$ and $\mu$ enter. It is computed with exactly the calls the
    verdict row already uses (`min_lethal_mass(..., E_thr=partial(perforation_threshold_energy, ...))`
    - `mott_N`), at 15 and 120 ft. §4 itself (line ~672) says so: "Re-running
        the falloff ratio through `arty.perforation` is the cheapest way to make
        this a two-observable test and is **not blocked on anything**." The banner
        contradicts the section it summarises.
- **(b)** The cited "why a separate thread" note (line ~137) argues that the
    *count* is total-against-total and cancels azimuthal weighting; it says
    nothing about the falloff ratio and does not wall it off. The falloff
    computation that exists in `../drag-gap-1944/tolch-1938-panel-distance.md`
    Result 1 is this same perforation-count ratio (A/B/C/D = 1.000 … .557), not
    $B(r)$ — the $B(r)$ attribution is a mischaracterisation.
- **(c)** $\mu$ does not cancel in the ratio (Mott tail
    $\exp(-\sqrt{m/\mu})$ at two different $m_{thr}$), so the aspect-ratio move
    changes it.

Live numbers (plug-shear, SPF-S η=½ `WoodPanelTarget()` default, shipped drag,
$V_0$ = 864.4 m/s; probe script above):

| case                            | μ [g]     | $m_{thr}$ A / D [g] | $N_A$    | predicted D/A | vs 0.557 ± 0.10     |
| ------------------------------- | --------- | ------------------- | -------- | ------------- | ------------------- |
| A = 1.577 (08-16 state, live k) | 1.068     | 0.166 / 2.084       | 1571     | 0.367         | −0.190, outside     |
| **live A = 1.950**              | **1.321** | 0.166 / 2.084       | **1322** | **0.406**     | **−0.151, outside** |

($N_A$ = 1322 reproduces the banner's verdict row, confirming the probe runs
the same chain.) So the commits moved the falloff prediction by +0.04 (~10 %),
and on live code the second observable is **run and outside tolerance by
1.5× the band half-width**.

**Impact.** The compound verdict changes qualitatively: "INDETERMINATE — one
arm never evaluated, open gap belongs to drag-gap-1944" becomes "not PASS —
count arm within 2×, falloff arm evaluated and outside 0.10 (0.41 vs 0.557)",
with the remaining gap routed back *into this thread* rather than to a thread
that does not compute it. No demo-rendered number changes; the challenge
verdict and its routing (the in-scope outcome of this thread) do. Also note
§4's trichotomy defines INDETERMINATE *only* as "C5 cutoff not bounded below
~1.5×" — a clause the same file says was discharged and did not fire —
so reusing the label for a different state is itself confusing (see F3).

Caveats the fix pass must weigh, not a reason to keep INDETERMINATE: with a
*sourced* (not fitted) threshold the ratio is drag-sensitive (drag-gap Result 1's
degeneracy holds only when $E_{thr}$ is refitted); Tolch's own perforation
ratio is biased toward 1 by a fixed threshold (rebaseline check block (B)
comment) — but the model ratio uses a threshold too, so the comparison is
like-for-like; and the η/f/τ bands of the count arm should be swept on this
arm as well before stating a range.

**Correction (do not apply here):** @modeler runs the falloff arm as a
retained check (η, f and drag bands), replaces claims (a)–(c) in both files
with the computed ratio, and restates the compound result using an explicit
label distinct from §4's C5-INDETERMINATE (e.g. "NOT PASS: count arm in band,
falloff arm 0.41 vs 0.557 ± 0.10").

### F2 — Note — the count-arm crossing is genuine, not a slip

Competing-explanation check: the direction change is corroborated by an
independent computation that predates the re-closure —
`updates/kappa-x-shell-regime/derivation.md` §5.3 table, "new (percell)" row:
c_eff 1.4217, μ 1.321 g, $N_0$ 1886, $N$ = 1323, 1.89×/1.70× (m_thr 0.166 g
held fixed). Same μ/$N_0$ as the banner; $N$ differs by 1 fragment. The move is
entirely through μ (0.915 → 1.321 g) with $m_{thr}$ fixed at 0.166 g — no unit
or sign change in the threshold path. No impact.

### F3 — Deferrable — "INDETERMINATE" overloads a label §4 already defines

§4 (line ~686) defines INDETERMINATE as the C5-unbounded case; the same file
states that clause "did not fire". The new banners then call the compound
result INDETERMINATE for a different reason. A reader of §4 gets two
contradictory statements about the same label. Impact: presentation only once
F1 is fixed (F1's fix should pick a distinct label, which closes this too).

### F4 — Deferrable — `derivation.md` "stays a genuine FAIL" at 1.89×/1.70×

`updates/kappa-x-shell-regime/derivation.md` ~line 341–342: "Against live
shipped code the challenge improves from 2.22×/2.00× to 1.89×/1.70× and stays a
genuine FAIL". Both numbers are < 2×, so under §4's FAIL branch ("count still
≥ 2× high") this was self-contradictory *when written* (as was its "scoping
predicted ~1.8×/1.6×" alongside FAIL) — the count-arm crossing was visible at
`18cd069` and nobody caught it. Severity: not Blocking — no shipped constant or
rendered surface rests on the word "FAIL" (the numbers in the sentence are
correct, and per F1 the compound test is indeed not a PASS, just for a
different reason). But deleting the adjacent marker left this sentence
contradicting the challenge thread with no pointer. Required: a one-line dated
supersession after the sentence ("count arm is inside 2×; see
count-gap-1938 current-verdict banner"), or a deferrable marker on it.

### F5 — Note — marker deletion was right on its own terms

The deleted marker's concern was specifically that the challenge published a
stale pre-`k` pair (2.28×/2.54×) as the shipped-code verdict. The banners now
supersede that pair everywhere I checked in `count-chain.md`, so that concern
is closed; the physics question (F1) was never that marker's content and did
not need to gate its deletion. The only miss is F4's orphaned sentence.

### F6 — Note — provenance of cited commits

`630dac8` (2026-08-17, "resolve Mott breadth-variance factor k per-shell …,
ship v0.14.0") and `18cd069` (2026-08-19, "re-solve kappa_x/k/c … l/x0~95, not
the l/x0=20 demonstration value, ship v0.15.0") match their commit subjects;
derivation §6.2 X1 confirms Λ = 95 vs Mott's Λ = 20 demonstration. "v0.14.0 /
v0.15.0" are commit-subject labels only — `pyproject.toml` reads 0.1.0 at both
commits — so they are not package versions; harmless, but don't cite them as
such.

### Limitation entries (if the fix pass keeps any caveat)

- "The A→D falloff arm is computed at the sourced plug-shear threshold and is
    drag-sensitive at fixed $E_{thr}$; its value depends on the shipped drag
    constant contested in `../drag-gap-1944/`."

______________________________________________________________________

## Re-review — fix cycle 1 of F1/F3/F4/F6 (2026-09-23, @model-reviewer)

Scope: only the four items raised in the adversarial-critique section above.
No new-scope findings.

**Verdict: FAIL** — one residual Blocking defect, a single stale live
sentence in `count-chain.md`. Everything else in the fix is correct. Cycle 2
needs one edit (R1), plus one optional wording fix (R2).

### Reproduction

- `uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-gap-1938-falloff-arm-reachability.py`
    prints: live A=1.950, μ=1.321 g, N_A=1322, **pred D/A = 0.406**, |Δ|=0.151
    OUTSIDE 0.10. The superseded 2026-08-16 row (A=1.577) prints 0.367, and the
    pre-c legacy row (A=1.600) prints 0.370. These match what I found before.
- `uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938`
    parses cleanly (exit 0; 2 pre-existing open entries, a deferrable and a note,
    both dated 2026-08-10 and outside this re-review's scope).
- `git show 630dac8:pyproject.toml` / `git show 18cd069:pyproject.toml` →
    `version = "0.1.0"` at both.

### F1 — mostly fixed; residual R1 (Blocking)

Verified correct, with consistent numbers (0.406 / 0.557 / −0.151 / ±0.10) and
a compound-FAIL conclusion:

- `count-chain.md` Status paragraph, lines 9–14
- the current-verdict banner, lines 28–85, including the drag / η-f-τ caveat
    logged as a limitation (it matches the limitation entry my prior section asked for)
- the §4 supersession note, lines 728–740
- the "What stands" first bullet, lines 784–795
- the closing bullet, lines 817–826
- `rebaseline-verdict.md` top notice, lines 14–29
- the sixth re-closure banner, lines 253–282

I checked every grep hit for INDETERMINATE / untested / unreachable /
untouched / compound in both files:

- rebaseline-verdict.md lines 101, 124, 130–151, 387, 397, 415–454 are all
    dated historical banners or audit-table cells. The "trending INDETERMINATE"
    clause is declared void at line 130.
- count-chain.md lines 596–599, 618, 716–718 and 742–757 are the §4
    definition or the dated C5 discharge. Lines 250 and 448 use "untouched" in
    an unrelated sense.

**R1 — Blocking (one live sentence still asserts the old wrong conclusion).**
`count-chain.md` lines 126–128, the parenthetical at the end of the C5 paragraph
in the header summary:

> *(That FAIL is the dated 2026-08-16 figure; on live shipped code the count arm
> is inside the band at 1.70×/1.89× and **the compound verdict is
> INDETERMINATE** — see the current-verdict banner above.)*

This is written in the present tense ("on live shipped code"), so it is a live
claim. It states exactly the conclusion F1 overturned, and it reuses
INDETERMINATE for the non-C5 case, which F3 forbids. It also contradicts the
banner it points the reader to, 45 lines above.

- Impact: a reader skimming the header summary gets a verdict (INDETERMINATE)
    that differs qualitatively from the authoritative one (FAIL). This is the same
    published-verdict defect as F1, just smaller in extent. It is Blocking only
    because it asserts a wrong published verdict. No number or shipped constant is
    affected.
- Required fix: replace "and the compound verdict is INDETERMINATE" with "but
    the compound verdict is FAIL on the falloff arm (0.406 vs 0.557, outside
    ±0.10)". Nothing else needs to change.

**Deferrable (not required for PASS):** two older sentences still describe the
falloff arm as unrun without a local pointer:

- `count-chain.md` §4 "What C1's check did", lines 694–698: "the second has
    not [been run] … remains compound … is not blocked on anything". The §4
    supersession note at lines 728–740 covers this, but only 30 lines later.
- line 807–808: "the falloff-ratio observable is still unrun", inside the C3
    narrative of the live "What stands" bullet.

Impact: none on any verdict, because both passages are overridden in the same
section. Suggested fix: add an inline "(run 2026-09-23: 0.406, see banner)"
after each one.

### F3 — fixed except at R1

The two-arm phrasing is used everywhere the fix pass edited. The only live
reuse of INDETERMINATE for the falloff case is R1 above. Every other hit is the
§4 definition or the dated C5 record.

### F4 — fixed; residual R2 (Deferrable)

A dated clarification block has been added at `updates/kappa-x-shell-regime/derivation.md`
lines 344–350. Its present-tense content is correct:

- 1.89×/1.70× puts the count arm inside 2×, so that arm passes
- the compound test fails on the falloff arm, 0.406 vs 0.557
- it points to the authoritative banner

**R2 — Deferrable (a new historical inaccuracy in the clarification).** The
block says the old sentence "referred, **when written**, to the compound §4
test". That cannot be right. When line 342 was written (at `18cd069`), the
falloff arm had never been run, and the threads at the time called it
unreachable. So "stays a genuine FAIL" could not have been a statement about the
compound test's falloff arm. My prior section (F4 above) recorded the sentence
as self-contradictory when it was written, and this clarification now claims a
different intent for it.

- Impact: no number, verdict or rendered output changes. The block's
    conclusion is right; only its account of what the sentence originally meant
    is wrong.
- Suggested wording: "The 'stays a genuine FAIL' above was inconsistent when
    written (1.89×/1.70× are inside the 2× band, so the count arm passes). The
    compound §4 test is nonetheless a FAIL, because its A→D falloff arm (run
    2026-09-23) predicts 0.406 vs 0.557 …"

Out-of-scope observation, for triage only: the paragraph right after the
block, lines 352–356, still frames the thread as "~120 % over-count" with C3
and C4 as "remaining candidates". Both are stale, because C3 and C4 were
discharged on 2026-08-15. The dated clarification makes this less of a problem.
It is not Blocking.

### F6 — fixed

Every occurrence reads "commit subject 'v0.14.0'" / "commit subject 'v0.15.0'":

- `count-chain.md` lines 33–36, which also notes that `pyproject.toml` reads
    0.1.0 at both commits
- `rebaseline-verdict.md` lines 232–234

No other v0.14.0 / v0.15.0 hits are in either file.

### Minor note (no action needed)

`rebaseline-verdict.md` lines 4–9 still say "Read **all five** re-closure
banners". There are now six, but the top notice at line 14 supersedes this
line.

### What cycle 2 must do (tight scope)

1. R1: edit `count-chain.md` lines 127–128 as specified above. This is required.
1. R2: reword the clarification's "referred, when written, to" in
    `updates/kappa-x-shell-regime/derivation.md` line 344. This is recommended,
    not required.
1. Optionally, add the two inline pointers at `count-chain.md` lines 694–698
    and 807–808.

With R1 done, the verdict becomes PASS-with-limitations. The limitation is the
drag / η-f-τ caveat on the falloff arm, which is already logged in both banners.

## Re-review — fix cycle 2 (final, cap 2/2) of R1/R2 (2026-09-23, @model-reviewer)

Scope: R1, R2, the two optional inline pointers and the two out-of-scope
observations from the cycle-1 section above. No new-scope findings.

**Verdict: PASS-with-limitations.**

### R1 — fixed

`count-chain.md` lines 126–128 now say: "on live shipped code the count arm is
inside the band at 1.70×/1.89× but the compound verdict is FAIL on the falloff
arm (0.406 vs 0.557, outside ±0.10) — see the current-verdict banner above."
This matches the banner at lines 28–85. I grepped the whole file for
INDETERMINATE. It has 9 hits, at lines 122, 125, 596, 599, 618, 717, 743, 745
and 757. Each is one of:

- the §4 clause definition (717)
- the dated C5 discharge record (596–599, 743–757)
- the ranking history (618)
- the explicitly past-tense 2026-08-16 sentence (122–125)

None is a live, present-tense claim that the compound verdict is INDETERMINATE.

### R2 — fixed

`updates/kappa-x-shell-regime/derivation.md` lines 344–352 now say the
sentence "was inconsistent when written". The reasons it gives are correct:

- it asserted FAIL while both cited numbers were inside the 2× band
- the falloff arm had not yet been run, "so nothing supported a FAIL at that time"

The block then says the count arm is a PASS, and that the compound test is a
FAIL today because the falloff arm (run 2026-09-23) gives 0.406 vs 0.557. This
is consistent with the banner, and the new wording adds no new error.

### Optional pointers — both landed

- `count-chain.md` line 698: "(Run 2026-09-23: 0.406 vs 0.557, distance
    −0.151, outside ±0.10 — see the current-verdict banner.)"
- `count-chain.md` lines 808–809: "(since run 2026-09-23: 0.406 vs 0.557, see
    current-verdict banner)"

Both are accurate. The second sits at column 0 inside an indented bullet. That
is cosmetic, and it is only a Note.

### Out-of-scope spot checks

- `derivation.md` lines 338–340 now say C3 and C4 were "both run and closed
    2026-08-15 … no sub-candidate remains". Lines 354–357 also add that they
    closed without shippable credit. The phrase "~15 % of a ~120 % over-count"
    remains. It describes the historical framing of the thread, affects no
    verdict, and is a Note.
- `rebaseline-verdict.md` lines 4–10 now say "Read **all six** re-closure
    banners" and list all six, the 2026-09-23 one included. This is fixed.

### Register

`uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938`
exits 0 and lists 2 pre-existing entries dated 2026-08-10: a deferrable one at
line 150 and a note at line 594. Both are outside this cycle's scope. Neither
is `blocking`.

### Limitation (already logged in both banners, no new entry needed)

The A→D falloff-arm prediction (0.406) is computed at a fixed, sourced
plug-shear threshold, so it depends on the shipped drag constant contested in
`../drag-gap-1944/`. It has also not yet been swept across the η/f/τ bands.
Neither is expected to flip the sign, since the result misses the tolerance
by 1.5× the band half-width.

Fix-cycle cap: this was cycle 2 of 2, and no residual items remain.

______________________________________________________________________

## Pass 2 — mechanical verification (2026-09-23, @model-reviewer)

**Scope:** reproduce the cited numbers, trace the live code path, confirm
cross-document consistency. No re-judging of adversarial-critique call judgments
(compound-test framing, INDETERMINATE-label choice, fix-cycle cap).

**Verdict: PASS-with-limitations.** All seven items below reproduce exactly.
No new finding. Limitations already logged in both banners; none are raised
fresh here.

### 1. collect-findings register

`uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges/count-gap-1938`
exits 0. Two open entries, both dated 2026-08-10:

- [deferrable] 1.221×/2.05× C5 figures on inadmissible datum
- [note] C1 plug-shear threshold 0.065 g

Both are pre-existing and outside this pass's scope. Neither is blocking.

### 2. Falloff-arm check script (standalone reproduction)

`uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-gap-1938-falloff-arm-reachability.py`
prints:

```
pre-c legacy A=1.600   mu=1.083 g  m_thr A/D = 0.166/2.084 g  N_A=1553  pred D/A = 0.370  |pred-0.557| = 0.187  OUTSIDE 0.10
2026-08-16 A=1.577     mu=1.068 g  m_thr A/D = 0.166/2.084 g  N_A=1571  pred D/A = 0.367  |pred-0.557| = 0.190  OUTSIDE 0.10
live A=1.950           mu=1.321 g  m_thr A/D = 0.166/2.084 g  N_A=1322  pred D/A = 0.406  |pred-0.557| = 0.151  OUTSIDE 0.10
```

Live A=1.950 → 0.406, superseded A=1.577 → 0.367. Both match what the Pass 1
adversarial-critique, cycle-1, and cycle-2 sections cite. N_A=1322 reproduces
the count-arm verdict row, confirming the same parameter chain.

### 3. Count-arm check script (standalone reproduction)

`uv run python experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-aspect-moment-reclosure.py`
prints (shipped row):

```
shipped A=1.950   mu = 1.321 g   2mu = 2.641 g   N0 = 1886
SPF-S eta=1/2 (VERDICT) shipped: N = 1322  /700 = 1.89  /779 = 1.70
```

Matches N=1322 → 1.70×(/779)/1.89×(/700) as cited throughout.

### 4. Live aspect_ratio in shipped code

`arty.shells.SHELLS["75mm M48 HE"].aspect_ratio` returns 1.950209408. Both
check scripts call `mott_params(shipped, V0)` on the live `SHELLS` object and
reach µ=1.321 g, N0=1886. No hand-typed parameter is silently different between
the two scripts' parameterization.

### 5. Tolch 0.557 provenance

The 0.557 target is not invented for this pass. `count-chain-rebaseline.py`
block (B) computes it from the CSV: `float(static["D"]["perf"]) / float(static["A"]["perf"])` read from `side-spray-density.csv`, printing
`ratio = 0.5570`. The falloff-arm script hardcodes `TOLCH_AD = 0.557` — a
one-decimal transcription of this CSV-derived value. The CSV is the primary;
the constant matches it.

### 6. Cross-document consistency (current text, fresh read)

- **count-chain.md** top-of-doc status (lines 9–16): "the count arm lands
    *inside* the within-2× band at 1.70×/1.89× … the compound §4 test is a
    genuine FAIL — the A→D falloff arm … predicts 0.406 vs Tolch's measured
    0.557 (distance −0.151, outside the ±0.10 tolerance)". Current-verdict banner
    lines 28–85 give the full argument. Lines 126–128 (R1): "but the compound
    verdict is FAIL on the falloff arm (0.406 vs 0.557, outside ±0.10)". No live
    INDETERMINATE claim found.
- **rebaseline-verdict.md** current-verdict notice (lines 16–31): "1.70× (/779)
    / 1.89× (/700) … compound verdict FAIL … 0.406 vs Tolch's measured 0.557,
    distance −0.151, outside the ±0.10 tolerance". Consistent with count-chain.md.
- **kappa-x-shell-regime/derivation.md** lines 345–353 (R2): "The 'stays a
    genuine FAIL' above was inconsistent when written … the compound test is
    nonetheless a genuine FAIL today because its A→D falloff arm (run 2026-09-23)
    predicts 0.406 vs Tolch's 0.557 (outside ±0.10)." Consistent with both.

All three documents are mutually consistent and agree on the verdict (count arm
PASS, compound FAIL on falloff arm).

### 7. Check-script retention requirements

`count-gap-1938-falloff-arm-reachability.py`:

- Has a module docstring naming its consumer: `experiment/fragmentation-field/challenges/count-gap-1938/review.md`.
- Runs standalone without relative-path assumptions (`from arty.…` imports;
    no `os.getcwd()` or `../` paths; confirmed via uv run from repo root).
- Named for what it checks.
- Cited by path in the current-verdict banner of `count-chain.md` (lines 71–72).

No finding on retention requirements.

### Limitation (inherits from banners, no new entry)

The A→D falloff-arm prediction (0.406) is at a fixed sourced threshold and
depends on the shipped drag constant contested in `../drag-gap-1944/`. The η/f/τ
bands have not been swept on this arm. Both are logged in both banners.
