"""Column-identity regression: check the six ordnance-1944 CSVs against the
page geometry of the retained source scan.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 1 (the column-inversion finding) and section 12.

WHY THIS SCRIPT EXISTS
----------------------
The 1944 Ordnance tables are printed as TWO INTERLEAVED TABLES PER PAGE --
CASUALTIES on the left, PERFORATION OF 1/8 IN. MILD STEEL on the right, sharing
identical column headers. Three committed check scripts read the wrong one of
the pair. Every digit had been extracted correctly; only the column assignment
was wrong, so the glyph-level extraction-quality scan passed it.

`tables/*.csv` were re-baselined off the MERGED MARKDOWN (`../ordnance-1944.md`),
where the two tables have already been flattened into a linear reading order --
i.e. off an artifact that no longer carries the very geometry that distinguishes
them. The identity rested on a numeric closure (1/2 m v^2 == 58 ft-lb on the
casualties column) plus elimination for its partner.

This script closes that gap directly. It reads the retained scan, splits each
page by the x-coordinate of every word, and asserts that each CSV's values are
physically printed on the side of the page whose caption names its criterion.
Reading order is never consulted -- only position on the page -- so a flattening
error of the kind that caused the incident cannot pass.

Anchors are greppable strings in the page text layer, never line numbers:
  75 mm  : "TABLE 38" / "TABLE 39"  (report page 70, pdf p.84)
  105 mm : "TABLE 48" / "TABLE 49"  (report page 75, pdf p.89)
  155 mm : "TABLE 56" / "TABLE 57"  (report page 79, pdf p.93)
  captions: "CASUALTIES", "PERFORATION"

Source: doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/
        source.pdf -- gitignored per .gitignore `doc-reference/**/*.pdf`, so it
        is retained on disk beside the extraction, not committed.
        sha256 bd97d4ee9466f9e76817efaadf4225469f70757a5c0f35156cebc1cd278edb2a
If the PDF is absent the script SKIPS with a clear message rather than failing.

Runtime: ~1 s (three pages of text-layer extraction, no rasterising).
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage"
PDF = DOC / "source.pdf"
TABLES = DOC / "tables"

# shell -> (pdf page, casualties table no., perforation table no.)
PAGES = {
    "75mm-m48": (84, "TABLE 38", "TABLE 39"),
    "105mm-m1": (89, "TABLE 48", "TABLE 49"),
    "155mm-m107": (93, "TABLE 56", "TABLE 57"),
}

fails = 0


def report(label, ok, detail=""):
    global fails
    fails += not ok
    print(f"  {label:<58} {'PASS' if ok else 'FAIL'} {detail}")


def norm(tok):
    """Canonical form of a printed numeric token: digits and one decimal point.

    The scan prints thousands with commas ('1,070') and the OCR layer sprinkles
    stray leading dots and mid-number spaces ('. 0.0533', '.. 642'). Normalising
    to bare digits+point makes the comparison insensitive to all of that without
    making it insensitive to the digits themselves.
    """
    tok = tok.replace(",", "").replace(" ", "")
    tok = re.sub(r"^[.·]+(?=\d)", "", tok)  # stray leading dot(s)
    tok = re.sub(r"[^0-9.]", "", tok)
    tok = re.sub(r"\.$", "", tok)
    return tok


def cells(path):
    """Every numeric cell of a CSV, canonicalised, in row order."""
    out = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for v in row.values():
                out.append(norm(v))
    return out


def main():
    if not PDF.exists():
        print(f"SKIP: retained scan not found at {PDF}")
        print("      (gitignored blob; re-acquire to run this regression)")
        return 0
    import fitz

    doc = fitz.open(PDF)

    for shell, (pno, tbl_cas, tbl_perf) in PAGES.items():
        page = doc[pno - 1]
        mid = page.rect.width / 2
        words = page.get_text("words")
        left_raw = [w[4] for w in words if (w[0] + w[2]) / 2 < mid]
        right_raw = [w[4] for w in words if (w[0] + w[2]) / 2 >= mid]
        left = {norm(w) for w in left_raw if norm(w)}
        right = {norm(w) for w in right_raw if norm(w)}
        ltext, rtext = " ".join(left_raw), " ".join(right_raw)

        print(f"\n== {shell}  (pdf p.{pno}) ==")

        # --- G1. the captions sit on the halves this script assumes ----------
        report("caption CASUALTIES is on the LEFT half", "CASUALTIES" in ltext)
        report("caption PERFORATION is on the RIGHT half", "PERFORATION" in rtext)
        report(f"{tbl_cas} (casualties) is on the LEFT half",
               tbl_cas.split()[-1] in ltext.split())
        report(f"{tbl_perf} (perforation) is on the RIGHT half",
               tbl_perf.split()[-1] in rtext.split())

        # --- G2. each CSV's cells are printed on its own half ----------------
        cas = cells(TABLES / f"{shell}-casualties.csv")
        perf = cells(TABLES / f"{shell}-perforation-1-8in.csv")

        for name, series, own, other in (
            ("casualties", cas, left, right),
            ("perforation", perf, right, left),
        ):
            # A value shared by both tables (the 20/30/40 ft rungs, 0.0001 in
            # both B columns) cannot discriminate; only unique values can.
            uniq = [c for c in series if c not in (perf if name == "casualties" else cas)]
            in_own = sum(c in own for c in uniq)
            inverted = [c for c in uniq if c not in own and c in other]
            missing = [c for c in uniq if c not in own and c not in other]
            pct = 100.0 * in_own / len(uniq) if uniq else 0.0
            print(f"  -- {name}: {len(series)} cells, {len(uniq)} discriminating")
            report("     no cell printed on the OPPOSITE half",
                   not inverted,
                   f"inverted={inverted[:6]}" if inverted else "")
            report("     >=90% of discriminating cells found on own half",
                   pct >= 90.0,
                   f"({in_own}/{len(uniq)} = {pct:.0f}%"
                   + (f", OCR-damaged: {missing[:6]}" if missing else "")
                   + ")")

    # --- G3. cross-shell closure the page images make available -------------
    # 105 mm and 155 mm share INITIAL FRAGMENT VELOCITY 3,500 F/S. The (m, v)
    # pair is the lightest fragment still meeting the criterion at range r --
    # a pure single-fragment ballistics result that depends on V0 and the drag
    # law, NOT on shell size. So the two shells should print identical m and v
    # wherever their range ladders coincide, across INDEPENDENTLY TYPESET tables
    # four pages apart. 75 mm (V0 = 3,120 f/s) must NOT match them.
    #
    # OBSERVED, and verified against the page images at 500 dpi: the identity
    # holds exactly on all 11 shared perforation ranges and on 8 of 10 shared
    # casualties ranges. It breaks in the LAST SIGNIFICANT DIGIT at r = 300 and
    # 400 ft of the casualties pair -- the source prints 0.166/598 and 0.232/507
    # for 105 mm against 0.161/598 and 0.233/505 for 155 mm. Both readings are
    # faithful; the divergence is the SOURCE's, not the transcription's, and it
    # is confined to the two longest casualty ranges. It is pinned here rather
    # than smoothed over, so a future re-extraction that "fixes" one of these
    # to match the other fails this check instead of passing silently.
    print("\n== G3. (m, v) identity between the two 3,500 f/s shells ==")

    def mv(path):
        with path.open(encoding="utf-8") as f:
            return {r["r_ft"]: (r["m_oz"], r["v_fps"]) for r in csv.DictReader(f)}

    KNOWN_SOURCE_DIVERGENCE = {"casualties": ["300", "400"], "perforation-1-8in": []}
    for kind in ("casualties", "perforation-1-8in"):
        a = mv(TABLES / f"105mm-m1-{kind}.csv")
        b = mv(TABLES / f"155mm-m107-{kind}.csv")
        shared = sorted(set(a) & set(b), key=int)
        diff = [r for r in shared if a[r] != b[r]]
        expect = KNOWN_SOURCE_DIVERGENCE[kind]
        report(f"  {kind}: 105 vs 155 agree on {len(shared) - len(expect)}"
               f"/{len(shared)} shared ranges",
               diff == expect,
               f"expected divergence at r={expect}, got r={diff}"
               if diff != expect else f"(known source divergence r={expect})"
               if expect else "")

    # The divergent rows still have to satisfy the table's own 58 ft-lb closure,
    # which is what bounds how much the disagreement can matter.
    print("  energy closure on the four divergent-row readings:")
    for shell, r_ft in (("105mm-m1", "300"), ("155mm-m107", "300"),
                        ("105mm-m1", "400"), ("155mm-m107", "400")):
        m_oz, v_fps = mv(TABLES / f"{shell}-casualties.csv")[r_ft]
        e = 0.5 * (float(m_oz) / 16 / 32.174) * float(v_fps) ** 2
        report(f"    {shell} r={r_ft} ft: {m_oz} oz @ {v_fps} f/s -> "
               f"{e:.1f} ft-lb", abs(e - 58) / 58 <= 0.05,
               f"({100 * (e - 58) / 58:+.1f}% vs stated 58)")

    c75 = mv(TABLES / "75mm-m48-casualties.csv")
    c105 = mv(TABLES / "105mm-m1-casualties.csv")
    shared = sorted(set(c75) & set(c105), key=int)
    same = [r for r in shared if c75[r] == c105[r]]
    report("  casualties: 75 mm (3,120 f/s) DIFFERS from 105 mm", not same,
           f"unexpectedly equal at r={same}" if same else "")

    print(f"\nRESULT: {fails} failure(s)")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
