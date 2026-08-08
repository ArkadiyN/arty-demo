# ES310 Damage Criteria (FAS / U.S. Navy, 1998) — Card

## Identification

|            |                                                                         |
| :--------- | :---------------------------------------------------------------------- |
| Title      | Damage Criteria — ES310 Naval Weapons Engineering                       |
| Publisher  | U.S. Navy course notes, hosted by the Federation of American Scientists |
| URL        | `https://man.fas.org/dod-101/navy/docs/es310/dam_crit/dam_crit.htm`     |
| Local copy | `fas-es310-damage-criteria.md` (no PDF; the source is a live web page)  |
| Re-fetched | 2026-08-03, cell-for-cell against the live page                         |

**This is teaching material, not a primary vulnerability study.** Its own
worked example calls itself "a crude measure to be sure". It cites no
underlying casualty data and gives no derivation for any of its numbers. What
it is good for is a *stated, self-consistent* Pk|hit scale; what it is not is
evidence about the physiology behind that scale.

## Tables

Transcribed once into `tables/`, per `.claude/rules/source-data-fidelity.md`.
Consumers read the CSV; nothing re-types these series.

| Table                                              | CSV                                         | Closure                                              |
| :------------------------------------------------- | :------------------------------------------ | :--------------------------------------------------- |
| Table 3 — sample damage criteria for fragmentation | `table-3-fragmentation-damage-criteria.csv` | ordering only — see below                            |
| The page's hand-grenade worked example             | `worked-example-hand-grenade.csv`           | the page's own hit model and aggregation rule, twice |

**Anchors:** the printed caption `Table 3. Sample damage criteria for fragmentation effects.` with its column headers `Light Damage (Pk = 0.1)` /
`Moderate Damage (Pk = 0.5)` / `Heavy Damage (Pk = 0.9)`; and, for the example,
the sentence `find the Pk from a hand-grenade against personnel at 2 m`. No
bare line numbers — and see the divergence list below, which rules out
positional anchors into `fas-es310-damage-criteria.md` as well.

## Closure

**Table 3 has no internal closure and this card does not pretend otherwise.**
It states nine independent criteria with no arithmetic linking them, so a
plausible wrong cell reads exactly like a right one. Per the rule, absence of a
check is recorded as a finding rather than waved through — and the ordering
checks that *do* live in `table-3-fragmentation-damage-criteria.invariant`
(energy rising with damage level, energy rising with target hardness, Pk
constant down each column) are labelled ordering checks there, not closures.

**The closure comes from elsewhere on the page.** The page works a hand-grenade
example numerically, and to do so it must read a Pk|hit off Table 3 at 3000 J.
Only one row can supply the 0.8 it takes:

```
target            linear in E  linear in logE   verdict
personnel               0.767           0.817   MATCHES the page
aircraft                0.000           0.000   cannot produce 0.8
armored vehicle         0.000           0.000   cannot produce 0.8
```

3000 J sits *below* the aircraft row's own light-damage floor of 4 kJ, so
neither of the other two rows can produce a Pk|hit anywhere near 0.8. **The
worked example identifies the personnel row uniquely** — which is precisely the
row-inversion defence this whole rule exists for, and it is available here only
because the page states a criterion in one place and exercises it in another.

The example closes on its own terms as well (both checks in
`worked-example-hand-grenade.invariant`): the page's stated hit model
`Nhits = A(N₀/4πR²)` reproduces the Nhits it prints at both ranges, and its
two-branch aggregation rule reproduces both printed Pk values.

Script: `experiment/fragmentation-field/challenges/source-data-audit/checks/es310-worked-example-closure.py`

### What the closure does and does not certify

- **Certified:** the three personnel anchors — 100 J / 1 kJ / 4 kJ at
    Pk|hit 0.1 / 0.5 / 0.9 — are this page's personnel row, not another target's,
    and `src/arty/fragmentation.py:271-272` carries them faithfully (the script
    checks the shipped constants against the CSV, not against a retyped array).
- **Not certified — the interpolation between anchors.** The page states no
    functional form. `pk_given_hit` interpolates in log₁₀E; the page's prose
    reasons linearly in E. At the one point the page works, log₁₀E gives 0.817
    and linear-in-E gives 0.767 against a stated 0.8 — so the shipped scheme
    happens to sit closer, on a single point, which is agreement and not
    derivation. Any claim that turns on the *shape* of Pk|hit between anchors
    rests on a choice this document does not make.
- **Not certified — anything about the other two rows.** Aircraft and armored
    vehicle are transcribed for completeness and are unused downstream.

## Table 3 (from `tables/table-3-fragmentation-damage-criteria.csv`)

Fragment energy in kJ, as the table's own stub column states.

| Target          | Light (Pk = 0.1) | Moderate (Pk = 0.5) | Heavy (Pk = 0.9) |
| :-------------- | ---------------: | ------------------: | ---------------: |
| Personnel       |              0.1 |                   1 |                4 |
| Aircraft        |                4 |                  10 |               20 |
| Armored vehicle |               10 |                 500 |             1000 |

