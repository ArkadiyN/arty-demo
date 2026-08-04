"""Render MIL-S-10520D pages for direct visual reading of its tables.

Consumer: doc-reference/ww2-shells/mil-s-10520d-projectile-steel/card.md
("Provenance of this card", leg 1) and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 20.

This scan has NO text layer -- 14 pages carrying 588 characters between them,
all of it an everyspec watermark -- so the cell-for-cell text diff that settled
the sibling AMCP 706-249 table is unavailable here.  Leg 1 of this document's
admissibility is therefore a direct human read of the page, and this script is
what produces the pages to read.  It exists so that read is reproducible: the
numbers in tables/*.csv can be checked against the same rasters they came from,
rather than against a re-render at whatever settings the next reader picks.

Two modes:

    --nav   whole pages at 110 dpi.  Enough to read section headings and see
            which pages hold tables, so only those pages need the 300-dpi read.
    (none)  page halves at 300 dpi, which is what a typewritten specification
            needs before its decimal points are legible.

Halves with overlap, not hand-picked coordinate crops: a rectangle chosen by
eyeballing silently renders the WRONG PASSAGE when a page's layout differs from
the one it was tuned on, and the reader has no way to tell (see the 1943 render
script).  The overlap guarantees no line falls in a seam.

Requires the retained scan, which is gitignored (.gitignore:58); it was
supplied by the user and has no stable public URL.  Absent it, the script
reports skipped rather than failing.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mil-s-10520d-page-render.py <outdir> [--nav]
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
PDF = ROOT / "doc-reference/ww2-shells/mil-s-10520d-projectile-steel/source.pdf"

DPI = 300
NAV_DPI = 110


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(f"usage: {pathlib.Path(sys.argv[0]).name} <outdir> [--nav]")
        return 2
    if not PDF.exists():
        print(f"skipped: {PDF.relative_to(ROOT)} absent (gitignored)")
        print("RESULT: skipped -- cannot render without the scan")
        return 0

    import fitz  # noqa: PLC0415 -- only needed when the scan is present

    out = pathlib.Path(args[0])
    out.mkdir(parents=True, exist_ok=True)
    nav = "--nav" in sys.argv

    with fitz.open(PDF) as doc:
        for i in range(doc.page_count):
            page = doc[i]
            if nav:
                page.get_pixmap(dpi=NAV_DPI).save(out / f"nav-p{i:02d}.png")
                continue
            h = page.rect.height
            for tag, clip in (
                ("top", fitz.Rect(0, 0, page.rect.width, h * 0.55)),
                ("bot", fitz.Rect(0, h * 0.45, page.rect.width, h)),
            ):
                page.get_pixmap(dpi=DPI, clip=clip).save(out / f"p{i:02d}-{tag}.png")

    n = len(list(out.glob("*.png")))
    print(f"wrote {n} images to {out} at dpi={NAV_DPI if nav else DPI}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
