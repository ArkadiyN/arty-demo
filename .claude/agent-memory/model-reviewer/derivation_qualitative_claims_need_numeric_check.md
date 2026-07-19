---
name: derivation-qualitative-claims-need-numeric-check
description: a derivation's untested qualitative field-shape prediction ("most of the belt saturates") can pass every dimensional/limit/monotonicity check and still be empirically false once the notebook computes the real numbers — don't accept it on paper, recompute
metadata:
  type: project
---

`experiment/fragmentation-field/updates/pkill-poisson-field/derivation.md` §4.7
predicted, from the `ρ_L` kernel's own reported peak (~74 m⁻² near `s_min`)
and a claim that "appreciable...densities of order 1–10 m⁻² [span] much of the
belt," that `P_k` would render as **"mostly saturated"** over most of the
lethal footprint. `review.md`'s implementation pass appeared to confirm this,
but only by spot-checking a *single* near-peak point (ρ_L≈5.48 → P_k≈0.990) —
never the actual fraction of the field that saturates.

When the notebook (`_pkill-field.qmd`) actually computed that fraction, the
real field is the opposite: at AoF=30°, h_b=2 m, median `ρ_L` over lethal
cells is ~0.11 m⁻² and only ~3% (single-zone) / ~1% (four-zone) of lethal
cells clear `P_k>0.95` — fringe-dominated, not saturated. Independently
re-verified 2026-07-18 (`compute_lethal_density_field_3d` + `pkill_field_3d`,
105 mm M1, same burst geometry): `frac(ρ_L>0.5)≈16%`, `frac(ρ_L>3.53)≈3.2%`
(3.53 = the ρ_L value at which `P_k=0.95`). The notebook prose was corrected to
say "fringe-dominated," but the source derivation.md §4.7 and review.md's
endorsement of it were never revised to match — a reader following the
`.qmd`'s "derived and reviewed in full at ..." link lands on a document that
still asserts the opposite of what the notebook shows.

**Why this matters generically:** a derivation's dimensional check, limit
cases (λ→0/∞), and monotonicity proof are about the *function's* shape
(`1-e^{-λ}`), not about *where the actual field's ρ_L values fall* along that
curve — that second question is empirical and depends on the real magnitude
distribution, which isn't known until someone computes it. A review that
"confirms" a saturation/fringe claim by checking one point (peak or otherwise)
is not the same as checking the histogram/fraction the claim is actually
about.

**How to apply:** when a derivation predicts a qualitative *fraction-of-field*
or *most-of-the-range* claim, don't accept it as re-verified until the actual
notebook/oracle numbers are pulled and the fraction is computed directly
(a couple of `np.mean(field > threshold)` lines) — a single representative-
point spot-check does not exercise it. If the notebook's own printed
diagnostic later contradicts the working-folder derivation/review documents,
flag the stale doc even though `updates/` folders are meant to be archived —
until archived, they're still one hyperlink away from the reader.
