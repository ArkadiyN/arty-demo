"""Does AEP-55 Vol. 3 contain the personnel presented-area scalar the repo says it would?

Consumer: doc-reference/wound-ballistics/aep-55-vol3/card.md, and
          experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 24.

Two repo surfaces name AEP-55 Vol. 3 as a canonical reference for personnel
posture geometry:

  _limitations.qmd     -- "the canonical references ... Cunniff (2014) and
                          AEP-55 Vol. 3 ... are not present in doc-reference/.
                          Treat absolute posture-resolved hit counts as +-25%
                          engineering estimates until the references are
                          collected."
  pkill-poisson-field/scoping.md -- both ARE collected, and neither carries a
                          quotable nominal personnel presented-area scalar.

The two disagree, and neither had been checked against the document, because
no scan was retained.  The scan arrived 2026-08-03.  This script settles it.

An absence claim is the easiest kind of claim to assert and the easiest to get
wrong, so it is made here by search rather than by reading: the terms a
silhouette area would have to be written in are enumerated, and the hit count
is printed.  A future pass that doubts the verdict re-runs this rather than
re-reading 106 pages.

The scan is gitignored (`doc-reference/**/*.pdf`); absent, this reports
`skipped` rather than failing -- the `sandia-cd-provenance.py` pattern.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/aep-55-vol3-scope-check.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]
SCAN = ROOT / "doc-reference/wound-ballistics/aep-55-vol3/source.pdf"

# The vocabulary a man-silhouette presented area would have to be written in.
# Deliberately broad -- a false hit costs a human one lookup, a false miss
# would license the "not present" claim this script exists to test.
SILHOUETTE = re.compile(
    r"presented area|projected area|silhouette|man-target|standing man|"
    r"prone man|frontal area|exposed area|body area", re.I)

# Any square-metre figure at all, so the verdict is not "we found no phrase"
# but "here is every area in the document, and here is what each one is".
AREA = re.compile(r"\d[\d.,]*\s*m\s*[²2]\b")


def main():
    if not SCAN.exists():
        print(f"scan absent ({SCAN.relative_to(ROOT)}) — skipped.\n"
              "The scan is gitignored by convention; re-supply it to re-run.")
        return 0

    import fitz  # noqa: PLC0415 — only needed when the scan is present

    with fitz.open(SCAN) as doc:
        pages = [p.get_text() for p in doc]

    print("1. WHAT THIS DOCUMENT IS\n")
    title = [ln.strip() for ln in pages[0].splitlines() if ln.strip()]
    for ln in title:
        if "NATO UNCLASSIFIED" in ln or "Releasable" in ln:
            continue
        print(f"    {ln}")
    print(f"\n    {len(pages)} pages, text layer on every page "
          f"(min {min(len(p) for p in pages)} chars).")

    print("\n2. SEARCH FOR A PERSONNEL PRESENTED-AREA SCALAR\n")
    hits = [(i, ln.strip()) for i, p in enumerate(pages)
            for ln in p.splitlines() if SILHOUETTE.search(ln)]
    print(f"    terms: {SILHOUETTE.pattern}")
    print(f"    hits:  {len(hits)}")
    for i, ln in hits[:20]:
        print(f"      p{i}: {ln[:120]}")

    print("\n3. EVERY SQUARE-METRE FIGURE IN THE DOCUMENT\n")
    areas = [(i, ln.strip()) for i, p in enumerate(pages)
             for ln in p.splitlines() if AREA.search(ln)]
    print(f"    {len(areas)} line(s):")
    for i, ln in areas:
        print(f"      p{i}: {ln[:120]}")

    print("\n4. VERDICT\n")
    if hits:
        print("    Silhouette-vocabulary hits found — a human must read them "
              "before the\n    'no quotable scalar' claim can stand.")
        return 1
    print("    No personnel presented-area scalar. The document is an armoured-")
    print("    vehicle IED protection TEST STANDARD: occupant survivability is")
    print("    assessed with instrumented ATDs (anthropomorphic test devices),")
    print("    not with a vulnerable-area model, so a man-silhouette area is not")
    print("    a quantity it would ever state.")
    print("\n    -> pkill-poisson-field/scoping.md is CORRECT.")
    print("    -> _limitations.qmd is stale twice over: the document IS in")
    print("       doc-reference/, and collecting it can never supply the posture")
    print("       dimensions it is cited as the canonical source for.")
    print("\n    The one body-related area in the document (Annex E, Figure E7,")
    print("    'Thorax model') is the effective area of a lumped-parameter")
    print("    blast-lung chest-wall model, NOT a presented area. It must not be")
    print("    picked up as one.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
