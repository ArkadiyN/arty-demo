"""Produces every number in ../derivation.md (UFC 4-023-07 Eq. 5-1 -> E_thr(m)).

Runs the validation checks that scoping.md's "Validation checks the derivation
pass must run" section specifies: (1) closure on small-arms / Sanborn-sphere
forward cases, (2) monotonicity and limits of E_thr(m), (3) bracketing of the
two non-fitted Tolch probes (78.6 J, 126 J).

Run from the repo root:  uv run python \
  experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/checks/ufc-5-1-perforation-threshold.py
"""

import csv
import math
import pathlib

# --- UFC 4-023-07 Eq. 5-1, verified against source.pdf p.40 (printed 5-9) ---
#   T_w = 9837 * v^0.4113 * w^1.4897 / ( rho * (pi D^2 / 4)^1.3596 * H^0.5414 )
# T_w [in], v [ft/s], w [lb], D [in], rho [lb/ft^3], H [lb Janka-scale]
C_UFC = 9837.0
A_V = 0.4113
A_W = 1.4897
A_A = 1.3596
A_H = 0.5414

IN_PER_M = 39.3701
FT_PER_M = 3.28084
LB_PER_KG = 2.2046226
RHO_STEEL = 7850.0  # kg/m^3

TABLE = (
    pathlib.Path(__file__).resolve().parents[4].parent
    / "doc-reference/fragmentation/ufc-4-023-07-direct-fire-weapons-effects"
    / "tables/table-5-5-wood-properties.csv"
)


def wood_props(species: str, condition: str) -> tuple[float, float]:
    """Return (rho [lb/ft^3], H [lb]) for a Table 5-5 row.

    The CSV headers were originally backwards (page image shows column 1 =
    Density, column 2 = Hardness, but the committed header row said the
    opposite); commit 10303e0 corrected the header labels in place, so the
    columns now read directly with no reversal.  See derivation.md section
    1.1 and review.md Finding 1 (this reader carried a stale double-swap
    after that fix, since corrected here).
    """
    with TABLE.open() as fh:
        for row in csv.DictReader(fh):
            if row["species"] == species and row["condition"] == condition:
                rho = float(row["density_lbs_per_ft3"])
                hardness = float(row["hardness_pounds"])
                return rho, hardness
    raise KeyError(f"{species}/{condition} not in {TABLE}")


def t_w(v_fps: float, w_lb: float, d_in: float, rho: float, hard: float) -> float:
    """Return UFC Eq. 5-1 perforation-limit thickness [in]."""
    area = math.pi * d_in**2 / 4.0
    return C_UFC * v_fps**A_V * w_lb**A_W / (rho * area**A_A * hard**A_H)


def v50_fps(t_in: float, w_lb: float, d_in: float, rho: float, hard: float) -> float:
    """Return the velocity [ft/s] at which Eq. 5-1 gives T_w = t_in (ballistic limit)."""
    area = math.pi * d_in**2 / 4.0
    return (t_in * rho * area**A_A * hard**A_H / (C_UFC * w_lb**A_W)) ** (1.0 / A_V)


def frag_diameter_m(m_kg: float) -> float:
    """Return sphere-equivalent diameter [m] of a compact steel fragment of mass m [kg]."""
    return (6.0 * m_kg / (math.pi * RHO_STEEL)) ** (1.0 / 3.0)


def e_thr_J(m_kg: float, t_in: float, rho: float, hard: float) -> float:
    """Return UFC-inverted perforation threshold energy [J] for fragment mass m [kg]."""
    d_in = frag_diameter_m(m_kg) * IN_PER_M
    v = v50_fps(t_in, m_kg * LB_PER_KG, d_in, rho, hard) / FT_PER_M  # m/s
    return 0.5 * m_kg * v**2


