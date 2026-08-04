"""CSV-vs-page residual at every CSV row, using a local fit of the PNG stroke
that interpolates ACROSS gridline columns rather than sampling beside them."""

import csv
import pathlib

import numpy as np
from PIL import Image

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
D = ROOT / "doc-reference/fragmentation/dod-1975-fragment-debris-hazards"
img = np.asarray(Image.open(D/"images/figure-3-drag-coefficient-vs-mach.png").convert("L"), dtype=float)
X0, X7, Y15, Y10 = 153.0, 991.5, 55.0, 658.0
def mach(c):
    return 7.0*(c-X0)/(X7-X0)


def cdf(r):
    return 1.0 + 0.5*(Y10-r)/(Y10-Y15)

grid = [X0 + k*(X7-X0)/14.0 for k in range(15)]
pts=[]
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
        pts.append((mach(c), cdf(0.5*(best[0]+best[1]-1)+59)))
P=np.array(pts)
# drop outliers vs a rolling median
P = P[np.argsort(P[:, 0])]
keep=[]
for i in range(len(P)):
    w=P[max(0,i-6):i+7,1]
    if abs(P[i,1]-np.median(w)) <= 0.02:
        keep.append(i)
P=P[keep]
rows=list(csv.DictReader(open(D/"tables/figure-3-drag-coefficient.csv")))
res=[]
for r in rows:
    m = float(r["mach"])
    v = float(r["cd"])
    sel=P[(P[:,0]>=m-0.18)&(P[:,0]<=m+0.18)]
    if len(sel) < 6:
        continue
    p=np.polyfit(sel[:,0],sel[:,1],3)
    res.append((m, v, float(np.polyval(p,m))))
res=np.array(res)
d=res[:,1]-res[:,2]
print(f"{len(res)} rows compared; mean {d.mean():+.4f}  RMS {np.sqrt((d**2).mean()):.4f}  max|d| {np.abs(d).max():.4f}")
print("\nrows with |CSV - page| > 0.010:")
for m,v,pg in res[np.abs(d)>0.010]:
    print(f"  Mach {m:4.2f}  CSV {v:.3f}   page {pg:.3f}   {v-pg:+.3f}")
