# Adversarial Review of Three "Void" Rulings

Date: 2026-08-03 · Reviewer: @model-reviewer (adversarial refutation pass)

Mandate: each of the three void rulings below was produced by a single pass. A
void is the least reversible verdict the audit can issue, so this pass assumes
each is wrong until independently reproduced from the evidence in its read set.

| #   | Ruling                                                              | Verdict of this pass                                                                                                                                     |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | C11 "Mach dependence buys nothing" — void                           | **upheld**, on stronger grounds than the pass gave                                                                                                       |
| 2   | count-gap-1938 §2 Fact 2 inference — void via a threshold-free test | **upheld with a narrower scope**; the test *is* threshold-free, but the quoted 1.2–2.7× band's lower half is an artefact — the true band is 2.2–2.7×     |
| 3   | BRL-126 "2740 ft/s" is not in that source — void                    | **refuted as stated.** The figure *is* in BRL-126. The downstream voids survive, but on different grounds, and the repair the ruling prescribes is wrong |

Evidence scripts re-run for this pass:
`updates/mach-dependent-fragment-drag/checks/mach-law-rebaseline.py`,
`challenges/count-gap-1938/checks/count-chain-rebaseline.py`, plus one new
script written for §2 below (`experiment/_scratch/tolch-case-mass-basis.py` —
**must be `git mv`'d to `challenges/source-data-audit/checks/` before this file
is committed**, per `.claude/rules/verification-scripts.md`).

______________________________________________________________________

## 1. C11 — "Mach dependence buys nothing" — **UPHELD**

### Reproduced

Every number in the verdict's Shock-B table is reproduced exactly by
`mach-law-rebaseline.py`:

| Law (one free scale each)       | casualties all | casualties M>0.7 | perforation | script line                                                                                           |
| ------------------------------- | -------------- | ---------------- | ----------- | ----------------------------------------------------------------------------------------------------- |
| best-fit constant               | 0.247          | 0.069            | 0.045       | `best-fit const, all pts = 2.140`; `best-fit const, M>0.7 = 2.875`; `best-fit const, all pts = 2.985` |
| Fig-3 corrected, best scale     | 0.199          | 0.052            | 0.036       | `Fig-3 CORRECTED, best scale on C_shape … scale_all=0.85 scale_sel=1.05`                              |
| Fig-3 at derived k=2600, no fit | 0.308          | 0.068            | 0.069       | `Fig-3 C_D(M) CORRECTED csv, k=2600`                                                                  |

Also reproduced: the Shock-B-alone improvement (old eyeballed → corrected CSV:
0.075 → 0.068 casualties M>0.7; 0.077 → 0.069 perforation), and the zero-fit
tie in the lethal band (Fig-3 0.068 vs best *fitted* constant 0.069). The
percentage renderings in the verdict are `exp(RMS) − 1` and are internally
consistent (0.069→7.1%, 0.052→5.3%, 0.045→4.6%, 0.036→3.7%) — the RMS is a
log-residual, so the dimensional bookkeeping closes.

### Is the "unfair comparison" framing itself sound?

Yes, and it is symmetric. I checked the specific way it could have been rigged:
the "best-fit constant" row takes 0.247 from the all-points fit (const 2.140)
and 0.069 from the M>0.7 fit (const 2.875) — two *different* constants — while
the Fig-3 row likewise takes 0.199 at scale_all=0.85 and 0.052 at
scale_sel=1.05 — two different scales. Both laws are refit per band. The
protocol is like-for-like, one free parameter each, in every cell.

### But the framing is not what carries the ruling — and the pass under-uses its own best evidence

Two grounds are stronger than the protocol argument, and neither needs it:

- **Zero free parameters on both sides, perforation column: Fig-3 at the
    derived k=2600 scores 0.069 against the adopted constant 2.6739 at 0.098** —
    a 30% RMS reduction with *nothing fitted anywhere*. "Does not beat a
    constant" is false on this line alone, with no protocol argument at all.
- **The refit configuration weakens the Mach law's own selling point.** Fig-3's
    preferred scale differs by 24% between bands (0.85 all vs 1.05 M>0.7). The
    derived, zero-free-parameter curve is not what wins the headline
    20–25%; a rescaled curve is. (The constant is worse on the same axis —
    2.140 vs 2.875, a 34% band disagreement — so the comparison still favours
    Fig-3, but the "derived" virtue should not be claimed for the 0.199/0.052
    row.)

### Scope limit this pass could not close

