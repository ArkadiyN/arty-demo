# Challenges — fragmentation-field

Each subdirectory is one **investigation thread**: a question chased across
several documents, with the check scripts that produced its numbers. Threads
are permanent — they publish a verdict that informs readers, and later passes
re-read them instead of re-deriving.

Layout inside a thread:

- `README.md` — thread index and current verdict (multi-document threads only)
- `*.md` / `*.qmd` — the challenge write-ups, in the order they were run
- `checks/*.py` — the scripts that produced the numbers, kept and runnable

## Threads

| Thread                                      | Question                                                                                         | Status                                                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [`drag-gap-1944/`](drag-gap-1944/README.md) | Does Family B reproduce the 1944 Ordnance Dept. B-vs-range data — and if not, is drag the cause? | **Closed** → `updates/mach-dependent-fragment-drag/`; residual sits at the geometric ceiling, not chased further |
| [`mott-scale-gap/`](mott-scale-gap/)        | Is `mott_params` an order of magnitude too small?                                                | **Resolved** → `updates/mott-fragment-shape-closure/`                                                            |
| [`gravity-ke/`](gravity-ke/gravity.qmd)     | Does omitting gravity matter for fragment KE?                                                    | **Closed** — no (≤0.003 % inside the 0–100 m envelope)                                                           |

## `mott-scale-gap/`

Three working notes, run in order:

- [`mott-scale-gap/_params_provenance_note.md`](mott-scale-gap/_params_provenance_note.md) — what `mott_params` is and where its values came from
- [`mott-scale-gap/_scale_verdict_ledger.md`](mott-scale-gap/_scale_verdict_ledger.md) — the gap is real; γ/σ_f is *not* the cause; localises it to the mass closure
- [`mott-scale-gap/_shape_closure_check.md`](mott-scale-gap/_shape_closure_check.md) — verdict **NO**: the cube closure is the model author's simplification, not the cited literature's

No `checks/` directory: the scripts behind these notes
(`mott_scale_check.py`, `mott_shape_closure.py`) were written before the
retention rule and were never committed — they are lost. The numbers survive
only as reported in the notes. Reproducing them means rewriting the scripts,
which is exactly the cost the retention rule exists to prevent.
