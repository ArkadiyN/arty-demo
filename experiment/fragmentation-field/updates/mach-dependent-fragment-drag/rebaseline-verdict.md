# Re-baseline verdict — `updates/mach-dependent-fragment-drag/`

**Pass type.** Correctness / re-baseline assessment. Nothing outside this file
is changed.

**Two independent shocks, ruled on separately (they are not netted).**

- **Shock A — the `B(r)` gap this update was spawned to close is void.**
    `challenges/drag-gap-1944/b-vs-range-rebaseline.md` shows the Family-B
    FAIL was against the mild-steel-perforation column while the model ran the
    58 ft-lb casualty criterion. Against the genuine casualties columns Family B
    passes 8/10, 9/11, 11/11 and the residual *inverts* sign with range.
- **Shock B — the curve against which the Mach-dependent law was rejected was
    wrong.** `figure-3-digitized.md` under-states $C_D$ by up to 0.082 across
    Mach 1.0–2.2; the closure-checked replacement is
    `doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/figure-3-drag-coefficient.csv`.

Shock A removes a *motive* for changing the drag law. Shock B changes the
*evidence* on which one candidate law was rejected. They are ruled on
independently below.

---

## Claim register

**Summary.** 15 claims ruled: **8 sound, 4 shifted, 3 void**. The one
consequential ruling is C11 — the *stated reason* for rejecting the
Mach-dependent law is void (it does beat a constant, once both are given the
same scale freedom), while the *decision* to reject survives on a different
ground (both laws sit inside the ±10% fidelity bar; only the architectural cost
still discriminates).

| # | Claim | Where | Ruling |
| --- | --- | --- | --- |
| C1 | Motive: Family B over-predicts *B(r)* 7–34×, growing with range; cause localises to drag | scoping §1 | **void** (Shock A) |
| C2 | Identity (4) $C_{shape}=(\rho_{steel}/k)^{2/3}$ | deriv §1 | **sound** |
| C3 | Cube/sphere inversion recovers $\rho_{steel}$ to 0.2% | deriv §3 | **sound** |
| C4 | Admissible envelope: combined ≥ 1.31; 0.585 is geometrically impossible | scoping §2, deriv §3 | **sound** |
| C5 | $C_D$ = 1.28 supersonic plateau, 1.08 subsonic, 1.40 transonic peak | scoping §2, deriv §2 | **sound** (Shock B confirms) |
| C6 | V1 — $L_1$ = 241.2 m/kg^{1/3} vs source 247 | deriv §4 | **sound** (Shock B changes nothing) |
| C7 | V2 — RMS(M>0.7) 0.710 → 0.092, PASS against ≤ 0.10 | deriv §4 | **shifted** |
| C8 | Best-fit constants bracket DoD *k* = 2.60 from independent data | scoping §3a | **shifted** |
| C9 | V3 — 155mm far-field lethal count cut ~3× | deriv §4 | **sound** |
| C10 | Adopt combined 2.674 (Option 1) | scoping §5, deriv §2 | **sound** |
| C11 | "Mach dependence buys nothing / does not beat a constant" | scoping §3a-2, §4 opt 3, deriv §5 | **void** |
| C12 | Decision: do not implement a Mach-dependent law | scoping §4, deriv §6 | **shifted** (survives, new reason) |
| C13 | L1 — Tolch over-predicts ~4–6×, not attributable to drag | deriv §7 | **sound** |
| C14 | L2 — sub-M-0.7 tail unclosed; not gravity | deriv §7 | **sound** |
| C15 | L3 — "does not close drag-gap-1944"; ≤10% headroom above 2.674 | deriv §7 | **void** (number survives, reason does not) |

---

### Shock A — the *B(r)* motive (C1, C15)

**C1 — void.** `challenges/drag-gap-1944/b-vs-range-rebaseline.md` is taken as
given: the 7–34× FAIL was the model's 58 ft-lb casualty criterion compared
against the mild-steel-perforation column. Against the genuine casualties
columns Family B passes 8/10, 9/11, 11/11 and the residual *inverts* sign with
range. Both halves of C1 die: the magnitude and the "grows with range" trend
which was the specific signature pointing at drag.

