# Mass-dependent wood-perforation threshold $E_{thr}(m)$ — derivation

**Aspect:** the perforation criterion behind `min_lethal_mass` /
`build_mmin_table` on the `count-gap-1938` panel arm. Scoping:
[`scoping.md`](scoping.md), Option A.

**Headline: Option A as scoped does not survive its own validation checks.**
The UFC 4-023-07 equation is confirmed from the page image and the algebra is
clean, but inverting it at Tolch's $t$ = 1 in panel puts it ~1.5 decades below
its calibration domain in thickness, and the inversion exponent $1/0.4113$ =
2.431 amplifies that extrapolation into a **ballistic limit of 5.4 m/s** for a
0.63 g fragment — $E_{thr}$ = 9.1 × 10⁻³ J, **four decades** below the two
non-fitted probes (78.6 J, 126 J). Scoping's own check 3 says a result 100×
away is an error, not a discovery; this is 10⁴×, and it is not a units error
(§3). Recommendation in §6: **do not implement Option A**; adopt the areal
(shear-plug) form A′, which is the same mass-dependent generalisation of (1)
with a defensible scale.

All numbers in §§1–6 are produced by
[`checks/ufc-5-1-perforation-threshold.py`](checks/ufc-5-1-perforation-threshold.py)
(`uv run python …`, < 1 s).

> **§7 (2026-08-09) is the pass's final word — read it with §6.** A′ is
> finalised there as **A″**, a plug-shear threshold
> $E_{thr}(m)=\tfrac12\tau\pi D(m)t^2$ with $\tau$ = 8.96 MPa sourced from
> Sanborn 2019 Table 2. Two things in §6 are corrected there: the 78.6 J probe
> may **not** anchor the threshold (§7.1), and §6's areal form **eq. (7) is
> superseded** by §7's eq. (9) — $E_{thr}\propto m^{1/3}$, not $m^{2/3}$
> (§7.2). §§1–5 stand as written.

______________________________________________________________________

## 1. Source equation, verified from the page image

UFC 4-023-07 (7 July 2008) §5-3.4.2.1.1, Equation 5-1 — read directly from
`doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/source.pdf`
p. 40 (printed "5-10"), **not** from Sanborn's transcription:

$$T_w \;=\; 9837\;\frac{v^{0.4113}\,w^{1.4897}}
{\rho \left(\dfrac{\pi D^2}{4}\right)^{1.3596} H^{0.5414}} \qquad (3)$$

| Symbol | Meaning | Unit (as stated) |
| --- | --- | --- |
| $T_w$ | thickness of wood to prevent perforation | in |
| $v$ | impact velocity | ft/s |
| $w$ | projectile weight | lb |
| $D$ | projectile diameter | in |
| $\rho$ | wood density | lb/ft³ |
| $H$ | wood hardness (Table 5-5 scale) | lb |

Confirmed against the image: $\rho$ carries **no** exponent (1.0), $H$ carries
**0.5414**, and the diameter term is the **presented area** $(\pi D^2/4)$ raised
to 1.3596. This vindicates `card.md`'s vision correction of Sanborn's Eq. (2)
($\rho^{0.5414}H^{2}$, $D^{1.3596}$ — wrong on all three).

Eq. 5-2 (residual velocity, $v_r = v[1-(t/T_w)^{0.5735}]$) is not needed: the
perforation criterion is $T_w(v,m) \ge t$, i.e. $v_r > 0$, and Eq. 5-2 vanishes
exactly at that boundary.

### 1.1 Blocking defect: Table 5-5's two columns are swapped downstream

The page image shows the column order **Species | Density (lbs./ft³) |
Hardness (pounds)** — Pine/Dry is $\rho$ = 23.5 lb/ft³, $H$ = 38.7 lb. Both
`card.md` (§"Table 5-5") and `tables/table-5-5-wood-properties.csv` (headers
originally `hardness_pounds,density_lbs_per_ft3`) carried them **reversed**.
This is the column-inversion failure `.claude/rules/source-data-fidelity.md`
exists to prevent. **Correction applied 2026-08-09** (below) fixed the CSV/card
headers in place; the check script originally compensated by reversing the two
fields on read, which became a stale double-swap once the headers were fixed —
caught and corrected 2026-08-10, see `review.md` Finding 1. The script now
reads the CSV directly, with no reversal.

