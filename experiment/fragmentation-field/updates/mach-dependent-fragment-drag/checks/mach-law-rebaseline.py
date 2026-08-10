"""Re-baseline of the Mach-dependent-drag rejection in
experiment/fragmentation-field/updates/mach-dependent-fragment-drag/rebaseline-verdict.md.

Re-runs derivation.md section 5 (and V2 of section 4) with the two inputs that
have since been corrected:

  1. C_D(M) read from the closure-checked
     doc-reference/fragmentation/dod-1975-fragment-debris-hazards/tables/
     figure-3-drag-coefficient.csv, not the superseded eyeballed
     figure-3-digitized.md array that the original script hand-copied.
  2. The 1944 Ordnance (r, m, v) triples read from the closure-checked
     doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/
     tables/*-casualties.csv, not hand-typed.  The original 105mm series was an
     exact match to 105mm-m1-perforation-1-8in.csv (wrong column); the 75mm
     series used only 3 of the 10 available casualties rows.

All sweeps are vectorised over rows; runtime ~1 s.
"""
import csv
import pathlib

import numpy as np

from arty.shells import SHELLS

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
DOC = ROOT / "doc-reference"

FT_TO_M = 0.3048
OZ_TO_KG = 0.028349523125
RHO_AIR = 1.225
A_SOUND = 340.3
K_DOD = 2600.0
CD_PLATEAU = 1.28

# V0 [ft/s] as used by every prior script in this thread. NOTE: the literal
# figures appear verbatim as "INITIAL FRAGMENT VELOCITY 3,120/3,500 F/S" table
# headers in six doc-reference/.../tables/*.invariant anchors -- but whether
# that table-caption occurrence constitutes *provenance* for V0_FTS as used
# here (a stated derivation, not just a repeated caption) is an open question;
# see verdict, Note V0 / OPEN-FINDINGS.md.
V0_FTS = {"75mm M48 HE": 3120.0, "105mm M1 HE": 3500.0, "155mm M107 HE": 3500.0}
CSVS = {
    "75mm M48 HE": "75mm-m48",
    "105mm M1 HE": "105mm-m1",
    "155mm M107 HE": "155mm-m107",
}


def load_cd(name):
    p = DOC / "fragmentation/dod-1975-fragment-debris-hazards/tables" / name
    m, c = [], []
    with p.open() as fh:
        for row in csv.DictReader(fh):
            m.append(float(row["mach"]))
            c.append(float(row["cd"]))
    return np.array(m), np.array(c)


def load_old_cd():
    """The superseded eyeballed table, parsed from its own markdown (not retyped)."""
    p = DOC / "fragmentation/dod-1975-fragment-debris-hazards/figure-3-digitized.md"
    m, c = [], []
    for line in p.read_text().splitlines():
        parts = [t.strip() for t in line.strip().strip("|").split("|")]
        if len(parts) == 2:
            try:
                m.append(float(parts[0]))
                c.append(float(parts[1]))
            except ValueError:
                pass
    return np.array(m), np.array(c)


def load_rows(column):
    """Return arrays (rho_steel, v0 [m/s], r [m], m [kg], v [m/s], shell-index)."""
    rho, v0, r, mm, vv, idx = [], [], [], [], [], []
    for i, (shell, stem) in enumerate(CSVS.items()):
        p = (DOC / "wound-ballistics/ordnance-dept-1944-shell-fragment-damage/tables"
             / f"{stem}-{column}.csv")
        with p.open() as fh:
            for row in csv.DictReader(fh):
                rho.append(SHELLS[shell].steel.rho)
                v0.append(V0_FTS[shell] * FT_TO_M)
                r.append(float(row["r_ft"]) * FT_TO_M)
                mm.append(float(row["m_oz"]) * OZ_TO_KG)
                vv.append(float(row["v_fps"]) * FT_TO_M)
                idx.append(i)
    return (np.array(rho), np.array(v0), np.array(r), np.array(mm),
            np.array(vv), np.array(idx))


