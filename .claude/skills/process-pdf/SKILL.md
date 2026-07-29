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
- `--vision-chunk-size N` — pages per vision API request when `-f` is set (default 8). Lower it (e.g. 3–4) for dense/scanned documents, where a large combined image makes the model burn its output budget on internal reasoning instead of transcribing — this is a real, observed failure mode, not a hypothetical.
- `--screenshot-pages` — save every image-based page as a full-page screenshot with **no vision AI call and no network dependency**. Pure local rasterization; cannot fail on API/quota/output-budget grounds. Ignores `--analyze-formulas`.

**Outputs** land next to the PDF by default:

- Images: `<pdf-dir>/images/fig1.jpeg`, `fig2.jpeg`, … (only real illustrations, not page-background scans)
- Markdown (with `--markdown`): `<pdf-dir>/<pdf-stem>.md`
    - Without `-f`: heuristic font/Unicode formula detection; no images for scanned docs
    - With `-f`: Claude vision extracts clean LaTeX; figures identified per-page

## Large or dense scanned documents (30+ pages, tables/formulas throughout)

`--analyze-formulas` chunks internally (`--vision-chunk-size` pages per request, one API
call per chunk) and writes the `.md` file only once, after every chunk in the
whole document has been attempted — a single unrecoverable chunk failure no
longer aborts the run (failed pages fall back per-page to Anthropic, then to
the heuristic path if that also fails), but the run itself is still one long
blocking call that can take several minutes on a large document, and a
heuristic-fallback page on a scanned doc is known to be low quality.

If only specific data (a table, a figure, a stated conclusion) is needed from
a large document rather than a full transcription:

1. Run `--screenshot-pages` first — it's fast, has no failure mode, and gets
    every page onto disk as an image immediately.
1. Identify which page(s) hold the needed content (scan filenames/order, or a
    quick heuristic-mode `--markdown` pass without `-f` for rough OCR text to
    grep against — heuristic quality is fine for locating a page, not for
    transcribing it).
1. `Read` those specific page images directly (multimodal) and transcribe the
    needed content by hand instead of waiting on a whole-document vision run.

Treat a full `--analyze-formulas` transcription of the remaining pages as a
lower-priority, optional follow-up once the needed content is already safely
captured — not a prerequisite for it.

## Steps

1. If the user didn't specify a PDF path, ask which PDF to process.
1. Ask if they want markdown output and/or `--analyze-formulas` (if not stated).
1. Check page count (`pdfinfo <pdf_path> | grep Pages`) and whether it's scanned
    (`pdfinfo`'s producer/creator often says "Paper Capture" or similar for OCR'd
    scans). If it's a large scanned document and only specific content is
    needed rather than a full transcription, follow "Large or dense scanned
    documents" above instead of a single whole-document `-f` run.
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
