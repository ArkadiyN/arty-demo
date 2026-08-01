## Context

`mott_params(shell, V0)` in `src/arty/fragmentation.py` currently reads two
fragment-shape constants — `_MOTT_ASPECT_RATIO` (`A = 1.6`) and
`_MOTT_BREADTH_FACTOR` (`κ_x = 1.5`) — as fixed module-level constants inside
the function body. Both were derived and reviewed (PASS) in
`experiment/fragmentation-field/updates/mott-fragment-shape-closure/derivation.md`
as literature point estimates with a documented spread (§ "Sourcing of A and
κ_x" in `_governing-equations.qmd`: Wilson 1:1.65, Grady 1:1.5, Mott's own
1.5x₀ finding). `fragmentation-physics`'s existing spec requirement locks
`mott_params(shell, V0)`'s signature and default-input numerical output —
this design must not touch either.

`ShellParams` already carries several optional fields with backward-compatible
defaults (the Tier-1 ogive geometry block) that functions read conditionally —
this is the established pattern for adding tunable inputs without changing a
function's positional signature.

## Goals / Non-Goals

**Goals:**
- Make `A` and `κ_x` overridable per-call, defaulting to the current reviewed
    values, with zero change to `mott_params`'s signature or default output.
- Expose both as sliders in the sensitivity app's existing "Mott Fragmentation"
    group, spanning the literature spread found in the derivation.

**Non-Goals:**
- No new physics or re-derivation — the values and their literature support
    already exist and were reviewed.
- No change to the wall-thickness/break-up (`t_bu`) treatment — `wall_t` is
    already an app slider and `t_bu` is derived from it via the existing
    incompressible-wall identity; this change does not touch that path.
- No change to `DragParams`/`C_shape` — the drag-parameter interaction was
    already logged as a documentation-only note in `_limitations.qmd` by the
    prior model update and is explicitly out of scope here.

## Decisions

**Where the two constants live: new `ShellParams` fields, not `SteelParams`
fields, not a `mott_params` keyword argument.**

- Not `SteelParams`: `A` and `κ_x` are fragment-geometry constants from a
    cross-dataset (Mott/Grady/Wilson) fracture-mechanics finding, not a
    per-steel-grade material property the way `γ`/`σ_f` are. Attaching them to
    `SteelParams` would imply a grade-dependence the derivation doesn't
    support.
- Not a `mott_params` keyword argument: would change the function's call
    signature, conflicting with the existing `fragmentation-physics` spec
    requirement that pins `mott_params(shell, V0)`.
- `ShellParams` fields (mirroring the existing optional Tier-1 ogive fields):
    `aspect_ratio: float = 1.6` and `breadth_factor: float = 1.5`. `mott_params`
    reads `shell.aspect_ratio` / `shell.breadth_factor` instead of the module
    constants; the module constants become the dataclass field defaults (single
    source of truth), keeping every existing call site byte-identical unless it
    explicitly overrides the new fields.

**Slider ranges.** Span the literature spread identified in
`_governing-equations.qmd`'s "Sourcing of A and κ_x" note rather than an
arbitrary symmetric band around the point estimate — this matches how the
existing `γ`/`σ_f` sliders are scoped (their range is the Mott Table 1 span,
not a synthetic ±X%).

**Implementation ownership.** The `ShellParams`/`mott_params` edit is a
`src/arty/` change to a function that computes a derived physical quantity, so
it is implemented by @modeler per `agents-routing.md` Gate 2, even though no
new math is introduced — only the app slider wiring (`app/sensitivity.py`) is
main-agent work.

## Risks / Trade-offs

- [Risk] A `ShellParams` field named generically (`aspect_ratio`) could later
    be misread as shell-geometry aspect ratio rather than fragment-shape
    aspect ratio. → Mitigation: field docstring/comment explicitly ties it to
    the Mott fragment-shape closure, mirroring how `wall_t`'s comment already
    disambiguates it from ogive geometry fields.
- [Risk] Widening the slider range beyond the literature spread could let
    users read the app as endorsing values outside the reviewed derivation.
    → Mitigation: slider bounds are exactly the cited literature spread
    (1.5–1.71 aspect ratio range across sources, 1.0–2.0 for κ_x per Mott's
    "mostly x₀..2x₀" finding), not an arbitrary widening.

## Migration Plan

Single-commit change on this worktree's branch, following the project's
squash-to-one-logical-commit convention. No data migration; `ShellParams` is a
frozen dataclass constructed fresh per call, so no existing persisted state to
migrate. Rollback is a plain revert — the new fields are additive and
default-preserving.

## Open Questions

None — both constants and their literature spread are already resolved in the
reviewed `mott-fragment-shape-closure` derivation; this change only re-exposes
them.
