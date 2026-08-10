# Model Review — case velocity at break-up, $f = v_{bu}/V_0$ (candidate C2)

**Scope:** `derivation.md`, `scoping.md`, `checks/f-breakup-limits.py` in this
folder. Workflow-B derivation pass; no `src/arty/` edits in scope (confirmed:
`git diff --stat main -- src/arty/` is empty for this branch).

**Open findings:** `collect-findings.py --for
experiment/fragmentation-field/updates/breakup-velocity-fraction` returns
none. The one `note` finding cited in the background (Kennedy card geometry
block) is correctly *not* relied on anywhere in this artifact — the
derivation cites the Martineau Table 5.3 closure and the shipped
`gurney_velocity` form instead (derivation.md §1, line 35-36).

## Verdict: **PASS**

No blocking findings. Two notes below, no action required.

______________________________________________________________________

## Verification performed

1. **Reproduced every numeric table in the derivation by re-running
    `checks/f-breakup-limits.py`.** All printed values (limit checks §4,
    Kennedy-bracket table, self-consistency-variant table, §5.1 registry
    table, §8 count-arm table, §6 double-count table) match the script's
    stdout digit-for-digit. The script imports `arty.fragmentation` and
    `arty.perforation` directly (no re-typed literals for the shipped
    functions) and its `mott_params`/`min_lethal_mass`/`perforation_threshold_energy`
    call shape matches
    `experiment/fragmentation-field/challenges/count-gap-1938/checks/count-chain-plug-shear.py`
    exactly (same `WoodPanelTarget()`, `S_PANEL=4.572`, `N_rec=779`) — the
    claimed "reproduces count-chain's published 2.47× exactly at $f=1$" is
    verified, not asserted.

