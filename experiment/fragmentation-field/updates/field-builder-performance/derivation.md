# Field-builder performance refactor — numerical-methods note

**Scope.** Pure performance/vectorisation of the field/volume/line builders in
`src/arty/zones.py` and `src/arty/fragmentation.py`. **No physics changed**: the
governing equations, parameters, belt gate, quadrature scheme and public
signatures/return shapes are untouched. This note records the equivalence
argument for each reformulation and the before/after timings. Every reformulation
below is either **bit-exact** (same floating-point operations, only reordered
into array ops) or reproduces the scalar algorithm element-for-element; the
measured max abs difference vs the original per-cell code is machine epsilon
(≤ 1.4e-15) on every builder — see §6.

The builders fall into four kernels; each is handled separately.

______________________________________________________________________

## §1 Family A — graded-kernel expected-count fields

Functions: `four_zone_field`, `_four_zone_field_split`, `four_zone_line_split`
(zones.py); `compute_frag_field_3d` (fragmentation.py).

Per ground cell each zone contributes (original inner loop)

$$
v_z(x,y) ;=; \\frac{A_p(\\gamma)}{2\\pi s^2, 2\\sin\\theta^z,\\delta}
\\int pdf^z(m),\\mathrm{pk}\\big(\\tfrac12 m (V_0^z e^{-\\lambda(m)s})^2\\big),dm ,
\\quad (1)
$$

with $s=\\sqrt{x^2+y^2+h_b^2}$ (ground plane $z=0$) and
$\\gamma=\\arcsin(h_b/s)$.

**Key observation (s-only factorisation).** Every factor in (1) — $\\gamma$, the
drag attenuation $e^{-\\lambda(m)s}$, and the $1/s^2$ spreading — is a function of
the slant range $s$ **alone**. The only per-direction dependence is the belt
membership gate $|\\cos\\Theta-\\cos\\theta^z|\\le\\sin\\delta$, with
$\\cos\\Theta=(x\\cos\\alpha+h_b\\sin\\alpha)/s$, which is a hard 0/1 mask that the
refactor preserves unchanged.

**Reformulation.** For each zone: build the belt mask (vectorised), gather the
slant ranges of the in-belt cells, evaluate the mass integral (1) exactly on
those cells with a single `(n_belt, n_mass)` `np.trapezoid`, and scatter back.
The geometric/presented-area prefactor $A_p(\\arcsin h_b/s)/(2\\pi s^2,2\\delta)$
is computed per cell at the exact $s$ (shared across zones bar the $1/\\sin\\theta^z$
scaling). This is the *same* set of floating-point operations as the loop, so it
is **bit-exact** (measured 2.2e-16). The `(n_cells×n_mass)` working array is
processed in chunks of ≤ `_FAMILY_A_CHUNK = 2e6` elements to bound peak memory
regardless of grid size or belt width.

*Note (rejected alternative).* An earlier attempt tabulated $v_z(s)$ on a dense
1-D $s$-grid and interpolated. Because $v_z(s)$ inherits the sharp $1/s^2$ and
`pk_given_hit` structure it needed ~10⁵ nodes for a clean field, and left a
residual ~1e-3 interpolation error at 4000 nodes. The exact in-belt vectorisation
above is both faster (the belt is a fraction of the grid) and bit-exact, so it
was preferred over interpolation.

`compute_frag_field_3d` is the single-zone variant. It differs only in that its
spreading factor uses the point's **own** polar $\\sin\\Theta$ (not a fixed
$\\sin\\theta^z$), so $v = J(s)/\\sin\\Theta$ with $J(s)$ the mass integral: the
mass integral is still evaluated exactly on in-belt cells and multiplied by the
per-cell $A_p/(2\\pi s^2,2\\sin\\Theta,\\delta)$. Bit-exact (3.3e-16).

______________________________________________________________________

## §2 Family B — lethal-density fields $\\rho_L(x,y,z)$

Functions: `four_zone_lethal_density_field` (zones.py),
`compute_lethal_density_field_3d` (fragmentation.py), and their `_vol` stackers.

