"""Clean value of C_D at Mach 1.0 from the PNG, interpolating ACROSS the
Mach-1.0 vertical rule instead of sampling next to it."""
import pathlib
import numpy as np
from PIL import Image
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
PNG = ROOT / "doc-reference/fragmentation/dod-1975-fragment-debris-hazards/images/figure-3-drag-coefficient-vs-mach.png"
img = np.asarray(Image.open(PNG).convert("L"), dtype=float)
X0, X7 = 153.0, 991.5
Y15, Y10 = 55.0, 658.0
def mach(c):
    return 7.0*(c-X0)/(X7-X0)


def cd(r):
    return 1.0 + 0.5*(Y10-r)/(Y10-Y15)

grid = [X0 + k*(X7-X0)/14.0 for k in range(15)]
pts = []
for c in range(int(X0)+3, int(X7)-2):
    if any(abs(c-g) <= 7 for g in grid):
        continue
    col = img[59:655, c] < 100
    best, i = None, 0
    while i < len(col):
        if col[i]:
            j = i
            while j < len(col) and col[j]:
                j += 1
            if j-i >= 3 and (best is None or j-i > best[1]-best[0]):
                best = (i, j)
            i = j
        else:
            i += 1
    if best:
        pts.append((mach(c), cd(0.5*(best[0]+best[1]-1)+59)))
pts = np.array(pts)
for lo, hi, tgt in [(0.82, 1.18, 1.0), (0.88, 1.12, 1.0), (1.32, 1.68, 1.5)]:
    sel = pts[(pts[:,0] >= lo) & (pts[:,0] <= hi)]
    p = np.polyfit(sel[:,0], sel[:,1], 4)
    print(f"window {lo}-{hi} ({len(sel)} cols): C_D(Mach {tgt}) = {np.polyval(p, tgt):.3f}")
sel = pts[(pts[:,0] >= 0.9) & (pts[:,0] <= 1.15)]
print("\nraw PNG stroke near Mach 1 (clean columns only):")
for m, v in sel[::3]:
    print(f"  {m:.3f}  {v:.3f}")
