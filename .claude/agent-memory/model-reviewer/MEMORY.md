# Model Reviewer Memory Index

- [zones.py mesh/line convention](zones_meshgrid_convention.md) — X/Y meshgrid axis convention in arty.zones, validated for four_zone_line_split vs \_four_zone_field_split
- [app/sensitivity.py physics leakage](sensitivity_physics_leakage.md) — both app/sensitivity.py and plots.py:fig_zone_elevation now call fragment_velocity; also: numeric-equivalence tests can't catch a bit-identical duplication, verify by reverting
- [belt axis convention pitfall](belt_axis_convention_pitfall.md) — single/four-zone axis sign only agrees on x=0; also flag notebook prose claiming the app's diff_pk "exactly" isolates zone contributions
- [min_lethal_mass saturation check](min_lethal_mass_saturation_check.md) — m_lo-saturation branch unreachable at default params + E_leth=1000J; flag "flat near burst" m_min(s) claims
- [lethal-density field src/ implementation](lethal_density_field_implementation.md) — rho_L(x,y,z) impl review, oracle re-verification, np.interp silent-clip footgun in caller-supplied grid API
- [P_k Poisson derivation vs ES-310 mismatch](pkill_poisson_eslevel_mismatch.md) — eq(1) must disclose Pk|hit=1 as a 2nd, separate simplification beyond rho_L's binary cut, not conflate them; re-check if eq(1)/E_leth changes
- [uv virtual project: arty unimportable](uv_virtual_project_arty_unimportable.md) — missing [build-system] in pyproject.toml means `uv run pytest`/`import arty` fail out-of-the-box (pre-existing, not a code bug); `uv pip install -e .` fixes it for the session
- [derivation qualitative claims need numeric check](derivation_qualitative_claims_need_numeric_check.md) — pkill §4.7 "mostly saturated" claim was empirically false (fringe-dominated); a single spot-check point isn't the same as computing the actual fraction
