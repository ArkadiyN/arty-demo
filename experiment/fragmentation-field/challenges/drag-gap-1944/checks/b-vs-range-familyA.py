"""Check: does Family A (the graded ES-310 A_p·pk_given_hit kernel) reproduce
the 1944 Ordnance Dept. B-vs-range casualty data, and does it agree with
Family B, for the three registry shells at ground-burst geometry?

Consumer: every number in
experiment/fragmentation-field/challenges/drag-gap-1944/b-vs-range-familyA.md
(the per-shell B(r) tables, the factor-of-2 verdict, and the cross-family
divergence table).

Reduction: b-vs-range.md Section 2, "Family A -> B". `_four_zone_familyA_eval`
returns the expected lethal-hit count N(x,y) = rho_L(x,y) * A_p(gamma) at each
ground column, with the presented area already folded in. Family A relocates
each zone's belt to its own representative height z_rep, so each zone carries
its own gamma_z and hence its own A_p(gamma_z) -- there is no single A_p at a
point. The reduction therefore divides A_p out *per zone*, exactly inverting
what the builder folded in:

    rho_L(x, y) = sum_z  N_z(x, y) / A_p(gamma_z(x, y))
    B_model(r)  = < rho_L(r cos phi, r sin phi) >_phi * (0.3048 m/ft)^2

gamma_z is recomputed from the same `_belt_column_zrep_vec` call the builder
makes (same arguments), so the division is exact, not approximate.

Family A uses its own ES-310 `pk_given_hit(E)` curve as-is (anchored at
E_LETH_DEFAULT = 1000 J), per b-vs-range.md Section 2; Family B is fed the
card's own 58 ft-lb casualty threshold. The cross-family comparison below is
therefore threshold-confounded -- see the .md for the caveat.

Family B numbers are not re-derived here: this script imports the three
published per-caliber check modules (checks/b-vs-range-{75,105,155}mm.py) and
calls their own `b_model_at_range`, so both families run at the same ranges,
same AoF, and the same current drag calibration (DragParams() default,
C_D*C_shape = 2.674).

Run: uv run python experiment/fragmentation-field/challenges/drag-gap-1944/checks/b-vs-range-familyA.py
"""
import importlib.util
from pathlib import Path

import numpy as np

from arty.fragmentation import (
    STANDING,
    DragParams,
    _belt_column_zrep_vec,
    presented_area,
    retardation_coeff,
)
from arty.shells import SHELLS
from arty.zones import _four_zone_familyA_eval, compute_shell_zones

CHECKS = Path(__file__).resolve().parent

FT_TO_M = 0.3048

H_B = 0.0            # ground burst, matching the card's ground-burst tables
DELTA_DEG = 15.0     # spray-belt half-width, four-zone default
POSTURE = STANDING
N_MASS = 200         # mass-grid resolution, matching the app/notebook path
N_PHI = 72           # azimuthal ring samples, matching the Family B checks

AOF_SWEEP_DEG = [0.0, 15.0, 30.0, 45.0, 60.0]
AOF_PRIMARY_DEG = 30.0

CALIBERS = {"75mm M48 HE": "75mm", "105mm M1 HE": "105mm", "155mm M107 HE": "155mm"}


