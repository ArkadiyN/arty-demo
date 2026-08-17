# C3 — the single-exponential Mott form in the sub-gram tail

**Thread:** `count-gap-1938` (Workflow A assessment). **Candidate:** C3, ranked
first by [`count-chain.md`](count-chain.md) §3 after C5 was discharged.
**Status:** closed 2026-08-15; **re-closed against shipped code 2026-08-16.**
**Verdict: C3 is real at 1.328× (~34 % of the 2.28× residual) but is not
sourced — no `src/arty/` change follows.** §5.

Check script: [`checks/count-chain-mott-tail-shape.py`](checks/count-chain-mott-tail-shape.py).

> **Re-closure banner — 2026-08-16 (per-shell aspect-ratio moment $c$).**
> `mass-dependent-fragment-shape` shipped a per-shell aspect-ratio moment
> correction into `arty.shells.SHELLS` (`5d742b4`;
> `src/arty/fragmentation.py` `MOTT_ASPECT_MOMENT_C` / `mott_aspect_ratio`,
> derivation §7). For the 75 mm M48 it gives $c_{75}$ = 0.9854,
> $A_\text{eff}$ 1.600 → 1.577, hence $\mu$ 0.929 → 0.915 g and
> $N_0$ 2681 → 2720 — about +1.3 % on every count on this page. This document
> was written against the pre-$c$ code, so **every model-side figure below has
> been re-run** against shipped `SHELLS` and restated. Legacy → shipped, for
> the figures the verdict rests on:
>
> | quantity                     | legacy (pre-$c$) | shipped (2026-08-16) |
> | ---------------------------- | ---------------- | -------------------- |
> | $N(\ge 0.63$ g$)$            | 1176             | 1187                 |
> | $N(\ge 0.166$ g$)$           | 1756             | 1777                 |
> | $R_\text{shipped}$ (eq. 2)   | 1.493            | **1.497**            |
> | C3 credit, (B2) anchored fit | 1.324×           | **1.328×**           |
> | restated residual /779       | 1.70×            | **1.72×**            |
> | restated residual /700       | 1.89×            | **1.91×**            |
>
> **Nothing about the verdict moves.** The (B2) fit itself
> ($\lambda$ = 0.759, $\mu$ = 5.688 g, $N_\text{tot}$ = 840) is fitted to
> Tolch's census alone and is *independent* of shipped code — it does not move
> at all; only the shipped-Mott comparison column does. C3 remains real,
> partial, and **not sourced**. These figures match what
> [`count-chain.md`](count-chain.md) §3 (C3 entry) already states.

______________________________________________________________________

## 1. The problem, restated

`arty.fragmentation.mott_params` supplies $(\mu, N_0)$ from case geometry and
the break-up velocity; `mott_N` then evaluates the **single-exponential Mott
form**

$$N(\ge m) = N_0 \exp\!\left[-\sqrt{m/\mu}\,\right] \quad (1)$$

with mass closure $N_0 = M_\text{case}/(2\mu)$ (i.e. mean fragment mass
$\bar m = 2\mu$).

C1's sourced plug-shear threshold lands at $m_{thr} = 0.166$ g — a factor 3.8
**below** Tolch's finest screen cut (~0.63 g). So the verdict row
$N(\ge 0.166) = 1777$ is 33 % (590 fragments) an *extrapolation* of (1) into a
mass range no Tolch measurement constrains. C3 asks whether that extrapolation
is sound, and is worth at most **1.50×** of the standing 2.28× (/779) residual
— enough on its own to reach the 2× band, but not to explain the 1.52× floor
above 0.63 g.

**The quantity that carries the whole question** is the dimensionless
*extrapolation multiplier*

$$R \;=\; \frac{N(\ge 0.166\ \text{g})}{N(\ge 0.63\ \text{g})} \quad (2)$$

For the shipped model $R = 1777/1187 = 1.497$. C3 earns credit
$R_\text{shipped}/R_\text{alt}$ if a literature-supported alternative spectrum
shape, anchored on the range Tolch **does** resolve, gives a smaller $R$.
$R$ is the right isolation because it is independent of $N_0$ and of
$M_\text{case}$ — the normalisation question is C4's, not C3's.

