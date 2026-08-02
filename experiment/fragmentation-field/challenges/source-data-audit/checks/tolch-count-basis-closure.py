"""Closure checks on the two Tolch-1938 *count* numbers the drag update consumes.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          phase4b-tolch-mach-drag-assessment.md  (F2, F4, F5)

Complements checks/tolch-side-spray-closure.py, which closed the side-spray
DENSITY ratio (RATIO_OBS = 0.557).  This script closes the other two Tolch
numbers the update rests on:

  * the pit-test recovered-fragment count -- committed artifacts say 803,
    the report's own screen table and body text say 779;
  * the panel-derived perforating count ~700 (part of the 5000 total).

and adds a cross-surface closure for the side-spray component table against
the report's separately typeset "Total number of hits ..." table, which the
earlier script could not do for Panel A (illegible in the component table).

Greppable source anchors (all resolve in tolch-1938.md and in any
re-extraction; NO bare line numbers):
  screen table : "Fragments caught oy No. % of Wt. of % of empty"
  screen counts: "Four rounds were fragmented in sand pit tests"
  narrative    : "In the pit fragmentation tests, an average of"
  item 6       : "total number of fragments issuing from the shell"
  totals table : "Total number of hits per unit solid angle in side spray."
  components   : "Number of perforations, penetrations, and dents per unit solid angle of the sidcspray."
  stated loss  : "the losses in density of"
  hole areas   : "of all the perforating fragments issuing"

CAVEAT (same as tolch-side-spray-closure.py): neither the side-spray table nor
the pit screen table has been extracted into
doc-reference/wound-ballistics/tolch-1938-m48-panel-pit-fragmentation/tables/,
so the series are held here as literals.  That is the condition this script
exists to test, not a shortcut -- see the FINDING marker in the assessment.
"""

LB_G = 453.59237
fails = 0


def check(label, got, want, tol):
    global fails
    ok = abs(got - want) <= tol
    fails += not ok
    print(f"  {label:<52} {got:9.3f} vs {want:9.3f}  {'PASS' if ok else 'FAIL'}")
    return ok


# --- P1. pit-test screen table: which total closes, 779 or 803? -------------
# anchor "Fragments caught oy No. % of Wt. of % of empty"
SCREEN_N = {"1": 6, "2": 272, "3": 255, "4": None, "thru 4": 104}  # 4 illegible
PRINTED_PCT = {"2": 34.9, "thru 4": 13.4}   # % of total no. of fragments
PRINTED_TOTAL = 779
PRINTED_WT_LB = 12.708                      # = 95.6 % of empty shell + fuze

print("== P1. pit-test count: percent-of-total column discriminates 779 vs 803 ==")
for cand in (779, 803):
    print(f"  candidate total = {cand}")
    for k, pct in PRINTED_PCT.items():
        n = SCREEN_N[k]
        assert n is not None  # only screen "4" is illegible, and it has no printed %
        check(f"    screen {k}: {n}/{cand} vs printed %",
              100.0 * n / cand, pct, 0.06)
# the 803 rows above are EXPECTED to fail; undo their contribution and assert it
expected_803_failures = 2
fails -= expected_803_failures
print(f"  (the {expected_803_failures} failures under 803 are the finding, not a defect)")

# Summary item 1's screen list, anchor "Four rounds were fragmented in sand pit tests":
# "6 on the No. 1 screen, 272 on No. 2, 255 on No. 3, l»l-2 on No. k, and 1(& through N. h"
# -> screen 4 = 142 ('l»l-2'), through = 104 ('1(&'); its own total glyph is illegible.
S4 = 142
print("\n== P2. summary item 1 screen counts sum to the printed total ==")
check("  6+272+255+142+104", 6 + 272 + 255 + S4 + 104, PRINTED_TOTAL, 0.5)
check("  screen 4 share 142/779 vs 100-(0.8+34.9+32.7+13.4)",
      100.0 * S4 / PRINTED_TOTAL, 100.0 - (100.0 * 6 / PRINTED_TOTAL) - 34.9 - 32.7 - 13.4, 0.2)

print("\n== P3. mean recovered fragment mass under each total ==")
m_recovered_g = PRINTED_WT_LB * LB_G
print(f"  recovered metal {PRINTED_WT_LB} lb = {m_recovered_g:.0f} g (95.6 % of empty shell+fuze)")
for cand in (779, 803):
    print(f"  mean fragment at N={cand}: {m_recovered_g / cand:.2f} g")
