# Review — shell case-mass basis (scoping + derivation, pre-implementation)

Reviewer pass. Scope: `scoping.md`, `derivation.md`, `checks/*.py`, and the new
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/round-weights.{csv,invariant}`.
No `src/arty/` edits exist yet (confirmed via `git status`) — this is a
pre-implementation review of the derivation, per the model-workflow skill.

`collect-findings.py --for experiment/fragmentation-field/updates/shell-case-mass-basis`
returned no open findings scoped to this folder. One new `deferrable` finding
was raised *by this pass* against a different scope
(`_parameters.qmd` literal-ShellParams drift) — correctly filed with
`affects:` pointing outward, not swallowed into this document's own scope.

## Verdict: **PASS**

No blocking findings. Two note-level (cosmetic, zero output impact) items
below; no action required, listed for completeness.

## What I verified mechanically

- `uv run src/utils/check-table-invariants.py .../round-weights.invariant` →
  **4 rows, 1 check, ok**. Confirms the closure `loaded_unfuzed − TNT + fuze
  = empty_and_fuze` holds on all four rounds and recovers the OCR-damaged
  glyphs claimed in the text.
- `uv run .../checks/tolch-round-weight-closure.py` and
  `uv run .../checks/registry-case-mass-consistency.py` both run clean and
  reproduce every number quoted in `derivation.md` §2/§4/§5/§7 to the last
  printed digit (M_case 4.9623 kg exact vs Tolch, +16.0% shipped error,
  V0 807.5→890.2, μ 793.29→652.70 mg, N0 3627.4→3801.4, +4.8%). Both scripts
  read the round-weight series from the CSV (`csv.DictReader` /
  `tolch_nominal_kg()`), never a hand-typed literal array — satisfies the
  source-data-fidelity numbers-extracted-once rule.
- Re-derived the Mott/Gurney chain from `fragmentation.py` by hand: with
  `x0 ∝ 1/V0`, `alpha ∝ V0`, `gamma = alpha^{-2/3} gamma' ∝ V0^{-2/3}`,
  `mu ∝ (sigma_f/gamma)^{1.5} (r_bu/V0)^3 ∝ V0^{-2}` — matches
  `derivation.md` eq. (4) exactly, and the script's central-finite-difference
  check confirms eq. (6)'s analytic log-sensitivities to 4 d.p. on every row.
  This is the derivation's central, non-obvious claim (scoping's own "16%
  error → 16% N0 error" propagation statement is wrong, and the derivation
  says so explicitly and re-derives it) — I re-derived it independently
  rather than trusting the script's self-report, and it holds.
- Cross-checked provenance: `tolch-1938.md:232` matches the table exactly as
  cited; the "mostly pieces of fuze" (~15%, screen 1), "60% of weight of
  empty shell and fuze," and "779 fragments... 95.c% of weight" anchors all
  resolve to the claimed lines and support the reading given in §3/§7. This
  is a primary source cited directly (BRL Report 126 itself), not attributed
  through an intermediate paper — no secondhand-attribution concern.
  `pit-screen-recovery.invariant` (pre-existing, independent extraction) also
  passes and its cross-check divisor (mean 13.29 lb) agrees with this table's
  four values — a genuine independent-column agreement, not a self-reference.
- Confirmed the "fuze cancels in Option B" robustness claim algebraically:
  `M_case = (loaded + fuze) − TNT − fuze = loaded − TNT`, independent of the
  disputed fuze glyph. Correct and non-trivial — it is exactly what makes the
  case-metal number robust to the one genuinely uncertain digit in the table.
- Criterion match: the model's `mass_shell` is consumed only by Gurney (M in
  the cylinder work equation) and Mott (wall break-up population) — both
  radially-confined-wall quantities. Tolch's "loaded unfuzed shell − TNT" is
  the shell body with fuze and filler both removed, i.e. the same physical
  object. The derivation explicitly flags that this is *not* the same
  quantity as Tolch's raw recovered-fragment count (which includes fuze
  pieces), and correctly declines to close that comparison here, deferring
  it to `count-gap-1938` with the sign of the discrepancy noted as flipping.
  This is the correct application of the criterion-match gate: rather than
  silently comparing model N0 to a fuze-inclusive count, the pass identifies
  the mismatch and refuses to score against it.