**What C1's death does *not* do — it does not resurrect 0.585.** The pre-update
constant's published *B(r)* over-prediction was 7–34× against perforation. In
the range band where the two columns share an r-grid (20–100 ft, all three
shells) the genuine casualties values run **1.2–2.25×** the perforation values
(read directly off the rebaseline tables: 75mm ≈ 2.0–2.25× at every row, 105mm
and 155mm 1.2–1.9× rising with range), so the same comparison against the
correct column would put pre-update drag at roughly **3–28×** — still a
several-fold, one-directional FAIL on every shell. Shock A removes the
*evidence that
localised the defect to drag*; it does not supply evidence that 0.585 was
right. The case for changing the constant now rests entirely on C4 and C7,
both of which are independent of *B(r)*.

**C15 — void as stated; the residual claim it makes is now backwards.** L3
says the update "delivers a ~3× far-field reduction against a 7–34× *B(r)*
over-prediction". The 7–34× is void, and the rebaseline was run *at the
adopted v0.9.0 drag* — so the correct statement is the inverse: with this
change in place, Family B passes at nearly every tabulated range on all three
shells, and the surviving residual is *sign-changing* (over-predicting inside
~150 ft, under-predicting beyond ~250 ft), not a one-directional miss awaiting
attribution. L3's instruction "the residual must be attributed elsewhere, not
to further drag increases" reaches the right answer for a now-wrong reason: the
long-range residual is an **under**-prediction, which more drag would worsen.

L3's second sentence is separately defective. "The geometric envelope leaves at
most another ~10% of headroom above 2.67 before the fragment must be denser
than a solid steel cube" inverts the direction of the bound. $C_{shape}$ =
$(\rho_{steel}/k)^{2/3}$ is *decreasing* in *k*: a larger $C_{shape}$ means a
**less** compact fragment, and there is no geometric ceiling at all (a sliver
has arbitrarily small *k*). The sphere bound at 1.209 is a floor, and the
adopted 2.089 already sits above the cube's 1.500. The ~10% figure is
nonetheless roughly right — but as an *empirical* bound from the source's own
tabulated *k* range: the lowest tabulated *k* (demolition bombs, 590 gr/in³ =
2.33 g/cm³, scoping §2) gives $C_{shape}$ = 2.248, combined 2.877, which is
**7.6%** above 2.674. Number survives, justification does not.

---

### The core math — untouched by either shock (C2, C3, C4, C5, C6, C9)

**C2, C3 — sound.** Identity (4) is algebra between two closures for the same
presented area; it consumes no tabulated data and neither shock reaches it.
The cube/sphere inversion (deriv §3) is a check *internal to the source's own*
*k* table and recovers 7846 / 7832 kg/m³ against steel's 7830–7850 — it is a
closure invariant in the sense of `.claude/rules/source-data-fidelity.md`, and
it passes.

**C4 — sound, and it is now the load-bearing leg of the whole update.** The
statement "0.585 implies *k* ≈ 25 400 kg/m³, a fragment 3.2× denser than steel
presenting less area than an equal-mass sphere" is pure geometry plus the
identity. It requires no velocity data, no *B(r)*, no $C_D(M)$ curve and no
$V_0$. With C1 void and C7 weakened (below), this is the only claim in the
update that survives every shock untouched — and on its own it is sufficient to
reject the pre-update constant.

**C5 — sound; Shock B confirms rather than disturbs it.** The closure-checked
`figure-3-drag-coefficient.csv` gives $C_D$(M=0) = 1.079, peak 1.399 at
M = 1.50, $C_D$(M=3) = 1.281, $C_D$(M=5) = 1.280 — the source's own quoted
1.08 / 1.40 / 1.28 to three digits. The digitization error runs in the interior
of the curve (Mach 1.0–2.2), not at the plateau the adopted constant is taken
from.

**C6 — sound.** `checks/mach-law-rebaseline.py` computes $L_1$ = 241.2
m/kg^{1/3} from the source plateau **and** 241.2 from the corrected CSV
asymptote — identical. The 2.4% shortfall against the source's 247 remains an
$\rho_{air}$ convention (1.196 vs 1.225), exactly as deriv §4 V1 argues.

**C9 — sound.** V3 is a pure function of λ and the Mott spectrum; it consumes
no Ordnance table and no $C_D(M)$ curve. Neither shock touches it.

---

### The velocity-decay dataset — which column was it? (C7, C8)

**The original 25-point set was mixed-column, and under-sampled.** Three
independent facts establish this:

