## Why

The `mott-fragment-shape-closure` model update (see
`experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`,
reviewed PASS) replaced the Mott fragment mass closure's implicit cube
assumption with an explicit prism shape factor built from two literature-derived
constants: fragment aspect ratio `A = 1.6` and mean-breadth factor `κ_x = 1.5`.
Both carry real literature spread (Wilson 1:1.65, Grady 1:1.5, Mott's own
1.5x₀ finding vs. Gold's implicit κ_x = 1) that the point estimates in
`src/arty/fragmentation.py` collapse to fixed module constants. Users of the
sensitivity app currently have no way to probe how much of the model's
fragment-count/mass output depends on these two point estimates — they can
already do this for the material-grade pair (`γ`, `σ_f`) but not for the shape
pair, even though the shape pair now has comparable leverage on `μ` (§ derivation.md
eq. 4c: `μ` is linear in the shape-derived `α^(-2/3)`).

## What Changes

- Promote the two shape constants from module-level constants in
    `fragmentation.py` into fields on `ShellParams` (defaults unchanged: `A =
    1.6`, `κ_x = 1.5`), following the same optional-override pattern already
    used for the Tier-1 ogive geometry fields on `ShellParams`.
- `mott_params(shell, V0)` reads the shape factor from `shell` instead of the
    fixed module constants — its signature and default numerical output are
    unchanged (backward-compatible within existing tolerance).
- Add two sliders to the sensitivity app's existing "Mott Fragmentation"
    group — fragment aspect ratio `A` and breadth factor `κ_x` — spanning the
    literature spread identified in the derivation, wired through to
    `ShellParams`.
- No new physics: the values and their literature support were already
    derived and reviewed in `mott-fragment-shape-closure`. This change only
    exposes existing, already-reviewed constants as user-adjustable inputs.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `fragmentation-physics`: `mott_params` reads the fragment shape factor from
    `ShellParams` fields rather than fixed module constants; the function's
    signature and default-input numerical output remain unchanged.
- `sensitivity-app`: the Mott Fragmentation slider group gains two sliders
    (aspect ratio `A`, breadth factor `κ_x`) driving the new `ShellParams`
    fields.

## Impact

- `src/arty/fragmentation.py`: `ShellParams` dataclass (two new fields),
    `mott_params()` internals (read from `shell` instead of module constants).
- `app/sensitivity.py`: Mott Fragmentation slider group, `ShellParams(...)`
    construction call sites.
- `tests/test_fragmentation.py`: add coverage that non-default `A`/`κ_x`
    values change `μ` in the expected direction, alongside existing
    default-preserving tests.
