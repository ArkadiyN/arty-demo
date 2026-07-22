# Project Memory Index

- [Four-zone field geometry](project_four_zone_field_geometry.md) — a missing ground lobe is usually correct geometry (check v_gz sign), not a bug
- [False ogive vs structural ogive](concept_false_ogive_vs_structural_ogive.md) — a windshield/false nose is inert; only the mass bookkeeping needs checking
- [Fragmentation-field structure](frag_field_structure.md) — code map for the 3D field paths; the spreading factor is inlined with the target-coupled factors
- [Shell-axis sign convention](gotcha_shell_axis_sign_convention.md) — legacy single-zone axis is a backward x-mirror sign error; forward axis is correct (mirror hides at x=0 / AoF=90°)
- [Posture vs intercept axis](concept_posture_vs_intercept_axis.md) — the A_p posture toggle and the target-column intercept are independent mechanisms
- [Belt-gate quadrature endpoint](gotcha_belt_gate_quadrature_endpoint.md) — integrate belt-gated kernels with midpoint nodes, never endpoint trapezoid; verify on a dense sweep
- [Hard-step fraction grid aliasing](gotcha_hard_step_fraction_grid_aliasing.md) — threshold-crossing stats over a hard step alias on coarse grids; use a dense grid or the onset radius
- [P_k volume bimodal only single-zone](gotcha_pkill_volume_bimodal_no_penumbra.md) — single-zone volume P_k is bimodal; four-zone has a real graded fringe
- [m_min table must stay per-layer](gotcha_mmin_table_perlayer.md) — don't share the m_min table across z-layers (breaks exact z0-matches-field tests); vectorize the bisection instead
- [P(kill) columns padded-segment bounds](gotcha_pkill_columns_padded_segment_bounds.md) — _pkill_columns_vec pads collapsed segments to z=h_b; bounds-check only weighted samples or it false-fires
