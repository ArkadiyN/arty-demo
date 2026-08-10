# Derivation — Four-Zone Shell Fragmentation Model (3D Geometry)

**Author:** modeler agent (transcribed to file by main agent)
**Date:** 2026-05-31
**Status:** derivation pass — no implementation code
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Scoping:** `experiment/fragmentation-field/updates/frag-field-3d-geometry/scoping.md`
**Bundled work:** `experiment/fragmentation-field/updates/target-area-profile/scoping.md`

______________________________________________________________________

## 1 · Problem statement

The existing model (notebook §3–§6) treats the HE shell as a single cylindrical Gurney–Mott source: one $V_0$, one $\mu$, one equatorial spray belt at 90° from the forward axis. This derivation extends it to four distinct zones — ogive, cylinder, boattail, base plate — each with zone-local Gurney velocity, Mott distribution, and spray elevation angle. Coupled with angle of fall (AoF), the four zones map onto distinct lobes on the ground plane. The presented-area replacement $A_p(\gamma, \text{posture})$ (already scoped in `target-area-profile/scoping.md`) is derived here and integrated into the field computation.

______________________________________________________________________

## 2 · Notation

| Symbol          | Definition                                                                      |
| --------------- | ------------------------------------------------------------------------------- |
| $D$             | Shell calibre (m)                                                               |
| $R^o$           | Ogive outer arc radius (m); `ogive_outer_R`                                     |
| $R^o_i$         | Ogive inner arc radius (m); `ogive_inner_R`                                     |
| $L_n$           | Ogive axial length (m); `ogive_len`                                             |
| $L_c$           | Cylinder axial length (m); `cylinder_len`                                       |
| $L_t$           | Boattail axial length (m); `boattail_len`                                       |
| $t_b$           | Base plate thickness (m); `base_thickness`                                      |
| $t_w$           | Cylinder wall thickness (m); `wall_t`                                           |
| $\theta_{bt}$ | Boattail half-taper angle (deg); `boattail_angle_deg`                           |
| $M_s$           | Total steel mass $= m_\text{total} - m_\text{filler} - m_\text{ded}$ (kg) |
| $M^z$           | Zone steel mass (kg)                                                            |
| $C^z$           | Zone explosive allocation (kg)                                                  |
| $V_g$           | Gurney characteristic velocity $= \sqrt{2E}$ (m/s)                             |
| $V_0^z$         | Zone initial fragment velocity (m/s)                                            |
| $k^z$           | Zone Gurney reduction factor (dimensionless, default 1.0)                       |
| $\mu^z$        | Zone Mott half-mass parameter (kg)                                              |
| $N_0^z$         | Zone total fragment count                                                       |
| $\theta^z$     | Zone spray elevation angle from forward shell axis (deg)                        |
| $\alpha$       | Shell axis tilt $= 90° - \text{AoF}$ (deg from vertical)                       |
| $\gamma$       | Fragment arrival angle from horizontal (rad)                                    |
| $A_p$           | Target presented area (m²)                                                      |
| $\rho_s$       | Steel density = 7850 kg/m³                                                      |

______________________________________________________________________

## 3 · Derivations

### 3.1 Zone mass partitioning — Tier-1 (arc geometry)

For shells with drawing-derived zone geometry ($R^o$, $R^o_i$, $L_n$, etc.), zone masses are computed by numerical integration of the annular cross-sectional area.

**Ogive.** The outer profile is a circular arc of radius $R^o$. Place the arc centre at $(x_c^o, r_c^o)$ such that the arc is tangent to the cylinder outer radius $D/2$ at $x = 0$ (shoulder) and passes through the tip radius $r_\text{tip}$ at $x = L_n$:

$$r_o(x) = r_c^o + \sqrt{(R^o)^2 - (x - x_c^o)^2}$$

The arc centre $x_c^o$ and $r_c^o$ are found by solving the two-point conditions simultaneously. Similarly for the inner profile with radius $R^o_i$:

$$r_i(x) = r_c^i + \sqrt{(R^o_i)^2 - (x - x_c^i)^2}$$

The ogive steel mass is:

