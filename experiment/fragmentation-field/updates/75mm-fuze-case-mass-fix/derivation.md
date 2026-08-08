# Derivation — 75 mm M48 HE mass basis (`mass_total`, `mass_filler`, `mass_deductions`)

**Aspect:** the three mass fields of `SHELLS["75mm M48 HE"]` in
`src/arty/shells.py`, whose difference `M_case = mass_total − mass_filler −
mass_deductions` is the only mass the physics consumes (`gurney_velocity` via
`C/M`, `mott_params` via `N₀ = M_case/2μ`). Derivation pass; no `src/` edit
here. `wall_t` untouched (scoping §8).

Numbers below are produced by
`experiment/fragmentation-field/updates/75mm-fuze-case-mass-fix/checks/tolch-75mm-mass-basis-variants.py`
against the live `arty` code — no hand arithmetic.

## 1. Decision: adopt the **production basis (variant E)**, not scoping's variant C

Scoping recommended variant C (rebaseline all three fields onto Tolch 1938's
weight row for the 1938 T3 / M39-fuze test article). **This pass departs from
that recommendation.** Two source facts that post-date the scoping pass remove
its two load-bearing premises:

| scoping premise | status now |
| --- | --- |
| §2: "*all three* mass fields rest on an unprocessed source (TM 43-0001-28)" | **False.** `doc-reference/ww2-shells/tm-9-1904-fuze-fitting/card.md` §"75-mm Gun Shell M48 (H.E.)" states "Mean weight of loaded and fuzed projectile: 14.6 pounds" (source.pdf p.414, grep `Fuzes M48, M48A1 and M54`). `mass_total = 6.622 kg` is now sourced in-repo. `mass_filler = 1.47 lb` is confirmed as the official M48 gun filler. |
| §4 rationale 1: "C is the only basis in which `M_case` is stated by an in-repo closure-checked source" | **False.** Under E, `mass_deductions` is built entirely from in-repo closure-checked numbers: TM-9-1901 M48 fuze 1.41 lb (§319.b, grep `weight, 1.41 pounds`) + the M21A2 booster increment 0.74 lb, which closes on **two independent pairs** in the same table (2.15−1.41 = 2.16−1.42 = 0.74; TM-9-1901 card §"Closure Invariant"). |

Variant E therefore is:

| field | value | source |
| --- | --- | --- |
| `mass_total` | 14.6 lb = **6.6225 kg** (shipped 6.622, unchanged) | TM-9-1904, mean weight of loaded and fuzed projectile |
| `mass_filler` | 1.47 lb = **0.6668 kg** (shipped, unchanged) | official M48 gun filler; TM-9-1904's rounder "1.49 pounds of TNT" bursting-charge figure not used |
| `mass_deductions` | 1.41 + 0.74 = 2.15 lb = **0.97522 kg** | TM-9-1901 M48 fuze (1.41 lb) + M20/M20A1 booster stood in by the closure-checked M21A2 increment (0.74 lb) |

⇒ **`M_case = 4980.4 g`** (was 5755.2 g, −13.5 %).

The M20/M20A1-booster-analog step is not new physics judgement: it is the
**same stand-in method already exercised and accepted** for the 105 mm M1 (same
M20/M20A1 booster) and 155 mm M107 entries in this file — i.e. the *method* was
swept and judged immaterial (MOOT verdict, ≤0.2 % on `N₀`) in
`experiment/fragmentation-field/challenges/fuze-mass-deductions-range/materiality.md`;
those two entries do **not** themselves ship the 0.975 kg value (they retain
their own unsourced placeholders, 0.75 and 1.5 kg).
Adopting E makes the 75 mm entry consistent with the registry's other two
WW2 US HE entries instead of the sole entry describing a 1938 test article.

### Why this is *better* than C, not merely equal

Under C, `M_case` agrees with Tolch **by construction** — the cross-check
scoping §5.2 asks for is a tautology and carries zero information. Under E,
`M_case` is assembled from three numbers Tolch never saw, so the comparison
below is a genuine independent corroboration of both sources.

## 2. Cross-check against Tolch's case-metal-alone figure (required)

