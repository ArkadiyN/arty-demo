## Why

The current model treats every HE shell as a uniform cylinder, assigning all steel mass to a single equatorial spray zone and ignoring angle of fall. This produces a symmetric circular hazard field that cannot distinguish forward from rear hazard, cannot model oblique impacts, and mis-attributes ~70% of shell steel (ogive, boattail, base plate) to the wrong geometry. Adding four-zone shell geometry coupled to angle of fall replaces the symmetric disk with a directional 3D hazard field.

## What Changes

- **Four spray zones** — ogive, cylinder, boattail, base plate — each with its own mass, wall thickness, Mott distribution, and spray elevation angle relative to the shell axis.
- **Angle-of-fall projection** — shell axis tilt α maps each zone's spray elevation onto the ground plane, producing forward (ogive), equatorial (cylinder), slightly-rearward (boattail), and strongly-rearward (base) lobes.
- **Two-tier zone mass model** — Tier 1: US shells (M1 105mm, M107 155mm) use drawing-derived arc geometry for numerical mass integration. Tier 2: non-US shells (no drawings available) use caliber-scaled mass fractions drawn from the M1/M107 empirical split (~50-56% ogive, ~27-28% cylinder, ~12-18% boattail, ~5-9% base).
- **Zone-specific Gurney/Mott** — each zone uses its own M (zone steel mass) and wall thickness to compute V₀ and μ independently. Gurney formula variant for the ogive and base plate treatment (Mott vs. discrete vs. non-fragmenting) deferred to modeler after literature review.
- **Target presented area A(γ)** — replaces fixed `w_target` scalar with `presented_area(γ, posture)` so fragment elevation angle correctly modulates lethality (bundles the already-scoped `target-area-profile` work).
- **ShellParams extended** — gains optional zone geometry fields (arc radii, lengths, taper angles) for Tier 1 shells; mass fractions used as fallback for Tier 2.

## Capabilities

### New Capabilities

- `shell-zone-model`: Four-zone shell geometry — arc-based mass partitioning for US shells, fraction-based fallback for non-US; spray elevation angle per zone; two-tier data model with a clear interface.

### Modified Capabilities

- `shell-registry`: `ShellParams` gains optional Tier-1 zone geometry fields (outer/inner arc radii, zone lengths, boattail angle). M1 and M107 entries populated from drawing data. Non-US shells omit these fields and receive Tier-2 fraction estimates.
- `fragmentation-physics`: `gurney_velocity` and `mott_params` become zone-aware — called per zone with zone mass and wall thickness. `compute_frag_field_3d` extended to accept zone spray geometry and accumulate the multi-zone hazard field.
- `burst-geometry`: `BurstParams.angle_of_fall` (already present) drives zone-to-ground projection. `compute_frag_field_3d` returns a field that is asymmetric in the line-of-fire direction. `PostureParams` / `presented_area` bundled here (target-area-profile).

## Impact

- `src/arty/shells.py` — `ShellParams` dataclass gains zone fields; M1 and M107 entries updated.
- `src/arty/fragmentation.py` — zone-dispatch logic added; `compute_frag_field_3d` signature stable but internal implementation changes; backward-compatible single-zone path retained.
- `experiment/fragmentation-field/fragmentation-field.qmd` — integrated after modeler derivation pass.
- Non-breaking: `compute_frag_field` (1D) and existing `compute_frag_field_3d` scenarios remain valid within tolerance.
