# `mach-dependent-fragment-drag` — CLOSED, partially retired

**Status: closed 2026-08-03. Half retired, half live. No further work planned
in this folder.**

This update was opened to close a *B(r)* over-prediction that turned out not to
exist, and it adjudicated a physics question on data that turned out to be the
wrong column. It nevertheless produced the drag anchor the model ships. Those
two halves are separated below so a future reader cites the right one.

## Read this before citing anything here

| Half | Status | Where |
| --- | --- | --- |
| **Ballistic-density anchor** — identity (4), the geometric-admissibility argument, $C_D$ = 1.28, $C_\text{shape}$ = 2.0890 | **LIVE** | `derivation.md` §1–§4, §6, §8; `scoping.md` §2, §5 |
| **Mach-dependence adjudication** — the motive, and the rejection of $C_D(M)$ on accuracy grounds | **WITHDRAWN** | `derivation.md` §5, §7 L3; `scoping.md` §1, §3a-2, §4 opt 3 |

Both source documents carry a banner stating the split. `rebaseline-verdict.md`
holds the 15-claim register (8 sound, 4 shifted, 3 void) that ruled it, and
`challenges/source-data-audit/review-void-rulings.md` is the independent
verification of that ruling.

## Why it was retired

Two independent shocks, ruled separately:

- **The motive was void.** The Family-B *B(r)* gap was the model's casualty
    criterion compared against the mild-steel-perforation column. Against the
    genuine casualties columns Family B passes at nearly every tabulated range
    for all three shells (see [`../drag-gap-1944/b-vs-range.qmd`](../drag-gap-1944/b-vs-range.qmd)
    §Verdict), and the residual *inverts* sign with range — the "grows with
    range" signature that pointed at drag in the first place is an artifact of
    the column swap.
- **The evidence was wrong, and the comparison was unfair.** The $C_D(M)$
    curve came from `figure-3-digitized.md`, which under-states $C_D$ across
    Mach 1.0–2.2 — in the direction that weakens the rejected candidate. Worse,
    the comparison gave the constant a free fitted parameter and the Fig-3 curve
    none. Given both laws one scale freedom on the corrected
    `figure-3-drag-coefficient.csv`, the Mach law **wins** on both columns (see
    [`checks/mach-law-rebaseline.py`](checks/mach-law-rebaseline.py)).

## Why the anchor was not retired with it

The anchor rests on C4, which is pure geometry plus identity (4): the
pre-update combined constant implies a fragment denser than steel presenting
less area than an equal-mass sphere (see `derivation.md` §4). That argument
consumes no velocity data, no *B(r)*, no $C_D(M)$ curve and no $V_0$, so
neither shock reaches it. C5 was *confirmed* by the corrected CSV, which
reproduces the source's own tabulated values to three digits.
`src/arty/fragmentation.py` and change-log v0.9.0 cite this half, and it
holds.

## What replaced the withdrawn half

Nothing is re-derived. The **decision** not to model $C_D(M)$ stands, on a
different and narrower reason: both laws land inside the arrival-velocity
fidelity bar over the lethal-relevant band, so the advantage is immaterial at
the stated target, while the change would replace a closed-form λ with a
per-fragment ODE integration at every call site (see `_limitations.qmd`
limitation **15** for the comparison). That is a **logged assumption**, and it
is published where readers meet it — limitation **15** in `_limitations.qmd`.
It is not looked up here.

## If the Mach law is ever revisited

Open a fresh `updates/<slug>/` change scoped against the corrected
`doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/figure-3-drag-coefficient.csv`.
Do **not** repair §5 in place — its inputs, its dataset and its framing are all
superseded, and a reader who finds a repaired §5 has no way to tell which
generation of the argument they are reading.

Two things a fresh pass would inherit rather than re-pay for:

- `checks/mach-law-rebaseline.py` already re-runs both laws per column on the
    corrected CSV — the per-column RMS comparison lives there.
- $V_0$ is **unverified**. `V0_FTS` (75mm 3120, 105mm 3500, 155mm 3500 ft/s) is
    not present in the processed Ordnance source and was carried over without
    provenance. A 10% $V_0$ error is comparable to the entire RMS at the adopted
    constant and is degenerate with the drag constant itself, so any re-opened
    comparison should settle $V_0$ first or it will re-run the same
    under-determined fit.

## Retained scripts

`checks/` is kept in full per `.claude/rules/verification-scripts.md` — the
scripts behind withdrawn numbers are the record of what was actually run, and
`mach-law-rebaseline.py` is the one a future pass starts from. Several
hard-code superseded values; that is expected of a record and is not repaired.
