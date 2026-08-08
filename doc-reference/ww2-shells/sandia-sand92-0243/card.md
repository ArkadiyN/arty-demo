# SAND92-0243 — Fragment Hazard Zone Analyses for Explosive Test Facilities

## Identification

|            |                                                                         |
| :--------- | :---------------------------------------------------------------------- |
| Title      | Fragment Hazard Zone Analyses for Explosive Test Facilities             |
| Report     | `SAND92-0243`, UC-742, Unlimited Release                                |
| Author     | Manuel G. Vigil, Explosive Components Division                          |
| Publisher  | Sandia National Laboratories, Albuquerque NM                            |
| Date       | Printed May 1992                                                        |
| Pages      | 63 (main text + Appendices A–D)                                         |
| Local copy | `source.pdf` (gitignored per `.gitignore:58`), summary in `index.md`    |
| Text layer | **present and clean on all 56 PDF pages** — no vision extraction needed |

## Why this document is in the repo

It is the source of the drag-coefficient range cited across the
`drag-gap-1944` thread — `checks/drag-coefficient-calibration.py` tests
"1.2 (SAND92-0243 low)" and "1.7 (SAND92-0243 high)" against the model's
current value, and `b-vs-range.qmd` and `_limitations.qmd` repeat the range in
prose. It is also cited in `updates/frag-field-3d-geometry/` as the
cylinder-Gurney baseline and trajectory framework.

## Admissibility

This scan carries a **real text layer on every page**, so the strongest
available check is not a closure but a direct positional read of the page text
— the same standard applied to AMCP 706-249, and better than a closure
because it answers "was the right line read?" directly. Every quotation below
is from that text layer.

Three arithmetic closures are declared anyway, because they are what catch a
value landing on the wrong line, and all three pass:

| Table                                   | CSV                               | Closure                                                                            |
| :-------------------------------------- | :-------------------------------- | :--------------------------------------------------------------------------------- |
| §9 parameter ranges (items a, c–g)      | `discussion-parameter-ranges.csv` | ordering only — declared weak, not a closure (see below)                           |
| Site and material constants (items h–j) | `site-and-material-constants.csv` | density span = min/max of the three materials; ideal-gas air density; ft/s ↔ mm/µs |

The three passing closures on `site-and-material-constants`:

1. **Density span closes on the materials.** §9 item (c) gives 2.77–16.6 g/cc;
    items (b) and the appendix `Conditions:` blocks name aluminium 2.77, steel
    7.86, tantalum 16.6. The span is exactly the min and max. Two
    independently-printed places in the document.
1. **Air density closes on the stated atmosphere.** The appendices' 0.000957
    g/cc is within 0.15 % of the dry-air ideal-gas value for the 12.06 psia and
    30 °C those same appendices state.
1. **The velocity bounds close across units.** The Introduction prints them
    twice, in ft/sec and mm/µs; the two printings agree to the printed
    precision. Swapping the two ends moves the residual from 0.04 to 7.4, so
    this catches a bound inversion.

**The drag-coefficient row has no closure available anywhere in the document.**
Flagged for human review per `.claude/rules/source-data-fidelity.md` — absence
of a check is a finding, not a pass. What follows is why no check exists.

## Findings on the cited drag coefficient

### 1. The report states two different ranges on the same page, and the repo cites the weaker one

Page 18 (§9, *Discussion and Conclusions*) carries both:

- In the parameter-range list, item (e): **"Drag coefficient: 1.0 to 1.71"** —
    this is the range actually spanned by *this report's computed trajectory
    data*.
- Three paragraphs later, in prose: *"The drag coefficient is a function of
    initial fragment velocity\*. The drag coefficient can vary between **1.2 and
    1.7**."* — a general statement about tumbling plate/disk fragments.

Every citation in this repo uses **1.2–1.7**, i.e. the prose sentence. It is a
faithful quotation. But the report's own data floor is **1.0**, not 1.2, and
`drag-coefficient-calibration.py` uses 1.2 as "SAND92-0243 low end".