A closure invariant settles it without the image, and the `.invariant` file's
claim that "no closure check is applicable" is wrong: **wet ≥ dry in column 1
on every species** (water adds mass — density) and **wet ≤ dry in column 2 on
every hardwood** (saturated wood is softer — hardness). Both hold; the labels
are what is backwards. Mechanised in the check script.

Sanity of the scale: $H$ = 38.7 lb for dry pine is ~1/10 of the standard Janka
side-hardness (≈ 380–870 lbf). **Do not substitute real Janka values into (3)** —
Eq. 5-1 is a curve fit to the Table 5-5 scale, whatever that scale is.

**Correction applied 2026-08-09:** Table 5-5 column transposition verified and corrected against source.pdf page image (page 40, printed 5-10). card.md and CSV now have density/hardness in correct order; invariant file updated with closure checks.

______________________________________________________________________

## 2. Deriving $E_{thr}(m)$ (Option A as scoped)

Set $T_w = t$ (the panel thickness) in (3) and solve for the impact velocity —
that velocity is the ballistic limit $v_{50}$:

$$v_{50}(m) \;=\;\left[\frac{t\,\rho\,A(m)^{1.3596} H^{0.5414}}
{9837\, w(m)^{1.4897}}\right]^{1/0.4113},\qquad
A(m)=\frac{\pi D(m)^2}{4} \qquad (4)$$

with the compact-fragment closure $D(m) = \bigl(6m/\pi\rho_{s}\bigr)^{1/3}$,
$\rho_s$ = 7850 kg/m³, so $A \propto m^{2/3}$. Then, per scoping (2),

$$E_{thr}(m) \;=\; \tfrac12 m\, v_{50}(m)^2. \qquad (5)$$

**Closed-form exponents** (the whole content of the model). Writing
$v_{50}\propto m^{p}$,

$$p \;=\; \frac{-1.4897 + \tfrac{2}{3}(1.3596)}{0.4113} \;=\; -1.418,
\qquad E_{thr}\propto m^{\,1+2p} \;=\; m^{-1.836}. \qquad (6)$$

Two consequences worth stating before any arithmetic:

- **$E_{thr}$ falls steeply with $m$** — it does *not* rise. Scoping §1's claim
  that "$E_{thr}$ is a rising function of $m$" is a generic-THOR intuition
  (mild-steel THOR gives $v_{50}\propto m^{-0.42}$, $E_{thr}\propto m^{+0.16}$),
  and UFC's wood fit is 3.4× steeper in mass. Under (6) a threshold is
  effectively a **mass floor with an extremely sharp edge**, not a graded
  criterion.
- **The velocity exponent 0.4113 is the fragile term.** It enters (4) as
  $1/0.4113$ = 2.431, so *any* error in $T_w$ — of the equation, or of the
  regime it is used in — is raised to the 2.431 power in $v_{50}$ and to 4.86
  in $E_{thr}$. A 5× thickness bias is a 50× velocity bias and a **2500×**
  energy bias. This sensitivity, not the algebra, is what defeats Option A.

______________________________________________________________________

## 3. Unit checks

(3) is dimensionally inhomogeneous by construction — the source says so:
*"Because the equations are largely curve fits of actual data, they are left in
their original form"* (p. 40, printed 5-9). So the check is **not** dimensional
analysis but strict unit discipline at the call site, and it was done:

- $w$: kg → lb (× 2.20462); $D$: m → in (× 39.3701); $v$: result in ft/s → m/s
  (÷ 3.28084); $t$ = 1 in exactly. Verified in the script's helpers.
- $\rho$, $H$ taken from Table 5-5 **in the source's own units**, after the §1.1
  column repair.
- Independent confirmation that $T_w$ is in **inches, not mm**: reading it as mm
  would make (3) *under*-predict Sanborn's CLT (34.8 mm = 1.37 in vs a 6.875 in
  panel that was perforated), contradicting Sanborn's stated finding that the
  original UFC equation over-predicts required thickness. Inches is the reading
  consistent with both the page and the independent secondary.

