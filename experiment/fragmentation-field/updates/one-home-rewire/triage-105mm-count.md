# Triage: 105mm B-vs-range in-band count, 9/11 vs 10/11

Pass: correctness / verification (modeler), 2026-09-26. No document edited.

## Findings so far

1. **Same criterion, rows, band, AoF.** The re-wired key-findings table
   (working tree `b-vs-range.qmd`, cell "Summary variables for inline wiring")
   counts `ratio (model/card)` from the notebook's own `results` dict — built
   at `AOF_PRIMARY_DEG = 30`, against the per-caliber `CARD_R_FT`/`CARD_B`
   rows (10/11/11 rows), inclusive band `[0.5, 2.0]`. The committed notebook's
   own validation cell (line ~229, `(ratio >= 0.5) & (ratio <= 2.0)`) uses the
   identical criterion. `checks/b-vs-range-drag-attribution.py` also uses the
   per-caliber modules at `AOF_PRIMARY_DEG` and the same band. No criterion
   difference exists between the typed and the code-built tables.
2. **Current shipped model gives 8/10, 10/11, 11/11.** Re-running
   `checks/b-vs-range-drag-attribution.py` at HEAD src/arty writes
   `checks/b-vs-range-drag-attribution.results.json`: 75mm 8/10 (0.224x –
   1.274x), 105mm 10/11 (0.415x – 1.283x), 155mm 11/11 (0.659x – 1.012x).
   The typed table's ratio spans (0.17–1.51, 0.34–1.74, 0.67–1.42) differ from
   these for all three shells, so the typed table is a snapshot of an earlier
   model state, not a different criterion.
3. The typed triple was authored in commit a01eb33 (2026-08-08). src/arty
   commits after it that touch the fragment count / mass chain: 86b1230
   (75mm case mass, merged via 2c34812), 3a5d800 (perforation E_thr), 74abdd7
   (break-up velocity fraction in Mott x0/mu), 5d742b4 / 630dac8 / 18cd069
   (Mott shape c, k, kappa_x triple). Bisection below.

## Verdict: typed table is STALE; the code-built 10/11 is correct

Bisection script: `experiment/fragmentation-field/updates/one-home-rewire/checks/b-vs-range-count-bisect.py`
(extracts each commit's `src/arty` via `git archive`, re-runs the current
per-caliber check modules at AoF 30 deg and shipped `DragParams()`; ~15 s).
The per-caliber `CARD_*` data in `challenges/drag-gap-1944/checks/` have not
changed since a01eb33, so only the model moves.

| src/arty at | 75mm | 105mm | 155mm | 105mm ratio at r=400 ft |
| --- | --- | --- | --- | --- |
| a01eb33 (typed table authored) | 8/10 (0.17–1.51) | 9/11 (0.34–1.74) | 11/11 (0.67–1.42) | 0.488 (fails) |
| 2c34812, cf402a8, 3a5d800, 74abdd7 | same as a01eb33 to 3 d.p. | same | same | 0.488 |
| **5d742b4** (per-shell aspect-ratio moment c) | 8/10 (0.16–1.52) | **10/11** (0.36–1.62) | 11/11 (0.67–1.19) | **0.503** (passes) |
| 630dac8 (per-shell k) | 8/10 (0.19–1.41) | 10/11 (0.38–1.51) | 11/11 (0.67–1.17) | 0.515 |
| 18cd069 = HEAD (kappa_x/k/c re-solve, v0.15.0) | 8/10 (0.22–1.27) | 10/11 (0.41–1.28) | 11/11 (0.66–1.01) | 0.534 |

- The a01eb33 row reproduces the typed table exactly (counts and spans), so the
  typed figures were right when written and use the same criterion as the
  code-built table.
- **The change that moved it: 5d742b4** (2026-08-16, per-shell aspect-ratio
  moment correction c in the SHELLS registry). It lifts the 105mm r=400 ft
  ratio from 0.488 to 0.503, just across the 0.5 bar; 630dac8 and 18cd069
  push it further in (0.534 at HEAD), so the crossing is no longer marginal.
  Only r=500 ft (0.415) fails at HEAD.
- 74abdd7 (break-up velocity fraction) and 3a5d800 (perforation E_thr) leave
  the B ratios unchanged at 3 d.p.
- **75mm and 155mm counts agree** (8/10, 11/11) at every commit, but their
  ratio spans moved: 75mm 0.17–1.51 -> 0.22–1.27; 155mm 0.67–1.42 -> 0.66–1.01.
  75mm's failing ranges are still r=300 and 400 ft (0.435, 0.224), so the prose
  "75mm: r=300-400 ft" still holds. The typed "worst case ~1/0.17 ≈ 5.9x" is
  now ~1/0.22 ≈ 4.5x.
- The PASS verdict is unaffected in direction (the count went up, not down),
  but every published copy of "9/11", the 105mm span 0.34–1.74, "105mm:
  r=400-500 ft", the 75mm/155mm spans, and the 5.9x worst case is stale.

## Documents carrying stale copies (for the doc-sync pass)

Live surfaces (need updating or replacing with a link):
- `experiment/fragmentation-field/_validation.qmd:201` — "105mm 9/11".
- `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md:335` — "8/10, 9/11 and 11/11".
- `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/rebaseline-verdict.md:12,58` — same triple.
- `experiment/fragmentation-field/challenges/source-data-audit/stale-surfaces.md:32` — same triple.
- `experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range.qmd:308` — "105mm: r=400-500 ft" (carried a blocking marker at :314, since resolved); also the working-tree column header "Ratio range, v0.9.0 (2.674, shipped)" labels HEAD (v0.15.0) ratios as v0.9.0.

Dated records (exempt from one-home per c2e8e67; at most a "superseded, see …" pointer):
- `experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-rebaseline.md:42,85,140-141` — a still-earlier state (105mm 0.30–1.99), pre-a01eb33.

grep for "9/11", "8/10", "1.74x", "0.34x", "400-500 ft" over `experiment/` and
`openspec/` found only the above; I did not find ~13 copies. The drag-gap-1944
`README.md` carries none of these strings (surface: grep of that file only).
