"""Does the Mott fragment-shape closure (v0.8.0) close the velocity-decay gap?

(1) Structural: recompute the drag-calibration ratio table with the CURRENT
    arty code (post shape-closure) and confirm it reproduces the pre-closure
    table -- mu/N0 do not enter retardation_coeff.
(2) Invert each source row for the combined C_D*C_shape it demands.
(3) Anchor C_shape to the reference-area convention of DoD 1975
    (10-F-0806 p.7): m = k A^{3/2} with k = 2.60 g/cm3 for forged steel
    projectile fragments => C_shape = (rho_s/k)^{2/3}.  Validate that identity
    against the same source's k for steel cubes and spheres.
"""
from dataclasses import dataclass

import numpy as np

from arty.shells import SHELLS
from arty.fragmentation import DragParams, retardation_coeff

FT_TO_M = 0.3048
FTS_TO_MS = 0.3048
OZ_TO_KG = 0.028349523125
GRAIN_PER_IN3_TO_G_PER_CM3 = 0.06479891 / 16.387064
A_SOUND = 340.0  # m/s, sea-level standard

RHO_S = 7850.0
C_D_DOD = 1.28  # DoD 1975 p.8 "constant at its supersonic value of 1.28"


def c_shape_from_k(k_g_cm3):
    """C_shape [-] implied by ballistic shape factor k [g/cm^3] via m = k A^{3/2}."""
    return (RHO_S / (k_g_cm3 * 1000.0)) ** (2.0 / 3.0)


def cauchy_box(a, b, c):
    """Tumbling-average C_shape [-] of a box a x b x c (Cauchy: <A> = S/4)."""
    return 0.5 * (a * b + b * c + c * a) / (a * b * c) ** (2.0 / 3.0)


CANDIDATES = {
    "current 0.585": 0.585,
    "prism C_sh=1.61": 0.65 * 1.61,
    "1.7 SAND high": 1.7,
    "DoD k=2.60 (2.67)": C_D_DOD * c_shape_from_k(2.60),
}

@dataclass
class ShellData:
    shell: str
    v0: float
    r: np.ndarray
    m_oz: np.ndarray
    v: np.ndarray


DATA = {
    "75mm M48 HE": ShellData(
        shell="75mm M48 HE", v0=3120.0,
        r=np.array([20, 100, 400], dtype=float),
        m_oz=np.array([0.014, 0.063, 0.244]),
        v=np.array([2060, 972, 494], dtype=float)),
    "105mm M1 HE": ShellData(
        shell="105mm M1 HE", v0=3500.0,
        r=np.array([20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300], dtype=float),
        m_oz=np.array([0.035, 0.047, 0.061, 0.095, 0.137, 0.192, 0.255, 0.326,
                       0.448, 0.580, 1.05]),
        v=np.array([2700, 2430, 2220, 1920, 1750, 1550, 1420, 1320, 1200, 1120,
                    955], dtype=float)),
    "155mm M107 HE": ShellData(
        shell="155mm M107 HE", v0=3500.0,
        r=np.array([20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600], dtype=float),
        m_oz=np.array([0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109,
                       0.161, 0.233, 0.402]),
        v=np.array([2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505,
                    383], dtype=float)),
}