A ×2.2 or ×39.4 slip anywhere would move $E_{thr}$ by ~1–2 decades, not 4;
no combination of unit errors produces the 10⁴ gap in §4.3.

______________________________________________________________________

## 4. Validation checks (scoping's list)

### 4.1 Check 1 — closure on the source's own regime — PASS (with a caveat)

Forward evaluation of (3) into dry pine ($\rho$ = 23.5, $H$ = 38.7):

| Case | $T_w$ from (3) |
| --- | --- |
| 7.62×51 M80 ball, 2750 ft/s, 147 gr, 0.308 in | 162.5 in |
| .50 BMG M33 ball, 2910 ft/s, 647 gr, 0.510 in | 383.8 in |
| Sanborn 12.7 mm steel sphere, 2500 ft/s (762 m/s) | 34.8 in |

Order-correct in the sense scoping asked (tens of inches, not 10⁻⁴ in — the
defect §2b flagged in Sanborn's card is gone once the exponents are right). The
caveat is that these are **large**: Sanborn's 5-ply, 6.875 in CLT was perforated
at this velocity, so (3) over-predicts the stopping thickness by roughly **5×**,
which is exactly the over-prediction Sanborn reports and independently
corroborates that the equation is being read correctly *and* that it is
conservative.

### 4.2 Check 2 — monotonicity and limits — PASS on limits, FAILS the expected sign

$t$ = 1 in dry pine, compact steel fragment:

| $m$ [g] | $D$ [mm] | $v_{50}$ [m/s] | $E_{thr}$ [J] |
| --- | --- | --- | --- |
| 0.05 | 2.30 | 195.4 | 9.54 × 10⁻¹ |
| 0.10 | 2.90 | 73.1 | 2.67 × 10⁻¹ |
| 0.63 | 5.35 | 5.37 | 9.10 × 10⁻³ |
| 2.00 | 7.87 | 1.04 | 1.09 × 10⁻³ |
| 10.0 | 13.45 | 0.107 | 5.68 × 10⁻⁵ |
| 50.0 | 23.00 | 0.011 | 2.96 × 10⁻⁶ |

- $v_{50}$ falling in $m$ ✓; $v_{50}\to\infty$ as $m\to0$ ✓.
- $E_{thr}$ **falling** in $m$, per (6) — scoping expected rising. Not a coding
  error: it is what the fitted exponents say.
- The $v_{50}$ values are physically impossible. A 10 g fragment does not
  perforate a 1-inch pine board at 0.1 m/s.

### 4.3 Check 3 — bracket the non-fitted probes — **FAIL by four decades**

$E_{thr}(0.63\ \mathrm{g})$ = **9.1 × 10⁻³ J**, against 78.6 J (ratio 1.2 × 10⁻⁴)
and 126 J (7.2 × 10⁻⁵). Scoping's stated tripwire ("100× away means a units
error") is exceeded by 100×. §3 rules out units. Under (6), $E_{thr}$ only
reaches 78.6 J at $m \approx$ 4.5 mg — i.e. the criterion admits essentially
every recovered fragment and is not a threshold at all.

**Diagnosis — regime, not arithmetic.** Eq. 5-1's calibration domain is
small-arms: $w \approx$ 9–41 g, $D \approx$ 7.6–12.7 mm, $v \approx$ 600–900
m/s, yielding $T_w$ of tens of inches. Tolch's arm needs $t$ = 1 in and
$m$ = 0.1–10 g. Inverting at $t$ = 1 in asks the fit for a thickness ~1.5
decades below anything it saw; because $\partial T_w/\partial v$ is weak
(exponent 0.4113), the velocity that satisfies it collapses by
$30^{2.431}\approx 5\times10^{3}$. **The equation is a design curve for sizing
thick barriers, not a ballistic-limit law for thin panels**, and the 2.431
amplification is what converts that difference in purpose into a four-decade
error.

Applying the Sanborn bias factor $b$ (over-predicted $T_w$) does not rescue it —
it makes the fragility explicit:

| $b$ (thickness) | amplification $b^{2.431}$ | $v_{50}$(0.63 g) | $E_{thr}$(0.63 g) |
| --- | --- | --- | --- |
| 2× | 5.4× | 29.0 m/s | 0.26 J |
| 5× | 50.1× | 269 m/s | 22.8 J |
| 8× | 156.9× | 843 m/s | 224 J |

The probes (78.6–126 J) sit between $b$ = 5 and $b$ = 8. So a *bias-corrected*
Option A can be made to agree with the probes — but only by tuning $b$, i.e. by
reintroducing exactly the free parameter this thread exists to eliminate, and
with a ±50% window on $E_{thr}$ corresponding to a ±9% window on $b$. That is
not a sourced threshold.

**Bias-sign correction to scoping §2a item 2.** Scoping states that an
over-predicted $T_w$ inverts to an *over*-estimated $v_{50}$ and hence an
under-counted $N$. That is backwards. $T_w(v)$ is increasing in $v$; a curve
shifted **up** reaches the panel thickness $t$ at a **lower** $v$. Over-predicted
$T_w$ ⇒ **under**-estimated $v_{50}$ ⇒ under-estimated $E_{thr}$ ⇒
**over**-counted $N$. Direction confirmed numerically by the table above
($b$ increases $v_{50}$, so the uncorrected $b$ = 1 case is the low one). The
UFC route is therefore **anti-conservative** on count, not conservative.

### 4.4 Check 4 — re-run count-chain §4 as a prediction — NOT RUN

Deliberately not run: feeding a threshold that fails check 3 by 10⁴ into the
count arm would produce a meaningless $N$ and, worse, an apparently improved
"prediction with zero free parameters". Deferred until an admissible
$E_{thr}(m)$ exists (§6).

### 4.5 Check 5 — `E_LETH_DEFAULT` regression — discharged by design

No `src/arty/` change is proposed by this pass, so the 1000 J ES-310 personnel
path is untouched by construction. The design constraint for any future
implementation pass stands as scoping wrote it: `min_lethal_mass` /
`build_mmin_table` take a **threshold callable defaulting to the present scalar
compare** (`_ke(m) >= E_LETH_DEFAULT`), so the personnel path, `p_kill`, and all
casualty-area outputs are bit-identical unless a wood-target spec is passed.

______________________________________________________________________

## 5. Assumptions logged

1. Compact-fragment sphere-equivalence $D(m)=(6m/\pi\rho_s)^{1/3}$, $\rho_s$ =
    7850 kg/m³. Real fragments are elongated with a presented area larger than
    the sphere-equivalent at fixed $m$; corroborated as an acceptable proxy for
    softwood at 180–1200 m/s by Sanborn's 122 sphere shots (scoping §2a,
    "does transfer" item 3).
