# Scoping — 75 mm M48 HE case-mass basis (`mass_deductions` placeholder)

**Aspect:** the mass bookkeeping of the single registry entry `"75mm M48 HE"`
in `src/arty/shells.py` — the three fields (`mass_total`, `mass_filler`,
`mass_deductions`) whose difference is `M_case`, the mass that feeds
`gurney_velocity` (via C/M) and `mott_params` (`N₀ = M_case / 2μ`).
**Workflow B, scoping pass only.** 105 mm M1 and 155 mm M107 are out of scope.

## 1. The defect, restated from the source

`src/arty/shells.py` (75 mm entry) ships:

```python
mass_total=6.622,        # 14.6 lb complete with M48 PD fuze
mass_filler=0.6668,      # 1.47 lb cast TNT
mass_deductions=0.200,   # M48 PD fuze placeholder (TM 43-0001-28)
```

⇒ `M_case = 5755.2 g`.

Tolch (1938), BRL Report 126 — the *only* fragmentation data this shell is
validated against — prints its own weight row for the tested rounds
(`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`,
greppable anchor `Wt. empty shell & fuze`):

| quantity | lb | kg |
| --- | --- | --- |
| Wt. loaded unfuzed shell | 12.50 | 5.6699 |
| Fuze (M39 P.D.) | 2.35 | 1.0659 |
| Wt. of TNT charge (ave.) | 1.56 | 0.7076 |
| Wt. empty shell & fuze | 13.29 (printed) | 6.0283 |

