"""Closure checks on Tolch (1938) spray-density tables, and resolution of the
cumulative base-fragment velocity distribution the card flags "UNVERIFIED".

Consumer: `experiment/fragmentation-field/challenges/source-data-audit/ledger.md`
section 4, and the Phase-2 rewrite of
`doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/card.md`.

Two invariants, both read off the report's own stated definitions -- no physics
is introduced here.

CHECK 1 -- additive closure. Of the "Total hits per unit solid angle" tables the
report says: "The average number of perforations, penetrations, and dents per
unit solid angle for the nose spray were added together" (anchor: `**Total
number of hits in the nose spray per unit solid angle.**`). So for every
(velocity, panel) cell the total must equal the sum of its three component rows.

CHECK 2 -- the velocity distribution. The card records two irreconcilable
extractions of one narrative sentence and rules the figure uncitable. But the
report states the sentence is *derived*, not measured: "The proportion of base
fragments remaining after giving the shell an increment in velocity may be
obtained from the above table" (anchor: `**Total hits per unit solid angle of
the base spray.**`). That makes it recomputable from the Panel A totals column,
which settles which extraction is right without a better scan.

Run: uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/tolch-spray-table-closure.py
"""

# Anchor: **Number of perforations, penetrations, and dents of the base spray
# per unit solid angle.**  -- (velocity -> per-panel value), panels A, B, C.
BASE_COMPONENTS = {
    "Perf.": {
        "Static": (1.62, 1.93, 1.48),
        "700": (1.51, 0.75, 0.77),
        "1085": (0.87, 0.17, 0.24),
        "1450": (0.24, 0.24, 0.12),
        "1685": (0.34, 0.34, 0.12),
        "2130": (0.0, 0.0, 0.04),
    },
    "Penet.": {
        "Static": (1.59, 2.76, 1.49),
        "700": (1.38, 0.96, 1.06),
        "1085": (1.89, 0.34, 0.53),
        "1450": (1.22, 0.50, None),
        "1685": (0.78, 0.57, 0.40),
        "2130": (0.50, 0.71, 0.12),
    },
    "Dents": {
        "Static": (6.30, 2.76, 0.96),
        "700": (4.86, 1.49, 0.21),
        "1085": (1.90, 0.27, 0.08),
        "1450": (1.26, 0.31, None),
        "1685": (0.31, 0.62, 0.08),
        "2130": (0.20, 0.41, 0.0),
    },
}

# Anchor: **Total hits per unit solid angle of the base spray.**
BASE_TOTALS = {
    "Static": (9.71, 7.45, 3.93),
    "700": (7.75, 3.20, 2.06),
    "1085": (4.66, 0.78, 0.65),
    "1450": (2.79, 1.50, None),
    "1685": (1.35, 1.37, 0.60),
    "2130": (0.70, 3.12, 0.16),
}

# Anchor: **Number of perforations, penetrations, and dents of the nose spray
# per unit solid angle.**
NOSE_COMPONENTS = {
    "Perf.": {
        "Static": (0.37, 0.10, 0.55),
        "700": (0.30, 0.68, 0.52),
        "1085": (0.53, 1.14, 1.11),
        "1450": (1.92, 1.36, 1.57),
        "1685": (1.66, 1.47, 1.57),
        "2130": (1.68, 2.66, 1.76),
    },
    "Penet.": {
        "Static": (0.37, 0.55, 2.39),
        "700": (2.08, 3.31, 2.31),
        "1085": (5.02, 5.39, 2.62),
        "1450": (6.60, 7.20, 2.69),
        "1685": (5.85, 8.00, 0.36),
        "2130": (5.17, 8.00, 3.32),
    },
    "Dents": {
        "Static": (1.22, 1.67, 2.34),
        "700": (9.94, 2.77, 1.20),
        "1085": (13.28, 11.16, 2.62),
        "1450": (11.50, 7.40, None),
        "1685": (12.18, 10.57, 6.29),
        "2130": (14.80, 15.45, 4.35),
    },
}

# Anchor: **Total number of hits in the nose spray per unit solid angle.**
NOSE_TOTALS = {
    "Static": (16.09, 2.42, 5.08),
    "700": (12.12, 11.96, 2.72),
    "1085": (16.89, 17.69, 6.35),
    "1450": (20.02, 13.62, None),
    "1685": (19.58, 19.24, 10.55),
    "2130": (21.45, 26.31, 9.43),
}

VELOCITIES = ["Static", "700", "1085", "1450", "1685", "2130"]
PANELS = ["A", "B", "C"]
TOL = 0.02  # the tables print 2 d.p.; allow rounding of three summed terms


def check_additive(name, components, totals):
    """total(v, panel) == perf + penet + dents, per the report's own wording."""
    print(f"\n{name}: total == perforations + penetrations + dents")
    bad = 0
    for v in VELOCITIES:
        for i, panel in enumerate(PANELS):
            parts = [components[t][v][i] for t in ("Perf.", "Penet.", "Dents")]
            stated = totals[v][i]
            if stated is None or any(p is None for p in parts):
                continue
            summed = sum(parts)
            delta = summed - stated
            flag = "" if abs(delta) <= TOL else "   <-- FAILS"
            if flag:
                bad += 1
                print(f"  v={v:>6} Panel {panel}: "
                      f"{parts[0]:.2f}+{parts[1]:.2f}+{parts[2]:.2f} = {summed:6.2f}  "
                      f"stated {stated:6.2f}  delta {delta:+.2f}{flag}")
    print(f"  -> {bad} cell(s) do not close.")
    return bad


def check_velocity_distribution():
    """The narrative fractions are the Panel A base-spray totals over static."""
    print("\nBase-fragment cumulative velocity distribution (Panel A totals / static):")
    static = BASE_TOTALS["Static"][0]
    derived = {}
    for v in VELOCITIES[1:]:
        derived[v] = 100.0 * BASE_TOTALS[v][0] / static

    # The two readings the card records as irreconcilable.
    heuristic = {"700": 80, "1085": 48, "1450": 29, "1685": 14, "2130": 7}
    vision = {"700": 20, "1085": 15, "1450": 25, "1685": 18, "2130": 7}

    print(f"  {'v (f/s)':>8} {'derived':>9} {'heuristic':>10} {'vision':>8}")
    for v in VELOCITIES[1:]:
        print(f"  {v:>8} {derived[v]:8.1f}% {heuristic[v]:9}% {vision[v]:7}%")

    h_err = max(abs(derived[v] - heuristic[v]) for v in heuristic)
    v_err = max(abs(derived[v] - vision[v]) for v in vision)
    print(f"\n  max deviation from derived: heuristic {h_err:.1f} pp, vision {v_err:.1f} pp")
    print("  -> The heuristic reading reproduces the table to rounding; the vision")
    print("     reading does not. The figure is RESOLVED without a better scan:")
    print("     80% > 700, 48% > 1085, 29% > 1450, 14% > 1685, 7% > 2130 f/s.")
    print("  Caveat: these are *shell* remaining velocities. The quantity is the")
    print("  fraction of base fragments whose charge-imparted velocity exceeds the")
    print("  shell velocity that cancels it -- burst geometry, not fragment drag.")


def main():
    bad = check_additive("Base spray", BASE_COMPONENTS, BASE_TOTALS)
    bad += check_additive("Nose spray", NOSE_COMPONENTS, NOSE_TOTALS)
    check_velocity_distribution()
    print(f"\n{bad} non-closing cell(s) total -- these are OCR defects in the")
    print("component tables or the totals, and must be resolved before either")
    print("table's numbers are cited.")


if __name__ == "__main__":
    main()