1. Tolch's panel wood is taken as **dry pine** from Table 5-5 ($\rho$ = 23.5,
    $H$ = 38.7). The species is not confirmed from the 1938 report (scoping §3
    item 4). This matters little: $E_{thr}\propto(\rho H^{0.5414})^{4.86}$ under
    (5) — enormous — but under the recommended form A′ it is a weak dependence,
    so confirming the species is *not* a prerequisite for A′.
1. Normal impact, no obliquity, no yaw. Eq. 5-1 carries no obliquity term.
1. Single panel, no back-face/edge effects; the criterion is
    perforation (exit at $v_r \to 0^+$), matching Tolch's counted holes.

______________________________________________________________________

## 6. Verdict and recommendation

**Option A (invert UFC Eq. 5-1 at $t$ = 1 in) is rejected on the evidence**:
checks 2 and 3 fail, the failure is a regime mismatch that no unit fix or
coefficient correction removes, and the only route to agreement (tuning $b$)
restores the free parameter the thread is trying to eliminate. Option B
(constant $E_{thr}$ frozen from the same inversion) inherits the same scale
error and is rejected with it. Option C was already rejected in scoping.

**Recommended: Option A′ — an areal (shear-plug) criterion, mass-dependent,
one sourced anchor.** Perforation of a thin panel by a compact fragment is a
plug-shear/crush process, so the threshold energy scales with the *sheared area*
$\pi D t$ times the plug travel $t$, i.e. with presented area at fixed panel
thickness:

$$E_{thr}(m) \;=\; e_a\,A(m) \;=\; e_a\,\frac{\pi}{4}D(m)^2
\;\propto\; m^{2/3}. \qquad (7)$$