def main() -> None:
    rho_p, h_p = wood_props("Pine", "Dry")
    print(f"Table 5-5 Pine/Dry: rho = {rho_p} lb/ft3, H = {h_p} lb")

    # -- closure invariant on Table 5-5 itself (see derivation.md 1.1) --------
    with TABLE.open() as fh:
        rows = list(csv.DictReader(fh))
    ok_rho = ok_h = True
    for i in range(0, len(rows), 2):
        dry, wet = rows[i], rows[i + 1]
        # density_lbs_per_ft3: wet >= dry for all species
        ok_rho &= float(wet["density_lbs_per_ft3"]) >= float(dry["density_lbs_per_ft3"])
        # hardness_pounds: wet <= dry, hardwoods only (bar Pine/Balsa, softwoods)
        if dry["species"] not in ("Pine", "Balsa"):
            ok_h &= float(wet["hardness_pounds"]) <= float(dry["hardness_pounds"])
    print(f"  density non-decreasing dry->wet (all species): {ok_rho}")
    print(f"  hardness non-increasing dry->wet (hardwoods): {ok_h}")

    # -- check 1: forward closure on cases outside/inside calibration domain --
    print("\nCHECK 1 - forward T_w [in], dry pine unless noted")
    cases = [
        ("7.62x51 M80 ball", 2750.0, 147 / 7000.0, 0.308),
        (".50 BMG M33 ball", 2910.0, 647 / 7000.0, 0.510),
        ("Sanborn 12.7 mm sphere @ 762 m/s", 2500.0, 8.41e-3 * LB_PER_KG, 0.500),
    ]
    for name, v, w, d in cases:
        print(f"  {name:34s} T_w = {t_w(v, w, d, rho_p, h_p):8.1f} in")
    print("  (Sanborn CLT: 6.875 in 5-ply was perforated at this velocity ->")
    print("   Eq. 5-1 over-predicts required thickness by ~5x, as Sanborn states)")

    # -- check 2: monotonicity / limits of E_thr(m) --------------------------
    print("\nCHECK 2 - E_thr(m) through 1 in dry pine")
    print(f"  {'m [g]':>8} {'D [mm]':>8} {'v50 [m/s]':>11} {'E_thr [J]':>12}")
    masses_g = [0.05, 0.1, 0.63, 2.0, 10.0, 50.0]
    prev_v = prev_e = None
    v_falls = e_falls = True
    for mg in masses_g:
        m = mg * 1e-3
        d_in = frag_diameter_m(m) * IN_PER_M
        v = v50_fps(1.0, m * LB_PER_KG, d_in, rho_p, h_p) / FT_PER_M
        e = 0.5 * m * v**2
        print(f"  {mg:8.2f} {d_in * 25.4:8.2f} {v:11.3f} {e:12.3e}")
        if prev_v is not None and prev_e is not None:
            v_falls &= v < prev_v
            e_falls &= e < prev_e
        prev_v, prev_e = v, e
    # closed-form exponents: v50 ~ m^p, E_thr ~ m^(1+2p)
    p = (-A_W + 2 * A_A / 3.0) / A_V
    print(f"  closed form: v50 ~ m^{p:+.3f}, E_thr ~ m^{1 + 2 * p:+.3f}")
    print(f"  v50 falls with m: {v_falls};  E_thr falls with m: {e_falls}")
    print(f"  v50 -> inf as m -> 0: {v50_fps(1.0, 1e-9, frag_diameter_m(1e-9 / LB_PER_KG) * IN_PER_M, rho_p, h_p) > 1e6}")

    # -- check 3: bracket the two non-fitted probes --------------------------
    print("\nCHECK 3 - bracket the non-fitted probes (78.6 J, 126 J)")
    e063 = e_thr_J(0.63e-3, 1.0, rho_p, h_p)
    print(f"  E_thr(0.63 g) = {e063:.4g} J   vs 78.6 J -> ratio {e063 / 78.6:.2e}")
    print(f"                            vs 126  J -> ratio {e063 / 126.0:.2e}")
    print(f"  VERDICT: {'PASS' if 0.1 <= e063 / 78.6 <= 10 else 'FAIL (>1 decade)'}")

    # -- bias amplification: thickness bias^(1/A_V) in velocity --------------
    print("\nBias amplification of a thickness-bias factor b into v50 / E_thr")
    for b in (2.0, 5.0, 8.0):
        amp = b ** (1.0 / A_V)
        d_in = frag_diameter_m(0.63e-3) * IN_PER_M
        v = v50_fps(1.0, 0.63e-3 * LB_PER_KG, d_in, rho_p, h_p) / FT_PER_M * amp
        print(f"  b = {b:4.1f}x thickness -> {amp:8.1f}x velocity;"
              f" v50 = {v:7.1f} m/s, E_thr(0.63 g) = {0.5 * 0.63e-3 * v**2:8.2f} J")


if __name__ == "__main__":
    main()
