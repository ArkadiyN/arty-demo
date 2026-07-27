# Challenge: Reproducing the 1944 Ordnance Dept. B-vs-range data

**Resolved (do not re-derive):** no new `src/arty/` math is needed for this
comparison. `lethal_density_point` (`src/arty/fragmentation.py`) and the
four-zone counterpart `four_zone_lethal_density_field` (`src/arty/zones.py`)
already return the lethal-fragment areal density $\rho_L(x,y,z)$ \[m$^{-2}$\] at
a field point — the same physical quantity as the historical document's
$B$ = "average number of effective hits per sq. ft. of target area at
distance $r$ from burst" (`doc-reference/wound-ballistics/ordnance-dept-1944- shell-fragment-damage/card.md`). Presenting our output in the document's
convention is a unit conversion (m$^{-2}$ → ft$^{-2}$) plus an azimuthal
average over already-computed field points at fixed range — a data reduction
of existing outputs, not new physics.

## 1. Problem statement

The project ships two independent lethality pathways for the ground field —
**Family A**, the graded ES-310 `pk_given_hit(E)` + presented-area `A_p(γ)`
mass-integral kernel (`_expected_kills_3d_vec` / `_four_zone_familyA_eval`),
and **Family B**, the Poisson binary-cut lethal-density kernel
(`lethal_density_point` / `four_zone_lethal_density_field`, transformed to
$P_k = 1-\exp(-\rho_L A_\text{ref})$ downstream). Both are exercised, per
`openspec/specs/pkill-ground-field/spec.md`, for the single-zone
(`arty.fragmentation`) and four-zone (`arty.zones`) geometries. This
challenge asks two separate questions. First: do Family A and Family B, run
at the shell/burst parameters the Ordnance Dept. document specifies,
reproduce the *casualty* $B$-vs-range curves it tabulates (Tables 43, 51, 59)
for the three shells this project already carries in its registry
(`src/arty/shells.py`: `"75mm M48 HE"`, `"105mm M1 HE"`, `"155mm M107 HE"`)?
Second, separately and only qualitatively: does our rendered ground $P_k$
polar/heatmap output resemble the shape of the document's damage-pattern
figures (Figs. 67–73, 93–100, 117–125, saved as images under that
`doc-reference` folder and described, not digitized, in `card.md`) — i.e. a
roughly ellipse-with-forward-bias fringe around the burst, not a comparison
of the shaded-band radii to specific numbers.

## 2. Governing equations for the comparison

No new equations — this section only fixes the reduction from each family's
existing output to the document's $B$.

**Family B → $B$.** `lethal_density_point(x, y, z, h_b, alpha_rad, delta_rad, N0, mu, s_grid, mmin_grid)` (single-zone) and
`four_zone_lethal_density_field(zones, aof_deg, h_b, drag, rho_steel, z, ...)`
(four-zone) already return $\rho_L$ \[m$^{-2}$\] — the identical quantity to
$B$ \[ft$^{-2}$\]. The reduction is
$$
B_\text{model}(r) \;=\; \left\langle \rho_L(r\cos\phi,\, r\sin\phi,\, z=0)\right\rangle_\phi \times (0.3048\,\text{m/ft})^2 ,
$$
i.e. sample the existing field builder's output grid on a ring of horizontal
ground range $r$ at $z=0$ (ground burst, matching the card's ground-burst
tables) and average over the azimuthal angle $\\phi$ already spanned by the
grid, then convert m$^{-2}!\\to!$ft$^{-2}$ by the area-scaling factor
$(0.3048)^2 \\approx 0.0929$.

**Family A → $B$.** `_expected_kills_3d_vec` / `_four_zone_familyA_eval`
return an *expected lethal-hit count on the target* at each ground point,
i.e. $N(x,y) = \rho_L(x,y)\cdot A_p(\gamma)$ with the presented area $A_p$
already folded in (see the `Ap` term inside `_expected_kills_3d_point`'s
integrand, `src/arty/fragmentation.py:1004`). To recover the areal-density
quantity $B$ comparable across families and to the card, divide out the same
$A_p(\gamma)$ that the field builder already computes at that point:
$B_\text{model}(r) = \langle N(x,y)/A_p(\gamma(x,y))\rangle_\phi \times
(0.3048)^2$. This is arithmetic on existing outputs (`A_p` is returned by
the existing `presented_area(gamma, posture)` call the same builder makes),
not a new physical model.

