# Phase 4b — does the shipped Mach-drag calibration survive the Tolch-1938 re-baseline?

**Status: IN PROGRESS — source-side groundwork closed, verdicts not yet
written.** Escalated to the human after three @modeler dispatches (~235k
subagent tokens); see "Dispatch history" below before spending a fourth.

## Dispatch history (why this file is unfinished)

Written by the main agent, not a modelling pass — bookkeeping only, no physics.

1. **Pass 1** — 20 read/grep calls, no `Write`, zero artifact. Over-read
    exhaustion; window discarded, re-dispatched fresh.
1. **Pass 2** — wrote F0 below and
    [`checks/tolch-side-spray-closure.py`](checks/tolch-side-spray-closure.py)
    (0 failures: side-spray component sums close; the source's own stated
    Panel A→D perforating losses of 44% / 19% / 33% reproduce; the update's
    `RATIO_OBS` 0.557 reproduces at 0.5570).
1. **Pass 3** — wrote
    [`checks/tolch-count-basis-closure.py`](checks/tolch-count-basis-closure.py),
    which **found two defects**: the side-spray series fails component-sum
    closure at v=1085 f/s on panels A/B/C, and the pit-test recovered count is
    803 in committed artifacts against 779 in the report's own screen table and
    body text. It did not append to this file before its budget ran out.
1. **Side-spray closure resolved by the main agent** (not a modelling pass).
    The table was never extracted into `tables/`; both scripts held it as a
    literal typed off the garbled text layer. Re-extracted through the fixed
    single-page vision path to
    `tables/side-spray-density.csv` — **all 20 cells close exactly**, so the
    failure was the transcription, not the source. That finding is closed; the
    803-vs-779 one remains open in `ledger.md` §10. Both scripts now read the
    CSV. Details in `ledger.md` §6, "2b, second sitting".

**Diagnosis for whoever picks this up:** this is not a read-bound loop — every
pass after the first produced real, durable, correct output. The output kept
landing in a *check script* rather than in this assessment. The remaining work
is the verdict layer (provenance → sound/shifted/void per consumed number →
does the update's overall position hold), which the two retained scripts now
have the arithmetic for. Brief the next pass to read those two scripts' output
and write verdicts only; it should not need to compute anything new.

Scope: `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/`.
Assess only; no `src/arty/` or update-artifact edits (deferred by design).

## Findings ledger

### F0. The corrected Tolch series (what consumers must now read)

`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/`
holds two re-baselined CSVs, extracted once off the page images:

- `base-spray-density.csv` — anchor `Number of perforations, penetrations, and dents of the`,
    source.pdf p.41-42 (report pages -19-, -20-). 17 rows: `v_fps, panel, perf, penet, dents, total`.
- `nose-spray-density.csv` — same schema, 17 rows.

Closure invariant on both: `perf + penet + dents - total == 0 within 0.02`,
holding exactly on all 17 cells of each table.

Two facts that already constrain this assessment, stated in
`base-spray-density.invariant`:

1. `v_fps` is **the shell's average remaining velocity at burst** — a firing
    condition, not a fragment velocity. `v_fps = 0` is the source's "Static" row.
1. `../tolch-1938.md` (the vision extraction) is **wrong in ~20 of 54 component
    cells**; the CSVs are the authority. Any update artifact whose Tolch numbers
    trace to the markdown is on corrupted provenance.