The same file carries a deferrable marker recording that `V0_FTS` has no provenance in
the processed 1944 source and is degenerate with the drag constant. The
20–25% margin is **not** shown robust to that exposure, and this pass did not
test it. That limits how strongly the *positive* claim ("the Mach law is
~20–25% better") may be stated. It does **not** touch the void: to restore
"the constant wins" a V0 perturbation would have to reverse a 20–25% gap with
both laws refitting, and it cannot make the zero-fit perforation result
(0.069 vs 0.098) go away, since both laws see the same V0 there.

**Verdict: upheld.** The C12 restatement that depends on it ("rejected as
immaterial at the stated fidelity target, not as unsupported by the data") is
the correct closure and is unaffected.

FINDING\[note\]: C11's Shock-B table headlines the per-band-refit row (0.199/0.052) whose Fig-3 scale varies 0.85-1.05 between bands; the zero-free-parameter perforation result (Fig-3 0.069 vs adopted constant 0.098) is a stronger and simpler void and should lead (affects: experiment/fragmentation-field/updates/mach-dependent-fragment-drag/rebaseline-verdict.md; since: 2026-08-03)

______________________________________________________________________

## 2. count-gap-1938 §2 Fact 2 — **UPHELD WITH A NARROWER SCOPE**

### Is block (E) genuinely threshold-free? Yes — I checked all three back doors

Read of `count-chain-rebaseline.py` block (E), line by line:

- **Lethality threshold** — block (E) never calls `min_lethal_mass` and no
    `E_thr` appears in it. The mass cut `m*` is *derived* by inverting the Mott
    cumulative-mass fraction at the observed φ, not imposed. Genuinely absent.
- **Drag chain** — `DragParams` is constructed at module level and used only in
    block (D). Block (E) consumes `N0`, `mu`, `M_case` and the pit CSV. `mu, N0   = mott_params(shell, V0)` with `V0 = gurney_velocity(shell)`; no drag term
    enters either. Genuinely absent.
- **Spray geometry** — block (E) reads `pit-screen-recovery.csv`, a total sand-pit
    recovery with no angular structure. `side-spray-density.csv` is used only in
    block (B). Genuinely absent.

The three confounds the ruling claims to have removed are removed. That part
of the claim holds.

### But a fourth confound takes their place, and the pass mis-handles it

φ = cum_w / M_tot makes the **total-mass basis** a free choice, and the script's
own output shows it has *more* leverage than the threshold it removed:

| basis                   | ratio at finest screen         |
| ----------------------- | ------------------------------ |
| model M_case (5755 g)   | 4.66× (φ = 1.0016, degenerate) |
| Tolch 13.29 lb (6028 g) | 2.15×                          |
| "fuze-excluded variant" | 1.19×                          |

A 1.19×–4.66× spread is not a footnote; the verdict quotes only 1.2–2.7× of it
and calls that the "genuine" over-count. Worse, **none of the three bases is
self-consistent**, and the quoted 2.15–2.70× band is a hybrid: it drops the
screen-1 *ratio* rows (5.58×/5.98×) from the band while keeping screen-1's
926.7 g inside `cum_w` for every later row.

### The fix, and it strengthens the ruling

Tolch prints the decomposition himself. `tolch-1938.md` line 232 (anchor
`Wt. empty shell & fuze`) gives, per round: loaded unfuzed shell 12.50 lb, TNT
1.56 lb, fuze (M39 P.D.) 2.35 lb, empty shell & fuze 13.29 lb — and
12.50 − 1.56 + 2.35 = 13.29 closes exactly. So **the fragmenting case metal is
10.94 lb = 4962.3 g**, and the fuze is 2.35 lb = 1065.9 g. Line 329 states the
No. 1 screen's 6 pieces (2.043 lb = 926.7 g) "are mostly pieces of fuze" — 87%
of the fuze weight, which is why that row is an outlier.

The script's "fuze-excluded variant" removes those 926.7 g from the
*numerator* but keeps the fuze-inflated model `M_case` (5755 g) in the
denominator. That single inconsistency is the entire source of the 1.19×
floor. Redone consistently — case metal on both sides, recovered case
4837.6 g = 97.5% of 4962.3 g, a closure the fuze-inclusive framing never
achieves:

| screen | φ      | m\* [g] | ratio (model N0=3627) | ratio (N0 from Tolch case mass) |
| ------ | ------ | ------- | --------------------- | ------------------------------- |
| 2      | 0.7723 | 2.14    | 2.58×                 | 2.23×                           |
| 3      | 0.9289 | 0.71    | 2.67×                 | 2.30×                           |
| 4      | 0.9622 | 0.42    | 2.61×                 | 2.25×                           |
| thru4  | 0.9749 | 0.30    | 2.52×                 | 2.18×                           |

(`experiment/_scratch/tolch-case-mass-basis.py`.) On a fuze-consistent basis
the threshold-free over-count is **2.2–2.7× at every screen**, with no basis
choice landing below ~2.2×, and — unlike the published table — it is *flat*
across screens, which is what a genuine spectrum-scale error should look like.

**Verdict: upheld, on partly different grounds.** The inference "the residual
is in the perforating fraction, not the population" is void: a ≥2.2× population
term survives with the threshold, the drag chain and the spray geometry all
deleted. But the verdict's stated band is wrong at its lower end, and that
matters for the repair: `f = 1/√ratio` in the §2 corollary must restate from
**0.61–0.92** to **0.61–0.68**, which no longer brackets the thread's assumed
f ≈ 0.85–0.9 — it excludes it. The C4 ruling ("spread is mass bookkeeping…
1.19×") must also be restated: the bookkeeping is *closeable* from the source's
own weight table, not an irreducible spread.

### A second defect surfaced by the same weight table

The count-gap verdict rules **sound** the row "$M_\text{case}$ 5755 g vs
Tolch's 6030 g". That compares the model's fragmenting-steel mass against
Tolch's *empty shell **and fuze*** weight. Like-for-like, Tolch's case metal is
4962 g and **the model's case mass is 16.0% high, not 4.5% low** — the sign of
the published comparison reverses. The magnitude is close to the fuze weight
net of the model's own deduction (1066 − 200 = 866 g vs the 793 g gap), which
is consistent with the fuze not being deducted from the M48 case mass at all.
This propagates directly: N0 = M_case/2μ, so 16% of every over-count ratio in
this thread is a case-mass input error, not a spectrum error. (Confirming
*where* the model's 5755 g comes from requires `src/arty/shells.py`, outside
this read set — that is the one grep that closes it.)

FINDING\[blocking\]: count-gap-1938 rebaseline-verdict.md rules sound the comparison "M_case 5755 g vs Tolch's 6030 g", but 6028 g is Tolch's empty shell AND fuze (tolch-1938.md:232, fuze 2.35 lb); case metal alone is 10.94 lb = 4962 g, so the model is 16% high not 4.5% low, and N0=M_case/2mu carries that error into every ratio in the thread (affects: experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md, experiment/fragmentation-field/challenges/count-gap-1938/count-chain.md, src/arty/shells.py; since: 2026-08-03)

FINDING\[deferrable\]: the "fuze-excluded variant" in count-chain-rebaseline.py block (E) removes screen-1 mass from the numerator but keeps the fuze-inclusive model M_case in the denominator, producing a spurious 1.19x floor; on a fuze-consistent basis the threshold-free band is 2.2-2.7x and the derived velocity fraction restates from f=0.61-0.92 to f=0.61-0.68 (affects: experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-rebaseline.py, experiment/fragmentation-field/challenges/count-gap-1938/rebaseline-verdict.md; since: 2026-08-03)

______________________________________________________________________

## 3. BRL-126 "2740 ft/s" attribution — **REFUTED AS STATED**

The ruling is a negative existence claim, so one counter-example settles it.
There is one.

### The figure is in BRL Report 126, three times

`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md`,
lines 146, 1658 and 1698 (Summary item 10), greppable anchor
`the velocity of the perforating fragments`:

> "the velocity of the perforating fragments duo to the explosive charge
> averaged **27^0 f/s** while that of the penetrat- ing fragments was
> **3030 f/s**."

`27^0 f/s` is a four-digit velocity whose third glyph the OCR lost. The
project's own card already resolved it —
`tolch-1938-m48-panel-pit-fragmentation/card.md:49` reads
`- **Perforating fragments:** 2,750 f/s` — and 2750 f/s = 838.2 m/s, which is
exactly the "Tolch's measured 838.2 m/s" the count-gap thread cites from
Summary item 10. The scoping's `2740 ft/s (835 m/s)` is the same figure with
the mangled glyph read as 4 rather than 5 (a 0.4% difference).

The ruling's evidence was a repo-wide grep for the literal string `2740`. That
grep cannot see a figure printed as `27^0`, and it did not see the card's
`2,750`. **"BRL 126 / Tolch 1938 does not contain this figure anywhere in the
processed source" is false**, and so is "traces instead to NWC TP 7124".

### The real defect is worse than the one the ruling names, and points the opposite way for repair

Two substantive errors in the scoping claim, both confirmed against the primary:

1. **Wrong spray class.** Tolch's ~2750 f/s is the **side spray** — Summary
    item 10 says it "was computed from the change in the angle of the sidespray
    with remaining velocity". BRL-126 reports **no** nose-spray velocity at all.
    The scoping calls it nose spray.
1. **The companion figure is inverted, not merely misattributed.** The scoping
    pairs it with "penetrating fragments at 1070 ft/s (326 m/s)". Tolch says
    penetrating fragments are **3030 f/s** — *faster* than perforating, and he
    explains why (smaller ballistic coefficients). The scoping has them 2.6×
    *slower*. The comparison Q1 leaned on is reversed in the source, not absent
    from it. (1070 f/s is indeed the low end of NWC TP 7124's range; only that
    half of the ruling's NWC trace holds.)

### What survives, and what a repair pass must now do differently

Every downstream **void** in §4 survives — scoping.md:61,65–78 (Q1 Option-C
rejection), :96–97 (corroboration bullet), :290 (literature table),
derivation.md:358 (§6 "range-panel artefact" paragraph), :379 (§7 open item 2).
"BRL 126's nose spray is higher than side spray" is unsupported either way.

But the ruling's prescribed repair — *re-attribute to NWC TP 7124 and reword
as a range* — is **wrong** and would introduce a second misattribution:

- `2740/2750 f/s` is BRL-126's, and is an **average**, for the **side spray**,
    perforating fragments. It should be re-attributed within BRL-126 to the
    correct spray class, not moved to NWC.
- `1070 ft/s (326 m/s)` should be **struck**, not re-attributed as half of a
    range: BRL-126's penetrating-fragment value is 3030 f/s and contradicts it.
- The blocking marker at `rebaseline-verdict.md:142` states the
    false premise verbatim and will route a repairer to the wrong fix. It must
    be rewritten before it is actioned.
- The derivation.md:358 reconciliation paragraph is void for a *different*
    reason than stated: not "BRL-126 does not say this", but "BRL-126 says
    nothing about nose-spray velocity, and its side-spray value (838 m/s) sits
    a factor ~1.9 below the model's V0_cyl = 1578 m/s". Whether that factor is
    a defect or a definitional mismatch (Gurney terminal vs velocity inferred
    from spray-angle change) is a @modeler question and is **not** settled here
    — it is, however, a live quantitative confrontation the void'd paragraph
    was standing in front of.

The main agent's escalation of the ogive/cylinder contradiction to `blocking`
and its routing to a Gate-3 @modeler pass is unaffected by any of the above and
remains correct.

FINDING\[blocking\]: frag-field-3d-geometry rebaseline-verdict.md:142 and its section 4 state the 2740 ft/s figure "is not in that source and traces to NWC TP 7124"; BRL-126 prints it three times as "27^0 f/s" (tolch-1938.md:146,1658,1698) and card.md:49 resolves it to 2,750 f/s, so the defect is a wrong spray class (side, not nose) plus an inverted companion value (Tolch's penetrating fragments are 3030 f/s, not 1070), and the prescribed re-attribution to NWC would be a second misattribution (affects: experiment/fragmentation-field/updates/frag-field-3d-geometry/rebaseline-verdict.md, experiment/fragmentation-field/updates/frag-field-3d-geometry/scoping.md, experiment/fragmentation-field/updates/frag-field-3d-geometry/derivation.md; since: 2026-08-03)

FINDING\[deferrable\]: the Tolch/BRL-126 processed source renders a four-digit velocity as "27^0 f/s" at tolch-1938.md:146,1658,1698 with the third digit lost, and card.md:49 states 2,750 f/s without recording that the glyph is unreadable on this surface; the disambiguating digit needs a read of source.pdf and a hedge in the card until then (affects: doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md, doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tolch-1938.md; since: 2026-08-03)

______________________________________________________________________

## The one fact each open item needs

- §2, model case mass: one grep of `src/arty/shells.py` for the 75mm M48 HE
    entry — does its mass bookkeeping deduct the 2.35 lb fuze? If not, the 16%
    is confirmed and every ratio in count-gap-1938 divides by 1.16.
- §3, the mangled digit: one read of the retained `source.pdf` page carrying
    Summary item 10 — is it 2740 or 2750? Either way the ruling is refuted; the
    digit only decides whether the scoping's transcription is also wrong.