$$M^o = \rho_s \int_0^{L_n} \frac{\pi}{4}\bigl[r_o(x)^2 - r_i(x)^2\bigr],dx \approx \rho_s \sum_{k=1}^{200} \frac{\pi}{4}\bigl[r_o(x_k)^2 - r_i(x_k)^2\bigr],\Delta x$$

using 200 equal-width slices (midpoint rule), $\Delta x = L_n/200$.

**Cylinder.** Uniform wall — exact analytic formula:

$$M^c = \rho_s \pi t_w (D - t_w) L_c$$

**Boattail.** Linear taper from outer diameter $D$ at $x = 0$ to base outer diameter $D_b$ at $x = L_t$, with inner bore tapering from $D - 2t_w$ toward `boattail_inner_dia`. Treat as a frustum of a hollow cone, integrable analytically or via 200 slices consistently with the ogive:

$$M^t = \rho_s \sum_{k=1}^{200} \frac{\pi}{4}\bigl[r_{t,o}(x_k)^2 - r_{t,i}(x_k)^2\bigr],\Delta x_t, \quad \Delta x_t = L_t/200$$

**Base plate.** Solid disk (the base plate has no significant through-bore):

$$M^b = \rho_s \frac{\pi D^2}{4} t_b$$

**Normalisation.** The four zone masses are rescaled so their sum equals $M_s$ exactly, absorbing any numerical integration error (typically $< 0.5%$):

$$\hat{M}^z = M^z \cdot \frac{M_s}{M^o + M^c + M^t + M^b}$$

______________________________________________________________________

### 3.2 Zone mass partitioning — Tier-2 (fraction defaults)

When arc geometry is absent (`ogive_outer_R is None`), apply fixed fractions to $M_s$:

| Zone     | With boattail | Without boattail (`has_boattail=False`) |
| -------- | ------------- | --------------------------------------- |
| Ogive    | 0.53          | 0.53                                    |
| Cylinder | 0.27          | 0.42                                    |
| Boattail | 0.15          | 0.00                                    |
| Base     | 0.05          | 0.05                                    |

These fractions derive from the empirical M1/M107 Tier-1 split; see scoping §Decision 5.

______________________________________________________________________

### 3.3 Per-zone explosive allocation

The filler $C_\text{total} = m_\text{filler}$ is distributed among zones in proportion to their share of the shell interior volume.

**Tier-1.** Integrate interior (bore) volume per zone:

$$V_\text{int}^z = \int_z \frac{\pi}{4} r_i(x)^2,dx$$

The cylinder interior is $V_\text{int}^c = \pi (D/2 - t_w)^2 L_c$. The ogive interior is computed from the inner arc profile by the same 200-slice sum. The boattail interior tapers similarly. The base plate has no cavity: $V_\text{int}^b = 0$.

Each zone receives:

$$C^z = C_\text{total} \cdot \frac{V_\text{int}^z}{\sum_{z'} V_\text{int}^{z'}}$$

Since $V_\text{int}^b = 0$, the base receives no direct filler allocation from this formula. To compute a physically meaningful $V_0^b$, an **equivalent-column convention** is adopted: the base plate is driven by an explosive column of effective mass $C^b_\text{eff} = C^c \cdot (t_b / L_c)$, representing the fraction of the adjacent explosive column that acts on the base face. This is an acknowledged approximation (see §7 Open items).

**Tier-2.** Use the same zone fractions as the steel mass allocation as a first approximation (interior volume $\approx$ proportional to steel mass for uniform-wall designs), with the same base convention.

______________________________________________________________________

### 3.4 Per-zone Gurney velocity

Per scoping Q1, the cylinder Gurney formula is applied with zone-local $M^z / C^z$:

$$V_0^z = k^z \cdot \frac{V_g}{\sqrt{M^z/C^z + 1/2}}$$

where $V_g = \sqrt{2E}$ is the Gurney characteristic velocity from `shell.filler.gurney_const` and $k^z$ is the zone reduction factor (default 1.0 for all zones except base).

**Base plate reduction (scoping Q2):** The NWC TP 7124 rarefaction mechanism reduces the effective driving pressure at the closed end. The reduction factors are:

- M1 (105mm): $k^b = 0.75$
- M107 (155mm): $k^b = 0.70$
- Tier-2 default: $k^b = 0.75$