Tolch (1938), BRL 126,
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`,
anchor `Wt. empty shell & fuze`. Closure invariant re-asserted in the check
script: `12.50 − 1.56 + 2.35 = 13.29` lb, exact.

Case metal alone (no TNT, no fuze) = `12.50 − 1.56` = **10.94 lb = 4962.3 g**.

Production basis, same quantity = `14.6 − 1.47 − 2.15` = **10.98 lb = 4980.4 g**.

> **Agreement: +0.37 % (18 g).** Two disjoint source chains — a 1938 BRL test
> report weighing T3 rounds with M39 fuzes, and two 1940s ordnance TMs
> describing the fielded round with M48-family fuzes — land on the same case
> metal to well inside the ±3 % fidelity bar. This is **corroborating, not
> decisive** — the same standing as the velocity check in §5.4, and for the
> admissibility reason given in §2a — but it is evidence that both are read
> correctly, and it is *only* obtainable under a non-Tolch basis.

The shipped value 5755.2 g is 1.160× the Tolch figure; both injected blocking
findings state this correctly and are confirmed here.

## 2a. Limitation on §2's admissibility (from `review.md`, Deferrable)

The weight row above is read off
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`
— a surface that source's own `card.md` (line 22) states **is not a citable
surface for any number** absent a `tables/*.csv` + `.invariant` extraction, and
no such extraction exists for this table (only the four pages-40–44
spray-density tables were re-extracted and closure-checked). The internal
closure `12.50 − 1.56 + 2.35 = 13.29` (exact, plus three further per-round rows
consistent to ±0.03 lb) is real protection against a silent digit swap, but it
is not the CSV-based admissibility gate `.claude/rules/source-data-fidelity.md`
requires.

**Bound on the exposure:** this changes no `src/` value. `mass_total`,
`mass_filler` and `mass_deductions` under variant E are sourced entirely from
TM-9-1904/TM-9-1901, independent of Tolch; the Tolch figures feed only §2's
corroborating cross-check, which §2 now labels accordingly. Pending either a
`tables/weight-row.csv` + `.invariant` extraction of the 4-round weight table,
or a @librarian ruling that card.md line 22's ban was scoped only to the
pages-40–44 spray tables (in which case the citation stands as-is and the
finding closes).

## 3. Test-article vs production trade-off (scoping §"Trade-off to declare explicitly")

Scoping framed the trade-off as *model the rounds Tolch actually fired, or
model the fielded shell*. On the evidence above the trade-off is **empirically
negligible on `M_case`** (0.37 %) and confined to one field:

| quantity | Tolch T3 rounds | production M48 | Δ | consequence |
| --- | --- | --- | --- | --- |
| case metal | 10.94 lb | 10.98 lb | +0.4 % | none — inside every bar |
| TNT charge | 1.56 lb (ave. of test rounds) | 1.47 lb (official) | −5.8 % | `C/M` 0.1426 → 0.1339 ⇒ `V₀` 890.2 → 864.3 m/s (−2.9 %) |
| fuze | M39 P.D., 2.35 lb | M48/M48A1/M54 + M20/M20A1, 2.15 lb | −8.5 % | absorbed in `mass_deductions`; does not fragment in the model either way |

