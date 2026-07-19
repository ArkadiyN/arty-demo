---
name: false-ogive-vs-structural-ogive
description: A shell windshield/false nose is inert and distinct from the model's structural-ogive zone
metadata:
  type: project
---

A **false ogive** (windshield / ballistic cap, e.g. on the M103 8-inch) is a
thin inert streamlining cone forward of the HE body — no explosive contact,
not Gurney-driven. The model's `ogive` zone (`zones.py::compute_shell_zones`)
is the *structural* steel nose of the HE body. Different parts: the false
ogive enters no part of the frag model and is a non-issue for lethality.

**Only check that matters per shell:** registered `mass_total` /
`mass_deductions` must bookkeep the inert cap so
`M_steel = mass_total − mass_filler − mass_deductions` is the real
fragmenting case mass. (M103 is not in the `SHELLS` registry; if added, its
`ogive_*` fields must describe the true HE nose, never the false cap.)