- the 105mm series in this thread's scripts is a digit-for-digit match to
    `105mm-m1-perforation-1-8in.csv` — the wrong column (same defect, same
    shell, as the one already on record for
    `challenges/drag-gap-1944/checks/drag-coefficient-calibration.py`);
- the 75mm series used **3 of the 10 available** casualties rows;
- 155mm matched its casualties CSV (spot-checked in
    `b-vs-range-rebaseline.md`, "Not re-examined in this pass").

3 + 11 + 11 = the published n = 25, against n = 32 for the full casualties set
and n = 33 for the full perforation set. So the rejection of the Mach law was
computed on a set that was **~44% wrong-column by point count, with the
remaining 75mm contribution cut to 30% of its rows** — and neither corrected
column reproduces the published RMS (0.864/0.710 at 0.585, against 0.967/0.755
casualties and 0.679/0.679 perforation), which is itself the signature of a
mixture.

**The mixture also corrupted the "lethal-relevant band" cut.** All 33
perforation rows have arrival M > 0.7; only 21 of 32 casualties rows do. The
M > 0.7 subset is therefore *preferentially* populated by wrong-column rows —
the published "n = 20 of 25" band was built from the column selected by the
harder mild-steel-perforation threshold while the model ran the 58 ft-lb
casualty criterion. This is the criterion-match failure named in
`.claude/rules/source-data-fidelity.md`, not merely a transcription slip.

FINDING[note]: the mixed-column 25-point Ordnance velocity set is discharged in the documents — derivation.md §4 V2 now publishes the per-column re-run and §5 is withdrawn — but checks/required-retardation-vs-mach.py still carries the mixed array as a hard-coded literal; it is retained as the record of what was run, so read it as a record and never as a live series (affects: experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/required-retardation-vs-mach.py; since: 2026-08-03)

**C7 — shifted; the PASS survives, on either column separately, but narrowly.**
Re-run cleanly per column (`checks/mach-law-rebaseline.py`):

| Combined $C_D C_{shape}$ | casualties, all (n=32) | casualties, M>0.7 (n=21) | perforation, all = M>0.7 (n=33) |
| --- | --- | --- | --- |
| 0.585 (pre-update) | 0.967 | 0.755 (≈ 2.1× error) | 0.679 |
| **2.674 (adopted)** | 0.405 | **0.096** (10.1%) | **0.098** (10.3%) |
| published (mixed set) | 0.349 | 0.092 | — |

The V2 bar was RMS(M > 0.7) ≤ 0.10. It passes on the casualties column at
0.096 and on the perforation column at 0.098 — a *stronger* result than the
published one in kind (it now holds on each criterion separately rather than on
a mixture) but weaker in margin (4% under the bar, not 8%). The conclusion
"0.585 fails by ~2× in the lethal band, 2.674 lands inside ±10%" is unchanged.

**C8 — shifted.** The best-fit constants move from the published 2.20 (all) /
2.94 (M>0.7) to 2.140 / 2.875 on casualties and 2.985 / 2.985 on perforation.
Inverted through identity (4) at $C_D$ = 1.28 these still bracket the DoD
recommended *k* = 2.60 g/cm³, so the corroboration stands; the bracket is
simply wider and its upper end now sits at the top of the admissible envelope.

**$V_0$ is unverified, and it is the term this whole comparison is most
exposed to.** `V0_FTS` (75mm 3120, 105mm 3500, 155mm 3500 ft/s) is used by
every prior script in this thread and is **not present in the processed
Ordnance source** — it was carried over without provenance. Its role is
structural, not incidental: the residual is
$\ln(v_{model}/v_{src}) = \ln V_0 - \lambda r - \ln v_{src}$, so an error
$\delta$ in $\ln V_0$ adds a **constant** $\delta$ to every residual of that
shell, which a fit absorbs by tilting λ. Consequences, in order of severity:

1. A 10% $V_0$ error is $\delta$ = 0.095 — **comparable to the entire 0.096
    RMS** at the adopted constant. The V2 PASS margin is therefore not
    established as robust to it, on either column.
1. It is **degenerate with the drag constant itself**: on the perforation
    column the corrected Fig-3 residual is a uniform +0.058 bias absorbed by a
    single scale of 1.10 on $C_{shape}$ — arithmetically indistinguishable from
    a 10% error in $\ln V_0$. Any "best-fit constant" from this data is really
    a fit to $(\lambda, V_0)$ with one of them assumed.
