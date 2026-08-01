# Review — Mott fragment shape closure derivation

Scope: `derivation.md` in this folder (pre-implementation, no `src/arty/`
changes yet). Also read `scoping.md` and the three prior challenge notes
(`_params_provenance_note.md`, `_scale_verdict_ledger.md`,
`_shape_closure_check.md`) it builds on.

## Verdict: **PASS**

No Blocking findings. The closed form is dimensionally sound, every
governing equation and numeric literature value was checked against the
actual source text (not just the derivation's paraphrase), and every
numeric claim in the document was reproduced independently by re-running
`experiment/_scratch/mott_shape_closure.py`. All identity, mass-closure,
tiling, and Tolch/registry-table numbers match the script output to the
displayed precision. Several deferred items are already logged as
assumptions (§9) or explicit src-pass action items — these are correctly
classified as deferrable, not blocking, and are listed below with the
language they should carry into the eventual `_limitations.qmd`/test
updates.

## Verification performed

- Re-derived the closed form (2)/(3) algebraically from Gold eq. (2), (4),
    (6): confirmed `ρ` cancels exactly (x̄² ∝ 1/ρ offsets the ρ in
    `2μ = ρl̄x̄t₀`), confirmed `α = A κ_x² t_bu/x₀` reduces correctly to
    Gold eq. (16)'s shape-absorbed form, and confirmed the "cube limit"
    (`A=κ_x=1, t₀=x₀`) reproduces the currently-coded expression exactly.
- Read Gold 2017 (`fragment-size-distribution-conwep/1-s2.0-S221491471730079X-main.md`
    lines 50–124, 190–225): eq. (2)/(4)/(6)/(7)≡(16) transcribed correctly;
    confirmed eq. (17) `N_0j = m_j/μ_j` (no factor of 2) genuinely
    contradicts line 54 `N₀ = M/2μ` — the derivation's claim that Gold's
    own eq. (17) is a typo, not a second convention, is correct and the
    resolution (follow line 54) is the only self-consistent reading.
    Confirmed Gold's own `γ` values (50, and 50/40/30/20 in the variable-γ
    study) support the derivation's "20–50 published range" claim used as
    an independent corroboration check in §7.4.
- Read Mott 1947 (`rspa.1947.0042.md` lines 150–205): confirmed line 190
    verbatim — "average length is about 1.5x₀" — and confirmed the
    ruled-line setup (lines 162–190) is explicitly a 1-D model of the
    *circumference*, supporting the derivation's reading that Mott's
    "average length" and Gold's "average circumferential length" (x̄) are
    the same quantity — a non-trivial but well-argued identification.
- Read `explosion-fragment-model/1-s2.0-S221491472030502X-main.md` line
    137: confirmed the 1:1.6 width:length aspect ratio and its
    cross-dataset provenance (Mott/Grady/Hiroe, corroborated by
    Wilson 1:1.65 and Grady 1:1.5) as cited. Confirmed the paper's own axis
    convention (line 104: X = circumference = width, Y = axial = length)
    matches how the derivation applies `A = l̄/x̄`.
- Verified identity (1) `t_bu·r_bu = t·r_mean` algebraically from
    `_shell_geometry`'s incompressibility bookkeeping
    (`r_o,bu² − r_i,bu² = r_o² − r_i²`) — holds exactly, independent of the
    numeric check.
- Ran `experiment/_scratch/mott_shape_closure.py`: every number quoted in
    derivation.md §6, §7.1–7.5 (x̄, l̄, t_bu, α, γ, μ, N₀, the four-point
    Tolch table, the 105/155/60 mm transfer table, the tiling ratios
    1.0000/1.6346, the mass-closure integral 5755.20 g, and the
    tumbling-average `C_shape` values 1.61/1.50) reproduced exactly.
