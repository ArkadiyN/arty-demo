from arty.fragmentation import FILLERS, STEELS, ShellParams

SHELLS: dict[str, ShellParams] = {
    "105mm M1 HE": ShellParams(
        caliber=0.105,
        wall_t=0.009208,      # 0.3625" min wall from M60 smoke drawing (shared body)
        mass_total=14.97,     # 33 lb complete with fuze
        mass_filler=2.18,     # cast TNT
        mass_deductions=0.75,
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
    ),
    "155mm M107 HE": ShellParams(
        caliber=0.155,
        wall_t=0.01429,       # 0.5625" min wall from manufacturing drawing
        mass_total=43.09,     # 95 lb complete with fuze (1943 spec)
        mass_filler=6.863,    # 15.13 lb cast TNT (1943 spec)
        mass_deductions=1.5,  # fuze + rotating band + base plug (estimate)
        filler=FILLERS["TNT"],
        steel=STEELS["WW2 US HE Shell"],
    ),
}
