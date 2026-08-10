# Review: sourced-wood-perforation-threshold derivation.md

**Reviewer pass, 2026-08-10.** Scope: `derivation.md` (all 7 sections) and the
three named check scripts in `checks/`. Per brief, `_limitations.qmd`,
`challenges/README.md`, and primary sources outside
`doc-reference/fragmentation/` are out of scope for this pass (a separate pass
covers them).

`collect-findings.py --for` this folder returned no open findings.

Status: COMPLETE. Verdict: **FAIL** (see below) — one Blocking finding, no
effect on the shipped/adopted §7 model.

---

## Finding 1 — `ufc-5-1-perforation-threshold.py` does not reproduce §1.1/§4.1/§4.2/§4.3's cited numbers (stale post-fix double-swap)

**Tag: Blocking.** Impact: the script named as the source of every number in §§1–6
(line 19-21 of derivation.md) currently prints numbers that materially disagree
with those tables when re-run today.

Root cause, verified by reading `checks/ufc-5-1-perforation-threshold.py` and the
git history of the CSV it reads:

- Commit `10303e0` ("correct UFC Table 5-5 density/hardness column transposition")
    fixed `doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/tables/table-5-5-wood-properties.csv`
    by **swapping only the header names** (`hardness_pounds,density_lbs_per_ft3` →
    `density_lbs_per_ft3,hardness_pounds`); the row values (23.5, 38.7 for
    Pine/Dry) did not change. After the fix, column 1 (`density_lbs_per_ft3`)
    correctly holds 23.5 and column 2 (`hardness_pounds`) correctly holds 38.7 —
    i.e. the CSV is now self-consistent with derivation.md §1.1's stated correct
    values (ρ = 23.5, H = 38.7).
- `checks/ufc-5-1-perforation-threshold.py`'s `wood_props()` (lines 37-50) was
    **not updated** in that commit. It still applies the pre-fix reversal —
    `rho = row["hardness_pounds"]`, `hardness = row["density_lbs_per_ft3"]` —
    which was the *correct* antidote when the CSV headers were backwards, but is
    now a **second, redundant swap** applied to an already-corrected CSV. Running
    the script today (verified: `uv run python checks/ufc-5-1-perforation-threshold.py`)
    prints `rho = 38.7 lb/ft3, H = 23.5 lb` — the reverse of derivation.md's
    stated ρ = 23.5, H = 38.7.
- Confirmed by direct computation with the un-swapped (correct) values
    (ρ=23.5, H=38.7): §4.1's three T_w figures (162.5, 383.8, 34.8 in) reproduce
    **exactly**. The script's current (double-swapped) output instead gives
    129.3, 305.3, 27.6 in — off by 15–20%. §4.2's table diverges further: at
    m = 0.05 g the script prints E_thr = 2.902 J against derivation.md's cited
    9.54 × 10⁻¹ J (3.0× high); at m = 0.63 g the script prints 2.767 × 10⁻² J
    against the cited 9.10 × 10⁻³ J (3.0× high). §4.3's ratio (2.20×10⁻⁴ vs the
    cited 1.2×10⁻⁴, both against the 78.6 J probe) likewise disagrees, though
    both still fail check 3 by more than a decade so the qualitative "FAIL by
    (roughly) four decades, reject Option A" verdict is not reversed by the bug.

**Why Blocking despite not reversing the verdict.** The task's own instruction
is to run each of the three named scripts and confirm the printed numbers match
what derivation.md cites — this one demonstrably does not, on two of its four
printed sections (§4.1, §4.2) by factors of 1.15–3.0×. Per
`.claude/rules/verification-scripts.md`, a retained check script exists so "the
next pass re-runs or re-reads the script instead of re-deriving it cold" — a
script that silently disagrees with the document that cites it defeats that
purpose and will actively mislead a future reader (or agent) who reruns it
expecting derivation.md's tables, or who reuses `wood_props()`'s reversal
pattern elsewhere in the Table 5-5 doc-reference tree.

**No impact on the shipped/adopted model.** §7 (the finalised A″ plug-shear
form that the implementation pass inherits, §7.6) does not use Table 5-5,
`wood_props()`, or this script at all — it sources τ from Sanborn 2019 Table 2
via a separate script (`plug-shear-perforation-threshold.py`, checked below).
Option A remains rejected under either the correct or the buggy numbers (check
3 fails by more than a decade either way). So this finding affects the
auditability of the (already-rejected) §§1–4 reasoning, not the demo's
rendered output.