- Confirmed `tests/test_fragmentation.py::test_mott_fragment_count_in_pafrag_range`
    (and `_all_grades`) currently assert the 3000–8000 band, and confirmed
    `_validation.qmd` Check 3 carries both the 3000–8000 model-consistency
    row and the 800–3000 arena-recovery row — matching the derivation's
    §7.4 claim precisely and validating its recommendation to re-base the
    test onto the data row rather than widen the existing band.
- Sanity-checked units on eq. (2): `[σ_F·t·(r/V)²] = (kg·m⁻¹s⁻²)(m)(s²) = kg`.
    No division-by-zero or negative-sqrt exposure: every denominator
    (`γ′`, `V₀`, `x₀`) is structurally positive for any physically valid
    shell/steel input.

## Findings

1. **Note.** §6's prose "the model prism is ~2× under on each in-plane
     dimension" compared to the ledger's ≈12×12×6 mm estimate is imprecise:
     the actual ratios are 12/9.39 ≈ 1.28× on `l̄` and 12/5.87 ≈ 2.04× on
     `x̄`, not a uniform 2× on both. This is descriptive commentary only —
     it feeds no downstream calculation — so it has no numeric impact.
     Suggested correction: reword to "the in-plane dimensions are 1.3–2.0×
     under, still of the right character (a plate, not a cube)."

2. **Deferrable.** The fidelity target (scoping §8) asks for `μ` inside
     0.95–3.5 g; the derived value is 0.79 g, 1.20× under the floor. The
     derivation correctly attributes this residual to the deliberately
     out-of-scope break-up-velocity item (scoping §5) and forbids absorbing
     it into `A` or `κ_x` (§7.3, A9.7). This is a legitimate, already-logged
     limitation, not a defect in this closure. **Limitation entry
     language**: "`μ` for the 75 mm M48 (0.79 g) sits 1.2× below Tolch's
     mass-constrained floor (0.95 g); the residual is attributed to feeding
     `mott_params` the terminal Gurney velocity `V₀` in place of the
     break-up velocity (`μ ∝ V₀⁻²` under this closure) — see
     `updates/mott-fragment-shape-closure/derivation.md` §4/A9.7 for the
     predicted size (1.6–1.8×) of that separate, deferred correction."

3. **Deferrable.** The 60 mm M49A2 mortar has `t_bu/x̄ = 1.14` (past the
     thin-case regime this closure assumes) and its implied `γ_eff = 14`
     falls below Gold's own published 20–50 calibration range — both
     already flagged in derivation §5 item 5 and §7.4 as needing a
     limitation note, not a fix. **Limitation entry language**: "The 60 mm
     M49A2 mortar's wall-to-breadth ratio at break-up (`t_bu/x̄ ≈ 1.14`)
     exceeds the thin-plate regime this shape closure assumes (other
     registry shells: 0.63–0.95); its derived `γ_eff ≈ 14` falls outside
     Gold's (2017) published 20–50 range for this parameter. Treat 60 mm
     mortar fragment-mass output as lower-confidence than the three gun
     shells."

4. **Deferrable — action item, not a derivation defect.** §7.4 documents
     that `test_mott_fragment_count_in_pafrag_range[_all_grades]` will
     nominally fail against the existing 3000–8000 band and recommends
     re-basing it onto the 800–3000 arena-recovery band already present in
     `_validation.qmd` Check 3, with the reasoning recorded in the test
     comment. Verified both bands exist as described; the recommendation
     is sound. This is correctly scoped as the *src pass's* job — flagged
     here only so the reviewer of that pass checks it was actually done
     (re-base + comment explaining why 3000–8000 was model-vs-model, not
     data), rather than silently widening the old band (which would
     re-import the defect this update removes).

5. **Note.** `wall_t` for the 75 mm M48 becomes first-order in `μ`
     under this closure (previously a weaker exposure) and is an unsourced
     caliber-scaled estimate (`shells.py:57`). Already logged as A9.6 with
     a bounded impact estimate (±20% wall error → ±20% on `μ`, inside the
     factor-2 fidelity target) and an optional (not required) `@librarian`
     ask. No further action needed unless the src pass wants to close it.

