# Criterion-match review — 1944 Ordnance re-baselined columns vs. their consumers

**Date:** 2026-08-03
**Gate reviewed:** `.claude/rules/source-data-fidelity.md` → *Criterion match* —
"does the cited data measure the same quantity the model computes?"
**Explicitly NOT reviewed:** transcription fidelity (discharged by the
`.invariant` closures) and provenance (separate pass).

**Read set:** the six
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables/*.csv`
and their `.invariant` files;
`experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-rebaseline.md`;
`experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/mach-law-rebaseline.py`;
`experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-rebaseline.py`.
`src/arty/` was **not** read (out of scope for this pass), which is why two
findings below are stated as conditionals with the single settling fact named.

**Supporting script:**
`experiment/fragmentation-field/challenges/source-data-audit/checks/criterion-match-column-defs.py`
(runtime \<1 s) — establishes the column *definitions* used throughout this
review, directly from the CSVs.

______________________________________________________________________

## 0. What the columns actually tabulate (established, not assumed)

Run on all six CSVs:

| closure                    | result                                                                                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `B == N / (4πr²)`          | holds on **every row of every one of the six tables**; ratio 1.000 ± rounding (deviations only where `B` is printed to 1 significant digit, e.g. 0.0001) |
| `½mv²` on casualties rows  | 55.9 – 58.2 ft-lb (10 of 11 rows within ±1 %) — the fixed 58 ft-lb criterion                                                                             |
| `½mv²` on perforation rows | 247.8 – 1145.8 ft-lb, monotonically rising with range — not a fixed-energy criterion                                                                     |

The first row of that table is the load-bearing new fact, and it is decisive
for consumer #1:

> **`B` in these tables is an *isotropic* areal density by construction.** It
> is not a measured local flux; it is the shell's *total* effective-fragment
> count `N(r)` divided by the full-sphere area `4πr²`. The source therefore
> reports the direction-averaged density and carries **no** directional
> information at all — a real HE shell's side-spray belt density is several
> times this figure and its nose/base density is far below it.

The `.invariant` column glosses ("N total number of effective fragments",
"B average number of effective fragments per sq. ft.") are consistent with
this; the arithmetic makes it exact rather than inferred.

Second definitional fact, load-bearing for consumer #2: `m_oz`/`v_fps` are the
**arrival** mass and velocity at range `r` of the marginal (lightest still
qualifying) fragment. The 58 ft-lb closure holding on the *tabulated* `v`
proves `v` is evaluated at `r`, at the target, not at any other station.

______________________________________________________________________

## 1. `drag-gap-1944/b-vs-range-rebaseline.md`

**Column now read:** `*-casualties.csv` → `B` (and its own `r` grid).
**Computation it feeds:** `B_model(r)`, compared row-by-row against `B_card`,
with a factor-of-2 acceptance band, `E_leth` overridden to 58 ft-lb.

### 1a. Threshold criterion — MATCH

The model is run with `E_leth` = 58 ft-lb and the column's stated criterion is
"a casualty is supposed caused by a hit with at least 58 ft.-lb. of energy",
which `½mv²` reproduces on every row (57.5–58.2 ft-lb, one 155 mm outlier at
55.9). The energy criterion the model applies and the energy criterion the
column tabulates are the same criterion, to within the source's own ±3.6 %
worst-row spread. The re-baseline's central move — swapping the perforation
column (248–1146 ft-lb, a *different and range-dependent* criterion) for the
casualties column — is correct on this axis and closes the original
column-inversion defect.

### 1b. Geometric criterion — raised as a conditional, then RESOLVED to MATCH

`B_card` is `N/(4πr²)` exactly: a **whole-sphere average**. The comparison in
`b-vs-range-rebaseline.md` is only criterion-matched if `B_model` is likewise
the shell's total effective-fragment count at range `r` divided by the full
`4πr²` sphere. Had `B_model` instead been a **direction-resolved** density —
the density in the side-spray belt, in a polar zone, or along a ray, which is
what a four-zone fragmentation model naturally produces — the two sides of
every row would be different physical quantities and the comparison invalid
regardless of which column was read. For a side-spray-dominant shell the belt
density runs several times the isotropic average, so this would show up as a
near-uniform multiplicative offset — precisely the residual shape the document
is interpreting.

The published ratios alone (1.5–2.0× short range, 0.16–0.66× long range) do not
discriminate. **An independent cross-check inside my read set does**, and it is
decisive by a factor of 4:

`count-chain-rebaseline.py` section (D) prints, for the **same shell**
(75 mm M48 HE), the **same threshold** (`E_thr = 78.6 J = 58 ft-lb`) and the
same `DragParams`, `N(≥ m_thr) = 1779` effective fragments at `r = 15 ft`.
Converting `b-vs-range-rebaseline.md`'s `B_model(20 ft) = 0.323` on the
whole-sphere hypothesis gives `0.323 × 4π(20)² = 1624` fragments:

| hypothesis for `B_model`           | implied total effective `N` | vs. independent 1779 @ 15 ft                                                 |
| ---------------------------------- | --------------------------- | ---------------------------------------------------------------------------- |
| whole-sphere `N/(4πr²)`            | 1624 @ 20 ft                | 0.91× — an 8.8 % drop over 5 ft of extra drag, right direction and magnitude |
| belt-local (30° belt, Ω/4π ≈ 0.26) | 422                         | **4.2× too low — rejected**                                                  |

The two threads were computed independently and agree to within the drag decay
expected between 15 and 20 ft. `B_model` is a whole-sphere average, matching
`B_card`'s construction. **No finding; the document's verdict stands on this
axis.** (Cheap confirmation if wanted: grep
`checks/b-vs-range-rebaseline.py` for `4 * pi * r**2` — but the arithmetic
above already closes it, so this is confirmation, not a gate.)

### 1b′. What the match does and does not license — Deferrable

Because `B_card` is isotropic *by construction*, the comparison validates only
the **direction-averaged** effective-fragment density and its range decay. It
carries zero information about the model's **angular** distribution: a model
with the correct total count and a completely wrong side-spray belt would score
identically on every row of every table in that document. The re-baselined
"Family B passes the §4 factor-of-2 criterion" is therefore evidence for the
count-and-decay chain, not for the belt geometry, and should not be cited as
external support for the four-zone angular structure.

Impact: no number changes; this bounds the claim's reach. Resolution is a
logged limitation.

*Closed 2026-08-09 — logged as the second addendum to limitation 14 in
`experiment/fragmentation-field/_limitations.qmd`, which states that the card's
`B` column is an isotropic reduction by construction, that the agreement
therefore tests only the direction-averaged density and its range decay in
either family, and that it must not be cited as external support for the
side-spray belt or the four-zone angular structure. Marker deleted.*

### 1c. Table-number labels — Note

The document names the casualties tables "Table 43 / 51 / 59". The re-baselined
`.invariant` files anchor them as **TABLE 38** (75 mm), **TABLE 48** (105 mm)
and **TABLE 56** (155 mm), with the paired perforation tables at 39 / 49 / 57.
The document's numbers match neither series. They are quoted from the old,
inverted scripts' docstrings, so this is a stale label rather than a new error,
but a reader grepping the source for "Table 51 CASUALTIES" will not find the
table the document is actually using, and the numbers differ from the
perforation tables too — so the label does not even identify the wrong column
correctly.

**Closed 2026-08-10.** `b-vs-range-rebaseline.md`'s three section headings now
read TABLE 38/48/56, with a note at first mention explaining the scripts'
own docstrings still say "Table 43/51/59" and pointing at the `.invariant`
anchors as the correct numbers.

______________________________________________________________________

## 2. `mach-dependent-fragment-drag/checks/mach-law-rebaseline.py`

**Columns now read:** `*-casualties.csv` and `*-perforation-1-8in.csv` →
`r_ft`, `m_oz`, `v_fps` (the `N`/`B` columns are not read at all).
**Computation they feed:** a single-fragment velocity-decay integration from
`V0` over path length `r`, compared against the tabulated arrival `v`.

### 2a. Quantity match — PASS

The script computes "velocity of a fragment of mass `m`, launched at `V0`,
after travelling distance `r`". The columns tabulate "mass and velocity, at
range `r`, of the marginal effective fragment". Same physical quantity. The
`½mv² = 58` closure holding on the tabulated `v` is direct evidence that `v` is
the arrival velocity at `r` and not a launch or mean velocity — a genuinely
useful confirmation, since a decay check reading a launch velocity would be
silently degenerate.

### 2b. The criterion column choice is immaterial here — PASS, and worth stating

This is the important asymmetry against consumer #1. For `B(r)`, the choice of
column *is* the criterion and swapping it changes the answer several-fold. For
a **drag-decay** check it does not: the criterion only selects *which*
`(m, v)` point is tabulated at each `r`; the decay relation itself is
criterion-free single-fragment ballistics. Evidence from the CSVs: at every
shared range the 105 mm and 155 mm tables print *identical* `(m, v)` — for both
their casualties columns (8 of 10 ranges exactly, 2 differing in the last
digit) and their perforation columns (11 of 11 exactly) — which is only
possible if `(m, v)` is a pure single-fragment ballistics result independent of
shell size. Running `report("perforation-1-8in")` alongside
`report("casualties")` is therefore legitimate and is an *asset*: the
perforation column samples heavier fragments at higher arrival Mach (248–1146
ft-lb vs. a flat 58), extending the fit's lever arm rather than contaminating
it. The script's docstring frames the perforation column only as the old
script's error; it is also a valid independent sample and should be described
that way.

### 2c. `V0_FTS` provenance — CLOSED by the read set, contrary to the brief

The dispatch brief states the muzzle/initial velocities are "absent from the
processed Ordnance source" and to treat provenance as open. The read set
contradicts that. Every one of the six `.invariant` files carries an explicit
greppable source anchor:

- `75mm-m48-*.invariant`: `anchor:  INITIAL FRAGMENT VELOCITY 3,120 F/S`
- `105mm-m1-*.invariant`: `anchor:  INITIAL FRAGMENT VELOCITY 3,500`
- `155mm-m107-*.invariant`: `anchor:  INITIAL FRAGMENT VELOCITY 3,500 F/S`

These match `V0_FTS = {75mm: 3120.0, 105mm: 3500.0, 155mm: 3500.0}` exactly,
and the label "INITIAL FRAGMENT VELOCITY" is the same quantity the script's
`V0` denotes: the fragment velocity at the start of the decay integration.
The values are printed in the tables' own headers.

The script's comment at line 38 ("not present in the processed Ordnance source;
carried over unverified") is therefore **stale and understates its own
footing**. Correcting it is a comment edit, not a numeric change.

**Closed 2026-08-10.** The comment no longer flatly claims V0 is absent from
the source — it now distinguishes the literal table-caption occurrence (which
the six `.invariant` anchors do confirm) from open provenance in the
derivation sense, and points at the still-open deferrable V0_FTS-provenance
finding (`rebaseline-verdict.md:211`) for that deeper question.

### 2d. The tabulated `v` is the 1944 source's own drag calculation — Deferrable

`λ = ln(V0/v)/r` computed from the CSVs is **not** consistent with a
constant-`C_D` exponential, and the pattern of its failure is itself
informative. `λ·m^(1/3)` (which is constant iff `C_D` is constant):

| column             | first row | last row | drift     |
| ------------------ | --------- | -------- | --------- |
| 75 mm casualties   | 0.00500   | 0.00288  | **1.74×** |
| 105 mm casualties  | 0.00389   | 0.00282  | 1.38×     |
| 155 mm casualties  | 0.00389   | 0.00272  | 1.43×     |
| 75 mm perforation  | 0.00488   | 0.00465  | 1.05×     |
| 105 mm perforation | 0.00424   | 0.00440  | 0.96×     |
| 155 mm perforation | 0.00424   | 0.00413  | 1.03×     |

The **perforation** columns are flat to within 5 % — their fragments stay
supersonic (arrival 1020–2700 f/s) where `C_D` is on its plateau. The
**casualties** columns drift by 1.4–1.7× — their marginal fragments decay into
the transonic/subsonic regime (arrival down to 383–507 f/s, M ≈ 0.34–0.45)
where `C_D` falls off. The drift ratio (~1.7×) is what a `C_D` falling from the
~1.3 supersonic plateau to ~0.75 subsonic would produce.

This is a clean, quantitative confirmation that the 1944 authors applied a
*Mach-dependent* drag law to generate these columns — i.e. the `(r, m, v)`
triples are the source's own ballistic **computation**, not independent
measurements of arrival velocity. (It is also, incidentally, corroborating
physical evidence *for* the Mach-dependence the update is investigating,
recovered from a completely separate source than DoD-1975 Fig. 3.)

Consequence for the consumer: `mach-law-rebaseline.py` is then comparing a
modern Mach-dependent drag law against a 1944 drag law, not against data. That
does not invalidate anything the script concludes — the 1944 law is itself
anchored on period firing data and the comparison remains the best available
external check at this fidelity bar — but it caps how much the residual can be
read as model error, and it means an RMS agreement better than the 1944 law's
own accuracy is not attainable and should not be sought. **Resolution is a
logged limitation, not a fix.** Note this is adjacent to the provenance gate
(is the source's `v` measured or derived?), which is a separate pass; what is
in *this* pass's scope is that the quantity is the same either way, so 2a's
PASS is unaffected.

Suggested limitation wording: *"The 1944 Ordnance `(r, m, v)` triples used to
check fragment velocity decay are internally consistent with a variable-drag
ballistic calculation performed by the source's own authors rather than with
direct arrival-velocity measurement (`λ·m^(1/3)` drifts 1.7× along a column).
The drag comparison is therefore model-against-period-model; residuals below
the 1944 law's own accuracy are not interpretable."*

*Closed 2026-08-09 — logged at the end of limitation 15 in
`experiment/fragmentation-field/_limitations.qmd`, carrying the `λ·m^(1/3)`
drift evidence, the model-against-period-model framing, and the consequence
that residuals below the 1944 law's own accuracy (the ~1.8-point
Mach-vs-constant margin included) are not interpretable. Marker deleted.*

______________________________________________________________________

## 3. `count-gap-1938/checks/count-chain-rebaseline.py`

**Columns now read:** the **Tolch-1938** CSVs
(`pit-screen-recovery.csv` → `screen`, `n_frag`, `wt_lb`;
`side-spray-density.csv` → `panel`, `v_fps`, `perf`). The 1944 Ordnance tables
are **not** read by this script; they appear only as the literal
`(78.6, "1944 Ordnance card casualty, 58 ft-lb")` row at line 89.

The Tolch CSVs are outside my assigned read set, so the rulings below are
confined to what the script's own code and column names make determinate.

### 3a. The 58 ft-lb constant — MATCH

`58 ft-lb × 1.3558179 J/ft-lb = 78.638 J`; the script uses `78.6`, correct to
its printed precision. The quantity is a fragment kinetic-energy threshold at
the target on both sides. Match.

### 3b. Section (E), the threshold-free spectrum test — MATCH, and it is the

right construction

Section (E) inverts the Mott cumulative-mass relation at each screen boundary
and compares the model's predicted count above the mass carrying the *same
cumulative mass fraction* against Tolch's cumulative recovered count. Both
sides are then "number of fragments accounting for the top φ of the case
mass" — no energy threshold, no drag, no panel geometry on either side. This is
a genuine criterion match and is the strongest comparison in the script.

### 3c. Section (D), model lethal count vs. recovered / perforating counts —

CONDITIONAL

Section (D) divides the model's `N(≥ m_thr)` — an **energy-effective count over
the whole shell** — by three denominators of visibly different criteria:

- `N/700`, labelled "perforating": a count gated by a **plate-perforation**
    threshold (not a 58 ft-lb energy threshold), and, if it comes from panel
    data, gated by the **solid angle the panel subtends** rather than the whole
    sphere.
- `N/803` (old) and `N/779` (`N_rec`, the re-baselined sum of `n_frag`): a
    **physical recovery census** with *no* energy criterion at all, bounded
    below by the finest screen's size cutoff and above by recovery efficiency
    (the script itself notes recovery is 95.6 % of the metal).

A ratio of an energy-thresholded whole-shell count to a size-thresholded
recovered census is only interpretable if the recovery census is complete down
to `m_thr`. **Running the script settles this and the answer is "not
complete":** it prints `m_thr = 0.403 g` for the 58 ft-lb row, while the finest
recovery bucket ("thru 4", 104 pieces) has a **mean** mass of 0.61 g. `m_thr`
therefore sits *inside* the unbounded residual bucket, in exactly the region
where the census stops being count-complete. The script's own section (E)
quantifies how badly: matched on cumulative mass fraction, the model predicts
3627 fragments against 779 recovered at the finest boundary (4.66×), i.e. the
recovery census misses most of the small-fragment *count* while capturing
95.6 % of the *mass* — the expected behaviour for a Mott spectrum.

So the `N/779 = 2.28` in row 3 of (D) is not a clean "the model over-predicts
by 2.28×"; part of it is census incompleteness at 0.4 g, and `N/700` compounds
that with a *third* criterion (plate perforation, panel-subtended solid angle).

**Impact is bounded and small, which is why this is Deferrable and not
Blocking.** The criterion-clean comparison — section (E) on the Tolch 13.29 lb
basis, finest bucket — gives **2.15×**, against (D)'s **2.28×**. The two agree
to ~6 %, and both support the same qualitative conclusion (the model
over-predicts effective fragment count by roughly a factor of two). No verdict
in the thread flips. What needs fixing is the *labelling*: (D)'s denominators
should not read as validation denominators, and the reported agreement should
be sourced to (E).

### 3d. `ratio_AD` from `side-spray-density.csv` — Note

`ratio_AD = perf(D)/perf(A)` at the static row is used as a spatial falloff
shape. Because it is a *ratio* of two perforation counts under a common
threshold and a common panel, the perforation criterion largely cancels and the
ratio approximates a fragment-density ratio. It does not cancel exactly: the
arriving fragment spectrum is softer at D than at A, so a fixed perforation
threshold rejects a larger share of arrivals at D and the ratio understates the
true density ratio (i.e. 0.557 is a lower bound on `ρ(D)/ρ(A)`). Directionally
conservative for a falloff-shape check; no action.

**Closed 2026-08-10.** `count-chain-rebaseline.py` now carries a comment at the
`ratio_AD` computation stating the bias direction (fixed threshold rejects
proportionally more of the softer spectrum at D, biasing the ratio toward 1).

______________________________________________________________________

## Verdict

**PASS-with-limitations.** No Blocking findings. All three consumers read
columns that tabulate the quantity the computation they feed actually
computes. The re-baseline fixed the one genuine criterion mismatch (a fixed
58 ft-lb energy threshold validated against a range-dependent 248–1146 ft-lb
plate-perforation threshold) and did not introduce a new one.

Two conditionals were raised during the pass and **both were closed inside the
read set**, by arithmetic rather than by further reading:

- **1b** (is `B_model` whole-sphere or belt-local?) — closed **MATCH** via the
    independent 75 mm count anchor in consumer #3: 1624 implied vs. 1779
    measured at 5 ft shorter range, against a 4.2× discrepancy under the
    belt-local hypothesis.
- **3c** (does `m_thr` lie inside the recovery census span?) — closed **NO**
    (0.403 g vs. a 0.61 g finest-bucket mean), but the resulting bias is ~6 %
    on the quoted ratio and flips no verdict, so it is Deferrable.

### Limitation entries to log

1. *(from 1b′)* "The 1944 Ordnance `B` column is `N/(4πr²)` — the total
    effective-fragment count spread isotropically over the full sphere.
    Agreement with it validates the model's direction-averaged density and its
    range decay only; it carries no information about the angular distribution,
    and must not be cited as external support for the side-spray belt or the
    four-zone angular structure."
1. *(from 2d)* "The 1944 Ordnance `(r, m, v)` triples used to check fragment
    velocity decay are the source's own variable-drag ballistic calculation,
    not direct arrival-velocity measurements — `λ·m^(1/3)` drifts 1.4–1.7×
    along the casualties columns (whose fragments go subsonic) while staying
    flat to 5 % along the perforation columns (which stay supersonic). The drag
    comparison is therefore model-against-period-model; residuals below the
    1944 law's own accuracy are not interpretable."
1. *(from 3c)* "`count-chain-rebaseline.py` section (D) reports ratios against
    a recovery census (779) and a perforation count (700) whose criteria differ
    from the model's energy threshold; `m_thr = 0.403 g` falls below the finest
    screen bucket's 0.61 g mean, where the census is count-incomplete. The
    criterion-clean figure is section (E)'s 2.15×, not (D)'s 2.28×."

### Summary table

| Consumer                    | Column read                             | Criterion match                                              | Verdict                                    |
| --------------------------- | --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| `b-vs-range-rebaseline.md`  | casualties `B`                          | energy **match**; geometry **match** (closed by cross-check) | **Pass** + 1 deferrable (1b′), 1 note (1c) |
| `mach-law-rebaseline.py`    | casualties + perforation `m_oz`,`v_fps` | **match**; column choice immaterial here                     | **Pass** + 1 deferrable (2d), 1 note (2c)  |
| `count-chain-rebaseline.py` | Tolch `n_frag`,`wt_lb`,`perf`           | (E) **match**; (D) mixed criteria                            | **Pass** + 1 deferrable (3c), 1 note (3d)  |

### Findings registered

| tag        | §   | one-line                                                     |
| ---------- | --- | ------------------------------------------------------------ |
| deferrable | 1b′ | isotropic `B` cannot validate angular structure              |
| note       | 1c  | table numbers cited as 43/51/59, invariants say 38/48/56     |
| note       | 2c  | stale "V0 not in source" comment; the invariants anchor it   |
| deferrable | 2d  | 1944 `(r,m,v)` is a period drag calculation, not measurement |
| deferrable | 3c  | (D)'s three denominators use three different criteria        |
| note       | 3d  | `perf(D)/perf(A)` is a lower bound on the density ratio      |