def base_coeff(m, c_shape, rho_steel):
    """lambda / C_D  [1/m]."""
    return RHO_AIR * c_shape / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)


def v_const(v0, r, m, combined, rho_steel):
    return v0 * np.exp(-base_coeff(m, combined, rho_steel) * r)


def v_mach(v0, r, m, c_shape, rho_steel, mach, cd, n=3000):
    """Vectorised RK2 march of dv/ds = -base * C_D(M(v)) * v over all rows."""
    base = base_coeff(m, c_shape, rho_steel)
    dx = r / n
    v = v0.copy()
    for _ in range(n):
        k1 = -base * np.interp(v / A_SOUND, mach, cd) * v
        vm = v + 0.5 * dx * k1
        k2 = -base * np.interp(vm / A_SOUND, mach, cd) * vm
        v = v + dx * k2
    return v


def rms(x):
    return float(np.sqrt(np.mean(np.square(x))))


def report(column):
    rho, v0, r, m, v, idx = load_rows(column)
    sel = v / A_SOUND > 0.7
    c_shape = (rho / K_DOD) ** (2.0 / 3.0)
    combined_dod = CD_PLATEAU * (7850.0 / K_DOD) ** (2.0 / 3.0)

    print(f"\n################ column = {column}   n = {len(r)} "
          f"(arrival M>0.7: {int(sel.sum())})")
    print(f"  DoD combined C_D*C_shape = {combined_dod:.4f}")

    grid = np.linspace(0.5, 6.0, 1101)
    r_all = np.array([rms(np.log(v_const(v0, r, m, c, rho) / v)) for c in grid])
    r_sel = np.array([rms(np.log(v_const(v0, r, m, c, rho)[sel] / v[sel]))
                      for c in grid])
    best_all, best_sel = grid[r_all.argmin()], grid[r_sel.argmin()]

    rows = [("const 0.585 (pre-update arty)", 0.585),
            ("const 2.6739 (adopted)", combined_dod),
            (f"best-fit const, all pts = {best_all:.3f}", best_all),
            (f"best-fit const, M>0.7  = {best_sel:.3f}", best_sel)]
    print(f"  {'law':44s} {'RMS all':>9} {'RMS M>0.7':>10}")
    for label, c in rows:
        e = np.log(v_const(v0, r, m, c, rho) / v)
        print(f"  {label:44s} {rms(e):9.3f} {rms(e[sel]):10.3f}")

    for label, (mach, cd) in [
            ("Fig-3 C_D(M) OLD eyeballed, k=2600", load_old_cd()),
            ("Fig-3 C_D(M) CORRECTED csv, k=2600", load_cd("figure-3-drag-coefficient.csv"))]:
        vm = v_mach(v0, r, m, c_shape, rho, mach, cd)
        e = np.log(vm / v)
        print(f"  {label:44s} {rms(e):9.3f} {rms(e[sel]):10.3f}"
              f"   bias(all)={e.mean():+.3f} bias(M>0.7)={e[sel].mean():+.3f}")

    # Fair fight: let the Mach law fit its own scale (equiv. to fitting k),
    # exactly as the constant law is allowed to fit its own value.
    mach, cd = load_cd("figure-3-drag-coefficient.csv")
    scales = np.linspace(0.5, 3.0, 51)
    sc_all = np.array([rms(np.log(v_mach(v0, r, m, s * c_shape, rho, mach, cd) / v))
                       for s in scales])
    sc_sel = np.array([rms(np.log(v_mach(v0, r, m, s * c_shape, rho, mach, cd)[sel]
                                  / v[sel])) for s in scales])
    print(f"  {'Fig-3 CORRECTED, best scale on C_shape':44s} "
          f"{sc_all.min():9.3f} {sc_sel.min():10.3f}"
          f"   scale_all={scales[sc_all.argmin()]:.2f} "
          f"scale_sel={scales[sc_sel.argmin()]:.2f}")

    # per-shell M>0.7 RMS at the adopted constant and at the corrected Fig-3
    vm = v_mach(v0, r, m, c_shape, rho, mach, cd)
    print("  per-shell (arrival M>0.7):  const 2.674 / Fig-3 corrected")
    for i, shell in enumerate(CSVS):
        s = sel & (idx == i)
        if not s.any():
            continue
        ec = np.log(v_const(v0, r, m, combined_dod, rho)[s] / v[s])
        em = np.log(vm[s] / v[s])
        print(f"    {shell:16s} n={int(s.sum()):2d}  {rms(ec):.3f} / {rms(em):.3f}")


