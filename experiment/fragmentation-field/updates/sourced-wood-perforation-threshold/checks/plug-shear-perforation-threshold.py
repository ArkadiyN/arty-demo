"""Numbers for derivation.md section 7 (Option A-double-prime, the plug-shear
wood-perforation threshold E_thr(m)).

Produces: the Sanborn Table 2 unit-conversion closure that makes the shear-
strength row admissible; the E_thr(m) table; the order-of-magnitude bracket
against the two mass-non-specific casualty-energy probes; the shear-vs-crush
term ratio that supersedes derivation.md section 6 eq. (7); and the forward
ballistic-limit check on Sanborn's own 6.875 in CLT panel.

Run: uv run python experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/checks/plug-shear-perforation-threshold.py
"""

import math

PSI_TO_PA = 6894.757
LBFT3_TO_KGM3 = 16.01846
LBF_TO_N = 4.448222
RHO_STEEL = 7850.0  # kg/m3
T_PANEL = 0.0254  # m, Tolch 1 in softwood panel
FT_LB = 1.3558179  # J

# --- Sanborn 2019 Table 2, as printed (source.md:87) -------------------------
# "Shear Strength Parallel to Grain, ASTM D143 ... 1,300 27% 14 / 1600 13% 19
#  psi (MPa) Section 14 (8.96) (11.0)"
TABLE2 = [
    # label, printed US value, printed SI value, converter
    ("density SPF-S    [lb/ft3->kg/m3]", 28.4, 455.0, LBFT3_TO_KGM3),
    ("density SYP      [lb/ft3->kg/m3]", 34.2, 548.0, LBFT3_TO_KGM3),
    ("shear || grain SPF-S [psi->MPa] ", 1300.0, 8.96, PSI_TO_PA / 1e6),
    ("shear || grain SYP   [psi->MPa] ", 1600.0, 11.0, PSI_TO_PA / 1e6),
    ("hardness SPF-S       [lbf->N]   ", 605.0, 2690.0, LBF_TO_N),
    ("hardness SYP         [lbf->N]   ", 656.0, 2920.0, LBF_TO_N),
    ("bond-line shear SPF-S[psi->MPa] ", 399.0, 2.75, PSI_TO_PA / 1e6),
    ("bond-line shear SYP  [psi->MPa] ", 880.0, 6.07, PSI_TO_PA / 1e6),
]

TAU_SPFS = 1300.0 * PSI_TO_PA  # Pa
TAU_SYP = 1600.0 * PSI_TO_PA  # Pa
COV_SPFS = 0.27  # Table 2, n = 14


def diameter(m_kg):
    """Sphere-equivalent diameter [m] of a compact steel fragment of mass [kg]."""
    return (6.0 * m_kg / (math.pi * RHO_STEEL)) ** (1.0 / 3.0)


def e_thr_shear(m_kg, tau_pa=TAU_SPFS, t=T_PANEL, eta=0.5):
    """Plug shear-out work [J] to perforate a panel of thickness t [m]."""
    return eta * tau_pa * math.pi * diameter(m_kg) * t * t


def e_thr_crush(m_kg, sigma_pa, t=T_PANEL):
    """Compaction work [J] of the wood column ahead of the fragment."""
    return sigma_pa * (math.pi / 4.0) * diameter(m_kg) ** 2 * t


def v50(m_kg, **kw):
    """Ballistic-limit velocity [m/s] implied by the plug-shear threshold."""
    return math.sqrt(2.0 * e_thr_shear(m_kg, **kw) / m_kg)


