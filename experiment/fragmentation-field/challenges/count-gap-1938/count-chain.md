# The count chain vs. Tolch's absolute perforating count — scoping

**Status: Scoped, paused; re-baselined 2026-08-08.** §1 exonerates the Mott
$(\mu, N_0)$ *parameter* stage — no material or geometric input can carry a
4–6× multiplier — and localizes the residual to the fitted perforation
threshold (C1) and, secondarily, the break-up-velocity treatment (C2). §2's
inference that the residual is confined to that threshold ("not the
population") does **not** survive: a threshold-free test still finds the
model over-counting 2.15–2.70× on the Tolch-metal basis, so a genuine
fragment-*spectrum* term (~1.2–2.7×) shares the residual alongside the
threshold-fit artefact (~2.1×) — see the restated Fact 2 below and
[`rebaseline-verdict.md`](rebaseline-verdict.md) for the full re-baseline
(all pit-count-denominated numbers here move from a published 803 to the
corrected 779). Closing C1 needs an independent perforation model (§5) — out
of scope for now; a perforation model is future work, not this pass's.
Nothing in `src/arty/` changes as a result of this thread yet.

FINDING\[blocking\]: this document's §1–§4 quantitative content (post-fix model $\mu=0.793$ g, $N_0=3627$, $V_0=807.5$ m/s, and every $m_{thr}$/$N$/ratio figure derived from them) was closure-checked against shipped `fragmentation.py` before commit 6c1faff (2026-08-08), which re-anchored $\gamma'$ 65→54.5 and fixed an ogive/cylinder $V_0$ contradiction. Re-running the retained script against current shipped code gives $\mu=0.826$ g, $N_0=3016$, $V_0=864.4$ m/s (Gurney) — none of which match. `rebaseline-verdict.md`'s own closure line ("reproduces §2's stated values exactly") is stale by the same commit. This thread was not in that commit's file list and needs a fresh @modeler pass to re-close §1's sensitivity table and §2–§4's decomposition against current shipped output (affects: experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md, experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md, experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-decomposition.py; since: 2026-08-08)

**Question.** `_limitations.qmd` L1 records that Tolch (1938)'s absolute
perforating-fragment count is still over-predicted by ~4–6× after both the Mott
shape-closure fix (`../mott-scale-gap/` → `updates/mott-fragment-shape-closure/`)
and the DoD-1975 drag anchor (`updates/mach-dependent-fragment-drag/`). L1 names
three candidate loci for the residual and rules out two of them for this thread:
drag (exhausted — the constant sits within ~10 % of the geometric ceiling) and
spray/belt geometry (a different aspect). This thread takes the third:
**what in the chain Gurney $V_0$ → Mott $(\mu, N_0)$ → perforation decision can
produce a systematic multiplicative over-count?**

**Why this is a legitimately separate thread from `../drag-gap-1944/`.** That
thread's observable is $B(r)$, a *density* reduced over azimuth; this one's is a
$4\pi$ *total count* — Tolch's ~700 perforations is itself an extrapolation from
panel densities to the whole shell (Summary item 6), so the comparison is
total-against-total and carries no azimuthal weighting. Any spray-belt or
solid-angle-partition error cancels on both sides. That is what makes the count
chain separable from geometry, and it is the premise of this thread.

______________________________________________________________________

## 1. The chain, and its algebraic sensitivities

Implementation: `arty.fragmentation.gurney_velocity`, `mott_params`, `mott_N`,
`min_lethal_mass` (`src/arty/fragmentation.py:281–393`).

$$V_0 = \frac{\sqrt{2E}}{\sqrt{M_\text{case}/C + 1/2}} \quad (1)$$

$$x_0 = \sqrt{\frac{2\sigma_f}{\rho\,\gamma'}}\;\frac{r_{bu}}{V_0},
\qquad \alpha = A\,\kappa_x^2\,\frac{t_{bu}}{x_0},
\qquad \gamma = \alpha^{-2/3}\gamma' \quad (2)$$

$$\mu = \sqrt{\tfrac{2}{\rho}}\left(\frac{\sigma_f}{\gamma}\right)^{3/2}
\left(\frac{r_{bu}}{V_0}\right)^{3},
\qquad N_0 = \frac{M_\text{case}}{2\mu} \quad (3)$$

$$N(\ge m) = N_0\,e^{-\sqrt{m/\mu}},
\qquad m_{thr}(s):\; \tfrac12 m\left(V_0 e^{-\lambda(m)s}\right)^2 = E_{thr}
\quad (4)$$

Substituting (2) into (3) collapses the shape-closed Mott stage to a form whose
sensitivities are readable by inspection — and which the notebook does not state:

$$\boxed{\;\mu \;=\; \frac{A\,\kappa_x^{2}\;t_{bu}\,r_{bu}^{2}\;\sigma_f}
{\gamma'\;V_0^{2}}\;}\quad (5)
\qquad\Longrightarrow\qquad
N_0 = \frac{M_\text{case}\,\gamma'\,V_0^{2}}
{2\,A\,\kappa_x^{2}\,t_{bu}\,r_{bu}^{2}\,\sigma_f}$$

Units: m·m²·Pa/(m²s⁻²) = kg ✓. Note $\rho_\text{steel}$ **cancels** — it enters
only via $x_0$ and is removed again by the shape closure; consistent with the
known result that only the ratio $\sigma_f/\gamma'$ is identifiable.

| Link | Parameter        | $N_0 \propto$             | Factor needed for 4–6×                | Admissible?                                                                |
| :--- | :--------------- | :------------------------ | :------------------------------------ | :------------------------------------------------------------------------- |
| (1)  | $V_0$            | $V_0^{2}$                 | $V_0$ high by 2.0–2.4×                | **No** — model 807.5 vs Tolch's measured 838.2 m/s (item 10)               |
| (3)  | $M_\text{case}$  | $M_\text{case}$           | case mass high by 4–6×                | **No** — 5755 g vs Tolch's 6030 g                                          |
| (5)  | $\sigma_f$       | $\sigma_f^{-1}$           | $\sigma_f \approx 130$–200 MPa        | **No** — Mott's own worked example is 772 MPa                              |
| (5)  | $\gamma'$        | $\gamma'$                 | $\gamma' \approx 260$–390             | **No** — Mott's table spans 42–67                                          |
| (5)  | $A,\kappa_x$     | $A\kappa_x^{2}$           | prism 4–6× more slender               | **No** — fixed by `updates/mott-fragment-shape-closure/derivation.md` §2–4 |
| (5)  | $t_{bu}, r_{bu}$ | $(t_{bu}r_{bu}^2)^{-1}$   | break-up radius/thinning wrong 2–2.5× | Bounded — see C2                                                           |
| (4)  | $E_{thr}$        | — (enters $N$, not $N_0$) | **unbounded**                         | fitted, not sourced                                                        |

**The Mott parameter stage cannot carry a 4–6× multiplier.** This is the same
closure argument the `../mott-scale-gap/` thread ran pre-fix, re-run against the
post-fix algebra (5): every material and geometric input would have to leave its
literature bracket by 4–6×. So if the residual is in the count chain at all, it
is in $V_0$ (bounded, below) or in the **decision stage** (4).

______________________________________________________________________

## 2. Where the residual actually sits — measured

75 mm M48 HE, DoD anchor $C_D C_\text{shape} = 2.674$, 15 ft panel station.
Script: [`checks/count-chain-decomposition.py`](checks/count-chain-decomposition.py).

Post-fix model: $\mu = 0.793$ g, $2\mu = 1.59$ g, $N_0 = 3627$.

| $E_{thr}$ [J] | source of the value                                                                               | $m_{thr}$(15 ft) [g] | $N(\ge m_{thr})$ | as % of $N_0$ | vs Tolch 700 |
| ------------: | :------------------------------------------------------------------------------------------------ | -------------------: | ---------------: | ------------: | -----------: |
|           1.9 | fitted to the 0.557 A→D falloff ratio                                                             |                0.022 |             3067 |          85 % |     **4.4×** |
|           3.6 | fitted (upper $V_0$ case)                                                                         |                0.035 |             2939 |          81 % |     **4.2×** |
|          78.6 | 1944 Ordnance Dept. card's own casualty threshold, 58 ft-lb (`../drag-gap-1944/b-vs-range.md` §2) |                0.403 |             1779 |          49 % |     **2.5×** |
|           126 | Tolch's own smallest-hole bound, $m\ge0.36$ g at 838 m/s                                          |                0.605 |             1515 |          42 % |     **2.2×** |
|         294.5 | pre-anchor fitted $E_{thr}$                                                                       |                1.281 |             1018 |          28 % |     **1.5×** |

**The 78.6 J row is an independent cross-check, not a fit.** It is lifted
verbatim from a second, unrelated 1944 historical source (the Ordnance Dept.
card's own stated casualty energy, already used as-is in `../drag-gap-1944/`
for the Family B comparison) — it is not tuned to Tolch's falloff shape and
not derived from Tolch's hole-size data the way the 126 J row is. At this
threshold $N/700 = 2.5\times$ and $N/779 = 2.3\times$ (**779, not 803** — the
re-baselined pit-recovered count, `rebaseline-verdict.md`; every $N/803$
figure below is corrected the same way, ×1.031), landing in the same band as
Tolch's own hole-size-bound row (2.2×) and well inside the fitted-threshold
band (4.2–4.4×) that L1 originally reported. Two independently-sourced
thresholds — one from Tolch's own recovered-fragment data, one from an
unrelated 1944 ordnance card — now agree with each other on the residual
(2.2–2.5×) far more closely than either agrees with the fitted values. That is
added corroboration for the §2 decomposition below, not a new number that
shifts it: it does not reach the table's own PASS band (within 2×) on its
own, but it confirms the ~2–2.5× band is not an artifact of which independent
threshold is chosen.

Two facts follow, and they reframe L1:

1. **$N_0$ is not 4–6× too high.** $N_0 = 3627$ sits *between* Tolch's two own
    totals: ~5000 fragments issuing from the shell (panel extrapolation, item 6)
    and **779** recovered in the pit at 95.6 % of the metal (items 1, 8) —
    re-baselined from a published 803 (`rebaseline-verdict.md`; the re-baselined
    `tables/pit-screen-recovery.csv` closes on 779 and only on 779). Those two
    Tolch numbers are mutually consistent — the 4221 non-recovered events carry
    the missing 4.4 % of mass at ~0.0625 g each — and the model's total lies
    inside them. **The gross fragment count is not the defect.**
1. **The residual is predominantly (not entirely) in the perforating
    *fraction*.** The model declares 81–85 % of $N_0$ able to perforate 1″
    spruce at 15 ft; Tolch measures 700/5000 = **14 %**. That single ratio,
    ~6×, *is* the L1 residual, and is produced by the fitted $E_{thr}$ =
    1.9–3.6 J, which the drag update's own scoping (§3d) already flagged as
    physically impossible (a ~4–14 mg fragment perforating a 1-inch board).
    **But this does not mean the residual is confined to the threshold**: a
    threshold-*free* test (matching cumulative mass fraction instead of
    imposing a mass cut) still finds the model over-counting 2.15–2.70× on
    the Tolch-metal basis — a residual that survives deleting the threshold
    entirely is by definition not "not the population" (the claim published
    here through 2026-08-03; void, see `rebaseline-verdict.md` §2). The
    correct statement: the residual is **predominantly** in the perforating
    fraction (~2.1× of the ~3.9×), but ~1.2–2.7× of it (1.19–1.73× with the
    coarsest, 15.4%-of-metal screen bin excluded — C4, below) is a genuine
    fragment-**spectrum** term that survives with the threshold removed.

So the honest decomposition of the 4–6× is: **a factor ~2.1× of it is an
artefact of fitting $E_{thr}$ to the falloff ratio at the anchor drag**, and a
residual **~1.6–2.3× is genuine count-chain excess** (independently
corroborated at 1.2–2.7× by the threshold-free test above) — visible as
$N(\ge0.63\text{ g}) = 1488$ against Tolch's **779** pit-recovered fragments
(mean **7.40 g**, re-baselined from a published 6.85 g, vs the model's
$2\mu$ = 1.59 g).

______________________________________________________________________

## 3. Sub-candidates, named and ranked

**C1 — the perforation decision is a hard step in KE with a fitted threshold.**
Equation (4) is a Heaviside: every fragment above $m_{thr}$ perforates, none
below. Real perforation depends on presented area, yaw and shape as well as KE,
so a compact fragment and a tumbling sliver of equal energy differ by a large
factor; and because $n(m)$ rises steeply toward small $m$, the location of the
step dominates the answer (table in §2: a 150× span in $E_{thr}$ moves $N$ by
3×). $E_{thr}$ is currently *fitted to the very falloff curve the test is meant
to check*, which is what makes Tolch a compound test rather than an anchor.
An independently-sourced threshold now exists to test this without fitting:
the 1944 Ordnance Dept. card's own 78.6 J casualty energy (§2 table, not
tuned to Tolch's data) lands at 2.2–2.5×, matching Tolch's own hole-size-bound
threshold (126 J → 2.2×) rather than the fitted values (4.2–4.4×). Two
threshold sources external to (or only weakly coupled to) the falloff fit now
agree with each other, which tightens confidence in the leverage estimate
below. **Leverage tightens to 1.7–2.1× of the residual** (fitted 1.9 J row
$N/779 = 3.94$ vs. the 0.63 g threshold-free cut $N/779 = 1.91$ ⇒ 2.06×; vs.
the sourced 78.6 J row $N/779 = 2.28$ ⇒ 1.73×; `rebaseline-verdict.md` §3).
Still the biggest single term and the only unbounded one.

**C2 — $V_0$ in (5) is the terminal Gurney velocity, not the case velocity at
break-up.** `mott_params` evaluates $x_0$ at break-up *radius* $r_{bu}$
($r_i\sqrt3$) but with the *asymptotic* Gurney $V_0$ — the case has not finished
accelerating at that radius, so the two are taken at different instants. Since
$N_0 \propto V_0^2$, using $v_{bu} = f V_0$ gives $N_0 \to f^2 N_0$: measured
0.81× at $f$ = 0.9, 0.64× at 0.8, 0.49× at 0.7. **Leverage: 1.2–2×, in the
right direction, and it is an internal inconsistency rather than a tuning knob.**
Explicitly *not* touched by the shape-closure fix (`../mott-scale-gap/_scale_verdict_ledger.md`
§4 item 2 raised it and deferred it; `updates/mott-fragment-shape-closure/derivation.md`
changes only $\alpha$/$\gamma$ and $t_{bu}$).

**Measured directly against the two non-fitted thresholds (§2, 78.6 J and
126 J), not merely as an $N_0$/$\mu$ ratio.** Sweeping $f\in\{1.0, 0.9, 0.8,
0.7, 0.6\}$ through `mott_params` and re-solving $m_{thr}$(15 ft) at each $f$
(script block (b2)) gives, at $E_{thr}$ = 78.6 J: $N/700$ = 2.54 → 2.08 → 1.66
→ 1.29 → 0.96 and $N/779$ = 2.28 → 1.87 → 1.49 → 1.16 → 0.86 (re-baselined
from a published 803, ×1.031 — `rebaseline-verdict.md`) as $f$ falls
1.0 → 0.6; at $E_{thr}$ = 126 J: $N/700$ = 2.16 → 1.77 → 1.42 → 1.10 → 0.82
and $N/779$ = 1.95 → 1.60 → 1.28 → 0.99 → 0.73. **Both non-fitted thresholds
cross into the §4 PASS band (within 2×) by $f\approx0.85$–0.9, and by
$f$ = 0.7 the 126 J row matches Tolch's totals almost exactly** ($N/779$ =
0.99). So C2's leverage is not just directionally plausible — at a *fixed,
sourced* threshold it is by itself large enough to move the 2.2–2.5× residual
measured at $f$ = 1 into, or past, the PASS band, with no change to C1.
Physically, $f$ = 0.85–0.9 is unremarkable: it is the fraction of terminal
Gurney velocity a case wall typically carries partway through its
detonation-driven acceleration, well before the asymptotic value is reached.

**Whether $f$ (or the true case velocity at $r_{bu}$) is derivable from
existing code: no — it is new physics, not a lookup.** `gurney_velocity`
(`src/arty/fragmentation.py:281`) returns only the closed-form *terminal*
Gurney velocity from the standard asymptotic formula; it contains no
expansion-time or expansion-radius state. `_shell_geometry` (line 266)
computes $r_{bu}$ as a pure geometric ratio ($r_i\sqrt3$, from Mott's
break-up-strain criterion) with no coupling to a velocity history either. The
module has no ODE or closed-form $v(r)$ trace of the case wall during
detonation-product expansion — Gurney's derivation is normally solved as an
energy-balance ODE in radius (or the equivalent closed form for simple
geometries) to get intermediate velocity, and neither exists in
`src/arty/`. Supplying $v_{bu}$ instead of an assumed $f$ would require
deriving and adding that piece, which is out of scope for this pass.

**C3 — the single-exponential Mott form in the sub-gram tail.** $N(\ge m)$ is
extrapolated to $m_{thr}$ = 0.02–0.04 g, i.e. 15–30× below Tolch's finest screen
cut (0.63 g). Nothing validates the form there. **Leverage: unquantifiable but
only bites through C1** — at a physical threshold ($m_{thr} \gtrsim 0.6$ g) the
extrapolation is not exercised at all. Do not chase this before C1.

**C4 — mass bookkeeping into $N_0$** (`mass_deductions` = 200 g placeholder,
fuze/band/base plug, fines below recovery). **Still not a 4–6× driver, so the
dismissal-as-a-driver holds — but the bound was understated and this is no
longer "note only".** The coarsest recovery-screen bin is 6 pieces / 926.7 g =
**15.4 %** of recovered metal at 154 g mean, against the model's 200 g
`mass_deductions` (3.3 %). Dropping that bin moves the threshold-free
population residual (Fact 2's inference fix, above) from 2.15× to **1.19×** —
it is now the single largest source of spread in the population term
(`rebaseline-verdict.md` §3, C4).

**C5 — the observed side is detection-limited, not physics-limited** (drag
scoping §3d, weighing point 3). Tolch's 700 counts holes he could *see*; the
model counts every fragment above threshold. This biases the comparison high at
every drag value by an unquantified amount and is **not a model defect** — but
it sets a floor on how much of the residual is even attributable, and must be
bounded before a fix is credited with closing anything.

**Recommendation: check C1 first, alone.** It carries the largest and only
unbounded share, and it is the term that makes the test compound (L1's own
words). **Correction to this paragraph's original claim:** "C2 cannot be
measured against anything until C1 is decoupled" is true only against the
*fitted* $E_{thr}$ rows (1.9–3.6 J), where a refit reabsorbs any $N_0$ change
by construction. It does **not** hold against the two non-fitted thresholds
(78.6 J, 126 J) — C2's leverage is directly measurable there (above), and on
its own is large enough to close most or all of the 2.2–2.5× residual left
after $E_{thr}$ is fixed. C1 is still recommended first because it remains
the larger, unbounded term and the one that makes the comparison compound;
but C2 is not blocked on C1 the way originally stated — it could equally be
run first, or the two combined and cross-checked, against either non-fitted
threshold. Implementing C2 still requires deriving $v_{bu}$ or sourcing $f$
(new physics, see above), so it does not change what's scoped for the next
pass.

______________________________________________________________________

## 4. The numerical investigation, and the verdict criterion

**What C1's check does.** Replace the fitted $E_{thr}$ with an **independently
determined** perforation criterion for 1″ spruce, then recompute $N(\ge m_{thr})$
at 15 ft as a *prediction* (no free parameter), and separately re-check the
A→D falloff ratio 0.557 which then also becomes a prediction. Two observables,
zero fitted parameters — the test stops being compound.

**Verdict criterion.** Tolch's own quoted probable errors give σ ≈ 0.12–0.15 on
density values ≈1.5 (i.e. ~10 %), and his two independent totals (700 panel
perforations, **779** pit fragments — re-baselined from a published 803)
differ by **11 %**, not the 15 % published here through 2026-08-03
(779/700 = 1.113; `rebaseline-verdict.md` §4 — the two totals agree *better*
than previously stated, which tightens rather than loosens this criterion).
Against that:

- **PASS / count chain exonerated** — predicted 15 ft count within **2×** of
    700–779 *and* predicted A→D ratio within 0.10 of 0.557. Then L1's 4–6× was
    a threshold-fit artefact, the count chain needs no change, and L1 should be
    rewritten to say so.
- **FAIL / count chain implicated** — count still ≥ 2× high at a sourced
    threshold. Then proceed to C2 (break-up velocity) as a Workflow-B change,
    with the now-fixed threshold as the invariant that makes the improvement
    measurable.
- **INDETERMINATE** — if C5's detection cutoff cannot be bounded below ~1.5×,
    say so and stop; the dataset cannot resolve a 2× claim.

Factor 2 is the right band here (and matches `../drag-gap-1944/b-vs-range.md`'s
criterion): a 1938 four-round average, hole-counted by eye, against an
ensemble-mean continuum model.

## 5. New math — flagged, not derived

**C1 needs physics that `src/arty/` does not have.** There is no perforation or
penetration model in `src/arty/` (`grep` for THOR/perforat returns nothing); the
existing chain only offers `min_lethal_mass`, a KE-threshold bisection against a
*supplied* $E_{thr}$. Supplying an independent number therefore requires one of:

1. **THOR-type penetration equations** (Ballistic Research Labs, Project THOR
    Report 47) — residual velocity / ballistic limit as a power law in fragment
    mass, striking velocity, obliquity and plate parameters. Coefficients for
    **wood** are the specific need. Not in `doc-reference/`.
1. A **spruce ballistic-limit** datum (energy or $v_{50}$ per unit thickness for
    a compact steel fragment against ~25 mm softwood), which would let $E_{thr}$
    be *sourced* rather than fitted without adding a model.

**@librarian is needed before C1's derivation pass**: THOR Report 47 (or a
secondary carrying its wood coefficients), and/or softwood ballistic-limit data.
Option 2 is the cheaper close and is sufficient for the verdict criterion above;
option 1 additionally converts Tolch into a reusable second anchor, which is what
`updates/mach-dependent-fragment-drag/scoping.md` §6 asks for.

Until that lands, **no `src/arty/` change is scoped by this thread**, and C2 must
not be implemented — a $N_0$ change made while $E_{thr}$ is still fitted is
unfalsifiable, because the fit will absorb it.

## Missing References

- Project THOR Report No. 47, *The Resistance of Various Non-Metallic Materials
    to Perforation by Steel Fragments* (Ballistic Analysis Laboratory / BRL,
    1961\) — wood/softwood perforation coefficients.
- Any source giving a ballistic limit ($v_{50}$ or $E_{50}$) for compact steel
    fragments against ~25 mm (1″) softwood.

## Fidelity target

This aspect drives the **absolute lethal-fragment count** (hence $N_\text{eff}$,
$p_\text{kill}$ and every casualty-area number in the demo), not its shape with
range. Tolerable error: **a factor of 2 on absolute count against 1938-era
recovered-fragment data** — the demo's $p_\text{kill}$ saturates, so a 2× count
error moves the lethal-radius contour by roughly the log-slope of $N(r)$, tens
of percent, whereas the present 4–6× does not.
