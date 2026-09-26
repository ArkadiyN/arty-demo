# Review — r50-not-reached

## Verification review, 2026-09-26

**Verdict: PASS-with-limitations**

Scope: `src/arty/fragmentation.py` R50 edits, `app/sensitivity.py` R50 edits,
`tests/test_fragmentation.py` R50 edits, and
`experiment/fragmentation-field/updates/r50-not-reached/` (derivation + check script).

Pre-review: `collect-findings.py --for experiment/fragmentation-field/updates/r50-not-reached/`
returned no open findings. Six open findings on `src/arty/fragmentation.py` are all
pre-existing and out of scope for this change.

---

### 1. Check script output vs derivation before/after table

Script: `experiment/fragmentation-field/updates/r50-not-reached/checks/r50-before-after.py`
Run: `uv run python experiment/fragmentation-field/updates/r50-not-reached/checks/r50-before-after.py`

Output (verbatim):

```
105 M1 hb=20 AoF=0 standing        maxPk=0.152  before= 11.00 m  after=   nan m  grid step=1.00 m
105 M1 hb=20 AoF=0 prone           maxPk=0.314  before=  1.00 m  after=   nan m  grid step=1.00 m
105 M1 hb=0.5 AoF=0 standing       maxPk=1.000  before= 15.00 m  after= 15.04 m  grid step=1.00 m
105 M1 hb=0.5 AoF=0 prone          maxPk=1.000  before=  8.00 m  after=  7.92 m  grid step=1.00 m
default hb=0.5 AoF=30 standing     maxPk=1.000  before= 17.22 m  after= 16.36 m  grid step=2.03 m
default hb=10 AoF=30 standing      maxPk=0.425  before= 15.19 m  after=   nan m  grid step=2.03 m
default hb=10 AoF=30 prone         maxPk=0.261  before= 17.22 m  after=   nan m  grid step=2.03 m
1D compute_frag_field default      maxPk=1.000  before= 44.57 m  after= 44.44 m  grid step=1.50 m
```

Every row matches the derivation's before/after table exactly. Crossing cases move by
less than Δ/2 as claimed: largest move is 0.86 m on a 2.03 m grid (Δ/2 = 1.015 m).

**[Note] The check script is untracked (in `r50-not-reached/checks/`), committed as part of
the untracked folder. No action needed here — it must be staged with the rest of
`experiment/fragmentation-field/updates/r50-not-reached/` in the commit.**

---

### 2. Consumer trace

Grep of `src/`, `app/`, `experiment/`, `tests/` for `r50`, `argmin.*0.5`, `idx50` finds
exactly the consumers in the derivation table. No unlisted consumer was found.