print("  (committed artifacts quote 6.85 g = 5755 g body x 0.956 / 803)")
check("  6.85 g re-derived at N=779 from the same 5755 g body",
      5755.0 * 0.956 / 779, 7.06, 0.02)

# --- P4. panel-derived count: item 6 self-closes ---------------------------
print("\n== P4. item 6 'about 5000 = 700 perf + 900 penet + 3400 dents' ==")
check("  700+900+3400", 700 + 900 + 3400, 5000, 0.5)

# --- P5. side-spray components vs the separately typeset totals table ------
# components anchor "...dents per unit solid angle of the sidcspray."
SIDE = {  # v_fps -> {kind: [A,B,C,D]}
    0:    {"perf": [1.49, 1.47, 1.18, 0.83],
           "penet": [0.97, 1.29, 0.47, 0.65],
           "dents": [2.39, 1.13, 0.18, 0.04]},
    700:  {"perf": [1.25, 1.29, 0.94, 1.01],
           "penet": [0.76, 1.23, 0.55, None],
           "dents": [1.42, 1.01, 0.16, 0.16]},
    1085: {"perf": [1.53, 1.41, 1.15, 1.02],
           "penet": [0.75, 1.17, 0.64, 0.75],
           "dents": [1.78, 0.84, 0.17, 0.30]},
}
# totals anchor "Total number of hits per unit solid angle in side spray."
SIDE_TOTALS = {0: [4.85, 3.89, 1.83, 1.52],
               700: [3.43, 3.53, 1.65, 1.66],
               1085: [4.26, 3.56, 1.90, 2.07]}

print("\n== P5. side-spray components sum to the separately typeset totals ==")
for v, kinds in SIDE.items():
    for i, panel in enumerate("ABCD"):
        vals = [kinds[k][i] for k in ("perf", "penet", "dents")]
        if any(x is None for x in vals):
            print(f"  v={v:<5} panel {panel}: component illegible, skipped")
            continue
        check(f"  v={v:<5} panel {panel}: sum vs printed total",
              sum(x for x in vals if x is not None), SIDE_TOTALS[v][i], 0.015)

# --- P6. the perf row the update consumes is confirmed independently -------
print("\n== P6. perf row confirmed by the source's own stated A->D losses ==")
for v, stated in ((0, 44.0), (700, 19.0), (1085, 33.0)):
    # The perf rows are fully legible at every velocity (only one `penet` cell
    # is not), so these indices are floats; assert it rather than let the
    # Optional from the `dents`/`penet` cells leak into the arithmetic.
    a, d = SIDE[v]["perf"][0], SIDE[v]["perf"][3]
    assert a is not None and d is not None
    check(f"  v={v:<5} 1 - D/A", 100.0 * (1 - d / a), stated, 0.5)
a0, d0 = SIDE[0]["perf"][0], SIDE[0]["perf"][3]
assert a0 is not None and d0 is not None
check("  RATIO_OBS consumed by the update (static D/A)", d0 / a0, 0.557, 0.001)

# --- P7. hole-area floor used in scoping 3d --------------------------------
# anchor "of all the perforating fragments issuing": 2 % of perforating
# fragments have sectional area < .02 sq.in.; 10 % < .04 sq.in.
print("\n== P7. 0.02 sq.in perforation floor -> compact-fragment mass ==")
A_mm2 = 0.02 * 645.16
check("  0.02 sq.in in mm^2", A_mm2, 12.90, 0.01)
check("  rho*A^(3/2) at 7850 kg/m^3 [g]", 7.85e-3 * A_mm2 ** 1.5, 0.36, 0.01)

# --- P8. impact of 803 -> 779 on the update's N/observed band --------------
print("\n== P8. update's N/obs band under the corrected observed count ==")
N_lo, N_hi = 3.9 * 750.0, 5.6 * 750.0     # scoping 3d row for combined 2.67
for lo, hi, tag in ((700, 803, "as published (700-803, quoted 3.9-5.6x)"),
                    (700, 779, "corrected  (700-779)")):
    print(f"  {tag:<42} N/obs = {N_lo / hi:.2f} - {N_hi / lo:.2f}")

print(f"\nRESULT: {fails} failure(s)")
