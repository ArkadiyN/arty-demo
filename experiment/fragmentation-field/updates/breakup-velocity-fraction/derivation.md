# Derivation — case velocity at break-up, $f = v_{bu}/V_0$ (candidate C2)

**Workflow B, derivation pass.** Executes
[`scoping.md`](scoping.md) §6 Option 1. No `src/arty/` edits in this pass.
Scoping's §1–§5 are taken as the accepted plan (reframing, Kennedy bracket,
literature audit, double-count gate) and are not re-litigated.

## 0. Symbols (the clash is real — keep these apart)

| symbol | meaning | value / range | unit |
| :----- | :------ | :------------ | :--- |
| $\gamma_g$ | detonation-product **isentrope (polytropic gas) exponent** | 2.5–3, adopt 3 | – |
| $\gamma'$ | Mott's **semi-empirical fracture constant** (`ShellSteel.gamma`, 54.5) | 42–67 table span | – |
| $\eta$ | gas-cavity volume expansion ratio $V/V_{0,\text{charge}}$ | $\eta_{bu}=3$ | – |
| $\eta_f$ | expansion ratio at which acceleration is complete | 2 normal / 7 grazing | – |
| $f$ | $v_{bu}/V_0$, case speed at break-up over terminal Gurney speed | derived | – |
| $V_0$ | terminal Gurney velocity, `gurney_velocity` | 864.4 m/s (75 mm M48) | m/s |
| $\dot\varepsilon_{bu}$ | hoop strain rate at break-up $= v_{bu}/r_{bu}$ | derived | s⁻¹ |

$\gamma_g$ and $\gamma'$ are numerically ~20× apart, so a symbol slip is loud,
not silent — but the module already carries `gamma` for $\gamma'$, so the new
quantity must **not** be named `gamma` in `src/arty/`.

______________________________________________________________________

## 1. The energy balance in expansion ratio

Gurney's method is an energy partition at a single instant: all chemical energy
released to that instant appears as kinetic energy of gas (linear velocity
profile, $v_{gas}(r) = v_{wall}\,r/r_{wall}$) plus kinetic energy of the wall
(uniform velocity $v_{wall}$). For the cylinder this gives the shipped form

$$V_0 = \sqrt{2E}\,\Big(\tfrac{M}{C}+\tfrac12\Big)^{-1/2}. \qquad (1)$$

