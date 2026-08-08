# Model Review — frag-field-3d-geometry

**Verdict:** PASS
**Reviewer:** model-reviewer agent
**Date:** 2026-05-31
**Review cycle:** 2 passes (initial FAIL → corrections applied → PASS)

______________________________________________________________________

## target-area-profile/derivation.md

Prior review result: reviewed and corrected before the current change. The two issues resolved were (1) explicit acknowledgement that $g_\text{new}$ differs from the old factor by $h/s$ and that $R_{50}$ calibration must be redone, and (2) documentation in §4.4 that eq. (9) (1D disk) is no longer a limit of eq. (22'). Both corrections are present in the derivation on file. Dimensional consistency passes ($\text{m}^2/\text{m}^2$), all posture limits are correct. **Status: PASS — no outstanding issues.**

______________________________________________________________________

## frag-field-3d-geometry/derivation.md

### 1. Dimensional consistency

All six equations in the §4 unit table are correct. The Mott $\mu^z$ formula (§3.5) carries no unit check in the table — it defers to the existing notebook convention. This is a non-blocking deferred item; the unit check must be added at integration time. All other equations check out.

Equivalent-column convention $C^b_\text{eff} = C^c \cdot (t_b / L_c)$ carries units [kg]·[m/m] = [kg]. Correct.

**Verdict: PASS** (with deferred $\mu^z$ unit check at integration).

______________________________________________________________________

### 2. Physical plausibility

**Per-zone Gurney velocities (corrected):**

| Zone          | $M^z/C^z$ | $V_0^z$ (m/s, formula) | $V_0^z$ (m/s, table) | Match? |
| ------------- | --------- | ---------------------- | -------------------- | ------ |
| Ogive         | 17.1      | 581                    | 578                  | ✓      |
| Cylinder      | 1.89      | 1578                   | 1578                 | ✓      |
| Boattail      | 30.2      | 440                    | 438                  | ✓      |
| Base (k=0.75) | 24.0      | 370                    | 375                  | ✓      |

All four zones now internally consistent with $V_0^z = k^z V_g / \sqrt{M^z/C^z + 1/2}$ at $V_g = 2440$ m/s. The corrected cylinder $V_0 \approx 1578$ m/s is consistent with BRL 126 panel data: the measured perforating velocity of ~835 m/s at 75 ft is after drag attenuation; starting at ~1578 m/s is physically plausible for thin-walled cylinder steel at this M/C.

Base reduction factors k = 0.75 (M1) and 0.70 (M107) are within NWC TP 7124's stated range 0.7–0.8.

**Verdict: PASS.**

______________________________________________________________________

### 3. Boundary conditions

Zero-boattail shell (`has_boattail=False`): Tier-2 table correctly assigns 0% boattail mass; implementation must exclude the zone from hazard computation when $M^t = 0$. Non-blocking implementation note.

$v_{g,z} \ge 0$ case (fragment upward or horizontal): the corrected §3.7 now explicitly states these fragments do not reach the ground in the straight-line model. The implementation must guard against division by $v_{g,z}$ near zero. Non-blocking implementation note, correctly documented.

**Verdict: PASS** (two implementation guards needed at integration).

______________________________________________________________________

### 4. Literature agreement

Base treatment ("mott" with k = 0.75–0.70): directly supported by NWC TP 7124 rarefaction mechanism and BRL 126 base-mass data (fewer, heavier fragments). Agreement strong.

Ogive Gurney (cylinder formula, zone-local M/C): consistent with SAND92-0243 cylinder baseline; NWC TP 7124 reduction factor (0.8×) correctly rejected for CRH 6–11 on geometric grounds.

Boattail: no dedicated data in any source; separate-zone treatment justified by 15% mass fraction and 4° spray-angle offset. Gap correctly acknowledged.

Tier-2 CRH = 6.0 default: engineering convention, no `doc-reference/` source, correctly disclosed. Disclosure pattern matches existing Limitation #5.

Base spray angle θ^b = 165°: phenomenological, no literature source, correctly flagged.

**Verdict: PASS.**

______________________________________________________________________

### 5. Open items

| #   | Item                                                             | Assessment                                                          |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| 1   | Base equivalent-column $C^b_\text{eff}$ not literature-sourced | Deferred-OK. Small contribution; geometrically motivated.           |
| 2   | M48 nose vs. side velocity cross-check                           | Deferred-OK. Future validation task.                                |
| 3   | AoF-resolved validation data absent                              | Deferred-OK. Phase-1 limitation correctly acknowledged.             |
| 4   | M107 secant-ogive arc centre spot-check                          | Deferred-OK for derivation; must be performed at integration.       |
| 5   | Boattail angle convention (full vs. half taper)                  | Integration-time blocker — must be resolved before code is written. |

**Verdict: PASS** (all five items correctly framed; item 5 is integration-time, not derivation-time).

______________________________________________________________________

### 6. Tier-2 ogive spray formula

Formula: $\theta^o_\text{Tier-2} = 90° - \arcsin!\left(\dfrac{\sqrt{\text{CRH}-1/4}}{2,\text{CRH}}\right)$

Geometry verified: the argument equals $L_n/(2R^o)$ for a tangent ogive, which is the sine of the surface slope angle at the axial midpoint, so the formula correctly subtracts it from 90° to obtain the normal angle from the axis.

Numerical spot-check:

| CRH | $\theta^o$ |
| --- | ----------- |
| 4   | 76.0°       |
| 6   | 78.5°       |
| 8   | 80.0°       |
| 10  | 81.0°       |
| 12  | 81.8°       |

All within spec band [75°, 88°]. Formula is geometrically correct and physically sensible.

**Verdict: PASS.**

______________________________________________________________________

### 7. Base equivalent-column convention

$C^b_\text{eff} = C^c \cdot (t_b / L_c)$: geometrically motivated (explosive column over base thickness), units correct, impact small (4% of steel mass). NWC TP 7124 rarefaction reduction $k^b$ partially compensates for the approximation's limitations. Correctly flagged as open item 1.

**Verdict: PASS** (acknowledged engineering approximation).

______________________________________________________________________

### 8. Cross-consistency with target-area-profile derivation

Both derivations produce the same geometry factor $A_p / (2\pi s^2 \cdot 2\sin\theta^z \delta)$. The target-area-profile eq. (P4) and the 3D geometry §3.8 boxed formula are identical in form with $\Theta \leftrightarrow \theta^z$.

**Verdict: PASS.**

______________________________________________________________________

## Corrections applied between passes

**Issue 1 — RESOLVED: AoF rotation geometry (§3.7 and §5)**

The original derivation wrote $\hat{u}_\text{fwd} = (\cos\alpha, 0, -\sin\alpha)$ with $\alpha = 90° - \text{AoF}$, which inverted the forward-axis direction at all AoF values. The correction replaces this with:

$$\hat{u}_\text{fwd} = (\cos(\text{AoF}),\\ 0,\\ -\sin(\text{AoF}))$$

and rewrites the rotation matrix as $R_y(\text{AoF})$. The expanded $v_{g,z}$ components are now:

$$v_{g,z} = -\sin(\text{AoF})\cos\theta^z + \cos(\text{AoF})\sin\theta^z\sin\phi$$

The special-case bullets are corrected: AoF=0° (horizontal shell) correctly shows cylinder spray going horizontal or upward (never reaching the ground in the straight-line model); AoF=90° (vertical shell) correctly gives $v_{g,z} = -\cos\theta^z$ independent of $\phi$.

The §5 circular-symmetry derivation is rewritten. At AoF=90° the ogive zone gives hit positions $(h_b\tan\theta^z\sin\phi, h_b\tan\theta^z\cos\phi)$ — a ring of radius $h_b\tan\theta^z$ independent of $\phi$. Cylinder fragments ($\theta^z = 90°$) have $v_{g,z} = 0$ and do not reach the ground, which is physically correct. Base fragments ($\theta^z = 165°$) have $v_{g,z} > 0$ and travel upward, also correct for a vertically-arriving shell.

**Issue 2 — RESOLVED: Cylinder $V_0$ in §6 (physical plausibility)**

The original table showed $M^c/C^c = 1.89$ and $V_0^c = 982$ m/s. The formula at $V_g = 2440$ m/s gives $1578$ m/s. The value 982 m/s was computed from total-shell M/C ($= 5.52$), inconsistent with the zone-local approach stated in §3.4. The table entry is corrected to $V_0^c = 1578$ m/s, and the accompanying note is rewritten to:

- Explain why the high cylinder velocity is physically correct (low zone-local M/C = 1.89, cylinder holds most of the interior explosive)
- Correctly interpret the BRL 126 panel measurements as drag-attenuated velocities at range, not initial velocities
- Explain the ratio $V_0^c / V_0^o \approx 2.7$ as the mechanism behind cylinder fragment dominance at side panels

______________________________________________________________________

## Deferred items (non-blocking)

- **Mott $\mu^z$ unit check** absent from §4 table. Add at integration, referencing Gold (2017) PAFRAG eq. 16.
- **Notation collision $\gamma$**: used for both fragment arrival angle and Mott material constant. Rename the Mott constant to $\Gamma_M$ or $B_M$ at integration.
- **$v_{g,z} \ge 0$ guard**: implementation must skip the hit-position formula when $v_{g,z} \ge 0$. Already documented in §3.7.
- **Boattail angle convention** (open item 5): resolve full vs. half-taper interpretation in `boattail_angle_deg` before writing implementation code.
- **M107 secant-ogive spot-check** (open item 4): perform before publishing M107 spray angle.
- **Tier-2 CRH = 6.0 limitations entry**: add to main `.qmd` at integration.
- **$R_{50}$ recalibration**: the new $s^{-2}$ geometry factor (vs. old $s^{-1}$) changes absolute hit counts; recalibrate against TM 9-1901 once the new factor is integrated.

______________________________________________________________________

## Overall verdict

**PASS** — both blocking issues corrected in the derivation. The corrected §3.7 AoF rotation geometry is internally consistent and verified for AoF = 0°, 25°, 45°, and 90°. The corrected §6 cylinder $V_0 = 1578$ m/s is consistent with the formula and the zone-local $M^c/C^c = 1.89$. All other areas of the derivation were sound in the initial pass and remain unchanged.

The integration pass may proceed. Deferred items listed above must be addressed during integration; none require a further derivation revision.

______________________________________________________________________

## Re-review 2026-08-08 — resolution of the "578/1578 m/s stale example" blocking finding

**Scope:** verify the modeler pass that closed two blocking findings —
(a) `derivation.md` §6's stale 578/1578 m/s M1 hand example contradicting the
shipped `zones.py`, and (b) the BRL 126 nose/side-spray citation
misattribution — by re-tracing `src/arty/zones.py` against the rewritten §6,
re-running `checks/zone-v0-ogive-vs-cylinder.py`, and checking the corrected
BRL 126 characterisation against `doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md`.

**Memory consulted:** `tolch-1938.md not a citable surface` — relevant because
this pass cites Tolch velocity figures again; checked whether the citation
sites have CSV backing or are markdown-only (see Finding 4 below).

### `collect-findings.py --for` scope check

One open item returned (SAND92-0243 C_D functional form), correctly out of
scope per the brief — not touched by this review.

### Findings

**1. `checks/zone-v0-ogive-vs-cylinder.py` reproduces `derivation.md` §6's
zone table exactly — Note, confirms fidelity.** Ran the script directly
(`uv run python experiment/fragmentation-field/updates/frag-field-3d-geometry/checks/zone-v0-ogive-vs-cylinder.py`).
M1 ogive M=3.716/C=0.841/M·C⁻¹=4.42/V0=1099.9, cylinder M=5.385/C=1.073/
M·C⁻¹=5.02/V0=1038.8, boattail 2.248/0.266/8.44/815.9, base 0.690/0.120/5.73/
732.9 — all match the table to the printed precision. M107 (961/1266 ordering,
−24%) and M48 (885/885, uniform Tier-2 fallback) rows also match. `C^o+C^c+C^t
= 2.180 kg = m_filler` is exact by construction (interior-volume-fraction
partition sums to `C_total`), confirmed against the registry's
`mass_filler=2.18` for "105mm M1 HE". `M_steel = 14.97 − 2.18 − 0.75 = 12.04`
matches the table total exactly.

**2. `_zone_gurney` and the mass/explosive partition in `zones.py` match
what §6 now describes — Note, confirms "no code change needed" is correct.**
Traced `compute_shell_zones` (zones.py:182–399): Tier-1 explosive allocation
is by interior-volume fraction (`C_ogive/cyl/bt = C_total · V_int_z/V_int_total`,
line 278–280) exactly as §6 states; base gets the equivalent-column proxy
`C_base = C_cyl·(t_b/L_c)` (line 284) deliberately outside the partition,
exactly as §6's footnote states. `_zone_gurney` (line 124–128) is
`k·V_g/√(M/C+0.5)`, matching the formula §6's energy-closure paragraph uses.
`_base_k` (line 175–179) gives k=0.75 for M1 (<150mm) — confirmed by hand:
`0.75·2440/√(5.729+0.5) = 733.0 m/s`, matching the table's 733 to the last
digit. The 578/1578 m/s pair the original finding cited does not appear
anywhere in `zones.py`; the modeler's conclusion that the shipped code was
never wrong is correct on independent trace, not just the script's word.

**3. Energy-closure identity in §6 is algebraically correct — Note.**
$V_0^z=k^zV_g/\sqrt{M^z/C^z+1/2} \Rightarrow \tfrac12(V_0^z)^2(M^z+C^z/2)=(k^z)^2C^zE$
with $E=V_g^2/2$ verified by direct substitution. Summing zones (base carries
$k^b{}^2$, others $k=1$) gives $(2.180+0.5625\times0.120)E=2.2477E=6.691$ MJ,
matching the script's `zone-sum=6.691 MJ` output exactly. This is a
self-consistency/unit check on the implementation of the formula the code
already uses, not an independent physical validation — the derivation labels
it "(unit check)" honestly and does not oversell it as a literature
cross-check. Correctly scoped.

**4. BRL 126 side-spray correction is faithful to `card.md`'s current
"Fragment Velocities (Charge Components)" section — Note, no provenance
gap.** `card.md` (already revised, presumably in a prior pass) states the two
velocities are "not directly measured... computed from the change in the
side-spray angle with remaining velocity" and that the third digit of
"27^0 f/s" is unreadable, "commonly read as 2,750... not certain" — this
matches §6's "the third glyph is unreadable on the held scan, commonly read
2,750" essentially verbatim. `card.md` line 22 bans citing `tolch-1938.md`
for any number without CSV backing (per
`tolch-1938.md not a citable surface` in memory); these two velocity figures
are **not** among the four spray-density tables with CSV/invariant backing —
they remain markdown-anchor citations only (`tolch-1938.md:146,1658,1698,1654`),
same as at the time that memory entry was written. This is a pre-existing gap
this pass did not introduce or worsen (the figures were already cited this way
before the correction); flagging for completeness per the memory note, not as
a new defect. **Deferrable** — extract these two lines to a `tables/*.csv` +
`.invariant` (even a 2-row table) to close the gap; no computed output changes
either way since the figures are used only as a qualitative magnitude
bracket, not a fitted parameter.

**5. Minor unit conversion drift: "835 m/s" vs. the sibling drag-gap-1944
document's "838.2 m/s" for the same unreadable-digit figure — Note, immaterial.**
`derivation.md` and `scoping.md` both read the unreadable third glyph as
"2,740 f/s" → 835 m/s (`rebaseline-verdict.md:52` states this explicitly:
"2740 ft/s (835 m/s)"), while
`experiment/fragmentation-field/challenges/drag-gap-1944/tolch-1938-panel-distance.md:134,140`
reads it as "2750 f/s" → 838.2 m/s for the same quantity. Both are guesses at
an admittedly-unreadable digit (`card.md` explicitly declines to certify
either reading), so neither is more "correct," but the two artifacts now
disagree by 3 m/s (0.4%) on a number both attribute to the same source line.
Immaterial to any conclusion in this pass (the M48 magnitude-check bracket
835–923 m/s vs. computed 885 m/s is unaffected at the ±0.4% level). Note only.

**6. Stale ogive spray angle in the untouched part of §6 — Deferrable,
same defect class as the one this pass just fixed, left uncaught.**
`derivation.md`'s "Ogive spray angle (Tier-1)" and "Spray angles summary for
M1" (lines ~407–418, **not modified by this diff** — confirmed via
`git log -p`, present verbatim since before this pass) state
$\theta^o \approx 79.5°$. Re-running the check script and reading
`ZoneParams.spray_deg` directly (`p.spray_deg` in
`checks/zone-v0-ogive-vs-cylinder.py`'s printed output) gives **83.5°** for
the M1 ogive zone — confirmed independently by hand-evaluating
`zones.py`'s `_ogive_arc_centre`/spray-angle formula (lines 228, 308–316)
with the M1 drawing constants ($R_o=0.6477$, $D=0.105$, $L_n=0.14681$):
$\text{atan2}(0.6435, 0.0734) = 83.5°$, not 79.5°. The 79.5° figure appears to
come from the Tier-2 tangent-ogive formula ($90° - \arcsin(\sqrt{CRH-0.25}/2CRH)$
at CRH≈6.02 gives ≈78.5°, close to 79.5° but not the Tier-1 arc-centre code
path M1 actually uses) rather than the shipped Tier-1 code. This is exactly
the same failure mode the pass was dispatched to fix (documented value
disagreeing with shipped `zones.py` output) recurring two paragraphs below
the section it rewrote, using the same check script that would have caught
it. **Impact: zero on any shipped output** — `spray_deg` is computed live by
`zones.py` wherever it's used (belt geometry, spray-cone rendering); nothing
reads the derivation's printed 79.5° figure. Purely a documentation-fidelity
gap, but one sitting in the exact section this pass certified as
"the shipped ones, regenerated by `checks/zone-v0-ogive-vs-cylinder.py`."
Suggested fix: update the "Ogive spray angle" line and the spray-angle
summary table to 83.5°, or extend the check script to print `spray_deg` per
zone so the next pass catches this class of drift automatically.

**7. Check-script Total-row single-zone reference doesn't match what the
script itself prints — Note, low materiality, script/table divergence.**
The derivation's Total row gives M/C=5.52, $V_0$=994 m/s "(1-zone)" — this
uses $C_\text{total}=2.180$ kg (the true `mass_filler`, excluding the
double-counted base proxy): $12.040/2.180=5.523$,
$2440/\sqrt{6.023}=994.2$ m/s ✓ matches the table. But
`checks/zone-v0-ogive-vs-cylinder.py` computes and prints a *different*
single-zone reference (`single-zone M/C=5.234 V0=1019.0 m/s`), because it
naively sums all four zones' `C_kg` including the base's equivalent-column
proxy (`tot_C = 2.3004`, double-counting explosive already assigned to the
cylinder). The derivation table's 994 m/s is the more physically correct
figure (it doesn't double-count); the script's printed 1019 m/s is not what
appears in the table it's meant to validate. This is the one cell the script
does *not* reproduce, undermining the "run it yourself to confirm it
reproduces §6" claim for that single row. **Impact: none on any conclusion**
(the Total row is a reference/sanity baseline, not used elsewhere), but worth
a one-line script fix (exclude `C_base` from the naive single-zone sum, or
add a second printed line using `C_total = C_ogive+C_cyl+C_bt`) so the
retained script fully reproduces every cell it's cited for.

**8. Self-referential line-number anchors in `rebaseline-verdict.md`'s
closure note are already stale — Note, internal cross-reference only.**
The "Closed 2026-08-08" paragraph reuses `derivation.md:358,379` (the
pre-edit line numbers established when the finding was originally filed) to
point at the now-corrected BRL 126 text, but the diff shifted §6 by +57
lines net — the corrected text is now at derivation.md:394 and :429, not
358/379. Not a source citation (so the letter of the
"anchors are greppable strings" rule doesn't bind an internal cross-doc
pointer the way it binds a citation into `doc-reference/`), but the same
failure mode: a bare line number that will rot. No physics or shipped-output
impact.

### Verdict: **PASS-with-limitations**

No Blocking findings. The two closed blocking findings (stale 578/1578 m/s
V0 pair; BRL 126 nose/side misattribution) are genuinely resolved: the
zone-mass/V0 table, the per-shell ordering table, and the corrected BRL 126
characterisation all check out against independently re-run/re-traced code
and against `card.md`. Leaving `src/arty/zones.py` unchanged is the right
call — traced `_zone_gurney` and the Tier-1 mass/explosive partition by hand
against §6's description and they match; the stale numbers never existed in
shipped code.

**Log as limitations (no fix required to pass, but should be recorded so a
future pass doesn't have to rediscover them):**

- §6's "Ogive spray angle (Tier-1)" / spray-angle summary table cites 79.5°
    for the M1 ogive zone; the shipped `zones.py` computes 83.5° (confirmed
    both via the check script's `spray_deg` output and by independent hand
    evaluation of the arc-centre formula). Update to 83.5° or note the
    discrepancy explicitly.
- The two Tolch fragment-velocity figures (2,7?0 / 3,030 f/s) cited in §6 and
    scoping.md have no `tables/*.csv` backing per `card.md`'s own
    citability ban — pre-existing gap, not introduced by this pass.
- `checks/zone-v0-ogive-vs-cylinder.py`'s printed "single-zone" reference
    (1019 m/s) doesn't match the derivation table's Total-row figure (994 m/s)
    because the script double-counts the base's equivalent-column explosive
    proxy; the table's own number is correct, only the script's auxiliary
    print line is inconsistent with it.
- `rebaseline-verdict.md`'s closure note cites pre-edit line numbers
    (`derivation.md:358,379`) that no longer point at the corrected text
    post-edit (now ~394/~429).
- Cross-document drift on the unreadable third glyph: this update reads it as
    "2,740 f/s" (835 m/s) while `drag-gap-1944/tolch-1938-panel-distance.md`
    reads it as "2,750 f/s" (838.2 m/s) for the same source line — both are
    admittedly uncertain reads, immaterial (0.4%) either way.

None of these change any shipped `src/arty/` output or the qualitative
conclusion (ordering is drawing-dependent, not a fixed rule); all are
documentation-fidelity gaps suitable for a logged limitation rather than a
blocking re-dispatch.
