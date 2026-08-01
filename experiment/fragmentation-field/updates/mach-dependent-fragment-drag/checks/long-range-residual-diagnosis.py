"""Diagnoses the long-range / low-arrival-Mach residual that no constant and no
Fig-3 C_D(M) candidate closes, and asks whether the best *constant* or the
Fig-3 curve wins on the lethal-relevant arrival-Mach subset.

Feeds experiment/fragmentation-field/updates/mach-dependent-fragment-drag/scoping.md
(sections "How much of the improvement is Mach-dependence?" and
"The long-range residual is not gravity").

Three questions:
  1. Best-fit constant restricted to arrival Mach > 0.7 -- does Fig-3 C_D(M)
     beat the *best* constant there, or only the DoD constant?
  2. Free-fall terminal velocity sqrt(g*L) per 1944 Ordnance point, vs. the
     model/source velocity gap. DOD (1975) p.9 argues the gravity-free
     exponential is valid until v drops to the free-fall terminal velocity;
     this checks whether that floor is anywhere near the observed residual.
  3. C_D implied by each point if the presented-area closure is held at the
     DoD ballistic density k = 2.60 g/cm3, tabulated against arrival Mach, for
     direct comparison with the digitized Figure 3 curve.
"""
import numpy as np

from arty.shells import SHELLS

FT_TO_M = 0.3048
OZ_TO_KG = 0.028349523125
RHO_AIR = 1.225
A_SOUND = 340.3
G = 9.80665
K_DOD = 2600.0

MACH = np.array([0.0, 0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.2, 2.6, 3.0, 4.0, 5.0, 7.0])
CD = np.array([1.08, 1.09, 1.10, 1.14, 1.38, 1.40, 1.35, 1.33, 1.30, 1.29, 1.28, 1.28, 1.28, 1.28])

DATA = [
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


def cd_of_mach(v):
    return np.interp(v / A_SOUND, MACH, CD)


def c_shape_for_k(k, rho_steel):
    return (rho_steel / k) ** (2.0 / 3.0)


def lam_of(m, combined, rho_steel):
    return RHO_AIR * combined / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)


def integrate(m, v0, r_end, rho_steel, c_shape, n=4000):
    dx = r_end / n
    v = v0
    base = RHO_AIR * c_shape / (2.0 * rho_steel ** (2.0 / 3.0)) * m ** (-1.0 / 3.0)
    for _ in range(n):
        k1 = -base * cd_of_mach(v) * v
        k2 = -base * cd_of_mach(v + 0.5 * dx * k1) * (v + 0.5 * dx * k1)
        v = v + dx * k2
    return v


def rows():
    out = []
    for name, v0f, rf, mo, vf in DATA:
        rho_s = SHELLS[name].steel.rho
        for r_, m_, v_ in zip(rf, mo, vf):
            out.append(dict(name=name, rho=rho_s, v0=v0f * FT_TO_M, r=r_ * FT_TO_M,
                            r_ft=r_, m=m_ * OZ_TO_KG, v=v_ * FT_TO_M))
    return out


def main():
    R = rows()
    cs = c_shape_for_k(K_DOD, 7850.0)

    # --- Q1: best-fit constant on the arrival-Mach > 0.7 subset -------------
    def rms(sel, c):
        e = [np.log(d["v0"] * np.exp(-lam_of(d["m"], c, d["rho"]) * d["r"]) / d["v"])
             for d in sel]
        return float(np.sqrt(np.mean(np.square(e))))

    for label, sel in (("all 25", R), ("arrival M>0.7", [d for d in R if d["v"] / A_SOUND > 0.7])):
        grid = np.linspace(0.5, 4.0, 3501)
        best = min(grid, key=lambda c: rms(sel, c))
        e = [np.log(integrate(d["m"], d["v0"], d["r"], d["rho"], cs) / d["v"]) for d in sel]
        print(f"[{label}, n={len(sel)}]")
        print(f"  current 0.585        RMS = {rms(sel, 0.585):.3f}")
        print(f"  DoD const 1.28*{cs:.2f}={1.28*cs:.2f}  RMS = {rms(sel, 1.28*cs):.3f}")
        print(f"  best-fit const {best:.2f}   RMS = {rms(sel, best):.3f}")
        print(f"  Fig-3 C_D(M), k=2.60 RMS = {float(np.sqrt(np.mean(np.square(e)))):.3f}\n")

    # --- Q2/Q3: gravity floor and implied C_D(M) ---------------------------
    print(f"{'shell':>14} {'r(ft)':>6} {'m(g)':>7} {'M(r)':>5} {'v_src':>7} "
          f"{'v_fig3':>7} {'v_term':>7} {'CD_req':>7}")
    for d in R:
        lam_req = np.log(d["v0"] / d["v"]) / d["r"]
        c_req = lam_req * 2.0 * d["rho"] ** (2.0 / 3.0) * d["m"] ** (1.0 / 3.0) / RHO_AIR
        L_dod = 247.0 * d["m"] ** (1.0 / 3.0)  # DoD-1975 L1 = 247 m/kg^(1/3)
        v_fig3 = integrate(d["m"], d["v0"], d["r"], d["rho"], cs)
        print(f"{d['name'][:14]:>14} {d['r_ft']:6.0f} {d['m']*1e3:7.3f} "
              f"{d['v']/A_SOUND:5.2f} {d['v']:7.1f} {v_fig3:7.1f} "
              f"{np.sqrt(G*L_dod):7.1f} {c_req/cs:7.2f}")


if __name__ == "__main__":
    main()
