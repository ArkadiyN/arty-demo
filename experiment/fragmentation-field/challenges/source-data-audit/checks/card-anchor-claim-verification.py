"""Do a card's bare line-number anchors point at the text the card claims?

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 25 (Phase 2.5d, narrative admissibility).

`.claude/rules/source-data-fidelity.md` forbids bare line numbers as the only
anchor, and gives one reason: they *rot* when a document is re-extracted, and
they rot silently -- landing the reader on a different table that looks like
the right one. This script tests that claim mechanically, and found the rule's
stated rationale to be incomplete.

The test needs no judgment. A card sentence that cites a line range almost
always also quotes something distinctive from it -- a table number, a value, a
velocity. So: pull the distinctive tokens out of the citing sentence, and ask
where in the source document they actually occur.

    HIT        the tokens are inside the cited range      -- anchor is good
    MISS       they occur, but somewhere else entirely    -- anchor is wrong
    UNRESOLVED they occur nowhere                         -- needs a human

MISS is the interesting verdict, and it is the one the rule warns about. What
it does NOT tell you on its own is *when* the anchor went bad, which is the
difference between a decay mode and an authoring defect. `--history` settles
that by re-running the same test against the revision that introduced the
document -- following renames, since both cards here were moved at least once
and a rename-blind check would silently test the wrong blob.

Neither document is rot. All 20 anchors across the two cards MISS at their
birth commit, against sources whose line count is unchanged from that commit to
today (ordnance 1466, Tolch 1715). They never pointed at their claimed content
-- Tolch's card cites "9.71 at lines 617-627" and 9.71 has always been at line
900. They were written, plausibly formatted, and never once checked.

That matters because it is not the failure the rule describes, and no amount of
re-extraction discipline would have caught it: there was nothing to decay from.
The two failures also have different fixes. Rot is fixed by preferring greppable
anchors; fabrication is fixed only by *verifying* an anchor at the moment it is
written, which is what this script does, in 0.3 s, cheaply enough to gate on.

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/card-anchor-claim-verification.py
    uv run python .../card-anchor-claim-verification.py --history
"""

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOCS = ROOT / "doc-reference"

# [text](file.md#L94-L106) or (file.md#L117) -- the two forms in use.
ANCHOR = re.compile(r"\[([^\]]*)\]\(([^)#]+)#L(\d+)(?:-L(\d+))?\)")

# What counts as "distinctive" in a citing sentence. Numbers with a decimal
# point or a thousands separator, degree/velocity figures, and TABLE <n>.
# Deliberately excludes bare small integers: "1" or "3" match everywhere and
# would turn every anchor into a false HIT.
TOKEN = re.compile(r"\bTABLE\s+\d+\b|\b\d{1,3},\d{3}\b|\b\d+\.\d+\b|\b\d{3,}\b",
                   re.I)

# Digit-group form, so "1,085" in the card matches "1,085" or "1085" on the
# page and vice versa -- OCR is inconsistent about separators.
def norm(tok):
    return re.sub(r"[,\s]", "", tok).upper()


def claim_tokens(block):
    """Distinctive tokens the card asserts are at this anchor.

    Every markdown link is deleted whole -- text *and* target -- before
    tokenizing. Nothing inside a link is evidence: the text is "lines 617-627"
    (the thing under test) and the target is "tolch-1938.md" (a filename whose
    year reads as a four-digit token and matches the report date on the title
    page). An earlier revision of this script tokenized the raw line and so
    scored every anchor against the digits in its own filename, which made all
    13 Tolch anchors resolve to the same spurious line.
    """
    block = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", block)
    block = re.sub(r"\blines?\s+\d+\s*[-–]\s*\d+", " ", block, flags=re.I)
    block = re.sub(r"\blines?\s+\d+", " ", block, flags=re.I)
    toks = {norm(t) for t in TOKEN.findall(block)}
    return {t for t in toks if len(t) >= 3}


def claim_block(card_lines, idx):
    """The card text whose truth this anchor is vouching for.

    Two card styles have to work. Tolch puts the claim and the citation in one
    sentence, so the line itself is the block. Ordnance puts a bare
    "**Anchor:** [Lines 340-369](...)" under a heading and lists the claimed
    values as bullets below it, so the block has to run from the heading to the
    next one.
    """
    start = idx
    while start > 0 and not card_lines[start].startswith("#"):
        start -= 1
    end = idx + 1
    while end < len(card_lines) and not card_lines[end].startswith("#"):
        end += 1
    return "\n".join(card_lines[start:end])


def heading_for(lines, idx):
    for j in range(idx, -1, -1):
        if lines[j].startswith("#"):
            return lines[j].lstrip("# ").strip()
    return "(no heading)"


