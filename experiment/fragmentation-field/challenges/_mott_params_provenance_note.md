# Provenance note: `mott_params` (scratch — locate-and-summarize only)

**Scope**: this is a narrow locate/summarize pass. It does not judge whether
the value is sound and does not cross-check it against the Tolch challenge
doc — that is a follow-up pass.

## What the value is

`mott_params(shell, V0)` in `src/arty/fragmentation.py:209` computes the Mott
half-weight `mu` and fragment count `N0`:

```
mu = sqrt(2/rho) * (sigma_f/gamma)^1.5 * (r_bu/V0)^3
N0 = mass_shell / (2*mu)
```

It consumes two `SteelParams` fields (`src/arty/fragmentation.py:26-30`):
`sigma_f = 800e6` Pa (dynamic fracture stress) and `gamma = 65.0` (Mott
fragmentation parameter), applied to the `"WW2 US HE Shell"` steel entry
(`src/arty/fragmentation.py:33` onward).

## Origin

The parameter pair (and the `mott_params` formula itself) was **not**
introduced by the MVP1 extraction commit — it was carried over unchanged from
the original derivation notebook that predates the `src/` module by one day:

- Commit `6935633` ("feat(experiment): fragmentation-field model — Gurney,
    Mott, drag, ES-310 lethality", 2026-05-21) added
    `experiment/fragmentation-field/fragmentation-field.qmd`, which is the
    actual derivation artifact (no separate `derivation.md`/`scoping.md`
    existed at that point — this repo's per-change artifact convention postdates
    it, introduced in `3ad72fe` "feat(modeler): formalize challenge/update
    artifact workflow").
- Commit `45f833e` ("feat(fragmentation-field-mvp1): physics module, shell
    registry, Streamlit sensitivity app", 2026-05-22) extracted the notebook's
    inline `mott_half_mass()` function and its `sigma_F = 800e6`,
    `gamma_mott = 65.0` constants verbatim into `src/arty/fragmentation.py` as
    `mott_params()` / `SteelParams` defaults. Its own `design.md` states the
    notebook is preserved as "an independent derivation artifact" that the
    module extraction must stay in parity with.

## What it was fit to (per the notebook, `fragmentation-field.qmd` §3, "Mott:

Fragment Mass Distribution")

- **Formula source**: cited as "the PAFRAG-Mott formulation (Gold 2017, eq.
    16)" — i.e. attributed to a secondary source (Gold 2017) restating Mott's
    (1947) result, not re-derived in the notebook. Gold 2017 is not present in
    `doc-reference/`; Mott (1947) itself is —
    `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`.
- **gamma = 65**: the notebook's own note reads: *"Mott (1947) Table 1 gives
    γ ≈ 53 for 0.2%C steel and γ ≈ 67 for 0.3%C steel. US M1 shell bodies use
    SAE 1045 steel (≈ 0.45%C); γ ≈ 65 is a central estimate."* — i.e. not a fit
    to fragment-count data, but a value read off/near the high end of the Mott
    1947 Table 1 bracket, justified only by an (uncited-at-the-time) assumption
    that the M1 shell body is SAE 1045 steel.
- **sigma_f = 800e6 Pa**: notebook text: *"Dynamic flow stress at high strain
    rate is typically 800–1000 MPa for hardened steel, higher than the
    quasi-static value of 600 MPa."* — the low end of that stated range, no
    further citation given in the notebook.
- **Self-consistency check only, not a fit target**: the notebook checks the
    resulting `N(>0.5g)` against a stated "Mott model self-consistency" range
    of 3000-8000, attributed to "Gold (2017) uses γ=50, Comp-B, similar
    velocity" (`fragmentation-field.qmd` lines ~413-439). This is presented as
    a plausibility check on the output, not as the basis the γ/σ_F values were
    solved for.

## Later touch (not origin, for cross-reference only)

`experiment/fragmentation-field/updates/wdss1-steel-grade/derivation.md`
(2026-07-25) revisited the steel-grade identity (WD-X1335 → AISI 1335
inference) two months later and left a trail of comments in
`src/arty/fragmentation.py` (lines ~33-49) explaining that only the ratio
`sigma_f/gamma` is observable, and flagging gamma=65 as sitting near the top
of the Mott 1947 bracket rather than at the value the shell's *inferred*
%C would interpolate to. It did not change `sigma_f` or `gamma`'s numeric
values — it re-examined and annotated them.

## Citations to carry forward

- Mott, N. F. (1947) "Fragmentation of shell cases," *Proc. Roy. Soc. A* 189 —
    present in `doc-reference/fragmentation/gurney-equations-fragmentation/rspa.1947.0042.md`.
- Gold (2017), "PAFRAG-Mott formulation eq. 16" — cited by the notebook as the
    immediate source of the `mu` formula and the 3000-8000 self-consistency
    band; **not found in `doc-reference/`** (not verified present/absent
    exhaustively in this pass — a follow-up should confirm before relying on
    it).
