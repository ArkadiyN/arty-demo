# The count chain vs. Tolch's absolute perforating count — scoping

**Status: Scoped, paused; re-baselined 2026-08-08, re-closed against shipped
code 2026-08-08 (post-6c1faff / `50b734e`).** §1 exonerates the Mott
$(\mu, N_0)$ *parameter* stage — no material or geometric input can carry a
4–6× multiplier — and localizes the residual to the fitted perforation
threshold (C1) and, secondarily, the break-up-velocity treatment (C2). §2's
inference that the residual is confined to that threshold ("not the
population") does **not** survive: a threshold-free test still finds the
model over-counting 1.78–2.24× on the Tolch-metal basis, so a genuine
fragment-*spectrum* term shares the residual alongside the threshold-fit
artefact (~1.65–2.05×) — see the restated Fact 2 below and
[`rebaseline-verdict.md`](rebaseline-verdict.md) for the full re-baseline
(all pit-count-denominated numbers here move from a published 803 to the
corrected 779). **The overall residual has fallen from the 4–6× L1 reports to
3.2–3.7× at a fitted threshold and 1.7–2.2× at a sourced one**, because
6c1faff re-anchored $\gamma'$ 65→54.5 and fixed the ogive/cylinder $V_0$
contradiction while `50b734e` sourced the 75 mm M48 case mass; the
consequences for this thread's verdict are set out at the end of §4 and are
material. Closing C1 still needs an independent perforation model (§5) — out
of scope for now. Nothing in `src/arty/` changes as a result of this thread.

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

| Link | Parameter        | $N_0 \propto$             | Factor needed for 4–6×                | Admissible?                                                                 |
| :--- | :--------------- | :------------------------ | :------------------------------------ | :-------------------------------------------------------------------------- |
| (1)  | $V_0$            | $V_0^{2}$                 | $V_0$ high by 2.0–2.4×                | **No** — model 864.4 vs Tolch's measured 838.2 m/s (item 10): high by 1.03× |
| (3)  | $M_\text{case}$  | $M_\text{case}$           | case mass high by 4–6×                | **No** — 4980 g, *below* Tolch's 13.29 lb (6028 g) pit-recovery basis       |
| (5)  | $\sigma_f$       | $\sigma_f^{-1}$           | $\sigma_f \approx 133$–200 MPa        | **No** — shipped 800 MPa; Mott's own worked example is 772 MPa              |
| (5)  | $\gamma'$        | $\gamma'$                 | $\gamma' \approx 218$–327             | **No** — shipped 54.5; Mott's table spans 42–67                             |
| (5)  | $A,\kappa_x$     | $A\kappa_x^{2}$           | prism 4–6× more slender               | **No** — fixed by `updates/mott-fragment-shape-closure/derivation.md` §2–4  |
| (5)  | $t_{bu}, r_{bu}$ | $(t_{bu}r_{bu}^2)^{-1}$   | break-up radius/thinning wrong 2–2.5× | Bounded — see C2                                                            |
| (4)  | $E_{thr}$        | — (enters $N$, not $N_0$) | **unbounded**                         | fitted, not sourced                                                         |

**The Mott parameter stage cannot carry a 4–6× multiplier.** This is the same
closure argument the `../mott-scale-gap/` thread ran pre-fix, re-run against the
post-fix algebra (5): every material and geometric input would have to leave its
literature bracket by 4–6×. So if the residual is in the count chain at all, it
is in $V_0$ (bounded, below) or in the **decision stage** (4).

______________________________________________________________________

## 2. Where the residual actually sits — measured

75 mm M48 HE, DoD anchor $C_D C_\text{shape} = 2.674$, 15 ft panel station.
Script: [`checks/count-chain-decomposition.py`](checks/count-chain-decomposition.py).

Current shipped model (re-closed against `src/arty/fragmentation.py` after
commit 6c1faff, which re-anchored $\gamma' = 54.5$ and fixed the
ogive/cylinder $V_0$ contradiction, and after `50b734e`, which sourced the
75 mm M48 `mass_deductions`): $V_0 = 864.4$ m/s, $M_\text{case} = 4980$ g,
$\mu = 0.826$ g, $2\mu = 1.65$ g, $N_0 = 3016$.

| $E_{thr}$ [J] | source of the value                                                                               | $m_{thr}$(15 ft) [g] | $N(\ge m_{thr})$ | as % of $N_0$ | vs Tolch 700 |
| ------------: | :------------------------------------------------------------------------------------------------ | -------------------: | ---------------: | ------------: | -----------: |
|           1.9 | fitted to the 0.557 A→D falloff ratio                                                             |                0.020 |             2577 |          85 % |     **3.7×** |
|           3.6 | fitted (upper $V_0$ case)                                                                         |                0.032 |             2478 |          82 % |     **3.5×** |
|          78.6 | 1944 Ordnance Dept. card's own casualty threshold, 58 ft-lb (`../drag-gap-1944/b-vs-range.md` §2) |                0.359 |             1560 |          52 % |     **2.2×** |
|           126 | Tolch's own smallest-hole bound, $m\ge0.36$ g at 838 m/s                                          |                0.538 |             1346 |          45 % |     **1.9×** |
|         294.5 | pre-anchor fitted $E_{thr}$                                                                       |                1.134 |              934 |          31 % |     **1.3×** |

**The 78.6 J row is an independent cross-check, not a fit.** It is lifted
verbatim from a second, unrelated 1944 historical source (the Ordnance Dept.
card's own stated casualty energy, already used as-is in `../drag-gap-1944/`
for the Family B comparison) — it is not tuned to Tolch's falloff shape and
not derived from Tolch's hole-size data the way the 126 J row is. At this
threshold $N/700 = 2.23\times$ and $N/779 = 2.00\times$ (**779, not 803** — the
re-baselined pit-recovered count, `rebaseline-verdict.md`; every $N/803$
figure below is corrected the same way, ×1.031), landing in the same band as
Tolch's own hole-size-bound row (1.92× / 1.73×) and well inside the
fitted-threshold band (3.5–3.7×) that L1 originally reported. Two
independently-sourced thresholds — one from Tolch's own recovered-fragment
data, one from an unrelated 1944 ordnance card — now agree with each other on
the residual (1.7–2.2×) far more closely than either agrees with the fitted
values. **Under the current shipped parameters both sourced-threshold rows
reach, or sit on, §4's own PASS band (within 2× of 700–779)**: the 126 J row
is inside it on both denominators, the 78.6 J row is inside it on the 779
denominator and 12 % outside on the 700 one. That is a change of verdict
direction relative to the pre-6c1faff numbers (2.2–2.5×, unambiguously
outside), and it is driven by shipped physics, not by anything re-argued here
— see the "verdict framing" note at the end of §4.

Two facts follow, and they reframe L1:

1. **$N_0$ is not 4–6× too high.** $N_0 = 3016$ sits *between* Tolch's two own
    totals: ~5000 fragments issuing from the shell (panel extrapolation, item 6)
    and **779** recovered in the pit at 95.6 % of the metal (items 1, 8) —
    re-baselined from a published 803 (`rebaseline-verdict.md`; the re-baselined
    `tables/pit-screen-recovery.csv` closes on 779 and only on 779). Those two
    Tolch numbers are mutually consistent — the 4221 non-recovered events carry
    the missing 4.4 % of mass at ~0.0625 g each — and the model's total lies
    inside them. **The gross fragment count is not the defect.**

1. **The residual is predominantly (not entirely) in the perforating
    *fraction*.** The model declares 82–85 % of $N_0$ able to perforate 1″
    spruce at 15 ft; Tolch measures 700/5000 = **14 %**. That single ratio,
    ~6×, *is* the L1 residual, and is produced by the fitted $E_{thr}$ =
    1.9–3.6 J, which the drag update's own scoping (§3d) already flagged as
    physically impossible (a ~4–14 mg fragment perforating a 1-inch board).
    **But this does not mean the residual is confined to the threshold**: a
    threshold-*free* test (matching cumulative mass fraction instead of
    imposing a mass cut) still finds the model over-counting 1.78–2.24× on
    the Tolch-metal basis (13.29 lb = 6028 g) — a residual that survives
    deleting the threshold entirely is by definition not "not the population"
    (the claim published here through 2026-08-03; void, see
    `rebaseline-verdict.md` §2). The correct statement: the residual is
    **predominantly** in the perforating fraction (~1.7–2.1× of the ~3.3×),
    but ~1.8–2.2× of it is a genuine fragment-**spectrum** term that survives
    with the threshold removed.

    *Basis caveat, new since 6c1faff + 50b734e:* the shipped
    $M_\text{case} = 4980$ g is now **below** Tolch's recovered metal
    (5764 g), so the threshold-free test's *model-mass* basis has gone
    degenerate — $\phi > 1$ for every screen cut past the coarsest, driving
    $m^\ast \to 0$ and collapsing $N_\text{model}$ onto $N_0$. Only the
    Tolch-13.29 lb basis is quotable now, and it is the one used above. The
    two figures are not in conflict: `50b734e` sourced $M_\text{case}$ to
    Tolch's own *empty shell & fuze* metal (10.94 lb = 4962 g, matched to
    0.4 %), whereas the pit test's 13.29 lb recovery basis is a larger,
    differently-defined metal weight. Which of the two is the right
    denominator for a spectrum comparison is a criterion-match question this
    thread does not settle.