## 2. What the literature says — and the sign trap

Collected at `doc-reference/mott-distribution-small-fragments/` (three sources).
The headline of the librarian's `index.md` ("the small-mass tail is power-law,
not exponential, so Mott is unsound below 0.6 g") is **directionally the
opposite of what C3 needs**, and that is the first thing this pass establishes:

- A power-law tail $n(m)\propto m^{-\tau}$, $\tau\approx1.9$–2.2
    (Carmona 2007 §V; Tavassoli 2000) rises **faster** toward small $m$ than a
    Mott exponential. Splicing one in at 0.63 g puts **more** fragments in the
    0.166–0.63 g window, not fewer — i.e. $R_\text{alt} > R_\text{shipped}$ and
    C3's credit is **negative**.
- The one lever that could give C3 positive credit is the **generalised Mott
    exponent**: Elek & Jaramaz (2009) eq. (6), $N(\ge m)=N_0\exp[-(m/\mu)^\lambda]$,
    noting that *"Mott had argued that in three-dimensional fragmentation of
    thick-walled cylinder, where fragments do not retain the inner and outer
    surface of original cylinder, exponent ⅓ instead ½ in (5) would be more
    appropriate"* (extraction line 60). For $m<\mu$, $(m/\mu)^{1/3} > (m/\mu)^{1/2}$,
    so $\lambda<1/2$ **depletes** the sub-gram window relative to (1). A 75 mm
    M48 is a thick-walled cylinder, so this is on-criterion, not analogy.

So the two candidate directions are in opposition, and the question is settled
numerically against Tolch's own resolved-range census, not by citation.

## 3. Method, and one method that does not work

Tolch does not publish his screen mesh openings, so two identifications of an
alternative spectrum were tried. Both fit the generalised Mott family
$N(\ge m)=N_\text{tot}\exp[-(m/\mu)^\lambda]$ to the pit census
(`tables/pit-screen-recovery.csv`), using the four screen boundaries and
holding out the census-incomplete through-screen-4 bucket.

**(B) Boundary-free locus fit — VOID, and instructive.** For this family the
locus traced in the (number-fraction, mass-fraction) plane,
$(\hat N,\varphi)=(e^{-u},\,\Gamma(1+1/\lambda,u)/\Gamma(1+1/\lambda))$,
$u=(m/\mu)^\lambda$, depends on $\lambda$ **alone** — so $\lambda$ can be fitted
without any mesh mass. It fits beautifully ($\lambda$ = 0.309, all four
residuals 0.92–1.03×, held-out row 0.99×) and is **worthless**: the mass scale
$\mu$ is then set only by the mass closure, and the implied screen boundaries
come out at **87 kg / 4.64 kg / 1.46 kg / 0.93 kg** against bucket means
154 g … 0.61 g — wrong by two to three orders of magnitude at the coarse end.
Block (C) shows the failure mode directly: as $\lambda$ rises the fit simply
inflates $\mu$ (0.38 → 10.9 kg) and $R\to1.000$, so *every* exponent "earns"
close to the full 1.50× ceiling. **A count-versus-mass locus does not identify
a fragment spectrum.** Any credit from (B)/(C) is an artefact and is not quoted.

*This does not impeach block (E) of
[`checks/count-chain-rebaseline.py`](checks/count-chain-rebaseline.py).* That
block holds the shipped $(\mu,N_0)$ **fixed** and inverts $\varphi$ only to
locate a comparison mass; nothing floats, so the degeneracy above cannot arise
there. The void is in fitting, not in testing.

**(B2) Absolute-mass-anchored fit — the identifying one.** Each screen boundary
is assigned the geometric mean of the two bucket means it separates (the
standard binned estimator): **46.65, 6.55, 1.88, 0.840 g**. Fitting
$(\lambda,\mu,N_\text{tot})$ to the cumulative counts at those four masses is
then fully determined. Result:

$$\lambda = 0.759,\qquad \mu = 5.688\ \text{g},\qquad N_\text{tot} = 840$$

Three closures **not** used in the fit all come out right, which is what makes
this fit admissible where (B) is not:

