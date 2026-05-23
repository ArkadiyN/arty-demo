## Context

The fragmentation field physics — Gurney, Mott, drag decay, ES-310 Pk|hit — lives entirely inside the Quarto notebook as inline cell code. It cannot be imported, tested independently, or consumed by an application. Stage 2 extracts it into a proper Python package and builds a Streamlit sensitivity app on top. The design must preserve the backend/frontend split so Stage 3 (FastAPI + HTMX) can wrap the same module over HTTP without touching physics code.

## Goals / Non-Goals

**Goals:**

- Extract all physics into `src/arty/fragmentation.py` with explicit, typed parameter structs
- Expose a shell registry (`src/arty/shells.py`) with the 105mm M1 HE preset
- Build a Streamlit sensitivity app that imports directly from `src/arty/`
- Use Plotly for all charts so the chart spec is JSON-backed and reusable in Stage 3
- Cover physics invariants with unit tests

**Non-Goals:**

- HTTP API layer (Stage 3)
- Any model feature not currently in the notebook (angle of fall, cover, airburst, ricochet)
- Modifying the Quarto notebook — it remains an independent derivation artifact
- Production deployment, auth, multi-user support

## Decisions

### 1 · Parameter structs as dataclasses, not keyword arguments

**Decision**: Physics functions accept typed dataclass instances (`ShellParams`, `MottParams`, `DragParams`, `TargetParams`), not long flat argument lists.

**Why**: The Stage 3 FastAPI endpoint will deserialize JSON into these same structs — the data contract is defined once. Streamlit reads slider values and constructs the structs; FastAPI deserializes request body into them. No glue code changes between stages.

**Alternative considered**: One big flat function with 12 keyword arguments. Rejected — hard to serialize to JSON, no grouping for the sensitivity app UI.

### 2 · Single `compute_frag_field()` entry point returning a result struct

**Decision**: One top-level function takes all parameter structs and returns `FragFieldResult` — a dataclass holding all output arrays (`r`, `p_kill`, `ke_by_mass`, `field_x`, `field_y`, `field_pk`, `r50`, `N0`, `mu`).

**Why**: Streamlit calls it once per slider change and destructures the result. Stage 3 FastAPI serializes the result to JSON in one `model_dump()` call. The Quarto notebook's individual functions (`gurney_velocity`, `mott_half_mass`, etc.) are preserved as internal helpers.

**Alternative considered**: Keeping individual functions public, letting the caller compose. Rejected — requires the caller to know the composition order; the notebook already shows this is error-prone (bisection bug came from wrong composition).

### 3 · Plotly for all charts

**Decision**: All figures in the Streamlit app use Plotly (`plotly.graph_objects`), not matplotlib.

**Why**: Plotly figures are JSON (`fig.to_json()`). Stage 3 FastAPI can return the same JSON; the browser renders it with `plotly.js` — no re-implementation of chart logic. Matplotlib produces images; switching to Plotly in Stage 3 would require rewriting every chart.

**Alternative considered**: Matplotlib for Stage 2 (simpler), convert later. Rejected — conversion cost is exactly what this decision avoids.

### 4 · Streamlit imports `src/arty/` directly — no HTTP in Stage 2

**Decision**: The Streamlit app is a direct Python consumer of the physics module. No FastAPI, no network calls.

**Why**: Stage 2 is a sensitivity tool for analysts, not a deployed product. Adding an HTTP layer adds latency, complexity, and a server process for no benefit at this stage. The module's API (function signatures, dataclasses) IS the contract; HTTP is just transport added in Stage 3.

### 5 · Shell registry as a dict of presets, not a database

**Decision**: `src/arty/shells.py` exports `SHELLS: dict[str, ShellParams]` with string keys (e.g., `"105mm M1 HE"`).

**Why**: MVP1 has one shell. The dict is trivially expandable by adding entries. No database, no config files, no external dependencies. Stage 3 can expose `GET /shells` returning `list(SHELLS.keys())`.

## Risks / Trade-offs

[Plotly learning curve] → Both `graph_objects` and `express` APIs exist; use `graph_objects` throughout for consistency and fine-grained control. Document the pattern in the first figure.

[Streamlit re-runs entire script on every slider change] → Acceptable for a sensitivity tool. For the 2D field figure (most expensive), use `@st.cache_data` keyed on params to avoid redundant recomputation.

[Dataclasses not directly JSON-serializable] → Use `dataclasses.asdict()` in Stage 3. `numpy` arrays in `FragFieldResult` need `.tolist()` — document this at the Stage 3 boundary, not now.

[Physics parity with notebook] → Unit tests lock in the notebook's validated outputs (V₀, μ, R₅₀ for default params) so any drift between notebook and module is caught immediately.
