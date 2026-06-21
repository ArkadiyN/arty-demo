---
name: false-ogive-vs-structural-ogive
description: A shell "false ogive" (windshield) is inert and distinct from the model's structural-ogive zone; do not conflate when asked if it affects fragmentation
metadata:
  type: project
---

A **false ogive** (a.k.a. windshield / ballistic cap / false nose, e.g. on the
M103 8-inch shell) is a thin, inert sheet-metal cone fitted *forward of* the HE
body's true nose purely for aerodynamic streamlining. It carries no explosive,
is not in contact with the burster, and is far too thin to be a Gurney-driven
fragmenting case.

The fragmentation model's **`ogive` zone** (`zones.py::compute_shell_zones`)
models the *structural* ogive — the load-bearing steel nose of the HE body that
holds filler and fragments under Gurney drive. These are physically different
parts. A false ogive does NOT enter any of: casing wall-thickness profile,
Mott mass distribution, zone V0/mu, or presented area of the *target* (A_p is
the human silhouette, not the shell).

**Why this is a non-issue for the model:** the false ogive contributes no
fragmenting steel mass, no explosive allocation, and at burst it is simply
shattered/blown clear as low-velocity inert debris — negligible vs. the HE
body's lethal steel. Including it would *add* a near-massless non-lethal zone,
not change lethality.

**How to apply:** if asked whether a false ogive / windshield affects frag
physics, the answer is no — provided the shell's registered `mass_total` and
`mass_deductions` already exclude (or correctly bookkeep) the inert cap so the
HE-body steel mass `M_steel = mass_total - mass_filler - mass_deductions` is the
real fragmenting case mass. That bookkeeping is the only thing to verify per
shell. Separately note: M103 (8-inch / 203 mm) is NOT in the `SHELLS` registry
at all (only M1 105 mm, M107 155 mm, M48 75 mm), so the question is moot until
someone adds it — and if added, its `ogive_*` fields must describe the true HE
nose, never the false cap.
