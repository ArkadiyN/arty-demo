---
title: "Engineering Model for Design of Explosive Fragmentation Munitions"
authors: "Vladimir M. Gold"
publication: "ARDEC Technical Report ARAET-TR-07001"
date: "February 2007"
source_type: "DTIC Technical Report (AD-EA403 106)"
---

# Card: Gold 2007 — CALE-MOTT Fragmentation Model

**Source**: ADA462991.md (ARDEC ARAET-TR-07001, Gold 2007).
No numeric data tables; figures only.

## Framework & Integration

Modified Mott model (`## MOTT CODE FRAGMENTATION MODELS`) integrates three-dimensional CALE hydrodynamics code with analytical fragmentation. CALE provides shell deformation, velocity, and radius at break-up; Mott provides fragment size and velocity distributions.

### Material and EOS Specification

- **Explosive**: Jones-Wilkins-Lee (JWL) equation of state, calibrated with copper cylinder shock-compression tests
- **Steel shell**: Johnson-Cook strength model, shock-Hugoniot equation of state from chemical-equilibrium detonation analysis (JAQUAR)
- **Copper shaper liner**: Experimental data for metals; constitutive behavior modeled Stüenger-Quinney plastic work conversion

## Fragment Size Distribution

**Basic Mott** (Eq. 1): $$N(m) = N_0 \exp\left(-\frac{m}{\mu}\right)$$
where $N(m)$ = number of fragments > mass $m$; $N_0$ = total fragments; $\mu$ = average fragment mass.

**Mott framework** (Eqs. 2–3):
- Average fragment circumferential length: $$v_r = \frac{2\pi\mu}{\rho a\gamma}$$
- Average fragment mass: $$\mu = \rho a^2\gamma$$

where $\rho$ = density, $a$ = strength, $\gamma$ = semi-empirical constant (no value specified).

**Modified ring-averaged** (Eq. 14): $$N(m) = N_0 e^{-\frac{m}{\mu}}$$

**Ring-segment-averaged** (Eq. 17): Accounts for fragment-mass variation along shell length due to geometry; detailed form incomplete in extraction.

## CALE-MOTT Velocity-Expansion Coupling

Fragment velocity couples to shell expansion ratio via CALE results:
- **Break-up occurs at**: V/V₀ = 3.1 (average expansion at critical fracture strain; `critical fracture strain at the moment of the shell break-up is expressed in terms of the high explosive detonation products volume expansions, the 'average' volume expansion at the time of the shell break-up is then approximately one-half of the value of volume expansions of the fully fragmented shell, hence V/VO =3.1`)
- **Fully fragmented**: V/V₀ ≈ 6.2 (at ~19.8 μs, when detonation products first escape; `the entire shell is fully fragmented`)

Axial and radial velocity components decomposed from CALE outputs (Eqs. 9–10):
$$v_z = v_0 \cos\theta, \quad v_r = v_0 \sin\theta$$

where $\theta$ is fragment angle; $v_0$ radial expansion velocity at break-up.

## Experimental Validation

**Charge A (Figure 3, Figure 5)**: Fragment velocity distribution vs. spray angle $\psi$ (12° and 30°); cumulative fragments vs. normalized mass $m/\mu$ for varying $\gamma$.

**Charge B (Figure 9, Figure 10)**:
- **Figure 9**: Fragment velocity distribution vs. spray angle $\psi$ — two scenarios: instantaneous fracture at t=13 ps (V/V₀=3) and t=30 ps (V/V₀=15). V/V₀=3 case shows better agreement with experimental radiographic data.
- **Figure 10**: Cumulative fragment count vs. mass $m$ (grams); experimental recovery via magnetic/vacuum separation from sawdust (>99.8% recovery). Eq. (14) over-predicts; Eq. (17) with $\gamma$=14 shows excellent agreement (error −7.3%).

## Validity & Scope

- **Geometry**: Cylindrical and curved (hemispherical nose) shell sections; difference in fragment sizes between surfaces explicitly modeled.
- **Process model**: Random surface-fracture growth under high-strain-rate plastic deformation, driven by detonation-product pressure.
- **Assumptions**: Instantaneous break-up at V/V₀=3.1; post-break-up velocity gains (escape of detonation products) negligible.
- **Test basis**: Arena (walling) tests and high-speed photography; flash radiography and sawdust fragment recovery.

## Source

No closure invariants are checkable in this source — all primary data are presented in figures, not tables, and no numeric series has a stated arithmetic relation. Source PDF not retained in directory.
