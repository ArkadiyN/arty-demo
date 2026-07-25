---
name: process-pdf
description: Extract images from a PDF and optionally generate a markdown file with LaTeX formulas and inline image references. Use when the user wants to process a PDF document in this project.
allowed-tools: Bash
---

Extract images and/or generate markdown from a PDF file in this project.

## Usage

```
uv run src/utils/pdf-processor.py <pdf_path> [--output-dir <dir>] [--markdown] [--analyze-formulas]
```

**Flags**

- `--output-dir` / `-o` — output root (default: same directory as the PDF)
- `--markdown` / `-m` — generate a `.md` file with image references
- `--analyze-formulas` / `-f` — use Claude vision for clean LaTeX and real figures only (recommended for scanned/OCR PDFs; requires auth)

**Outputs** land next to the PDF by default:

- Images: `<pdf-dir>/images/fig1.jpeg`, `fig2.jpeg`, … (only real illustrations, not page-background scans)
- Markdown (with `--markdown`): `<pdf-dir>/<pdf-stem>.md`
    - Without `-f`: heuristic font/Unicode formula detection; no images for scanned docs
    - With `-f`: Claude vision extracts clean LaTeX; figures identified per-page

## Steps

1. If the user didn't specify a PDF path, ask which PDF to process.
1. Ask if they want markdown output and/or `--analyze-formulas` (if not stated).
1. Run the command with the Bash tool.
1. If markdown was generated, run the extraction-quality check:
    `uv run src/utils/scan-extraction-quality.py <generated .md path>`
1. Report how many figures were extracted and where the markdown landed. If the
    quality check flagged the file, report the flags too (PUA glyphs, suspect
    symbol-run lines, abnormal short-token ratio) — these usually mean a broken
    font cmap or OCR garbling. Fixing them is out of scope for this skill; a
    PUA/symbol flag is often fixable by re-running with `--analyze-formulas`
    (vision extraction bypasses the broken cmap); a high short-token ratio on a
    scanned doc usually needs the same. Otherwise, note the flag for manual repair.
