---
name: four-zone-field-geometry
description: Gotcha for the 4-zone 3D fragmentation field — an empty/missing ground lobe is usually correct geometry, not a bug; pointer to derivation.md
metadata:
  type: project
---

Four-zone 3D fragmentation field (ogive / cylinder / boattail / base).

**Gotcha:** a zone lobe that is missing or empty in the rendered ground field
(including P(kill) ~= 0 along the y=0 downrange/backward centerline) is usually
*physically correct*, not a wiring/azimuth bug. A zone reaches the ground only
where its fragment $v_{g,z} < 0$; at high AoF whole zones legitimately drop out
(cylinder spray goes horizontal at AoF=90°, the rearward base spray goes upward
for most AoF). The reflex to debug "blank lobe = broken geometry" is the trap —
check the $v_{g,z}$ sign first.

It is *not* an azimuth-coverage bug: the belt acceptance test is polar-angle-only
about the shell axis, which is **azimuth-complete** (accepts the whole spray ring,
all $\phi$, backward fragments included). The elevation chart's $\phi$=0/180 rays
are just the x-z cross-section of that full 3D cone — a display convention.

**Why:** the zone→lobe mapping, the per-azimuth ground-intersection mechanism,
and the base-zone upward gate are all derived and limit-checked in
`experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md`
(§3.6 spray angles, §3.7 AoF projection, §5 limit checks). Don't restate that
math here — read it there.

**How to apply:** when a field-geometry "defect" is reported (missing/asymmetric
lobe), reproduce the $v_{g,z}$ sign per zone/azimuth at the reported AoF before
treating it as a bug. Only an azimuth-incomplete lobe that *should* close (per
§5) is a real defect.