1. It does **not** reach the shipped parameter. 2.674 is *derived* from
    identity (4) at DoD's *k* = 2600, not fitted to this data; V2 is
    corroboration. C10 therefore survives (below) — but the corroboration is
    softer than the derivation presents it.
1. It is **not** the explanation for L2. A $\ln V_0$ error shifts required λ by
    $\delta/r$, i.e. most at *short* range; L2's anomaly is a *depressed*
    required constant at *long* range. Wrong shape.

FINDING[deferrable]: V0_FTS (75mm 3120, 105mm 3500, 155mm 3500 ft/s) is used by every check script in this thread but has no provenance in the processed 1944 Ordnance source; it is degenerate with the drag constant and the V2 PASS margin (0.096 vs a 0.10 bar) is inside its plausible error (affects: experiment/fragmentation-field/updates/mach-dependent-fragment-drag/derivation.md, experiment/fragmentation-field/updates/mach-dependent-fragment-drag/checks/, experiment/fragmentation-field/challenges/drag-gap-1944/checks/; since: 2026-08-03)

---

### Shock B — the rejection of the Mach-dependent law (C11, C12)

This is the consequential ruling. Both inputs to the comparison have changed:
the $C_D(M)$ curve (Shock B proper) and the dataset it was scored on (the
mixed-column defect above).

**The published comparison was not like-for-like.** It pitted the Fig-3 curve
at the *derived* $k$ = 2600 — **zero free parameters** — against a constant
*fitted to the same data* — **one free parameter** — and reported that the
constant won (0.250 vs 0.259 all; 0.047 vs 0.072 on M > 0.7). Note that even in
the published table, Fig-3 at fixed $k$ beat every *non-fitted* constant,
including the adopted one (0.072 vs 0.092). Giving both laws the same single
scale freedom on $C_{shape}$ reverses the result on **both** columns:

| Law (one free scale each) | casualties, all | casualties, M>0.7 | perforation |
| --- | --- | --- | --- |
| best-fit **constant** | 0.247 | 0.069 (7.1%) | 0.045 (4.6%) |
| **Fig-3 $C_D(M)$, corrected CSV** | **0.199** | **0.052** (5.3%) | **0.036** (3.7%) |
| Fig-3 at derived *k* = 2600, no fit | 0.308 | 0.068 | 0.069 |

A consistent **~20–25% RMS reduction** for the Mach law, on both columns, in
both bands. And on the casualties column in the lethal band the Mach law with
*no* fitted parameter (0.068) already ties the best *fitted* constant (0.069).

**Shock B alone moves it in the predicted direction.** Old eyeballed curve →
corrected CSV improves the Mach law from 0.075 → 0.068 (casualties, M > 0.7)
and 0.077 → 0.069 (perforation). The registered open finding was right that the
digitization error "runs in the direction that weakens the rejected candidate";
the effect is real but ~10%, i.e. it is the like-for-like framing, not the
curve error, that carries most of the reversal.

**C11 — void.** "Mach dependence buys nothing", "does not beat a constant",
"the challenge's surviving velocity-dependent hypothesis is not supported"
(scoping §3a-2, §4 Option 3, deriv §5) are all contradicted on the corrected
inputs. It buys ~20–25% of RMS at equal parameter cost. The supporting appeal
to the source's own line 338 ("a useful approximation … constant at its
supersonic value") is still a fair reading of the *source*, but it was
presented as *numerically confirmed on this data*, and it is not.

**C12 — shifted: the decision survives, the reason must be replaced.** Two
legs supported Option 3's rejection. Leg (a), negative accuracy return, is
void with C11. Leg (b), the architectural cost, is untouched — and it now has
to carry the decision alone, against a *positive* return. The defensible
restatement:

> Both laws land inside the ±10% arrival-velocity fidelity bar over the
> lethal-relevant band (constant 7.1%, Mach-dependent 5.3% on the casualties
> column). The Mach law is genuinely more accurate, by ~1.8 percentage points
> of velocity error, and that difference is below the aspect's own materiality
> threshold — while the change replaces a closed-form λ with a per-fragment ODE
> integration. Rejected as **immaterial at the stated fidelity target**, not as
> unsupported by the data.

