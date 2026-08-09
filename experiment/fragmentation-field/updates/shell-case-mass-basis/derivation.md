# Derivation — shell case-mass basis (`src/arty/shells.py`)

Workflow B, derivation pass. Implements the option chosen in `scoping.md` §4:
**Option B — rebase the whole 75mm M48 row on Tolch 1938's own weight
breakdown**, plus a documented closure for the unsourced 105mm/155mm
deductions. No `src/arty/` edits here; that is the next pass.

Checks live in `checks/` and are cited inline. Both are runnable standalone
from the repo root.

## 1. The quantity being derived

`fragmentation.py:299` computes the model's only case-metal number:

$$M_\text{case} \;=\; m_\text{total} - m_\text{filler} - m_\text{ded}
\quad (1)$$

| symbol | meaning | unit |
|---|---|---|
| $m_\text{total}$ | complete projectile as weighed, fuze fitted | kg |
| $m_\text{filler}$ | explosive charge $C$ | kg |
| $m_\text{ded}$ | inert, non-Gurney-driven mass (see §3) | kg |
| $M_\text{case}$ | steel wall accelerated by the filler | kg |

Eq. (1) is a *bookkeeping identity*, not physics: it asserts only that the
three registry numbers come from one coherent weight breakdown. The physics
claim is what $M_\text{case}$ then means — §3.

## 2. Source closure — Tolch 1938 per-round weights