Per point each zone contributes
$\\rho_L = \\mathbb{1}[\\text{belt}]\\cdot g(s), N_0^z e^{-\\sqrt{m\_{\\min}(s)/\\mu^z}}$,
$g(s)=1/(2\\pi s^2,2\\sin\\theta^z,\\delta)$, where $m\_{\\min}(s)$ is **already** a
precomputed 1-D table interpolated with `np.interp`. So the whole point kernel is
a function of $s$ and the belt mask — trivially vectorisable over the `(x,y)`
layer with array `np.interp`/`np.exp`. **Bit-exact** (≤ 1.1e-16): same table,
same interpolation, same formula, just array-valued.

**Volume builders** (`four_zone_lethal_density_volume`,
`compute_lethal_density_volume_3d`, and the `pkill_volume` transforms of them).
The dominant cost was **rebuilding the `m_min` bisection table once per z-layer**
(30 layers × 4 zones × 400 nodes of 80-iteration bisection). The tables depend on
slant range only, not on $z$, so one is tempted to build a single shared table
over the whole box. **That was tried and reverted**: it changes the $s$-grid node
placement, so the volume's $z=0$ layer no longer *bit-matches* the standalone
`field(z=0)` (the four `..._volume_z0_matches...` / `..._is_point_transform`
tests assert exact equality). Instead the layer loop is kept — each layer builds
its own table with the *same* `slant_range_grid` the field uses — and the
bisection is made cheap by §4. This keeps the volume's $z=0$ layer bit-identical
to the field and every existing test passing, while still removing the cost.

______________________________________________________________________

## §3 Vectorised column integral — P(kill) ground fields

Functions: `pkill_field_3d` (fragmentation.py), `four_zone_pkill_field`,
`four_zone_pkill_line` (zones.py), via the new `_pkill_columns_vec` engine.

$P_k(x,y)=1-e^{-\\lambda}$, $\\lambda=w\_\\perp\\int_0^h \\rho_L(x,y,z),dz$, evaluated
by the **belt-segmented composite-midpoint** rule of the original code: the
column $[0,h]$ is split at the belt-membership crossing heights
(`belt_column_breakpoints`), and each sub-interval is integrated with `n_seg`
strictly-interior midpoint nodes (never an endpoint, to avoid the belt-edge 0/1
coin-flip — preserved exactly).

**Vectorisation.** The set of belt-edge target cosines $K=c\\pm\\sin\\delta$ is
*global* (independent of $(x,y)$), so for each $K$ the crossing heights solve one
quadratic $A\\zeta^2+B\\zeta+C=0$ (§5.1 of the target-height-intercept derivation)
whose coefficients are arrays over cells. `_vec_quadratic_roots` reproduces the
scalar `_stable_quadratic_roots` element-for-element (same cancellation-free
Numerical-Recipes form, same $A!\\to!0$ linear degeneracy and double-root
branch). Per-cell breakpoints are stacked into a padded `(P, M)` array, sorted,
and every consecutive pair defines a segment; midpoint nodes and weights are
built with `n_seg`, $\\rho_L$ is evaluated at all `(P, M-1, n_seg)` samples with
array ops, and $\\lambda$ is the weighted sum. Columns are chunked to bound memory.

**Equivalence.** Every *true* membership flip is captured (as in the scalar
path), and the midpoint samples on each smooth segment are identical. The one
deviation is that near-coincident breakpoints are **not** deduplicated (the
scalar path merges roots within 1e-12): an unmerged pair leaves an extra segment
of width $\\lesssim$1e-12 whose midpoint contribution is $\\rho_L\\cdot!$1e-12, and
shifts the neighbouring segment's nodes by $\\lesssim$1e-12 — a
$\\mathcal{O}(\\text{1e-12})$ perturbation on $\\lambda$. Measured max diff on
$P_k$: 1.4e-15 (float reassociation dominates), i.e. bit-exact in practice.

______________________________________________________________________

## §4 Vectorised `m_min` bisection — `build_mmin_table`