These are stored on `ZoneParams.gurney_reduction_factor` (default 1.0) and applied as a multiplier. They are not hard-coded — a shell can override via `ShellParams`.

______________________________________________________________________

### 3.5 Per-zone Mott parameters

The existing Gold (2017) / PAFRAG formula is applied with zone-local inputs. From the current notebook, $\mu$ (the half-mass parameter) follows:

$$\mu^z = \frac{1}{8}\left(\frac{r_{bu}^z}{V_0^z}\right)^2 \gamma^2 \sigma_f / \rho_s$$

where $r_{bu}^z$ is the zone break-up radius at the moment of case rupture (the initial inner radius scaled by the 3× expansion criterion: $r_{bu}^z = 3 r_{i,\text{mean}}^z / \sqrt{3} \approx \sqrt{3} r_{i,\text{mean}}^z$, following the existing notebook convention).

**Zone-mean inner radii:**

- Cylinder: $r_{i,\text{mean}}^c = D/2 - t_w$
- Ogive: $r_{i,\text{mean}}^o$ = mean of inner arc profile over $[0, L_n]$ (from Tier-1 integration) or $0.75 \times (D/2 - t_w)$ (Tier-2 scaling)
- Boattail: $r_{i,\text{mean}}^t$ from integration or $0.75 \times (D/2 - t_w)$ (Tier-2)
- Base: $r_{i,\text{mean}}^b = D/2 - t_b$ (outer radius minus base thickness, appropriate for plate expansion)

**Zone wall thickness (Tier-2 scaling):**

| Zone     | $t_w^z$                                            |
| -------- | -------------------------------------------------- |
| Cylinder | $t_w$ (given)                                      |
| Ogive    | $0.75 \times t_w$                                 |
| Boattail | $2.0 \times t_w$                                  |
| Base     | `base_thickness` (or $2.5 \times t_w$ for Tier-2) |

$N_0^z$ follows from $\mu^z$ and $M^z$ via the existing Mott CDF as in the notebook.

______________________________________________________________________

### 3.6 Per-zone spray elevation angle

**Cylinder:** Exact by symmetry — uniform hoop expansion perpendicular to axis:

$$\theta^c = 90°$$

**Boattail:** The boattail outer surface is a linear cone of half-taper angle $\theta_{bt}$. The outward surface normal of a cone with half-angle $\theta_{bt}$ from the axis makes angle $(90° + \theta_{bt})$ with the forward axis. Using the midpoint taper:

$$\theta^t = 90° + \theta_{bt}$$

For M1: $\theta^t = 90° + 9.267°/2 \approx 94.6°$\
For M107: $\theta^t = 90° + 8.0°/2 = 94.0°$

(Note: the boattail_angle_deg in `ShellParams` is the full taper angle; the half-angle used here is half that value.)

**Base plate:** Fragments from the base plate are driven rearward. The spray angle is set to:

$$\theta^b = 165°$$

This is a phenomenological value consistent with observed base-spray directionality in artillery fragmentation (strongly rearward, but not exactly 180° due to the finite base diameter). It is flagged as an engineering convention pending dedicated literature.

**Ogive — Tier-1.** The outer profile is a circular arc of radius $R^o$ with known centre $(x_c^o, r_c^o)$. At the axial midpoint $x_\text{mid} = L_n/2$, the outward surface normal points radially outward from the arc centre. The angle of this normal from the forward (negative-$x$) axis is:

$$\theta^o = 90° - \arctan!\left(\frac{r_o(x_\text{mid}) - r_c^o}{x_\text{mid} - x_c^o}\right)$$

(taking care of sign conventions so $\theta^o < 90°$, i.e., the ogive sprays forward of equatorial).

**Ogive — Tier-2 (tangent-ogive approximation).** For a tangent ogive of CRH $= R^o/D$, the arc is tangent to the cylinder at the shoulder. The nose length is $L_n = D\sqrt{\text{CRH} - 1/4}$. At the midpoint $x = L_n/2$ the slope of the outer surface is:

$$\left.\frac{dr}{dx}\right|_{x=L_n/2} = \frac{L_n/2}{\sqrt{(R^o)^2 - (L_n/2)^2}}$$

