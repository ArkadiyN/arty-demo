"""Check that every Mott & Linfoot (1943) anchor this repo cites is greppable.

Consumer: doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation/
{card.md, quotes.md, tables/section2-fragment-weight-distribution.invariant} and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 18.

.claude/rules/source-data-fidelity.md requires every citation into a processed
source to name a stable string that `grep` will find.  For this document there
is no processed source: the scan's embedded OCR layer is unusable, so the card
records facts read visually off a 300 dpi render and `quotes.md` carries the
cited passages verbatim.  This script is what makes "greppable" true rather than
asserted, and it checks two things at once:

  A  EVERY ANCHOR IS FOUND IN quotes.md (fails the script if not).  This is a
     live regression guard, not a one-off: an anchor phrase that straddles a
     newline is not greppable, and re-flowing a quoted paragraph silently
     breaks it.  Two of these nine anchors failed exactly that way when
     quotes.md was first written.

  B  HOW MANY ARE FOUND IN THE EMBEDDED OCR LAYER (reported, never fails).
     This is the measurement behind the card's "there is no markdown extraction
     of this document, deliberately" -- the layer is not merely noisy, it does
     not contain the sentences the finding rests on.  Requires the retained
     scan; skipped with a note when source.pdf is absent, since it is
     gitignored (.gitignore:58) and re-acquired from DTIC ADB968781.

Render the pages the quotes were read from with the companion script,
mott-linfoot-1943-page-render.py, in this same directory.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/mott-linfoot-1943-anchor-greppability.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/mott-linfoot-1943-theory-of-fragmentation"
QUOTES = DOC / "quotes.md"
PDF = DOC / "source.pdf"

# Report pp. 1-5 are pdf pp. 5-9; the rest is cover, distribution matter and
# the figure plates, which carry no text layer at all.
TEXT_PAGES = range(4, 9)

# Every anchor string cited anywhere in the repo for this document, with where
# it is cited from.  Adding a citation means adding it here.
ANCHORS = [
    ("THE MEAN FRAGMENT SIZE", "card.md sect. 1"),
    ("For r we take 2.2 inches", "card.md worked example; the C3 closure"),
    ("DISTRIBUTION OF FRAGMENT WEIGHTS", "card.md sect. 2"),
    ("MATHEMATICAL DISCUSSION OF THE DISTRIBUTION LAW", "card.md sect. 3"),
    ("The agreement is shown below", "tables/*.invariant"),
    ("We have not been able to find a theory", "card.md finding, disclaimer 1"),
    ("we have no theory of what determines the lengths", "card.md finding, disclaimer 2"),
    ("our theory is incomplete", "card.md finding, disclaimer 3"),
    ("the lengths have an average value", "card.md finding, independence of x0 and y0"),
]


def main():
    failures = []

    quotes = QUOTES.read_text(encoding="utf-8")
    print(f"A  anchors vs {QUOTES.relative_to(ROOT)}")
    for anchor, cited_by in ANCHORS:
        hit = anchor in quotes
        print(f"    {'ok  ' if hit else 'MISS'}  {anchor!r}")
        if not hit:
            failures.append(
                f"A: {anchor!r} (cited by {cited_by}) is not greppable in quotes.md "
                f"-- most likely the phrase now straddles a line break"
            )

    print()
    if not PDF.exists():
        print(f"B  skipped: {PDF.relative_to(ROOT)} absent (gitignored; DTIC ADB968781)")
    else:
        import fitz  # noqa: PLC0415 -- only needed when the scan is present

        with fitz.open(PDF) as doc:
            ocr = "\n".join(doc[i].get_text() for i in TEXT_PAGES)
        found = sum(1 for anchor, _ in ANCHORS if anchor in ocr)
        print(f"B  anchors vs the scan's embedded OCR layer ({len(ocr)} chars, report pp.1-5)")
        for anchor, _ in ANCHORS:
            print(f"    {'found  ' if anchor in ocr else 'ABSENT '}  {anchor!r}")
        print(f"    {found}/{len(ANCHORS)} found -- this is why the card cites quotes.md,")
        print("    and why no markdown extraction of this document exists.")

    print()
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
