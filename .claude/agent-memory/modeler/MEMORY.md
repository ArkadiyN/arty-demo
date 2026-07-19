# Project Memory Index

- [Four-zone field geometry](project_four_zone_field_geometry.md) — a missing ground lobe is usually correct geometry (check v_gz sign), not a bug
- [False ogive vs structural ogive](concept_false_ogive_vs_structural_ogive.md) — a windshield/false nose is inert; only the mass bookkeeping needs checking
- [Fragmentation-field structure](frag_field_structure.md) — code map for the 3D field paths; the spreading factor is inlined with the target-coupled factors
- [Shell-axis sign convention](gotcha_shell_axis_sign_convention.md) — single-zone vs four-zone e_axis differ; standardised by construction, never proven equivalent
- [Posture vs intercept axis](concept_posture_vs_intercept_axis.md) — the A_p posture toggle and the target-column intercept are independent mechanisms
- [Belt-gate quadrature endpoint](gotcha_belt_gate_quadrature_endpoint.md) — integrate belt-gated kernels with midpoint nodes, never endpoint trapezoid; verify on a dense sweep
- [Hard-step fraction grid aliasing](gotcha_hard_step_fraction_grid_aliasing.md) — threshold-crossing stats over a hard step alias on coarse grids; use a dense grid or the onset radius
- [P_k volume bimodal only single-zone](gotcha_pkill_volume_bimodal_no_penumbra.md) — single-zone volume P_k is bimodal; four-zone has a real graded fringe