Since $\arctan(\text{slope}) = \arcsin(L_n / 2R^o) = \arcsin!\left(\frac{\sqrt{\text{CRH}-1/4}}{2,\text{CRH}}\right)$, the normal angle is:

$$\boxed{\theta^o_\text{Tier-2} = 90° - \arcsin!\left(\frac{\sqrt{\text{CRH}-1/4}}{2,\text{CRH}}\right)}$$

For the nominal Tier-2 ogive length, $L_n = 4.0 \times D$ is assumed (representative of WW2 HE shells; flagged as an assumption).

______________________________________________________________________

### 3.7 Angle-of-fall ground projection

Define the ground-frame coordinate system: $x_g$ is positive downrange (direction of fire), $y_g$ is cross-range, $z_g$ is vertical (positive up). The burst occurs at $(0, 0, h_b)$.

The shell axis points in the direction of arrival. The shell arrives **nose-first and downward**. Let $\text{AoF}$ (angle of fall) be measured from horizontal, so AoF = 90° for a vertically descending shell and AoF ≈ 20°–35° for medium-range fire. The forward shell-frame $+x$ direction maps to the ground-frame direction:

$$\hat{u}_\text{fwd} = (\cos(\text{AoF}),\\ 0,\\ -\sin(\text{AoF}))$$

Verification: AoF = 90° (vertical shell) → $\hat{u}_\text{fwd} = (0, 0, -1)$ (straight down) ✓; AoF = 0° (horizontal shell) → $\hat{u}_\text{fwd} = (1, 0, 0)$ (horizontal downrange) ✓.

The auxiliary angle $\alpha = 90° - \text{AoF}$ (retained in §2 notation for reference) satisfies $\cos(\text{AoF}) = \sin\alpha$ and $\sin(\text{AoF}) = \cos\alpha$.

A fragment leaving zone $z$ at polar angle $\theta^z$ (from forward axis) and azimuth $\phi$ around the axis has shell-frame direction:

$$\hat{v}_\text{shell} = (\cos\theta^z,\\ \sin\theta^z\cos\phi,\\ \sin\theta^z\sin\phi)$$

Rotating to the ground frame by $R_y(\text{AoF})$ (rotation by AoF about the cross-range $y$-axis):

$$\begin{pmatrix} v_{g,x} \\ v_{g,y} \\ v_{g,z} \end{pmatrix} = \begin{pmatrix} \cos(\text{AoF}) & 0 & \sin(\text{AoF}) \\ 0 & 1 & 0 \\ -\sin(\text{AoF}) & 0 & \cos(\text{AoF}) \end{pmatrix} \begin{pmatrix} \cos\theta^z \\ \sin\theta^z\cos\phi \\ \sin\theta^z\sin\phi \end{pmatrix}$$

Expanding:

$$v_{g,x} = \cos(\text{AoF})\cos\theta^z + \sin(\text{AoF})\sin\theta^z\sin\phi$$
$$v_{g,y} = \sin\theta^z\cos\phi$$
$$v_{g,z} = -\sin(\text{AoF})\cos\theta^z + \cos(\text{AoF})\sin\theta^z\sin\phi$$

Fragment ground impact position (starting from burst point at height $h_b$, fragment travelling in direction $\hat{v}_g$):

$$x_\text{hit} = -\frac{v_{g,x}}{v_{g,z}} h_b, \qquad y_\text{hit} = -\frac{v_{g,y}}{v_{g,z}} h_b$$

(valid when $v_{g,z} < 0$, i.e., the fragment descends and reaches the ground; when $v_{g,z} \geq 0$ the fragment travels upward or horizontally and does not reach the ground in the straight-line model). The fragment arrival angle below horizontal:

$$\sin\gamma = |v_{g,z}|$$

This $\gamma$ feeds directly into the presented-area calculation §3.8.

**Special cases:**