def load_familyB(caliber):
    """Import a published per-caliber Family B check module by path."""
    path = CHECKS / f"b-vs-range-{caliber}.py"
    spec = importlib.util.spec_from_file_location(f"bvr_{caliber}", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rho_L_familyA(zones, aof_deg, drag_lam_grid, m_grid, xg, yg, flat_Ap=False):
    """Family A lethal-fragment areal density rho_L [m^-2] at ground points (xg, yg) [m].

    Divides the presented area A_p(gamma_z) back out of `_four_zone_familyA_eval`'s
    per-zone expected-hit counts, zone by zone at each zone's own relocation
    height z_rep. Returns (rho_L [m^-2], min A_p encountered [m^2]).

    flat_Ap : divide by the head-on A_p(gamma = 0) everywhere instead. Used only
              to bound how much the reduction depends on the A_p treatment.
    """
    xg = np.asarray(xg, dtype=float)
    yg = np.asarray(yg, dtype=float)
    _, by_zone = _four_zone_familyA_eval(
        zones, aof_deg, H_B, POSTURE, drag_lam_grid, m_grid, DELTA_DEG, xg, yg,
    )

    aof = np.radians(aof_deg)
    delta = np.radians(DELTA_DEG)
    zone_list = [("ogive", zones.ogive), ("cylinder", zones.cylinder),
                 ("boattail", zones.boattail), ("base", zones.base)]

    rho = np.zeros_like(xg)
    ap_min = np.inf
    for name, z in zone_list:
        N_z = by_zone[name]
        if not np.any(N_z > 0.0):
            continue
        theta_z = np.radians(z.spray_deg)
        z_rep, lit = _belt_column_zrep_vec(
            xg, yg, H_B, aof, delta, [float(np.cos(theta_z))], 0.0, POSTURE.h,
            x_axis=xg,
        )
        dz = z_rep - H_B
        s_z = np.sqrt(xg**2 + yg**2 + dz**2)
        gamma = np.arcsin(np.clip((H_B - z_rep) / np.where(s_z > 0, s_z, 1.0), -1.0, 1.0))
        Ap = (np.full_like(gamma, presented_area(0.0, POSTURE)) if flat_Ap
              else np.asarray(presented_area(gamma, POSTURE)))
        use = lit & (N_z > 0.0)
        if not np.any(use):
            continue
        ap_min = min(ap_min, float(Ap[use].min()))
        rho[use] += N_z[use] / Ap[use]
    return rho, ap_min


def b_model_familyA(zones, drag, rho_steel, r_ft, aof_deg, n_phi=N_PHI):
    """Azimuthally-averaged Family A B_model(r) [ft^-2] at ground range r_ft [ft].

    Ring points are evaluated directly by `_four_zone_familyA_eval` (which takes
    arbitrary ground columns), so no grid interpolation enters -- unlike the
    Family B checks, which read a 121x121 field grid.
    """
    m_grid = np.logspace(-6, np.log10(0.5), N_MASS)
    lam = retardation_coeff(m_grid, drag, rho_steel)
    r_m = r_ft * FT_TO_M
    phis = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    xg = r_m * np.cos(phis)
    yg = r_m * np.sin(phis)
    rho, ap_min = rho_L_familyA(zones, aof_deg, lam, m_grid, xg, yg)
    return rho.mean() * FT_TO_M**2, ap_min  # m^-2 -> ft^-2


def in_band(x, lo=0.5, hi=2.0):
    return lo <= x <= hi


if __name__ == "__main__":
    drag = DragParams()
    print(f"drag: C_D={drag.C_D}, C_shape={drag.C_shape:.4f}, "
          f"combined={drag.C_D * drag.C_shape:.4f}")
    print(f"posture={POSTURE}, h_b={H_B} m, delta={DELTA_DEG} deg, "
          f"primary AoF={AOF_PRIMARY_DEG} deg, AoF sweep={AOF_SWEEP_DEG} deg\n")

    summary = []
    ap_floor = np.inf
    for shell_name, caliber in CALIBERS.items():
        modB = load_familyB(caliber)
        shell = SHELLS[shell_name]
        zones = compute_shell_zones(shell)
        rho_steel = shell.steel.rho

        print(f"=== {shell_name} ===")
        print(f"{'r (ft)':>8} {'B_A':>11} {'B_B':>11} {'B_card':>10} "
              f"{'A/card':>9} {'B/card':>9} {'A/B':>9} {'A band (AoF)':>26}")
        rA, rB, rAB = [], [], []
        for r_ft, b_card in zip(modB.CARD_R_FT, modB.CARD_B):
            b_a, ap_min = b_model_familyA(zones, drag, rho_steel, r_ft, AOF_PRIMARY_DEG)
            ap_floor = min(ap_floor, ap_min)
            b_b = modB.b_model_at_range(zones, drag, rho_steel, r_ft, AOF_PRIMARY_DEG)
            band = [b_model_familyA(zones, drag, rho_steel, r_ft, aof)[0]
                    for aof in AOF_SWEEP_DEG]
            rA.append(b_a / b_card)
            rB.append(b_b / b_card)
            rAB.append(b_a / b_b if b_b > 0 else float("inf"))
            print(f"{r_ft:8.0f} {b_a:11.4g} {b_b:11.4g} {b_card:10.4g} "
                  f"{rA[-1]:9.3g} {rB[-1]:9.3g} {rAB[-1]:9.3g} "
                  f"{'[%.4g, %.4g]' % (min(band), max(band)):>26}")

        mono_A = bool(np.all(np.diff(np.array(rA) * np.array(modB.CARD_B)) <= 1e-15))
        n_in_A = sum(in_band(x) for x in rA)
        n_in_AB = sum(in_band(x) for x in rAB)
        print(f"  Family A / card : {min(rA):.2f}x - {max(rA):.2f}x, "
              f"{n_in_A}/{len(rA)} in [0.5, 2]")
        print(f"  Family B / card : {min(rB):.2f}x - {max(rB):.2f}x, "
              f"{sum(in_band(x) for x in rB)}/{len(rB)} in [0.5, 2]")
        print(f"  Family A / B    : {min(rAB):.2f}x - {max(rAB):.2f}x, "
              f"{n_in_AB}/{len(rAB)} in [0.5, 2]")
        print(f"  Family A B(r) monotone non-increasing: {mono_A}\n")
        summary.append((shell_name, rA, rB, rAB, mono_A))

    print("=== Summary ===")
    print(f"{'shell':>16} {'A/card':>18} {'B/card':>18} {'A/B':>18} {'A mono':>8}")
    for shell_name, rA, rB, rAB, mono_A in summary:
        print(f"{shell_name:>16} {min(rA):7.2f}x -{max(rA):8.2f}x "
              f"{min(rB):7.2f}x -{max(rB):8.2f}x "
              f"{min(rAB):7.2f}x -{max(rAB):8.2f}x {str(mono_A):>8}")
    print(f"\nsmallest A_p encountered across all divisions: {ap_floor:.4f} m^2 "
          f"(A_p(0) = {presented_area(0.0, POSTURE):.4f} m^2; a value near zero "
          f"would make the division ill-conditioned)")
