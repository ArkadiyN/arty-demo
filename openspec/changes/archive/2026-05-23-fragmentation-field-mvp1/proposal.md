## Why

The fragmentation field physics model is fully derived and validated in the Quarto notebook (Stage 1), but it is embedded as inline notebook code — not importable, not testable, and not consumable by any application. MVP1 extracts it into a proper Python module and builds a Streamlit sensitivity app on top, making the model interactive and laying the architecture for the eventual Stage 3 webapp.

## What Changes

- New Python package `src/arty/` with a `fragmentation.py` module exposing the full physics model as typed, testable functions
- Shell registry with the 105mm M1 HE preset (structured for future shells)
- Streamlit sensitivity app at `app/sensitivity.py` — all model parameters as grouped sliders, Plotly figures updating live, R₅₀ as headline output
- Unit tests covering physics invariants already validated in the notebook
- `streamlit` and `plotly` added as project dependencies

## Capabilities

### New Capabilities

- `fragmentation-physics`: Pure-Python physics module — Gurney velocity, Mott distribution, drag decay, ES-310 Pk|hit, Poisson p_kill — accepting explicit parameter structs and returning structured results; no I/O, no plots
- `shell-registry`: Named shell presets (105mm M1 HE for MVP1) with all geometry, mass, and explosive parameters; expandable for future shells
- `sensitivity-app`: Streamlit frontend exposing all model parameters as grouped sliders; Plotly figures for Mott distribution, KE vs range, p_kill vs range, and 2D fragmentation field

### Modified Capabilities

## Impact

- New files: `src/arty/__init__.py`, `src/arty/fragmentation.py`, `src/arty/shells.py`, `app/sensitivity.py`, `tests/test_fragmentation.py`
- New dependencies: `streamlit`, `plotly`
- The Quarto notebook (`experiment/fragmentation-field/fragmentation-field.qmd`) is **not modified** — it remains the model derivation artifact; it does not import from `src/arty/`
- No breaking changes — additive only
