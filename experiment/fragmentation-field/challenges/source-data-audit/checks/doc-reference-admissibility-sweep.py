"""Which doc-reference documents carry unchecked numbers, and who reads them.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 23 (Phase 2.5c, the eyeball/vision sweep).

Phase 2.5c asks a mechanical question: which documents hold numbers that were
read by eye or by the vision extractor and never checked against the page? The
triage in the plan is "an `images/` directory, or a markdown table of numbers,
with no `tables/*.csv` beside it".

That alone would flag a dozen documents nobody cites, so this also computes
**exposure** -- which committed artifacts name the document at all, split by
surface. An uncited document with unchecked numbers is a latent problem; a
document whose numbers reach `src/arty/` is a live one, and the two get
different outcomes.

Exposure is deliberately over-broad. It greps the directory slug, the leaf
slug, and the processed-source filename across `experiment/`, `src/` and
`app/`. Section 19 of the ledger recorded why: a source can be cited by
*title* rather than slug, and a slug-only grep silently under-tiers exactly
the citations that were written most carefully. Over-broad here means a human
reads a few extra rows; under-broad means a document is declared unexposed
when it is not.

What this script does NOT decide: whether a citing artifact reads *numbers*
out of the document or merely points at it. That needs a human to open the
hit, and the ledger records the judgment per document.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/doc-reference-admissibility-sweep.py
"""

import dataclasses
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOCS = ROOT / "doc-reference"
SEARCH_ROOTS = ("experiment", "src", "app")

# This audit's own bookkeeping names every document it sweeps, so counting it
# as exposure would mark all 25 "cited" and destroy the signal. A mention in
# the ledger is a record *about* a document, not a claim resting on one.
SELF = "experiment/fragmentation-field/challenges/source-data-audit/"

# A markdown line that is a table row carrying at least two numbers -- the
# shape a transcribed data table takes. Prose with a single figure in it does
# not match, which is intended: one number in a sentence is not a table.
NUMERIC_ROW = re.compile(r"^\|[^|]*\|.*?\d.*\|.*?\d")


# A report designator: letters then digits, optionally hyphenated, as it would
# be printed on a cover -- ES310, SAND92-0243, MIL-S-10520D, TP-7124, AD-A462991.
# This is the §19f lesson made mechanical: a source is often cited by its report
# number rather than its directory slug, and a slug-only grep silently reports
# such a document as unexposed. `fragmentation.py` names ES-310 exactly this way,
# and an earlier revision of this script therefore called it uncited while the
# file hardcoded three of its numbers.
DESIGNATOR = re.compile(r"\b([A-Z]{2,}(?:-[A-Z0-9]+)*-?\d{2,}[A-Z]?)\b")


def designators(doc_dir):
    """Report-number aliases for this document, with hyphenation variants.

    Drawn from the front-matter title and the directory name. Both spellings
    are searched because the two surfaces disagree in practice: the title says
    "ES310" and the code says "ES-310".
    """
    text = doc_dir.name.upper()
    for md in doc_dir.glob("*.md"):
        head = md.read_text(encoding="utf-8", errors="replace")[:600]
        text += "\n" + head.upper()
    found = set()
    for d in DESIGNATOR.findall(text):
        found.add(d)
        found.add(d.replace("-", ""))
        # Insert a hyphen at the letters/digits boundary: ES310 -> ES-310.
        m = re.fullmatch(r"([A-Z]+)(\d.*)", d)
        if m:
            found.add(f"{m.group(1)}-{m.group(2)}")
    return found


def citations(doc_dir):
    """Repo paths outside doc-reference/ that name this document, deduped.

    Searches the full slug pair (topic/docname), the leaf slug, each
    processed-source stem, and every report designator -- because none of them
    alone is reliable, and a false "uncited" is the expensive error here.
    """
    keys = {f"{doc_dir.parent.name}/{doc_dir.name}", doc_dir.name}
    keys |= {p.stem for p in doc_dir.glob("*.md") if p.name != "card.md"}
    keys |= designators(doc_dir)
    hits = set()
    for key in keys:
        if len(key) < 6:                     # too short to be a distinctive key
            continue
        proc = subprocess.run(
            ["grep", "-rl", "--binary-files=without-match", key, *SEARCH_ROOTS],
            cwd=ROOT, capture_output=True, text=True, check=False)
        hits |= {ln for ln in proc.stdout.splitlines() if ln and not ln.startswith(SELF)}
    return sorted(hits)


def numeric_rows(doc_dir):
    total = 0
    for md in doc_dir.glob("*.md"):
        if md.name == "card.md":
            continue
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            if NUMERIC_ROW.match(line):
                total += 1
    return total


@dataclasses.dataclass
class Doc:
    """One doc-reference document, as the sweep sees it."""

    slug: str
    csv: int
    inv: int
    images: int
    rows: int
    pdf: bool
    card: bool
    cites: list[str]
    shipped: list[str]

    @property
    def unchecked(self):
        """Carries numbers -- a numeric table, or figures whose values could
        only have been read off a curve -- with no CSV beside them."""
        return self.csv == 0 and (self.rows > 0 or self.images > 0)


def survey(doc_dir):
    cites = citations(doc_dir)
    return Doc(
        slug=f"{doc_dir.parent.name}/{doc_dir.name}",
        csv=len(list((doc_dir / "tables").glob("*.csv"))),
        inv=len(list((doc_dir / "tables").glob("*.invariant"))),
        images=len(list((doc_dir / "images").glob("*"))) if (doc_dir / "images").is_dir() else 0,
        rows=numeric_rows(doc_dir),
        pdf=bool(list(doc_dir.glob("*.pdf"))),
        card=(doc_dir / "card.md").exists(),
        cites=cites,
        shipped=[c for c in cites if c.startswith(("src/", "app/"))],
    )


def main():
    docs = [survey(p) for p in sorted(DOCS.glob("*/*")) if p.is_dir()]

    print(f"{'document':<56} {'csv':>3} {'inv':>3} {'img':>4} {'rows':>5} "
          f"{'pdf':>4} {'card':>5} {'cited':>6} {'shipped':>8}")
    print("-" * 104)
    for d in docs:
        flag = "  <-- unchecked" if d.unchecked else ""
        print(f"{d.slug:<56} {d.csv:>3} {d.inv:>3} {d.images:>4} "
              f"{d.rows:>5} {'Y' if d.pdf else '-':>4} "
              f"{'Y' if d.card else '-':>5} {len(d.cites):>6} "
              f"{len(d.shipped):>8}{flag}")

    unchecked = [d for d in docs if d.unchecked]
    exposed = [d for d in unchecked if d.cites]
    shipped = [d for d in unchecked if d.shipped]

    print(f"\n{len(docs)} documents; {len(unchecked)} carry unchecked numbers "
          f"({len(exposed)} cited by some artifact, {len(shipped)} reaching src/ or app/).")

    print("\nUnchecked AND cited — each needs re-baseline or an explicit "
          "non-citable mark:")
    for d in sorted(exposed, key=lambda d: -len(d.cites)):
        print(f"\n  {d.slug}  ({d.rows} numeric rows, {d.images} images, "
              f"card={'Y' if d.card else 'MISSING'}, "
              f"scan={'retained' if d.pdf else 'ABSENT'})")
        for c in d.cites:
            mark = " **SHIPPED**" if c.startswith(("src/", "app/")) else ""
            print(f"      {c}{mark}")

    print("\nUnchecked and uncited — latent, no artifact rests on them today:")
    for d in unchecked:
        if not d.cites:
            print(f"  {d.slug}  ({d.rows} numeric rows, {d.images} images)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