2. **Independently re-derived the $\gamma'_{eq}=54.5f^2$ claim (§6) from the
    actual `mott_params` code**, rather than trusting the shorthand
    $\mu\propto\sigma_f/(\gamma'V^2)$ used in the prose. Because `mott_params`
    folds a shape-closure factor $\alpha$ back into an effective $\gamma$ that
    itself depends self-consistently on $\gamma'$ (via $x_0$), the naive
    power-counting I did by hand (which gives $\gamma'_{eq}=\gamma'f^{4/3}$,
    not $\gamma'f^2$) is wrong; a numeric root-find against the real
    `mott_params(shell, V0)` reproduces the paper's 48.44 / 44.01 exactly.
    **The derivation's number is right; a reviewer power-counting it from the
    simplified formula alone would wrongly flag it.** Recorded as a gotcha in
    memory (see below) so a future pass doesn't repeat that mis-derivation.

3. **Checked dimensional consistency** of eq. (1)-(4): $W=[p][V]=$ J ✔;
    $E(\eta)/E$ and $f$ dimensionless ✔; $\dot\varepsilon_{bu}=fV_0/r_{bu}$ in
    s⁻¹ ✔. No unit errors found.

4. **Checked boundary behaviour**: $f\to0$ as $\eta\to1^+$, $f\to1$ as
    $\eta\to\infty$, monotone in $\eta$ and $\gamma_g$ — all confirmed
    numerically by the check script, not just asserted. $\eta_{bu}=3$ is
    produced exactly by the shipped `_shell_geometry` (`r_inner_bu =
    r_inner*sqrt(3)`), matching eq. (4)'s requirement by construction; no
    div-by-zero or negative-sqrt risk at the values the code actually
    produces ($\eta\ge1$ always, by geometry).

5. **Provenance-checked every direct quote against its primary**, since two
    of the three load-bearing citations attribute a specific claim to a
    source and the rule requires this be checked, not assumed from a clean
    extraction:
    - Kennedy 1970 "Acceleration is completed after ... twice ... or ...
      seven times ..." — `grep` on `doc-reference/fragmentation/
      kennedy1970-gurney-energy/source.md:296` matches verbatim.
    - Kennedy 1970 Appendix B, "constant 7 [γ] law", "$Q = D^2/2(\gamma-1)$",
      "drops off sharply at" — all three anchors resolve at
      `source.md:751-780`, verbatim (including the γ≈2.7 renormalisation
      claim used in derivation.md §4's residual-tension discussion).
    - Gold 2017 "At the instant of fracture, let $r$ be the radius of the
      ring and $V$ be the velocity with which the shell is moving outwards"
      — resolves verbatim at
      `1-s2.0-S221491471730079X-main.md:56`. This is the citation that
      actually establishes the **criterion match** for this whole change
      (mott_params's $V$ argument is defined by its own cited source as a
      fracture-instant velocity, not the terminal one) — checked, not
      assumed.
    - Mott/Linfoot 1943 "For $r$ we take 2.2 inches, and for $V$, the
      velocity of the fragments, 2500 ft/sec" and "thick cased shells expand
      further than thin ones before breaking up" — both resolve verbatim in
      `quotes.md` (at lines 125 and 163 respectively; derivation cites 127/158,
      off by a couple of lines but the anchors are the phrases, which do
      resolve — no substantive drift).
    All primaries say what the derivation cites them as saying. No secondhand
    misattribution found.

6. **Checked the cited table's closure and criterion match.** §6/§8 read
    `tables/pit-screen-recovery.csv`
    (`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/`)
    via `csv.DictReader` in the check script, not a hand-typed array. Its
    `.invariant` passes (`check-table-invariants.py … pit-screen-recovery.invariant`
    → "5 rows, 6 checks, ok"). Sum of `n_frag` = 779 and mean mass from
    `wt_lb` = 7.40 g both match the numbers the derivation cites. This is the
    same table and the same denominator count-chain already established (not
    a new criterion introduced by this pass), so no new criterion-match risk
    is created here.

7. **Comparison-protocol check**: not applicable. This pass is a physics
    correction with a sensitivity/bracket analysis, not a fitted-vs-derived
    model comparison between rival laws.

8. **Layering / no-physics-in-.qmd**: not applicable yet — this pass adds no
    `.qmd` or `src/arty/` code; it is derivation-only, correctly scoped per
    `scoping.md` §6 and confirmed by the empty `src/arty/` diff.

______________________________________________________________________

## Findings

**[Note] §1's Martineau consistency remark is looser than its supporting data.**
Derivation.md lines 53-56 state the acceleration time doubling from
$M/C=0.498$ to $1.02$ happens "while the velocity approaches the same
fraction of its own Gurney value." The card's own extracted numbers
(`doc-reference/fragmentation/martineau1998-viscoplastic-shell-expansion/card.md`,
Figs. 5.7/5.8) give peak/Gurney ≈ 0.95-0.97 at $M/C=0.498$ and ≈ 0.98-1.0 at
$M/C=1.02$ — a real ~3-5 percentage-point difference, not "the same
fraction." **Impact:** none on the adopted $f$ or the count-arm result — this
remark is illustrative colour supporting the (separately, algebraically
derived) $M/C$-independence claim in eq. (2), not an input to any computed
number. Tag: Note, no rewrite required, but "the same fraction" could be
softened to "a similar fraction" if the derivation is touched again.

**[Note] §5's "γ_g≈3 ... is the exponent implied by Kennedy's own
Q=D²/2(γ-1)" overstates what that formula shows.** Line 196-197. Kennedy's
$Q=D^2/2(\gamma-1)$ is a generic relation between detonation velocity,
release energy and $\gamma$; it does not by itself "imply" $\gamma\approx3$
without also fixing $D$ and $Q$ for a specific explosive, and a back-of-
envelope check with textbook TNT values ($D\approx6900$ m/s,
$Q\approx4.3$ MJ/kg) returns $\gamma\approx6.5$ from that formula alone, not
3. **The conclusion itself is fine and is independently well-supported** —
Kennedy's own Table 3 and Fig. 9 (`source.md:780-884`) report WONDY input
$\gamma$ values of ≈2.5 (TNT) to ≈2.85 (Comp B, AWRE), with Fig. 9's axis
spanning 2.6-3.2, which is exactly the bracket the derivation already adopts
from a different, correct argument (symbol-table line 12: "2.5-3, adopt 3").
**Impact:** none on the adopted value or the band — the correct support for
$\gamma_g\in[2.5,3]$ already exists in the same source and is cited
elsewhere in the document; only the specific parenthetical justification via
the $Q$-formula is unsubstantiated as stated. Tag: Note — the parenthetical
should cite Table 3/Fig. 9 instead of (or in addition to) the $Q$ formula if
revisited, but nothing downstream depends on it.

No Blocking or Deferrable findings. The double-count risk (§6, A5) is
correctly identified as a genuine, unresolved residual risk rather than
closed, and is explicitly slated for `_limitations.qmd` at implementation
time — that is the right disposition for a risk that is real but not yet
falsifiable with sources in hand; it does not need to block this derivation
pass.

______________________________________________________________________

## Suggested corrections (not applied)

- Soften "approaches the same fraction" → "a similar fraction (within a few
  percent)" at derivation.md line ~55-56, or drop the clause since eq. (2)'s
  algebraic argument doesn't need it.
- Replace or supplement the "$Q=D^2/2(\gamma-1)$" parenthetical at line 196
  with a direct cite to Kennedy Table 3 / Fig. 9 (`source.md:780-884`), which
  actually gives the $\gamma\approx2.5$-3.2 range for TNT/Comp B that the
  sentence is trying to support.

______________________________________________________________________

## Scope note for the implementation pass

Confirmed §9's implementation instructions are consistent with everything
checked above: one new `src/arty/fragmentation.py` function, consumed only in
`mott_params`'s $x_0$ via `v_bu = f*V0`, terminal `gurney_velocity` and
`min_lethal_mass` untouched. The reviewer for that pass should re-verify the
`x0`/`mu` exponent chain against the actual code (not the simplified
$\mu\propto\sigma_f/(\gamma'V^2)$ shorthand in §6) if any $\gamma'$-equivalent
number is re-derived by hand — see verification item 2 above.
