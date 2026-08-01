# Review: `drag-gap-1944/b-vs-range` (Family B vs. 1944 Ordnance Dept. B-vs-range data)

**Reviewed:** `b-vs-range.qmd` (+ rendered `.html`),
`b-vs-range.md`, `checks/b-vs-range-{75mm,105mm,155mm}.py`,
source tables in `doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md`
and `card.md`.

## Verdict: PASS-with-limitations

The reduction formula (Eq. 1: ring-sample + azimuthal average + unit
conversion) is dimensionally sound, matches the card's own definition of $B$
("averaged over different azimuthal directions from the burst", `card.md`
line 15), and is implemented correctly (meshgrid axis order, ring containment
inside the field domain, no leaked physics — see below). The headline
quantitative FAIL verdict (7-34x over-prediction, growing with range) is
real, reproducible (independently re-run below), and correctly reported
against the scoping doc's factor-of-2 criterion. One genuine data-
transcription defect was found (75mm, r=40 ft row) that was missed during
the pass; it does not change the FAIL verdict or the reported order of
magnitude, so it is not blocking, but it should be corrected and is logged
below along with a documentation misattribution.

## Findings

### 1. Material-but-deferrable (recommend direct fix, not just a logged limitation): 75mm Table 43 transcription error at r=40 ft

`ordnance-1944.md` interleaves Table 44 (perforation) and Table 43
(casualties) row-by-row from a two-column OCR scan, exactly as the 105mm and
155mm scratch scripts document for their own tables. The 75mm script
(`checks/b-vs-range-75mm.py`) identifies the casualties column
correctly for every row **except r=40 ft**, where the raw text reads:

```
ordnance-1944.md:396   40   386   .0192   .082   2,010
ordnance-1944.md:397   40   750   .0375   .024   1,570
```

The current transcription (`CARD_B[2] = 0.0375`, i.e. line 397) is the
**perforation** value, not casualties. Cross-checking against the same two
invariants the 105mm script already uses to catch and fix its own r=100
swap (N monotonically decreasing with r within each table; B_casualties ≤
B_perforation at every shared r) shows line 397 is inconsistent with both:
taking line 397 as casualties makes N jump 442→750 (increase) between r=30
and r=40, and makes B_casualties (.0375) > B_perforation (.0192) — the only
row in the whole table where that inequality flips. Swapping in line 396
(N=386, B=.0192) restores strict monotonic N-decrease and
casualties≤perforation for both interleaved columns across all 10 rows, the
same signature the 105mm fix already relies on. **Correct value: `B_card` at
r=40 for 75mm M48 HE should be `0.0192`, not `0.0375`.**

**Impact:** the ratio at that one row changes from 4.63x to ≈9.05x (still
nowhere near the 2× band — no qualitative change to the FAIL verdict or
monotonicity check). The printed "ratio spans" statistic for 75mm
(`b-vs-range.html`: *"ratio spans 4.6x - 33.2x"*) is wrong as a
result and should read **7.4x - 33.2x** — which, note, is what the
**Key Findings** narrative table two sections later already states
(*"75 mm M48 HE ... ~7x – 33x"*, qmd line 249). That is, the prose summary
already reports (probably by eyeballing rather than reading the computed
statistic) the number that the corrected data would produce, while the
printed validation-cell output does not — an internal inconsistency between
two parts of the same rendered notebook that would tip a careful reader off
even without checking the source.

Suggested correction (not applied): in both
`experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-75mm.py` and the
`CARD_DATA["75mm M48 HE"]["B"]` array in the `.qmd`, change the r=40 entry
from `0.0375` to `0.0192`; add a docstring note analogous to the 105mm
script's, documenting the swap and citing lines 396-397.

### 2. Deferrable (documentation/source-attribution only, no output change): `E_LETH_DEFAULT` misattribution

Both the `.qmd` (lines 52-56) and the scoping doc (lines 68-74) state that
the card's 58 ft-lb casualty threshold "already" is
`E_LETH_DEFAULT` in `src/arty/fragmentation.py`, "converted to joules below,"
and that "no new threshold parameter is introduced." This is factually
wrong: `E_LETH_DEFAULT = 1000.0` J (`src/arty/fragmentation.py:439`,
documented there as the ES-310 $P_{k\mid hit}=0.5$ "moderate personnel kill"
anchor — a different physical basis entirely, ≈737 ft-lb, not 58). There is
no "58 ft-lb" or "78.6 J" constant anywhere in `src/arty/` (grepped, zero
hits) — the value is introduced fresh in this notebook
(`E_LETH_58FTLB_J = 58.0 * FT_LB_TO_J`) and passed as an explicit override to
`four_zone_lethal_density_field`'s existing `E_leth` keyword, correctly
displacing the unrelated 1000 J default.

