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
        # mass_deductions: fuze+booster. Authorized fuzes (TM-9-1904 p.481/
        # printed p.473): M48 or M54 w/ M20 or M20A1 Booster. TM-9-1901 sources
        # fuze-only weight (M48/M54 = 1.41-1.42 lb = 0.640-0.644 kg); M20/M20A1
        # booster weight is NOT tabulated in TM-9-1901. Value bracketed by
        # fuze-only (0.640 kg) and fuze+M21A2-booster-analog (2.15 lb = 0.975
        # kg, a stand-in for the unsourced M20/M20A1); materiality confirmed
        # <=0.2% N0 shift across this range — see
        # experiment/fragmentation-field/challenges/fuze-mass-deductions-range/materiality.md
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
        # mass_deductions: fuze+booster+rotating band+base plug (estimate).
        # Authorized fuzes (TM-9-1904 p.529/printed p.521): P.D. M51 w/ M21
        # Booster or M51A1 w/ M21A1 Booster. TM-9-1901 only tabulates the
        # superseding pair M51A3 w/ M21A2 = 2.15 lb = 0.975 kg (fuze+booster
        # only, no band/plug); M51/M21 and M51A1/M21A1 weights are not
        # directly sourced (expected close by within-family analogy, see
        # doc-reference/ww2-shells/tm-9-1901-artillery-ammunition/card.md).
        # Materiality confirmed <=0.2% N0 shift across the sourced range —
        # see experiment/fragmentation-field/challenges/fuze-mass-deductions-range/materiality.md
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
    "60mm M49A2 HE": ShellParams(
        caliber=0.0599948,        # 2.362" max body OD
        wall_t=0.007112,          # 0.280" min wall (drawing spec)
        mass_total=1.043262,      # 2.30 lb = 2.01 lb body + 0.29 lb fuze
        mass_filler=0.154221,     # 0.34 lb flake TNT
        mass_deductions=0.131542, # 0.29 lb fuze only (no rotating band)
        filler=FILLERS["TNT"],
        steel=STEELS["US WW2 WDSS1"],
        # Tail fin assembly (0.43 lb) excluded from mass_total — separate
        # steel grade, doesn't fragment with the body (Ammunition Series 6
        # Table 6-1, 17 Feb 1953).
        # NOTE: stated "fused projectile" weight (2.96 lb) exceeds
        # body+fuze+fins (2.01+0.29+0.43=2.73 lb) by 0.23 lb — unexplained
        # (possibly rounding in source table); not chased down.
        cylinder_len=0.023876,       # 0.94"
        ogive_len=0.019050,          # 1.69" - 0.94" (cyl+ogive - cyl)
        ogive_inner_R=0.014224,      # 0.56" R
        ogive_tip_dia=0.048514,      # 1.91" flat-front width
        boattail_len=0.097206,       # 5.517" - 1.69" (total excl. base plate - cyl+ogive)
        boattail_inner_dia=0.029464, # 0.58" R -> 1.16" dia
        base_thickness=0.014732,     # 0.58"
        has_boattail=True,
        base_treatment="mott",       # matches catalog convention; base plate small
        # --- KNOWN GAP: zone-geometry schema mismatch (unresolved) ---
        # Outer ogive is a STRAIGHT taper with a flat front, not a curved
        # arc — doesn't fit Tier-1 (ogive_outer_R arc) or Tier-2 (ogive_crh
        # tangent-ogive curve). Inner cavity wall IS curved (ogive_inner_R
        # above, 0.56" R) — straight-outer/curved-inner, not symmetric.
        # Boattail is two large-radius curves (outer 15.605" R = 0.396367 m,
        # inner 11.30" R = 0.287020 m, over the 3.827"/0.097206 m
        # boattail_len above) visually close to straight but not
        # measured/derived as a taper angle.
        # Full cross-section drawing: /mnt/f/Projects/TMP/img/m49_shape.png
        # — also shows an uncaptured fin-boom joint at the tail (15° angle
        # callout, "6.4 REFERENCE" dim, and "1.13±.06"/"1.04±.02" dims whose
        # exact referents weren't legible from the crop).
        # ogive_outer_R and ogive_crh are left unset and boattail_angle_deg
        # is left at its 0.0 default ON PURPOSE — filling ogive_crh would
        # silently invoke CRH_DEFAULT_TIER2=6.0 (a curved-ogive assumption
        # this shell doesn't have), and boattail_angle_deg=0.0 reads as "no
        # taper" despite a real tapered section. Zone/spray-angle geometry
        # for this shell is therefore NOT physically meaningful yet — needs
        # a modeler pass to add straight-cone ogive + curve-to-angle
        # boattail schema support before use in fragmentation-zone output.
        # Mass/Gurney-velocity fields above are unaffected by this gap.
    ),
}
