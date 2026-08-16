# Review — fragment retardation anchored to the DoD-1975 ballistic density

**Scope.** `derivation.md` (dimensional consistency, physical plausibility,
boundary behaviour, agreement with `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/`),
cross-checked against `scoping.md` and the cited check script
`checks/drag-anchor-validation.py`. No `src/arty/` edit exists yet (this pass
is derivation-only, per its own §6); `DragParams` in
`src/arty/fragmentation.py` still carries the old `C_D=0.65`, `C_shape=0.90`
defaults and `retardation_coeff` matches eq. (3) verbatim (lines 272–279).

## Verdict: **PASS**

No blocking findings. The derivation is dimensionally sound, its identity is
algebraically exact (not fitted), every numeric claim reproduces from the
committed check script, and the source citations check out against the actual
`doc-reference` text. The two logged limitations (L1, L2) and the explicit
non-closure claim (L3) are appropriately scoped and already meet the bar this
project holds documented assumptions to.

## Verification performed

- Re-ran `uv run python experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/drag-anchor-validation.py`
    end-to-end: V1 (241.2 vs 247 m/kg^(1/3), ratio 0.9764), V1b (geometric
    cube/sphere inversion → 7846/7832 kg/m³), V2 (RMS 0.864→0.349 all-points,
    0.710→0.092 on M>0.7, PASS against the ≤0.10 bar), and V3 (the 155mm
    m_min/N_leth table) all reproduce **exactly** the numbers quoted in
    `derivation.md` §4.
- Re-ran the two supporting scoping scripts also cited by the derivation:
    `required-retardation-vs-mach.py` (reproduces the 0.259/0.072 Fig-3-integrated
    RMS used in derivation §5 to reject Mach dependence) and
    `tolch-count-post-shape-closure.py` (reproduces the 3.9–5.6× N/observed row
    used in L1). Both match.
- Cross-checked the cited source passages directly against
    `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/10-F-0806_Fragment_and_Debris_Hazards.md`
    lines 299–373: the mass-area law (line 316), k=660 gr/in³=2.60 g/cm³ (line
    321), "constant at its supersonic value of 1.28" (line 338–339),
    L=2(k²m)^(1/3)/(C_D ρ) (line 350), L1=247 m/kg^(1/3) (line 358), and the
    gravity-perturbation discussion (lines 360–373) all read exactly as quoted.
    `figure-3-digitized.md`'s (Mach, C_D) table matches the ±0.02/±0.1
    uncertainty derivation §5 relies on.
- Independently re-derived identity (4) from the two area closures
    ($A=(m/k)^{2/3}$ vs $A=C_{shape}(m/\rho_{steel})^{2/3}$, both dimensionally
    m², kg/(kg/m³)=m³ then ^(2/3)=m²) — algebra matches the boxed result.
- Independently checked dimensions of eq. (3):
    $[\rho_{air}][C_D][C_{shape}]/[\rho_{steel}^{2/3}]\cdot[m]^{-1/3}$ →
    (kg/m³)/(kg/m³)^{2/3}·kg^{-1/3} = m⁻¹. Correct, λ is 1/length as required by
    $v=V_0 e^{-\lambda s}$.
- Ran an unweighted per-caliber breakdown of the V2 RMS (not in the derivation,
    a robustness check on my own initiative, since the 25-point set is
    caliber-imbalanced — 3/11/11): 75mm 0.706→0.101, 105mm 0.678→0.094, 155mm
    0.760→0.086 (arrival M>0.7 subsets). All three calibers individually pass
    the ≤0.10 bar at the adopted constant and all three individually fail badly
    at 0.585 — the aggregate RMS is not an artefact of caliber imbalance.
