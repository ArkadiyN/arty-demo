# Scoping — shell case-mass basis (`src/arty/shells.py`)

Workflow B, scoping pass. Aspect: the mass basis from which `src/arty/`
derives **case metal mass** `M_case`, i.e. the `mass_total / mass_filler /
mass_deductions` triple in the `SHELLS` registry and the single subtraction
that consumes it.

## 1. Problem statement

`src/arty/fragmentation.py:299`:

```python
mass_shell = shell.mass_total - shell.mass_filler - shell.mass_deductions
```

`mass_shell` is the **only** case-metal number in the model. It feeds:

- Gurney: `V0 = sqrt(2E)/sqrt(M/C + 0.5)` (`fragmentation.py:310`) — enters as
  the ratio `M_case/M_filler`, so an error is partly damped (V0 ∝ ~M^-1/2).
- Mott: `N0 = mass_shell / (2 mu)` (`fragmentation.py:337`) — **linear**, so a
  16% error in `M_case` is a ~16% error in every fragment count, and `mu`
  itself depends on `V0` (`mu ∝ V0^-...`), so the two effects do not cancel.

Every lethal-count, hit-density, and P(kill) field in the notebook is
downstream of `N0`.

For the **75mm M48** row the deduction is a self-declared placeholder
(`shells.py:60`, `mass_deductions=0.200, # M48 PD fuze placeholder`), and the
open blocking finding (`collect-findings.py --for src/arty/shells.py`) shows it
is wrong by a factor ~5 against the source's own fuze weight. Two of the other
three rows are likewise unsourced ("estimate", or no comment at all). The
defect is settled evidence; this pass scopes the fix, it does not re-litigate.

## 2. Source table — Tolch 1938's own weight breakdown

`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`,
grep anchor `"Pit Fragmentation Tests of 75 mm T3 Shell from 75 mm"` (the table
caption; the data row follows immediately). Report title, grep
`"FRAGMENTATION EFFECTS OF THE 75MMH. E. SHELL T3 (M48)"` — **the source
itself equates T3 with M48**, so shell identity for this registry row is not in
question.

Four rounds, weights in lb:

| Row (source wording) | Rd 1 | Rd 2 | Rd 3 | Rd 4 |
|---|---|---|---|---|
| Wt. loaded unfuzed shell | 12.50 | 12.50 | 12.47 | 12.53 |
| Fuze (M39 P.D.) Wt., lbs. | 2.35 | 2.35 | 2.35 | 2.36 |
| Wt. of TNT charge (ave.), lbs. | 1.56 | 1.56 | 1.56 | 1.56 |
| Wt. empty shell & fuze, lbs. | 13.29 | 13.29 | 13.26 | 13.33 |

(OCR renders some digits as `^`/`I.56`/`1.5b`/`2.10^`; the closure below is
what pins them.)

