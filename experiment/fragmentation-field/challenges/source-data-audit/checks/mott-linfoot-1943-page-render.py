"""Re-render Mott & Linfoot (1943) report pp. 1-5 at the dpi the quotes were read at.

Consumer: doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/
quotes.md, and every digit on card.md and in tables/.

The scan's embedded OCR layer is unusable (see the companion script
mott-linfoot-1943-anchor-greppability.py, which measures how unusable), so this
document's whole fidelity chain rests on a controlled visual read of the page.
This script reproduces that read: it is how a future pass re-checks a quotation
or a table digit without re-deriving the setup.

Two choices here are the ones that made the page legible, and are worth keeping:

  - 300 dpi.  Enough to resolve the stacked-fraction bin boundaries in the p.3
    table and the handwritten exponents in eqs. (1)-(3); higher gained nothing.
  - Page HALVES with a 10% vertical overlap, not point-coordinate crops.  An
    earlier attempt clipped to hand-picked rectangles and silently rendered the
    wrong passages -- a crop that lands on the neighbouring paragraph looks
    perfectly fine, which is the same class of failure this whole audit exists
    to catch.  Halves cannot land on the wrong thing.

Writes to a temp directory (the PNGs are ~1 MB each and regenerable); pass a
different one as the sole argument.  The scan itself is gitignored
(.gitignore:58) -- re-acquire from DTIC accession ADB968781.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-page-render.py
"""

import pathlib
import sys
import tempfile

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[5]
PDF = ROOT / "doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/source.pdf"

DPI = 300
# Report page -> pdf page index.  Report pp. 1-5 are the text; pp. 6-8 are the
# figure plates (pdf pp. 10-12), which carry no text and are not transcribed.
PAGES = {"p1": 4, "p2": 5, "p3": 6, "p4": 7, "p5": 8}


def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(tempfile.gettempdir())
    out.mkdir(parents=True, exist_ok=True)

    if not PDF.exists():
        print(f"missing: {PDF}")
        print("The scan is gitignored; re-acquire from DTIC accession ADB968781.")
        return 1

    with fitz.open(PDF) as doc:
        for label, index in PAGES.items():
            page = doc[index]
            h = page.rect.height
            halves = (
                ("top", fitz.Rect(0, 0, page.rect.width, h * 0.55)),
                ("bot", fitz.Rect(0, h * 0.45, page.rect.width, h)),
            )
            for half, clip in halves:
                pixmap = page.get_pixmap(dpi=DPI, colorspace=fitz.csRGB, clip=clip)
                path = out / f"mott43-{label}-{half}.png"
                pixmap.save(path)
                print(f"{path}  {pixmap.width}x{pixmap.height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