**Closure invariant (source's own definitions):** `12.50 − 1.56 + 2.35 = 13.29`
— reproduces the printed row exactly (`assert` in the check script, §4). The
table is therefore admissible.

Case metal alone (no TNT, no fuze) = `12.50 − 1.56 = 10.94 lb = 4962.3 g`.
The shipped `M_case = 5755.2 g` is **1.160× = 16 % high**.

Two independent facts make `0.200 kg` indefensible on its own terms:

1. It is self-declared a placeholder in the comment.
1. 0.200 kg = 0.44 lb is lighter than any WW2-era US PD fuze. The two in-repo
    sourced points bracket it far above: TM 9-1901 gives fuze M48/M54 =
    1.41–1.42 lb = 0.640 kg (cited in this same file's 105 mm comment), and
    Tolch's M39 P.D. = 2.35 lb = 1.066 kg.

## 2. Why the fix is not "swap one number"

The three mass fields must share **one basis**. `mass_total = 14.6 lb` is
attributed to TM 43-0001-28 — **which is not processed in `doc-reference/`**
(only a web link in `doc-reference/ww2-shells/index.md:388`). So on the shipped
entry, *all three* mass fields rest on an unprocessed source, and the one
number the physics actually consumes (`M_case`) is a residual of three
unverifiable inputs. Dropping Tolch's 2.35 lb fuze into a TM-basis `mass_total`
would mix bases (Tolch's round is the T3/M39 combination; 14.6 lb is a
production-M48/M48-fuze figure) and is not admissible either.

The physics-correct target is not the fuze weight — it is `M_case`, which Tolch
states **directly** as a difference of two printed, closure-checked numbers.

## 3. Candidate bases and their consequences

Computed by
`experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/tolch-75mm-mass-basis-variants.py`
against the live `arty` code, so `V₀`, `μ`
and `N₀` are the model's own, not hand-arithmetic:

| variant | ded [g] | M_case [g] | vs Tolch | V₀ [m/s] | μ [g] | N₀ |
| --- | --- | --- | --- | --- | --- | --- |
| **A** shipped (placeholder 0.200) | 200.0 | 5755.2 | 1.160× | 807.5 | 0.793 | 3627 |
| **B** TM 9-1901 M48 fuze only (1.41 lb) | 639.6 | 5315.6 | 1.071× | 838.3 | 0.736 | 3611 |
| **C** full Tolch rebaseline (all 3 fields) | 1065.9 | 4962.3 | 1.000× | 890.2 | 0.653 | 3801 |
| **D** residual ded., TM total/filler kept | 992.9 | 4962.3 | 1.000× | 865.8 | 0.690 | 3596 |

Variant C sets `mass_total = 14.85 lb = 6.7358 kg` (loaded unfuzed + fuze),
`mass_filler = 1.56 lb = 0.7076 kg`, `mass_deductions = 2.35 lb = 1.0659 kg`.

**Two non-obvious results, both worth carrying into the derivation pass:**

- **`N₀` is nearly invariant** (3596–3801, ≤ 5 % spread) across a 16 % case-mass
    error. `μ ∝ V₀⁻³` and `V₀` rises as `M_case` falls, so the two effects in
    `N₀ = M_case/2μ` very nearly cancel. The fix is therefore **not** a
    fragment-count correction — anyone expecting the count-gap ratios to move is
    going to be surprised. What it *does* move materially is **`V₀` (+10 %, 807.5
    → 890 m/s) and `μ` (−18 %, 0.793 → 0.653 g)**, i.e. per-fragment energy
    (`∝ V₀²`, +21 %) and the whole mass spectrum — which is what the lethality
    chain actually integrates.
- **Independent `V₀` check:** Tolch's own inferred charge-component fragment
    velocities are penetrating 3030 f/s = **923.5 m/s** (clean at four anchors)
    and perforating ~2750 f/s = 838 m/s (third digit unreadable per the card —
    do not treat as exact). Variant C's 890 m/s sits *between* them; the shipped
    807.5 m/s sits *below both*. This is corroborating, not decisive (Gurney
    `V₀` is an initial radial speed, Tolch's are inferred from side-spray angle
    change), and must be stated as such in `derivation.md`.

## 4. Recommendation

**Adopt variant C**: rebaseline all three mass fields of `"75mm M48 HE"` onto
Tolch's weight row, with the closure `12.50 − 1.56 + 2.35 = 13.29` cited in the
code comment and the greppable anchor `Wt. empty shell & fuze` named.

Rationale, in priority order:

1. It is the only basis in which `M_case` — the quantity the physics consumes —
    is *stated by an in-repo, closure-checked source* rather than inferred as a
    residual of unprocessed numbers.
1. It makes the shell's mass basis and its *only* validation dataset the same
    rounds, which is a precondition for every Tolch-vs-model ratio in
    `challenges/count-gap-1938/` meaning anything.
1. It moves `V₀` toward, not away from, the source's own fragment-velocity
    figures.

**Rejected:** B (still 7 % high; mixes a TM-9-1901 fuze onto an unprocessed
TM-43-0001-28 total, and adds no booster the M48 round does need). D (right
`M_case`, but `mass_deductions` becomes an uninterpretable residual carrying the
TM/Tolch discrepancy — the same opacity that produced the present defect).

**Trade-off to declare explicitly in `derivation.md`:** variant C describes the
1938 T3 test article, not the fielded production M48. That is the right choice
*for this model* because the entry exists to be checked against Tolch, but the
entry's docstring/comment must say so, and `_limitations.qmd` should carry one
line to that effect.

## 5. Validation checks the derivation pass must run

1. Weight-row closure re-asserted from the source values (already in the check
    script; keep the `assert`).
1. `M_case` after the edit equals 4962.3 g to < 1 g.
1. Mott mass closure `∫ m(−dN/dm)dm = 2N₀μ = M_case` still holds (the
    `mott-fragment-shape-closure` update's identity — its 5755.20 g figure
    becomes 4962.3 g).
1. `μ = 0.653 g` against Tolch's own recovered fragment-size floor (the
    `mott-fragment-shape-closure/rebaseline-verdict.md:149` row quotes a
    0.95–3.5 g comparison band). **Flag:** this moves the model *further below*
    that floor, 0.793 → 0.653 g. That is an expected, physically consistent
    consequence of a smaller case at higher `V₀` — it is not a new defect
    introduced here, but the derivation must say it out loud rather than let a
    reviewer find it.
1. No other shell entry's numbers change (`mott_params` is per-shell; run the
    existing test suite).

