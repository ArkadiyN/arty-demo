---
name: four-zone-field-geometry
description: A missing/empty ground lobe in the four-zone field is usually correct geometry, not a bug
metadata:
  type: project
---

**Gotcha:** a zone lobe missing or empty in the rendered ground field
(including P(kill)≈0 along the y=0 centerline) is usually *physically
correct*: a zone reaches the ground only where its fragment v_gz < 0, and at
high AoF whole zones legitimately drop out (cylinder spray goes horizontal at
AoF=90°, base spray goes upward for most AoF). The "blank lobe = broken
geometry" debugging reflex is the trap — check the v_gz sign per zone first.

It is not an azimuth-coverage bug: the belt acceptance test is
polar-angle-only about the shell axis and azimuth-complete; the elevation
chart's φ=0/180 rays are just the x-z cross-section of the full cone.

Full derivation and limit checks:
`experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md`
(§3.6, §3.7, §5). Only an azimuth-incomplete lobe that should close per §5
is a real defect.
