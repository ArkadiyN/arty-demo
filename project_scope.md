# WW2 Field Artillery — Subject Matter Scope

## Goal

Demonstrate how field artillery guns operated in WW2 and what impact they had
on a battlefield. Scope: a single battery conducting HE fire missions.

## In Scope

### Equipment

- **Artillery pieces** — caliber, charge system, elevation limits, rate of
  fire, low- vs. high-angle capability
- **HE shells** — single shell type; mass, fragmentation characteristics
- **Fuses** — PD, Delay (incl. ricochet), Time (airburst)

### Errors

- **Systematic error** — met, propellant temp, barrel wear, survey → shifts
  Mean Point of Impact (MPI)
- **Random dispersion** — Probable Error (range + deflection), beaten zone
- **Registration** — correcting systematic error against a known point

### Firing technique

- **Fire mission chain** — Observer (FO) → FDC → gun line
- **Planned fires** — pre-surveyed targets, firing data computed in advance
- **Observed fires** — FO adjusts rounds onto target in real time;
  **bracketing** (over/short, left/right) to walk rounds on
- **Destruction mission** — precision adjustment until a point target is hit
- **Rate of fire** → mission time

### Trajectory

- Modified point-mass ballistics (drag, gravity, charge → range/elevation)
- High- vs. low-angle solutions for the same range; time of flight

### Impact

- **Blast wave** — overpressure vs. distance; ground vs. airburst profile
- **Fragmentation field** — fuse-dependent pattern, lethal area
- **Fortification destruction** — penetration/damage of earth, timber, and
  concrete works (empirical formulas, discrete damage states)
- **Target types** — standing/prone/foxhole infantry, gun crew, soft vehicle
  (dimensions + hardness threshold)
- **Cover** — foxhole, trench, bunker, reverse slope

## Deferred / Out of Scope

- **Armor — permanently out.** No steel plate, no kinetic AP penetrators, no
  vehicles as hard targets (anti-armor firewall: `expansion-scope.md`,
  Track C)
- **Direct laying** — deferred; no new machinery once ballistics + LOS +
  point-target damage exist, but needs empirical hit-probability data
- Smoke, incendiary, illumination, shrapnel, canister (may add later)
- Time on Target; battalion/multi-battery coordination

## Tool Flow

- **Scenario inputs** — who, what, where, how
- **Instrumentation** — event log of orders, shots, observations, adjustments
- **Mission visualization** — impact areas with effects on a map
- **Learning tools** — frag field, blast, trajectories

## Roadmap

Phase 1 (fragmentation field: physics models for fragment count, field
shape, fragment energy, target hit/casualties + demo app) is in progress.
The expansion — HLD, options, risks — lives in **`expansion-scope.md`**:

- **Track A** — fire missions: ballistics, fuses, dispersion/error budget,
  multi-shell effects aggregation, FO/FDC choreography (Phases 2a, 2d, 2e)
- **Track B** — terrain: analytic surfaces → DEM relief, fragment masking,
  map visualization (Phases 2b, 2c)
- **Track C** — fortification destruction & blast, extended target
  catalogue (Phase 2f)
- **Track D** — scenario capstone integrating all tracks (Phase 3),
  grown as a walking skeleton from Phase 2a