The single largest cost in the density/volume/pkill builders was
`build_mmin_table` doing a Python list-comprehension of scalar
`min_lethal_mass` bisections (one 80-iteration root-find per $s$-node).
$\\mathrm{KE}(m;s)=\\tfrac12 m(V_0 e^{-\\lambda(m)s})^2$ is monotone in $m$, so a
single bisection is vectorised over all $s$-nodes at once. To stay
**bit-identical** to the scalar routine — which breaks each element's loop early
once its bracket narrows below `tol` — each node is *frozen* (its `lo/hi` stop
updating) the iteration its bracket first falls below `tol`, exactly reproducing
the scalar early-stop. Verified `np.array_equal` (0.0 diff) against the scalar
`min_lethal_mass` over dense $s$-grids for $V_0\\in{500,900,1500,1800,2500}$
m/s. Because the field/volume/pkill builders all route through this one function,
the change is bit-exact everywhere it appears.

______________________________________________________________________

## §5 Achieved tolerance

All reformulations are exact or scalar-reproducing; the achieved max abs
difference vs the original per-cell implementation is **≤ 1.4e-15** on every
builder (machine epsilon), far below the model's own fidelity (±30%-class). No
interpolation-error budget is spent — the interpolation-table approach of the
early Family-A attempt was discarded in favour of exact vectorisation.

______________________________________________________________________

## §6 Regression max-diff and before/after timings

Representative parameters: 155 mm M107 HE (Tier-1, four active zones), AoF 30°,
$h_b=2$ m, $\\delta=15°$, STANDING. Harness: `experiment/_scratch/bench.py`
(`capture` on the original tree → `ref.npz`; `compare` on the refactor). Timings
are single-call wall-clock, this machine.

### Max abs difference vs original (worst over all cases): **1.44e-15**

| builder                                     | max abs diff |
| ------------------------------------------- | ------------ |
| `_four_zone_field_split` (total + per-zone) | 2.2e-16      |
| `four_zone_field`                           | 2.2e-16      |
| `four_zone_line_split`                      | 2.2e-16      |
| `compute_frag_field_3d` (field + cross)     | 3.3e-16      |
| `four_zone_lethal_density_field`            | 5.6e-17      |
| `compute_lethal_density_field_3d`           | 1.1e-16      |
| `four_zone_pkill_field`                     | 1.4e-15      |
| `pkill_field_3d`                            | 2.2e-16      |
| `four_zone_pkill_line`                      | 2.2e-16      |
| `four_zone_pkill_volume`                    | 1.1e-16      |
| `pkill_volume_3d`                           | 1.1e-16      |
| `four_zone_lethal_density_volume`           | 4.4e-16      |

### Timings (ms)

| case                                          | before | after | speedup |
| --------------------------------------------- | -----: | ----: | ------: |
| `_four_zone_field_split` n=161, r=200         |  436.1 | 115.4 |    3.8× |
| `four_zone_field` n=161                       |  425.5 | 100.8 |    4.2× |
| `four_zone_line_split` n=481                  |   31.5 |   5.3 |    5.9× |
| `compute_frag_field_3d` n=161                 |  183.0 |  27.6 |    6.6× |
| `four_zone_lethal_density_field` n=150        |  426.3 |   4.6 |     93× |
| `compute_lethal_density_field_3d` n=150       |  130.8 |   1.1 |    119× |
| `four_zone_pkill_field` n=150, r=60           | 2482.2 | 436.0 |    5.7× |
| `pkill_field_3d` n=150                        |  824.0 |  87.4 |    9.4× |
| `four_zone_pkill_line` n=481                  |  319.3 |   9.2 |     35× |
| `four_zone_pkill_volume` n=40, nz=30          | 7813.0 |  74.1 |    105× |
| `pkill_volume_3d` n=40, nz=30                 | 2031.2 |  20.0 |    102× |
| `four_zone_lethal_density_volume` n=40, nz=30 | 7713.8 |  74.9 |    103× |

