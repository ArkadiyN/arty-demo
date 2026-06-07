# Model Review — frag-field-3d-geometry

**Verdict:** PASS
**Reviewer:** model-reviewer agent
**Date:** 2026-05-31
**Review cycle:** 2 passes (initial FAIL → corrections applied → PASS)

______________________________________________________________________

## target-area-profile/derivation.md

Prior review result: reviewed and corrected before the current change. The two issues resolved were (1) explicit acknowledgement that $g\_\\text{new}$ differs from the old factor by $h/s$ and that $R\_{50}$ calibration must be redone, and (2) documentation in §4.4 that eq. (9) (1D disk) is no longer a limit of eq. (22'). Both corrections are present in the derivation on file. Dimensional consistency passes ($\\text{m}^2/\\text{m}^2$), all posture limits are correct. **Status: PASS — no outstanding issues.**

______________________________________________________________________

## frag-field-3d-geometry/derivation.md

### 1. Dimensional consistency

All six equations in the §4 unit table are correct. The Mott $\\mu^z$ formula (§3.5) carries no unit check in the table — it defers to the existing notebook convention. This is a non-blocking deferred item; the unit check must be added at integration time. All other equations check out.

Equivalent-column convention $C^b\_\\text{eff} = C^c \\cdot (t_b / L_c)$ carries units [kg]·[m/m] = [kg]. Correct.

**Verdict: PASS** (with deferred $\\mu^z$ unit check at integration).

______________________________________________________________________

### 2. Physical plausibility

**Per-zone Gurney velocities (corrected):**

| Zone          | $M^z/C^z$ | $V_0^z$ (m/s, formula) | $V_0^z$ (m/s, table) | Match? |
| ------------- | --------- | ---------------------- | -------------------- | ------ |
| Ogive         | 17.1      | 581                    | 578                  | ✓      |
| Cylinder      | 1.89      | 1578                   | 1578                 | ✓      |
| Boattail      | 30.2      | 440                    | 438                  | ✓      |
| Base (k=0.75) | 24.0      | 370                    | 375                  | ✓      |

All four zones now internally consistent with $V_0^z = k^z V_g / \\sqrt{M^z/C^z + 1/2}$ at $V_g = 2440$ m/s. The corrected cylinder $V_0 \\approx 1578$ m/s is consistent with BRL 126 panel data: the measured perforating velocity of ~835 m/s at 75 ft is after drag attenuation; starting at ~1578 m/s is physically plausible for thin-walled cylinder steel at this M/C.

Base reduction factors k = 0.75 (M1) and 0.70 (M107) are within NWC TP 7124's stated range 0.7–0.8.

**Verdict: PASS.**

______________________________________________________________________

### 3. Boundary conditions

Zero-boattail shell (`has_boattail=False`): Tier-2 table correctly assigns 0% boattail mass; implementation must exclude the zone from hazard computation when $M^t = 0$. Non-blocking implementation note.

$v\_{g,z} \\ge 0$ case (fragment upward or horizontal): the corrected §3.7 now explicitly states these fragments do not reach the ground in the straight-line model. The implementation must guard against division by $v\_{g,z}$ near zero. Non-blocking implementation note, correctly documented.

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
| 1   | Base equivalent-column $C^b\_\\text{eff}$ not literature-sourced | Deferred-OK. Small contribution; geometrically motivated.           |
| 2   | M48 nose vs. side velocity cross-check                           | Deferred-OK. Future validation task.                                |
| 3   | AoF-resolved validation data absent                              | Deferred-OK. Phase-1 limitation correctly acknowledged.             |
| 4   | M107 secant-ogive arc centre spot-check                          | Deferred-OK for derivation; must be performed at integration.       |
| 5   | Boattail angle convention (full vs. half taper)                  | Integration-time blocker — must be resolved before code is written. |

**Verdict: PASS** (all five items correctly framed; item 5 is integration-time, not derivation-time).

______________________________________________________________________

### 6. Tier-2 ogive spray formula

Formula: $\\theta^o\_\\text{Tier-2} = 90° - \\arcsin!\\left(\\dfrac{\\sqrt{\\text{CRH}-1/4}}{2,\\text{CRH}}\\right)$

Geometry verified: the argument equals $L_n/(2R^o)$ for a tangent ogive, which is the sine of the surface slope angle at the axial midpoint, so the formula correctly subtracts it from 90° to obtain the normal angle from the axis.

Numerical spot-check:

| CRH | $\\theta^o$ |
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

$C^b\_\\text{eff} = C^c \\cdot (t_b / L_c)$: geometrically motivated (explosive column over base thickness), units correct, impact small (4% of steel mass). NWC TP 7124 rarefaction reduction $k^b$ partially compensates for the approximation's limitations. Correctly flagged as open item 1.

**Verdict: PASS** (acknowledged engineering approximation).

______________________________________________________________________

### 8. Cross-consistency with target-area-profile derivation

Both derivations produce the same geometry factor $A_p / (2\\pi s^2 \\cdot 2\\sin\\theta^z \\delta)$. The target-area-profile eq. (P4) and the 3D geometry §3.8 boxed formula are identical in form with $\\Theta \\leftrightarrow \\theta^z$.

**Verdict: PASS.**

______________________________________________________________________

## Corrections applied between passes

**Issue 1 — RESOLVED: AoF rotation geometry (§3.7 and §5)**

The original derivation wrote $\\hat{u}\_\\text{fwd} = (\\cos\\alpha, 0, -\\sin\\alpha)$ with $\\alpha = 90° - \\text{AoF}$, which inverted the forward-axis direction at all AoF values. The correction replaces this with:

$$\\hat{u}\_\\text{fwd} = (\\cos(\\text{AoF}),\\ 0,\\ -\\sin(\\text{AoF}))$$

and rewrites the rotation matrix as $R_y(\\text{AoF})$. The expanded $v\_{g,z}$ components are now:

$$v\_{g,z} = -\\sin(\\text{AoF})\\cos\\theta^z + \\cos(\\text{AoF})\\sin\\theta^z\\sin\\phi$$

The special-case bullets are corrected: AoF=0° (horizontal shell) correctly shows cylinder spray going horizontal or upward (never reaching the ground in the straight-line model); AoF=90° (vertical shell) correctly gives $v\_{g,z} = -\\cos\\theta^z$ independent of $\\phi$.

The §5 circular-symmetry derivation is rewritten. At AoF=90° the ogive zone gives hit positions $(h_b\\tan\\theta^z\\sin\\phi, h_b\\tan\\theta^z\\cos\\phi)$ — a ring of radius $h_b\\tan\\theta^z$ independent of $\\phi$. Cylinder fragments ($\\theta^z = 90°$) have $v\_{g,z} = 0$ and do not reach the ground, which is physically correct. Base fragments ($\\theta^z = 165°$) have $v\_{g,z} > 0$ and travel upward, also correct for a vertically-arriving shell.

**Issue 2 — RESOLVED: Cylinder $V_0$ in §6 (physical plausibility)**

The original table showed $M^c/C^c = 1.89$ and $V_0^c = 982$ m/s. The formula at $V_g = 2440$ m/s gives $1578$ m/s. The value 982 m/s was computed from total-shell M/C ($= 5.52$), inconsistent with the zone-local approach stated in §3.4. The table entry is corrected to $V_0^c = 1578$ m/s, and the accompanying note is rewritten to:

- Explain why the high cylinder velocity is physically correct (low zone-local M/C = 1.89, cylinder holds most of the interior explosive)
- Correctly interpret the BRL 126 panel measurements as drag-attenuated velocities at range, not initial velocities
- Explain the ratio $V_0^c / V_0^o \\approx 2.7$ as the mechanism behind cylinder fragment dominance at side panels

______________________________________________________________________

## Deferred items (non-blocking)

- **Mott $\\mu^z$ unit check** absent from §4 table. Add at integration, referencing Gold (2017) PAFRAG eq. 16.
- **Notation collision $\\gamma$**: used for both fragment arrival angle and Mott material constant. Rename the Mott constant to $\\Gamma_M$ or $B_M$ at integration.
- **$v\_{g,z} \\ge 0$ guard**: implementation must skip the hit-position formula when $v\_{g,z} \\ge 0$. Already documented in §3.7.
- **Boattail angle convention** (open item 5): resolve full vs. half-taper interpretation in `boattail_angle_deg` before writing implementation code.
- **M107 secant-ogive spot-check** (open item 4): perform before publishing M107 spray angle.
- **Tier-2 CRH = 6.0 limitations entry**: add to main `.qmd` at integration.
- **$R\_{50}$ recalibration**: the new $s^{-2}$ geometry factor (vs. old $s^{-1}$) changes absolute hit counts; recalibrate against TM 9-1901 once the new factor is integrated.

______________________________________________________________________

## Overall verdict

**PASS** — both blocking issues corrected in the derivation. The corrected §3.7 AoF rotation geometry is internally consistent and verified for AoF = 0°, 25°, 45°, and 90°. The corrected §6 cylinder $V_0 = 1578$ m/s is consistent with the formula and the zone-local $M^c/C^c = 1.89$. All other areas of the derivation were sound in the initial pass and remain unchanged.

The integration pass may proceed. Deferred items listed above must be addressed during integration; none require a further derivation revision.
