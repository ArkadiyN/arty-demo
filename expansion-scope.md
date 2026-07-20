# Project Expansion Scope: Fire Missions & Simulated Terrain

Status: scope document — not an implementation plan. Each physics-bearing item
below is a future Workflow B aspect (@modeler + @model-reviewer); this document
names candidate methods without deriving any of them.

## 1. What the expansion adds, conceptually

The current engine answers *"what does one burst do at a known point?"* —
shell registry → four-zone Mott/Gurney fragmentation → P(kill) fields/volumes
on a flat, featureless plane, with burst height and angle-of-fall as free
parameters. The expansion adds the layers that make it a battlefield
simulation:

- **Track A — Fire missions:** *where do the bursts actually land*
  (ballistics + error budget + sheaf), and *what does a volley/mission of many
  bursts do cumulatively*.
- **Track B — Terrain:** the ground stops being `z = 0`. Terrain moves burst
  points, changes angle of fall, masks fragments (reverse slope, defilade),
  and becomes the map canvas for mission visualization.
- **Track C — Fortification destruction & blast:** overpressure and
  penetration effects against static works (and blast casualties), behind an
  explicit anti-armor firewall.
- **Track D — Scenario capstone:** a scenario schema that integrates all
  tracks into end-to-end missions on a map — completing coverage of
  `project_scope.md`, into which this document's roadmap is summarized.

The single-burst pkill field becomes the **kernel**: the expansion is largely
"place many kernels correctly, on real ground, and aggregate them." That
framing keeps `src/arty`'s existing API almost untouched.

**Materiality principle.** Fidelity is judged where it is consumed. The full
four-zone kernel exists to teach single-burst physics; battery-level
questions are dominated by dispersion, which smears metre-scale kernel
structure across a beaten zone many PE wide. Every mission-level component
therefore uses the simplest model whose simplification does not change
mission outcomes within a stated tolerance — and the tolerance is a
modeler-owned number, not a vibe (A0). This is the project's main defense
against fidelity creep and the performance rabbit hole (§10).

## 2. High-level design

```
                         ┌─────────────────────────────────────┐
                         │  app/ mission app + learning tools  │  Streamlit + Plotly (existing stack)
                         └──────────────────┬──────────────────┘
                 ┌───────────────────┬──────┴────────┬──────────────────┐
                 │ mission engine    │ effects       │ instrumentation  │   NEW src/arty modules
                 │ (FO→FDC→guns,     │ aggregation   │ (event log of    │
                 │  adjust/bracket)  │ (multi-burst) │  orders/splash)  │
                 └───────┬───────────┴──────┬────────┴──────────────────┘
        ┌────────────────┼──────────────────┼────────────────┐
        │ ballistics     │ dispersion/error │ terrain        │            NEW src/arty modules
        │ (charge+elev → │ (MPI bias, PE    │ (ElevationPro- │
        │  range,AoF,ToF)│  round-to-round) │  vider + LOS)  │
        └────────────────┴────────┬─────────┴────────────────┘
                         ┌────────┴─────────┐
                         │ EXISTING kernel: │  shells.py, zones.py,
                         │ single-burst     │  fragmentation.py
                         │ pkill field      │  (unchanged API)
                         └──────────────────┘
```

Proposed module boundaries (each maps to one or more modeler aspects under
Workflow B):

| Module                | Owns                                                                                                                     | Physics-bearing?                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `arty/ballistics.py`  | firing solution: charge + elevation → range, angle of fall, time of flight, terminal velocity; high/low-angle            | yes → @modeler                                                                             |
| `arty/dispersion.py`  | error budget: MPI bias sampling, probable errors → per-round impact distribution, registration effect                    | yes → @modeler                                                                             |
| `arty/terrain.py`     | `ElevationProvider` protocol (`z(x,y)`, gradient, normal), analytic surfaces, DEM adapter, line-of-sight/masking queries | geometry, partly @modeler                                                                  |
| `arty/mission.py`     | mission state machine (fire order, volleys, FO observation, bracketing corrections), sheaf geometry                      | orchestration; correction *rules* are doctrine, math inside stays in ballistics/dispersion |
| `arty/effects.py`     | aggregate N bursts over a target grid (survivor rule / expected coverage)                                                | yes → @modeler                                                                             |
| `arty/blast.py`       | scaled-distance overpressure, fortification penetration/damage-given-hit, P(direct hit) on point targets (Track C)       | yes → @modeler                                                                             |
| `arty/scenario.py`    | scenario schema (who/what/where/how), capstone wiring of mission + terrain + effects (Track D)                           | orchestration only                                                                         |
| `data/firing-tables/` | digitized WW2 firing table data (see A1 Option A)                                                                        | data, via @librarian                                                                       |

