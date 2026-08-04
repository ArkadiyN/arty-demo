"""Establish which interleaved column of each 1944 Ordnance table-pair is CASUALTIES.

Consumer: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
(section "The discriminator") — every provenance verdict in that ledger rests on
the numbers this script prints.

The scan interleaves two tables row-by-row (CASUALTIES and PERFORATION OF
1/8-IN. MILD STEEL). Column identity is *not* locally derivable from layout: the
two caption lines and the two TABLE numbers appear in opposite order, both
columns are monotone in r/N/B, and neither range grid is labelled. The one
discriminator internal to the table is the source's own stated definition of the
casualties criterion — each row lists the *lightest effective fragment* (m, v),
so KE = 1/2 m v^2 must reproduce the caption's stated 58 ft-lb threshold on
every row of the casualties column and only there.

This is the same closure declared in `.claude/rules/source-data-fidelity.md` and
run mechanically by `src/utils/check-table-invariants.py`; it is reproduced here
standalone so the audit's central claim is auditable without the re-transcribed
CSVs (which land in Phase 1).

Data is transcribed from
`doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage/ordnance-1944.md`,
anchors `# 75-MM H.E. SHELL, M48`, `# 105-MM H.E. SHELL,'Ml`, `# 155-MM N.E.
SHELL, M107`. Within each shell block the rows pair up: the FIRST line of each
pair is one column, the SECOND line the other. That first/second split -- not
any caption -- is what this script tests.

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/column-identity-energy-closure.py
"""

# 1 oz = 1 / (16 * 32.174) slug; KE in ft-lb with v in ft/s.
OZ_PER_SLUG = 16 * 32.174
CRITERION_FTLB = 58.0  # stated in each table's caption block

# (r ft, N, B per sq ft, m oz, v f/s), first line of each printed row-pair.
FIRST_LINE = {
    "75mm M48": [
        (20, 1070, 0.213, 0.014, 2060),
        (30, 920, 0.0809, 0.018, 1820),
        (40, 750, 0.0375, 0.024, 1570),
        (60, 640, 0.0141, 0.037, 1270),
        (80, 510, 0.0064, 0.051, 1080),
        (100, 450, 0.0036, 0.063, 972),
        (150, 370, 0.0013, 0.090, 813),
        (200, 320, 0.0006, 0.116, 716),
        (300, 250, 0.0002, 0.173, 587),
        (400, 200, 0.0001, 0.244, 494),
    ],
    "105mm M1": [
        (20, 1160, 0.231, 0.010, 2440),
        (30, 1115, 0.0986, 0.014, 2060),
        (40, 1072, 0.0533, 0.019, 1770),
        (60, 996, 0.0220, 0.030, 1410),
        (80, 932, 0.0116, 0.043, 1180),
        (100, 875, 0.0070, 0.055, 1040),
        (150, 745, 0.0026, 0.083, 846),
        (200, 642, 0.0013, 0.109, 738),
        (300, 513, 0.0004, 0.166, 598),
        (400, 433, 0.0002, 0.232, 507),
        (500, 358, 0.0001, 0.312, 438),
    ],
    "155mm M107": [
        (20, 1460, 0.291, 0.010, 2440),
        (30, 1400, 0.124, 0.014, 2060),
        (40, 1360, 0.0676, 0.019, 1770),
        (60, 1280, 0.0283, 0.030, 1410),
        (80, 1190, 0.0148, 0.043, 1180),  # scan prints "..0148" (stray dot)
        (100, 1130, 0.0090, 0.055, 1040),
        (150, 990, 0.0034, 0.083, 846),
        (200, 900, 0.0018, 0.109, 738),
        (300, 767, 0.0007, 0.161, 598),
        (400, 669, 0.0003, 0.233, 505),
        (600, 540, 0.0001, 0.402, 383),
    ],
}

# Second line of each printed row-pair.
SECOND_LINE = {
    "75mm M48": [
        (20, 534, 0.106, 0.049, 2390),
        (30, 442, 0.0391, 0.065, 2180),
        (40, 386, 0.0192, 0.082, 2010),
        (60, 300, 0.0066, 0.127, 1790),
        (80, 242, 0.0030, 0.185, 1580),
        (100, 197, 0.0016, 0.253, 1430),
        (130, 132, 0.0006, 0.375, 1270),
        (160, 86, 0.0003, 0.508, 1160),
        (190, 57, 0.0001, 0.655, 1080),
        (225, 39, 0.0001, 0.820, 1020),
    ],
    "105mm M1": [
        (20, 975, 0.194, 0.035, 2700),
        (30, 923, 0.0816, 0.047, 2430),
        (40, 853, 0.0424, 0.061, 2220),
        (60, 700, 0.0155, 0.095, 1920),
        (80, 570, 0.0071, 0.137, 1750),
        (100, 470, 0.0037, 0.192, 1550),
        (120, 403, 0.0022, 0.255, 1420),
        (140, 341, 0.0014, 0.326, 1320),
        (170, 262, 0.0007, 0.448, 1200),
        (200, 210, 0.0004, 0.580, 1120),
        (300, 88, 0.0001, 1.05, 955),
    ],
    "155mm M107": [
        (20, 1240, 0.247, 0.035, 2700),
        (30, 1170, 0.104, 0.047, 2430),
        (40, 1100, 0.0547, 0.061, 2220),
        (60, 945, 0.0209, 0.095, 1920),
        (80, 820, 0.0102, 0.137, 1750),
        (100, 717, 0.0057, 0.192, 1550),
        (120, 648, 0.0036, 0.255, 1420),
        (140, 592, 0.0024, 0.326, 1320),
        (170, 513, 0.0014, 0.448, 1200),
        (200, 440, 0.0009, 0.580, 1120),
        (300, 265, 0.0002, 1.05, 955),
        (400, 111, 0.0001, 1.61, 856),
    ],
}


def ke_ftlb(m_oz, v_fps):
    return 0.5 * (m_oz / OZ_PER_SLUG) * v_fps**2


def report(shell, label, rows):
    kes = [ke_ftlb(m, v) for _, _, _, m, v in rows]
    lo, hi = min(kes), max(kes)
    closes = all(abs(k - CRITERION_FTLB) <= 0.05 * CRITERION_FTLB for k in kes)
    verdict = "CASUALTIES" if closes else "not casualties"
    print(f"  {label:12s} r={rows[0][0]}-{rows[-1][0]:>3} ft  "
          f"B(20)={rows[0][2]:<6}  KE {lo:7.1f}-{hi:7.1f} ft-lb   -> {verdict}")
    return closes


def main():
    print(f"Closure: KE = 1/2 m v^2 must equal the caption's {CRITERION_FTLB:g} ft-lb "
          f"casualty criterion (+/-5%) on every row.\n")
    for shell in FIRST_LINE:
        print(shell)
        first = report(shell, "first line", FIRST_LINE[shell])
        second = report(shell, "second line", SECOND_LINE[shell])
        if first == second:
            print("    AMBIGUOUS -- closure does not discriminate for this shell")
        print()

    print("Discriminators that do NOT work, and why:")
    print("  * max range        -- casualties runs to 400/500/600 ft, perforation to")
    print("                        225/300/400 ft. Nothing in the scan says which is")
    print("                        which; b-vs-range-75mm.py asserted the opposite.")
    print("  * B non-increasing -- true of BOTH columns at every row, all three shells.")
    print("  * caption order    -- TABLE numbers print in reverse order relative to the")
    print("                        CASUALTIES / PERFORATION caption lines.")


if __name__ == "__main__":
    main()
