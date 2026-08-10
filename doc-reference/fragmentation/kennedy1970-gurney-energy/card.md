# Kennedy 1970 — Gurney Energy of Explosives

**Source:** Sandia Laboratories Report SC-RR-70-790 (December 1970)\
**Author:** J. E. Kennedy, Sandia Laboratories\
**Blob:** `source.pdf` (1.9 MB, 29 pp.); SHA256 available on request\
**Focus:** Final velocity imparted to driven metal by detonating explosives; energy partition between gas and metal phases.

## Key Contribution

Kennedy reviews and extends the Gurney method, a rational energy/momentum-balance approach to estimate final metal velocities from explosive/metal assemblies. Derives explicit algebraic expressions for several common geometries. Establishes that Gurney energy E (kinetic energy per unit explosive mass) is ~0.7× the chemical heat of detonation ΔH_d for most explosives, enabling estimation of E from calorimetric data alone.

**Note:** The method yields final velocity only; acceleration-phase dynamics are explicitly excluded (see "Not in Source" below).

## Gurney Method Core Relations

**Linear gas velocity profile assumption** (sec. 2): Detonation product gases expand with linearly-varying velocity from 0 at centerline to peak v_gas,max at driven metal surface; metal moves at constant velocity v throughout its thickness.

**Energy balance for unit area** (line 131):
$$CE = \frac{1}{2}Mv^2 + \int_0^{y_0} \frac{1}{2}P_e(\dot{y})[v_{\text{gas}}(y)]^2 dy$$

Momentum balance (line 134):
$$0 = -Mv - \int_0^{y_0} P_e(\dot{y})[v_{\text{gas}}(y) - v] dy$$

Integration yields final metal velocity in open-faced sandwich (lines 139–144):
$$v = \sqrt{2E} \left(1 + 2\frac{M}{C}\right)^{-1/2}$$

## Standard Gurney Equations by Geometry

**Flat Sandwich** (symmetric, line 168):
$$v = \sqrt{2E} \left(1 + \frac{M}{C}\right)^{-1/2}$$

**Cylindrical Case** (line 173):
$$v = \sqrt{2E} \left(1 + \frac{M}{2C}\right)^{-1/2}$$

**Spherical Case** (line 177):
$$v = \sqrt{2E} \left(1 + \frac{2M}{3C}\right)^{-1/2}$$

**Asymmetric (two-plate) Sandwich** (line 189):
$$v = \sqrt{2E} \left[\frac{1 + 2(N/C)}{3(1 + (N/C)/2)} + \frac{M}{C}\right]^{-1/2}$$

**Symbol definitions** (from Fig. 3):

- $v$ = driven metal velocity (final state)
- $E$ = Gurney specific energy (kcal/g); characteristic per explosive
- $M$ = total driven metal mass
- $C$ = total explosive mass
- $N$ = total tamper (reaction mass) mass
- $M/C$ = loading factor (dimensionless)

**Characteristic velocity:** $\sqrt{2E}$ (velocity units, mm/μsec) tabulated per explosive in Table 2.

## Table 2 — Energies and Specific Impulses of Explosives

Lists $\sqrt{2E}$ (mm/μsec) and $I_{\text{sp}}$ (dyne-sec/g explosive) for common explosives at standard configurations, plus efficiency $E/\Delta H_d$ (kcal/g ratio). RDX: $\sqrt{2E} = 2.83$ mm/μsec; Comp B: $2.71$ mm/μsec; TNT: $2.37$ mm/μsec; HMX: $2.97$ mm/μsec; PETN: $2.93$ mm/μsec; PBX-9140: $2.90$ mm/μsec. Tabulated energy efficiency $E/\Delta H_d$ ranges 0.61–0.76 for high explosives, 0.56 for nitromethane.

**Empirical energy estimation** (line 476):
$$E \approx 0.7 \Delta H_d$$

where $\Delta H_d$ is measured heat of detonation (kcal/g). Validated by computer calculations (Appendix B) across explosives with varying equation-of-state properties; systematic error small (\<3%) over typical M/C range.

## Impulse Relations

**Specific impulse** (momentum per unit explosive mass, line 338):
$$I_{\text{sp}} = \frac{Mv}{C}$$

**For unconfined surface charge** (M/C >> 1, line 348):
$$I_{\text{sp}} \approx \sqrt{1.5 E}$$

**With tamper** (line 371; N/C = tamper ratio):
$$I_{\text{sp}} = I_{\text{sp,bare}} \sqrt{1 + 2(N/C)}/(1 + (N/C))$$

where bare-charge impulse is given by Eq. (12).

## Applicability Range & Limitations

**Recommended M/C restriction** (Table 1, item 1): $0.2 < M/C < 10$ for velocity calculations; impulse calculations acceptable for $M/C > 0.2$.

**Acceleration phase not modeled** (Table 1, item 2): "Gurney method is not capable of analyzing motion during acceleration." Acceleration completed after gas expansion to 2× original charge volume (normal detonation incidence) or 7× (grazing incidence, Appendix B, line 762–763). Final velocity only attained if no external forces applied during acceleration phase.

**Gross assumptions** (sec. 2, lines 107–109): Linear velocity profile and constant-density gas assumption deviate significantly from gasdynamic reality; typically affect correlation only at extreme M/C (M/C > 10 or M/C < 0.2). Free-surface effects (open-faced configuration) can overestimate velocity by ~7% due to rarefaction-wave interaction.

**Other limitations** (Table 1): One-dimensional motion only; hoop-stress reduction (~few percent at M/C ~2.5); metal spallation possible for M/C < 2 with high-density materials; early case fracture can reduce velocity by ≤10%.

## Velocity during Radial Expansion

**Not in Source.** Kennedy explicitly excludes transient acceleration-phase kinematics. The method is predicated on energy and momentum balance in the final state and assumes linear velocity profile in the gas phase. No information is provided on:

- Wall velocity as a function of expansion ratio (V/V₀)
- Acceleration history during expansion
- Time-dependent velocity profile
- Strain-rate effects or material strength coupling during acceleration

Only the **final velocity** (after acceleration completes, typically after 2× to 7× expansion depending on incidence angle) is predicted by this method.

## Source Summary

Kennedy's Gurney method is a closed-form energy-partition framework yielding final metal velocities for symmetric and asymmetric explosive/metal geometries. The method is calibrated to experimental shell and cylinder acceleration data and does not address transient dynamics or radial-expansion kinematics. For shell fragmentation studies, it provides the velocity *endpoint* (end of acceleration) but not the path to that endpoint.
