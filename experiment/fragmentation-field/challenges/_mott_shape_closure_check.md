# Is the cube-shape mass closure literature-supported? — verdict: NO

Literature-fidelity check on the Mott mass closure flagged as the leading
scale-gap suspect in `_mott_scale_verdict_ledger.md` §4. No `src/arty/` changes.

Passage checked: `experiment/fragmentation-field/_governing-equations.qmd`
§3 "Mott: Fragment Mass Distribution" (eq. 3–4 and the γ/σ_F note).
Sources read:

- Gold (2017), *Defence Technology* 13(4) 300–309 — in-repo at
    `doc-reference/fragmentation/fragment-size-distribution-conwep/1-s2.0-S221491471730079X-main.md`
    (the directory name is misleading; this **is** the cited "Gold 2017").
- Mott (1947) `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`.

## 1. What the .qmd claims

Eq. (4), μ = √(2/ρ)(σ_F/γ)^{3/2}(r_bu/V₀)³, is attributed to
"the PAFRAG-Mott formulation (Gold 2017, eq. 16)". **That attribution is
literally correct** — it is verbatim Gold's eq. (16) (source line 112).
The γ note then sources the *value* γ = 65 to "Mott (1947 §3) tabulates … 0.45%C
→ γ = 67". **That is the defect: the two γ's are different quantities.**

## 2. What Gold actually specifies (source lines 68–82, eqs. 2–7)

- eq. (2): x₀ = (2σ_F/ργ′)^{1/2}·r/V is the average **circumferential breadth**
    only. γ′ is the material fracture-scatter constant — Mott's tabulated one.
- Prose before eq. (4): fragments are "irregularly sized **prism-shaped**"
    splinters, "idealized … with a **parallelepiped** (Mott, 1943) having a
    longitudinal length l₀, breadth x₀, and a thickness t₀".
- eq. (4): μ = ½·**α**·ρ·x₀³ with **α = (l₀/x₀)·(t₀/x₀)** — an explicit
    shape factor, not 1.
- eq. (6): γ ≡ **α^{−2/3} γ′**, "since the … relationship warrants knowledge of
    the average fragment mass but not the shape". eq. (7)/(16) is then the
    shape-**absorbed** form.

So the literature closes x₀ into a mass with an explicit aspect-ratio factor and
then *hides* it inside γ. Using eq. (16) with γ = γ′ (Mott's table) asserts
α = 1 — i.e. l₀ = t₀ = x₀, a **cube**. Nothing in either source supports α = 1;
both describe elongated wall-thickness prisms.

## 3. Mott 1947 supports the cube even less

Mott's x₀ (source line ~160, and x_g = 1.6/√γ in the p.306 worked example) is a
**circumferential length**; Mott never converts it to a mass in this paper.
Mott's own statistics (p.305, findings (1)–(3)) give **average length ≈ 1.5 x₀**,
not x₀ — a further 1.5× per linear dimension the .qmd does not carry.

## 4. Gold's own γ is calibrated, not composition-read

Gold runs γ = 50 for HF-1 steel/Comp-B (source line 190) and Fig. 7 (line 214,
after ref. [18]) plots empirical γ **against explosive CJ pressure** — γ varies
with the loading, not the carbon content. The .qmd's carbon-content sourcing of
γ = 65 is therefore doubly off-book: wrong symbol (γ′ vs γ) and wrong
calibration axis.

## 5. Size of the correction (bounding only — for the derivation pass)

μ ∝ α at fixed x₀. For 75 mm M48: x₀ ≈ 3.9 mm (ledger §4), wall t₀ = 6.0 mm →
t₀/x₀ ≈ 1.54; l₀/x₀ ≈ 2.6 (l₀ ≈ 10 mm, vs Tolch's ~12 mm mean recovered
fragment) → **α ≈ 4**, giving μ ≈ 0.95 g — the mass-constrained Tolch fit.
So the single unsupported α = 1 accounts for most of the ledger's 4–8× gap,
with the residual left to the break-up-velocity item (ledger §4 item 2).

**Open, for the derivation pass:** x₀ predicted (3.9 mm) is ~3× below Tolch's
recovered breadth (~12 mm). α cannot absorb that; either γ′ is not 65 in the
PAFRAG sense, or the breadth estimate in the ledger is coarse. Do not treat
α ≈ 4 as calibrated — treat it as the literature-shaped free parameter that
must be fixed against data, exactly as Gold does with γ.

## Verdict

The cube closure is a **simplification introduced by the model author, not by
the cited literature.** The literature specifies a parallelepiped closure whose
aspect-ratio factor α is folded into a *calibrated* γ; the model took the
shape-absorbed formula but supplied a *material* γ′ from Mott's composition
table, silently setting α = 1.