So the honest decomposition of the (now) ~3.3–3.7× is: **a factor ~1.65–2.05×
of it is an artefact of fitting $E_{thr}$ to the falloff ratio at the anchor
drag** (fitted 1.9 J row $N/779 = 3.31$ against the sourced 78.6 J row's 2.00
and the threshold-free 0.63 g cut's 1.62), and a residual **~1.7–2.0× is
genuine count-chain excess** (independently corroborated at 1.78–2.24× by the
threshold-free test above) — visible as $N(\ge0.63\text{ g}) = 1259$ against
Tolch's **779** pit-recovered fragments (mean **7.40 g**, re-baselined from a
published 6.85 g, vs the model's $2\mu$ = 1.65 g).

______________________________________________________________________

## 3. Sub-candidates, named and ranked

**C1 — the perforation decision is a hard step in KE with a fitted threshold.**
Equation (4) is a Heaviside: every fragment above $m_{thr}$ perforates, none
below. Real perforation depends on presented area, yaw and shape as well as KE,
so a compact fragment and a tumbling sliver of equal energy differ by a large
factor; and because $n(m)$ rises steeply toward small $m$, the location of the
step dominates the answer (table in §2: a 155× span in $E_{thr}$ moves $N$ by
2.8×). $E_{thr}$ is currently *fitted to the very falloff curve the test is
meant to check*, which is what makes Tolch a compound test rather than an
anchor. An independently-sourced threshold now exists to test this without
fitting: the 1944 Ordnance Dept. card's own 78.6 J casualty energy (§2 table,
not tuned to Tolch's data) lands at 2.00–2.23×, matching Tolch's own
hole-size-bound threshold (126 J → 1.73–1.92×) rather than the fitted values
(3.2–3.7×). Two threshold sources external to (or only weakly coupled to) the
falloff fit now agree with each other, which tightens confidence in the
leverage estimate below. **Leverage: 1.65–2.05× of the residual** (fitted
1.9 J row $N/779 = 3.31$ vs. the 0.63 g threshold-free cut $N/779 = 1.62$
⇒ 2.05×; vs. the sourced 78.6 J row $N/779 = 2.00$ ⇒ 1.65×;
`rebaseline-verdict.md` §3).
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
(script block (b2)) gives, at $E_{thr}$ = 78.6 J: $N/700$ = 2.23 → 1.82 → 1.46
→ 1.13 → 0.84 and $N/779$ = 2.00 → 1.64 → 1.31 → 1.01 → 0.75 (re-baselined
from a published 803, ×1.031 — `rebaseline-verdict.md`) as $f$ falls
1.0 → 0.6; at $E_{thr}$ = 126 J: $N/700$ = 1.92 → 1.57 → 1.26 → 0.98 → 0.73
and $N/779$ = 1.73 → 1.41 → 1.13 → 0.88 → 0.65. **Under the current shipped
parameters both non-fitted thresholds are already at or inside the §4 PASS
band (within 2×) at $f$ = 1**, so C2 is no longer needed to reach it: the only
row still outside is 78.6 J on the 700 denominator (2.23×), which crosses by
$f\approx0.95$. By $f$ = 0.7 the 78.6 J row matches Tolch's totals almost
exactly ($N/779$ = 1.01) and the 126 J row has gone *under* (0.88), i.e. an
aggressive $f$ now risks over-correcting. So C2's leverage remains
directionally right, but it is no longer the term that decides the verdict —
that changed with the shipped $\gamma'$ / $V_0$ fixes, not with any argument
here.
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
extrapolated to $m_{thr}$ = 0.02–0.03 g, i.e. 20–30× below Tolch's finest screen
cut (0.63 g). Nothing validates the form there. **Leverage: unquantifiable but
only bites through C1** — at a physical threshold ($m_{thr} \gtrsim 0.6$ g) the
extrapolation is not exercised at all. Do not chase this before C1.

**C4 — mass bookkeeping into $N_0$** (fuze/band/base plug, fines below
recovery). **Not a 4–6× driver, and — unlike the position published here
through 2026-08-08 — no longer the largest source of spread in the population
term either.** Two things changed underneath it. (i) `50b734e` replaced the
200 g `mass_deductions` placeholder with a sourced 975 g fuze+booster
(TM-9-1901 / TM-9-1904), so the deduction is 19.6 % of the loaded metal, not
3.3 %, and is no longer a free knob. (ii) With $M_\text{case}$ = 4980 g the
coarsest recovery-screen bin (6 pieces / 926.7 g = **15.4 %** of recovered
metal at 154 g mean) no longer dominates: dropping it moves the threshold-free
population residual from 1.78× to 2.03×, i.e. slightly *up* rather than down to
the 1.19× previously reported. The earlier 1.19× figure came from the
fuze-excluded variant that subtracts screen-1 mass from the numerator while
keeping the fuze-inclusive $M_\text{case}$ in the denominator — an
inconsistency already raised as an open finding against
`checks/count-chain-rebaseline.py`, and one that the sourced deduction makes
more visible, not less. **C4's residual live question is now a
criterion-match one** (which metal weight — Tolch's 10.94 lb empty-shell-and-fuze
or his 13.29 lb pit-recovery basis — is the right spectrum denominator), not a
magnitude one (`rebaseline-verdict.md` §3, C4).

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
its own is large enough to close most or all of the 1.7–2.2× residual left
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

**Verdict framing after the 2026-08-08 re-closure — read before reusing this
thread's conclusion.** The criterion above is unchanged, but the shipped
model has moved *into* it without C1 or C2 being done. At a sourced
threshold the current code predicts $N/779$ = 1.73 (126 J) to 2.00 (78.6 J)
and $N/700$ = 1.92 to 2.23 — i.e. **the count arm of the PASS test is now
met or marginal, not failed**. What is *not* yet met is the second PASS
condition, the A→D falloff ratio within 0.10 of 0.557, which is still tied to
the fitted $E_{thr}$ and therefore still compound. So:

- L1's headline "4–6× over-prediction" is stale as a description of the
    shipped model at a sourced threshold; at the *fitted* threshold it is now
    3.2–3.7×, and essentially all of that excess is the threshold fit.
- The thread's original FAIL-leaning framing ("count chain implicated,
    proceed to C2") is **not supported by the current numbers**. C2 at
    $f\approx0.7$–0.77 would push the 126 J row below unity (§3's sweep: 126 J
    is 1.26 on the 700 denominator and 1.13 on the 779 one at $f$ = 0.8,
    dropping to 0.98 / 0.88 at $f$ = 0.7) — over-correction.
- What still stands unchanged: C1 is the unbounded term, the test is compound
    until $E_{thr}$ is sourced, and §5's @librarian need (a spruce ballistic
    limit) is the gating item. Sourcing $E_{thr}$ is now a *confirmation* of a
    provisional PASS rather than an attempt to rescue a FAIL — which, if
    anything, raises its value.

This re-framing is a consequence of shipped physics changes (6c1faff's
$\gamma'$ re-anchor and $V_0$ fix, `50b734e`'s sourced $M_\text{case}$), not
of any new argument in this thread.

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