**Suggested correction (not applied):** remove the reversal in `wood_props()`
(read `density_lbs_per_ft3` → rho, `hardness_pounds` → hardness directly,
matching the now-corrected CSV headers) and re-run to confirm the script
reproduces §4.1's 162.5/383.8/34.8 in and §4.2's table verbatim.

**Independent confirmation of what the *correct* (un-swapped) values give:**
recomputed the three §4.1 cases by hand with ρ=23.5, H=38.7 (no reversal) —
gives 162.47, 383.78, 34.75 in, matching derivation.md's cited 162.5 / 383.8 /
34.8 in to the last printed digit. §1's exponents (9837, 0.4113, 1.4897,
1.3596, 0.5414) were also independently cross-checked against
`doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/card.md`
(itself grounded in a page-image vision inspection, resolved 2026-08-09) and
match exactly — §1's equation transcription is sound; the defect is confined
to the check script's stale CSV-reading logic.

---

## Section-by-section verification notes

**§1 (source equation).** Exponents (9837, 0.4113, 1.4897, 1.3596, 0.5414)
verified against `card.md`'s independently-recorded vision-confirmed values —
match exactly. The $(\pi D^2/4)^{1.3596}$ area form (vs. Sanborn's $D^{1.3596}$)
and $\rho^{1.0}$ (vs. Sanborn's $\rho^{0.5414}$) are also confirmed there.
**§1.1 (Table 5-5 swap).** The closure-invariant claim (col 1 non-decreasing
dry→wet, col 2 non-increasing dry→wet for hardwoods) is independently verified
by `table-5-5-closure-check.py` (run output: both PASS, all 7 species) and
matches the CSV as currently committed. This script — unlike
`ufc-5-1-perforation-threshold.py` — reads the CSV headers directly with no
extra reversal, and is correctly in sync with the post-fix CSV. No finding.

**§2 (closed-form exponents, eq. 6).** $p=-1.418$, $E_{thr}\propto m^{-1.836}$
independently re-derived by hand from the stated substitution
($A\propto m^{2/3}$, $w\propto m$) and match to 3 decimals. These exponents are
pure functions of the UFC exponents and do not depend on ρ, H — so they are
unaffected by Finding 1's swap bug. No finding.

**§3 (unit checks).** Conversion constants (2.2046226 lb/kg, 39.3701 in/m,
3.28084 ft/m) are all correct to 6 figures. The mm-vs-inch argument
(34.8 mm = 1.37 in would *under*-predict against the 6.875 in CLT panel,
contradicting Sanborn's stated over-prediction finding) is logically sound and
independently checked: 34.75/6.875 ≈ 5.06×, consistent with the "~5×
over-prediction" claim in §4.1. No finding.

**§4.2 (bias-sign correction, "Bias-sign correction to scoping §2a item 2").**
Independently re-derived: since $T_w(v)$ is monotonically increasing in $v$,
an equation that over-predicts $T_w$ at any given $v$ (i.e. the biased curve
sits above the true one) means inverting the *biased* equation directly at a
fixed panel thickness $t$ finds a $v$ that is *lower* than the true $v_{50}$
(because the biased curve reaches the horizontal line $T_w=t$ "too early," at
too-low a $v$). So over-predicted $T_w$ ⇒ under-estimated $v_{50}$ ⇒
under-estimated $E_{thr}$ ⇒ over-counted $N$ — the derivation's stated
correction to scoping is directionally correct, and consistent with the bias
table (larger bias-correction factor $b$ raises $v_{50}$, so the naive $b=1$
case is the low one). No finding.

Minor arithmetic imprecision (Note, no impact): §4.3 states "the velocity that
satisfies it collapses by $30^{2.431}\approx5\times10^3$"; computed exactly,
$30^{2.431}\approx3.9\times10^3$ (using the more precise $10^{1.5}=31.6$ for
"30", $\approx4.4\times10^3$). Both are within the same order of magnitude the
prose is making the point with ("several thousand-fold collapse"), and this
number does not feed any downstream table or conclusion — it is a single
illustrative aside. **Tag: Note.** No correction needed beyond tightening the
approximation if the section is touched again.

**§7.1 (probe inadmissibility).** The "58 ft.-lb." quote and its
mass-non-specificity were verified as in-scope for the criterion-match gate;
the grepped anchor (`For the lightest effective Fragment`) sits outside
`doc-reference/fragmentation/` (it is in `doc-reference/wound-ballistics/`) and
is therefore outside this pass's brief — not independently re-verified here.
The **criterion-match reasoning itself** (58 ft-lb personnel-incapacitation ≠
1-in-softwood perforation limit) is sound on its face and correctly applied:
this is exactly the class of error `.claude/rules/source-data-fidelity.md`'s
"criterion match" gate exists to catch, and the derivation catches it in its
own self-review, correctly demotes both probes to a plausibility-only role in
§7.4, and correctly does not use either to fix any parameter of the finalised
model (9). No finding — flagging this as done right, since it is exactly the
kind of thing this review is required to check.

**§7.2 (crush-vs-shear ratio, eq. 8).** Re-derived algebraically:
$E_{crush}/E_{shear} = \sigma_c D/(2\tau t)$ — matches eq. (8) exactly.
Numerically cross-checked against `plug-shear-perforation-threshold.py`'s
printed ratios (5.7%, 10.6%, 15.5%, 26.5% at 0.1/0.63/2/10 g) — the text's "6–27%"
range is consistent (5.7%→"6%", 26.5%→"27%", ordinary rounding). $\sigma_c$'s
derivation (Janka mean pressure 26.9 MPa ÷ 3 "spherical-indenter constraint
factor" → 9.0 MPa) is a standard indentation-hardness approximation (Tabor-type
factor ≈3, common for Brinell-style hardness-to-yield-stress conversion) rather
than a value read directly off Sanborn's table; this is a physically reasonable
modelling choice, but note it is **not itself sourced** the way $\tau$ is — it
only feeds the *crush* term, which §7.2 explicitly drops from the adopted model
(9). **Tag: Note** (crush is <27% of shear at all masses tested and is not part
of the adopted formula, so even a large error in $\sigma_c$ cannot move the
final $E_{thr}(m)$ by more than that bound).

**§7.3 (plug-shear derivation, eq. 9).** The integral
$\int_0^t \tau\pi D(t-x)\,dx = \tfrac12\tau\pi D t^2$ was independently
re-derived and confirmed exactly, giving $\eta=1/2$ correctly. Dimensional
check: $[\tau][D][t^2] = \text{Pa}\cdot\text{m}\cdot\text{m}^2 = \text{J}$ —
correct. $\tau$ = 8.96 MPa (SPF-S) and 11.0 MPa (SYP), with COV/n/ρ, verified
**directly against the primary**: grepped
`doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/source.md`
line 87, `Shear Strength Parallel to Grain, ASTM D143 ... 1,300 27% 14 1600 13%
19 psi (MPa) ... (8.96) (11.0)` — matches derivation.md's table exactly
(τ, COV, n, ρ for both species). The unit-conversion closure claimed in the
text ("all eight dual-unit pairs reconcile to ≤0.29%") is independently
reproduced by `plug-shear-perforation-threshold.py`'s printed output (worst
deviation 0.29%, PASS) — the script reads the values as literals rather than
from a `tables/*.csv`, but they are traceable 1:1 to the single quoted primary
line and cross-checked against it directly above, so this does not raise a
transcription-fidelity concern for this pass. No finding.

**§7.4 (validation).** All five numeric blocks (Check 1 Sanborn-panel forward
evaluation — 5453 J / 1139 m/s; Check 2 monotonicity table; Check 3
35.5–97.2 J band, 48.6 J central; sensitivity linear-in-τ) were independently
re-run via the script and reproduce derivation.md's cited figures exactly
(verified `uv run python checks/plug-shear-perforation-threshold.py` output
above, cross-referenced line by line against §7.4's text). "Sanborn shot
envelope 180–1200 m/s, 59 of 122 perforating" independently verified against
`source.md`: line 67 states "500 to just over 3500 ft/s (180 - 1200 m/s)"; line
77's species table sums to 63 embedded + 59 perforated = 122 total, matching
line 82's "Fifty-nine ... resulted in complete penetrations." No finding.

**§5, §7.5 (assumptions logged).** Physically reasonable and consistently
labelled with their direction of bias (e.g. A6: quasi-static τ used at
ballistic strain rates is explicitly flagged anti-conservative on count). No
finding.

---

## Verdict: **FAIL**

One Blocking finding (Finding 1): the check script named as producing every
number in derivation.md §§1–6 does not, as currently committed, reproduce
those numbers — it applies a stale post-fix double-reversal of Table 5-5's
density/hardness columns, left over from before commit `10303e0` corrected the
CSV's own header labels. This is squarely within this pass's mandate (run each
script, confirm it reproduces what derivation.md cites) and demonstrably fails
on §4.1 (15–20% off) and §4.2 (up to 3.0× off). It does **not** reverse
derivation.md's "reject Option A" conclusion (both the correct and the buggy
numbers fail check 3 by more than a decade) and has **zero** effect on the
finalised, implementation-inheriting model in §7 (which uses a wholly separate
script and does not touch Table 5-5). The fix is small and mechanical: remove
the now-redundant reversal in `ufc-5-1-perforation-threshold.py`'s
`wood_props()`.

Everything else checked — §1's equation transcription, §1.1's Table 5-5
closure invariant (correctly implemented in the sibling script), the closed-form
exponent algebra, the unit-conversion chain, the bias-sign correction, the
crush-vs-shear derivation and its Sanborn Table 2 sourcing (independently
grepped against the primary and matched exactly), the plug-shear integral and
its dimensional consistency, and every number in `plug-shear-perforation-threshold.py`
— reproduces cleanly and matches derivation.md. §7's criterion-match
self-correction (demoting the two casualty/hole-size probes from calibration
anchors to a plausibility-only band) is exactly the discipline
`.claude/rules/source-data-fidelity.md` calls for, done correctly and
proactively by the derivation itself.

### Findings summary

| # | Section | Tag | Impact |
| --- | --- | --- | --- |
| 1 | `checks/ufc-5-1-perforation-threshold.py` vs. §1.1/§4.1/§4.2/§4.3 | **Blocking** | Script currently prints numbers 15–20% (§4.1) to 3.0× (§4.2) off from what derivation.md cites, due to a stale double-swap of Table 5-5's ρ/H columns left over from a since-fixed CSV. Does not reverse the "reject Option A" verdict and does not touch the shipped §7 formula. |
| 2 | §4.3, "$30^{2.431}\approx5\times10^3$" | Note | Illustrative aside is ~25–28% off ($3.9$–$4.4\times10^3$ actual); feeds no table or conclusion. |
| 3 | §7.2, $\sigma_c$ (Janka ÷3 constraint factor) | Note | Physically reasonable but not itself a sourced value (unlike $\tau$); only feeds the crush term, which is dropped from the adopted model (9) and bounded at <27% of the shear term regardless. |

### Suggested corrections (not applied)

1. In `checks/ufc-5-1-perforation-threshold.py`'s `wood_props()`, read
   `row["density_lbs_per_ft3"]` → `rho` and `row["hardness_pounds"]` → `hard`
   directly (drop the reversal), matching the CSV as corrected in commit
   `10303e0`. Re-run and confirm the output reproduces §4.1's 162.5/383.8/34.8 in
   and §4.2/§4.3's tables verbatim; update the docstring/comment that still
   describes the CSV as carrying the swap.
2. Optional, not blocking: tighten the "$\approx5\times10^3$" aside in §4.3 to
   the computed $\approx4\times10^3$, or drop the numeric approximation and
   keep the qualitative "collapses by several thousand-fold."
3. Optional, not blocking: note in §7.2 that $\sigma_c$ (unlike $\tau$) is a
   derived estimate via a generic indentation-constraint factor, not a value
   read directly off Sanborn's table, since it is currently presented in the
   same sentence as the sourced Janka force without that distinction being
   flagged.

### Re-review scope

A re-review pass verifying the Finding-1 fix should: (a) re-run
`ufc-5-1-perforation-threshold.py` and confirm its output now matches
derivation.md §4.1/§4.2/§4.3 verbatim, and (b) confirm no other file in the
repo reuses the old (pre-fix) `wood_props()` reversal pattern against the
now-corrected CSV.

