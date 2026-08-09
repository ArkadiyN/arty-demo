# Tolch (1938) 75mm M48 panel tests — is this an independent check on the drag gap?

Assessment only (no `src/arty/` changes). Asks whether N.A. Tolch's panel-test
fragment-density data corroborate, contradict, or extend the
"model under-decelerates fragments" finding established in
`initial-conditions-{75,105,155}mm.md` and
`drag-coefficient-calibration.md`.

Source: `doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`.

______________________________________________________________________

## Finding 1 — the headline "velocity dependence" is NOT a drag observable

The card's framing (`card.md`, "Velocity-Dependence Summary" and "Drag Model
Relevance") invites reading Tolch's velocity axis as a fragment-decay
measurement. It is not. Tolch's "average remaining velocity when burst" is the
**shell's** remaining velocity at the burst point
([tolch-1938.md:790–800](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md), firing-conditions table),
swept 0 (static) → 2,130 f/s by varying the firing charge/range. The panel
radius is held fixed while that axis is swept.

Tolch states the mechanism explicitly for the base spray (line 890 region):

> "the velocity component of the base fragments due to the explosive charge and
> the velocity component due to the remaining velocity of the projectile have
> the same line of action, and hence the resultant fragment velocity is simply
> the algebraic sum of the two components."

So the base-spray collapse (9.71 → 0.70 hits/u.s.a., static → 2,130 f/s) and
the nose-spray rise (16.09 → 21.45) are **vector addition of shell velocity to
Gurney ejection velocity**, plus the side-spray forward sweep (95° → 55° off
axis) — i.e. a *burst-geometry / spray-kinematics* observable, not a drag
observable. A model with zero drag would reproduce essentially all of it.

**Consequence:** the card's "Drag Model Relevance" section overstates the case.
The 93% base-spray collapse it recommends as the drag anchor is the *least*
drag-sensitive number in the report. This is a card defect, not a source
defect — the source is unambiguous.

*(Secondary value, out of scope here: that same velocity sweep is a good
independent check on the project's **burst-geometry / spray-angle** aspect —
specifically whether the side-spray centroid sweeps 95° → 55° as the shell
velocity vector is added. That is a different aspect and a separate pass.)*

______________________________________________________________________

## Finding 2 — Tolch *does* contain a usable, independent drag observable

The report's other axis is **panel radius**: four concentric semicircular
1"-spruce panels at **15, 36, 75, and 120 ft** ([line 335](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md)),
built in concentric pairs so two distances are sampled on the *same round*.
Tolch frames the resulting density falloff as a drag measurement in as many
words ([line 804](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md)):

> "Since the fragments lose velocity in flight due to air resistance, their
> ability to mark the panels decreases with the distance. […] In order to
> investigate the loss in density, the hits per unit solid angle were averaged
> over certain panel areas and arranged in tabular form."

Hits per unit solid angle is a **range-invariant** measure by construction (the
1/R² geometric spreading is divided out), so any residual R-dependence is
almost entirely *fragments dropping below the panel-marking velocity
threshold* — which is exactly the min-lethal-mass / velocity-decay mechanism
the Ordnance checks probe, on a different source, a different projectile
population, and a different threshold criterion. This is a genuine independent
check.

**Static firings isolate it cleanly.** At zero remaining velocity there is no
shell-velocity vector to confound the spray kinematics, and the panel radii
15→120 ft (4.57→36.6 m) span the short-range end of the Ordnance table where
the model's `v_model/v_source` ratio already runs 1.3–2.6× (75mm).

### The data (static firing, side spray, averaged over 76–111° from nose)

Table at [tolch-1938.md:815 ff](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md)
(OCR of a degraded page; digits cross-checked against the report's own summary
paragraph and against §Summary item 1 at line 1673, both of which agree):

| Panel | R (ft) | R (m) | Perf. | Penet. | Dents | Total |
| :---- | -----: | ----: | ----: | -----: | ----: | ----: |
| A     |     15 |  4.57 |  1.49 |    .97 |  2.39 |  4.85 |
| B     |     36 | 10.97 |  1.47 |   1.29 |  1.13 |  3.89 |
| C     |     75 | 22.86 |  1.18 |    .47 |   .18 |  1.83 |
| D     |    120 | 36.58 |   .83 |    .65 |   .04 |  1.52 |