**Declared:** the entry models the **fielded production Shell M48**. Against
Tolch's fragmentation data it therefore under-states the burst charge by ~6 %
(Tolch's rounds averaged a heavier fill than the official 1.47 lb), which
propagates as a ~3 % low `V₀` in every Tolch comparison. That is one third of
the ±10 % `V₀` bar (scoping §9) and is the *only* residual of the
test-article-vs-production choice. It must be stated in the code comment and
carried as one line in `_limitations.qmd`.

The reverse trade-off under C would have been an entry whose `mass_total`,
`mass_filler` and fuze all describe a round the US Army never fielded, used
for every non-Tolch output (P(kill), R50) the model produces.

## 4. Variant table (live `arty` code)

| variant | ded [g] | M_case [g] | vs Tolch case metal | V₀ [m/s] | μ [g] | N₀ |
| --- | --- | --- | --- | --- | --- | --- |
| A shipped (placeholder 0.200) | 200.0 | 5755.2 | 1.160× | 807.5 | 0.793 | 3627 |
| B TM-9-1901 M48 fuze only (1.41 lb) | 639.6 | 5315.6 | 1.071× | 838.3 | 0.736 | 3611 |
| C full Tolch rebaseline (scoping's pick) | 1065.9 | 4962.3 | 1.000× | 890.2 | 0.653 | 3801 |
| D residual ded., TM total/filler kept | 992.9 | 4962.3 | 1.000× | 865.8 | 0.690 | 3596 |
| **E production basis (adopted)** | **975.2** | **4980.4** | **1.004×** | **864.3** | **0.692** | **3597** |

E and D are numerically near-identical (`M_case` differs by 18 g), but D's
`mass_deductions` is an uninterpretable residual — the same opacity that
produced the present defect — whereas E's is 1.41 lb fuze + 0.74 lb booster,
each traceable and each independently closure-checked. E ≠ D in provenance,
which is the whole point of this pass.

## 5. Validation checks (scoping §5), all run

1. **Weight-row closure** `12.50 − 1.56 + 2.35 = 13.29` — `assert`, PASS.
   Added: the M21A2 booster increment closes at 0.74 lb on both TM-9-1901
   pairs — `assert`, PASS.
1. **`M_case`** = 4980.4 g. (Scoping wrote this check as "= 4962.3 g to < 1 g"
   under variant C; under E the meaningful form is the cross-basis agreement,
   +0.37 %, PASS against the ±3 % bar.)
1. **Mott mass closure** `∫₀^∞ N(m) dm = 2N₀μ = M_case`: numerically
   4980.46 g vs `M_case` 4980.44 g, +0.000 % — PASS. (Grid truncated at
   `m = 400μ`; the analytic tail `2N₀μ(x₀+1)e^{−x₀}`, `x₀ = 20`, is 4×10⁻⁸ of
   the total, so the residual is quadrature error only. The
   `mott-fragment-shape-closure` update's 5755.20 g figure becomes 4980.4 g.)
1. **`μ` vs Tolch's recovered-fragment floor.** μ moves 0.793 → 0.692 g, i.e.
   *further below* the 0.95–3.5 g comparison band quoted at
   `mott-fragment-shape-closure/rebaseline-verdict.md:149`. Stated out loud, as
   scoping instructed: this is the expected consequence of a smaller case at
   higher `V₀` (`μ ∝ V₀⁻³`), not a new defect. E is 6 % *less* extreme than C
   (0.692 vs 0.653 g) on this axis.
1. **`V₀` against Tolch's own inferred fragment velocities.** 864.3 m/s sits
   inside Tolch's band — perforating ~2750 f/s ≈ 838 m/s (third digit
   unreadable per the card; not exact) to penetrating 3030 f/s = 923.5 m/s.
   The shipped 807.5 m/s sits below both. Corroborating only, **not decisive**:
   Gurney `V₀` is an initial radial speed, Tolch's are inferred from side-spray
   angle change — different quantities that need not coincide.
1. **No other shell entry changes** — `mott_params` is per-shell and only the
   75 mm entry's fields move. Baseline recorded here for the `src/` pass to
   compare against: `uv run pytest -q --ignore=tests/test_pdf_processor.py` →
   **210 passed, 1 skipped**. (`tests/test_pdf_processor.py` fails at
   *collection* on `AttributeError: module 'pdf_processor' has no attribute
   '_try_get_google_client'` — pre-existing and unrelated to this aspect.)

## 5a. Provenance caveat on the TM-9-1904 anchor (for @model-reviewer)

The anchor `Fuzes M48, M48A1 and M54` resolves **only in
`doc-reference/ww2-shells/tm-9-1904-fuze-fitting/card.md`** — the in-repo
extraction `fuze-fitting-extraction.md` contains the 105 mm and 155 mm
sections but **not** the 75 mm one, so no in-repo *text* surface carries the
"14.6 pounds" figure. The card cites `source.pdf` p.414 (retained, gitignored);
that PDF page is the only surface behind it.

This is stated, not waved through, because it is the sole source for
`mass_total`. Two things bound the exposure: (a) `mass_total` is **unchanged**
by this pass — the card *confirms* a value that was already shipped from
TM 43-0001-28, it does not introduce a new one; (b) the +0.37 % agreement in
§2 is a numerical check on that same figure from a wholly independent source,
which a mis-read 14.6 would be very unlikely to pass. If @model-reviewer wants
the text surface closed, the fix is a librarian pass extracting TM-9-1904
p.414 into `fuze-fitting-extraction.md` — not a change to any number here.

## 6. Assumptions logged (not defects, not to be re-derived)

- **M20/M20A1 booster weight is not tabulated anywhere in-repo.** The M21A2
  increment (0.74 lb) stands in. Same open gap already recorded for the 105 mm
  M1 entry (the deferrable marker in `materiality.md`); the 75 mm entry
  inherits it, and its N₀ sensitivity across the whole fuze-only ↔
  fuze+booster bracket is <0.2 % per that document. No new finding needed —
  the existing marker's `affects:` already lists `src/arty/shells.py`.
- **The gilding-metal rotating band is not deducted**, on either basis. Tolch's
  12.50 lb loaded-unfuzed and TM-9-1904's 14.6 lb both include it, so both
  `M_case` figures carry it and the +0.37 % agreement is like-for-like. A
  nominal 75 mm band ≈ 0.20 lb = 91 g = **1.8 % of `M_case`** — i.e. the model
  treats ~1.8 % non-fragmenting copper as fragmenting steel. This is smaller
  than the ±3 % bar, and deducting it on one basis only would *break* the
  cross-check. Deliberately not corrected here. (The 155 mm entry does deduct
  band+plug; the 105 mm and 75 mm entries do not — a registry inconsistency
  worth one line, not a defect of this aspect.)

  FINDING[note]: rotating-band treatment is inconsistent across the registry — 155mm M107 deducts band+plug in mass_deductions, 105mm M1 and 75mm M48 do not, so those two carry ~1.8% non-fragmenting gilding metal inside M_case (affects: src/arty/shells.py; since: 2026-08-08)
- **The steel base cover** (spot-welded, TM-9-1904) is steel and left inside
  `M_case`; it fragments.
- **`N₀` is nearly invariant** across every variant (3596–3801, ≤5 % spread)
  despite a 16 % case-mass change, because `μ ∝ V₀⁻³` and `V₀` rises as
  `M_case` falls, so the two effects in `N₀ = M_case/2μ` nearly cancel. This
  fix is **not** a fragment-count correction. What it moves is `V₀` (+7 %,
  807.5 → 864.3) and `μ` (−13 %, 0.793 → 0.692) — per-fragment energy `∝ V₀²`
  is +15 % — which is what the lethality chain integrates.

## 7. What the `src/` pass must write

```python
mass_total=6.622,     # 14.6 lb mean loaded+fuzed projectile (TM-9-1904 p.414,
                      #   "Fuzes M48, M48A1 and M54")
mass_filler=0.6668,   # 1.47 lb cast TNT (official M48 filler; TM-9-1904 quotes
                      #   a rounder 1.49 lb bursting charge — not used)
# mass_deductions: fuze+booster.  Authorized (TM-9-1904 p.414): Fuzes M48,
# M48A1, M54; Boosters M20, M20A1.  TM-9-1901 sources fuze-only 1.41 lb
# (M48/M48A1/M48A2, sec.319.b); M20/M20A1 booster weight is NOT tabulated, so
# the closure-checked M21A2 increment 0.74 lb stands in (2.15-1.41 =
# 2.16-1.42), same stand-in as the 105 mm M1 entry above.  1.41+0.74 = 2.15 lb.
# => M_case = 4980.4 g, +0.37 % vs Tolch 1938's independently-stated case metal
# 12.50-1.56 = 10.94 lb = 4962.3 g (tolch-1938.md, "Wt. empty shell & fuze").
# NOTE: entry models the FIELDED production round; Tolch's 1938 T3 test rounds
# averaged 1.56 lb TNT, so Tolch comparisons run ~3 % low on V0.
mass_deductions=0.97522,
```

And one line in `experiment/fragmentation-field/_limitations.qmd` (which also
needs its `N₀ = 3627` figure for this shell updated to 3597):

> The 75 mm M48 entry models the **fielded production round** (TM-9-1904
> 14.6 lb, official 1.47 lb TNT, M48-family fuze + M20/M20A1 booster). Tolch
> (1938) — the only fragmentation dataset this shell is validated against —
> fired 1938 T3 articles with M39 fuzes and an average 1.56 lb TNT fill, ~6 %
> heavier. Case metal agrees between the two to 0.4 %, but Gurney `V₀` in
> Tolch comparisons runs ~3 % low for this reason.

Both injected blocking markers close when that edit lands — the
first directly, the second because `M_case` 4980.4 g vs Tolch's case metal
4962.3 g replaces the mis-based "5755 g vs 6030 g" comparison (6028 g is
Tolch's empty shell **and** fuze, as the finding states).

## 7a. Zone-level effect (present pass)

The four-zone breakdown rendered in `_four-zone-3d.qmd` §6.4 moves as
`checks/zone-effect-75mm-mass-basis.py` reports: every zone mass −13.5 %,
every zone $V_0^z$ ×1.070 (base plate ×1.072, its $k^b$ reduction being
multiplicative), and the zone mass **fractions** exactly unchanged
(0.420 / 0.360 / 0.170 / 0.050) because this Tier-2 shell splits by fixed
fractions, not drawing geometry. Spray angles are geometric and unmoved.
(Note the script reports `M_case` = 4980.0 g against §4's 4980.4 g: the
shipped `mass_total` is the rounded 6.622 kg, not 6.6225 kg — 0.4 g, i.e.
0.008 %.)

## 8. Fidelity target (carried from scoping §9)

Drives the 75 mm M48 fragment initial-velocity and mass-spectrum inputs, hence
every Tolch-comparison ratio in `challenges/count-gap-1938/` and the shell's
P(kill) figures. Tolerable: **±3 % on `M_case`** (achieved: 0.37 % against an
independent source) and **±10 % on `V₀`** (residual test-article-vs-production
exposure: ~3 %).
