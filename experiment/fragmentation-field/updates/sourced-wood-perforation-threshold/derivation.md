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

All numbers below are produced by
[`checks/ufc-5-1-perforation-threshold.py`](checks/ufc-5-1-perforation-threshold.py)
(`uv run python …`, < 1 s).

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
`hardness_pounds,density_lbs_per_ft3`) carry them **reversed**. This is the
column-inversion failure `.claude/rules/source-data-fidelity.md` exists to
prevent; the check script reads the CSV and reverses the two fields explicitly.

A closure invariant settles it without the image, and the `.invariant` file's
claim that "no closure check is applicable" is wrong: **wet ≥ dry in column 1
on every species** (water adds mass — density) and **wet ≤ dry in column 2 on
every hardwood** (saturated wood is softer — hardness). Both hold; the labels
are what is backwards. Mechanised in the check script.

Sanity of the scale: $H$ = 38.7 lb for dry pine is ~1/10 of the standard Janka
side-hardness (≈ 380–870 lbf). **Do not substitute real Janka values into (3)** —
Eq. 5-1 is a curve fit to the Table 5-5 scale, whatever that scale is.

FINDING[blocking]: UFC Table 5-5 density/hardness columns are transposed in card.md and the CSV (page image: col1=density, col2=hardness) (affects: doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/card.md, doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/tables/table-5-5-wood-properties.csv, doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects/tables/table-5-5-wood-properties.invariant; since: 2026-08-09)

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
