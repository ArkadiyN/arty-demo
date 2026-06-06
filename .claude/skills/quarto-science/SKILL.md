---
name: quarto-science
description: Conventions for writing Quarto experiment notebooks in this project. Covers document structure, LaTeX math notation, scientific Python standards, and validation plot style. Use when producing or reviewing experiment/<modelname>/<modelname>.qmd files.
allowed-tools: Bash, Read, Write, Edit
---

Standards for experiment notebooks in this project.

## Document structure

Each `.qmd` file must have this YAML frontmatter:

```yaml
---
title: "<Model Name>"
format:
  html:
    code-fold: true
    toc: true
jupyter: python3
---
```

Section order:

1. **Background** — one paragraph, purpose of the model and scope
1. **Governing equations** — LaTeX derivation, symbols table, assumptions
1. **Parameters** — table of inputs with symbol, description, unit, and typical value
1. **Implementation** — Python code with inline prose explaining each step
1. **Validation** — sanity checks and spot-checks against published values
1. **Key findings** — what the model tells us; parameter sensitivity notes

## LaTeX math

- Inline math: `$...$`
- Display equations: `$$...$$` on their own line
- Number important equations with `\quad (N)` inline label
- Define every symbol in a Markdown table immediately after it first appears

## No physics in the notebook

The project's physics is **common** — it lives in `src/arty/`, not in any
`.qmd`. The notebook is a **thin presentation layer**: it imports from `arty`,
calls functions, and renders results and prose. It must **not** contain:

- physics or geometry functions (put them in `src/arty/`),
- parameter values or material constants (define them in `src/arty/`, e.g. the
  shell/explosive registries, and import them),
- computation or plotting helpers reused across figures (factor them into
  `src/arty/`, e.g. an `arty.plots` module).

A `.qmd` code cell should read like: `from arty.fragmentation import ...`, then
call + display. If you find yourself writing a derivation, a loop over physics,
or a constant in the notebook, it belongs in `src/arty/`.

## Modular notebook structure

The model notebook is a **thin parent** that pulls in per-section partials:

```markdown
{{< include _background.qmd >}}
{{< include _governing-equations.qmd >}}
{{< include _zone-geometry.qmd >}}
```

- One section / model aspect per `_<section>.qmd` partial.
- A new aspect adds one partial + one include line — it does not touch the rest.
- Keeps every edit local to one small file.

## Editing notebooks and modules — edit, never rewrite

Make **targeted edits** to the one partial or `src/arty/` module that changes.
Never `Write` (rewrite) a whole notebook, partial, or module to change part of
it — emit the diff, not the file. Rewriting a large file wastes tokens and
risks clobbering unrelated content.

## Scientific Python

- All function arguments and return values must carry units in the one-line docstring: `"""Return fragment velocity [m/s] given C/M ratio [-] and Gurney energy [J/kg]."""`
- Use SI units internally; convert to display units (mm, g, kJ) only in plots and tables

## Rendering

`QUARTO_PYTHON` must point at the project venv so Quarto uses installed packages:

```bash
set -a; source .env; set +a
quarto render experiment/<modelname>/<modelname>.qmd
```

Run this before reporting the task complete. Fix any errors before finishing.
