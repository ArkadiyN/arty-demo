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

______________________________________________________________________

# Review: `shape-closure-orthogonality` (does the Mott shape-closure fix bear on the drag-calibration check?)

**Reviewed:** `shape-closure-orthogonality.md`,
`src/arty/fragmentation.py` (current, and the `b12f553` diff),
`checks/drag-coefficient-calibration.py`,
`drag-coefficient-calibration.md`,
`initial-conditions-75mm.md`, `src/arty/shells.py`.

## Verdict: PASS

This is a factual dependency-trace claim (not a derivation), so the review
focused on verifying the trace rather than physical plausibility. Every
specific claim checked out:

- Line numbers cited (`fragmentation.py:244-269`, `261`, `262`, `263-267`,
    `268`, `272-279`, `299-306`) match the current file exactly, character for
    character in content.
- `retardation_coeff`'s body (lines 272-279) references only `m`, `drag.rho_air`,
    `drag.C_D`, `drag.C_shape`, `rho_steel` — no `mu`, `N0`, `alpha`, `aspect_ratio`,
    or `breadth_factor` symbol appears anywhere in its body. Confirmed by reading
    the function directly, not just the doc's claim about it.
- The check script (`checks/drag-coefficient-calibration.py`) imports only
    `SHELLS`, `DragParams`, `retardation_coeff` — no `mott_params` import, no
    `mu`/`N0` reference anywhere in the file. The `m_oz` arrays are literal,
    hardcoded floats; spot-checked the 75mm array (`[0.014, 0.063, 0.244]`,
    `v_fts=[2060, 972, 494]`) against `initial-conditions-75mm.md`
    line 16 — matches verbatim.
- `git show b12f553 -- src/arty/fragmentation.py` confirms the shape-closure
    commit touched only `mott_params` (added `t_bu`, `x0`, `alpha`, `gamma`
    lines) and a docstring/comment on `STEELS`; `retardation_coeff` and
    `DragParams` are byte-identical before/after. `git show b12f553 --stat --   src/arty/shells.py` returns empty — the `SHELLS` registry (and hence
    `shell.steel.rho`, the one `arty` quantity the check script does consume)
    was untouched by the commit.
- Checked for any *other* code path that could carry the shape-closure output
    into `retardation_coeff`'s inputs, beyond what the assessment inspected:
    grepped the whole repo for `mott_params`/`retardation_coeff` co-occurrence.
    Found four production sites in `fragmentation.py`
    (`compute_frag_field` and three others near lines 1268/1381/1458) where
    both are called in the same function — but in every one, the masses passed
    to `retardation_coeff` are either the field's own mass grid (`m_grid`,
    for the KE/lethality field, independent of `mu`) or a fixed literal
    representative-mass list (`rep_masses_g = [0.5, 5.0, 50.0]`, `line 440`),
    never a value derived from `mu`/`N0`. So even a codebase-wide check (a
    broader claim than the assessment attempted) turns up no path from the
    shape-closure output to any `retardation_coeff` call, production or
    check-script. This strengthens, not weakens, the assessment's conclusion.
- The doc's "current (0.585)" figure matches `DragParams`'s live defaults
    (`C_D=0.65`, `C_shape=0.90`, product 0.585) — no drift.
- A related, earlier scratch script (`checks/shape-closure-orthogonality.py`,
    docstring: *"mu/N0 do not enter retardation_coeff"*) independently states
    the same finding — consistent corroboration, not a conflicting result.

No gap in the trace was found: the assessment's scope (this specific check)
is correctly bounded, and a broader repo-wide search (beyond what the
assessment itself checked) turns up the same answer.

## Findings

None — no Blocking, Deferrable, or Note-level issues.

## Verified independently

- Re-read `mott_params`, `retardation_coeff`, `compute_frag_field` and all
    other `mott_params`+`retardation_coeff` co-occurrence sites directly from
    `src/arty/fragmentation.py`.
- Diffed `b12f553` against `src/arty/fragmentation.py` and confirmed
    `src/arty/shells.py` was untouched.
- Re-read `checks/drag-coefficient-calibration.py` in
    full; confirmed no `arty` import beyond `SHELLS`, `DragParams`,
    `retardation_coeff`.
- Cross-checked the 75mm literal data triple against its cited source check
    file.

## What to log

Nothing — no limitation or correction to log for this artifact.

______________________________________________________________________

# Review: `b-vs-range-familyA` (Family A vs. 1944 Ordnance Dept. B-vs-range data)

**Reviewed:** `b-vs-range-familyA.md`, `checks/b-vs-range-familyA.py`,
`checks/b-vs-range-familyA-aof-ap.py`, `b-vs-range.md` §2 (the reduction this
implements), `src/arty/zones.py::_four_zone_familyA_eval`,
`src/arty/fragmentation.py::_belt_column_zrep_vec`/`presented_area`.

## Verdict: PASS-with-limitations

