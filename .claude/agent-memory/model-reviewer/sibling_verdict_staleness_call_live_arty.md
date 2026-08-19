---
name: sibling-verdict-staleness-call-live-arty
description: A challenge's published "shipped code" verdict can silently predate a sibling update's ship — reproduce it by calling live arty before quoting or building on it
metadata:
  type: feedback
---

Never take a sibling challenge's banner figures ("shipped code gives μ = …,
verdict FAIL at N×") as the current baseline. Call live `arty` and reproduce
them:

```
uv run python -c "import arty.fragmentation as F, arty.shells as S; print(F.mott_params(S.SHELLS['75mm M48 HE'], 864.4))"
```

**Why:** a verdict is computed at one moment and never re-runs. When a sibling
update ships a new constant (e.g. `MOTT_ASPECT_MOMENT_C` × `MOTT_BREADTH_VARIANCE_K`),
every challenge that quoted the old chain goes stale with no diff, no failing
test, and no marker. Found 2026-08-18: a published FAIL arm was the *pre-*
correction chain, off by ~13 %, and a new derivation printed both the stale and
the live row in one table without noticing they disagreed.

**How to apply:** whenever a derivation says "the challenge improves from X to
Y", verify X against live code, not against the challenge document. Detail:
`experiment/fragmentation-field/updates/kappa-x-shell-regime/review.md` Pass 1
finding B2. Related: [[cross-aspect-notebook-citation-staleness]].
