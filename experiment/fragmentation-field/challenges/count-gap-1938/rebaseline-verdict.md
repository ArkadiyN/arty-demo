# `count-gap-1938` re-baseline verdict — does the count chain's conclusion survive?

**Status: complete, but the *model* side of every claim below was evaluated
against shipped code as of 2026-08-08 *before* commit 6c1faff.** Read the
re-closure banner first; the re-baseline itself (the Tolch-series side) is
unaffected.

> **Re-closure banner — model numbers, 2026-08-08 (post-6c1faff / `50b734e`).**
> This file's §1 closure line and every model-derived figure in the tables
> below quote $M_\text{case} = 5755$ g, $V_0 = 807.5$ m/s, $\mu = 0.793$ g,
> $N_0 = 3627$. Commit 6c1faff re-anchored $\gamma'$ 65→54.5 and fixed an
> ogive/cylinder $V_0$ contradiction; `50b734e` sourced the 75 mm M48
> `mass_deductions` to TM-9-1901/TM-9-1904. Current shipped code gives
> **$M_\text{case} = 4980$ g, $V_0 = 864.4$ m/s, $\mu = 0.826$ g,
> $2\mu = 1.65$ g, $N_0 = 3016$** — so the "reproduces §2's stated values
> exactly" line below is a closure against the *then*-shipped code, not
> against today's. `count-chain.md` has been re-closed against current output
> and is the live document; three verdicts here move with it:
>
> - **§2 Fact 2 "void as written" — still void, magnitude restates.** The
>     threshold-free (E) result is **1.78–2.24×** on the Tolch-13.29 lb basis
>     (was 2.15–2.70×). The *model-mass* basis of (E) has gone **degenerate**:
>     $M_\text{case}$ = 4980 g now sits *below* the 5764.3 g recovered metal, so
>     φ > 1 past the coarsest screen and $m^\ast\to0$. Only the Tolch basis is
>     quotable.
> - **§4 "FAIL / count chain implicated" — no longer supported.** At a sourced
>     threshold the current model gives $N/779$ = 2.00 (78.6 J) and 1.73
>     (126 J), $N/700$ = 2.23 and 1.92 — at or inside the 2× PASS band on the
>     count arm. See `count-chain.md` §4's verdict-framing note.
> - **§3 C4 "single largest source of spread" — no longer holds.** Dropping
>     the coarsest screen now moves the threshold-free residual from 1.78× to
>     2.03× (up, not down to 1.19×), and the 1.19× came from the
>     numerator/denominator-inconsistent fuze-excluded variant already flagged
>     as an open finding. The derived $f = 1/\sqrt{\text{ratio}}$ corollary
>     restates to **0.67–0.75** on the Tolch basis.
>
> Of 20 published claims: 12 sound, 7 shifted, 1 void — that tally scores the
> *Tolch-series* re-baseline only and is not restated here.
>
> **§2 "Overall status" and §3 "Restatement" below are superseded by this
> banner.** Both were written against the pre-6c1faff shipped parameters and
> read as final; §2's "no verdict flips … stands unchanged" and §3's "No
> PASS/FAIL row changes side" are contradicted by the bullets above and by
> `count-chain.md` §4's verdict-framing note. Each carries an inline
> superseding note; `challenges/README.md` was restated to match on
> 2026-08-08 (this pass) — the earlier claim in this banner that the §3 text
> had *already* been applied to README was wrong, README then still carried
> the pre-6c1faff wording.

Block (E)'s arithmetic — the threshold-free test that carries the one void
verdict — was independently re-derived by the main agent before this file was
committed: at the finest screen φ = 5764.3/6028 = 0.9562 inverts to u ≈ 0.775,
giving m\* = μu² = 0.48 g and N = 3627·e^(−0.775) = 1671, against the script's
then-printed 0.48 g / 1672 / 2.15×; and f = 1/√ratio reproduces all four
printed velocity fractions. The identity is unaffected by the parameter
change: on current shipped values the same screen gives m\* = 0.49 g,
N = 3016·e^(−0.775) = 1390, ratio 1.78×. The refutation stands on its own
arithmetic.

