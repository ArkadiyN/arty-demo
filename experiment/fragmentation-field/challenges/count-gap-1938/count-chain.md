# The count chain vs. Tolch's absolute perforating count — scoping

**Status: C1 and C2 both discharged and shipped; re-closed against shipped code
2026-08-16 (post `breakup_velocity_fraction`, and post the per-shell
aspect-ratio moment $c$ that `mass-dependent-fragment-shape` shipped into
`arty.shells.SHELLS` — $c_{75}$ = 0.9854, $A_\text{eff}$ 1.600 → 1.577, which
moves $\mu$ 0.929 → 0.915 g and $N_0$ 2681 → 2720; every count on this page has
been re-run against it and the direction of the verdict is unchanged).
Verdict: count arm FAILS at
2.28× (band 2.11–2.44×) — outside the within-2× PASS band, but by far less than
the 4–6× L1 originally reported. C5, C3, and C4 have since been investigated
(2026-08-10, 2026-08-15, 2026-08-15) and are all now discharged — C5 without
credit, C3 real but diagnostic-only at 1.328× (see banner below §3's C3 entry
and [`mott-tail-shape.md`](mott-tail-shape.md)), C4 a criterion-match choice
worth ≈0.2× (see [`spectrum-mass-basis.md`](spectrum-mass-basis.md)); none
reopens `src/arty/`, and **no sub-candidate remains.**** Both sub-candidates
this thread named as actionable (C1, C2) have since been implemented,
reviewed and merged, so this document is no longer a scoping document for
them; it is the standing record of what the count arm now measures, and its
investigation is complete.

- **C1** — a sourced, mass-*dependent* wood-perforation threshold (plug shear-out,
    $E_{thr}(m) = \eta\,\tau\,\pi D(m)\,t^2$) now exists as
    `arty.perforation.perforation_threshold_energy`
    ([`../../updates/sourced-wood-perforation-threshold/`](../../updates/sourced-wood-perforation-threshold/derivation.md)).
    Nothing in it is fitted to Tolch. It moved the count arm the *wrong* way —
    1.73× → 2.50× on /779 — because a mass-independent scalar threshold
    over-charges the light end of the spectrum.
- **C2** — Mott's $V$ is the case velocity *at the instant of fracture*, not the
    terminal Gurney velocity; `mott_params` now evaluates the $x_0$/$\mu$ chain at
    $v_{bu} = fV_0$, $f$ = 0.943 (band 0.899–0.953), from
    `arty.fragmentation.breakup_velocity_fraction`
    ([`../../updates/breakup-velocity-fraction/`](../../updates/breakup-velocity-fraction/derivation.md)).
    It moves the arm the right way — 2.50× → **2.28×** — but does not clear the
    band at any admissible $f$, and per its §6 it may **not** be cited as a
    validation win ($f$ is degenerate with $\gamma'$ inside Mott's tabulated
    42–67 span).

§1 still exonerates the Mott $(\mu, N_0)$ *parameter* stage — no material or
geometric input can carry the multiplier. §2's original inference that the
residual is confined to the threshold ("not the population") did **not** survive
and is now decisively refuted: with the threshold sourced and the velocity basis
corrected, the surviving 2.28× is *predominantly a spectrum/census term* — the
threshold-free test lands at 1.61–2.02× on the Tolch-metal basis, i.e. it
accounts for most of the 2.28× on its own. See the restated Fact 2 below and
[`rebaseline-verdict.md`](rebaseline-verdict.md) for the full re-baseline (all
pit-count-denominated numbers here move from a published 803 to the corrected
779). **The overall residual has fallen 4–6× → 2.11–2.44×** through five
shipped changes: 6c1faff's $\gamma'$ 65→54.5 re-anchor and ogive/cylinder $V_0$
fix, `50b734e`'s sourced case mass, C1's threshold, C2's break-up velocity, and `5d742b4`'s per-shell
aspect-ratio moment.
**C5 has since been investigated and discharged (§3): it was the only
candidate that could have absorbed the residual as a comparison-basis
artefact rather than a model defect, and it does not — bounded at ≤1.222× on
its most generous reading, and at ~0 on the correct reading of Tolch's census
(perforation/penetration/dent grading, not a detection floor).** That also
discharges §4's INDETERMINATE clause, which fired only if C5's cutoff could
not be bounded below ~1.5×: it is bounded well inside that, so the verdict is
a plain, genuine **FAIL at 2.28× (/779) and 2.54× (/700)** — not "FAIL
trending INDETERMINATE" as earlier drafts of this banner had it.
**C3 has since been investigated and discharged (2026-08-15, §3):
diagnostic-only credit of 1.328× — real, applied to the residual it restates
2.28× → 1.72× (/779), but every *sourced* alternative spectrum shape moves the
residual the wrong way, so nothing ships and the count arm may not be
re-declared PASS on it.** See
[`mott-tail-shape.md`](mott-tail-shape.md) for the full study.
**C4 has since been investigated and discharged too (2026-08-15, §3): the
criterion-correct spectrum denominator is Tolch's 10.94 lb fuze-excluded case
metal, restating the threshold-free residual as 1.8–2.1× — a criterion choice
worth ≈0.2×, not a driver.** See
[`spectrum-mass-basis.md`](spectrum-mass-basis.md) for the full study. **No
sub-candidate remains** — C3, C5 and C4 have all dropped off the ranking,
discharged without credit that can ship. Nothing further in `src/arty/` is
scoped by this thread. **One out-of-band avenue outside this ranking was tried
and then shipped (2026-08-16) as a correctness fix rather than as a
residual-reducer: the per-shell aspect-ratio moment $c$ restates the 75 mm chain
2.51×/2.25× → 2.54×/2.28×, i.e. marginally *away* from PASS. It is now the
baseline every number on this page is closed against.**
See §3's closing entry below and
[`../../updates/mass-dependent-fragment-shape/`](../../updates/mass-dependent-fragment-shape/derivation.md).

