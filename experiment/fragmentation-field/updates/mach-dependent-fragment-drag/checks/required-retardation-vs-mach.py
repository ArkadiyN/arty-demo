"""Scoping screen for experiment/fragmentation-field/updates/mach-dependent-fragment-drag/scoping.md.

Two questions, one script:

 1. What combined C_D*C_shape (in arty's `retardation_coeff` parameterization)
    would each 1944 Ordnance (m(r), v(r), V0) point require, and over what Mach
    band does that point's trajectory live?  Reported also as the equivalent
    unit-mass 1/e distance L1 [m/kg^(1/3)] and ballistic density k [kg/m3], so
    it can be compared directly against DoD-1975's recommended
    k = 2.60 g/cm3, C_D = 1.28, L1 = 247 m/kg^(1/3).

 2. Does the digitized DoD-1975 Figure 3 C_D(M) curve, integrated numerically
    along the trajectory, reproduce v(r) once the presented-area closure uses
    the DoD ballistic density instead of a compact-cube area?

(m(r), v(r), V0) triples reused verbatim from
challenges/drag-gap-1944/checks/drag-coefficient-calibration.py.
"""
import numpy as np

from arty.shells import SHELLS

FT_TO_M = 0.3048
OZ_TO_KG = 0.028349523125
RHO_AIR = 1.225
A_SOUND = 340.3  # m/s, sea-level standard

# DoD-1975 Figure 3, digitized (doc-reference/.../figure-3-digitized.md)
MACH = np.array([0.0, 0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.2, 2.6, 3.0, 4.0, 5.0, 7.0])
CD = np.array([1.08, 1.09, 1.10, 1.14, 1.38, 1.40, 1.35, 1.33, 1.30, 1.29, 1.28, 1.28, 1.28, 1.28])

K_DOD = 2600.0  # kg/m3, forged steel projectile/frag-bomb fragments (DoD-1975 p.7)


def cd_of_mach(v):
    return np.interp(v / A_SOUND, MACH, CD)


def c_shape_for_k(k, rho_steel):
    """arty C_shape equivalent to a DoD ballistic density k [kg/m3]."""
    return (rho_steel / k) ** (2.0 / 3.0)


def lam_of(m, combined, rho_steel):
    return RHO_AIR * combined / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)


def integrate(m, v0, r_end, rho_steel, c_shape, n=4000):
    """dv/dx = -lam(m) * C_D(M(v)) * v, exact for the velocity-squared law."""
    dx = r_end / n
    v = v0
    base = RHO_AIR * c_shape / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)
    for _ in range(n):
        k1 = -base * cd_of_mach(v) * v
        k2 = -base * cd_of_mach(v + 0.5 * dx * k1) * (v + 0.5 * dx * k1)
        v = v + dx * k2
    return v


def run(label, shell_name, v0_fts, r_ft, m_oz, v_fts):
    shell = SHELLS[shell_name]
    rho_s = shell.steel.rho
    r = r_ft * FT_TO_M
    m = m_oz * OZ_TO_KG
    v = v_fts * FT_TO_M
    v0 = v0_fts * FT_TO_M

    # required path-averaged combined C_D*C_shape
    lam_req = np.log(v0 / v) / r
    c_req = lam_req * 2.0 * rho_s ** (2.0 / 3.0) * m ** (1.0 / 3.0) / RHO_AIR
    L1_req = 1.0 / (lam_req * m ** (1.0 / 3.0))
    # equivalent ballistic density if C_D were held at 1.28
    k_req = (RHO_AIR * 1.28 / (2.0 * lam_req * m ** (1.0 / 3.0))) ** 1.5

    cs = c_shape_for_k(K_DOD, rho_s)
    print(f"\n=== {label}  (rho_steel={rho_s:.0f}, DoD C_shape={cs:.2f}, "
          f"combined at C_D=1.28: {1.28 * cs:.2f}) ===")
    print(f"{'r(ft)':>6} {'m(oz)':>6} {'M0':>5} {'M(r)':>5} {'C_req':>6} "
          f"{'L1_req':>7} {'k_req':>7} {'ratio_fig3':>10} {'ratio_C=2.68':>12}")
    for i in range(len(r)):
        v_fig3 = integrate(m[i], v0, r[i], rho_s, cs)
        lam_c = lam_of(m[i], 1.28 * cs, rho_s)
        v_const = v0 * np.exp(-lam_c * r[i])
        print(f"{r_ft[i]:6.0f} {m_oz[i]:6.3f} {v0 / A_SOUND:5.2f} "
              f"{v[i] / A_SOUND:5.2f} {c_req[i]:6.2f} {L1_req[i]:7.0f} "
              f"{k_req[i]:7.0f} {v_fig3 / v[i]:10.2f} {v_const / v[i]:12.2f}")


