from arty.fragmentation import FILLERS, STEELS, ShellParams

# ---------------------------------------------------------------------------
# Shell registry — fully populated ShellParams instances.
#
# Tier-1 shells (M1, M107) carry full drawing-derived zone arc geometry so
# that `compute_shell_zones` integrates real annular volumes per zone.
# Tier-2 shells (M48) omit zone arc fields; `compute_shell_zones` falls back
# to fixed mass fractions plus a CRH-based tangent-ogive spray angle.
# ---------------------------------------------------------------------------

SHELLS: dict[str, ShellParams] = {
    "105mm M1 HE": ShellParams(
        caliber=0.105,
        wall_t=0.009208,        # 0.3625" min wall from M60 smoke drawing (shared body)
        mass_total=14.97,       # 33 lb complete with fuze
        mass_filler=2.18,       # cast TNT
        mass_deductions=0.75,
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
        # Tier-1 zone arc geometry (US Army drawing)
        ogive_outer_R=0.6477,        # 25.5"
        ogive_inner_R=0.4572,        # 18"
        ogive_len=0.14681,           # 5.78"
        ogive_tip_dia=0.07315,       # 2.88"
        cylinder_len=0.15735,        # 6.195"
        boattail_len=0.05156,        # 2.03"
        boattail_angle_deg=9.267,    # FULL included taper angle (drawing)
        boattail_inner_dia=0.06350,  # 2.5" approx
        base_thickness=0.017653,     # 0.695"
        has_boattail=True,
        base_treatment="mott",
    ),
    "155mm M107 HE": ShellParams(
        caliber=0.155,
        wall_t=0.014288,        # 0.5625" min wall from manufacturing drawing
        mass_total=43.09,       # 95 lb complete with fuze (1943 spec)
        mass_filler=6.863,      # 15.13 lb cast TNT (1943 spec)
        mass_deductions=1.5,    # fuze + rotating band + base plug (estimate)
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
        # Tier-1 zone arc geometry (US Army drawing — secant ogive)
        ogive_outer_R=1.66294,       # 65.47"
        ogive_inner_R=1.09220,       # 43"
        ogive_len=0.30937,           # 12.18"
        ogive_tip_dia=0.060452,      # 2.38"
        cylinder_len=0.18720,        # 7.37"
        boattail_len=0.06934,        # 2.73"
        boattail_angle_deg=8.0,      # FULL included taper angle
        boattail_inner_dia=0.081026, # 3.19"
        base_thickness=0.036576,     # 1.44"
        has_boattail=True,
        base_treatment="mott",
    ),
    "75mm M48 HE": ShellParams(
        caliber=0.075,
        wall_t=0.006,                # estimate; caliber-scaled from M1 (needs confirmation)
        mass_total=6.622,            # 14.6 lb complete with M48 PD fuze
        mass_filler=0.6668,          # 1.47 lb cast TNT
        mass_deductions=0.200,       # M48 PD fuze placeholder (TM 43-0001-28)
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
        # Tier-2: inner-arc radius unknown; outer geometry from Handbook of
        # Ballistic and Engineering Data for Ammunition Vol.1 (1930).
        # Secant ogive: arc R=7.43 cal but only 1.18 cal used — shell looks
        # blunt because it's a short section of a large-radius arc.
        ogive_crh=7.43,              # 7.43 cal radius (handbook)
        ogive_len=0.08850,           # 1.18 cal (handbook); drives secant spray angle
        cylinder_len=0.15900,        # 2.12 cal (handbook)
        boattail_angle_deg=9.0,      # 9° full taper (handbook)
        boattail_len=0.03675,        # 0.49 cal (handbook)
        has_boattail=True,
        base_treatment="mott",
    ),
}