- $\text{AoF} = 90°$ (vertical shell): $v_{g,z} = -\cos\theta^z$ for all $\phi$. This is constant in $\phi$, so every fragment in a given zone strikes the ground at the same slant from the burst. The hit positions $(x_\text{hit}, y_\text{hit})$ trace a ring of radius $h_b|\cos\theta^z/\cos\theta^z| \cdot \ldots$ — see §5 for the full circular-symmetry argument.
- $\text{AoF} = 0°$ (horizontal shell): $v_{g,z} = \cos(0°)\sin\theta^z\sin\phi = \sin\theta^z\sin\phi$. For cylinder fragments ($\theta^z = 90°$): $v_{g,z} = \sin\phi$, which is zero at $\phi = 0°, 180°$ and non-negative for $\phi \in (0°, 180°)$ — the cylinder spray travels horizontally or upward, never reaching the ground. For the ogive ($\theta^z < 90°$): $v_{g,z}$ depends on $\phi$; fragments with $\sin\phi < 0$ (lower hemisphere) reach the ground forward of the burst. This is the expected physical behaviour for a horizontally-arriving shell.

______________________________________________________________________

### 3.8 Presented-area replacement

From `target-area-profile/scoping.md` Option A, the target presented area (cross-section exposed to a fragment arriving at elevation angle $\gamma$ from horizontal) is:

$$A_p(\gamma, \text{posture}) = w_\perp \bigl(h\cos\gamma + d\sin\gamma\bigr)$$

where $w_\perp$ is body width, $h$ is height, $d$ is depth (all in metres). Named instances:

- `STANDING`: $(w_\perp, h, d) = (0.5, 1.7, 0.3)$ → $A_p(0) = 0.85,\text{m}^2$, $A_p(\pi/2) = 0.15,\text{m}^2$
- `PRONE`: $(w_\perp, h, d) = (0.5, 0.3, 1.8)$ → $A_p(0) = 0.15,\text{m}^2$, $A_p(\pi/2) = 0.90,\text{m}^2$

**Re-derivation of eq. (22).** The existing field equation uses a width-based factor:

$$\text{(old)} \quad \Delta p_k = P_h \cdot \frac{w_\text{target}}{2\pi s \cdot 2\sin\Theta,\delta}$$

where $s$ is slant range (m), $2\sin\Theta,\delta$ is the fractional solid-angle belt of the spray, and $w_\text{target}/(2\pi s)$ is the fraction of the belt circumference subtended by the target width.

The correct generalisation replaces the width-based interception fraction with an area-based one. A fragment crossing a sphere of radius $s$ at the spray-belt location subtends solid angle $d\Omega = \sin\theta,d\theta,d\phi$. The belt solid angle is $\Omega_\text{belt} = 2\pi \cdot 2\sin\theta^z,\delta$ (sr). The target presented area $A_p(\gamma)$ intercepts a fraction $A_p(\gamma)/(\pi s^2)$...

Actually the interception probability per fragment is the ratio of presented area to the area of the shell of radius $s$ covered by the spray belt:

$$P_\text{intercept} = \frac{A_p(\gamma)}{2\pi s^2 \cdot 2\sin\theta^z,\delta}$$

**Unit check:** $A_p$ in m², $s^2$ in m², ratio dimensionless ✓. Compare with old: $w/(2\pi s \cdot 2\sin\Theta,\delta)$ — also dimensionless (m/m). The new form is exact; the old form implicitly assumed the target height equals $s,d\theta$ (i.e., a thin-belt approximation for the height direction).

The updated field contribution per zone per azimuthal strip:

$$\Delta p_k^z = P_h^z(s) \cdot \frac{A_p(\gamma, \text{posture})}{2\pi s^2 \cdot 2\sin\theta^z,\delta}$$

where $P_h^z(s) = 1 - \exp(-N_0^z \exp(-m_{50}/\mu^z) \cdot f_\text{KE}(s))$ is the zone hit-and-kill probability at slant range $s$, computed from the zone Mott distribution and KE threshold (as in the existing model), and $\gamma = \gamma(x_g, y_g)$ is the fragment arrival angle at the ground point.

______________________________________________________________________

## 4 · Unit checks