if __name__ == "__main__":
    print("arty current: C_D*C_shape=0.585 ->",
          f"L1 = {1.0 / (RHO_AIR * 0.585 / (2 * 7850 ** (2 / 3))):.0f} m/kg^(1/3)")
    print("DoD-1975 quoted: k=2.60 g/cm3, C_D=1.28 -> L1 = 247 m/kg^(1/3)")
    run("75mm M48 HE", "75mm M48 HE", 3120.0,
        np.array([20, 100, 400], dtype=float),
        np.array([0.014, 0.063, 0.244]),
        np.array([2060, 972, 494], dtype=float))
    run("105mm M1 HE", "105mm M1 HE", 3500.0,
        np.array([20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300], dtype=float),
        np.array([0.035, 0.047, 0.061, 0.095, 0.137, 0.192, 0.255, 0.326, 0.448, 0.580, 1.05]),
        np.array([2700, 2430, 2220, 1920, 1750, 1550, 1420, 1320, 1200, 1120, 955], dtype=float))
    run("155mm M107 HE", "155mm M107 HE", 3500.0,
        np.array([20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600], dtype=float),
        np.array([0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109, 0.161, 0.233, 0.402]),
        np.array([2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505, 383], dtype=float))


def summarise():
    """RMS of ln(v_model/v_source) over all 25 points, per candidate law."""
    data = [
        ("75mm M48 HE", 3120.0, [20, 100, 400], [0.014, 0.063, 0.244], [2060, 972, 494]),
        ("105mm M1 HE", 3500.0,
         [20, 30, 40, 60, 80, 100, 120, 140, 170, 200, 300],
         [0.035, 0.047, 0.061, 0.095, 0.137, 0.192, 0.255, 0.326, 0.448, 0.580, 1.05],
         [2700, 2430, 2220, 1920, 1750, 1550, 1420, 1320, 1200, 1120, 955]),
        ("155mm M107 HE", 3500.0,
         [20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600],
         [0.010, 0.014, 0.019, 0.030, 0.043, 0.055, 0.083, 0.109, 0.161, 0.233, 0.402],
         [2440, 2060, 1770, 1410, 1180, 1040, 846, 738, 598, 505, 383]),
    ]
    rows = []
    for name, v0f, rf, mo, vf in data:
        rho_s = SHELLS[name].steel.rho
        cs = c_shape_for_k(K_DOD, rho_s)
        for r_, m_, v_ in zip(rf, mo, vf):
            rows.append((rho_s, cs, np.array(v0f) * FT_TO_M, r_ * FT_TO_M,
                         m_ * OZ_TO_KG, v_ * FT_TO_M))

    def rms_for_const(c):
        e = [np.log(v0 * np.exp(-lam_of(m, c, rs) * r) / v)
             for rs, cs, v0, r, m, v in rows]
        return float(np.sqrt(np.mean(np.square(e))))

    grid = np.linspace(0.5, 4.0, 351)
    best = min(grid, key=rms_for_const)
    for label, c in [("current 0.585", 0.585), ("1.2", 1.2), ("1.7", 1.7),
                     ("DoD 1.28*2.09 = 2.67", 1.28 * c_shape_for_k(K_DOD, 7850.0)),
                     (f"best-fit const {best:.2f}", best)]:
        print(f"  const {label:28s} RMS ln-ratio = {rms_for_const(c):.3f}")
    e = [np.log(integrate(m, v0, r, rs, cs) / v) for rs, cs, v0, r, m, v in rows]
    print(f"  Fig-3 C_D(M), k=2.60          RMS ln-ratio = "
          f"{float(np.sqrt(np.mean(np.square(e)))):.3f}")
    # restricted to arrival Mach > 0.7 (the lethal-fragment regime)
    sel = [i for i, (rs, cs, v0, r, m, v) in enumerate(rows) if v / A_SOUND > 0.7]
    print(f"  [arrival M>0.7 subset, n={len(sel)}]")
    for label, c in [("DoD const 2.67", 1.28 * c_shape_for_k(K_DOD, 7850.0)),
                     ("current 0.585", 0.585)]:
        e2 = [np.log(rows[i][2] * np.exp(-lam_of(rows[i][4], c, rows[i][0]) * rows[i][3])
                     / rows[i][5]) for i in sel]
        print(f"    const {label:24s} RMS = {float(np.sqrt(np.mean(np.square(e2)))):.3f}")
    e2 = [e[i] for i in sel]
    print(f"    Fig-3 C_D(M), k=2.60          RMS = "
          f"{float(np.sqrt(np.mean(np.square(e2)))):.3f}")


summarise()