The actual **computation is correct** — the code passes 78.64 J, matching
the card's own definition (`card.md` line 25, "Casualty: Hit with ≥58 ft-lb
kinetic energy"), which is the right thing to do for this comparison. This
finding is about the prose only: the Parameters table lower in the same
`.qmd` (line 71) correctly attributes the source as "card's casualty
definition, converted to SI" with no mention of `E_LETH_DEFAULT` — so the
document contradicts itself on where this constant comes from. This is a
legitimate use of an existing function parameter with a card-sourced value
(not a Gate-2 violation, analogous to transcribing `CARD_DATA`), but the
"no new threshold parameter is introduced" / "already the project's
constant" framing should be corrected to state plainly that this notebook
overrides the app's own different default (1000 J, ES-310-derived) with the
card's literal 58 ft-lb definition, to match the historical source being
compared against.

**Impact:** none on any rendered number — purely a source-attribution
correction to prose in two files.

### Note (no action required)

- `FT2_PER_M2` is defined but unused in all three `_scratch` scripts —
    harmless dead code.
- The 75mm ratio series is non-monotonic at its tail (r=190: 33.2x, then
    r=225: 19.7x, both drop from card values that round to the same `0.0001`
    at 4-decimal precision) and the 155mm series dips similarly at its last
    point (r=300: 34.2x → r=400: 29.7x). This is a card-rounding artifact, not
    a model or transcription defect, and the qmd's "grows with range" language
    is a defensible general characterization, not a strict per-row claim.

## Verified independently

- Re-ran all three `checks/b-vs-range-*.py` scripts
    (`uv run python ...`); reproduced the exact ratios reported in the `.qmd`'s
    tables and the Key Findings summary (except for the finding-1 discrepancy
    above).
- Cross-checked all three shells' `CARD_R_FT`/`CARD_B` transcriptions,
    row-by-row, against the raw OCR text at the cited line ranges in
    `ordnance-1944.md` (75mm: lines 381-411; 105mm: lines 725-759; 155mm: lines
    874-907), including both documented column-identity/transposition fixes
    (105mm r=100 swap; 155mm reversed "TABLE 60"/"TABLE 59" header order) — both
    confirmed correct against source.
- Confirmed `card.md`'s explicit statement that $B$ is azimuthally averaged
    (line 15), validating the notebook's Eq. (1) reduction as the right
    comparison convention, not an invented one.
- Confirmed the `.qmd`'s `RegularGridInterpolator` axis order
    (`(Y[:, 0], X[0, :])`, query stacked as `[ys, xs]`) matches
    `four_zone_lethal_density_field`'s meshgrid convention (X varies along
    columns, Y along rows) — no axis-swap bug.
- Confirmed the sampling ring (radius $r$) is always strictly inside the
    field domain (`max_r = 1.25r`) for every query, so no boundary
    fill-value clipping affects any tabulated point.
- Confirmed no Family A code appears in the `.qmd` (matches its own scope
    note deferring the Family A reduction to a follow-up pass) and no physics/
    parameter values beyond straightforward unit conversion, ring-averaging,
    and calls into existing `arty.zones`/`arty.shells` functions — Gate 2
    compliant.
- Confirmed `delta_deg=15.0`, `E_leth` keyword, and the four-zone builder's
    signature all match `src/arty/zones.py::four_zone_lethal_density_field`
    current defaults/parameters (no drift from source).
- Confirmed no AoF/striking-condition field exists on `ShellParams`
    (`src/arty/shells.py`), validating the "not carried in the registry, hence
    swept" fallback claim.

## What to log

- A fix (not a limitation) for finding 1: correct the 75mm r=40 `B_card`
    entry to `0.0192` in both the `.qmd` and its `_scratch` script, and update
    the printed "ratio spans" statistic and Key Findings table's stated 75mm
    ratio-range accordingly (the Key Findings prose number, ~7x-33x, already
    happens to be correct post-fix; only the computed-and-printed 4.6x needs
    to change).
- A prose fix (not a limitation) for finding 2: remove the
    `E_LETH_DEFAULT`/"no new threshold parameter" framing in both the `.qmd`
    and the scoping doc; state instead that the notebook overrides the
    project's default lethal-energy threshold (1000 J, ES-310 anchor) with the
    card's own literal 58 ft-lb (≈78.6 J) casualty definition, sourced from
    `card.md`, to match the historical comparison.