Row order is **as printed on the page**. The page also carries a Table 1
("Levels of damage and probability of kill") and a Table 2 ("Sample damage
criteria for blast effects"); **neither is transcribed here**, and neither is
cited anywhere in this repo. If a future pass needs blast criteria, it must go
back to the page — nothing in `doc-reference/` covers Table 2.

## Formulas (verbatim from the page)

- `Pk = Phit Pk|hit`
- `Nhits = A(No/4πR²)` — "Nhits is the expected number of fragments hitting the
    target; No is the initial number of fragments from the warhead; A is the
    frontal area of the target presented to the warhead; and R is the range of
    the target to the warhead."
- Aggregation: if Nhits > 1, `Pk = 1 - (1-Pk|hit)^Nhits`; if Nhits < 1, the
    expected count "can be taken directly as the probability of being hit", so
    `Pk = Nhits × Pk|hit`.
- **Lethal range** — "the range within which there will be a 50% probability of
    kill".
- Velocity decay, as printed: "For a typical fragment, about the size of a 120
    grain, 9-mm bullet, the velocity at 200 m is about 1/3 of its initial value,
    and therefore the kinetic energy is down to 10% of its original value."

## Divergences found on re-fetch, recorded not repaired

Every *number* in `fas-es310-damage-criteria.md` that this repo consumes is
faithful to the page. The divergences are structural and narrative — which is
the failure mode this audit exists to catch, since none of them would show up
in a glyph-level scan.

1. **The "Personnel Damage Criteria Table" in the extraction is not a table on
    the page.** It is Table 3's *personnel row* transposed into three rows, with
    the aircraft and armored-vehicle rows silently dropped and a "Caliber
    Reference" column welded on from prose found elsewhere on the page. The
    values are right; the *object* is a construction. A reader who cites "the
    ES-310 personnel damage criteria table" is citing something that does not
    exist, and would not find the aircraft row that sits beside it.
1. **Caliber references drift on the way into that table.** The page says ".22
    long bullet"; the extraction says ".22 Long Rifle equivalent", a specific
    cartridge designation the page never uses. The page says 4000 J is
    "sufficient to penetrate body armor" and names a "7.62 full metal jacket or
    .30-06 armor piercing bullet"; the extraction reduces this to
    "Armor-penetrating level".
1. **The velocity-decay figure is re-derived, not quoted.** The page prints "the
    kinetic energy is down to 10% of its original value"; the extraction says
    "~1/9 of muzzle value" — the square of the stated 1/3 velocity ratio, i.e.
    11.1%. Close, but it is the extractor's arithmetic presented as the source's
    number, and the page's own 10% is not a squared 1/3.
1. **The worked example is transcribed lossily.** The extraction keeps the two
    answers (0.9984 and 0.50) but drops `A = 1 m²` and `Pk|hit = 0.8` — the two
    numbers that make the example *closable at all*. This is the ordnance-1944
    failure in miniature: a summary that keeps the conclusion and discards the
    fields that identify what it was computed from. The full set is in
    `tables/worked-example-hand-grenade.csv`.
1. **The page never mentions 79 J or 80 J.** Confirmed by targeted re-fetch.
    See the next section.

## The "Implications for 79 J Threshold" section is not from this source

`fas-es310-damage-criteria.md` carries a section titled "Implications for 79 J
Threshold", a Key Findings bullet leading with "not 79–80 J", and a Summary
clause about "making the 79–80 J fixed threshold appear conservative". **None of
this is on the page.** It is a comparison between this source and a *different*
threshold used elsewhere in the repo, written into the reference document as
though the source had made it.

The comparison may well be correct — it is not adjudicated here. What is wrong
is its location: it is a modelling claim in a reference doc's clothing, so a
@modeler or @model-reviewer that reads this card inherits it as a premise
rather than reviewing it as an argument. That is exactly the shape of the Tolch
"Drag Model Relevance" defect (`.claude/rules/source-data-fidelity.md`, and
Phase 2.5d of the source-data audit), and the structural fix is the same: it
belongs in a `derivation.md` or `_limitations.qmd` where the reviewer sees it.
Marked as a finding in `fas-es310-damage-criteria.md`; **not repaired here**,
per the audit's deferred-repairs scope.

Note the argument is also load-bearing downstream —
`experiment/fragmentation-field/_limitations.qmd` §374-396 turns on the same
ES-310-vs-78.6 J criterion mismatch — so striking it from the card must not
mean losing it.

## Provenance of this card

1. **Original extraction** into `fas-es310-damage-criteria.md`, undated, by
    summary rather than transcription.
1. **Independent re-fetch of the live page, 2026-08-03**, in three targeted
    passes: the table cells, then Table 3 reproduced verbatim with its
    neighbours named, then the worked example and the prose sentences. Three
    passes because the first returned a summary that answered "NOT STATED" to
    the Pk-value question while Table 3 in fact carries it — the
    fetch-summary-is-not-a-transcription lesson recorded on the aisi-1335 card,
    recurring here.
1. **Closure** via the page's own worked example, uniquely identifying the
    personnel row and verifying the shipped constants against the CSV.

### Why this document had no card until now

It was found by the Phase 2.5c admissibility sweep
(`checks/doc-reference-admissibility-sweep.py`), which initially reported it as
**uncited** — because the sweep grepped directory slugs and every consumer,
including `src/arty/fragmentation.py`, names the source "ES-310" instead. Once
the sweep learned to search report designators, the count went from 0 shipped
files to 4. It was the widest-footprint unverified source in the repo:
30 citing artifacts, no card, no CSV, no closure.