FINDING\[deferrable\]: headline 1.221x/2.05x C5 figures rest on the inadmissible 0.36g/838m/s datum (iv) though the sound census-grading argument (i) alone suffices; three status surfaces lead with the numeric figures instead of (i) (affects: experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md, experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md, experiment/fragmentation-field/challenges/README.md; since: 2026-08-10)

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

Current shipped model, **re-closed 2026-08-16 against `src/arty/fragmentation.py`
with C2's $f$ = 0.943 and the per-shell $c_{75}$ = 0.9854 both active** (and after 6c1faff, which re-anchored
$\gamma' = 54.5$ and fixed the ogive/cylinder $V_0$ contradiction, and
`50b734e`, which sourced the 75 mm M48 `mass_deductions`): $V_0 = 864.4$ m/s
(terminal, unchanged), $v_{bu} = 815.1$ m/s, $M_\text{case} = 4980$ g,
$\mu = 0.915$ g, $2\mu = 1.83$ g, $N_0 = 2720$. *The pre-C2 values were
$\mu = 0.826$ g, $2\mu = 1.65$ g, $N_0 = 3016$; every count in this section has
been re-run and moved down accordingly. The 2026-08-16 per-shell $c$ then moved
$\mu$ 0.929 → 0.915 g and $N_0$ 2681 → 2720 — a +1.5 % shift in $N_0$ that
propagates to every count below at roughly +1.3 %, since the smaller $\mu$ eats
part of it through the survival factor
([`checks/count-chain-aspect-moment-reclosure.py`](checks/count-chain-aspect-moment-reclosure.py)
prints the legacy and shipped columns side by side).*

| $E_{thr}$ [J] | source of the value                                                                                                                                                                 | $m_{thr}$(15 ft) [g] | $N(\ge m_{thr})$ | as % of $N_0$ | vs Tolch 700 |
| ------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------: | ---------------: | ------------: | -----------: |
|           1.9 | fitted to the 0.557 A→D falloff ratio                                                                                                                                               |                0.020 |             2343 |          86 % |     **3.3×** |
|           3.6 | fitted (upper $V_0$ case)                                                                                                                                                           |                0.032 |             2257 |          83 % |     **3.2×** |
|          78.6 | 1944 Ordnance Dept. **personnel-casualty (incapacitation)** criterion, 58 ft-lb — *not a wood-perforation criterion; plausibility probe only, not a sourced threshold for this arm* |                0.359 |             1455 |          53 % |       (2.1×) |
|           126 | Tolch's own smallest-hole bound, $m\ge0.36$ g at 838 m/s — a criterion-matched but *mass-independent* row, superseded by the plug-shear model below                                 |                0.538 |             1264 |          46 % |     **1.8×** |
|         294.5 | pre-anchor fitted $E_{thr}$                                                                                                                                                         |                1.134 |              894 |          33 % |     **1.3×** |

*Note $m_{thr}$ is unaffected by C2 — it depends on terminal $V_0$, which C2
leaves untouched. All movement in this table is through $N_0$ and $\mu$.*