Confirmed:
- `compute_frag_field_3d`: argmin replaced by `r50_cross_slice` (fragmentation.py:1818)
- `compute_frag_field` (1D): argmin replaced by `r50_outer` (fragmentation.py:762)
- `app/sensitivity.py _compute_zones`: private argmin copy replaced by `r50_cross_slice` (line 259)
- App metrics and three figure titles: `_fmt_r50` helper used in all three places (lines 380, 387, 812, 845, 864)
- `_plotly_elevation` call: finite guard `if np.isfinite(result.r50_cross) else 0.0` (line 823)
- `_r50_contour`: traces the 0.5 plotly contour directly on the field; does not use `r50_cross`. Unaffected.
- `test_3d_ground_burst_limit`: updated assertions (test_fragmentation.py:476-479)
- `test_r50_in_expected_range`, `test_backward_compat`: 1D r50 (44.44 m) stays within 30-80 m band
- `mach-dependent-fragment-drag/checks/r50-drag-anchor-shift.py`: uses 1D r50; now interpolated, shift ≤ Δ/2
- `wdss1-steel-grade/checks/recompute.py`: uses 1D r50; now interpolated, shift ≤ Δ/2
- `target-area-profile/checks/posture-crossover-ground-vs-air.py`: prints r50_cross; now prints nan at h_b=20 m. Derivation notes "argmin artefact" wording in its docstring is stale (another pass's file, not in scope here).
- `_field-plots.qmd:31`, `_change-log.qmd:51,61`: own inline argmin, not touched (covered by deferrable finding)

---

### 3. Definition choices

**Outermost crossing** (`r50_outer` takes `above[-1]`, the last sample where pk >= 0.5, then
interpolates to the next sample below 0.5): correct for non-monotone (airburst ring) profiles
where the inner rising flank would give a smaller, wrong value. The ring test in
`test_r50_outer_helper` confirms this: pk=[0,1,1,0] gives 25 m (outer edge), not 5 m (inner).

**NaN for not reached** (`above.size == 0`): no division by zero, type stays float.
Downstream arithmetic on NaN is visibly undefined rather than silently wrong. ✓

**+inf for beyond domain** (`i == r.size - 1`): the last sample is above 0.5, so R50 lies
outside the computed grid. Returning the domain edge would be a distance the field does not
support. ✓

**Larger half of cross-range slice** (`r50_cross_slice` takes `max(vals)` after filtering NaN):
conservative bound for asymmetric profiles (angled AoF). ✓

**Interpolation arithmetic** (fragmentation.py:722-724): with p0 = pk[i] >= 0.5 and
p1 = pk[i+1] < 0.5, the denominator `(p0 - p1) > 0` — no division by zero. Fraction
`(p0 - 0.5) / (p0 - p1)` ∈ [0, 1). Result ∈ [r[i], r[i+1]). ✓

**Negative-half reversal** (`r50_cross_slice`: `-y[neg][::-1]`): `y[neg]` = values ≤ 0;
reversed is ascending from most-negative to 0; negated makes it ascending from 0 outward.
The corresponding pk values are correctly co-reversed. ✓

All definition choices are consistent and documented in derivation.md. ✓

---

### 4. Tests

`uv run pytest -q --ignore=tests/test_pdf_processor.py`:

```
227 passed, 1 skipped, 6 deselected in 4.95s
```

**`test_3d_ground_burst_limit` still tests something meaningful.** Old test: asserted
`r50_cross > 0` on both h_b=0 and h_b=10 m cases — the second was passing on the argmin
artefact (peak location, not a crossing). New test:

1. Explicitly asserts `r_lo.r50_cross` is finite and positive (the near-ground burst
   definitely reaches P_k > 0.5 everywhere near the burst).
2. For both r_lo and r_hi: asserts the defined-iff-reached invariant
   `np.isnan(r50) == (pk_cross.max() < 0.5)`. This is the semantic invariant of the
   new helper.

The h_b=10 m case at n_grid=30 is grid-marginal (~0.50 peak); the test correctly avoids
asserting either NaN or finite for that case, checking only the invariant.

Three new tests added: `test_r50_not_reached_is_nan` (explicit NaN), `test_r50_outer_helper`
(unit tests: NaN / inf / ring / asymmetric cross-range). All pass. ✓

---

### 5. App display of NaN and inf

`_fmt_r50(r50)` (sensitivity.py:364-370):
- `np.isnan(r50)` → "not reached" ✓
- `np.isinf(r50)` → f"> {max_radius:.0f} m" ✓
- finite → f"{r50:.0f} m" ✓

`_r50_delta(r50, pk_max)` (sensitivity.py:373-375):
- Returns the max P(kill) caption when NaN (so user sees why R50 is absent) ✓
- Returns None when finite (metric delta suppressed) ✓

`_plotly_elevation` guard (sensitivity.py:823): passes `0.0` when r50 is non-finite.
`x_max = max(abs(0.0) * 1.5, 50.0) = 50.0` — falls back to the stated 50 m floor. ✓

All four metric call sites and all three figure title sites use `_fmt_r50`. ✓

---

### 6. Deferrable finding tier — `_field-plots.qmd` and `_change-log.qmd`

The deferrable marker in derivation.md (line 81) is correctly tiered.

The two notebooks use `r_vals[np.argmin(np.abs(P - 0.5))]` on 1D ground-burst profiles
(`r_vals = np.linspace(2, 300, 250)`) that start above 0.5 and fall monotonically. On a
strictly monotone profile the argmin is the unique crossing, so it agrees with `r50_outer`
to within one grid step (Δ = 298/249 ≈ 1.20 m). No qualitative output change.

The tier would move to Blocking if a notebook cell were extended to a not-reached profile
or a non-monotone (airburst) profile — the argmin would silently report a peak location
as an R50. That is a future risk, not a current defect. The pattern is also a layering
violation (inline physics/computation in .qmd), but with no current numeric impact.

Limitation to log: `_field-plots.qmd` and `_change-log.qmd` compute R50 inline with
`argmin |P-0.5|` instead of `arty.fragmentation.r50_outer`; correct on their
monotone ground-burst inputs but would silently mis-report on a not-reached or
non-monotone profile.

---

### Findings summary

| # | Tag | Location | Finding | Impact |
|---|---|---|---|---|
| 1 | **Deferrable** | `_field-plots.qmd:31`, `_change-log.qmd:51,61` | Inline argmin R50 instead of `r50_outer`; correct on current monotone inputs, would mis-report on not-reached or airburst profiles | No current numeric effect; risk on extension |

No Blocking findings.

---

### Script to stage

`experiment/fragmentation-field/updates/r50-not-reached/checks/r50-before-after.py`
is untracked. It must be included in the commit that lands `r50-not-reached/`.
