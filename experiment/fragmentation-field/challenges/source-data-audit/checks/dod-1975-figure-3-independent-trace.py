"""Independent re-trace of DoD-1975 Figure 3, off the extracted PNG not the PDF.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          review-provenance.md, item 1 (provenance gate).

WHY. tables/figure-3-drag-coefficient.csv is produced by
checks/dod-1975-figure-3-trace.py, which renders source.pdf p.33 at 300 dpi with
hard-coded axis pixel coordinates (X0, X7, Y10, Y15). Those four constants are
the whole calibration and they are asserted, not derived, in that script. This
script re-derives the calibration from scratch on a DIFFERENT file -- the
extraction pipeline's own images/figure-3-drag-coefficient-vs-mach.png -- by
locating the heavy axis rules from their dark-pixel fraction, then re-traces the
stroke. If the two agree, the CSV is what the page shows and not an artifact of
one script's assumed axis box.

Nothing from the CSV or from figure-3-digitized.md is read as input.

Usage:  uv run python experiment/_scratch/dod-1975-figure-3-independent-trace.py
Runtime: ~2 s.
"""

import csv
import pathlib

import numpy as np
from PIL import Image

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
DOC = ROOT / "doc-reference/fragmentation/dod-1975-fragment-debris-hazards"
PNG = DOC / "images/figure-3-drag-coefficient-vs-mach.png"
CSV_IN = DOC / "tables/figure-3-drag-coefficient.csv"

img = np.asarray(Image.open(PNG).convert("L"), dtype=float)
H, W = img.shape
print(f"PNG {W}x{H}")
dark = img < 128

# --- locate the heavy axis rules ------------------------------------------
# A heavy rule spans most of the plot; the grid texture does not.
rowfrac = dark.mean(axis=1)
# Vertical rules: measure only over the plot's own row band, and only over the
# columns the frame spans, so page margins do not dilute the fraction.
colfrac = None  # set after the horizontal rules fix the row band


def peaks(frac, thresh):
    """Centres of contiguous runs above thresh."""
    out, i = [], 0
    while i < len(frac):
        if frac[i] >= thresh:
            j = i
            while j < len(frac) and frac[j] >= thresh:
                j += 1
            out.append(0.5 * (i + j - 1))
            i = j
        else:
            i += 1
    return out


hrules = peaks(rowfrac, 0.55)
print(f"horizontal rules at rows {[round(r, 1) for r in hrules]}")
assert len(hrules) == 6, f"expected 6 C_D rules (1.0..1.5), got {len(hrules)}"

r0, r1 = int(hrules[0]) + 4, int(hrules[-1]) - 3
colfrac = dark[r0:r1, :].mean(axis=0)
vrules = peaks(colfrac, 0.45)
print(f"vertical   rules at cols {[round(c, 1) for c in vrules]}")
assert len(vrules) == 8, f"expected 8 Mach rules (0..7), got {len(vrules)}"

# hrules top->bottom = C_D 1.5 .. 1.0 ; vrules left->right = Mach 0 .. 7
Y15, Y10 = hrules[0], hrules[-1]
X0, X7 = vrules[0], vrules[-1]
# linearity check: rules must be evenly spaced
hs = np.diff(hrules)
vs = np.diff(vrules)
print(f"row spacing  {np.round(hs, 1)}  (spread {hs.max() - hs.min():.1f} px)")
print(f"col spacing  {np.round(vs, 1)}  (spread {vs.max() - vs.min():.1f} px)")

TOP, BOT = int(Y15) + 3, int(Y10) - 2


def mach(c):
    return 7.0 * (c - X0) / (X7 - X0)


def cd(r):
    return 1.0 + 0.5 * (Y10 - r) / (Y10 - Y15)


# --- trace the stroke ------------------------------------------------------
INK = 100          # PNG is cleaner than the 300-dpi PDF render
gridcols = [X0 + k * (X7 - X0) / 14.0 for k in range(15)]
stroke = {}
for c in range(int(X0) + 3, int(X7) - 2):
    if any(abs(c - g) <= 3 for g in gridcols):
        continue
    col = img[TOP:BOT, c] < INK
    best, i = None, 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]:
                j += 1
            if j - i >= 2 and (best is None or j - i > best[1] - best[0]):
                best = (i, j)
            i = j
        else:
            i += 1
    if best:
        stroke[c] = 0.5 * (best[0] + best[1] - 1) + TOP

cols = sorted(stroke)
med = {}
for i, c in enumerate(cols):
    win = [stroke[k] for k in cols[max(0, i - 8):i + 9]]
    if abs(stroke[c] - float(np.median(win))) <= 8:
        med[c] = stroke[c]
print(f"traced {len(med)} columns ({len(stroke) - len(med)} rejected)")


def at(m):
    c = X0 + m * (X7 - X0) / 7.0
    near = [k for k in med if abs(k - c) <= 5]
    return cd(med[min(near, key=lambda k: abs(k - c))]) if near else None


# --- compare against the committed CSV ------------------------------------
with CSV_IN.open(newline="") as fh:
    ref = {float(r["mach"]): float(r["cd"]) for r in csv.DictReader(fh)}

print("\n  Mach   CSV(from PDF)   PNG re-trace     diff")
worst = 0.0
for m in [0.0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.45, 1.5,
          1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 4.0, 5.0, 6.0, 7.0]:
    a = ref.get(round(m, 2))
    b = at(m)
    if a is None or b is None:
        print(f"  {m:4.2f}   {'-' if a is None else f'{a:.3f}':>10}"
              f"   {'-' if b is None else f'{b:.3f}':>12}")
        continue
    d = b - a
    worst = max(worst, abs(d))
    print(f"  {m:4.2f}   {a:10.3f}   {b:12.3f}   {d:+7.3f}")

# peak from the PNG trace, independent of the PDF script's answer
pk = min((c for c in med if 1.1 <= mach(c) <= 1.9), key=lambda c: med[c])
print(f"\nPNG peak: C_D = {cd(med[pk]):.3f} at Mach {mach(pk):.2f}")
print(f"worst |CSV - PNG| over the sampled Machs: {worst:.3f}")
