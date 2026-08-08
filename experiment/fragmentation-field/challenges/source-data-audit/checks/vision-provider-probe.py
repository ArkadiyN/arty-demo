"""Probe which Google vision provider/resolution combination can actually read a
scanned numeric table, using the Tolch page for which we now have ground truth.

Consumer: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
section 7, and the Phase 7/8 workflow fixes in the review plan.

Two questions this settles empirically rather than by argument:

  1. Does `gemma-4-31b-it` (the configured GOOGLE_MODEL) accept image input at
     all? Observed symptom in the field is a 403, which would explain silent
     degradation to a path with no credentials behind it.
  2. Does raising the raster from the shipped dpi=60 to dpi=200 actually recover
     the digits, on a real call?

Ground truth is the base-spray Perf. row block on report p.19 (PDF page 41),
read off the page image and committed to
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/base-spray-density.csv`.

Requires GOOGLE_API_KEY. Reads .env from the primary checkout because worktrees
do not carry one (itself a finding -- see the ledger).

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-provider-probe.py
"""

import io
import os
from pathlib import Path

import fitz
from dotenv import load_dotenv
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
PDF = REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/source.pdf"
PAGE = 41

# .env lives in the primary checkout only; a worktree has none.
for env in (REPO / ".env", Path.home() / "arty_demo/.env"):
    if env.exists():
        load_dotenv(env, override=False)
        break

PROMPT = (
    "Transcribe the table 'Number of perforations, penetrations, and dents of "
    "the base spray per unit solid angle' from this page. Output only the "
    "Perf. block: one line per remaining-velocity row, as "
    "`velocity | PanelA | PanelB | PanelC` using the 'No. per u.s.a.' columns "
    "only (ignore the P.E. of Mean columns). Use a dash for blank cells. "
    "Do not guess a value you cannot read; write ? instead."
)

# From tables/base-spray-density.csv -- the Perf. rows, Panel A/B/C.
TRUTH = {
    "Static": ("1.82", "1.93", "1.48"),
    "700": ("1.51", ".75", ".77"),
    "1085": (".87", ".17", ".24"),
    "1450": (".24", ".24", "-"),
    "1685": (".34", ".18", ".12"),
    "2130": ("0", "0", ".04"),
}


def render(dpi, quality):
    doc = fitz.open(PDF)
    pm = doc[PAGE - 1].get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    doc.close()
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return buf.getvalue(), pm.width, pm.height


def score(text):
    """Count how many of the 18 ground-truth cells appear on their row line."""
    hits = total = 0
    for vel, cells in TRUTH.items():
        line = next((line for line in text.splitlines()
                     if line.strip().lower().startswith(vel.lower())), "")
        norm = line.replace("0.", ".")
        for c in cells:
            total += 1
            hits += c in norm
    return hits, total


def probe(model, dpi, quality):
    from google import genai
    from google.genai import types

    data, w, h = render(dpi, quality)
    label = f"{model} @ dpi={dpi} ({w}x{h}, {len(data) / 1024:.0f} KB)"
    try:
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        resp = client.models.generate_content(
            model=model,
            contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg"), PROMPT],
        )
        text = resp.text or ""
    except Exception as exc:  # noqa: BLE001
        kind = type(exc).__name__
        msg = str(exc).split("\n")[0][:140]
        print(f"  {label}\n      FAILED [{kind}] {msg}")
        return
    hits, total = score(text)
    print(f"  {label}\n      {hits}/{total} ground-truth cells correct")
    for line in text.strip().splitlines()[:8]:
        print(f"        {line.strip()[:76]}")


def render_stacked(dpi, quality, n_pages):
    """Reproduce _render_pages_combined: N pages stacked with separator bars."""
    from PIL import ImageDraw

    doc = fitz.open(PDF)
    start = PAGE - 1
    imgs = []
    for i in range(start, min(start + n_pages, len(doc))):
        pm = doc[i].get_pixmap(dpi=dpi)
        imgs.append(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))
    doc.close()

    SEP_H = 30
    width = max(i.width for i in imgs)
    total = sum(i.height for i in imgs) + SEP_H * len(imgs)
    combined = Image.new("RGB", (width, total), (255, 255, 255))
    draw = ImageDraw.Draw(combined)
    y = 0
    for n, img in enumerate(imgs):
        draw.rectangle([0, y, width - 1, y + SEP_H - 1], fill=(30, 80, 200))
        draw.text((10, y + 8), f"PAGE {n + 1}", fill=(255, 255, 255))
        y += SEP_H
        combined.paste(img, (0, y))
        y += img.height
    buf = io.BytesIO()
    combined.save(buf, "JPEG", quality=quality)
    return buf.getvalue(), combined.width, combined.height


def probe_stacked(model, dpi, quality, n_pages):
    from google import genai
    from google.genai import types

    data, w, h = render_stacked(dpi, quality, n_pages)
    label = f"{model} @ dpi={dpi}, {n_pages}-page stack ({w}x{h}, {len(data) / 1024:.0f} KB)"
    prompt = (
        "The image contains several scanned pages separated by blue 'PAGE N' bars. "
        "On PAGE 1 only, " + PROMPT[0].lower() + PROMPT[1:]
    )
    try:
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        resp = client.models.generate_content(
            model=model,
            contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg"), prompt],
        )
        text = resp.text or ""
    except Exception as exc:  # noqa: BLE001
        print(f"  {label}\n      FAILED [{type(exc).__name__}] {str(exc).split(chr(10))[0][:140]}")
        return
    hits, total = score(text)
    print(f"  {label}\n      {hits}/{total} ground-truth cells correct")
    for line in text.strip().splitlines()[:8]:
        print(f"        {line.strip()[:76]}")


def main():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY not set -- cannot probe.")
        return
    print(f"Tolch p.{PAGE} base-spray Perf. block, 18 cells of ground truth.\n")

    print("--- single page, configured model (the control) ---")
    for dpi, quality in ((60, 70), (200, 90)):
        probe("gemma-4-31b-it", dpi, quality)

    print("\n--- as shipped: pages stacked into one tall image ---")
    for n in (3, 8):
        probe_stacked("gemma-4-31b-it", 60, 70, n)

    print("\n--- a currently-live Gemini for comparison ---")
    probe("gemini-3.5-flash", 60, 70)


if __name__ == "__main__":
    main()