> **SUPERSEDED by §7.2 — do not implement (7).** The step from "sheared area
> $\pi Dt$ × plug travel $t$" to "presented area $A$" does not follow:
> $\pi Dt\cdot t \propto D$, not $D^2$. The plug-shear mechanism gives
> $E_{thr}\propto m^{1/3}$ (§7 eq. 9), and $e_a$ is not a parameter of the
> model. The $e_a$ = 3.5 × 10⁶ J/m² anchored on 78.6 J below is also
> inadmissible on provenance and criterion-match grounds (§7.1).

This is *rising* in $m$ — the behaviour scoping §1 argued for — has one constant,
and is not fragile: an error in $e_a$ passes to $E_{thr}$ at power 1, not 4.86.
Anchoring $e_a$ so that $E_{thr}$(0.63 g) = 78.6 J (the 1944 Ordnance-card probe)
gives $e_a$ = 3.5 × 10⁶ J/m² = 3.5 J/mm². Independent corroboration: a
plug-shear estimate $W = \tau\,\pi D t\cdot t$ with softwood transverse shear
$\tau \approx$ 7–10 MPa gives 75–108 J for the same fragment, i.e.
$e_a \approx$ 3.4–4.8 × 10⁶ J/m² — the same value from unrelated physics.

Two things A′ still needs, and they are the *next* pass, not this one:

- a **sourced** $e_a$ (or a sourced $(m, E)$ pair to anchor it). The 78.6 J
  probe's provenance — the 1944 Ordnance card, and the mass it is stated at —
  must be read before $e_a$ is fixed, or the anchor is circular in the same way
  the 1.9–3.6 J fit was;
- @librarian is likely needed for one softwood transverse-shear / ballistic-limit
  datum if the Ordnance-card mass is not recoverable.

**This changes the option chosen in an approved scoping doc, so it is the
human's/reviewer's call, not mine.** If A′ is judged too much for a confirmation
pass, the fallback is scoping's **Option D** — log the constant-$E$ step as a
limitation, and record §4.3's finding (the only THOR-family wood equation in
`doc-reference/` cannot supply a thin-panel ballistic limit) as the reason the
compound-test objection stays open.

**Fidelity note.** Under A′ the ±50% target on $E_{thr}$ is reachable — $e_a$ is
bounded within ~40% by the two independent estimates above — and the count is
only logarithmically sensitive to it, so the factor-2 count tolerance holds.
Under A it is not: $E_{thr}$ is uncertain by four decades.

______________________________________________________________________

## 7. Finalising A′ — the anchor moves from the 78.6 J probe to a sourced $\tau$

**Added 2026-08-09**, after the human approved §6's recommendation (reject A,
adopt A′) and after a librarian pass reported that the 78.6 J figure is stated
mass-non-specifically in its source. §6 flagged exactly this as A′'s open
prerequisite. It resolves **in A′'s favour, but not by the route §6 expected**:
the anchor is not a sourced $(m,E)$ pair at all, and the areal form (7) is
itself the wrong mechanism. Both are corrected here.

**Verdict: A′ is finalised as A″ below, with $\tau$ = 8.96 MPa sourced from
Sanborn 2019 Table 2. No fallback to Option D, and no @librarian pass needed.**

All §7 numbers come from
[`checks/plug-shear-perforation-threshold.py`](checks/plug-shear-perforation-threshold.py)
(`uv run python …`, < 1 s).

### 7.1 The 78.6 J probe is inadmissible as an anchor — on two independent grounds

*Verified against the source in this pass, not taken from the brief.*

