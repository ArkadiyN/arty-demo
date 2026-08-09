"""Trace DoD-1975 Figure 3 off the page and check the digitized curve against it.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 13, and
          doc-reference/fragmentation/dod-1975-fragment-debris-hazards/
          tables/figure-3-drag-coefficient.csv (this script produces it).

WHY THIS SCRIPT EXISTS
----------------------
`figure-3-digitized.md` in that document folder is an EYEBALLED reading of
Figure 3 ("curve traced by eye at grid intersections"). Its (Mach, C_D) table
was then hand-copied into
`updates/mach-dependent-fragment-drag/checks/required-retardation-vs-mach.py`,
which is the check that REJECTED a Mach-dependent drag law in favour of the
constant C_D = 1.28 now shipped in `src/arty/fragmentation.py`. So an eyeball
reading of a 1975 scan is load-bearing for a shipped modelling decision, and
nothing had ever compared it back to the page.

It also disagrees with `card.md` in the same folder: the card says the
transonic rise runs "from 1.08 to ~1.27" over Mach 0.7-1.0 and peaks near
Mach 1.5, while the table says C_D = 1.14 at Mach 1.0 and peaks at Mach 1.4.
Two artifacts derived from one figure, disagreeing by ~0.13 in C_D.

METHOD
------
The curve is a solid black stroke; the scan's grid is a grey dotted/hatched
texture. Per pixel column, take the longest run of near-black pixels
(grey < 40, >= 6 px), skip the columns occupied by the half-Mach vertical
gridlines, and reject any column whose reading departs from its neighbours by
more than a stroke width. Nothing about the published table is consulted while
tracing -- the trace is independent, then compared.

CALIBRATION, and how it is validated
------------------------------------
Axis pixel coordinates come from the six heavy horizontal rules (C_D = 1.0 ...
1.5) and eight heavy vertical rules (Mach = 0 ... 7) found by a dark-fraction
scan of the rendered page. Three features the source states independently
confirm it:
  * supersonic plateau   -> traced 1.280  (source: "constant at its
                            supersonic value of 1.28", p.8)
  * subsonic plateau     -> traced 1.079  (card.md: "flat at ~1.08")
  * transonic peak       -> traced 1.400  (card.md: "peak ~1.40")
A calibration that reproduces all three to 0.001 is not plausibly off in the
band between them.

Anchors are greppable strings, never line numbers:
  "Figure 3 Drag Coefficient of Fragments"   (the figure caption, pdf p.33)
  "supersonic value of 1.28"                  (the text, pdf p.18)

Source: doc-reference/fragmentation/dod-1975-fragment-debris-hazards/source.pdf
        -- gitignored per .gitignore `doc-reference/**/*.pdf`, retained on disk
        beside the extraction, not committed.
        sha256 9ff9e66f43b6ecf08598bfcc23ec3b729b0e3b5466d146a99b775df331393903
If the PDF is absent the script SKIPS with a clear message rather than failing.

Usage:  uv run python <this file>            # verify the committed CSV
        uv run python <this file> --write    # regenerate it from the page
Runtime: ~3 s.

MANUAL CORRECTION 2026-08-08, mach=1.00 and mach=2.60 rows. source.pdf was
not present in the checkout doing this fix (gitignored blob), so `at()`'s
interpolation fix above could not be re-verified against it end-to-end; the
two rows were instead hand-corrected to 1.257 and 1.294 using three
independent PNG re-traces that converge there (see the .invariant's new
pinning rows and OPEN-FINDINGS.md history). Re-running this script with
--write once source.pdf is available again should reproduce those two values
from the fixed `at()`; if it does not, the interpolation fix above needs a
second look, not the two rows.
"""

import csv
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/dod-1975-fragment-debris-hazards"
PDF = DOC / "source.pdf"
CSV_OUT = DOC / "tables/figure-3-drag-coefficient.csv"

PAGE = 33            # pdf page carrying "Figure 3  Drag Coefficient of Fragments"
DPI = 300
X0, X7 = 672.5, 2770.0     # pixel columns of the Mach 0 and Mach 7 rules
Y10, Y15 = 1878.0, 370.5   # pixel rows of the C_D 1.0 and 1.5 rules
TOP, BOT = 376, 1873       # plot interior, excluding the frame
INK = 40                   # the stroke is near-black; the grid texture is grey
MINRUN = 6                 # stroke is 6-12 px at 300 dpi off the horizontal

