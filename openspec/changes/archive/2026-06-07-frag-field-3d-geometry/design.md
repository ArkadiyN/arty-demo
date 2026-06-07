## Context

The fragmentation model in `src/arty/fragmentation.py` currently computes a 1D radial kill-probability and a symmetric 2D hazard disk. The `compute_frag_field_3d` function already accepts `BurstParams` (which carries `angle_of_fall` and `h_b`) and `PostureParams`, and already produces an asymmetric field driven by burst height. This change adds the second axis of asymmetry: the spray pattern is not a uniform belt but four elevation-distinct zones determined by shell geometry.

Two US shells have full drawing-derived zone geometry (M1, M107). All other shells currently in the registry have only total mass and wall thickness — no zone breakdown. The design must accommodate both without making non-US shells a second-class API.

The modeler (physics agent) must resolve two open questions before the derivation pass: (1) which Gurney formula applies to the ogive zone, and (2) whether the base plate is Mott-fragmented, a discrete large fragment, or non-fragmenting dead mass. The software design must be flexible enough to accommodate any answer.

## Goals / Non-Goals

**Goals:**

- Zone mass partitioning for US shells from arc geometry; fraction-based fallback for non-US
- Per-zone Mott distribution (own μ from zone wall thickness and zone V₀)
- Per-zone spray elevation angle; AoF projects each zone onto the ground plane correctly
- `presented_area(γ, posture)` replaces the fixed `w_target` scalar throughout `compute_frag_field_3d`
- Backward compatibility: `compute_frag_field` (1D) and the existing `compute_frag_field_3d` scenarios pass unchanged within tolerance

**Non-Goals:**

- Elevation spread within a zone (Gold 2007 Fig. 9 velocity-vs-angle variation — deferred)
- Ground ricochet
- Body armour / partial cover
- Monte Carlo discrete-fragment sampling

## Decisions

### Decision 1 — Zone geometry lives in ShellParams, not a separate dataclass

**Choice:** Add optional zone fields directly to `ShellParams` (outer arc radius, inner arc radius, zone lengths, boattail angle). When absent, a `zone_fractions` fallback dict provides mass fractions.

**Rationale:** The registry pattern already owns per-shell physical data. A separate `ZoneGeometry` dataclass would require parallel registry entries and two-step lookups. Keeping it in `ShellParams` means callers receive a complete shell description in one object.

**Alternative considered:** A separate `ZoneGeometry` registry keyed by shell name. Rejected: duplicates the shell identity key and complicates the Tier-2 fallback path.

### Decision 2 — Zone masses computed lazily via a `ShellZones` result struct

**Choice:** Expose `compute_shell_zones(shell: ShellParams) -> ShellZones` that returns per-zone mass, wall thickness, and spray half-angle. For Tier-1 shells it integrates the arc geometry numerically; for Tier-2 it applies fraction defaults.

**Rationale:** Separates the geometry calculation from the fragmentation physics. `compute_frag_field_3d` calls `compute_shell_zones` once and then loops over zones. This also makes the zone masses inspectable and testable independently.

**Alternative considered:** Computing zones inline inside `compute_frag_field_3d`. Rejected: untestable and conflates two responsibilities.

### Decision 3 — Spray elevation angle from surface normal of outer arc

**Choice:** For each zone, the mean spray elevation angle relative to the shell axis is the outward surface normal at the zone midpoint of the outer arc profile. Cylinder → 90°. Boattail → 90° + taper/2. Ogive → midpoint normal from arc parameters. For Tier-1 shells this uses the drawing-derived outer arc. For Tier-2 shells two sub-cases apply:

- **`ogive_len` absent:** full-tangent ogive of the given CRH (or `CRH_DEFAULT_TIER2 = 6.0`).
- **`ogive_len` present (secant ogive):** arc tangent is at the shoulder; the midpoint is at `ogive_len / 2` along the arc. Formula: `atan2(sqrt(R_o² − x_m²), x_m)` where `R_o = CRH × D`. This corrects the over-estimate from the full-tangent formula when only a short section of a large-radius arc is used (e.g. M48: CRH 7.43, 1.18 cal long → full-tangent gives 79.6°, secant gives 85.4°).

**Rationale:** Consistent with Gurney physics — fragments fly perpendicular to the surface. The midpoint normal gives a single representative angle per zone without integrating the full elevation distribution (which is a future extension). The secant branch avoids a systematic error for shells with visually blunt noses that are geometrically a short section of a gentle arc.