**(a) Mass-non-specific, and demonstrably so.** The source states it as a bare
definition: *"A casualty is supposed caused by a hit with at least 58 ft.-lb. of
energy. It is incapacitation and not necessarily death."*
— quoted verbatim, and greppable as written (1 hit) in
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md`
(line 309; PDF p. 78 / printed p. 64). No mass appears in the sentence, the
paragraph, or the section. Column anchor, 2 hits:
`For the lightest effective Fragment`.

This is **not** a null result over a derived surface — there is *positive*
evidence that the source treats 58 ft-lb as mass-independent. The damage tables'
last two columns are *"For the lightest effective fragment: Weight (oz.),
Velocity (f/s)"*, and the retained CSVs close on the definition at every range:
`tables/105mm-m1-casualties.invariant` carries
`row: 0.5 * (m_oz / 16 / 32.174) * v_fps**2 == 58 within 5%`, and it holds
across $m$ = 0.010 → 0.312 oz (0.28 → 8.8 g) — a **31× mass span** on one shell,
six such tables in the set. The source is applying one constant KE across the
whole fragment spectrum. So 58 ft-lb is not a value *at* 0.63 g; the pairing
with Tolch's finest screen cut is an import from an unrelated document, and
dividing by $A(0.63\ \mathrm{g})$ to obtain $e_a$ has no standing.

**(b) Criterion mismatch — the deeper objection.** 58 ft-lb is a **personnel
incapacitation** threshold. The quantity A′ needs is the **perforation limit of
1 in softwood**. Under `.claude/rules/source-data-fidelity.md` ("criterion
match"), calibrating a wood-perforation constant on a soft-tissue casualty
criterion is a Blocking-class defect however faithful the transcription. This
holds even if a mass *were* attached, so it disposes of the 126 J Tolch
hole-size probe as an anchor too. **Neither probe may set $e_a$.** They are
retained below only as an order-of-magnitude plausibility band, explicitly
labelled mass-non-specific and criterion-mismatched.

*No `card.md` defect.* The card states the threshold exactly as the source does,
attributes it to nothing, and its "Data Sources" section already records that
the source gives no provenance for it. No FINDING is filed against the card.

**But a FINDING is filed downstream.** `_limitations.qmd` (~line 143) and
`challenges/README.md` (~line 55) describe 78.6 J and 126 J as *"sourced
(non-fitted) energy thresholds"* for the **panel-perforation** arm, and rest a
published verdict on them — *"the count arm of the PASS test is now met or
marginal, not failed"*. 78.6 J is sourced, but for **personnel incapacitation**;
using it as a 1-inch-softwood perforation threshold is the criterion mismatch
§7.1(b) identifies, which `.claude/rules/source-data-fidelity.md` classes
Blocking regardless of transcription fidelity. The arithmetic is right; the word
"sourced" is what is not, and it is on a published surface. §7.3 supplies the
criterion-correct replacement, so the fix is available, not merely the diagnosis.


### 7.2 §6's areal form (7) is the wrong mechanism — superseded

§6 wrote "the threshold energy scales with the sheared area $\pi D t$ times the
plug travel $t$, i.e. with presented area", and concluded $E_{thr} = e_a A(m)
\propto m^{2/3}$. **That step does not follow.** $\pi D t\cdot t \propto D$,
whereas $A \propto D^2$; the two scale differently and cannot be identified.
Dividing a plug-shear work by $A$ recovers $e_a$ only at the one mass where it
was evaluated — which is why §6's "same value from unrelated physics" agreement
looked stronger than it was.

The areal form is a genuine but *different* mechanism — compaction of the wood
column ahead of the fragment, $E_{crush} = \sigma_c A(m)\,t$. Both act; which
dominates is settled by their ratio:

$$\frac{E_{crush}}{E_{shear}} \;=\; \frac{\sigma_c\,(\pi/4)D^2 t}
{\tfrac12\tau\,\pi D t^2} \;=\; \frac{\sigma_c D}{2\,\tau\,t}. \qquad (8)$$

With $\sigma_c \approx$ 9.0 MPa (from Sanborn Table 2's SPF-S hardness, 605 lb
over the Janka ball's 11.28 mm projected area = 26.9 MPa mean indentation
pressure, ÷3 for the spherical-indenter constraint factor) and $t$ = 25.4 mm,
the two are equal only at $D$ = 51 mm. Over the fragment range the crush term is
**6–27%** of the shear term (0.1 g → 10 g). Shear-out dominates, and dropping
crush understates $E_{thr}$ by ~10% at the reference mass — inside the ±50%
target. **Eq. (7) is superseded by (9); $e_a$ is not a parameter of this model.**

### 7.3 Option A″ — plug-shear threshold, one sourced constant, no anchor

A plug of diameter $D$ shearing out of a panel of thickness $t$ presents a
cylindrical shear surface $\pi D(t-x)$ at displacement $x$, so

$$E_{thr}(m) \;=\; \int_0^t \tau\,\pi D(m)\,(t-x)\,dx
\;=\; \eta\,\tau\,\pi\,D(m)\,t^2,\quad \eta = \tfrac12,
\qquad D(m)=\Bigl(\tfrac{6m}{\pi\rho_s}\Bigr)^{1/3} \qquad (9)$$

$$\Longrightarrow\quad E_{thr}\propto m^{1/3},\qquad
v_{50}(m)=\sqrt{2E_{thr}/m}\;\propto\;m^{-1/3}. \qquad (10)$$

$\eta=\tfrac12$ is the linear shear-area-decay idealisation; $\eta=1$ (full
$\tau\pi Dt$ resisting over the whole travel) is the rigid upper bound. Both are
carried in the band below.

**The constant is $\tau$, and it is sourced.** Sanborn et al. 2019 Table 2,
in `doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/source.md`.
Anchor (greppable, verified 1 hit, line 87 for convenience only):
`Shear Strength Parallel to Grain, ASTM D143`.

| Species | $\tau$ | COV | $n$ | $\rho$ |
| --- | --- | --- | --- | --- |
| SPF-S (spruce-pine-fir south) | 1300 psi = **8.96 MPa** | 27% | 14 | 455 kg/m³ |
| SYP (southern yellow pine) | 1600 psi = 11.0 MPa | 13% | 19 | 548 kg/m³ |

SPF-S is taken as primary: scoping §2a item 4 already accepted it as a good
stand-in for Tolch's softwood on density and Janka grounds, and that judgement
is independent of this pass. **These are solid-wood coupon values, not the CLT
bond-line values** (2.75 / 6.07 MPa, same table) — the CLT-specific objections
of scoping §2a items 1–3 do not touch them.

*Admissibility (source-data-fidelity closure).* Table 2 prints every mechanical
row in **both** US and SI units, which is a closure invariant on the row used
here. All eight dual-unit pairs reconcile to **≤ 0.29%** (§1 of the check
script) — the row is admissible, and this also rules out a psi/MPa column swap.

**This closes the sourcing chain with no free parameter and no anchor.** $t$ is
Tolch's panel (1 in), $D(m)$ is the compact-fragment closure already logged in
§5.1, $\rho_s$ is steel, $\eta$ is geometry, and $\tau$ is a measured coupon
value from a document already in `doc-reference/`. Nothing is fitted to Tolch's
$B(r)$, and nothing is fitted to the count the test checks.

### 7.4 Validation — the same checks §4 ran

**Check 2 — monotonicity and limits — PASS, correct sign.**
$t$ = 1 in, SPF-S, $\eta$ = ½:

| $m$ [g] | $D$ [mm] | $v_{50}$ [m/s] | $E_{thr}$ [J] |
| --- | --- | --- | --- |
| 0.05 | 2.30 | 914.1 | 20.9 |
| 0.10 | 2.90 | 725.5 | 26.3 |
| 0.63 | 5.35 | 392.8 | 48.6 |
| 2.00 | 7.87 | 267.3 | 71.4 |
| 10.0 | 13.45 | 156.3 | 122.2 |
| 50.0 | 23.00 | 91.4 | 208.9 |

$E_{thr}$ **rising** in $m$ ✓ (scoping §1's expectation, which Option A
inverted); $v_{50}$ falling in $m$ ✓; $v_{50}\to\infty$ as $m\to0$ ✓. The
$v_{50}$ values are physically sane — 393 m/s for a 5.35 mm fragment through a
1-inch board — where Option A gave 5.4 m/s.

**Check 3 — order-of-magnitude bracket — PASS, with the probes demoted.**
At 0.63 g the defensible band (SPF-S $\tau \pm 1\sigma$, SYP, $\eta$ = ½→1) is
**35.5 – 97.2 J**, central **48.6 J**. The 78.6 J casualty probe lies **inside**
that band (central ratio 0.62); the 126 J Tolch hole-size probe lies 1.3× above
it (ratio 0.39). Both are within a factor ~2.6 of central — decade-level
agreement, against a criterion that failed this same check by 10⁴ under Option A.

This is now a **plausibility check only, not a calibration**: per §7.1 the
probes are mass-non-specific and measure a different criterion, so exact
agreement is neither expected nor desirable. What it discharges is scoping's
stated tripwire ("a result 100× away means a units error"), passed with two
orders of magnitude of margin.

**Check 1 — closure on an independent regime — PASS (order).** Forward-applying
(9) to Sanborn's *own* panel — 12.7 mm / 8.4 g steel sphere into 6.875 in 5-ply
CLT — gives $E_{thr}$ = 5453 J, $v_{50}$ = **1139 m/s** (SPF-S) / 1264 m/s
(SYP). Sanborn's shot envelope is 180–1200 m/s with 59 of 122 perforating, so
the true limit for the thickest panels lies inside that envelope and the
prediction sits at its upper end — correct to order, and mildly conservative, as
expected: at $t/D$ = 13.7 pure plugging over-states resistance (deep penetration
is cavity expansion, not shear-out), and CLT adds cross-ply and bond-line
planes. **This check uses no Tolch data at all**, which is the point.

**Sensitivity — PASS, and this is A″'s core advantage.** $E_{thr}$ is **linear**
in $\tau$: a ±27% COV on $\tau$ is ±27% on $E_{thr}$, inside the ±50% fidelity
target. Under Option A the same class of input error entered at power 4.86.

**Check 4 — count-chain §4 re-run — still NOT RUN**, deferred to the
implementation pass as §4.4 set out. **The direction is predictable and is
stated now, before the run, so it cannot be back-fitted:** (9) is *more
permissive* than a constant 78.6 J at the arrival velocities in play. Equating
the two puts the $m_{min}$ crossover at $v$ = 243 m/s; above it (9) admits
lighter fragments — at 1000 m/s, $m_{min}$ = 0.038 g against 0.157 g for the
constant probe. Since $N(\ge m)$ is steep in $m$, **A″ will raise the predicted
count relative to the 78.6 J probe run**, whose $N/779$ was already 1.73–2.00.
A″ may therefore *fail* the factor-2 count arm. That is a legitimate outcome of
a zero-free-parameter prediction and must not be tuned away; it is exactly the
information the compound-test objection was suppressing.

**Check 5 — `E_LETH_DEFAULT` regression — unchanged**, per §4.5: the
implementation is a threshold *callable* defaulting to today's scalar compare,
so the 1000 J ES-310 personnel path stays bit-identical.

### 7.5 Assumptions added (extending §5)

*Numbered A5–A8, continuing §5's list.*

1. **(A5) Plug-shear is the governing mechanism** at $t/D \approx$ 3–10, with crush
    as a ≤27% additive correction that is dropped (§7.2). Not valid as
    $D \to t$; out of scope for the fragment spectrum here.
1. **(A6) $\tau$ is a quasi-static ASTM D143 coupon value** used at ballistic strain
    rates. Wood shear strength rises with strain rate, so (9) is a **lower**
    bound on $E_{thr}$ and therefore **anti-conservative on count** — the same
    sign as the $\eta$ = ½ choice. This is the largest un-quantified term, and
    the honest reason the band's upper edge (97 J, $\eta$ = 1) is retained.
1. **(A7) Tolch's species is still unconfirmed**, and this no longer matters: under
    (9) $E_{thr}\propto\tau^1$ and the SPF-S/SYP spread is 23%. Under Option A
    it entered at power 4.86, which is why §5.2 made confirming the species a
    prerequisite there and not here. Scoping §3 item 4 is **closed as
    immaterial**.
1. **(A8) $\eta$ = ½ is geometry, not a fit.** It is not free to be adjusted to match
    the count; if the count arm fails, $\eta$ may not be moved.

### 7.6 What the implementation pass inherits

$E_{thr}(m) = \tfrac12\,\tau\,\pi\,D(m)\,t^2$ with $\tau$ = 8.96 MPa,
$t$ = 25.4 mm, $D(m) = (6m/\pi\rho_s)^{1/3}$, $\rho_s$ = 7850 kg/m³ — as a
`perforation_threshold_energy(m, target)` in `src/arty/`, with
`min_lethal_mass` / `build_mmin_table` taking a threshold callable defaulting to
the present `>= E_LETH_DEFAULT` scalar compare. Then run check 4 and report
whatever it gives.
