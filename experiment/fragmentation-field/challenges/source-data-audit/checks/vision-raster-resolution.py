"""Measure the glyph resolution the vision path actually sees, for the Tolch page
whose table came back with ~37% of its cells wrong.

*** SUPERSEDED AS A DIAGNOSIS -- retained as the measurement it is. ***
This script was written to test the hypothesis that dpi=60 was too low to read
the digits. `vision-provider-probe.py` then tested that hypothesis against the
live API and REFUTED it: a single page at dpi=60 transcribes 18/18 ground-truth
cells correctly, on the configured Gemma model. The numbers below are accurate;
the conclusion drawn from them was not. Raising dpi would not have fixed
anything -- and combined with page stacking would have made it worse, since a
taller image is downscaled harder. See the probe for the real cause.

Consumer: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
section 7, and the librarian/process-pdf workflow review.

`src/utils/pdf-processor.py:_render_pages_combined` rasterises at **dpi=60** and
JPEG-encodes at **quality=70**, then stacks N pages into one tall image. This
script reports, for the base-spray table page, how many pixels a single printed
digit ends up occupying under that setting versus the 150 dpi used for
single-page rendering -- and how tall the combined image gets, which matters
because vision APIs downscale images past a max dimension, costing resolution a
second time.

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-raster-resolution.py
"""

import io
from pathlib import Path

import fitz
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
PDF = REPO / "doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/source.pdf"
PAGE = 41  # 1-indexed; report page -19-, the base-spray component table

# Measured off the page image: the table's numeric block spans roughly this
# fraction of page width, carrying 6 numeric columns of 4 glyphs each.
TABLE_WIDTH_FRAC = 0.62
NUMERIC_COLUMNS = 6
GLYPHS_PER_CELL = 4


def report(dpi, quality, n_pages_combined):
    doc = fitz.open(PDF)
    page = doc[PAGE - 1]
    pm = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    kb = len(buf.getvalue()) / 1024

    table_px = pm.width * TABLE_WIDTH_FRAC
    glyph_px = table_px / (NUMERIC_COLUMNS * GLYPHS_PER_CELL)
    combined_h = (pm.height + 30) * n_pages_combined

    print(f"  dpi={dpi:<4} quality={quality:<4} page={pm.width}x{pm.height} px  ({kb:.0f} KB)")
    print(f"      numeric block ~{table_px:.0f} px wide / {NUMERIC_COLUMNS * GLYPHS_PER_CELL} glyphs"
          f"  ->  ~{glyph_px:.1f} px per digit")
    print(f"      combined image at {n_pages_combined} pages/chunk: {pm.width}x{combined_h} px")
    doc.close()
    return glyph_px


def main():
    print(f"Tolch 1938 (DTIC AD0702233), PDF page {PAGE} -- base-spray component table\n")

    print("AS SHIPPED -- _render_pages_combined(dpi=60), JPEG quality=70, chunk=8:")
    low = report(60, 70, 8)

    print("\nSingle-page path -- _render_page_jpeg(dpi=150):")
    mid = report(150, 90, 1)

    print("\nWhat a scanned table actually needs (300 dpi is the OCR convention):")
    high = report(300, 95, 1)

    print(f"\n  -> the shipped combined path gives ~{low:.1f} px per printed digit,")
    print(f"     against {mid:.1f} single-page at 150 dpi and {high:.1f} at 300 dpi.")
    print("\n  CAUTION -- this measurement does NOT explain the failure.")
    print("  vision-provider-probe.py shows a SINGLE page at dpi=60 transcribes")
    print("  18/18 cells correctly. ~13.7 px per digit is sufficient. The damage")
    print("  comes from what happens to a MULTI-PAGE stack, below.")
    # Second, compounding loss. Gemini/Gemma scale an input image to fit within
    # a max tile dimension (~3072 px) before the model sees it, so a very tall
    # combined image loses resolution a second time.
    MAX_DIM = 3072
    doc = fitz.open(PDF)
    pm = doc[PAGE - 1].get_pixmap(dpi=60)
    doc.close()
    combined_h = (pm.height + 30) * 8
    if combined_h > MAX_DIM:
        shrink = MAX_DIM / combined_h
        print(f"\n  COMPOUNDING LOSS: the 8-page combined image is {pm.width}x{combined_h} px.")
        print(f"  If the API caps the long side at ~{MAX_DIM} px (Gemini's documented")
        print(f"  behaviour), it is downscaled by {shrink:.2f}x server-side before the")
        print(f"  model sees it -> ~{low * shrink:.1f} px per digit, an effective")
        print(f"  {60 * shrink:.0f} dpi. That is decisively below any OCR threshold,")
        print("  and no prompt or model change can recover information already")
        print("  destroyed in rasterisation.")


if __name__ == "__main__":
    main()
