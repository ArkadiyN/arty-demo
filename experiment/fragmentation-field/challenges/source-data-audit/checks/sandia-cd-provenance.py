"""Where SAND92-0243's drag coefficient actually comes from, printed off the page.

Consumer: doc-reference/ww2-shells/sandia-sand92-0243/card.md ("Findings on the
cited drag coefficient", and "Provenance of this card"), and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 21.

This document is cited across the drag-gap-1944 thread as the source of
"C_D = 1.2-1.7, velocity-dependent" -- in checks/drag-coefficient-calibration.py
as the tested low and high ends, and in b-vs-range.qmd and _limitations.qmd in
prose.  This script re-reads the page those numbers came from.

Unlike the other documents in this audit, SAND92-0243 has a clean text layer on
every page, so no closure invariant is needed to answer "was the right line
read?" -- the line itself can be printed.  That is what this does.  The three
arithmetic closures that ARE declared live in the document's tables/ directory
and are run by src/utils/check-table-invariants.py; they cover the density,
atmosphere and velocity rows, none of which is the drag coefficient.

Three things it establishes, each a direct quotation:

  1. Page 18 states TWO ranges for Cd.  The parameter-range list gives
     "Drag coefficient: 1.0 to 1.71" -- the span of this report's own computed
     data.  The prose three paragraphs down gives "can vary between 1.2 and
     1.7".  Every citation in this repo uses the prose sentence, so the cited
     floor is 0.2 above the report's own.
  2. The report supplies no Cd(V) function.  Appendices A-C take "Drag
     coefficient = variable (Ref. 1)", and Ref. 1 is SAND91-0277, which the
     repo does not hold.
  3. The asterisk in "a function of initial fragment velocity*" has no footnote
     text.  Checked against raw block order, not reading-order extraction --
     a footnote lost to reading order would still appear as a block.

It also prints the two source irregularities the card records: Appendix D
citing Equation 12 (the range parameter) for Cd where A-C cite Ref. 1, and the
symbol K carrying two different meanings.

Requires the retained scan, which is gitignored (.gitignore:58).  Absent it,
reports skipped rather than failing.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/sandia-cd-provenance.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]
PDF = ROOT / "doc-reference/ww2-shells/sandia-sand92-0243/source.pdf"

# The two Cd statements the card contrasts, as printed.  The number pattern
# stops before a trailing sentence period -- the prose one ends "1.7." and a
# greedy [\d.]+ swallows the full stop.
_NUM = r"(\d+(?:\.\d+)?)"
LIST_RANGE = re.compile(rf"Drag coefficient:\s*{_NUM}\s*to\s*{_NUM}")
PROSE_RANGE = re.compile(rf"can vary between\s*{_NUM}\s*and\s*{_NUM}")
CITED_BY_REPO = (1.2, 1.7)


def show(label, lines):
    print(f"\n{label}")
    for where, text in lines:
        print(f"    [{where}] {text}")
    if not lines:
        print("    (none found)")


def main():
    if not PDF.exists():
        print(f"skipped: {PDF.relative_to(ROOT)} absent (gitignored)")
        print("RESULT: skipped -- cannot read the page without the scan")
        return 0

    import fitz  # noqa: PLC0415 -- only needed when the scan is present

    list_hits, prose_hits, delegations, sym_k, eq9 = [], [], [], [], []
    with fitz.open(PDF) as doc:
        n = doc.page_count
        for i in range(n):
            text = doc[i].get_text()
            for line in text.splitlines():
                s = line.strip()
                if LIST_RANGE.search(s):
                    list_hits.append((f"p{i}", s))
                if PROSE_RANGE.search(s) or "function of initial fragment velocity" in s:
                    prose_hits.append((f"p{i}", s))
                if re.search(r"Drag coefficient\s*=\s*variable", s):
                    delegations.append((f"p{i}", s))
                if re.match(r"^K\s+Fluid flow parameter", s) or s.startswith("K = 0.262"):
                    sym_k.append((f"p{i}", s))
                if s.startswith("K = 0.262"):
                    eq9.append((f"p{i}", s))

        print(f"{PDF.name}: {n} pages, text layer present on "
              f"{sum(1 for i in range(n) if doc[i].get_text().strip())}/{n}")

        show("1a. Cd in the DISCUSSION parameter-range list (the report's own data span):",
             list_hits)
        show("1b. Cd in the DISCUSSION prose (what this repo cites):", prose_hits)

        def ranges(pattern, hits):
            """Every (lo, hi) `pattern` matches across `hits`, in page order."""
            found = []
            for _, s in hits:
                m = pattern.search(s)
                if m:
                    found.append(tuple(float(x) for x in m.groups()))
            return found

        listed = ranges(LIST_RANGE, list_hits)
        prose = ranges(PROSE_RANGE, prose_hits)
        print()
        if listed and prose and listed[0] != prose[0]:
            print(f"    -> the page gives TWO ranges: list {listed[0]}, prose {prose[0]}")
            print(f"    -> this repo cites {CITED_BY_REPO}, i.e. the prose sentence;")
            print(f"       the report's own data floor is {listed[0][0]}, "
                  f"{CITED_BY_REPO[0] - listed[0][0]:.1f} below the cited one")
        elif listed and prose:
            print("    -> both statements agree; the card's finding 1 no longer holds")
        else:
            print("    -> WARNING: could not locate both statements; re-check the anchors")

        show("2. What the report's own analyses use for Cd:", delegations)
        ref1 = [(f"p{i}", ln.strip())
                for i in range(n)
                for ln in doc[i].get_text().splitlines()
                if "SAND91-0277" in ln]
        show("   Ref. 1 resolves to:", ref1)
        print("    -> SAND91-0277 is not held in this repo, so the velocity "
              "dependence is cited but not sourced")

        # 3. Orphaned footnote marker -- raw block order, not reading order.
        print("\n3. The footnote marker after 'initial fragment velocity*':")
        pages = {int(w[1:]) for w, _ in prose_hits}
        for p in sorted(pages):
            blocks = [b for b in doc[p].get_text("blocks") if b[4].strip()]
            marker_y = next((b[1] for b in blocks if "initial fragment velocity*" in b[4]), None)
            if marker_y is None:
                continue
            below = [b for b in blocks if b[1] > marker_y]
            print(f"    p{p}: {len(below)} block(s) below the marker: "
                  + ", ".join(repr(b[4].strip().replace("\n", " ")[:40]) for b in below))
            print("    -> the only block below it is the page number; no footnote text exists")

        print("\n4. Source irregularities recorded on the card:")
        variants = {s for _, s in delegations}
        for v in sorted(variants):
            print(f"    Cd condition line variant: {v}")
        print("    -> Appendix D cites Equation 12 where A-C cite Ref. 1; "
              "Equation 12 as printed is the range parameter R, not a drag coefficient")
        show("    The symbol K, defined twice:", sym_k)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
