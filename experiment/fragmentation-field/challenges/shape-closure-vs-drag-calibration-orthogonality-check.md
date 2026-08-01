# Does the Mott shape-closure fix feed the drag-coefficient calibration check?

**No.** The `m` values `ordnance-1944-drag-coefficient-calibration-check.md`
feeds into `retardation_coeff` are the source's own tabulated per-range
"lightest effective fragment" masses (Table 43/51/59 `m(r)` columns,
transcribed as literal `oz` arrays), never the model's own Mott
mass-distribution output. The shape-closure fix (commit `b12f553`,
`feat(fragmentation-field): expose Mott fragment-shape closure factors (A, kappa_x) ...`) is structurally orthogonal to this specific check's outcome.

## Trace

**What the shape-closure fix touches.** `mott_params(shell, V0)` in
`src/arty/fragmentation.py:244-269` computes the Mott half-mass `mu` and
fragment count `N0`. The fix added the shape-closure factor `alpha = aspect_ratio * breadth_factor**2 * t_bu/x0` (line 261) and folded it into
`gamma = alpha**(-2/3) * shell.steel.gamma` (line 262), which feeds `mu` (line
263-267) and hence `N0 = mass_shell/(2*mu)` (line 268). This is the "mean
fragment mass / fragment count" closure named in the task. It is consumed
downstream by `mott_N(m, N0, mu)` (line 299-306) and by any
`expected_kills`/field code that needs a fragment-count or mean-mass
distribution.

**What the drag-calibration check calls.** Per its own header,
`ordnance-1944-drag-coefficient-calibration-check.md` calls
`arty.fragmentation.retardation_coeff` "against the three calibers'
already-tabulated `(m(r), v(r), V0)` triples, reused verbatim from the three
check files." Its script,
`experiment/_scratch/ordnance-1944-drag-calibration-check.py`, confirms this:
`m_oz` arrays (e.g. `[0.014, 0.063, 0.244]` for 75mm) are hardcoded literals
copied from the source's Table 43/51/59, converted to kg with a fixed
`OZ_TO_KG` constant — no call to `mott_params`, `mu`, `N0`, or any shape
factor anywhere in the script. The only `arty` calls in the script are
`SHELLS[shell_name]` (for `shell.steel.rho`, a pre-existing material
constant unaffected by the fix) and `retardation_coeff(m_kg, drag, rho_steel)`.

**Why `retardation_coeff` itself cannot see the fix.** Its signature is
`retardation_coeff(m: np.ndarray, drag: DragParams, rho_steel: float)`
(`fragmentation.py:272-279`) — a pure function of an externally-supplied
fragment mass `m`, drag parameters, and a steel density. It contains no
reference to `mu`, `N0`, `alpha`, `aspect_ratio`, or `breadth_factor`; those
symbols do not appear in its body. Whatever mass value is passed in — a
source-tabulated mass or a model-predicted Mott mass — `retardation_coeff`
treats identically. In this check the mass passed in is the former.

**Confirmation from the upstream check files.** The three
`ordnance-1944-initial-conditions-check-{75,105,155}mm.md` files (which this
check follows up on) explicitly document that `m(r)` is "Table 43
(CASUALTIES) ... a *per-range* 'lightest effective fragment' weight `m(r)`
[oz]," verified against the source's own 58 ft-lb casualty-energy threshold
— i.e. a source-table quantity, not a `mott_params` output. The drag check
reuses these same literal numbers "verbatim."

## Verdict

**Unaffected.** The drag-coefficient calibration challenge's inputs, method,
and conclusions (that no single constant `C_D·C_shape` in the 0.585-1.7
range closes the velocity-decay gap uniformly, and that the residual is
range/caliber-dependent) do not depend in any way on the Mott shape-closure
fix — the check never calls `mott_params` or consumes `mu`/`N0`, and
`retardation_coeff` has no code path back to the shape-closure factors. The
fix's correctness (or any future revision to it) has zero bearing on this
check's results, and vice versa; they are independently verifiable aspects.