# What figure-3-digitized.md claims, and what required-retardation-vs-mach.py
# hand-copied from it. Quoted here to be REFUTED, not to be used as input.
DIGITIZED = [(0.0, 1.08), (0.5, 1.09), (0.8, 1.10), (1.0, 1.14), (1.2, 1.38),
             (1.4, 1.40), (1.6, 1.35), (1.8, 1.33), (2.2, 1.30), (2.6, 1.29),
             (3.0, 1.28), (4.0, 1.28), (5.0, 1.28), (7.0, 1.28)]

fails = 0


def report(label, ok, detail=""):
    global fails
    fails += not ok
    print(f"  {label:<52} {'PASS' if ok else 'FAIL'} {detail}")


def trace_curve():
    """{pixel column: (row_top, row_bottom)} of the curve stroke."""
    import numpy as np

    import fitz

    pix = fitz.open(PDF)[PAGE - 1].get_pixmap(dpi=DPI)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape(pix.height, pix.width, pix.n)
    grey = img[:, :, :3].mean(axis=2)
    grid = [round(X0 + 0.5 * k * (X7 - X0) / 7.0) for k in range(15)]

    raw = {}
    for c in range(int(X0) + 6, int(X7) - 5):
        if any(abs(c - g) <= 10 for g in grid):
            continue
        col = grey[TOP:BOT, c] < INK
        best, i = None, 0
        while i < len(col):
            if col[i]:
                j = i
                while j < len(col) and col[j]:
                    j += 1
                if j - i >= MINRUN and (best is None or j - i > best[1] - best[0]):
                    best = (i, j)
                i = j
            else:
                i += 1
        if best:
            raw[c] = (best[0] + TOP, best[1] - 1 + TOP)

    # Reject columns where the grid texture beat the stroke: a real curve moves
    # smoothly, so a reading far from its neighbours' median is contamination.
    cols = sorted(raw)
    mid = {c: 0.5 * (raw[c][0] + raw[c][1]) for c in cols}
    clean = {}
    for i, c in enumerate(cols):
        window = [mid[k] for k in cols[max(0, i - 12):i + 13]]
        if abs(mid[c] - statistics.median(window)) <= 40:
            clean[c] = raw[c]
    print(f"traced {len(clean)} columns ({len(raw) - len(clean)} rejected as "
          f"grid contamination)")
    return clean