The reduction is a faithful implementation of `b-vs-range.md` §2's Family-A
rule (divide the field builder's own $A_p(\gamma)$ back out of $N(x,y)$), the
per-zone $A_p$-inversion is the correct handling of the fact that
`_four_zone_familyA_eval` relocates each zone's belt to its own $z_\text{rep}$
(so there is no single ground-point $A_p$ to divide by), all 33 tabulated
numbers reproduce exactly on independent re-run, and the write-up's central
"cancellation, not validation" argument is sound and, unusually for this
project, understates rather than overstates its own result (a numeric PASS is
correctly *not* claimed as a validated kernel). No Blocking findings. Two
Deferrable items (an already-logged-adjacent threshold-matched follow-up that
should be named explicitly as a limitation, one unused import) and one Note.

## Findings

### 1. Deferrable: the "cancellation, not validation" conclusion is correct but not yet captured in `_limitations.qmd`

The write-up (§5) explicitly declines to claim Family A is validated by this
comparison, and instead states the numeric PASS is the product of two
offsetting, threshold-confounded errors: Family B's 2-5x over-prediction
against the card's own 58 ft-lb threshold, times Family A's own ES-310 curve
being anchored ~10-13x stricter (`E_LETH_DEFAULT`/`_PK_E[1]` = 1000 J vs. the
card's 78.6 J). This algebraic identity ($B_A/B_\text{card} = (B_A/B_B) \times
(B_B/B_\text{card})$) is verified below and holds to rounding at every row.
The reasoning is physically grounded, not just curve-fitted: `pk_given_hit`
has **no** `E_leth` parameter at all (confirmed by reading
`_familyA_zone_massintegral`, `src/arty/zones.py:468-491` — it calls
`pk_given_hit(E)` directly on the hardcoded `_PK_E=[100,1000,4000]` curve),
so Family A structurally cannot be threshold-matched to the card without a
code change — which is exactly why the write-up names, but does not attempt,
a threshold-matched variant as the real follow-up.

This is the right call, but right now the finding lives only in this one
challenge document. `b-vs-range.qmd`'s own `.html` and `_limitations.qmd` #14
(already referenced by name in §4's "Out-of-scope follow-up" paragraph) do
not yet carry Family A's side of this story — a reader who only reads the
`.qmd`'s Family-B FAIL and this document's Family-A PASS in isolation, without
reading §5's cancellation argument, would wrongly read this as "Family A is
validated, Family B is broken." **Impact:** no numeric output changes; this is
purely about whether the caveat is discoverable from the rendered
notebook/limitations surface rather than only from a challenge markdown file
one directory level away. Recommend logging in `_limitations.qmd` (as an
addendum to #14, since it's the same lethality-criterion axis) a one-paragraph
pointer: "Family A's agreement with the 1944 card (`b-vs-range-familyA.md`) is
confounded by a ~10x threshold mismatch with Family B's card-matched run and
should not be read as an independent kernel validation."

### 2. Note (no action required): unused `_ZONE_NAMES` import

`checks/b-vs-range-familyA.py:50` imports `_ZONE_NAMES` from `arty.zones` but
never references it — the script hardcodes its own equivalent `zone_list = [("ogive", ...), ("cylinder", ...), ("boattail", ...), ("base", ...)]`
(line 96-97), which was confirmed to match `_ZONE_NAMES = ("ogive", "cylinder", "boattail", "base")` (`src/arty/zones.py:462`) exactly — no zone
omitted, no drift. Harmless dead import, same category as the `FT2_PER_M2`
note in the `b-vs-range` review section above.

## Verified independently

- **Numeric reproduction.** Re-ran both `checks/b-vs-range-familyA.py` and
    `checks/b-vs-range-familyA-aof-ap.py` (`uv run python ...`). Every number in
    every table of `b-vs-range-familyA.md` §2 (all 33 rows across 3 shells: $B_A$,
    $B_B$, A/card, B/card, A/B, AoF band), §3 (AoF-sweep verdict table, graded-vs-
    flat $A_p$ ratios, the `ap_floor=0.7831 m²` figure), and the summary
    (A/card, B/card, A/B ranges, monotonicity) reproduces exactly.
- **Per-zone $A_p$-inversion is exact, not approximate.** Read
    `_four_zone_familyA_eval` (`src/arty/zones.py:494-565`) directly: it computes
    `gamma = arcsin(clip((h_b - z_rep)/s_z, -1, 1))`, `geom = presented_area(gamma,   posture)/(2π s² · 2δ)`, and `field_N_z = J · geom / sin(theta_z)` — i.e. the
    zone's output already has $A_p(\gamma_z)$ multiplied in. The check script's
    `rho_L_familyA` recomputes `z_rep`/`lit` via the *same*
    `_belt_column_zrep_vec` call with identical arguments (including
    `x_axis=xg`, the correct forward-axis choice for four-zone belts per that
    function's own docstring, `src/arty/fragmentation.py:877-881`), then computes
    `gamma` with the identical `(h_b - z_rep)/s_z` sign convention and divides
    `N_z / A_p(gamma)`. This is an exact algebraic inverse of the builder's own
    multiplication, not a reconstruction from a different formula — confirmed by
    reading both sides side by side, not just trusting the docstring's claim.
- **Masking/filtering consistency.** Traced the builder's `ok = s_z >= 1e-6`
    singularity guard and its early-`continue` zone-skip conditions
    (`mass_kg<=1e-6`, `V0_ms<=0`, non-finite `mu`, `sin(aof+theta_z)<=0`) against
    the check script's `use = lit & (N_z > 0.0)` mask: every point/zone the
    builder suppresses ends up with `N_z = 0`, which `use` correctly excludes
    regardless of what the check script's own independently-recomputed `gamma`/
    `A_p` evaluate to at that (masked-out) point — no risk of a stale or
    mismatched divisor leaking into `rho_L` at an excluded cell.
- **Dimensional check.** $B_\text{model} = \langle\rho_L\rangle_\phi \times
    (0.3048\,\text{m/ft})^2$: $\rho_L\,[\text{m}^{-2}] \times [\text{m}^2/\text{ft}^2]
    = [\text{ft}^{-2}]$ — correct (same formula already validated in the Family-B
    review section above; re-confirmed it's used identically here).
- **Family B inputs match the published, previously-reviewed scripts exactly.**
    Grepped all three `checks/b-vs-range-{75,105,155}mm.py` for
    `E_LETH_58FTLB_J`/`AOF_PRIMARY_DEG`/`DELTA_DEG`/`H_B` — all three use
    `E_leth=58 ft-lb (78.6 J)`, `AOF_PRIMARY_DEG=30`, `DELTA_DEG=15`, `H_B=0`,
    identical to the Family-A script's own settings, confirming the "same
    ranges, AoF, posture, drag calibration" claim in the docstring and §1 table.
    Also confirmed the 75mm script's `CARD_B[2]` already carries the `0.0192`
    r=40 fix from the prior `b-vs-range` review's Finding 1 (not a regression).
- **`E_LETH_DEFAULT` anchor claim is accurate here** (unlike the analogous
    finding flagged for `b-vs-range.qmd` above): `E_LETH_DEFAULT = 1000.0`
    (`src/arty/fragmentation.py:533`) is documented in-line as deliberately set
    to match "the 0.5 point of the graded `pk_given_hit` weighting it replaces"
    — i.e. it is the *design intent* anchor for `_PK_E[1] = 1000.0`, not a
    coincidental match being misattributed. Confirmed `pk_given_hit` has no
    `E_leth` parameter and cannot be overridden (`_familyA_zone_massintegral`,
    `src/arty/zones.py:468-491`), consistent with the write-up's claim that
    Family A structurally "uses its own curve as-is."
- **Algebraic identity check.** Spot-verified $B_A/B_\text{card} = (B_A/B_B)
    \times (B_B/B_\text{card})$ at 75mm r=20 ($0.372 \times 3.05 = 1.135
    \approx 1.13$ reported A/card) and confirmed the reported "26/33 points
    outside the 2x A/B band" count ($0+1+6=7$ in-band, $33-7=26$ out) and the
    "0.19x-0.71x" / "1.94x-5.30x" summary ranges against the per-shell min/max
    in the tables.
- **Monotonicity re-derived from the printed values directly** (not just
    trusting the script's own round-trip `rA * CARD_B` diff check) for all
    three shells — all strictly decreasing in $r$, confirming "Monotone: yes"
    independent of the script's internal check method.
- **AoF/robustness table and flat-vs-graded $A_p$ sensitivity numbers**
    reproduce exactly on re-run; confirmed the "\<1%" flat/graded claim against
    the actual printed range (0.9903-1.0, i.e. ≤0.97% deviation).
- **No physics/parameter leakage.** All physical quantities come from
    `arty.fragmentation`/`arty.zones` imports (`STANDING`, `DragParams`,
    `_belt_column_zrep_vec`, `presented_area`, `retardation_coeff`,
    `_four_zone_familyA_eval`, `compute_shell_zones`, `SHELLS`); the only
    literal constant in the check scripts is `FT_TO_M = 0.3048` (a unit
    conversion, same precedent already accepted for the Family-B scripts). The
    `s_z = sqrt(x²+y²+dz²)`/`gamma = arcsin(...)` lines in the check script are
    not new physics — they are the exact geometric inverse of formulas the
    builder itself already computes with the same inputs, required to recover
    $A_p$ per zone rather than a reimplementation of a different model. No
    `.qmd`/notebook was touched by this pass, so the "no physics in `.qmd`"
    layering rule does not apply here; both artifacts reviewed are a `.md`
    write-up and standalone `checks/*.py` scripts.

## What to log

- **A limitation, not a fix**, for Finding 1: add a pointer in
    `_limitations.qmd` (as an addendum to #14) stating that Family A's
    factor-of-2 PASS against the 1944 card (`b-vs-range-familyA.md`) is
    threshold-confounded against Family B's card-matched run and must not be
    read as an independent validation of the Family-A kernel; the real
    follow-up is the named-but-not-implemented threshold-matched Family-A
    variant.
- Nothing to log for Finding 2 (unused import) — cosmetic only, fix at
    convenience, not a limitation.