Key data objects: `Gun` (charge system, elevation limits — in project scope
but not yet implemented; firing data is per gun-and-charge, not per shell, so
this entity is on the Phase 2a critical path), `FiringSolution`,
`ErrorBudget`, `RoundImpact` (burst point, AoF, terminal velocity), `Sheaf`,
`FireMission`, `MissionResult` (impacts, aggregated field, event log).

## 3. Track A — Fire missions

### A0. Mission kernel — fidelity chosen by materiality (named work item)

Mission superposition needs the single-burst effect expressed in ground
coordinates at arbitrary position/azimuth/AoF on a shared grid. Naive
re-evaluation of the full four-zone kernel per round × grid cell × MC
realization multiplies the current workload by ~10³–10⁴, undoes the
vectorization win — and, per the materiality principle, is probably
pointless at battery scale. Two designs, decided by a **modeler materiality
test** (compare mission outcomes under both; the tolerance and comparison
protocol are the aspect's first deliverable):

- **Reduced footprint (recommended).** Fit a compact parametric lethal-area
  function (Carleton-family) to the full four-zone model offline, per
  (shell, fuse, AoF bucket); missions consume only the fitted footprint. The
  full model stays the source of truth and the learning tool's engine.
- **Full-kernel cache (fallback).** Canonical-grid cache per AoF bucket,
  placed by rotate/translate interpolation — only if the materiality test
  shows mission outcomes shift beyond tolerance under the footprint.

This test is also the standing gate for every later performance decision:
no compiled dependency (Numba/Rust) enters without a *failed* materiality
comparison on record (§10).

### A1. Ballistics (prerequisite for honest dispersion)

Ballistics is a prerequisite for the dispersion *model* even though the
dispersion *data* (PE values) comes from the A1 data source, for three
reasons: PE values are indexed by charge and range, so selecting the right
one requires the firing solution; converting trajectory scatter into a
ground-plane impact ellipse goes through the angle of fall (decisive once
terrain arrives — a reverse slope compresses or stretches the beaten zone);
and every sampled round needs per-impact burst parameters (AoF, terminal
velocity) for the fragmentation kernel, not just a position. Three options,
ordered as an escalation path:

- **Option A — Anchor-point-calibrated point mass (recommended start).**
  Point-mass ODE (scipy `solve_ivp`, drag + gravity) with the drag scale
  fitted to a *handful* of published anchor points — (range, elevation, ToF,
  AoF, PE) tuples from secondary sources (BRL reports, artillery histories).
  Gives a real trajectory (needed later for terrain intercept) while avoiding
  the full-table digitization risk below. Less authentic in the last few
  percent; far more robust to sourcing failure.
- **Option B — Digitized firing tables (upgrade path).** Full WW2 firing
  tables (e.g., FT 105-H-3 for the 105 mm M1 shell, FT 155 series for the
  M107) tabulate per charge: elevation ↔ range, AoF, ToF, terminal velocity,
  **and the probable errors themselves**. Maximum authenticity, and the
  ground truth Option A calibrates against where available. Known risks:
  scans live in archive.org / CARL / DTIC, not the librarian's Scopus
  pipeline (expect manual curation); PE tables sit in the worst-scanned
  appendices; OCR of dense 1940s numeric tables fails *silently* — a
  digitization QA step with human spot-checks is mandatory, and each new
  gun/charge repeats the cost.
- **Option C — Fully sourced KD drag curves (research-grade end-state).**
  Modified point mass with literature drag data for the actual shell shapes;
  only worth it if the librarian sweep surfaces usable KD data.

### A2. Error model — the core of "uncertainty of accuracy"

Standard gunnery decomposition, which `project_scope.md` already anticipates:

1. **Systematic error (MPI bias)** — met, propellant temperature, wear,
   survey. One draw per mission/occasion; shifts the whole pattern. Reduced
   (not eliminated) by **registration** or FO adjustment.
1. **Random dispersion** — round-to-round, irreducible. Bivariate normal in
   range/deflection, parameterized by PE_r and PE_d from the A1 data source
   (firing-table lookups under Option B; fitted PE anchor points under
   Option A), with PE = 0.6745σ. Range PE ≫ deflection PE → the elongated
   beaten zone falls out naturally.
1. **Aim/target-location error** — by the FO; matters for the adjustment
   simulation.

Deliverable quantity: per-round impact distribution around the aim point,
conditioned on mission state (registered? adjusted? map-shooting?).
Literature (FM 6-40 era gunnery texts, BRL dispersion reports) via
@librarian.

### A3. Multi-shell effects aggregation

Two complementary methods — recommend building **both**; they share the
kernel:

- **Expected-coverage convolution (fast, deterministic).** The pkill field is
  already a grid; the expected mission effect is (approximately) the
  single-burst kernel convolved with the impact-point PDF, scaled by round
  count (`scipy.signal.fftconvolve`). Instant "heat map" as sliders move —
  fits the existing sensitivity-app interaction model.
- **Monte Carlo realizations (variability, storytelling).** Sample actual
  impact points per volley, superpose per-round pkill via the survivor rule
  `P = 1 − ∏(1−pᵢ)`. Shows *a* mission, not the average — crucial for the
  instructional point that identical missions differ. Cheap: N ≈ 24–72 bursts
  × precomputed kernel lookups (see A0). Variance reduction via
  `scipy.stats.qmc` if needed.

**Early modeler question — consistency criterion between the two paths.**
The convolution computes expected lethal *exposure*; converting it to P(kill)
assumes overlap behaves Poisson-like, which breaks exactly where users look:
the high-pkill core near the aim point, where the survivor rule
`1 − ∏(1−pᵢ)` saturates but expected coverage keeps climbing. Without an
agreed criterion the two paths visibly disagree in the most-scrutinized
region of the chart and it reads as a bug. This is the problem
Carleton-damage-function / expected-fractional-damage methods exist for; the
modeler must define the reconciliation (or the declared divergence bound)
**before** both paths are built.

### A4. Mission choreography (FO → FDC → guns)

A **discrete state machine, not physics**: fire order → initial data → volley
→ FO spotting (over/short/left/right, derived from true impact vs. the FO's
perceived target) → bracketing corrections → fire for effect. Plus
rate-of-fire → mission timeline. This is where the **instrumentation** goal
lands: every order, shot, splash, and correction becomes a structured log
event that the app replays. No heavyweight framework needed — plain Python
objects; SimPy would be overkill.

**Declared stance: doctrine emulation, not validated physics.** Adjustment
simulation needs a model of the FO's *perception* error, and quantitative
WW2 data on spotting error is thin to nonexistent. This layer is scoped as
doctrine emulation with declared assumptions — otherwise the model-reviewer
loop has no literature to check against and review stalls. It is also the
scope-creep magnet of the project (mils/deflection conventions, US vs.
generic procedure); fidelity limits get set in the proposal, not discovered
during implementation.

### A5. Fuses — from burst-height parameter to terminal event

Today `h_b` and AoF are app inputs; with ballistics they become *outputs* of
a fuse acting on the terminal trajectory. This is the integration seam
between Track A and the kernel (the API keeps both entry points: mission
mode derives burst parameters, the learning tool still sets them freely):

- **PD** — burst at the surface intercept (h_b ≈ 0).
- **Time** — airburst at set time of flight; height-of-burst error joins the
  A2 budget as its own dispersion component (rides Phase 2a).
- **Delay incl. ricochet** — genuinely new physics (graze-angle-dependent
  ricochet, burst on the bounce); its own modeler aspect, interacting with
  Track B's local surface slope.

## 4. Track B — Simulated surface

### B1. Staged approach

- **Stage 1 — Analytic surfaces.** `ElevationProvider` protocol: `z(x,y)`,
  `gradient(x,y)`; implementations: flat, tilted plane, ridge/valley
  primitives, Gaussian hills, composable sums. Enough to demo reverse-slope
  protection and crest masking — the two terrain effects with the biggest
  instructional payoff.
- **Stage 2 — Real relief (DEM).** Same protocol, backed by a raster patch
  re-projected into the local gun-target frame (meters). Sources, best-first:

| Source                                              | Resolution               | Access                                   | Notes                                          |
| --------------------------------------------------- | ------------------------ | ---------------------------------------- | ---------------------------------------------- |
| **Copernicus GLO-30**                               | 30 m                     | free, AWS open data / OpenTopography API | best global default                            |
| USGS 3DEP                                           | 10 m (1 m lidar patches) | free, `py3dep`                           | US only — fine for demo terrain                |
| SRTM                                                | 30 m                     | free, `elevation` pkg                    | older, voids in relief                         |
| National lidar (e.g. Environment Agency UK, IGN FR) | 1–2 m                    | free                                     | if a specific historical battlefield is wanted |

A 5×5 km patch at 30 m is a 167×167 array — trivially cached as a local
`.tif`/`.npy`; no live-service dependency after first fetch.

**Resolution caveat (realism trap).** The pkill grid works at ~1 m; GLO-30
cells are 30 m. Masking computed on 30 m terrain produces smooth,
confident-looking shadow edges at a scale the data cannot support, and the
things that actually provide cover (foxholes, berms, micro-terrain) are
invisible at any DEM resolution. Stage 1 analytic surfaces carry the
instructional reverse-slope demo; Stage 2 DEM masking is presented as a
terrain-scale effect, not a target-scale one — or a 1 m lidar patch is
fetched for the demo battlefield and claims capped accordingly.

### B2. Terrain × physics interactions, ordered by payoff/cost

1. **Impact-point intercept** — trajectory ∩ terrain instead of `z=0`: shifts
   range on slopes, changes *local* angle of fall relative to the surface
   (grazing vs. plunging → fragmentation pattern changes already modeled via
   AoF). Needs Option B/C ballistics (a trajectory to intersect).
1. **Burst height above local ground** for time/VT airburst realism.
1. **Fragment masking** — line-of-sight from burst point to each target cell
   over the height field (classic reverse-slope defilade). Pure geometry with
   a big visual payoff, but naive per-cell raycasting does not scale
   (~250k cells × 36 bursts × ~100 steps/ray); use per-burst viewshed sweep
   algorithms (O(cells) each) — an algorithm choice, not a loop.
1. **Crest clearance / high-angle necessity** — low-angle solution blocked by
   a ridge forces high-angle; ties terrain into the ballistics options.
1. (Later) **FO line-of-sight** — what the observer can actually see governs
   the adjustment loop.

### B3. Map visualization

- **Recommended: stay Plotly** (existing stack): `go.Surface` relief with
  pkill draped as color, plus 2-D contour+hillshade for the tactical map
  view. Zero new UI deps.
- Option: **pydeck** in Streamlit for real-basemap presentations
  (satellite/topo tiles under the overlays) — worth it only at Stage 2.
- Option: folium/leaflet — better for lat/lon web maps, weaker for draped
  scalar fields; not recommended here.

## 5. Track C — Fortification destruction & blast

Fortification defeat by HE lives in the quasi-static, empirical regime —
damage *categories* with wide tolerance bands, which is the fidelity the
source formulas themselves carry. Three quantities, each a modeler aspect:

1. **Scaled-distance overpressure** — Kingery–Bulmash-family blast scaling,
   ground vs. airburst reflection. Serves *two* consumers: structural loading
   here, and blast-on-personnel casualties (the original scope's
   "overpressure vs. distance" line is about people, not just works).
   Well-covered literature; clean librarian + modeler aspect.
1. **Penetration / damage-given-hit** — empirical formulas of the
   ACE / modified-NDRC / TM 5-855 family for low-velocity HE shell into
   soil, timber, and mass concrete; earth-cover equivalence; discrete damage
   states (suppressed / damaged / destroyed).
1. **P(direct hit) on a point target** — the A2 dispersion model evaluated at
   small-target scale. This is the physics behind A4's *destruction mission*:
   Track C completes that mission type rather than adding a separate
   simulation.
1. **Target catalogue extension** — gun-crew and soft-vehicle targets
   (dimensions + hardness threshold) as consumers of fragmentation + blast,
   extending the existing presented-area/posture machinery; foxhole/trench
   protection enters as Track C cover classes. Soft vehicles stay soft — see
   the firewall.

**Anti-armor firewall.** Armor stays permanently out of scope, and the
firewall is defined by materials and projectiles, not target names — the
math itself must be incapable of expressing an armor engagement:

1. Materials whitelist: soil, timber, unreinforced/lightly-reinforced
   concrete. Steel plate is excluded as a material.
1. Projectile whitelist: HE shell (PD/delay fuze). No kinetic AP penetrators.
1. Target whitelist: static works — foxhole, trench, earth-timber bunker,
   concrete pillbox. No vehicles as hard targets; the soft-vehicle target
   stays a fragmentation/blast target with a hardness threshold, never a
   penetration target.
1. Output form: discrete damage states from empirical formulas — deliberately
   unable to express a penetration duel.

**Direct laying — reclassified from "out of scope" to deferred add-on.**
Direct fire introduces no new machinery: same point-mass trajectory in an
easier regime, engagement LOS from Track B, and effects = P(hit) × Track C
damage-given-hit. What changes is error provenance: the error budget becomes
gunner-dominated (range estimation, sight lay, observed corrections),
parameterized from wartime operational-research hit-probability curves —
same doctrine/empirics-emulation stance as the FO layer (A4). Its cost is
sourcing empirical hit-probability data, not building models; cheap once
A1 + B (LOS) + C exist.

## 6. Track D — Scenario capstone

The integration layer the original Tool Flow envisions: a **scenario schema**
(who/what/where/how — guns, targets with posture/cover, terrain patch,
mission type) that drives the mission engine end-to-end and renders the map
view plus the event-log replay. No new physics — deliberately: Track D is
the proof that the module boundaries in §2 were right. If the capstone needs
anything beyond wiring `arty` calls together, that's a signal a quantity is
missing from a track, handled via Gate 2, never inlined. To de-risk late
integration, Phase 3 *finishes* the walking skeleton stood up in Phase 2a
(§8) rather than starting integration from scratch.

## 7. Tooling recommendations (delta from current stack)

| Need                    | Tool                                            | Why                               |
| ----------------------- | ----------------------------------------------- | --------------------------------- |
| ODE trajectory          | `scipy.integrate.solve_ivp`                     | already a dep                     |
| Table interpolation     | `scipy.interpolate`                             | already a dep                     |
| Convolution aggregation | `scipy.signal.fftconvolve`                      | already a dep                     |
| MC sampling             | `numpy.random.Generator`, `scipy.stats.qmc`     | already a dep                     |
| DEM read/reproject      | **`rasterio`** (+ `pyproj`)                     | the standard, minimal footprint   |
| DEM fetch               | **OpenTopography API** (plain HTTP) or `py3dep` | one-time fetch, cache locally     |
| Map/3-D viz             | Plotly (existing)                               | no new stack                      |
| Mission engine          | plain Python dataclasses + event list           | SimPy/geopandas would be overkill |

New hard dependencies: **rasterio + pyproj only**, and only at Terrain
Stage 2.

## 8. Phasing (dependency-ordered, each phase demos standalone)

1. **Phase 2a — Dispersion on flat ground.** Anchor-point data (librarian) →
   ballistics Option A → PD/Time fuse function + error model (incl. HOB
   error) → sheaf → A0 materiality test + footprint → MC + convolution
   aggregation → "beaten zone" mission app view. *Highest instructional
   value per effort; zero terrain dependency.*
1. **Phase 2b — Analytic terrain.** `ElevationProvider`,
   burst-height-above-ground, fragment masking, reverse-slope demo.
   *Hidden dependency:* impact on a slope shifts the burst point, but a full
   trajectory-terrain intersection belongs to 2c. 2b therefore adopts an
   explicit approximation — the descending branch treated as a straight line
   at AoF — documented as such (modeler sign-off), or the phase ordering
   silently breaks.
1. **Phase 2c — Real relief.** DEM adapter, trajectory-terrain intercept
   (needs ballistics Option C), map-styled visualization.
1. **Phase 2d — Mission choreography.** FO/FDC state machine, bracketing,
   registration, mission timeline + event log replay.
1. **Phase 2e — Terminal events.** Delay/ricochet fuse physics (A5); needs
   2b's local surface slope. PD/Time fuses and HOB error already rode 2a.
1. **Phase 2f — Fortification destruction.** Track C: overpressure,
   penetration/damage states, point-target P(hit), target catalogue;
   completes the destruction mission. Needs 2a (dispersion at small-target
   scale) and the delay fuse from 2e.
1. **Phase 3 — Scenario capstone.** Track D: scenario schema, end-to-end
   mission on a map with event-log replay. Integrates everything; the
   original Tool Flow delivered.

2a and 2b are independent and could run as parallel OpenSpec changes; 2c
needs both; 2d needs 2a; 2e needs 2a + 2b; 2f needs 2a + 2e; Phase 3 needs
all tracks — but a thin end-to-end scenario slice (walking skeleton: one
gun, one target, stub terrain) stands from Phase 2a onward and grows with
each phase, so integration seams surface early instead of at the capstone.

## 9. Process fit

Every physics-bearing item above (ballistics, error model, aggregation math,
terrain-intercept, masking geometry) is a **Workflow B aspect owned by
@modeler with @model-reviewer sign-off**. First concrete step of Phase 2a is
a **@librarian sweep**: WW2 firing tables (FT 105-H-3 family), probable-error
tables, and a gunnery-error-budget reference into `doc-reference/`. Each
phase then becomes an OpenSpec change proposal, with physics-computation
specs held until the modeler derivations are confirmed.

## 10. Risks, counterfactuals, and scaling

Ranked by likelihood of being the thing that actually stalls the expansion:

| #   | Risk                                                                                                                                                                            | Counterfactual / mitigation                                                                                                                                                                                                        |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Fidelity creep** — running learning-tool fidelity at mission scale; the road to performance collapse, compiled-dependency rabbit holes, and app rot                           | Materiality principle (§1) enforced by the A0 test; performance work must cite a *failed* materiality comparison before adding complexity                                                                                          |
| 2   | **Ballistics data sourcing** — anchor points thin, firing-table scans outside the librarian's Scopus pipeline; OCR of PE appendices fails silently; cost repeats per gun/charge | Option A anchor-point calibration as primary path (A1); timeboxed librarian sourcing spike with a go/no-go before committing to Option B; human QA on any digitized numbers                                                        |
| 3   | **Mission-kernel work item underestimated** — touches perf-tuned vectorized builders                                                                                            | A0 footprint-first design; fit/interpolation tolerance is an explicit modeler decision                                                                                                                                             |
| 4   | **Convolution vs. MC disagreement** — Poisson-overlap assumption breaks in the high-pkill core; the two app views show different numbers where users look hardest               | Consistency criterion defined by modeler *before* both paths are built (A3)                                                                                                                                                        |
| 5   | **Late integration** — tracks built in isolation; frames, units, and event-schema seams discovered at the capstone                                                              | Walking skeleton from Phase 2a (§8); conventions (local ENU frame, azimuth origin, mils vs. degrees, PE vs. σ) fixed in the first OpenSpec change                                                                                  |
| 6   | **Streamlit rerun model vs. stateful mission app** — timeline scrub/replay fights whole-script reruns; session_state is a bug farm                                              | Hard compute/render split: "run mission" yields an immutable `MissionResult`; all interaction re-renders cached arrays. If the discipline can't hold, re-platforming (Dash/Panel/marimo) is a priced alternative, not an emergency |
| 7   | **DEM resolution vs. defilade scale** — 30 m terrain yields authoritative-looking masking fiction at 1 m pkill scale                                                            | Analytic surfaces carry the instructional demo; DEM masking presented terrain-scale, or 1 m lidar for the demo battlefield (B1 caveat)                                                                                             |
| 8   | **CRS/reprojection bugs** — axis order, ellipsoid vs. geoid heights in the local ENU frame                                                                                      | Verification step against a known landmark when the DEM adapter lands                                                                                                                                                              |

**Does it scale?**

- **Compute — yes, conditionally.** Convolution path is FFT-bounded.
  MC path is linear in rounds × realizations: fine at battery scale
  (≤72 rounds, ~10² realizations) with the A0 footprint; with naive
  full-kernel re-evaluation it is not.
- **Compiled acceleration (Numba/Rust) — not needed by design.** At battery
  scale with the reduced footprint, everything is numpy/scipy-bounded
  (~10⁷-op mission evaluations, milliseconds). The only path to compiled
  dependencies is fidelity creep (risk #1), and the A0 materiality test is
  the gate that keeps them out; they'd also cost deployment friction (JIT
  warm-up in Streamlit, build toolchain in uv) with no user-visible gain.
- **Visualization — 2D yes, 3D no.** Mission-scale 3D volume rendering dies
  in the browser. 3D volumes stay a single-burst learning tool; missions get
  2D draped fields. Locked as a presentation-architecture decision.
- **Data — the real non-scaling axis.** Adding guns/shells is bounded by
  archival sourcing and digitization QA, not code. The single-battery,
  single-shell-type cap is what keeps the project tractable.
- **Scope ceiling.** Everything holds at battery level; battalion fires/TOT
  would strain MC counts and the event log — out of scope by design.

## Recommended defaults

Start with **anchor-point-calibrated ballistics (A1 Option A) + the A0
materiality test and reduced footprint + both aggregation methods (with the
A3 consistency criterion settled first) + analytic terrain**, standing up
the walking skeleton in Phase 2a; defer DEM to a later change; keep all
visualization in Plotly, 3D reserved for the single-burst learning tool.