**Alternative considered:** Using the zone centroid angle or the tip/shoulder average. These give similar results for gentle arcs but diverge for short sharp ogives; the midpoint normal is physically grounded.

### Decision 4 — Base plate: modeler decides, code handles all three options

**Choice:** `ShellParams` gains a `base_treatment` field: `"mott"`, `"plate"` (single large fragment), or `"dead"` (non-fragmenting mass, excluded from hazard). The modeler's derivation pass sets this per shell after literature review. Default: `"dead"` (conservative, matches current behaviour).

**Rationale:** The design must not pre-judge the physics. All three treatments are plausible given shell base plate thicknesses (~18–37 mm). Coding all three now avoids a later structural refactor.

### Decision 5 — Tier-2 fraction defaults from M1/M107 empirical split

**Choice:** Non-US shells receive default zone fractions: ogive 42%, cylinder 36%, boattail 17%, base 5% (midpoints of the geometry-corrected M1 and M107 values). Applied to total shell steel mass (`mass_total - mass_filler - mass_deductions`). Wall thickness for each non-cylinder zone is estimated by scaling from cylinder `wall_t` using the observed ratio from US shells.

**Note:** Initial fractions (ogive 53%, cylinder 27%) were based on a pre-correction M1 ogive estimate. After fixing the inner-arc two-point fit for M1 (ogive 31%, cyl 45%) and verifying M107 (ogive 52%, cyl 28%), the Tier-2 midpoints were corrected to the current values. Shells without a boattail use ogive 42%, cylinder 53%, base 5%.

**Rationale:** Using midpoints of the two validated Tier-1 shells gives a defensible engineering estimate. Callers can override via explicit zone fields if partial drawing data becomes available.

**Alternative considered:** Single-zone (cylinder-only) fallback. Rejected: defeats the purpose of the change for non-US shells; the spray geometry correction (AoF) is still valid even with approximate masses.

### Decision 6 — presented_area(γ, posture) as a free function, not a method

**Choice:** `presented_area(gamma: float, posture: PostureParams) -> float` as a module-level function using `w_perp * (h * cos(γ) + d * sin(γ))`.

**Rationale:** Already scoped and derived in `updates/target-area-profile/scoping.md`. Pure function, easy to test, no state. Matches the pattern of other physics helpers in `fragmentation.py`.

## Risks / Trade-offs

**Zone spray angle approximation (midpoint normal)** → The single midpoint normal per zone ignores the elevation spread within the zone. For the cylinder (90° by symmetry) this is exact. For the M107 ogive (79–90° range) the midpoint is ~84°, suppressing the ±5° spread. This is an acknowledged limitation documented in the notebook.

**Tier-2 fractions are empirical, not derived** → Applying M1/M107 fractions to Soviet or German shells assumes similar design philosophy. Some WW2 shells (e.g., short-bodied Soviet designs) deviate. Mitigation: Tier-2 fractions are overridable; the approximation is flagged in the model limitations section.

**Gurney formula for ogive pending modeler** → If the modeler recommends a cone Gurney formula, the ogive V₀ may differ significantly from the cylinder formula. The `compute_shell_zones` interface must accept a per-zone `gurney_fn` callable so the physics can be swapped without touching the field integration code.

**Numerical integration of arc mass (Tier-1)** → The ogive steel volume requires integrating between two offset circular arcs (outer secant arc and inner tangent arc). A simple midpoint Riemann sum over 100 axial slices is sufficient (error < 0.5% for these geometries) and avoids a scipy dependency.

## Open Questions (resolved)

1. **Ogive Gurney formula** — *Resolved: cylinder approximation.* Zone-local M/C ratio applied to the standard Gurney cylinder formula; cone formula not used (derivation §2.1).
1. **Base plate treatment per shell** — *Resolved: `"mott"` for M1, M107, M48.* NWC TP 7124 supports Mott fragmentation of the base plate with a Gurney reduction factor k^b (0.75 for M1-class, 0.70 for M107-class).
1. **Boattail: own Gurney zone or merged with cylinder?** — *Resolved: own zone.* Spray angle 90° + taper/2 (≈ 94°–95° for M1/M107); distinct enough from 90° to affect the rearward ground footprint. Zone-local M/C and μ computed separately.
1. **Non-US spray angle for ogive** — *Resolved: `CRH_DEFAULT_TIER2 = 6.0`, overridable per shell via `ogive_crh`.* For shells with known ogive length (secant geometry), `ogive_len` activates the secant midpoint formula (Decision 3).
