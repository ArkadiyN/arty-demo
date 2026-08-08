# Is `mott_params` an order of magnitude too small? — correctness classification

Working notes for the pass answering the user's "that seems extreme. How is the
existing number selected and why?" against
`../drag-gap-1944/tolch-1938-panel-distance.md` Result 3. No `src/arty/` changes.

Inputs: `_params_provenance_note.md`, `_validation.qmd` Check 3,
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`,
`doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`.
Script: `experiment/_scratch/mott_scale_check.py`.

## 1. The γ/σ_f selection is sound — and cannot be the defect

- σ_f = 800 MPa is better supported than the provenance note credited: Mott's
    own worked example (Mott 1947 p.306, anchor `As a numerical example`) uses "flow stress in the
    work-hardened state of 50 tons/sq.in." = **772 MPa**. The code's 800 MPa is
    Mott's own number, not just a bracket endpoint.
- γ = 65 is on the correct table row (Mott §3 table, line 305-310: 0.45 C →
    γ = 67). γ is a *fracture-strain scatter* parameter (dp/ds ∝ C e^{γs}),
    correctly used.
- **Closure argument**: μ ∝ (σ_f/γ)^1.5, so a 10× μ correction demands
    σ_f/γ × 4.6 → σ_f ≈ 3.7 GPa or γ ≈ 14. Both far outside any admissible
    value (Mott's table spans γ = 42–67). The whole admissible σ_f × γ box spans
    ≈1.5–2× on μ. **The parameter pair is arithmetically incapable of being the
    source of the discrepancy.** Re-picking γ/σ_f is not the fix.

## 2. Tolch's pit test is screen-resolved — it gives a real N(>m) curve

`tolch-1938.md:196` (screen sizes), `:319-329` and `:1672` (4-round averages).
Hand screen 0.22 in; screens No.1/2/3/4 openings 0.64/0.36/0.23/0.17 in.
Mass cut per screen estimated as ρ·s³ (compact fragment; **conservative** —
elongated slivers pass a screen at higher mass, which would push the implied
μ *up*, i.e. widen the gap).

| screen cut (g) | Tolch N(>m) | model N(>m) | model/Tolch |
| -------------: | ----------: | ----------: | ----------: |
|          33.72 |           6 |           0 |        0.01 |
|           6.00 |         278 |          78 |        0.28 |
|           1.57 |         533 |         927 |        1.74 |
|           0.63 |         675 |        2376 |        3.52 |

(model = `mott_params("75mm M48 HE")`: μ = 0.235 g, N₀ = 12 256, V₀ = 807.5 m/s.)

**The model crosses over.** It over-counts fines by 3.5× *and under-counts
heavy fragments by 3.6× (100× above 34 g)*. A recovery/screening loss can only
make an observed count too LOW — so the heavy-fragment deficit is
screening-immune and is a clean defect signature. `_validation.qmd` Check 3's
"Mott overestimates small fragments" defence does **not** cover it.

Mott fits to Tolch: μ = 3.46 g (large-fragment-weighted), μ = 0.95 g
(mass-constrained N₀ = M/2μ, M = 6030 g). No single μ fits all four points and
the mass budget — the real spectrum is steeper at the fine end than Mott.

## 3. Size of the gap

| anchor                               | Tolch       | model   | gap       |
| ------------------------------------ | ----------- | ------- | --------- |
| μ (Mott half-weight)                 | 0.95–3.5 g  | 0.235 g | **4–15×** |
| N₀                                   | 1 000–3 200 | 12 256  | 3.9–12×   |
| N₀ vs Tolch's own panel total ~5 000 | 5 000       | 12 256  | 2.5×      |
| N(>6 g)                              | 278         | 78      | 3.6× LOW  |

So "order of magnitude too small" is the **top** of the credible bracket, not
the centre. Better statement: **μ is ~4–8× too small (up to ~15× on the
large-fragment-weighted read)** — half to one order of magnitude. The
challenge doc's 7.5× count excess sits inside this and is corroborated.

`_validation.qmd` Check 3's 3 000–8 000 band cannot certify the scale: it is
Gold (2017) running the *same* Mott formula at γ = 50 — a model-to-model
consistency check, as the code comment itself says. Its second row (arena
recovery 800–3 000 for >0.5 g) is the data row, and the model (2 848 at

> 0.5 g for 75mm, 5 324 for 105mm) sits at/above its top while Tolch shows
> recovery efficiency is *not* the explanation (95.6% of mass recovered at a
> ~0.6 g cut).

## 4. Where the scale actually lives (target for the next pass)

Algebraically the implemented μ is
`μ = ρ·x₀³ / (2 γ^{3/2})` with `x₀ = sqrt(2σ_f/ρ)·r_bu/V₀` — i.e. Mott's own
circumferential length scale (Mott 1947 p.304, anchor `The length`, and his x₀ = 1.6/√γ — subscript zero, not `g` — in
example) closed into a mass by assuming the fragment is a **cube of edge
x₀/√γ**. For the 75mm that edge is 3.9 mm — but the wall is 6.0 mm thick, and
Tolch's mean recovered fragment (7 g) is ≈12 × 12 × 6 mm.

Candidate loci, in order of leverage:

1. **Cube closure.** A fragment is a wall-thickness plate, not a cube:
    m = ρ · t · L_axial · L_circ. With t = 6 mm and axial:circumferential
    aspect 2–3:1 (real shell slivers) this alone is ~3–5×.
1. **V₀ is the terminal Gurney velocity, not the case velocity at break-up.**
    x₀ ∝ 1/v and μ ∝ v⁻³; break-up at ~0.7–0.8 V₀ gives 2–3×.
1. Cross-check option: Mott's engineering closed form
    sqrt(μ) = B·t^{5/6}·d_i^{1/3}(1 + t/d_i) with B ≈ 0.0554 (g^½ mm^{-7/6})
    gives μ = 1.15 g (75mm) / 2.97 g (105mm) — inside Tolch's bracket.
    **Caveat: that form and B are NOT in the digitized Mott 1947 here**
    (this copy stops at the length scale); adopting it needs @librarian to
    source B.

(1)×(2) ≈ 6–15× — the right size, from two defensible physics corrections,
with no re-tuning of γ or σ_f.

## 5. Impact

μ too small / N₀ too high means the model breaks the shell into ~4–12× too
many fragments, each ~4–15× too light. That inflates hit counts while
shortening per-fragment reach — the same signature as the 7–33× B(r)
over-prediction in `../drag-gap-1944/b-vs-range.md`, and it is confounded with
the drag gap. Confirms the Tolch challenge's closing recommendation: fix the
Mott scale **before** any further drag calibration.
