# C4 — which metal weight is the spectrum denominator (Tolch 1938)

*Workflow A assessment, count-gap-1938 thread. Closes the last open
sub-candidate C4. Script:
[`checks/count-chain-spectrum-basis.py`](checks/count-chain-spectrum-basis.py);
the block-(E) fix lands in
[`checks/count-chain-rebaseline.py`](checks/count-chain-rebaseline.py).*

## 0. Verdict in one line

**The criterion-correct denominator is Tolch's 10.94 lb = 4962 g *empty
unfuzed shell* (case metal alone), paired with a fuze-excluded numerator — not
his 13.29 lb pit-recovery basis.** On that consistent basis the threshold-free
residual is **1.8–2.1×** (not 1.19×, and not the 2.1–2.2× floor the open
finding predicted, though the top of that band is reached). The count arm
therefore stays **FAIL** — outside the ≤1.5× acceptance band on every
admissible reading — and the *spread* attributed to C4 collapses: the basis
choice is worth ≈0.2× within the fuze-consistent family, not the 1.19×→2.7×
range the open findings anticipated. **No `src/arty/` change follows** (this is a
criterion-match choice on the comparison, not a shipped defect).

## 1. What each Tolch figure measures

From the round-weights table (`tolch-1938.md` line 232, greppable anchor
`Wt. loaded unfuzed shell`; CSV
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/round-weights.csv`):

| Tolch column             | Rd 1 value   | what it is                                   |
| ------------------------ | ------------ | -------------------------------------------- |
| Wt. loaded unfuzed shell | 12.50 lb     | case metal + TNT                             |
| Fuze (M39 P.D.)          | 2.35 lb      | fuze, a separate machined body               |
| Wt. of TNT charge        | 1.56 lb      | explosive                                    |
| Wt. empty shell & fuze   | 13.29 lb     | case metal + fuze                            |
| *(derived)* 12.50 − 1.56 | **10.94 lb** | **case metal alone** (empty *unfuzed* shell) |

10.94 lb is not printed by Tolch; it is arithmetic on his own printed columns
under his own stated definitions, and closes to the printed 13.29 lb
(10.94 + 2.35 = 13.29 ✓, `tables/round-weights.invariant`).

> **Nomenclature correction.** `count-chain.md` §2 (and the C4 brief) call
> 10.94 lb "Tolch's *empty shell & fuze* metal". That phrase is Tolch's own
> label for **13.29 lb**. 10.94 lb is the empty *unfuzed* shell. This mislabel
> is the proximate cause of the second open finding below — see §4.

Tolch's recovery percentages ("% of empty shell & fuze") divide by 13.29 lb,
so his headline *95.6 % of the metal recovered* is a fuze-inclusive
book-keeping statement about the pit census, **not** a statement about case
metal.

## 2. Why 10.94 lb is the criterion-correct denominator

The threshold-free test (block E) matches on **cumulative mass fraction of one
physical body** and then compares counts. For that to be criterion-clean, the
"body" must be the same object on both sides.

- **Model side.** `mott_params` generates $\mu$ and $N_0$ from
    $M_\text{case}$ = 4980 g — the explosive-driven cylinder wall, with
    `mass_deductions` = 975 g of fuze+booster already removed
    (`src/arty/shells.py`, `mass_shell = mass_total − mass_filler − mass_deductions`; `50b734e`). The Mott spectrum describes *that* body and
    nothing else. It agrees with Tolch's 10.94 lb = 4962 g to **0.4 %** — an
    independent corroboration, since 4980 g comes from geometry + TM-9-1901/1904
    fuze weights, not from Tolch.
- **Observed side.** Tolch states outright that screen No. 1 is not case
    metal: *"The fragments caught on No. 1 screen are few in number but an
    appreciable part of the original shell weight, about 15%. **These fragments
    are mostly pieces of fuze.**"* (`tolch-1938.md` line 329, greppable anchor
    `These fragments are mostly pieces of fuze`). Screen 1 is 6 pieces /
    926.7 g at a 154 g mean — against a fuze weighing 2.35 lb = 1066 g.

So the fuze appears on the observed side as **6 coarse pieces carrying 16 % of
the recovered mass**, and on the model side as **nothing at all**. Any pairing
that leaves it in one and not the other is a basis mix.

Two internally consistent pairings exist, and only one is criterion-matched:

| pairing                 | numerator                                  | denominator                               | status                                                                                                                       |
| ----------------------- | ------------------------------------------ | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **fuze-excluded**       | census minus screen 1 (773 frag, 4837.6 g) | $M_\text{case}$ 4980 g (≡ Tolch 10.94 lb) | **criterion-matched** — both sides are case metal                                                                            |
| fuze-inclusive          | full census (779 frag, 5764.3 g)           | Tolch 13.29 lb = 6028 g                   | internally consistent as *census book-keeping*, but scores a case-metal Mott spectrum against a shell+fuze body. Mismatched. |
| mixed (as shipped in E) | full census (5764.3 g)                     | $M_\text{case}$ 4980 g                    | **inadmissible** — drives $\varphi$ to 1.16 > 1, $m^\*\to0$, ratios meaningless                                              |

The fuze-inclusive row is not merely inelegant: the Mott distribution is a
statement about a *casing* breaking up under internal loading. A machined fuze
body is not a Mott-fragmenting cylinder wall, and its 6 recovered pieces at
154 g mean are ~166× the model's $\mu$ = 0.929 g — visibly a different
population, not a tail of the same one.

## 3. The corrected numbers

Fuze-excluded, denominator $M_\text{case}$ = 4980 g
(`count-chain-rebaseline.py` block E, "fuze-excluded variant"):

| through screen | cum n | cum w [g] | $\varphi$ | $N_\text{model}$ | ratio     |
| -------------- | ----- | --------- | --------- | ---------------- | --------- |
| 2              | 272   | 3832.4    | 0.7696    | 513              | **1.89×** |
| 3              | 527   | 4609.4    | 0.9256    | 1019             | **1.93×** |
| 4              | 669   | 4774.5    | 0.9587    | 1259             | **1.88×** |
| thru 4         | 773   | 4837.6    | 0.9714    | 1396             | **1.81×** |

**Band: 1.81–1.93×** at $f=1$ (screen 1 taken as entirely fuze). Using Tolch's
own 10.94 lb = 4962 g instead of the model's 4980 g gives 1.87–1.97× — a
0.4 % denominator change moving the answer by ≈0.06×, so *which* of the two
case-metal figures is used is immaterial. What is not immaterial is $f$; see
the sensitivity below.

For contrast, the fuze-*inclusive* consistent pairing (13.29 lb) gives
1.58–1.99× over the same four rows — overlapping, and lower at the finest cut
only because the 926.7 g of fuze inflates $\varphi$ toward 1 faster than it
inflates the count. Either way the answer is **~1.6–2.0×, never below 1.5×**.

### Sensitivity to "mostly" — and a mass-closure bound on it

Tolch says screen 1 is *mostly* fuze, not *entirely*, so let $f$ be the fuze
fraction of the 926.7 g caught on screen 1; the remaining $(1-f)\cdot926.7$ g
is case metal and must be added back to the numerator.

**$f$ is not free: mass closure bounds it.** Screens 2–thru4 already hold
4837.6 g of case metal against $M_\text{case}$ = 4980 g. Adding back more than
142.4 g would recover more case metal than the case contains, so
$f \ge 0.846$. Tolch's qualitative "mostly" and the shell's own mass budget
therefore agree: screen 1 is 85–100 % fuze.

| $f$   | fuze [g] | case added back [g] | $\varphi$(thru4) | scr 2 | scr 3 | scr 4 | thru4                            |
| ----- | -------- | ------------------- | ---------------- | ----- | ----- | ----- | -------------------------------- |
| 0.70  | 648.7    | 278.0               | 1.0272           | 2.34× | 2.92× | 4.00× | 3.46× *(excluded — $\varphi>1$)* |
| 0.846 | 784.3    | 142.4               | 1.0000           | 2.10× | 2.31× | 2.49× | — *(degenerate)*                 |
| 0.90  | 834.0    | 92.7                | 0.9900           | 2.02× | 2.16× | 2.21× | 2.24×                            |
| 0.95  | 880.4    | 46.3                | 0.9807           | 1.95× | 2.04× | 2.03× | 1.98×                            |
| 1.00  | 926.7    | 0.0                 | 0.9714           | 1.89× | 1.93× | 1.88× | 1.81×                            |

**Conditioning caveat (new, and it matters for how these rows are quoted).**
The finest cut sits at $\varphi\to1$, where $\mathrm{d}x/\mathrm{d}\varphi$
diverges — a 3 % change in recovered mass swings its ratio from 1.81× to 3.46×.
That row is ill-conditioned and must not be quoted as a point estimate. The
**screen-2 cut ($\varphi\approx0.77$) is the well-conditioned anchor**: across
the whole closure-admissible range $f\in[0.85,1.0]$ it moves only
**1.89×–2.10×**.

So the honest fuze-consistent statement is **1.8–2.1×**, anchored on the
screen-2 cut, with the finest-cut rows quoted as a range and not a value.

## 4. Disposition of the two open findings

**(i) `review-void-rulings.md:204` — "fuze-excluded variant keeps the
fuze-inclusive model $M_\text{case}$ in the denominator, producing a spurious
1.19× floor."**

**Resolved — overtaken by `50b734e`, and its diagnosis no longer holds.** When
the finding was raised (2026-08-03) `mass_deductions` was a 200 g placeholder,
so $M_\text{case}$ ≈ 5755 g did carry ~775 g of un-deducted fuze and the
finding was correct on the state of the code that day. `50b734e` replaced the
placeholder with the sourced 975 g fuze+booster, and the current
$M_\text{case}$ = 4980 g is fuze-excluded by construction. The fuze-excluded
variant is therefore now the *consistent* pairing, not the inconsistent one.
The 1.19× floor is gone (it does not appear in any current run); the band it
predicted post-fix (2.1–2.2×) turns out to be the *upper edge* of the
fuze-consistent family rather than its floor: the answer is **1.8–2.1×**, with
2.1× reached only at the mass-closure limit $f=0.85$. The finding's
*velocity-fraction* restatement (f = 0.67–0.69
rather than 0.61–0.92) rested on that superseded band and should not be
carried forward from it. Marker deleted.

**(ii) `review-criterion-match.md:337` — "block (D) divides an
energy-thresholded whole-shell count by a size-thresholded recovery census and
a perforation-thresholded panel count; quote (E)'s figure instead."**

**Upheld and now actionable, but its replacement number restates.** The
finding is right that (D) is basis-mixed, and right that the threshold-free
(E) comparison is the criterion-clean one to quote. Its specific replacement
figure (2.15×) was computed on the pre-`50b734e`, fuze-inclusive (E) state and
is doubly superseded (basis and $M_\text{case}$ both changed since); it is not
close to the current criterion-clean fuze-excluded band **1.8–2.1×** and is
not cited anywhere in current artifacts. Marker deleted and replaced by the
corrected pointer in `rebaseline-verdict.md`.

Separately, block (E)'s *first* basis row ("model M_case", full census) is a
live basis mix — $\varphi$ = 1.16 > 1 is the tell — and is now labelled
inadmissible in the script rather than printed as if quotable.

## 5. What this does to the count arm

C4 was the last open sub-candidate. Composing with §4's standing residuals:

| reading                                     | residual      | in band (≤1.5×)? |
| ------------------------------------------- | ------------- | ---------------- |
| threshold-free, fuze-consistent (this pass) | 1.8–2.1×      | **no**           |
| threshold-free, fuze-inclusive consistent   | 1.58–1.99×    | **no**           |
| plug-shear cut 0.166 g vs 779 / 700         | 2.25× / 2.51× | **no**           |
| 0.63 g (finest census cut) vs 779 / 700     | 1.51× / 1.68× | **no**           |

Every admissible pairing sits above the band. **C4 discharged: it is a
criterion choice worth ≈0.2× inside the correct family, not a 4–6× driver and
not the largest source of spread. The count arm closes FAIL** (not
INDETERMINATE — no remaining candidate has the leverage to reach 1.5×).

**No `src/arty/` change.** The shipped $M_\text{case}$ = 4980 g is the
fuze-excluded case metal the Mott spectrum should be built on, and it is
corroborated to 0.4 % by Tolch's own 10.94 lb. The defect was in the
*comparison*, in `checks/`, not in the model.
