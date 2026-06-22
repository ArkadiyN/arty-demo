---
name: belt-axis-convention-pitfall
description: single-zone vs four-zone shell-axis sign convention (-cosα vs +cosα) only agrees on the x=0 plane, not pointwise — flag any derivation that claims pointwise equivalence; also watch for "fixes" that re-derive the same false invariance under new wording (e.g. "safe normalisation" framing)
metadata:
  type: project
---

`fragmentation.py:_shell_axis` uses `e_axis = (-cosα, 0, -sinα)`;
`zones.py:_four_zone_field_split`/`four_zone_field`/`four_zone_line_split` use
`e_axis = (+cosα, 0, -sinα)` (α = angle of fall). These differ by a sign flip
on the **x-component only** — not the whole vector. For a general ray
`r̂ = (rx, ry, rz)`:

```
cosΘ_single = -rx·cosα - rz·sinα
cosΘ_four   =  rx·cosα - rz·sinα
```

`cosΘ_single = -cosΘ_four` only when `rz = 0`; in general (`α≠0`, `rx≠0`)
`|cosΘ_single| ≠ |cosΘ_four|`. Verified by hand: α=30°, point (x,y,z)=(20,0,2)
relative to burst → `|cosΘ_single|≈0.812` vs `|cosΘ_four|≈0.912` — clearly
different, even though both happen to land on the same side of a `sinδ≈0.259`
guard in that particular example. The single-zone path's `|cosΘ|≤sinδ` guard
and the four-zone path's `|cosΘ-cosθᶻ|≤sinδ` guard at the equatorial
specialization (`θᶻ=90°⇒cosθᶻ=0`, reducing to `|cosΘ|≤sinδ`) are **not**
pointwise-equivalent tests of the same physical region off the `x=0` plane —
they only provably agree there, or in the degenerate `α=0` case.

**Why this matters:** the [[zones_meshgrid_convention]] memory already
established that `zones.py`'s grid/axis roles must be tracked carefully when
generalizing ground-plane code; this is the *companion* pitfall one level
deeper — the **physics convention** (which way the shell axis points), not
just the grid indexing, also silently differs between the single-zone and
four-zone paths. A derivation or implementation that "unifies" the two paths
(e.g. for an arbitrary-3D-point field, or any future single-vs-four-zone
consistency check) must not assume the existing per-point belt tests already
agree pointwise — only the prior `frag-field-3d-geometry/derivation.md`'s
*aggregate* claim (full Mott-integrated field magnitude matches after merging
zones into one equivalent cylinder) was ever validated; nobody validated a
pointwise `cosΘ` agreement, and it does not hold.

**How to apply:** whenever a new derivation or src/ change claims the
single-zone and four-zone belt-acceptance tests are "equivalent" or
"identical in magnitude" at the equatorial specialization, hand-check with a
concrete off-axis point (not on `x=0`, with `α≠0`) before accepting the
claim — it is very likely to be false off that plane. Caught 2026-06-20 in
`experiment/fragmentation-field/updates/lethal-fragment-density-field/derivation.md`
§5.4 (FAIL, Major) — flagged in `review.md` in the same folder.

**RESOLVED 2026-06-20 (third pass, PASS).** The modeler's third revision
finally took the exact legitimate fix recorded below: it dropped *all*
analytical-invariance language, explicitly named and rejected the partial-flip
trap ("We therefore make **no** claim that the flip is physics-neutral"),
kept the 0.812-vs-0.912 counterexample labelled as "proof of non-equivalence,"
and reframed the standardisation as by-construction (same formula written
into both paths) with all pointwise-agreement evidence deferred to the §8
numerical spot-check — consistently across §5.4, §5.5, §7 checklist, and §8
(checked all four did not slip back into a stronger claim). Independently
re-verified the quoted source lines still match: `fragmentation.py:381-382`
`_shell_axis` is still `(-cosα,0,-sinα)`; `zones.py:429,453` (and duplicated
at 521-523/609-611) is still `(+cosα,0,-sinα)` — pre-implementation, src/
unchanged as expected. **Takeaway confirmed:** the fix that actually works is
demoting the claim from "proof of equivalence" to "deliberate standardisation,
agreement holds by construction, pointwise evidence deferred to numerics" —
exactly the suggested correction from the second FAIL. This is the durable
template for any future "are these two conventions/paths equivalent" claim
in this codebase: look for whether the document still asserts an *analytical*
invariance anywhere (even reworded) versus correctly demoting to
by-construction + empirical spot-check.

See [[zones_meshgrid_convention]] for the related (but distinct) grid-indexing
pitfall in the same file.

**Update 2026-06-20 (re-review):** the modeler's revision did NOT fix this —
it replaced the "identical in magnitude" claim with a new but equally false
claim: "flipping only the x-component of `ê_axis` is a safe normalisation
because the equatorial belt has no forward/aft asymmetry." This is wrong
because the operation that *is* neutral for a fore/aft-symmetric belt is
negating the **entire** vector (`ê→−ê`, all 3 components, under which
`cosΘ→−cosΘ` so `|cosΘ|` is exactly invariant) — not flipping a single
component. A partial-component flip is a genuinely different vector
(`ê_new ≠ −ê_old` unless `sinα=0`), and the same `cosΘ_old/cosΘ_new` algebra
as the original pitfall applies unchanged. Re-running the document's own
worked example with the opposite z-sign convention reproduces the identical
0.812-vs-0.912-magnitude gap, just relabeled — i.e. the revision's own
numbers already falsify its conclusion. **Lesson for future review:** when a
modeler "fixes" a flagged equivalence claim, check whether the new argument
is the *same* algebra under new wording (re-derive it symbolically, don't
just check whether the prose sounds different) — a superficially different
justification ("relabeling," "arbitrary sign," "no physics change") can still
encode the identical mathematical error. The legitimate fix here is to drop
the "provably neutral" framing entirely and just state it as a deliberate
standardisation choice (both paths converge to one formula by construction,
which is trivially true), backed by the numerical spot-check the document
already plans — not by an analytical invariance argument.

**src/ implementation verified 2026-06-20.** `fragmentation.py` added
`_forward_shell_axis(alpha_rad) = (+cosα, 0, −sinα)` alongside the untouched
legacy `_shell_axis` (`(−cosα,0,−sinα)`, still used only by the legacy
`_expected_kills_3d_point`). New `lethal_density_point` (single-zone ρ_L) uses
`_forward_shell_axis`; new `lethal_density_four_zone_point` (zones.py) already
used the four-zone `(+cosα,...)` convention (no change needed there — it was
never wrong). Independently re-verified by hand/script (not trusting the
modeler's numbers): (1) scanning a 200×200 grid at z=0 with real default
params, the old vs new single-zone axis convention disagree on belt
acceptance at 3.1% of grid points (1244/40000) — concrete proof the fix is
not vacuous; (2) a synthetic collapsed-equal-cylinder four-zone case (4
identical zones, θ=90°, summing to the single-zone N0/μ) reproduced the
single-zone ρ_L to exact bit-for-bit equality (0.0 rel error) at an off-x=0
point `(5,20,0)`, confirming pointwise agreement is real, not just claimed.
This is the resolution template working as designed — re-run this same
collapsed-cylinder + off-x=0-grid-scan pattern for any future axis-convention
change in this area.
