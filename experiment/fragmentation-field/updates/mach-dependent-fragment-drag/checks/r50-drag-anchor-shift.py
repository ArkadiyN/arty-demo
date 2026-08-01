"""R50 shift caused by the DoD-1975 drag anchor (updates/mach-dependent-fragment-drag).

Produces the old/new R50 numbers quoted when re-banding
tests/test_fragmentation.py::test_r50_in_expected_range after the
DragParams C_D/C_shape change (derivation.md §6 item 4).
"""

from arty.fragmentation import DragParams, compute_frag_field

OLD = DragParams(C_D=0.65, C_shape=0.90)
NEW = DragParams()

for label, drag in (("old 0.585", OLD), ("new 2.674", NEW)):
    res = compute_frag_field(drag=drag)
    combined = drag.C_D * drag.C_shape
    print(f"{label:10s}  C_D*C_shape={combined:.4f}  R50={res.r50:.2f} m")