- No physics/computation is inlined outside `src/arty/`-bound artifacts —
  this pass is scoping+derivation only, no `.qmd` touched, no `src/arty/`
  edits (`git status` confirms only `doc-reference/`, `updates/`, and
  unrelated `agent-memory` changes).

## Findings

**[Note] `derivation.md:177` C/M band text (0.10–0.20) contradicts its own
family table on the same line.** The prose says 75mm's C/M=0.1426 "is inside
the 0.10–0.20 band ... 60mm 0.204, 105mm 0.181, 155mm 0.198" — but 0.204 >
0.20, i.e. the cited band excludes one of the four values used to illustrate
it. The actual check script (`checks/registry-case-mass-consistency.py:41`)
uses `CM_LO, CM_HI = 0.10, 0.25`, which the 60mm value satisfies. The
computed numbers and the pass/fail verdict are unaffected — only the prose
band bound is wrong. Impact: zero on any rendered output; purely a
documentation inconsistency. Suggested correction: change "0.10–0.20" to
"0.10–0.25" in `derivation.md` §7 point 3 to match the script it cites.

**[Note] `derivation.md:112` prints `mass_total` = 6.7359, script computes
6.7358.** `14.85 lb × 0.45359237 kg/lb = 6.735847 kg`, which rounds to 6.7358
(matches `checks/registry-case-mass-consistency.py` output), not 6.7359.
0.1 g difference, <0.001% — no effect on any downstream number since the
checks and (eventually) `src/arty/shells.py` will read/compute the value
directly, not copy the markdown table. Note only.

**[Note] The new `round-weights.csv`/`.invariant` table is not yet
referenced in `doc-reference/.../tolch-1938-m48-panel-pit-fragmentation/card.md`.**
The sibling `base-spray-density`, `nose-spray-density`, `side-spray-density`,
and `pit-screen-recovery` tables all have a card.md section (caption,
columns, closure summary); this pass's new table does not. The mechanical
provenance is fully present in the `.invariant` file itself (caption anchor,
column definitions, closure math, OCR-damage explanation, cross-check), so
nothing is under-sourced — this is a navigability gap for a future reader
who starts from `card.md` rather than `derivation.md`, not a fidelity gap.
Zero effect on any computed output. Suggested correction (not required for
this pass to close): add a short "Round Weight Breakdown" mechanical section
to `card.md` mirroring the existing table sections, in a later pass that
touches this card.

## Scope items correctly deferred, not closed

- **105mm M1 / 155mm M107 `mass_deductions`** remain unsourced placeholders,
  closed here on a bounded, logged assumption (A1) rather than a guess or a
  silent pass. The derivation tightens the scoping pass's own (linear, and
  shown wrong) exposure estimate from ~4%/~3% down to 0.35%/0.26% using the
  same sensitivity relation (eq. 7) validated against the shipped code —
  self-consistent and appropriately conservative language ("retained pending
  the librarian request").
- **`count-gap-1938` reconciliation** is explicitly named as required
  follow-on work, not swept into this pass, with the sign-flip consequence
  (16% high, not 4.5% low) stated up front so the next pass isn't surprised.
- **Option C (explicit `mass_case` field)** is deferred with a stated
  revisit trigger, consistent with keeping this pass to the smallest
  closeable scope.

## Assessment of the scoping→derivation self-correction

Worth calling out explicitly: `derivation.md` §5 identifies and corrects an
error in its own `scoping.md` (the claimed linear N0-vs-M_case sensitivity),
backs the correction with both an independent analytic derivation and a
finite-difference check against the live `src/arty/` code, and then uses the
corrected (much smaller) sensitivity to re-close the 105mm/155mm assumption
bound tighter than the scoping pass could support. This is exactly the kind
of self-checking a derivation pass should do rather than carrying a scoping
pass's error downstream unexamined, and I independently re-derived it above
rather than taking the script's agreement at face value.
