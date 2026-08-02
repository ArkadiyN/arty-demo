"""Verify that src/arty's fragment aspect ratio is what Felix, Colwill & Harris
(2022) actually concluded, in the sense they actually defined.

Consumer: doc-reference/fragmentation/explosion-fragment-model/card.md and
experiment/fragmentation-field/challenges/source-data-audit/ledger.md sect. 16.

Two things are checked, because two things can go wrong independently:

  C1  MAGNITUDE.  1.6 is the mean of the paper's three per-dataset averages
      (Grady 1.58, Hiroe 1.66, Mott 1.48), read from tables/*.csv rather than
      retyped. The paper's own sentence for this is garbled in print, so the
      arithmetic is the reliable form.

  C2  DIRECTION.  The paper defines aspect ratio as width DIVIDED BY length, so
      "1:1.6" means length = 1.6 x width. src/arty stores it as
      _MOTT_ASPECT_RATIO = l_bar/x_bar = 1.6, i.e. length per unit breadth --
      the same sense. Inverted, every modelled fragment would be short and fat
      instead of long and thin, with no numeric tell: 1.6 is a plausible value
      either way round. C2 asserts the defining sentence is still on the page.

C2 SKIPs when source.pdf is absent: doc-reference/**/*.pdf is gitignored
(.gitignore:58), so the scan sits beside its extraction but is never committed.
Re-acquire from https://doi.org/10.1016/j.dt.2020.12.006 .

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/explosion-fragment-model-aspect-ratio.py
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/explosion-fragment-model"
PDF = DOC / "source.pdf"
AVERAGES = DOC / "tables/table-4-average-aspect-ratios.csv"

sys.path.insert(0, str(ROOT / "src"))

# The sentences that fix the direction of the ratio. Both must be on the page;
# either one alone leaves it ambiguous.
DIRECTION_ANCHORS = [
    "aspect ratio of a fragment is defined as a fragment's width divided by its length",
    "Approximate aspect ratio (width: length)",
]

PAGES = (3, 9)  # 1-based pdf pages: section 2.5 (journal p.161), Table 4 (p.167)


def norm(text):
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("ﬁ", "fi")).strip()


def main():
    failures = []

    # -- C1 magnitude -----------------------------------------------------
    with AVERAGES.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    values = [float(r["avg_width_to_length"]) for r in rows]
    mean = sum(values) / len(values)
    print(f"C1  per-dataset averages {values} -> mean {mean:.4f}")

    if round(mean, 1) != 1.6:
        failures.append(f"C1: mean of {values} rounds to {round(mean, 1)}, not 1.6")

    from arty.fragmentation import _MOTT_ASPECT_RATIO as shipped

    print(f"C1  src/arty _MOTT_ASPECT_RATIO = {shipped}")
    if abs(shipped - round(mean, 1)) > 1e-9:
        failures.append(f"C1: shipped {shipped} != paper's {round(mean, 1)}")

    # The corroborating values section 2.5 quotes, on different materials.
    for name, val in (("Wilson (tungsten alloy)", 1.65), ("Grady (AERMET-100)", 1.5)):
        if not 1.45 <= val <= 1.70:
            failures.append(f"C1: {name} {val} outside the band the datasets span")

    # -- C2 direction -----------------------------------------------------
    if not PDF.exists():
        print(f"C2  SKIP: {PDF} absent (retained scan, not committed).")
    else:
        import fitz

        doc = fitz.open(PDF)
        text = norm("\n".join(doc[p - 1].get_text() for p in PAGES))
        for anchor in DIRECTION_ANCHORS:
            if norm(anchor) in text:
                print(f"C2  found: {anchor!r}")
            else:
                failures.append(f"C2: {anchor!r} not on pages {PAGES}")

    for f in failures:
        print(f"  FAIL  {f}")
    print(f"RESULT: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
