"""Why the vision pipeline extracted nothing from MIL-S-10520D, and what fixed it.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
sect. 20, and doc-reference/ww2-shells/mil-s-10520d-projectile-steel/card.md
("Provenance of this card").

pdf-processor.py routed a page to vision only when ONE embedded image rect
covered >50% of the page, and refused a document as scanned only when pages had
`bool(text.strip())` false.  Both gates fail on this document at once: its pages
are stored as 43-58 horizontal strips (largest 3.4% of the page), and an
everyspec watermark puts 41 characters on every one of them.  So 1 of 14 pages
reached vision, the other 13 fell through to their watermark, and the run
printed "Done." and exited 0.

The fix SUMS image coverage over all rects and counts characters instead of
testing truthiness.  This probe prints both criteria side by side so the
difference is visible per page rather than asserted.

Takes any PDF, so it doubles as the triage tool for the Phase 2.5c sweep: run
it on a document before trusting an extraction, and it says whether the
pipeline will actually route that document's pages to vision.  Defaults to
MIL-S-10520D, the document the bug was found on.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/vision-gating-probe.py [pdf]
"""

import pathlib
import sys

import fitz

# Must match pdf-processor.py.
IMAGE_PAGE_COVERAGE = 0.5
MIN_TEXT_CHARS_PER_PAGE = 100

ROOT = pathlib.Path(__file__).resolve().parents[5]
DEFAULT_PDF = ROOT / "doc-reference/ww2-shells/mil-s-10520d-projectile-steel/source.pdf"

PDF = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF


def rect_fracs(page):
    area = page.rect.width * page.rect.height
    return [
        (r.width * r.height) / area
        for info in page.get_images(full=True)
        for r in page.get_image_rects(info[0])
    ]


def main():
    if not PDF.exists():
        print(f"skipped: {PDF} absent (the scan is gitignored, .gitignore:58)")
        print("RESULT: skipped -- cannot probe routing without the PDF")
        return 0
    with fitz.open(PDF) as doc:
        print(f"{PDF.name}: {doc.page_count} pages\n")
        print(
            f"{'page':>4} {'chars':>6} {'imgs':>5} "
            f"{'largest rect':>13} {'summed':>8}   {'before':>9}  after"
        )
        before = after = 0
        for i in range(doc.page_count):
            page = doc[i]
            fracs = rect_fracs(page)
            largest = max(fracs, default=0.0)
            summed = min(sum(fracs), 1.0)
            b = largest > IMAGE_PAGE_COVERAGE
            a = summed > IMAGE_PAGE_COVERAGE
            before += b
            after += a
            chars = len(page.get_text().strip())
            print(
                f"{i:>4} {chars:>6} {len(fracs):>5} {largest:>13.3f} {summed:>8.3f}   "
                f"{'VISION' if b else 'text':>9}  {'VISION' if a else 'text'}"
            )

        n = doc.page_count
        print(f"\nrouted to vision:  before {before}/{n}   after {after}/{n}")

        thin = sum(
            1
            for i in range(n)
            if len(doc[i].get_text().strip()) < MIN_TEXT_CHARS_PER_PAGE
        )
        nonblank = sum(1 for i in range(n) if doc[i].get_text().strip())
        print(
            f"\n'appears scanned' guard:\n"
            f"  pages with ANY text (the old test):            {nonblank}/{n}\n"
            f"  pages under {MIN_TEXT_CHARS_PER_PAGE} chars (the new test):    {thin}/{n}\n"
            "  The old test saw a full text layer on a document that has none."
        )
        return 0 if after == n else 1


if __name__ == "__main__":
    raise SystemExit(main())
