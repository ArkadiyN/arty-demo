"""V0 sensitivity of the 1944-Ordnance drag corroboration and of shipped R50 / lethal area.

Consumer: experiment/fragmentation-field/challenges/drag-gap-1944/v0-sensitivity.md
(every number in that document is printed by this script).

A. Assert no src/arty file carries the 1944 V0 captions (3120 / 3500 ft/s).
B. V2 corroboration RMS (arrival M>0.7) at the shipped combined constant vs a
   uniform scale s on V0_FTS, both 1944 columns; the s-band inside RMS <= 0.10.
C. Free two-parameter fit ln v = ln V0 - c * x, x = rho_air/(2 rho^(2/3)) m^(-1/3) r,
   per shell and pooled: the V0 the tables themselves imply (constant C_D).
D. Shipped-model response: R50 (cross slice) and lethal area from
   compute_frag_field_3d with the Gurney constant scaled by s -- i.e. what a
   V0 change *would* do if it reached the model (it does not; see A).
"""
import csv
import dataclasses
import pathlib
import re
import time

import numpy as np

from arty.fragmentation import (DragParams, compute_frag_field_3d, gurney_velocity)
from arty.shells import SHELLS

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
TAB = ROOT / "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"

FT = 0.3048
OZ = 0.028349523125
A_SOUND = 340.3
# Source-stated captions, kept as literals (ordnance-1944.md "INITIAL FRAGMENT VELOCITY ... F/S")
V0_FTS = {"75mm M48 HE": 3120.0, "105mm M1 HE": 3500.0, "155mm M107 HE": 3500.0}
STEM = {"75mm M48 HE": "75mm-m48", "105mm M1 HE": "105mm-m1", "155mm M107 HE": "155mm-m107"}
COLUMNS = ("casualties", "perforation-1-8in")

drag = DragParams()
COMBINED = drag.C_D * drag.C_shape

# ---------------- A ----------------
hits = [f"{p.name}:{i+1}" for p in (ROOT / "src/arty").glob("*.py")
        for i, line in enumerate(p.read_text().splitlines())
        if re.search(r"\b(3120|3,120|3500|3,500)\b", line)]
print(f"A. src/arty lines containing 3120/3500: {hits or 'none'}")
print(f"   shipped combined C_D*C_shape = {COMBINED:.4f} (derived from k=2600, not fitted)")


def load(column):
    rho, v0, r, m, v, idx = [], [], [], [], [], []
    for i, (shell, stem) in enumerate(STEM.items()):
        with (TAB / f"{stem}-{column}.csv").open() as fh:
            for row in csv.DictReader(fh):
                rho.append(SHELLS[shell].steel.rho)
                v0.append(V0_FTS[shell] * FT)
                r.append(float(row["r_ft"]) * FT)
                m.append(float(row["m_oz"]) * OZ)
                v.append(float(row["v_fps"]) * FT)
                idx.append(i)
    return tuple(np.array(a) for a in (rho, v0, r, m, v, idx))


def xcoord(rho, r, m):
    return drag.rho_air / (2.0 * rho ** (2.0 / 3.0)) * m ** (-1.0 / 3.0) * r


# ---------------- B ----------------
S = np.linspace(0.85, 1.15, 601)
print("\nB. V2 RMS(M>0.7) of ln(v_model/v_src) at shipped constant vs V0 scale s")
for col in COLUMNS:
    rho, v0, r, m, v, idx = load(col)
    sel = v / A_SOUND > 0.7
    base = np.log(v0 / v) - COMBINED * xcoord(rho, r, m)       # residual at s=1
    res = base[sel][None, :] + np.log(S)[:, None]              # (len S, n)
    rms = np.sqrt(np.mean(res ** 2, axis=1))
    ok = S[rms <= 0.10]
    i1 = np.argmin(np.abs(S - 1.0))
    band = f"[{ok.min():.3f}, {ok.max():.3f}]" if ok.size else "empty"
    print(f"  {col:18s} n={int(sel.sum()):2d} RMS(s=1)={rms[i1]:.3f} "
          f"RMS(0.9)={rms[np.argmin(abs(S-0.9))]:.3f} RMS(1.1)={rms[np.argmin(abs(S-1.1))]:.3f} "
          f"min={rms.min():.3f} at s={S[rms.argmin()]:.3f}  PASS band s in {band}  "
          f"mean bias={base[sel].mean():+.3f}")

# ---------------- C ----------------
print("\nC. Free fit ln v = ln V0 - c x  (constant C_D; c = C_D*C_shape)")
for col in COLUMNS:
    rho, v0, r, m, v, idx = load(col)
    x = xcoord(rho, r, m)
    for i, shell in [(k, s) for k, s in enumerate(STEM)] + [(None, "pooled (common s)")]:
        if i is None:
            # common fractional V0 scale s and common c, all shells
            A = np.column_stack([np.ones_like(x), -x])
            y = np.log(v / v0)
            (lns, c), *_ = np.linalg.lstsq(A, y, rcond=None)
            print(f"  {col:18s} {shell:18s} s_fit={np.exp(lns):.3f}  c_fit={c:.3f}")
            continue
        for tag, k in (("all  ", idx == i), ("M>0.7", (idx == i) & (v / A_SOUND > 0.7))):
            A = np.column_stack([np.ones(k.sum()), -x[k]])
            (lnv0, c), *_ = np.linalg.lstsq(A, np.log(v[k]), rcond=None)
            print(f"  {col:18s} {shell:14s} {tag} n={int(k.sum()):2d} "
                  f"V0_fit={np.exp(lnv0)/FT:6.0f} ft/s (caption {V0_FTS[shell]:.0f}, "
                  f"ratio {np.exp(lnv0)/FT/V0_FTS[shell]:.3f})  c_fit={c:.3f}  "
                  f"x-span={x[k].min():.3f}-{x[k].max():.3f}")

# ---------------- D ----------------
print("\nD. Shipped model: R50_cross [m] and lethal area [m^2] vs Gurney V0 scale s")
t0 = time.time()
for shell_name in STEM:
    sh = SHELLS[shell_name]
    g = gurney_velocity(sh)
    s_src = V0_FTS[shell_name] * FT / g
    row = [f"  {shell_name:14s} V0_gurney={g:6.1f} m/s  caption/gurney={s_src:.3f} |"]
    out = {}
    for s in (0.9, 1.0, s_src, 1.1):
        sh_s = dataclasses.replace(sh, filler=dataclasses.replace(
            sh.filler, gurney_const=sh.filler.gurney_const * s))
        res = compute_frag_field_3d(sh_s, max_radius=120.0, n_grid=241)
        out[s] = (res.r50_cross, res.lethal_area, res.N0)
    r0, a0, n0 = out[1.0]
    for s, (r5, la, n) in out.items():
        row.append(f" s={s:.3f}: R50={r5:5.1f} ({r5/r0-1:+.1%}) "
                   f"LA={la:5.0f} ({la/a0-1:+.1%}) N0={n:5.0f}")
    print("".join(row))
    lo, hi = out[0.9], out[1.1]
    print(f"     elasticity dlnR50/dlnV0={np.log(hi[0]/lo[0])/np.log(1.1/0.9):.2f}  "
          f"dlnLA/dlnV0={np.log(hi[1]/lo[1])/np.log(1.1/0.9):.2f}")
print(f"   (D took {time.time()-t0:.1f} s)")