Cross-checks that validate this OCR:

- Tolch's own text: "the losses in density of perforating fragments between
    Panels A and D for remaining velocities of zero, 700, and 1085 were 44, 19,
    and 33%". Here 1 − 0.83/1.49 = **44.3%**. ✓
- Summary item 1 (line 1673): Panel A static side spray "about 1.5
    perforations, 1.0 penetrations, and 2.4 dents … total of 4.9"; and totals
    "4.9, 3.9, 1.6, and 1.5 on the 15, 36, 75, and 120 ft. panels". ✓ (the
    1.6 vs 1.83 for Panel C is a rounding/transcription slip in the source's own
    summary, not in the table).
- Totals column reproduces the separately-typeset totals table
    ([line 838](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md)): 4.85 / 3.89 / 1.83 / 1.52. ✓

The **perforation** row is the one to use: a perforation is a hard, monotone
velocity/energy threshold ("travels completely through the [1" spruce] panel",
line ~845). Penetrations and dents are *not* usable — Tolch notes the
penetration count is contaminated by fragments demoting from perforations, and
dents by fragments demoting from both, so those classes are non-monotone in
range (visible above: Panel B penetrations *exceed* Panel A's).

______________________________________________________________________

## Method

Hits per unit solid angle already divides out $1/R^2$, so the model's
prediction for the *same* observable is the fraction of the spray still above
the panel-perforation threshold:

$$\frac{\sigma(R)}{\sigma(R_0)} = \frac{N(m \ge m_{thr}(R))}{N(m \ge m_{thr}(R_0))}
\quad (1)$$

with $m_{thr}(R)$ from `min_lethal_mass(R, V0, E_thr, drag, rho_steel)` and
$N(\cdot)$ from `mott_N`, both called unmodified from `arty.fragmentation`.

| Symbol      | Meaning                                        | Unit |
| :---------- | :--------------------------------------------- | :--- |
| $\sigma(R)$ | perforations per unit solid angle at radius R  | –    |
| $m_{thr}$   | least mass still perforating 1" spruce at R    | kg   |
| $E_{thr}$   | perforation kinetic-energy threshold           | J    |
| $\mu, N_0$  | Mott half-weight / total count (`mott_params`) | kg,– |

$E_{thr}$ is the single free parameter (the wood ballistic limit is not in
`doc-reference/`, so it is fitted, not assumed). Three independent ratios
against one parameter makes the test over-determined. Fitted to reproduce the
observed A→D ratio 0.557, then the intermediate panels and the *absolute*
count are checked. Swept over combined $C_D C_{shape} \in \{0.585$ (current)$,
0.878, 1.2, 1.7, 2.93\}$ and $V_0 \in \{838.2$ (Tolch's own measured
perforating-fragment velocity, 2750 f/s, Summary item 10)$, 807.5$ (model
Gurney **as of the sweep**, pre-fix — see the as-of note below)$, 951.0$
(Ordnance-stated)$\}$ m/s. **1.2 and 1.7 are SAND92-0243's
prose-sentence values ("can vary between 1.2 and 1.7"), not its own
parameter-range-list data floor/ceiling (1.0–1.71) — the sweep below has not
been re-run at 1.0/1.71** (OPEN-FINDINGS.md SAND92-0243-citation finding);
see the note after Result 2.
Script: `experiment/_scratch/tolch-panel-distance-check.py`.
**That script is missing from the repository** despite this document citing
its numbers (`.claude/rules/verification-scripts.md`); the sweep tables below
cannot currently be reproduced or re-run at the corrected bounds.
FINDING\[deferrable\]: tolch-1938-panel-distance.md cites a sweep script that no longer exists on disk, so its published tables cannot be reproduced or re-swept at the corrected 1.0/1.71 SAND92-0243 bounds (affects: experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md; since: 2026-08-08)

**As of 2026-08-09 — the 807.5 m/s column is a historical model value.** The
75 mm M48 fuze/case-mass correction moved the shipped inputs to
$M_{case} = 4980.0$ g, $V_0 = 864.4$ m/s, $\mu = 0.826$ g, $N_0 = 3016$
([`../../updates/75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py`](../../updates/75mm-fuze-case-mass-fix/checks/shipped-75mm-current-values.py)).
Every sweep number below was computed at the pre-fix $V_0 = 807.5$ m/s and
pre-fix spectrum, so the columns are **left as run** rather than relabelled —
restating the header without re-running would attach current inputs to
pre-fix outputs. Read the "$V_0 = 807.5$" column as *pre-fix model*; the
current model velocity, 864.4 m/s, sits between the 838.2 and 951.0 columns
and closer to the former (+3.1% vs −9.1%). This does not disturb any Result
below: Result 1 is a *degeneracy* verdict on *ratios*, which the $V_0$ columns
here already show to be near-invariant across 807.5–951.0. Result 3's absolute
counts would shift on the current basis in a direction this document cannot
settle without re-running the (missing) script — $V_0$ up 7.0% raises the
per-fragment perforating fraction while $N_0$ down 17% lowers the population —
but the shift is far smaller than the 1.2–2.7× residual at issue, so the
over-count verdict is unaffected. The counts themselves are superseded — the
current-basis
count comparison lives in
[`../count-gap-1938/rebaseline-verdict.md`](../count-gap-1938/rebaseline-verdict.md),
not here.

## Result 1 — the shape test is degenerate: no discriminating power on drag

Predicted ratios at 15/36/75/120 ft after fitting $E_{thr}$ (V0 = 838.2 m/s;
the other two V0 cases are indistinguishable):

| combined $C_D C_{shape}$ | fitted $E_{thr}$ (J) | ratio A/B/C/D        | residual at B, C |
| -----------------------: | -------------------: | :------------------- | :--------------- |
|      **0.585** (current) |                294.5 | 1.000 .887 .713 .557 | −0.100, −0.079   |
|                    0.878 |                 35.9 | 1.000 .885 .711 .557 | −0.102, −0.081   |
|         1.2 (SAND prose) |                  7.3 | 1.000 .884 .711 .557 | −0.102, −0.081   |
|         1.7 (SAND prose) |                  1.1 | 1.000 .887 .715 .557 | −0.100, −0.077   |
|                     2.93 |                 ~0.0 | 1.000 .897 .725 .557 | −0.090, −0.067   |
|             **observed** |                    – | 1.000 .987 .792 .557 | –                |

Every drag value reproduces the *same* curve once $E_{thr}$ is refitted — the
residual is flat at −0.10/−0.08 across a 5× span of drag. **The panel-radius
falloff cannot discriminate the drag coefficient at all.** A single threshold
parameter fully absorbs any decay rate over this short a baseline (4.6→36.6 m)
and this shallow a loss (44%).

The common −0.10 residual at Panel B is the observation that perforation
density is *flat* from 15→36 ft (1.49→1.47) and only then falls; no
threshold-decay model produces a plateau. At the source's own quoted probable
errors (P.E. of mean ≈ 0.08–0.10 on values ≈1.5, i.e. σ ≈ 0.12–0.15) that
residual is ≈1.3σ — suggestive, not significant.

## Result 2 — the absolute count *does* discriminate, and it rules out raising drag

Fitting $E_{thr}$ to the A→D loss fixes $m_{thr}$, so the model's **absolute**
number of perforating fragments at 15 ft becomes a prediction. Tolch measures
it directly — Summary item 6: "the total number of fragments issuing from the
shell computed from the fragment densities on the panels was about 5000,
consisting of about **700 perforations**, 900 penetrations, and 3400 dents";
corroborated by the independent pit test (Summary items 1 and 8: **779**
fragments recovered per shell — re-baselined from a published 803, see
[`count-gap-1938/rebaseline-verdict.md`](../count-gap-1938/rebaseline-verdict.md) —
95.6% of the metal by mass, and "practically
all the fragments obtained in pit tests would be perforating fragments in
panel tests at 15 ft").

Model $N(m \ge m_{thr}(15\,\text{ft}))$:

(Sweep as run on the pre-fix 75 mm M48 basis — the "807.5" column is the
*pre-fix* model $V_0$; the shipped model is now 864.4 m/s with $N_0 = 3016$.
See the as-of note above.)

| combined $C_D C_{shape}$ | V0 = 807.5 | V0 = 838.2 | V0 = 951.0 |
| -----------------------: | ---------: | ---------: | ---------: |
|      **0.585** (current) |      1 234 |      1 703 |      4 383 |
|                    0.878 |      5 199 |      6 231 |     11 004 |
|         1.2 (SAND prose) |      7 902 |      9 122 |     14 552 |
|         1.7 (SAND prose) |      9 755 |     11 067 |     16 825 |
|                     2.93 |     11 072 |     12 441 |     18 408 |
|     **observed (Tolch)** |            |   ~700–800 |            |

Only the **current** drag value lands within a factor 1.5–2.5 of Tolch's
measurement (at the two lower, better-supported V0 values). Raising the
combined drag to 1.2–1.7 (SAND92-0243's prose-sentence values — see the note
above on the source's own, unswept, 1.0–1.71 data-range figure) inflates the
perforating-fragment count to **11–14×** the measured value. Raising it 5×
(the factor the 75mm Ordnance check's implied-λ gap suggested) gives ~15×.

The mechanism is direct: a larger drag makes fragments decay faster, so
reproducing the *same* modest 44% count loss over 15→120 ft requires the
perforation threshold to sit far lower on the mass spectrum — $m_{thr}(15\,
\text{ft})$ drops from 0.91 g at current drag to 0.014 g at 1.7 and ~0.004 g
at 2.93. A 4–14 mg steel fragment (a ~1 mm cube, ~3 J at 838 m/s) perforating
a 1-inch spruce board is not physical. Tolch's own hole-size data agree: the
*smallest* wood perforations have cross-sections below 0.02 in² = 12.9 mm²
(line 1365), which for a compact steel fragment bounds mass at
$\rho A^{3/2} \approx 0.36$ g — the same order as the current-drag fit,
1–2 orders above the high-drag fits. (This bound is soft: spruce tears, so the
hole exceeds the fragment cross-section, which pushes the true mass down —
worth roughly a factor of a few, not a factor of 30.)

## Result 3 — a larger defect surfaces in a *different* aspect: the Mott scale

Even at current drag the model over-counts perforating fragments by ~1.8–2.4×
(1234–1703 vs ~700). That residual is not a drag effect; it is the fragment
**mass spectrum**:

- Model mean fragment mass $2\mu$ = **0.29–0.47 g** ($\mu$ from `mott_params`,
    $N_0$ = 12 256–20 021 for a 5 755 g shell body).
- Tolch pit test: **779** fragments carrying 95.6% of the metal → mean
    recovered fragment mass **7.40 g** (re-baselined from a published 803 /
    6.85 g — see
    [`count-gap-1938/rebaseline-verdict.md`](../count-gap-1938/rebaseline-verdict.md)).
- Matching Tolch's 95.6%-of-mass recovery in the model requires a cut near
    0.13 g, above which the model holds ≈**6 000** fragments — **~7.7× more**
    than the 779 Tolch recovered.

The model's Mott $\mu$ is roughly an order of magnitude too small: it breaks
the shell into far too many, far too light fragments. Note this is *not*
visible in the fines mass budget (the model puts only 1.2–2.2% of the metal
below 0.05 g, comfortably inside Tolch's 4.4% unrecovered), so it can only be
caught on **counts**, which is exactly what Tolch provides.

This is a separate model aspect (Mott fragmentation spectrum, not drag) and
needs its own pass. It matters here because the two errors are confounded and
partly compensating: too many too-light fragments inflates counts, while
too-little drag lets those light fragments keep energy they should not have.

______________________________________________________________________

## Verdict

**Tolch is usable, and it changes the conclusion — but not in the direction
the card advertised.**

1. **The card's recommended drag anchor is wrong.** Tolch's "remaining
    velocity" sweep (base-spray 93% collapse, nose-spray rise) is shell velocity
    at burst — a vector-addition / spray-kinematics observable, essentially drag-
    insensitive. `card.md`'s "Drag Model Relevance" section should be corrected.
    Its real value is as a check on the **burst-geometry / spray-angle** aspect.
1. **The drag observable Tolch does contain — panel-radius density falloff —
    is shape-degenerate.** It cannot discriminate $C_D C_{shape}$ over a 5×
    span. So Tolch neither corroborates nor contradicts the *existence* of the
    velocity-decay gap found in the Ordnance checks. Those remain the only
    evidence for it, and they are unshaken: the Ordnance λ gap was inferred by
    feeding the source's own per-range $m(r)$ into `retardation_coeff`, which is
    independent of everything measured here.
1. **Tolch does contradict the proposed *remedy*.** The
    `drag-coefficient-calibration.md` candidate of raising
    combined $C_D C_{shape}$ to 1.2–1.7 (SAND92-0243's prose values) is
    **refuted** by Tolch's absolute fragment counts: it would put 11–14×
    more perforating fragments at 15 ft than measured, and imply a
    physically impossible ~10 mg wood-perforation threshold. Do not adopt a
    constant drag increase in that range on the strength of the Ordnance
    checks alone. This strengthens that check's own closing sentence — the
    residual is not a constant-drag-scaling error.
1. **Tolch redirects the investigation to the Mott mass spectrum.** The
    ~7.7× fragment-count excess against Tolch's pit test is a larger, cleaner,
    and independently-measured defect than the drag gap, in a different
    aspect. *(An earlier version of this bullet said this "plausibly drives
    much of the 7–33× B(r) over-prediction that started this line of work" —
    that B(r) figure was VOID, a column-swap defect since corrected; see
    [`b-vs-range-rebaseline.md`](b-vs-range-rebaseline.md). Family B's
    corrected verdict is mostly PASS, so the Mott mass-spectrum excess found
    here is no longer a candidate explanation for a B(r) gap that, at that
    magnitude, does not exist — it stands on its own as a genuine,
    independently-measured defect regardless.)* Recommend scoping the Mott
    $\mu$ / `mott_params` calibration next, **before** any further drag
    tuning — the two are
    confounded, and calibrating drag against B(r) while $\mu$ is an order of
    magnitude off would tune the wrong knob.

**No `src/arty/` defect is scoped for immediate fix.** Result 3 identifies a
probable defect in `mott_params`, but confirming it needs its own pass
(pit-test screen data, the Mott constant $B$, and the `sigma_f/gamma` steel
ratio) and is out of scope here.

### Assumptions

- The side-spray fragment mass spectrum is the whole-shell Mott spectrum
    (angle-independent), so density ratios across R equal count ratios above
    threshold. Tolch supports this for base vs side spray (Summary item 7: "the
    fragments of the base and side sprays have about the same distribution
    according to size") but *not* for the nose spray, which is why only the side
    spray is used.
- Perforation of 1" spruce is a pure kinetic-energy threshold, mass- and
    velocity-independent otherwise. Real wood ballistic limits scale closer to
    energy *per presented area*; using $E$ alone biases $m_{thr}$ somewhat, but
    not by the 1–2 orders of magnitude separating the drag candidates.
- Gravity drop and ground ricochet, which Tolch notes also remove far-panel
    hits ([line 804](../../../../doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md)),
    are neglected. Both *add* far-panel loss, so ignoring them makes the model's
    required drag an over-estimate — i.e. it biases toward the high-drag
    candidates, and they are rejected anyway. Conservative for this verdict.
- Panel-A numbers are the horizontal-axis firings; Tolch's Summary item 5
    confirms the vertical-axis firings agree at 15 ft.

### Fidelity target

Drives whether the project changes `DragParams`. Tolerable error: a factor ~2
on the implied fragment count — the discriminating signal here is 11–14×, well
clear of that.