def verify(card_path, source_text, card_text):
    """One verdict per anchor in this card."""
    src = source_text.splitlines()
    src_norm = [norm(line) for line in src]
    out = []
    card_lines = card_text.splitlines()

    for i, line in enumerate(card_lines):
        for m in ANCHOR.finditer(line):
            fname, a, b = m.group(2), int(m.group(3)), m.group(4)
            b = int(b) if b else a
            toks = claim_tokens(claim_block(card_lines, i))
            if not toks:
                out.append((i + 1, fname, a, b, "NO-TOKENS", heading_for(card_lines, i), "", ""))
                continue

            in_range, elsewhere = set(), {}
            for t in toks:
                where = [n + 1 for n, sl in enumerate(src_norm) if t in sl]
                if any(a <= w <= b for w in where):
                    in_range.add(t)
                elif where:
                    elsewhere[t] = where[:3]

            if in_range:
                v = "HIT" if not elsewhere else "PARTIAL"
            elif elsewhere:
                v = "MISS"
            else:
                v = "UNRESOLVED"
            near = ""
            if elsewhere:
                first = min(w for ws in elsewhere.values() for w in ws)
                near = f"actually near L{first}"
            out.append((i + 1, fname, a, b, v, heading_for(card_lines, i),
                        ",".join(sorted(toks))[:44], near))
    return out


# Ground truth, read off the retained scan (see `heading_association` below).
# Not a data series -- six table numbers and three titles, which is provenance
# and cannot come from the .md, since the .md is the artifact under test. The
# row values themselves are never typed here; they are loaded from the CSVs.
#   pdf p.84 = report p.70,  pdf p.89 = report p.75,  pdf p.93 = report p.79
PAGE_TRUTH = [
    # csv stem,            scan pdf p., title as printed,          casualties, perforation
    ("75mm-m48",           84, "75 mm HE SHELL, M48",   38, 39),
    ("105mm-m1",           89, "105 mm HE SHELL, M1",   48, 49),
    ("155mm-m107",         93, "155 mm HE SHELL, M107", 56, 57),
]


def heading_association(doc_dir, source_text):
    """Do `TABLE n` headings in the .md belong to the data printed beneath them?

    They do not, and this is the root cause of a defect the ledger already
    records as a symptom.

    The 1944 report prints two tables side by side -- casualties left,
    perforation right, under one shell title. Extraction flattens that page into
    a single column, and the flattening does not keep a heading with its own
    table: both page headings emit together, in scan order, above data belonging
    to only one of them. Whatever the .md's `TABLE n` lines mean, they do not
    mean "the rows below are from this table".

    The test needs no judgment and no eyeballing. Each shell's casualties series
    was transcribed from the scan and lives in `tables/*.csv`; find that series'
    first row in the .md, then ask which `TABLE n` heading most recently
    preceded it, and compare against the number actually printed on the page.

    What makes this worth a check rather than a note is the second column of the
    result: the heading the .md *implies* is, for all three shells, exactly the
    number the card asserts. The card was not guessing. It was reading the
    nearest preceding heading in the flattened file -- the same inference this
    script's own earlier revision made, and the reason the remedy for the
    bare-line-number findings cannot be "anchor on `TABLE n`" instead.
    """
    src = source_text.splitlines()
    heads = [(i + 1, int(m.group(1)))
             for i, line in enumerate(src)
             if (m := re.match(r"TABLE\s+(\d+)\s*$", line.strip()))]

    rows = []
    for stem, page, title, cas, _perf in PAGE_TRUTH:
        csv = doc_dir / "tables" / f"{stem}-casualties.csv"
        if not csv.exists():
            continue
        first = csv.read_text(encoding="utf-8").splitlines()[1].split(",")
        # r and N are enough to locate the row and are separator-insensitive.
        needle_r, needle_n = norm(first[0]), norm(first[1])
        at = next((i + 1 for i, line in enumerate(src)
                   if norm(line).startswith(needle_r + needle_n)), None)
        implied = None
        for ln, num in heads:
            if at and ln <= at:
                implied = num
        rows.append((title, page, at, implied, cas))
    return rows


