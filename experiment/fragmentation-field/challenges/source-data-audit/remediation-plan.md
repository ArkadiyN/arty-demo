# Remediation plan — working the source-data audit down

**Written for a session with no prior context.** You do not need to have run the
audit, and you should not try to reconstruct it. Everything you need is either
in this file or reachable by one command from it.

The audit found and classified the defects; it deliberately did not repair them.
This file is how the repairs get done, one bounded session at a time, without
re-deriving what is already settled.

______________________________________________________________________

## 0 · The one thing to understand before starting

**The register is the work queue. This file is only the ordering and the rules.**

```
uv run python src/utils/collect-findings.py --for <path>
```

`OPEN-FINDINGS.md` is generated from `FINDING` markers living next to the
defects they describe. It is always current; a hand-written task list in this
file would not be. So this plan never enumerates the work — it tells you which
query to run and in what order to work the results.

A finding is closed by **deleting its marker at the source**, never by editing
the register. Then regenerate and stage:

```
uv run python src/utils/collect-findings.py
```

Pre-commit fails if you forget.

______________________________________________________________________

## 1 · Cold start — 5 minutes, in this order

1. `experiment/fragmentation-field/challenges/source-data-audit/README.md` —
    what the audit was and what each of its files holds.
1. `uv run python src/utils/collect-findings.py --for <the surface you picked  from §3>` — the actual work, with each finding's evidence path.
1. Only the ledger sections a finding cites (`§17b`, `§34a`, …). Find them with
    `grep -n '^#' ledger.md`.

**Do not read `ledger.md`, `review-provenance.md`, or `review-criterion-match.md`
sequentially.** They are 242 KB / 43 KB / 25 KB of evidence indexed for
citation. Reading them cold is the documented way to burn a session's whole
budget before writing anything
(`.claude/rules/subagent-harness.md`, over-read exhaustion).

**Do not re-audit.** Phases 3 and 5 already classified every downstream claim
sound / shifted / void, and Phase 5 adversarially re-checked every void ruling.
If you find yourself re-deriving a verdict, stop — read the verdict.

______________________________________________________________________

## 2 · The gates that bind, before you touch anything

These are not this plan's rules; they are the project's, and they are why the
work is shaped the way it is below.

- **Worktree first.** Never work in the primary checkout
    (`.claude/rules/git-flow.md`). Call `EnterWorktree`.
- **You do not write physics.** Every item in §3.1 and most of §3.2 is a
    physical or derived quantity. `agents-routing.md` Gate 2 puts all of it in
    `src/arty/` via @modeler, through Workflow B (model-workflow skill). **The
    main agent's job here is to decide, brief, and verify — not to edit
    `src/arty/`.** Editing a constant directly because "the correct value is
    right there in the finding" is the gate violation.
- **One dispatch per pass.** Gate 4 — never `SendMessage` a modelling agent to
    advance a workflow. Fix and re-review are separate fresh dispatches briefed
    from `review.md`.
- **Brief by reference.** Put
    `uv run python src/utils/collect-findings.py --for <scope>` in the dispatch
    prompt and let the agent read its own findings. Paraphrasing them costs
    top-tier output tokens and has already dropped one blocking finding.
- **Re-tier on return.** A brief that forbids `src/arty/` caps the severity the
    pass can assign (`.claude/rules/deferred-findings.md`). Check any
    `deferrable` it returns whose `affects:` paths sit inside the restriction
    you imposed.
- **Check scripts are permanent.** Anything producing a number that lands in a
    committed document goes to `<artifact>/checks/`, committed with it
    (`.claude/rules/verification-scripts.md`). The audit's 36 are there; reuse
    them rather than writing new ones.

______________________________________________________________________

## 3 · The queue — ordered by exposure, not by severity tag

Severity tags were assigned by passes with capped scope, so they under-rank
systematically. **Exposure is the reliable ordering**: how far a wrong number
travels before a human sees it.

Counts below were current at 2026-08-04; re-run the query rather than trusting
them.

### 3.1 · Shipped code — 12 findings, 4 blocking

```
uv run python src/utils/collect-findings.py --for src/arty
uv run python src/utils/collect-findings.py --for app
```

The only place a wrong number is **executing**. Everything else is a document
that misleads a reader; this is a model that computes wrong.

Route: **Workflow B per aspect** (model-workflow skill). One `updates/<slug>/`
per aspect — do not bundle. Each blocking item is its own aspect; they touch
`shells.py`, `zones.py` and `fragmentation.py` independently.

Exit per item: the quantity is corrected in `src/arty/`, `derivation.md` records
why, @model-reviewer PASSes, the notebook reflects it, the marker is deleted.

### 3.2 · The reader-facing notebook — 14 findings, 7 blocking

```
uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/_validation.qmd
uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/_limitations.qmd
```

