---
name: ordnance-1944-B-is-isotropic
description: 1944 Ordnance B column is exactly N/(4*pi*r^2), so column identity is decisive for B(r) checks but immaterial for drag-decay checks
metadata:
  type: project
---

The 1944 Ordnance shell-fragment-damage tables print `B == N/(4*pi*r^2)` on
every row of all six tables — `B` is the *total* effective-fragment count
spread isotropically, not a measured local flux.

**Why:** two consequences that are easy to get backwards.

- Agreement with `B` validates only the **direction-averaged** density. A
    model with the right total count and a completely wrong side-spray belt
    scores identically on every row — never accept `B` agreement as support
    for angular/four-zone structure.
- The casualties-vs-perforation column choice is **decisive** for `B(r)`
    checks (58 ft-lb vs a range-dependent 248-1146 ft-lb criterion) but
    **immaterial** for drag-decay checks, where the criterion only selects
    which `(m,v)` point is tabulated and the decay law is criterion-free.
    Running the perforation column alongside casualties is an asset there.

**How to apply:** before flagging a `B_model` vs `B_card` comparison as
belt-vs-sphere mismatched, convert `B_model * 4*pi*r^2` and compare against an
independent total-count anchor — a belt-local reading is off by 4x+, which
settles it without reading `src/arty/`. Detail and the arithmetic:
`experiment/fragmentation-field/challenges/source-data-audit/review-criterion-match.md`
and its `checks/criterion-match-column-defs.py`. Related:
[[gap-closure-check-source-own-confidence]].