- Checked `min_lethal_mass`'s bisection bounds (`m_lo=1e-6`, `m_hi=2.0` kg,
    `src/arty/fragmentation.py:322-362`) against the new, larger λ: at s=120 m
    (derivation's most extreme demo row) m_min=12.08 g, three orders of
    magnitude below the 2 kg cap — no saturation risk introduced by raising the
    constant (this project has previously flagged m_hi-saturation as a real
    failure mode; not triggered here).
- Confirmed no physics/constants leaked into any `.qmd`: the only `.qmd`-family
    file touched by this change-set is
    `experiment/fragmentation-field/challenges/drag-gap-1944/README.md`, and its
    diff is annotation-only (⚠-marks on superseded conclusions, citing numbers
    already verified above) — it computes nothing.

## Findings

**Note 1 — "within 0.2%" is slightly loose for the sphere row.**
`derivation.md` lines 101–103: the cube inversion is 7846/7850 = 0.05% off,
but the sphere inversion is 7832/7850 = 0.23% off, marginally outside the
literal "0.2%" claim. Impact: none — both still support the qualitative point
(inverting DoD's own cube/sphere *k* through identity (4) recovers the density
of steel to a few tenths of a percent, with no free parameter). No output
changes; a wording nit only.

**Note 2 — combined-constant rounding between scoping (2.67) and derivation
(2.0890/2.6739) already self-disclosed.** `derivation.md` lines 76–79
explicitly flags and explains the 0.2% discrepancy between scoping's rounded
table value and the exact identity value, and directs the implementer to use
the derived expression rather than a decimal literal. This is exactly the
right way to close a cross-document rounding gap — no action needed.

**Note 3 — V2's RMS metric pools three calibers with unequal point counts
(3/11/11).** Not raised by the derivation. My own per-caliber breakdown above
shows this doesn't matter here (all three calibers pass individually), so it
is not even a deferrable limitation — recorded only so a future reader doesn't
have to re-run the check to confirm the aggregate isn't hiding a caliber-level
failure.

## Limitations already logged (assessed as adequate, not re-litigated)

- **L1** (Tolch absolute count 4–6× high) — correctly attributed to the count
    chain / hole-detection cutoff rather than drag, with the reasoning
    (test-cleanliness, pre-existing count bias, observational cutoff,
    admissibility) laid out; the reviewer's own re-run of
    `tolch-count-post-shape-closure.py` matches the cited 3.9–5.6× numbers.
- **L2** (sub-Mach-0.7 tail unclosed, not gravity) — the terminal-velocity
    argument ($20$–$23$ m/s vs. observed $117$–$154$ m/s) is a valid order-of-
    magnitude rule-out; correctly scoped as outside the stated fidelity bar
    (arrival M>0.7 only).
- **L3** (does not close `drag-gap-1944`) — correctly quantifies the remaining
    headroom (~10% before the fragment would need to be denser than a solid
    cube) and explicitly forecloses re-litigating by further raising drag.

## Suggested corrections (not applied)

- Derivation.md line 102: soften "within 0.2%" to "within ~0.25%" or drop the
    number and just say "both land within a few tenths of a percent of steel"
    to match the sphere row's actual 0.23%.

No other correction suggested — the identity, the unit checks, the geometric
bounds, and every reported number were independently reproduced.

---

# Review — implementation (`src/arty/fragmentation.py`, `tests/test_fragmentation.py`)

**Scope.** `git diff src/arty/fragmentation.py tests/test_fragmentation.py`
against derivation.md §6's spec: `DragParams` defaults, the new
`c_shape_from_ballistic_density` helper, and the two updated R50 test bands.
Test suite already confirmed green (307 passed, 4 skipped, 6 deselected) by
the dispatching agent; not re-run here except where a specific number needed
independent confirmation.

## Verdict: **PASS-with-limitations**

No blocking defect in the reviewed diff itself — the implementation is a
faithful, exact transcription of derivation.md §6. One real, silent defect was
found, but it sits in `app/sensitivity.py`, a file **outside the reviewed
diff** and not mentioned in derivation.md §6's spec; it is logged below as an
out-of-scope-but-real finding for the main agent to triage, not counted
against this diff's verdict.

## Verification performed

- Recomputed `c_shape_from_ballistic_density(2600.0, 7850.0)` = 2.0889636…,
    matching derivation.md's quoted 2.0890 to 4 sig figs; `C_D * C_shape` =
    2.67387, matching the derivation's "2.674 (was 0.585)".
- Confirmed `retardation_coeff` (fragmentation.py:314–321) is **byte-for-byte
    unchanged** by the diff (not in the diff hunks) and its body still matches
    eq. (3) verbatim — the derivation's §6 item 3 ("unchanged") is satisfied.
- Confirmed the helper's signature/dimensions: `c_shape_from_ballistic_density(k: float, rho_steel: float) -> float`
    returns `(rho_steel/k)**(2/3)`, dimensionless in ⇐ (kg/m³)/(kg/m³) raised
    to a power — matches identity (4) exactly, no unit slip.
- Ran `compute_frag_field()` with current defaults: **R50 = 46.075 m**,
    matching the test comment's "R50 = 46 m" and sitting mid-band in the new
    `30 <= r50 <= 80` assertion.
- Ran `compute_frag_field(drag=DragParams(C_D=0.65, C_shape=0.90))` (the old
    defaults): **R50 = 91.15 m**, matching the test comment's "R50 = 91 m"
    exactly and confirming it falls *outside* the new upper bound of 80 — i.e.
    the new band is not loosened to paper over anything; it is tight enough
    that reverting the drag anchor by accident would fail
    `test_r50_in_expected_range` and `test_airburst_prone_advantage`, exactly
    as both new comments claim.
- Checked `test_ke_by_mass_radial`, `test_retardation_decreasing_with_mass`,
    and the three `min_lethal_mass` tests for stale hardcoded golden values the
    diff should have touched but didn't: none hardcode a drag-sensitive
    numeric literal in an assertion (they use `pytest.approx` against
    self-consistent quantities, or loose structural bounds), so no update was
    needed there. Derivation §6 item 4's prediction ("Expect golden-value
    updates" limited to R50/lethal-count-adjacent tests) is consistent with
    what the diff actually touched — no missed test.
- Grepped `tests/` and `app/` for other references to the old `C_D=0.65` /
    `C_shape=0.90` literals or the old `50–200 m` R50 band: none remain in
    `tests/`. `app/sensitivity.py` does reference `DragParams()` defaults (see
    Finding 1 below).

## Findings

**Finding 1 (out-of-scope observation, not counted against this diff's
verdict) — `app/sensitivity.py`'s C_D slider bound is now silently stale.**
`app/sensitivity.py:108–110`:
```python
C_D = st.slider(
    "C_D (drag coefficient)", 0.40, 0.90, float(DragParams().C_D), step=0.01
)
```
`DragParams().C_D` is now 1.28, above the hardcoded `max_value=0.90`. This
file is not part of the reviewed diff and not addressed by derivation.md §6,
so it is not a defect *in this change*, but it is a direct, silent consequence
of it. I confirmed with `streamlit.testing.v1.AppTest` that this does not
crash: Streamlit's slider widens `max_value` to match an out-of-range default
(`slider.py` lines 944–949, "adjusting the bounds as necessary") — the
rendered slider silently becomes 0.40–1.28, not 0.40–0.90. Impact: the Drag
expander's C_D control on the Sensitivity page silently exposes a ~42% wider
range than its own coded/intended ceiling, with no test coverage (`tests/`
has no reference to `sensitivity`, confirmed by grep) so the 307-green suite
cannot catch it. The `C_shape` slider (0.50–3.00) is unaffected — the new
default 2.089 sits comfortably inside it. **Deferrable / adjacent-file
follow-up**, not blocking: it is a widget-bound staleness in a file this pass
did not touch, not a physics or numerics error, and the silent widening is
harmless (it does not clip or misrepresent the underlying physics — the
slider still maps 1:1 to a valid `DragParams.C_D`). Suggested correction (not
applied): bump the slider's `max_value` in `app/sensitivity.py:109` to comfortably
bracket 1.28 (e.g. 1.50, matching the geometric/admissibility discussion in
derivation.md §3) so the coded bound and the actual default agree again.

**Finding 2 (Note) — `min_lethal_mass_returns_m_hi_when_all_sub_lethal`'s
explanatory comment is now off by ~1000×.** `tests/test_fragmentation.py:514`:
`# m_hi=0.1g at 50m with E_leth=500J: KE≈7J < 500J`. Recomputed with current
defaults: KE at m=1e-4 kg, s=50 m is **0.0065 J**, not ≈7 J — the much larger
λ now decays this small fragment's KE far harder over 50 m. The assertion
itself (`result == pytest.approx(m_hi)`, i.e. "still sub-lethal") is
unaffected and still correct — 0.0065 J is, if anything, more clearly
sub-lethal than 7 J was. Impact: none on test correctness or on any rendered
output; the comment's illustrative number is stale documentation, not a
behavioural claim anyone depends on. The sibling comment on
`test_min_lethal_mass_returns_m_lo_when_all_lethal` ("KE≈485J") was checked
and is still accurate (454.9 J, ~6% off, unaffected in direction). No action
required beyond an optional comment fix.

**Finding 3 (Note) — derivation.md §6 item 1 wording ("do not leave C_shape
documented as a presented-area shape factor with no provenance") is honored.**
The new `DragParams.C_shape` docstring comment (fragmentation.py:186–189)
names eq. (4), k, and ρ_steel explicitly, and the preceding module comment
block (145–162) carries the full derivation summary. No gap.

## Suggested corrections (not applied)

- `app/sensitivity.py:109` — raise the C_D slider's `max_value` from 0.90 to
    comfortably bracket the new default (e.g. 1.50), so the coded bound and the
    live default agree (Finding 1).
- `tests/test_fragmentation.py:514` — update the comment's "KE≈7J" to
    "KE≈0.006J" or drop the illustrative number (Finding 2).

## Limitations to log

None beyond what derivation.md §7 (L1–L3) already logs; this pass introduces
no new physics, only a faithful transcription. Finding 1, if the main agent
chooses to log it rather than fix it immediately, should be recorded as: "the
Sensitivity page's C_D slider bound (`app/sensitivity.py`) was not updated
alongside the DoD-1975 drag anchor and now silently widens past its coded
0.90 ceiling to accommodate the new 1.28 default — cosmetic/UX only, no
physics impact, tracked for a follow-up UI-only commit."

# Review — Tolch (1938) pit-recovery count re-baseline (803 → 779)

**Scope.** The uncommitted working-tree diff closing the ledger finding that
`TOLCH_PERFORATIONS` (and the "~700–800"/"~4–6×" language derived from it)
rested on a published pit-recovery count of 803 when the source's own
screen-recovery table and body text give 779. Files reviewed:
`checks/tolch-count-post-shape-closure.py`, `derivation.md` (L1 restatement +
2026-08-08 re-run note), `scoping.md` (§3d table + re-run note),
`challenges/drag-gap-1944/README.md` (row #6), and
`challenges/source-data-audit/ledger.md`.

## Verdict: **FAIL**

**Finding 1 (Blocking, resolved 2026-08-09 by the main agent after this
review) — the ledger finding this pass exists to close was never closed; it
still read as an open Blocking item.** The blocking marker at
`challenges/source-data-audit/ledger.md:600`
("the pit-test recovered-fragment count is 803 in committed artifacts...")
was byte-for-byte unchanged in the diff. Contrast with the two *other* Blocking
findings edited in this same ledger.md diff (B-vs-range wrong-column,
SAND92-0243 floor): both had their marker line **deleted outright** and
replaced with a `*(Closed 2026-08-08: ...)*` prose note, which is the pattern
`.claude/rules/deferred-findings.md` requires ("Close a finding by deleting
its marker — never by editing the register") and the pattern that makes
`collect-findings.py` stop reporting it. The 803→779 marker got neither
treatment. Consequence, confirmed two ways: (a) `uv run python
src/utils/collect-findings.py --for experiment/fragmentation-field/updates/mach-dependent-fragment-drag`
still returned this exact finding as the first Blocking hit; (b) the diff to
`OPEN-FINDINGS.md` showed the "## Blocking (3)" section still carrying this
entry (only its line number shifted, 589→600) alongside the two genuinely-new
2026-08-08 blocking items — it was never removed. Impact: the audit register
was factually stale (it still asserted "803 in committed artifacts," which is
no longer true of the two files it names) and would mislead or duplicate work
in the next dispatch briefed from `OPEN-FINDINGS.md`, since a future pass has
no way to tell "already fixed, marker forgotten" from "still open." **Closed:**
the marker at `ledger.md:600` has since been deleted and replaced with a
closure note naming the three files actually fixed, and `OPEN-FINDINGS.md`
regenerated.

**Finding 2 (Note, informational only) — the substantive fix is correct and
verified.** Independently re-ran `checks/tolch-count-post-shape-closure.py`;
its printed table reproduces every number quoted in `derivation.md`'s L1
re-run note and `scoping.md` §3d exactly (E_thr 3.2–6.1 J / m_thr 0.026–0.052 g
/ N/observed 2.8–4.1× at combined 2.67; 1–9 counts at 0.585; TOLCH_PERF_LO/HI
= 700/779, midpoint 739.5).

> **Superseded 2026-08-16 — this reproduction is stale, not wrong at the
> time it was written.** The script calls `mott_params` with no `f_breakup`
> override, so its output silently moved when commit `74abdd7` (2026-08-10,
> one day *after* this review pass) changed that default. Re-run today the
> script prints E_thr 4.6–8.6 J / m_thr 0.033–0.067 g / N/observed 2.5–3.6× at
> combined 2.67 and **0–4 counts** (not 1–9) at 0.585 — see
> `scoping.md` §3d and `derivation.md` §7 L1, both restated to match. The
> reproduction claim below no longer holds against current source; the
> conclusion it was checking (status-quo drag is vetoed by Tolch) is
> unaffected and, if anything, strengthened by the restatement.

The 779 figure itself is source-backed by a
passing closure invariant (`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/pit-screen-recovery.invariant`,
confirmed re-run: "5 rows, 6 checks, ok") that shows 4 of 5 screen rows fail
their printed percentage under 803 and all close under 779, and by
`challenges/count-gap-1938/rebaseline-verdict.md` (path confirmed to exist and
to state "Recovered pit count is 779, not 803" with its own closure evidence,
lines 70–77). All remaining "803"/"750" strings inside the update folder
(`derivation.md:278`, `scoping.md:171`, `checks/tolch-count-post-shape-closure.py:12,34`)
are explanatory historical references ("re-baselined from a published 803"),
not live citations — no stale live figure remains in this update. This
finding does not change the verdict; it is recorded so Finding 1's fix is not
mistaken for a physics problem.

**Out-of-scope observation (for main-agent triage, not this pass's fault).**
`checks/tolch-count-post-shape-closure.py`'s V0 sweep tuple (`807.5, 838.2,
951.0`, current line 61) still carries the pre-gamma'-recloser V0=807.5 figure
that a separate, already-open 2026-08-08 Blocking finding names at this exact
file (`...tolch-count-post-shape-closure.py:48 (V0 sweep tuple)`,
`OPEN-FINDINGS.md` "this table was scoped but never actioned for most rows").
That finding is already correctly tiered Blocking and already tracks this
file — it does not need re-tiering here, just flagging that it was not
addressed by this pass either.

## Suggested corrections (not applied)

- ~~`challenges/source-data-audit/ledger.md:600` — delete the marker line and
    replace with a `*(Closed <date>: ...)*` note naming the three files
    actually fixed (Finding 1).~~ Done 2026-08-09, see Finding 1 above.
- ~~Regenerate `OPEN-FINDINGS.md` after the above so the Blocking count
    reflects reality.~~ Done.

## Limitations to log

None beyond what is already logged. Finding 1 is a register-hygiene defect,
not a physics limitation, and should not be logged as one — it should simply
be fixed (delete the stale marker) before this change is considered closed.
