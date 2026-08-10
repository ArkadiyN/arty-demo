---
name: single-projectile-mass-exponents-unidentifiable
description: Sanborn 2019 CLT constants print w and D exponents but every shot used one projectile — the mass/area scaling is unidentifiable, so its recalibrations cannot supply E_thr(m)
metadata:
  type: project
---

A ballistic dataset fired with **one** projectile cannot constrain the mass or
diameter exponents of a model fitted to it, even when the published table
prints them as if measured.

**Why:** Sanborn et al. (2019) fired only the 0.5 in S-2 sphere in all 122
shots. §5.4 says so outright and *removes* `w` from the CLT THOR model for that
reason — but the CLT UFC refit (Table 8) keeps `w^1.434 / D^0.201`, where
`C_1 w^b / D^c` is a single lumped constant. Those exponents are fitting
artefacts. The "substantial change" from the original UFC `D^1.360` is evidence
of non-identifiability, not new physics.

**How to apply:** for the wood perforation threshold the project needs
`E_thr(m)` (mass-dependent — a compact fragment has `D ∝ m^(1/3)`), which is
exactly what this dataset cannot give. Use the **original** UFC 4-023-07
equation (THOR-derived, thin *solid* wood) as primary; use Sanborn only for
projectile-proxy validity and for the sign of the bias. Full reasoning:
`experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/scoping.md` §2.

Its `card.md` equation block is separately inadmissible — see the blocking
finding and `checks/sanborn2019-equation-closure.py` in that same folder.
Related: [[gotcha_steel_sigma_gamma_ratio_only]],
[[gotcha_density_falloff_shape_is_threshold_degenerate]].