That is a logged-assumption closure, and it is the right one: the discriminating
quantity is the lethal-fragment count vs range, and a 1.8-point velocity
difference inside a band where both laws already meet the bar cannot move it
enough to matter. But the update must not keep publishing the *accuracy* claim,
because a future reader re-opening this on better data will find the stated
premise false and the decision correct.

**Conditional on shipped code.** Leg (b)'s weight depends on a fact this pass
did not verify (`src/arty/` deliberately not read): whether λ is still consumed
in closed form — `min_lethal_mass`'s bisection and both field builders — rather
than through an already-numeric path. **The one fact that settles it:** grep
`src/arty/` for uses of `retardation_coeff` and for closed-form
`exp(-lambda * s)` / analytic inversions of it. If any of those call sites has
since become numeric, leg (b) weakens too and C12 should be re-opened rather
than restated.

**Conditional resolved by the main agent, 2026-08-03 — leg (b) holds, and is
stronger than stated.** λ is consumed in closed form at every call site, with
**no** analytic inversion anywhere in `src/arty/`: `retardation_coeff`
(`fragmentation.py:333`) is called at `:406`, `:470`, `:503`, `:1526`, `:1547`
and `plots.py:90`, and every consumer evaluates `V0 * np.exp(-lam * s)` —
`:380`, `:473`, `:506`, `:596`, `:1117`, `:1210`, `:1551`. `np.log` appears
nowhere in the module, so nothing inverts λ analytically either. The site that
matters most for leg (b) is `:1210`, where the field kernel evaluates
`lam[None, :] * s_c[:, None]` — a single broadcast outer product over the whole
mass × standoff grid. A Mach-dependent $C_D$ cannot be substituted there: $C_D$
would depend on the instantaneous $v$, so the one vectorised exponential becomes
a per-fragment, per-standoff ODE march. So leg (b) is not merely "untouched",
it is the dominant cost, and C12's **shifted** ruling stands on it.

---

### The adopted constant and the limitations (C10, C13, C14)

**C10 — sound.** Adopting combined 2.674 survives both shocks, but its support
has been re-weighted and this should be recorded: it is now carried by C4
(geometric admissibility — 0.585 is impossible, independent of every dataset)
and by the source's own recommended $k$ = 2600 through identity (4). C7 remains
corroborating and still passes on each column separately, but at a 4% margin
and with a $V_0$ exposure comparable to the whole residual. C1's death removes
one motive; no shock supplies any evidence *for* the pre-update value.

Note that C11's reversal does **not** argue for a different constant. The Mach
law's advantage is in residual *shape*, not level: its own best scale on
$C_{shape}$ is 1.05 (casualties, M > 0.7) and 1.10 (perforation) — i.e. it
wants the adopted constant to within 5–10%, well inside the $V_0$ degeneracy.

**C13 — sound.** The Tolch limitation is untouched by both shocks: it consumes
neither *B(r)* nor the $C_D(M)$ curve, and its four-part weighing (compound
test, drag-orthogonal count bias, hole-detection cutoff, admissibility) does
not rest on anything that moved. Its reason (iv) — Tolch's preferred ≈1.2 lies
below the sphere floor of 1.31 — is C4, which is the claim that came through
strongest.

**C14 — sound.** The sub-M-0.7 tail is still unclosed on the corrected inputs:
on the casualties column 11 of 32 points fall below M = 0.7, and the corrected
Fig-3 integration's all-points bias is −0.130 with a preferred scale of 0.85
against 1.05 in the lethal band — the two bands still want opposite
corrections, which is the same anomaly L2 records. Gravity remains excluded on
L2's own terminal-velocity argument, which no shock touches. L2's leading
untested candidate (the source's long-range tabulated *m*(*r*) is fixed by its
own lethality criterion and may not be a clean ballistic observable) is now
*more* credible, since the two columns are exactly two different criteria and
they disagree most at long range.

---

### What this pass did not rule

- Whether `challenges/drag-gap-1944/README.md` rows should be rewritten — that
    thread's own bookkeeping, and Shock A's document already carries it.
- Anything in `src/arty/` (not read by instruction). Only C12 depends on a
    shipped-code fact, and it is stated conditionally above with the settling
    grep named.
- The magnitude of the `figure-3-digitized.md` error itself — taken as given
    from the registered finding; this pass consumed only the closure-checked
    CSV.