def main():
    print("--- (3) reference-area identity C_shape = (rho_s/k)^{2/3} ---")
    for name, k_grains, ref in [
        ("steel cube", 1080.0, "Cauchy 1.500"),
        ("steel sphere", 1490.0, "Cauchy 1.209"),
    ]:
        k = k_grains * GRAIN_PER_IN3_TO_G_PER_CM3
        print(f"  {name:12s} k={k:.3f} g/cm3 -> C_shape={c_shape_from_k(k):.3f} "
              f"(closed form {ref})")
    k_frag = 2.60
    cs = c_shape_from_k(k_frag)
    print(f"  forged steel projectile fragments k={k_frag:.2f} g/cm3 -> "
          f"C_shape={cs:.3f}; combined with C_D=1.28 -> {C_D_DOD*cs:.2f}")
    L1_dod = 2.0 * (k_frag * 1000.0) ** (2.0 / 3.0) / (C_D_DOD * 1.2)
    print(f"  reproduce source L1: {L1_dod:.1f} m/kg^(1/3) (source states 247)")
    L1_arty = 2.0 * RHO_S ** (2.0 / 3.0) / (1.225 * 0.585)
    print(f"  arty L1 (C_D*C_shape=0.585): {L1_arty:.0f} m/kg^(1/3) "
          f"= {L1_arty/L1_dod:.2f}x the DoD value")
    print(f"  derivation prism 9.39x5.87x3.67mm -> C_shape="
          f"{cauchy_box(9.39, 5.87, 3.67):.3f} -> implied k="
          f"{7.85/cauchy_box(9.39,5.87,3.67)**1.5:.2f} g/cm3 (measured 2.60)")

    for label, d in DATA.items():
        shell = SHELLS[d.shell]
        rho = shell.steel.rho
        s = d.r * FT_TO_M
        m = d.m_oz * OZ_TO_KG
        v_src = d.v * FTS_TO_MS
        v0 = d.v0 * FTS_TO_MS

        k_src = np.log(v0 / v_src) / (s * m ** (-1.0 / 3.0))
        req = 2.0 * rho ** (2.0 / 3.0) * k_src / DragParams().rho_air
        mach = v_src / A_SOUND

        print(f"\n=== {label} ===")
        # req_comb / C_shape(k=2.60) = the path-averaged C_D the row demands
        cd_imp = req / c_shape_from_k(2.60)
        hdr = f"{'r(ft)':>6} {'m(oz)':>7} {'Mach':>5} {'req_comb':>9} {'C_D_imp':>8}"
        for c in CANDIDATES:
            hdr += f" {c:>19}"
        print(hdr)
        cols = {}
        for cname, comb in CANDIDATES.items():
            lam = retardation_coeff(m, DragParams(C_D=comb, C_shape=1.0), rho)
            cols[cname] = (v0 * np.exp(-lam * s)) / v_src
        for i in range(len(s)):
            row = (f"{d.r[i]:6.0f} {d.m_oz[i]:7.3f} {mach[i]:5.2f} "
                   f"{req[i]:9.2f} {cd_imp[i]:8.2f}")
            for cname in CANDIDATES:
                row += f" {cols[cname][i]:19.2f}"
            print(row)
        sup = mach >= 0.9
        print(f"  req combined: all {req.min():.2f}-{req.max():.2f} "
              f"(mean {req.mean():.2f}); Mach>=0.9 rows "
              f"{req[sup].min():.2f}-{req[sup].max():.2f} "
              f"(mean {req[sup].mean():.2f}, n={sup.sum()})")
        d_col = cols["DoD k=2.60 (2.67)"]
        print(f"  DoD-anchored ratio: all {d_col.min():.2f}-{d_col.max():.2f}; "
              f"Mach>=0.9 {d_col[sup].min():.2f}-{d_col[sup].max():.2f}")
        E = 0.5 * m * v_src ** 2
        print(f"  striking energy of tabulated rows: {E.min():.0f}-{E.max():.0f} J "
              f"(mean {E.mean():.0f})")


def sphere_floor():
    """Isoperimetric floor on C_shape: Cauchy <A>=S/4 and S >= (36 pi V^2)^(1/3)."""
    return (36.0 * np.pi) ** (1.0 / 3.0) / 4.0


if __name__ == "__main__":
    main()
    print("\n--- convex floor ---")
    print(f"  min possible C_shape (sphere) = {sphere_floor():.4f}; "
          f"arty ships 0.90 = {0.90/sphere_floor():.2f}x the floor")
    _RUN_EXTRA = True


def extra():
    """What prism length reproduces the measured k = 2.60 g/cm3 at the 75mm
    derivation breadth/thickness (5.87 x 3.67 mm)?"""
    from scipy.optimize import brentq
    b, c = 5.87, 3.67
    target = c_shape_from_k(2.60)

    def residual(length):
        return cauchy_box(length, b, c) - target

    length = brentq(residual, 5.87, 200.0)
    print("\n--- prism re-shaping ---")
    print(f"  target C_shape {target:.3f}; l={length:.2f} mm at b={b}, c={c} "
          f"-> aspect l/b = {length/b:.2f} (derivation asserts 1.60)")
    print(f"  alpha and hence mu scale with l -> mu would rise "
          f"{length/9.39:.2f}x vs the shipped closure")


if __name__ == "__main__":
    extra()