def v1():
    """L1 = 1/(lambda * m^(1/3)) at m = 1 kg."""
    for cd_label, cd in [("C_D=1.28 (source plateau)", 1.28),
                         ("C_D=1.280 (corrected csv asymptote)", 1.280)]:
        L1 = 2.0 * (K_DOD ** 2 * 1.0) ** (1.0 / 3.0) / (cd * RHO_AIR)
        print(f"  V1 {cd_label:38s} L1 = {L1:7.1f} m/kg^(1/3)  "
              f"(source 247, ratio {L1 / 247:.4f})")
    mach, cd = load_cd("figure-3-drag-coefficient.csv")
    print(f"  corrected csv: C_D(M=0)={cd[0]:.3f}  C_D(M=3)="
          f"{np.interp(3.0, mach, cd):.3f}  C_D(M=5)={np.interp(5.0, mach, cd):.3f}"
          f"  peak={cd.max():.3f} at M={mach[cd.argmax()]:.2f}")


def l2(column="casualties"):
    """Re-run derivation L2 / scoping 3b on the corrected column: per-point
    required combined constant, implied C_D at k=2600, Fig-3 shortfall."""
    rho, v0, r, m, v, idx = load_rows(column)
    names = list(CSVS)
    mach, cd = load_cd("figure-3-drag-coefficient.csv")
    c_shape = (rho / K_DOD) ** (2.0 / 3.0)
    vm = v_mach(v0, r, m, c_shape, rho, mach, cd)
    lam_req = np.log(v0 / v) / r
    c_req = lam_req / base_coeff(m, 1.0, rho)
    cd_impl = c_req / (7850.0 / K_DOD) ** (2.0 / 3.0)
    L = 1.0 / lam_req
    v_term = np.sqrt(9.80665 * L)
    print(f"\n############ L2 re-run, column = {column}")
    print(f"  {'shell':14s} {'r_ft':>6} {'M(r)':>5} {'C_req':>6} {'CD_impl':>8} "
          f"{'v_obs':>7} {'v_Fig3':>7} {'ratio':>6} {'v_term':>7}")
    for i in np.argsort(idx * 1000 + r):
        flag = "  <-- M<0.7" if v[i] / A_SOUND <= 0.7 else ""
        print(f"  {names[idx[i]]:14s} {r[i]/FT_TO_M:6.0f} {v[i]/A_SOUND:5.2f} "
              f"{c_req[i]:6.2f} {cd_impl[i]:8.3f} {v[i]:7.1f} {vm[i]:7.1f} "
              f"{vm[i]/v[i]:6.2f} {v_term[i]:7.1f}{flag}")
    sub = v / A_SOUND <= 0.7
    print(f"  M<0.7 subset (n={int(sub.sum())}): C_req range "
          f"{c_req[sub].min():.2f}-{c_req[sub].max():.2f}, implied C_D "
          f"{cd_impl[sub].min():.3f}-{cd_impl[sub].max():.3f}; "
          f"Fig-3 v ratio {vm[sub].min()/v[sub][np.argmin(vm[sub])]:.2f} min "
          f"{(vm[sub]/v[sub]).min():.2f}")


if __name__ == "__main__":
    v1()
    report("casualties")
    report("perforation-1-8in")
    l2("casualties")