| check (not fitted)  | fit    | Tolch                                |
| ------------------- | ------ | ------------------------------------ |
| mean fragment mass  | 6.71 g | 7.40 g (recovered)                   |
| implied total metal | 5632 g | 5764 g recovered / 6028 g (13.29 lb) |
| count above 0.166 g | 784    | 779 recovered                        |

| boundary [g] | Tolch $n(\ge m)$ | (B2) fit | shipped Mott |
| ------------ | ---------------- | -------- | ------------ |
| 46.65        | 6                | 6        | **2**        |
| 6.55         | 278              | 276      | **187**      |
| 1.88         | 533              | 545      | **648**      |
| 0.840        | 675              | 665      | **1044**     |

*(The "shipped Mott" column is the only one in this table that moved on
2026-08-16; legacy values were 2 / 188 / 646 / 1036. The direction of the shape
error is unchanged and slightly sharper.)*

The shipped Mott is **too steep at the coarse end and too shallow at the fine
end** — a single-exponent shape error, exactly what $\lambda$ too small means.
The data want $\lambda\approx0.76$, i.e. a spectrum that falls off *faster*
toward small mass than $\sqrt{m/\mu}$.

## 4. Results — and the sign trap resolved

All rows are the extrapolation multiplier $R$ of eq. (2) and the C3 credit
$R_\text{shipped}/R$, at $R_\text{shipped}=1.497$ (re-run 2026-08-16; the
legacy pre-$c$ column had $R_\text{shipped}=1.493$ and credit 1.324× on the
(B2) row). Only the anchored rows are admissible.

| spectrum in 0.166–0.63 g                         | source of the shape               | $R$       | C3 credit      |
| ------------------------------------------------ | --------------------------------- | --------- | -------------- |
| shipped Mott, $\lambda=1/2$                      | `mott_params`                     | 1.497     | 1.000×         |
| **(B2) Tolch-anchored, $\lambda=0.759$**         | **fitted to the pit census**      | **1.127** | **1.328×**     |
| $\lambda=1/2$ at the same anchors                | Mott 2D                           | 1.370     | 1.093×         |
| $\lambda=1/3$ at the same anchors                | Mott's own 3D thick-wall exponent | 1.756     | **0.853×**     |
| power-law splice at 0.63 g, $\tau=1.9$           | Carmona 2007                      | 2.070     | **0.723×**     |
| power-law splice at 0.63 g, $\tau=2.2$           | Carmona 2007 (with cutoff)        | 2.367     | **0.633×**     |
| power-law splice at 3.0 g, $\tau=1.9\text{–}2.2$ | Carmona 2007                      | 3.33–4.77 | **0.45–0.31×** |

*The $R$ of the three anchored-fit rows is set by the (B2)/fixed-$\lambda$ fits
to Tolch alone and does not move with shipped code; only the credit column
(which divides by $R_\text{shipped}$) and the two spliced rows do.*

**The sign trap, resolved.** §2 set out two opposed literature directions. The
Tolch data agree with **neither**:

- The **power-law reading is refuted for this shell.** Splicing $\tau$ = 1.9–2.2
    at 0.63 g would put 2456–2809 fragments above 0.166 g where the census finds
    779, and would drive the residual *up* from 2.28× to 3.2–3.6×. The three
    collected sources are brittle-sphere impact, glass rods and mercury droplets;
    none is an HE-driven thick-walled steel cylinder, and Elek & Jaramaz's own
    survey says the power law "cannot successfully describe the HE projectile
    fragmentation". The librarian `index.md` headline ("Mott is unsound below
    0.6 g because the tail is power-law") **must not be carried forward** — it is
    a correct statement about brittle-impact comminution and the wrong sign for
    this problem.
- **Mott's own 3D exponent $\lambda=1/3$ is also refuted**, and in the same
    direction: at the anchored masses it gives $R$ = 1.756, worse than the shipped
    $\lambda=1/2$. The one sourced lever that *could* have paid C3 does not.
- What the data support is $\lambda\approx0.76$ — **between** the shipped Mott
    ($1/2$) and Grady's linear exponential ($\lambda=1$, Elek & Jaramaz eq. (7)).
    That is inside the generalised-Mott family the paper ranks best-fitting
    ($R^2\approx0.994$ over 30 projectiles), but it is a *fitted* exponent, not a
    derived one.

