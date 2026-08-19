---
name: gotcha-ruled-line-regime-caliber-free
description: Mott's ruled-line control parameter l/x0 is caliber-independent because x0 is proportional to r; the regime is set by break-up velocity alone
metadata:
  type: project
---

Mott 1947's ruled line has one control parameter, `l/x0 = 2*pi*r_bu/x0`, and it
carries **no caliber dependence**: `x0 = sqrt(2 sigma_f/(rho gamma)) * r_bu/v_bu`
so `r_bu` cancels exactly, leaving `l/x0 = 2*pi*v_bu / sqrt(2 sigma_f/(rho gamma))`.
Mott says the same in his finding (2), p. 305 ("x0 is proportional to r").

**Why:** the instinct that "shell circumference depends on caliber, so the
regime must too" is wrong and has already been written into a brief. The
shipped fleet sits at `l/x0` 84-100, spread driven by C/M (through `v_bu`) and
by the 60 mm's different steel `gamma` -- 0.4 % on `kappa_x`.

**How to apply:** any question of the form "should this ruled-line moment be
per-shell?" is answered by that cancellation, not by a per-shell sweep. Numbers
and the derived slope (`kappa_x` rises ~0.032 per e-fold in `l/x0`, i.e.
logarithmically) live in
`experiment/fragmentation-field/updates/kappa-x-shell-regime/scoping.md` secs. 2-3.
Related: [[gotcha-mott-count-not-f-squared]], [[gotcha-mott-V-is-fracture-instant-velocity]].