This is the audit's own defect class in a new form: not a mis-transcribed
digit, but a number taken from the wrong sentence on the right page, where a
different sentence on the same page gives a different range for the same
symbol.

**Direction of the effect** (for Phase 3/4 to settle, not this card): the
thread's argument is that the model's $C_D$ sits far below the literature. A
floor of 1.0 rather than 1.2 narrows that gap without closing it. The expected
verdict is *shifted*, not *void* — but that is the modeller's call.

### 2. SAND92-0243 does not supply a $C_d(V)$ law at all — it delegates

The report states the range but never the function. Its own analyses take
**"Drag coefficient = variable (Ref. 1)"** in the `Conditions:` block of
Appendices A, B and C — and Ref. 1 is:

> Manuel G. Vigil, "Explosively Driven Missile Trajectory Parameters for
> Various Fragment Materials and Velocities," Sandia National Laboratories,
> **SAND91-0277**, June 1991.

**SAND91-0277 is not in the repo.** So "1.2–1.7, velocity-dependent
(SAND92-0243)" cites a document that has the range but not the dependence.
Anything downstream that needs the *functional form* is citing a delegation,
the same shape as MIL-S-10520D delegating mechanical properties to the
projectile drawing.

The asterisk after "initial fragment velocity\*" has **no corresponding
footnote text** on the page — confirmed against the raw text blocks in printed
order, not just the reading-order extraction. Whatever it pointed at is absent.

### 3. Criterion match is an open question, not settled here

Recorded for @model-reviewer, whose mandate this is. The report's $C_d$ is
defined for **"tumbling (assumed), plate or disk like irregular fragments"**
and enters the range calculation through

```
K = 0.262(Rhop)Sf/[Cd(Rhoa)(Re + 1)]        (9)
```

i.e. always as a product with the shape factor $R_e$ and the effective
thickness factor $S_f$, never alone. Whether a bare $C_D$ in `src/arty` is the
same quantity is exactly the criterion-match check, and this card does not
answer it.

The report also warns its data "may not give accurate results for more regular
shapes like spheres or cubes or other more aerodynamically stable fragments."

## Irregularities recorded as printed, not repaired

- **Appendix D's `Conditions:` block cites the wrong equation for $C_d$.**
    Appendices A–C say "Drag coefficient = variable (Ref. 1)"; Appendix D says
    "Drag coefficient = variable (**Equation 12**)". Equation 12 as printed is
    `R = Vb2/(K)(g)` — the range parameter, not a drag coefficient. An internal
    inconsistency in the source.
- **The symbol `K` is used for two different quantities.** The List of Symbols
    defines "K Fluid flow parameter, plate or disk, 0.93"; equations (8)–(9)
    define `W = KQ` with `K = 0.262(Rhop)Sf/[Cd(Rhoa)(Re + 1)]`, a ballistic
    coefficient with units. Anyone reimplementing these equations must not carry
    0.93 into equation (9).

## Anchors

Greppable strings in the PDF text layer, no bare line or page numbers:

- `9. DISCUSSION AND CONCLUSIONS` — the parameter-range list and both $C_d$
    statements.
- `6. FRAGMENT TRAJECTORY THEORY` — equations (7)–(12).
- `LIST OF SYMBOLS` — the symbol definitions, including the duplicated `K`.
- `REFERENCES` — the Ref. 1 delegation.

## Provenance of this card

Read directly from `source.pdf`'s text layer on 2026-08-02 with
`experiment/fragmentation-field/challenges/source-data-audit/checks/sandia-cd-provenance.py`,
which prints the two $C_d$ statements, the delegation, and the raw block order
that shows the orphaned footnote marker. The gating probe
(`checks/vision-gating-probe.py`) confirms 56/56 pages carry real text and 0
fall under the thin-page threshold, so no vision extraction is involved and
none of the vision-pipeline failure modes apply to this document.
