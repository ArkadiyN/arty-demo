---
name: mott-table-nonuniform-carbon-spacing
description: Mott 1947 p.308 composition table rows are NOT evenly spaced (0, 0.1, 0.25, 0.45 %C) — don't assume 0.1-step spacing when bracketing a %C for gamma interpolation
metadata:
  type: project
---

Mott (1947) §3 p.308 table, after Körber & Rohland (1924), corrected reading:
iron 0.0%C→γ=20, steel 0.1%C→γ=42, 0.25%C→γ=53, 0.45%C→γ=67. The row spacing
is **non-uniform** — do not assume the historically-misread "0.1/0.2/0.3 %C,
γ=32/53/67" grid; that version was an OCR artifact (fixed 2026-07-25, see the
Extraction note at the top of
`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`).

**Consequence:** any composition inside 0.2–0.45 %C that was previously
treated as "beyond the table, needs extrapolation" (e.g. a ~0.35 %C baseline)
is actually **bracketed** by the real 0.25C/0.45C rows — interpolation, not
extrapolation. Re-check bracket endpoints against the source table directly
before reusing any prior interpolation, not just the endpoint γ values.

Also: the phrase "for mild steel … assume γ = 40" that a prior derivation
cited as independent corroboration does **not** appear anywhere in the
corrected source text — treat it as unverified if it resurfaces.

Flagged-but-unfixed as of this note:
`experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md` §2/§4/C6/C7
and `recompute.py`'s `MOTT_SERIES`/`gamma_quadratic` still use the old grid.
