"""Locate and re-quote the cited passages of AMCP 706-249 in the retained scan.

Consumer: doc-reference/ww2-shells/ammunition-series-6-wdss-specs/card.md (the
document identity, the page indices, and every quoted passage in "What the
source contains" / "Internal inconsistencies") and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 19b
(the text-layer density figure, and the accession number).

It replaces three throwaway probes written during the Phase-2.5b re-baseline
(_scratch/wdss_{locate,dump,front}.py) and reproduces all of their cited output,
so the card's quotations can be re-verified without re-deriving where anything
sits.

Its companion checks the TABLE; this one checks the PROSE around it.  Table 6-1
itself is verified cell-for-cell by ammunition-series-6-table-6-1-fidelity.py --
run that too.  The split matters because the sect.-6-14 prose is where this
source's real defect lived: a card asserted the handbook states no yield
strength and no calibers for WDSS 3/5/6/7, and both are in one sentence here.

Prose has no closure invariant, so what this script offers is not a pass/fail on
meaning -- only that each anchor still resolves to a page and that the sentences
the card quotes are present verbatim.  That is exactly the greppability guard,
not a fidelity proof.

Requires the retained scan, which is gitignored (.gitignore:58); re-acquire as
DTIC AD830266.  Absent it, the script reports skipped rather than passing.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/ammunition-series-6-source-locator.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]
PDF = ROOT / "doc-reference/ww2-shells/ammunition-series-6-wdss-specs/source.pdf"

# Where the cited material sits, by 0-indexed pdf page.  Established by anchor
# search, not assumed -- the script re-checks each below.
PAGES = {
    "accession / distribution": 0,
    "title page (AMCP 706-249)": 1,
    "sect. 6-11 / 6-12 / 6-13 / 6-14": 10,
    "table 6-1 + footnote": 11,
}

# Anchors the card cites.  Each must resolve to exactly the page named.
ANCHORS = [
    ("AD830266", 0, "card.md: DTIC accession"),
    ("AMMUNITION SERIES", 1, "card.md: document identity"),
    ("Steel Used Early in World War", 10, "card.md: sect. 6-11, X-1340 lineage"),
    ("Steels Used After World War II", 10, "card.md: sect. 6-13, the replacement"),
    ("Prevailing Shell Steel Specifications", 10, "card.md + .invariant: sect. 6-14"),
    ("Table 6-1", 11, "card.md: the table itself"),
    ("incidental elements shall not exceed", 11, "card.md: the table footnote"),
]

# Sentences the card quotes.  Whitespace is normalised before comparison because
# the text layer breaks lines mid-sentence and pads around numerals; the words
# and digits must match exactly.
QUOTES = [
    (
        10,
        "The other grades cover all calibers from 37-mm to over 155-mm, in which "
        "the yield strengths vary from 60,000 psi to 80,000 psi.",
        "card.md: the sentence a prior card said was absent -- the sect. 19d finding",
    ),
    (
        10,
        "Grades WDSS 1 and 2 are used for the most part for 60-mm and 81-mm "
        "mortar shell forgings; also for the 57-mm recoilless gun shell.",
        "card.md: application by grade",
    ),
    (
        10,
        "All shell steel is made by the basic open-hearth process to fine grain "
        "practice, silicon 0.15 to 0.30 percent.",
        "card.md: melting practice; the WDSS-1 silicon contradiction (sect. 19e-1)",
    ),
    (
        10,
        "phosphorus, 0.45 percent maximum",
        "card.md: the X-1340 phosphorus defect (sect. 19e-2)",
    ),
    (
        11,
        "In the above steels, incidental elements shall not exceed the following: "
        "nickel, 0.25 percent; chromium, 0.20 percent; copper, 0.50 percent; "
        "molybdenum, 0.06 percent.",
        "card.md: incidental elements -- NOT sect. 6-13's residual list",
    ),
    (
        10,
        "nickel, 0.35 percent; chromium, 0.30 percent; copper, 0.25 percent",
        "card.md: sect. 6-13 residuals, the list the footnote is confused with",
    ),
]


def norm(text):
    """Delete all whitespace and hyphens, reducing both sides to one character run.

    Two properties of this text layer defeat a raw substring test on a correct
    quotation.  It wraps mid-sentence on every line, and it preserves the
    printed page's SOFT HYPHENS -- "mortar shell forg- ings", "nickel, 0.25 per-
    cent", "basic open- hearth process".  Nothing distinguishes those from the
    hard hyphen in "open-hearth" or "37-mm", so de-hyphenating only at line ends
    would fix the first case and break the second; and dropping the hyphen alone
    still leaves "per cent" where the quotation says "percent".

    So layout is discarded on both sides rather than reconciled.  The cost is
    real and worth naming: this cannot tell "open-hearth" from "openhearth", nor
    "per cent" from "percent".  It is a presence check on the character run --
    every letter, digit and mark of punctuation, in order.  The digits are
    untouched, and "60,000 psi to 80,000 psi" is what the card's quotations turn
    on.
    """
    return re.sub(r"[\s-]+", "", text)


def main():
    if not PDF.exists():
        print(f"skipped: {PDF.relative_to(ROOT)} absent (gitignored; DTIC AD830266)")
        print("RESULT: skipped -- cannot verify without the scan")
        return 0

    import fitz  # noqa: PLC0415 -- only needed when the scan is present

    failures = []
    with fitz.open(PDF) as doc:
        pages = [doc[i].get_text() for i in range(doc.page_count)]

    chars = sum(len(p) for p in pages)
    print(f"{len(pages)} pages, {chars} text-layer chars "
          f"({chars / len(pages):.0f}/page)")
    print("A dense, well-formed layer is why this source needed no closure "
          "invariant -- see ledger sect. 19b.\n")

    print("where the cited material sits (0-indexed pdf pages):")
    for what, page in PAGES.items():
        print(f"  p.{page:<3d} {what}")

    print("\nanchors:")
    for anchor, page, consumer in ANCHORS:
        found = [i for i, p in enumerate(pages) if anchor in p]
        ok = page in found
        print(f"  [{'ok' if ok else 'FAIL'}] p.{page:<3d} {anchor!r} -> {found}")
        print(f"          {consumer}")
        if not ok:
            failures.append(
                f"anchor {anchor!r} not on pdf page {page} (found on {found}) -- "
                f"the scan has been re-paginated, or the anchor is wrong"
            )

    print("\nquoted passages:")
    for page, quote, consumer in QUOTES:
        ok = norm(quote) in norm(pages[page])
        print(f"  [{'ok' if ok else 'FAIL'}] p.{page:<3d} {quote[:64]}...")
        print(f"          {consumer}")
        if not ok:
            failures.append(f"quotation not found verbatim on pdf page {page}: {quote!r}")

    print()
    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
