# V0 sensitivity — does the 1944 initial fragment velocity reach shipped outputs?

**Pass type.** Workflow A assessment (sensitivity bound). Nothing in `src/arty/`
or any notebook is changed. Check script:
[`checks/v0-sensitivity.py`](checks/v0-sensitivity.py) (every number below
comes from it; re-run with `uv run python experiment/fragmentation-field/challenges/drag-gap-1944/checks/v0-sensitivity.py`).

**Question.** The open finding (raised in
[`rebaseline-verdict.md`](../../updates/mach-dependent-fragment-drag/rebaseline-verdict.md),
"$V_0$ is unverified") says `V0_FTS` = 3120 / 3500 / 3500 ft/s (75 / 105 /
155 mm) has no provenance and is degenerate with the drag constant. Does its
uncertainty move the shipped headline outputs (R50, lethal area)?

## 1. How V0_FTS reaches shipped code — it does not

- **Shipped drag constant is derived, not fitted.** `DragParams.C_shape =   c_shape_from_ballistic_density(_K_BALLISTIC=2600, _RHO_STEEL_REF=7850)`
    (`src/arty/fragmentation.py`, `_K_BALLISTIC` block; TP-12 "Ballistic
    Properties", 2.60 g/cm³) and `C_D = 1.28` (TP-12 plateau). Neither is
    fitted to the 1944 Ordnance $(m, v)$ tables. The 1944 fit (V2) is
    corroboration only — rebaseline-verdict.md C8 item 3 already rules this.
- **Shipped initial velocity is Gurney.** Every field path starts fragments at
    `gurney_velocity(shell)` (× `breakup_velocity_fraction()` where applied),
    computed from the shell's own geometry and filler Gurney constant. No
    `src/arty/` file contains 3120 / 3500 (asserted by the check script, §A).
- **Consequence.** The swing in shipped R50 and lethal area caused by
    `V0_FTS` is **exactly zero, by construction**, for all three calibers.
    What V0_FTS *does* reach is the V2 corroboration margin (§3).

## 2. Provenance — the finding's premise is partly stale

The finding says V0_FTS "has no provenance in the processed 1944 Ordnance
source". The processed source **does print it**, one caption per shell,
directly under the shell heading and governing both tables of the pair
(greppable in `doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md`):

| Shell       | Heading anchor              | Caption anchor                                              |
| ----------- | --------------------------- | ----------------------------------------------------------- |
| 75 mm M48   | `# 75-MM H.E. SHELL, M48`   | `INITIAL FRAGMENT VELOCITY 3,120 F/S`                       |
| 105 mm M1   | `# 105-MM H.E. SHELL,'Ml`   | `INITIAL FRAGMENT VELOCITY 3,500 F/S` (first after heading) |
| 155 mm M107 | `# 155-MM N.E. SHELL, M107` | `INITIAL FRAGMENT VELOCITY 3,500 F/S` (first after heading) |

The same captions are the `anchor:` lines of the six closure-checked
`tables/*.invariant` files. The source states a *different* V0 for sibling
shells (e.g. 105 mm M38A1: 3,320 F/S), so the caption is a per-shell stated
value, not page furniture. `source.pdf` is not on disk in this checkout, so the
caption was confirmed on the derived `.md` only, not on the page image
(surface stated per source-data-fidelity rule).

What remains genuinely open is not provenance but **accuracy**: the source
gives no measurement method or error for V0. §3 bounds that.

## 3. What V0 uncertainty does to the V2 corroboration margin (script §B)

V2 is the RMS over M > 0.7 of ln(v_model / v_src) at the shipped drag
constant, with the bar at 0.10. The script re-runs it with every caption V0
scaled by a common factor *s*.

- **The margin is one-sided.** Both series pass for *s* from about 0.85–0.86
    up to about 1.00. The RMS is lowest at *s* ≈ 0.92–0.93. The caption values
    (*s* = 1) sit at the **upper edge** of the band. If V0 were under 1 % higher,
    V2 would fail. It could be about 14 % lower and still pass.
- **The mean bias is positive** (model faster than source) at *s* = 1. The fit
    would prefer a V0 a few percent lower, or equivalently a slightly larger
    drag constant. This is the V0 / drag degeneracy the finding names, now
    measured. V2 constrains the product, not either factor.
- **The shipped Gurney V0 is lower than every caption** (§5: caption/Gurney =
    1.10 / 1.07 / 1.03). The matching per-caliber scales, 0.91 / 0.93 / 0.97,
    each fall inside the PASS band and near the RMS minimum. The script only
    tests a *common* scale, so the pooled RMS for this per-caliber mix is not
    computed. The per-caliber positions still suggest the model's own V0 would
    corroborate *better* than the caption, not worse.
- **So** "V2 PASS" is a statement about caption V0 plus the shipped drag
    constant. It is fragile upward and robust downward. It is corroboration
    only (§1) and no shipped constant depends on it.

## 4. What the free fits say about the caption values (script §C)

The script fits ln v = ln V0 − c·x (constant C_D) to each shell's source series,
leaving V0 free.

- **Perforation (1/8 in) series.** The fitted V0 lands within −4 % / +1.3 % of
    the caption for all three shells, and the pooled scale is *s* = 0.975. The
    fitted *c* ≈ 2.8–3.1 is close to the shipped 2.67. The same table that
    carries the caption is therefore **internally consistent with it**: this is
    data-implied corroboration of the stated V0 at about the 5 % level. It is
    not proof, because the V0/c degeneracy still allows a trade.
- **Casualties series, full range.** This fit gives *s* ≈ 0.68 with *c* ≈ 1.6.
    That is an artefact of the fit form, not evidence against the caption. The
    series runs to x ≈ 1.0–1.26, into the subsonic tail where real C_D falls.
    A constant-C_D line is then forced to flatten (*c* too small) and pays for
    it with a low intercept. Restricted to M > 0.7, the same series gives
    *s* = 0.86 / 0.98 / 0.98 with *c* ≈ 2.5–2.8, which is consistent with the
    perforation fits.
- **Net.** Wherever the constant-C_D form is valid, the data support the caption
    V0 to within about 2–14 % (low side). No fit asks for a V0 *higher* than
    the caption by more than 1.3 %.

## 5. Shipped R50 and lethal area vs the Gurney initial velocity (script §D)

`V0_FTS` never reaches shipped outputs (§1). The shipped input with the same
role is the Gurney velocity. The script scales it by *s* and re-computes
R50_cross and lethal area per caliber.

- **Elasticities** are below 1 for R50 (0.76–0.85) and about 1 for lethal area
    (0.95–1.19). A ±10 % change in V0 moves R50 by about ±8 % and lethal area
    by about ±10–12 %. The larger calibers are a little more sensitive.
- **The observed caption-vs-Gurney gap.** The 1944 captions exceed the shipped
    Gurney V0 by 10.0 / 7.3 / 3.1 % (75 / 105 / 155 mm). Suppose the captions
    were right and Gurney low. Shipped R50 would then be low by 7.3 / 5.5 /
    2.6 %, and lethal area low by 9.3 / 7.4 / 3.7 %. The shipped outputs are
    therefore biased **conservative**, not optimistic.
- **Orderings.** Nominal R50 is 11.8 / 15.5 / 17.9 m. Neighbouring calibers are
    separated by 15–30 %, and the per-caliber shifts above differ by at most
    about 5 points, so the caliber ordering cannot flip. The comparative claims
    (posture crossover, "airburst narrows but never reverses the prone
    advantage") compare configurations that share one V0. To first order a
    common V0 scale moves both sides of each comparison together. **Not
    tested:** the script does not re-run the posture comparisons under scaled
    V0, so this is an argument, not a computation.

## Verdict

**Within threshold — log as limitation.**

**Threshold.** The test is whether a plausible V0 error changes a shipped claim
or moves an absolute headline output (R50, lethal area) by **more than
±20 %**. The shipped claims are comparative orderings, which fail only on a
sign or ordering change. The absolute R50 and lethal-area figures are shown as
engineering magnitudes. This thread already validates against the source with
a factor-of-2 band, and the Mott / drag limitations already carry errors of
tens of percent. A ±20 % bar is therefore tighter than anything the model
claims, but loose enough that an error below it would not change what the demo
shows.

**Where the results fall:**

- The plausible V0 error has two measures. The caption-vs-Gurney gap is 3–10 %,
    and the data-implied scatter (§4) is about 2–14 %. Over that range the
    shipped outputs move by at most about 8 % (R50) and about 12 % (lethal
    area). Both are within ±20 %. The direction is conservative, and no
    ordering flips.
- `V0_FTS` itself has zero reach into shipped outputs (§1).
- The V0 caption has provenance: a per-shell stated caption (§2). What is
    unstated is its measurement accuracy.

**Remaining caveat for the limitation entry.** The V2 corroboration PASS is
one-sided: it fails if V0 is more than about 1 % higher than the caption.
Treat V2 as corroborating the V0·drag product, not the drag constant alone.
No sourcing or model change is needed before Phase 2a.