Headline detailed cases on the refactored code (the app's max slider settings):

| case                                                            |   after |
| --------------------------------------------------------------- | ------: |
| `four_zone_pkill_field` **n=300**, r=60 (ground-field expander) | 1226 ms |
| `pkill_field_3d` **n=300**, r=60                                |  275 ms |

The detailed four-zone ground field (n=300, 90 000 columns), previously ~10 s
(2.5 s at n=150, scaling $\\propto n^2$), is now ~1.2 s; every other slow case is
sub-100 ms. All 220 existing tests pass; `ruff` clean.

______________________________________________________________________

## §7 Review closure (follow-up pass)

`review.md` returned **PASS-with-limitations**. Each finding was addressed as
part of normal work; nothing was deferred to a future pass.

| review.md finding                                                                             | disposition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Deferrable** — dropped defensive bounds assert in the vectorised ρ_L/P_k paths              | **Closed in code.** Added a cheap vectorised guard (one `min`/`max` over the query set, compared to `s_grid[0]`/`s_grid[-1]`) to `_four_zone_density_layer_vec` (zones.py) and the per-chunk loop of `_pkill_columns_vec` (fragmentation.py), restoring the loud-failure parity the scalar `lethal_density_*_point` references keep. In `_pkill_columns_vec` the guard is taken over **weighted** samples only: collapsed padded segments (width 0, weight 0) force `z=h_b`, producing a spurious sub-grid `s=`horizontal-radius that carries no weight and is never evaluated by the scalar path, so checking all samples would false-fire on that artifact. |
| **Note** — stale comments describing the rejected interpolation design                        | **Closed.** Reworded the `_ZONE_NAMES` module comment and the `_four_zone_familyA_eval` docstring to state exact in-belt vectorised evaluation (bit-for-bit as the trapezoid, chunked for memory), matching §1.                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Note** — stale docstrings citing the scalar breakpoint mechanism / dead code                | **Closed.** Updated the `four_zone_pkill_field` and `pkill_field_3d` docstrings to name `_pkill_columns_vec` / `_belt_breakpoints_vec` and to state that the scalar reference functions (`belt_column_breakpoints`, `integrate_column_density`, `lethal_density_*_point`) are **intentionally retained** as the equivalence baseline for `bench.py` and the new property tests.                                                                                                                                                                                                                                                                               |
| **Note** — duplicated `_FAMILY_A_CHUNK` constant                                              | **Closed.** `fragmentation.py` is now the canonical definition; `zones.py` imports it, so the single-zone and four-zone builders share one tuning knob.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **Limitation to log** — belt-breakpoint vectoriser does not deduplicate near-coincident roots | **Logged** (already documented in §3). The measured effect stays at 1e-16–1e-15 on $P_k$ — float-reassociation noise, not a real deviation; it is an accepted approximation, not a defect to fix. The new `test_pkill_columns_vec_matches_scalar` property test pins this to a 1e-10 tolerance against the scalar reference.                                                                                                                                                                                                                                                                                                                                  |
| **Limitation to log** — no runtime `s_grid` coverage check in the vectorised paths            | **Superseded by the Deferrable closure above** — the vectorised bounds guard is now present, so this limitation no longer applies.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

### Regression tests added

- `tests/test_field_builder_perf.py` — wall-clock budgets on the motivating
  cases (four-zone P(kill)/lethal-density volumes, single-zone volume, detailed
  n=300 four-zone ground field, n=150 density field). Marked `perf` and
  **deselected by default** (`addopts = -m 'not perf'` in pyproject.toml) so
  `uv run pytest` stays fast; run via `uv run pytest -m perf`. Budgets carry
  ≈5–50× headroom over the §6 refactored timings yet sit below the old
  order-of-magnitude cost, so a regression trips them without CI-variance flakes.
- `tests/test_vectorized_equivalence.py` — property tests pinning the
  vectorised paths to the retained scalar references (not stored snapshots):
  `build_mmin_table` vs elementwise `min_lethal_mass` (bit-identical),
  `_pkill_columns_vec` vs the scalar breakpoint+midpoint column integral
  (≤1e-10, incl. the A→0 spray-angle degeneracy), `_four_zone_density_layer_vec`
  vs per-cell `lethal_density_four_zone_point` (bit-identical), chunk/batch
  invariance, and the new bounds-guard firing on an undersized grid.
