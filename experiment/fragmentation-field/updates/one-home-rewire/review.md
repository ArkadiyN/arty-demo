# Review — one-home-rewire

**Date:** 2026-09-26
**Scope:** Uncommitted working-tree diff across
`experiment/fragmentation-field/challenges/README.md`,
`challenges/drag-gap-1944/README.md`,
`challenges/drag-gap-1944/b-vs-range.qmd`,
`challenges/drag-gap-1944/checks/b-vs-range-drag-attribution.py`,
`challenges/gravity-ke/gravity.qmd`,
`updates/mach-dependent-fragment-drag/README.md`

**Render status (pre-supplied):** all 34 cells executed without error; no
literal `{python}` strings or tracebacks in the output HTML.

---

## Verdict — FAIL

Two blocking findings; no physics was changed but one introduced a stale-prose
discrepancy and neither blocking item was resolved before the diff stopped.

---

## Findings

### F1 — Blocking: open blocking marker in scope, prose not updated

**File:** `challenges/drag-gap-1944/b-vs-range.qmd`, line 314

The rewire pass replaced the static key-findings table (hard-coded 9/11 for
105 mm) with a code-computed table reading live from `_sum_vars`. The live
computation gives **105 mm 10/11**, not 9/11: only the longest tabulated range
(r = 500 ft) fails, not the two ranges r = 400–500 ft the prose below still
names. The rewire pass inserted a blocking finding marker at line 314
documenting this but did not fix the prose before stopping.

Per the review checklist, a diff that introduces a blocking marker in its own
scope and does not resolve it is a blocking finding for the review. The
description "two-to-three *longest* tabulated ranges (75mm: r=300-400 ft;
105mm: r=400-500 ft)" is factually wrong at current shipped parameters for the
105 mm shell — "105mm: r=500 ft" is the correct description. Impact: a reader
checking whether one or two ranges fail for 105 mm gets the wrong answer from
the prose, while the rendered table shows the correct number.

**Suggested correction:** update the prose to "75mm: r=300-400 ft;
105mm: r=500 ft" (or, since the count is now 10/11, to "the one or two longest
tabulated ranges") and delete the FINDING marker at line 314.

---

### F2 — Blocking: notebook reads untracked results JSON; fresh checkout fails

**File:** `challenges/drag-gap-1944/b-vs-range.qmd` (summary-variables block,
approx. line 438); `checks/b-vs-range-drag-attribution.results.json` (untracked)

The rewire added a `_attr_df` comparison table that reads pre-anchor ratio
spans from `checks/b-vs-range-drag-attribution.results.json`:

```python
_attr = _json.loads(open("checks/b-vs-range-drag-attribution.results.json").read())
_attr_s = _attr["shells"]
```

The JSON is produced by the extended `b-vs-range-drag-attribution.py` and
appears in `git status` as `??` (untracked). On a fresh checkout the file does
not exist; the notebook raises `FileNotFoundError` and the `_attr_df` table
(the pre-anchor vs. post-anchor comparison) cannot render.

The render pass succeeded only because the JSON was already present in the
working tree from a prior script run.

**Suggested correction:** commit `b-vs-range-drag-attribution.results.json`
with the diff. Per `verification-scripts.md`, a script and the artifact it
produces belong in the same commit. The JSON is a permanent output of the check
script, not scratch.

---

## Non-blocking observations

### N1 — Note: README de-duplication is correct

`challenges/README.md` and `drag-gap-1944/README.md` removed inline computed
numbers (specific ratios like "8/10, 9/11, 11/11", "7–34×", "2.674") and
replaced them with links to the notebooks/derivations that own those values.
This is the one-home rule applied correctly. No factual information was dropped;
all figures remain reachable through the linked artifacts.

### N2 — Note: gravity.qmd rewiring is clean

All replaced inline literals (`0.003 %`, `17 cm`, `≈0.6 %`, `±15 %`,
`±30 % on KE`) derive from variables computed by code already in the notebook:
`max_dke_pct`, `worst_drop_cm`, `dke_pct_200m`, `cd_v_swing_*_pct`,
`cd_ke_swing_*_pct`. The sweep loop that produces `df` and the drag-variation
loop were already present; the rewire adds only the scalar captures and
replaces the static prose with inline expressions. No new physics. The
"`±15 %`" → `+X%/-Y%` asymmetric split is more accurate (the V swing for
C_D = 0.5 and C_D = 0.9 is not symmetric) and not a change of substance.

### N3 — Note: mach-dependent-drag README de-duplication correct

