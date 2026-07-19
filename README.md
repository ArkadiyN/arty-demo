# arty-demo

## Rendering the Quarto notebooks

Model notebooks live under `experiment/<model>/<model>.qmd` (e.g.
`experiment/fragmentation-field/fragmentation-field.qmd`). Rendered HTML
output is generated on demand and not committed automatically — render
locally, or check for it in version control if you need the last committed
copy.

1. Install dependencies with `uv`:

   ```bash
   uv sync
   ```

1. Copy `.env.example` to `.env` and set `QUARTO_PYTHON` to point at the
   project venv (already the default in `.env.example`):

   ```bash
   cp .env.example .env
   ```

1. Export the `.env` variables into your shell so Quarto's Python engine
   uses the project venv, then render:

   ```bash
   set -a; source .env; set +a
   quarto render experiment/<model>/<model>.qmd
   ```

   For example:

   ```bash
   set -a; source .env; set +a
   quarto render experiment/fragmentation-field/fragmentation-field.qmd
   ```

This produces `<model>.html` alongside the `.qmd` source, plus a
`<model>_files/` directory containing the figures and static assets the
HTML depends on to display correctly (both are required — the HTML alone
will render broken/unstyled if `_files/` is missing).

Requires the [Quarto CLI](https://quarto.org/docs/get-started/) to be
installed separately (not managed by `uv`).

## Running the sensitivity app

The interactive Streamlit explorer (`app/sensitivity.py`) lets you sweep shell,
Mott, drag, burst-geometry, and posture parameters live and see the
fragmentation-field, 3D kill-probability, and ground kill-probability views
update in real time.

1. Install dependencies with `uv` (if not already done above):

   ```bash
   uv sync
   ```

1. Start the app:

   ```bash
   uv run streamlit run app/sensitivity.py
   ```

   Streamlit prints a local URL (default `http://localhost:8501`) — open it
   in a browser. Stop the server with `Ctrl+C`.