**Casualty threshold.** The card's own casualty definition is 58 ft-lb
kinetic energy (`card.md` line 25), a different value from the project's
existing default (`E_LETH_DEFAULT` in `src/arty/fragmentation.py` = 1000 J,
$\approx$ 737 ft-lb — the ES-310 $P_{k|hit}=0.5$ "moderate personnel kill"
anchor, not the card's threshold). For a like-for-like comparison, Family B's
Mott $m_\text{min}(s)$ table is fed the card's own 58 ft-lb ($\approx$ 78.6 J)
value as an explicit override of `E_leth`, not the project's default; Family
A's `pk_given_hit(E)` ES-310 curve is used as-is (its own 1000 J-scale
calibration is out of scope for this pass's Family-B-only comparison).

## 3. Numerical study to run

For each of the three shells (`"75mm M48 HE"`, `"105mm M1 HE"`,
`"155mm M107 HE"`), at the ground-burst geometry the card's own tables use
(`h_b = 0`, angle of fall as recorded per shell — the card's ground-burst
casualty figures state remaining velocity and gun range rather than a bare
angle of fall; take the angle of fall the project's existing
`gurney_velocity`/registry striking-condition already assumes for that shell,
or, if unconstrained, sweep angle of fall and report the $B(r)$ sensitivity
band rather than pick one value):

1. Run the existing four-zone field builder (`four_zone_lethal_density_field`
    for Family B, `_four_zone_familyA_eval` via `four_zone_line_split` for
    Family A — both already exposed, no new wiring) over a ground grid dense
    enough to resolve $r = 20$ to $225/300/400$ ft (per-shell max range from
    Tables 43/51/59), converting the grid to feet only for the comparison
    plot/table, never internally.
1. Reduce to $B_\text{model}(r)$ per §2 for both families, at the same
    $r$ values the card tabulates (20 ft first row, then the card's own row
    spacing — read directly from `card.md`'s tables when producing the run,
    no interpolation guesswork needed since the card gives the full row set).
1. Tabulate $B_\text{model}(r)$ alongside the card's $B(r)$ for casualties,
    per shell, per family — a 3-shell × 2-family × N-range side-by-side table.
1. Separately, render the existing ground $P_k$ polar/heatmap output (already
    produced by the notebook's existing plotting path, e.g.
    `_field-plots.qmd` / `_four-zone-3d.qmd`) at the ground-burst,
    height-of-burst-30-ft, and height-of-burst-60-ft geometries the
    figure captions specify, and visually compare the overall shape (forward-
    biased ellipse vs. more symmetric ring, fringe extent) to the
    corresponding saved images — no shaded-band digitization.

## 4. Verdict criterion

**Quantitative (Tables 43/51/59):** the model reproduces the data for a
shell/family if, at every tabulated range $r$ within the card's stated
distance range for that shell, $B_\text{model}(r)$ falls within a factor of
2× of the card's $B(r)$ (i.e. $0.5 \le B_\text{model}/B_\text{card} \le 2$),
**and** the two curves' shape agrees — $B(r)$ is monotonically decreasing in
both, with no sign of the model producing a qualitatively different falloff
(e.g. a different power/exponential order, or a spurious plateau/ring the
card's data does not show). A factor-of-2 band is used (rather than a tight
percentage) because $B$ compounds several independently-uncertain physical
inputs already flagged as approximate in this project's `derivation.md`/
`_limitations.qmd` (Mott $\gamma$, Gurney $V_0$, drag $C_D$, ES-310
$P_{k|hit}$) — a tight match would indicate accidental parameter tuning, not
a validated model; a >2× miss or wrong-shaped curve is a genuine defect
worth a correctness pass. If Family A and Family B disagree with each other
by more than the same 2× band at a given $r$, that is reported as a finding
(a family divergence), separately from either family's agreement/disagreement
with the card.

**Qualitative (damage-pattern figures):** the model reproduces the pattern if
the rendered $P_k$ field's high-probability region is forward-of-burst-axis
elongated (matching the "Θ" pear/ellipse shape visible in Figs. 67–73 etc.)
rather than a symmetric ring or a uniform disk, and if the fringe (the
lowest non-zero contour) extends to roughly the same range as the card's
darkest-shade boundary (≥1 hit per 25 sq ft) — judged by eye, not measured;
any qualitative mismatch (e.g. a symmetric ring where the card shows a
forward lobe) is reported as a finding for a follow-up correctness pass, not
adjudicated numerically in this study.