## 5. Verdict

**Criterion (stated before the result, in this thread's §4 style).** C3 is
credited only if an alternative sub-gram spectrum shape (i) is admissible —
identified in absolute mass, not merely in a count/mass locus — and (ii)
reduces the extrapolation multiplier $R$ below the shipped 1.497. C3 is a
*sufficient* explanation of the residual only if the credited correction alone
brings $N/779$ inside the thread's 2× band, and a *sourced* explanation only if
the shape that delivers it comes from outside the Tolch dataset.

**Verdict: C3 is REAL and PARTIAL — 1.33× of the 2.28× residual — but it is
NOT SOURCED, and no Workflow-B change follows from it.**

- **(i) Magnitude.** On the admissible (B2) anchored fit, C3's credit is
    **1.328×**. Applied to the 1.52× above-0.63 g floor (which is C4's, not C3's)
    this restates the residual as **2.28× → 1.72× (/779)** and **2.54× → 1.91×
    (/700)**. In log terms C3 accounts for **~34 %** of the standing residual
    ($\ln 1.328/\ln 2.28$). The thread's §3 estimate of "up to 1.50×" was an
    upper bound and is confirmed as such: the realised figure is 89 % of it —
    the first sub-candidate in this thread whose predicted leverage was close to
    right.
- **(ii) Sufficiency.** 1.72× is inside the 2× band. **But the count arm may
    not be re-declared PASS on this**, for two independent reasons: the second
    observable (the A→D falloff ratio) is still unrun and still compound (§4), and
    the credit is not sourced — see (iii). The honest statement is that **the
    residual outside the band is no longer attributable to the sub-gram
    extrapolation**; what remains at 1.72× is the above-0.63 g floor, which is
    measured against fragments Tolch resolves and belongs to C4.
- **(iii) Sourcing — this is where C3 fails.** Every *sourced* alternative shape
    moves the residual the wrong way ($\lambda=1/3$: 0.85×; power law: 0.31–0.72×).
    The only shape that pays is $\lambda$ fitted to the very census the model is
    being validated against. Shipping it would rebaseline the model onto its own
    validation source and make the comparison tautological — the failure mode this
    project has already recorded. **So C3 is diagnostic, not actionable.**

**Recommendation (Workflow A stops here).**

1. **No `src/arty/` change is scoped by C3.** Do not ship a fitted $\lambda$.
    The correct disposition is a **limitation entry**: the shipped Mott form is a
    two-decade-old 2D result used 3.8× below the finest mass any validating
    census resolves, and against the one HE-shell census available its exponent
    is low by ~0.26 (0.5 vs 0.76), over-populating 0.166–0.63 g by ~1.33×.
1. A *sourced* $\lambda$ would make this actionable and is the only thing that
    would. That needs a **derivation** of the exponent from the fracture
    statistics (Gold 2017 / Mott 1947 route, 3D thick-wall), or an independent
    HE-shell census with sub-gram resolution. @librarian's sweep found no such
    census in the open literature — that gap is real and is recorded in
    `doc-reference/mott-distribution-small-fragments/index.md`.
1. **C4 is now the whole remaining story.** With C3 quantified at 1.33×, the
    1.52× above-0.63 g floor is 100 % of what is left, and it is a
    normalisation/denominator question — exactly the two open findings already
    standing against `checks/count-chain-rebaseline.py` and
    `rebaseline-verdict.md`. Those should be resolved before any further
    sub-candidate is opened.
1. **Retire the `index.md` headline before it is reused.** Its "power-law tail"
    conclusion is sign-wrong for this application; §4 above records why.

**Scope cut, declared.** Two things this pass did not do: (a) it did not test
the bimodal generalised Grady (Elek & Jaramaz eq. (8)), which the paper ranks
best overall — with three free parameters against four anchored points it is
not identifiable from this census, and its physical reading (fine fragments
from the central cylinder, coarse from residual casing) is a *geometry* claim
that belongs with C4; (b) it did not re-run the A→D falloff arm, which remains
the largest gap in the *test*.