Extracted once (per `.claude/rules/source-data-fidelity.md`) to
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/round-weights.csv`,
with the closure in the sibling `.invariant`. Anchors:
`Pack Howitzer Complete Rounds, Shell Lot 276I-3` and
`Wt. loaded unfuzed shell` (`tolch-1938.md:230-232`).

**Closure invariant**, from the source's own row labels, on every round:

$$W_\text{loaded,unfuzed} - W_\text{TNT} + W_\text{fuze}
  \;=\; W_\text{empty\&fuze} \quad (2)$$

`uv run src/utils/check-table-invariants.py doc-reference/.../round-weights.invariant`
→ **4 rows, 1 check, ok**. Eq. (2) is non-vacuous: all four columns are
separately typeset, and the fourth is a cross-row identity, not a printed
subtotal. It is what recovers the damaged glyphs — the OCR at
`tolch-1938.md:232` gives round 3's loaded weight as `12.^7`, the TNT row as
`I.56 I.56 1.5b I.56`, and the round-4 column header as `^`. No other
single-digit reading of those glyphs satisfies (2) on all four rounds.

Independent cross-check: the neighbouring `pit-screen-recovery.invariant`
divides its `pct_empty` column by 13.29 lb, stated there as the mean of this
table's `empty_and_fuze_lb`. mean(13.29, 13.29, 13.26, 13.33) = 13.2925 →
13.29. Two transcriptions, made in different passes, agree.

**Case metal is derived, not transcribed** (`checks/tolch-round-weight-closure.py`):

$$M_\text{case} = W_\text{loaded,unfuzed} - W_\text{TNT} \quad (3)$$

| rd | loaded lb | TNT lb | fuze lb | case lb | case kg | fuzed lb | C/M |
|---|---|---|---|---|---|---|---|
| 1 | 12.50 | 1.56 | 2.35 | 10.94 | 4.9623 | 14.85 | 0.1426 |
| 2 | 12.50 | 1.56 | 2.35 | 10.94 | 4.9623 | 14.85 | 0.1426 |
| 3 | 12.47 | 1.56 | 2.35 | 10.91 | 4.9487 | 14.82 | 0.1430 |
| 4 | 12.53 | 1.56 | 2.36 | 10.97 | 4.9759 | 14.89 | 0.1422 |

Lot spread on $M_\text{case}$: **0.55%** — an order below the ±5% fidelity bar
(`scoping.md` §9), so round 1/2 (the modal round) is the nominal, per
`scoping.md` §8. **`W_\text{empty\&fuze}` = 13.29 lb = 6.0282 kg is 21.5% above
case metal and must never be read as $M_\text{case}$** — it is the fuzed empty
projectile, and it is the divisor of Tolch's own recovery percentages.

**Robustness of $M_\text{case}$ to the disputed fuze glyph.** Eq. (3) does not
contain $W_\text{fuze}$. Even if 2.35 lb were misread, $M_\text{case}$, $C$ and
therefore $C/M$ are unaffected — the fuze enters Option B's $m_\text{total}$
and $m_\text{ded}$ *equally* and cancels in eq. (1). The fuze reading is load-
bearing only for the redundant closure (2), which is exactly why (2) can
validate it.

## 3. Semantics of `mass_deductions` — the decision to record

`scoping.md` §3 posed reading (a) *non-fragmenting inert mass* vs (b)
*non-case mass for Gurney/Mott purposes*, and recommended (b). **Adopted, on
the following physical grounds, and the docstring at `fragmentation.py:138`
must be changed to say so.**

$M_\text{case}$ is consumed at exactly two places, and both make (b) the only
consistent reading:

- **Gurney** (`fragmentation.py:310`): $V_0 = \sqrt{2E}\,/\sqrt{M/C + 1/2}$.
  The $M$ in the Gurney cylinder is the mass the detonation products do $pdV$
  work against — a mass *radially* enclosing the charge. A nose fuze sits
  **ahead of** the explosive column, is not radially confined by it, and is
  not part of the accelerated annulus.
- **Mott** (`fragmentation.py:315-337`): $N_0 = M_\text{case}/2\mu$ counts
  break-up of a *plastically expanding cylindrical wall* at fracture spacing
  $x_0$. The fuze body is neither a wall nor at $r_\text{bu}$.

Tolch shows this is a real distinction rather than a definitional one: fuze
pieces **do** fragment and are recovered (`tolch-1938.md`, anchor
`These fragments are mostly pieces of fuze.` — ~15% of screen-1 recovered
weight). So reading (a) and reading (b) genuinely differ for the fuze, and
$M_\text{case}$ under (b) is *not* the total fragmenting metal. Consequence,
which `count-gap-1938` must carry (`scoping.md` §7): the model's $N_0$ is not
expected to reproduce Tolch's raw recovered count.

## 4. The 75mm M48 rebase (Option B)

Round 1/2 nominal, 1 lb = 0.45359237 kg exactly:

| field | shipped | Option B | source |
|---|---|---|---|
| `mass_total` | 6.622 | **6.7359** | 12.50 + 2.35 = 14.85 lb |
| `mass_filler` | 0.6668 | **0.70760** | 1.56 lb, TNT row |
| `mass_deductions` | 0.200 (placeholder) | **1.06594** | 2.35 lb, M39 P.D. fuze |
| ⇒ $M_\text{case}$ | 5.7552 | **4.9623** | 10.94 lb, eq. (3) — exact |

*(src/ pass note: the `mass_total` cell rounds to 6.7359 but
14.85 × 0.45359237 = 6.735847, and at 4 d.p. the triple closes 0.1 g off
Tolch's 10.94 lb. The registry therefore carries all three fields at 6 d.p. —
6.735847 / 0.707604 / 1.065942 — which closes to 4.962301 kg against
4.9623005 kg. Values, not basis, differ from the table above.)*

`checks/registry-case-mass-consistency.py` confirms the rebase reproduces
Tolch's case metal to `+0.0000 %` (exact by construction) against `+16.0 %`
shipped. **All three fields move together**: the shipped row mixed a TM-era
catalog total (14.6 lb) and filler (1.47 lb) with a placeholder fuze, so its
internal closure was accidental. Under Option B the row is one source, one
lot, one closure.

`mass_deductions` comment must be corrected to **M39 P.D.**, not M48 PD
(`scoping.md` §8): the tested rounds carried the M39, and the row is now
M39-consistent throughout. Do not mix.

## 5. Sensitivity — the scoping pass's propagation claim is wrong, in a way that matters

`scoping.md` §1 states that "a 16% error in `M_case` is a ~16% error in every
fragment count", $N_0$ being linear in $M_\text{case}$. **That is incorrect**,
because $\mu$ is not independent of $M_\text{case}$. Chaining the shipped code:

$$x_0 \propto V_0^{-1},\qquad
\alpha = A\,\kappa_x^2\,t_\text{bu}/x_0 \propto V_0,\qquad
\gamma = \alpha^{-2/3}\gamma' \propto V_0^{-2/3}$$
$$\mu \propto (\sigma_f/\gamma)^{3/2} V_0^{-3}
      \propto \gamma^{-3/2} V_0^{-3}
      \propto V_0^{\,1} V_0^{-3} = V_0^{-2} \quad (4)$$

so with the Mott shape closure in place $\mu \propto V_0^{-2}$, **not**
$V_0^{-3}$. (Numerically confirmed: $V_0$ +10.2% → $\mu$ −17.7%, and
$1.102^{-2} = 0.823$.) Then with $V_0^2 \propto (M/C + 1/2)^{-1}$,

$$N_0 = \frac{M_\text{case}}{2\mu} \;\propto\; M_\text{case} V_0^2
      \;\propto\; \frac{C\,M_\text{case}}{M_\text{case} + C/2} \quad (5)$$

giving the logarithmic sensitivities

$$\frac{\partial \ln N_0}{\partial \ln M_\text{case}}
 = \frac{C/2}{M_\text{case}+C/2} = \frac{C/M}{2 + C/M},
\qquad
\frac{\partial \ln N_0}{\partial \ln C} = \frac{2}{2 + C/M} \quad (6)$$

At the 75mm's $C/M = 0.1426$: **0.067 in $M_\text{case}$, 0.933 in $C$.**

Eq. (6) is not an approximation to the shipped chain — it *is* the shipped
chain. `checks/registry-case-mass-consistency.py` compares it against a
central finite difference in $m_\text{ded}$ (which perturbs $M_\text{case}$ at
fixed $C$, exactly the error mode of interest) and they agree to 4 d.p. on
every row:

| shell | $C/M$ | eq. (6) analytic | finite difference | $\partial\ln N_0/\partial\ln C$ |
|---|---|---|---|---|
| 105mm M1 | 0.1811 | 0.0830 | 0.0830 | 0.9170 |
| 155mm M107 | 0.1976 | 0.0899 | 0.0899 | 0.9101 |
| 75mm M48 shipped | 0.1159 | 0.0548 | 0.0548 | 0.9452 |
| 60mm M49A2 | 0.2036 | 0.0924 | 0.0924 | 0.9076 |
| 75mm M48 Option B | 0.1426 | 0.0666 | 0.0666 | 0.9334 |

**$N_0$ is set by the filler mass, essentially not by the case mass.** The
Gurney feedback cancels the linear $M_\text{case}$ term to within 7%. This is
why the rebase moves $N_0$ by only +4.8% despite a −13.8% move in
$M_\text{case}$: −13.8% × 0.067 = −0.9%, +6.1% in $C$ × 0.933 = +5.7%.

Before/after, all four shells, from `checks/registry-case-mass-consistency.py`:

| shell | $M_\text{case}$ kg | C/M | $V_0$ m/s | $\mu$ mg | $N_0$ |
|---|---|---|---|---|---|
| 105mm M1 | 12.0400 | 0.1811 | 994.2 | 1538.33 | 3913.3 |
| 155mm M107 | 34.7270 | 0.1976 | 1034.8 | 4737.73 | 3664.9 |
| 60mm M49A2 | 0.7575 | 0.2036 | 1048.9 | 438.71 | 863.3 |
| 75mm M48 **shipped** | 5.7552 | 0.1159 | 807.5 | 793.29 | 3627.4 |
| 75mm M48 **Option B** | **4.9623** | **0.1426** | **890.2** | **652.70** | **3801.4** |
| Δ | −13.8% | +23.1% | +10.2% | −17.7% | **+4.8%** |

The $V_0$ change (+10.2%, 807 → 890 m/s) is the *larger* physical consequence
of this update and moves 890 m/s into much better company for a 75mm HE shell
than 807 m/s was. It is a correction, not a side effect: the shipped $V_0$ was
computed from a filler weight the tested rounds did not carry.

**Consequence for the two unsourced rows** — this is what closes them, §6.

## 6. 105mm M1 and 155mm M107 — bounded-assumption closure

@librarian's fuze-weight request had not returned when this pass ran
(`doc-reference/ww2-shells/` unchanged). Per `scoping.md`'s instruction, these
close on a documented assumption rather than blocking.

Eq. (6) makes the bound much tighter than `scoping.md` §5 estimated (it used
the linear-in-$M_\text{case}$ assumption now shown wrong). With
$\partial\ln N_0/\partial\ln M_\text{case}$ = **0.0830** (M1) and **0.0899**
(M107) — verified numerically in §5 — and $m_\text{ded}$ entering $N_0$ *only*
through $M_\text{case}$:

$$\left|\frac{\Delta N_0}{N_0}\right|
 = \frac{C/M}{2+C/M}\cdot\frac{|\Delta m_\text{ded}|}{M_\text{case}} \quad (7)$$

| shell | $m_\text{ded}$ | plausible $|\Delta m_\text{ded}|$ | $\Delta M_\text{case}$ | ⇒ $\Delta N_0$ |
|---|---|---|---|---|
| 105mm M1 | 0.75 kg | 0.5 kg | 4.2% | **0.35%** |
| 155mm M107 | 1.5 kg | 1.0 kg | 2.9% | **0.26%** |

Both are ~15× inside the ±5% bar of `scoping.md` §9 — and inside it on
$M_\text{case}$ itself (4.2% and 2.9%). **Logged assumption, not a derivation**:

> **A1.** 105mm M1 `mass_deductions = 0.75 kg` and 155mm M107
> `mass_deductions = 1.5 kg` are unsourced allowances for fuze + rotating band
> (+ base plug on the M107). The only partial evidence in `doc-reference/` is
> `ww2-shells/ordnance-105mm-m1-1940/tables/bill-of-material.csv`, whose
> `Band, Rotating` 0.653 lb and `Cover, Base` 0.0852 lb are **raw stock
> issued**, not finished-part mass (the same column gives `Body, Shell` as
> 53.9 lb against a 33 lb finished projectile), hence upper bounds only:
> non-fuze deduction ≤ 0.33 kg, leaving ~0.45 kg implied fuze. No source in
> the repo states a fuze weight for either round. Retained pending the
> librarian request; exposure bounded at <0.4% on $N_0$ by eq. (7).

`_limitations.qmd` entry to add in the notebook pass:

> **105mm and 155mm inert-mass deductions are unsourced.** The fuze and
> rotating-band allowances subtracted from those two projectiles' total mass
> (0.75 kg and 1.5 kg) are engineering estimates, not read from a weight
> table; no fuze-weight source for these rounds is currently in
> `doc-reference/`. Because fragment count depends on case mass only weakly
> (∂ln N₀/∂ln M_case ≈ 0.07, the Gurney velocity feedback cancelling most of
> the linear term), a ±0.5 kg / ±1.0 kg error moves fragment counts by under
> 0.4%. The 75mm M48 row, by contrast, is grounded on Tolch (1938)'s own
> per-round weight table.

## 7. Validation checks — results

Against `scoping.md` §6:

1. **Source-table closure**, four rounds — **PASS**, §2.
   `checks/tolch-round-weight-closure.py` + the `.invariant`.
1. **Registry self-consistency** — **PASS** on (a) $M_\text{case} > 0$ and
   (b) deductions < case for all four shells; **FAIL** on (d) 75mm vs Tolch
   (+16.0%) as shipped, **PASS** exactly under Option B. Check (d) is the
   regression guard for the src/ pass.
1. **Unit check** — $C/M$ is kg/kg, dimensionless. 75mm Option B $C/M$ =
   **0.1426**, inside the 0.10–0.20 band for a WW2 thick-walled HE shell and
   now bracketed by its own family (60mm 0.204, 105mm 0.181, 155mm 0.198 —
   the shipped 0.1159 was the outlier). And $\mu$ closes to a mass:
   $\sqrt{2/\rho}\,(\sigma_f/\gamma)^{3/2}(r_\text{bu}/V_0)^3$ has units
   $(\mathrm{m^3\,kg^{-1}})^{1/2}\cdot(\mathrm{kg\,m^{-1}s^{-2}})^{3/2}
   \cdot\mathrm{s^3}
   = \mathrm{kg^{-1/2+3/2}\,m^{3/2-3/2}\,s^{-3+3}} = \mathrm{kg}$ ✔
   ($\gamma$ dimensionless), so $N_0 = M_\text{case}/2\mu$ is dimensionless ✔.
1. **Limit check** — table in §5, all four shells. $C \to 0 \Rightarrow$ eq.
   (5) gives $N_0 \to 0$ (no drive, no break-up) ✔;
   $M_\text{case}\to\infty$ at fixed $C$ gives $N_0 \to C$·const, finite ✔ —
   an infinitely heavy case does not make infinitely many fragments, which is
   the correct behaviour and the reason for §5's result.
1. **Literature agreement vs Tolch's pit count** — **not closed here, by
   design.** Tolch recovers 779 fragments/round accounting for 95.6% of the
   *fuzed* empty weight, so his population includes fuze pieces that
   $M_\text{case}$ under reading (b) excludes (§3). Model $N_0$ = 3801 against
   a fuze-inclusive 779-fragment recovery is not an apples-to-apples pair, and
   the reconciliation is `count-gap-1938`'s job in a later pass
   (`scoping.md` §7). Note the direction now flips there: the reference is
   4962 g, not 6030 g.

## 8. Assumptions logged (not derived)

- **A1** — 105mm/155mm deductions, §6.
- **A2 — the rotating band stays inside $M_\text{case}$.** Eq. (3) is
  loaded-unfuzed minus TNT, which still contains the copper band and any base
  plug. A 75mm band is O(50–70 g), ≤1.4% of $M_\text{case}$, and by eq. (6)
  ≤0.1% on $N_0$. Below the bar. Same for the M1/M107 rows.
- **A3 — round 1/2 as nominal**, not the 4-round mean; spread 0.55% (§2).
- **A4 — M39 P.D., not M48 PD.** Registry comment corrected in the src/ pass.
- **A5 — Tolch's lot is representative of the M48.** His complete fuzed round
  is 14.85 lb against the TM-era catalog 14.6 lb (−1.7%), most plausibly a
  different fuze model. We take the *measured lot* over the catalog because
  Option B's whole point is one coherent breakdown; the 1.7% is inside the bar
  either way.
- **A6 — `source.pdf` is not retained** in this document's directory (nor in
  the sibling tables' — a pre-existing repo-wide condition, not introduced
  here), so page-level re-verification of §2 is currently against
  `tolch-1938.md` only. The closure (2) and the independent agreement with
  `pit-screen-recovery.invariant` are what stand in for it.
- **Option C deferred** (`scoping.md` §4): no explicit `mass_case` field on
  `ShellParams`. Revisit if a second shell turns up with a directly-stated
  case weight; for now the triple's closure is recorded as a comment.

## 9. Handoff to the src/ pass

Single-row edit in `src/arty/shells.py` (`75mm M48 HE`): the three mass fields
in §4, the corrected fuze designation, and a comment citing
`round-weights.csv` + this file. Docstring change at `fragmentation.py:138`
per §3. Then re-run
`checks/registry-case-mass-consistency.py` — check (d) must go green with zero
failures. Nothing else in `src/arty/` changes.

Downstream re-checks the src/ pass must *not* silently absorb (`scoping.md`
§7): `count-gap-1938/rebaseline-verdict.md` and `count-chain.md` (both carry
open blocking findings), `challenges/drag-gap-1944/initial-conditions-75mm.md`,
`challenges/source-data-audit/stale-surfaces.md`, and `_parameters.qmd`
(open deferrable finding — it inlines a literal `ShellParams` and will not
follow the registry).