(Form confirmed by Martineau Table 5.3 closure, scoping §3; **do not** cite the
Kennedy card's geometry block — see the open `note` finding.)

**Key structural observation.** Equation (1)'s $M/C$ factor is purely the
*geometry of the partition* — it comes from integrating $\tfrac12\rho_g v^2$
over a linear profile inside a cylinder and adding the wall term. That geometry
is **the same at every expansion ratio**: at intermediate $\eta$ the gas still
fills the cavity with a linear profile matched to the wall. Therefore the
partition coefficient is $\eta$-independent, and applying the same balance with
only the released energy $E(\eta)$ substituted for the total $E$ gives

$$v(\eta) = \sqrt{2E(\eta)}\,\Big(\tfrac{M}{C}+\tfrac12\Big)^{-1/2}
\qquad\Longrightarrow\qquad
f(\eta) \;\equiv\; \frac{v(\eta)}{V_0} \;=\; \sqrt{\frac{E(\eta)}{E}} . \qquad (2)$$

**This is the derivation's main result about $M/C$: $f$ carries no $M/C$
dependence at all** — it cancels identically between numerator and denominator.
$M/C$ survives only in the *timescale* $t(\eta)$, which the Mott step never
uses (it uses a strain *rate* at a *radius*). This is consistent with
Martineau's data, where the measured acceleration time doubles from
$M/C=0.498$ to $1.02$ while the velocity approaches the same fraction of its
own Gurney value. It also means the $M/C = 5$–7.5 registry extrapolation
flagged in scoping §3 is **not an extrapolation of $f$** — only of eq. (1),
which is already validated at $M/C\approx7$ against Tolch (864.4 vs 838.2 m/s,
1.03×).

## 2. Released energy under a constant-$\gamma_g$ isentrope

Detonation products expanding along $p V^{\gamma_g} = \text{const}$ from the CJ
state do $pV$ work; the internal energy of a polytropic gas is $e = pV/(\gamma_g-1)$,
so the work done expanding from $V_1$ to $V = \eta V_1$ is

$$W(\eta) = \int_{V_1}^{\eta V_1}\! p\,dV
= \frac{p_1V_1}{\gamma_g-1}\Big[1-\eta^{-(\gamma_g-1)}\Big]
= e_1\Big[1-\eta^{-(\gamma_g-1)}\Big], \qquad (3)$$

and $W(\infty) = e_1$, i.e. the Gurney energy $E$ is identified with the full
isentropic work $e_1$ available to the products. Hence

$$\boxed{\;\frac{E(\eta)}{E} = 1-\eta^{-(\gamma_g-1)},
\qquad f(\eta) = \sqrt{1-\eta^{-(\gamma_g-1)}}\;} \qquad (4)$$

which is exactly the form scoping §4 Option 1 anticipated. Two things earn it
its keep beyond that: eq. (2) shows the $M/C$-independence is *derived*, not
assumed; and Kennedy's Appendix B independently states the same physical
picture in the same variable — the WONDY calculations used "detonation product
isentropes represented by the constant $\gamma$ law, where $\gamma$ is the
polytropic gas exponent" and $Q = D^2/2(\gamma-1)$
(`doc-reference/fragmentation/kennedy1970-gurney-energy/source.md`, Appendix B,
grep anchor `"constant 7 law"` — the extraction renders $\gamma$ as `7`).

### 2.1 Unit / dimensional check

$W$: $[p][V] = $ Pa·m³ = J. $E$ per unit mass in `gurney_velocity` is
$\sqrt{2E}$ in m/s, so eq. (2)'s ratio $E(\eta)/E$ is **dimensionless** and $f$
is dimensionless — the correction is a pure multiplier on a velocity, which is
what the $x_0$ step needs. $\eta$ is a volume ratio, dimensionless.
$\dot\varepsilon_{bu} = f V_0/r_{bu}$: (m/s)/m = s⁻¹. ✔

______________________________________________________________________

## 3. Which radius $\eta$ is taken over (bookkeeping, made explicit)

`_shell_geometry` (`src/arty/fragmentation.py:315`) is already unambiguous on
this and it matches eq. (4)'s requirement:

```
r_inner_bu = r_inner * sqrt(3)                                   # cavity
r_outer_bu = sqrt(r_inner_bu**2 + (r_outer**2 - r_inner**2))     # wall vol. conserved
r_bu       = 0.5 * (r_inner_bu + r_outer_bu)                     # mid-wall
```

- **$\eta$ is the gas-cavity volume ratio**:
    $\eta = (r_{i,bu}/r_i)^2 = 3$ **exactly**, by construction of the code, per
    unit length of cylinder. This is the ratio eq. (3) integrates over (it is the
    volume the products occupy) and it is Mott's $\sqrt3$ break-up strain.
- The registry's **1.79–1.83 is $r_{bu}/r_i$ — mid-wall-at-break-up over
    original *inner* radius**, a mixed ratio that is not an expansion ratio of
    anything. Squaring it (3.2–3.35) does not give $\eta$; it is larger than 3
    only because the numerator is a mid-wall radius and the denominator a cavity
    radius. **Using it as $\eta$ would be a bookkeeping error**, which is why
    scoping demanded this paragraph.
- If one instead defined $\eta_{wall} = (r_{bu}/r_{mean})^2$ with
    $r_{mean}=(r_o+r_i)/2$ — a defensible alternative reading of "how far has
    the case moved" — the values are tabulated in §5 and shift $f$ by well under
    1 %, confirming scoping's "bookkeeping, not physics". **Adopt the cavity
    definition**: it is the one eq. (3) is written over, and it is the one for
    which $\eta_{bu}=3$ exactly.

$r_{bu}$ itself (mid-wall) stays as the radius in $x_0$ — it is the radius of
the *material* whose hoop strain rate is wanted. The two radii play different
roles and both are correct in their place.

______________________________________________________________________

## 4. Limit and bracket checks

All numbers from [`checks/f-breakup-limits.py`](checks/f-breakup-limits.py).

**Analytic limits.** As $\eta\to1^+$, $\eta^{-(\gamma_g-1)}\to1$ so $f\to0$: no
expansion, no work, no velocity — computed $f(1.0001)=0.0141$, $f(1.01)=0.140$
at $\gamma_g=3$. ✔ As $\eta\to\infty$, $f\to1$ from below monotonically:
$f(100)=0.9999$, $f(10^4)=1.000000$. ✔ $f$ is monotone increasing in $\eta$ and
in $\gamma_g$ (larger $\gamma_g$ = stiffer isentrope = more work done early).

**Kennedy's bracket — the falsifiable test.** Kennedy states acceleration is
*complete* at $\eta=7$ (grazing) and at $\eta=2$ (normal). Eq. (4) is not fitted
to either number, so what it returns there is a real test:

| $\gamma_g$ | $f(2)$ | $f(2.7)$ | $f(3)$ | $f(5)$ | $f(7)$ | $1-f(7)$ |
| ---------: | -----: | -------: | -----: | -----: | -----: | -------: |
| 3.0 | 0.8660 | 0.9289 | **0.9428** | 0.9798 | 0.9897 | 1.0 % |
| 2.8 | 0.8443 | 0.9125 | 0.9282 | 0.9720 | 0.9848 | 1.5 % |
| 2.5 | 0.8040 | 0.8801 | **0.8986** | 0.9542 | 0.9726 | 2.7 % |

- **$f(7) = 0.973$–0.990 — within 1–3 % of unity.** "Acceleration complete at
    $\eta=7$" is reproduced, not imposed. **PASS.**
- **$f(2) = 0.804$–0.866 — 13–20 % short.** Clearly \<1. **PASS** on the
    "not by $\eta=2$" half.
- **Residual tension, and it is informative.** Kennedy's *normal*-incidence
    statement ("essentially final velocity by $\eta=2$", Kury et al.) is *not*
    reproduced — eq. (4) says only 87 % there. Kennedy's Appendix B explains the
    same gap in his own WONDY runs and gives the reason: the constant-$\gamma$
    law over-predicts late-time plate velocity by ~10 % because real $\gamma$
    "drops off sharply at $V/V_0 = 3$ to 5 … the effect of retaining most of the
    remaining internal energy in the gases rather than transferring it to the
    metal" (`source.md`, grep anchor `"drops off sharply at"`). His remedy was
    to declare the velocity at $\eta = 2.7$ to *be* the final velocity — and eq.
    (4) at $\eta=2.7$ returns 0.929, i.e. the same ~7 % deficit he absorbed by
    renormalising. So the constant-$\gamma_g$ form is a **lower bound** on $f$
    near $\eta=3$, by a known and small amount.

**Self-consistency variant (upper bound).** Kennedy's calibration means the
empirical Gurney energy $E$ (the shipped $\sqrt{2E}=2440$ m/s for TNT) is
*defined* as the energy delivered by the completion ratio, not by $\eta\to\infty$.
Normalising eq. (3) on $W(\eta_f)$ instead of $W(\infty)$ gives
$f=\sqrt{(1-\eta^{-(\gamma_g-1)})/(1-\eta_f^{-(\gamma_g-1)})}$, and with
$\eta_f=7$ (grazing):

| $\gamma_g$ | $f(2)$ | $f(3)$ | $f(7)$ |
| ---------: | -----: | -----: | -----: |
| 3.0 | 0.8750 | **0.9526** | 1 (by construction) |
| 2.5 | 0.8266 | **0.9239** | 1 (by construction) |

At $\eta_f=2$ (normal incidence) this variant returns $f=1$ for all $\eta\ge2$ —
**no correction at all**, exactly the sanity limit scoping §2 asked for. That
the normal-incidence case self-cancels is the strongest structural check here:
$f<1$ exists in this model *only* because an artillery shell is grazing-driven.

## 5. Adopted value

The two corrections to the plain form act in **opposite** directions and
substantially cancel: a lower effective $\gamma_g$ over the expansion pushes $f$
down (0.943 → 0.899), while the finite completion ratio in the denominator
pushes it up (0.943 → 0.953). Their span is the honest uncertainty:

$$\boxed{\;f(\eta_{bu}=3) = 0.94,\qquad \text{band } 0.90\text{–}0.95,
\qquad f^2 = 0.885\ \ (0.81\text{–}0.91)\;}$$

Implement the plain form eq. (4) with $\gamma_g=3$ (giving 0.9428): it is the
simplest closed form, $\gamma_g\approx3$ is the conventional near-CJ value for
TNT/Comp B products (and is the exponent implied by Kennedy's own
$Q=D^2/2(\gamma-1)$), and it sits near the middle of the band the two
corrections bracket. The band half-width (±0.025) is **inside** scoping's
fidelity target of ±0.05 absolute on $f$. ✔

Equivalent strain rate, 75 mm M48: $\dot\varepsilon_{bu} = f V_0/r_{bu}
= 0.943\times864.4/0.05639 = 1.45\times10^{4}$ s⁻¹, against $1.53\times10^{4}$
s⁻¹ at $f=1$ — both squarely in the range where a dynamic $\sigma_f$ of 800 MPa
is appropriate, so the correction does **not** invalidate the shipped
$\sigma_f$.

### 5.1 $\eta$ bookkeeping across the registry (§3 made numerical)

| shell | $r_i$ [mm] | $r_{bu}$ [mm] | $r_{bu}/r_i$ | $\eta_{gas}$ | $\eta_{wall}$ | $f(\eta_{gas})$ | $f(\eta_{wall})$ |
| :---- | ---------: | ------------: | -----------: | -----------: | ------------: | --------------: | ---------------: |
| 75 mm M48 | 31.50 | 56.39 | 1.790 | 3.000 | 2.672 | 0.9428 | 0.9273 |
| 105 mm M1 | 43.29 | 77.82 | 1.798 | 3.000 | 2.640 | 0.9428 | 0.9255 |
| 155 mm M107 | 63.21 | 113.90 | 1.802 | 3.000 | 2.621 | 0.9428 | 0.9243 |
| 60 mm M49A2 | 22.89 | 41.88 | 1.830 | 3.000 | 2.509 | 0.9428 | 0.9171 |

$\eta_{gas}=3$ for every shell **by construction** — `_shell_geometry` sets
$r_{i,bu}=\sqrt3\,r_i$, so $f$ is a single constant across the registry, not a
per-shell quantity. The alternative wall reading gives $\eta_{wall}=2.51$–2.67
and $f=0.917$–0.927, i.e. **1.6–2.7 % below** the adopted value and inside the
band of §5 — confirming scoping's "bookkeeping, not physics", and confirming
also that the registry's 1.79–1.83 must *not* be squared into an $\eta$
(that would give 3.20–3.35 and $f=0.947$, an error of the same size but in the
opposite direction, from a ratio of two different radii).

______________________________________________________________________

## 6. Double-count check (scoping §5 gate zero)

The double-count signature would be: $N$ moves toward Tolch while the predicted
**mean fragment mass** $2\mu$ moves *away* from his recovered spectrum. Since
$\mu\propto f^{-2}$ and $N_0\propto f^{2}$, applying $f<1$ makes fragments
**heavier and fewer** — and the shipped model's fragments are already far too
light against the pit census:

| $f$ | $2\mu$ [g] | Tolch recovered mean / model | $N_0$ |
| --: | ---------: | ---------------------------: | ----: |
| 1.000 | 1.651 | 4.48× | 3016 |
| 0.943 | 1.858 | 3.98× | 2681 |
| 0.899 | 2.045 | 3.62× | 2435 |

Tolch: 779 pit-recovered fragments, mean **7.40 g** (`tables/pit-screen-recovery.csv`,
via count-chain §2). **The check passes: $f<1$ improves the count *and* the mean
mass simultaneously**, closing ~11 % of the mean-mass gap while removing ~9 % of
the count. No double-count signature. (The 4× mean-mass gap itself is not a
measure of model error — 779 recovered of ~5000 events is a size-screened
census, biased heavily high against a full Mott mean. Only the *sign* of the
movement is admissible evidence here, and it is favourable.)

**The residual risk scoping flagged is real and must be reported, not closed.**
$\mu\propto\sigma_f/(\gamma' V^2)$, so $f$ enters $\mu$ **degenerately with
$\gamma'$**: the $\gamma'$ that would reproduce the same $\mu$ with $f=1$ is
$\gamma'_{eq} = 54.5\,f^2 = 48.5$ (at $f=0.943$) or $44.0$ (at $f=0.899$).
**Both are inside Mott's tabulated 42–67 span.** Consequences:

1. The correction is *not independently observable* — it is indistinguishable
    from a within-table shift of a semi-empirical constant, consistent with the
    known result that only $R=\sigma_f/\gamma'$ is identifiable in this model.
2. Therefore the case for applying it rests **entirely** on the source-definition
    argument (Gold 2017: $V$ is "the velocity with which the shell is moving
    outwards" *at the instant of fracture*; PAFRAG supplies it from a hydrocode
    at break-up time), **not** on the count improvement. That argument is sound
    and is the reason to proceed.
3. It also means the correction **cannot be cited as an independent validation
    win.** If the carbon-content $\gamma'$ table were itself calibrated against
    terminal velocities (unestablished — see A5 below), applying $f$ on top is a
    re-anchoring of $\gamma'$ in disguise. This is a *reporting* constraint on
    the count-chain verdict, and it must be carried into `_limitations.qmd` when
    the implementation pass lands.

______________________________________________________________________

## 7. Assumptions logged (not derived)

- **A1 — $\eta_{bu}=3$ fixed for all shells.** Mott/Linfoot 1943 warn "thick
    cased shells expand further than thin ones before breaking up"
    (`mott-linfoot-1943-theory-of-fragmentation/quotes.md`, grep anchor
    `"thick cased shells expand further"`). Not modelled. Leverage is small:
    $\partial f/\partial\eta = \eta^{-3}/f = 0.039$ per unit $\eta$ at
    $\eta=3,\gamma_g=3$, so even $\eta_{bu}=4$ moves $f$ only to 0.968 (+2.7 %),
    at the top edge of the §5 band.
- **A2 — grazing incidence for every registry shell.** Base-fuzed and
    nose-fuzed HE shells both have an axially sweeping detonation front. A
    normal-incidence configuration would give $f=1$ (§4, self-consistency
    variant at $\eta_f=2$); no registry shell is that geometry.
- **A3 — no $M/C$ dependence in $f$ beyond the energy balance.** §1 eq. (2)
    shows the balance supplies *none*: the partition coefficient cancels. This is
    a derived result, but it rests on Gurney's linear-profile assumption holding
    at intermediate $\eta$, which is an assumption.
- **A4 — constant $\gamma_g$ over the expansion.** Known false (Kennedy,
    Appendix B: $\gamma$ falls sharply at $\eta=3$–5). Its effect is bounded by
    §4's two variants and absorbed into the 0.90–0.95 band, not modelled.
- **A5 — the velocity basis of the tabulated $\gamma'$ is not established.**
    Gold 2017 defines $V$ at fracture and PAFRAG supplies it from a hydrocode,
    but Mott/Linfoot's own 1943 worked example pairs the burst radius with the
    *terminal* fragment velocity ("For $r$ we take 2.2 inches, and for $V$, the
    velocity of the fragments, 2500 ft/sec"). §6 item 3 is the consequence.
- **A6 — unvalidated against measurement.** No measured $v(\eta)$ anchors this.
    Martineau 1998 Figs. 5.5/5.6 ($r(t)$) would supply one at $M/C\approx0.5$–1;
    they are not extracted (scoping §6 item 2, an optional @librarian ask). §1's
    $M/C$-cancellation is what makes that a *validation*, not a prerequisite.
- **A7 — fragments are still gas-driven after break-up.** Terminal $V_0$ stays
    in `gurney_velocity` and `min_lethal_mass`; only $x_0$ sees $f V_0$. Two
    instants, one model (scoping §1).

______________________________________________________________________

## 8. Effect on the count arm — does it clear 2×?

75 mm M48 HE, SPF-S $\eta=\tfrac12$ plug-shear central row, denominator 779
(reproduces count-chain's published 2.47× exactly at $f=1$):

| $f$ | $\mu$ [g] | $N_0$ | $m_{thr}$ [g] | $N$ | $N/779$ | realised leverage | $f^2$ |
| --: | --------: | ----: | ------------: | --: | ------: | ----------------: | ----: |
| 1.000 (shipped) | 0.826 | 3016 | 0.1663 | 1925 | **2.47×** | — | — |
| 0.953 (upper) | 0.910 | 2737 | 0.1663 | 1784 | **2.29×** | 1.079× | 1.103 |
| **0.943 (adopted)** | 0.929 | 2681 | 0.1663 | 1756 | **2.25×** | 1.096× | 1.125 |
| 0.899 (lower) | 1.022 | 2435 | 0.1663 | 1627 | **2.09×** | 1.183× | 1.237 |
| 0.800 (retired) | 1.290 | 1930 | 0.1663 | 1348 | 1.73× | 1.428× | 1.563 |

**$N$ does not scale as $f^2$** — and this matters, because scoping's estimate
assumed it did. $N = N_0\exp(-\sqrt{m_{thr}/\mu})$ with $N_0\propto f^2$ and
$\mu\propto f^{-2}$: the rising $\mu$ *raises* the survival factor, partly
offsetting the falling $N_0$. Realised leverage at $f=0.943$ is **1.096×**, not
$1/f^2 = 1.125\times$ — about 22 % of the intended correction is eaten back.
$m_{thr}$ is unchanged, as it must be (it depends on terminal $V_0$, untouched).

**Verdict: the count arm does not clear the within-2× band.**
$2.47\times \to 2.25\times$ at the adopted $f$, and $2.09\times$ even at the
band's most favourable edge. Scoping §5's prediction (2.0–2.2×) is **confirmed
and slightly corrected upward** — the true post-fix range is **2.09–2.29×**, all
of it outside 2×. C2 is a correct, cheap, direction-right fix that moves the
residual by ~9 % and **does not change the FAIL verdict**. The threshold/spectrum
arm (count-chain C1/C3) remains the deciding term, and the over-correcting
$f=0.7$–0.8 rows should be retired from the thread's framing: no source read in
this scope or in scoping supports $f<0.90$.

______________________________________________________________________

## 9. What the implementation pass must do

One new function in `src/arty/fragmentation.py`, e.g.
`breakup_velocity_fraction(eta_bu=3.0, gamma_g=3.0) -> float` returning eq. (4),
consumed **only** in `mott_params`'s $x_0$ (i.e. `mott_params` forms
`v_bu = f * V0` internally, or takes `f` as a keyword defaulting to eq. (4)).
Do **not** name the argument `gamma` (§0). Terminal `gurney_velocity` and
`min_lethal_mass` are untouched. No re-fit of $\gamma'$, $\sigma_f$, $A$,
$\kappa_x$. Expected shipped movement: $N_0 \times 0.889$, $2\mu \times 1.125$,
75 mm count arm $2.47\times\to2.25\times$. §6's degeneracy note and A1–A7 go to
`_limitations.qmd`.