No other issues found. The `ρ`-cancellation, `γ′`-exponent weakening
(`γ′⁻³/₂ → γ′⁻¹`), and `r_bu`/`V₀` sensitivity changes documented in §4 were
all independently re-derived and confirmed correct — these are disclosed
consequences of the physics fix, not new defects.

## Scope note

This is a pre-implementation review of `derivation.md` only; there is no
`.qmd` or `src/arty/` diff to check for physics leakage or layering
violations at this stage. That check applies to the subsequent
implementation pass.

______________________________________________________________________

## Addendum (2026-07-31) — `src/arty/zones.py` gap-closure review

**Scope.** `git diff -- src/arty/zones.py` and `git diff -- tests/test_zones.py`
(uncommitted at review time), which extend `_zone_mott_mu` (previously the
legacy unshaped cube formula, `SteelParams`-only) to the same Option-A
`α`/`γ` shape closure `mott_params` already carries, plus a new
`_t_bu_from_inner` helper computing per-zone wall-thickness-at-break-up via
identity (1) from §3 of `derivation.md`. This closes a real gap: before this
fix, the single-zone path used the shaped closure and the four-zone path
(`compute_shell_zones` → `_zone_mott_mu`) silently still used the old cube
form, so the two paths disagreed on `μ` for the same shell. No `.qmd` touched
by this diff — no layering/physics-leakage issue to check.

### Verdict: **PASS-with-limitations**

No Blocking findings. The closure math is a correct, dimensionally-sound
mirror of the already-reviewed single-zone form, and the code paths were
verified argument-by-argument (not just read) to apply it consistently. One
real, quantified side effect on the base/boattail zones needs a limitations
entry; it does not block because it (a) is confined to minor-mass zones whose
governing conventions were already flagged as unsourced/approximate, and (b)
is the same *class* of thin-case-regime excursion `derivation.md` finding 3
already accepted as deferrable for the 60 mm mortar — just larger in
magnitude and now present on all four registry shells' base zones rather than
one shell.

### Verification performed

- Re-derived `_t_bu_from_inner(r_i, r_o) = (r_o−r_i)·½(r_o+r_i)/_r_bu_from_inner(r_i,r_o)`
    algebraically against `mott_params`' `t_bu = shell.wall_t·½(r_outer+r_inner)/r_bu`
    (`fragmentation.py:250`) — identical form, `_r_bu_from_inner` is the
    pre-existing per-zone generalisation of `_shell_geometry`'s `r_bu`. Confirms
    identity (1) is applied correctly per zone.
- Checked every zone/tier call site pairs the *same* `(r_i, r_o)` into
    `_r_bu_from_inner` (for `rbu_*`) and `_t_bu_from_inner` (for `tbu_*`) —
    verified for all three annulus zones (ogive, cylinder, boattail) in both
    the Tier-1 (drawing-derived) and Tier-2 (fraction-fallback) branches. No
    cross-zone argument mismatch.
- Base plate: `tbu_base = t_w_base` (no thinning) is the correct pairing with
    the *pre-existing, unmodified* `rbu_base = D/2 − t_b/2` convention, which
    likewise skips the √3 cavity-expansion factor other zones get (the base is
    modelled as an axially-driven disk, not an expanding annulus). The two
    "no expansion" choices are mutually consistent — this diff did not
    introduce an inconsistency here, it correctly extended the existing
    no-expansion convention to the new thinning step.
- Instrumented `_zone_mott_mu` (spy wrapper) to capture the actual `t_bu_z`
    argument used per zone/shell, then computed `α = A·κ_x²·t_bu/x₀` and
    `t_bu/x̄` (`x̄ = κ_x·x₀`) for all four registry shells — reproduced below.
    (An initial pass mistakenly substituted `ZoneParams.wall_t`, the
    as-manufactured thickness, for the thinned `t_bu`; re-verified with the
    instrumented value, which is what the code actually computes.)
