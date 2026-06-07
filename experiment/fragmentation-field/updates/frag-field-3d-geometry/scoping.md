# Scoping — Four-Zone Shell Fragmentation Model (3D Geometry)

**Author:** modeler agent
**Date:** 2026-05-25
**Status:** scoping pass — no code or derivation math
**Parent model:** `experiment/fragmentation-field/fragmentation-field.qmd`
**Change folder:** `experiment/fragmentation-field/updates/frag-field-3d-geometry/`
**Bundled work:** `experiment/fragmentation-field/updates/target-area-profile/scoping.md` (presented-area profile, already scoped — explicitly included in this change per `proposal.md`)

______________________________________________________________________

## 1 · Problem — what the single-zone model lacks

The current notebook (§3–§6) treats the entire HE shell as one cylindrical
Gurney–Mott source:

- A single $V_0$ from one $M/C$ ratio.
- A single $\\mu$ from one wall thickness $t_w$ and one break-up radius $r\_{bu}$.
- All steel mass mapped into one equatorial spray belt at $90°$ from the
  forward shell axis.
- Result: a perfectly **circular** hazard field, symmetric in azimuth, that
  cannot tell forward from rearward and ignores angle of fall (AoF).

Three concrete consequences are visible in the existing notebook
(`fragmentation-field.qmd`, §Model Limitations #1 and #4):

1. **~70 % of shell steel is in the wrong place.** Drawing-derived M1 and
   M107 zone splits put ~50–56 % of steel in the ogive, ~12–18 % in the
   boattail, ~5–9 % in the base — all currently lumped into the cylinder
   belt. The notebook explicitly flags this as the dominant unmodelled
   effect (Limitation #1).
1. **The forward/rear asymmetry is missing.** When the shell axis is tilted
   by AoF = α (typical 20°–35° for medium-range fire), the ogive spray cone
   projects onto the ground *ahead* of the burst, the cylinder belt
   projects roughly symmetrically, and the base cap projects *behind*. The
   current model cannot resolve this — Limitation #4 quantifies the gap as
   ~30–50 % more density forward than rearward at AoF ≈ 25°.
1. **`w_target` is a fixed scalar.** Already addressed in the
   `target-area-profile` scoping pass; bundling it here means the
   $A_p(\\gamma, \\text{posture})$ generalisation enters the 3-D field along
   with the zone-spray geometry, so the airburst / posture story works
   end-to-end after one integration pass.

The literature now in `doc-reference/ww2-shells/` (BRL 126, NWC TP 7124,
SAND92-0243) collectively supports a four-zone reformulation: BRL 126
identifies three measured spray zones (nose, side, base) with distinct
densities and velocities; NWC TP 7124 explains the physical mechanism
(four-phase expansion with end-effects); SAND92-0243 provides the closed-form
Gurney/trajectory mapping for arbitrary $C/M$ and casing geometry.

______________________________________________________________________

## 2 · Open questions — options ranked

### Q1 · Gurney formula for the ogive zone

| Option                                                    | Description                                                                                          | Literature support                                                                                                                                                          | Cost                                                     |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **A. Cylinder formula, zone-local $C/M$**                 | Use eq. (1) of the main notebook with $M$ = ogive steel mass, $C$ = explosive within ogive envelope. | SAND92-0243 Table I is a steel-cylinder table; the cylinder formula is the only one with a tabulated reference. NWC TP 7124 acknowledges "fundamental physics" of cylinder. | Trivial — reuse existing `gurney_velocity()`.            |
| **B. Gurney cone / reduced-coefficient formula**          | Apply a geometric reduction factor (≈ 0.8 × $V_0^\\text{cyl}$, per NWC TP 7124 §Q1).                 | NWC TP 7124 recommends a stress-projection argument: oblique detonation incidence reduces radial impulse on the ogive wall.                                                 | One scalar factor; no new equation.                      |
| **C. Combine ogive + cylinder into a single Gurney zone** | Compute one $V_0$ from total (ogive+cylinder) $C/M$; only split mass between zones for Mott $\\mu$.  | Simplest interpretation of BRL 126 which reports two velocities (nose 2740 ft/s, side ?). But BRL 126's *nose* spray is *higher*, not lower, than side spray.               | Loses the velocity contrast BRL 126 explicitly measures. |

**Evidence weighing the velocity difference:**

- BRL 126 reports nose-spray perforating fragments averaging **2740 ft/s
  (835 m/s)** vs. penetrating fragments at **1070 ft/s (326 m/s)**. The
  high-velocity nose-spray population is the headline observation. This
  argues *against* a blanket "ogive is slower" reduction (Option B).
- NWC TP 7124's stress-projection argument predicts the ogive should be
  *slower* (lower radial impulse). This is in **direct tension** with
  BRL 126's measured nose velocity.
- Reconciliation: the high BRL 126 nose velocity is plausibly a
  **forward-projection artefact** — fragments from the ogive shoulder
  travel along the shell-axis direction and combine the shell's
  pre-detonation residual velocity with $V_0$. Velocity *normal to the
  zone surface* (which is what Gurney gives) may still be lower than the
  cylinder, while the *lab-frame* velocity along the line of fire is
  higher. The BRL 126 data is from a near-static burst (no pre-detonation
  velocity), so this artefact cannot be the full explanation.
- For CRH 6–11 ogives (M1 has CRH ≈ 7, M107 has CRH ≈ 9): the *mean
  surface normal angle* across the ogive is ~80°–85° from the axis (per
  design Decision 3). The wall-normal component of detonation pressure
  is $\\sin(\\text{normal angle})$ ≈ 0.98–1.00, so the geometric reduction
  in radial impulse is only **2–6 %**. This makes Option B's "0.8 ×"
  factor look excessive for these CRHs.

**Recommendation: Option A** — cylinder Gurney with zone-local $C/M$.

Rationale:

1. The geometric reduction factor argued for in NWC TP 7124 (Option B)
   assumes a sharp cone (cone half-angle 30°–40°). For artillery CRH
   6–11 the local arc is nearly parallel to the cylinder over most of
   the ogive length, so the cylinder formula is a good first approximation.
1. The zone-local $C/M$ for the ogive is higher than the cylinder's
   $C/M$ (less steel, similar explosive column), which naturally
   produces a *higher* $V_0$ in the ogive — consistent with BRL 126's
   nose-spray velocity being above side-spray.
1. Option B's reduction factor can be added later as a single multiplier
   on $V_0^\\text{ogive}$ if dedicated cone data appears; the interface
   from Decision 2 (`compute_shell_zones` returns per-zone $V_0$) makes
   this trivial. **No structural change required.**
1. Option C is rejected: it discards the zone-specific velocity that
   BRL 126's three-zone spray data and the main proposal explicitly
   call for.

**Action:** derivation pass uses cylinder Gurney per zone. A scalar
`gurney_reduction_factor` field (default 1.0) lives on `ZoneParams` so
Option B can be enabled per-zone without refactoring.

______________________________________________________________________

### Q2 · Base plate treatment for M1 and M107

| Option                            | Description                                                                                                    | Literature support                                                                                                                                                                                              |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`"dead"`**                      | Base plate is excluded from hazard (treated as non-fragmenting mass).                                          | None of the three sources support this. Default in current Decision 4 only because it matches existing behaviour.                                                                                               |
| **`"plate"`**                     | Single near-intact fragment; mass = base plate mass; $V_0$ from Gurney plate formula or tangential estimate.   | Weak — BRL 126 sees no single dominant base fragment in pit recovery.                                                                                                                                           |
| **`"mott"` (reduced parameters)** | Treated as a normal Mott zone with reduced $V_0$ (× ~0.7–0.8) and increased $\\mu$ (fewer, heavier fragments). | **Direct match:** NWC TP 7124 (rarefaction limits cross-linkage → larger, fewer fragments at the closed end). BRL 126 base ≈ 15 % of weight in fewer, heavier pieces (Screen 1 is "mostly fuze" but also base). |

**Evidence summary:**

- **NWC TP 7124 §Phase 3 and §Q2:** "End effects may already have produced
  smaller fragments at both ends of the cylinder." But then the literature
  index explicitly clarifies: rarefaction waves reflecting from the closed
  base *prevent normal cross-linkage*, producing **larger, fewer fragments**
  with **lower initial velocity (~0.7–0.8 × cylinder $V_m$)**. Quote from
  index.md: *"NOT: Single 'dead' plate. NOT: Identical to cylinder. YES:
  Mott-fragmented, but with end-effect modification."*
- **BRL 126:** Base region contributes ~15 % of mass in fewer, heavier
  pieces (Screen 1: 6 fragments at 15.4 % of weight) — explicitly *not*
  intact, *not* dust. The shape of the distribution matches a Mott zone
  with reduced $N_0$ and increased $\\mu$.
- **SAND92-0243:** Treats fragments as plate-like with $S_f \\in [0, 0.5]$
  and $R_e \\in [0, 1.0]$. The base contributes plate-like fragments
  consistent with Mott but with no special "dead-mass" treatment.

**M1 vs. M107 base thickness:**

- M1 base plate: **0.695 ″ ≈ 17.7 mm** (~1.6 × cylinder wall $t_w$ = 11 mm).
- M107 base plate: **1.44 ″ ≈ 36.6 mm** (~3.4 × cylinder wall $t_w$ = 10.7 mm).

Both bases are massively thicker than the cylinder wall — so the
expansion-and-fracture geometry is genuinely different from the cylinder,
not just a "thicker version of the same thing." Treating these as Mott
zones with **lower $V_0$** (NWC TP 7124's 0.7–0.8 reduction) and **larger
$\\mu$** (which $\\mu \\propto (r\_{bu}/V_0)^3$ already gives automatically
once a thicker wall produces a smaller break-up expansion ratio and a
lower $V_0$) is physically coherent.

**Recommendation:**

| Shell              | `base_treatment` | Justification                                                                                                                                                                                                                                                                                                    |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M1 (105 mm)**    | `"mott"`         | Base ~1.6 × cylinder wall; thick but not massive. NWC TP 7124 + BRL 126 directly support a Mott zone with reduced $V_0$ (factor ≈ 0.75) and the $\\mu$ correction follows from $r\_{bu}^3 / V_0^3$.                                                                                                              |
| **M107 (155 mm)**  | `"mott"`         | Base ~3.4 × cylinder wall; very thick. Same reasoning — but the velocity reduction is more aggressive (use 0.70) to reflect deeper rarefaction effects. The contribution to far-field hazard will be small (heavier and slower fragments lose KE per mass slower than cylinder spray but start with less $V_0$). |
| **Tier-2 default** | `"mott"`         | Same physics applies generically.                                                                                                                                                                                                                                                                                |

The design's `"dead"` default is **not** recommended for either US shell.
It remains available as an override for a hypothetical "armour-piercing
plug" base that doesn't fragment — none of our shells fit that
description.

**Note on `"plate"`:** Option remains in the type system (per Decision 4)
but is not selected for any shell. It would apply to e.g. anti-armour
ground-burst munitions where a discrete forged base plug is designed —
not relevant for thin-walled HE.

______________________________________________________________________

### Q3 · Boattail — own Gurney zone or merged with cylinder?

**Geometry:**

- Boattail taper angle on M1 ≈ 9°, on M107 ≈ 8° (drawing data referenced in
  the spec).
- Boattail spray angle = 90° + taper_angle/2 ≈ 94.0°–94.5° from forward
  axis (per Decision 3, midpoint surface normal).
- Boattail mass fraction: ~12–18 % of steel (drawings).
- Boattail wall is slightly thicker than cylinder near the base end
  (taper to the base shoulder).

**Evidence:**

- **BRL 126:** No separate boattail data. Three zones identified (nose,
  side, base) — the boattail is implicitly bundled with "side."
- **NWC TP 7124:** No boattail analysis. Index entry suggests
  $V_m(\\text{boattail}) \\approx 0.92 \\times V_m(\\text{cylinder})$ as an
  inference from intermediate geometry, but admits this is unvalidated.
- **SAND92-0243:** No boattail case among its seven casing geometries.

**Velocity difference if treated separately:**

- Boattail local $C/M$ is *lower* than cylinder (less explosive in the
  tapered region per unit steel because the inner cavity is also tapered
  or stepped down to meet the base). Net effect: boattail $V_0$ is
  slightly *lower* than cylinder, ~5–10 %. NWC TP 7124's 0.92 inference
  is in the same ballpark.

**Mass and spray-angle difference:**

- Spray angle difference: 94° vs. 90° is **4°**. Projected onto the ground
  with AoF = 25°, this displaces the boattail spray-pattern centroid by
  ≈ 4° downward in the shell frame ≈ a few metres in the line-of-fire
  direction on the ground. **Small but non-zero.**
- Mass: 12–18 % of total steel is significant; merging it with the
  cylinder inflates the cylinder Mott $N_0$ by ~15 %.

**Recommendation: separate zone** with the same cylinder Gurney formula,
but `wall_t` and zone-local $C/M$ taken from boattail geometry.

Rationale:

1. The mass fraction (12–18 %) is too large to ignore — merging
   contaminates the cylinder $\\mu$ calculation.
1. The 4° spray-angle offset matters when AoF tilts the field, because the
   boattail spray ends up *just behind* the cylinder belt on the ground,
   contributing to the rear-sector hazard that the proposal aims to
   capture.
1. The cost is one extra zone in `ShellZones` — already in the spec
   (Requirement: `ShellZones` has four fields). No new code.
1. If empirical validation shows the boattail contribution is negligible
   (e.g., its $V_0$ × mass × fragment count product is < 5 % of cylinder
   for both M1 and M107), the integration pass can quietly drop it; but
   the architecture supports it.

**Shells without a boattail** (e.g., older Russian F-354, per the spec's
acceptance criteria) set `boattail_len = 0` and the zone contributes zero
mass — already covered by the spec.

______________________________________________________________________

### Q4 · Non-US ogive CRH default for Tier-2 spray angle

**The question:** Without drawing data, what CRH (calibre radius head, the
ratio of the ogive outer-arc radius to the shell calibre) is
representative for WW2 HE shells (Soviet OF-462 / F-354, German 10.5 cm
Gr 38, etc.)? The spec currently assumes **6.0 cal**.

**Evidence from `doc-reference/`:**

- None of the three new sources (BRL 126, NWC TP 7124, SAND92-0243) tabulate
  CRH for non-US shells. BRL 126 covers the US 75 mm M48 only.
- The 75 mm M48 in BRL 126 is broadly representative of WW2-era US HE: the
  M48 ogive is a **CRH ≈ 5–6** design (standard WW2 practice). The M1
  105 mm (CRH ≈ 7) and M107 155 mm (CRH ≈ 9) are newer designs with
  longer, sharper ogives.
- General background knowledge (not in `doc-reference/`): WW2-era HE
  shells from Soviet, German, and British manufacture typically used
  **CRH 5–6**, occasionally lower for older designs and up to 7–8 for
  long-range projectiles. Soviet OF-462 (122 mm) ≈ CRH 5; German 10.5 cm
  Gr 38 ≈ CRH 5.5. The 6 cal default in the spec is slightly on the
  modern side but defensible.

**Spray-angle sensitivity to CRH:**

- For CRH 4: mean ogive surface-normal angle ≈ 71°–78° from forward axis.
- For CRH 6 (current default): mean ≈ 77°–83°.
- For CRH 8: mean ≈ 81°–86°.
- The notebook spec requires ogive spray angle in $[75°, 88°]$. CRH 6 sits
  comfortably in this range; CRH 4 produces an angle right at the lower
  edge.

**Recommendation: keep CRH = 6.0 cal as Tier-2 default**, but:

1. Document explicitly in the derivation that this is a "WW2 HE
   representative" value sourced from general design-practice knowledge
   (not `doc-reference/`).
1. Make `crh_default` a module-level constant (not a magic number) so it
   can be overridden per shell when partial drawing data becomes
   available.
1. Flag in the model limitations section that "Tier-2 CRH default 6.0
   cal" is unsourced engineering convention, in the same style as the
   notebook's existing Limitation #5 (TM 9-1901 not in
   `doc-reference/`).

Rationale: 6 cal is a defensible central value; the spray-angle output
sits in the spec's acceptance band; the field-of-fire sensitivity to a
±1 cal change in CRH is small (≤ 3° in spray angle → ≤ a few metres of
ground-pattern displacement at typical AoF). Pushing CRH to 5 or 7 would
not change the model's qualitative behaviour and is not warranted in the
absence of shell-specific drawings.

______________________________________________________________________

## 3 · Literature audit

| Source                                                                 | What it contributes                                                                                                                                                                                                                                      | Used for                                                                                                                                   |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **BRL Report 126** (Tolch 1938, 75 mm M48)                             | Experimental three-zone spray identification (nose/side/base); fragment-velocity range 1070–2740 ft/s; mass-screening bins; pit-test mass distribution showing base ≈ 15 % of weight in fewer, heavier pieces. **Anchors the empirical four-zone case.** | Q1 nose-velocity reality check; Q2 base-mass evidence.                                                                                     |
| **NWC TP 7124** (Pearson 1990, cylindrical warhead expansion)          | Four-phase expansion mechanism; end-effect physics (rarefaction → larger fewer base fragments, ~0.7–0.8 × $V_m$); SAE 1015 / Rb 78–85 steel baseline; temperature-dependent fracture mode. **Physical explanation for the four-zone partition.**         | Q2 base treatment ("mott" with reduced $V_0$); $V_0$ reduction factor for base; potentially future "ogive reduction" if we adopt Option B. |
| **SAND92-0243** (Vigil 1992, hazard zones)                             | Closed-form Gurney velocity vs. $C/M$ (Table I, steel/HMX); fragment shape factors $R_e$, $S_f$; trajectory and max-range $X_r$ formulas; lists seven casing geometries (cylinder is primary; no ogive/boattail).                                        | Q1 cylinder-Gurney baseline; trajectory framework reference for the derivation.                                                            |
| **Mott (1947)** (in `doc-reference/fragmentation/`)                    | $\\gamma$ table for low-carbon steels (γ ≈ 53 for 0.2 %C; γ ≈ 67 for 0.3 %C). Used unchanged.                                                                                                                                                            | Per-zone $\\mu$ calculation.                                                                                                               |
| **Gold (2017 PAFRAG)**                                                 | Mott $\\mu$ formula (eq. 16); 3× expansion criterion. Used unchanged.                                                                                                                                                                                    | Per-zone $\\mu$ calculation; $r\_{bu}$ for each zone using zone-local pre-detonation inner radius.                                         |
| **Existing presented-area scoping** (`target-area-profile/scoping.md`) | Closed-form $A_p(\\gamma) = w\_\\perp \\cdot (h\\cos\\gamma + d\\sin\\gamma)$ projection; posture parameters; eq. (22) re-derivation flagged as the highest-risk step.                                                                                   | Bundled into this change; replaces `w_target` scalar.                                                                                      |

**Gaps and acknowledged unsourced numbers:**

- **No CRH data for non-US shells** in `doc-reference/`. CRH 6.0 default
  flagged as engineering convention (Q4).
- **No direct boattail $V_0$ measurement** in any of the three new
  sources. The "boattail ≈ 0.92 × cylinder $V_m$" inference rests on
  geometry alone (Q3); the derivation pass will derive it from
  zone-local $C/M$ instead, which is more defensible.
- **AoF-specific validation data missing.** BRL 126 is a static burst.
  None of the three sources tabulate lethal area vs. AoF. This limits
  Phase-1 validation of the field asymmetry to internal sanity checks
  (forward density > rearward density at AoF < 90°, monotone in AoF)
  and qualitative comparison with the proposal's stated 30–50 % forward
  enhancement at AoF ≈ 25°.

**Reference availability check (per workflow step 3):** all three new
sources (BRL 126, NWC TP 7124, SAND92-0243) plus the previously collected
Mott / Gold / Gurney / Felix set cover the four-zone derivation. **No
additional librarian collection is needed before the derivation pass.**

______________________________________________________________________

## 4 · Recommendation — ready-to-implement decisions

| #      | Decision                                                                                                                                                                                                                                                                                                       | Confidence  |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **Q1** | **Cylinder Gurney per zone with zone-local $M/C$.** Keep a `gurney_reduction_factor` field on `ZoneParams` (default 1.0) so a future cone correction (NWC TP 7124 Option B) is one-line.                                                                                                                       | High        |
| **Q2** | **M1: `base_treatment = "mott"`** with $V_0$ reduction factor 0.75 and $r\_{bu}$ scaled from base-plate thickness. **M107: `base_treatment = "mott"`** with reduction factor 0.70. Tier-2 default also `"mott"` (factor 0.75). `"dead"` and `"plate"` remain in the type system as overrides but are not used. | High        |
| **Q3** | **Boattail is its own Gurney zone.** Uses cylinder Gurney with zone-local $M/C$ and zone-local wall thickness. Spray angle from midpoint surface normal (per Decision 3). Shells without a boattail (`boattail_len = 0`) contribute zero — already in the spec.                                                | Medium-high |
| **Q4** | **Tier-2 ogive CRH default = 6.0 cal**, documented as WW2 engineering convention. Implemented as a module-level constant `CRH_DEFAULT_TIER2 = 6.0` so it is overridable per shell.                                                                                                                             | Medium      |

**Derivation pass should produce:**

1. Per-zone $V_0$ formula: $V_0^z = V_g \\cdot k^z / \\sqrt{M^z/C^z + 1/2}$
   where $k^z$ is the (default-1.0) reduction factor and $M^z, C^z$ are
   zone-local mass and explosive contribution.
1. Per-zone $\\mu^z$ via Gold (2017) eq. 16 with zone-local $r\_{bu}^z$
   (from zone-local initial inner radius) and zone-local $V_0^z$.
1. Per-zone spray-angle $\\theta^z$ from outer-arc midpoint surface normal
   (Decision 3) — ogive analytic, cylinder = 90° exact, boattail =
   90° + taper/2, base ≈ 160°–170° from forward axis.
1. AoF projection: rotate each zone's spray cone about the line-of-fire
   axis by tilt angle $\\alpha = 90° - \\text{AoF}$ to map shell-frame
   spray onto the ground. Express ground-frame fragment-arrival direction
   in $(x_g, y_g)$ coordinates so the existing 3-D field integrator can
   accumulate the four zones.
1. Replace the scalar `w` factor in eq. (22) with
   $A_p(\\gamma, \\text{posture})$ from `target-area-profile/scoping.md`,
   propagating the unit-check (this is the highest-risk step — flagged
   there as a non-trivial dimensional re-derivation).
1. Unit checks and limit checks: at AoF = 90° (axis vertical) the field
   must collapse to the existing symmetric disk within tolerance; at
   AoF = 0° (axis horizontal) the spray field is a strongly elongated
   pattern.

**Out of scope (deferred):**

- Per-zone elevation spread within a zone (Gold 2007 Fig. 9
  velocity-vs-angle variation).
- Per-zone fragment shape-factor variation ($R_e$, $S_f$ from
  SAND92-0243) — the existing $C_D = 0.65$, $C\_\\text{shape} = 0.9$
  applies uniformly to all zones.
- Cone-Gurney for ogive (Option B above).
- Ground ricochet, body armour, partial cover.
- Monte Carlo discrete-fragment sampling.

______________________________________________________________________

## 5 · Scope note — bundled work

**Confirmed:** the `target-area-profile` scoping output
(`experiment/fragmentation-field/updates/target-area-profile/scoping.md`)
is **bundled into this change**, per the parent proposal:

> Target presented area $A(\\gamma)$ — replaces fixed `w_target` scalar
> with `presented_area(γ, posture)` so fragment elevation angle correctly
> modulates lethality (bundles the already-scoped `target-area-profile`
> work).

Concretely, the derivation pass will:

- Adopt Option A (cosine + sine projection,
  $A_p(\\gamma) = w\_\\perp (h\\cos\\gamma + d\\sin\\gamma)$) directly from the
  target-area scoping recommendation.
- Re-derive the geometry factor in eq. (22) from width-based
  $w/(2\\pi s \\cdot 2\\sin\\Theta\\delta)$ to area-based
  $A_p(\\gamma)/(s^2 \\cdot 2\\pi \\cdot 2\\sin\\Theta\\delta)$ — the
  dimensional change identified as the highest-risk step in
  target-area-profile §4.4.
- Use the three NATO-convention postures (standing / crouching / prone)
  with the box-model parameters from that scoping doc, flagged as
  engineering convention because Cunniff 2014 and AEP-55 Vol. 3 were
  not collected.
- Validate via the limit checks in target-area-profile §4.3: γ = 0
  prone → $A_p \\approx 0.15$ m², γ = 0 standing → $A_p \\approx 0.85$ m²;
  ground-burst $R\_{50}$ for standing recovers the current model value
  within tolerance.

No separate change-folder is needed for the area work — its scoping doc
remains in place as the historical record, and the derivation /
integration are absorbed into this update.

______________________________________________________________________

## Status for next step

**Ready for derivation pass.** No further literature collection needed.
All four open questions have a recommended answer with literature
support. The derivation pass should produce `derivation.md` in this
folder, carrying:

- Per-zone Gurney $V_0^z$ and Mott $\\mu^z$ derivations
- Zone-spray-angle formulas (ogive analytic from CRH; cylinder = 90°
  exact; boattail from taper angle; base from base-plate geometry)
- AoF-projection geometry
- Eq. (22) re-derivation with $A_p(\\gamma, \\text{posture})$
- Unit checks and limit recoveries (AoF = 90° → existing symmetric
  field; $A_p$ at γ = 0 recovers existing $w\_\\text{target}$ within a
  documented normalisation factor)
- Numerical-integration scheme for the Tier-1 ogive mass (200-slice
  midpoint Riemann sum per the spec)
