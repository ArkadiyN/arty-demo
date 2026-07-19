---
name: min-lethal-mass-saturation-check
description: m_lo-saturation branch of min_lethal_mass is unreachable at default params + E_leth=1000J — flag "flat near-burst m_min" claims
metadata:
  type: project
---

`min_lethal_mass` clips to `m_lo=1e-6 kg` only when `KE(m_lo) ≥ E_leth`. At
default `ShellParams()` (V0≈995 m/s), `KE(m_lo) ≈ 0.49 J` even at s→0 with
zero drag — four orders below `E_leth=1000 J`, so the "saturated near burst"
branch never triggers and `m_min(s)` genuinely varies arbitrarily close to
the burst.

**How to apply:** any derivation justifying a grid/error bound via a "flat
near-burst m_min plateau" is wrong for the actual defaults (caught as a FAIL
in `lethal-fragment-density-field/derivation.md` §6.1/6.2 — see its
review.md). Do the one-line `0.5·m_lo·V0²` vs `E_leth` check before
accepting such a claim; if it fails, require an empirical m_min(s) shape
check or the standard interpolation-vs-bisection oracle instead.