- Ran the full suite: 210 passed, 1 skipped (as reported); independently
    reran `tests/test_zones.py tests/test_fragmentation.py` — 91 passed.

| shell | zone | α | `t_bu/x̄` | `μ` new/legacy |
| --- | --- | ---: | ---: | ---: |
| 105mm M1 | ogive / cylinder | 4.64 / 4.86 | 0.86 / 0.90 | 4.6× / 4.9× |
| 105mm M1 | boattail / base | 6.23 / 19.05 | 1.15 / 3.53 | 6.2× / 19.1× |
| 155mm M107 | ogive / cylinder | 9.39 / 6.31 | 1.74 / 1.17 | 9.4× / 6.3× |
| 155mm M107 | boattail / base | 9.02 / 38.37 | 1.67 / 7.11 | 9.0× / 38.4× |
| 75mm M48 | ogive / cylinder | 3.46 / 3.46 | 0.64 / 0.64 | 3.5× / 3.5× |
| 75mm M48 | boattail / base | 9.39 / 17.06 | 1.74 / 3.16 | 9.4× / 17.1× |
| 60mm M49A2 | ogive / cylinder | 6.29 / 6.29 | 1.16 / 1.16 | 6.3× / 6.3× |
| 60mm M49A2 | boattail / base | 16.83 / 31.89 | 3.12 / 5.91 | 16.8× / 31.9× |

(For reference, `derivation.md` §7.4's whole-shell calibration: `α` = 3.38
(75mm), 4.66 (105mm), 5.15 (155mm), 6.15 (60mm); `t_bu/x̄` = 0.63–1.14, with
1.14 (60mm mortar) already flagged in that derivation's own finding 3 as past
the thin-case regime.)

### Findings

1. **Note / no defect.** Ogive and cylinder — the two dominant-mass zones
    (≈65–83% of shell steel across the registry) — land inside or close to
    the whole-shell calibrated `α`/`t_bu/x̄` range above, and their `μ`
    increases 3.5×–9.4× vs. the pre-fix legacy formula, in line with the
    3.4×–6.2× the single-zone closure was validated to produce. This is the
    core purpose of the fix (closing the single-zone/four-zone disagreement)
    and it does so correctly for the zones that carry most of the mass and
    dominate the forward/lateral fields the demo's headline charts show.

