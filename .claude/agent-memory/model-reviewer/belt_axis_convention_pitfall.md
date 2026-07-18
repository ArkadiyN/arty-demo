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
claim — it is very likely to be false off that plane. This includes
superficially-reworded versions of the same claim (e.g. "safe normalisation,"
"no physics change," "arbitrary sign") — re-derive the algebra symbolically
rather than judging by whether the prose sounds different; a partial
(single-component) axis flip is not the same operation as negating the whole
vector, and only the latter leaves `|cosΘ|` invariant.

**The durable template:** the only fix that survives review here is demoting
the claim from "provably equivalent" to "deliberate standardisation — both
paths converge to one formula by construction, with pointwise agreement
checked numerically, not asserted analytically." `fragmentation.py` now has a
`_forward_shell_axis = (+cosα,0,−sinα)` used by the new single-zone
`lethal_density_point`, kept separate from the legacy `_shell_axis`
(`(−cosα,0,−sinα)`, still used only by `_expected_kills_3d_point`) — the two
paths were never reconciled, only standardised going forward. Resolution and
the independent re-verification live in
`experiment/fragmentation-field/updates/lethal-fragment-density-field/review.md`.

See [[zones_meshgrid_convention]] for the related (but distinct) grid-indexing
pitfall in the same file.

**New surface (2026-07-18): notebook prose about the app's `diff_pk` feature,
not just derivations.** `app/sensitivity.py` computes
`diff_pk = result_zones["pk_total"] - result.field_pk`, where `result.field_pk`
comes from `compute_frag_field_3d` → `_expected_kills_3d_point` — the legacy
function confirmed above to still use `_shell_axis` (`-cosα`), never
reconciled with the four-zone `+cosα` convention, and which also carries the
separately-confirmed `sinΘ`-vs-`sinθᶻ` bug
([[lethal_density_field_implementation]]). A notebook/`.qmd` reframing pass
that describes this app diff as "exact" or as isolating/attributing "exactly"
the end-zone contribution is making the same false-equivalence claim this
memory exists to catch, just in reader-facing prose instead of a derivation —
apply the same skepticism: the grid alignment is exact (no interpolation
error), but the physics on the two sides of the subtraction is not on a
reconciled axis convention, so "exact attribution" is unsupported off the
`x=0` plane. Flagged in `experiment/fragmentation-field/_four-zone-3d.qmd`
(division-of-labor table + "Why both 3-D variants are live" prose, added in
the pkill-field/two-model-coexistence documentation pass) — see that file's
review for the specific wording.

**Recurrence trap: fixing the flagged instance doesn't catch sibling
instances of the same phrasing in the same file.** When the division-of-labor
prose above was corrected, a second, independent instance of the same
false-isolation framing survived untouched in §6.8 of the same
`_four-zone-3d.qmd` ("...the four-zone field's distinct contribution,
**isolated as the diff** against the belt baseline") — worse, that sentence
sits under the *deterministic ray-footprint* plot (`fig_zone_footprint`),
which performs no subtraction/diff at all, so it also misattributes the "diff"
framing to a figure that isn't one. **How to apply going forward:** once this
phrasing pattern is flagged anywhere in a file, `grep` the whole file for
"isolat", "exact", and "diff" before signing off — a single corrected
paragraph is not evidence the rest of the file was swept.