| Equation                                                                        | LHS units     | RHS units                        | OK? |
| ------------------------------------------------------------------------------- | ------------- | -------------------------------- | --- |
| $M^o = \rho_s \int \frac{\pi}{4}(r_o^2 - r_i^2),dx$                         | kg            | kg/m³ · m² · m = kg              | ✓   |
| $V_0^z = V_g / \sqrt{M^z/C^z + 1/2}$                                           | m/s           | m/s (dimensionless ratio inside) | ✓   |
| $\theta^o = 90° - \arcsin(\ldots)$                                           | degrees       | degrees                          | ✓   |
| $x_\text{hit} = -(v_{g,x}/v_{g,z}) h_b$                                     | m             | (m/s)/(m/s) · m = m              | ✓   |
| $A_p(\gamma) = w_\perp(h\cos\gamma + d\sin\gamma)$                       | m²            | m · m = m²                       | ✓   |
| $\Delta p_k^z = P_h^z \cdot A_p / (2\pi s^2 \cdot 2\sin\theta^z,\delta)$ | dimensionless | m² / m² = dimensionless          | ✓   |

______________________________________________________________________

## 5 · Limit checks and self-consistency

**AoF = 90° → circular symmetry.** When $\text{AoF} = 90°$ (shell arrives vertically):

$$v_{g,x} = \cos(90°)\cos\theta^z + \sin(90°)\sin\theta^z\sin\phi = \sin\theta^z\sin\phi$$
$$v_{g,y} = \sin\theta^z\cos\phi$$
$$v_{g,z} = -\sin(90°)\cos\theta^z + \cos(90°)\sin\theta^z\sin\phi = -\cos\theta^z$$

Key result: $v_{g,z} = -\cos\theta^z$ is **independent of $\phi$** and negative for $\theta^z < 90°$ (ogive) or zero for $\theta^z = 90°$ (cylinder). The cylinder spray ($\theta^z = 90°$) travels entirely horizontally ($v_{g,z} = 0$) and does not reach the ground in the straight-line model — physically correct for a vertically-arriving shell whose equatorial spray goes outward in the horizontal plane.

For the ogive zone ($\theta^z < 90°$), every fragment hits the ground ($v_{g,z} < 0$ for all $\phi$). The hit position is:

$$x_\text{hit} = -\frac{\sin\theta^z\sin\phi}{-\cos\theta^z} h_b = h_b\tan\theta^z\sin\phi$$
$$y_\text{hit} = -\frac{\sin\theta^z\cos\phi}{-\cos\theta^z} h_b = h_b\tan\theta^z\cos\phi$$

The distance from origin $r = \sqrt{x_\text{hit}^2 + y_\text{hit}^2} = h_b\tan\theta^z$ is **constant in $\phi$** — the fragments strike a ring of radius $h_b\tan\theta^z$ centred on the burst. This is a circularly symmetric field ✓. For the base zone ($\theta^z = 165°$): $v_{g,z} = -\cos 165° = \cos 15° > 0$ — base fragments travel upward and do not reach the ground under vertical shell arrival, which is physically correct (the base spray is directed away from the ground when the shell falls straight down). The field magnitude recovers the single-zone model when all zones are merged into one equivalent cylinder within the tolerances of the Mott $\mu$ differences.

**$A_p$ limits:**

- $\gamma = 0$ (horizontal fragment), STANDING: $A_p = 0.5 \times 1.7 = 0.85,\text{m}^2$ ✓
- $\gamma = \pi/2$ (vertical fragment), PRONE: $A_p = 0.5 \times 1.8 = 0.90,\text{m}^2$ ✓

**Zone mass sum:** By construction (post-normalisation), $\sum_z \hat{M}^z = M_s$ exactly.

**Ogive spray angle bounds:** For CRH $\in [4, 12]$:

- CRH = 4: $\theta^o = 90° - \arcsin(\sqrt{3.75}/8) = 90° - \arcsin(0.242) = 90° - 14.0° = 76.0°$
- CRH = 12: $\theta^o = 90° - \arcsin(\sqrt{11.75}/24) = 90° - \arcsin(0.143) = 90° - 8.2° = 81.8°$

Both within [75°, 88°] per spec ✓

______________________________________________________________________

## 6 · Numerical validation — M1 105mm HE

**Given:** caliber $D = 105,\text{mm}$, $M_s = 14.97 - 2.18 - 0.75 = 12.04,\text{kg}$, $m_\text{filler} = 2.18,\text{kg}$, CRH $\approx 6.02$.