**Closure invariant** (source's own definitions, must hold every column):
`loaded_unfuzed − TNT + fuze = empty shell & fuze`.
Rd 1/2: 12.50 − 1.56 + 2.35 = 13.29 ✔; Rd 3: 12.47 − 1.56 + 2.35 = 13.26 ✔;
Rd 4: 12.53 − 1.56 + 2.36 = 13.33 ✔. Table closes on all four rounds; the
disputed OCR glyphs are recovered by the closure, not by eyeballing. This is
the check to re-run mechanically in the derivation pass (see §6).

Derived quantities (Rd 1/2, the modal round; 1 lb = 0.45359237 kg):

| Quantity | lb | kg | Definition |
|---|---|---|---|
| Loaded, fuzed, complete | 14.85 | 6.7359 | 12.50 + 2.35 |
| TNT filler | 1.56 | 0.70760 | source row |
| Fuze M39 P.D. | 2.35 | 1.06594 | source row |
| **Case metal (body, no fuze, no filler)** | **10.94** | **4.9623** | 12.50 − 1.56 |
| Empty shell **and fuze** | 13.29 | 6.0282 | source row |

**Do not read 13.29 lb / 6028 g as case metal.** It is the fuzed empty
projectile, and it is the basis Tolch's own recovery percentages are quoted
against — see §5.

Shipped model today: 6.622 − 0.6668 − 0.200 = **5.755 kg**, i.e. **+16.0%**
against the source's 4.962 kg. Note the shipped `mass_total` (14.6 lb) and
`mass_filler` (1.47 lb) also disagree with Tolch (14.85 lb, 1.56 lb) — the row
is currently a **mixture of a TM-era catalog weight and a placeholder**, not
any one source's coherent breakdown. That mixture, not just the placeholder
line, is the defect to fix.

## 3. What `mass_deductions` is supposed to mean

Declared in `fragmentation.py:138` as `# fuze + rotating band [kg]` — i.e.
*projectile mass that is not case steel driven by the filler*. Two candidate
readings are in play across the registry and they give different numbers:

- **(a) non-fragmenting inert mass** — fuze + band + base plug.
- **(b) non-case mass for Gurney/Mott purposes** — everything not a
  filler-sleeved steel wall, regardless of whether it happens to break up.

Tolch settles that (a) and (b) differ for the fuze: fuze pieces **do**
fragment and are recovered (grep `"These fragments are mostly pieces of fuze."`
— screen-1 fragments, ~15% of recovered weight). But the fuze sits ahead of
the explosive column, is not Gurney-accelerated by it, and is not a Mott
case-wall break-up population. **Recommendation: `mass_deductions` means (b)**
and the docstring should say so explicitly, because that is what `M_case` is
used for (Gurney C/M, Mott `mu`, `N0`). This is a semantics decision the
derivation pass must record, not just a number change.

## 4. Options for the fix

**Option A — patch the 75mm deduction only.** Set
`mass_deductions = 1.06594` (2.35 lb M39 fuze), leave `mass_total = 6.622` and
`mass_filler = 0.6668`. → `M_case` = 4.889 kg, within 1.5% of source. Cheapest,
but keeps a three-way source mixture (TM total, TM filler, Tolch fuze) whose
internal closure is accidental. **Not recommended.**

**Option B — rebase the whole 75mm row on Tolch's own breakdown (recommended).**
`mass_total = 6.7359` (14.85 lb), `mass_filler = 0.70760` (1.56 lb),
`mass_deductions = 1.06594` (2.35 lb) → `M_case = 4.9623 kg` **exactly** the
source's 10.94 lb, by construction, and C/M is the source's own too. One
source, one closure, auditable in a single line. Cost: `mass_total` and
`mass_filler` change too, so V0 shifts (C/M rises from 0.1159 → 0.1426, +23%),
which moves more than `N0` alone. This is correct, not a side-effect: the
current C/M was built on a filler weight the tested rounds did not have.

**Option C — add an explicit `mass_case` field to `ShellParams`,** primary
where a source states case metal directly, with the subtraction as fallback.
Schema change, touches `fragmentation.py`. Attractive long-term (it makes the
provenance of the *used* number visible rather than emergent from three others)
but it is a second aspect; **defer**, and record the triple's closure in a
comment instead. Revisit if a second shell turns up with a directly-stated case
weight.

## 5. Audit of the other registry rows (this is not a 75mm-only fix)

| Shell | `mass_deductions` (kg) | Stated basis | Verdict |
|---|---|---|---|
| 105mm M1 HE | 0.75 | none — no comment at all | **unsourced**; needs a weight-breakdown source or an explicit assumption |
| 155mm M107 HE | 1.5 | `# ... (estimate)` | **self-declared estimate**; same |
| 75mm M48 HE | 0.200 | `# ... placeholder` | **wrong** — Tolch says 1.066 (§2) |
| 60mm M49A2 HE | 0.131542 | 0.29 lb fuze, Ammunition Series 6 Table 6-1 | **sourced and coherent** — the pattern to match |

The M49A2 row is the template: a named source table, the deduction identified
as a specific component, and the tail-fin assembly explicitly excluded with a
stated reason. The derivation pass should bring M1 and M107 to that standard
or, failing an available source, replace the bare number with a documented
scaling assumption plus a `_limitations.qmd` entry.

**105mm M1 — partial source already in the repo.**
`doc-reference/ww2-shells/ordnance-105mm-m1-1940/tables/bill-of-material.csv`
(Description of Manufacture, 30 Aug 1940) itemises, per shell:
`Band, Rotating` gilding metal 0.653 lb (0.2962 kg) and `Cover, Base` steel
WD 1010 0.0852 lb (0.0386 kg). **Read the caveat before using these:** the same
column gives `Body, Shell` as 53.9 lb against a 33 lb finished projectile, so
`lbs_per_shell` is *raw stock issued*, not finished-component mass — machining
loss is inside it. The band and base-cover figures are therefore **upper
bounds** on the finished parts, not the parts. Even so they bracket the
non-steel deduction at ≤0.33 kg, which means the shipped 0.75 kg is mostly an
implicit fuze allowance (~0.45 kg / 1.0 lb) that no source in `doc-reference/`
currently states. The fuze is not part of shell manufacture and is **not** in
this document — that is the gap.

**155mm M107** has no analogous document in `doc-reference/ww2-shells/`.

If the M1/M107 fuze weights are not found, that is a @librarian request
(see Missing References), not a guess.

Sizing the exposure: M1 `M_case` = 14.97 − 2.18 − 0.75 = 12.04 kg; a 0.5 kg
error in the deduction is ~4% on `N0`. M107: 43.09 − 6.863 − 1.5 = 34.73 kg;
1 kg error ≈ 3%. Both are an order less severe than the 75mm's 16%, so the
75mm is the blocking item and the other two are correctness-of-provenance work
that can ride in the same pass.

## 6. Validation checks the derivation pass must run

1. **Closure of the source table** (§2), all four rounds, as a retained script
   under `updates/shell-case-mass-basis/checks/`. Prefer extracting the four
   rounds to `doc-reference/.../tables/round-weights.csv` + `.invariant` once,
   per the source-data-fidelity rule, rather than hand-typing the series a
   fourth time (three artifacts already quote it).
1. **Registry self-consistency**: for every shell,
   `0 < mass_total − mass_filler − mass_deductions` and the resulting `M_case`
   within a stated tolerance of any directly-sourced case weight.
1. **Unit check**: `M_case/M_filler` dimensionless; 75mm C/M = 0.1426 lands in
   the normal HE-shell band (0.10–0.20).
1. **Limit check**: `N0` and `V0` before/after, printed for all four shells, so
   the 16% count shift is visible and attributable.
1. **Literature agreement**: 75mm `N0` against Tolch's pit-test recovery — but
   read §7 first, the comparison is not apples-to-apples.

## 7. Downstream dependency — count-gap-1938 needs a corresponding correction

Not fixed in this update; flagged here as required follow-on work (the second
open blocking finding covers it).

`experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md`
and `count-chain.md` compare model `M_case` = 5755 g against "Tolch's 6030 g".
6028 g is **empty shell *and fuze*** (§2), not case metal. Correcting the
reference to 4962 g flips the sign of the discrepancy: the model was 16% **high**,
not 4.5% low, and every ratio in that thread inherits it.

There is a real subtlety that thread must resolve rather than just swapping the
number: Tolch's own count statistics are referenced to the *fuzed* empty weight.
Grep `"60# of the weight of the empty shell and fuze is determined"` (the 60%
test definition) and `"accounting for 95.c% of the weight of metal"` (779
fragments per shell in the pit tests). So the experimentally fragmenting metal
**includes** the fuze body, ~15% of recovered weight on screen 1. A Mott `N0`
built on 4962 g of case wall is therefore not expected to reproduce Tolch's raw
total count; the honest comparison is either model-`N0` vs. Tolch-count-minus-
fuze-pieces, or a stated ~10–15% fuze allowance. **That reconciliation is the
count-gap-1938 thread's job, in a separate pass, after this update lands.**

Other surfaces that display or restate these masses and will need re-checking
once the registry changes (grep `mass_deductions`):
`experiment/fragmentation-field/_four-zone-3d.qmd` (reads the registry — safe,
it will follow automatically),
`challenges/drag-gap-1944/initial-conditions-75mm.md` (and the 105/155 siblings),
`challenges/source-data-audit/stale-surfaces.md`.

**`_parameters.qmd` is a separate, pre-existing defect, found during this pass
and not covered by `stale-surfaces.md`.** Lines 22-25 build a `ShellParams`
from *literal* values rather than importing `SHELLS["105mm M1 HE"]`, and the
copy has already drifted: `wall_t=0.011` there vs `0.009208` in the registry.
It hardcodes `mass_deductions=0.75`, so it will silently keep the old number
after this update. Fix is to import the registry entry — presentation-layer
work, not physics, and not part of this update.

**Closed 2026-08-10.** `_parameters.qmd` now imports `mass_total`,
`mass_filler`, `mass_deductions`, `caliber`, `filler` and `steel` from
`arty.shells.SHELLS["105mm M1 HE"]`, so those fields can no longer drift from
the registry. `wall_t=0.011` remains a deliberate override (documented
in-place) for the historical TM 9-1901 cylindrical wall the single-cylinder
model uses, distinct from the drawing-derived registry geometry the
four-zone section uses — this was never drift, only under-documented.

## 8. Assumptions to log (not to derive)

- **Rotating band stays inside `M_case`.** Tolch's 10.94 lb is
  loaded-unfuzed minus TNT, which still contains the copper band and any base
  plug. A 75mm band is O(50–70 g), ≤1.4% of `M_case` — below the fidelity bar
  below, so it is an assumption entry, not a correction. Same logic applies to
  the M1/M107 rows whichever source grounds them.
- **Round 1/2 weights are used as the nominal**, not the 4-round mean; the
  spread is 0.5% and the model is not lot-specific.
- **M39 P.D. vs. M48 P.D. fuze.** Tolch's rounds carried the M39; the registry
  comment names an M48 fuze. If the row is rebased on Tolch (Option B) the
  whole row is M39-consistent and the comment must be corrected. Do not mix.

## 9. Fidelity target

This aspect drives `N0`, hence every lethal-fragment count, hit-density field
and P(kill) contour in the notebook — linearly. Tolerable error on `M_case`:
**±5%**, which is well inside what a sourced weight breakdown gives (±0.5%) and
well outside the current 16%. Anything that only moves `M_case` by <5% (the
rotating band, lot-to-lot spread, round-1-vs-mean) is an assumption entry, not
a derivation.

## Missing references

None blocking for the 75mm — Tolch 1938 is in `doc-reference/` and carries the
breakdown, so the derivation pass can proceed now on the blocking finding.

**@librarian is needed for the 105mm/155mm rows** (§5), and only for these:

1. **Fuze weights** for the fuzes actually fitted to 105mm M1 HE and 155mm
   M107 HE (PD M48/M51 family, and whatever the M107's 1943 spec names). None
   of the four `doc-reference/ww2-shells/` documents covers fuzes — a fuze is
   not part of shell manufacture, so the manufacture documents structurally
   cannot supply it. TM 9-1901 / TM 43-0001-28 style ammunition-data tables are
   the natural target.
1. **Finished** (not raw-stock) rotating-band and base-cover weights for
   105mm M1, to replace the upper bounds in §5; and the 155mm M107 equivalents.

This is a scoping-pass judgement, not a hard stop: the derivation pass should
fix the 75mm row against Tolch (Option B) and, if the librarian request has not
returned, close M1/M107 with an explicit bounded assumption plus a
`_limitations.qmd` entry rather than blocking on it. Their exposure is ~3-4%
on `N0` (§5), inside the ±5% bar in §9 — a logged assumption is a valid
closure there.