**The 78.6 J row is a plausibility probe, not an admissible sourced
perforation threshold.** It is lifted verbatim from a second, unrelated 1944
historical source (the Ordnance Dept. card's own stated casualty energy,
already used as-is in `../drag-gap-1944/` for the Family B comparison), so it
is at least not tuned to Tolch's falloff shape. It measures a *different
physical quantity*: its own source defines 58 ft-lb as the energy at which a
hit produces a **personnel casualty** ("It is incapacitation and not
necessarily death"), stated mass-independently and never in connection with
wood — the perforation figures in that same section are for 1/8-, 1/4-, 3/8-
and 1/2-in. **mild steel**. Soft-tissue penetration depth and softwood
plug shear-out are different failure mechanisms, so feeding 78.6 J to the
perforate/no-perforate step is a criterion mismatch under
`.claude/rules/source-data-fidelity.md`, and this row is **not counted as a
sourced threshold** for the count arm
([`../../updates/sourced-wood-perforation-threshold/review-criterion-check.md`](../../updates/sourced-wood-perforation-threshold/review-criterion-check.md)).
It is retained in the table only to show where the count sits at that energy.
At this threshold $N/700 = 2.08\times$ and $N/779 = 1.87\times$ (**779, not
803** — the re-baselined pit-recovered count, `rebaseline-verdict.md`; every
$N/803$ figure below is corrected the same way, ×1.031).

**The 126 J row is superseded, and its near-pass was misleading.** It is
Tolch's own smallest-perforating-hole bound, computed from the same experiment
the model is scored against, so it is at least a wood-perforation quantity; at
shipped parameters it now reads $N/700 = 1.81\times$, $N/779 = 1.62\times$.
But it is a *mass-independent scalar* applied to a mechanism that is not, and
the criterion-correct plug-shear model below shows what that costs: the scalar
row's apparent pass is bought by over-charging the light end of the spectrum,
where most of the count lives. **The 126 J row is retained for continuity and
is not the verdict row.** Its remaining use is as a *detection* datum rather
than a perforation one — see C5 in §3, where it becomes the best available
bound on Tolch's hole-counting floor.

### The verdict row: mass-dependent plug shear, at the break-up velocity (2026-08-10)

Every row above is a **mass-independent scalar** $E_{thr}$, which no
perforation mechanism actually is. C1 has since been discharged:
[`../../updates/sourced-wood-perforation-threshold/derivation.md`](../../updates/sourced-wood-perforation-threshold/derivation.md)
§7.3 derives a plug-shear threshold
$E_{thr}(m) = \tfrac12\,\tau\,\pi D(m)\,t^2$ — $\tau$ = 8.96 MPa from Sanborn
2019 Table 2 (ASTM D143 solid-wood coupon), $t$ = Tolch's 1″ panel,
$D(m)$ the compact-fragment closure — with **no free parameter and nothing
fitted to Tolch**. It is shipped as
`arty.perforation.perforation_threshold_energy`. Re-running *this* chain
through it (derivation.md §7.4 Check 4, pre-registered before the run;
script [`checks/count-chain-plug-shear.py`](checks/count-chain-plug-shear.py)):

C2 then landed on top of it, moving $N_0$ 3016 → 2681 and $\mu$ 0.826 → 0.929 g;
the per-shell $c$ then moved them again, to $N_0$ = 2720, $\mu$ = 0.915 g.
The table below is the **combined C1+C2+$c$ result at shipped defaults** (re-run
2026-08-16); the parenthesised figures are the same rows at $f$ = 1, i.e. C1
alone, as this section reported them before C2 shipped:

| variant                                          | $m_{thr}$(15 ft) [g] |         $N$ |          $N/700$ |          $N/779$ |
| ------------------------------------------------ | -------------------: | ----------: | ---------------: | ---------------: |
| **SPF-S, $\eta$ = ½ — central, the verdict row** |            **0.166** |    **1776** | **2.54×** (2.78) | **2.28×** (2.50) |
| SPF-S ∓1σ on $\tau$, $\eta$ = ½                  |        0.118 / 0.218 | 1901 / 1670 |     2.72 / 2.39× |     2.44 / 2.14× |
| SYP, $\eta$ = ½                                  |                0.210 |        1685 |            2.41× |            2.16× |
| $\eta$ = 1 rigid bound (SPF-S / SYP)             |        0.370 / 0.474 | 1441 / 1325 |     2.06 / 1.89× |     1.85 / 1.70× |

Separately, sweeping C2's own uncertainty band on the central row gives
$N/779$ = 2.32× at $f$ = 0.953 and 2.11× at $f$ = 0.899
([`../../updates/breakup-velocity-fraction/derivation.md`](../../updates/breakup-velocity-fraction/derivation.md)
§8). Note $N$ does **not** scale as $f^{-2}$: $N_0\propto f^2$ falls while
$\mu\propto f^{-2}$ rises and the larger $\mu$ raises the survival factor, so
realised leverage is 1.096× against the naive 1.125× — about 22 % of the
intended correction is eaten back.

**The count arm FAILS on the criterion-correct threshold even with C2 applied:
2.28× on /779, 2.54× on /700, outside §4's within-2× PASS band on both
denominators.** The whole $\eta$ = ½ band is outside on /779 (2.14–2.44) and on
/700 (2.39–2.72); so is the whole admissible $f$ band (2.11–2.32 on /779).
Only the $\eta$ = 1 rigid bound falls inside, and per assumption A8 $\eta$ is
geometry and may **not** be moved to buy the pass, so the central row is what is
reported. **C2 is a correct, direction-right fix worth ~9 % of the residual; it
does not change the verdict, and per its §6 it is not independently falsifiable
from data in hand** ($f$ is degenerate with $\gamma'$ — the $\gamma'$
reproducing the same $\mu$ at $f$ = 1 is 48.5, inside Mott's tabulated 42–67
span, so the case for C2 rests on Gold 2017's source definition of $V$, not on
this count improvement).

The direction was pre-registered and is confirmed: the plug-shear $m_{thr}$
arrives at the panel at 612 m/s, above the 243 m/s crossover where plug shear
becomes *more permissive* than the 78.6 J constant, so $m_{thr}$ drops
0.359 → 0.166 g and $N$ rises 1.22×.

**What this changes, and it is the central result of the thread.** The 126 J
row's near-pass (now 1.61×) was partly the threshold being too strict for the
wrong reason — it is a whole-fragment hole-size bound applied
mass-independently, so it over-charges the light end where most of the count
is. With a mechanism-correct, mass-dependent criterion the perforating-fraction
residual is **larger**, not smaller. That does not indict the threshold (its own
checks 1–3 and its ±27 % $\tau$ sensitivity all pass — derivation.md §7.4).

What it does is **relocate the residual off the threshold and onto the
spectrum/census side**, and C2 has since removed the velocity-basis candidate
from that list as well (worth only ~9 %). The re-closed threshold-*free* test
now lands at **1.61–2.02×** on the Tolch-metal basis (block (E), re-run
2026-08-16; was 1.78–2.24× pre-C2) — i.e. a comparison that never imposes a
mass cut at all already reproduces most of the 2.28×. The threshold is no
longer where the residual lives. This row also inherits the standing block-(D)
caveat — an energy-thresholded whole-shell count over a size-thresholded
recovery census — so the criterion-clean (E) figure remains the
better-conditioned statement of the same gap, and the plug-shear row now sits
just above it rather than far above it.

Two facts follow, and they reframe L1:

1. **$N_0$ is not 4–6× too high.** $N_0 = 2720$ sits *between* Tolch's two own
    totals: ~5000 fragments issuing from the shell (panel extrapolation, item 6)
    and **779** recovered in the pit at 95.6 % of the metal (items 1, 8) —
    re-baselined from a published 803 (`rebaseline-verdict.md`; the re-baselined
    `tables/pit-screen-recovery.csv` closes on 779 and only on 779). Those two
    Tolch numbers are mutually consistent — the 4221 non-recovered events carry
    the missing 4.4 % of mass at ~0.0625 g each — and the model's total lies
    inside them. **The gross fragment count is not the defect.**

1. **The residual is now predominantly in the fragment *spectrum*, not in the
    perforating fraction — this reverses the original Fact 2.** At the *fitted*
    $E_{thr}$ = 1.9–3.6 J the model declares 83–86 % of $N_0$ able to perforate
    1″ spruce at 15 ft against Tolch's 700/5000 = **14 %**, and that ~6× ratio
    *was* the L1 residual. It was produced by the fit, which the drag update's
    own scoping (§3d) already flagged as physically impossible (a ~4–14 mg
    fragment perforating a 1-inch board). But a threshold-*free* test (matching
    cumulative mass fraction instead of imposing a mass cut) still finds the
    model over-counting **1.61–2.02×** on the Tolch-metal basis (13.29 lb =
    6028 g; re-run 2026-08-16, was 1.78–2.24× pre-C2) — a residual that
    survives deleting the threshold entirely is by definition not "not the
    population" (the claim published here through 2026-08-03; void, see
    `rebaseline-verdict.md` §2). With C1 sourcing the threshold and C2 fixing
    the velocity basis, the surviving 2.28× and the threshold-free 1.61–2.02×
    have converged: **the threshold now contributes at most ~1.1–1.4× on top of
    a spectrum/census term that carries the rest.** That is what re-ranks
    C3/C4/C5 in §3.

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

