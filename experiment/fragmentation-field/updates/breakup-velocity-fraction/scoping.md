# Scoping — case velocity at break-up radius (candidate C2)

**Workflow B, scoping pass.** Aspect: the velocity entering the Mott
shape-closure step in `arty.fragmentation.mott_params`. Nothing derived or
implemented in this pass.

Problem statement and algebra: do not re-derive, cite
[`../../challenges/count-gap-1938/count-chain.md`](../../challenges/count-gap-1938/count-chain.md)
§1 eq. (2), (5) and §3 "C2".

______________________________________________________________________

## 1. What the defect actually is (restated precisely)

`mott_params` forms

$$x_0 = \sqrt{\frac{2\sigma_f}{\rho\,\gamma'}}\;\frac{r_{bu}}{V_0}
\qquad\Longrightarrow\qquad
\mu \;=\; \frac{A\,\kappa_x^{2}\,t_{bu}\,r_{bu}^{2}\,\sigma_f}{\gamma'\,V_0^{2}},
\qquad N_0 = \frac{M_\text{case}}{2\mu}$$

The factor $r_{bu}/V_0$ is **the reciprocal of the hoop strain rate at
break-up**, $\dot\varepsilon_{bu}^{-1} = r_{bu}/v_{bu}$ — that is its only role
in Mott's plastic-instability argument. So C2 is *not* "which velocity do
fragments fly at"; it is **"what is the hoop strain rate at the instant the case
breaks"**. This reframing is the load-bearing part of the scope and it narrows
the change sharply:

- The quantity to source or derive is $\dot\varepsilon_{bu}$ (equivalently
    $v_{bu}$ at $r_{bu}$), **not** a fragment launch velocity.
- `gurney_velocity`'s terminal $V_0$ must stay as the **fragment launch
    velocity** in eq. (4) / `min_lethal_mass` — it is independently validated
    there (model 864.4 m/s vs Tolch's measured 838.2 m/s, 1.03×, count-chain §1
    row (1)). Fragments continue to be driven by the gas after break-up, so
    terminal $V_0$ at launch and $v_{bu} < V_0$ at break-up are **two different
    instants legitimately appearing in one model**, not a contradiction to be
    unified. Any option that replaces $V_0$ globally is wrong and would break a
    validated number.

So the minimal change is: one new quantity $f = v_{bu}/V_0$ (or
$\dot\varepsilon_{bu}$ directly), consumed **only** in `mott_params`'s $x_0$.
$N_0 \propto f^2$.

## 2. Does the case still accelerate at $r_{bu} = \sqrt3\,r_i$? — yes, for a shell

Mott's break-up radius is $r_{bu}=\sqrt3\,r_i$, i.e. **volume expansion ratio
$V/V_0 = 3$** for a cylinder. Kennedy 1970 states the end of the acceleration
phase in exactly those units (`source.md:296`, Table 1 item 2, verbatim):

> "Acceleration is completed after detonation products have expanded to twice
> that original charge volume for normal incidence of detonation onto metal, or
> to seven times original charge volume for grazing incidence onto metal (see
> Appendix B)."

This single sentence decides whether C2 exists:

| incidence | acceleration complete at | equivalent $r/r_i$ | vs $r_{bu}=1.732\,r_i$ |
| :-------- | :----------------------- | -----------------: | :--------------------- |
| normal    | $V/V_0 = 2$              |              1.414 | already terminal — C2 is a non-issue, $f=1$ |
| grazing   | $V/V_0 = 7$              |              2.646 | still accelerating — C2 is real, $f<1$ |

An artillery shell is detonated at one end (fuze/booster) and the detonation
front sweeps **along** the case: **grazing incidence**. So $r_{bu}$ sits at
$V/V_0=3$ of a run that does not finish until $V/V_0=7$ — the defect is real,
and Kennedy's own applicability table is the citation for it. Conversely this
is also the bound: a *normal*-incidence driven plate would need no correction,
which is a useful sanity limit for the derivation pass.

## 3. Literature audit

### Kennedy 1970 (`doc-reference/fragmentation/kennedy1970-gurney-energy/`)

- **Cannot supply $v(r)$.** The card's "Velocity during Radial Expansion — Not
    in Source" is correct and is confirmed by the source text above: the method
    is a final-state energy/momentum balance and Table 1 item 2 disclaims
    acceleration-phase motion explicitly.
- **Does supply the two things that matter for scoping:** (i) the
    expansion-ratio *endpoint* of acceleration, in the same $V/V_0$ units as
    $r_{bu}$ (§2 above) — this is the criterion match, and it is exact, not a
    transfer; (ii) Appendix B's method of computing **energy-release efficiency
    as a function of expansion ratio** (`source.md:774–776`) — which is the
    functional form a first-principles $f(V/V_0)$ would use.
- **Card defect, worth flagging to @librarian (does not affect this scope).**
    The card's "Standard Gurney Equations by Geometry" block transcribes the
    cylinder as $\sqrt{2E}(1+M/2C)^{-1/2}$ and the flat sandwich as
    $\sqrt{2E}(1+M/C)^{-1/2}$. The standard Kennedy results are
    $(M/C+1/2)^{-1/2}$ and $(M/C+1/3)^{-1/2}$; the shipped `gurney_velocity` and
    count-chain eq. (1) use the $(M/C+1/2)^{-1/2}$ form, which is corroborated
    by Martineau's Table 5.3 closure below. The card's geometry block should not
    be cited by anyone; a note-tier finding marker is filed at the foot of this
    document.

### Martineau 1998 (`.../martineau1998-viscoplastic-shell-expansion/`)

- **Closure check passes** on Table 5.3 (I ran it as arithmetic, not
    eyeballing): $\sqrt{2E}=2900$ m/s, $(M/C+1/2)^{-1/2}$ gives 2903 m/s at
    $M/C=0.498$ and 2352 m/s at $M/C=1.02$ vs tabulated 2902 / 2351. The table
    is admissible, and it independently confirms the $(M/C+1/2)^{-1/2}$ cylinder
    form (the extraction's eq. (6.1) has a misplaced closing paren —
    $\sqrt{2E(\ldots)^{-1/2}}$ — that the closure resolves in favour of
    $\sqrt{2E}\,(\ldots)^{-1/2}$).
- **This is the only source in `doc-reference/` with a measured
    velocity-vs-time trace of an explosively-expanded cylinder** (Fig. 5.7,
    Fabry-Perot + numerical; Fig. 5.8 numerical only after a hardware failure).
    Criterion match on *configuration* is good: internally detonated cylinder,
    axially propagating detonation (grazing incidence), measurement at
    mid-length.
- **But as extracted it cannot yield $f$ at $r/r_i=\sqrt3$**, for one specific
    reason: Figs. 5.7–5.8 are $v(t)$, and $r_{bu}$ is a *radius* condition. The
    conversion needs $r(t)$ — which the report has as **Figures 5.5 and 5.6
    ("radial displacement plots", named on printed p. 90 / `source.pdf` p. 105)
    — and those figures were not extracted.** With Fig. 5.5 plus the Chapter 4
    tube geometry (inner radius), $f(\sqrt3)$ is a direct read-off from the
    measured data with **no free knob**. That is the single highest-value
    @librarian ask in this scope.
- **Two criterion mismatches that survive even with Fig. 5.5 extracted**, and
    they are why Martineau alone cannot close the aspect:
    1. **$M/C$ is off by 5–15×.** Martineau: 0.498 and 1.02. The shipped
        registry (read off `_shell_geometry` + `mass_filler` this pass): 75 mm
        M48 **7.47**, 105 mm M1 5.52, 155 mm M107 5.06, 60 mm M49A2 4.91 — all
        with $\sqrt{2E}=2440$ m/s. Martineau's own data show the acceleration
        *timescale* scaling strongly with $M/C$ (25–30 µs at 0.498, ~50 µs at
        1.02). Two points at $M/C\lesssim1$ cannot be extrapolated to
        $M/C\approx5$–7.5 by interpolation; they can only **validate a model**
        that itself carries the $M/C$ dependence. Note also that Kennedy's
        recommended validity band is $0.2<M/C<10$ (Table 1 item 1), so the
        shipped shells sit in the upper half of it — usable, but not central.
    2. **Material:** annealed OFE copper, not fragmenting steel — irrelevant for
        $v(r)$ (gas-driven inertia dominates) but it means the shell does *not*
        break at $\sqrt3\,r_i$ in these tests, so the measurement is of a
        continuous ductile expansion, not of a break-up event. That is fine for
        the velocity history and must be stated as an assumption.

### Gold 2017 / PAFRAG-Mott (`doc-reference/fragmentation/fragment-size-distribution-conwep/`)

Not in the brief, but it is **the source `mott_params` actually implements**
(`src/arty/fragmentation.py:342` cites "Gold 2017 eq. (2) / Mott 1947 after
eq. (5)"), so it is the source that defines the disputed symbol. Verbatim,
immediately before eq. (2)
(`1-s2.0-S221491471730079X-main.md:56`):

> "At the instant of fracture, let $r$ be the radius of the ring and $V$ be the
> velocity with which the shell is moving outwards."

**This settles the criterion match: $V$ in eq. (2) is defined by its own source
as the velocity at the instant of fracture, not the terminal velocity.** The
shipped code substitutes terminal $V_0$ into a symbol the source defines
otherwise — C2 is a genuine defect against the source's own definition, and the
sign is the residual's sign (over-stated $\dot\varepsilon$ → under-stated $x_0$
→ under-stated $\mu$ → over-stated $N_0$).

It also shows how the reference implementation obtains that velocity: PAFRAG
takes per-segment pairs $(r_j, V_j)$ from a **CALE hydrocode run** at the
break-up time (eq. (16)), which is precisely the $v(r)$ trace `src/arty/` does
not have. And it confirms the break-up criterion the project uses is the same
rule of thumb (card: `V/V₀ ~ 3`, "criterion is accepted as a rule of thumb",
p. 301), i.e. $\eta_{bu}=3$ is Gold's assumption too, not an independent one.

### Verdict of the audit

Neither source alone gives a knob-free $f$. **Kennedy fixes the *bracket*
(acceleration incomplete at $V/V_0=3$, complete at 7) and supplies the
functional form; Martineau can supply the *validation data* but only after
Figs. 5.5/5.6 are extracted, and only at $M/C\sim1$.** The $M/C=7$ regime the
model needs is reachable only through a derived $v(V/V_0; M/C)$ — i.e. new
math, validated against Martineau, bracketed by Kennedy.

## 4. Options, ranked

**Option 1 (recommended) — derive $f$ from a Gurney energy-balance in
expansion ratio, validate against Martineau, bracket with Kennedy.**
Retain Gurney's own two assumptions (linear gas velocity profile, uniform wall
velocity) but apply the energy balance at an *intermediate* expansion ratio:
the fraction of Gurney energy released by expansion to $V/V_0=\eta$ under a
$\gamma_g$-law isentrope is $1-\eta^{-(\gamma_g-1)}$, giving

$$f(\eta) \;=\; \frac{v(\eta)}{V_0} \;=\; \sqrt{1-\eta^{-(\gamma_g-1)}}\;,
\qquad \eta_{bu}=3 .$$

($\gamma_g$ = detonation-product isentrope exponent; **not** Mott's $\gamma'$ —
the symbol clash is a real hazard in this module and the derivation must keep
them distinct.) Sanity numbers (scoping-level, to be redone properly in
derivation): $\gamma_g=3$ → $f=0.94$; $\gamma_g=2.5$ → $f=0.90$. Limit checks
it must pass: $f\to0$ as
$\eta\to1$; $f\to1$ as $\eta\to\infty$; and $f(\eta)$ must be ≈1 by $\eta=7$
and *not* by $\eta=2$, reproducing Kennedy's grazing/normal bracket — that is a
real falsifiable test of the closure, not a fit. $M/C$ dependence enters through
how the released energy is partitioned, which is where Martineau's two $M/C$
points earn their keep as validation.
**Cost:** ~1 derivation pass + 1 small `src/arty/` pass (one new function
returning $f$ or $\dot\varepsilon_{bu}$, threaded into `mott_params` only).
**Risk:** $\gamma$ for detonation products is itself a choice (2.5–3 is
conventional); the $f$ range 0.90–0.94 is narrow, so the choice is not
load-bearing — see §5.
**No free knob:** $\eta_{bu}=3$ comes from Mott's break-up strain, $\gamma$ from
the detonation-product EOS, nothing is tuned to the count residual.

**Option 2 — @librarian extracts Martineau Figs. 5.5/5.6 + Chapter 4 tube
geometry; read $f(\sqrt3)$ off the measured trace directly.**
This is not an alternative to Option 1 so much as **its validation arm**, and it
should be requested in parallel. On its own it delivers $f$ only at
$M/C\approx0.5$–1.0 and would have to be applied to $M/C=7$ as a constant,
which is an unjustified transfer. Cheap, though, and the only *measured*
anchor available.

**Option 3 — adopt a literature-typical constant $f=0.9$ with the Kennedy
bracket as justification, log the assumption, and stop.**
Legitimate closure under the project's assumption-logging rule. $f=0.9$ gives
$f^2=0.81$, i.e. **1.23× of the 2.47× count residual** — leaving 2.0×, still
inside the §4 PASS band but not by much. Costs one `derivation.md` section, no
new physics. Weakness: $f$ is a bare number in `src/arty/` with no functional
dependence on $M/C$ or shell geometry, so it will not travel to the 105/155 mm
shells with different $M/C$ — and this model is a multi-shell registry.

**Option 4 — full viscoplastic/hydrocode route (Martineau's actual GTN +
Mie-Grüneisen model).** Rejected. Out of proportion to a $\le1.25\times$ effect
in a Poisson count, needs an EOS and a damage model the project has no
parameters for, and is not cheap to evaluate.

**Option 5 — do nothing; log C2 as a limitation.** The honest fallback if §5's
sensitivity argument is accepted as decisive. See §5.

## 5. The sensitivity finding that should change the priority

count-chain §3 states C2's leverage as **1.2–2×**, from sweeping
$f\in\{1.0\ldots0.6\}$. That range is a *sweep*, not a physics bound. Every
physically-grounded estimate of $f$ available here lands at the **top** of the
$f$ range and therefore the **bottom** of the leverage range:

- Kennedy: acceleration is $\ge$ half-done by $V/V_0=2$ and complete by 7;
    $\eta_{bu}=3$ is well past the knee.
- Martineau Fig. 5.7: measured plateau 2750–2800 vs Gurney 2902 — the *terminal*
    measured value is already 0.95× Gurney, and the curve is within a few percent
    of plateau over most of the trace.
- Option 1's closed form: $f = 0.90$–0.94.

So the defensible leverage is $f^2 \approx 0.81$–0.89, i.e. **1.12–1.24×** —
the bottom edge of the published band. $f=0.7$ (leverage 2×) is not supported by
any source read here and should be retired from the thread's framing.
Consequence: **C2 cannot by itself bring the count arm from 2.47× to under 2×**
(2.47/1.24 = 1.99, i.e. exactly borderline at the most favourable defensible
$f$). It is a correct, cheap, direction-right fix, not the fix that decides the
verdict. C1's successor (the threshold/spectrum residual, count-chain §3 C1/C3)
remains the larger term.

**Gate zero — the double-counting risk, now largely (not wholly) resolved.**
$\gamma'$ (shipped 54.5, table span 42–67) is *semi-empirical* — Gold's own
words, "a semi-empirical statistical constant determining the dynamic fracture
properties of the material". If its calibration basis had paired the tabulated
$\gamma'$ with a **terminal** velocity, then $\gamma'$ already absorbs $f^2$ and
applying $f^2$ on top **double-counts**, converting a sourced constant into a
fit and moving the count the right way for the wrong reason (the project's
"rebaseline onto validation source" trap). Evidence read this pass:

- **For C2 being real:** Gold 2017 defines $V$ at the instant of fracture
    (§3 above), and PAFRAG supplies it from a hydrocode — so the reference
    implementation of *this exact formula* never used a terminal velocity, and
    $\gamma\approx50$ is calibrated against fracture-instant velocities.
- **Against, and the residual risk:** Mott/Linfoot 1943's own worked example
    pairs the burst radius with *the terminal fragment velocity* —
    `mott-linfoot-1943-theory-of-fragmentation/quotes.md:127`, verbatim: "For $r$
    we take 2.2 inches, and for $V$, **the velocity of the fragments**, 2500
    ft/sec." That is the 1943 $W$-based breadth formula, not the 1947 $\gamma'$
    form the code implements, so it does not directly impugn $\gamma'$ — but it
    does show the terminal-velocity pairing is what the *original* calibration
    used, and the shipped 54.5 comes from a carbon-content table whose own
    velocity basis was not established in this pass.
- Same page also warns $\eta_{bu}$ is not universal: "thick cased shells expand
    further than thin ones before breaking up" (`quotes.md:158`) — relevant to
    Option 1's fixed $\eta_{bu}=3$, and an assumption to log.

**Consequence for the derivation pass:** proceed with Option 1, but the
derivation must state the $\gamma'$ basis explicitly and check that the adopted
$f$ does not push $\gamma'$-equivalent outside Mott's 42–67 table span. Since
$\gamma \propto$ (nothing in $f$) but $\mu \propto f^{-2}$, an equivalent test
is: does applying $f=0.9$ leave the predicted **mean fragment mass** consistent
with Tolch's recovered spectrum, or does it merely move the count? A fix that
improves the count while worsening $\mu$ against the screen census is the
double-count signature — that check is mandatory, and it is cheap because the
census is already in `../../challenges/count-gap-1938/checks/`.

## 6. Recommendation

**This is resolvable without new sourcing.** Option 1 proceeds — the audit
delivered the two things a knob-free derivation needs: a source-stated symbol
definition making C2 a defect rather than a preference (Gold 2017, §3) and a
source-stated expansion-ratio bracket to test the closure against (Kennedy
$V/V_0 = 2$ vs 7, §2). Martineau is the validation arm, not a prerequisite.

1. **Derivation pass — Option 1**, with these mandatory contents:
    - $f(\eta) = \sqrt{1-\eta^{-(\gamma_g-1)}}$ (or the equivalent Gurney
        energy-balance in radius), $\gamma_g$ the detonation-product isentrope
        exponent, sensitivity of $f$ to $\gamma_g$ over 2.5–3 reported.
    - Limit checks: $f\to0$ at $\eta\to1$; $f\to1$ at large $\eta$; $f$ ≈1 by
        $\eta=7$ and clearly \<1 at $\eta=2$ (Kennedy's bracket).
    - **Define $\eta$ from the gas cavity, not the wall.** The shipped
        `_shell_geometry` gives $r_{bu}/r_i$ = 1.79–1.83 across the registry
        (not exactly $\sqrt3$ = 1.732), so $\eta$ is 3.2–3.35 if the ratio is
        read as an inner-radius ratio. Which radius the volume ratio is taken
        over must be stated; it moves $f$ by ~1 %, so it is bookkeeping, not
        physics, but leaving it implicit is how sign/ratio errors enter.
    - **The double-count check of §5**: confirm the adopted $f$ does not push
        predicted $\mu$ away from Tolch's recovered mass spectrum while
        improving the count.
    - Log as assumptions: fixed $\eta_{bu}=3$ despite Mott's "thick cased shells
        expand further"; grazing incidence assumed for all shells; no $M/C$
        dependence in $f$ beyond what the energy balance supplies.
1. **In parallel, one @librarian ask** (Option 2, optional — Option 1 does not
    block on it): Martineau 1998 Figures 5.5 and 5.6 (radial displacement vs
    time, named on printed p. 90 / `source.pdf` p. 105; the figures themselves
    are ~2 pages earlier) plus the Chapter 4 test-cylinder inner radius and wall
    geometry. Combined with the already-extracted Fig. 5.7 $v(t)$ this yields a
    **measured** $f(\eta)$ at $M/C\approx0.5$ — the only such anchor in reach.
1. **Scope cap for the derivation pass:** one new `src/arty/fragmentation.py`
    function returning $f(\eta_{bu};\gamma_g)$ or $\dot\varepsilon_{bu}$,
    consumed **only** in `mott_params`'s $x_0$. Terminal `gurney_velocity` stays
    untouched everywhere else (§1). No re-fit of $\gamma'$, $\sigma_f$, $A$,
    $\kappa_x$. Expected effect: $N_0 \times 0.81$–0.89, count arm
    2.47× → ~2.0–2.2×.
1. **Expectation management for the parent:** this does **not** close the count
    arm's FAIL on its own (§5). If the parent's goal is a PASS, C2 must be
    sequenced with a second change on the threshold/spectrum arm, and that
    should be decided before the derivation pass is spent.

**Fidelity target.** This aspect drives the absolute perforating-fragment count
against Tolch 1938 (currently 2.47× on the /779 basis) via $N_0\propto f^2$.
Tolerable error on $f$ is ±0.05 absolute (±10% on $N_0$) — anything tighter is
unrecoverable given the $M/C=7$ extrapolation, and anything looser makes the
correction indistinguishable from the assumption it replaces.

FINDING[note]: kennedy1970-gurney-energy/card.md "Standard Gurney Equations by Geometry" transcribes the cylinder as sqrt(2E)(1+M/2C)^-1/2 and flat sandwich as (1+M/C)^-1/2; standard Kennedy forms are (M/C+1/2)^-1/2 and (M/C+1/3)^-1/2, and the (M/C+1/2) form is what shipped gurney_velocity uses and what Martineau Table 5.3 closes on (affects: doc-reference/fragmentation/kennedy1970-gurney-energy/card.md; since: 2026-08-10)
