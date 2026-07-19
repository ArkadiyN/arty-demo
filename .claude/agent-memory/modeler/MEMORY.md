# Project Memory Index

- [Four-zone field geometry](project_four_zone_field_geometry.md) — a missing ground lobe is usually correct geometry (check v_gz sign), not a bug; pointer to derivation.md
- [False ogive vs structural ogive](concept_false_ogive_vs_structural_ogive.md) — a shell windshield/false nose is inert; not the model's frag-driving ogive zone; non-issue for lethality
- [Fragmentation-field structure](frag_field_structure.md) — where the single-zone vs four-zone 3D field code and target-coupled factors live, and the spreading-factor isolation gotcha
- [Posture vs intercept axis](concept_posture_vs_intercept_axis.md) — the standing/prone A_p toggle is a different axis than the z=0 intercept test; it does NOT fix the false safe zone
- [Belt-gate quadrature endpoint](gotcha_belt_gate_quadrature_endpoint.md) — integrate a belt-gated kernel piecewise with MIDPOINT nodes, never endpoint-trapezoid (edge node coin-flips gate to 0.0); verify on a dense sweep
- [Hard-step fraction grid aliasing](gotcha_hard_step_fraction_grid_aliasing.md) — a threshold-crossing cell-count over a hard step aliases on a coarse plot grid (PRONE false-safe "0%" was an n_grid coincidence); use a dense near-field grid or the onset radius
- [P_k volume bimodal only single-zone](gotcha_pkill_volume_bimodal_no_penumbra.md) — single-zone point-P_k is bimodal (no near-burst penumbra); four-zone has a real grid-stable graded near-burst fringe. Don't conflate. Bicone annulus head-lit lower = (h_b−1.7)/tanδ
