---
name: min-lethal-mass-saturation-check
description: with default ShellParams + E_leth=1000J, min_lethal_mass's m_lo-saturation branch is essentially unreachable — KE at m_lo is ~0.5 J even at s=0; flag any derivation that assumes a flat near-burst m_min(s) plateau
metadata:
  type: project
---

`fragmentation.py:min_lethal_mass` saturates to `m_lo=1e-6 kg` only when
`_ke(m_lo) ≥ E_leth`. With default `ShellParams()` (TNT, `mass_total=14.97`,
`mass_filler=2.18`, `mass_deductions=0.75` → `mass_shell≈12.04 kg`),
`gurney_velocity` gives `V0 ≈ 995 m/s`. Even at `s→0` with **zero** drag,
`KE(m_lo) = 0.5·1e-6·995² ≈ 0.49 J` — four orders of magnitude below the
ES-310 `P_k=0.5` anchor `E_leth=1000 J` (`_PK_E/_PK_VAL` at
`fragmentation.py:140-141`). So for this shell + this `E_leth`, the
`m_min=m_lo` "saturated near burst" branch never actually triggers; `m_min(s)`
is genuinely varying (bisected, not clipped) arbitrarily close to the burst.

**Why this matters:** any derivation that argues a resolution/grid/error
bound by assuming `m_min(s)` is "flat near the burst, only steep near the far
lethal edge" is asserting something that doesn't hold for the actual default
parameters — there may be no flat plateau at all except possibly the far
`m_hi` clip. This doesn't necessarily invalidate a chosen grid resolution,
but it invalidates the *written justification* for it if that justification
leans on a near-burst flat region.

**How to apply:** when reviewing any new `m_min(s)` tabulation/interpolation
scheme (slant-range grids, Numba kernels, etc.), do this back-of-envelope
check — `0.5·m_lo·V0²` vs `E_leth` — before accepting a "flat near s_min"
claim. If the inequality fails (as it does for the current defaults), require
either (a) an empirical check of the actual `m_min(s)` shape near `s_min`
before trusting the stated error bound, or (b) reliance on a numerical
interpolation-vs-bisection oracle (already standard practice in this model,
see the `min_lethal_mass`/`mott_N` validation pattern) rather than an
analytical "it's flat there" argument. Caught 2026-06-20 in
`experiment/fragmentation-field/updates/lethal-fragment-density-field/derivation.md`
§6.1/§6.2 (FAIL, Moderate) — flagged in `review.md` in the same folder.

Note: bash/python execution was denied in that review session for ad hoc
numeric scripts (sandbox policy, intermittent — sometimes simple commands like
`echo` worked, multi-line heredocs/python did not); this was worked out by
hand arithmetic instead. Don't assume Bash will be available for verification
— be ready to do the arithmetic manually.