Specific numbers removed ("0.585", "2.674", "7–34×", "20–25% RMS", "7.1%",
"5.3%") are replaced by links to the derivation sections and check scripts
where they are computed. Factual substance preserved; no index numbers lost.

---

## Deferred findings from register (pre-existing, not introduced by this diff)

The collect-findings.py run found 15 open findings in this scope; 14 are
pre-existing (raised 2026-08-02 to 2026-08-16) and are not affected by this
diff's re-wiring changes. They are noted here for completeness but are out of
scope for this pass. Finding F1 above corresponds to the one finding raised
2026-09-26 (today) — it was introduced by this diff.

---

## Re-review — 2026-09-26

**Scope:** Second half of the one-home-rewire diff: b-vs-range.qmd fixes
(F1, F2 from first review), doc-sync of stale copies in derivation.md /
rebaseline-verdict.md / stale-surfaces.md / b-vs-range-rebaseline.md, and
partial rewiring of _limitations.qmd, _validation.qmd,
_governing-equations.qmd, _implementation.qmd, _pkill-field.qmd,
_four-zone-3d.qmd.

### Verdict — FAIL

F2 remains open: the results JSON is still untracked.

---

### F1 (first review) — RESOLVED

**b-vs-range.qmd** blocking marker deleted; confirmed by grep (no output).
Prose updated from static "75mm: r=300-400 ft; 105mm: r=400-500 ft" to
inline `{python} _75_fail` / `{python} _105_fail` expressions computed live
from `results`. The count bisect script (`checks/b-vs-range-count-bisect.py`)
re-run at HEAD confirms 105mm is 10/11 (only r=500 ft fails), consistent with
the live expressions. The final-verdict prose at line 485 likewise wired to
`{python} f"{_105['n_pass']}/{_105['n_total']}"`. No static 9/11 or wrong
range description survives.

---

### F2 (first review) — STILL BLOCKING

`experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-drag-attribution.results.json`
is still **untracked** (`??` in git status). The notebook cell added in this
diff reads it unconditionally:

```python
_attr = _json.loads(open("checks/b-vs-range-drag-attribution.results.json").read())
```

On a fresh checkout the file does not exist and the notebook raises
`FileNotFoundError` — the second table in the "Drag attribution" section cannot
render. The task brief notes it "will be committed with this change"; it has
not been staged or committed. The render only succeeded because the JSON was
already present in this working tree from a prior script run.

Suggested correction: stage and commit the JSON in the same commit as
b-vs-range.qmd. Per `verification-scripts.md`, the script and the artifact it
produces belong in the same commit.

---

### New-scope findings — partials rewiring

Checked the four partial passes for blocking issues.

**_limitations.qmd** (limitations partial): specific multipliers (2.25×,
2.51×, 1.73/1.92, 2.47/2.75, 2.09–2.29×) replaced with qualitative verdicts
plus links to `count-chain.md`. The substitution is directionally correct for
the one-home rule; the linked document is responsible for the live numbers.
No physics changed; no new typed computed values introduced. No blocking issue.

**_validation.qmd / _governing-equations.qmd** (validation-goveq partial):
typed computed figures replaced with prose summaries and links to derivation
documents. The 8/10, 9/11, 11/11 triple in `_validation.qmd` was replaced
with "Verdict: PASS — see the 1944 B-vs-range challenge" link, no digits. This
correctly removes a now-stale triple. No blocking issue.

**_implementation.qmd / _pkill-field.qmd / _four-zone-3d.qmd** (misc-partials):
four values rewired to inline expressions or links. No new physics. No
blocking issue.

**Stale-copy doc-sync** (derivation.md, rebaseline-verdict.md,
stale-surfaces.md, b-vs-range-rebaseline.md): the "8/10, 9/11, 11/11" triple
replaced with linked verdict labels pointing to b-vs-range.qmd. Confirmed:
derivation.md now reads "8/10, 10/11, 11/11 — see b-vs-range.qmd". No other
typed figures changed. No blocking issue.

**Malformed marker in triage-105mm-count.md line 71:** collect-findings.py
reports a malformed marker there (a backtick reference that partially matches
the marker syntax). This file is new/untracked and is an analysis document,
not a code artifact. The malformed line is not a blocking finding, but it
will prevent `collect-findings.py` from running cleanly. Note only — the
formatting should be corrected before commit.

---

### Summary

One blocking item remains: the results JSON must be committed. All other items
in this re-review are either resolved (F1) or non-blocking notes (malformed
marker in triage file). The renders (both `fragmentation-field.qmd` and
`b-vs-range.qmd`) completed cleanly as reported.
