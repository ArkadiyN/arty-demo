---
name: numpy-trapz-removed
description: this project's numpy version has removed np.trapz (AttributeError); use np.trapezoid instead in any ad-hoc verification/reference-quadrature script
metadata:
  type: reference
---

Hit while writing an independent verification script
(`experiment/_scratch/verify_thi.py`) to re-check a derivation's quadrature
claims: `np.trapz` raises `AttributeError: module 'numpy' has no attribute
'trapz'. Did you mean: 'trace'?` in this project's `uv`-managed numpy. Use
`np.trapezoid` instead. Purely an environment/version fact, not a project
physics gotcha — but every future numeric spot-check script that builds a
reference quadrature (a recurring task for this reviewer role, see
[[derivation_qualitative_claims_need_numeric_check]]) will hit this
identically on the first run.
