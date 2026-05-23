# WW2 Field Artillery — Subject Matter Scope

## Goal

Demonstrate how field artillery guns operated in WW2 and what
impact they had on a battlefield. Scope is limited to a single
battery conducting HE fire missions.

## In Scope

### Equipment

- **Artillery pieces** — caliber, charge system, elevation limits,
  rate of fire, low-angle vs. high-angle capability
- **HE Shells** — single shell type; properties (mass,
  fragmentation characteristics)
- **Fuses** — PD, Delay (incl richochet), Time (airburst)

### Errors

- **Systematic error** — met conditions, propellant temp, barrel
  wear, survey error → shifts Mean Point of Impact (MPI)
- **Random dispersion** — Probable Error (range + deflection),
  beaten zone geometry
- **Registration** — correcting systematic error against a known
  point

### Firing Technique

- **Fire mission chain** — Observer (FO) → FDC → Gun line
- **Planned fires** — pre-surveyed targets, firing data computed
  in advance
- **Observed fires** — FO adjusts rounds onto target in real time
- **Destruction mission** — precision adjustments to ensure target is hit
- **Bracketing** — over/short, left/right corrections to walk
  rounds onto target
- **Rate of fire** — mission time

### Trajectory

- Modified point-mass ballistics (drag, gravity, charge →
  range/elevation)
- High-angle vs. low-angle solutions for same range
- Time of flight

### Impact

- **Blast wave** — overpressure vs. distance, ground vs. airburst
  profile
- **Fragmentation field** — fuse-dependent pattern (ground burst
  vs. airburst), lethal area
- **Target types** — standing/prone/foxhole infantry, gun crew,
  soft vehicle (dimensions + hardness)
- **Cover** — foxhole, trench, bunker, reverse slope

## Deferred / Out of Scope

- Smoke, incendiary, illumination, shrapnel, canister (may add later)
- Direct fire (may add later)
- AP / HEAT (No anti-armor action)
- Time on Target (TOT)
- Battalion-level or multi-battery coordination

## Tool Flow

- **Scenario inputs** - who, what, where, how
- **instrumentation** - logs for what exactly happens, including simulation of adjustments, orders and observations
- **mission visualization** - impact areas with effects on a map
- **learning tools visualization** - frag field/mine action, trajectories

## Phase 1 MVP

### Fragmentation Field

- establish physics model needed for calculating number of fragments;
- establish physics model needed for calculating shape of frag field;
- establish physics model needed for calculating energy of fragments at different points of trajectory;
- assume flat trajectory of fragments;
- assume no obstacles (flat surface, absorbs all fragments);
- demo app to diplay the outcome given the parameters;