def main():
    if not PDF.exists():
        print(f"SKIP: retained scan not found at {PDF}")
        print("      (gitignored blob; re-acquire to run this trace)")
        return 0

    write = "--write" in sys.argv
    clean = trace_curve()

    def mach(c):
        return 7.0 * (c - X0) / (X7 - X0)

    def cd(r):
        return 1.0 + 0.5 * (Y10 - r) / (Y10 - Y15)

    def at(m):
        """(cd_lo, cd_hi) of the stroke at Mach m, linearly interpolated
        between the nearest traced columns flanking c on either side.

        Fixed 2026-08-08 (was: single nearest column). On a steep segment,
        the +-10px half-Mach-gridline exclusion above can leave the nearest
        surviving column several px off-c on one side only; picking that
        single column reads the curve several hundredths of a Mach
        off-label. Interpolating between the flanking columns instead tracks
        a locally-linear steep segment correctly, and is a no-op (reduces to
        the same single-column read) on flat segments where the gridline gap
        does not matter -- see the C1 plateau/peak checks below, unaffected.
        """
        c = X0 + m * (X7 - X0) / 7.0
        left = max((k for k in clean if k <= c), default=None)
        right = min((k for k in clean if k >= c), default=None)
        if left is not None and abs(left - c) > 20:
            left = None
        if right is not None and abs(right - c) > 20:
            right = None
        if left is None and right is None:
            return None
        if left is None:
            left = right
        if right is None:
            right = left
        assert left is not None and right is not None
        if left == right:
            lo, hi = clean[left]
            return cd(hi), cd(lo)
        t = (c - left) / (right - left)
        lo = clean[left][0] + t * (clean[right][0] - clean[left][0])
        hi = clean[left][1] + t * (clean[right][1] - clean[left][1])
        return cd(hi), cd(lo)

    # --- C1. calibration validated against three source-stated features ------
    print("\n== C1. calibration, checked against features the source states ==")
    plateau = [0.5 * (cd(a) + cd(b)) for c, (a, b) in clean.items()
               if mach(c) >= 3.2]
    subsonic = [0.5 * (cd(a) + cd(b)) for c, (a, b) in clean.items()
                if mach(c) <= 0.45]
    peak_c = min((c for c in clean if 1.2 <= mach(c) <= 1.8),
                 key=lambda c: clean[c][0])
    p_med, s_med = statistics.median(plateau), statistics.median(subsonic)
    report("supersonic plateau (M>=3.2) == 1.28", abs(p_med - 1.28) <= 0.01,
           f"traced {p_med:.4f} over {len(plateau)} columns")
    report("subsonic plateau (M<=0.45) == 1.08", abs(s_med - 1.08) <= 0.01,
           f"traced {s_med:.4f} over {len(subsonic)} columns")
    report("transonic peak == 1.40", abs(cd(clean[peak_c][0]) - 1.40) <= 0.02,
           f"traced {cd(clean[peak_c][0]):.4f} at Mach {mach(peak_c):.2f}")
    report("peak sits near Mach 1.5, not 1.4",
           1.42 <= mach(peak_c) <= 1.58, f"Mach {mach(peak_c):.2f}")

    # --- C2. the published digitization, compared against the page -----------
    #
    # This does NOT assert the published table is right -- it is not, and the
    # defect is recorded as a blocking finding pending repair (ledger s13). It
    # pins the discrepancy instead, exactly as the 1944 page-geometry check
    # pins that source's own divergences: the recorded errors below are what
    # the page shows today, so a re-digitization that changes them -- in either
    # direction, including a partial "fix" -- fails here rather than passing
    # silently. Repairing figure-3-digitized.md means emptying this dict.
    RECORDED_DEFECT = {1.0: -0.082, 1.2: +0.025, 1.6: -0.038,
                       1.8: -0.034, 2.2: -0.020}
    print("\n== C2. figure-3-digitized.md vs the page ==")
    print(f"  {'Mach':>5} {'published':>10} {'traced stroke':>20} {'error':>8}")
    seen = {}
    for m, claimed in DIGITIZED:
        span = at(m)
        if span is None:
            print(f"  {m:5.2f} {claimed:10.2f}          (on a gridline)")
            continue
        lo, hi = span
        err = 0.0 if lo - 0.02 <= claimed <= hi + 0.02 else (
            claimed - hi if claimed > hi else claimed - lo)
        if err:
            seen[m] = err
        flag = "  <-- OUTSIDE the stroke" if err else ""
        print(f"  {m:5.2f} {claimed:10.2f}   {lo:8.3f}..{hi:<8.3f} "
              f"{err:+8.3f}{flag}")
    same = set(seen) == set(RECORDED_DEFECT) and all(
        abs(seen[m] - RECORDED_DEFECT[m]) <= 0.005 for m in seen)
    report("discrepancy is the one recorded in ledger s13", same,
           f"{len(seen)} of {len(DIGITIZED)} points outside the stroke, "
           f"worst {min(seen.values(), default=0.0):+.3f} at Mach "
           f"{min(seen, key=lambda k: seen[k]) if seen else '-'}"
           + ("" if same else f"; recorded {RECORDED_DEFECT}, got "
              + str({k: round(v, 3) for k, v in seen.items()})))

    # --- C3. emit / verify the transcribe-once CSV ---------------------------
    print("\n== C3. tables/figure-3-drag-coefficient.csv ==")
    rows = []
    m = 0.0
    while m <= 7.0001:
        span = at(m)
        if span is not None:
            lo, hi = span
            rows.append({"mach": f"{m:.2f}", "cd": f"{0.5 * (lo + hi):.3f}",
                         "cd_lo": f"{lo:.3f}", "cd_hi": f"{hi:.3f}"})
        m += 0.05
    if write:
        CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
        with CSV_OUT.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["mach", "cd", "cd_lo", "cd_hi"])
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {len(rows)} rows to {CSV_OUT.relative_to(ROOT)}")
    elif CSV_OUT.exists():
        with CSV_OUT.open(newline="") as fh:
            have = list(csv.DictReader(fh))
        same = len(have) == len(rows) and all(
            abs(float(a["mach"]) - float(b["mach"])) < 1e-9
            and abs(float(a["cd"]) - float(b["cd"])) <= 0.002
            for a, b in zip(have, rows, strict=False))
        report(f"committed CSV reproduces the trace ({len(rows)} rows)", same)
    else:
        report("committed CSV exists", False, "run with --write")

    print(f"\nRESULT: {fails} failure(s)")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