## 6. Artifacts whose cited figures go stale (annotate in a *later* pass — do not edit here)

Every path below cites at least one of `M_case = 5755(.2) g`, `V₀ = 807.5 m/s`,
`μ = 0.793 g`, `N₀ = 3627` for this shell:

| path | what goes stale |
| --- | --- |
| `experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md:66,67,87,115` | row "5755 g vs Tolch's 6030 g" (wrong on *both* sides — 6028 g is shell **+ fuze**); `V₀ 807.5 vs 838.2`; `μ/2μ/N₀` line |
| `experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md:8,39-42,56-58,66-67` | the "sound" rulings on the `M_case` and `V₀` rows; the 100.2 %-of-case statement |
| `experiment/fragmentation-field/challenges/source-data-audit/review-void-rulings.md:114,135,141,165-177` | already diagnoses this; its FINDING marker closes when the fix lands |
| `experiment/fragmentation-field/challenges/source-data-audit/checks/tolch-case-mass-basis.py:38-39` | hard-coded `M_CASE_MODEL = 5755.2`, `MU_G, N0_MODEL = 0.793, 3627.0` |
| `experiment/fragmentation-field/challenges/source-data-audit/checks/tolch-count-basis-closure.py:100-102` | `5755 g body` in two derived figures |
| `experiment/fragmentation-field/challenges/source-data-audit/stale-surfaces.md:67,105,123` | the register row for this defect; the `N₀ = 3627` "unaffected" claim |
| `experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md:149,171,184,200,234` | `V₀ = 807.5`, mass-closure 5755.20 g, `μ 0.235 → 0.793`, `N₀ 12256 → 3627` table rows |
| `experiment/fragmentation-field/updates/mott-fragment-shape-closure/review.md:57`, `scoping.md:69`, `rebaseline-verdict.md:149` | same figures quoted |
| `experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/tolch-count-post-shape-closure.py:48` | sweep pins `V0 in (807.5, 838.2, 951.0)` |
| `experiment/fragmentation-field/challenges/mott-scale-gap/_scale_verdict_ledger.md:42` | `μ = 0.235 g, N₀ = 12256, V₀ = 807.5` (already historical) |
| `experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md:134` | `807.5` (model) vs 2750 f/s comparison |
| `experiment/fragmentation-field/_limitations.qmd:134` | `N₀ = 3627` for 75 mm M48 |

Superseding notes, not rewrites — the count-gap-1938 rebaseline is separately
tracked work per the dispatch constraint.

## 7. Librarian

**Not needed.** Every number the recommendation uses is already processed
in-repo (Tolch weight row; TM 9-1901 fuze weights for the rejected variant B).
@librarian would only be required if the project instead chooses to keep the
production-M48 basis, in which case **TM 43-0001-28** (Army Ammunition Data
Sheets, 75 mm HE M48 data sheet) must be collected and processed — it is
currently cited by `src/arty/shells.py` but exists nowhere in `doc-reference/`.

## 8. Adjacent, explicitly out of scope

`wall_t = 0.006 m` on the same entry is commented "estimate; caliber-scaled
from M1 (needs confirmation)". It drives `μ` through `t_bu` and is a second
unsourced input on this shell — a separate aspect, separate pass. Not touched
here, and the derivation pass must not silently fold it in.

## 9. Fidelity target

Drives the 75 mm M48 fragment initial-velocity and mass-spectrum inputs, hence
every Tolch-comparison ratio in `challenges/count-gap-1938/` and the shell's
P(kill) figures. Tolerable error: **±3 % on `M_case`** (it is a directly stated
source difference — there is no reason to accept more) and **±10 % on `V₀`**,
which is the spread between Tolch's own two inferred fragment-velocity figures.