> **Revision note (2026-08-08).** The table below previously carried a
> *hand-worked* zone split (ogive 6.50 kg / 54 %, $C^o = 0.38$ kg,
> $V_0^o = 578$ m/s; cylinder 3.25 kg / 27 %, $C^c = 1.72$ kg,
> $V_0^c = 1578$ m/s) that the implementation never reproduced. That example
> assumed the explosive cavity barely enters the ogive. The shipped Tier-1
> integration (`zones.py`, inner arc fitted through the two *drawing* bore
> anchors — shoulder bore and truncated-tip bore — rather than assumed
> shoulder-tangent) puts far more cavity, and far less steel, in the ogive.
> The change is recorded in
> `openspec/changes/archive/2026-06-07-frag-field-3d-geometry/design.md:65`
> ("Initial fractions (ogive 53 %, cylinder 27 %) were based on a
> pre-correction M1 ogive estimate. After fixing the inner-arc two-point fit
> for M1 (ogive 31 %, cyl 45 %) …"), and the live spec
> `openspec/specs/shell-zone-model/spec.md:67` already carries the corrected
> fractions — **only this section was left stale.** The numbers below are the
> shipped ones, regenerated by `checks/zone-v0-ogive-vs-cylinder.py`. This is
> what resolves the scoping-vs-derivation $V_0$ contradiction: no shipped
> quantity is wrong; the 578 / 1578 pair never existed in `zones.py`.

**Zone masses and explosive (Tier-1 integration, shipped `compute_shell_zones`):**

| Zone       | $M^z$ (kg) | Fraction | $C^z$ (kg) | $M^z/C^z$ | $V_0^z$ (m/s) |
| ---------- | ---------- | -------- | ---------- | --------- | ------------- |
| Ogive      | 3.716      | 30.9 %   | 0.841      | 4.42      | 1100          |
| Cylinder   | 5.385      | 44.7 %   | 1.073      | 5.02      | 1039          |
| Boattail   | 2.248      | 18.7 %   | 0.266      | 8.44      | 816           |
| Base plate | 0.690      | 5.7 %    | 0.120 eq.  | 5.73      | 733           |
| **Total**  | **12.040** | **100%** | **2.180**  | 5.52      | 994 (1-zone)  |

$C^o + C^c + C^t = 2.180$ kg $= m_\text{filler}$ exactly (allocation is by
interior volume fraction); $C^b_\text{eff} = C^c\,t_b/L_c = 0.120$ kg is the
*equivalent-column* proxy of §3.3 and is deliberately **not** part of the
partition — the base plate is driven by explosive already assigned to the
cylinder.

**Energy closure (unit check).** With $V_0^z = k^z V_g/\sqrt{M^z/C^z + 1/2}$
the Gurney relation is equivalent to $\tfrac12 (V_0^z)^2 (M^z + C^z/2) = (k^z)^2 C^z E$,
so summing over zones must give $\big(\sum_{z\ne b} C^z + (k^b)^2 C^b_\text{eff}\big)E$.
Computed: $6.691$ MJ vs. $(2.180 + 0.5625\times0.120)E = 2.2477\,E = 6.691$ MJ ✓
(with $E = V_g^2/2$). Partitioning $C$ and $M$ into zones and applying the
cylinder Gurney relation zone-locally therefore conserves the released Gurney
energy exactly, up to the documented base over-allocation of $+3.1\,\%$.

**Ogive-vs-cylinder $V_0$: which zone is faster is set by the drawing, not by a rule.**
$V_0(M/C) = kV_g(M/C + 1/2)^{-1/2}$ is strictly decreasing in $M/C$, so *for a
given* zone $C/M$ the ordering follows immediately. What is **not** a general
truth is the geometric premise. Running the shipped integration across the
registry:

| Shell | $M^o/C^o$ | $M^c/C^c$ | $V_0^o$ | $V_0^c$ | ordering |
| ----- | --------- | --------- | ------- | ------- | -------- |
| 105mm M1 (Tier-1)   | 4.42 | 5.02 | 1100 | 1039 | ogive **faster** (+6 %) |
| 155mm M107 (Tier-1) | 5.95 | 3.21 | 961  | 1266 | ogive **slower** (−24 %) |
| 75mm M48 (Tier-2)   | 7.10 | 7.10 | 885  | 885  | equal (uniform fallback) |

The M1 ogive is *marginally* explosive-rich relative to its own steel (long
CRH-6 cavity, thin ogive wall); the M107 ogive is steel-rich (secant nose,
larger fuze cavity). Neither "the ogive is always faster" (the Q1 scoping
rationale as originally written) nor "the ogive is always slower" (the old
hand example's note) is correct: the sign falls out of the two arc integrals
and flips between shells of the same family. §7's open item 2 is restated
accordingly.

**Comparison with BRL 126 (Tolch 1938, 75 mm M48).** Tolch reports **two**
velocities and they are *both* side-spray, back-computed from the forward
rotation of the side-spray angle with shell remaining velocity: perforating
fragments ≈ 2,7?0 f/s (≈ 835 m/s; the third glyph is unreadable on the held
scan, commonly read 2,750) and penetrating fragments 3,030 f/s (923 m/s)
— grep `duo to the explosive charge averaged` (`tolch-1938.md:146`) and
`Ave. 3030` (line 1654). Tolch attributes the *higher* figure to the
penetrating class's smaller ballistic coefficient, i.e. these are two fragment
*size* classes of one spray, not two sprays. The model's M48 cylinder-zone
$V_0 = 885$ m/s falls inside that 835–923 m/s bracket (+6 % on the perforating
figure, −4 % on the penetrating one) ✓. This is the only $V_0$ anchor BRL 126
supports; it says nothing about nose-vs-side velocity ordering.

**Ogive spray angle (Tier-1):**

Using the shipped `_ogive_arc_centre` integration for M1 CRH 6.02 (Tier-1, the
code path M1 actually uses — not the Tier-2 tangent-ogive formula, which gives
$\approx 78.5°$): $\theta^o \approx 83.5°$ ∈ [75°, 88°] ✓
(`checks/zone-v0-ogive-vs-cylinder.py`, hand-confirmed against `zones.py`'s
arc-centre formula with the M1 drawing constants).

**Spray angles summary for M1:**

| Zone     | $\theta^z$ |
| -------- | ----------- |
| Ogive    | 83.5°       |
| Cylinder | 90.0°       |
| Boattail | 94.6°       |
| Base     | 165.0°      |

______________________________________________________________________

## 7 · Open items

1. **Base plate equivalent-column convention.** The $C^b_\text{eff} = C^c \cdot t_b/L_c$ approximation is geometrically motivated but not literature-sourced. A future librarian pass on base-plate driving pressure (e.g., from shaped-charge literature) could anchor this more rigorously.

1. **Nose-vs-side velocity ordering is unvalidated — no source in hand constrains it.**
    §6 shows the ordering of $V_0^o$ and $V_0^c$ is drawing-dependent and flips
    between M1 and M107. BRL 126 cannot adjudicate it: both of Tolch's velocity
    figures are **side**-spray (perforating ≈ 835 m/s, penetrating 923 m/s,
    two fragment-size classes of the one spray), and no nose-spray velocity is
    reported at all — the nose-spray tables are hit *densities*, not
    velocities. What BRL 126 *does* support is the magnitude check in §6
    (M48 cylinder-zone $V_0 = 885$ m/s inside 835–923 m/s). Closing the
    ordering question needs a source that measures nose- and side-spray
    velocity in the same round; none is held. Until then the zone-local Gurney
    ordering is taken as-computed and is a stated limitation.

1. **AoF-resolved validation data.** None of the three literature sources (BRL 126, NWC TP 7124, SAND92-0243) provide fragment density vs. AoF. Phase-1 validation of the ground-asymmetry prediction is limited to qualitative checks (forward density > rearward at AoF < 90°) and will remain so until empirical data is collected.

1. **Secant ogive arc centre (M107).** The M107 outer ogive is a secant arc defined by two reference points from the drawing. The arc-centre solution is implemented via simultaneous circle equations in the integration code; the resulting $\theta^o$ should be spot-checked against the Tier-2 tangent-ogive formula at equivalent CRH to confirm consistency.

1. **Boattail angle convention.** The spec uses `boattail_angle_deg` as the full taper angle; §3.6 uses the half-angle. The integration pass should clarify and enforce consistent convention in `compute_shell_zones`.