Read `stale-surfaces.md` first — it is exactly this inventory, with each claim
as published, what the re-baseline did to it, and which artifact carries the
corrected reading. It is ordered by reader exposure already.

Two are worth naming because they are the sharpest: `_validation.qmd` **Check 7**
labels the ordnance tables 43/51/59, which are the extraction's numbering and
resolve to a different shell in the source; **Check 5b** hard-asserts a PASS
against a source the audit recorded UNVERIFIABLE (§29).

Route: a `.qmd` carries **no physics** — if a corrected number is needed and
`arty` does not return it, that is Gate 2 and §3.1 work first. Otherwise this is
a @modeler notebook pass: edit the partial, re-render, change-log entry.

**Sequencing:** most of §3.2 depends on §3.1. Do not repair a published number
that a pending `src/arty/` fix will move again — check whether the claim's
source quantity is in the §3.1 queue before editing it.

### 3.3 · Audit and challenge artifacts — 23 findings

```
uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/challenges
uv run python src/utils/collect-findings.py --for experiment/fragmentation-field/updates
```

Mostly check scripts reading the wrong column or hand-typing a series that now
has a CSV. Lower exposure — these are read by the next audit, not by a user —
but they are what a future pass will trust, so a wrong one re-seeds the defect.

Route: mechanical for the hand-typed-array cases (point the script at
`tables/<slug>.csv`, re-run, confirm the number it produced is unchanged or
update the citing document). Physics only if the conclusion moves — then Gate 3.

### 3.4 · `doc-reference/` internals — 26 findings

```
uv run python src/utils/collect-findings.py --for doc-reference
```

Card and extraction defects with no live consumer. Safe to leave; cheap to
close. Good work for a short session. @librarian handles these (cheap model),
but **never authors a closure invariant** — the dispatcher does
(`.claude/rules/source-data-fidelity.md`).

______________________________________________________________________

## 4 · How to close a finding honestly

A finding is closed when the **defect** is gone, not when one of its `affects:`
paths is fixed.

- **Multi-path finding, one leg repaired** → narrow the marker to the paths
    still carrying it. Do not delete it.
- **Finding turns out to be wrong** → delete it and say why in the commit
    message. This has happened: two findings in this audit were false verdicts
    produced by searching a derived surface.
- **Finding is real but you are not doing it** → leave it. That is what
    `deferrable` means and the register is the routing.
- **Finding is `blocking`** → it may not be closed by deferral at all
    (`.claude/rules/deferred-findings.md`). Only the human decides it can wait.

______________________________________________________________________

## 5 · Session-end checklist

- [ ] `experiment/_scratch/` is empty — every retained script `git mv`-ed into a
    `checks/` folder next to the artifact citing it.
- [ ] `uv run python src/utils/collect-findings.py` run and staged.
- [ ] `uv run src/utils/check-table-invariants.py doc-reference/ --all` still
    passes (was 0/28 failed at audit close).
- [ ] Notebook re-rendered if a `.qmd` changed.
- [ ] One logical unit per commit, Conventional Commits, squashed.
- [ ] Anything you deferred left a `FINDING` marker — not a note in a
    document nobody reads.

______________________________________________________________________

## 6 · Stop and ask the human

- A `blocking` finding whose repair you cannot verify — blocking findings are
    the human's call by rule, not yours to downgrade.
- Two dispatches on the same scope returning zero artifact bytes — that is a
    read-bound loop, not bad luck (`.claude/rules/subagent-harness.md`). Do not
    fire a third.
- A repair that would change a **published verdict** in `challenges/README.md`
    or the rendered notebook, rather than a number inside one.
- A source that needs re-acquiring. Several documents in this repo are
    unverifiable only because nobody has the scan; the human may have it — one
    such request during the audit turned a document recorded un-re-baselineable
    into a routine one.

______________________________________________________________________

## 7 · Out of scope — do not do these

- **Re-auditing.** The classification is done and adversarially reviewed.
- **Widening a repair into a redesign.** If a fix reveals a modelling question,
    register it as a finding and stop; the audit's own scope discipline is why
    it finished.
- **Reopening the workflow rules.** Phase 8 landed them and they are in force.
    If one is wrong, `.claude/incidents.md` holds the evidence behind each —
    argue from that, and only when you are about to break one.

______________________________________________________________________

## 8 · When this plan is done

When `OPEN-FINDINGS.md` reports **0 blocking**, the audit's substantive work is
discharged and the remaining `deferrable`/`note` entries are ordinary backlog.
That is the milestone worth reporting.

The real test comes after: **the next unrelated modelling pass is the regression
test for the workflow fixes.** Watch whether the new gates actually fire — a
closure invariant demanded before a table is cited, an anchor grepped when it is
written, a card that refers a transfer question instead of answering it, a
librarian that reports "not found in `<file>`" instead of "the source does not
say it". If a pass sails through without any of them binding, the fixes are
decoration and that is worth knowing.