Scope: re-run the claims published in
[`count-chain.md`](count-chain.md) against the re-baselined Tolch-1938
extracted-once series in
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/`.
Assess only — no `src/arty/` change is made or scoped here.

______________________________________________________________________

## 0. Findings ledger (appended as established)

- **Recovered pit count is 779, not 803.** The thread and its check script use
    803 throughout (`count-chain.md` §2 item 1, §2 closing paragraph;
    `checks/count-chain-decomposition.py` `N/803` column). The re-baselined
    `tables/pit-screen-recovery.csv` closes on **779** and only on 779 — the
    `pct_no` column reproduces every row's printed percentage at N=779 and misses
    by >1 pp at N=803 (`tables/pit-screen-recovery.invariant`, and the audit's
    `challenges/source-data-audit/checks/tolch-count-basis-closure.py`).
    Direction: makes the model's over-count **larger**, by 803/779 = 1.031 (3.1 %).

- **Mean recovered fragment mass is 7.40 g, not 6.85 g.** `count-chain.md` §2
    closing paragraph quotes "mean 6.85 g". The re-baselined series gives
    W_rec = 5764.3 g over 779 pieces = **7.400 g**; on the *old* 803 basis the
    same weight gives 7.178 g, so 6.85 g is not reproducible from this table on
    either count basis. Direction: **widens** the gap against the model's
    2μ = 1.587 g from 4.3× to 4.66×.

- **Recovered metal (5764.3 g) exceeds the model's whole case mass
    (5755.2 g).** So on a model-mass basis the pit accounts for 100.2 % of the
    case and any matched-mass comparison is degenerate at the tail. Quote the
    Tolch-metal basis (13.29 lb = 6028 g), not the model basis. Bears on C4.

______________________________________________________________________

## 1. Claim-by-claim verdict

Evidence lines are from
[`checks/count-chain-rebaseline.py`](checks/count-chain-rebaseline.py),
blocks (A)–(F); it reads the extracted-once CSVs, nothing hand-typed.

### §1 — the Mott-stage closure argument

| Claim                                                                                              | Verdict        | Deciding evidence                                                                                                                                                                                                                                                                                                                                                     |
| :------------------------------------------------------------------------------------------------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Eq. (5) collapse, sensitivity table, "**the Mott parameter stage cannot carry a 4–6× multiplier**" | **sound**      | (C) reproduced §2's then-stated values exactly (`M_case = 5755.2 g  V0 = 807.5 m/s  mu = 0.793 g  2mu = 1.587 g  N0 = 3627`); current shipped code gives `4980.0 g / 864.4 m/s / 0.826 g / 1.651 g / 3016`, matching `count-chain.md` §2 as re-closed — see banner. No Mott input is a Tolch series, so the re-baseline cannot touch the closure argument either way. |
| Row "$M_\text{case}$ 5755 g vs Tolch's 6030 g"                                                     | **superseded** | (A) recovered 5764.3 g = 12.708 lb at 95.6 % of 13.29 lb ⇒ Tolch metal 6028 g. Shipped $M_\text{case}$ is now **4980 g** (`50b734e`, sourced to Tolch's own 10.94 lb empty-shell-and-fuze metal); the row's *verdict* (no 4–6× multiplier available) is unaffected, its number is not.                                                                                |
| Row "$V_0$ model 807.5 vs Tolch's measured 838.2 m/s"                                              | **superseded** | Shipped $V_0$ is now **864.4 m/s** (6c1faff), i.e. 1.03× *above* Tolch rather than below. The 838.2 m/s is a scalar from Tolch Summary item 10, not one of the re-baselined CSV series — **not re-checked in this pass**.                                                                                                                                             |

### §2 — where the residual sits

| Claim                                                                                                                                                 | Verdict                                     | Deciding evidence                                                                                                                                                                                                                                                                                                         |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| §2 table: $m_{thr}$, $N(\ge m_{thr})$, and the "vs Tolch 700" column (4.4 / 4.2 / 2.5 / 2.2 / 1.5×)                                                   | **sound**                                   | (D) `N/700 = 4.38, 4.20, 2.54, 2.16, 1.45` at $m_{thr}$ = 0.022 / 0.035 / 0.403 / 0.605 / 1.281 g. The 700-perforation denominator is untouched by the re-baseline.                                                                                                                                                       |
| Every "$N/803$" figure in the thread (§2's "$N/803 = 2.2\times$"; §3 C2's whole sweep column)                                                         | **shifted**                                 | (D) `N/803(old) → N/779(new)`: 3.82→3.94, 3.66→3.77, 2.22→**2.28**, 1.89→**1.94**, 1.27→1.31. Uniform ×1.031; no row changes side of the factor-2 band.                                                                                                                                                                   |
| Fact 1 — "$N_0$ is **not** 4–6× too high; 3627 sits *between* Tolch's own ~5000 issuing and 803 recovered"                                            | **sound** (number shifted 803→779)          | (A) 779 recovered; 779 < 3627 < 5000 still holds. The sub-claim "4200 non-recovered events carry the missing 4.4 % at ~0.06 g each" re-closes: (5000 − 779) = 4221 events over (6028 − 5764.3) = 263.7 g ⇒ **0.0625 g** each.                                                                                             |
| Fact 2, arithmetic — "model declares 81–85 % of $N_0$ perforating; Tolch measures 700/5000 = 14 %; that ~6× *is* the L1 residual"                     | **sound**                                   | (D) `N = 3067, 2939` = 85 %, 81 % of `N0 = 3627`. Neither side uses the pit count.                                                                                                                                                                                                                                        |
| Fact 2, **inference** — "the residual is in the perforating *fraction*, **not the population**"                                                       | **void as written**                         | (E) is threshold-free — it matches *cumulative mass fraction* instead of imposing a mass cut — and still finds the model over-counting **2.15–2.70×** on the Tolch-metal basis (`thru4 … 2.15x`, `screen 2 … 2.70x`). A residual that survives deleting the threshold entirely is by definition not "not the population". |
| §2 closing decomposition — "~2–3× is a threshold-fit artefact × **~1.5–2.2× genuine count-chain excess**", evidenced by $N(\ge 0.63\text{ g}) = 1488$ | **shifted, and independently corroborated** | (F) `cut 0.63 g: N = 1488  N/779(new) = 1.91`; (D) fitted row `N/779 = 3.94`. So the split is **2.06× artefact × 1.91× genuine** (was 2.06 × 1.85). Band restates as **~1.6–2.3×**. Independently, the threshold-free (E) route reaches 2.15× on the same mass basis without using any mass cut.                          |
| §2 closing — "mean 6.85 g vs the model's $2\mu$ = 1.59 g"                                                                                             | **shifted (wrong on both bases)**           | Finding above: (A) `mean recovered mass = 7.400 g … same weight basis / 803 = 7.178 g`.                                                                                                                                                                                                                                   |

**Reconciling the void with the rest of §2.** §2's own closing paragraph
already asserts a "genuine count-chain excess" — i.e. a population term — so
"not the population" was internally inconsistent with the paragraph three lines
below it, independently of the re-baseline. The correct statement is:

> The residual is **predominantly** in the perforating fraction (~2.1× of the
> 3.9×), but ~1.2–2.7× of it is a genuine fragment-**spectrum** term that
> survives with the threshold removed.

The 1.2–2.7× spread is a *mass-bookkeeping* spread, not statistical: (E) gives
2.15–2.70× with the coarsest screen included and **1.19–1.73×** with it dropped
(`fuze-excluded variant`). See C4 below — that term is no longer "dismissed".

**Corollary — (E) measures $\mu$, which is exactly what C2 proposes to fix.**
For Mott's form, the mass fraction above $m$ is
$\varphi(u) = \tfrac12(u^2+2u+2)e^{-u}$ with $u=\sqrt{m/\mu}$, and the count
above is $N_0e^{-u} = (M/2\mu)e^{-u}$. At **matched $\varphi$**, $u$ is fixed,
so the model/Tolch count ratio is exactly $\propto 1/\mu \propto V_0^2$ — the
threshold-free ratio *is* the $\mu$-scale error, with no threshold, no drag and
no spray geometry in it. Hence C2's velocity fraction is directly readable:
$f = 1/\sqrt{\text{ratio}}$ ⇒ **$f$ = 0.61 (2.70×) … 0.68 (2.15×) … 0.76
(1.73×) … 0.92 (1.19×)**. That brackets the thread's assumed
$f\approx0.85$–0.9 **from below**. Flagged as an inference for a follow-up
derivation pass; nothing is changed in `src/arty/` here.

### §3 — the ranked sub-candidates

| Claim                                                                                                                                                                              | Verdict                                                                 | Deciding evidence                                                                                                                                                                                                                                                                                                                                                                                                  |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **C1** (fitted $E_{thr}$ is a hard KE step) — "leverage 2–3× of the residual, the biggest single term and the only unbounded one"                                                  | **sound**                                                               | (D)+(F): fitted 1.9 J row `N/779 = 3.94` vs the 0.63 g cut `1.91` ⇒ 2.06×; vs the sourced 78.6 J row `2.28` ⇒ 1.73×. Leverage band tightens to **1.7–2.1×**, still the largest term and still unbounded.                                                                                                                                                                                                           |
| §2/C1 — the 78.6 J row is an *independent, non-fitted* cross-check landing at 2.5× (700) / 2.2× (803)                                                                              | **sound** (denominator shifted)                                         | (D) `E_thr = 78.6 J … N/700 = 2.54  N/779(new) = 2.28`. Its provenance question (the 1944 Ordnance casualty column) is settled outside this thread and is **not** re-opened here.                                                                                                                                                                                                                                  |
| **C2** ($V_0$ is terminal Gurney, not case velocity at break-up) — leverage 1.2–2×, direction correct, crosses the PASS band at $f\approx0.85$–0.9, and 126 J matches at $f$ = 0.7 | **sound; $N/803$ column shifted; leverage now *measured***              | ×1.031 on every $N/803$ entry: 78.6 J → 2.28/1.87/1.49/1.16/0.86, 126 J → 1.95/1.60/1.28/0.99/0.73 for $f$ = 1.0…0.6. No crossing moves. The $f$ = 0.7 / 126 J match improves to **0.99**. And (E) now supplies $f$ independently of any threshold: 0.61–0.92 (corollary above).                                                                                                                                   |
| **C3** (single-exponential Mott tail) — "leverage unquantifiable … **only bites through C1**; at $m_{thr}\gtrsim0.6$ g the extrapolation is not exercised at all"                  | **shifted**                                                             | (E) exercises the spectrum only at $m^\ast$ = **0.48–1.97 g**, i.e. at or above Tolch's finest screen cut (0.63 g), with **no** sub-gram extrapolation — and still shows 2.15–2.70×. So the shape mismatch is measurable inside the validated mass range and does *not* only bite through C1. The priority advice ("do not chase before C1") survives on ranking grounds.                                          |
| **C4** (mass bookkeeping) — "bounded at ~5–10 %; **dismissed as a driver**; note only"                                                                                             | **shifted — dismissal sound, bound understated, no longer "note only"** | (A) the coarsest screen is 6 pieces / **926.7 g = 15.4 %** of recovered metal at 154 g mean, against the model's 200 g `mass_deductions` (3.3 %). Dropping it moves the threshold-free residual from **2.15× to 1.19×** (E, `fuze-excluded variant`) — it is now the single largest source of spread in the population term, not a 5–10 % footnote. Still not a 4–6× driver, so the dismissal *as a driver* holds. |
| **C5** (Tolch's 700 is detection-limited, not physics-limited)                                                                                                                     | **sound, untouched**                                                    | Not a numeric claim against any re-baselined series.                                                                                                                                                                                                                                                                                                                                                               |
| §3 recommendation — "check C1 first, alone; C2 is not blocked on C1"                                                                                                               | **sound**                                                               | Unchanged by the re-baseline; strengthened by the corollary, which makes C2 measurable with no threshold at all.                                                                                                                                                                                                                                                                                                   |

### §4–§5 — criterion, new math

| Claim                                                                                           | Verdict                               | Deciding evidence                                                                                                                                                                                                               |
| :---------------------------------------------------------------------------------------------- | :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "his two independent totals (700 panel perforations, **803** pit fragments) **differ by 15 %**" | **shifted**                           | 779/700 = 1.113 ⇒ **11 %**, not 15 %. Direction: the two Tolch totals agree *better* than published, which mildly tightens — never loosens — the verdict criterion.                                                             |
| PASS band "within **2×** of 700–803 *and* A→D ratio within 0.10 of 0.557"                       | **sound** (range restates to 700–779) | (B) `perf A = 1.49  perf D = 0.83  ratio = 0.5570` — the 0.557 the thread uses is exact on the re-baselined series. No row crosses the 2× line: the sourced 78.6 J threshold is 2.54 (700) / 2.28 (779) at $f$ = 1, still FAIL. |
| §4 status **FAIL / count chain implicated** at a sourced threshold                              | **sound**                             | (D) 78.6 J and 126 J both ≥ 2× on the 700 denominator.                                                                                                                                                                          |
| §5 new-math flag and Missing References (THOR Report 47; softwood ballistic limit)              | **sound, untouched**                  | No Tolch series enters either. @librarian still needed before C1's derivation pass.                                                                                                                                             |
| Fidelity target — "the present 4–6×"                                                            | **sound**                             | (D) fitted rows 4.38/4.20 (700) and 3.94/3.77 (779); Fact 2's ~6× perforating-fraction ratio unchanged.                                                                                                                         |

______________________________________________________________________

## 2. Overall status

> **Superseded in part (2026-08-08, post-6c1faff).** The paragraph below scores
> the *Tolch-series* re-baseline in isolation, against the then-shipped model
> parameters. Its "no verdict flips … stands unchanged" holds for that
> re-baseline and **no longer holds for the thread as a whole**: the
> 6c1faff / `50b734e` parameter changes move the count arm of §4's PASS test
> from unambiguously outside the 2× band (2.2–2.5×) to at-or-inside it
> ($N/779$ = 1.73–2.00, $N/700$ = 1.92–2.23), so §4's FAIL is no longer
> supported and the C1-is-the-largest-term headline restates. The live
> statement of the verdict is `count-chain.md` §4's "Verdict framing after the
> 2026-08-08 re-closure" note; read it in preference to the paragraph below.
> The A→D falloff-ratio arm of the PASS test remains unmet, so the test as a
> whole is still compound and still gated on a sourced $E_{thr}$ (C1). The
> "Net new for the next pass" note below (C4 must be closed before C2) is
> superseded too — see the banner's third bullet: C4 is no longer the largest
> source of spread, and C2 is no longer the term that decides the verdict.

**The thread survives the re-baseline: no verdict flips, one inference is
void, and every pit-count-denominated number moves up 3.1 %.** Of 20 published
claims, 12 are sound, 7 are shifted (all in the same direction — the model
over-counts slightly *more* than published), and exactly one is void: §2 Fact
2's "not the population", which was already inconsistent with §2's own closing
paragraph and is now refuted by a threshold-free test showing a 1.2–2.7×
population/spectrum residual. The thread's headline — C1 (fitted $E_{thr}$) is
the largest term at ~1.7–2.1×, with a genuine ~1.6–2.3× count-chain excess
behind it, and no `src/arty/` change scoped until @librarian lands a sourced
perforation threshold — stands unchanged.

**Net new for the next pass:** the threshold-free route (E) measures the
$\mu$-scale error directly and hands C2 a value, $f = 1/\sqrt{\text{ratio}}$ =
0.61–0.92, whose spread is set almost entirely by C4's fuze/base mass
bookkeeping — so **C4 must be closed before C2 is derived**, a reordering the
thread does not currently state.

## 3. Restatement for `challenges/README.md`

> **Superseded (2026-08-08, post-6c1faff).** The row and status-detail text
> below were applied to `challenges/README.md` and have since been replaced
> there, because "verdict stands" / "No PASS/FAIL row changes side" is false
> under current shipped parameters. **`challenges/README.md` is the live text**
> — it now reads "Re-baselined, then re-closed post-6c1faff — count arm now
> met-or-marginal; one inference void" and states which rows move. The block
> below is retained as the record of what the Tolch-series re-baseline alone
> concluded; do not re-apply it.

The thread has **no row** in the Threads table. Add one, after the
`mott-scale-gap/` row:

> | [`count-gap-1938/`](count-gap-1938/count-chain.md) | Why is Tolch 1938's absolute perforating-fragment count over-predicted 4–6×? | **Re-baselined — verdict stands, one inference void.** See [`count-gap-1938/rebaseline-verdict.md`](count-gap-1938/rebaseline-verdict.md) |

and a status-detail paragraph:

> **`count-gap-1938` status detail.** Re-baselined against the extracted-once
> Tolch series: the scoping verdict survives. The pit-recovered count is **779,
> not 803** — every $N/803$ figure in `count-chain.md` moves up 3.1 %, and the
> mean recovered fragment mass is 7.40 g, not 6.85 g. No PASS/FAIL row changes
> side. One inference is **void**: §2's "the residual is in the perforating
> fraction, *not the population*" — a threshold-free cumulative-spectrum test
> finds the model over-counting 1.2–2.7× with the threshold removed entirely.
> The decomposition restates as ~2.1× threshold-fit artefact × ~1.9× genuine
> count-chain excess. C1 (a sourced perforation threshold, blocked on
> @librarian) remains the recommended first move; C4 (fuze/base mass
> bookkeeping, 15.4 % of recovered metal against a 3.3 % model deduction) is
> promoted from "note only" and now gates C2.