So the honest decomposition of the fitted-threshold ~2.9–3.0× (re-run: the
1.9 J row is now $N/779 = 3.01$, not 3.31) is: **a factor ~1.5–2.0× of it is an
artefact of fitting $E_{thr}$ to the falloff ratio at the anchor drag** (3.01
against the 0.63 g threshold-free cut's 1.52), and a residual **~1.5–2.0× is
genuine count-chain excess** (independently corroborated at 1.61–2.02× by the
threshold-free test above) — visible as $N(\ge0.63\text{ g}) = 1187$ against
Tolch's **779** pit-recovered fragments (mean **7.40 g**, re-baselined from a
published 6.85 g, vs the model's $2\mu$ = 1.83 g). Note that this 1.52× floor
sits **above** Tolch's finest screen cut, so it is not an artefact of the
sub-gram extrapolation and not an artefact of census incompleteness at the
light end — it is the part of the residual that C3 (§3) cannot explain.

______________________________________________________________________

## 3. Sub-candidates — C1 through C5 all discharged; none remain

**C1 — the perforation decision was a hard step in KE with a *fitted*
threshold. DISCHARGED (shipped).** Equation (4) is a Heaviside: every fragment
above $m_{thr}$ perforates, none below. Because $n(m)$ rises steeply toward
small $m$, the location of the step dominated the answer (§2 table: a 155× span
in $E_{thr}$ moves $N$ by 2.6×), and $E_{thr}$ was *fitted to the very falloff
curve the test is meant to check* — which is what made Tolch a compound test
rather than an anchor. That is now fixed:
[`../../updates/sourced-wood-perforation-threshold/derivation.md`](../../updates/sourced-wood-perforation-threshold/derivation.md)
§7.3 derives a mass-dependent plug-shear criterion with no free parameter and
nothing fitted to Tolch, shipped as
`arty.perforation.perforation_threshold_energy`; it passed review.

**C1's realised leverage was ~1.3×, and in the *unfavourable* direction —
neither the magnitude nor the sign earlier passes assumed.** This thread
estimated 1.65–2.05× of the residual would come off when $E_{thr}$ was sourced.
Instead $N/779$ went 2.97 (fitted) → 2.47 (sourced, $f$=1), a 1.20× improvement
against the fit, but *up* from the 1.61× the mass-independent 126 J proxy had
suggested. The Heaviside step is still a Heaviside — C1 replaced a fitted
scalar with a sourced *function of mass*, it did not soften the step, and yaw
and shape dependence remain unmodelled. **What C1 settles is that the threshold
is no longer the unbounded term, and no longer the largest one.**

**C2 — $V_0$ in (5) was the terminal Gurney velocity, not the case velocity at
break-up. DISCHARGED (shipped).** `mott_params` evaluated $x_0$ at break-up
*radius* $r_{bu}$ ($r_i\sqrt3$) but with the *asymptotic* Gurney $V_0$ — two
different instants. Gold (2017) states the source definition: Mott's $V$ is the
velocity at the instant of fracture (PAFRAG supplies it from a hydrocode at
break-up time). `mott_params` now takes `f_breakup`, defaulting to
`breakup_velocity_fraction()` = $\sqrt{1-\eta_{bu}^{-(\gamma_g-1)}}$ = **0.943**
(band 0.899–0.953 at $\eta_{bu}$ = 3); terminal $V_0$ is untouched in
`gurney_velocity` and `min_lethal_mass` — two instants, one model
([`../../updates/breakup-velocity-fraction/derivation.md`](../../updates/breakup-velocity-fraction/derivation.md)
§5, §8).

**C2's realised leverage was 1.096×, not the 1.2–2× estimated here.** Two
reasons the earlier estimate was too generous. (i) The $f$ = 0.7–0.8 rows that
made the range look wide are **retired** — no source read supports $f<0.90$,
and the physical argument for "0.85–0.9 is unremarkable" recorded in earlier
versions of this section was an assertion, not a derivation; the derived value
is 0.943. (ii) $N$ does **not** move as $f^{-2}$: $N_0\propto f^2$ falls while
$\mu\propto f^{-2}$ rises, and the larger $\mu$ raises the survival factor, so
~22 % of the intended correction is eaten back. **And it may not be counted as
a validation win**: $f$ is degenerate with $\gamma'$ in $\mu$
($\gamma'_\text{eq}$ = 48.5 at $f$ = 0.943, inside Mott's tabulated 42–67), so
the case for it rests entirely on the source definition of $V$. The
double-count gate does pass — $f<1$ makes fragments heavier *and* fewer, closing
~11 % of the mean-mass gap against Tolch's pit census while removing ~9 % of the
count (derivation §6).

*Superseded note, kept for provenance:* earlier versions of this section
concluded "$f$ is new physics, not a lookup — `src/arty/` has no $v(r)$ trace of
the case wall, so supplying $v_{bu}$ requires an expansion ODE." That framing
was wrong about the cost. The break-up update did **not** need a velocity
history: applying Gurney's energy partition at finite expansion instead of at
infinity makes the partition coefficient $(M/C+1/2)$ cancel in the *ratio*, so
$f$ depends on the released-energy fraction alone and closes in one line from
the CJ isentrope. The lesson for future sub-candidates in this thread is that
"needs new physics" is not the same as "needs a big model".

**C3 — the single-exponential Mott form in the sub-gram tail. RUN AND CLOSED
2026-08-15: real at 1.328×, but not sourced — see
[`mott-tail-shape.md`](mott-tail-shape.md).** The realised credit is 1.328× of
the "up to 1.50×" estimated below (the first sub-candidate in this thread whose
predicted leverage was close to right), restating the residual as **1.72×
(/779) / 1.91× (/700)**. It is **not actionable**: the only shape that pays is
a $\lambda$ fitted to Tolch itself; Mott's own 3D exponent $\lambda=1/3$ and the
literature's power-law tail both move the residual *up* (0.85× and 0.31–0.72×).
**No `src/arty/` change follows.** The original entry stands below as the
scoping that was executed.

$N(\ge m)$ is extrapolated well
below Tolch's finest screen cut (0.63 g) and nothing validates the form there.
This thread previously dismissed C3 on the premise that "at a physical
threshold ($m_{thr}\gtrsim0.6$ g) the extrapolation is not exercised at all" —
**that premise is now falsified.** The sourced plug-shear threshold lands at
$m_{thr}$ = **0.166 g**, a factor 3.8 *below* the finest screen cut, so the
verdict row sits squarely inside the unvalidated tail. Quantified: of the 1776
fragments in the verdict row, $N(\ge0.63\,\text{g}) = 1187$ are in the
Tolch-resolved range and **590 (33 %) come from the 0.166–0.63 g window that no
Tolch measurement constrains**. Equivalently, C3 has up to 1.50× of leverage —
enough on its own to take 2.28× to 1.52×, inside the band. **But it cannot
explain the 1.52× floor above 0.63 g**, which is measured against fragments the
census does resolve; that part belongs to C4/C5.

**C4 — mass bookkeeping into $N_0$** (fuze/band/base plug, fines below
recovery). **RUN AND CLOSED 2026-08-15: criterion-match question resolved,
not a driver — see [`spectrum-mass-basis.md`](spectrum-mass-basis.md).** Two
things changed underneath it before this pass. (i) `50b734e` replaced the
200 g `mass_deductions` placeholder with a sourced 975 g fuze+booster
(TM-9-1901 / TM-9-1904), so the deduction is 19.6 % of the loaded metal, not
3.3 %, and is no longer a free knob. (ii) With $M_\text{case}$ = 4980 g the
coarsest recovery-screen bin (6 pieces / 926.7 g = **15.4 %** of recovered
metal at 154 g mean) no longer dominates: dropping it moves the
threshold-free population residual *up* (1.61× → 1.83× at the
through-screen-4 row), not down to the 1.19× previously reported. **This pass
resolved the criterion-match question the open finding raised**: the
correct denominator is Tolch's **10.94 lb** *empty unfuzed shell* (case metal
alone — not "empty shell and fuze", a mislabel this thread previously
carried; that name belongs to the 13.29 lb figure), paired with a
fuze-excluded numerator, because Tolch's own text identifies screen 1 as
"mostly pieces of fuze" and the model's $M_\text{case}$ = 4980 g is
fuze-excluded by construction (`mass_deductions` already removes fuze+booster)
— corroborated to 0.4 % against Tolch's own 10.94 lb. On that consistent
basis the threshold-free residual is **1.8–2.1×** (anchored on the
well-conditioned screen-2 cut), not the 1.19× floor: that figure was an
artefact of a since-superseded pre-`50b734e` placeholder and never existed on
current shipped code. **C4 is a criterion choice worth ≈0.2× inside the
correct family, not a 4–6× driver and not the largest source of spread. No
`src/arty/` change follows** — the defect was in the comparison script, not
the model (`rebaseline-verdict.md`'s fourth re-closure banner).

**C5 — the observed side is detection-limited, not physics-limited.
DISCHARGED 2026-08-10: bounded, and it does not clear the band on any
admissible reading.** The premise recorded here through 2026-08-08 was that
"Tolch's 700 counts holes he could *see*, the model counts every fragment above
threshold", with the bound to come from Tolch's own
**smallest-perforating-hole** datum, $m\ge0.36$ g at 838 m/s (the same figure
that supplied the 126 J row). The closure below keeps the arithmetic and
rejects the premise. Block (G) of
[`checks/count-chain-rebaseline.py`](checks/count-chain-rebaseline.py) is the
script; block (F) now prints both denominators so the basis cannot be mixed
silently.

**(i) The premise is wrong: the 700 column is perforation-limited by
construction, not detection-limited.** Tolch does not record "holes"; he
records **perforations, penetrations and dents as three separate columns**, on
every panel, in every table (`card.md`, base/nose/side-spray table criteria —
e.g. grep `"Number of perforations, penetrations, and dents of the base spray per unit solid angle."`).
A fragment too weak to go through is therefore *not lost from the census* — it
is counted in the adjacent column. The detection floor of that census is the
smallest **dent** he could see in a softwood plank, which lies far below any
perforating mass; the binding constraint on the 700 column is the perforation
mechanism itself. That mechanism is precisely what C1 already models. **C5 is
not a separate term from C1 — on the correct reading of the census it collapses
into it**, and there is no independent detection credit to take.

**(ii) Even granting the premise, the bound is an upper bound on the *credit*,
not a conservative one, and it fails.** The smallest hole Tolch *recorded* is
$\ge$ the true detection floor, so 0.36 g removes the most fragments any valid
floor could remove. At that maximum credit,
$N(\ge0.36\,\text{g}) = 1453$: **$N/700 = 2.08\times$** — the criterion-matched
pairing, a panel-side floor against the panel perforating count — i.e. still
outside the 2× band. Realised leverage 1.222×.

**(iii) The 1.85× headline published here through 2026-08-10 was a mixed
basis and is void.** It divides a model count carrying a *panel hole-visibility*
floor by the **pit sand-recovery census** (779), whose own floor is a screen
aperture, not hole visibility. That is the identical defect the open finding
raises against block (D), transferred to block (F) by how C5 quoted it. The
census-matched cut for the 779 denominator is Tolch's finest screen cut,
0.63 g → $N/779 = 1.52\times$; but that is a *census-completeness* correction
belonging to C4, not a detection correction, and it may not be quoted as C5's.

**(iv) Admissibility of the 0.36 g datum itself — weak, and the closure does
not rest on it.** `card.md` states that `tolch-1938.md` "is not a citable
surface for any number" and that "a number that has no CSV has no admissible
surface in this repo". **0.36 g has no CSV**, and the word *smallest* does not
occur anywhere in the extraction; 126 J is reconstructible as
$\tfrac12(0.36\,\text{g})(838.2\,\text{m/s})^2$ with 838.2 m/s taken from
Summary item 10's sidespray velocity, so the mass is the primary and its
provenance is unanchored. Per `.claude/rules/source-data-fidelity.md` a null
over a known-unreliable extraction bounds the surface, not the source — so this
is **flagged, not a fabrication verdict**, and `source.pdf` is not retained
locally to settle it. It does not need settling: readings (i) and (ii) bracket
the answer, and both leave the arm outside the band.

**(v) A model-side note falls out of (i), and it is C1's, not C5's.** Read as a
*perforation* observation, 0.36 g at 838 m/s rescales to the 15 ft panel through
the shipped plug-shear law ($E_{thr}\propto m^{1/3}$ against
$\text{KE}\propto mv^2 \Rightarrow m_{thr}\propto v^{-3}$): the shipped
threshold would admit **0.065 g** at 838 m/s against a smallest observed
perforation of 0.36 g — permissive by 5.6× in mass. That is a statement about
`arty.perforation`, not about the comparison basis, and it is only as good as
(iv)'s unanchored datum. Recorded as a note, not actioned here.

FINDING\[note\]: C1 plug-shear threshold rescales to 0.065 g at 838 m/s vs. Tolch's smallest observed perforation 0.36 g (5.6x permissive in mass); rests on an unanchored datum (affects: experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md; since: 2026-08-10)

**Consequence for §4's INDETERMINATE clause: discharged.** The clause fires only
if C5's cutoff "cannot be bounded below ~1.5×". It is bounded at **≤1.222×**,
and at 0 on reading (i). The verdict is therefore a genuine **FAIL**, not
INDETERMINATE — and not a PASS.

**C3 and C5 bite on the same fragments and are not additive** — the reason this
mattered, and why C5 was ordered first. Both act on the 0.166–0.63 g window: C3
says the model may not have that many fragments there, C5 said Tolch would not
have counted them if it did. With C5 discharged at ≤1.222× (and at ~0 on the
graded-census reading), **that window is now C3's alone** and the
double-counting hazard is gone. C5 was a comparison-basis question throughout;
no `src/arty/` change followed from it, as scoped.

### Recommendation, re-reasoned 2026-08-15 (C4 now closed): none remain

The old recommendation ("C1 first, alone") is spent — C1 and C2 are both
shipped. C5, C3, and now C4 have all been run and discharged in turn (above).
**No sub-candidate remains** in this thread — the count arm's investigation
is exhausted.

1. ~~**C5 (detection limit) first.**~~ **Run and discharged 2026-08-10.** The
    reasoning that put it first was sound — it was the only candidate bounded by
    data already in hand, and §4's INDETERMINATE clause required it — but the
    outcome was negative on both readings: the premise fails (Tolch's census
    grades hits as perforation/penetration/dent, so the 700 column is
    perforation-limited, not detection-limited), and even at maximum credit the
    bound leaves the arm at 2.08× on the criterion-matched denominator. The
    ~1.22× figure quoted here in the morning was real arithmetic on the wrong
    denominator (1.87× on /779 mixes a panel-side floor with the pit census).
1. ~~**C3 (sub-gram Mott tail) first now.**~~ **Run and discharged 2026-08-15
    — see [`mott-tail-shape.md`](mott-tail-shape.md), reviewed PASS.** Real at
    1.328× (residual 2.28×→1.72× on /779), but not actionable: the only
    spectrum shape that pays is a $\lambda$ fitted to the very Tolch census
    the model is validated against ($\lambda$=0.759 vs shipped 0.5), while
    every *sourced* alternative — Mott's own 3D exponent $\lambda=1/3$, and a
    spliced power-law tail per the collected literature — moves the residual
    the *wrong* way (credit 0.85× and 0.31–0.72× respectively). No
    `src/arty/` change follows; disposition is a logged limitation, not a
    Workflow-B change.
1. ~~**C4 (mass bookkeeping / census denominator) — now the whole remaining
    story.**~~ **Run and discharged 2026-08-15 — see
    [`spectrum-mass-basis.md`](spectrum-mass-basis.md), reviewed
    PASS-with-limitations.** The criterion-correct denominator is Tolch's
    10.94 lb case metal (empty *unfuzed* shell), paired fuze-excluded, giving
    a threshold-free residual of **1.8–2.1×** — resolving both open findings
    this section referenced, neither of which survives: the "1.19×" floor
    never existed on current shipped code (it was a pre-`50b734e` placeholder
    artefact), and the criterion mismatch it flagged is fixed by adopting the
    fuze-excluded pairing. **C4 is a criterion choice worth ≈0.2× within the
    correct family, not a driver. No `src/arty/` change follows.**

**Also tried, out of this ranking: mass-dependent fragment shape (`A(m)`),
2026-08-16 — shipped as a correctness fix; it moves this arm the wrong way and
is now the baseline.** A separate update
([`../../updates/mass-dependent-fragment-shape/`](../../updates/mass-dependent-fragment-shape/derivation.md))
tested whether making the aspect-ratio moment correction $c$ mass-dependent —
solved per shell against each shell's own Mott spectrum, rather than frozen at
Table 3's global 155 mm-weighted value — would move the 75 mm chain. It does
not: the per-shell fixed point gives $c$ = 0.99 at 75 mm ($A_\text{eff}$ =
1.58, vs 2.00/1.76/1.47 for 155/105/60 mm), restating the 75 mm count chain at
**2.54× (/700) / 2.28× (/779)** — marginally *worse* than the 2.51×/2.25×
it replaced, not better. It shipped anyway (`5d742b4`), because `c` is a
moment identity of the shipped Mott shape closure and belongs in the registry
whether or not it flatters this thread; **the whole of this page is now closed
against it**, so 2.54×/2.28× is the standing verdict, not an alternative to
it. This was never a ranked sub-candidate of this thread:
its own `scoping.md` §6 (Action C) explicitly scopes it to not edit
`count-chain.md`. It is recorded here because it is a real, reviewed (PASS,
[`../../updates/mass-dependent-fragment-shape/review.md`](../../updates/mass-dependent-fragment-shape/review.md))
attempt on the same residual, and belongs in this thread's record of what has
been tried against it. The `src/arty/` change it carries (`SHELLS`
`aspect_ratio` per shell) is that update's, not this thread's; no *further*
`src/arty/` change follows from here.

**What earlier passes got wrong, recorded so it is not repeated.** Both
sub-candidate leverage estimates in this section were wrong in the same
direction — C1 was predicted at 1.65–2.05× and delivered 1.20× *against the
fit* while moving the arm *away* from PASS; C2 was predicted at 1.2–2× and
delivered 1.096×. The common cause is estimating leverage from a ratio of
published $N$ values rather than re-solving the chain: $m_{thr}$, $N_0$ and
$\mu$ do not move independently, and the exponential survival factor
systematically eats part of any $N_0$ change. **Leverage figures in the ranking
above (1.222× for C5, 1.50× for C3) are re-solved counts, not scaled ones** —
but they are still upper bounds, because each assumes the others are absent.
**C5 is the third instance of the same over-estimate**, in a new form: its
1.22× was arithmetically correct but was quoted against the wrong denominator,
and the premise generating it did not survive contact with how Tolch's census
is actually graded. The generalised lesson is now *check the comparison basis
before quoting the leverage*, not only *re-solve the chain*.

______________________________________________________________________

## 4. The numerical investigation, and the verdict criterion

**What C1's check did.** Replace the fitted $E_{thr}$ with an **independently
determined** perforation criterion for 1″ spruce, then recompute
$N(\ge m_{thr})$ at 15 ft as a *prediction* (no free parameter), and separately
re-check the A→D falloff ratio 0.557 which then also becomes a prediction. Two
observables, zero fitted parameters. **The first observable has been run and is
reported in §2; the second has not** — the A→D ratio is still evaluated against
the fitted $E_{thr}$, so that arm of the test remains compound. Re-running the
falloff ratio through `arty.perforation` is the cheapest way to make this a
two-observable test and is not blocked on anything.

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
    say so and stop; the dataset cannot resolve a 2× claim. *(Did not fire —
    bounded at ≤1.222× on 2026-08-10, restated 2026-08-16; see below and §3 C5.)*

**Outcome (2026-08-10, re-closed 2026-08-16): FAIL, and the FAIL branch has
been executed to
exhaustion.** The sourced threshold gave 2.50× (≥ 2×, FAIL); C2 was run as the
prescribed Workflow-B follow-up against that fixed threshold and returned
**2.28×** — still ≥ 2×. Both denominators agree on the sign
($N/700 = 2.54\times$). So the count arm fails on the criterion the thread set
itself.

**The INDETERMINATE clause is now discharged, and it did not fire (2026-08-10,
later pass).** That clause was the last thing standing between "FAIL" and "FAIL
trending INDETERMINATE": it fires only if C5's detection cutoff *cannot* be
bounded below ~1.5×. C5 has been run and closed (§3): the cutoff is bounded at
**≤1.222×** on the datum's most generous reading, and at ~0 on the correct
reading of Tolch's census, which grades hits as perforation / penetration /
dent and is therefore perforation-limited rather than detection-limited in the
700 column. Applying the maximum credit against the criterion-matched
denominator gives **$N/700 = 2.08\times$ — still outside the band.** *The
1.85× reading published in this section earlier on 2026-08-10 is void: it
divided a panel-side detection floor by the pit sand-recovery census, the same
basis mix the open finding raises against block (D).*

**So the standing verdict is a plain FAIL at 2.28× (/779) and 2.54× (/700), not
INDETERMINATE.** The dataset *can* resolve a 2× claim at this residual — that
is what bounding C5 established — and the residual is real. The bar on
crediting further fixes is correspondingly lifted: C3 may now be worked without
crediting a model fix against an unbounded comparison bias, which is what the
criterion forbade.

Factor 2 is the right band here (and matches `../drag-gap-1944/b-vs-range.md`'s
criterion): a 1938 four-round average, hole-counted by eye, against an
ensemble-mean continuum model.

**Verdict framing after the 2026-08-10 C1+C2 re-closure — read before reusing
this thread's conclusion.** The criterion above is unchanged. Two earlier
framings recorded in this section are now void and must not be quoted:

- The **"provisional PASS at 1.73×"** reading (published 2026-08-08, keyed to
    the 126 J scalar row) is void. It rested on a mass-independent threshold
    that over-charges the light end; the criterion-correct replacement moved the
    arm to 2.50×, i.e. the near-pass was an artefact of the proxy, not a
    property of the model.
- The **"proceed to C2, it will close the gap"** reading is also void. C2 was
    run and delivered 1.096×, not the 1.2–2× projected here; the $f$ = 0.7–0.8
    rows that made over-correction look like a risk are retired, since no source
    read supports $f<0.90$ (§3). **There is no longer any prospect of C2
    over-correcting**, and no velocity-basis lever left to pull.

What stands after both:

- **The verdict is FAIL at 2.28× (band 2.11–2.44×), on a two-observable test of
    which only one observable has been run.** The A→D falloff-ratio arm is still
    tied to the fitted $E_{thr}$ and therefore still compound — that is now the
    single largest gap in the *test*, as distinct from the model.
- **L1's headline "4–6× over-prediction" is stale**, as is the 3.2–3.7×
    fitted-threshold figure that replaced it (re-run: 2.9–3.0×). The current
    honest headline is 2.28× at a sourced, mass-dependent threshold and a
    source-defined break-up velocity.
- **$N_0$ is still not the defect** (Fact 1, §2) — it sits between Tolch's own
    two totals, and moved *closer* to the pit census under C2.
- **The residual has migrated from the threshold to the spectrum/census side**,
    and every candidate that could have moved it has now been run (§3). C5 was
    ranked first and was **discharged without credit**; C3 ran next and closed
    at a real but non-actionable 1.328× (2026-08-15,
    [`mott-tail-shape.md`](mott-tail-shape.md)) — restating the residual
    2.28×→1.72× (/779) but not clearing it to a PASS, since the credit is
    unsourced and the falloff-ratio observable is still unrun. **C4 ran last
    and closed 2026-08-15 as a criterion-match choice worth ≈0.2×, not a
    driver** ([`spectrum-mass-basis.md`](spectrum-mass-basis.md)) — **no
    sub-candidate remains.**
- **The comparison basis is no longer an open excuse.** C5 was the only
    candidate that could have absorbed the residual without any model being
    wrong; it cannot. C3 quantified the model's sub-gram spectrum term at
    1.328× and found no sourced fix. C4 settled which metal weight denominates
    the spectrum comparison (10.94 lb, fuze-excluded) and found the choice
    worth ≈0.2×, not the factor the verdict turns on. **The count arm's
    standing verdict is now final: genuine FAIL at 2.28×/2.54× (plug-shear)
    and 1.8–2.1× (threshold-free) — every admissible pairing this thread has
    produced sits above the band, and no further work is scoped here.**

This re-framing is a consequence of shipped, independently reviewed physics
(C1's plug-shear threshold, C2's break-up velocity), not of any new argument in
this thread. The only new reasoning here is the §3 re-ranking, which follows
from C1's realised magnitude and direction differing from what this thread
predicted.

## 5. New math — both items closed

**Closed 2026-08-10. This section is retained as provenance; nothing in it is
outstanding, and no `src/arty/` change is scoped by this thread.**

- **C1's missing perforation model now exists.** `src/arty/perforation.py`
    supplies `perforation_threshold_energy` and `ballistic_limit_velocity` for a
    `WoodPanelTarget`, from a plug-shear derivation anchored on Sanborn 2019's
    ASTM D143 coupon shear strength. THOR Report 47 was **not** needed — option
    2 below (a sourced material property, no penetration correlation) was the
    cheaper close, as this section predicted.
- **C2's $f$ needed no expansion ODE.** See the superseded note in §3: the
    partition coefficient cancels in the ratio, so $f$ closes in one line from
    the CJ isentrope.

*Original text follows.* There was no perforation or penetration model in
`src/arty/` (`grep` for THOR/perforat returned nothing); the existing chain
only offered `min_lethal_mass`, a KE-threshold bisection against a *supplied*
$E_{thr}$. Supplying an independent number therefore required one of:

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