def report_association(rows, doc_dir):
    if not rows:
        return 0
    print("\n--- do the .md's `TABLE n` headings match the printed page?")
    print(f"    {'shell (as printed on the scan)':<24} {'data at':>8}  "
          f"{'.md implies':>11}  {'page says':>9}   verdict")
    bad = 0
    for title, page, at, implied, truth in rows:
        ok = implied == truth
        bad += (not ok)
        print(f"    {title:<24} {'L' + str(at):>8}  {'TABLE ' + str(implied):>11}  "
              f"{'TABLE ' + str(truth):>9}   "
              f"{'ok' if ok else '** MISASSOCIATED ** (scan p.' + str(page) + ')'}")
    if bad:
        print("\n    The .md cannot support table-level citation at all: its `TABLE n`\n"
              "    lines are page furniture from a two-up scan, not headings over the\n"
              "    rows that follow. Anchor on the shell title instead -- and verify\n"
              "    it greps, because OCR damaged one of the three (`N.E.` for `H.E.`).")
    return bad


def report(rows, label):
    print(f"\n{'=' * 78}\n{label}\n{'=' * 78}")
    print(f"{'card':>5}  {'anchor':>11}  {'verdict':<11} {'section':<34} {'where it really is'}")
    print("-" * 108)
    for ln, _f, a, b, v, head, _toks, near in rows:
        rng = f"L{a}" if a == b else f"L{a}-{b}"
        print(f"{ln:>5}  {rng:>11}  {v:<11} {head[:34]:<34} {near}")
    bad = [r for r in rows if r[4] in ("MISS", "UNRESOLVED")]
    print(f"\n  {len(rows)} anchors, {len(bad)} not resolving to their claim.")
    return bad


def at_revision(rev, path):
    p = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT,
                       capture_output=True, text=True, check=False)
    return p.stdout if p.returncode == 0 else None


def birth(path):
    """Oldest (revision, path-at-that-revision) for a file, across renames.

    `git log -- <path>` stops at the rename, so on a moved file it returns the
    move commit and calls it the birth. Both cards here were moved
    (tolch-1944-… -> tolch-1938-…), and a rename-blind check reports "unchanged
    since birth" while actually comparing a file to itself one commit back --
    the check would look like it passed and would have tested nothing.
    """
    p = subprocess.run(
        ["git", "log", "--follow", "--name-only", "--format=%h", "--", path],
        cwd=ROOT, capture_output=True, text=True, check=False)
    rev, pairs = None, []
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"[0-9a-f]{7,40}", line):
            rev = line
        elif rev:
            pairs.append((rev, line))
            rev = None
    return pairs[-1] if pairs else (None, None)


CARDS = [
    ("wound-ballistics/ordnance-dept-1944-shell-fragment-damage", "ordnance-1944.md"),
    ("wound-ballistics/tolch-1938-m48-panel-pit-fragmentation", "tolch-1938.md"),
]


def main():
    history = "--history" in sys.argv
    failures = 0

    for slug, srcname in CARDS:
        card_p = DOCS / slug / "card.md"
        src_p = DOCS / slug / srcname
        if not card_p.exists() or not src_p.exists():
            print(f"skipped (missing): {slug}")
            continue

        card_t = card_p.read_text(encoding="utf-8", errors="replace")
        src_t = src_p.read_text(encoding="utf-8", errors="replace")
        rows = verify(card_p, src_t, card_t)
        bad = report(rows, f"{slug}  —  as committed today")
        failures += len(bad)
        failures += report_association(heading_association(DOCS / slug, src_t),
                                       DOCS / slug)

        if not history:
            continue

        rev, old_card_path = birth(str(card_p.relative_to(ROOT)))
        _, old_src_path = birth(str(src_p.relative_to(ROOT)))
        if not rev or not old_src_path:
            continue
        old_card, old_src = (at_revision(rev, old_card_path),
                             at_revision(rev, old_src_path))
        if not old_card or not old_src:
            continue
        old_rows = verify(card_p, old_src, old_card)
        moved = "" if old_card_path == str(card_p.relative_to(ROOT)) else \
            f"\n  (renamed since: {old_card_path})"
        old_bad = report(old_rows, f"{slug}  —  at its birth commit {rev}{moved}")

        now_len, then_len = len(src_t.splitlines()), len(old_src.splitlines())
        print(f"\n  source length: {then_len} lines at {rev}, {now_len} today")
        if len(old_bad) == len(bad) and then_len == now_len:
            print("  VERDICT: not rot. The anchors never resolved, against a\n"
                  "           source of unchanged length. Fabricated at authoring.")
        elif len(old_bad) < len(bad):
            print("  VERDICT: rot. The anchors resolved when written and stopped\n"
                  "           resolving when the source was re-extracted.")

    print(f"\n{'=' * 78}")
    print(f"RESULT: {failures} anchor(s) do not resolve to their claimed content.")
    print("Bare line numbers are non-conforming per "
          ".claude/rules/source-data-fidelity.md\nregardless of whether they "
          "currently resolve; this reports the ones already broken.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
