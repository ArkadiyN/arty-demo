from arty.fragmentation import ShellParams

SHELLS: dict[str, ShellParams] = {
    "105mm M1 HE": ShellParams(
        caliber=0.105,
        wall_t=0.011,
        mass_total=14.97,
        mass_charge=2.18,
        mass_deductions=0.75,
        gurney_const=2700.0,
        rho_steel=7850.0,
    ),
}