def main():
    print("=== 1. Sanborn Table 2 unit-conversion closure (admissibility) ===")
    worst = 0.0
    for label, us, si, k in TABLE2:
        got = us * k
        err = abs(got - si) / si
        worst = max(worst, err)
        print(f"  {label} {us:>8.1f} -> {got:>9.3f} vs printed {si:>8.2f}  ({err:+.2%})")
    print(f"  worst deviation {worst:.2%} -> {'PASS' if worst < 0.01 else 'FAIL'} (<1%)\n")

    # Janka-derived crush strength: mean pressure under the 11.28 mm ball at
    # half-diameter embedment, divided by the ~3x indentation constraint factor.
    d_janka = 0.444 * 0.0254
    a_janka = math.pi * (d_janka / 2.0) ** 2
    sigma_c = (605.0 * LBF_TO_N / a_janka) / 3.0
    print("=== 2. Shear vs crush mechanism (supersedes sec.6 eq.(7)) ===")
    print(f"  Janka mean pressure {605*LBF_TO_N/a_janka/1e6:.1f} MPa -> sigma_c ~ {sigma_c/1e6:.1f} MPa")
    for m_g in (0.1, 0.63, 2.0, 10.0):
        m = m_g / 1000.0
        es, ec = e_thr_shear(m), e_thr_crush(m, sigma_c)
        print(f"  m={m_g:>5.2f} g  D={diameter(m)*1e3:5.2f} mm  shear {es:7.2f} J"
              f"  crush {ec:6.2f} J  crush/shear {ec/es:.3f}")
    d_cross = 2.0 * TAU_SPFS * T_PANEL / sigma_c
    print(f"  crush = shear only at D = 2*tau*t/sigma_c = {d_cross*1e3:.0f} mm"
          f" -> shear dominates over the whole fragment range\n")

    print("=== 3. E_thr(m) and v50(m), SPF-S tau = 8.96 MPa, t = 1 in ===")
    print("   m [g]   D [mm]   v50 [m/s]   E_thr [J]")
    for m_g in (0.05, 0.10, 0.63, 2.0, 10.0, 50.0):
        m = m_g / 1000.0
        print(f"  {m_g:6.2f}  {diameter(m)*1e3:7.2f}  {v50(m):9.1f}  {e_thr_shear(m):9.3f}")
    ms = [0.05, 0.10, 0.63, 2.0, 10.0, 50.0]
    rising = all(e_thr_shear(b / 1000) > e_thr_shear(a / 1000) for a, b in zip(ms, ms[1:]))
    falling = all(v50(b / 1000) < v50(a / 1000) for a, b in zip(ms, ms[1:]))
    print(f"  E_thr rising in m: {rising};  v50 falling in m: {falling};"
          f"  v50 -> inf as m -> 0: {v50(1e-9) > v50(1e-6)}\n")

    print("=== 4. Order-of-magnitude bracket vs the two probes (0.63 g) ===")
    m_ref = 0.63e-3
    band = {
        "SPF-S tau, eta=0.5 (central)": e_thr_shear(m_ref),
        "SPF-S tau -1 sigma (COV 27%)": e_thr_shear(m_ref, tau_pa=TAU_SPFS * (1 - COV_SPFS)),
        "SPF-S tau +1 sigma (COV 27%)": e_thr_shear(m_ref, tau_pa=TAU_SPFS * (1 + COV_SPFS)),
        "SYP tau, eta=0.5":             e_thr_shear(m_ref, tau_pa=TAU_SYP),
        "SPF-S tau, eta=1.0 (upper)":   e_thr_shear(m_ref, eta=1.0),
    }
    for k, v in band.items():
        print(f"  {k:<30} {v:7.2f} J")
    lo, hi = min(band.values()), max(band.values())
    print(f"  defensible band {lo:.1f}-{hi:.1f} J")
    for name, probe in (("1944 Ordnance 58 ft-lb", 58.0 * FT_LB), ("Tolch hole-size", 126.0)):
        print(f"  vs {name:<24} {probe:6.1f} J -> central ratio {e_thr_shear(m_ref)/probe:.2f}"
              f"; in band: {lo <= probe <= hi}")
    print()

    print("=== 5. Forward check on Sanborn's own panel (independent of Tolch) ===")
    m_sph, d_sph, t_clt = 0.0084, 0.0127, 6.875 * 0.0254
    for tau, lab in ((TAU_SPFS, "SPF-S"), (TAU_SYP, "SYP")):
        e = 0.5 * tau * math.pi * d_sph * t_clt * t_clt
        print(f"  {lab}: E_thr = {e:7.0f} J -> v50 = {math.sqrt(2*e/m_sph):6.0f} m/s"
              f" ({math.sqrt(2*e/m_sph)*3.28084:.0f} ft/s)")
    print("  Sanborn shot envelope 180-1200 m/s, 59 of 122 perforating -> the")
    print("  true limit for the thickest panels lies inside that envelope.\n")

    print("=== 6. Sensitivity: E_thr is linear in tau (power 1) ===")
    for f in (0.5, 0.73, 1.0, 1.27, 2.0):
        print(f"  tau x {f:4.2f} -> E_thr(0.63 g) x {e_thr_shear(m_ref, tau_pa=TAU_SPFS*f)/e_thr_shear(m_ref):4.2f}")


if __name__ == "__main__":
    main()
