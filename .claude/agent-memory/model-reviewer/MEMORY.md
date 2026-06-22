# Model Reviewer Memory Index

- [zones.py mesh/line convention](zones_meshgrid_convention.md) — X/Y meshgrid axis convention in arty.zones, validated for four_zone_line_split vs \_four_zone_field_split
- [app/sensitivity.py physics leakage](sensitivity_physics_leakage.md) — spray-cone duplication now RESOLVED via arty.zones.fragment_velocity; also notes an unrelated app wiring bug pattern (x/y arg swap between elevation/across plot fns)
- [belt axis convention pitfall](belt_axis_convention_pitfall.md) — single/four-zone axis sign only agrees on x=0; "fixes" may re-derive the same false invariance under new wording, re-check symbolically
- [min_lethal_mass saturation check](min_lethal_mass_saturation_check.md) — m_lo-saturation branch unreachable at default params + E_leth=1000J; flag "flat near burst" m_min(s) claims
- [lethal-density field src/ implementation](lethal_density_field_implementation.md) — rho_L(x,y,z) impl review, oracle re-verification, np.interp silent-clip footgun in caller-supplied grid API
- [P_k Poisson derivation vs ES-310 mismatch](pkill_poisson_eslevel_mismatch.md) — eq(1) must disclose Pk|hit=1 as a 2nd, separate simplification beyond rho_L's binary cut, not conflate them; re-check if eq(1)/E_leth changes