1. **Material but deferrable.** The **base zone**, on all four registry
    shells, and the **boattail zone** on the two lighter shells, have
    `t_bu/x̄` ratios of 1.15–7.11 — 1×–6× past the 1.14 ceiling
    `derivation.md` finding 3 already flagged (there, for one shell only,
    the 60 mm mortar) as exceeding the thin-plate assumption the whole
    closure depends on (`t_bu` — the fragment's *smallest* dimension by
    construction — becoming comparable to or larger than its breadth `x̄`).
    `μ_base` inflates 17×–38× vs. the pre-fix legacy value (vs. 3.5×–9.4×
    for ogive/cylinder). Root cause: the base zone's `t_bu` is now
    unthinned (finding above: correctly so, given the pre-existing
    `rbu_base` convention) while its `x₀ ∝ r_bu/V₀` is small (low `V₀^b`
    from the `k^b` reduction factor, small unexpanded `r_bu^b`) — the two
    effects compound `α^b` well past the calibrated zones.
    **Observable impact** (75 mm M48, quantified): at a representative
    rearward slant range (s = 10 m), the base zone's lethal-hit contribution
    `N_leth = N0·exp(−√(m_min/μ))` rises **≈23×** (N0 drops ≈17× but the
    lethal-survival fraction rises ≈400× as `m_min` moves closer to the
    now-larger `μ_base`). A rough four-zone `P(kill)` field probe
    (AoF=45°, h_b=3 m, max_r=40 m, n_grid=40) showed the rear-lobe region
    (x < −5 m) mean `P(kill)` rise **≈2.7×** and max rise **≈2.0×** going
    from an all-legacy-`μ` field to the fixed one — a visible change to the
    rear/base lobe magnitude in the four-zone charts
    (`_four-zone-3d.qmd`, `_lethal-density.qmd`, the `pkill` fields) that
    explicitly render per-zone contributions. This does not block because:
    it is the same *class* of thin-case excursion the project already
    treats as a logged limitation, not a fix, for one shell (finding 3
    above); it is confined to a zone whose driving conventions
    (`θ^b = 165°`, `C^b_eff`, Tier-2 `t_w` scaling) are already flagged in
    `_limitations.qmd` §12 as unsourced/approximate; and it produces no
    out-of-bounds probabilities or numerical instability.
    **Suggested limitation-entry language** (append to `_limitations.qmd`
    §12, "Four-zone model assumptions"): "The base zone's (and, on lighter
    shells, the boattail zone's) fragment shape closure now implies
    `t_bu > x̄` — the fragment thickness exceeds its own breadth, 1.2×–7.1×
    depending on shell/zone, past the thin-plate regime this closure
    assumes (registry whole-shell worst case: 1.14×, `mott-fragment-
    shape-closure/derivation.md` §5 item 5). This inflates `μ^base` 17×–38×
    vs. the pre-fix cube formula (vs. 3.5×–9.4× for ogive/cylinder) and can
    move the rendered rear-lobe `P(kill)`/lethal-density magnitude by a
    factor of ~2–3×. Treat the base-zone (and boattail-zone, lighter
    shells) lobe magnitude as lower-confidence than the ogive/cylinder
    lobes; not corrected here per the same reasoning as the 60 mm mortar
    limitation above."

1. **Deferrable.** The new code comment in `compute_shell_zones` (Tier-1
    branch, the `tbu_base` block) attributes the base-plate no-thinning
    choice to "derivation section 3.4" — but `frag-field-3d-geometry/
    derivation.md` §3.4 is "Per-zone Gurney velocity" and does not discuss
    wall thinning or the Mott shape closure at all; §3.5 documents the
    `r_i,mean^b` convention but not this specific no-thinning pairing, which
    postdates that derivation (it did not exist before the shape closure was
    added). The reasoning given is sound and self-consistent (finding above),
    but the citation currently points at content that isn't there — a
    source-attribution miss, not a physics error. No output impact. Suggested
    correction: either cite §3.5's base-radius-convention paragraph (the
    closest existing anchor) or drop the section reference and instead state
    the pairing rationale inline, as the comment prose already does.

1. **Note.** The two new tests
    (`test_default_shape_factors_preserve_zone_mott_output`,
    `test_higher_aspect_ratio_gives_larger_cylinder_mu`) exercise only the
    cylinder zone directionally; the self-consistency test does check
    `.ogive.mu`/`.base.mu` equality between two defaulted calls but nothing
    exercises boattail, and no test bounds `t_bu/x̄` or `α` for any zone (the
    way finding 2 above would need to be caught by a future regression). Not
    required to block — the cylinder-only coverage is consistent with the
    single-zone precedent (`test_fragmentation.py`) this update mirrors — but
    worth adding a boattail/base monotonicity check and/or a `t_bu/x̄` sanity
    assertion if the base/boattail limitation above is ever revisited.

### Logging recommendation

This fix completes a gap left by the original `mott-fragment-shape-closure`
update (four-zone path never received the shape closure) — recording it here,
in this update's own review, is the right home; no separate update folder is
needed since no new derivation was required (the math is a direct, verified
mirror of already-approved `derivation.md` content). The one action item is
the `_limitations.qmd` §12 addition in finding 2 above, which is new content
(the base/boattail thin-case excursion was not previously documented anywhere,
including in the original derivation, which only characterised the
whole-shell case).
